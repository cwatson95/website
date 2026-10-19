#!/usr/bin/env python3
"""derive.py -- reference values for keplers-laws.html (the Python twin of
build/keplers-laws/p2_engine.js and p2_kl.js).

    python3 derive.py > refvals.txt        (read it in full; never through head/tail)

The last line of the output is `REFJSON {...}`: every number selfTest pins,
emitted by the arithmetic that produced it.  gen_tables.py turns that line into
p2_ref_kl.js.  Nothing in REF is typed by hand.

THE MODEL.  A test body about a fixed star (PhET's model: the star does not
move, the planet's mass does not enter).  mu = G M, units AU, Julian years,
solar masses:  K = GM_sun yr^2 / AU^3.  Everything is Kepler's closed form:
    elements from the state vector (vis-viva, the eccentricity vector),
    E - e sin E = M = M0 + n t  (Newton, safeguarded by a bracket),
    tan(nu/2) = sqrt((1+e)/(1-e)) tan(E/2),   T = 2 pi sqrt(a^3 / mu).
Checked here against scipy (brentq on Kepler's equation, solve_ivp at rtol
1e-13 on the equations of motion, quad on 1/2 r^2 dnu for the swept areas).

MEASURED / DEFINED INPUTS
  AU = 149,597,870.7 km (IAU 2012 Resolution B2, exact by definition).
  Julian year = 365.25 d = 31,557,600 s (exact by definition).
  GM_sun = 1.32712440042e20 m^3 s^-2 (Wikipedia "Standard gravitational
  parameter", the value lagrange_points.html already carries).

PhET's VALUES (read out of docs/phets/keplers-laws_en.html, Kepler's Laws 1.2.12)
  SOLAR_SYSTEM_COMMON: G = 4.4567 in AU (km/s)^2 per 1e28 kg, masses in 1e28 kg;
  KeplersLawsConstants: MASS_OF_OUR_SUN = 200, PLANET_MASS = 50, star mass
  range 100..400 with a snap to 200 within 5 %, PERIOD_DIVISIONS 2..6 (4);
  the default planet at (2, 0) AU moving (0, 17.2358) km/s;
  EllipticalOrbitEngine: mu = 4.45669 M, T = sqrt(a^3 891.34 / mu) years,
  escape speed 0.99 sqrt(2 mu / r) (the speed is capped there and the orbit
  flagged at 0.99 of that), crash when a(1 - e) < massToRadius(M) =
  max(0.03, 0.023 M^(1/3)) AU, e shown as 0 below 0.01, Newton on Kepler's
  equation from E = M stopped once a step is below 0.01 rad, the clock: mean
  anomaly advances 500/T per engine unit while time advances 1000/12.6 years
  per engine unit, i.e. 6.3/T rad per year; target orbits (e, a): Mercury
  (0.2056, 0.4), Venus (0.0068, 0.7), Earth (0.0167, 1), Mars (0.0934, 1.5),
  Jupiter (0.0484, 5.2), drawn with periapsis toward +x.
"""
import json
import math
import sys

import numpy as np
from scipy import integrate, optimize

TAU = 2.0 * math.pi
AU_KM = 149597870.7
YR_S = 365.25 * 86400.0
GM_SUN = 1.32712440042e20
K_SUN = GM_SUN * YR_S ** 2 / (AU_KM * 1e3) ** 3      # AU^3 yr^-2 per solar mass
KMS = AU_KM / YR_S                                   # km/s per AU/yr

PHET = dict(G=4.4567, mass_unit_kg=1e28, sun=200.0, planet=50.0, mu_coeff=4.45669, mu_norm=891.34,
            r0=(2.0, 0.0), v0=(0.0, 17.2358), divisions=(2, 6, 4), newton_tol=0.01,
            engine_time_scale=0.002, model_to_view_time=1000.0 / 12.6, mean_motion_num=500.0)
