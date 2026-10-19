
/* ================================================================== *
 *  state, the clock, the per-view model, the readout and the eqbar    *
 * ================================================================== */
const TABS = [['first', 'the first law'], ['second', 'the second law'], ['third', 'the third law'],
              ['all', 'all laws'], ['anom', 'Kepler&rsquo;s equation']];
const COL = {pos: '#b8ec4c', ref: '#e8843a', live: '#cd35c4', struct: '#5ac8e0', dim: '#8b93a6',
             star: '#f2c14e', planet: '#cd35c4', orbit: '#b8ec4c', target: '#7b8496', edge: '#242a3a',
             foci: '#5ac8e0', amaj: '#e8843a', bmin: '#b8ec4c', cfoc: '#c9a7ff', warn: '#e8843a',
             sector: '#cd35c4', sectorOn: '#f06ae8', off: '#161c2c'};
const RO_W = 300;
const SPEEDS = [{id: 'slow', name: 'slow', f: 0.25}, {id: 'normal', name: 'normal', f: 1},
                {id: 'fast', name: 'fast', f: 1.75}];          /* PhET's timeSpeedMap: 1/4, 1, 7/4 */
const ZOOMS = [{id: 'near', name: 'near', R: 3.2}, {id: 'far', name: 'far', R: 7.4}];
const POWERS = [{id: 1, name: '1'}, {id: 2, name: '2'}, {id: 3, name: '3'}];
const V_DEF = auYrToKms(Math.sqrt(K_SUN * (2 / 2 - 1 / 1.5)));   /* a = 1.5 AU, e = 1/3 at (2,0) */
const VSCALE = 4.2;              /* px per km/s for the velocity arrow (printed on the canvas) */
const FSCALE = 60;               /* px for the gravity arrow at 1 AU, times 10^fpow */
const F_REF = 1.0;               /* the reference distance of that arrow, AU */

const DEFAULTS = {
  view: 'first', mass: 1, px: 2, py: 0, vx: 0, vy: V_DEF, circular: false, target: 'none',
  /* PhET's defaults: the velocity arrow on, everything else off, the semi-major axis on */
  foci: false, string: false, axes: false, semiaxes: false, ecc: false,
  apo: false, peri: false, div: PHET.DIV_DEF, swept: true, areaVals: false, timeVals: false,
  showA: true, showT: false, pa: 1, pt: 1, loglog: false,
  speedLab: false, velocity: true, gravity: false, fpow: 0,
  grid: false, tape: false, stopwatch: false,
  running: false, speed: 'normal', zoom: 'near', mfrac: 0.18
};
const ST = Object.assign({}, DEFAULTS);
/* the clock: t is years since the orbit was set (a drag, a preset or restart sets t = 0) */
const SIM = {t: 0, sw: 0, swRun: false, sweep: {erased: false, tErase: 0}, trace: null,
             tape: {ax: 0, ay: 1, bx: 1, by: 1}, periodTrace: null};
/* every view's stage keeps equal scale on both axes; the zoom sets the HALF-HEIGHT of the
   world window and the width follows the box, so a wide stage shows more sky, not a
   stretched orbit */
const DRAGK = {what: null, id: 0};

