#!/usr/bin/env python3
"""derive.py -- reference values for my-solar-system.html (the Python twin of the
N-body half of build/keplers-laws/p2_engine.js and of build/my-solar-system/p2_mss.js).

    python3 derive.py > refvals.txt      (read it in full; never through head/tail)

The last line is `REFJSON {...}`: every number selfTest pins, printed by the
arithmetic that produced it.  gen_tables.py turns it into p2_ref_mss.js.

THE MODEL.  Newtonian N-body in the plane, in PhET's units: distance AU, mass
10^28 kg, velocity "km/s", G = 4.4567 (SOLAR_SYSTEM_COMMON's own value, read out
of the published build).  The integrator here and in the sim is PEFRL (Omelyan,
Mryglod & Folk 2002) with the force re-evaluated at each of its four kicks,
substepped so that no step is longer than eta times the shortest pairwise
crossing or free-fall time.  Checked against scipy solve_ivp (DOP853, rtol
1e-12) and, where the system has two bodies, against the exact Kepler solution.

PhET's OWN INTEGRATOR, AS SHIPPED, is also implemented here (phet_step): it uses
the PEFRL coefficients but evaluates the acceleration ONCE per step and reuses it
for all four kicks.  That composition is exactly x + v h + a h^2/2, v + a h -- a
first-order method, not the fourth-order PEFRL it is named after.  This file
measures both orders.

PhET's VALUES (docs/phets/my-solar-system_en.html, My Solar System 1.3.16)
  G = 4.4567, mass unit 1e28 kg, POSITION_MULTIPLIER 0.01, TIME_MULTIPLIER =
  0.01^1.5 sqrt(G) AU^1.5 / (sqrt(G_SI 1e28) yr), VELOCITY_MULTIPLIER =
  0.01/TIME_MULTIPLIER AU per year in km/s, engineTimeScale 0.05, 4000/N
  substeps per engine call, mass slider 0.1..300, body radius
  max(0.03, 0.023 m^(1/3)) AU, zoom levels 1..6 -> 25..125 view units per AU,
  path length capped at 20 AU, and the twelve orbital systems of the Lab screen.
"""
import json
import math
import sys

import numpy as np
from scipy import integrate, optimize

TAU = 2.0 * math.pi
AU_KM = 149597870.7
AU_M = AU_KM * 1e3
YR_S = 365.25 * 86400.0
G_SI = 6.6743e-11                 # PhET writes 66743e-15
MASS_UNIT = 1e28
G_PHET = 4.4567                   # AU (km/s)^2 per 1e28 kg, SOLAR_SYSTEM_COMMON
TIME_MULTIPLIER = math.pow(0.01, 1.5) * math.sqrt(G_PHET) * math.pow(AU_M, 1.5) / (math.sqrt(G_SI) * math.sqrt(MASS_UNIT) * YR_S)
VELOCITY_MULTIPLIER = 0.01 / TIME_MULTIPLIER * AU_M / YR_S / 1e3
T_U_YR = 1000 * TIME_MULTIPLIER   # one model time unit, in Julian years
G_SI_UNITS = G_SI * MASS_UNIT / (AU_M * 1e6)   # what G would be in AU (km/s)^2 per 1e28 kg
ETA = 0.02                        # the sim's step limit: eta x the shortest pairwise time
REF = {}


def r17(x):
    return float('%.17g' % x)


def out(*a):
    print(*a)


