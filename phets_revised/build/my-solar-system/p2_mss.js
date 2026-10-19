
/* ================================================================== *
 *  My Solar System: PhET's units, its orbital systems, and the state  *
 *  of a running system (the bodies, their paths and their clock)      *
 * ================================================================== */
/* measured / defined */
const AU_KM = 149597870.7;                 /* IAU 2012 B2, exact by definition */
const AU_M = AU_KM * 1e3;
const YR_S = 365.25 * 86400;               /* the Julian year, exact by definition */
const G_SI = 6.6743e-11;                   /* CODATA; PhET writes it as 66743e-15 */
const MASS_UNIT = 1e28;                    /* kg, PhET's mass unit */
const DEG = PI / 180;                      /* DEG converts degrees INTO radians */

/* PhET's values, read out of docs/phets/my-solar-system_en.html (1.3.16) */
const G_MSS = 4.4567;                      /* SOLAR_SYSTEM_COMMON, AU (km/s)^2 per 1e28 kg */
/* PhET solves its time unit from its own G, so a "km/s" here is 1.000538 true km/s */
const TIME_MULT = Math.pow(0.01, 1.5) * Math.sqrt(G_MSS) * Math.pow(AU_M, 1.5)
                  / (Math.sqrt(G_SI) * Math.sqrt(MASS_UNIT) * YR_S);
const T_U_YR = 1000 * TIME_MULT;           /* one model time unit, in Julian years */
const G_SI_UNITS = G_SI * MASS_UNIT / (AU_M * 1e6);   /* what G is in these units from CODATA */
const KMS_TRUE = AU_KM / (T_U_YR * YR_S);  /* what one model velocity unit really is, km/s */
const PHET = {
  ENGINE_SCALE: 0.05,                      /* model units per second of wall clock */
  FRAME: 0.05 / 60,                        /* ... so one 1/60-s frame at normal speed */
  MASS_MIN: 0.1, MASS_MAX: 300,            /* the mass slider (1e28 kg) */
  PATH_AU: 20, PATH_PTS: 5800,             /* MAX_PATH_DISTANCE, MAX_PATH_POINTS */
  ZOOM_MIN: 1, ZOOM_MAX: 6, ZOOM_DEF: 4,   /* zoomLevelRange; scale 25..125 view units per AU */
  ZOOM_LO: 25, ZOOM_HI: 125,
  SUBSTEPS: 4000,                          /* its engine takes 4000/N substeps per call */
  FORCE_POW_MIN: -2, FORCE_POW_MAX: 8      /* gravityForceScalePowerProperty */
};
const NBODY_ETA_MSS = NBODY_ETA;           /* 0.02, the shared engine's step limit */