const TAPE0 = {ax: 0, ay: 1, bx: 1, by: 1};       /* PhET's measuring-tape default */
function simReset(){
  SIM.t = 0; SIM.sw = 0; SIM.swRun = false;
  SIM.sweep = {erased: false, tErase: 0};
  SIM.periodTrace = null;
  SIM.tape = Object.assign({}, TAPE0);
  traceReset();
}
function traceReset(){
  const el = klOrbit(ST.px, ST.py, ST.vx, ST.vy, ST.mass, ST.circular);
  SIM.trace = el.allowed ? {aMin: el.a, aMax: el.a} : null;
}
function traceNote(el){
  if(!el.allowed) return;
  if(!SIM.trace){ SIM.trace = {aMin: el.a, aMax: el.a}; return; }
  SIM.trace.aMin = Math.min(SIM.trace.aMin, el.a);
  SIM.trace.aMax = Math.max(SIM.trace.aMax, el.a);
}
function speedFactor(){ const s = SPEEDS.find(s => s.id === ST.speed); return s ? s.f : 1; }
function frameDt(){ return PHET.FRAME_YR * speedFactor(); }
function viewRadius(){ const z = ZOOMS.find(z => z.id === ST.zoom); return z ? z.R : 3.2; }
/* one frame: the clock runs only on an orbit PhET would allow */
function runStep(){
  if(!ST.running) return false;
  const el = klOrbit(ST.px, ST.py, ST.vx, ST.vy, ST.mass, ST.circular);
  if(!el.allowed) return false;
  const dt = frameDt();
  SIM.t += dt;
  if(SIM.swRun) SIM.sw += dt;
  if(SIM.periodTrace) SIM.periodTrace.t = Math.min(SIM.periodTrace.t + dt, el.T);
  return true;
}
/* pressing play erases the sectors, as PhET does ("the areas disappear and the planet starts
   swiping"); pausing leaves them as they are.  onPlay() is the only place that work lives:
   the checkbox sets ST.running BEFORE its handler runs, so a guard of the form
   `if(on && !ST.running)` inside setRunning is already false by then and the erase never
   happened -- found by the UI drive. */
function onPlay(){
  SIM.sweep = {erased: true, tErase: SIM.t};
  if(ST.showT && !SIM.periodTrace) SIM.periodTrace = {t0: SIM.t, t: 0};
}
function setRunning(on){
  if(on && !ST.running) onPlay();
  ST.running = on;
}
function eraseSectors(){ SIM.sweep = {erased: true, tErase: SIM.t}; }
/* the planet's state now: on the orbit if it is allowed, at the set point if it is not */
function planetNow(el){
  if(!el.allowed) return {x: el.px, y: el.py, vx: auYrToKms(el.vx), vy: auYrToKms(el.vy),
                          r: el.r, vKms: auYrToKms(el.v), nu: el.nu0, E: el.E0 === undefined ? 0 : el.E0,
                          M: el.M0 === undefined ? 0 : el.M0};
  return klStateAt(el, SIM.t);
}

/* ---- the model each view draws from ------------------------------------------------------ */
function secondModel(el){
  const N = ST.div, cuts = klSectors(el, N), sw = klSwept(el, N, SIM.t, SIM.sweep);
  const areas = sw.frac.map(f => f * sw.full);
  return {N, cuts, frac: sw.frac, full: sw.full, areas, dt: el.T / N, total: PI * el.a * el.b,
          rate: 0.5 * Math.abs(el.h)};
}
function thirdModel(el){
  const th = klThird(el, ST.pa, ST.pt);
  const tr = SIM.trace;
  const pts = [];
  if(tr){
    const lo = Math.min(tr.aMin, el.a), hi = Math.max(tr.aMax, el.a);
    for(let i = 0; i <= 60; i++){
      const a = lo + (hi - lo) * i / 60;
      pts.push([Math.pow(a, ST.pa), Math.pow(periodOf(a, starMu(ST.mass)), ST.pt)]);
    }
  }
  const tgt = ST.target === 'none' || ST.mass !== 1 ? null : targetById(ST.target);
  const planets = TARGETS.filter(t => t.a).map(t => ({id: t.id, name: t.name, a: t.a,
                                                      T: periodOf(t.a, starMu(ST.mass))}));
  const aMax = Math.max(2, el.a * 1.15, tgt ? tgt.a * 1.1 : 0);
  return {th, pts, tgt, planets, aMax, Tmax: periodOf(aMax, starMu(ST.mass)), K: klConst(ST.mass)};
}
/* the anomaly view follows the same clock as every other view: M is the planet's own mean
   anomaly at SIM.t, and its slider scrubs SIM.t through one period rather than keeping a
   second clock of its own */
