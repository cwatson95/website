
/* ================================================================== *
 *  physics — hydrogen, exactly; and PhET's own model constants,      *
 *  read out of the minified build 1.0.9 and labelled as PhET's.      *
 *  Twin: build/models-of-the-hydrogen-atom/derive.py                 *
 * ================================================================== */

/* DEG converts degrees INTO radians and RAD converts radians INTO degrees.
   A constant named after a unit does not say which way it goes, and reading
   this pair backwards once put a factor of 3283 on every angle in
   bloch_sphere.html (Known-bad).  selfTest pins DEG*90 = pi/2. */
const DEG = PI / 180, RAD = 180 / PI;

/* ---- CODATA 2022, from scipy.constants (derive.py section 1) ------------- */
const R_INF   = 10973731.568157;        /* Rydberg constant, m^-1              */
const RYD_EV  = 13.60569312299;         /* R_inf h c, eV (infinite nuclear mass)*/
const A0      = 5.29177210544e-11;      /* Bohr radius, m                       */
const ALPHA   = 0.0072973525643;        /* fine-structure constant              */
const C_LIGHT = 299792458;              /* m/s, exact by definition             */
const ME_MP   = 0.00054461702149015;    /* electron / proton mass               */
/* the electron-proton reduced mass: every wavelength of real hydrogen needs it,
   and it moves the lines by 5.4e-4 — 350 times the residual against NIST */
const MU_ME   = 1 / (1 + ME_MP);
const R_H     = R_INF * MU_ME;          /* m^-1 */
const RH_EV   = RYD_EV * MU_ME;         /* eV   */
const NMAX    = 6;                      /* PhET's ceiling; the sim keeps it     */

function energyEV(n){ return -RH_EV / (n * n); }                 /* reduced mass */
function energyEVinf(n){ return -RYD_EV / (n * n); }
function orbitRadius(n){ return n * n * A0; }                    /* m            */
function orbitSpeed(n){ return ALPHA * C_LIGHT / n; }            /* m/s          */
/* the vacuum wavelength of the n2 -> n1 transition, in nm */
function lamVac(n1, n2){ return 1e9 / (R_H * (1 / (n1 * n1) - 1 / (n2 * n2))); }
function lamVacInf(n1, n2){ return 1e9 / (R_INF * (1 / (n1 * n1) - 1 / (n2 * n2))); }
function seriesLimit(n1){ return 1e9 / (R_H / (n1 * n1)); }
const SERIES_NAME = ['', 'Lyman', 'Balmer', 'Paschen', 'Brackett', 'Pfund', 'Humphreys'];
/* de Broglie wavelength of the electron in orbit n, m.  Analytically
   lambda_dB = h/(m v_n) = 2 pi a_0 n, so n*lambda_dB = 2 pi r_n is an identity
   — but m_e, a_0 and alpha are three SEPARATELY rounded CODATA values, so it
   only closes to 5.178e-12 here.  m_e is taken from CODATA rather than derived
   from a_0 and alpha, so that residual is real and the assertion has teeth. */
const H_PLANCK = 6.62607015e-34;        /* J s, exact by definition (SI 2019)   */
const M_E      = 9.1093837139e-31;      /* kg, CODATA 2022 (scipy.constants)    */
function lamDeBroglie(n){ return H_PLANCK / (M_E * orbitSpeed(n)); }

/* ---- PhET's own wavelength table --------------------------------------
   PhET: round(1240 / (13.6 (1/n1^2 - 1/n2^2))), integer nanometres, n <= 6.
   1240 eV nm and 13.6 eV are PhET's values; the true hc is 1239.841984 eV nm
   and the true R_H h c is 13.598287 eV. */
const PHET_HC = 1240, PHET_RYD = 13.6;
function phetLam(n1, n2){
  return Math.round(PHET_HC / (PHET_RYD * (1 / (n1 * n1) - 1 / (n2 * n2))));
}
const TRANSITIONS = [];                 /* every (n1,n2) with n2 > n1, n2 <= 6 */
for(let a = 1; a < NMAX; a++) for(let b = a + 1; b <= NMAX; b++)
  TRANSITIONS.push({n1: a, n2: b, phet: phetLam(a, b), exact: lamVac(a, b)});