# ------------------------------------------------------------------ PhET's orbital systems
# (mass in 1e28 kg, position in AU, velocity in km/s), read out of the published build
SYSTEMS = {
    'sunPlanet': [(250, (0, 0), (0, -2.3446)), (25, (2, 0), (0, 23.4457))],
    'sunPlanetMoon': [(200, (0, 0), (0, 0)), (10, (1.6, 0), (0, 25.3467)), (1e-6, (1.4, 0), (0, 11.1948))],
    'sunPlanetComet': [(200, (0, 0), (0, 0)), (1, (1.5, 0), (0, 25.3467)), (1e-6, (-2.2, 1.3), (-4.2244, -7.3928))],
    'trojan': [(200, (0, 0), (0, 0)), (5, (1.5, 0), (0, 25.1355)),
               (1e-6, (0.75, -1.3), (21.7559, 12.6733)), (1e-6, (0.75, 1.3), (-21.7559, 12.6733))],
    'ellipses': [(250, (-1, 0), (0, 0)), (1e-6, (-0.15, 0), (0, 31.8946)),
                 (1e-6, (1.5, 0), (0, 12.6733)), (1e-6, (3.2, 0), (0, 7.8152))],
    'hyperbolic': [(250, (0, 0.25), (0, 0)), (1e-6, (-2.5, -0.7), (25.3467, 0)),
                   (1e-6, (-2.5, -1.4), (25.3467, 0)), (1e-6, (-2.5, -2.1), (25.3467, 0))],
    'slingshot': [(200, (0.01, 0), (0, -0.2112)), (10, (1.31, 0.55), (-11.6172, 24.2906)),
                  (1e-6, (-0.06, -1.28), (17.5315, 0))],
    'doubleSlingshot': [(200, (0, 0), (0, -0.2112)), (5, (0, -1.12), (28.3038, 0)),
                        (5, (1.86, -0.05), (0.2112, 23.4457)), (1e-6, (0.7, 0.72), (-9.9275, 13.307))],
    'binaryPlanet': [(150, (-1, 0), (0, -12.6733)), (120, (1, 0), (0, 10.5611)), (1e-6, (-0.5, 0), (0, 25.3467))],
    'fourStar': [(120, (-1, 1), (-10.5611, -10.5611)), (120, (1, 1), (-10.5611, 10.5611)),
                 (120, (1, -1), (10.5611, 10.5611)), (120, (-1, -1), (10.5611, -10.5611))],
    'doubleDouble': [(60, (-1.15, -0.03), (0, -32.5283)), (70, (1.02, 0), (0.2112, 31.6834)),
                     (55, (-0.77, -0.02), (-0.2112, 8.8713)), (62, (1.35, 0), (-0.2112, -10.9836))],
}
ORDER = ['sunPlanet', 'sunPlanetMoon', 'sunPlanetComet', 'trojan', 'ellipses', 'hyperbolic',
         'slingshot', 'doubleSlingshot', 'binaryPlanet', 'fourStar', 'doubleDouble']


def load(key, follow_com=True):
    """PhET loads a preset and then subtracts the centre-of-mass VELOCITY
    (followCenterOfMass), which is what keeps the systems on screen."""
    m = np.array([b[0] for b in SYSTEMS[key]], float)
    x = np.array([b[1][0] for b in SYSTEMS[key]], float)
    y = np.array([b[1][1] for b in SYSTEMS[key]], float)
    vx = np.array([b[2][0] for b in SYSTEMS[key]], float)
    vy = np.array([b[2][1] for b in SYSTEMS[key]], float)
    if follow_com:
        M = m.sum()
        vx -= (m * vx).sum() / M
        vy -= (m * vy).sum() / M
    return m, x, y, vx, vy


def accel(m, x, y, G=G_PHET):
    n = len(m)
    ax = np.zeros(n)
    ay = np.zeros(n)
    for i in range(n):
        for j in range(i + 1, n):
            dx, dy = x[j] - x[i], y[j] - y[i]
            r2 = dx * dx + dy * dy
            f = G / (r2 * math.sqrt(r2))
            ax[i] += f * m[j] * dx
            ay[i] += f * m[j] * dy
            ax[j] -= f * m[i] * dx
            ay[j] -= f * m[i] * dy
    return ax, ay


XI, LAM, CHI = 0.1786178958448091, -0.2123418310626054, -0.06626458266981849


def pefrl_step(m, x, y, vx, vy, h):
    x += XI * h * vx; y += XI * h * vy
    ax, ay = accel(m, x, y); c = (1 - 2 * LAM) * h / 2; vx += c * ax; vy += c * ay
    x += CHI * h * vx; y += CHI * h * vy
    ax, ay = accel(m, x, y); vx += LAM * h * ax; vy += LAM * h * ay
    c = (1 - 2 * (CHI + XI)) * h; x += c * vx; y += c * vy
    ax, ay = accel(m, x, y); vx += LAM * h * ax; vy += LAM * h * ay
    x += CHI * h * vx; y += CHI * h * vy
    ax, ay = accel(m, x, y); c = (1 - 2 * LAM) * h / 2; vx += c * ax; vy += c * ay
    x += XI * h * vx; y += XI * h * vy
    return x, y, vx, vy