TARGETS = [('mercury', 'Mercury', 0.2056, 0.4), ('venus', 'Venus', 0.0068, 0.7), ('earth', 'Earth', 0.0167, 1.0),
           ('mars', 'Mars', 0.0934, 1.5), ('jupiter', 'Jupiter', 0.0484, 5.2)]
REF = {}


def out(*a):
    print(*a)


def r17(x):
    return float('%.17g' % x)


def jsround(x):
    """JavaScript Math.round (floor(x + 0.5)); Python's round() is banker's rounding."""
    return math.floor(x + 0.5)


# ------------------------------------------------------------------ the engine twin
def kepler_E(M, e):
    """E - e sin E = M by Newton safeguarded with the bracket [M - e, M + e]
    (Numerical Recipes' rtsafe: bisect only when a Newton step leaves the
    bracket or is not halving the interval).  The JS twin step for step.
    Returns (E, iterations).

    The naive safeguard -- reject a Newton step that is not strictly inside
    (lo, hi) -- stalls: the converged step lands exactly ON the bracket end it
    has just set, is rejected, and the solver falls back to bisection for
    another 46 iterations (measured, e = 0.99, M = 0.3)."""
    turns = jsround(M / TAU)
    Mr = M - TAU * turns
    if e == 0.0:
        return Mr + TAU * turns, 0
    lo, hi = Mr - e, Mr + e              # f(lo) = -e(1 + sin lo) <= 0 <= f(hi) = e(1 - sin hi)
    if e < 0.8:
        E = Mr + e * math.sin(Mr)
    else:
        E = Mr + (0.85 * e if Mr >= 0 else -0.85 * e)
    E = min(max(E, lo), hi)
    dxold = hi - lo
    dx = dxold
    f = E - e * math.sin(E) - Mr
    fp = 1.0 - e * math.cos(E)
    k = 0
    while k < 100:
        k += 1
        if ((E - hi) * fp - f) * ((E - lo) * fp - f) > 0 or abs(2 * f) > abs(dxold * fp):
            dxold = dx
            dx = 0.5 * (hi - lo)
            E = lo + dx
        else:
            dxold = dx
            dx = f / fp
            E = E - dx
        if abs(dx) <= 1e-15:
            break
        f = E - e * math.sin(E) - Mr
        fp = 1.0 - e * math.cos(E)
        if f < 0:
            lo = E
        else:
            hi = E
    return E + TAU * turns, k


def true_from_E(E, e):
    turns = jsround(E / TAU)
    Er = E - TAU * turns
    nu = 2.0 * math.atan2(math.sqrt(1.0 + e) * math.sin(Er / 2), math.sqrt(1.0 - e) * math.cos(Er / 2))
    return nu + TAU * turns


def E_from_true(nu, e):
    turns = jsround(nu / TAU)
    nr = nu - TAU * turns
    E = 2.0 * math.atan2(math.sqrt(1.0 - e) * math.sin(nr / 2), math.sqrt(1.0 + e) * math.cos(nr / 2))
    return E + TAU * turns


def conic(x, y, vx, vy, mu):
    """Elements of the orbit through (x, y) with velocity (vx, vy)."""
    r = math.hypot(x, y)
    v2 = vx * vx + vy * vy
    rv = x * vx + y * vy
    h = x * vy - y * vx
    energy = 0.5 * v2 - mu / r
    ex = ((v2 - mu / r) * x - rv * vx) / mu
    ey = ((v2 - mu / r) * y - rv * vy) / mu
    e = math.hypot(ex, ey)
    dirn = 1.0 if h >= 0 else -1.0
    if e < 1e-9:
        e = 0.0
        w = math.atan2(y, x)
    else:
        w = math.atan2(ey, ex)
    nu0 = math.atan2(dirn * (y * math.cos(w) - x * math.sin(w)), x * math.cos(w) + y * math.sin(w))
    el = dict(mu=mu, r=r, v=math.sqrt(v2), h=h, dir=dirn, energy=energy, e=e, w=w, nu0=nu0,
              p=h * h / mu, ex=ex, ey=ey)
    if energy < 0:
        a = -mu / (2 * energy)
        n = math.sqrt(mu / a ** 3)
        E0 = E_from_true(nu0, e)
        el.update(kind='ellipse', a=a, b=a * math.sqrt(max(0.0, 1 - e * e)), c=a * e, n=n, T=TAU / n,
                  E0=E0, M0=E0 - e * math.sin(E0), q=a * (1 - e), Q=a * (1 + e))
    else:
        el.update(kind='open')
    return el


