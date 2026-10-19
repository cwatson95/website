
/* ================================================================== *
 *  state, the particle engine, and the model the views read           *
 * ================================================================== */
const TABS = [['nucleus', 'the nucleus'], ['foil', 'the foil'], ['pudding', 'plum pudding'],
              ['hyperbola', 'the hyperbola'], ['sigma', 'the cross section'],
              ['gold', 'gold, for real']];

const COL = {
  pos: '#b8ec4c',      /* green   — the thing this file computes        */
  ref: '#e8843a',      /* orange  — the closed form, PhET's own value   */
  live: '#cd35c4',     /* magenta — the alpha particle, the live marker */
  str: '#5ac8e0',      /* cyan    — nucleus, atom, axes, asymptotes     */
  dim: '#8b93a6', text: '#cfd4de', faint: '#6f7789', bg: '#070b18',
  proton: '#e8843a', neutron: '#6b7486', electron: '#5ac8e0', pudding: '#3b2d52',
};
const RO_W = 300;                       /* the floating readout's footprint */

const SCENES = [{id: 'nucleus', name: 'nuclear scale'}, {id: 'atom', name: 'atomic scale'}];

const DEFAULTS = {
  view: 'nucleus',
  sceneSel: 'nucleus',   /* PhET's own radio pair, mirrored onto the two tabs */
  energy: 80,            /* PhET's Energy slider: 50..100, used as the speed */
  protons: 79,
  neutrons: 118,
  traces: true,          /* PhET defaults this OFF; the traces are the point */
  gunOn: true,
  running: true,
  rate: 1,
  seed: 20260922,
  showClosed: true,      /* the analytic hyperbola over the live particles   */
  /* the hyperbola view */
  bModel: 20,
  nPaths: 9,
  showInt: true,
  showAsym: true,
  /* the cross-section view */
  nSample: 20000,
  bMax: 120,          /* wide enough that the 1/sin^4 law spans five decades */
  logY: true,
  showSample: true,
  showJac: true,
  /* real units — the plum-pudding and gold views */
  EMeV: 7.7,
  foilNm: 400,
  exagg: 1,
};
const ST = Object.assign({}, DEFAULTS);

/* one memo slot per expensive quantity; the sweep never touches most of them */
const MEMO = {};
function memo(name, key, fn){
  const e = MEMO[name];
  if(e && e.key === key) return e.val;
  const val = fn();
  MEMO[name] = {key: key, val: val};
  return val;
}

/* ------------------------------------------------------------------ *
 *  the scenes: PhET's own atom placements                             *
 *    RutherfordNucleusSpace  one atom at the origin, box = the bounds  *
 *    RutherfordAtomSpace     five atoms of width 30 at (-n/2, +n/2),   *
 *                            (+n/2, +n/2), (0, -n/2), (-n, -n/2),      *
 *                            (+n, -n/2) with n = bounds.width/2        *
 * ------------------------------------------------------------------ */
const HALF_BOX = PHET.boxW / 2;
function atomsFor(view){
  if(view === 'foil'){
    const n = HALF_BOX, s = n / 2;
    return [{x: -s, y: s, L: PHET.atomW}, {x: s, y: s, L: PHET.atomW},
            {x: 0, y: -s, L: PHET.atomW}, {x: -n, y: -s, L: PHET.atomW},
            {x: n, y: -s, L: PHET.atomW}];
  }
  if(view === 'nucleus') return [{x: 0, y: 0, L: PHET.boxW}];
  return [];                    /* PhET's plum-pudding space has NO atoms */
}
function liveView(v){ return v === 'nucleus' || v === 'foil' || v === 'pudding'; }

/* ------------------------------------------------------------------ *
 *  the engine                                                         *
 * ------------------------------------------------------------------ */
const RUN = {t: 0, ticks: 0, fired: 0, left: 0, sinceFire: 0, acc: 0, rng: null,
             ps: [], hist: null, maxTheta: 0, clamps: 0, view: null, key: ''};
const NHIST = 36;
const DT_TICK = 1 / 60;          /* PhET's own manualStep is 1/60 s        */
const TRAIL_MAX = 260;

function engineKey(st){
  return [st.view, st.energy, st.protons, st.seed, st.EMeV, st.exagg].join('|');
}
function engineReset(st){
  RUN.t = 0; RUN.ticks = 0; RUN.fired = 0; RUN.left = 0; RUN.sinceFire = 1e9; RUN.acc = 0;
  RUN.rng = mulberry32(st.seed | 0);
  RUN.ps = []; RUN.maxTheta = 0; RUN.clamps = 0;
  RUN.hist = new Float64Array(NHIST);
  RUN.view = st.view; RUN.key = engineKey(st);
}
engineReset(ST);

