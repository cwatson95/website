#!/usr/bin/env python3
"""derive.py — the Python twin of masses-and-springs-basics.html.

Re-derives every closed form the sim implements and prints reference values to
17 significant digits for selfTest() to assert against.  Nothing here is copied
from PhET; the CONSTANTS are read out of PhET's own minified build
(docs/phets/masses-and-springs-basics_en.html, version 1.0.28) and are marked
as PhET's.

The model.  Let y be the downward extension of the spring below its unstretched
length, so the mass hangs at y and the spring pulls up with k*y (Hooke).  With
gravity g down and a linear damper b (PhET's dampingCoefficient, N s/m):

      m y'' = m g - k y - b y'                                             (1)

The equilibrium is y_eq = m g / k, and with u = y - y_eq,

      m u'' + b u' + k u = 0,   u(0) = u0, u'(0) = v0                      (2)

whose characteristic equation is m s^2 + b s + k = 0 -- which is what PhET's own
doc/model.md says it solves.  Write

      w0 = sqrt(k/m),  gam = b/(2 m),  zeta = gam/w0 = b/(2 sqrt(k m))
      s  = w0^2 - gam^2                                                    (3)

and define the two analytic functions (one pair of formulas for all three
regimes, by analytic continuation in s)

      C(t)  = cos(sqrt(s) t)        (s > 0)   cosh(sqrt(-s) t)   (s < 0)
      Sn(t) = sin(sqrt(s) t)/sqrt(s)          sinh(sqrt(-s) t)/sqrt(-s)     (4)

both entire in s, C = 1 - s t^2/2 + ..., Sn = t - s t^3/6 + ...  Then the exact
solution of (2) is

      u(t) = e^{-gam t} [ u0 (C + gam Sn) + v0 Sn ]
      v(t) = e^{-gam t} [ -w0^2 u0 Sn + v0 (C - gam Sn) ]                  (5)

which is also the exact one-step propagator: the sim advances the state by (5)
with t = dt every frame, so its trajectory is the closed form to machine
precision at any frame rate.  An RK4 integrator of (2) is implemented beside it
and measured (below) to be 4th order, converging onto the same trajectory.

Energy: E = 1/2 m v^2 + 1/2 k u^2, dE/dt = -b v^2, so the damper's thermal
energy is E(0) - E(t) and equals b times the integral of v^2 -- checked here by
quadrature, which is an independent route.
"""
import io, os, math
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

OUT = []


def P(*a):
    s = ' '.join(str(x) for x in a)
    OUT.append(s)
    print(s)


def g17(x):
    return repr(float(x))


# =====================================================================
# 1.  PhET's constants, read out of its minified build 1.0.28
# =====================================================================
# MassesAndSpringsConstants (docs/phets/masses-and-springs-basics_en.html):
#   DEFAULT_SPRING_LENGTH:.5, FLOOR_Y:0, CEILING_Y:1.47, SHELF_HEIGHT:.02,
#   HOOK_HEIGHT:.037, HOOK_CENTER:.0185, SLOW_SIM_DT_RATIO:8,
#   DAMPING_RANGE:(0,.7,.3), GRAVITY_RANGE:(0,30,9.8), SPRING_CONSTANT_RANGE:(3,12,6),
#   EARTH_GRAVITY:9.8, MOON_GRAVITY:1.6, JUPITER_GRAVITY:24.8, PLANET_X:14.2,
#   LEFT_SPRING_X:1, RIGHT_SPRING_X:1.3, SPRING_X:1.2
CEILING_Y = 1.47
FLOOR_Y = 0.0
SHELF_H = 0.02
HOOK_H = 0.037
HOOK_C = 0.0185
L0 = 0.5
KMIN, KMAX, KDEF = 3.0, 12.0, 6.0          # N/m, integer-constrained by PhET's slider
BMIN, BMAX, BDEF = 0.0, 0.7, 0.3           # N s/m  (MASSES_AND_SPRINGS; Basics has no slider)
GMIN, GMAX = 0.0, 30.0
G_EARTH, G_MOON, G_JUPITER, G_PLANETX = 9.8, 1.6, 24.8, 14.2
# real surface gravities, for comparison only
G_EARTH_REAL, G_MOON_REAL, G_JUPITER_REAL = 9.81, 1.62, 24.79
# Basics rack: createMass(.25,..), (.25,..), (.1,..), (.1,..), (.05,..), (.05,..)
# and the mystery masses (.2 large, .1 medium, .075 small)
RACK = [0.25, 0.25, 0.10, 0.10, 0.05, 0.05]
MYST = [0.20, 0.10, 0.075]
# Lab (basics): adjustable mass 0.1 default, slider Range(50,300) g; mystery .18 and .12
MASS_G_MIN, MASS_G_MAX, MASS_G_DEF = 50.0, 300.0, 100.0
LAB_MYST = [0.18, 0.12]
# per-screen damping: Stretch sets dampingProperty to .7, Bounce and Lab to 0
B_STRETCH, B_BOUNCE, B_LAB = 0.7, 0.0, 0.0
# Mass node geometry: density option 80, module constants S = 2.5 and y = 4:
#   radius = sqrt(m/(80*2.5*pi))*4,  cylinderHeight = 2.5*radius
MASS_DENS, MASS_S, MASS_Y = 80.0, 2.5, 4.0