def phet_step(m, x, y, vx, vy, h):
    """PhET's step as shipped: ONE force evaluation, reused by all four kicks."""
    ax, ay = accel(m, x, y)
    x += XI * h * vx; y += XI * h * vy
    c = (1 - 2 * LAM) * h / 2; vx += c * ax; vy += c * ay
    x += CHI * h * vx; y += CHI * h * vy
    vx += LAM * h * ax; vy += LAM * h * ay
    c = (1 - 2 * (CHI + XI)) * h; x += c * vx; y += c * vy
    vx += LAM * h * ax; vy += LAM * h * ay
    x += CHI * h * vx; y += CHI * h * vy
    c = (1 - 2 * LAM) * h / 2; vx += c * ax; vy += c * ay
    x += XI * h * vx; y += XI * h * vy
    return x, y, vx, vy


def step_limit(m, x, y, vx, vy, eta=ETA, G=G_PHET):
    tau = math.inf
    n = len(m)
    for i in range(n):
        for j in range(i + 1, n):
            dx, dy = x[j] - x[i], y[j] - y[i]
            r = math.hypot(dx, dy)
            dv = math.hypot(vx[j] - vx[i], vy[j] - vy[i])
            tau = min(tau, math.sqrt(r ** 3 / (G * (m[i] + m[j]))))
            if dv > 0:
                tau = min(tau, r / dv)
    return eta * tau


def advance(m, x, y, vx, vy, dt, eta=ETA, step=pefrl_step):
    """The sim's own rule: one call, substepped to the step limit."""
    lim = step_limit(m, x, y, vx, vy, eta)
    n = max(1, math.ceil(abs(dt) / lim))
    h = dt / n
    for _ in range(n):
        x, y, vx, vy = step(m, x, y, vx, vy, h)
    return x, y, vx, vy, n


def energy(m, x, y, vx, vy, G=G_PHET):
    K = 0.5 * float((m * (vx * vx + vy * vy)).sum())
    U = 0.0
    n = len(m)
    for i in range(n):
        for j in range(i + 1, n):
            U -= G * m[i] * m[j] / math.hypot(x[j] - x[i], y[j] - y[i])
    return K + U


def angular(m, x, y, vx, vy):
    return float((m * (x * vy - y * vx)).sum())


def momentum(m, vx, vy):
    return float((m * vx).sum()), float((m * vy).sum())


def rhs(t, s, m, G=G_PHET):
    n = len(m)
    x, y, vx, vy = s[:n], s[n:2 * n], s[2 * n:3 * n], s[3 * n:]
    ax, ay = accel(m, x.copy(), y.copy(), G)
    return np.concatenate([vx, vy, ax, ay])


def ivp(m, x, y, vx, vy, T, rtol=1e-12, atol=1e-14):
    s0 = np.concatenate([x, y, vx, vy])
    return integrate.solve_ivp(rhs, (0, T), s0, args=(m,), method='DOP853', rtol=rtol, atol=atol,
                               dense_output=True)


def conic(x, y, vx, vy, mu):
    """Elements of a relative orbit (an independent implementation of the JS engine's)."""
    r = math.hypot(x, y)
    v2 = vx * vx + vy * vy
    rv = x * vx + y * vy
    h = x * vy - y * vx
    en = 0.5 * v2 - mu / r
    ex = ((v2 - mu / r) * x - rv * vx) / mu
    ey = ((v2 - mu / r) * y - rv * vy) / mu
    e = math.hypot(ex, ey)
    d = dict(r=r, v=math.sqrt(v2), h=h, energy=en, e=e, w=math.atan2(ey, ex))
    if en < 0:
        a = -mu / (2 * en)
        d.update(a=a, T=TAU * math.sqrt(a ** 3 / mu), q=a * (1 - e), Q=a * (1 + e), kind='ellipse')
    else:
        a = -mu / (2 * en)
        d.update(a=a, kind='hyperbola', turn=2 * math.asin(1 / e), q=(h * h / mu) / (1 + e))
    return d


