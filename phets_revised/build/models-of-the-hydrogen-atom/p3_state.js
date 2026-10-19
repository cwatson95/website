
/* ================================================================== *
 *  state, the live atom (PhET's model, on a fixed 1/60 s tick),      *
 *  the per-view model, the readout, the equation bar, the tag        *
 * ================================================================== */
const TABS = [['box', 'the box'], ['levels', 'the levels'], ['wave', 'the standing wave'],
              ['orbitals', 'the orbitals'], ['series', 'the series'], ['rates', 'the rates']];
const COL = {
  pos: '#b8ec4c',      /* the exact quantum answer                       */
  ref: '#e8843a',      /* PhET's own model values / the measured line    */
  live: '#cd35c4',     /* the electron, the chosen wavelength            */
  struct: '#5ac8e0',   /* the box, the orbits, the axes                  */
  dim: '#8b93a6', edge: '#242a3a', text: '#aeb6c6',
  proton: '#e05c4a', electron: '#5ac8e0', uv: '#8a8fa0', ir: '#9a8272',
  pudding: '#b06be0', ball: '#c44e0e',
};
const RO_W = 300;                       /* the floating readout's footprint */

const MODEL_LIST = [
  {id: 'billiard', name: 'billiard ball', year: 1600},
  {id: 'pudding', name: 'plum pudding', year: 1904},
  {id: 'classical', name: 'solar system', year: 1911},
  {id: 'bohr', name: 'Bohr', year: 1913},
  {id: 'debroglie', name: 'de Broglie', year: 1924},
  {id: 'schrodinger', name: 'Schrödinger', year: 1926},
  {id: 'experiment', name: 'experiment', year: 0},
];
const MODEL_NAME = {};
for(const o of MODEL_LIST) MODEL_NAME[o.id] = plain(o.name);
const QUANTUM = {bohr: 1, debroglie: 1, schrodinger: 1, experiment: 1};
const LIGHT_LIST = [{id: 'white', name: 'white'}, {id: 'mono', name: 'monochromatic'}];
const DB_LIST = [{id: 'radial', name: 'radial distance'}, {id: 'height', name: '3-D height'},
                 {id: 'bright', name: 'brightness'}];
const SPEED_LIST = [{id: 'slow', name: 'slow'}, {id: 'normal', name: 'normal'}, {id: 'fast', name: 'fast'}];
const SERIES_LIST = [{id: 'all', name: 'all five'}, {id: '1', name: 'Lyman'}, {id: '2', name: 'Balmer'},
                     {id: '3', name: 'Paschen'}, {id: '4', name: 'Brackett'}, {id: '5', name: 'Pfund'}];

/* PhET opens with the light source OFF and the monochromatic knob at 380 nm,
   which is not a transition wavelength of hydrogen — nothing happens until you
   move it.  A default that makes the view show nothing is a defect (Known-bad),
   so this file opens on, at 122 nm, PhET's own rounded Lyman-alpha, and says
   what PhET's default is on the canvas. */
const DEFAULTS = {
  view: 'box', model: 'bohr', light: 'mono', lam: 122, lightOn: true,
  running: true, speed: 'normal', dbRep: 'radial',
  n: 3, l: 2, m: 0, showExact: true, showSpectro: true, showPhet: true,
  series: 'all', trials: 4000, seed: 20260921, fromN: 6, logCount: false, nu: 3,
};
const ST = Object.assign({}, DEFAULTS);

const MEMO = {};
function memo(name, key, fn){
  const m = MEMO[name];
  if(m && m.key === key) return m.val;
  const val = fn();
  MEMO[name] = {key, val};
  return val;
}

/* ---- the live atom ------------------------------------------------------
   PhET's probabilities are per ANIMATION FRAME.  This file fixes the frame at
   1/60 s — PhET's own rate on a 60 Hz display — so the run is deterministic
   and a seeded run is reproducible.  Everything else (the 300 units/s photon,
   the 0.0792 s between emissions, the 0.75 s and 1.0 s waits, the 0.5 emission
   chance, the 150 nm plum-pudding line) is PhET's value. */
const DT_TICK = 1 / 60;                 /* PhET's own frame on a 60 Hz display */
const HALF_BOX = PHET.boxSide / 2;
const ATOM = {};
function atomReset(st){
  ATOM.t = 0; ATOM.acc = 0; ATOM.tState = 0; ATOM.ticks = 0;
  ATOM.n = 1; ATOM.l = 0; ATOM.m = 0; ATOM.angle = 0;
  ATOM.photons = []; ATOM.photonAcc = 0;
  ATOM.counts = {}; ATOM.emitted = 0; ATOM.absorbed = 0; ATOM.bounced = 0; ATOM.fired = 0;
  ATOM.last = null; ATOM.metaT = 0; ATOM.squiggle = null;
  ATOM.cls = {r: PHET.classicalR0, a: 0, w: PHET.classicalOmega0 * DEG, dead: false};
  ATOM.pud = {held: 0, moving: false, cross: 0, prevAmp: 0, px: 0, py: 0,
              ex: 0, ey: 0, dir: 1};
  ATOM.rng = makeRng(st.seed | 0);
  puddingNewPerimeter();
  ATOM.key = atomKey(st);
}
/* only the model and the seed restart the run: moving the wavelength or
   switching the lamp mid-flight is what the sim is for, and a key that
   included them would reset the atom on every drag of the slider */