def mass_radius(m):
    return math.sqrt(m / (MASS_DENS * MASS_S * math.pi)) * MASS_Y


P('=' * 68)
P("PhET's constants (build 1.0.28 of masses-and-springs-basics)")
P('=' * 68)
P('ceiling %g m, floor %g, shelf %g, hook height %g, hook centre %g' % (CEILING_Y, FLOOR_Y, SHELF_H, HOOK_H, HOOK_C))
P('natural spring length %g m; springs at x = 1.0 and 1.3 m (two-spring screens), 1.2 m (lab)' % L0)
P('spring constant %g..%g N/m default %g (integers); damping %g..%g N s/m default %g'
  % (KMIN, KMAX, KDEF, BMIN, BMAX, BDEF))
P('gravity slider %g..%g m/s^2; Moon %g, Earth %g, Planet X %g, Jupiter %g'
  % (GMIN, GMAX, G_MOON, G_EARTH, G_PLANETX, G_JUPITER))
P('real surface gravities: Moon %g, Earth %g, Jupiter %g m/s^2' % (G_MOON_REAL, G_EARTH_REAL, G_JUPITER_REAL))
P('rack %s kg + mystery %s kg; lab slider %g..%g g default %g, lab mystery %s kg'
  % (RACK, MYST, MASS_G_MIN, MASS_G_MAX, MASS_G_DEF, LAB_MYST))
P('screen damping: stretch %g, bounce %g, lab %g N s/m' % (B_STRETCH, B_BOUNCE, B_LAB))
for m in (0.05, 0.1, 0.25, 0.3):
    P('mass block %.3f kg: radius %s m, height %s m'
      % (m, g17(mass_radius(m)), g17(MASS_S * mass_radius(m))))

# =====================================================================
# 2.  Hooke's law and the equilibrium extension, over everything the sim allows
# =====================================================================
P('')
P('=' * 68)
P("Hooke's law:  F = -k y,  y_eq = m g / k  (every setting the sim allows)")
P('=' * 68)

MASSES_ALL = sorted(set(RACK + MYST + LAB_MYST + [i / 1000.0 for i in range(50, 301)]))
KS = [float(k) for k in range(3, 13)]
GS = [G_MOON, G_EARTH, G_PLANETX, G_JUPITER]

# checksum: plain left-to-right float sum, reproducible bit-for-bit in JS
tot = 0.0
mx = 0.0
n = 0
for m in MASSES_ALL:
    for k in KS:
        for gv in GS:
            y = m * gv / k
            tot += y
            if y > mx:
                mx = y
            n += 1
P('grid: %d masses x %d spring constants x %d planets = %d states' % (len(MASSES_ALL), len(KS), len(GS), n))
P('sum of y_eq over the grid  = %s m' % g17(tot))
P('largest y_eq on the grid   = %s m  (m = 0.3 kg, k = 3 N/m, Jupiter)' % g17(mx))
P('largest possible y_eq      = %s m  (m = 0.3, k = 3, g = 30: through the floor)' % g17(0.3 * 30.0 / 3.0))