function newParticle(x, y, vx, vy){
  return {x: x, y: y, vx: vx, vy: vy, ai: -1, lastA: -1, b: 0, D: 0, phi: 0,
          ix: 1, iy: 0, jx: 0, jy: 1, vinf: 0, trail: [x, y], b0: 0, th0: 0,
          chi0: 0, hit: 0, rIn: 0, rOut: 0};
}
/* PhET's Gun fires one particle every bounds.width/energy/20 seconds at a
   uniformly random x, then pushes it AWAY from any atom whose centre it came
   within 4% of the bounds width of -- because the trajectory algorithm is
   singular at b = 0.  (PhET spends two random draws on the sign and the
   magnitude; one draw has the same distribution and is what this uses.) */
function gunFire(st, atoms){
  let x = (2 * RUN.rng() - 1) * HALF_BOX;
  const win = PHET.nudgeWindow * PHET.boxW;
  for(let i = 0; i < atoms.length; i++){
    const a = atoms[i];
    if(Math.abs(x - a.x) < win){
      const c = phetNudge(a.L);
      x = x > a.x ? x + c : x - c;
    }
  }
  const p = newParticle(x, -HALF_BOX, 0, st.energy);
  RUN.ps.push(p); RUN.fired++;
  return p;
}

/* the (i, j) frame of an atom for a particle moving along j: j is the
   direction of travel, i points at the side the particle is offset to */
function frameOf(p, a){
  const v = Math.hypot(p.vx, p.vy) || 1;
  const jx = p.vx / v, jy = p.vy / v;
  const nx = jy, ny = -jx;                    /* v rotated by -90 degrees */
  const rx = p.x - a.x, ry = p.y - a.y;
  return {jx: jx, jy: jy, nx: nx, ny: ny,
          X: rx * nx + ry * ny, Y: rx * jx + ry * jy, r: Math.hypot(rx, ry)};
}
function insideBox(f, L){ return Math.abs(f.X) <= L / 2 && Math.abs(f.Y) <= L / 2; }
/* once a particle is ON an orbit its velocity has turned, so the release test
   must use the frame the orbit was SET UP in, not a fresh one built from the
   current velocity: reading the box in the rotated frame let particles leave
   and re-enter the same atom on alternate ticks. */
function frameXY(p, a){
  const rx = p.x - a.x, ry = p.y - a.y;
  return {X: rx * p.ix + ry * p.iy, Y: rx * p.jx + ry * p.jy, r: Math.hypot(rx, ry)};
}

/* PhET's entry quadratic: the hyperbola with asymptotic speed s0 whose
   asymptote is parallel to the entry direction and which passes through the
   entry point has  b^2 - X0 b + (D/2)(Y0 + r0) = 0.  On the rotated SQUARE
   PhET uses, the discriminant is positive over the whole slider space; the
   clamp below is a guard, and the model counts how often it fires. */
function captureOrbit(p, a, ai, st){
  const f = frameOf(p, a);
  const X0 = Math.abs(f.X), sgn = f.X >= 0 ? 1 : -1;
  const D = phetD(a.L, st.protons, st.energy);
  let disc = X0 * X0 - 2 * D * (f.Y + f.r);
  if(!(disc > 0)){ disc = 0; RUN.clamps++; }
  const b = Math.max(1e-6, 0.5 * (X0 + Math.sqrt(disc)));
  p.ai = ai; p.b = b; p.D = D; p.vinf = st.energy;
  p.phi = Math.atan2(X0, -f.Y);
  p.ix = sgn * f.nx; p.iy = sgn * f.ny; p.jx = f.jx; p.jy = f.jy;
  if(p.b0 === 0){ p.b0 = b; p.th0 = thetaOfB(b, D); p.chi0 = velAngle(p.phi, b, D); p.rIn = f.r; }
  placeOnOrbit(p, a);
}
/* The velocity's angle from the incoming asymptote, at polar angle phi.
   Differentiating the conic, the b^2/den^2 factor cancels out of the ratio
   and everything collapses to
       dX/dphi : dY/dphi  =  (D/2)(1 - cos phi) : b - (D/2) sin phi,
   which has no singularity at phi = 0 (where the radius is infinite and the
   first version returned NaN) and no cancellation anywhere.  The versine is
   written as 2 sin^2(phi/2), which is the only form with any correct digits
   near phi = 0 (Known-bad, brachistochrone).  selfTest checks it against the
   brute-force derivative and against chi(phi_inf) = theta. */
