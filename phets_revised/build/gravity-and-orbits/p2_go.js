
/* ================================================================== *
 *  Gravity and Orbits: PhET's data, its four systems on its two       *
 *  screens, and the engine that runs them.  Units are SI throughout   *
 *  (metres, kilograms, seconds), as PhET's model is.                  *
 *                                                                     *
 *  Python twin: build/gravity-and-orbits/derive.py (scipy brentq,     *
 *  solve_ivp DOP853 at rtol 1e-13, and its own PEFRL twin).           *
 * ================================================================== */

/* ---- PhET's constants, read out of docs/phets/gravity-and-orbits_en.html (1.6.28).
   Each line names the minified identifier it came from, so the grep can be repeated. */
const G_SI = 667408e-16;                 /* PhysicalConstants (Yg), = 6.67408e-11, CODATA 2014 */
const PH = {
  SUN_MASS: 1.989e30,                    /* SceneFactory's ZI */
  EARTH_MASS: 59724e20,                  /* GravityAndOrbitsConstants (bp).EARTH_MASS */
  MOON_MASS: 7346e19,                    /* SceneFactory's LI */
  STATION_MASS: 419725,                  /* bp.SPACE_STATION_MASS */
  SUN_RADIUS: 6957e5, EARTH_RADIUS: 6371e3, MOON_RADIUS: 1727400, STATION_RADIUS: 45.5,
  EARTH_X: 147098074e3, EARTH_VY: 30300, /* SunEarthModeConfig */
  MOON_Y: 3633e5, MOON_VX: -1082,        /* SunEarthMoonModeConfig / PlanetMoonModeConfig */
  STATION_X: 6718045.5, STATION_VY: 7706, STATION_ROT: 5484,
  MOON_ROT: 27.322 * 24 * 3600,          /* PhET writes 27.322 d */
  DAY: 86400,                            /* GravityAndOrbitsClock.SECONDS_PER_DAY */
  DEFAULT_DT: 36e3,                      /* GravityAndOrbitsClock.DEFAULT_DT */
  SUBSTEP: 0.13125,                      /* GravityAndOrbitsPhysicsEngine.stepModel */
  SPEED_STEPS: [1, 4, 7],                /* slow / normal / fast */
  STAGE_W: 987.5, STAGE_H: 772.5,        /* GravityAndOrbitsSceneView.STAGE_SIZE */
  VIEW_SCALE: 1.5e-9,                    /* view units per metre, times the scene's zoom */
  ZOOM_MIN: 0.5, ZOOM_MAX: 1.3,          /* GravityAndOrbitsConstants.ZOOM_RANGE */
  MOON_BOOST: 10200,                     /* ModelState.getTwoBodyForce, adjustMoonOrbit */
  MODEL_SUN_R: 50, MODEL_PLANET_R: 800, MODEL_MOON_R: 800,
  MODEL_MOON_VX: 21, MODEL_MOON_Y_R: 1.7,
  MODEL_PM_R: 15, MODEL_SAT_PLANET_R: 0.8, MODEL_SAT_R: 2e4
};
/* ---- the measured column, each value at the precision its source prints.
   NASA planetary fact sheets (nssdc.gsfc.nasa.gov/planetary/factsheet/) for the Sun, the
   Earth and the Moon; NASA's ISS "Facts and Figures" page for the station. */
const MEAS = {
  SUN_MASS: 1988400e24, SUN_RADIUS: 695700e3, SUN_GM: 132712e6 * 1e9,
  EARTH_MASS: 5.9722e24, EARTH_RADIUS: 6371.000e3, EARTH_GM: 0.39860e6 * 1e9,
  EARTH_A: 149.598e9, EARTH_PERI: 147.095e9, EARTH_VMAX: 30.29e3, EARTH_YEAR: 365.256,
  MOON_MASS: 7.346e22, MOON_RADIUS: 1737.4e3, MOON_PERI: 363300e3, MOON_A: 384400e3,
  MOON_VMAX: 1.082e3, MOON_MONTH: 27.3217, MOON_ROT: 655.720 * 3600,
  STATION_MASS: 419725, STATION_TRUSS: 94.0
};
const AU_M = 149597870.7e3;              /* IAU 2012 B2, exact by definition */

