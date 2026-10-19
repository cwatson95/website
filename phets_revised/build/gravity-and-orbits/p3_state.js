
/* ================================================================== *
 *  state, the two running screens, the per-view model and the readout *
 * ================================================================== */
const TABS = [['model', 'the model'], ['scale', 'to scale'], ['circ', 'the circular orbit'],
              ['exact', 'the exact orbit'], ['cons', 'what is conserved']];
const COL = {pos: '#b8ec4c', ref: '#e8843a', live: '#cd35c4', struct: '#5ac8e0', dim: '#8b93a6',
             edge: '#242a3a', com: '#e8556d', warn: '#e8843a', phet: '#c9a7ff'};
const RO_W = 300;
const SPEEDS = [{id: 0, name: 'slow'}, {id: 1, name: 'normal'}, {id: 2, name: 'fast'}];
const VEL_PX = 90;              /* px for the scene's reference speed; printed on the canvas */
const FSCALE = 60;              /* px for the gravity arrow at the reference pull, times 10^n */
const HIST_MAX = 1200;

const DEFAULTS = {
  view: 'model', screen: 'model', system: 'starPlanet',
  gravity: true, velocity: true, force: false, path: true, grid: false, tape: false,
  massOn: false, com: false, shadow: true,
  mass0: 1, mass1: 1, mass2: 1,       /* multiples of each body's own default mass */
  fpow: 0, running: false, speed: 1, zoom: 1, vfrac: 1
};
const ST = Object.assign({}, DEFAULTS);
const SIM = {model: null, scale: null, hist: [], ehist: [], order: null};
const DRAGM = {what: null, i: -1};

/* ---- a running screen -------------------------------------------------------------------- */
function sysMake(screen, sid){
  const cfg = sceneCfg(screen, sid);
  const S = goState(cfg);
  const sys = {cfg, S, screen, t: 0, paths: [], plen: [], start: null, base: null,
               ref: null, shadow: null, shadowT: 0,
               tape: null, coast: {dev: 0, dspeed: 0, travel: 1}};
  sysClearPaths(sys);
  sysSaveStart(sys);
  /* the measuring tape starts where PhET's does: a third of the way out from the centre,
     one grid step long (PhET's initialMeasuringTapePosition, in the same spirit) */
  const R = viewHalf(cfg, 1);
  sys.tape = {ax: -0.45 * R, ay: -0.62 * R, bx: -0.45 * R + cfg.grid, by: -0.62 * R};
  if(cfg.centre){ sys.tape.ax += cfg.centre[0]; sys.tape.bx += cfg.centre[0]; }
  return sys;
}
function sysClearPaths(sys){
  sys.paths = []; sys.plen = [];
  for(let i = 0; i < sys.S.n; i++){ sys.paths.push([]); sys.plen.push(0); }
}
function sysSaveStart(sys){
  const S = sys.S;
  sys.start = [];
  for(let i = 0; i < S.n; i++) sys.start.push([S.m[i], S.x[i], S.y[i], S.vx[i], S.vy[i]]);
  sys.t = 0;
  sys.ref = goTwoBody(S);
  sys.base = {E: nbodyEnergy(S, G_SI), L: nbodyAngular(S), p: nbodyMomentum(S), pscale: pScale(S)};
  sys.shadow = goCopy(S);
  sys.shadowT = 0;
  coastAnchor(sys);
  SIM.hist = []; SIM.ehist = []; SIM.order = null;
}
/* The straight-line measurement is taken from wherever gravity was switched OFF, not from
   t = 0.  Cutting gravity in mid-orbit and watching a planet leave along the tangent is the
   single most memorable thing PhET's switch does; rewinding the clock to the start would
   throw it away, and anchoring the residual at t = 0 would measure the orbit instead. */