const PHET_LAMS = TRANSITIONS.map(t => t.phet);
/* PhET maps an integer wavelength back to a transition; two different
   transitions never round to the same integer (asserted) */
function transitionForPhetLam(w){
  for(const t of TRANSITIONS) if(t.phet === w) return t;
  return null;
}
function phetHigherState(n, w){
  for(let b = n + 1; b <= NMAX; b++) if(phetLam(n, b) === w) return b;
  return null;
}
function phetLowerState(n, w){
  for(let a = 1; a < n; a++) if(phetLam(a, n) === w) return a;
  return null;
}
function phetGroundAbsorptionLams(){
  const out = [];
  for(let b = 2; b <= NMAX; b++) out.push(phetLam(1, b));
  return out;
}

/* ---- hydrogen wavefunctions (a_0 = 1 throughout) ------------------------ */
function factorial(k){ let f = 1; for(let i = 2; i <= k; i++) f *= i; return f; }
function binom(n, k){
  if(k < 0 || k > n) return 0;
  let r = 1;
  for(let i = 0; i < k; i++) r = r * (n - i) / (i + 1);
  return Math.round(r);
}
/* the generalised Laguerre polynomial L_k^a(x), by the three-term recurrence.
   Used only as the independent check on the polynomial coefficients below. */
function laguerreL(k, a, x){
  if(k === 0) return 1;
  if(k === 1) return 1 + a - x;
  let p0 = 1, p1 = 1 + a - x;
  for(let i = 1; i < k; i++){
    const p2 = ((2 * i + 1 + a - x) * p1 - (i + a) * p0) / (i + 1);
    p0 = p1; p1 = p2;
  }
  return p1;
}
/* R_nl(r) = exp(-r/n) * sum_k coef[k] r^k.  Exact coefficients: the sum form of
   L_{n-l-1}^{2l+1} is  sum_k (-1)^k C(n+l, n-l-1-k) rho^k / k!  with rho = 2r/n. */
const _RPOLY = {};
function rnlPoly(n, l){
  const key = n + ',' + l;
  if(_RPOLY[key]) return _RPOLY[key];
  const norm = Math.sqrt(Math.pow(2 / n, 3) * factorial(n - l - 1) / (2 * n * factorial(n + l)));
  const co = new Array(n).fill(0);
  for(let k = 0; k <= n - l - 1; k++){
    const term = (k % 2 ? -1 : 1) * binom(n + l, n - l - 1 - k) / factorial(k) * Math.pow(2 / n, k);
    co[l + k] += norm * Math.pow(2 / n, l) * term;
  }
  _RPOLY[key] = co;
  return co;
}
function Rnl(n, l, r){
  const co = rnlPoly(n, l);
  let s = 0;
  for(let k = co.length - 1; k >= 0; k--) s = s * r + co[k];
  return s * Math.exp(-r / n);
}
/* the same thing through laguerreL — a second implementation, asserted equal */
function RnlDirect(n, l, r){
  const rho = 2 * r / n;
  const norm = Math.sqrt(Math.pow(2 / n, 3) * factorial(n - l - 1) / (2 * n * factorial(n + l)));
  return norm * Math.exp(-rho / 2) * Math.pow(rho, l) * laguerreL(n - l - 1, 2 * l + 1, rho);
}
/* associated Legendre P_l^m(x) for 0 <= m <= l, |x| <= 1, Condon-Shortley phase */
function legendreP(l, m, x){
  m = Math.abs(m);
  if(m > l) return 0;
  let pmm = 1;
  if(m > 0){
    const somx2 = Math.sqrt(Math.max(0, 1 - x * x));
    let f = 1;
    for(let i = 1; i <= m; i++){ pmm *= -f * somx2; f += 2; }
  }
  if(l === m) return pmm;
  let pmmp1 = x * (2 * m + 1) * pmm;
  if(l === m + 1) return pmmp1;
  let pll = 0;
  for(let ll = m + 2; ll <= l; ll++){
    pll = ((2 * ll - 1) * x * pmmp1 - (ll + m - 1) * pmm) / (ll - m);
    pmm = pmmp1; pmmp1 = pll;
  }
  return pll;
}
/* |Y_l^m(theta, phi)|^2 — no phi dependence, which is why the drawn cloud is
   a figure of revolution about z */