# ------------------------------------------------------------------ the units
out('# my-solar-system derive.py')
out("PhET's G                    =", repr(G_PHET), ' AU (km/s)^2 per 1e28 kg')
out('G from CODATA in the same units =', repr(G_SI_UNITS), ' (PhET is %.4f %% low)' % (100 * (1 - G_PHET / G_SI_UNITS)))
out('TIME_MULTIPLIER             =', repr(TIME_MULTIPLIER), ' yr per 0.01-AU-based time unit')
out('one model time unit         = %.15f yr = %.9f d' % (T_U_YR, T_U_YR * 365.25))
out('VELOCITY_MULTIPLIER         =', repr(VELOCITY_MULTIPLIER), ' km/s per model velocity unit at 0.01 AU')
out('the model velocity unit is  = %.9f true km/s (PhET calls it 1 km/s)' % (AU_KM / (T_U_YR * YR_S)))
out('a frame at normal speed     = %.15f model units = %.9f yr' % (0.05 / 60, 0.05 / 60 * T_U_YR))
REF['units'] = dict(G=G_PHET, G_si=G_SI_UNITS, time_mult=TIME_MULTIPLIER, T_U_YR=T_U_YR,
                    vel_mult=VELOCITY_MULTIPLIER, kms_true=AU_KM / (T_U_YR * YR_S),
                    frame=0.05 / 60, frame_yr=0.05 / 60 * T_U_YR)

# ------------------------------------------------------------------ the presets as loaded
out('\n# the orbital systems, after PhET subtracts the centre-of-mass velocity')
pres = {}
for key in ORDER:
    m, x, y, vx, vy = load(key)
    E = energy(m, x, y, vx, vy)
    L = angular(m, x, y, vx, vy)
    px, py = momentum(m, vx, vy)
    com = (float((m * x).sum() / m.sum()), float((m * y).sum() / m.sum()))
    pres[key] = dict(n=len(m), m=[r17(v) for v in m], x=[r17(v) for v in x], y=[r17(v) for v in y],
                     vx=[r17(v) for v in vx], vy=[r17(v) for v in vy], E=r17(E), L=r17(L),
                     comx=r17(com[0]), comy=r17(com[1]), pmag=r17(math.hypot(px, py)),
                     lim=r17(step_limit(m, x, y, vx, vy)))
    out('%-16s n=%d  E = %+.12f  L = %+.12f  |p| = %.2e  COM = (%+.6f, %+.6f)  step limit %.3e'
        % (key, len(m), E, L, math.hypot(px, py), com[0], com[1], step_limit(m, x, y, vx, vy)))
REF['presets'] = pres

# ------------------------------------------------------------------ the order of the two integrators
out('\n# the order of the integrators: the Sun-Planet system over 0.4 model units')
m, x, y, vx, vy = load('sunPlanet')
Tint = 0.4
sol = ivp(m, x, y, vx, vy, Tint, rtol=1e-13, atol=1e-15)
ref = sol.sol(Tint)
orders = {}
for name, step in (('pefrl', pefrl_step), ('phet', phet_step)):
    errs = []
    for N in (200, 400, 800, 1600):
        xx, yy, vvx, vvy = x.copy(), y.copy(), vx.copy(), vy.copy()
        h = Tint / N
        for _ in range(N):
            xx, yy, vvx, vvy = step(m, xx, yy, vvx, vvy, h)
        err = max(abs(xx[1] - ref[1]), abs(yy[1] - ref[len(m) + 1]))
        errs.append((N, err))
    ratios = [errs[i][1] / errs[i + 1][1] for i in range(len(errs) - 1)]
    order = [math.log2(r) for r in ratios]
    orders[name] = dict(errs=[[n, r17(e)] for n, e in errs], ratios=[r17(r) for r in ratios],
                        order=r17(sum(order) / len(order)))
    out('%-6s %s   halving ratios %s -> order %.2f'
        % (name, '  '.join('N=%-5d err %.3e' % (n, e) for n, e in errs),
           ' '.join('%.1f' % r for r in ratios), sum(order) / len(order)))
REF['orders'] = orders
out('PEFRL is fourth order (ratio 16 per halving); PhET\'s as-shipped step is first order (ratio 2).')
out('At PhET\'s own substep -- 4000/N substeps of a 1/60 s frame -- that first-order error is small:')
h_phet = (0.05 / 60) / (4000 / 2)
xx, yy, vvx, vvy = x.copy(), y.copy(), vx.copy(), vy.copy()
nfr = 60
for _ in range(nfr * 1):
    for _ in range(2000):
        xx, yy, vvx, vvy = phet_step(m, xx, yy, vvx, vvy, h_phet)