function coastAnchor(sys){
  const S = sys.S;
  sys.anchor = {x0: Array.from({length: S.n}, (_, i) => S.x[i]),
                y0: Array.from({length: S.n}, (_, i) => S.y[i]),
                vx0: Array.from({length: S.n}, (_, i) => S.vx[i]),
                vy0: Array.from({length: S.n}, (_, i) => S.vy[i]),
                v0: Array.from({length: S.n}, (_, i) => Math.hypot(S.vx[i], S.vy[i])), t: sys.t};
  sys.coast = {dev: 0, dspeed: 0, travel: 1};
}
function sysRestart(sys){
  const S = sys.S;
  for(let i = 0; i < S.n; i++){
    S.m[i] = sys.start[i][0]; S.x[i] = sys.start[i][1]; S.y[i] = sys.start[i][2];
    S.vx[i] = sys.start[i][3]; S.vy[i] = sys.start[i][4];
  }
  sys.t = 0;
  sysClearPaths(sys);
  sysSaveStart(sys);
}
function pScale(S){ let s = 0; for(let i = 0; i < S.n; i++) s += S.m[i] * Math.hypot(S.vx[i], S.vy[i]); return s || 1; }
/* PhET keeps a bounded trail; here the cap is one grid step's worth of points per body */
function sysAddPath(sys){
  const S = sys.S, cap = 14 * sys.cfg.grid;
  for(let i = 0; i < S.n; i++){
    const p = sys.paths[i];
    if(p.length){
      const last = p[p.length - 1], d = Math.hypot(S.x[i] - last[0], S.y[i] - last[1]);
      if(d === 0) continue;
      p.push([S.x[i], S.y[i]]); sys.plen[i] += d;
      while(sys.plen[i] > cap || p.length > 4000){
        sys.plen[i] -= Math.hypot(p[1][0] - p[0][0], p[1][1] - p[0][1]); p.shift();
      }
    } else p.push([S.x[i], S.y[i]]);
  }
}
function curKey(){ return (ST.view === 'model' || ST.view === 'scale') ? ST.view : ST.screen; }
function curSys(){ return SIM[curKey()]; }
function simReset(){
  SIM.model = sysMake('model', ST.system);
  SIM.scale = sysMake('scale', ST.system);
  SIM.hist = []; SIM.ehist = []; SIM.order = null;
  syncMasses();
}
function loadSystem(sid){
  ST.system = sid;
  simReset();
  ST.running = false;
}
/* the mass sliders carry MULTIPLES of each body's own default (PhET's slider is half to
   double), so switching system keeps the panel meaningful */
function syncMasses(){
  const sys = curSys(); if(!sys) return;
  const base = sceneCfg(sys.screen, sys.cfg.id);
  for(let i = 0; i < 3; i++) ST['mass' + i] = i < sys.S.n ? sys.S.m[i] / base.bodies[i].m : 1;
}
function defaultMass(sys, i){ return sceneCfg(sys.screen, sys.cfg.id).bodies[i].m; }
function setMass(i, mult){
  const sys = curSys(), S = sys.S;
  if(!sys || i >= S.n) return;
  /* back to the start state first (PhET stops the clock and rewinds when a mass is set), then
     the new mass.  Setting it on the running state instead would leave the body mid-orbit with
     a different orbit, which is not what PhET does and is not what the readout would claim. */
  for(let k = 0; k < S.n; k++){
    S.m[k] = sys.start[k][0]; S.x[k] = sys.start[k][1]; S.y[k] = sys.start[k][2];
    S.vx[k] = sys.start[k][3]; S.vy[k] = sys.start[k][4];
  }
  S.m[i] = defaultMass(sys, i) * mult;
  ST.running = false;
  sys.t = 0;
  sysClearPaths(sys);
  sysSaveStart(sys);
}
function speedSteps(){ return PH.SPEED_STEPS[ST.speed]; }
function curFrameDt(sys){ return frameDt(sys.cfg, speedSteps()); }
function viewRadius(sys){ return viewHalf(sys.cfg, ST.zoom); }
/* PhET's gridCenter is also the centre of the view window: the origin for three systems, and
   the planet for Planet-and-Moon, whose pair sits 1 AU out from the sun's origin */
