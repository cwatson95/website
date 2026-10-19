#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""derive.py — the Python twin for docs/phets_revised/rutherford-scattering.html.

Re-derives every closed form the sim implements and prints reference values to
15 significant figures.  make_refs.py turns the printed block into p7_refs.js,
so no number the JS suite asserts against was typed by hand.

Nothing here is quoted from memory: every closed form is checked against an
independent numerical route (quadrature, solve_ivp of the equations of motion,
or a brute-force sum), and the constants come from scipy.constants.

    python3 derive.py > refvals.txt
"""
from __future__ import print_function

import math

import numpy as np
import scipy.constants as sc
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq, minimize_scalar

OUT = []


def p(label, value, ind=0):
    """One reference line: label, two or more spaces, value.  make_refs.py
    parses exactly this, and an indented label belongs to the one above it."""
    if isinstance(value, float):
        if value != value or value in (float("inf"), float("-inf")):
            s = repr(value)
        else:
            s = "%.15g" % value
    else:
        s = str(value)
    pad = "  " * ind
    line = "%-62s  %s" % (pad + label, s)
    print(line)
    OUT.append(line)


def head(t):
    print("")
    print("===== %s =====" % t)


# =====================================================================
# 1. constants
# =====================================================================
head("1. constants (scipy.constants, CODATA 2022)")
C = sc.c
E_Q = sc.e
EPS0 = sc.epsilon_0
KE = 1.0 / (4 * math.pi * EPS0)
M_E = sc.m_e
M_U = sc.value("atomic mass constant")
N_A = sc.N_A
MEV = 1e6 * E_Q
FM = 1e-15
BARN = 1e-28
M_ALPHA = sc.value("alpha particle mass")

p("c (m/s)", C)
p("e (C)", E_Q)
p("eps0 (F/m)", EPS0)
p("k = 1/(4 pi eps0) (N m^2/C^2)", KE)
p("m_e (kg)", M_E)
p("m_alpha (kg)", M_ALPHA)
p("atomic mass constant (kg)", M_U)
p("N_A (1/mol)", N_A)
# k e^2 in MeV fm -- the constant every nuclear text quotes as 1.44 MeV fm.
# Derived, never typed.
KE2_MEVFM = KE * E_Q * E_Q / (MEV * FM)
p("k e^2 (MeV fm)", KE2_MEVFM)
p("m_e/m_alpha", M_E / M_ALPHA)
p("max lab deflection off a free electron, rad (asin m_e/m_alpha)",
  math.asin(M_E / M_ALPHA))
p("max lab deflection off a free electron, deg",
  math.degrees(math.asin(M_E / M_ALPHA)))


# =====================================================================
# 2. the Rutherford orbit -- closed forms and independent routes
# =====================================================================
head("2. the Rutherford hyperbola")

# D is the distance of closest approach for a head-on hit:  E = k q1 q2 / D.
# a = D/2 is the constant in b = a cot(theta/2).


def D_of(Z1, Z2, E_J):
    return KE * Z1 * Z2 * E_Q * E_Q / E_J


def theta_of_b(b, D):
    """closed form: tan(theta/2) = D/(2b)"""
    if b == 0.0:
        return math.pi
    return 2.0 * math.atan(D / (2.0 * b))


def b_of_theta(th, D):
    return 0.5 * D / math.tan(th / 2.0)


def rmin_of_b(b, D):
    return 0.5 * D + math.sqrt(0.25 * D * D + b * b)


def dsdo(th, D):
    """Rutherford differential cross section, (D/4)^2 / sin^4(theta/2)"""
    s = math.sin(th / 2.0)
    return (D / 4.0) ** 2 / (s ** 4)


def rofphi(phi, b, D):
    """the orbit in polar form about the nucleus, phi measured from the
    INCOMING asymptote: the particle enters at phi -> 0+ from (b, -inf)."""
    return b * b / (b * math.sin(phi) + 0.5 * D * (math.cos(phi) - 1.0))


def phi_inf(b, D):
    """where r -> infinity on the way out; theta = pi - phi_inf"""
    return 2.0 * math.atan(2.0 * b / D)


# -- quadrature route for theta(b): theta = pi - 2 b int dr/(r^2 sqrt(...)) --
def theta_quad(b, D):
    """u = rmin/r puts it on [0,1]; u = 1 - s^2 removes the inverse-square-root
    singularity at the turning point exactly."""
    rm = rmin_of_b(b, D)

    def f(s):
        u = 1.0 - s * s
        rad = 1.0 - D * u / rm - (b * b) * u * u / (rm * rm)
        if rad <= 0:
            return 0.0
        return 2.0 * s / math.sqrt(rad)

    val, _ = quad(f, 0.0, 1.0, limit=200, epsabs=1e-14, epsrel=1e-13)
    return math.pi - 2.0 * (b / rm) * val


D_TEST = 3.0
for b in (0.25, 0.5, 1.0, 2.0, 5.0, 20.0):
    th = theta_of_b(b, D_TEST)
    tq = theta_quad(b, D_TEST)
    p("theta(b=%g, D=3) closed form, rad" % b, th)
    p("quadrature", tq, 1)
    p("rel. difference", abs(th - tq) / th, 1)

p("theta(b=0, D=3) head-on, rad", theta_of_b(0.0, D_TEST))
p("rmin(b=0, D=3) = D", rmin_of_b(0.0, D_TEST))
for b in (0.5, 1.0, 3.0):
    p("rmin(b=%g, D=3)" % b, rmin_of_b(b, D_TEST))
    p("a (1 + 1/sin(theta/2))", 0.5 * D_TEST * (1 + 1 / math.sin(theta_of_b(b, D_TEST) / 2)), 1)
p("b(theta=90deg, D=3) = D/2", b_of_theta(math.pi / 2, D_TEST))
p("eccentricity at b=1, D=3 (1/sin(theta/2))", 1.0 / math.sin(theta_of_b(1.0, D_TEST) / 2))

# -- the conic is the orbit: check r(phi) against the polar-form invariant,
#    the asymptote offset, and the turning point --
head("2b. the conic r(phi) = b^2 / (b sin phi + (D/2)(cos phi - 1))")
for b in (0.5, 1.0, 4.0):
    pi_ = phi_inf(b, D_TEST)
    p("phi_inf(b=%g, D=3), rad" % b, pi_)
    p("pi - theta", math.pi - theta_of_b(b, D_TEST), 1)
    # turning point: r is minimum at phi = phi_inf/2 by symmetry
    rm = rofphi(pi_ / 2.0, b, D_TEST)
    p("r at phi_inf/2", rm, 1)
    p("rmin closed form", rmin_of_b(b, D_TEST), 1)
    # the perpendicular offset of the INCOMING asymptote from the nucleus is b
    small = 1e-9
    r0 = rofphi(small, b, D_TEST)
    p("x = r sin(phi) at phi=1e-9 (-> b)", r0 * math.sin(small), 1)
    # the outgoing asymptote's perpendicular offset is b as well
    r1 = rofphi(pi_ - small, b, D_TEST)
    x1, y1 = r1 * math.sin(pi_ - small), -r1 * math.cos(pi_ - small)
    # distance from origin to the line through (x1,y1) with direction (sin,-cos)
    dx, dy = math.sin(pi_), -math.cos(pi_)
    off = abs(x1 * dy - y1 * dx)
    p("outgoing asymptote offset (-> b)", off, 1)

# -- b recovered from a point on the orbit: b^2 - x0 b + (D/2)(y0 + r0) = 0 --
head("2c. the entry quadratic  b = [x0 + sqrt(x0^2 - 2 D (y0 + r0))]/2")
for (b, phi) in ((1.0, 0.30), (4.0, 0.10), (0.5, 0.80)):
    r0 = rofphi(phi, b, D_TEST)
    x0, y0 = r0 * math.sin(phi), -r0 * math.cos(phi)
    disc = x0 * x0 - 2.0 * D_TEST * (y0 + r0)
    brec = 0.5 * (x0 + math.sqrt(disc))
    p("b recovered at b=%g phi=%g" % (b, phi), brec)
    p("error", abs(brec - b), 1)


# =====================================================================
# 3. the equations of motion -- solve_ivp, independent of every formula above
# =====================================================================
head("3. Newton's equations (solve_ivp, DOP853, rtol 1e-12)")
# scaled: unit mass, unit asymptotic speed, so E = 1/2 and U(r) = (D/2)/r.
# Force = +(D/2) r_vec / r^3.


def rhs(t, y, D):
    x, yy, vx, vy = y
    r = math.hypot(x, yy)
    f = 0.5 * D / (r ** 3)
    return [vx, vy, f * x, f * yy]


def integrate_orbit(b, D, y0=-400.0, tmax=None):
    r0 = math.hypot(b, y0)
    # start on the orbit, not on the straight line: use the conic point whose
    # y equals y0, so the integration and the closed form describe one orbit.
    phi0 = math.atan2(b, -y0)
    # refine phi0 so that -r cos(phi) = y0 exactly
    phi0 = brentq(lambda ph: -rofphi(ph, b, D) * math.cos(ph) - y0,
                  1e-12, phi_inf(b, D) / 2, xtol=1e-16, rtol=1e-15)
    r = rofphi(phi0, b, D)
    x, yy = r * math.sin(phi0), -r * math.cos(phi0)
    v = math.sqrt(1.0 - D / r)            # v_inf = 1
    # velocity direction: tangent to the conic, moving toward increasing phi
    dr = _drdphi(phi0, b, D)
    ex, ey = math.sin(phi0), -math.cos(phi0)         # radial unit
    tx, ty = math.cos(phi0), math.sin(phi0)          # d/dphi of the radial unit
    vx = (dr * ex + r * tx)
    vy = (dr * ey + r * ty)
    n = math.hypot(vx, vy)
    vx, vy = v * vx / n, v * vy / n
    if tmax is None:
        tmax = 2.0 * abs(y0) / 1.0 * 1.6
    sol = solve_ivp(rhs, (0.0, tmax), [x, yy, vx, vy], args=(D,),
                    rtol=1e-12, atol=1e-14, method="DOP853", dense_output=True,
                    max_step=abs(y0) / 8.0)
    return sol


def _drdphi(phi, b, D):
    den = b * math.sin(phi) + 0.5 * D * (math.cos(phi) - 1.0)
    dden = b * math.cos(phi) - 0.5 * D * math.sin(phi)
    return -b * b * dden / (den * den)


for b in (0.5, 2.0, 8.0):
    sol = integrate_orbit(b, D_TEST)
    ys = sol.y
    n = ys.shape[1]
    # conservation
    E = 0.5 * (ys[2] ** 2 + ys[3] ** 2) + 0.5 * D_TEST / np.hypot(ys[0], ys[1])
    L = ys[0] * ys[3] - ys[1] * ys[2]
    p("b=%g: energy drift (max |E-E0|/E0)" % b, float(np.max(np.abs(E - E[0])) / E[0]))
    p("angular momentum drift (max |L-L0|/|L0|)",
      float(np.max(np.abs(L - L[0])) / abs(L[0])), 1)
    p("L0 (should be b, v_inf = 1)", float(L[0]), 1)
    p("E0 (should be 1/2)", float(E[0]), 1)
    # final direction vs the closed form
    vx, vy = ys[2, n - 1], ys[3, n - 1]
    th = math.atan2(vx, vy)               # deflection from +y
    p("final deflection, rad", float(th), 1)
    p("closed form 2 atan(D/2b)", theta_of_b(b, D_TEST), 1)
    p("rel. difference", abs(th - theta_of_b(b, D_TEST)) / theta_of_b(b, D_TEST), 1)
    # every integrated point lies on the conic: r(phi) must match
    phis = np.arctan2(ys[0], -ys[1])
    rr = np.hypot(ys[0], ys[1])
    rc = np.array([rofphi(float(f), b, D_TEST) if 1e-12 < f < phi_inf(b, D_TEST) - 1e-12
                   else float("nan") for f in phis])
    m = np.isfinite(rc)
    p("max |r_integrated - r_conic| / r", float(np.max(np.abs(rr[m] - rc[m]) / rr[m])), 1)
    # closest approach along the integrated path vs the closed form
    fr = minimize_scalar(lambda t: float(np.hypot(*sol.sol(t)[:2])),
                         bounds=(0.0, sol.t[-1]), method="bounded",
                         options={"xatol": 1e-12})
    p("rmin integrated", float(fr.fun), 1)
    p("rmin closed form", rmin_of_b(b, D_TEST), 1)

# The direction only reaches the asymptote at r = infinity, so the residual of
# the integrated deflection is a TRUNCATION, and the thing worth pinning is its
# RATE: it falls as 1/r_final (Known-bad: assert the rate of approach, never
# that a limit is reached exactly).
head("3a. the deflection residual is a truncation that falls as 1/r_final")
for b in (2.0,):
    for y0 in (-200.0, -400.0, -800.0):
        sol = integrate_orbit(b, D_TEST, y0=y0)
        n = sol.y.shape[1]
        rf = math.hypot(sol.y[0, n - 1], sol.y[1, n - 1])
        th = math.atan2(sol.y[2, n - 1], sol.y[3, n - 1])
        err = abs(th - theta_of_b(b, D_TEST))
        p("b=2, start y0=%g: final r" % y0, rf)
        p("deflection residual (rad)", err, 1)
        p("residual * r_final^2 (constant => the rate is 1/r^2)", err * rf * rf, 1)

head("3b. head-on, b = 0 exactly")
# The radial problem has a cusp in r(t) at the turn, so a polynomial dense
# output cannot find it (a first attempt read 2.9777 for 3, an 0.74% "error"
# that was entirely the interpolant).  Sundman's regularisation ds = dt/r
# removes the cusp: dr/ds = r v, dv/ds = D/(2 r).
# The starting speed must be the speed AT r0, sqrt(1 - D/r0), not v_inf: a
# first version launched at v = -1 from r = 400 and the integration dutifully
# turned at 2.9777, which is the right answer to the wrong question (that orbit
# really does have E = 0.50375 and turns at (D/2)/E).
R0H = 400.0
V0H = -math.sqrt(1.0 - D_TEST / R0H)
p("head-on launch radius", R0H)
p("head-on launch speed sqrt(1 - D/r0)", -V0H)
sol = solve_ivp(lambda s, y, D: [y[0] * y[1], 0.5 * D / y[0]],
                (0.0, 4000.0), [R0H, V0H], args=(D_TEST,),
                rtol=1e-13, atol=1e-16, method="DOP853", dense_output=True,
                events=[lambda s, y, D: y[1]])
tturn = float(sol.t_events[0][0])
rturn = float(sol.sol(tturn)[0])
p("turning radius at b=0 (Sundman-regularised integration)", rturn)
p("D", D_TEST)
p("rel. difference", abs(rturn - D_TEST) / D_TEST)
# and the exact parametric solution of the radial problem, r = (D/2)(cosh n + 1),
# t = (D/2)(sinh n + n), which satisfies v^2 = 1 - D/r identically
for eta in (0.0, 0.5, 2.0):
    r = 0.5 * D_TEST * (math.cosh(eta) + 1.0)
    tt = 0.5 * D_TEST * (math.sinh(eta) + eta)
    v = math.sqrt(1.0 - D_TEST / r) if r > D_TEST else 0.0
    # drdt from the parametric form: (dr/deta)/(dt/deta)
    drdt = (0.5 * D_TEST * math.sinh(eta)) / (0.5 * D_TEST * (math.cosh(eta) + 1.0))
    p("radial parametric: eta=%g -> r" % eta, r)
    p("t", tt, 1)
    p("v from energy", v, 1)
    p("dr/dt from the parametrisation", drdt, 1)
    p("difference", abs(v - drdt), 1)
# the b -> 0 limit of the hyperbola: rmin = D + b^2/D + O(b^4)
for b in (1e-2, 1e-3, 1e-4):
    p("rmin(b=%g) - D" % b, rmin_of_b(b, D_TEST) - D_TEST)
    p("b^2/D", b * b / D_TEST, 1)
    p("pi - theta(b)", math.pi - theta_of_b(b, D_TEST), 1)
    p("2b/a = 4b/D", 4 * b / D_TEST, 1)


# =====================================================================
# 4. the differential cross section, as a Jacobian
# =====================================================================
head("4. dsigma/dOmega = (b/sin theta)|db/dtheta| = (D/4)^2 / sin^4(theta/2)")
for thdeg in (1.0, 5.0, 15.0, 30.0, 60.0, 90.0, 135.0, 179.0):
    th = math.radians(thdeg)
    b = b_of_theta(th, D_TEST)
    hsteps = 1e-7
    dbdth = (b_of_theta(th + hsteps, D_TEST) - b_of_theta(th - hsteps, D_TEST)) / (2 * hsteps)
    jac = (b / math.sin(th)) * abs(dbdth)
    cf = dsdo(th, D_TEST)
    p("dsdo(%g deg, D=3) closed form" % thdeg, cf)
    p("Jacobian from b(theta)", jac, 1)
    p("rel. difference", abs(cf - jac) / cf, 1)

# the 1/sin^4 law itself: ratios at fixed D
p("dsdo(5 deg)/dsdo(90 deg)", dsdo(math.radians(5), D_TEST) / dsdo(math.radians(90), D_TEST))
p("sin^4(45)/sin^4(2.5) (the same number)",
  math.sin(math.radians(45)) ** 4 / math.sin(math.radians(2.5)) ** 4)

# integrated cross section beyond theta: sigma(>theta) = pi b(theta)^2
head("4b. sigma(> theta) = pi b(theta)^2, by quadrature and in closed form")
for thdeg in (10.0, 90.0, 150.0):
    th = math.radians(thdeg)
    val, _ = quad(lambda t: dsdo(t, D_TEST) * 2 * math.pi * math.sin(t), th, math.pi,
                  limit=400, epsabs=1e-13, epsrel=1e-12)
    p("sigma(>%g deg) quadrature" % thdeg, val)
    p("pi b^2 closed form", math.pi * b_of_theta(th, D_TEST) ** 2, 1)
    p("rel. difference", abs(val - math.pi * b_of_theta(th, D_TEST) ** 2) / val, 1)


# =====================================================================
# 5. sampling -- a seeded beam must reproduce the cross section
# =====================================================================
head("5. mulberry32 and the sampled scattering-angle distribution")


def _u32(x):
    return x & 0xFFFFFFFF


def _i32(x):
    x &= 0xFFFFFFFF
    return x - 0x100000000 if x & 0x80000000 else x


def _imul(a, b):
    return _i32(_u32(_i32(a)) * _u32(_i32(b)))


def mulberry32(seed):
    state = [_i32(seed)]

    def nxt():
        state[0] = _i32(state[0] + 0x6D2B79F5)
        a = state[0]
        t = _imul(a ^ (_u32(a) >> 15), 1 | a)
        t = _i32(t + _imul(t ^ (_u32(t) >> 7), 61 | t)) ^ t
        return _u32(t ^ (_u32(t) >> 14)) / 4294967296.0

    return nxt


rng = mulberry32(12345)
first = [rng() for _ in range(6)]
for i, v in enumerate(first):
    p("mulberry32(12345) draw %d" % i, v)
rng = mulberry32(1)
s = 0.0
NDRAW = 100000
for _ in range(NDRAW):
    s += rng()
p("mulberry32(1) mean of 100000 draws", s / NDRAW)

# a beam uniform on a disc of radius bmax: b = bmax sqrt(u)
NS = 200000
BMAX = 30.0
rng = mulberry32(20260922)
bs = np.empty(NS)
for i in range(NS):
    bs[i] = BMAX * math.sqrt(rng())
ths = 2.0 * np.arctan(D_TEST / (2.0 * bs))
p("sample size", NS)
p("bmax", BMAX)
p("D", D_TEST)
p("mean impact parameter (-> 2 bmax/3)", float(bs.mean()))
p("2 bmax / 3", 2 * BMAX / 3)
# the smallest angle this beam can produce is the one at b = bmax
p("smallest angle in the beam, deg", math.degrees(theta_of_b(BMAX, D_TEST)))
for thdeg in (6.0, 8.0, 12.0, 20.0, 45.0, 90.0):
    th = math.radians(thdeg)
    frac = float(np.mean(ths > th))
    exact = (b_of_theta(th, D_TEST) / BMAX) ** 2
    sig = math.sqrt(exact * (1 - exact) / NS)
    p("fraction scattered beyond %g deg (sample)" % thdeg, frac)
    p("closed form (b(theta)/bmax)^2", exact, 1)
    p("binomial sigma", sig, 1)
    p("z = (sample - exact)/sigma", (frac - exact) / sig, 1)
# and the shape: bin in theta, divide by the solid angle, compare with 1/sin^4
edges = np.radians(np.array([6.0, 8.0, 13.0, 21.0, 34.0, 55.0, 89.0, 144.0]))
cnt, _ = np.histogram(ths, bins=edges)
for i in range(len(edges) - 1):
    lo, hi = edges[i], edges[i + 1]
    dom = 2 * math.pi * (math.cos(lo) - math.cos(hi))
    dens = cnt[i] / (NS * dom) * (math.pi * BMAX * BMAX)
    mid = 0.5 * (lo + hi)
    # the exact bin average of dsdo over the bin's solid angle
    ex = (math.pi * b_of_theta(lo, D_TEST) ** 2 - math.pi * b_of_theta(hi, D_TEST) ** 2) / dom
    p("bin %g-%g deg: sampled dsdo" % (math.degrees(lo), math.degrees(hi)), float(dens))
    p("exact bin average", ex, 1)
    p("ratio", float(dens) / ex, 1)
    p("count", int(cnt[i]), 1)
    p("Poisson relative sigma 1/sqrt(count)", 1.0 / math.sqrt(max(1, int(cnt[i]))), 1)

# the gun in the live views fires along a LINE, not over a disc, so its angle
# distribution is the 2-D one: the fraction beyond theta is b(theta)/X.
head("5b. a line beam (what the gun actually does) is the 2-D distribution")
XLINE = 30.0
rng = mulberry32(7)
NL = 200000
cnt2 = {}
angs = np.empty(NL)
for i in range(NL):
    x = XLINE * (2.0 * rng() - 1.0)
    angs[i] = theta_of_b(abs(x), D_TEST) if x != 0 else math.pi
for thdeg in (8.0, 20.0, 45.0, 90.0):
    th = math.radians(thdeg)
    frac = float(np.mean(angs > th))
    exact = b_of_theta(th, D_TEST) / XLINE
    sig = math.sqrt(exact * (1 - exact) / NL)
    p("line beam: fraction beyond %g deg (sample)" % thdeg, frac)
    p("closed form b(theta)/X", exact, 1)
    p("binomial sigma", sig, 1)
    p("z", (frac - exact) / sig, 1)
_ = cnt2


# =====================================================================
# 6. the plum pudding -- Thomson's atom, and how small its deflections are
# =====================================================================
head("6. the Thomson atom (uniform positive ball radius R, neutral outside)")
# U(r)/E = D (R^2 - r^2) / (2 R^3)  for r <= R,  0 outside.
# Impulse (straight line):  theta = D b sqrt(R^2 - b^2) / R^3.


def thomson_theta_impulse(b, D, R):
    if b >= R:
        return 0.0
    return D * b * math.sqrt(R * R - b * b) / (R ** 3)


def thomson_U_over_E(r, D, R):
    if r >= R:
        return 0.0
    return D * (R * R - r * r) / (2.0 * R ** 3)


def thomson_theta_exact(b, D, R):
    """the deflection integral for the Thomson potential, done properly"""
    if b >= R:
        return 0.0

    def g(r):
        return 1.0 - thomson_U_over_E(r, D, R) - b * b / (r * r)

    rm = brentq(g, b * (1 + 1e-14), R, xtol=1e-18, rtol=8.9e-16)

    def f(s):
        u = 1.0 - s * s
        r = rm / u if u > 0 else float("inf")
        rad = 1.0 - thomson_U_over_E(r, D, R) - (b * b) * u * u / (rm * rm)
        if rad <= 0:
            return 0.0
        return 2.0 * s / math.sqrt(rad)

    val, _ = quad(f, 0.0, 1.0, limit=400, epsabs=1e-15, epsrel=1e-14)
    return math.pi - 2.0 * (b / rm) * val


D_T, R_T = 1.0, 500.0                  # a wide, weak ball: D/R = 1/500
# the impulse approximation's relative error is O(theta): halving D must halve
# it.  Measured, not assumed.
for dd in (1.0, 0.5, 0.25):
    b = 0.3 * R_T
    ti = thomson_theta_impulse(b, dd, R_T)
    te = thomson_theta_exact(b, dd, R_T)
    p("impulse error at b=0.3R, D=%g (relative)" % dd, abs(ti - te) / te)
    p("theta itself", te, 1)
for frac in (0.1, 0.3, 1 / math.sqrt(2), 0.9, 0.99):
    b = frac * R_T
    ti = thomson_theta_impulse(b, D_T, R_T)
    te = thomson_theta_exact(b, D_T, R_T)
    p("Thomson theta(b=%.4f R) impulse, rad" % frac, ti)
    p("exact deflection integral", te, 1)
    p("rel. difference", abs(ti - te) / ti, 1)
p("Thomson theta_max = D/(2R) (D=1, R=500)", D_T / (2 * R_T))
p("impulse at b = R/sqrt(2)", thomson_theta_impulse(R_T / math.sqrt(2), D_T, R_T))
fr = minimize_scalar(lambda b: -thomson_theta_impulse(b, D_T, R_T),
                     bounds=(1e-6, R_T * (1 - 1e-9)), method="bounded",
                     options={"xatol": 1e-12})
p("argmax b/R (-> 1/sqrt 2)", float(fr.x) / R_T)
p("1/sqrt(2)", 1 / math.sqrt(2))
# <theta^2> over a disc of radius R
val, _ = quad(lambda b: thomson_theta_impulse(b, D_T, R_T) ** 2 * 2 * b / (R_T * R_T),
              0.0, R_T, limit=400, epsabs=1e-16, epsrel=1e-14)
p("<theta^2> over the disc, quadrature", val)
p("closed form D^2/(6 R^2)", D_T ** 2 / (6 * R_T ** 2))
p("rel. difference", abs(val - D_T ** 2 / (6 * R_T ** 2)) / val)
# the multiple-scattering integral: <theta^2>_total = n t pi D^2 / 6
val2, _ = quad(lambda b: thomson_theta_impulse(b, D_T, R_T) ** 2 * 2 * math.pi * b,
               0.0, R_T, limit=400, epsabs=1e-16, epsrel=1e-14)
p("int theta^2 2 pi b db, quadrature", val2)
p("closed form pi D^2 / 6", math.pi * D_T ** 2 / 6)
p("rel. difference", abs(val2 - math.pi * D_T ** 2 / 6) / val2)


# =====================================================================
# 7. gold, for real
# =====================================================================
head("7. alpha on gold -- the real numbers")
Z_AU, A_AU = 79, 197
RHO_AU = 19300.0                       # kg/m^3, the density this file uses
M_AU = 196.966570e-3                   # kg/mol, molar mass of gold-197
E77 = 7.7 * MEV                        # RaC' alphas, the 1913 beam
D77 = D_of(2, Z_AU, E77)
p("Z gold", Z_AU)
p("A gold", A_AU)
p("neutrons in gold-197", A_AU - Z_AU)
p("alpha energy (MeV)", E77 / MEV)
p("D = k Z1 Z2 e^2 / E (m)", D77)
p("D (fm)", D77 / FM)
p("a = D/2 (fm)", D77 / 2 / FM)
p("k e^2 Z1 Z2 / E in MeV fm / MeV (cross-check, fm)", KE2_MEVFM * 2 * Z_AU / 7.7)
p("b at 90 deg (fm)", b_of_theta(math.pi / 2, D77) / FM)
p("b at 1 deg (fm)", b_of_theta(math.radians(1), D77) / FM)
p("rmin head-on (fm)", rmin_of_b(0.0, D77) / FM)
p("rmin at b = a (fm)", rmin_of_b(D77 / 2, D77) / FM)
R_AU_NUC = 1.2 * FM * A_AU ** (1.0 / 3.0)
R_ALPHA = 1.2 * FM * 4.0 ** (1.0 / 3.0)
p("nuclear radius 1.2 A^(1/3) fm, gold (fm)", R_AU_NUC / FM)
p("nuclear radius, alpha (fm)", R_ALPHA / FM)
p("touching separation R_Au + R_alpha (fm)", (R_AU_NUC + R_ALPHA) / FM)
E_TOUCH = KE * 2 * Z_AU * E_Q * E_Q / (R_AU_NUC + R_ALPHA)
p("energy at which a head-on alpha touches gold (MeV)", E_TOUCH / MEV)
p("ratio D(7.7 MeV) / touching separation", D77 / (R_AU_NUC + R_ALPHA))
n_AU = RHO_AU * N_A / M_AU
p("gold number density (1/m^3)", n_AU)
p("gold atomic spacing n^(-1/3) (m)", n_AU ** (-1.0 / 3.0))
R_ATOM = 1.44e-10                      # metallic radius of gold, the sim's R
p("gold atomic radius used for the Thomson ball (m)", R_ATOM)
p("atom / nucleus diameter ratio", R_ATOM / R_AU_NUC)
p("dsdo at 90 deg (m^2/sr)", dsdo(math.pi / 2, D77))
p("dsdo at 90 deg (barn/sr)", dsdo(math.pi / 2, D77) / BARN)
p("dsdo at 10 deg (barn/sr)", dsdo(math.radians(10), D77) / BARN)
p("dsdo at 170 deg (barn/sr)", dsdo(math.radians(170), D77) / BARN)

head("7b. a 400 nm gold leaf")
T_FOIL = 400e-9
p("foil thickness (m)", T_FOIL)
p("atoms deep (t / n^(-1/3))", T_FOIL * n_AU ** (1.0 / 3.0))
p("n t (1/m^2)", n_AU * T_FOIL)
for thdeg in (1.0, 10.0, 90.0, 150.0):
    th = math.radians(thdeg)
    f = n_AU * T_FOIL * math.pi * b_of_theta(th, D77) ** 2
    p("Rutherford fraction beyond %g deg" % thdeg, f)
    p("one in", 1.0 / f, 1)
# Thomson, same foil
TH_MAX = D77 / (2 * R_ATOM)
p("Thomson theta_max, single atom (rad)", TH_MAX)
p("Thomson theta_max, single atom (deg)", math.degrees(TH_MAX))
p("Thomson theta_rms, single atom (rad)", D77 / (R_ATOM * math.sqrt(6)))
TH2 = math.pi * n_AU * T_FOIL * D77 ** 2 / 6.0
p("Thomson <theta^2> through the foil (rad^2)", TH2)
p("Thomson theta_rms through the foil (rad)", math.sqrt(TH2))
p("Thomson theta_rms through the foil (deg)", math.degrees(math.sqrt(TH2)))
p("Rutherford theta_rms would be (deg) -- undefined, the integral diverges", float("inf"))
lp = -(math.pi / 2) ** 2 / TH2 / math.log(10)
p("log10 P(theta > 90 deg) under Thomson multiple scattering", lp)
p("log10 of the Rutherford fraction beyond 90 deg",
  math.log10(n_AU * T_FOIL * math.pi * b_of_theta(math.pi / 2, D77) ** 2))
p("ratio of exponents (how many decades apart)",
  lp - math.log10(n_AU * T_FOIL * math.pi * b_of_theta(math.pi / 2, D77) ** 2))


# =====================================================================
# 8. PhET's scaled model, reproduced
# =====================================================================
head("8. PhET's scaled model (rutherford-scattering 1.1.29)")
# read out of the minified build:
#   RSConstants: MIN/MAX/DEFAULT_ALPHA_ENERGY 50/100/80,
#   MIN/MAX/DEFAULT_PROTON_COUNT 20/100/79, MIN/MAX/DEFAULT_NEUTRON_COUNT
#   20/150/118, SPACE_NODE_WIDTH/HEIGHT 510, DEFAULT_SHOW_TRACES false.
#   RSBaseModel: bounds = +-SPACE_NODE_WIDTH/4 = +-127.5.
#   RutherfordAtomSpace: five atoms of atomWidth 30.
#   RutherfordNucleusSpace: one atom of boundingRect width = bounds.width.
#   RutherfordAtom.moveParticle: D = (L/8)(p/79)(80^2/s0^2).
#   Gun.step: dtPerGunFired = bounds.width / energy / 20.
PHET_W = 255.0
PHET_DEF_E = 80.0
PHET_DEF_P = 79


def phet_D(L, protons, s0):
    return (L / 8.0) * (protons / float(PHET_DEF_P)) * (PHET_DEF_E ** 2 / (s0 * s0))


p("PhET model bounds width", PHET_W)
p("PhET atom width, atomic scene", 30.0)
p("PhET atom width, nuclear scene", PHET_W)
p("PhET D, nuclear scene, defaults", phet_D(PHET_W, 79, 80.0))
p("PhET D, atomic scene, defaults", phet_D(30.0, 79, 80.0))
p("PhET D / L (both scenes)", phet_D(PHET_W, 79, 80.0) / PHET_W)
p("PhET D, nuclear, 100 protons, energy 50", phet_D(PHET_W, 100, 50.0))
p("PhET D, nuclear, 20 protons, energy 100", phet_D(PHET_W, 20, 100.0))
p("PhET gun period at energy 80 (s)", PHET_W / 80.0 / 20.0)
p("PhET gun period at energy 50 (s)", PHET_W / 50.0 / 20.0)
p("PhET crossing time at energy 80 (s)", PHET_W / 80.0)
p("PhET particles in flight at energy 80", (PHET_W / 80.0) / (PHET_W / 80.0 / 20.0))
# PhET nudges the fired x away from an atom: LinearFunction(20, 255, 2, 10)
for w in (30.0, PHET_W):
    corr = 2.0 + (w - 20.0) / (PHET_W - 20.0) * (10.0 - 2.0)
    p("PhET gun nudge for atom width %g" % w, corr)
p("PhET gun nudge window (0.04 * bounds width)", 0.04 * PHET_W)
# the biggest deflection PhET's nuclear scene can show
BMIN_NUC = 10.0
p("smallest |x| the nuclear gun can produce", BMIN_NUC)
p("theta at that b, defaults (deg)",
  math.degrees(theta_of_b(BMIN_NUC, phet_D(PHET_W, 79, 80.0))))
p("theta at that b, 100 protons energy 50 (deg)",
  math.degrees(theta_of_b(BMIN_NUC, phet_D(PHET_W, 100, 50.0))))
p("PhET atomic-scale caption (m)", 6.0e-10)
p("PhET nuclear-scale caption (m)", 1.5e-13)
p("PhET caption scale ratio", 6.0e-10 / 1.5e-13)
p("PhET geometric zoom ratio (atom box 30 -> 255)", PHET_W / 30.0)
p("true gold atom / nucleus diameter ratio", R_ATOM / R_AU_NUC)

head("8b. PhET's stepper against the conic")
# The sim advances phi with dphi/dt = v_inf b / r^2 (angular momentum).  PhET
# advances it with the arc-length form dphi/dt = b^2 s / (r sqrt(b^4 + r^2 t^2)),
# t = b cos phi - (D/2) sin phi, s = v_inf sqrt(1 - D/r).  They are the same
# number on the orbit -- worth pinning, because it ties the speed law to the
# geometry.
Dn = phet_D(PHET_W, 79, 80.0)
for b in (10.0, 40.0, 120.0):
    for phi in (0.05, 0.4, 1.0):
        r = rofphi(phi, b, Dn)
        if not (r > 0):
            continue
        sspeed = math.sqrt(1.0 - Dn / r)
        t3 = b * math.cos(phi) - 0.5 * Dn * math.sin(phi)
        arc = b * b * sspeed / (r * math.sqrt(b ** 4 + r * r * t3 * t3))
        angmom = b / (r * r)
        p("dphi/dt at b=%g phi=%g: arc-length form" % (b, phi), arc)
        p("angular-momentum form", angmom, 1)
        p("rel. difference", abs(arc - angmom) / angmom, 1)

# RK4 in phi against the exact time: t(phi) = int_0^phi r^2 dphi / (v b)
head("8c. RK4 in phi reaches the same angle as the exact quadrature")


def time_between(phi0, phi1, b, D):
    """the elapsed time along the orbit between two polar angles: dt = r^2
    dphi / (v_inf b).  The integral from phi = 0 DIVERGES (r ~ b/phi there, so
    the integrand goes as 1/phi^2) -- a first version integrated from 1e-12 and
    the 'RK4 error' it reported was entirely that."""
    val, _ = quad(lambda f: rofphi(f, b, D) ** 2 / b, phi0, phi1,
                  limit=400, epsabs=1e-14, epsrel=1e-13)
    return val


def rk4_phi(phi0, b, D, T, nsteps):
    def f(ph):
        r = rofphi(ph, b, D)
        return b / (r * r)
    ph = phi0
    hh = T / nsteps
    for _ in range(nsteps):
        k1 = f(ph)
        k2 = f(ph + 0.5 * hh * k1)
        k3 = f(ph + 0.5 * hh * k2)
        k4 = f(ph + hh * k3)
        ph += hh * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
    return ph


for b in (10.0, 60.0):
    phi0, phi1 = 0.05, 0.9
    T = time_between(phi0, phi1, b, Dn)
    p("elapsed time from phi=0.05 to 0.9, b=%g" % b, T)
    for n in (15, 60, 240):
        got = rk4_phi(phi0, b, Dn, T, n)
        p("RK4 phi after T, %d steps" % n, got, 1)
        p("abs error vs target 0.9", abs(got - phi1), 1)


# =====================================================================
# 9. numbers the drawing needs
# =====================================================================
head("9. drawing")
# nucleon packing: PhET draws the nucleons in rings.  This file packs them on a
# sunflower (Vogel) spiral, which is deterministic and needs no table.
GOLDEN = math.pi * (3.0 - math.sqrt(5.0))
p("golden angle (rad)", GOLDEN)
p("sunflower radius for 197 nucleons, unit spacing", math.sqrt(197.0))
p("nucleon count at gold defaults", 79 + 118)

print("")
print("===== done =====")
