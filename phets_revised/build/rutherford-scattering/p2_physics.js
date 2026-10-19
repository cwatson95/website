
/* ================================================================== *
 *  the Coulomb problem                                                *
 *                                                                     *
 *  D  = k Z1 Z2 e^2 / E    the head-on distance of closest approach   *
 *  a  = D/2                so that  b = a cot(theta/2)                *
 *  tan(theta/2) = D/(2b)                                              *
 *  r_min = D/2 + sqrt(D^2/4 + b^2) = (D/2)(1 + 1/sin(theta/2))        *
 *  dsigma/dOmega = (b/sin theta)|db/dtheta| = (D/4)^2/sin^4(theta/2)  *
 *                                                                     *
 *  The 4 in (D/4)^2 is not decoration.  differential_scattering.html   *
 *  wrote a^2/sin^4 in its first draft and the |db/dtheta| cross-check  *
 *  caught the missing factor, which is why that cross-check is in      *
 *  selfTest here rather than in a comment.                             *
 * ================================================================== */

/* DEG converts degrees INTO radians and RAD the other way.  A constant named
   after a unit does not tell you which way it converts, and reading this one
   backwards put a factor of 3283 on every angle in bloch_sphere.html
   (Known-bad); selfTest pins 90 degrees against pi/2. */
const DEG = PI / 180, RAD = 180 / PI;

/* ---- constants: SI, CODATA 2022 (scipy.constants), pinned in selfTest -- */
const E_Q   = 1.602176634e-19;          /* C, exact since 2019           */
const EPS0  = 8.8541878188e-12;         /* F/m                           */
const KE    = 1 / (4 * PI * EPS0);      /* Coulomb constant, derived     */
const M_E   = 9.1093837139e-31;         /* kg                            */
const M_ALPHA = 6.644657345e-27;        /* kg                            */
const N_AVO = 6.02214076e23;            /* 1/mol, exact                  */
const MEV   = 1e6 * E_Q;                /* J                             */
const FM    = 1e-15;                    /* m                             */
const BARN  = 1e-28;                    /* m^2                           */
/* k e^2 in MeV fm -- the 1.44 every nuclear text quotes.  DERIVED. */
const KE2_MEVFM = KE * E_Q * E_Q / (MEV * FM);

/* ---- gold, and the 1913 beam ---- */
const GOLD = {
  Z: 79, A: 197,
  rho: 19300,                    /* kg/m^3                               */
  molar: 196.96657e-3,           /* kg/mol, gold is monoisotopic          */
  rAtom: 1.44e-10,               /* m, metallic radius -- the Thomson ball*/
  r0nuc: 1.2 * FM,               /* the nuclear-radius constant           */
};
function nuclearRadius(A){ return GOLD.r0nuc * Math.cbrt(A); }
function numberDensity(rho, molar){ return rho * N_AVO / molar; }

/* ---- the closed forms ---- */
function coulombD(Z1, Z2, EJ){ return KE * Z1 * Z2 * E_Q * E_Q / EJ; }
function thetaOfB(b, D){ return b > 0 ? 2 * Math.atan(D / (2 * b)) : PI; }
function bOfTheta(th, D){ return 0.5 * D / Math.tan(th / 2); }
function rminOfB(b, D){ return 0.5 * D + Math.sqrt(0.25 * D * D + b * b); }
function eccOfTheta(th){ return 1 / Math.sin(th / 2); }
function dsdoOf(th, D){
  const s = Math.sin(th / 2);
  return (D / 4) * (D / 4) / (s * s * s * s);
}
/* the cumulative cross section beyond theta is exactly pi b(theta)^2 */
function sigmaBeyond(th, D){ const b = bOfTheta(th, D); return PI * b * b; }

/* the conic, phi measured from the INCOMING asymptote: the particle comes in
   at phi -> 0+ from (b, -infinity) and leaves along phi_inf = pi - theta */
function rOfPhi(phi, b, D){
  return b * b / (b * Math.sin(phi) + 0.5 * D * (Math.cos(phi) - 1));
}
function drdPhi(phi, b, D){
  const den = b * Math.sin(phi) + 0.5 * D * (Math.cos(phi) - 1);
  const dd = b * Math.cos(phi) - 0.5 * D * Math.sin(phi);
  return -b * b * dd / (den * den);
}
function phiInfOf(b, D){ return 2 * Math.atan(2 * b / D); }
/* the polar angle at which the orbit crosses radius r.  In the half-angle
   variable t = tan(phi/2) the conic is a plain quadratic,
       (D + q) t^2 - 2 b t + q = 0,   q = b^2/r,
   whose two roots are the approach and the recession.  The obvious route --
   write b sin phi + (D/2) cos phi as R sin(phi + theta/2) and take an arcsine
   -- is the SAME equation and is useless for small b: R and C then agree to
   fifteen digits and the arcsine has no correct digits left.  At b = 1e-6 and
   D = 31.875 it returned phi = 0 for every radius; the form below returns
   8.4e-9 and 1.2e-7, which are the right answers. */