E0 = energy(m, x, y, vx, vy)
E1 = energy(m, xx, yy, vvx, vvy)
out('  after %d frames (%.4f model units) PhET\'s energy has drifted %.3e relative' % (nfr, nfr * 0.05 / 60, abs(E1 - E0) / abs(E0)))
REF['phet_drift'] = dict(frames=nfr, h=r17(h_phet), drift=r17(abs(E1 - E0) / abs(E0)))

# ------------------------------------------------------------------ the two-body preset, exactly
out('\n# Sun, Planet: two bodies, so the relative orbit is an exact Kepler ellipse')
m, x, y, vx, vy = load('sunPlanet')
mu = G_PHET * (m[0] + m[1])
el = conic(x[1] - x[0], y[1] - y[0], vx[1] - vx[0], vy[1] - vy[0], mu)
out('mu = G(m1+m2) = %.12f; a = %.12f AU, e = %.12f, T = %.12f model units = %.9f yr'
    % (mu, el['a'], el['e'], el['T'], el['T'] * T_U_YR))
out('periapsis %.9f AU, apoapsis %.9f AU; the bodies move on similar ellipses about the COM'
    % (el['q'], el['Q']))
solT = ivp(m, x, y, vx, vy, el['T'])
endT = solT.sol(el['T'])
out('after one period solve_ivp returns to the start within %.3e AU'
    % max(abs(endT[0] - x[0]), abs(endT[1] - x[1]), abs(endT[2] - y[0]), abs(endT[3] - y[1])))
two = dict(mu=r17(mu), a=r17(el['a']), e=r17(el['e']), T=r17(el['T']), T_yr=r17(el['T'] * T_U_YR),
           q=r17(el['q']), Q=r17(el['Q']), close=r17(max(abs(endT[0] - x[0]), abs(endT[1] - x[1]))))
# the sim's own stepping, pinned: advance frame by frame as the sim does
xx, yy, vvx, vvy = x.copy(), y.copy(), vx.copy(), vy.copy()
frame = 0.05 / 60
steps = []
subs = []
for k in range(1, 121):
    xx, yy, vvx, vvy, n = advance(m, xx, yy, vvx, vvy, frame)
    subs.append(n)
    if k in (1, 30, 60, 120):
        r = solT.sol(k * frame)
        steps.append(dict(frame=k, t=r17(k * frame), x1=r17(xx[1]), y1=r17(yy[1]),
                          vx1=r17(vvx[1]), vy1=r17(vvy[1]), ivp_x1=r17(r[1]), ivp_y1=r17(r[3]),
                          nsub=n))
        out('  frame %3d (t = %.6f): body 2 at (%+.12f, %+.12f); solve_ivp (%+.12f, %+.12f); %d substeps'
            % (k, k * frame, xx[1], yy[1], r[1], r[3], n))
two['steps'] = steps
two['subs'] = [min(subs), max(subs)]
out('  substeps per frame over 120 frames: %d..%d' % (min(subs), max(subs)))
REF['twobody'] = two

# ------------------------------------------------------------------ conservation over a long run
out('\n# conservation over 2000 frames of the sim\'s own stepping')
cons = {}
for key in ('sunPlanet', 'trojan', 'fourStar', 'doubleDouble'):
    m, x, y, vx, vy = load(key)
    E0 = energy(m, x, y, vx, vy)
    L0 = angular(m, x, y, vx, vy)
    p0 = momentum(m, vx, vy)
    xx, yy, vvx, vvy = x.copy(), y.copy(), vx.copy(), vy.copy()
    wE = wL = wP = 0.0
    for k in range(2000):
        xx, yy, vvx, vvy, n = advance(m, xx, yy, vvx, vvy, 0.05 / 60)
        if k % 50 == 0 or k == 1999:
            wE = max(wE, abs(energy(m, xx, yy, vvx, vvy) - E0) / abs(E0))
            wL = max(wL, abs(angular(m, xx, yy, vvx, vvy) - L0) / max(1e-12, abs(L0)))
            p = momentum(m, vvx, vvy)
            wP = max(wP, math.hypot(p[0] - p0[0], p[1] - p0[1]) / float((m * np.hypot(vx, vy)).sum()))
    cons[key] = dict(dE=r17(wE), dL=r17(wL), dP=r17(wP), t=r17(2000 * 0.05 / 60),
                     xend=[r17(v) for v in xx], yend=[r17(v) for v in yy])
    out('%-14s over %.3f model units: |dE/E| <= %.2e, |dL/L| <= %.2e, |dp|/p_scale <= %.2e'
        % (key, 2000 * 0.05 / 60, wE, wL, wP))
