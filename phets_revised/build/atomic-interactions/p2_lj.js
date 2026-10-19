/* ================================================================== *
 *  the Lennard-Jones pair: potential, force, well geometry, exact     *
 *  turning points, the regularised period quadrature and the three    *
 *  time-steppers.  No DOM, no view state — the Python twin is         *
 *  build/atomic-interactions/derive.py and refvals.txt is the pin.    *
 *                                                                     *
 *  UNITS  lengths pm, times ps, masses u.  Then pm/ps is m/s exactly  *
 *  and the energy unit is u (pm/ps)^2 = u m^2 s^-2.  An epsilon        *
 *  quoted the way everyone quotes it, as eps/k_B in kelvin, converts   *
 *  with K_TO_E = k_B/m_u.                                             *
 * ================================================================== */

/* CODATA 2022 via scipy.constants 1.18 (derive.py prints them). */
const KBOLTZ = 1.380649e-23;            /* J/K, exact since the 2019 SI       */
const MU_KG = 1.66053906892e-27;        /* kg per u                            */
const QE = 1.602176634e-19;             /* J per eV, exact since the 2019 SI  */
const K_TO_E = KBOLTZ / MU_KG;          /* (pm/ps)^2 per K   = 8314.4626094101 */
const E_TO_MEV = MU_KG / QE * 1e3;      /* meV per u (pm/ps)^2                 */
const E_TO_ZJ = MU_KG * 1e21;           /* zJ  per u (pm/ps)^2                 */
const F_TO_PN = MU_KG * 1e24;           /* pN  per u (pm/ps)^2 / pm            */
const CBRT2 = Math.pow(2, 1 / 3);       /* 1.25992104989487                    */
const SIXRT2 = Math.pow(2, 1 / 6);      /* 1.12246204830937                    */

/* ---------------------------------------------------------------- the pair */
/* PhET's tables, read out of docs/phets/atomic-interactions_en.html (1.2.21).
   nitroglycerin's Element table gives the van der Waals radii and the atomic
   weights; SOMConstants gives the slider bounds and the adjustable defaults;
   InteractionStrengthTable.getInteractionPotential gives eps/k_B in K and
   SigmaTable.getSigma gives sigma in pm.  Each is PhET's value. */
const ATOM = {
  Ne: {sym: 'Ne', name: 'neon', r: 154, m: 20.1797, col: '#5ac8e0'},
  Ar: {sym: 'Ar', name: 'argon', r: 188, m: 39.948, col: '#cd35c4'},
  O: {sym: 'O', name: 'oxygen', r: 152, m: 15.9994, col: '#e8843a'},
  X: {sym: 'A', name: 'adjustable', r: 175, m: 25, col: '#b8ec4c'}
};
const PHET_MIN_SIGMA = 75, PHET_MAX_SIGMA = 500;
const PHET_MIN_EPSILON = 20, PHET_MAX_EPSILON = 450;
const PHET_ADJ_SIGMA = 350, PHET_ADJ_EPSILON = 100;   /* 2*175 pm, 100 K */
/* PhET's own States-of-Matter constants for the same species, kept because
   they contradict the Atomic Interactions oxygen row and the sim says so. */
const PHET_SOM = {epsO2: 113, sigO2: 365};
const PHET_CRIT = {Ne: 45, Ar: 151, O: 155};     /* K, critical points   */
const PHET_TRIPLE = {Ne: 24.5, Ar: 75, O: 54};   /* K, triple points     */