function velAngle(phi, b, D){
  const s = Math.sin(phi / 2);
  return Math.atan2(D * s * s, b - 0.5 * D * Math.sin(phi));
}
function placeOnOrbit(p, a){
  const r = rOfPhi(p.phi, p.b, p.D);
  const X = r * Math.sin(p.phi), Y = -r * Math.cos(p.phi);
  p.x = a.x + p.ix * X + p.jx * Y;
  p.y = a.y + p.iy * X + p.jy * Y;
  const chi = velAngle(p.phi, p.b, p.D);
  const sp = p.vinf * Math.sqrt(Math.max(0, 1 - p.D / r));
  const cx = Math.sin(chi), cy = Math.cos(chi);
  p.vx = sp * (p.ix * cx + p.jx * cy);
  p.vy = sp * (p.iy * cx + p.jy * cy);
}
/* advance phi by RK4 on dphi/dt = v_inf b / r^2 -- angular momentum, which is
   the same number as PhET's arc-length form (asserted).  The substep count
   follows the angle swept and is CAPPED: a mutation sweep has no per-mutant
   timeout, so every loop here must terminate. */
function advanceOrbit(p, a, dt){
  const phiMax = phiInfOf(p.b, p.D) * (1 - 1e-9);
  const f = ph => {
    const r = rOfPhi(ph, p.b, p.D);
    return (r > 0 && isFinite(r)) ? p.vinf * p.b / (r * r) : 0;
  };
  const est = f(p.phi) * dt;
  const n = clamp(Math.ceil(Math.abs(est) / 0.02), 1, 64);
  const hh = dt / n;
  for(let i = 0; i < n; i++){
    const k1 = f(p.phi);
    const k2 = f(Math.min(phiMax, p.phi + 0.5 * hh * k1));
    const k3 = f(Math.min(phiMax, p.phi + 0.5 * hh * k2));
    const k4 = f(Math.min(phiMax, p.phi + hh * k3));
    p.phi += hh * (k1 + 2 * k2 + 2 * k3 + k4) / 6;
    if(p.phi >= phiMax){ p.phi = phiMax; break; }
  }
  placeOnOrbit(p, a);
}
/* Thomson's ball: the whole deflection happens as the particle crosses, and
   at the real D/R it is 1e-4 rad.  exagg multiplies it so the wiggle can be
   seen, and the factor is printed on the canvas. */
function puddingKick(p, st){
  const R = HALF_BOX;
  const b = Math.abs(p.x);
  if(b >= R) return;
  /* call the pinned closed form rather than writing theta(b) out a second
     time: the duplicate let a mutant drop the square root and survive a
     102-mutant sweep (Known-bad, the drum's group velocity three times).
     With D_model = (D/R) R the two are the same number by construction. */
  const Dm = realDoverR(st) * R;
  const th = thomsonTheta(b, Dm, R) * st.exagg;
  /* AWAY from the ball: a positive ball repels a positive alpha, so a
     particle crossing at +b leaves with a +x component.  The first version
     used the counter-clockwise rotation matrix and pushed both sides INWARD
     -- an attractive Thomson atom -- and no bound on the deflection SIZE
     could see it, because the size is the same either way. */
  const s = p.x >= 0 ? 1 : -1;
  const c = Math.cos(s * th), sn = Math.sin(s * th);
  const vx = p.vx * c + p.vy * sn, vy = -p.vx * sn + p.vy * c;
  p.vx = vx; p.vy = vy; p.hit = 1;
}
/* the real, dimensionless strength of a Thomson atom: D/R with D from the
   proton count and the alpha energy in MeV, R the gold metallic radius */
function realD(st){ return coulombD(2, st.protons, st.EMeV * MEV); }
function realDoverR(st){ return realD(st) / GOLD.rAtom; }