/* ---- the four systems, exactly as PhET's SceneFactory builds them ------------------------ */
const SYSTEMS = [
  {id: 'starPlanet', name: 'Sun and Planet'},
  {id: 'starPlanetMoon', name: 'Sun, Planet and Moon'},
  {id: 'planetMoon', name: 'Planet and Moon'},
  {id: 'planetSatellite', name: 'Planet and Space Station'}
];
function systemById(id){ const s = SYSTEMS.find(s => s.id === id); if(!s) throw new Error('no system ' + id); return s; }
const SCREENS = [{id: 'model', name: 'Model'}, {id: 'scale', name: 'To Scale'}];
/* PhET's own body colours: yellow star, grey planet, magenta moon, grey satellite.  Here the
   house palette's roles are kept and only the star keeps PhET's yellow. */
const BODY_COL = {star: '#f2c14e', planet: '#5ac8e0', moon: '#cd35c4', satellite: '#b8ec4c'};

function bodyCfg(name, kind, m, r, x, y, vx, vy, rot){
  return {name, kind, m, r, x, y, vx, vy, rot: rot === undefined ? null : rot, fixed: false,
          settable: true};
}
function baseScene(sid){
  if(sid === 'starPlanet') return {
    id: sid, zoom: 1.25, dt: PH.DEFAULT_DT, grid: PH.EARTH_X / 2, minutes: false,
    bodies: [bodyCfg('Our Sun', 'star', PH.SUN_MASS, PH.SUN_RADIUS, 0, 0, 0, 0),
             bodyCfg('Earth', 'planet', PH.EARTH_MASS, PH.EARTH_RADIUS, PH.EARTH_X, 0, 0, PH.EARTH_VY)]};
  if(sid === 'starPlanetMoon'){
    /* PhET builds this scene's moon with massSettable false (SceneFactory's MoonNode takes
       the flag; only Planet-and-Moon gets a settable one), so its slider is dead there */
    const moon = bodyCfg('Our Moon', 'moon', PH.MOON_MASS, PH.MOON_RADIUS, PH.EARTH_X, PH.MOON_Y,
                         PH.MOON_VX, PH.EARTH_VY);
    moon.settable = false;
    return {id: sid, zoom: 1.25, dt: PH.DEFAULT_DT, grid: PH.EARTH_X / 2, minutes: false,
            bodies: [bodyCfg('Our Sun', 'star', PH.SUN_MASS, PH.SUN_RADIUS, 0, 0, 0, 0),
                     bodyCfg('Earth', 'planet', PH.EARTH_MASS, PH.EARTH_RADIUS, PH.EARTH_X, 0, 0, PH.EARTH_VY),
                     moon]};
  }
  if(sid === 'planetMoon'){
    /* PhET puts this pair in its own centre-of-momentum frame by hand */
    const vp = -PH.MOON_VX * PH.MOON_MASS / (PH.EARTH_MASS + PH.MOON_MASS), vm = vp + PH.MOON_VX;
    return {id: sid, zoom: 400, dt: PH.DEFAULT_DT / 3, grid: PH.MOON_Y / 2, minutes: false,
            centre: [PH.EARTH_X, 0],
            bodies: [bodyCfg('Earth', 'planet', PH.EARTH_MASS, PH.EARTH_RADIUS, PH.EARTH_X, 0, vp, 0),
                     bodyCfg('Our Moon', 'moon', PH.MOON_MASS, PH.MOON_RADIUS, PH.EARTH_X, PH.MOON_Y, vm, 0)]};
  }
  if(sid === 'planetSatellite') return {
    id: sid, zoom: 21600, dt: 9e-4 * PH.DEFAULT_DT, grid: PH.STATION_X, minutes: true,
    bodies: [bodyCfg('Earth', 'planet', PH.EARTH_MASS, PH.EARTH_RADIUS, 0, 0, 0, 0),
             bodyCfg('Space Station', 'satellite', PH.STATION_MASS, PH.STATION_RADIUS,
                     PH.STATION_X, 0, 0, PH.STATION_VY, PH.STATION_ROT)]};
  throw new Error('no system ' + sid);
}
/* ModeConfig.center(): subtract the centre-of-momentum velocity from every body */
function centreCfg(cfg){
  let M = 0, px = 0, py = 0;
  for(const b of cfg.bodies){ M += b.m; px += b.m * b.vx; py += b.m * b.vy; }
  for(const b of cfg.bodies){ b.vx -= px / M; b.vy -= py / M; }
  return cfg;
}
/* A scene of either screen.  The Model screen's exaggerations are PhET's own, applied in
   PhET's order (the subclass constructors run, THEN the factory calls center()). */