function anomModel(el){
  const Mabs = el.M0 + el.n * SIM.t;
  const M = ((Mabs % TAU) + TAU) % TAU;
  const sol = keplerSolve(M, el.e), E = sol.E, nu = trueFromE(E, el.e);
  const tr = [];              /* Newton from E0 = M, PhET's start, for the picture */
  let Ei = M, stop = -1;
  tr.push(Ei);
  for(let k = 0; k < 10; k++){
    const f = Ei - el.e * Math.sin(Ei) - M, fp = 1 - el.e * Math.cos(Ei), d = f / fp;
    Ei -= d; tr.push(Ei);
    if(stop < 0 && Math.abs(d) <= PHET.NEWTON_TOL) stop = k;      /* where PhET's loop stops */
    if(Math.abs(d) < 1e-16) break;
  }
  const curve = [];
  for(let i = 0; i <= 160; i++){
    const m = TAU * i / 160, e2 = keplerE(m, el.e);
    curve.push([m, e2, trueFromE(e2, el.e)]);
  }
  return {M, E, nu, it: sol.it, res: E - el.e * Math.sin(E) - M, trace: tr, stop, curve,
          t: SIM.t, tPeri: M / el.n, r: el.a * (1 - el.e * Math.cos(E))};
}
function buildModel(){
  const st = ST;
  const el = klOrbit(st.px, st.py, st.vx, st.vy, st.mass, st.circular);
  const now = planetNow(el);
  const M = {view: st.view, st, t: SIM.t, el, now, foci: klFoci(el), R: viewRadius(),
             warn: el.crash ? 'The body will crash into the star.' : el.escaping ? 'The body will escape the system.' : null,
             K: klConst(st.mass), tgt: st.target === 'none' ? null : targetById(st.target),
             tgtOn: st.target !== 'none' && st.mass === 1};
  if(el.allowed && (st.view === 'second' || st.view === 'all')) M.sec = secondModel(el);
  if(el.allowed && (st.view === 'third' || st.view === 'all')) M.thd = thirdModel(el);
  if(el.allowed && st.view === 'anom') M.an = anomModel(el);
  if(el.allowed) M.rv = {r: now.r, thr: Math.atan2(now.y, now.x), v: now.vKms,
                         thv: Math.atan2(now.vy, now.vx),
                         thrv: Math.atan2(now.vy, now.vx) - Math.atan2(now.y, now.x)};
  return M;
}