function ylmSq(l, m, cosTh){
  const am = Math.abs(m);
  const p = legendreP(l, am, cosTh);
  return (2 * l + 1) / (4 * PI) * factorial(l - am) / factorial(l + am) * p * p;
}
function psiSq(n, l, m, x, y, z){
  const r = Math.sqrt(x * x + y * y + z * z);
  const cth = r > 0 ? clamp(z / r, -1, 1) : 1;
  const R = Rnl(n, l, r);
  return R * R * ylmSq(l, m, cth);
}
function radialProb(n, l, r){ const R = Rnl(n, l, r); return r * r * R * R; }
/* <r>, <r^2>, <1/r> in a_0 — closed forms, asserted against quadrature */
function meanR(n, l){ return (3 * n * n - l * (l + 1)) / 2; }
function meanR2(n, l){ return n * n * (5 * n * n + 1 - 3 * l * (l + 1)) / 2; }
function meanInvR(n){ return 1 / (n * n); }
function radialNodes(n, l){ return n - l - 1; }
function angularNodes(l, m){ return l - Math.abs(m); }
/* the column density the cloud view paints: integrate |psi|^2 along the line of
   sight y, Simpson on [0, ymax] doubled by symmetry.  ymax and the panel count
   follow the state's own size, not a fixed number (Known-bad: resolution must
   follow the structure). */
function columnDensity(n, l, m, x, z, panels){
  const ymax = 30 + 14 * n * n;
  /* the integrand varies on the scale of n a_0, so the step follows n, not the
     range: a fixed panel count tuned on n = 6 is 40x too coarse at n = 1 and
     the 1s column came out 1e-5 low (Known-bad: resolution follows the
     structure).  N is forced even for Simpson. */
  const N = panels || 2 * Math.ceil(ymax / (0.1 * n));
  const hstep = ymax / N;
  let s = psiSq(n, l, m, x, 0, z) + psiSq(n, l, m, x, ymax, z);
  for(let i = 1; i < N; i++) s += (i % 2 ? 4 : 2) * psiSq(n, l, m, x, i * hstep, z);
  return 2 * s * hstep / 3;
}

/* ---- Einstein A coefficients ------------------------------------------
   A(n_u l_u -> n_l l_l), averaged over m_u and summed over m_l, in s^-1:
      A = (4/3) alpha^3 omega^3 (max(l)/(2 l_u + 1)) |R|^2   [atomic units]
   with omega in hartree and R the radial dipole integral in a_0.  The integral
   is exact: both radial functions are a polynomial times exp(-r/n), so the
   integrand is a polynomial times exp(-s r) and int r^k e^{-sr} dr = k!/s^{k+1}. */
const T_AU = 2.4188843265863e-17;       /* hbar / E_h, s (derive.py) */
function radialDipole(n1, l1, n2, l2){
  const c1 = rnlPoly(n1, l1), c2 = rnlPoly(n2, l2), s = 1 / n1 + 1 / n2;
  let tot = 0;
  for(let i = 0; i < c1.length; i++){
    if(c1[i] === 0) continue;
    for(let j = 0; j < c2.length; j++){
      if(c2[j] === 0) continue;
      const k = i + j + 3;
      tot += c1[i] * c2[j] * factorial(k) / Math.pow(s, k + 1);
    }
  }
  return tot;
}
function einsteinA(nu, lu, nl, ll){
  if(Math.abs(lu - ll) !== 1 || nu <= nl || ll > nl - 1 || ll < 0 || lu > nu - 1 || lu < 0) return 0;
  const w = 0.5 / (nl * nl) - 0.5 / (nu * nu);            /* hartree */
  const R = radialDipole(nu, lu, nl, ll);
  const lmax = Math.max(lu, ll);
  return (4 / 3) * Math.pow(ALPHA, 3) * w * w * w * (lmax / (2 * lu + 1)) * R * R / T_AU;
}
function decayRate(n, l){                                  /* s^-1 */
  let tot = 0;
  for(let np = 1; np < n; np++) for(const lp of [l - 1, l + 1]){
    if(lp < 0 || lp > np - 1) continue;
    tot += einsteinA(n, l, np, lp);
  }
  return tot;
}
function lifetimeNS(n, l){ const g = decayRate(n, l); return g > 0 ? 1e9 / g : Infinity; }
/* the rate from n to n', averaged over l with the statistical weight 2l+1 —
   the quantity PhET's chooseLower_n is standing in for */