SPOT = [(0.25, 6.0, G_EARTH), (0.25, 6.0, G_MOON), (0.25, 6.0, G_JUPITER), (0.25, 6.0, G_PLANETX),
        (0.10, 6.0, G_EARTH), (0.10, 3.0, G_EARTH), (0.10, 12.0, G_EARTH),
        (0.05, 3.0, G_MOON), (0.30, 12.0, G_JUPITER), (0.075, 9.0, G_PLANETX),
        (0.18, 6.0, G_EARTH), (0.12, 6.0, G_EARTH)]
for (m, k, gv) in SPOT:
    P('  m %-6g k %-5g g %-5g ->  y_eq = %s m  ( %s cm )' % (m, k, gv, g17(m * gv / k), g17(100 * m * gv / k)))
# the Planet X inversion: read the extension, get g
P('Planet X inverted: m 0.1 kg, k 6 N/m, y_eq %s m  ->  g = k y/m = %s m/s^2'
  % (g17(0.1 * G_PLANETX / 6.0), g17(6.0 * (0.1 * G_PLANETX / 6.0) / 0.1)))
P('Planet X is %g m/s^2 -- PhET\'s invented value; no solar-system body has it' % G_PLANETX)
P('  (it sits between Earth %g and Jupiter %g; Neptune 11.15 and Saturn 10.44 are the nearest real ones)'
  % (G_EARTH, G_JUPITER))
# two springs, the Stretch screen's own comparison
P('stretch screen: 250 g on k = 3 and on k = 12, Earth: %s cm and %s cm (ratio %s)'
  % (g17(100 * 0.25 * G_EARTH / 3), g17(100 * 0.25 * G_EARTH / 12), g17(4.0)))

# =====================================================================
# 3.  The damped harmonic oscillator, closed form
# =====================================================================
P('')
P('=' * 68)
P('the damped oscillator:  m u" + b u\' + k u = 0')
P('=' * 68)


def CSn(s, t):
    """C(t), Sn(t) of (4), entire in s; the three-term series below the join.

    The join is |s| t^2 < 1e-5, chosen so that BOTH terms of each series are
    load-bearing at the top of the branch (the x^2 terms are worth 4.167e-12 of
    C and 8.333e-13 of Sn there) while the truncation, x^3/720 = 1.4e-18, is
    still far below a rounding error.  Below 1e-8 the x^2 terms fall under half
    an ulp and the double is bit-identical with or without them.
    """
    if abs(s) * t * t < 1e-5:
        s2 = s * s
        t2 = t * t
        C = 1.0 - s * t2 / 2.0 + s2 * t2 * t2 / 24.0
        Sn = t * (1.0 - s * t2 / 6.0 + s2 * t2 * t2 / 120.0)
    elif s > 0:
        w = math.sqrt(s)
        C = math.cos(w * t)
        Sn = math.sin(w * t) / w
    else:
        r = math.sqrt(-s)
        C = math.cosh(r * t)
        Sn = math.sinh(r * t) / r
    return C, Sn


def prop(m, k, b, u0, v0, t):
    """exact (u, v) at time t -- equation (5)."""
    w02 = k / m
    gam = b / (2.0 * m)
    s = w02 - gam * gam
    C, Sn = CSn(s, t)
    e = math.exp(-gam * t)
    return (e * (u0 * (C + gam * Sn) + v0 * Sn),
            e * (-w02 * u0 * Sn + v0 * (C - gam * Sn)))


def rk4(m, k, b, u0, v0, T, n):
    """classical RK4 on (2), n equal steps."""
    h = T / n
    u, v = u0, v0

    def f(u, v):
        return v, (-k * u - b * v) / m
    for _ in range(n):
        a1, b1 = f(u, v)
        a2, b2 = f(u + h * a1 / 2, v + h * b1 / 2)
        a3, b3 = f(u + h * a2 / 2, v + h * b2 / 2)
        a4, b4 = f(u + h * a3, v + h * b3)
        u += h * (a1 + 2 * a2 + 2 * a3 + a4) / 6
        v += h * (b1 + 2 * b2 + 2 * b3 + b4) / 6
    return u, v


