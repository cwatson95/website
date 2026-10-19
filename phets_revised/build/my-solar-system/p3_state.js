
/* ================================================================== *
 *  state, the two running systems, the per-view model and the readout *
 * ================================================================== */
const TABS = [['intro', 'two bodies'], ['lab', 'the lab'], ['exact', 'the exact orbit'],
              ['conserve', 'conservation']];
const COL = {pos: '#b8ec4c', ref: '#e8843a', live: '#cd35c4', struct: '#5ac8e0', dim: '#8b93a6',
             edge: '#242a3a', com: '#e8556d', path: '#7f88a0', warn: '#e8843a', phet: '#c9a7ff'};
const RO_W = 300;
const SPEEDS = [{id: 'slow', name: 'slow', f: 0.25}, {id: 'normal', name: 'normal', f: 1},
                {id: 'fast', name: 'fast', f: 1.75}];       /* PhET's timeSpeedMap: 1/4, 1, 7/4 */
const NBODIES = [{id: 1, name: '1'}, {id: 2, name: '2'}, {id: 3, name: '3'}, {id: 4, name: '4'}];
const VSCALE = 4.2;             /* px per km/s for the velocity arrow (printed on the canvas) */
const FSCALE = 60;              /* px for the gravity arrow at the reference pull, times 10^n */
/* the reference pull the 60 px stands for: PhET's own star and planet at their starting
   separation, G x 250 x 25 / 2^2 in these units */
const F_REF = G_MSS * 250 * 25 / 4;

const DEFAULTS = {
  view: 'intro', preset: 'sunPlanet', nb: 2,
  mass1: 250, mass2: 25, mass3: 0.1, mass4: 0.1,
  /* PhET's defaults: the path and the velocity arrows on, everything else off */
  com: false, speedLab: false, velocity: true, gravity: false, fpow: 0, path: true,
  grid: false, tape: false, values: false, shadow: true,
  running: false, speed: 'normal', zoom: PHET.ZOOM_DEF
};
const ST = Object.assign({}, DEFAULTS);
const SIM = {intro: null, lab: null, tape: {ax: 0, ay: 1, bx: 1, by: 1}, hist: [], shadow: null,
             shadowT: 0, base: null, order: null, ehist: [], exact: null, exactT0: 0};
const DRAGM = {what: null, i: -1};
const HIST_MAX = 1200;

/* the intro system is PhET's Intro screen (its two bodies); the lab system is whichever
   orbital system is chosen.  The analysis views ride along: "the exact orbit" reads the
   intro system, "conservation" reads the lab one. */
function sysKey(view){ return (view === 'lab' || view === 'conserve') ? 'lab' : 'intro'; }
function curSys(){ return SIM[sysKey(ST.view)]; }
function simReset(){
  SIM.intro = sysLoad('sunPlanet');
  SIM.lab = sysLoad(ST.preset, ST.nb);
  ST.nb = SIM.lab.S.n;                     /* a named system sets the count, not the other way */
  SIM.tape = {ax: 0, ay: 1, bx: 1, by: 1};
  histReset(); ehistReset();
  syncMasses();
}
function histReset(){
  const sys = SIM.lab;
  SIM.hist = [];
  SIM.base = sys ? {E: nbodyEnergy(sys.S, G_MSS), L: nbodyAngular(sys.S), p: nbodyMomentum(sys.S),
                    pscale: pScale(sys.S)} : null;
  SIM.shadow = sys ? nbodyCopy(sys.S) : null;
  SIM.shadowT = 0;
  SIM.order = null;
}
/* the exact-orbit view's record: the two-body solution is anchored at the state the intro
   system started from, so it is rebuilt whenever that start changes.  It is anchored at the
   START's own clock reading too (sys.t0): the centre-of-mass button saves a start mid-run. */