def state_at(el, t):
    M = el['M0'] + el['n'] * t
    E, _ = kepler_E(M, el['e'])
    a, b, e, n, w, d = el['a'], el['b'], el['e'], el['n'], el['w'], el['dir']
    cE, sE = math.cos(E), math.sin(E)
    X, Y = a * (cE - e), b * sE
    r = a * (1 - e * cE)
    VX, VY = -n * a * a * sE / r, n * a * b * cE / r
    Px, Py = math.cos(w), math.sin(w)
    Qx, Qy = -d * math.sin(w), d * math.cos(w)
    return (X * Px + Y * Qx, X * Py + Y * Qy, VX * Px + VY * Qx, VX * Py + VY * Qy, E, M)


def third_law(a, mu):
    return TAU * math.sqrt(a ** 3 / mu)


def star_radius(M_sun):
    """PhET's massToRadius, on PhET's mass number (200 per solar mass)."""
    return max(0.03, 0.023 * (PHET['sun'] * M_sun) ** (1.0 / 3.0))


# ------------------------------------------------------------------ constants
out('# keplers-laws derive.py -- run %s' % 'python3 derive.py')
out('K_SUN (AU^3/yr^2 per M_sun) =', repr(K_SUN))
out('km/s per AU/yr             =', repr(KMS))
T1 = third_law(1.0, K_SUN)
out('T(1 AU, 1 M_sun) = %.15f yr = %.9f d' % (T1, T1 * 365.25))
out('   (2 pi / sqrt(K) years: the Gaussian year, 365.2569 d, not the Julian 365.25)')
vc1 = math.sqrt(K_SUN) * KMS
out('circular speed at 1 AU        = %.12f km/s' % vc1)
out('T^2/a^3 for our Sun          = %.15f yr^2/AU^3  (4 pi^2 / K)' % (TAU ** 2 / K_SUN))
REF['K_SUN'] = K_SUN
REF['KMS'] = KMS
REF['T1'] = T1
REF['vc1'] = vc1
REF['kepler_const'] = TAU ** 2 / K_SUN

# ------------------------------------------------------------------ PhET's own numbers
out('\n# PhET\'s model, re-evaluated')
mu_p = PHET['mu_coeff'] * PHET['sun']
out('PhET mu at our Sun = 4.45669 * 200 =', repr(mu_p), ' (PhET also types 891.34)')
r0 = 2.0
v0p = 17.2358
a_p = r0 * PHET['mu_norm'] / (2 * PHET['mu_norm'] - r0 * v0p ** 2)
e_p = math.sqrt(abs(1 - (r0 * v0p) ** 2 / (a_p * PHET['mu_norm'])))
out('PhET default orbit (its mu 891.34): a = %.9f AU, e = %.9f' % (a_p, e_p))
T_p = math.sqrt(a_p ** 3 * PHET['mu_norm'] / PHET['mu_norm'])
out('PhET period T = sqrt(a^3 891.34 / mu) =', repr(T_p), 'yr')
vcirc_phet = math.sqrt(PHET['mu_norm'])
out('PhET circular speed at 1 AU sqrt(891.34) = %.9f km/s  vs 2 pi AU per its 1-yr period: %.9f km/s (ratio %.6f)'
    % (vcirc_phet, TAU * KMS, vcirc_phet / (TAU * KMS)))
clock = PHET['mean_motion_num'] / PHET['model_to_view_time']
out('PhET clock: dM/dt = %.12f / T rad per year against 2 pi / T; one revolution reads %.9f T on its clock'
    % (clock, TAU / clock))