const PAIRS = [
  {key: 'NeNe', label: 'neon-neon', a: 'Ne', b: 'Ne', sig: 308, eps: 35.8},
  {key: 'ArAr', label: 'argon-argon', a: 'Ar', b: 'Ar', sig: 376, eps: 111.84},
  {key: 'OO', label: 'oxygen-oxygen', a: 'O', b: 'O', sig: 200, eps: 1000},
  {key: 'NeAr', label: 'neon-argon', a: 'Ne', b: 'Ar', sig: 343, eps: 59.5},
  {key: 'NeO', label: 'neon-oxygen', a: 'Ne', b: 'O', sig: 154 + 152, eps: 51},
  {key: 'ArO', label: 'argon-oxygen', a: 'Ar', b: 'O', sig: 188 + 152, eps: 85},
  {key: 'Adj', label: 'adjustable', a: 'X', b: 'X',
   sig: PHET_ADJ_SIGMA, eps: PHET_ADJ_EPSILON}
];
const PAIR_BY_KEY = {};
PAIRS.forEach(p => {PAIR_BY_KEY[p.key] = p;});

/* The literature, with its sources.  Ne and Ar: Attard arXiv:1702.00096
   Table I, after van Sciver, Helium Cryogenics 2nd ed. (Springer 2012) —
   the table prints sigma AND r_min, and r_min/sigma reproduces 2^(1/6) to
   its own precision, which is the cheapest possible check on it.  Ar (second
   set) and O2: Bird, Stewart & Lightfoot, Transport Phenomena 2nd ed. (2007)
   pp. 864-865.  Nothing here is quoted from memory; see the header. */
const LIT = {
  Ne: {sig: 278.9, eps: 35.7, rmin: 313.1, src: 'van Sciver 2012'},
  Ar: {sig: 341.8, eps: 124.0, rmin: 383.7, src: 'van Sciver 2012'},
  O: {sig: 343.3, eps: 113.0, rmin: null, src: 'Bird Stewart Lightfoot 2007'}
};
const LIT_ALT = {Ar: {sig: 343.2, eps: 122.4, src: 'Bird Stewart Lightfoot 2007'}};
/* the whole source table, used only for the r_min/sigma = 2^(1/6) check */
const LIT_RMIN_TABLE = [['He', 255.6, 286.9], ['Ne', 278.9, 313.1],
                        ['Ar', 341.8, 383.7]];

/* Lorentz-Berthelot: the arithmetic mean of the sizes and the geometric mean
   of the depths.  Used for the mixed pairs when the literature set is live —
   there is no measured Ne-Ar potential in the sources above. */
function lorentzBerthelot(pa, pb){
  return {sig: 0.5 * (pa.sig + pb.sig), eps: Math.sqrt(pa.eps * pb.eps)};
}

/* The (sigma, eps/k_B) actually in force for a pair, in PhET's set or the
   literature's.  `adj` carries the adjustable pair's two sliders. */
function pairParams(key, useLit, adj){
  const p = PAIR_BY_KEY[key];
  if(!p) throw new Error('unknown pair ' + key);
  if(key === 'Adj') return {sig: adj.sig, eps: adj.eps, lit: false,
                            src: 'the two sliders'};
  if(!useLit) return {sig: p.sig, eps: p.eps, lit: false, src: "PhET's value"};
  const la = LIT[p.a], lb = LIT[p.b];
  if(p.a === p.b) return {sig: la.sig, eps: la.eps, lit: true, src: la.src};
  const lb2 = lorentzBerthelot(la, lb);
  return {sig: lb2.sig, eps: lb2.eps, lit: true, src: 'Lorentz-Berthelot'};
}

/* ------------------------------------------------------------ the potential */
/* V(r) = 4 eps [ (sigma/r)^12 - (sigma/r)^6 ].  eps here is an ENERGY in
   u (pm/ps)^2, not a temperature: multiply eps/k_B by K_TO_E first. */
function ljV(r, sig, eps){
  const x6 = Math.pow(sig / r, 6);
  return 4 * eps * (x6 * x6 - x6);
}
/* F(r) = -dV/dr = (24 eps/r)[ 2(sigma/r)^12 - (sigma/r)^6 ].  Positive is
   repulsive (pushing the movable atom out).  Asserted against a 60-digit
   Decimal central difference in derive.py and against a Richardson-extrapolated
   central difference inside selfTest, so the closed form is never the only
   route to it. */