CASES = [('PhET bounce, 250 g on k = 6, undamped', 0.25, 6.0, 0.0, 0.08, 0.0),
         ('PhET stretch, 100 g on k = 6, b = 0.7', 0.10, 6.0, 0.7, 0.05, 0.0),
         ('lightest/softest, 50 g on k = 3, b = 0.7 (zeta closest to 1)', 0.05, 3.0, 0.7, 0.06, 0.0),
         ('heaviest/stiffest, 300 g on k = 12, b = 0.7', 0.30, 12.0, 0.7, 0.04, -0.2),
         ('critically damped (beyond PhET: b = 2 sqrt(km))', 0.10, 6.0, 2 * math.sqrt(0.6), 0.05, 0.0),
         ('overdamped (beyond PhET: b = 3.0)', 0.10, 6.0, 3.0, 0.05, 0.0)]

for (nm, m, k, b, u0, v0) in CASES:
    w0 = math.sqrt(k / m)
    gam = b / (2 * m)
    z = gam / w0
    s = w0 * w0 - gam * gam
    P('')
    P('--- %s' % nm)
    P('  m %g kg, k %g N/m, b %s N s/m, u0 %g m, v0 %g m/s' % (m, k, g17(b), u0, v0))
    P('  w0 = %s rad/s   T0 = 2 pi sqrt(m/k) = %s s' % (g17(w0), g17(2 * math.pi / w0)))
    P('  gam = b/2m = %s 1/s   zeta = %s   b_crit = 2 sqrt(km) = %s' % (g17(gam), g17(z), g17(2 * math.sqrt(k * m))))
    if s > 0:
        wd = math.sqrt(s)
        Td = 2 * math.pi / wd
        P('  underdamped: w_d = %s rad/s   T_d = %s s   T_d/T0 = %s' % (g17(wd), g17(Td), g17(Td / (2 * math.pi / w0))))
        P('  log decrement delta = gam T_d = 2 pi zeta/sqrt(1-zeta^2) = %s' % g17(gam * Td))
        P('  amplitude ratio per damped period e^-delta = %s' % g17(math.exp(-gam * Td)))
        P('  quality factor Q = 1/(2 zeta) = %s' % g17(1 / (2 * z)) if z > 0 else '  Q = infinite (no damping)')
    elif s == 0:
        P('  critically damped exactly: zeta = 1, one real root -gam')
    else:
        r = math.sqrt(-s)
        P('  overdamped: roots %s and %s 1/s; slow time constant %s s'
          % (g17(-gam + r), g17(-gam - r), g17(1 / (gam - r))))
    for t in (0.1, 0.5, 1.0, 2.0):
        u, v = prop(m, k, b, u0, v0, t)
        P('  t = %-4g  u = %-24s v = %s' % (t, g17(u), g17(v)))
    # the propagator IS the solution: group property
    ua, va = prop(m, k, b, u0, v0, 1.3)
    ub, vb = prop(m, k, b, *prop(m, k, b, u0, v0, 0.7), t=0.6)
    P('  group property |P(0.7)P(0.6) - P(1.3)| = %s, %s' % (g17(abs(ua - ub)), g17(abs(va - vb))))
    # solve_ivp, an independent route
    sol = solve_ivp(lambda t, y: [y[1], (-k * y[0] - b * y[1]) / m], [0, 2.0], [u0, v0],
                    rtol=1e-12, atol=1e-14, dense_output=True)
    us, vs = sol.sol(2.0)
    ue, ve = prop(m, k, b, u0, v0, 2.0)
    P('  scipy solve_ivp at t = 2: u %s (closed form %s), |d| = %s' % (g17(us), g17(ue), g17(abs(us - ue))))
    P('                            v %s (closed form %s), |d| = %s' % (g17(vs), g17(ve), g17(abs(vs - ve))))
    # RK4 order
    prev = None
    P('  RK4 to t = 2 s:')
    for nst in (200, 400, 800, 1600):
        ur, vr = rk4(m, k, b, u0, v0, 2.0, nst)
        err = math.hypot(ur - ue, vr - ve)
        rat = '' if prev is None else '  ratio %s  (order %s)' % (g17(prev / err), g17(math.log(prev / err) / math.log(2)))
        P('    n = %-5d |err| = %-24s%s' % (nst, g17(err), rat))
        prev = err
    # energy
    E0 = 0.5 * m * v0 * v0 + 0.5 * k * u0 * u0
    for t in (1.0, 2.0):
        u, v = prop(m, k, b, u0, v0, t)
        E = 0.5 * m * v * v + 0.5 * k * u * u
        I = quad(lambda tt: prop(m, k, b, u0, v0, tt)[1] ** 2, 0, t, limit=400)[0]
        P('  energy: E(0) = %s J, E(%g) = %s J; b*int v^2 dt = %s J, residual %s'
          % (g17(E0), t, g17(E), g17(b * I), g17(abs(E0 - E - b * I))))