REF['phet'] = dict(mu=mu_p, a_default=a_p, e_default=e_p, T_default=T_p, vcirc1=vcirc_phet,
                   clock=clock, rev_reads=TAU / clock, vratio=vcirc_phet / (TAU * KMS))

# PhET's Newton loop: start at E = M, stop once the applied step is <= 0.01 rad
def phet_E(M, e):
    t = M
    i = 1.0
    n = 0
    while abs(i) > 0.01:
        i = (t - e * math.sin(t) - M) / (1 - e * math.cos(t))
        t -= i
        n += 1
    return t, n


def true_E(M, e):
    return optimize.brentq(lambda E: E - e * math.sin(E) - M, M - e - 1e-12, M + e + 1e-12, xtol=1e-16, rtol=8.9e-16, maxiter=500)


out('\nPhET\'s 0.01-rad Newton tolerance, worst error in E over 2001 mean anomalies in [0, 2 pi):')
phet_tol = {}
for e in (1.0 / 3.0, 0.2056, 0.0934, 0.75, 0.967):
    worst, worstM, worstN = 0.0, 0.0, 0
    for k in range(2001):
        M = TAU * k / 2001
        Ep, n = phet_E(M, e)
        Et = true_E(M, e)
        d = abs(Ep - Et)
        if d > worst:
            worst, worstM, worstN = d, M, n
    phet_tol['%.4f' % e] = dict(e=e, worst=worst, M=worstM, iters=worstN)
    out('  e = %.4f: |E_phet - E| <= %.3e rad (at M = %.4f, %d steps)' % (e, worst, worstM, worstN))
# position error on the default orbit (a = 1.5, e = 1/3) from the worst E error
a_d, e_d = 1.5, 1.0 / 3.0
worst_pos = 0.0
for k in range(2001):
    M = TAU * k / 2001
    Ep, _ = phet_E(M, e_d)
    Et = true_E(M, e_d)
    b_d = a_d * math.sqrt(1 - e_d * e_d)
    dp = math.hypot(a_d * (math.cos(Ep) - math.cos(Et)), b_d * (math.sin(Ep) - math.sin(Et)))
    worst_pos = max(worst_pos, dp)
out('  default orbit: the planet sits up to %.3e AU = %.0f km from where Kepler puts it' % (worst_pos, worst_pos * AU_KM))
REF['phet_tol'] = phet_tol
REF['phet_pos_err_au'] = worst_pos

# ------------------------------------------------------------------ Kepler's equation against brentq
out('\n# Kepler\'s equation: the twin against brentq (xtol 1e-16)')
kep = []
worst = 0.0
for e in (0.0, 0.0167, 0.2056, 1.0 / 3.0, 0.5, 0.75, 0.9, 0.967, 0.99, 0.999):
    for M in (1e-6, 0.01, 0.3, 1.0, 2.0, 3.0, 3.14159, 4.0, 6.0, -1.5, 12.5, -20.0):
        E, it = kepler_E(M, e)
        turns = jsround(M / TAU)
        Mr = M - TAU * turns
        if e == 0:
            Eb = Mr
        else:
            Eb = optimize.brentq(lambda x: x - e * math.sin(x) - Mr, Mr - e - 1e-12, Mr + e + 1e-12, xtol=1e-16, rtol=8.9e-16, maxiter=500)
        Eb += TAU * turns
        worst = max(worst, abs(E - Eb))
        kep.append(dict(M=M, e=e, E=r17(Eb), it=it, nu=r17(true_from_E(Eb, e))))
out('worst |E_twin - E_brentq| over %d cases = %.3e' % (len(kep), worst))
out('max Newton iterations = %d' % max(k['it'] for k in kep))
for k in kep[::7]:
    out('  M = %-10g e = %-7g E = %.17g  nu = %.17g  (%d it)' % (k['M'], k['e'], k['E'], k['nu'], k['it']))
REF['kepler'] = kep
REF['kepler_worst'] = worst