function viewCentre(sys){ return sys.cfg.centre || [0, 0]; }
/* the reference speed the velocity arrow is scaled by: the fastest body's speed relative to
   the first one at the START of the run (so the arrow scale does not change as it runs) */
function vRef(sys){
  let v = 0;
  for(let i = 1; i < sys.S.n; i++)
    v = Math.max(v, Math.hypot(sys.start[i][3] - sys.start[0][3], sys.start[i][4] - sys.start[0][4]));
  return v || 1;
}
function velScale(sys){ return VEL_PX / vRef(sys); }        /* px per m/s */
/* the reference pull the 60 px stands for: the first pair at their starting separation */
function fRef(sys){
  const s = sys.start, r = Math.hypot(s[1][1] - s[0][1], s[1][2] - s[0][2]);
  return G_SI * s[0][0] * s[1][0] / (r * r);
}

/* ---- one frame ---------------------------------------------------------------------------- */
function runStep(){
  if(!ST.running) return false;
  const sys = curSys(), dt = curFrameDt(sys);
  goAdvance(sys.S, dt, ST.gravity);
  sys.t += dt;
  if(ST.path) sysAddPath(sys);
  if(ST.gravity && ST.shadow && sys.shadow.n === sys.S.n){
    goAdvance(sys.shadow, dt, true, goPhetStep); sys.shadowT += dt;
  }
  if(!ST.gravity) coastSample(sys);
  histSample(sys);
  if(sys.ref) ehistSample(sys);
  return true;
}
/* gravity off: the residual perpendicular to the starting velocity (a straight line has none)
   and the change in speed (a drift changes none).  Both are measured, not assumed. */
function coastSample(sys){
  const S = sys.S, B = sys.anchor;
  let dev = 0, dsp = 0, travel = 1;
  for(let i = 0; i < S.n; i++){
    if(S.fix[i] || B.v0[i] === 0) continue;
    const ux = B.vx0[i] / B.v0[i], uy = B.vy0[i] / B.v0[i];
    const dx = S.x[i] - B.x0[i], dy = S.y[i] - B.y0[i];
    dev = Math.max(dev, Math.abs(dx * uy - dy * ux));
    travel = Math.max(travel, Math.hypot(dx, dy));
    dsp = Math.max(dsp, Math.abs(Math.hypot(S.vx[i], S.vy[i]) - B.v0[i]));
  }
  sys.coast = {dev, dspeed: dsp, travel};
}
function histSample(sys){
  const S = sys.S, B = sys.base;
  const E = nbodyEnergy(S, G_SI), L = nbodyAngular(S), p = nbodyMomentum(S);
  let K = 0;
  for(let i = 0; i < S.n; i++) K += 0.5 * S.m[i] * (S.vx[i] * S.vx[i] + S.vy[i] * S.vy[i]);
  const s = {t: sys.t, K, U: E - K,
             dE: Math.abs(E - B.E) / Math.abs(B.E),
             dL: Math.abs(L - B.L) / Math.max(1e-300, Math.abs(B.L)),
             dP: Math.hypot(p[0] - B.p[0], p[1] - B.p[1]) / B.pscale, dPhet: null};
  if(ST.gravity && ST.shadow && sys.shadow.n === S.n)
    s.dPhet = Math.abs(nbodyEnergy(sys.shadow, G_SI) - B.E) / Math.abs(B.E);
  SIM.hist.push(s);
  if(SIM.hist.length > HIST_MAX) SIM.hist.shift();
}
function ehistSample(sys){
  if(!ST.gravity) return;
  const e = goTwoBodyAt(sys.ref, sys.t), S = sys.S;
  const err = Math.max(Math.hypot(S.x[0] - e.x1, S.y[0] - e.y1),
                       Math.hypot(S.x[1] - e.x2, S.y[1] - e.y2));
  SIM.ehist.push({t: sys.t, err,
                  rn: Math.hypot(S.x[1] - S.x[0], S.y[1] - S.y[0]),
                  re: Math.hypot(e.x2 - e.x1, e.y2 - e.y1)});
  if(SIM.ehist.length > HIST_MAX) SIM.ehist.shift();
}
/* The time the order sweep runs over: a ninth of the CLOSEST pair's reference period, so that
   the coarsest step is a small fraction of an orbit on every system.  A fixed 40 days is more
   than a whole (boosted) lunar orbit on the Model screen, where PhET's first-order step then
   saturates at the size of the system and the measured "order" collapses to 0.58 -- a number
   about the saturation, not about the method.  For PhET's Sun and Planet this rule gives
   40.6 days, which is the 40 days derive.py measures at. */