# =====================================================================
# 4.  Which damping regimes the sim's own ranges can reach
# =====================================================================
P('')
P('=' * 68)
P('the reachable damping regimes')
P('=' * 68)
mlo, mhi = MASS_G_MIN / 1000.0, MASS_G_MAX / 1000.0
bc_min = 2 * math.sqrt(KMIN * mlo)
bc_max = 2 * math.sqrt(KMAX * mhi)
P('b_crit = 2 sqrt(k m); over k in [%g,%g], m in [%g,%g] kg it runs %s .. %s N s/m'
  % (KMIN, KMAX, mlo, mhi, g17(bc_min), g17(bc_max)))
P("PhET's damping slider tops out at b = %g N s/m < %s, so zeta_max = %s < 1:"
  % (BMAX, g17(bc_min), g17(BMAX / bc_min)))
P('  EVERY state the sim can reach is UNDERDAMPED.  Critical and overdamped need')
P('  b >= %s N s/m, which is %s times the top of the slider.' % (g17(bc_min), g17(bc_min / BMAX)))
P('  (Masses and Springs: Basics itself has no damping slider at all: its three')
P('   screens fix b at %g (stretch), %g (bounce) and %g (lab).)' % (B_STRETCH, B_BOUNCE, B_LAB))
P('zeta at the corners of the box, b = %g:' % BMAX)
for k in (KMIN, KMAX):
    for m in (mlo, mhi):
        P('  k %-5g m %-5g  zeta = %s   T_d/T0 = %s'
          % (k, m, g17(BMAX / (2 * math.sqrt(k * m))), g17(1 / math.sqrt(1 - (BMAX / (2 * math.sqrt(k * m))) ** 2))))

# =====================================================================
# 5.  The period, measured from the motion
# =====================================================================
P('')
P('=' * 68)
P('the period, measured from the integrated motion')
P('=' * 68)
for (m, k, b) in [(0.1, 6.0, 0.0), (0.25, 6.0, 0.0), (0.1, 12.0, 0.0), (0.1, 6.0, 0.35), (0.05, 3.0, 0.7)]:
    w0 = math.sqrt(k / m)
    gam = b / (2 * m)
    wd = math.sqrt(w0 * w0 - gam * gam)
    T0 = 2 * math.pi / w0
    Td = 2 * math.pi / wd
    f = lambda t: prop(m, k, b, 0.05, 0.0, t)[0]
    # u starts at a maximum, so zeros are at Td/4 + n Td/2 (shifted a little by damping)
    z1 = brentq(f, 1e-9, Td * 0.6, xtol=1e-15, rtol=8.9e-16)
    z2 = brentq(f, Td * 0.6, Td * 1.1, xtol=1e-15, rtol=8.9e-16)
    z3 = brentq(f, Td * 1.1, Td * 1.6, xtol=1e-15, rtol=8.9e-16)
    P('m %-5g k %-5g b %-5g: T0 = %s s, T_d = %s s' % (m, k, b, g17(T0), g17(Td)))
    P('   zeros at %s, %s, %s -> 2*(z3-z1)/2 = %s  (|d| = %s)'
      % (g17(z1), g17(z2), g17(z3), g17(z3 - z1), g17(abs((z3 - z1) - Td))))
    # peaks: u' = 0
    pk = brentq(lambda t: prop(m, k, b, 0.05, 0.0, t)[1], Td * 0.4, Td * 0.9, xtol=1e-15, rtol=8.9e-16)
    pk2 = brentq(lambda t: prop(m, k, b, 0.05, 0.0, t)[1], Td * 0.9, Td * 1.4, xtol=1e-15, rtol=8.9e-16)
    P('   turning points at %s and %s; |u| ratio consecutive peaks = %s (e^-delta/2 = %s)'
      % (g17(pk), g17(pk2), g17(abs(f(pk2) / f(pk))), g17(math.exp(-gam * Td / 2))))