function atomKey(st){ return [st.model, st.seed].join('|'); }
function puddingNewPerimeter(){
  const th = ATOM.rng.angle();
  ATOM.pud.px = Math.abs(PHET.puddingR * Math.sin(th));
  ATOM.pud.py = ATOM.rng.sign() * PHET.puddingR * Math.cos(th);
  ATOM.pud.ex = 0; ATOM.pud.ey = 0;
  ATOM.pud.dir = ATOM.rng.next() < 0.5 ? -1 : 1;
}
/* the drawn orbit radius, in PhET's view units — PhET's compressed ladder */
function viewRadius(n){ return PHET.orbitR[n - 1]; }
/* the same ladder if it were the true n^2 — scaled so n=1 matches */
function trueViewRadius(n){ return PHET.orbitR[0] * n * n; }

function electronXY(st){
  if(st.model === 'classical') return [ATOM.cls.r * Math.cos(ATOM.cls.a), ATOM.cls.r * Math.sin(ATOM.cls.a)];
  if(st.model === 'pudding') return [ATOM.pud.ex, ATOM.pud.ey];
  const r = viewRadius(ATOM.n);
  return [r * Math.cos(ATOM.angle), r * Math.sin(ATOM.angle)];
}
/* de Broglie's standing wave: PhET's getAmplitude(n, angle) =
   sin(n*angle) * sin(electron angle) — a standing wave in angle whose height
   breathes with the electron's own rotation */
function dbAmplitude(n, ang){ return Math.sin(n * ang) * Math.sin(ATOM.angle); }

/* PhET's own rule for which way a spontaneously emitted photon goes: from
   n < 5 any direction at all, and from n >= 5 back along the electron's own
   direction to within a tenth of a turn.  Lifted out of trySpontaneous so the
   suite can assert it — a choice made inside a step function and never read
   back is invisible to every test (Known-bad). */
function emissionDirection(n, angle, rng){
  if(n < 5) return rng.angle();
  return angle + PI + 0.1 * rng.sign() * PI;
}
/* PhET adjustEmissionDirection: never within pi/8 of straight up, so an
   emitted photon is not mistaken for one from the source */
function adjustEmission(dir){
  const w = PI / 8, up = PI / 2;
  let d = dir - up;
  d = Math.atan2(Math.sin(d), Math.cos(d));
  if(Math.abs(d) < w) return up + (d < 0 ? -w : w);
  return dir;
}
function emitPhoton(st, lam, x, y, dir){
  ATOM.photons.push({x, y, dir, lam, emit: true, hit: false, age: 0});
  ATOM.counts[lam] = (ATOM.counts[lam] || 0) + 1;
  ATOM.emitted++;
}
function firePhoton(st){
  let lam = st.lam;
  if(st.light === 'white'){
    /* PhET: 40% of white photons are aimed at an n=1 absorption line */
    if(ATOM.rng.next() < PHET.whiteGroundFraction){
      const g = phetGroundAbsorptionLams();
      lam = g[ATOM.rng.int(g.length)];
    } else {
      lam = PHET.lamMin + ATOM.rng.int(PHET.lamMax - PHET.lamMin + 1);
    }
  }
  const x = -HALF_BOX + ATOM.rng.next() * PHET.boxSide;
  ATOM.photons.push({x, y: -HALF_BOX, dir: PI / 2, lam, emit: false, hit: false, age: 0});
  ATOM.fired++;
}
/* one 1/60 s tick of PhET's model */
function atomTick(st){
  const dt = DT_TICK;
  ATOM.t += dt; ATOM.ticks++;
  /* the light source */
  if(st.lightOn){
    ATOM.photonAcc += dt;
    while(ATOM.photonAcc >= PHET.dtPhoton){ ATOM.photonAcc -= PHET.dtPhoton; firePhoton(st); }
  }
  /* the atom */
  if(st.model === 'classical') classicalStep(dt);
  else if(st.model === 'pudding') puddingStep(st, dt);
  else if(QUANTUM[st.model]) quantumStep(st, dt);
  /* the photons */
  const keep = [];
  for(const p of ATOM.photons){
    p.x += Math.cos(p.dir) * PHET.photonSpeed * dt;
    p.y += Math.sin(p.dir) * PHET.photonSpeed * dt;
    p.age += dt;
    if(!p.emit && processPhoton(st, p)) continue;        /* absorbed */
    if(Math.abs(p.x) < HALF_BOX + 40 && Math.abs(p.y) < HALF_BOX + 40) keep.push(p);
  }
  ATOM.photons = keep;
  if(ATOM.squiggle) ATOM.squiggle.age += dt;
}
function classicalStep(dt){
  const c = ATOM.cls;
  if(c.dead) return;
  c.a -= c.w * dt;
  c.r -= PHET.classicalDrdt * dt;
  c.w *= PHET.classicalSpin;
  if(c.r <= PHET.classicalRmin){ c.r = 0; c.dead = true; }
}
/* PlumPuddingModel: the electron runs back and forth along a chord through the
   centre; its amplitude is the number of photons it is holding; after half an
   oscillation it has a 0.1 chance per step of re-emitting at 150 nm */