function stepOne(st, dt){
  const atoms = atomsFor(st.view);
  /* the gun */
  if(st.gunOn){
    RUN.sinceFire += dt;
    const per = phetGunPeriod(st.energy);
    let guard = 0;
    while(RUN.sinceFire >= per && RUN.ps.length < 160 && guard++ < 8){
      gunFire(st, atoms);
      RUN.sinceFire -= per;
    }
    if(RUN.sinceFire > per) RUN.sinceFire = per;
  }
  const keep = [];
  for(let k = 0; k < RUN.ps.length; k++){
    const p = RUN.ps[k];
    if(p.ai >= 0){
      const a = atoms[p.ai];
      advanceOrbit(p, a, dt);
      if(!insideBox(frameXY(p, a), a.L) || p.phi >= phiInfOf(p.b, p.D) * (1 - 1e-8)){
        p.lastA = p.ai; p.ai = -1;
        p.rOut = Math.hypot(p.x - a.x, p.y - a.y);
      }
    } else {
      const wasY = p.y;
      p.x += p.vx * dt; p.y += p.vy * dt;
      if(st.view === 'pudding' && wasY < 0 && p.y >= 0) puddingKick(p, st);
      for(let i = 0; i < atoms.length; i++){
        if(i === p.lastA) continue;
        if(insideBox(frameOf(p, atoms[i]), atoms[i].L)){ captureOrbit(p, atoms[i], i, st); break; }
      }
    }
    if(st.traces){
      const n = p.trail.length;
      if(n < 2 || Math.hypot(p.x - p.trail[n - 2], p.y - p.trail[n - 1]) > 1.2){
        p.trail.push(p.x, p.y);
        if(p.trail.length > 2 * TRAIL_MAX) p.trail.splice(0, 2);
      }
    }
    const M = HALF_BOX * 1.02;
    if(p.x < -M || p.x > M || p.y > M || p.y < -M * 1.2){
      const th = Math.abs(Math.atan2(p.vx, p.vy));
      RUN.maxTheta = Math.max(RUN.maxTheta, th);
      RUN.hist[clamp(Math.floor(th / PI * NHIST), 0, NHIST - 1)]++;
      RUN.left++;
    } else keep.push(p);
  }
  RUN.ps = keep;
  RUN.t += dt; RUN.ticks++;
}
/* The leftover has to ACCUMULATE.  Flooring dtWall/DT_TICK each frame throws
   it away, and a browser frame is 16.6 ms against a 16.67 ms tick, so the
   floor is zero on most frames and the sim crawls or stops outright. */
function engineAdvance(st, dtWall){
  if(RUN.key !== engineKey(st)) engineReset(st);
  RUN.acc = Math.min(0.2, RUN.acc + Math.max(0, dtWall) * st.rate);
  let n = 0;
  while(RUN.acc >= DT_TICK && n < 6){ stepOne(st, DT_TICK); RUN.acc -= DT_TICK; n++; }
  return n;
}
function engineStepOnce(st){
  if(RUN.key !== engineKey(st)) engineReset(st);
  stepOne(st, DT_TICK);
}

/* ------------------------------------------------------------------ *
 *  the analysis the views read                                        *
 * ------------------------------------------------------------------ */
/* the drawn turn of one hyperbola tracked only between radii r_in and r_out:
   the asymptote is reached only at infinity, so a tracked arc delivers
   theta - chi(in) - (theta - chi(out)) of it */
function drawnTurn(b, D, rIn, rOut){
  const p0 = phiAtRadius(rIn, b, D, false), p1 = phiAtRadius(rOut, b, D, true);
  return velAngle(p1, b, D) - velAngle(p0, b, D);
}
function beamSample(st){
  const D = phetD(PHET.boxW, st.protons, st.energy);
  const key = [st.nSample, st.bMax, D, st.seed].join('|');
  return memo('beam', key, () => {
    const th = sampleBeam(st.nSample | 0, st.bMax, D, st.seed | 0);
    const edges = [];
    const lo = Math.log(thetaOfB(st.bMax, D)), hi = Math.log(PI);
    for(let i = 0; i <= 14; i++) edges.push(Math.exp(lo + (hi - lo) * i / 14));
    edges[14] = PI;
    return {th: th, D: D, bins: binBeam(th, edges, st.bMax, D), edges: edges};
  });
}
function goldNumbers(st){
  const key = [st.protons, st.EMeV, st.foilNm].join('|');
  return memo('gold', key, () => {
    const E = st.EMeV * MEV;
    const D = coulombD(2, st.protons, E);
    const A = st.protons === GOLD.Z ? GOLD.A : Math.round(2.5 * st.protons);
    const Rn = nuclearRadius(A), Ra = nuclearRadius(4);
    const n = numberDensity(GOLD.rho, GOLD.molar);
    const t = st.foilNm * 1e-9, nt = n * t;
    const th2 = thomsonFoilTheta2(D, nt);
    return {
      E: E, D: D, a: D / 2, A: A, Rnuc: Rn, Ralpha: Ra, n: n, t: t, nt: nt,
      bt90: bOfTheta(PI / 2, D), rmin0: D, rminA: rminOfB(D / 2, D),
      Etouch: KE * 2 * st.protons * E_Q * E_Q / (Rn + Ra),
      spacing: Math.pow(n, -1 / 3), deep: t * Math.pow(n, 1 / 3),
      f90: nt * sigmaBeyond(PI / 2, D), f10: nt * sigmaBeyond(PI / 18, D),
      f150: nt * sigmaBeyond(150 * PI / 180, D),
      thMax: thomsonThetaMax(D, GOLD.rAtom), thRms1: D / (GOLD.rAtom * Math.sqrt(6)),
      th2: th2, thRms: Math.sqrt(th2),
      log10P: thomsonLog10P(PI / 2, th2),
      dsdo90: dsdoOf(PI / 2, D), dsdo10: dsdoOf(PI / 18, D),
      ratio: GOLD.rAtom / Rn,
    };
  });
}