P('')
P('gravity does not touch the period, only the equilibrium:')
for gv, nm in [(G_MOON, 'Moon'), (G_EARTH, 'Earth'), (G_PLANETX, 'Planet X'), (G_JUPITER, 'Jupiter')]:
    P('  %-9s g %-5g: T = %s s, y_eq = %s cm' % (nm, gv, g17(2 * math.pi * math.sqrt(0.1 / 6.0)), g17(100 * 0.1 * gv / 6.0)))

# =====================================================================
# 6.  The undamped limit: exact energy conservation
# =====================================================================
P('')
P('=' * 68)
P('the undamped limit')
P('=' * 68)
m, k, u0, v0 = 0.1, 6.0, 0.05, 0.3
E0 = 0.5 * m * v0 * v0 + 0.5 * k * u0 * u0
worst = 0.0
for i in range(1, 2001):
    t = i * 0.01
    u, v = prop(m, k, 0.0, u0, v0, t)
    E = 0.5 * m * v * v + 0.5 * k * u * u
    worst = max(worst, abs(E - E0) / E0)
P('m %g k %g u0 %g v0 %g: E = %s J, worst relative drift over 2000 exact steps = %s'
  % (m, k, u0, v0, g17(E0), g17(worst)))
A = math.sqrt(u0 * u0 + (v0 / math.sqrt(k / m)) ** 2)
P('amplitude A = sqrt(u0^2 + (v0/w0)^2) = %s m; E = 1/2 k A^2 = %s J' % (g17(A), g17(0.5 * k * A * A)))
P('RK4 energy drift over the same 20 s at 2000 steps:')
for nst in (2000, 4000):
    ur, vr = rk4(m, k, 0.0, u0, v0, 20.0, nst)
    ER = 0.5 * m * vr * vr + 0.5 * k * ur * ur
    P('  n = %-6d E = %s J, relative drift %s' % (nst, g17(ER), g17(abs(ER - E0) / E0)))

# =====================================================================
# 7.  The full energy ledger with gravity (what PhET's energy bars show)
# =====================================================================
P('')
P('=' * 68)
P('the energy ledger, measured from the hanging position')
P('=' * 68)
P('y is the extension and the gravitational zero is at the BOTTOM of the swing,')
P('y_bot = 2 m g / k, so all three shares are non-negative:')
P('  KE = 1/2 m v^2,  PE_elastic = 1/2 k y^2,  PE_grav = m g (y_bot - y),')
P('  KE + PE_el + PE_grav = 1/2 m v^2 + 1/2 k u^2 + 3 (m g)^2/(2 k)  is constant when b = 0,')
P('  and at the release (y = 0, v = 0) that constant is 2 (m g)^2 / k.')
m, k, gv, b = 0.1, 6.0, G_EARTH, 0.0
yeq = m * gv / k
u0, v0 = 0.08, 0.0
off = 1.5 * (m * gv) ** 2 / k
P('m %g, k %g, g %g: y_eq = %s m, y_bot = %s m, offset 3(mg)^2/2k = %s J'
  % (m, k, gv, g17(yeq), g17(2 * yeq), g17(off)))