function sceneCfg(screen, sid){
  const cfg = baseScene(sid), b = cfg.bodies;
  cfg.screen = screen;
  cfg.boost = 1;
  if(screen === 'model'){
    if(sid === 'starPlanet'){
      b[0].r *= PH.MODEL_SUN_R; b[1].r *= PH.MODEL_PLANET_R; b[0].fixed = true;
    } else if(sid === 'starPlanetMoon'){
      b[0].r *= PH.MODEL_SUN_R; b[1].r *= PH.MODEL_PLANET_R; b[2].r *= PH.MODEL_MOON_R;
      b[2].vx *= PH.MODEL_MOON_VX;
      b[2].y = b[1].y + PH.MODEL_MOON_Y_R * b[1].r;
      b[0].fixed = true;
      cfg.boost = PH.MOON_BOOST;
    } else if(sid === 'planetMoon'){
      b[0].r *= PH.MODEL_PM_R; b[1].r *= PH.MODEL_PM_R; b[1].rot = PH.MOON_ROT;
    } else {
      b[0].r *= PH.MODEL_SAT_PLANET_R; b[1].r *= PH.MODEL_SAT_R;
    }
  }
  return centreCfg(cfg);
}
/* PhET's view window: the 987.5 x 772.5 stage at 1.5e-9 view units per metre times the
   scene's own zoom and the user's zoom level (0.5-1.3). */
function viewHalf(cfg, level){ return PH.STAGE_H / (2 * PH.VIEW_SCALE * cfg.zoom * (level || 1)); }
/* one frame of PhET's clock: 0.13125 of the scene's base dt, taken 1, 4 or 7 times */
function frameDt(cfg, steps){ return PH.SUBSTEP * cfg.dt * steps; }

/* ================================================================== *
 *  the engine.  Flat arrays, PEFRL, and PhET's two Model-screen       *
 *  distortions carried explicitly (a fixed body, and a one-sided      *
 *  force boost on the moon).                                          *
 * ================================================================== */
function goState(cfg){
  const n = cfg.bodies.length;
  const S = {n, m: new Float64Array(n), x: new Float64Array(n), y: new Float64Array(n),
             vx: new Float64Array(n), vy: new Float64Array(n),
             ax: new Float64Array(n), ay: new Float64Array(n),
             fix: new Float64Array(n), kind: [], boost: cfg.boost, r: new Float64Array(n),
             rot: [], name: [], settable: []};
  cfg.bodies.forEach((b, i) => {
    S.m[i] = b.m; S.x[i] = b.x; S.y[i] = b.y; S.vx[i] = b.vx; S.vy[i] = b.vy;
    S.fix[i] = b.fixed ? 1 : 0; S.kind.push(b.kind); S.r[i] = b.r; S.rot.push(b.rot);
    S.name.push(b.name); S.settable.push(b.settable !== false);
  });
  return S;
}
function goCopy(S){
  const T = Object.assign({}, S);
  for(const k of ['m', 'x', 'y', 'vx', 'vy', 'ax', 'ay', 'fix', 'r']) T[k] = S[k].slice(0, S.n);
  T.kind = S.kind.slice(); T.rot = S.rot.slice(); T.name = S.name.slice();
  T.settable = S.settable.slice();
  return T;
}
/* The acceleration on every body.  PhET's Model Sun-Planet-Moon scene multiplies the pull of
   the PLANET on the MOON by 10200 and does NOT apply the reaction, so Newton's third law is
   broken there on purpose -- the exaggerated moon sits 23.85 times too far out and would
   otherwise drift away.  The pair loop is therefore NOT symmetric and cannot use the shared
   nbodyAccel. */
function goAccel(S){
  const n = S.n;
  for(let i = 0; i < n; i++){ S.ax[i] = 0; S.ay[i] = 0; }
  for(let i = 0; i < n; i++) for(let j = 0; j < n; j++){
    if(i === j) continue;
    const dx = S.x[j] - S.x[i], dy = S.y[j] - S.y[i];
    const r2 = dx * dx + dy * dy, r = Math.sqrt(r2);
    const k = (S.boost !== 1 && S.kind[i] === 'moon' && S.kind[j] === 'planet') ? S.boost : 1;
    const f = k * G_SI * S.m[j] / (r2 * r);
    S.ax[i] += f * dx; S.ay[i] += f * dy;
  }
}
function goDrift(S, c){
  for(let i = 0; i < S.n; i++){ if(S.fix[i]) continue; S.x[i] += c * S.vx[i]; S.y[i] += c * S.vy[i]; }
}
function goKick(S, c){
  goAccel(S);
  for(let i = 0; i < S.n; i++){ if(S.fix[i]) continue; S.vx[i] += c * S.ax[i]; S.vy[i] += c * S.ay[i]; }
}
/* PEFRL, with PhET's own three coefficients (they are in its doc/model.md too) */
function goPefrl(S, h){
  goDrift(S, PEFRL_XI * h);
  goKick(S, (1 - 2 * PEFRL_LAM) * h / 2);
  goDrift(S, PEFRL_CHI * h);
  goKick(S, PEFRL_LAM * h);
  goDrift(S, (1 - 2 * (PEFRL_CHI + PEFRL_XI)) * h);
  goKick(S, PEFRL_LAM * h);
  goDrift(S, PEFRL_CHI * h);
  goKick(S, (1 - 2 * PEFRL_LAM) * h / 2);
  goDrift(S, PEFRL_XI * h);
}
/* PhET's step AS SHIPPED: the same composition, but the acceleration is evaluated once at the
   start and reused by all four kicks.  That composition is exactly x + vh + a h^2/2, v + a h --
   a first-order method wearing a fourth-order method's coefficients.  derive.py measures both
   orders (16 and 2 per halving). */