/* ================================================================== *
 *  readout / equation bar / tag                                       *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">' + t + '</td></tr>'; }
function rrow(a, b, cls){ return '<tr><td>' + a + '</td><td class="v' + (cls ? ' ' + cls : '') + '">' + b + '</td></tr>'; }
function degStr(rad){ let d = rad / DEG; d = ((d % 360) + 360) % 360; return fmt(d, 1) + '&deg;'; }
function yrStr(t){ return Math.abs(t) < 1 ? fmt(t * 365.25, 2) + ' d' : fmt(t, 3) + ' yr'; }
function readoutHTML(M){
  const st = ST, el = M.el;
  let s = '<div class="rname">Kepler&rsquo;s laws<small>' + plain(TABS.find(t => t[0] === M.view)[1]) + '</small></div><table>';
  s += hd('the star and the clock')
     + rrow('mass', fmt(st.mass, 2) + ' M<sub>&#9737;</sub>' + (st.mass === 1 ? ' (our Sun)' : ''))
     + rrow('&mu; = GM', sigf(starMu(st.mass), 6) + ' AU&sup3;/yr&sup2;')
     + rrow('t since the orbit was set', yrStr(SIM.t))
     + (st.stopwatch ? rrow('stopwatch', yrStr(SIM.sw), SIM.swRun ? 'good' : '') : '');
  if(M.warn){
    s += hd('this orbit is not allowed') + rrow('PhET&rsquo;s warning', M.warn, 'bad')
       + rrow('speed', fmt(el.vKms, 3) + ' km/s of an escape speed ' + fmt(el.vescKms, 3) + ' km/s')
       + rrow('periapsis', sigf(el.q, 4) + ' AU against a star of radius ' + sigf(el.star, 4) + ' AU')
       + '</table><div class="note">PhET caps the speed at 0.99 of the escape speed and will not run the clock on an orbit it has flagged; neither will this. Drag the velocity back, or move the planet out.</div>';
    return s;
  }
  s += hd('the orbit (first law)')
     + rrow('semi-major axis a', sigf(el.a, 6) + ' AU')
     + rrow('semi-minor axis b', sigf(el.b, 6) + ' AU')
     + rrow('focal distance c = ae', sigf(el.c, 6) + ' AU')
     + rrow('eccentricity e = c/a', fmt(el.e, 4) + (el.e < PHET.E_ROUND ? ' <span class="good">(PhET shows 0)</span>' : ''), 'good')
     + rrow('periapsis, apoapsis', sigf(el.q, 5) + ', ' + sigf(el.Q, 5) + ' AU')
     + rrow('d&#8321; + d&#8322; (the string)', sigf(2 * el.a, 6) + ' AU')
     + rrow('sense', el.dir > 0 ? 'counterclockwise' : 'clockwise');
  if(M.rv){
    s += hd('the planet now')
       + rrow('|r|, &theta;<sub>r</sub>', sigf(M.rv.r, 5) + ' AU, ' + degStr(M.rv.thr))
       + rrow('|v|, &theta;<sub>v</sub>', fmt(M.rv.v, 3) + ' km/s, ' + degStr(M.rv.thv))
       + rrow('&theta;<sub>rv</sub> between them', degStr(M.rv.thrv))
       + rrow('true anomaly &nu;', degStr(M.now.nu));
  }
  if(M.view === 'second' || M.view === 'all'){
    const c = M.sec;
    if(c) s += hd('equal areas (second law)')
       + rrow('divisions N', String(c.N))
       + rrow('area of each sector &pi;ab/N', sigf(c.full, 6) + ' AU&sup2;', 'good')
       + rrow('time in each sector T/N', yrStr(c.dt))
       + rrow('dA/dt = &frac12;|h|', sigf(c.rate, 6) + ' AU&sup2;/yr', 'good')
       + rrow('swept so far', sigf(c.areas.reduce((a, b) => a + b, 0), 5) + ' of ' + sigf(c.total, 5) + ' AU&sup2;');
  }
  if(M.view === 'third' || M.view === 'all'){
    const d = M.thd;
    if(d) s += hd('the third law')
       + rrow('period T', fmt(el.T, 5) + ' yr')
       + rrow('T<sup>' + st.pt + '</sup>/a<sup>' + st.pa + '</sup>', fmt(d.th.ratio, 4) + ' yr<sup>' + st.pt + '</sup>/AU<sup>' + st.pa + '</sup>',
              d.th.correct ? 'good' : '')
       + rrow('4&pi;&sup2;/GM (the law)', fmt(d.K, 5) + ' yr&sup2;/AU&sup3;', 'good')
       + rrow('powers', d.th.correct ? 'a&sup3; and T&sup2;: a constant' : 'only a&sup3; with T&sup2; is constant', d.th.correct ? 'good' : 'bad')
       + rrow('a visited', SIM.trace ? sigf(SIM.trace.aMin, 4) + ' &hellip; ' + sigf(SIM.trace.aMax, 4) + ' AU' : '&mdash;');
  }
  if(M.view === 'anom' && M.an){
    const A = M.an;
    s += hd('Kepler&rsquo;s equation')
       + rrow('mean anomaly M = nt', degStr(A.M) + ' at t = ' + yrStr(A.t))
       + rrow('eccentric anomaly E', degStr(A.E))
       + rrow('true anomaly &nu;', degStr(A.nu))
       + rrow('Newton steps to 1e-15', String(A.it), 'good')
       + rrow('residual E &minus; e sin E &minus; M', A.res === 0 ? '0' : A.res.toExponential(2), 'good')
       + rrow('PhET stops after', (A.stop + 1) + ' steps (its tolerance is ' + PHET.NEWTON_TOL + ' rad)', 'bad');
  }
  if(M.tgt && M.tgtOn) s += hd('target orbit') + rrow(M.tgt.name, 'a = ' + fmt(M.tgt.a, 3) + ' AU, e = ' + fmt(M.tgt.e, 4))
       + rrow('its period', fmt(periodOf(M.tgt.a, starMu(1)), 4) + ' yr');
  s += '</table><div class="note">Every number here is closed form: the elements from the state vector, the position from '
     + 'Kepler&rsquo;s equation (Newton to 1e-15), T = 2&pi;&radic;(a&sup3;/GM). Pinned in selfTest to '
     + 'build/keplers-laws/derive.py (scipy brentq, quad, solve_ivp at rtol 1e-13).</div>';
  return s;
}
function eqbarHTML(M){
  const E = (eq, sm) => '<span class="lhs">' + eq + '</span><span class="sm">' + sm + '</span>';
  if(M.view === 'first') return E('<span class="hl">r = a(1 &minus; e&sup2;) / (1 + e cos &nu;)</span> &nbsp;&middot;&nbsp; d&#8321; + d&#8322; = 2a &nbsp;&middot;&nbsp; e = c/a &nbsp;&middot;&nbsp; b = a&radic;(1 &minus; e&sup2;)',
    'the orbit of a planet is an ellipse with the star at one focus — the first law, 1609; drag the planet or its velocity arrow and the ellipse follows');
  if(M.view === 'second') return E('<span class="hl">dA/dt = &frac12;r&sup2; d&nu;/dt = &frac12;|h| = &pi;ab/T</span> &nbsp;&middot;&nbsp; equal areas in equal times &nbsp;&middot;&nbsp; M = E &minus; e sin E = nt',
    'the line from star to planet sweeps equal areas in equal times — the second law; it is the conservation of angular momentum, and it is why the mean anomaly, not the angle you see, runs uniformly');
  if(M.view === 'third') return E('<span class="hl">T&sup2; = 4&pi;&sup2;a&sup3;/GM</span> &nbsp;&middot;&nbsp; T&sup2;/a&sup3; = ' + fmt(M.K, 4) + ' yr&sup2;/AU&sup3; for this star &nbsp;&middot;&nbsp; log T = (3/2) log a &minus; &frac12; log(GM/4&pi;&sup2;)',
    'the square of the period goes as the cube of the semi-major axis — the third law, 1619; the constant belongs to the star alone, so every body about it lies on one line of slope 3/2');
  if(M.view === 'all') return E('<span class="hl">r = a(1 &minus; e&sup2;)/(1 + e cos &nu;)</span> &nbsp;&middot;&nbsp; <span class="hl2">dA/dt = &frac12;|h|</span> &nbsp;&middot;&nbsp; T&sup2; = 4&pi;&sup2;a&sup3;/GM',
    'the three laws on one orbit: the shape, the pace around it, and how that pace scales with size');
  return E('<span class="hl">M = E &minus; e sin E</span> &nbsp;&middot;&nbsp; tan(&nu;/2) = &radic;((1+e)/(1&minus;e)) tan(E/2) &nbsp;&middot;&nbsp; r = a(1 &minus; e cos E)',
    'Kepler’s equation: the bridge from time to place — transcendental in E, solved by Newton in a handful of steps');
}
function tagHTML(M){
  const st = ST, nm = plain(TABS.find(t => t[0] === M.view)[1]);
  let s = '<b>' + nm + '</b> — ' + (st.mass === 1 ? 'our Sun' : fmt(st.mass, 2) + ' M☉')
        + ', a = ' + sigf(M.el.a, 4) + ' AU, e = ' + fmt(M.el.e, 3);
  if(M.warn) s = '<b>' + nm + '</b> — ' + plain(M.warn);
  else if(st.circular) s += ' (held circular)';
  return s;
}
