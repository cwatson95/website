
/* ================================================================== *
 *  SOLAR_SYSTEM_COMMON, rebuilt: the two-body (Kepler) engine and the  *
 *  N-body integrator.  Shared by keplers-laws.html and                 *
 *  my-solar-system.html (my-solar-system's assemble.py reads this very  *
 *  file, so the two cannot drift).  Units-agnostic: every function      *
 *  takes mu = G M (or G and masses) in whatever units the caller uses.  *
 *                                                                      *
 *  Python twin: build/keplers-laws/derive.py (Kepler) and              *
 *  build/my-solar-system/derive.py (N-body), both checked against      *
 *  scipy (brentq, quad, solve_ivp at rtol 1e-13).                      *
 * ================================================================== */

/* ---- Kepler's equation ------------------------------------------------------------------
   E - e sin E = M, solved by Newton safeguarded with the bracket [M - e, M + e]
   (Numerical Recipes' rtsafe: bisect only when a Newton step leaves the bracket or is not
   halving the interval).  The naive safeguard -- "reject a step that is not strictly inside
   (lo, hi)" -- STALLS: the converged step lands exactly on the bracket end it has just set,
   is rejected, and bisection then takes 46 more iterations (e = 0.99, M = 0.3, measured in
   derive.py).  The tolerance is on the STEP, which is the error of the previous iterate. */
const KEP_TOL = 1e-15, KEP_MAXIT = 100;
function keplerSolve(M, e){
  const turns = Math.round(M / TAU), Mr = M - TAU * turns;
  if(e === 0) return {E: Mr + TAU * turns, it: 0};
  let lo = Mr - e, hi = Mr + e;                    /* f(lo) <= 0 <= f(hi) for 0 < e <= 1 */
  let E = e < 0.8 ? Mr + e * Math.sin(Mr) : Mr + (Mr >= 0 ? 0.85 * e : -0.85 * e);
  E = clamp(E, lo, hi);
  let dxold = hi - lo, dx = dxold;
  let f = E - e * Math.sin(E) - Mr, fp = 1 - e * Math.cos(E), k = 0;
  while(k < KEP_MAXIT){
    k++;
    if(((E - hi) * fp - f) * ((E - lo) * fp - f) > 0 || Math.abs(2 * f) > Math.abs(dxold * fp)){
      dxold = dx; dx = 0.5 * (hi - lo); E = lo + dx;
    } else {
      dxold = dx; dx = f / fp; E = E - dx;
    }
    if(Math.abs(dx) <= KEP_TOL) break;
    f = E - e * Math.sin(E) - Mr; fp = 1 - e * Math.cos(E);
    if(f < 0) lo = E; else hi = E;
  }
  return {E: E + TAU * turns, it: k};
}
function keplerE(M, e){ return keplerSolve(M, e).E; }
/* the hyperbolic twin: e sinh H - H = M (e > 1).  Newton from a start that is right in both
   limits: H ~ M/(e-1) for small M, H ~ ln(2M/e) for large. */
function keplerH(M, e){
  const s = M < 0 ? -1 : 1, Ma = Math.abs(M);
  let H = Ma < 1 ? Ma / (e - 1) : Math.log(2 * Ma / e + 1.8);
  for(let k = 0; k < KEP_MAXIT; k++){
    const f = e * Math.sinh(H) - H - Ma, fp = e * Math.cosh(H) - 1;
    const d = f / fp; H -= d;
    if(Math.abs(d) <= KEP_TOL * (1 + Math.abs(H))) break;
  }
  return s * H;
}
/* the anomalies.  Both keep the turn count, so nu(t) is continuous and increasing. */
function trueFromE(E, e){
  const turns = Math.round(E / TAU), Er = E - TAU * turns;
  return 2 * Math.atan2(Math.sqrt(1 + e) * Math.sin(Er / 2), Math.sqrt(1 - e) * Math.cos(Er / 2)) + TAU * turns;
}
function eccFromTrue(nu, e){
  const turns = Math.round(nu / TAU), nr = nu - TAU * turns;
  return 2 * Math.atan2(Math.sqrt(1 - e) * Math.sin(nr / 2), Math.sqrt(1 + e) * Math.cos(nr / 2)) + TAU * turns;
}
function meanFromTrue(nu, e){ const E = eccFromTrue(nu, e); return E - e * Math.sin(E); }
function trueFromH(H, e){ return 2 * Math.atan2(Math.sqrt(e + 1) * Math.tanh(H / 2), Math.sqrt(e - 1)); }
function hypFromTrue(nu, e){ return 2 * Math.atanh(Math.sqrt((e - 1) / (e + 1)) * Math.tan(nu / 2)); }