function puddingStep(st, dt){
  const P = ATOM.pud;
  if(P.held > 0){
    P.moving = true;
    puddingMove(dt, P.held);
    if(P.cross % 2 !== 0 && ATOM.rng.next() < PHET.puddingPEmit){
      P.held--;
      const dir = adjustEmission(ATOM.rng.angle());
      emitPhoton(st, PHET.puddingLam, P.ex, P.ey, dir);
      if(P.held === 0) P.prevAmp = 1;
    }
  } else if(P.moving){
    const before = P.cross % 2;
    puddingMove(dt, P.prevAmp);
    if(before !== P.cross % 2){
      P.moving = false; P.cross = 0; P.prevAmp = 0;
      puddingNewPerimeter();
    }
  }
}
function puddingMove(dt, amp){
  const P = ATOM.pud;
  const sx = -P.px, sy = -P.py, rx = P.px, ry = P.py;
  const d = dt * amp * (2 * PHET.puddingR);
  let dx = Math.abs(sx) * (d / PHET.puddingR), dy = Math.abs(sy) * (d / PHET.puddingR);
  const s = P.dir;
  dx *= s; dy *= s;
  if(sy > ry) dy *= -1;
  let nx = P.ex + dx, ny = P.ey + dy;
  if(Math.abs(nx) > Math.abs(sx) || Math.abs(ny) > Math.abs(sy)){
    if(P.dir > 0){ nx = rx; ny = ry; } else { nx = sx; ny = sy; }
    P.dir = -P.dir;
  }
  if((nx === 0 && ny === 0) || (nx > 0) !== (P.ex > 0) || (ny > 0) !== (P.ey > 0)) P.cross++;
  P.ex = nx; P.ey = ny;
}
function quantumStep(st, dt){
  ATOM.tState += dt;
  /* the electron goes round: PhET divides by n^2 for Bohr and Schrodinger and
     does NOT for de Broglie (a standing wave has no orbital period) */
  const w = PHET.bohrOmegaDeg * DEG;
  ATOM.angle -= dt * (st.model === 'debroglie' ? w : w / (ATOM.n * ATOM.n));
  ATOM.angle = ((ATOM.angle % TAU) + TAU) % TAU;
  if(ATOM.tState >= PHET.tAbsorb) trySpontaneous(st);
  /* PhET's metastable handler: in white light, a Schrodinger atom stuck in
     (2,0,0) is re-excited by a photon fired at it every 2 s */
  if(st.model === 'schrodinger' || st.model === 'experiment'){
    if(ATOM.n === 2 && ATOM.l === 0 && st.lightOn && st.light === 'white'){
      ATOM.metaT += dt;
      if(ATOM.metaT >= PHET.metastableWait){
        ATOM.metaT = 0;
        const abs = [];
        for(let b = 3; b <= NMAX; b++) abs.push(phetLam(2, b));
        const lam = abs[ATOM.rng.int(abs.length)];
        ATOM.photons.push({x: 0, y: -HALF_BOX, dir: PI / 2, lam, emit: false, hit: false, age: 0, meta: true});
      }
    } else ATOM.metaT = 0;
  }
}
function trySpontaneous(st){
  if(ATOM.n === NMAX + 99) return;
  if(ATOM.n === 1 || ATOM.tState < PHET.tEmit) return;
  const nl = chooseLowerN(st);
  if(nl === null) return;
  if(!(ATOM.rng.next() < PHET.pEmit)) return;
  const lam = phetLam(nl, ATOM.n);
  const [ex, ey] = electronXY(st);
  emitPhoton(st, lam, ex, ey, adjustEmission(emissionDirection(ATOM.n, ATOM.angle, ATOM.rng)));
  setStateFromDecay(st, nl);
}
function chooseLowerN(st){
  if(st.model === 'schrodinger' || st.model === 'experiment'){
    const d = phetLowerDist(ATOM.n, ATOM.l);
    if(!d.length) return null;
    return ATOM.rng.weighted(d);
  }
  return ATOM.n === 1 ? null : 1 + ATOM.rng.int(ATOM.n - 1);
}
function setStateFromDecay(st, nl){
  const from = {n: ATOM.n, l: ATOM.l, m: ATOM.m};
  if(st.model === 'schrodinger' || st.model === 'experiment') setNLM(st, nl);
  else { ATOM.n = nl; ATOM.l = 0; ATOM.m = 0; }
  ATOM.tState = 0;
  ATOM.last = {n1: Math.min(from.n, ATOM.n), n2: Math.max(from.n, ATOM.n), down: true,
               lam: phetLam(Math.min(from.n, ATOM.n), Math.max(from.n, ATOM.n))};
  ATOM.squiggle = {from, to: {n: ATOM.n, l: ATOM.l, m: ATOM.m}, lam: ATOM.last.lam, age: 0};
}
/* PhET SchrodingerQuantumNumbers.getNextState */
function setNLM(st, nNew){
  const l = ATOM.l, m = ATOM.m;
  const lp = ATOM.rng.weighted(phetChooseL(l, nNew));
  const mp = ATOM.rng.weighted(phetChooseM(m, lp));
  if(!phetTransitionAllowed(ATOM.n, l, m, nNew, lp, mp)){ ATOM.n = 1; ATOM.l = 0; ATOM.m = 0; return; }
  ATOM.n = nNew; ATOM.l = lp; ATOM.m = mp;
}
/* a photon meeting the atom */
function processPhoton(st, p){
  if(st.model === 'billiard'){
    if(!p.hit && Math.hypot(p.x, p.y) <= PHET.billiardR){
      const t = (p.x > 0 ? 1 : -1) * (PHET.bounceLo + ATOM.rng.next() * (PHET.bounceHi - PHET.bounceLo)) * DEG;
      p.dir += PI + t; p.hit = true; ATOM.bounced++;
    }
    return false;
  }
  if(st.model === 'classical') return false;
  if(st.model === 'pudding'){
    const P = ATOM.pud;
    const canAbsorb = !(P.held === 1 || (P.held === 0 && P.moving));
    const d = Math.hypot(p.x - P.ex, p.y - P.ey);
    if(canAbsorb && d <= PHET.photonRadius + PHET.electronRadius && ATOM.rng.next() < PHET.puddingPAbsorb){
      P.held++; ATOM.absorbed++; return true;
    }
    return false;
  }
  if(!QUANTUM[st.model]) return false;
  if(!quantumCollides(st, p)) return false;
  if(tryAbsorb(st, p)) return true;
  tryStimulated(st, p);
  return false;
}
function quantumCollides(st, p){
  const r = viewRadius(ATOM.n);
  if(st.model === 'bohr'){
    const [ex, ey] = electronXY(st);
    return Math.hypot(p.x - ex, p.y - ey) <= PHET.photonRadius + PHET.electronRadius;
  }
  if(st.model === 'debroglie'){
    if(st.dbRep === 'height'){
      const th = Math.atan2(p.y, p.x);
      const rx = r * Math.cos(th), ry = PHET.db3dYScale * r * Math.sin(th);
      return Math.hypot(p.x - rx, p.y - ry) <= PHET.photonRadius + 8;
    }
    return Math.abs(Math.hypot(p.x, p.y) - r) <= PHET.photonRadius + 8;
  }
  /* Schrodinger / experiment: PhET keeps de Broglie's ring test */
  return Math.abs(Math.hypot(p.x, p.y) - r) <= PHET.photonRadius + 8;
}
function tryAbsorb(st, p){
  if(p.emit || ATOM.n === NMAX || ATOM.tState < PHET.tAbsorb) return false;
  const nh = phetHigherState(ATOM.n, p.lam);
  if(nh === null) return false;
  const from = {n: ATOM.n, l: ATOM.l, m: ATOM.m};
  if(st.model === 'schrodinger' || st.model === 'experiment') setNLM(st, nh);
  else { ATOM.n = nh; ATOM.l = 0; ATOM.m = 0; }
  ATOM.tState = 0; ATOM.absorbed++;
  ATOM.last = {n1: Math.min(from.n, ATOM.n), n2: Math.max(from.n, ATOM.n), down: false, lam: p.lam};
  ATOM.squiggle = {from, to: {n: ATOM.n, l: ATOM.l, m: ATOM.m}, lam: p.lam, age: 0};
  return true;
}
function tryStimulated(st, p){
  if(p.emit || ATOM.tState < PHET.tEmit || ATOM.n === 1) return;
  const nl = phetLowerState(ATOM.n, p.lam);
  if(nl === null) return;
  if(st.model === 'schrodinger' || st.model === 'experiment'){
    /* PhET forbids a stimulated drop to n=1 unless l = 1 */
    if(nl >= ATOM.n || (nl === 1 && ATOM.l !== 1)) return;
  }
  emitPhoton(st, p.lam, p.x + PHET.photonRadius, p.y, p.dir);
  setStateFromDecay(st, nl);
}
function atomAdvance(st, dtSim){
  if(ATOM.key !== atomKey(st)) atomReset(st);
  ATOM.acc += dtSim;
  let n = 0;
  while(ATOM.acc >= DT_TICK * (1 - 1e-9) && n < 400){ ATOM.acc -= DT_TICK; atomTick(st); n++; }
  return n;
}
function atomStepOnce(st){
  if(ATOM.key !== atomKey(st)) atomReset(st);
  ATOM.acc = 0; atomTick(st); return 1;
}
function simFactor(st){ return PHET.speeds[st.speed]; }