/* A particle is picked up on the hyperbola whose ASYMPTOTE is parallel to
   its direction, not on the one tangent to it, so its own direction steps by
   chi(phi_in) at that moment -- PhET's algorithm does the same thing.  The
   step is largest for the particle fired at the edge of the beam, where b is
   largest; this returns that worst case so the canvas can print it instead of
   guessing at it. */
function pickupKink(L, D){
  const x0 = L / 2, y0 = -L / 2, r0 = Math.hypot(x0, y0);
  const disc = Math.max(0, x0 * x0 - 2 * D * (y0 + r0));
  const b = Math.max(1e-9, 0.5 * (x0 + Math.sqrt(disc)));
  return velAngle(Math.atan2(x0, -y0), b, D);
}
function buildModel(){
  const st = ST;
  const atoms = atomsFor(st.view);
  const L = st.view === 'foil' ? PHET.atomW : PHET.boxW;
  const D = phetD(L, st.protons, st.energy);
  const alpha = phetAlpha(L, st.protons);
  const bmin = Math.max(1e-9, phetNudge(L));
  const M = {
    view: st.view, st: st, atoms: atoms, L: L, D: D, alpha: alpha,
    Ddirect: phetDDirect(L, st.protons, st.energy),
    thMaxPhet: thetaOfB(bmin, D),
    bAt90: bOfTheta(PI / 2, D),
    speedStep: 1 - Math.sqrt(Math.max(0, 1 - D / (L / 2))),
    kinkMax: pickupKink(L, D),
    element: elementName(st.protons),
    nucleons: st.protons + st.neutrons,
    gunPeriod: phetGunPeriod(st.energy),
    inFlight: RUN.ps.length, fired: RUN.fired, left: RUN.left,
    t: RUN.t, maxTheta: RUN.maxTheta, clamps: RUN.clamps,
    /* the hyperbola view */
    bSel: st.bModel,
    thSel: thetaOfB(st.bModel, D),
    rminSel: rminOfB(st.bModel, D),
    eccSel: eccOfTheta(thetaOfB(st.bModel, D)),
    turnSel: drawnTurn(Math.max(1e-6, st.bModel), D, HALF_BOX, HALF_BOX),
    /* real units */
    gold: goldNumbers(st),
    DoverR: realDoverR(st),
  };
  M.thNumeric = dsdoNumeric(PI / 2, D);
  return M;
}

/* ------------------------------------------------------------------ *
 *  readout, equation bar, tag                                         *
 * ------------------------------------------------------------------ */
function hd(t){ return '<tr><td class="hd" colspan="2">' + t + '</td></tr>'; }
function row(a, b, cls){
  return '<tr><td>' + a + '</td><td class="v' + (cls ? ' ' + cls : '') + '">' + b + '</td></tr>';
}
function deg(x){ return fmt(x * 180 / PI, 2) + '&deg;'; }
function metres(x){ return sigf(x, 3) + ' m'; }