/* ---- the conic through a state ----------------------------------------------------------
   Vis-viva for a, the eccentricity vector for e and the periapsis direction, the sign of the
   angular momentum for the sense of travel.  An orbit rounder than E_CIRC is treated as a
   circle and its "periapsis" put at the body's own position, so the sectors of the second
   law start somewhere definite rather than at a direction made of rounding noise. */
const E_CIRC = 1e-9;
function conicFromState(x, y, vx, vy, mu){
  const r = Math.hypot(x, y), v2 = vx * vx + vy * vy, rv = x * vx + y * vy;
  const h = x * vy - y * vx, energy = 0.5 * v2 - mu / r;
  const ex = ((v2 - mu / r) * x - rv * vx) / mu, ey = ((v2 - mu / r) * y - rv * vy) / mu;
  let e = Math.hypot(ex, ey), w;
  const dir = h >= 0 ? 1 : -1;
  if(e < E_CIRC){ e = 0; w = Math.atan2(y, x); } else w = Math.atan2(ey, ex);
  const cw = Math.cos(w), sw = Math.sin(w);
  const nu0 = Math.atan2(dir * (y * cw - x * sw), x * cw + y * sw);
  const el = {mu, r, v: Math.sqrt(v2), h, dir, energy, e, w, nu0, p: h * h / mu, ex, ey,
              vesc: Math.sqrt(2 * mu / r)};
  if(energy < 0){
    const a = -mu / (2 * energy), n = Math.sqrt(mu / (a * a * a));
    const E0 = eccFromTrue(nu0, e);
    el.kind = 'ellipse'; el.a = a; el.b = a * Math.sqrt(Math.max(0, 1 - e * e)); el.c = a * e;
    el.n = n; el.T = TAU / n; el.E0 = E0; el.M0 = E0 - e * Math.sin(E0);
    el.q = a * (1 - e); el.Q = a * (1 + e);
  } else {
    const a = energy === 0 ? Infinity : -mu / (2 * energy);        /* a < 0 for a hyperbola */
    el.kind = energy === 0 ? 'parabola' : 'hyperbola';
    el.a = a; el.c = a * e; el.q = el.p / (1 + e); el.Q = Infinity; el.T = Infinity;
    if(el.kind === 'hyperbola'){
      el.n = Math.sqrt(mu / Math.pow(-a, 3));
      el.H0 = hypFromTrue(nu0, e);
      el.M0 = e * Math.sinh(el.H0) - el.H0;
      el.b = -a * Math.sqrt(e * e - 1);
      el.turn = 2 * Math.asin(1 / e);                              /* the asymptotes' angle */
      el.nuInf = Math.acos(-1 / e);
    }
  }
  return el;
}
/* the state on the conic a time t after the state it was built from */
function stateOnConic(el, t){
  const w = el.w, d = el.dir, cw = Math.cos(w), sw = Math.sin(w);
  const Px = cw, Py = sw, Qx = -d * sw, Qy = d * cw;
  let X, Y, VX, VY, anom, M;
  if(el.kind === 'ellipse'){
    M = el.M0 + el.n * t;
    const E = keplerE(M, el.e), cE = Math.cos(E), sE = Math.sin(E);
    const r = el.a * (1 - el.e * cE);
    X = el.a * (cE - el.e); Y = el.b * sE;
    VX = -el.n * el.a * el.a * sE / r; VY = el.n * el.a * el.b * cE / r;
    anom = E;
  } else {
    M = el.M0 + el.n * t;
    const H = keplerH(M, el.e), cH = Math.cosh(H), sH = Math.sinh(H), A = -el.a;
    X = A * (el.e - cH); Y = A * Math.sqrt(el.e * el.e - 1) * sH;
    /* dH/dt = n/(e cosh H - 1), so dX/dt = -A sinh H dH/dt */
    VX = -A * el.n * sH / (el.e * cH - 1);
    VY = A * Math.sqrt(el.e * el.e - 1) * el.n * cH / (el.e * cH - 1);
    anom = H;
  }
  return {x: X * Px + Y * Qx, y: X * Py + Y * Qy, vx: VX * Px + VY * Qx, vy: VX * Py + VY * Qy,
          anom, M, r: Math.hypot(X * Px + Y * Qx, X * Py + Y * Qy)};
}
/* a point of the conic at true anomaly nu (drawing) */
function conicPoint(el, nu){
  const r = el.p / (1 + el.e * Math.cos(nu));
  const w = el.w, d = el.dir, cw = Math.cos(w), sw = Math.sin(w);
  const cn = Math.cos(nu), sn = Math.sin(nu);
  return [r * (cn * cw - d * sn * sw), r * (cn * sw + d * sn * cw)];
}
function periodOf(a, mu){ return TAU * Math.sqrt(a * a * a / mu); }
function escapeSpeed(r, mu){ return Math.sqrt(2 * mu / r); }
/* the area swept between two true anomalies of an ellipse: exactly 1/2 a b dM (Kepler's
   second law is the statement that dM/dt is constant).  The caller passes nu2 > nu1. */