function ljF(r, sig, eps){
  const x6 = Math.pow(sig / r, 6);
  return 24 * eps / r * (2 * x6 * x6 - x6);
}
/* V''(r) = (24 eps/r^2)[ 26 (sigma/r)^12 - 7 (sigma/r)^6 ]. */
function ljVpp(r, sig, eps){
  const x6 = Math.pow(sig / r, 6);
  return 24 * eps / (r * r) * (26 * x6 * x6 - 7 * x6);
}
/* PhET's own two halves, kept so the sim can draw them separately the way
   PhET's "Components" force display does.  PhET writes them as
   48 e' sigma^12/r^13 and 24 e' sigma^6/r^7; their difference is ljF. */
function ljRepulsive(r, sig, eps){
  const x6 = Math.pow(sig / r, 6);
  return 48 * eps / r * x6 * x6;
}
function ljAttractive(r, sig, eps){
  const x6 = Math.pow(sig / r, 6);
  return 24 * eps / r * x6;
}

function rMin(sig){ return sig * SIXRT2; }
/* V''(r_min) = 72 eps / (2^(1/3) sigma^2), the small-oscillation spring. */
function ljK(sig, eps){ return 72 * eps / (CBRT2 * sig * sig); }
/* omega = sqrt(V''(r_min)/mu); mu is the reduced mass of whatever is free. */
function ljOmega(sig, eps, mu){ return Math.sqrt(ljK(sig, eps) / mu); }
function ljPeriod(sig, eps, mu){ return 2 * Math.PI / ljOmega(sig, eps, mu); }

/* The effective mass of the separation coordinate.  With the left atom pinned
   only the right one moves, so it is that atom's mass; with both free the
   separation obeys mu r-double-dot = F with mu = m1 m2/(m1+m2), and the centre
   of mass stays put.  This is the only place the reduced mass enters, and it
   is why "Moving" shortens every period by sqrt(2) for a like pair. */
function effMass(ma, mb, pinned){
  return pinned ? mb : ma * mb / (ma + mb);
}

/* ----------------------------------------------------- exact turning points */
/* With u = (sigma/r)^6 the potential is 4 eps (u^2 - u), so V(r) = E is the
   quadratic u^2 - u - E/(4 eps) = 0 and the two roots satisfy u_in + u_out = 1.
   E >= 0 is unbound (no outer turning point); E < -eps is impossible. */
function turningPoints(E, sig, eps){
  const d = 1 + E / eps;
  if(d < 0) return null;
  const s = Math.sqrt(d);
  const uIn = 0.5 * (1 + s), uOut = 0.5 * (1 - s);
  return {rIn: sig * Math.pow(uIn, -1 / 6),
          rOut: uOut <= 0 ? Infinity : sig * Math.pow(uOut, -1 / 6)};
}

/* sum_{k=0..5} x^k y^(5-k) = (x^6 - y^6)/(x - y), formed without the division
   so the factorisation below never divides by a vanishing difference. */
function powSum6(x, y){
  const x2 = x * x, y2 = y * y;
  return y2 * y2 * y + x * y2 * y2 + x2 * y2 * y + x2 * x * y2 + x2 * x2 * y
       + x2 * x2 * x;
}

/* The period of a bound orbit, by quadrature, with BOTH singularities removed
   in closed form rather than merely softened.
     E - V(r) = 4 eps (u_in - u)(u - u_out)          [u_in + u_out = 1]
   and with r = a - b cos(th) that becomes
     E - V = 4 eps sigma^12 b^2 sin^2(th) S_in S_out / (r^12 r_in^6 r_out^6),
   so v carries an exact sin(th) which cancels the dr = b sin(th) dth of the
   numerator.  The integrand is then analytic AND free of the catastrophic
   cancellation that ruins `E - V(r)` at small amplitude, where E and V agree
   to fifteen digits over most of the orbit (derive.py measures the naive form
   failing: 1.6e-4 relative at a = 0.002 pm).  Gauss-Legendre, n panels. */