function phiAtRadius(r, b, D, receding){
  const q = b * b / r;
  const disc = b * b - q * D - q * q;
  if(!(disc >= 0)) return receding ? phiInfOf(b, D) / 2 : phiInfOf(b, D) / 2;
  const s = Math.sqrt(disc), den = D + q;
  if(!(den > 0)) return 0;
  const t = (receding ? (b + s) : (b - s)) / den;
  return 2 * Math.atan(t);
}

/* ================================================================== *
 *  quadrature: the deflection function for ANY central potential      *
 *                                                                     *
 *   theta = pi - 2 b int_rmin^inf dr / (r^2 sqrt(1 - U/E - b^2/r^2))  *
 *                                                                     *
 *  u = rmin/r puts it on [0,1]; u = 1 - s^2 removes the inverse-square *
 *  -root singularity at the turning point exactly.  Extracted from     *
 *  projects/simulations/differential_scattering.html, which is this    *
 *  collection's own scattering sim.                                    *
 * ================================================================== */
const GLN = (function(){
  const n = 32, x = [], w = [];
  for(let i = 0; i < n; i++){
    let t = Math.cos(PI * (i + 0.75) / (n + 0.5));
    for(let it = 0; it < 100; it++){
      let p0 = 1, p1 = 0;
      for(let j = 0; j < n; j++){ const p2 = p1; p1 = p0; p0 = ((2 * j + 1) * t * p1 - j * p2) / (j + 1); }
      const dp = n * (t * p0 - p1) / (t * t - 1), dt = -p0 / dp; t += dt;
      if(Math.abs(dt) < 1e-16) break;
    }
    let p0 = 1, p1 = 0;
    for(let j = 0; j < n; j++){ const p2 = p1; p1 = p0; p0 = ((2 * j + 1) * t * p1 - j * p2) / (j + 1); }
    const dp = n * (t * p0 - p1) / (t * t - 1);
    x.push(t); w.push(2 / ((1 - t * t) * dp * dp));
  }
  return {x: x, w: w};
})();
function glQuad(f, a, b, nseg){
  const N = nseg || 8; let s = 0;
  for(let k = 0; k < N; k++){
    const p = a + (b - a) * k / N, q = a + (b - a) * (k + 1) / N;
    const hm = (q - p) / 2, mid = (p + q) / 2;
    for(let i = 0; i < GLN.x.length; i++) s += hm * GLN.w[i] * f(mid + hm * GLN.x[i]);
  }
  return s;
}
/* turning point of U/E = uoe(r) at impact parameter b: the largest root of
   1 - uoe(r) - b^2/r^2.  Bisection on a bracket found by walking outward. */
function turningPoint(b, uoe, rhi){
  const g = r => 1 - uoe(r) - b * b / (r * r);
  let hi = Math.max(b, 1e-30), guard = 0;
  while(g(hi) <= 0 && guard++ < 400) hi *= 1.6;
  if(guard >= 400) return null;
  let lo = hi / 1.6; guard = 0;
  while(g(lo) > 0 && lo > 1e-40 && guard++ < 400) lo /= 1.6;
  for(let i = 0; i < 200; i++){ const m = Math.sqrt(lo * hi); if(g(m) > 0) hi = m; else lo = m; }
  return Math.sqrt(lo * hi);
}
function thetaQuad(b, uoe, nseg){
  const rm = turningPoint(b, uoe);
  if(rm === null) return 0;
  const f = s => {
    const u = 1 - s * s;
    if(u <= 0) return 0;
    const r = rm / u;
    const val = 1 - uoe(r) - b * b * u * u / (rm * rm);
    return val > 0 ? 2 * s / Math.sqrt(val) : 0;
  };
  return PI - 2 * (b / rm) * glQuad(f, 0, 1, nseg || 12);
}
/* dsigma/dOmega straight from its definition, by differencing theta(b) */
function dsdoNumeric(th, D){
  const b = bOfTheta(th, D);
  if(!(b > 0)) return NaN;
  const hh = b * 1e-5;
  const dthdb = (thetaOfB(b + hh, D) - thetaOfB(b - hh, D)) / (2 * hh);
  if(!isFinite(dthdb) || dthdb === 0) return NaN;
  return Math.abs(b / Math.sin(th) / dthdb);
}