function sectorArea(el, nu1, nu2){
  return 0.5 * el.a * el.b * (meanFromTrue(nu2, el.e) - meanFromTrue(nu1, el.e));
}
/* the same area the long way, for the suite: 1/2 integral r^2 dnu by Gauss-Legendre (8-point
   panels), which knows nothing about Kepler's equation */
const GL8_X = [-0.9602898564975363, -0.7966664774136267, -0.5255324099163290, -0.1834346424956498,
               0.1834346424956498, 0.5255324099163290, 0.7966664774136267, 0.9602898564975363];
const GL8_W = [0.1012285362903763, 0.2223810344533745, 0.3137066458778873, 0.3626837833783620,
               0.3626837833783620, 0.3137066458778873, 0.2223810344533745, 0.1012285362903763];
function sectorAreaQuad(el, nu1, nu2, panels){
  const N = panels || 24; let A = 0;
  for(let i = 0; i < N; i++){
    const a0 = nu1 + (nu2 - nu1) * i / N, a1 = nu1 + (nu2 - nu1) * (i + 1) / N;
    const hm = 0.5 * (a1 - a0), mid = 0.5 * (a0 + a1);
    for(let k = 0; k < 8; k++){
      const nu = mid + hm * GL8_X[k], r = el.p / (1 + el.e * Math.cos(nu));
      A += GL8_W[k] * hm * 0.5 * r * r;
    }
  }
  return A;
}

/* ---- the N-body system ------------------------------------------------------------------
   Flat arrays; every function takes G explicitly. */
function nbodyMake(m, x, y, vx, vy){
  const n = m.length;
  return {n, m: Float64Array.from(m), x: Float64Array.from(x), y: Float64Array.from(y),
          vx: Float64Array.from(vx), vy: Float64Array.from(vy),
          ax: new Float64Array(n), ay: new Float64Array(n)};
}
function nbodyCopy(S){ const T = nbodyMake(S.m.slice(0, S.n), S.x.slice(0, S.n), S.y.slice(0, S.n),
                                           S.vx.slice(0, S.n), S.vy.slice(0, S.n)); return T; }
function nbodyAccel(S, G){
  const n = S.n, ax = S.ax, ay = S.ay;
  for(let i = 0; i < n; i++){ ax[i] = 0; ay[i] = 0; }
  for(let i = 0; i < n; i++) for(let j = i + 1; j < n; j++){
    const dx = S.x[j] - S.x[i], dy = S.y[j] - S.y[i];
    const r2 = dx * dx + dy * dy, r = Math.sqrt(r2), f = G / (r2 * r);
    ax[i] += f * S.m[j] * dx; ay[i] += f * S.m[j] * dy;
    ax[j] -= f * S.m[i] * dx; ay[j] -= f * S.m[i] * dy;
  }
}
function nbodyDrift(S, c){ for(let i = 0; i < S.n; i++){ S.x[i] += c * S.vx[i]; S.y[i] += c * S.vy[i]; } }
function nbodyKick(S, G, c){ nbodyAccel(S, G); for(let i = 0; i < S.n; i++){ S.vx[i] += c * S.ax[i]; S.vy[i] += c * S.ay[i]; } }
/* PEFRL (Omelyan, Mryglod & Folk 2002): fourth order, four force evaluations a step.  The
   three coefficients are PhET's own (SOLAR_SYSTEM_COMMON's NumericalEngine carries them). */