/* ---- the cloud grid the orbitals view paints (cached per state) --------- */
function cloudGrid(n, l, m, G, rmax){
  const key = [n, l, m, G, rmax].join(',');
  return memo('cloud', key, () => {
    const g = new Float64Array(G * G);
    let mx = 0;
    for(let j = 0; j < G; j++){
      const z = rmax * (2 * (j + 0.5) / G - 1);
      for(let i = 0; i < G; i++){
        const x = rmax * (2 * (i + 0.5) / G - 1);
        const v = columnDensity(n, l, m, x, z, 72);
        g[j * G + i] = v;
        if(v > mx) mx = v;
      }
    }
    return {g, mx, G, rmax};
  });
}
/* the radius that holds 99 % of the probability — the box the cloud is drawn in */
function cloudExtent(n, l){
  const rm = meanR(n, l), step = rm / 60;
  let s = 0, r = 0;
  const tot = 1;
  while(r < 40 * n * n){
    const a = radialProb(n, l, r), b = radialProb(n, l, r + step);
    s += 0.5 * (a + b) * step;
    if(s > 0.99 * tot) break;
    r += step;
  }
  return r;
}

/* ---- the ensemble the rates view measures ------------------------------ */
function ensemble(st){
  const key = [st.model, st.seed, st.trials, st.fromN].join('|');
  return memo('ens', key, () => {
    const rng = makeRng(st.seed | 0);
    const cnt = {}, hist = {};
    let hops = 0, stuck = 0;
    const schro = (st.model === 'schrodinger' || st.model === 'experiment');
    for(let i = 0; i < st.trials; i++){
      const hs = schro ? cascadeSchrodinger(rng, st.fromN, Math.min(1, st.fromN - 1), 0)
                       : cascadeBohr(rng, st.fromN);
      for(const hp of hs){
        const k = hp[1] + '<-' + hp[0];
        cnt[k] = (cnt[k] || 0) + 1; hops++;
        hist[hp[1]] = (hist[hp[1]] || 0) + 1;
      }
      if(!hs.length || hs[hs.length - 1][1] !== 1) stuck++;
    }
    /* the first hop, against the distribution it was drawn from */
    const exact = schro ? phetLowerDist(st.fromN, Math.min(1, st.fromN - 1))
                        : Array.from({length: st.fromN - 1}, (_, i) => [i + 1, 1 / (st.fromN - 1)]);
    const first = {};
    const rng2 = makeRng((st.seed | 0) + 1);
    for(let i = 0; i < st.trials; i++){
      const v = schro ? rng2.weighted(exact) : 1 + rng2.int(st.fromN - 1);
      first[v] = (first[v] || 0) + 1;
    }
    const rows = exact.map(([k, p]) => {
      const f = (first[k] || 0) / st.trials;
      const se = Math.sqrt(p * (1 - p) / st.trials);
      return {n: k, p, f, z: se > 0 ? (f - p) / se : 0};
    });
    return {cnt, hops, stuck, rows, mean: hops / st.trials};
  });
}