REF['conserve'] = cons

# ------------------------------------------------------------------ what each preset does
out('\n# the qualitative facts each preset is built to show')
facts = {}

# Sun, Planet, Moon: the moon stays inside the planet's Hill sphere
m, x, y, vx, vy = load('sunPlanetMoon')
mu_p = G_PHET * (m[1] + m[2])
rel = conic(x[2] - x[1], y[2] - y[1], vx[2] - vx[1], vy[2] - vy[1], mu_p)
hill = math.hypot(x[1], y[1]) * (m[1] / (3 * m[0])) ** (1 / 3)
sol = ivp(m, x, y, vx, vy, 1.5)
ts = np.linspace(0, 1.5, 3001)
d = np.array([math.hypot(sol.sol(t)[2] - sol.sol(t)[1], sol.sol(t)[5] - sol.sol(t)[4]) for t in ts])
facts['moon'] = dict(a=r17(rel['a']), e=r17(rel['e']), T=r17(rel['T']), hill=r17(hill),
                     dmin=r17(float(d.min())), dmax=r17(float(d.max())), span=r17(1.5))
out('moon: planetocentric a = %.9f AU, e = %.9f, T = %.9f (%.4f yr); Hill radius %.9f AU'
    % (rel['a'], rel['e'], rel['T'], rel['T'] * T_U_YR, hill))
out('      over 1.5 model units its distance from the planet stays in %.6f..%.6f AU, inside the Hill sphere'
    % (d.min(), d.max()))

# Trojan asteroids: they librate about +-60 degrees from the planet
m, x, y, vx, vy = load('trojan')
sol = ivp(m, x, y, vx, vy, 3.0)
ts = np.linspace(0, 3.0, 2001)
angs = {2: [], 3: []}
for t in ts:
    s = sol.sol(t)
    n = len(m)
    ap = math.atan2(s[n + 1] - s[n + 0], s[1] - s[0])
    for i in (2, 3):
        ai = math.atan2(s[n + i] - s[n + 0], s[i] - s[0])
        dd = math.degrees((ai - ap + math.pi) % TAU - math.pi)
        angs[i].append(dd)
facts['trojan'] = {str(i): dict(lo=r17(min(angs[i])), hi=r17(max(angs[i]))) for i in (2, 3)}
out('trojans: asteroid 3 stays between %+.3f and %+.3f deg of the planet, asteroid 4 between %+.3f and %+.3f'
    % (min(angs[2]), max(angs[2]), min(angs[3]), max(angs[3])))

# Ellipses: three test bodies, three Kepler ellipses about one star
m, x, y, vx, vy = load('ellipses')
mu_s = G_PHET * m[0]
els = []
for i in (1, 2, 3):
    e = conic(x[i] - x[0], y[i] - y[0], vx[i] - vx[0], vy[i] - vy[0], mu_s)
    els.append(dict(a=r17(e['a']), e=r17(e['e']), T=r17(e['T']), q=r17(e['q']), Q=r17(e['Q'])))
    out('ellipses body %d: a = %.9f, e = %.9f, T = %.9f (%.4f yr), periapsis %.9f'
        % (i + 1, e['a'], e['e'], e['T'], e['T'] * T_U_YR, e['q']))
facts['ellipses'] = els

