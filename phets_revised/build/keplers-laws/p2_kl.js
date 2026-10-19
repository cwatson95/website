
/* ================================================================== *
 *  Kepler's Laws: the units, PhET's rules, and the model of one orbit *
 * ================================================================== */
/* measured / defined (sources in the header comment; pinned in selfTest to
   build/keplers-laws/derive.py, which prints them from these same three) */
const AU_KM = 149597870.7;                      /* IAU 2012 B2, exact by definition */
const YR_S = 365.25 * 86400;                    /* the Julian year, exact by definition */
const GM_SUN = 1.32712440042e20;                /* m^3 s^-2, Wikipedia "Standard gravitational parameter" */
const K_SUN = GM_SUN * YR_S * YR_S / Math.pow(AU_KM * 1e3, 3);   /* AU^3 yr^-2 per solar mass */
const KMS = AU_KM / YR_S;                       /* km/s per AU/yr */
const DEG = PI / 180;    /* the house convention: DEG converts degrees INTO radians, so a value
                            in radians is PRINTED as x/DEG (Known-bad: bloch_sphere read it the
                            other way at nineteen call sites) */

/* PhET's values, read out of docs/phets/keplers-laws_en.html (Kepler's Laws 1.2.12) */
const PHET = {
  G: 4.4567,                 /* SOLAR_SYSTEM_COMMON, AU (km/s)^2 per 1e28 kg */
  SUN: 200,                  /* KeplersLawsConstants.MASS_OF_OUR_SUN, 1e28 kg */
  PLANET: 50,                /* KeplersLawsConstants.PLANET_MASS, 1e28 kg (it does not enter the orbit) */
  MU_COEFF: 4.45669,         /* EllipticalOrbitEngine: mu = 4.45669 M */
  MU_NORM: 891.34,           /* ... and T = sqrt(a^3 891.34 / mu) years */
  R0: [2, 0], V0: [0, 17.2358],
  DIV_MIN: 2, DIV_MAX: 6, DIV_DEF: 4,
  NEWTON_TOL: 0.01,          /* its Newton loop stops once a step is below this */
  CLOCK: 6.3,                /* 500 / (1000/12.6): the mean anomaly it adds per year, times T */
  E_ROUND: 0.01,             /* eccentricity shown as 0 below this */
  ESC_CAP: 0.99, ESC_FLAG: 0.9801,
  FRAME_YR: (1 / 60) * 0.002 * (1000 / 12.6)    /* one frame at normal speed: 1/378 yr */
};
/* PhET's target orbits (e, a), drawn with periapsis toward +x */
const TARGETS = [
  {id: 'none', name: 'none'},
  {id: 'mercury', name: 'Mercury', e: 0.2056, a: 0.4},
  {id: 'venus', name: 'Venus', e: 0.0068, a: 0.7},
  {id: 'earth', name: 'Earth', e: 0.0167, a: 1},
  {id: 'mars', name: 'Mars', e: 0.0934, a: 1.5},
  {id: 'jupiter', name: 'Jupiter', e: 0.0484, a: 5.2}
];
function targetById(id){ const t = TARGETS.find(t => t.id === id); if(!t) throw new Error('no target ' + id); return t; }

function starMu(M){ return K_SUN * M; }                    /* M in solar masses */
/* PhET's massToRadius on PhET's mass number (200 per solar mass) */
function starRadius(M){ return massToRadius(PHET.SUN * M); }
function kmsToAuYr(v){ return v / KMS; }
function auYrToKms(v){ return v * KMS; }

/* ---- the orbit of one planet about a fixed star -------------------------------------------
   PhET's rules, kept: the speed is capped at 0.99 of the escape speed, the orbit is flagged
   as escaping from 0.9801 of it, and an orbit whose periapsis lies inside the star crashes.
   A flagged orbit is drawn but not run (PhET disables play through playingAllowedProperty). */