function readoutHTML(M){
  const st = M.st, G = M.gold;
  let h2 = '<div class="rname">' + TABS.filter(t => t[0] === M.view)[0][1]
    + '<small>' + (liveView(M.view) ? 'PhET&rsquo;s model units' : 'the closed form') + '</small></div><table>';
  if(M.view === 'nucleus' || M.view === 'foil'){
    h2 += hd('the atom');
    h2 += row('protons', fmt(st.protons, 0) + (M.element ? ' &middot; ' + M.element : ''));
    h2 += row('neutrons', fmt(st.neutrons, 0));
    h2 += row('nucleons drawn', fmt(M.nucleons, 0));
    h2 += hd('PhET&rsquo;s scaled model');
    h2 += row('gun energy (= speed)', fmt(st.energy, 0));
    h2 += row('D = 2&alpha;/v&sup2;', fmt(M.D, 3) + ' u');
    h2 += row('D / box', fmt(M.D / PHET.boxW, 4));
    h2 += row('&alpha; = 400 L (Z/79)', sigf(M.alpha, 4));
    h2 += row('b at 90&deg;', fmt(M.bAt90, 3) + ' u');
    h2 += row('largest &theta; the gun can give', deg(M.thMaxPhet));
    h2 += row('pick-up kink, worst case', deg(M.kinkMax));
    h2 += hd('the run');
    h2 += row('fired', fmt(M.fired, 0));
    h2 += row('in flight', fmt(M.inFlight, 0));
    h2 += row('left the frame', fmt(M.left, 0));
    h2 += row('biggest turn seen', deg(M.maxTheta), M.maxTheta > PI / 2 ? 'good' : '');
    h2 += row('one every', fmt(M.gunPeriod, 3) + ' s');
  } else if(M.view === 'pudding'){
    h2 += hd('Thomson&rsquo;s atom');
    h2 += row('Z', fmt(st.protons, 0) + (M.element ? ' &middot; ' + M.element : ''));
    h2 += row('alpha energy', fmt(st.EMeV, 2) + ' MeV');
    h2 += row('ball radius R', metres(GOLD.rAtom));
    h2 += row('D = k Z1 Z2 e&sup2;/E', metres(G.D));
    h2 += row('D / R', sigf(M.DoverR, 4));
    h2 += hd('what it can do');
    h2 += row('&theta;max = D/2R', sigf(G.thMax, 4) + ' rad');
    h2 += row('', deg(G.thMax));
    h2 += row('&theta;rms, one atom', sigf(G.thRms1, 4) + ' rad');
    h2 += row('free electron bound', sigf(electronMaxDeflection(), 4) + ' rad');
    h2 += hd('through ' + fmt(st.foilNm, 0) + ' nm of gold');
    h2 += row('atoms deep', fmt(G.deep, 0));
    h2 += row('&theta;rms', deg(G.thRms));
    h2 += row('P(&theta; &gt; 90&deg;)', '10' + supStr(Math.round(G.log10P)), 'bad');
    h2 += row('Rutherford gives', '1 in ' + sigf(1 / G.f90, 3), 'good');
    h2 += row('drawn &times;', fmt(st.exagg, 0));
  } else if(M.view === 'hyperbola'){
    h2 += hd('this trajectory');
    h2 += row('impact parameter b', fmt(M.bSel, 3) + ' u');
    h2 += row('b / (D/2)', fmt(M.bSel / (M.D / 2), 4));
    h2 += row('&theta; = 2 atan(D/2b)', deg(M.thSel));
    h2 += row('eccentricity 1/sin(&theta;/2)', fmt(M.eccSel, 4));
    h2 += row('r min', fmt(M.rminSel, 3) + ' u');
    h2 += row('r min / D', fmt(M.rminSel / M.D, 4));
    h2 += hd('what the box can show');
    h2 += row('turn inside the frame', deg(M.turnSel));
    h2 += row('lost to truncation', deg(M.thSel - M.turnSel));
    h2 += hd('conservation');
    const io = hyperCheck(M), bInt = hyperB(M);
    const thInt = thetaOfB(bInt, M.D);
    h2 += row('energy drift', sigf(io.dE, 2), io.dE < 1e-8 ? 'good' : 'bad');
    h2 += row('angular momentum drift', sigf(io.dL, 2), io.dL < 1e-8 ? 'good' : 'bad');
    h2 += row('RK4 &theta; &minus; closed form', sigf(Math.abs(io.theta - thInt), 2));
    h2 += row('residual &times; r&sup2;', fmt(Math.abs(io.theta - thInt) * io.rEnd * io.rEnd, 3));
    if(bInt !== M.bSel) h2 += row('overlay drawn at b', fmt(bInt, 3) + ' u', 'bad');
  } else if(M.view === 'sigma'){
    const B = beamSample(st);
    h2 += hd('the beam');
    h2 += row('particles', fmt(st.nSample, 0));
    h2 += row('b uniform on a disc', 'r &le; ' + fmt(st.bMax, 1) + ' u');
    h2 += row('D', fmt(B.D, 3) + ' u');
    h2 += row('smallest angle', deg(thetaOfB(st.bMax, B.D)));
    h2 += hd('sampled vs exact');
    for(const t0 of [10, 45, 90]){
      const th = t0 * PI / 180;
      if(th < thetaOfB(st.bMax, B.D)) continue;
      const f = fractionBeyond(B.th, th), ex = sigmaBeyond(th, B.D) / (PI * st.bMax * st.bMax);
      const sg = Math.sqrt(ex * (1 - ex) / st.nSample);
      h2 += row('beyond ' + t0 + '&deg;', sigf(f, 4));
      h2 += row('&nbsp;&nbsp;exact &middot; z', sigf(ex, 4) + ' &middot; ' + fmt((f - ex) / sg, 2),
        Math.abs((f - ex) / sg) < 3 ? 'good' : 'bad');
    }
    h2 += hd('the law');
    h2 += row('d&sigma;/d&Omega; at 90&deg;', sigf(dsdoOf(PI / 2, B.D), 4) + ' u&sup2;');
    h2 += row('from |db/d&theta;|', sigf(dsdoNumeric(PI / 2, B.D), 4) + ' u&sup2;');
    h2 += row('5&deg; : 90&deg;', sigf(dsdoOf(PI / 36, B.D) / dsdoOf(PI / 2, B.D), 4));
  } else {
    h2 += hd('alpha on ' + (M.element || 'Z = ' + st.protons));
    h2 += row('Z', fmt(st.protons, 0));
    h2 += row('energy', fmt(st.EMeV, 2) + ' MeV');
    h2 += row('D = k Z1 Z2 e&sup2;/E', fmt(G.D / FM, 3) + ' fm');
    h2 += row('a = D/2', fmt(G.a / FM, 3) + ' fm');
    h2 += row('b at 90&deg;', fmt(G.bt90 / FM, 3) + ' fm');
    h2 += hd('the nucleus');
    h2 += row('R = 1.2 A&#8531; fm', fmt(G.Rnuc / FM, 3) + ' fm');
    h2 += row('R(alpha)', fmt(G.Ralpha / FM, 3) + ' fm');
    h2 += row('r min, head-on', fmt(G.rmin0 / FM, 2) + ' fm',
      G.rmin0 > G.Rnuc + G.Ralpha ? 'good' : 'bad');
    h2 += row('touching energy', fmt(G.Etouch / MEV, 2) + ' MeV');
    h2 += hd(fmt(st.foilNm, 0) + ' nm of gold leaf');
    h2 += row('atoms deep', fmt(G.deep, 0));
    h2 += row('beyond 10&deg;', '1 in ' + sigf(1 / G.f10, 3));
    h2 += row('beyond 90&deg;', '1 in ' + sigf(1 / G.f90, 3));
    h2 += row('d&sigma;/d&Omega; at 90&deg;', fmt(G.dsdo90 / BARN, 3) + ' b/sr');
    h2 += hd('PhET&rsquo;s picture');
    h2 += row('atom : nucleus, real', sigf(G.ratio, 4));
    h2 += row('PhET&rsquo;s two captions', fmt(PHET.atomicScaleM / PHET.nuclearScaleM, 0));
    h2 += row('PhET&rsquo;s geometry', fmt(PHET.boxW / PHET.atomW, 2));
  }
  h2 += '</table>' + readoutNote(M);
  return h2;
}
function supStr(e){
  const d = '⁰¹²³⁴⁵⁶⁷⁸⁹';
  let s = (e < 0 ? '⁻' : ''); const a = Math.abs(e) + '';
  for(const ch of a) s += d[+ch];
  return s;
}
function readoutNote(M){
  const st = M.st;
  if(M.view === 'nucleus')
    return '<div class="note">Every curve is the exact hyperbola <b>r = b&sup2;/(b sin&phi; + (D/2)(cos&phi; &minus; 1))</b>. '
      + 'Only the timing along it is integrated. The neutron slider changes the drawn nucleus and <b>nothing else</b> '
      + '&mdash; PhET&rsquo;s model notes say so too.</div>';
  if(M.view === 'foil')
    return '<div class="note">PhET&rsquo;s atomic-scale scene. Each atom carries its own D = L/8 with L = 30, so the two '
      + 'scenes differ by <b>8.5&times;</b> in geometry and <b>4000&times;</b> in their captions. Outside an atom&rsquo;s '
      + 'box the potential is zero, so a particle drops ' + fmt(100 * M.speedStep, 1) + '% in speed on entering one.</div>';
  if(M.view === 'pudding')
    return '<div class="note">PhET&rsquo;s plum-pudding screen has <b>no atoms in its model at all</b>: the particles go '
      + 'straight through. They do here too at &times;1 &mdash; the real deflection is '
      + sigf(M.gold.thMax, 2) + ' rad, a fraction of a pixel. Turn the exaggeration up to see it.</div>';
  if(M.view === 'hyperbola')
    return '<div class="note">Green is an RK4 integration of <b>Newton&rsquo;s equations</b> started on the conic; '
      + 'orange is the closed form. They are two independent routes to the same curve, which is the only reason '
      + 'either can be believed.</div>';
  if(M.view === 'sigma')
    return '<div class="note">Three routes to one law: the closed form, the Jacobian (b/sin&theta;)|db/d&theta;|, and '
      + fmt(st.nSample, 0) + ' seeded particles binned in solid angle. The error bars are 1/&radic;N, not a fit.</div>';
  return '<div class="note">Gold is monoisotopic &mdash; <b>79 protons, 118 neutrons</b>, which is exactly what PhET opens '
    + 'with. Below the touching energy the alpha never reaches the nuclear surface and the 1/sin&#8308; law is exact.</div>';
}
/* The RK4 cross-check the hyperbola view prints and draws.  Below b = 0.02 D
   the orbit is a hairpin whose turning point is a near-cusp -- the transverse
   speed there is only v_inf b / r_min -- and no fixed-step integrator can
   cross it, so the overlay is drawn from b = max(b, 0.02 D) and the canvas
   says so.  At b = 0 exactly the motion is radial and has its OWN closed
   solution, r = (D/2)(cosh n + 1), t = (D/2)(sinh n + n), which is what
   selfTest asserts there instead.  0.02 D is 177.7 degrees: the difference is
   well under a pixel. */