function goPhetStep(S, h){
  goAccel(S);
  const n = S.n, ax = S.ax.slice(0, n), ay = S.ay.slice(0, n);
  const kick = c => { for(let i = 0; i < n; i++){ if(S.fix[i]) continue; S.vx[i] += c * ax[i]; S.vy[i] += c * ay[i]; } };
  goDrift(S, PEFRL_XI * h);
  kick((1 - 2 * PEFRL_LAM) * h / 2);
  goDrift(S, PEFRL_CHI * h);
  kick(PEFRL_LAM * h);
  goDrift(S, (1 - 2 * (PEFRL_CHI + PEFRL_XI)) * h);
  kick(PEFRL_LAM * h);
  goDrift(S, PEFRL_CHI * h);
  kick((1 - 2 * PEFRL_LAM) * h / 2);
  goDrift(S, PEFRL_XI * h);
}
/* the step a system can take: eta times the shortest of every pair's crossing time r/|dv| and
   free-fall time sqrt(r^3/(G(mi+mj))).  A fixed step cannot serve both a 1-AU orbit and a
   90-minute one, and the four systems here span eight decades of time. */
const GO_ETA = 0.02;
function goLimit(S){
  let tau = Infinity;
  for(let i = 0; i < S.n; i++) for(let j = i + 1; j < S.n; j++){
    const dx = S.x[j] - S.x[i], dy = S.y[j] - S.y[i], r = Math.hypot(dx, dy);
    const boosted = S.boost !== 1 && ((S.kind[i] === 'moon' && S.kind[j] === 'planet') ||
                                      (S.kind[j] === 'moon' && S.kind[i] === 'planet'));
    const k = boosted ? S.boost : 1;
    tau = Math.min(tau, Math.sqrt(r * r * r / (k * G_SI * (S.m[i] + S.m[j]))));
    const dv = Math.hypot(S.vx[j] - S.vx[i], S.vy[j] - S.vy[i]);
    if(dv > 0) tau = Math.min(tau, r / dv);
  }
  return isFinite(tau) ? GO_ETA * tau : Infinity;
}
/* advance by dt.  With gravity OFF this is PhET's getNextCoastingState: one drift and nothing
   else, so the bodies move in exactly straight lines at exactly constant speed. */
function goAdvance(S, dt, gravity, stepFn){
  if(!gravity){ goDrift(S, dt); return 1; }
  const lim = goLimit(S);
  const n = Math.max(1, Math.ceil(Math.abs(dt) / lim));
  const h = dt / n, step = stepFn || goPefrl;
  for(let k = 0; k < n; k++) step(S, h);
  return n;
}
/* the rotation of a body with a rotation period (PhET spins the moon and the station) */
function goRotation(S, i, t){
  const p = S.rot[i];
  return p ? TAU * (t / p) : 0;
}

/* ---- the exact answers ------------------------------------------------------------------
   A FIXED star makes the scene a one-body problem about mu = G M; two free bodies reduce to
   the relative orbit about mu = G(m1+m2) with the centre of mass drifting in a straight line.
   Both are Kepler conics, and both are solved by the shared engine's conicFromState /
   stateOnConic (Newton on E - e sin E = M, safeguarded, to 1e-15 in the step). */