# the series branch the JS does NOT have: assert the small-M behaviour directly (E ~ M/(1-e))
for e in (0.2, 0.9):
    M = 1e-9
    E, _ = kepler_E(M, e)
    out('small M: e = %.1f, M = 1e-9 -> E = %.17g  (M/(1-e) = %.17g)' % (e, E, M / (1 - e)))

# Newton from E0 = M (PhET's start) -- the iterates the anomaly view draws
out('\n# Newton from E0 = M (PhET\'s start), plain, for the anomaly view')
def newton_trace(M, e, n=12):
    E = M
    tr = [E]
    for _ in range(n):
        f = E - e * math.sin(E) - M
        fp = 1 - e * math.cos(E)
        E = E - f / fp
        tr.append(E)
        if abs(f / fp) < 1e-15:
            break
    return tr
ntr = {}
for (M, e) in ((1.0, 1.0 / 3.0), (0.5, 0.9), (2.5, 0.967)):
    tr = newton_trace(M, e)
    ntr['%g_%g' % (M, e)] = [r17(v) for v in tr]
    out('  M = %g, e = %.4f:' % (M, e), ' '.join('%.12f' % v for v in tr))
REF['newton'] = ntr

# ------------------------------------------------------------------ elements from a state, against solve_ivp
out('\n# elements from the state vector, and the state at t by Kepler against solve_ivp (rtol 1e-13)')


def rhs(t, s, mu):
    x, y, vx, vy = s
    r3 = (x * x + y * y) ** 1.5
    return [vx, vy, -mu * x / r3, -mu * y / r3]


STATES = [
    ('default', 2.0, 0.0, 0.0, math.sqrt(K_SUN * (2 / 2.0 - 1 / 1.5)), 1.0),       # a = 1.5, e = 1/3 by construction
    ('tilted', 1.2, -0.7, 2.9, 4.1, 1.0),
    ('clockwise', -0.9, 1.4, 3.8, 2.2, 1.0),
    ('heavy star', 0.8, 0.6, -5.5, 7.3, 1.73),
    ('light star', 3.1, -1.9, 1.1, 2.4, 0.55),
    ('eccentric', 0.45, 0.0, 0.0, 12.5, 1.0),
]
els = {}
for name, x, y, vx, vy, M_sun in STATES:
    mu = K_SUN * M_sun
    el = conic(x, y, vx, vy, mu)
    assert el['kind'] == 'ellipse', name
    # independent: a from vis-viva, e from h and energy, T from a
    e_alt = math.sqrt(max(0.0, 1 + 2 * el['energy'] * el['h'] ** 2 / mu ** 2))
    sol = integrate.solve_ivp(rhs, (0, 2.5 * el['T']), [x, y, vx, vy], args=(mu,), method='DOP853', rtol=1e-13,
                              atol=1e-15, dense_output=True)
    times = [0.0, 0.25 * el['T'], 0.61 * el['T'], el['T'], 2.3 * el['T']]
    pts = []
    werr = 0.0
    for t in times:
        s = state_at(el, t)
        ref = sol.sol(t)
        werr = max(werr, math.hypot(s[0] - ref[0], s[1] - ref[1]) / el['a'])
        pts.append(dict(t=r17(t), x=r17(ref[0]), y=r17(ref[1]), vx=r17(ref[2]), vy=r17(ref[3]),
                        kx=r17(s[0]), ky=r17(s[1])))
    # the elements are constants of the motion: recompute at t = 0.61 T from solve_ivp's state
    s61 = sol.sol(0.61 * el['T'])
    el61 = conic(s61[0], s61[1], s61[2], s61[3], mu)
    # the period by the clock: the first return of the angle (solve_ivp event on y crossing the start ray)
    out('%-11s a=%.15f e=%.15f (alt %.3e) w=%.12f dir=%+d T=%.15f  |Kepler - ivp| <= %.2e a;  a,e at 0.61T: %.1e, %.1e'
        % (name, el['a'], el['e'], abs(el['e'] - e_alt), el['w'], el['dir'], el['T'], werr,
           abs(el61['a'] - el['a']) / el['a'], abs(el61['e'] - el['e'])))
    els[name] = dict(x=x, y=y, vx=vx, vy=vy, M=M_sun, a=r17(el['a']), e=r17(el['e']), w=r17(el['w']), dir=el['dir'],
                     T=r17(el['T']), b=r17(el['b']), c=r17(el['c']), h=r17(el['h']), energy=r17(el['energy']),
                     nu0=r17(el['nu0']), M0=r17(el['M0']), q=r17(el['q']), Q=r17(el['Q']), p=r17(el['p']),
                     pts=pts, werr=werr)