# "Hyperbolic": what PhET's preset actually is.  Each test body's speed is compared with the
# escape speed at its own distance; the answer decides whether the path is a hyperbola or a
# very eccentric ellipse, and it is not what the preset's name says.
m, x, y, vx, vy = load('hyperbolic')
mu_s = G_PHET * m[0]
hyp = []
for i in (1, 2, 3):
    dx, dy = x[i] - x[0], y[i] - y[0]
    r = math.hypot(dx, dy)
    v = math.hypot(vx[i] - vx[0], vy[i] - vy[0])
    vesc = math.sqrt(2 * mu_s / r)
    e = conic(dx, dy, vx[i] - vx[0], vy[i] - vy[0], mu_s)
    rec = dict(e=r17(e['e']), q=r17(e['q']), energy=r17(e['energy']), kind=e['kind'],
               r=r17(r), v=r17(v), vesc=r17(vesc), ratio=r17(v / vesc))
    if e['kind'] == 'ellipse':
        rec.update(a=r17(e['a']), T=r17(e['T']), Q=r17(e['Q']))
    else:
        rec.update(turn_deg=r17(math.degrees(e['turn'])))
    hyp.append(rec)
    out('"hyperbolic" body %d: r = %.6f AU, v = %.6f of an escape speed %.6f (%.4f of it) -> %s, e = %.9f'
        % (i + 1, r, v, vesc, v / vesc, e['kind'], e['e']))
    if e['kind'] == 'ellipse':
        out('      a bound orbit: a = %.6f AU, apoapsis %.6f AU, period %.4f model units (%.2f yr)'
            % (e['a'], e['Q'], e['T'], e['T'] * T_U_YR))
    else:
        out('      a hyperbola: the asymptotes turn 2 arcsin(1/e) = %.4f deg' % math.degrees(e['turn']))
# measure the turn of body 2's velocity over the fly-by either way
sol = ivp(m, x, y, vx, vy, 4.0)
s0, s1 = sol.sol(0.0), sol.sol(4.0)
n = len(m)
ang0 = math.atan2(s0[3 * n + 1], s0[2 * n + 1])
ang1 = math.atan2(s1[3 * n + 1], s1[2 * n + 1])
turn_meas = math.degrees((ang1 - ang0 + math.pi) % TAU - math.pi)
out('   body 2\'s velocity turns %.4f deg over the first 4 model units of the fly-by' % turn_meas)
facts['hyperbolic'] = dict(bodies=hyp, turn_measured=r17(turn_meas))

# Slingshot: the test body leaves with more energy than it arrived with
m, x, y, vx, vy = load('slingshot')
mu_s = G_PHET * m[0]
sol = ivp(m, x, y, vx, vy, 2.0)
def helio_energy(s, i):
    n = len(m)
    dx, dy = s[i] - s[0], s[n + i] - s[n + 0]
    dvx, dvy = s[2 * n + i] - s[2 * n + 0], s[3 * n + i] - s[3 * n + 0]
    return 0.5 * (dvx * dvx + dvy * dvy) - mu_s / math.hypot(dx, dy)
e_before = helio_energy(sol.sol(0.0), 2)
e_after = helio_energy(sol.sol(2.0), 2)
out('slingshot: the comet\'s energy about the star goes %+.9f -> %+.9f (a gain of %.1f %%)'
    % (e_before, e_after, 100 * (e_after - e_before) / abs(e_before)))
facts['slingshot'] = dict(before=r17(e_before), after=r17(e_after), gain=r17((e_after - e_before) / abs(e_before)))

# Four Star Ballet: a homographic solution -- the square stays square, on Kepler ellipses
m, x, y, vx, vy = load('fourStar')
r0 = math.hypot(x[0], y[0])
mu_eff = G_PHET * m[0] * (1 / math.sqrt(2) + 0.25)      # the pull on one corner, per unit mass, at r
v0 = math.hypot(vx[0], vy[0])
el4 = conic(x[0], y[0], vx[0], vy[0], mu_eff)
sol = ivp(m, x, y, vx, vy, el4['T'])
end = sol.sol(el4['T'])
ret = max(abs(end[i] - x[i]) for i in range(4)) + max(abs(end[4 + i] - y[i]) for i in range(4))
ts = np.linspace(0, el4['T'], 400)
sq = 0.0
for t in ts:
    s = sol.sol(t)
    sides = [math.hypot(s[(i + 1) % 4] - s[i], s[4 + (i + 1) % 4] - s[4 + i]) for i in range(4)]
    sq = max(sq, (max(sides) - min(sides)) / max(sides))
out('four star ballet: each star is on a Kepler ellipse about the centre with mu_eff = G m (1/sqrt2 + 1/4) = %.9f'
    % mu_eff)
out('   e = %.9f, T = %.9f model units (%.4f yr); after one period it returns to within %.3e AU'
    % (el4['e'], el4['T'], el4['T'] * T_U_YR, ret))