function ehistReset(){
  SIM.ehist = [];
  const sys = SIM.intro;
  SIM.exactT0 = sys ? sys.t0 : 0;
  SIM.exact = (sys && sys.S.n === 2)
    ? twoBodyReduce({n: 2, m: sys.start.map(b => b[0]), x: sys.start.map(b => b[1]), y: sys.start.map(b => b[2]),
                     vx: sys.start.map(b => b[3]), vy: sys.start.map(b => b[4])}, G_MSS)
    : null;
}
function exactAge(sys){ return sys.t - SIM.exactT0; }
function ehistSample(){
  const sys = SIM.intro, red = SIM.exact;
  if(!red || sys.S.n !== 2 || sys.merged.length) return;
  const e = twoBodyAt(red, exactAge(sys));
  const err = Math.max(Math.hypot(sys.S.x[0] - e.x1, sys.S.y[0] - e.y1),
                       Math.hypot(sys.S.x[1] - e.x2, sys.S.y[1] - e.y2));
  SIM.ehist.push({t: sys.t, err, rn: Math.hypot(sys.S.x[1] - sys.S.x[0], sys.S.y[1] - sys.S.y[0]),
                  re: Math.hypot(e.rel.x, e.rel.y)});
  if(SIM.ehist.length > HIST_MAX) SIM.ehist.shift();
}
function pScale(S){ let s = 0; for(let i = 0; i < S.n; i++) s += S.m[i] * Math.hypot(S.vx[i], S.vy[i]); return s || 1; }
/* the mass sliders mirror whichever system is on screen */
function syncMasses(){
  const sys = curSys(); if(!sys) return;
  for(let i = 0; i < 4; i++) ST['mass' + (i + 1)] = i < sys.S.n ? sys.S.m[i] : DEFAULTS['mass' + (i + 1)];
}
function setMass(i, m){
  const sys = curSys();
  if(!sys || i >= sys.S.n) return;
  sys.S.m[i] = m;
  ST.running = false;
  sys.t = 0; sysClearPaths(sys);
  sysSaveStart(sys);
  if(sysKey(ST.view) === 'lab'){ ST.preset = 'custom'; histReset(); } else ehistReset();
}
function speedFactor(){ const s = SPEEDS.find(s => s.id === ST.speed); return s ? s.f : 1; }
function frameDt(){ return PHET.FRAME * speedFactor(); }
/* PhET's zoom: levels 1..6 map to 25..125 view units per AU; here that sets the half-height
   of the world window, and the canvas prints the scale it ends up with */
function viewRadius(){
  const s = PHET.ZOOM_LO + (PHET.ZOOM_HI - PHET.ZOOM_LO) * (ST.zoom - PHET.ZOOM_MIN) / (PHET.ZOOM_MAX - PHET.ZOOM_MIN);
  return 309 / s;
}
function viewAnimates(v){ return true; }
/* one frame of the clock: the system, and (on the conservation view) PhET's own integrator
   running the same system beside it */
function runStep(){
  if(!ST.running) return false;
  const sys = curSys(), dt = frameDt();
  const r = sysStep(sys, dt, ST.path);
  if(sysKey(ST.view) === 'intro') ehistSample();
  if(sysKey(ST.view) === 'lab'){
    if(SIM.shadow && SIM.shadow.n === sys.S.n){ phetShadowStep(SIM.shadow, dt); SIM.shadowT += dt; }
    histSample();
  }
  return true;
}
function histSample(){
  const sys = SIM.lab, B = SIM.base;
  if(!B || sys.merged.length) return;                 /* a merge is not a drift: stop sampling */
  const E = nbodyEnergy(sys.S, G_MSS), L = nbodyAngular(sys.S), p = nbodyMomentum(sys.S);
  let K = 0;
  for(let i = 0; i < sys.S.n; i++) K += 0.5 * sys.S.m[i] * (sys.S.vx[i] * sys.S.vx[i] + sys.S.vy[i] * sys.S.vy[i]);
  const s = {t: sys.t, K, U: E - K, dE: Math.abs(E - B.E) / Math.abs(B.E),
             dL: Math.abs(L - B.L) / Math.max(1e-30, Math.abs(B.L)),
             dP: Math.hypot(p[0] - B.p[0], p[1] - B.p[1]) / B.pscale, dPhet: null};
  if(SIM.shadow && SIM.shadow.n === sys.S.n)
    s.dPhet = Math.abs(nbodyEnergy(SIM.shadow, G_MSS) - B.E) / Math.abs(B.E);
  SIM.hist.push(s);
  if(SIM.hist.length > HIST_MAX) SIM.hist.shift();
}
/* the order of the two integrators, measured on the system now on the bench: the error after
   a fixed time against a reference run, at four step counts.  Memoised per system. */