const PEFRL_XI = 0.1786178958448091, PEFRL_LAM = -0.2123418310626054, PEFRL_CHI = -0.06626458266981849;
function pefrlStep(S, G, h){
  nbodyDrift(S, PEFRL_XI * h);
  nbodyKick(S, G, (1 - 2 * PEFRL_LAM) * h / 2);
  nbodyDrift(S, PEFRL_CHI * h);
  nbodyKick(S, G, PEFRL_LAM * h);
  nbodyDrift(S, (1 - 2 * (PEFRL_CHI + PEFRL_XI)) * h);
  nbodyKick(S, G, PEFRL_LAM * h);
  nbodyDrift(S, PEFRL_CHI * h);
  nbodyKick(S, G, (1 - 2 * PEFRL_LAM) * h / 2);
  nbodyDrift(S, PEFRL_XI * h);
}
/* PhET's step AS SHIPPED, for the comparison in the conservation view: the same five drifts
   and four kicks, but the acceleration is evaluated ONCE, at the start of the step, and
   reused by all four kicks.  That composition is exactly x + v h + a h^2/2, v + a h: a
   first-order method, not the fourth-order PEFRL it is named after.  derive.py measures both
   orders (error ratios 2.0 and 16 per halving). */
function phetStep(S, G, h){
  nbodyAccel(S, G);
  const n = S.n, ax = S.ax.slice(0, n), ay = S.ay.slice(0, n);
  const kick = c => { for(let i = 0; i < n; i++){ S.vx[i] += c * ax[i]; S.vy[i] += c * ay[i]; } };
  nbodyDrift(S, PEFRL_XI * h);
  kick((1 - 2 * PEFRL_LAM) * h / 2);
  nbodyDrift(S, PEFRL_CHI * h);
  kick(PEFRL_LAM * h);
  nbodyDrift(S, (1 - 2 * (PEFRL_CHI + PEFRL_XI)) * h);
  kick(PEFRL_LAM * h);
  nbodyDrift(S, PEFRL_CHI * h);
  kick((1 - 2 * PEFRL_LAM) * h / 2);
  nbodyDrift(S, PEFRL_XI * h);
}
/* the step a system can take: eta times the shortest of every pair's crossing time r/|dv|
   and free-fall time sqrt(r^3/(G(mi+mj))).  A fixed step cannot serve both a 5-AU orbit and
   a slingshot 0.06 AU from a star. */
function nbodyStepLimit(S, G, eta){
  let tau = Infinity;
  for(let i = 0; i < S.n; i++) for(let j = i + 1; j < S.n; j++){
    const dx = S.x[j] - S.x[i], dy = S.y[j] - S.y[i], r = Math.hypot(dx, dy);
    const dvx = S.vx[j] - S.vx[i], dvy = S.vy[j] - S.vy[i], dv = Math.hypot(dvx, dvy);
    const tff = Math.sqrt(r * r * r / (G * (S.m[i] + S.m[j])));
    tau = Math.min(tau, tff);
    if(dv > 0) tau = Math.min(tau, r / dv);
  }
  return isFinite(tau) ? eta * tau : Infinity;
}
/* advance by dt in equal substeps, at most the step limit long.  Returns the substep count
   (the caller's tests pin it: a changed rule shows up there). */