function orderTime(S){
  let T = Infinity;
  for(let i = 0; i < S.n; i++) for(let j = i + 1; j < S.n; j++){
    const r = Math.hypot(S.x[j] - S.x[i], S.y[j] - S.y[i]);
    const boosted = S.boost !== 1 && ((S.kind[i] === 'moon' && S.kind[j] === 'planet') ||
                                      (S.kind[j] === 'moon' && S.kind[i] === 'planet'));
    const k = boosted ? S.boost : 1;
    T = Math.min(T, TAU * Math.sqrt(r * r * r / (k * G_SI * (S.m[i] + S.m[j]))));
  }
  return T / 9;
}
/* the order of the two integrators on the system now on the bench.  The step counts stay
   COARSE on purpose: positions are ~1e11 m, so one ulp is 3e-5 m and a fine run random-walks
   into that floor -- at 1600 steps over 40 days PEFRL's truncation error IS the roundoff and
   the measured ratio falls to 1.2 on correct code (derive.py measures exactly that). */
function orderSweep(sys){
  const key = sys.screen + '/' + sys.cfg.id + '/' + sys.start.map(b => b.join(',')).join(';');
  if(SIM.order && SIM.order.key === key) return SIM.order;
  const T = orderTime(sys.S);
  const make = () => {
    const S = goCopy(sys.S);
    for(let i = 0; i < S.n; i++){
      S.m[i] = sys.start[i][0]; S.x[i] = sys.start[i][1]; S.y[i] = sys.start[i][2];
      S.vx[i] = sys.start[i][3]; S.vy[i] = sys.start[i][4];
    }
    return S;
  };
  const run = (N, step) => { const S = make(), h = T / N; for(let k = 0; k < N; k++) step(S, h); return S; };
  const REFS = run(25600, goPefrl);
  const Ns = [20, 40, 80, 160], out = {key, N: Ns, T, pefrl: [], phet: []};
  for(const N of Ns) for(const [nm, step] of [['pefrl', goPefrl], ['phet', goPhetStep]]){
    const S = run(N, step);
    let d = 0;
    for(let i = 0; i < S.n; i++) d = Math.max(d, Math.abs(S.x[i] - REFS.x[i]), Math.abs(S.y[i] - REFS.y[i]));
    out[nm].push(d);
  }
  out.slope = nm => {
    const e = out[nm]; let s = 0;
    for(let i = 0; i + 1 < e.length; i++) s += Math.log2(e[i] / e[i + 1]);
    return s / (e.length - 1);
  };
  SIM.order = out;
  return out;
}