function rateNtoN(n, np){
  let num = 0, den = 0;
  for(let l = 0; l < n; l++){
    const g = 2 * l + 1;
    den += g;
    for(const lp of [l - 1, l + 1]){
      if(lp < 0 || lp > np - 1) continue;
      num += g * einsteinA(n, l, np, lp);
    }
  }
  return num / den;
}
function trueBranching(n){
  const w = [];
  for(let np = 1; np < n; np++) w.push(rateNtoN(n, np));
  const tot = w.reduce((a, b) => a + b, 0);
  return {rates: w, frac: w.map(x => x / tot), total: tot};
}

/* ---- PhET's stochastic model (its own values) -------------------------- */
/* PhET's transition-strength table, indexed [n-1][n'-1].  Its first column is
   2 x A(np -> 1s) in units of 1e8 /s, to 0.05-1.2 % — the rest is PhET's own. */
const PHET_W = [[], [12.53], [3.34, 0.87], [1.36, 0.24, 0.07],
                [0.69, 0.11, 0, 0.04], [0.39, 0.06, 0.02, 0, 0]];
function phetLowerDist(n, l){                 /* PhET SchrodingerQuantumNumbers.chooseLower_n */
  const out = [];
  if(n === 1) return out;
  if(n === 2) return l === 0 ? out : [[1, 1]];
  /* an s state cannot go to n' = 1 (that would be s -> s), so PhET starts it
     at 2; every other l starts at l itself.  Written as ONE decision: the
     Math.max(l,1) that used to stand in front of it could only ever differ at
     l = 0, where the next line overwrote it, so its mutant was equivalent. */
  const lo = (l === 0) ? 2 : l;
  let tot = 0;
  for(let i = lo; i <= n - 1; i++){ const w = PHET_W[n - 1][i - 1]; if(w > 0){ out.push([i, w]); tot += w; } }
  if(tot === 0) return [];
  return out.map(p => [p[0], p[1] / tot]);
}
function phetChooseL(l, nNew){                /* PhET choose_l, as a distribution */
  if(l === 0) return [[1, 1]];
  if(l === nNew || l === nNew - 1) return [[l - 1, 1]];
  return [[l + 1, 0.5], [l - 1, 0.5]];
}
function phetChooseM(m, lNew){                /* PhET choose_m, as a distribution */
  if(lNew === 0) return [[0, 1]];
  if(m > lNew) return [[lNew, 1]];
  if(m < -lNew) return [[-lNew, 1]];
  if(m === lNew) return [[m, 0.5], [m - 1, 0.5]];
  if(m === -lNew) return [[m, 0.5], [m + 1, 0.5]];
  return [[m + 1, 1 / 3], [m - 1, 1 / 3], [m, 1 / 3]];
}
function validState(n, l, m){
  return n >= 1 && n <= NMAX && l >= 0 && l <= n - 1 && m >= -l && m <= l;
}
function phetTransitionAllowed(n, l, m, n2, l2, m2){
  return validState(n, l, m) && validState(n2, l2, m2) && n !== n2
      && Math.abs(l - l2) === 1 && Math.abs(m - m2) <= 1;
}