function nbodyAdvance(S, G, dt, eta, stepFn){
  const lim = nbodyStepLimit(S, G, eta === undefined ? NBODY_ETA : eta);
  const n = Math.max(1, Math.ceil(Math.abs(dt) / lim));
  const h = dt / n, step = stepFn || pefrlStep;
  for(let k = 0; k < n; k++) step(S, G, h);
  return n;
}
const NBODY_ETA = 0.02;
/* the constants of the motion */
function nbodyEnergy(S, G){
  let K = 0, U = 0;
  for(let i = 0; i < S.n; i++) K += 0.5 * S.m[i] * (S.vx[i] * S.vx[i] + S.vy[i] * S.vy[i]);
  for(let i = 0; i < S.n; i++) for(let j = i + 1; j < S.n; j++)
    U -= G * S.m[i] * S.m[j] / Math.hypot(S.x[j] - S.x[i], S.y[j] - S.y[i]);
  return K + U;
}
function nbodyMomentum(S){
  let px = 0, py = 0;
  for(let i = 0; i < S.n; i++){ px += S.m[i] * S.vx[i]; py += S.m[i] * S.vy[i]; }
  return [px, py];
}
function nbodyAngular(S){
  let L = 0;
  for(let i = 0; i < S.n; i++) L += S.m[i] * (S.x[i] * S.vy[i] - S.y[i] * S.vx[i]);
  return L;
}
function nbodyCom(S){
  let M = 0, x = 0, y = 0, vx = 0, vy = 0;
  for(let i = 0; i < S.n; i++){ M += S.m[i]; x += S.m[i] * S.x[i]; y += S.m[i] * S.y[i];
                                vx += S.m[i] * S.vx[i]; vy += S.m[i] * S.vy[i]; }
  return {M, x: x / M, y: y / M, vx: vx / M, vy: vy / M};
}
/* PhET's body radius: max(0.03, 0.023 m^(1/3)) AU, on its mass number (PhET's value) */
function massToRadius(m){ return Math.max(0.03, 0.023 * Math.cbrt(m)); }
/* a collision merges the pair: mass, momentum and the centre of mass are all conserved
   (PhET instead keeps the heavier body's mass and position and gives it the lighter one's
   momentum, which conserves momentum but destroys mass -- the difference is stated on the
   page).  Returns the list of merges. */
function nbodyCollide(S, radiusFn){
  const rad = radiusFn || massToRadius;
  const merges = [];
  let again = true;
  while(again){
    again = false;
    for(let i = 0; i < S.n && !again; i++) for(let j = i + 1; j < S.n && !again; j++){
      const d = Math.hypot(S.x[j] - S.x[i], S.y[j] - S.y[i]);
      if(d >= rad(S.m[i]) + rad(S.m[j])) continue;
      const big = S.m[i] >= S.m[j] ? i : j, small = big === i ? j : i;
      const M = S.m[i] + S.m[j];
      merges.push({keep: big, gone: small, x: S.x[small], y: S.y[small], m: M});
      S.x[big] = (S.m[i] * S.x[i] + S.m[j] * S.x[j]) / M;
      S.y[big] = (S.m[i] * S.y[i] + S.m[j] * S.y[j]) / M;
      S.vx[big] = (S.m[i] * S.vx[i] + S.m[j] * S.vx[j]) / M;
      S.vy[big] = (S.m[i] * S.vy[i] + S.m[j] * S.vy[j]) / M;
      S.m[big] = M;
      for(let k = small; k < S.n - 1; k++){
        S.m[k] = S.m[k + 1]; S.x[k] = S.x[k + 1]; S.y[k] = S.y[k + 1];
        S.vx[k] = S.vx[k + 1]; S.vy[k] = S.vy[k + 1];
      }
      S.n--;
      again = true;
    }
  }
  return merges;
}
/* the two-body reduction: the relative orbit is a Kepler conic about mu = G(m1+m2) and the
   centre of mass moves in a straight line.  Used by my-solar-system's exact view and by
   both suites. */
function twoBodyReduce(S, G){
  const mu = G * (S.m[0] + S.m[1]);
  const el = conicFromState(S.x[1] - S.x[0], S.y[1] - S.y[0], S.vx[1] - S.vx[0], S.vy[1] - S.vy[0], mu);
  const com = nbodyCom(S);
  return {mu, el, com, f1: S.m[1] / (S.m[0] + S.m[1]), f2: S.m[0] / (S.m[0] + S.m[1])};
}
function twoBodyAt(red, t){
  const s = stateOnConic(red.el, t);
  const cx = red.com.x + red.com.vx * t, cy = red.com.y + red.com.vy * t;
  return {x1: cx - red.f1 * s.x, y1: cy - red.f1 * s.y,
          x2: cx + red.f2 * s.x, y2: cy + red.f2 * s.y,
          vx1: red.com.vx - red.f1 * s.vx, vy1: red.com.vy - red.f1 * s.vy,
          vx2: red.com.vx + red.f2 * s.vx, vy2: red.com.vy + red.f2 * s.vy, rel: s};
}