const GL_CACHE = {};
function gaussLegendre(n){
  if(GL_CACHE[n]) return GL_CACHE[n];
  const x = new Float64Array(n), w = new Float64Array(n);
  for(let i = 0; i < n; i++){
    let z = Math.cos(Math.PI * (i + 0.75) / (n + 0.5)), pp = 0;
    for(let it = 0; it < 100; it++){
      let p0 = 1, p1 = 0;
      for(let j = 0; j < n; j++){
        const p2 = p1; p1 = p0;
        p0 = ((2 * j + 1) * z * p1 - j * p2) / (j + 1);
      }
      pp = n * (z * p0 - p1) / (z * z - 1);
      const dz = p0 / pp; z -= dz;
      if(Math.abs(dz) < 1e-15) break;
    }
    x[i] = z; w[i] = 2 / ((1 - z * z) * pp * pp);
  }
  GL_CACHE[n] = {x, w};
  return GL_CACHE[n];
}

function periodQuad(E, sig, eps, mu, n){
  n = n || 96;
  const tp = turningPoints(E, sig, eps);
  if(!tp || !isFinite(tp.rOut)) return Infinity;
  const r1 = tp.rIn, r2 = tp.rOut;
  const a = 0.5 * (r1 + r2), b = 0.5 * (r2 - r1);
  const gl = gaussLegendre(n);
  const sig6 = Math.pow(sig, 6);
  const pre = Math.pow(r1, 3) * Math.pow(r2, 3) / sig6;
  let s = 0;
  for(let i = 0; i < n; i++){
    const th = 0.5 * Math.PI * (gl.x[i] + 1), ww = 0.5 * Math.PI * gl.w[i];
    const r = a - b * Math.cos(th);
    const Sin = powSum6(r, r1), Sout = powSum6(r2, r);
    const r6 = Math.pow(r, 6);
    s += ww * pre * r6 * Math.sqrt(mu / (8 * eps * Sin * Sout));
  }
  return 2 * s;
}

/* The same integral with E - V(r) formed as a difference.  Kept ONLY so the
   suite can assert that it is worse, and where, so the regular form above
   cannot be quietly replaced by the obvious one. */
function periodQuadNaive(E, sig, eps, mu, n){
  n = n || 96;
  const tp = turningPoints(E, sig, eps);
  if(!tp || !isFinite(tp.rOut)) return Infinity;
  const a = 0.5 * (tp.rIn + tp.rOut), b = 0.5 * (tp.rOut - tp.rIn);
  const gl = gaussLegendre(n);
  let s = 0;
  for(let i = 0; i < n; i++){
    const th = 0.5 * Math.PI * (gl.x[i] + 1), ww = 0.5 * Math.PI * gl.w[i];
    const r = a - b * Math.cos(th);
    const ke = Math.max(E - ljV(r, sig, eps), 0);
    const v = Math.sqrt(2 * ke / mu);
    if(v > 0) s += ww * b * Math.sin(th) / v;
  }
  return 2 * s;
}

/* ------------------------------------------------------- the time-steppers */
/* Velocity Verlet: the sim's integrator.  Symplectic, time-reversible,
   globally second order, and its energy error is BOUNDED rather than
   secular — derive.py measures order 2.00 and no growth from 1 to 100
   periods.  The state is {r, v, a, t}; `a` is carried so each step costs
   one force evaluation. */
function ljState(r, v, sig, eps, mu){
  return {r: r, v: v, a: ljF(r, sig, eps) / mu, t: 0};
}
function stepVerlet(s, sig, eps, mu, dt){
  s.v += 0.5 * s.a * dt;
  s.r += s.v * dt;
  s.a = ljF(s.r, sig, eps) / mu;
  s.v += 0.5 * s.a * dt;
  s.t += dt;
  return s;
}
/* PhET's own stepper (DualAtomModel.updateAtomMotion): a = F/m, then v += a dt,
   then x += v dt.  That is semi-implicit (symplectic) Euler — first order, but
   still bounded, which is why PhET's atoms do not spiral away. */