function orderSweep(sys){
  const key = [sys.S.n, sys.start.map(b => b.join(',')).join(';')].join('|');
  if(SIM.order && SIM.order.key === key) return SIM.order;
  const T = 0.4;
  const make = () => nbodyMake(sys.start.map(b => b[0]), sys.start.map(b => b[1]), sys.start.map(b => b[2]),
                               sys.start.map(b => b[3]), sys.start.map(b => b[4]));
  const run = (N, step) => { const S = make(), h = T / N; for(let k = 0; k < N; k++) step(S, G_MSS, h); return S; };
  const REFS = run(12800, pefrlStep);
  const Ns = [200, 400, 800, 1600], out = {key, N: Ns, pefrl: [], phet: []};
  for(const N of Ns){
    for(const [nm, step] of [['pefrl', pefrlStep], ['phet', phetStep]]){
      const S = run(N, step);
      let d = 0;
      for(let i = 0; i < S.n; i++) d = Math.max(d, Math.abs(S.x[i] - REFS.x[i]), Math.abs(S.y[i] - REFS.y[i]));
      out[nm].push(d);
    }
  }
  out.slope = nm => {
    const e = out[nm];
    let s = 0;
    for(let i = 0; i + 1 < e.length; i++) s += Math.log2(e[i] / e[i + 1]);
    return s / (e.length - 1);
  };
  SIM.order = out;
  return out;
}