/* ================================================================== *
 *  Newton's equations, integrated -- the independent route            *
 *                                                                     *
 *  Unit mass, U(r)/m = alpha/r, so the acceleration is +alpha r/r^3    *
 *  and D = 2 alpha / v_inf^2.  Adaptive RK4: the substep count follows *
 *  the distance to the centre, and it is CAPPED, because a mutation    *
 *  sweep with no per-mutant timeout cannot survive an unbounded loop.  *
 * ================================================================== */
function coulombRHS(y, alpha){
  const r2 = y[0] * y[0] + y[1] * y[1];
  const r3 = r2 * Math.sqrt(r2);
  const f = alpha / r3;
  return [y[2], y[3], f * y[0], f * y[1]];
}
function rk4Step(y, hh, alpha){
  const k1 = coulombRHS(y, alpha);
  const y2 = [y[0] + 0.5 * hh * k1[0], y[1] + 0.5 * hh * k1[1],
              y[2] + 0.5 * hh * k1[2], y[3] + 0.5 * hh * k1[3]];
  const k2 = coulombRHS(y2, alpha);
  const y3 = [y[0] + 0.5 * hh * k2[0], y[1] + 0.5 * hh * k2[1],
              y[2] + 0.5 * hh * k2[2], y[3] + 0.5 * hh * k2[3]];
  const k3 = coulombRHS(y3, alpha);
  const y4 = [y[0] + hh * k3[0], y[1] + hh * k3[1], y[2] + hh * k3[2], y[3] + hh * k3[3]];
  const k4 = coulombRHS(y4, alpha);
  return [y[0] + hh * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6,
          y[1] + hh * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6,
          y[2] + hh * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]) / 6,
          y[3] + hh * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3]) / 6];
}
/* integrate a trajectory from (b, -y0) with asymptotic speed 1, returning the
   path, the deflection, and the worst energy and angular-momentum drift */
function integrateOrbit(b, D, y0, nsteps){
  const alpha = D / 2;                       /* v_inf = 1, so D = 2 alpha */
  const N = Math.max(8, Math.min(200000, nsteps || 4000));
  /* start ON the conic at the radius whose y is -y0, so the integration and
     the closed form describe ONE orbit and not two nearby ones */
  const phi0 = phiAtRadius(Math.hypot(b, y0), b, D, false);
  const r0 = rOfPhi(phi0, b, D);
  const x = r0 * Math.sin(phi0), y = -r0 * Math.cos(phi0);
  const dr = drdPhi(phi0, b, D);
  let vx = dr * Math.sin(phi0) + r0 * Math.cos(phi0);
  let vy = -dr * Math.cos(phi0) + r0 * Math.sin(phi0);
  const nrm = Math.hypot(vx, vy), sp = Math.sqrt(Math.max(0, 1 - D / r0));
  vx = sp * vx / nrm; vy = sp * vy / nrm;
  let st = [x, y, vx, vy];
  const E0 = 0.5 * (vx * vx + vy * vy) + alpha / r0;
  const L0 = x * vy - y * vx;
  const T = 3.2 * y0;                        /* v_inf = 1, so t ~ distance */
  const pts = [x, y];
  const minSeg = y0 / 150;                   /* thin the drawn polyline    */
  let lx = x, ly = y, dE = 0, dL = 0;
  for(let i = 0; i < N; i++){
    const r = Math.hypot(st[0], st[1]);
    /* the step follows the distance to the centre: close in, the direction
       turns fast.  Capped both ways so the loop always terminates. */
    const hh = clamp(T / N, 1e-12, Math.max(1e-12, 0.02 * r));
    st = rk4Step(st, hh, alpha);
    const rr = Math.hypot(st[0], st[1]);
    const E = 0.5 * (st[2] * st[2] + st[3] * st[3]) + alpha / rr;
    const L = st[0] * st[3] - st[1] * st[2];
    dE = Math.max(dE, Math.abs(E - E0) / E0);
    dL = Math.max(dL, Math.abs(L - L0) / Math.abs(L0));
    if(Math.hypot(st[0] - lx, st[1] - ly) > minSeg){ pts.push(st[0], st[1]); lx = st[0]; ly = st[1]; }
    if(st[1] > y0 && rr > y0) break;
  }
  pts.push(st[0], st[1]);
  return {pts: pts, theta: Math.atan2(st[2], st[3]), rEnd: Math.hypot(st[0], st[1]),
          dE: dE, dL: dL, E0: E0, L0: L0, x: st[0], y: st[1]};
}
/* the exact hyperbola as a polyline in the same frame, for comparison */
function conicPath(b, D, rmax, n){
  const N = n || 240;
  const p0 = phiAtRadius(rmax, b, D, false), p1 = phiAtRadius(rmax, b, D, true);
  const out = [];
  for(let i = 0; i <= N; i++){
    const ph = p0 + (p1 - p0) * i / N;
    const r = rOfPhi(ph, b, D);
    if(!(r > 0) || !isFinite(r)) continue;
    out.push(r * Math.sin(ph), -r * Math.cos(ph));
  }
  return out;
}