function klOrbit(px, py, vxk, vyk, M, circular){
  const mu = starMu(M);
  let x = px, y = py;
  let r = Math.hypot(x, y);
  if(!(r > 0)){ x = 0.01; y = 0; r = 0.01; }               /* PhET's enforceValidPosition */
  let vx = kmsToAuYr(vxk), vy = kmsToAuYr(vyk);
  const vesc = escapeSpeed(r, mu);
  if(circular){
    const vc = Math.sqrt(mu / r), s = (x * vy - y * vx) >= 0 ? 1 : -1;
    vx = -s * vc * y / r; vy = s * vc * x / r;
  }
  let sp = Math.hypot(vx, vy);
  const escaping = sp >= PHET.ESC_FLAG * vesc;
  if(sp >= PHET.ESC_CAP * vesc){                            /* PhET's enforceEscapeSpeed */
    const f = PHET.ESC_CAP * vesc / sp; vx *= f; vy *= f; sp = PHET.ESC_CAP * vesc;
  }
  const el = conicFromState(x, y, vx, vy, mu);
  const R = starRadius(M);
  const crash = el.q < R;
  el.star = R; el.M_sun = M; el.escaping = escaping; el.crash = crash;
  el.allowed = !escaping && !crash;
  el.vKms = auYrToKms(el.v); el.vescKms = auYrToKms(vesc);
  el.eShown = el.e < PHET.E_ROUND ? 0 : el.e;               /* PhET rounds e below 0.01 to 0 */
  el.px = x; el.py = y; el.vx = vx; el.vy = vy;
  return el;
}
/* the state a time t later, in the sim's own units (AU and km/s) */
function klStateAt(el, t){
  const s = stateOnConic(el, t);
  return {x: s.x, y: s.y, vx: auYrToKms(s.vx), vy: auYrToKms(s.vy), E: s.anom, M: s.M, r: s.r,
          v: Math.hypot(s.vx, s.vy), vKms: auYrToKms(Math.hypot(s.vx, s.vy)),
          nu: trueFromE(s.anom, el.e)};
}
/* the two foci: the star sits at the origin, the empty one 2c along the anti-periapsis */
function klFoci(el){
  const cw = Math.cos(el.w), sw = Math.sin(el.w);
  return {f1: [0, 0], f2: [-2 * el.c * cw, -2 * el.c * sw], centre: [-el.c * cw, -el.c * sw]};
}

/* ---- the second law: N sectors of equal area, cut at equal steps of mean anomaly ---------- */
function klSectors(el, N){
  const out = [];
  for(let k = 0; k <= N; k++){
    const E = keplerE(TAU * k / N, el.e);
    out.push(trueFromE(E, el.e));            /* true anomalies of the cuts, 0 .. 2 pi */
  }
  return out;
}
/* how much of each sector is painted.  Before the clock runs (or after an erase while
   paused) every sector shows its full area; once erased the sectors fill as the planet
   sweeps them, from each sector's own starting cut (PhET's rule), and stay full. */
function klSwept(el, N, tNow, sweep){
  const D = TAU / N, full = PI * el.a * el.b / N;
  const fr = new Array(N).fill(0);
  if(!sweep.erased){ for(let k = 0; k < N; k++) fr[k] = 1; return {frac: fr, full}; }
  const Me = el.M0 + el.n * sweep.tErase, Mn = el.M0 + el.n * tNow;
  if(Mn - Me >= TAU){ for(let k = 0; k < N; k++) fr[k] = 1; return {frac: fr, full}; }
  const je = Math.floor(Me / D), jn = Math.floor(Mn / D);
  for(let j = je; j <= jn; j++){
    const k = ((j % N) + N) % N;
    fr[k] = Math.max(fr[k], j < jn ? 1 : clamp((Mn - j * D) / D, 0, 1));
  }
  return {frac: fr, full};
}
/* the polygon of one sector: the star, then the arc from cut k to cut k+1 (to the planet if
   the sector is only part swept) */
function klSectorPoly(el, nu0, nu1, nSeg){
  const pts = [[0, 0]];
  const n = nSeg || 48;
  for(let i = 0; i <= n; i++) pts.push(conicPoint(el, nu0 + (nu1 - nu0) * i / n));
  return pts;
}
/* the true anomaly a fraction f of the way through sector k (by mean anomaly, i.e. by time) */
function klSweepNu(el, N, k, f){
  const D = TAU / N;
  return trueFromE(keplerE(D * (k + f), el.e), el.e);
}

/* ---- the third law ----------------------------------------------------------------------- */
function klThird(el, pa, pt){
  const ap = Math.pow(el.a, pa), Tp = Math.pow(el.T, pt);
  return {ap, Tp, ratio: Tp / ap, correct: pa === 3 && pt === 2};
}
/* T^2/a^3 = 4 pi^2 / GM: the constant belongs to the star, not to the planet */
function klConst(M){ return TAU * TAU / starMu(M); }