/* ---- the per-view model ------------------------------------------------ */
function buildModel(){
  const st = ST;
  const M = {view: st.view, st, model: st.model, name: MODEL_NAME[st.model]};
  M.n = ATOM.n; M.l = ATOM.l; M.m = ATOM.m;
  M.tState = ATOM.tState; M.t = ATOM.t;
  M.E = energyEV(M.n); M.E1 = energyEV(1);
  M.rn = orbitRadius(M.n); M.vn = orbitSpeed(M.n);
  M.quantum = !!QUANTUM[st.model];
  M.lam = st.lam;
  M.lamBand = bandOf(st.lam);
  M.lamTrans = transitionForPhetLam(st.lam);
  M.counts = ATOM.counts; M.emitted = ATOM.emitted; M.absorbed = ATOM.absorbed;
  M.fired = ATOM.fired; M.bounced = ATOM.bounced;
  M.photons = ATOM.photons; M.last = ATOM.last; M.squiggle = ATOM.squiggle;
  M.dead = st.model === 'classical' && ATOM.cls.dead;
  M.clsR = ATOM.cls.r; M.clsW = ATOM.cls.w;
  M.held = ATOM.pud.held;
  M.metastable = (st.model === 'schrodinger' || st.model === 'experiment') && M.n === 2 && M.l === 0;
  /* the orbitals view has its own (n,l,m) */
  M.on = st.n; M.ol = Math.min(st.l, st.n - 1); M.om = clamp(st.m, -M.ol, M.ol);
  M.nodesR = radialNodes(M.on, M.ol); M.nodesA = angularNodes(M.ol, M.om);
  M.meanR = meanR(M.on, M.ol); M.meanR2 = meanR2(M.on, M.ol);
  M.lamDB = lamDeBroglie(M.n);
  M.tau = lifetimeNS(M.on, M.ol);
  M.A21 = einsteinA(2, 1, 1, 0);
  if(st.view === 'rates') M.ens = ensemble(st);
  return M;
}