/* ---- the model each view draws from ------------------------------------------------------- */
function bodyList(sys){
  const S = sys.S, out = [];
  for(let i = 0; i < S.n; i++) out.push({i, name: S.name[i], kind: S.kind[i], m: S.m[i], r: S.r[i],
    x: S.x[i], y: S.y[i], vx: S.vx[i], vy: S.vy[i], fixed: !!S.fix[i],
    col: BODY_COL[S.kind[i]], rot: goRotation(S, i, sys.t)});
  return out;
}
function forcesOn(sys){
  const S = sys.S, out = [];
  goAccel(S);
  for(let i = 0; i < S.n; i++) out.push([S.ax[i] * S.m[i], S.ay[i] * S.m[i]]);
  return out;
}
/* view 3: the conic a start speed of f x the circular speed makes, at the system's own radius */
function circModel(sys){
  const s = sys.start;
  const M = s[0][0], r = Math.hypot(s[1][1] - s[0][1], s[1][2] - s[0][2]);
  const vc = circSpeed(M, r), vesc = Math.SQRT2 * vc, mu = G_SI * M;
  const v = ST.vfrac * vc;
  const el = conicFromState(r, 0, 0, v, mu);
  /* the four real orbits, on the two analysis panels */
  const marks = [
    {name: 'Earth about the Sun', short: 'Earth', M: PH.SUN_MASS, r: PH.EARTH_X, col: COL.struct},
    {name: 'the Moon about the Earth', short: 'Moon', M: PH.EARTH_MASS, r: PH.MOON_Y, col: COL.live},
    {name: 'the station about the Earth', short: 'station', M: PH.EARTH_MASS, r: PH.STATION_X, col: COL.pos}
  ];
  for(const k of marks){ k.vc = circSpeed(k.M, k.r); k.T = circPeriod(k.M, k.r); }
  /* an orbit whose periapsis is inside the central body is not an orbit at all */
  const rTrue = sceneCfg('scale', sys.cfg.id).bodies[0].r;
  return {M, r, vc, vesc, mu, v, el, marks, rTrue, hits: el.q < rTrue,
          start: Math.hypot(s[1][3] - s[0][3], s[1][4] - s[0][4])};
}
function exactModel(sys){
  if(!sys.ref) return null;
  const now = goTwoBodyAt(sys.ref, sys.t), S = sys.S;
  const err = Math.max(Math.hypot(S.x[0] - now.x1, S.y[0] - now.y1),
                       Math.hypot(S.x[1] - now.x2, S.y[1] - now.y2));
  const el = sys.ref.el, pts1 = [], pts2 = [];
  if(el.kind === 'ellipse'){
    for(let k = 0; k <= 260; k++){
      const p = goTwoBodyAt(sys.ref, el.T * k / 260);
      pts1.push([p.x1, p.y1]); pts2.push([p.x2, p.y2]);
    }
  } else {
    const span = 400 * curFrameDt(sys);
    for(let k = -130; k <= 130; k++){
      const p = goTwoBodyAt(sys.ref, sys.t + k * span / 130);
      pts1.push([p.x1, p.y1]); pts2.push([p.x2, p.y2]);
    }
  }
  return {ref: sys.ref, el, now, err, pts1, pts2, hist: SIM.ehist};
}
function consModel(sys){
  const S = sys.S, B = sys.base;
  const E = nbodyEnergy(S, G_SI), L = nbodyAngular(S), p = nbodyMomentum(S);
  let K = 0;
  for(let i = 0; i < S.n; i++) K += 0.5 * S.m[i] * (S.vx[i] * S.vx[i] + S.vy[i] * S.vy[i]);
  const sw = (ST.gravity && ST.shadow && sys.shadow.n === S.n) ? {
    E: nbodyEnergy(sys.shadow, G_SI), t: sys.shadowT,
    dev: (() => { let d = 0; for(let i = 0; i < S.n; i++)
      d = Math.max(d, Math.hypot(sys.shadow.x[i] - S.x[i], sys.shadow.y[i] - S.y[i])); return d; })()
  } : null;
  return {E, K, U: E - K, L, p, base: B, hist: SIM.hist, shadow: sw, order: orderSweep(sys),
          coast: sys.coast,
          dE: Math.abs(E - B.E) / Math.abs(B.E),
          dL: Math.abs(L - B.L) / Math.max(1e-300, Math.abs(B.L)),
          dP: Math.hypot(p[0] - B.p[0], p[1] - B.p[1]) / B.pscale,
          broken: brokenBy(sys)};
}
/* what the Model screen breaks, named so the conservation view can say which is which */
function brokenBy(sys){
  const out = [];
  for(let i = 0; i < sys.S.n; i++) if(sys.S.fix[i]) out.push(sys.S.name[i] + ' is nailed down');
  if(sys.S.boost !== 1) out.push('the moon feels ' + fmt(sys.S.boost, 0) + '&times; the planet&rsquo;s pull, one-sidedly');
  return out;
}
function buildModel(){
  const sys = curSys(), S = sys.S;
  const M = {view: ST.view, st: ST, sys, key: curKey(), cfg: sys.cfg, bodies: bodyList(sys),
             t: sys.t, R: viewRadius(sys), centre: viewCentre(sys), com: nbodyCom(S), forces: forcesOn(sys),
             E: nbodyEnergy(S, G_SI), L: nbodyAngular(S), P: nbodyMomentum(S),
             vscale: velScale(sys), fref: fRef(sys), ref: sys.ref,
             sep: Math.hypot(S.x[1] - S.x[0], S.y[1] - S.y[0]),
             sysName: systemById(sys.cfg.id).name, screenName: sys.screen === 'model' ? 'Model' : 'To Scale',
             broken: brokenBy(sys)};
  M.vc = circSpeed(S.m[0], M.sep);
  M.vrel = Math.hypot(S.vx[1] - S.vx[0], S.vy[1] - S.vy[0]);
  if(ST.view === 'circ') M.ci = circModel(sys);
  if(ST.view === 'exact') M.ex = exactModel(sys);
  if(ST.view === 'cons') M.cn = consModel(sys);
  return M;
}