/* PhET's eleven orbital systems: [mass (1e28 kg), x, y (AU), vx, vy (km/s)] */
const PRESETS = [
  {id: 'sunPlanet', name: 'Sun, planet', bodies: [[250, 0, 0, 0, -2.3446], [25, 2, 0, 0, 23.4457]]},
  {id: 'sunPlanetMoon', name: 'Sun, planet, moon',
   bodies: [[200, 0, 0, 0, 0], [10, 1.6, 0, 0, 25.3467], [1e-6, 1.4, 0, 0, 11.1948]]},
  {id: 'sunPlanetComet', name: 'Sun, planet, comet',
   bodies: [[200, 0, 0, 0, 0], [1, 1.5, 0, 0, 25.3467], [1e-6, -2.2, 1.3, -4.2244, -7.3928]]},
  {id: 'trojan', name: 'trojan asteroids',
   bodies: [[200, 0, 0, 0, 0], [5, 1.5, 0, 0, 25.1355], [1e-6, 0.75, -1.3, 21.7559, 12.6733],
            [1e-6, 0.75, 1.3, -21.7559, 12.6733]]},
  {id: 'ellipses', name: 'ellipses',
   bodies: [[250, -1, 0, 0, 0], [1e-6, -0.15, 0, 0, 31.8946], [1e-6, 1.5, 0, 0, 12.6733],
            [1e-6, 3.2, 0, 0, 7.8152]]},
  {id: 'hyperbolic', name: '\u201chyperbolic\u201d',      /* literal quotes: plain() has no &ldquo; */
   bodies: [[250, 0, 0.25, 0, 0], [1e-6, -2.5, -0.7, 25.3467, 0], [1e-6, -2.5, -1.4, 25.3467, 0],
            [1e-6, -2.5, -2.1, 25.3467, 0]]},
  {id: 'slingshot', name: 'slingshot',
   bodies: [[200, 0.01, 0, 0, -0.2112], [10, 1.31, 0.55, -11.6172, 24.2906], [1e-6, -0.06, -1.28, 17.5315, 0]]},
  {id: 'doubleSlingshot', name: 'double slingshot',
   bodies: [[200, 0, 0, 0, -0.2112], [5, 0, -1.12, 28.3038, 0], [5, 1.86, -0.05, 0.2112, 23.4457],
            [1e-6, 0.7, 0.72, -9.9275, 13.307]]},
  {id: 'binaryPlanet', name: 'binary star, planet',
   bodies: [[150, -1, 0, 0, -12.6733], [120, 1, 0, 0, 10.5611], [1e-6, -0.5, 0, 0, 25.3467]]},
  {id: 'fourStar', name: 'four star ballet',
   bodies: [[120, -1, 1, -10.5611, -10.5611], [120, 1, 1, -10.5611, 10.5611], [120, 1, -1, 10.5611, 10.5611],
            [120, -1, -1, 10.5611, -10.5611]]},
  {id: 'doubleDouble', name: 'double double',
   bodies: [[60, -1.15, -0.03, 0, -32.5283], [70, 1.02, 0, 0.2112, 31.6834], [55, -0.77, -0.02, -0.2112, 8.8713],
            [62, 1.35, 0, -0.2112, -10.9836]]},
  {id: 'custom', name: 'custom', bodies: null}
];
function presetById(id){ const p = PRESETS.find(p => p.id === id); if(!p) throw new Error('no orbital system ' + id); return p; }
/* PhET's own colours for the four bodies (yellow, magenta, cyan, green) */
const BODY_COL = ['#f2c14e', '#cd35c4', '#5ac8e0', '#b8ec4c'];
/* the four bodies a Lab system falls back on when one is added (PhET's defaultBodyInfo) */
const SPARE = [[0.1, 3, 0, 0, 10], [0.1, -3, 0, 0, -10], [0.1, 0, 3, -10, 0], [0.1, 0, -3, 10, 0]];

function yrOf(t){ return t * T_U_YR; }                      /* model time -> Julian years */
function kmsTrue(v){ return v * KMS_TRUE; }                 /* PhET's "km/s" -> true km/s */