out('   and the four sides stay equal to %.2e of a side over that period (a homographic solution)' % sq)
facts['fourStar'] = dict(mu_eff=r17(mu_eff), e=r17(el4['e']), a=r17(el4['a']), T=r17(el4['T']),
                         T_yr=r17(el4['T'] * T_U_YR), ret=r17(ret), square=r17(sq), r0=r17(r0), v0=r17(v0))

# Binary star, planet: the two stars' own orbit
m, x, y, vx, vy = load('binaryPlanet')
mu_b = G_PHET * (m[0] + m[1])
elb = conic(x[1] - x[0], y[1] - y[0], vx[1] - vx[0], vy[1] - vy[0], mu_b)
out('binary star: a = %.9f AU, e = %.9f, T = %.9f model units (%.4f yr)'
    % (elb['a'], elb['e'], elb['T'], elb['T'] * T_U_YR))
facts['binary'] = dict(a=r17(elb['a']), e=r17(elb['e']), T=r17(elb['T']), T_yr=r17(elb['T'] * T_U_YR))
REF['facts'] = facts

# ------------------------------------------------------------------ every preset against solve_ivp
out('\n# every preset: the sim\'s own stepping against solve_ivp after 60 and 300 frames')
runs = {}
for key in ORDER:
    m, x, y, vx, vy = load(key)
    T = 300 * 0.05 / 60
    sol = ivp(m, x, y, vx, vy, T)
    xx, yy, vvx, vvy = x.copy(), y.copy(), vx.copy(), vy.copy()
    rec = {}
    worst = 0.0
    for k in range(1, 301):
        xx, yy, vvx, vvy, n = advance(m, xx, yy, vvx, vvy, 0.05 / 60)
        if k in (60, 300):
            s = sol.sol(k * 0.05 / 60)
            nn = len(m)
            d = max(max(abs(xx[i] - s[i]) for i in range(nn)), max(abs(yy[i] - s[nn + i]) for i in range(nn)))
            worst = max(worst, d)
            rec[str(k)] = dict(x=[r17(v) for v in xx], y=[r17(v) for v in yy],
                               vx=[r17(v) for v in vvx], vy=[r17(v) for v in vvy], dev=r17(d), nsub=n)
    runs[key] = rec
    out('%-16s worst deviation from solve_ivp after 300 frames: %.3e AU (%d substeps a frame at the end)'
        % (key, worst, rec['300']['nsub']))
REF['runs'] = runs

# ------------------------------------------------------------------ the collision rule
out('\n# collisions: mass, momentum and the centre of mass are conserved (PhET keeps the heavier')
out('# body\'s mass and gives it the lighter one\'s momentum, which loses the mass -- stated on the page)')
mm = np.array([200.0, 5.0])
xx = np.array([0.0, 0.05]); yy = np.array([0.0, 0.0])
vv = np.array([0.0, 10.0]); vw = np.array([0.0, 0.0])
Mtot = mm.sum()
merged = dict(m=r17(Mtot), x=r17(float((mm * xx).sum() / Mtot)), y=r17(float((mm * yy).sum() / Mtot)),
              vx=r17(float((mm * vw).sum() / Mtot)), vy=r17(float((mm * vv).sum() / Mtot)))
out('   200 + 5 at 0.05 AU apart -> one body of %.6f at (%.9f, %.9f) moving (%.9f, %.9f)'
    % (Mtot, merged['x'], merged['y'], merged['vx'], merged['vy']))
out('   PhET\'s rule would instead keep m = 200 and set v = (%.9f, %.9f)' % (0.0, 5 * 10.0 / 200))
REF['merge'] = merged
REF['merge_phet_vy'] = r17(5 * 10.0 / 200)
out('   radius rule: a 200-mass body is %.9f AU across, a 1e-6 one %.9f (the 0.03 floor)'
    % (max(0.03, 0.023 * 200 ** (1 / 3)), max(0.03, 0.023 * (1e-6) ** (1 / 3))))
REF['radius'] = dict(m200=r17(max(0.03, 0.023 * 200 ** (1 / 3))), tiny=0.03,
                     m250=r17(max(0.03, 0.023 * 250 ** (1 / 3))), m25=r17(max(0.03, 0.023 * 25 ** (1 / 3))))

out('\nREFJSON ' + json.dumps(REF, sort_keys=True))