/* ---- the readout ------------------------------------------------------- */
function hd(t){ return '<tr><td class="hd" colspan="2">' + t + '</td></tr>'; }
function row(a, b, cls){ return '<tr><td>' + a + '</td><td class="v' + (cls ? ' ' + cls : '') + '">' + b + '</td></tr>'; }
function readoutHTML(M){
  const st = M.st;
  let name = '', sub = '', body = '';
  if(M.view === 'box'){
    name = M.name; sub = 'the atom in the box';
    body += hd('the light');
    body += row('source', st.lightOn ? (st.light === 'white' ? 'white' : 'monochromatic') : 'off');
    body += row('&lambda;', st.light === 'white' ? '92&ndash;780 nm' : fmt(st.lam, 0) + ' nm');
    if(st.light === 'mono') body += row('band', M.lamBand, M.lamBand === 'visible' ? 'good' : '');
    if(st.light === 'mono') body += row('a transition?', M.lamTrans
      ? 'yes, ' + M.lamTrans.n1 + ' &rarr; ' + M.lamTrans.n2 : 'no', M.lamTrans ? 'good' : 'bad');
    body += row('fired', String(M.fired));
    body += hd('the atom');
    if(M.quantum){
      body += row('state', st.model === 'experiment' ? '?' : 'n = ' + M.n
        + ((st.model === 'schrodinger') ? ', l = ' + M.l + ', m = ' + M.m : ''));
      body += row('E<sub>n</sub> (exact)', fmt(M.E, 4) + ' eV');
      body += row('r<sub>n</sub> = n&sup2;a<sub>0</sub>', sigf(M.rn * 1e12, 4) + ' pm');
      body += row('time in state', fmt(M.tState, 2) + ' s');
      if(M.metastable) body += row('metastable', '(2,0,0)', 'bad');
    } else if(st.model === 'classical'){
      body += row('orbit radius', M.dead ? 'collapsed' : fmt(M.clsR, 1) + ' units', M.dead ? 'bad' : '');
      body += row('&omega;', sigf(M.clsW * RAD, 4) + ' &deg;/s');
      body += row('atom', M.dead ? 'destroyed' : 'alive', M.dead ? 'bad' : 'good');
    } else if(st.model === 'pudding'){
      body += row('photons held', String(M.held));
      body += row('emits at', PHET.puddingLam + ' nm (PhET)');
    } else {
      body += row('radius', PHET.billiardR + ' units (PhET)');
      body += row('photons bounced', String(M.bounced));
    }
    body += hd('the spectrometer');
    body += row('emitted', String(M.emitted));
    const ks = Object.keys(M.counts).map(Number).sort((a, b) => a - b);
    for(const k of ks.slice(0, 6)) body += row(k + ' nm (' + bandOf(k) + ')', String(M.counts[k]));
    if(ks.length > 6) body += row('&hellip; and ' + (ks.length - 6) + ' more', '');
    if(!ks.length) body += row('nothing yet', '&mdash;');
  } else if(M.view === 'levels'){
    name = M.name; sub = 'the electron energy levels';
    body += hd('where the electron is');
    body += row('state', st.model === 'experiment' ? '?' : 'n = ' + M.n
      + ((st.model === 'schrodinger') ? ', l = ' + M.l + ', m = ' + M.m : ''));
    body += row('E<sub>n</sub> (exact)', fmt(M.E, 5) + ' eV');
    body += row('E<sub>n</sub> (PhET, &minus;13.6/n&sup2;)', fmt(-PHET_RYD / (M.n * M.n), 5) + ' eV');
    body += row('to ionise', fmt(-M.E, 4) + ' eV');
    if(M.last){
      body += hd('the last transition');
      body += row('n', M.last.n2 + ' ' + (M.last.down ? '&rarr; ' : '&larr; ') + M.last.n1);
      body += row('&lambda; (PhET)', M.last.lam + ' nm');
      body += row('&lambda; (exact)', fmt(lamVac(M.last.n1, M.last.n2), 3) + ' nm');
      body += row('&Delta;E', fmt(Math.abs(energyEV(M.last.n2) - energyEV(M.last.n1)), 4) + ' eV');
    }
    body += hd('the ladder');
    body += row('E<sub>1</sub>', fmt(energyEV(1), 6) + ' eV');
    body += row('E<sub>6</sub>', fmt(energyEV(6), 6) + ' eV');
    body += row('PhET draws n = 2 at', fmt(PHET.levelY[1], 3) + ' of the axis');
    body += row('truth puts it at', fmt(1 - 1 / 4, 3), 'good');
  } else if(M.view === 'wave'){
    name = 'de Broglie'; sub = 'n&lambda; = 2&pi;r';
    body += hd('the orbit');
    body += row('n', String(M.n));
    body += row('r<sub>n</sub> = n&sup2;a<sub>0</sub>', sigf(M.rn * 1e12, 5) + ' pm');
    body += row('v<sub>n</sub> = &alpha;c/n', sigf(M.vn, 5) + ' m/s');
    body += row('&lambda;<sub>dB</sub> = h/m v', sigf(M.lamDB * 1e12, 5) + ' pm');
    body += hd('the closure');
    body += row('n&lambda;<sub>dB</sub>', sigf(M.n * M.lamDB * 1e12, 6) + ' pm');
    body += row('2&pi;r<sub>n</sub>', sigf(TAU * M.rn * 1e12, 6) + ' pm');
    body += row('ratio &minus; 1', (M.n * M.lamDB / (TAU * M.rn) - 1).toExponential(2), 'good');
    body += hd('what is drawn');
    body += row('representation', DB_LIST.filter(o => o.id === st.dbRep)[0].name);
    body += row('waves round the ring', String(M.n));
    body += row('PhET radius', viewRadius(M.n) + ' units');
    body += row('true n&sup2; radius', trueViewRadius(M.n) + ' units', 'good');
  } else if(M.view === 'orbitals'){
    name = 'n = ' + M.on + ', l = ' + M.ol + ', m = ' + M.om;
    sub = 'the orbital ' + M.on + 'spdfgh'.charAt(M.ol);
    body += hd('the wavefunction');
    body += row('radial nodes, n&minus;l&minus;1', String(M.nodesR));
    body += row('angular nodes, l&minus;|m|', String(M.nodesA));
    body += row('&lang;r&rang;', fmt(M.meanR, 3) + ' a<sub>0</sub>');
    body += row('&lang;r&sup2;&rang;', fmt(M.meanR2, 2) + ' a<sub>0</sub>&sup2;');
    body += row('&lang;1/r&rang;', fmt(meanInvR(M.on), 5) + ' /a<sub>0</sub>');
    body += row('&lang;r&rang; in pm', sigf(M.meanR * A0 * 1e12, 4) + ' pm');
    body += hd('the energy');
    body += row('E<sub>n</sub>', fmt(energyEV(M.on), 5) + ' eV');
    body += row('degeneracy n&sup2;', String(M.on * M.on));
    body += hd('how long it lives');
    body += row('&Gamma; = &Sigma;A', isFinite(M.tau) ? sigf(decayRate(M.on, M.ol), 4) + ' /s' : '0 (no allowed drop)');
    body += row('&tau;', isFinite(M.tau) ? fmt(M.tau, 3) + ' ns' : '&infin;', isFinite(M.tau) ? '' : 'bad');
  } else if(M.view === 'series'){
    name = 'the hydrogen spectrum'; sub = 'every line, in its own colour';
    body += hd('the series shown');
    body += row('series', SERIES_LIST.filter(o => o.id === st.series)[0].name);
    if(st.series !== 'all'){
      const n1 = +st.series;
      body += row('longest line', fmt(lamVac(n1, n1 + 1), 3) + ' nm');
      body += row('series limit', fmt(seriesLimit(n1), 3) + ' nm');
      body += row('limit energy', fmt(RH_EV / (n1 * n1), 4) + ' eV');
    }
    body += hd('the marker');
    body += row('&lambda;', fmt(st.lam, 0) + ' nm');
    body += row('band', M.lamBand);
    body += row('a transition?', M.lamTrans ? M.lamTrans.n2 + ' &rarr; ' + M.lamTrans.n1 : 'no',
      M.lamTrans ? 'good' : '');
    if(M.lamTrans) body += row('exact &lambda;', fmt(M.lamTrans.exact, 4) + ' nm', 'good');
    body += hd('against NIST');
    body += row('H-&alpha; measured (air)', '656.28518 nm');
    body += row('this model (air)', fmt(lamAir(2, 3), 5) + ' nm');
    body += row('residual', ((lamAir(2, 3) - 656.28518) / 656.28518).toExponential(2));
    body += row('&alpha;&sup2;/4', (ALPHA * ALPHA / 4).toExponential(2), 'good');
  } else {
    name = 'transition rates'; sub = 'PhET&rsquo;s table against Einstein&rsquo;s A';
    body += hd('real hydrogen');
    body += row('A(2p &rarr; 1s)', sigf(einsteinA(2, 1, 1, 0), 6) + ' /s');
    body += row('&tau;(2p)', fmt(lifetimeNS(2, 1), 4) + ' ns');
    body += row('&tau;(2s)', '&infin; (no allowed drop)', 'bad');
    body += row('&tau;(3d)', fmt(lifetimeNS(3, 2), 3) + ' ns');
    body += hd('PhET&rsquo;s table');
    body += row('weight n = 2 &rarr; 1', fmt(PHET_W[1][0], 2));
    body += row('2A(2p&rarr;1s)/10&#8312;', fmt(2 * einsteinA(2, 1, 1, 0) / 1e8, 4), 'good');
    body += hd('the seeded ensemble');
    body += row('cascades', String(st.trials));
    body += row('from n', String(st.fromN));
    body += row('hops', String(M.ens.hops));
    body += row('mean hops', fmt(M.ens.mean, 4));
    let worst = 0;
    for(const r of M.ens.rows) worst = Math.max(worst, Math.abs(r.z));
    body += row('worst |z|', fmt(worst, 2), worst < 3 ? 'good' : 'bad');
  }
  return '<div class="rname">' + name + '<small>' + sub + '</small></div><table>' + body + '</table>'
    + '<div class="note">' + readoutNote(M) + '</div>';
}
function readoutNote(M){
  if(M.view === 'box') return '<b>Green</b> is exact hydrogen, <b>orange</b> is PhET&rsquo;s own model value, '
    + '<b>magenta</b> is the electron. Photon speed, size and firing rate are PhET&rsquo;s and are nothing like real.';
  if(M.view === 'levels') return 'PhET compresses the ladder so that n = 2&hellip;6 are visible at all; the true '
    + '1 &minus; 1/n&sup2; spacing is drawn beside it in green.';
  if(M.view === 'wave') return 'The closure n&lambda; = 2&pi;r is an identity; the residual you see is how '
    + 'consistent CODATA&rsquo;s separately rounded a<sub>0</sub>, &alpha; and m<sub>e</sub> are.';
  if(M.view === 'orbitals') return 'The cloud is &int;|&psi;|&sup2; dy through the orbital &mdash; what a camera '
    + 'looking down y would record. Nodes are surfaces, not dots.';
  if(M.view === 'series') return 'Wavelengths are vacuum unless marked air. The residual against NIST is the '
    + 'relativistic correction this model leaves out, not an error in it.';
  return 'PhET&rsquo;s first column is twice the Einstein A for np &rarr; 1s; the rest of its table is its own.';
}