function stepSymplecticEuler(s, sig, eps, mu, dt){
  s.a = ljF(s.r, sig, eps) / mu;
  s.v += s.a * dt;
  s.r += s.v * dt;
  s.t += dt;
  return s;
}
/* Forward Euler: both updates from the OLD state.  Not symplectic; its energy
   grows without bound.  Drawn only in the integrator view, as the control. */
function stepForwardEuler(s, sig, eps, mu, dt){
  s.a = ljF(s.r, sig, eps) / mu;
  const r0 = s.r;
  s.r = r0 + s.v * dt;
  s.v = s.v + s.a * dt;
  s.t += dt;
  return s;
}
const STEPPERS = {verlet: stepVerlet, symplectic: stepSymplecticEuler,
                  forward: stepForwardEuler};

function ljEnergy(s, sig, eps, mu){
  return 0.5 * mu * s.v * s.v + ljV(s.r, sig, eps);
}

/* Run `n` steps and report the worst excursion of the energy, as a fraction of
   the well depth.  This is what the integrator view plots and what selfTest
   pins the measured order against. */
const MAX_STEPS=6e5;      /* the integrator's own ceiling, enforced below.
   Six times the longest run any view asks for: 20 periods at 1 fs of the
   slowest pair the sliders reach (sigma 500 pm, eps 20 K) is 102,000 steps.
   Keep it small — the mutant that DELETES the clamp has to stay fast enough
   for a sweep, or it is the hang BRIEF.md warns about. */
function energyExcursion(r0, v0, sig, eps, mu, dt, n, kind){
  const step = STEPPERS[kind || 'verlet'];
  /* A step count derived from a period is only as finite as that period.  A
     bound that is computed and then not applied is not a bound (wind_tunnel
     Known-bad), and here an unbounded one is a hang rather than a bad plot. */
  n = isFinite(n) && n > 0 ? Math.min(n, MAX_STEPS) : 0;
  const s = ljState(r0, v0, sig, eps, mu);
  const E0 = ljEnergy(s, sig, eps, mu);
  let lo = E0, hi = E0;
  for(let i = 0; i < n; i++){
    step(s, sig, eps, mu, dt);
    const e = ljEnergy(s, sig, eps, mu);
    if(e < lo) lo = e;
    if(e > hi) hi = e;
  }
  return {E0: E0, lo: lo, hi: hi, s: s,
          worst: Math.max(Math.abs(hi - E0), Math.abs(lo - E0)) / eps};
}

/* The period measured from the motion itself: the time between two successive
   maxima of r(t), each refined by the parabola through its three samples.  A
   grid argmax staircases at first order in dt, so the refinement is not an
   optimisation — without it this tracks the quadrature only to O(dt). */
function periodFromMotion(r0, sig, eps, mu, dt, nmax){
  const s = ljState(r0, 0, sig, eps, mu);
  let p2 = null, p1 = null;
  const hits = [];
  const lim = nmax || 400000;
  for(let i = 0; i < lim; i++){
    stepVerlet(s, sig, eps, mu, dt);
    if(p2 !== null && p1 > p2 && p1 >= s.r){
      const den = p2 - 2 * p1 + s.r;
      const d = den !== 0 ? 0.5 * (p2 - s.r) / den : 0;
      hits.push((i - 1 + d) * dt);
      if(hits.length >= 2) return hits[1] - hits[0];
    }
    p2 = p1; p1 = s.r;
  }
  return NaN;
}

/* The speed the movable atom needs at r to escape: E = 0. */
function escapeSpeed(r, sig, eps, mu){
  const v = ljV(r, sig, eps);
  return v >= 0 ? 0 : Math.sqrt(-2 * v / mu);
}