/* ================================================================== *
 *  Thomson's atom: a uniform ball of charge +Ze of radius R with the   *
 *  electron charge on its surface, so the atom is NEUTRAL outside and  *
 *  the field inside is the ball's alone.  Then                         *
 *      U(r)/E = D (R^2 - r^2) / (2 R^3)   for r <= R,  0 outside,      *
 *  which is continuous at R, and the straight-line impulse gives       *
 *      theta(b) = D b sqrt(R^2 - b^2) / R^3,                           *
 *      theta_max = D/(2R) at b = R/sqrt2,   <theta^2> = D^2/(6 R^2).   *
 *  The electrons are not deflectors here: a FREE electron can turn an  *
 *  alpha by at most asin(m_e/m_alpha) = 1.37e-4 rad, which is the      *
 *  bound the historical argument uses.                                 *
 * ================================================================== */
function thomsonU(r, D, R){ return r >= R ? 0 : D * (R * R - r * r) / (2 * R * R * R); }
function thomsonTheta(b, D, R){
  if(b >= R || b < 0) return 0;
  return D * b * Math.sqrt(R * R - b * b) / (R * R * R);
}
function thomsonThetaMax(D, R){ return D / (2 * R); }
function thomsonTheta2Mean(D, R){ return D * D / (6 * R * R); }
/* the exact deflection integral in the same potential -- the independent
   route that says how good the impulse form is (its relative error is
   O(theta), measured, not assumed) */
function thomsonThetaExact(b, D, R, nseg){
  if(b >= R || b <= 0) return 0;
  return thetaQuad(b, r => thomsonU(r, D, R), nseg || 14);
}
/* a foil n t atoms per unit area deep: <theta^2> adds, so
   <theta^2>_total = n t int theta(b)^2 2 pi b db = n t pi D^2 / 6 */
function thomsonFoilTheta2(D, nt){ return nt * PI * D * D / 6; }
/* the projected multiple-scattering distribution is Gaussian in the plane, so
   P(theta > Th) = exp(-Th^2 / <theta^2>).  Return log10 of it: the number is
   far below the smallest double. */
function thomsonLog10P(Th, theta2){ return -Th * Th / theta2 / Math.LN10; }
/* the largest angle a free electron can give an alpha */
function electronMaxDeflection(){ return Math.asin(M_E / M_ALPHA); }

/* ================================================================== *
 *  PhET's scaled model, read out of rutherford-scattering 1.1.29      *
 *                                                                     *
 *  RSConstants        MIN/MAX/DEFAULT_ALPHA_ENERGY  50 / 100 / 80     *
 *                     MIN/MAX/DEFAULT_PROTON_COUNT  20 / 100 / 79     *
 *                     MIN/MAX/DEFAULT_NEUTRON_COUNT 20 / 150 / 118    *
 *                     SPACE_NODE_WIDTH 510, DEFAULT_SHOW_TRACES false *
 *  RSBaseModel        bounds = +- SPACE_NODE_WIDTH/4 = +- 127.5       *
 *  RutherfordAtomSpace   five atoms, atomWidth 30                     *
 *  RutherfordNucleusSpace one atom, width = the whole bounds          *
 *  RutherfordAtom.moveParticle  D = (L/8)(p/79)(80^2/s0^2)            *
 *  Gun.step           one particle every bounds.width/energy/20 s     *
 *                                                                     *
 *  Note what that D means.  PhET's slider is LABELLED Energy and used  *
 *  as the particle's SPEED, and D goes as 1/speed^2 -- which is the    *
 *  right 1/E scaling.  Writing D = 2 alpha / s0^2 makes the Coulomb    *
 *  strength alpha = 400 L (p/79) independent of the speed, as it must  *
 *  be: the field does not know how fast the projectile is going.       *
 * ================================================================== */