/* ---- mulberry32: the seeded PRNG, bit-identical to derive.py ------------ */
function mulberry32(seed){
  let a = seed | 0;
  return function(){
    a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function makeRng(seed){
  const f = mulberry32(seed);
  return {
    next: f,
    int: k => Math.min(k - 1, Math.floor(f() * k)),
    /* PhET's chooseWeightedValue: normalise, accumulate, take the first
       cumulative weight the draw does not exceed */
    weighted: function(items){
      let tot = 0;
      for(const it of items) tot += it[1];
      if(!(tot > 0)) return null;
      const r = f();
      let acc = 0;
      for(const it of items){ acc += it[1] / tot; if(r <= acc) return it[0]; }
      return items[items.length - 1][0];
    },
    angle: () => f() * TAU,
    sign: () => (f() < 0.5 ? -1 : 1),
  };
}

/* ---- the cascade the ensemble tests pin -------------------------------- */
/* Bohr: PhET picks the lower n uniformly on 1..n-1 */
function cascadeBohr(rng, n){
  const hops = [];
  while(n > 1){ const nl = 1 + rng.int(n - 1); hops.push([n, nl]); n = nl; }
  return hops;
}
/* Schrodinger: PhET's weighted lower n, then choose_l, choose_m, with the
   (1,0,0) fallback when the drawn triple is not an allowed transition */
function cascadeSchrodinger(rng, n, l, m){
  const hops = [];
  for(let guard = 0; guard < 200; guard++){
    const d = phetLowerDist(n, l);
    if(!d.length) break;
    const nn = rng.weighted(d);
    const lp = rng.weighted(phetChooseL(l, nn));
    const mp = rng.weighted(phetChooseM(m, lp));
    let tn = nn, tl = lp, tm = mp;
    if(!phetTransitionAllowed(n, l, m, nn, lp, mp)){ tn = 1; tl = 0; tm = 0; }
    hops.push([n, tn]);
    n = tn; l = tl; m = tm;
    if(n === 1) break;
  }
  return hops;
}

/* ---- vacuum -> standard air, Edlen 1966 (Metrologia 2, 71) -------------- */
function nAirEdlen(lamNm){
  const s2 = Math.pow(1000 / lamNm, 2);                 /* (1/lambda in um^-1)^2 */
  return 1 + 1e-8 * (8342.13 + 2406030 / (130 - s2) + 15997 / (38.9 - s2));
}
function lamAir(n1, n2){ const lv = lamVac(n1, n2); return lv / nAirEdlen(lv); }

/* NIST, Handbook of Basic Atomic Spectroscopic Data, "Strong Lines of
   Hydrogen (H I)", physics.nist.gov/PhysRefData/Handbook/Tables/
   hydrogentable2.htm (fetched 2026-09-21).  [intensity, wavelength in
   angstroms, n1, n2]; NIST prints Lyman in vacuum and the rest in air. */
const NIST_VAC = [[15, 926.2256, 1, 8], [20, 930.7482, 1, 7], [30, 937.8034, 1, 6],
                  [50, 949.7430, 1, 5], [100, 972.5367, 1, 4], [300, 1025.7222, 1, 3],
                  [1000, 1215.66824, 1, 2], [500, 1215.67364, 1, 2]];
const NIST_AIR = [[5, 3835.384, 2, 9], [6, 3889.049, 2, 8], [8, 3970.072, 2, 7],
                  [15, 4101.74, 2, 6], [30, 4340.462, 2, 5],
                  [30, 4861.2786, 2, 4], [10, 4861.2870, 2, 4], [60, 4861.3615, 2, 4],
                  [90, 6562.7110, 2, 3], [30, 6562.7248, 2, 3], [180, 6562.8518, 2, 3],
                  [5, 9545.97, 3, 8], [7, 10049.4, 3, 7], [12, 10938.1, 3, 6],
                  [20, 12818.07, 3, 5], [40, 18751.01, 3, 4], [5, 21655.3, 4, 7],
                  [8, 26251.5, 4, 6], [15, 40511.6, 4, 5], [4, 46525.1, 5, 7],
                  [6, 74578, 5, 6], [3, 123685, 6, 7]];

/* ---- PhET's model constants (build 1.0.9, read from the minified file) -- */
const PHET = {
  boxSide: 475,                 /* ZoomedInBox.SIDE_LENGTH                    */
  photonSpeed: 300,             /* Photon.SPEED, view units/s                 */
  photonRadius: 15,             /* Photon.RADIUS                              */
  electronRadius: 5,            /* Electron.RADIUS                            */
  photonsAcrossBox: 20,         /* dtBetweenPhotonEmission = h/SPEED/20       */
  orbitR: [15, 44, 81, 124, 174, 233],           /* getElectronOrbitRadius(n) */
  levelY: [0.025, 0.6, 0.73, 0.81, 0.86, 0.9],   /* EnergyDiagram fractions   */
  bohrOmegaDeg: 480,            /* BohrModel.ELECTRON_ANGLE_DELTA, deg/s      */
  dbOmegaDeg: 480,              /* de Broglie: the same, and NOT divided by n^2 */
  tAbsorb: 0.75,                /* min time in state before absorbing, s      */
  tEmit: 1.0,                   /* min time in state before emitting, s       */
  pEmit: 0.5,                   /* spontaneous emission per step              */
  billiardR: 30,                /* BilliardBallModel.RADIUS                   */
  puddingR: 35,                 /* PlumPuddingModel.RADIUS                    */
  puddingLam: 150,              /* PlumPuddingModel.PHOTON_EMISSION_WAVELENGTH*/
  puddingPAbsorb: 0.5,
  puddingPEmit: 0.1,
  bounceLo: 30, bounceHi: 60,   /* bounceBack scatter, degrees                */
  emitCone: 22.5,               /* adjustEmissionDirection: pi/8 either side   */
  classicalR0: 150, classicalOmega0: 600, classicalDrdt: 220,
  classicalSpin: 1.008, classicalRmin: 5,
  db3dYScale: 0.35, dbRingThick: 3,
  whiteGroundFraction: 0.4,     /* white light aimed at the n=1 lines         */
  lamMin: 92, lamMax: 780,      /* MONOCHROMATIC_WAVELENGTH_RANGE             */
  metastable: [2, 0, 0], metastableWait: 2.0,
  snapshots: 4,
  speeds: {fast: 3, normal: 1, slow: 0.25},
  stepDt: 0.1,                  /* MOTHAModel.STEP_ONCE_NORMAL_DT             */
};
PHET.dtPhoton = PHET.boxSide / PHET.photonSpeed / PHET.photonsAcrossBox;

/* ---- colorimetry: CIE 1931 2-degree observer (table in p2_cie.js) ------- */
const CIE_STEP = 5;
const SRGB_M = [[ 3.2406, -1.5372, -0.4986],
                [-0.9689,  1.8758,  0.0415],
                [ 0.0557, -0.2040,  1.0570]];
function srgbGamma(u){
  u = clamp(u, 0, 1);
  return u <= 0.0031308 ? 12.92 * u : 1.055 * Math.pow(u, 1 / 2.4) - 0.055;
}
function xyzToLin(X, Y, Z){
  return [SRGB_M[0][0] * X + SRGB_M[0][1] * Y + SRGB_M[0][2] * Z,
          SRGB_M[1][0] * X + SRGB_M[1][1] * Y + SRGB_M[1][2] * Z,
          SRGB_M[2][0] * X + SRGB_M[2][1] * Y + SRGB_M[2][2] * Z];
}
function cmfAt(nm){
  if(!(nm >= 360 && nm <= 830)) return null;
  const f = (nm - 360) / CIE_STEP, i = Math.min(CIE1931.length - 2, Math.floor(f)), t = f - i;
  const a = CIE1931[i], b = CIE1931[i + 1];
  return [a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t, a[3] + (b[3] - a[3]) * t];
}
function monoLinear(nm){
  const c = cmfAt(nm);
  if(!c) return [0, 0, 0];
  let v = xyzToLin(c[0], c[1], c[2]);
  const lo = Math.min(v[0], v[1], v[2]);
  if(lo < 0) v = v.map(u => u - lo);
  const m = Math.max(v[0], v[1], v[2]);
  return m > 0 ? v.map(u => u / m) : [0, 0, 0];
}
/* how bright the eye finds it (display only): sqrt(min(1, 4 ybar)) */
function monoLevel(nm){ const c = cmfAt(nm); return c ? Math.sqrt(Math.min(1, 4 * c[1])) : 0; }
function cssOfLinear(v, k){
  const s = k === undefined ? 1 : k;
  return 'rgb(' + Math.round(255 * srgbGamma(v[0] * s)) + ',' + Math.round(255 * srgbGamma(v[1] * s))
       + ',' + Math.round(255 * srgbGamma(v[2] * s)) + ')';
}
/* the colour a wavelength is drawn in.  Below 380 nm and above 780 nm the eye
   sees nothing, so PhET paints both grey (its UV_COLOR = IR_COLOR =
   rgb(160,160,160)); this file dims them instead so the visible band stands
   out, and says so on the canvas. */
const UV_GREY = '#8a8fa0', IR_GREY = '#9a8272';
function lamColour(nm){
  if(nm < 380) return UV_GREY;
  if(nm > 780) return IR_GREY;
  const lev = monoLevel(nm);
  return cssOfLinear(monoLinear(nm), 0.35 + 0.65 * lev);
}
function bandOf(nm){ return nm < 380 ? 'UV' : (nm > 780 ? 'IR' : 'visible'); }