REF['els'] = els

# ------------------------------------------------------------------ second law: equal areas
out('\n# the second law: the N sectors from periapsis at equal mean-anomaly steps, areas by quad on 1/2 r^2 dnu')
sec = {}
el = conic(2.0, 0.0, 0.0, math.sqrt(K_SUN * (1.0 - 1 / 1.5)), K_SUN)
a, e, b = el['a'], el['e'], el['b']
p = a * (1 - e * e)
for N in range(2, 7):
    bounds = []
    areas = []
    for k in range(N + 1):
        E, _ = kepler_E(TAU * k / N, e)
        bounds.append(true_from_E(E, e))
    for k in range(N):
        A, err = integrate.quad(lambda nu: 0.5 * (p / (1 + e * math.cos(nu))) ** 2, bounds[k], bounds[k + 1],
                                epsabs=1e-15, epsrel=1e-14, limit=200)
        areas.append(A)
    target = math.pi * a * b / N
    dev = max(abs(A - target) for A in areas)
    out('N = %d: sector area pi a b / N = %.15f AU^2; quad worst deviation %.2e; bounds (deg) %s'
        % (N, target, dev, ' '.join('%.6f' % (bb * 180 / math.pi) for bb in bounds)))
    sec[str(N)] = dict(area=r17(target), bounds=[r17(bb) for bb in bounds], quad=[r17(A) for A in areas],
                       dt=r17(el['T'] / N))
REF['sectors'] = sec
REF['default_el'] = dict(a=r17(a), e=r17(e), b=r17(b), T=r17(el['T']), c=r17(el['c']), q=r17(el['q']),
                         Q=r17(el['Q']), v0=r17(math.sqrt(K_SUN * (1.0 - 1 / 1.5))),
                         v0_kms=r17(math.sqrt(K_SUN * (1.0 - 1 / 1.5)) * KMS), area=r17(math.pi * a * b))
out('default orbit: v0 = %.15f AU/yr = %.12f km/s (PhET 17.2358), T = %.15f yr, area pi a b = %.15f AU^2'
    % (math.sqrt(K_SUN / 3), math.sqrt(K_SUN / 3) * KMS, el['T'], math.pi * a * b))

# the area swept between two times is 1/2 h dt; brute force: the shoelace polygon of 20001 points of the ellipse
t1, t2 = 0.137 * el['T'], 0.588 * el['T']
pts = [state_at(el, t1 + (t2 - t1) * i / 20000.0) for i in range(20001)]
poly = [(0.0, 0.0)] + [(s[0], s[1]) for s in pts]
shoe = 0.0
for i in range(len(poly)):
    x1, y1 = poly[i]
    x2, y2 = poly[(i + 1) % len(poly)]
    shoe += x1 * y2 - x2 * y1
shoe = 0.5 * abs(shoe)
closed = 0.5 * abs(el['h']) * (t2 - t1)
out('swept area between 0.137 T and 0.588 T: 1/2 h dt = %.15f, shoelace (20001 pts) = %.15f, rel %.2e'
    % (closed, shoe, abs(shoe - closed) / closed))
REF['sweep_check'] = dict(t1=r17(t1), t2=r17(t2), closed=r17(closed), shoelace=r17(shoe))