/* ---- a running system ------------------------------------------------------------------- */
function sysFromBodies(list, followCom){
  const m = list.map(b => b[0]), x = list.map(b => b[1]), y = list.map(b => b[2]),
        vx = list.map(b => b[3]), vy = list.map(b => b[4]);
  const S = nbodyMake(m, x, y, vx, vy);
  if(followCom){                       /* PhET's followCenterOfMass on every preset it loads */
    const c = nbodyCom(S);
    for(let i = 0; i < S.n; i++){ S.vx[i] -= c.vx; S.vy[i] -= c.vy; }
  }
  const sys = {S, col: list.map((b, i) => i), t: 0, paths: list.map(() => []), plen: list.map(() => 0),
               merged: [], start: [], startCom: followCom};
  /* AFTER the subtraction, not before: the start is what restart returns to, and PhET's own
     load leaves the centre of mass at rest */
  sysSaveStart(sys);
  return sys;
}
function sysLoad(id, nb){
  const p = presetById(id);
  /* a named system brings its own bodies and its own count; nb only sizes a custom one */
  const list = p.bodies ? p.bodies.map(b => b.slice()) : SPARE.slice(0, nb || 2).map(b => b.slice());
  return sysFromBodies(list, !!p.bodies);
}
/* the state the restart button returns to: PhET saves it whenever the user lets go */
function sysSaveStart(sys){
  sys.start = [];
  for(let i = 0; i < sys.S.n; i++) sys.start.push([sys.S.m[i], sys.S.x[i], sys.S.y[i], sys.S.vx[i], sys.S.vy[i]]);
  sys.startCol = sys.col.slice();
  /* the clock reading this start was taken at.  The centre-of-mass button saves a start
     WITHOUT stopping the clock, so a saved start is not always at t = 0, and the exact
     two-body orbit anchored on it has to be read from here, not from zero. */
  sys.t0 = sys.t;
}
function sysRestart(sys){
  const list = sys.start.map(b => b.slice());
  const S = nbodyMake(list.map(b => b[0]), list.map(b => b[1]), list.map(b => b[2]),
                      list.map(b => b[3]), list.map(b => b[4]));
  sys.S = S; sys.t = 0; sys.t0 = 0; sys.merged = [];
  sys.col = sys.startCol ? sys.startCol.slice() : list.map((b, i) => i);
  sys.paths = list.map(() => []); sys.plen = list.map(() => 0);
}
function sysSetN(sys, n){
  const list = [];
  for(let i = 0; i < n; i++){
    if(i < sys.S.n) list.push([sys.S.m[i], sys.S.x[i], sys.S.y[i], sys.S.vx[i], sys.S.vy[i]]);
    else list.push(SPARE[i].slice());
  }
  const keep = sys.col.slice(0, n);
  while(keep.length < n) keep.push(keep.length);
  sys.S = nbodyMake(list.map(b => b[0]), list.map(b => b[1]), list.map(b => b[2]), list.map(b => b[3]), list.map(b => b[4]));
  sys.col = keep; sys.paths = list.map(() => []); sys.plen = list.map(() => 0); sys.merged = [];
  sysSaveStart(sys);
}
/* the centre-of-mass frame: PhET's "Follow Center of Mass" subtracts both */
function sysComFrame(sys){
  const c = nbodyCom(sys.S);
  for(let i = 0; i < sys.S.n; i++){
    sys.S.x[i] -= c.x; sys.S.y[i] -= c.y; sys.S.vx[i] -= c.vx; sys.S.vy[i] -= c.vy;
  }
  sysClearPaths(sys); sysSaveStart(sys);
}
function sysClearPaths(sys){ sys.paths = []; sys.plen = []; for(let i = 0; i < sys.S.n; i++){ sys.paths.push([]); sys.plen.push(0); } }
/* PhET keeps at most 20 AU of path (MAX_PATH_DISTANCE) and 5800 points */
function sysAddPath(sys){
  for(let i = 0; i < sys.S.n; i++){
    const p = sys.paths[i], x = sys.S.x[i], y = sys.S.y[i];
    if(p.length){
      const last = p[p.length - 1], d = Math.hypot(x - last[0], y - last[1]);
      if(d === 0) continue;
      p.push([x, y]); sys.plen[i] += d;
      while(sys.plen[i] > PHET.PATH_AU || p.length > PHET.PATH_PTS){
        sys.plen[i] -= Math.hypot(p[1][0] - p[0][0], p[1][1] - p[0][1]); p.shift();
      }
    } else p.push([x, y]);
  }
}
/* one frame: advance, merge anything touching, extend the paths */
function sysStep(sys, dt, keepPaths){
  const nsub = nbodyAdvance(sys.S, G_MSS, dt, NBODY_ETA_MSS);
  const merges = nbodyCollide(sys.S);
  for(const mg of merges){
    sys.merged.push({x: mg.x, y: mg.y, t: sys.t, m: mg.m});
    sys.col.splice(mg.gone, 1);
    sys.paths.splice(mg.gone, 1); sys.plen.splice(mg.gone, 1);
  }
  sys.t += dt;
  if(keepPaths) sysAddPath(sys);
  return {nsub, merges};
}
/* PhET's own engine, as shipped, run beside ours for the comparison: 4000/N substeps a frame,
   one force evaluation each, the PEFRL coefficients applied to that single acceleration */
function phetShadowStep(S, dt){
  const n = Math.max(1, Math.round(PHET.SUBSTEPS / S.n));
  const h = dt / n;
  for(let k = 0; k < n; k++) phetStep(S, G_MSS, h);
  return n;
}
/* the two-body reduction, for the exact view and the suites */
function sysTwoBody(sys){ return sys.S.n === 2 ? twoBodyReduce(sys.S, G_MSS) : null; }
/* how far a body is from the centre of mass, in units of its own radius: used to decide
   whether the "return bodies" button is offered (PhET offers it when one goes off screen) */
function sysOffscreen(sys, R){
  for(let i = 0; i < sys.S.n; i++) if(Math.abs(sys.S.x[i]) > R * 1.6 || Math.abs(sys.S.y[i]) > R * 1.6) return true;
  return false;
}