/* ---- the equation bar -------------------------------------------------- */
function eqbarHTML(M){
  if(M.view === 'box')
    return '<span class="lhs">E<sub>n<sub>2</sub></sub> &minus; E<sub>n<sub>1</sub></sub></span> = '
      + '<span class="hl">hc/&lambda;</span><span class="sm">a photon is absorbed only if its energy is exactly '
      + 'the gap between two levels &mdash; that is why one wavelength lights the atom up and its neighbour does nothing</span>';
  if(M.view === 'levels')
    return '<span class="lhs">E<sub>n</sub></span> = &minus;<span class="hl">R<sub>H</sub>hc</span>/n&sup2; = '
      + '&minus;<span class="hl2">13.598287</span> eV / n&sup2;<span class="sm">the whole ladder from one number; '
      + 'PhET uses 13.6 eV and 1240 eV nm and rounds every wavelength to the nearest nanometre</span>';
  if(M.view === 'wave')
    return '<span class="lhs">n&lambda;<sub>dB</sub></span> = <span class="hl">2&pi;r<sub>n</sub></span>, '
      + '&lambda;<sub>dB</sub> = h/m<sub>e</sub>v<span class="sm">the orbit is allowed when the electron&rsquo;s own '
      + 'wave closes on itself &mdash; a whole number of wavelengths round the ring</span>';
  if(M.view === 'orbitals')
    return '<span class="lhs">|&psi;<sub>n l m</sub>|&sup2;</span> = '
      + '<span class="hl">R<sub>n l</sub>(r)&sup2;</span> &middot; <span class="hl2">|Y<sub>l</sub><sup>m</sup>(&theta;,&phi;)|&sup2;</span>'
      + '<span class="sm">n &minus; l &minus; 1 radial nodes, l &minus; |m| angular nodes; the picture is that '
      + 'squared modulus integrated along the line of sight</span>';
  if(M.view === 'series')
    return '<span class="lhs">1/&lambda;</span> = <span class="hl">R<sub>H</sub></span>'
      + '(1/n<sub>1</sub>&sup2; &minus; 1/n<sub>2</sub>&sup2;)<span class="sm">Rydberg&rsquo;s formula, with the '
      + 'electron&ndash;proton reduced mass: R<sub>H</sub> = 10 967 758.34 m&#8315;&sup1;</span>';
  return '<span class="lhs">A<sub>ul</sub></span> = <span class="hl">(4/3)&alpha;&sup3;&omega;&sup3;</span> '
    + '&middot; l<sub>max</sub>/(2l<sub>u</sub>+1) &middot; |&lang;u|r|l&rang;|&sup2;'
    + '<span class="sm">the spontaneous emission rate of real hydrogen, in atomic units &mdash; what PhET&rsquo;s '
    + 'weight table is standing in for</span>';
}
function tagHTML(M){
  const st = M.st;
  if(M.view === 'box') return '<b>' + M.name + '</b> &middot; '
    + (st.lightOn ? (st.light === 'white' ? 'white light' : fmt(st.lam, 0) + ' nm') : 'light off')
    + ' &middot; t = ' + fmt(M.t, 2) + ' s';
  if(M.view === 'levels') return '<b>' + M.name + '</b> &middot; n = '
    + (st.model === 'experiment' ? '?' : M.n) + ' &middot; t = ' + fmt(M.t, 2) + ' s';
  if(M.view === 'wave') return '<b>de Broglie</b> &middot; n = ' + M.n + ' &middot; '
    + DB_LIST.filter(o => o.id === st.dbRep)[0].name;
  if(M.view === 'orbitals') return '<b>' + M.on + 'spdfgh'.charAt(M.ol) + '</b> &middot; (n,l,m) = ('
    + M.on + ',' + M.ol + ',' + M.om + ')';
  if(M.view === 'series') return '<b>the hydrogen spectrum</b> &middot; '
    + SERIES_LIST.filter(o => o.id === st.series)[0].name;
  return '<b>transition rates</b> &middot; ' + M.name + ' &middot; ' + st.trials + ' cascades from n = ' + st.fromN;
}