/* ================================================================== *
 *  readout / equation bar / tag                                       *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">' + t + '</td></tr>'; }
function rrow(a, b, cls){ return '<tr><td>' + a + '</td><td class="v' + (cls ? ' ' + cls : '') + '">' + b + '</td></tr>'; }
function readoutHTML(M){
  const sys = M.sys, S = sys.S, min = sys.cfg.minutes;
  let s = '<div class="rname">Gravity and orbits<small>' + plain(TABS.find(t => t[0] === M.view)[1])
        + '</small></div><table>';
  s += hd(plain(M.sysName) + ' &mdash; PhET&rsquo;s ' + M.screenName + ' screen')
     + rrow('clock', plain(timeStr(sys.t, min)) + ' <span class="dim">(' + plain(timeStrFine(sys.t, min)) + ')</span>')
     + rrow('gravity', ST.gravity ? 'on' : 'off', ST.gravity ? 'good' : 'bad')
     + rrow('separation', plain(lenStr(M.sep, 5)))
     + rrow('relative speed', fmt(M.vrel, 1) + ' m/s')
     + rrow('circular speed there', fmt(M.vc, 1) + ' m/s <span class="dim">&radic;(GM/r)</span>')
     + rrow('their ratio', fmt(M.vrel / M.vc, 5), Math.abs(M.vrel / M.vc - 1) < 0.05 ? 'good' : '');
  s += hd('the bodies (PhET&rsquo;s own readout)');
  for(const b of M.bodies)
    s += rrow('<span style="color:' + b.col + '">' + b.name + '</span>' + (b.fixed ? ' <span class="dim">(fixed)</span>' : ''),
              plain(massReadout(S, b.i, sys.cfg.id)) + '<br><span class="dim">' + sigf(b.m, 5) + ' kg, '
              + fmt(Math.hypot(b.vx, b.vy), 1) + ' m/s</span>');
  if(M.ref){
    const el = M.ref.el;
    s += hd('the exact orbit (' + (M.ref.kind === 'fixed' ? 'about the fixed star' : 'two free bodies') + ')')
       + rrow('&mu;', sigf(M.ref.mu, 6) + ' m&sup3;/s&sup2;')
       + rrow('conic', el.kind, el.kind === 'ellipse' ? 'good' : 'bad')
       + rrow('a', el.kind === 'ellipse' ? plain(lenStr(el.a, 6)) : '&mdash;')
       + rrow('e', fmt(el.e, 6))
       + (el.kind === 'ellipse'
          ? rrow('period T', plain(timeStr(el.T, min)) + ' <span class="dim">(' + plain(timeStrFine(el.T, min)) + ')</span>', 'good')
            + rrow('periapsis, apoapsis', plain(lenStr(el.q, 5)) + ', ' + plain(lenStr(el.Q, 5)))
          : rrow('escape speed here', fmt(el.vesc, 1) + ' m/s', 'bad'));
  } else s += hd('three bodies') + rrow('closed form', 'none &mdash; this is the three-body problem', 'bad');
  if(M.view === 'circ' && M.ci){
    const el = M.ci.el;
    s += hd('the circular-orbit view')
       + rrow('v / v<sub>c</sub>', fmt(ST.vfrac, 4))
       + rrow('start speed', fmt(M.ci.v, 1) + ' m/s of an escape ' + fmt(M.ci.vesc, 1))
       + rrow('the conic it makes', el.kind, el.kind === 'ellipse' ? 'good' : 'bad')
       + rrow('e', fmt(el.e, 9), Math.abs(ST.vfrac - 1) < 1e-12 ? 'good' : '')
       + (el.kind === 'ellipse' ? rrow('T', plain(timeStr(el.T, min))) : rrow('T', 'infinite', 'bad'))
       + (M.ci.hits ? rrow('periapsis', plain(lenStr(el.q, 4)) + ' &mdash; inside the '
                           + plain(lenStr(M.ci.rTrue, 4)) + ' body, so it hits', 'bad') : '');
  }
  if(M.view === 'exact' && M.ex)
    s += hd('the integration against Kepler')
       + rrow('|r<sub>num</sub> &minus; r<sub>Kepler</sub>|', M.ex.err === 0 ? '0' : M.ex.err.toExponential(2) + ' m',
              M.ex.err < 1e-3 * M.sep ? 'good' : 'bad')
       + rrow('as a fraction of r', (M.ex.err / M.sep).toExponential(2))
       + rrow('after', plain(timeStr(sys.t, min)));
  if(M.view === 'cons' && M.cn){
    const c = M.cn;
    s += hd('the constants of the motion')
       + rrow('|&Delta;E/E|', c.dE === 0 ? '0' : c.dE.toExponential(2), c.dE < 1e-8 ? 'good' : 'bad')
       + rrow('|&Delta;L/L|', c.dL === 0 ? '0' : c.dL.toExponential(2), c.dL < 1e-10 ? 'good' : 'bad')
       + rrow('|&Delta;p|/p', c.dP === 0 ? '0' : c.dP.toExponential(2), c.dP < 1e-10 ? 'good' : 'bad');
    if(c.broken.length) s += rrow('but PhET&rsquo;s Model screen', c.broken.join('; '), 'bad');
    if(!ST.gravity)
      s += hd('gravity off: a pure drift')
         + rrow('off the straight line by', c.coast.dev === 0 ? '0 m (exactly)' : c.coast.dev.toExponential(2) + ' m',
                'good')
         + rrow('... of a path', plain(lenStr(c.coast.travel, 4)) + ' long')
         + rrow('|v| has changed by', c.coast.dspeed === 0 ? '0 m/s (exactly)' : c.coast.dspeed.toExponential(2) + ' m/s',
                c.coast.dspeed === 0 ? 'good' : 'bad')
         + rrow('and the energy?', 'not conserved &mdash; the ledger still counts a potential '
                + 'the bodies no longer feel', 'bad');
    if(c.shadow)
      s += hd('PhET&rsquo;s own step, beside ours')
         + rrow('its |&Delta;E/E|', (Math.abs(c.shadow.E - c.base.E) / Math.abs(c.base.E)).toExponential(2), 'bad')
         + rrow('the two runs differ by', plain(lenStr(c.shadow.dev, 3)))
         + rrow('measured order', 'PEFRL ' + fmt(c.order.slope('pefrl'), 2) + ', PhET&rsquo;s '
                + fmt(c.order.slope('phet'), 2), 'good');
  }
  s += hd('PhET&rsquo;s numbers against the measurement')
     + rrow('Moon radius', fmt(PH.MOON_RADIUS / 1e3, 1) + ' km vs ' + fmt(MEAS.MOON_RADIUS / 1e3, 1)
            + ' km <span class="dim">(NASA)</span>', 'bad')
     + rrow('Sun mass', sigf(PH.SUN_MASS, 4) + ' vs ' + sigf(MEAS.SUN_MASS, 5) + ' kg')
     + rrow('Earth mass', sigf(PH.EARTH_MASS, 5) + ' vs ' + sigf(MEAS.EARTH_MASS, 5) + ' kg')
     + rrow('ISS mass', sigf(PH.STATION_MASS, 6) + ' kg <span class="dim">(NASA&rsquo;s own figure)</span>', 'good')
     + rrow('G', sigf(G_SI, 6) + ' <span class="dim">(CODATA 2014; 2018 gives 6.67430e-11)</span>');
  s += '</table><div class="note">The sim RUNS on PhET&rsquo;s numbers, so its systems move as PhET&rsquo;s do; '
     + 'the measured column sits beside them. Two-body runs are pinned against the closed-form Kepler '
     + 'solution and against scipy&rsquo;s solve_ivp (DOP853, rtol 1e-13) in '
     + 'build/gravity-and-orbits/derive.py.</div>';
  return s;
}
function eqbarHTML(M){
  const E = (eq, sm) => '<span class="lhs">' + eq + '</span><span class="sm">' + sm + '</span>';
  if(M.view === 'model' || M.view === 'scale')
    return E('<span class="hl">F = G m&#8321;m&#8322;/r&sup2;</span> &nbsp;&middot;&nbsp; G = 6.67408&times;10&#8315;&sup1;&sup1; m&sup3; kg&#8315;&sup1; s&#8315;&sup2; <span class="rm">(PhET&rsquo;s value, CODATA 2014)</span>',
      M.view === 'model'
        ? 'one law, every pair — and on this screen the bodies are drawn far bigger than they are, so that you can see them at all'
        : 'the same law and the same bodies, now drawn true: at PhET’s own zoom the Earth is a fortieth of a pixel across');
  if(M.view === 'circ')
    return E('<span class="hl">GMm/r&sup2; = mv&sup2;/r &nbsp;&rArr;&nbsp; v = &radic;(GM/r)</span> &nbsp;&middot;&nbsp; T = 2&pi;&radic;(r&sup3;/GM) &nbsp;&middot;&nbsp; v<sub>esc</sub> = &radic;2 v',
      'the one speed at which falling and moving sideways exactly balance; slower and the orbit dips inside, faster and it swings out, and at √2 it never comes back');
  if(M.view === 'exact')
    return E('<span class="hl">M = E &minus; e sin E = n(t &minus; t&#8320;), &nbsp; n = &radic;(&mu;/a&sup3;)</span> &nbsp;&middot;&nbsp; r = a(1 &minus; e cos E) &nbsp;&middot;&nbsp; &mu; = GM <span class="rm">(or G(M+m))</span>',
      'two bodies are the case that can be solved: the position at any time follows from Kepler’s equation, and the orange curve is that answer, not an integration');
  return E('<span class="hl">E = &sum;&frac12;m<sub>i</sub>v<sub>i</sub>&sup2; &minus; &sum;<sub>i&lt;j</sub>Gm<sub>i</sub>m<sub>j</sub>/r<sub>ij</sub></span> &nbsp;&middot;&nbsp; p = &sum;m<sub>i</sub>v<sub>i</sub> &nbsp;&middot;&nbsp; L = &sum;m<sub>i</sub>(x<sub>i</sub>v<sub>yi</sub> &minus; y<sub>i</sub>v<sub>xi</sub>)',
    'a closed system keeps all three; a nailed-down star and a one-sided force do not, and PhET’s Model screen has both — this view measures the damage');
}
function tagHTML(M){
  const nm = plain(TABS.find(t => t[0] === M.view)[1]);
  return '<b>' + nm + '</b> — ' + plain(M.sysName) + ', PhET’s ' + M.screenName + ' screen, gravity '
    + (ST.gravity ? 'on' : 'OFF') + ', t = ' + plain(timeStr(M.t, M.cfg.minutes));
}