const PHET = {
  version: '1.1.29',
  minEnergy: 50, maxEnergy: 100, defEnergy: 80,
  minProtons: 20, maxProtons: 100, defProtons: 79,
  minNeutrons: 20, maxNeutrons: 150, defNeutrons: 118,
  boxW: 255,                       /* SPACE_NODE_WIDTH/2                 */
  atomW: 30,                       /* RutherfordAtomSpace                */
  gunRateDiv: 20,                  /* Gun.step: width/energy/20          */
  nudgeWindow: 0.04,               /* of the bounds width                */
  nudgeLo: 2, nudgeHi: 10,         /* LinearFunction(20, 255, 2, 10):    */
  nudgeW0: 20, nudgeW1: 255,       /* 2 units at width 20, 10 at 255     */
  showTraces: false,
  atomicScaleM: 6.0e-10,           /* its "{0} m (atomic scale)" caption */
  nuclearScaleM: 1.5e-13,          /* its "{0} m (nuclear scale)"        */
  nucleonR: 3,                     /* RutherfordNucleus nucleonRadius    */
};
/* the Coulomb strength of one PhET atom, in model units^3/s^2 */
function phetAlpha(L, protons){ return 400 * L * (protons / PHET.defProtons); }
/* and its head-on distance at gun speed s0 -- algebraically PhET's own
   (L/8)(p/79)(80/s0)^2, which selfTest asserts both ways */
function phetD(L, protons, s0){ return 2 * phetAlpha(L, protons) / (s0 * s0); }
function phetDDirect(L, protons, s0){
  return (L / 8) * (protons / PHET.defProtons) * (PHET.defEnergy * PHET.defEnergy / (s0 * s0));
}
function phetGunPeriod(s0){ return PHET.boxW / s0 / PHET.gunRateDiv; }
/* PhET pushes a particle fired within 4% of the bounds width of an atom's
   centre further away from it, because its algorithm is singular at b = 0 */
function phetNudge(atomW){
  return PHET.nudgeLo + (atomW - PHET.nudgeW0)
       / (PHET.nudgeW1 - PHET.nudgeW0) * (PHET.nudgeHi - PHET.nudgeLo);
}

/* ================================================================== *
 *  mulberry32 -- the seeded stream, reproduced bit for bit in Python   *
 *  (derive.py prints its first draws and selfTest asserts them)        *
 * ================================================================== */
function mulberry32(seed){
  let a = seed | 0;
  return function(){
    a = a + 0x6D2B79F5 | 0;
    let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

/* ================================================================== *
 *  a seeded beam: b uniform on a DISC of radius bmax (a real beam),    *
 *  binned in solid angle, which must reproduce dsigma/dOmega.          *
 *  The gun in the live views fires along a LINE instead, whose         *
 *  fraction beyond theta is b(theta)/X rather than (b(theta)/bmax)^2.  *
 * ================================================================== */
function sampleBeam(n, bmax, D, seed){
  const rng = mulberry32(seed), th = new Float64Array(n);
  for(let i = 0; i < n; i++) th[i] = thetaOfB(bmax * Math.sqrt(rng()), D);
  return th;
}
function fractionBeyond(th, t0){
  let c = 0;
  for(let i = 0; i < th.length; i++) if(th[i] > t0) c++;
  return c / th.length;
}
/* bin edges in theta -> the sampled dsigma/dOmega, with the exact bin average
   beside it and the Poisson sigma the comparison is allowed */
function binBeam(th, edges, bmax, D){
  const out = [];
  for(let i = 0; i < edges.length - 1; i++){
    const lo = edges[i], hi = edges[i + 1];
    let c = 0;
    for(let k = 0; k < th.length; k++) if(th[k] > lo && th[k] <= hi) c++;
    const dom = TAU * (Math.cos(lo) - Math.cos(hi));
    const dens = c / (th.length * dom) * (PI * bmax * bmax);
    const exact = (sigmaBeyond(lo, D) - sigmaBeyond(hi, D)) / dom;
    out.push({lo: lo, hi: hi, n: c, dens: dens, exact: exact,
              sigma: c > 0 ? 1 / Math.sqrt(c) : Infinity});
  }
  return out;
}