/* ---- the model each view draws from ------------------------------------------------------ */
function bodyList(sys){
  const out = [];
  for(let i = 0; i < sys.S.n; i++) out.push({i, m: sys.S.m[i], x: sys.S.x[i], y: sys.S.y[i],
    vx: sys.S.vx[i], vy: sys.S.vy[i], r: massToRadius(sys.S.m[i]), col: BODY_COL[sys.col[i] % 4]});
  return out;
}
function forcesOn(sys){
  const S = sys.S, out = [];
  for(let i = 0; i < S.n; i++){
    let fx = 0, fy = 0;
    for(let j = 0; j < S.n; j++){
      if(j === i) continue;
      const dx = S.x[j] - S.x[i], dy = S.y[j] - S.y[i], r = Math.hypot(dx, dy);
      const f = G_MSS * S.m[i] * S.m[j] / (r * r * r);
      fx += f * dx; fy += f * dy;
    }
    out.push([fx, fy]);
  }
  return out;
}
function exactModel(sys){
  if(sys.S.n !== 2) return null;
  if(!SIM.exact) ehistReset();
  const red = SIM.exact;
  if(!red) return null;
  const now = twoBodyAt(red, exactAge(sys));
  const err = Math.max(Math.hypot(sys.S.x[0] - now.x1, sys.S.y[0] - now.y1),
                       Math.hypot(sys.S.x[1] - now.x2, sys.S.y[1] - now.y2));
  const el = red.el, pts1 = [], pts2 = [], rel = [];
  if(el.kind === 'ellipse'){
    for(let k = 0; k <= 240; k++){
      const s = twoBodyAt(red, el.T * k / 240);
      pts1.push([s.x1, s.y1]); pts2.push([s.x2, s.y2]); rel.push([s.rel.x, s.rel.y]);
    }
  } else {
    for(let k = -120; k <= 120; k++){
      const s = twoBodyAt(red, exactAge(sys) + k * 0.004);
      pts1.push([s.x1, s.y1]); pts2.push([s.x2, s.y2]); rel.push([s.rel.x, s.rel.y]);
    }
  }
  return {red, el, now, err, pts1, pts2, rel, com: red.com, mu: red.mu};
}
function conserveModel(sys){
  const B = SIM.base;
  if(!B) return null;
  const E = nbodyEnergy(sys.S, G_MSS), L = nbodyAngular(sys.S), p = nbodyMomentum(sys.S);
  let K = 0;
  for(let i = 0; i < sys.S.n; i++) K += 0.5 * sys.S.m[i] * (sys.S.vx[i] * sys.S.vx[i] + sys.S.vy[i] * sys.S.vy[i]);
  const sw = SIM.shadow && SIM.shadow.n === sys.S.n
    ? {E: nbodyEnergy(SIM.shadow, G_MSS), t: SIM.shadowT,
       dev: (() => { let d = 0; for(let i = 0; i < sys.S.n; i++)
         d = Math.max(d, Math.hypot(SIM.shadow.x[i] - sys.S.x[i], SIM.shadow.y[i] - sys.S.y[i])); return d; })()}
    : null;
  return {E, L, p, K, U: E - K, base: B, hist: SIM.hist, shadow: sw, order: orderSweep(sys),
          dE: Math.abs(E - B.E) / Math.abs(B.E), dL: Math.abs(L - B.L) / Math.max(1e-30, Math.abs(B.L)),
          dP: Math.hypot(p[0] - B.p[0], p[1] - B.p[1]) / B.pscale, merged: sys.merged.length};
}
function buildModel(){
  const st = ST, sys = curSys();
  const M = {view: st.view, st, sys, key: sysKey(st.view), bodies: bodyList(sys), t: sys.t,
             com: nbodyCom(sys.S), R: viewRadius(), E: nbodyEnergy(sys.S, G_MSS), L: nbodyAngular(sys.S),
             P: nbodyMomentum(sys.S), forces: forcesOn(sys), merged: sys.merged,
             preset: presetById(st.preset)};
  M.chaotic = sys.S.n > 2;
  if(st.view === 'exact') M.ex = exactModel(sys);
  if(st.view === 'conserve') M.cn = conserveModel(sys);
  if(sys.S.n === 2) M.two = twoBodyReduce(sys.S, G_MSS);
  return M;
}