const HYPER_B_FLOOR = 0.02;
function hyperB(M){ return Math.max(HYPER_B_FLOOR * M.D, M.bSel); }
function hyperCheck(M){
  const b = hyperB(M), D = M.D;
  return memo('hyper', [b, D].join('|'), () => integrateOrbit(b / D, 1, 12, 6000));
}
function eqbarHTML(M){
  const E = {
    nucleus: ['<span class="lhs">r(&phi;)</span> = b<sup>2</sup> / [ b sin&phi; + '
      + '<span class="hl">(D/2)</span>(cos&phi; &minus; 1) ]',
      'the exact Rutherford hyperbola. D is the head-on distance of closest approach; every particle on screen is on one of these.'],
    foil: ['tan(<span class="hl">&theta;</span>/2) = <span class="hl2">D</span> / 2b',
      'the deflection depends on one number, the impact parameter &mdash; and almost every particle has a big one.'],
    pudding: ['<span class="lhs">&theta;<sub>max</sub></span> = <span class="hl">D</span> / 2R'
      + ' &nbsp;&nbsp; &#8249;&theta;&sup2;&#8250; = D&sup2;/6R&sup2;',
      'a uniform ball of charge cannot turn an alpha by more than this, however you aim it.'],
    hyperbola: ['<span class="lhs">b</span> = (D/2) cot(&theta;/2) &nbsp;&nbsp; '
      + '<span class="lhs">r<sub>min</sub></span> = (D/2)[1 + <span class="hl">cosec</span>(&theta;/2)]',
      'the impact parameter, the scattering angle and the closest approach are one relation seen three ways.'],
    sigma: ['<span class="lhs">d&sigma;/d&Omega;</span> = (b/sin&theta;)|db/d&theta;| = '
      + '<span class="hl">(D/4)&sup2;</span> / sin<sup>4</sup>(&theta;/2)',
      'the cross section is a Jacobian: how much beam area lands in how much solid angle.'],
    gold: ['<span class="lhs">N(&gt;&theta;)/N</span> = n t &pi; b(&theta;)&sup2; = '
      + 'n t &pi; <span class="hl">(D/2)&sup2;</span> cot&sup2;(&theta;/2)',
      'the fraction of a beam turned past &theta; by a foil n t atoms per unit area thick.'],
  }[M.view];
  return E[0] + '<span class="sm">' + E[1] + '</span>';
}
function tagHTML(M){
  const st = M.st;
  if(M.view === 'nucleus')
    return '<b>' + fmt(st.protons, 0) + ' protons</b> &middot; gun energy ' + fmt(st.energy, 0)
      + ' &middot; D = ' + fmt(M.D, 2) + ' model units';
  if(M.view === 'foil')
    return '<b>five atoms</b> &middot; D = ' + fmt(M.D, 3) + ' in a box of ' + fmt(PHET.boxW, 0);
  if(M.view === 'pudding')
    return '<b>Thomson&rsquo;s atom</b> &middot; deflection drawn &times;' + fmt(st.exagg, 0)
      + ' &middot; true &theta;max = ' + sigf(M.gold.thMax, 2) + ' rad';
  if(M.view === 'hyperbola')
    return '<b>b = ' + fmt(M.bSel, 2) + '</b> &middot; &theta; = ' + deg(M.thSel)
      + ' &middot; e = ' + fmt(M.eccSel, 3);
  if(M.view === 'sigma')
    return '<b>' + fmt(st.nSample, 0) + ' particles</b> &middot; b &le; ' + fmt(st.bMax, 0)
      + ' &middot; seed ' + fmt(st.seed, 0);
  return '<b>alpha on ' + (M.element || ('Z = ' + st.protons)) + '</b> &middot; '
    + fmt(st.EMeV, 2) + ' MeV &middot; ' + fmt(st.foilNm, 0) + ' nm foil';
}