function goTwoBody(S){
  if(S.n !== 2) return null;
  if(S.fix[0] && !S.fix[1]){
    const mu = G_SI * S.m[0];
    return {kind: 'fixed', mu, el: conicFromState(S.x[1] - S.x[0], S.y[1] - S.y[0], S.vx[1], S.vy[1], mu),
            cx: S.x[0], cy: S.y[0]};
  }
  const mu = G_SI * (S.m[0] + S.m[1]);
  const el = conicFromState(S.x[1] - S.x[0], S.y[1] - S.y[0], S.vx[1] - S.vx[0], S.vy[1] - S.vy[0], mu);
  const c = nbodyCom(S);
  return {kind: 'free', mu, el, cx: c.x, cy: c.y, cvx: c.vx, cvy: c.vy,
          f1: S.m[1] / (S.m[0] + S.m[1]), f2: S.m[0] / (S.m[0] + S.m[1])};
}
function goTwoBodyAt(ref, t){
  const s = stateOnConic(ref.el, t);
  if(ref.kind === 'fixed')
    return {x1: ref.cx, y1: ref.cy, vx1: 0, vy1: 0,
            x2: ref.cx + s.x, y2: ref.cy + s.y, vx2: s.vx, vy2: s.vy, rel: s};
  const cx = ref.cx + ref.cvx * t, cy = ref.cy + ref.cvy * t;
  return {x1: cx - ref.f1 * s.x, y1: cy - ref.f1 * s.y,
          vx1: ref.cvx - ref.f1 * s.vx, vy1: ref.cvy - ref.f1 * s.vy,
          x2: cx + ref.f2 * s.x, y2: cy + ref.f2 * s.y,
          vx2: ref.cvx + ref.f2 * s.vx, vy2: ref.cvy + ref.f2 * s.vy, rel: s};
}
/* the circular-orbit condition, and its period.  These two lines are the subject of view 3. */
function circSpeed(M, r){ return Math.sqrt(G_SI * M / r); }
function circPeriod(M, r){ return TAU * Math.sqrt(r * r * r / (G_SI * M)); }

/* ---- PhET's own readouts ----------------------------------------------------------------- */
/* EarthMassReadoutNode: > 1000 Earth masses reads in thousands, within 1 % of one reads
   "1 Earth mass", otherwise two decimals of Earth masses. */
function earthMassStr(m){
  const e = m / PH.EARTH_MASS;
  if(e > 1000) return fmt(Math.round(e / 1000), 0) + ' thousand Earth masses';
  if(Math.abs(e - 1) < 0.01) return '1 Earth mass';
  return fmt(e, 2) + ' Earth masses';
}
/* SpaceStationMassReadoutNode: the same idea in units of the station itself */
function stationMassStr(m){
  const e = m / PH.STATION_MASS;
  if(e > 1e18) return fmt(e / 1e18, 0) + ' billion billion Space Station masses';
  if(Math.abs(e - 1) < 0.01) return '1 Space Station Mass';
  return fmt(e, e < 1 ? 3 : 2) + ' Space Station Mass';
}
function massReadout(S, i, sid){
  return sid === 'planetSatellite' ? stationMassStr(S.m[i]) : earthMassStr(S.m[i]);
}
/* Digit superscripts.  There is no Unicode superscript for most letters and the ones that
   exist are not all in the rasteriser's font, so only digits are safe on the canvas. */
const SUPD = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹'];
function supNum(n){
  const s = String(Math.abs(Math.round(n)));
  let out = n < 0 ? '⁻' : '';
  for(const ch of s) out += SUPD[+ch];
  return out;
}
/* The shared sigf() renders a big number as "7.3549×10^+7"; the caret and the plus are noise
   on a canvas, so the exponent is turned into a real superscript here rather than by editing
   the helper three sims share. */
function sci(x, n){
  const s = sigf(x, n);
  const i = s.indexOf('×10^');
  return i < 0 ? s : s.slice(0, i) + '×10' + supNum(parseInt(s.slice(i + 4), 10));
}
/* lengths: PhET's measuring tape reads kilometres; anything bigger gets a unit that fits */
function lenStr(m, sig){
  const a = Math.abs(m), s = sig || 4;
  if(a >= 0.1 * AU_M) return sci(m / AU_M, s) + ' AU';
  if(a >= 1e9) return sci(m / 1e9, s) + ' Gm';
  if(a >= 1e6) return sci(m / 1e6, s) + ' Mm';
  return sci(m / 1e3, s) + ' km';
}
function kmStr(m, sig){ return sci(m / 1e3, sig || 4) + ' km'; }
/* times: PhET's clock reads Earth days, and Earth minutes on the space-station scene */
function timeStr(t, minutes){
  if(minutes) return fmt(t / 60, 0) + ' Earth minutes';
  return fmt(t / PH.DAY, 0) + ' Earth days';
}
function timeStrFine(t, minutes){
  if(minutes) return fmt(t / 60, 2) + ' min';
  const d = t / PH.DAY;
  return Math.abs(d) < 1 ? fmt(d * 24, 2) + ' h' : fmt(d, 3) + ' d';
}