for t in (0.0, 0.2, 0.4, 0.8):
    u, v = prop(m, k, b, u0, v0, t)
    y = u + yeq
    KE = 0.5 * m * v * v
    PEe = 0.5 * k * y * y
    PEg = m * gv * (2 * yeq - y)
    P('  t %-5g y %-22s KE %-22s PE_el %-22s PE_gr %-22s sum %s'
      % (t, g17(y), g17(KE), g17(PEe), g17(PEg), g17(KE + PEe + PEg)))
P('  invariant 1/2 m v^2 + 1/2 k u^2 + offset = %s J' % g17(0.5 * k * u0 * u0 + off))
P('  released from y = 0: the ledger total 2(mg)^2/k = %s J' % g17(2 * (m * gv) ** 2 / k))
P('  and the three shares there: KE 0, PE_el 0, PE_gr = %s J' % g17(m * gv * 2 * yeq))
# thermal, damped
b = 0.35
P('with b = %g the damper takes E(0) - E(t):' % b)
E0 = 0.5 * k * u0 * u0
for t in (0.5, 1.0, 2.0, 5.0):
    u, v = prop(m, k, b, u0, v0, t)
    E = 0.5 * m * v * v + 0.5 * k * u * u
    P('  t %-5g  E %-24s  E_thermal %-24s  fraction %s' % (t, g17(E), g17(E0 - E), g17((E0 - E) / E0)))

# =====================================================================
# 8.  The spring drawing: PhET's coil, and the stage
# =====================================================================
P('')
P('=' * 68)
P('the stage')
P('=' * 68)
P('spring bottom at natural length: %s m above the floor' % g17(CEILING_Y - L0))
for (m, k, gv) in [(0.25, 6.0, G_EARTH), (0.3, 3.0, G_JUPITER), (0.3, 3.0, 30.0)]:
    y = m * gv / k
    bot = CEILING_Y - L0 - y
    P('  m %-5g k %-4g g %-5g: extension %s m, spring bottom %s m %s'
      % (m, k, gv, g17(y), g17(bot), '(below the floor: PhET lets it go)' if bot < 0 else ''))

# =====================================================================
# 9.  Period-trace geometry: PhET marks quarter periods from a turning point
# =====================================================================
P('')
P('=' * 68)
P('the period trace')
P('=' * 68)
m, k, b = 0.1, 6.0, 0.0
T0 = 2 * math.pi * math.sqrt(m / k)
P('released from rest at u0: the trace runs peak -> centre -> trough -> centre -> peak,')
P('four quarter periods of %s s each, one period %s s' % (g17(T0 / 4), g17(T0)))
u0 = 0.06
for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
    u, v = prop(m, k, b, u0, 0.0, frac * T0)
    P('  t = %-6s T0: u = %-24s v = %s' % (g17(frac), g17(u), g17(v)))

# =====================================================================
# 10.  A sweep that pins the propagator against solve_ivp everywhere
# =====================================================================
P('')
P('=' * 68)
P('propagator vs scipy over the whole control space')
P('=' * 68)
worst_u = worst_v = 0.0
cnt = 0
for m in (0.05, 0.1, 0.18, 0.25, 0.3):
    for k in (3.0, 6.0, 9.0, 12.0):
        for b in (0.0, 0.2, 0.35, 0.7):
            sol = solve_ivp(lambda t, y, k=k, b=b, m=m: [y[1], (-k * y[0] - b * y[1]) / m],
                            [0, 1.7], [0.05, -0.1], rtol=1e-12, atol=1e-15)
            ue, ve = prop(m, k, b, 0.05, -0.1, 1.7)
            worst_u = max(worst_u, abs(sol.y[0][-1] - ue))
            worst_v = max(worst_v, abs(sol.y[1][-1] - ve))
            cnt += 1
P('%d (m, k, b) states: worst |du| = %s, worst |dv| = %s' % (cnt, g17(worst_u), g17(worst_v)))

here = os.path.dirname(os.path.abspath(__file__))
io.open(os.path.join(here, 'refvals.txt'), 'w', encoding='utf-8').write('\n'.join(OUT) + '\n')
print('\n[wrote refvals.txt, %d lines]' % len(OUT))