/* ================================================================== *
 *  readout / equation bar / tag                                       *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">' + t + '</td></tr>'; }
function rrow(a, b, cls){ return '<tr><td>' + a + '</td><td class="v' + (cls ? ' ' + cls : '') + '">' + b + '</td></tr>'; }
function yrStr(t){ const y = yrOf(t); return Math.abs(y) < 1 ? fmt(y * 365.25, 1) + ' d' : fmt(y, 3) + ' yr'; }
function massStr(m){ return m < PHET.MASS_MIN ? '&le; ' + fmt(PHET.MASS_MIN, 1) : fmt(m, m < 10 ? 2 : 1); }
function readoutHTML(M){
  const st = ST, sys = M.sys;
  let s = '<div class="rname">My solar system<small>' + plain(TABS.find(t => t[0] === M.view)[1]) + '</small></div><table>';
  s += hd(M.key === 'lab' ? plain(M.preset.name) + ' — ' + sys.S.n + (sys.S.n === 1 ? ' body' : ' bodies') : 'PhET&rsquo;s two bodies')
     + rrow('t', yrStr(sys.t) + ' <span class="dim">(' + fmt(sys.t, 3) + ' model)</span>')
     + rrow('total mass', fmt(M.com.M, 1) + ' &times; 10&sup2;&#8312; kg')
     + rrow('centre of mass', '(' + fmt(M.com.x, 3) + ', ' + fmt(M.com.y, 3) + ') AU', Math.hypot(M.com.x, M.com.y) < 1 ? 'good' : '')
     + rrow('its velocity', fmt(Math.hypot(M.com.vx, M.com.vy), 4) + ' km/s', Math.hypot(M.com.vx, M.com.vy) < 0.01 ? 'good' : 'bad')
     + rrow('energy E = K + U', sigf(M.E, 6))
     + rrow('angular momentum L', sigf(M.L, 6));
  if(M.merged.length) s += rrow('collisions', M.merged.length + ' merge' + (M.merged.length > 1 ? 's' : ''), 'bad');
  if(st.values || M.view === 'lab'){
    s += hd('the bodies (mass 10&sup2;&#8312; kg, AU, km/s)');
    for(const b of M.bodies)
      s += rrow('<span style="color:' + b.col + '">body ' + (b.i + 1) + '</span>',
                massStr(b.m) + ' &nbsp; (' + fmt(b.x, 2) + ', ' + fmt(b.y, 2) + ') &nbsp; ('
                + fmt(b.vx, 1) + ', ' + fmt(b.vy, 1) + ')');
  }
  if(M.two){
    const el = M.two.el;
    s += hd('two bodies: the exact orbit')
       + rrow('&mu; = G(m&#8321;+m&#8322;)', sigf(M.two.mu, 6))
       + rrow('relative orbit', el.kind === 'ellipse' ? 'an ellipse' : 'a ' + el.kind, 'good')
       + rrow('a, e', el.kind === 'ellipse' ? sigf(el.a, 5) + ' AU, ' + fmt(el.e, 4) : '&mdash;, ' + fmt(el.e, 4))
       + (el.kind === 'ellipse' ? rrow('period T', fmt(el.T, 5) + ' model = ' + fmt(yrOf(el.T), 4) + ' yr', 'good') : '')
       + (el.kind === 'ellipse' ? rrow('periapsis, apoapsis', sigf(el.q, 4) + ', ' + sigf(el.Q, 4) + ' AU') : '');
  }
  if(M.view === 'exact' && M.ex){
    s += hd('numerical against exact')
       + rrow('|r<sub>num</sub> &minus; r<sub>Kepler</sub>|', M.ex.err === 0 ? '0' : M.ex.err.toExponential(2) + ' AU',
              M.ex.err < 1e-6 ? 'good' : 'bad')
       + rrow('after', yrStr(sys.t))
       + rrow('the centre of mass moves', fmt(Math.hypot(M.ex.com.vx, M.ex.com.vy), 4) + ' km/s, in a straight line');
  }
  if(M.view === 'conserve' && M.cn){
    const c = M.cn;
    s += hd('the constants of the motion')
       + rrow('|&Delta;E/E|', c.dE === 0 ? '0' : c.dE.toExponential(2), c.dE < 1e-6 ? 'good' : 'bad')
       + rrow('|&Delta;L/L|', c.dL === 0 ? '0' : c.dL.toExponential(2), c.dL < 1e-10 ? 'good' : 'bad')
       + rrow('|&Delta;p|/p', c.dP === 0 ? '0' : c.dP.toExponential(2), c.dP < 1e-10 ? 'good' : 'bad')
       + rrow('K, U', sigf(c.K, 5) + ', ' + sigf(c.U, 5));
    if(c.shadow) s += hd('PhET&rsquo;s own step, beside ours')
       + rrow('its |&Delta;E/E|', Math.abs(c.shadow.E - c.base.E) / Math.abs(c.base.E) === 0 ? '0'
              : (Math.abs(c.shadow.E - c.base.E) / Math.abs(c.base.E)).toExponential(2), 'bad')
       + rrow('the two runs differ by', c.shadow.dev.toExponential(2) + ' AU')
       + rrow('measured order', 'PEFRL ' + fmt(c.order.slope('pefrl'), 2) + ', PhET&rsquo;s ' + fmt(c.order.slope('phet'), 2), 'good');
  }
  s += hd('units (PhET&rsquo;s)')
     + rrow('1 model time unit', fmt(T_U_YR, 4) + ' yr')
     + rrow('G', fmt(G_MSS, 4) + ' AU(km/s)&sup2;/10&sup2;&#8312;kg')
     + rrow('CODATA G in the same units', fmt(G_SI_UNITS, 4) + ' (PhET is 0.11 % low)', 'bad')
     + rrow('so its &ldquo;km/s&rdquo; is', fmt(KMS_TRUE, 6) + ' true km/s');
  s += '</table><div class="note">' + (M.chaotic
    ? 'Three bodies and more are chaotic: this run is one possible history, and a different last digit gives another. '
    : 'Two bodies have a closed-form answer, and the exact-orbit view draws it. ')
    + 'Momentum and angular momentum are conserved to rounding by construction; the energy is not, and the '
    + 'conservation view measures the difference. Pinned in selfTest to build/my-solar-system/derive.py (scipy '
    + 'solve_ivp at rtol 1e-12).</div>';
  return s;
}
function eqbarHTML(M){
  const E = (eq, sm) => '<span class="lhs">' + eq + '</span><span class="sm">' + sm + '</span>';
  if(M.view === 'intro') return E('<span class="hl">m<sub>i</sub> r&Prime;<sub>i</sub> = &minus;G &sum;<sub>j&ne;i</sub> m<sub>i</sub>m<sub>j</sub> (r<sub>i</sub> &minus; r<sub>j</sub>)/|r<sub>i</sub> &minus; r<sub>j</sub>|&sup3;</span> &nbsp;&middot;&nbsp; G = 4.4567 AU(km/s)&sup2;/10&sup2;&#8312;kg <span class="rm">(PhET&rsquo;s)</span>',
    'one law, applied to every pair: drag a body or the tip of its velocity arrow and the whole future changes');
  if(M.view === 'lab') return E('<span class="hl">E = &sum; &frac12;m<sub>i</sub>v<sub>i</sub>&sup2; &minus; &sum;<sub>i&lt;j</sub> Gm<sub>i</sub>m<sub>j</sub>/r<sub>ij</sub></span> &nbsp;&middot;&nbsp; p = &sum; m<sub>i</sub>v<sub>i</sub> &nbsp;&middot;&nbsp; L = &sum; m<sub>i</sub>(x<sub>i</sub>v<sub>yi</sub> &minus; y<sub>i</sub>v<sub>xi</sub>)',
    'eleven systems built by PhET, one law behind all of them; with three bodies or more there is no closed-form answer and the motion is chaotic');
  if(M.view === 'exact') return E('<span class="hl">r = r&#8322; &minus; r&#8321; obeys r&Prime; = &minus;&mu;r/|r|&sup3;, &nbsp; &mu; = G(m&#8321;+m&#8322;)</span> &nbsp;&middot;&nbsp; r&#8321; = R &minus; (m&#8322;/M)r, &nbsp; r&#8322; = R + (m&#8321;/M)r, &nbsp; R = R&#8320; + V t',
    'two bodies reduce to one: the separation follows a Kepler conic about the total mass, and each body traces a similar conic about the centre of mass, which itself drifts in a straight line');
  return E('<span class="hl">PEFRL: drift &xi;h, kick (1&minus;2&lambda;)h/2, drift &chi;h, kick &lambda;h, drift (1&minus;2(&chi;+&xi;))h, &hellip;</span> &nbsp;&middot;&nbsp; error &prop; h&#8308; <span class="rm">(PhET&rsquo;s shipped step reuses one acceleration: &prop; h)</span>',
    'every kick is an equal and opposite pair, so momentum and angular momentum are exact; the energy is only nearly conserved, and how nearly is the order of the method');
}
function tagHTML(M){
  const nm = plain(TABS.find(t => t[0] === M.view)[1]);
  const sys = M.sys;
  let s = '<b>' + nm + '</b> — ' + (M.key === 'lab' ? plain(M.preset.name) : 'a star and a planet')
        + ', ' + sys.S.n + (sys.S.n === 1 ? ' body' : ' bodies') + ', t = ' + plain(yrStr(sys.t));
  if(M.merged.length) s += ' — ' + M.merged.length + ' merged';
  return s;
}