# ------------------------------------------------------------------ third law: the targets
out('\n# the third law: PhET\'s target orbits about our Sun (1 M_sun)')
tg = {}
for key, name, e_t, a_t in TARGETS:
    T = third_law(a_t, K_SUN)
    vq = math.sqrt(K_SUN * (1 + e_t) / (a_t * (1 - e_t)))
    tg[key] = dict(name=name, e=e_t, a=a_t, T=r17(T), T2a3=r17(T * T / a_t ** 3), vq=r17(vq), vq_kms=r17(vq * KMS),
                   q=r17(a_t * (1 - e_t)))
    out('%-8s a = %-4g e = %-6g T = %.12f yr  T^2/a^3 = %.15f  periapsis speed %.9f km/s'
        % (name, a_t, e_t, T, T * T / a_t ** 3, vq * KMS))
REF['targets'] = tg
for M_sun in (0.5, 1.0, 1.5, 2.0):
    out('star %.1f M_sun: T^2/a^3 = %.15f yr^2/AU^3; star radius %.9f AU' % (M_sun, TAU ** 2 / (K_SUN * M_sun),
                                                                              star_radius(M_sun)))
REF['star_radius'] = {str(m): r17(star_radius(m)) for m in (0.5, 0.75, 1.0, 1.5, 2.0)}
REF['star_radius_floor'] = r17(star_radius(1e-6))

# ------------------------------------------------------------------ escape and crash (PhET's rules)
out('\n# escape and crash, PhET\'s rules, at the default position (2, 0) about our Sun')
vesc = math.sqrt(2 * K_SUN / 2.0)
out('escape speed at 2 AU = %.12f km/s; PhET caps at 0.99 of it (%.12f), flags from 0.9801 (%.12f)'
    % (vesc * KMS, 0.99 * vesc * KMS, 0.9801 * vesc * KMS))
cap = conic(2.0, 0.0, 0.0, 0.99 * vesc, K_SUN)
out('orbit at the cap: a = %.12f AU, e = %.12f, T = %.9f yr' % (cap['a'], cap['e'], cap['T']))
# the crash boundary on the default ray: the tangential speed whose periapsis equals the star radius
R1 = star_radius(1.0)
v_crash = math.sqrt(K_SUN * 2 * R1 / (2.0 * (2.0 + R1)))   # apoapsis 2, periapsis R1: v_apo^2 = mu 2 q / (Q (Q+q))
chk = conic(2.0, 0.0, 0.0, v_crash, K_SUN)
out('tangential speed at 2 AU whose periapsis is the star radius %.9f AU: %.12f km/s (check q = %.12f)'
    % (R1, v_crash * KMS, chk['q']))
REF['escape'] = dict(vesc_kms=r17(vesc * KMS), cap_a=r17(cap['a']), cap_e=r17(cap['e']), cap_T=r17(cap['T']),
                     v_crash_kms=r17(v_crash * KMS), R1=r17(R1))

# ------------------------------------------------------------------ the anomalies over one period (anomaly view)
out('\n# the anomalies over one period on the default orbit')
an = []
for f in (0.0, 0.1, 0.25, 0.5, 0.75, 0.9):
    M = TAU * f
    E, _ = kepler_E(M, 1.0 / 3.0)
    an.append(dict(f=f, M=r17(M), E=r17(E), nu=r17(true_from_E(E, 1.0 / 3.0))))
    out('  t/T = %.2f: M = %.12f  E = %.12f  nu = %.12f' % (f, M, E, true_from_E(E, 1.0 / 3.0)))
REF['anom'] = an

# ------------------------------------------------------------------ one frame of PhET's clock
FRAME_YR = (1.0 / 60.0) * PHET['engine_time_scale'] * PHET['model_to_view_time']
out('\nPhET\'s clock: one 1/60-s frame at normal speed = %.15f yr (1/%.6f)' % (FRAME_YR, 1 / FRAME_YR))
REF['frame_yr'] = FRAME_YR

out('\nREFJSON ' + json.dumps(REF, sort_keys=True))
