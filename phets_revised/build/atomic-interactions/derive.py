#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""derive.py — the Python twin of atomic-interactions.html.

Re-derives every closed form the sim implements and prints reference values to
12+ digits for selfTest() to assert against (refvals.txt).  Nothing here is
copied from the JS; where the two must agree they are written independently and
the numbers are the contract.

WHAT IS CHECKED HERE
  * V(r) = 4 eps [ (sig/r)^12 - (sig/r)^6 ], its zero at sig and its minimum
    -eps at r = 2^(1/6) sig.
  * F(r) = -dV/dr, THREE ways: the closed form; a 60-digit Decimal central
    difference with Richardson extrapolation (the definition of a derivative);
    and scipy.differentiate.derivative.  Same for V''(r).
  * V''(r_min) = 72 eps / (2^(1/3) sig^2) and omega = sqrt(V''(r_min)/mu).
  * the exact turning points of a bound orbit (a quadratic in u = (sig/r)^6).
  * the period of a bound orbit by regularised Gauss-Legendre quadrature, by
    velocity-Verlet integration, and (small amplitude) by 2 pi / omega.
  * the measured order of three integrators: velocity Verlet (2), symplectic
    (semi-implicit) Euler (1, PhET's), forward Euler (divergent).
  * PhET's own parameter tables, transcribed from the minified original, and
    the literature values beside them.

UNITS.  Lengths pm, times ps, masses u.  Then speed is pm/ps = m/s exactly and
energy is u (pm/ps)^2 = u m^2/s^2; K_TO_E = k_B/m_u converts an epsilon quoted
as eps/k_B in kelvin into that energy unit.

Run:  python3 derive.py            (writes refvals.txt beside this file)
"""
import io
import math
import os
from decimal import Decimal, getcontext

import numpy as np
import scipy.constants as sc
from scipy.differentiate import derivative as sp_derivative
from scipy.optimize import brentq
from scipy.integrate import quad

OUT = []


def say(s=""):
    OUT.append(s)
    print(s)


def val(name, x, nd=12):
    say("%-46s %s" % (name, ("%." + str(nd) + "g") % x))


# ----------------------------------------------------------------- constants
K_B = sc.value("Boltzmann constant")               # J/K
M_U = sc.value("atomic mass constant")             # kg
EV = sc.value("elementary charge")                 # J per eV
K_TO_E = K_B / M_U          # (pm/ps)^2 per kelvin, i.e. m^2 s^-2 K^-1
E_TO_MEV = M_U / EV * 1e3   # meV per u (pm/ps)^2
E_TO_ZJ = M_U * 1e21        # zJ  per u (pm/ps)^2
F_TO_PN = M_U / 1e-12 * 1e12  # pN per u (pm/ps)^2 / pm

# ------------------------------------------------- PhET's values (originals)
# docs/phets/atomic-interactions_en.html, build 1.2.21.  Read out of the
# minified source; each is PhET's value, not a literature value.
#   nitroglycerin Element table:  Ne(69,154,-,20.1797)  Ar(97,188,-,39.948)
#                                 O(73,152,3.44,15.9994)
#   SOMConstants: MIN_SIGMA 75, MAX_SIGMA 500, MIN_EPSILON 20, MAX_EPSILON 450,
#                 ADJUSTABLE_ATTRACTION_DEFAULT_RADIUS 175, K_BOLTZMANN 138e-25,
#                 EPSILON_FOR_DIATOMIC_OXYGEN 113, SIGMA_FOR_DIATOMIC_OXYGEN 365,
#                 NEON_TRIPLE_POINT_IN_KELVIN 24.5, NEON_CRITICAL_POINT_IN_KELVIN 45,
#                 ARGON_TRIPLE_POINT_IN_KELVIN 75, ARGON_CRITICAL_POINT_IN_KELVIN 151,
#                 O2_TRIPLE_POINT_IN_KELVIN 54,  O2_CRITICAL_POINT_IN_KELVIN 155
#   InteractionStrengthTable.getInteractionPotential  (epsilon/k_B in K)
#   SigmaTable.getSigma                               (sigma in pm)
PHET_R = {"Ne": 154.0, "Ar": 188.0, "O": 152.0, "X": 175.0}       # pm, vdW radii
PHET_M = {"Ne": 20.1797, "Ar": 39.948, "O": 15.9994, "X": 25.0}   # u
PHET_MIN_SIGMA, PHET_MAX_SIGMA = 75.0, 500.0
PHET_MIN_EPSILON, PHET_MAX_EPSILON = 20.0, 450.0
PHET_ADJ_SIGMA, PHET_ADJ_EPSILON = 2 * PHET_R["X"], 100.0
PHET_CRIT = {"Ne": 45.0, "Ar": 151.0, "O": 155.0}      # K, critical points
PHET_TRIPLE = {"Ne": 24.5, "Ar": 75.0, "O": 54.0}      # K, triple points

PAIRS = [  # key, label, atom a, atom b, PhET sigma (pm), PhET eps/k_B (K)
    ("NeNe", "neon-neon", "Ne", "Ne", 308.0, 35.8),
    ("ArAr", "argon-argon", "Ar", "Ar", 376.0, 111.84),
    ("OO", "oxygen-oxygen", "O", "O", 200.0, 1000.0),
    ("NeAr", "neon-argon", "Ne", "Ar", 343.0, 59.5),
    ("NeO", "neon-oxygen", "Ne", "O", PHET_R["Ne"] + PHET_R["O"], 51.0),
    ("ArO", "argon-oxygen", "Ar", "O", PHET_R["Ar"] + PHET_R["O"], 85.0),
    ("Adj", "adjustable", "X", "X", PHET_ADJ_SIGMA, PHET_ADJ_EPSILON),
]

# ------------------------------------------------------ literature values
# Ne and Ar: Attard, arXiv:1702.00096 Table I ("Lennard-Jones Parameters",
#   attributed there to van Sciver, Helium Cryogenics, 2nd ed., Springer 2012):
#      He 0.2556 nm / 0.2869 nm / 10.22 K,  Ne 0.2789 / 0.3131 / 35.7,
#      Ar 0.3418 / 0.3837 / 124.0.   (sigma, r_min, eps/k_B)
# Ar and O2: Bird, Stewart & Lightfoot, Transport Phenomena 2nd ed. (2007)
#   pp. 864-865, the table reproduced at
#   en.wikipedia.org/wiki/Temperature_dependence_of_viscosity:
#      Ar 3.432 A / 122.4 K,  O2 3.433 A / 113 K,  N2 3.667 / 99.8,
#      CO2 3.996 / 190,  CH4 3.780 / 154,  He 2.576 / 10.2,  H2 2.915 / 38.0,
#      dry air 3.617 / 97.0.
# Argon therefore has two retrieved sets, 1.3% apart in eps and 0.4% in sigma;
# that spread is the honest uncertainty on an LJ fit.  Neon has one.
LIT = {  # atom: (sigma pm, eps/k_B K, printed r_min pm or None, source tag)
    "Ne": (278.9, 35.7, 313.1, "vanSciver"),
    "Ar": (341.8, 124.0, 383.7, "vanSciver"),
    "O": (343.3, 113.0, None, "BSL"),
}
LIT_ALT = {"Ar": (343.2, 122.4, None, "BSL")}
LIT_TABLE_RMIN = [("He", 255.6, 286.9), ("Ne", 278.9, 313.1), ("Ar", 341.8, 383.7)]


# --------------------------------------------------------------- the potential
def V(r, sig, eps):
    """LJ 12-6 potential.  eps in the same energy unit as the result."""
    x = sig / r
    return 4.0 * eps * (x ** 12 - x ** 6)


def F(r, sig, eps):
    """-dV/dr, closed form."""
    x = sig / r
    return 24.0 * eps / r * (2.0 * x ** 12 - x ** 6)


def Vpp(r, sig, eps):
    """d2V/dr2, closed form."""
    x = sig / r
    return 24.0 * eps / (r * r) * (26.0 * x ** 12 - 7.0 * x ** 6)


def r_min(sig):
    return sig * 2.0 ** (1.0 / 6.0)


def k_spring(sig, eps):
    """V''(r_min) in closed form: 72 eps / (2^(1/3) sig^2)."""
    return 72.0 * eps / (2.0 ** (1.0 / 3.0) * sig * sig)


# ------------------------------------- derivative checks (independent routes)
def dec_derivs(r, sig, eps, order=1, nd=60):
    """Central difference + Richardson at `nd` significant decimal digits.

    Uses the DEFINITION of the derivative, so it shares no algebra with F/Vpp.
    Two step sizes a factor 2 apart, Richardson-extrapolated (error O(h^4)).
    """
    getcontext().prec = nd
    R, S, E = Decimal(repr(r)), Decimal(repr(sig)), Decimal(repr(eps))

    def v(x):
        q = S / x
        return 4 * E * (q ** 12 - q ** 6)

    def d1(h):
        return (v(R + h) - v(R - h)) / (2 * h)

    def d2(h):
        return (v(R + h) - 2 * v(R) + v(R - h)) / (h * h)

    h = Decimal(r) / Decimal(10 ** 12)
    f = d1 if order == 1 else d2
    a, b = f(h), f(h / 2)
    return float((4 * b - a) / 3)          # Richardson: O(h^2) term removed


def dec_derivs_n(r, sig, eps, n, nd=90):
    """n-th derivative of V by the central stencil sum_k (-1)^k C(n,k)
    f(x + (n/2 - k)h) / h^n, Richardson-extrapolated over two step sizes.
    Pure arithmetic on the definition; shares nothing with the closed forms."""
    getcontext().prec = nd
    R, S, E = Decimal(repr(r)), Decimal(repr(sig)), Decimal(repr(eps))
    c = [1]
    for i in range(n):
        c = [1] + [c[j] + c[j + 1] for j in range(len(c) - 1)] + [1]

    def v(x):
        q = S / x
        return 4 * E * (q ** 12 - q ** 6)

    def d(h):
        tot = Decimal(0)
        for k in range(n + 1):
            off = (Decimal(n) / 2 - k) * h
            tot += (-1) ** k * c[k] * v(R + off)
        return tot / (h ** n)

    h = R / Decimal(10 ** 8)
    a, b = d(h), d(h / 2)
    return float((4 * b - a) / 3)


def scipy_derivs(r, sig, eps, order=1):
    if order == 1:
        res = sp_derivative(lambda x: V(x, sig, eps), r, initial_step=r * 1e-3,
                            tolerances=dict(rtol=1e-13))
        return float(res.df)
    res = sp_derivative(lambda x: -F(x, sig, eps), r, initial_step=r * 1e-3,
                        tolerances=dict(rtol=1e-13))
    return float(res.df)


# --------------------------------------------------------- bound-orbit tools
def turning_points(E, sig, eps):
    """Exact roots of V(r) = E for -eps < E < 0.

    4 eps (u^2 - u) = E with u = (sig/r)^6  ->  u = (1 +- sqrt(1 + E/eps))/2,
    and r = sig u^(-1/6).  The + root is the inner turning point.
    """
    d = 1.0 + E / eps
    if d < 0:
        return None
    s = math.sqrt(d)
    u_in, u_out = 0.5 * (1.0 + s), 0.5 * (1.0 - s)
    r_in = sig * u_in ** (-1.0 / 6.0)
    r_out = float("inf") if u_out <= 0 else sig * u_out ** (-1.0 / 6.0)
    return r_in, r_out


def _pow_sum(x, y):
    """sum_{k=0..5} x^k y^(5-k)  =  (x^6 - y^6)/(x - y), without the division."""
    return (y ** 5 + x * y ** 4 + x * x * y ** 3 + x ** 3 * y * y
            + x ** 4 * y + x ** 5)


def period_quad(E, sig, eps, mu, n=200):
    """T = 2 int dr/v over the bound orbit, with the singularities removed in
    CLOSED FORM rather than merely softened.

    With u = (sig/r)^6 the turning points are the roots of u^2 - u = E/(4 eps),
    so u_in + u_out = 1 and

        E - V(r) = 4 eps (u_in - u)(u - u_out).

    Substituting r = a - b cos(th) (a, b the half sum and half difference of the
    turning points) gives r - r_in = 2b sin^2(th/2) and r_out - r = 2b cos^2(th/2),
    and factoring x^6 - y^6 = (x - y) sum x^k y^(5-k) turns the product into

        E - V = 4 eps sig^12 b^2 sin^2(th) S_in S_out / (r^12 r_in^6 r_out^6),

    so v carries an exact factor sin(th) that cancels the dr = b sin(th) dth of
    the numerator.  The integrand is then analytic AND free of the
    catastrophic cancellation in `E - V(r)` that ruins the naive form at small
    amplitude (where E and V agree to fifteen digits over most of the orbit).
    """
    r1, r2 = turning_points(E, sig, eps)
    if not math.isfinite(r2):
        return float("inf")
    a, b = 0.5 * (r1 + r2), 0.5 * (r2 - r1)
    x, w = np.polynomial.legendre.leggauss(n)
    th = 0.5 * math.pi * (x + 1.0)
    ww = 0.5 * math.pi * w
    r = a - b * np.cos(th)
    S_in, S_out = _pow_sum(r, r1), _pow_sum(r2, r)
    integ = (r ** 6 * r1 ** 3 * r2 ** 3 / sig ** 6) * np.sqrt(
        mu / (8.0 * eps * S_in * S_out))
    return 2.0 * float(np.sum(ww * integ))


def period_quad_naive(E, sig, eps, mu, n=200):
    """The same substitution with E - V(r) evaluated directly — kept only so
    the suite can assert that it IS worse, and where."""
    r1, r2 = turning_points(E, sig, eps)
    a, b = 0.5 * (r1 + r2), 0.5 * (r2 - r1)
    x, w = np.polynomial.legendre.leggauss(n)
    th = 0.5 * math.pi * (x + 1.0)
    ww = 0.5 * math.pi * w
    r = a - b * np.cos(th)
    ke = np.maximum(E - V(r, sig, eps), 0.0)
    v = np.sqrt(2.0 * ke / mu)
    integ = np.where(v > 0, b * np.sin(th) / np.maximum(v, 1e-300), 0.0)
    return 2.0 * float(np.sum(ww * integ))


def verlet(r0, v0, sig, eps, mu, dt, nstep):
    """Velocity Verlet.  Returns (t, r, v, Emin, Emax) trace summary."""
    r, v = r0, v0
    a = F(r, sig, eps) / mu
    E0 = 0.5 * mu * v * v + V(r, sig, eps)
    emin = emax = E0
    rs = [r]
    for _ in range(nstep):
        v += 0.5 * a * dt
        r += v * dt
        a = F(r, sig, eps) / mu
        v += 0.5 * a * dt
        e = 0.5 * mu * v * v + V(r, sig, eps)
        emin = min(emin, e)
        emax = max(emax, e)
        rs.append(r)
    return np.array(rs), r, v, E0, emin, emax


def euler_sym(r0, v0, sig, eps, mu, dt, nstep):
    """PhET's step: a = F/m; v += a dt; r += v dt  (symplectic Euler)."""
    r, v = r0, v0
    E0 = 0.5 * mu * v * v + V(r, sig, eps)
    emin = emax = E0
    for _ in range(nstep):
        v += F(r, sig, eps) / mu * dt
        r += v * dt
        e = 0.5 * mu * v * v + V(r, sig, eps)
        emin, emax = min(emin, e), max(emax, e)
    return r, v, E0, emin, emax


def euler_fwd(r0, v0, sig, eps, mu, dt, nstep):
    """Forward Euler: both updates from the OLD state.  Not symplectic."""
    r, v = r0, v0
    E0 = 0.5 * mu * v * v + V(r, sig, eps)
    emin = emax = E0
    for _ in range(nstep):
        a = F(r, sig, eps) / mu
        r, v = r + v * dt, v + a * dt
        e = 0.5 * mu * v * v + V(r, sig, eps)
        emin, emax = min(emin, e), max(emax, e)
    return r, v, E0, emin, emax


def period_verlet(r0, sig, eps, mu, dt, nmax=600000):
    """Period from r(t) released at rest at r0: time between two successive
    maxima of r, refined by the 3-point parabola through the samples.

    A grid argmax staircases at first order in dt, so the parabola matters:
    without it this tracks the quadrature only to O(dt) (Known-bad list).
    """
    r, v = r0, 0.0
    a = F(r, sig, eps) / mu
    hits, prev2, prev1 = [], None, None
    for i in range(nmax):
        v += 0.5 * a * dt
        r += v * dt
        a = F(r, sig, eps) / mu
        v += 0.5 * a * dt
        if prev2 is not None and prev1 > prev2 and prev1 >= r:
            # parabola through (i-2, prev2), (i-1, prev1), (i, r)
            den = prev2 - 2.0 * prev1 + r
            d = 0.5 * (prev2 - r) / den if den != 0 else 0.0
            hits.append((i - 1 + d) * dt)
            if len(hits) >= 2:
                return hits[1] - hits[0]
        prev2, prev1 = prev1, r
    return float("nan")


# =====================================================================  main
say("=" * 74)
say("atomic-interactions — derive.py")
say("=" * 74)
say()
say("CODATA / scipy %s constants" % sc.__name__)
val("k_B (J/K)", K_B, 12)
val("m_u (kg)", M_U, 12)
val("e  (J)", EV, 12)
val("K_TO_E = k_B/m_u  ((pm/ps)^2 per K)", K_TO_E, 14)
val("E_TO_MEV = m_u/e*1e3 (meV per u(pm/ps)^2)", E_TO_MEV, 14)
val("E_TO_ZJ  = m_u*1e21 (zJ per u(pm/ps)^2)", E_TO_ZJ, 14)
val("F_TO_PN (pN per u(pm/ps)^2/pm)", F_TO_PN, 14)
say()

say("-" * 74)
say("1.  the potential and its landmarks")
say("-" * 74)
val("2^(1/6)", 2.0 ** (1.0 / 6.0), 15)
val("2^(1/3)", 2.0 ** (1.0 / 3.0), 15)
val("72 / 2^(1/3)", 72.0 / 2.0 ** (1.0 / 3.0), 15)
say()
sig0, eps0 = 308.0, 35.8 * K_TO_E          # neon-neon, PhET
val("neon sigma (pm)", sig0, 6)
val("neon eps (K)", 35.8, 6)
val("neon eps (u (pm/ps)^2)", eps0, 14)
val("neon eps (meV)", eps0 * E_TO_MEV, 14)
val("neon eps (zJ)", eps0 * E_TO_ZJ, 14)
val("neon r_min (pm)", r_min(sig0), 14)
val("V(sigma)  (must be 0)", V(sig0, sig0, eps0), 6)
val("V(r_min)/eps (must be -1)", V(r_min(sig0), sig0, eps0) / eps0, 15)
val("F(r_min)  (must be 0)", F(r_min(sig0), sig0, eps0), 6)
say()
say("V and F at fixed multiples of sigma (neon-neon, PhET's parameters)")
say("%-8s %-22s %-22s" % ("r/sigma", "V (u (pm/ps)^2)", "F (u (pm/ps)^2/pm)"))
VF_PINS = []
for f in (0.9, 0.95, 1.0, 1.122462048309373, 1.2, 1.5, 2.0, 3.0):
    r = f * sig0
    say("%-8.6g %-22.14g %-22.14g" % (f, V(r, sig0, eps0), F(r, sig0, eps0)))
    VF_PINS.append((f, V(r, sig0, eps0), F(r, sig0, eps0)))
say()

say("-" * 74)
say("2.  F = -dV/dr checked three ways (neon-neon)")
say("-" * 74)
say("the force is compared against the natural scale 24 eps/r rather than")
say("against |F| itself: F vanishes identically at r_min, where a relative")
say("difference is measuring floating-point cancellation and nothing else.")
say("%-9s %-21s %-21s %-12s %-12s" % ("r/sigma", "closed form", "60-digit Richardson",
                                      "/(24eps/r)", "scipy same"))
worst1 = 0.0
for f in (0.85, 0.95, 1.0, 1.122462048309373, 1.4, 2.0, 3.5):
    r = f * sig0
    a = F(r, sig0, eps0)
    b = -dec_derivs(r, sig0, eps0, 1)
    c = -scipy_derivs(r, sig0, eps0, 1)
    scale = 24.0 * eps0 / r
    d1, d2 = abs(a - b) / scale, abs(a - c) / scale
    worst1 = max(worst1, d1)
    say("%-9.6g %-21.14g %-21.14g %-12.3g %-12.3g" % (f, a, b, d1, d2))
val("worst |closed - Richardson| / (24 eps/r)", worst1, 3)
val("F(r_min) / (24 eps/r_min)  (must be ~0)",
    F(r_min(sig0), sig0, eps0) / (24.0 * eps0 / r_min(sig0)), 3)
say()
say("%-9s %-21s %-21s %-12s %-12s" % ("r/sigma", "V'' closed", "60-digit Richardson",
                                      "rel diff", "scipy rel"))
worst2 = 0.0
for f in (0.85, 0.95, 1.0, 1.122462048309373, 1.4, 2.0, 3.5):
    r = f * sig0
    a = Vpp(r, sig0, eps0)
    b = dec_derivs(r, sig0, eps0, 2)
    c = scipy_derivs(r, sig0, eps0, 2)
    scale = max(abs(a), abs(b), 1e-300)
    d1, d2 = abs(a - b) / scale, abs(a - c) / scale
    worst2 = max(worst2, d1)
    say("%-9.6g %-21.14g %-21.14g %-12.3g %-12.3g" % (f, a, b, d1, d2))
val("worst |V'' closed - Richardson| / |V''|", worst2, 3)
say()
val("V''(r_min) closed 72 eps/(2^(1/3) sig^2)", k_spring(sig0, eps0), 14)
val("V''(r_min) from Vpp()", Vpp(r_min(sig0), sig0, eps0), 14)
val("V''(r_min) 60-digit Richardson", dec_derivs(r_min(sig0), sig0, eps0, 2), 14)
say()

say("-" * 74)
say("3.  every pair: PhET's parameters, the well, and the oscillation")
say("-" * 74)
say("%-6s %-8s %-9s %-9s %-9s %-11s %-11s %-11s" %
    ("pair", "sig(pm)", "eps(K)", "r_min", "mu_mov", "k(u/ps^2)", "T_pin(ps)", "T_mov(ps)"))
PAIR_PINS = {}
for key, lab, a, b, sig, epsK in PAIRS:
    eps = epsK * K_TO_E
    ma, mb = PHET_M[a], PHET_M[b]
    mu_pin, mu_mov = mb, ma * mb / (ma + mb)
    k = k_spring(sig, eps)
    w_pin, w_mov = math.sqrt(k / mu_pin), math.sqrt(k / mu_mov)
    T_pin, T_mov = 2 * math.pi / w_pin, 2 * math.pi / w_mov
    say("%-6s %-8.6g %-9.6g %-9.6g %-9.6g %-11.6g %-11.6g %-11.6g" %
        (key, sig, epsK, r_min(sig), mu_mov, k, T_pin, T_mov))
    PAIR_PINS[key] = dict(sig=sig, epsK=epsK, eps=eps, mu_pin=mu_pin, mu_mov=mu_mov,
                          k=k, w_pin=w_pin, w_mov=w_mov, T_pin=T_pin, T_mov=T_mov)
say()
say("full precision, neon-neon and argon-argon:")
for key in ("NeNe", "ArAr"):
    p = PAIR_PINS[key]
    val("%s  eps (u (pm/ps)^2)" % key, p["eps"], 14)
    val("%s  r_min (pm)" % key, r_min(p["sig"]), 14)
    val("%s  k = V''(r_min) (u/ps^2)" % key, p["k"], 14)
    val("%s  omega pinned (rad/ps)" % key, p["w_pin"], 14)
    val("%s  T pinned (ps)" % key, p["T_pin"], 14)
    val("%s  omega moving (rad/ps)" % key, p["w_mov"], 14)
    val("%s  T moving (ps)" % key, p["T_mov"], 14)
    val("%s  omega SI pinned (rad/s)" % key, p["w_pin"] * 1e12, 14)
say()

say("-" * 74)
say("4.  turning points (exact) and the period by three routes")
say("-" * 74)
p = PAIR_PINS["NeNe"]
sig, eps, mu = p["sig"], p["eps"], p["mu_pin"]
say("neon-neon, left atom pinned, mu = m(Ne) = %.6g u" % mu)
say()
say("%-10s %-16s %-16s %-16s %-16s" % ("E/eps", "r_in (pm)", "r_out (pm)",
                                       "T_quad (ps)", "T_verlet (ps)"))
TP_PINS = []
for frac in (-0.999, -0.99, -0.9, -0.5, -0.2, -0.05, -0.01):
    E = frac * eps
    r1, r2 = turning_points(E, sig, eps)
    Tq = period_quad(E, sig, eps, mu)
    Tv = period_verlet(r2, sig, eps, mu, Tq / 20000.0)
    say("%-10.6g %-16.12g %-16.12g %-16.12g %-16.12g" % (frac, r1, r2, Tq, Tv))
    TP_PINS.append((frac, r1, r2, Tq, Tv))
say("  (verlet at 20000 steps per period, peaks parabola-refined; the two")
say("   routes share no algebra beyond V and F)")
say()
val("T at E -> -eps (2 pi/omega, ps)", p["T_pin"], 14)
say()
say("ANHARMONICITY.  Released at rest at r_min + A, the orbit runs between")
say("r_in and r_out; its harmonic amplitude is a = (r_out - r_in)/2, which is")
say("NOT A (the well is asymmetric, so the orbit's centre shifts outward).")
say("Landau & Lifshitz Mechanics 28 for V = mu omega0^2 x^2/2 + mu alpha x^3/3")
say("+ mu beta x^4/4 gives omega = omega0 + kappa a^2 with")
say("kappa = 3 beta/(8 omega0) - 5 alpha^2/(12 omega0^3).  Here the Taylor")
say("coefficients of the LJ well at its minimum are exactly")
say("   V2 =    72 eps / r_min^2")
say("   V3 = -1512 eps / r_min^3")
say("   V4 = 26712 eps / r_min^4")
say("so V4/V2 = 371/r_min^2 and (V3/V2)^2 = 441/r_min^2, and")
say("   kappa = omega0 (371/16 - 2205/48) / r_min^2 = -(91/4) omega0/r_min^2,")
say("   T(a) = T0 (1 + (91/4) a^2/r_min^2) + O(a^4).")
say()
rm0 = r_min(sig)
for n, want in ((2, 72.0), (3, -1512.0), (4, 26712.0)):
    got = dec_derivs_n(rm0, sig, eps, n)
    val("V%d(r_min) r_min^%d/eps  (want %g)" % (n, n, want), got * rm0 ** n / eps, 12)
c_pred = p["T_pin"] * (91.0 / 4.0) / (rm0 * rm0)
val("predicted (T-T0)/a^2  (ps/pm^2)", c_pred, 14)
say()
say("%-9s %-14s %-13s %-15s %-15s %-9s" %
    ("A (pm)", "E/eps", "a (pm)", "T_quad (ps)", "(T-T0)/a^2", "/pred"))
AMP = []
for A in (0.03125, 0.0625, 0.125, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0):
    r0 = r_min(sig) + A
    E = V(r0, sig, eps)
    r1, r2 = turning_points(E, sig, eps)
    aa = 0.5 * (r2 - r1)
    Tq = period_quad(E, sig, eps, mu)
    c = (Tq - p["T_pin"]) / (aa * aa)
    say("%-9.6g %-14.10g %-13.10g %-15.12g %-15.10g %-9.6g" %
        (A, E / eps, aa, Tq, c, c / c_pred))
    AMP.append((A, aa, Tq, c))
say("  (the last column -> 1 as A -> 0: the O(a^2) law and its coefficient)")
say()
say("halving the amplitude quarters the period excess:")
say("%-9s %-17s %-10s" % ("A (pm)", "T - T0 (ps)", "ratio"))
prev = None
for A, aa, Tq, c in AMP:
    d = Tq - p["T_pin"]
    say("%-9.6g %-17.10g %-10s" % (A, d, "-" if prev is None else "%.6g" % (d / prev)))
    prev = d
say("  (-> 4 exactly as A -> 0; assert the RATE, not the destination)")
say()
say("the naive form of the same integral, for comparison — E - V(r) formed")
say("as a difference is useless below about a = 0.5 pm:")
say("%-9s %-17s %-17s %-11s" % ("A (pm)", "T regular (ps)", "T naive (ps)", "rel diff"))
for A in (0.002, 0.03125, 0.125, 0.5, 2.0, 8.0):
    E = V(r_min(sig) + A, sig, eps)
    a1 = period_quad(E, sig, eps, mu)
    a2 = period_quad_naive(E, sig, eps, mu)
    say("%-9.6g %-17.12g %-17.12g %-11.3g" % (A, a1, a2, abs(a2 - a1) / a1))
say()
say("quadrature convergence of the regular form (A = 1 pm):")
E1 = V(r_min(sig) + 1.0, sig, eps)
ref = period_quad(E1, sig, eps, mu, 400)
for n in (8, 16, 32, 64, 128, 200):
    say("   n = %-5d T = %-18.14g  |T - T(400)| = %.3g"
        % (n, period_quad(E1, sig, eps, mu, n),
           abs(period_quad(E1, sig, eps, mu, n) - ref)))
say()
A0 = 1.0
r0 = r_min(sig) + A0
E0 = V(r0, sig, eps)
val("A=1 pm: E (u (pm/ps)^2)", E0, 14)
val("A=1 pm: E/eps", E0 / eps, 14)
val("A=1 pm: r_in (pm)", turning_points(E0, sig, eps)[0], 14)
val("A=1 pm: r_out (pm)", turning_points(E0, sig, eps)[1], 14)
val("A=1 pm: T_quad (ps)", period_quad(E0, sig, eps, mu), 14)
val("A=1 pm: T small-osc (ps)", p["T_pin"], 14)
say()
A0 = 10.0
r0 = r_min(sig) + A0
E0 = V(r0, sig, eps)
val("A=10 pm: E/eps", E0 / eps, 14)
val("A=10 pm: r_in (pm)", turning_points(E0, sig, eps)[0], 14)
val("A=10 pm: r_out (pm)", turning_points(E0, sig, eps)[1], 14)
val("A=10 pm: T_quad (ps)", period_quad(E0, sig, eps, mu), 14)
say()

say("-" * 74)
say("5.  the integrators: energy conservation and measured order")
say("-" * 74)
r_start = r_min(sig) + 10.0
E_start = V(r_start, sig, eps)
Tq = period_quad(E_start, sig, eps, mu)
say("neon-neon released at rest at r_min + 10 pm; one period is %.6g ps" % Tq)
say("the error measured is max|E(t) - E(0)|/eps over exactly ONE period.")
say()
say("%-10s %-14s %-14s %-14s" % ("dt (ps)", "verlet dE/eps", "sympl dE/eps", "fwd dE/eps"))
ORD = []
for dt in (4e-3, 2e-3, 1e-3, 5e-4, 2.5e-4):
    n = int(round(Tq / dt))
    _, _, _, E0v, lo, hi = verlet(r_start, 0.0, sig, eps, mu, dt, n)
    dv = max(abs(hi - E0v), abs(lo - E0v)) / eps
    _, _, E0s, lo, hi = euler_sym(r_start, 0.0, sig, eps, mu, dt, n)
    ds = max(abs(hi - E0s), abs(lo - E0s)) / eps
    _, _, E0f, lo, hi = euler_fwd(r_start, 0.0, sig, eps, mu, dt, n)
    df = max(abs(hi - E0f), abs(lo - E0f)) / eps
    say("%-10.4g %-14.6g %-14.6g %-14.6g" % (dt, dv, ds, df))
    ORD.append((dt, dv, ds, df))


def order_of(col):
    return math.log(ORD[0][col] / ORD[-1][col]) / math.log(ORD[0][0] / ORD[-1][0])


val("velocity Verlet measured order", order_of(1), 6)
val("symplectic Euler measured order", order_of(2), 6)
val("forward Euler measured order", order_of(3), 6)
say("   (order is the log-log slope over dt = 4e-3 .. 2.5e-4 ps, a factor 16)")
say()
say("consecutive-halving ratios (2^p), velocity Verlet:")
for i in range(len(ORD) - 1):
    say("   dt %.4g -> %.4g   ratio %.6g" % (ORD[i][0], ORD[i + 1][0],
                                             ORD[i][1] / ORD[i + 1][1]))
say()
say("boundedness: the same run at dt = 1e-3 ps over 1, 10 and 100 periods.")
say("a symplectic scheme's energy error stays BOUNDED; forward Euler's grows.")
say("%-10s %-14s %-14s %-14s" % ("periods", "verlet dE/eps", "sympl dE/eps", "fwd dE/eps"))
BOUND = []
for np_ in (1, 10, 100):
    n = int(round(np_ * Tq / 1e-3))
    _, _, _, E0v, lo, hi = verlet(r_start, 0.0, sig, eps, mu, 1e-3, n)
    dv = max(abs(hi - E0v), abs(lo - E0v)) / eps
    _, _, E0s, lo, hi = euler_sym(r_start, 0.0, sig, eps, mu, 1e-3, n)
    ds = max(abs(hi - E0s), abs(lo - E0s)) / eps
    _, _, E0f, lo, hi = euler_fwd(r_start, 0.0, sig, eps, mu, 1e-3, n)
    df = max(abs(hi - E0f), abs(lo - E0f)) / eps
    say("%-10d %-14.6g %-14.6g %-14.6g" % (np_, dv, ds, df))
    BOUND.append((np_, dv, ds, df))
val("verlet  100-period / 1-period", BOUND[2][1] / BOUND[0][1], 6)
val("sympl.  100-period / 1-period", BOUND[2][2] / BOUND[0][2], 6)
val("forward 100-period / 1-period", BOUND[2][3] / BOUND[0][3], 6)
say()
say("a fixed trajectory pin: neon-neon, pinned, released at rest at r_min+10 pm,")
say("velocity Verlet dt = 1e-3 ps, state after exactly 1000 steps:")
rs, rf, vf, E0v, lo, hi = verlet(r_start, 0.0, sig, eps, mu, 1e-3, 1000)
val("r(1.0 ps) (pm)", rf, 14)
val("v(1.0 ps) (pm/ps)", vf, 14)
val("E(0) (u (pm/ps)^2)", E0v, 14)
say()

say("-" * 74)
say("6.  escape: the unbound case")
say("-" * 74)
say("released at rest, every start is bound (E = V(r0) < 0).  Give it speed:")
r0 = r_min(sig) + 10.0
Vr0 = V(r0, sig, eps)
v_esc = math.sqrt(-2.0 * Vr0 / mu)
val("r0 (pm)", r0, 14)
val("V(r0)/eps", Vr0 / eps, 14)
val("escape speed at r0 (pm/ps = m/s)", v_esc, 14)
val("  same in km/s", v_esc * 1e-3, 14)
_, rf, vf, E0, lo, hi = verlet(r0, 1.02 * v_esc, sig, eps, mu, 1e-3, 20000)
val("E with v = 1.02 v_esc, /eps", E0 / eps, 14)
val("r after 20 ps (pm)", rf, 14)
val("v at infinity (pm/ps), = sqrt(2E/mu)", math.sqrt(2 * E0 / mu), 14)
val("v after 20 ps (pm/ps)", vf, 14)
say()

say("-" * 74)
say("7.  PhET's parameters against the literature")
say("-" * 74)
say("the printed r_min/sigma of the source table reproduces 2^(1/6):")
for nm, s_, rm in LIT_TABLE_RMIN:
    say("   %-4s r_min/sigma = %.6f   (2^(1/6) = %.6f, diff %.2g)" %
        (nm, rm / s_, 2 ** (1 / 6), abs(rm / s_ - 2 ** (1 / 6))))
say()
say("PhET's sigma is the literature r_min, not the literature sigma:")
say("%-5s %-9s %-10s %-10s %-9s %-9s" %
    ("atom", "PhET sig", "lit sigma", "lit r_min", "vs sigma", "vs r_min"))
LIT_CMP = []
for at, key in (("Ne", "NeNe"), ("Ar", "ArAr"), ("O", "OO")):
    ps = PAIR_PINS[key]["sig"]
    ls, le, lrm, src = LIT[at]
    lrm_c = lrm if lrm is not None else ls * 2 ** (1 / 6)
    say("%-5s %-9.6g %-10.6g %-10.6g %-9.3g %-9.3g" %
        (at, ps, ls, lrm_c, ps / ls - 1, ps / lrm_c - 1))
    LIT_CMP.append((at, ps, ls, lrm_c, ps / ls - 1, ps / lrm_c - 1))
say("   (2^(1/6) - 1 = %.4f, i.e. 12.2%%)" % (2 ** (1 / 6) - 1))
say()
say("%-5s %-10s %-10s %-9s" % ("atom", "PhET eps", "lit eps/k_B", "PhET/lit"))
for at, key in (("Ne", "NeNe"), ("Ar", "ArAr"), ("O", "OO")):
    pe = PAIR_PINS[key]["epsK"]
    ls, le, lrm, src = LIT[at]
    say("%-5s %-10.6g %-10.6g %-9.4g" % (at, pe, le, pe / le))
say("   Ar second source (BSL): sigma %.4g pm, eps/k_B %.4g K" % LIT_ALT["Ar"][:2])
say("   PhET's own SOMConstants: EPSILON_FOR_DIATOMIC_OXYGEN 113 K (= the")
say("   literature O2 value), SIGMA_FOR_DIATOMIC_OXYGEN 365 pm; the Atomic")
say("   Interactions oxygen pair uses 1000 K and 200 pm instead.")
say()
say("Lorentz-Berthelot on the mixed pairs: sig_ab = (sig_a+sig_b)/2,")
say("eps_ab = sqrt(eps_a eps_b).")
say("%-6s %-10s %-10s %-10s %-10s" % ("pair", "PhET sig", "LB sig", "PhET eps", "LB eps"))
LB = []
for key, a, b in (("NeAr", "Ne", "Ar"), ("NeO", "Ne", "O"), ("ArO", "Ar", "O")):
    pa, pb = PAIR_PINS[a + a], PAIR_PINS[b + b]
    lbs = 0.5 * (pa["sig"] + pb["sig"])
    lbe = math.sqrt(pa["epsK"] * pb["epsK"])
    q = PAIR_PINS[key]
    say("%-6s %-10.6g %-10.6g %-10.6g %-10.6g" % (key, q["sig"], lbs, q["epsK"], lbe))
    LB.append((key, q["sig"], lbs, q["epsK"], lbe))
say("   PhET's mixed sigma is r_a + r_b (van der Waals radii), which equals the")
say("   Lorentz mean only when sigma = 2r for both atoms — true for Ne and Ar,")
say("   false for O.  Lorentz on the literature r_min values:")
for a, b in (("Ne", "Ar"),):
    ra = LIT[a][2] or LIT[a][0] * 2 ** (1 / 6)
    rb = LIT[b][2] or LIT[b][0] * 2 ** (1 / 6)
    say("      %s-%s: (r_min_a + r_min_b)/2 = %.4g pm  vs PhET %.4g pm" %
        (a, b, 0.5 * (ra + rb), PAIR_PINS["NeAr"]["sig"]))
say()
say("law of corresponding states — kT_c/eps from PhET's own critical points")
say("and the literature eps (nothing quoted from memory):")
CS = []
for at in ("Ne", "Ar", "O"):
    ratio = PHET_CRIT[at] / LIT[at][1]
    say("   %-3s T_c = %-6.4g K / eps = %-6.4g K  ->  kT_c/eps = %.4f" %
        (at, PHET_CRIT[at], LIT[at][1], ratio))
    CS.append(ratio)
val("mean kT_c/eps", sum(CS) / 3, 8)
val("spread (max-min)/mean", (max(CS) - min(CS)) / (sum(CS) / 3), 6)
say()

say("-" * 74)
say("8.  PhET's own arithmetic, reproduced")
say("-" * 74)
say("PhET's LjPotentialCalculator uses K_BOLTZMANN = 138e-25 and its own")
say("model units; getRepulsiveLjForce = 48 e' sig^12/r^13 and")
say("getAttractiveLjForce = 24 e' sig^6/r^7, whose difference is exactly")
say("-dV/dr.  Checked here as an identity, in this file's units:")
for f in (0.95, 1.122462048309373, 1.5):
    r = f * sig0
    rep = 48.0 * eps0 * sig0 ** 12 / r ** 13
    att = 24.0 * eps0 * sig0 ** 6 / r ** 7
    say("   r/sig %-6.4g  F_rep - F_att = %-20.14g  F() = %-20.14g" %
        (f, rep - att, F(r, sig0, eps0)))
val("PhET MIN_SIGMA (pm)", PHET_MIN_SIGMA, 6)
val("PhET MAX_SIGMA (pm)", PHET_MAX_SIGMA, 6)
val("PhET MIN_EPSILON (K)", PHET_MIN_EPSILON, 6)
val("PhET MAX_EPSILON (K)", PHET_MAX_EPSILON, 6)
val("PhET adjustable default sigma (pm)", PHET_ADJ_SIGMA, 6)
val("PhET adjustable default eps (K)", PHET_ADJ_EPSILON, 6)
say()

say("-" * 74)
say("9.  drawing scales")
say("-" * 74)
say("the well drawn over r in [0.85, 3] sigma; V in [-1.25, 1.5] eps")
for key in ("NeNe", "ArAr", "OO", "Adj"):
    q = PAIR_PINS[key]
    say("   %-5s sigma %-7.6g r_min %-9.6g  0.85 sig %-9.6g  3 sig %-9.6g" %
        (key, q["sig"], r_min(q["sig"]), 0.85 * q["sig"], 3 * q["sig"]))
say()
say("-" * 74)
say("10.  the pins selfTest quotes, in the sim's own units")
say("-" * 74)
say("the strongest pull: V''(r) = 0 at (sigma/r)^6 = 7/26, r = (26/7)^(1/6) sigma")
val("(26/7)^(1/6)", (26.0 / 7.0) ** (1.0 / 6.0), 15)
for key in ("NeNe", "ArAr"):
    q = PAIR_PINS[key]
    rF = q["sig"] * (26.0 / 7.0) ** (1.0 / 6.0)
    val("%s  r_F (pm)" % key, rF, 14)
    val("%s  F(r_F) (u (pm/ps)^2/pm)" % key, F(rF, q["sig"], q["eps"]), 14)
    val("%s  F(r_F) (pN)" % key, F(rF, q["sig"], q["eps"]) * F_TO_PN, 14)
    val("%s  V''(r_F) (must be 0)" % key, Vpp(rF, q["sig"], q["eps"]), 3)
say()
say("argon-argon, V and F at multiples of sigma (PhET's parameters)")
qa = PAIR_PINS["ArAr"]
for f in (0.95, 1.0, 1.122462048309373, 1.5, 2.5):
    r = f * qa["sig"]
    say("   r/sig %-8.6g V = %-22.14g F = %-22.14g" %
        (f, V(r, qa["sig"], qa["eps"]), F(r, qa["sig"], qa["eps"])))
say()
say("the adjustable pair at PhET's defaults (sigma 350 pm, eps 100 K, m 25 u)")
qA = PAIR_PINS["Adj"]
val("Adj  eps (u (pm/ps)^2)", qA["eps"], 14)
val("Adj  r_min (pm)", r_min(qA["sig"]), 14)
val("Adj  k (u/ps^2)", qA["k"], 14)
val("Adj  T pinned (ps)", qA["T_pin"], 14)
val("Adj  T moving (ps)", qA["T_mov"], 14)
say()
say("display conversions at the neon well depth")
val("eps (meV)", eps0 * E_TO_MEV, 14)
val("4 eps/sigma (pN)", 4 * eps0 / sig0 * F_TO_PN, 14)
val("F at 1.2 sigma (pN)", F(1.2 * sig0, sig0, eps0) * F_TO_PN, 14)
val("F at 0.95 sigma (pN)", F(0.95 * sig0, sig0, eps0) * F_TO_PN, 14)
say()
say("the quadrature at the JS default panel count (n = 96) against n = 400")
for frac in (-0.9, -0.5, -0.05):
    E = frac * eps0
    a96 = period_quad(E, sig0, eps0, PAIR_PINS["NeNe"]["mu_pin"], 96)
    a400 = period_quad(E, sig0, eps0, PAIR_PINS["NeNe"]["mu_pin"], 400)
    say("   E/eps %-7.4g  n=96  %-18.14g  n=400 %-18.14g  rel %.3g"
        % (frac, a96, a400, abs(a96 - a400) / a400))
say()
say("the 20-period drift at dt = 1e-3 ps (what the integrator view plots)")
nn = int(round(20 * Tq / 1e-3))
for kind, fn in (("verlet", verlet), ("symplectic", euler_sym), ("forward", euler_fwd)):
    out = fn(r_start, 0.0, sig, eps, mu, 1e-3, nn)
    E0x, lox, hix = out[-3], out[-2], out[-1]
    val("  %s max|dE|/eps over 20 periods" % kind,
        max(abs(hix - E0x), abs(lox - E0x)) / eps, 8)
say()
say("the escape speed at r_min + 10 pm (neon, pinned)")
val("v_esc (pm/ps = m/s)", math.sqrt(-2 * V(r_min(sig0) + 10, sig0, eps0) / PAIR_PINS["NeNe"]["mu_pin"]), 14)
say()
say("Lorentz-Berthelot on the LITERATURE like-pairs (what the sim uses when")
say("the literature switch is on and the pair is mixed):")
for k, a, b in (("NeAr", "Ne", "Ar"), ("NeO", "Ne", "O"), ("ArO", "Ar", "O")):
    s_ = 0.5 * (LIT[a][0] + LIT[b][0])
    e_ = math.sqrt(LIT[a][1] * LIT[b][1])
    say("   %-5s sigma %-10.10g  eps %-10.10g  r_min %-10.10g" % (k, s_, e_, r_min(s_)))
say()

say("-" * 74)
say("11.  the comparison numbers, at FULL precision")
say("-" * 74)
say("(section 7 prints these rounded for reading; a rounded number pasted into")
say("a test is a value nobody computed, which is how four pins were wrong on")
say("the first run.  These are the ones selfTest quotes.)")
val("mu(Ne,Ar) = m1 m2/(m1+m2)  (u)",
    PHET_M["Ne"] * PHET_M["Ar"] / (PHET_M["Ne"] + PHET_M["Ar"]), 17)
val("mu(Ne,Ne)/2", PHET_M["Ne"] / 2, 17)
val("PhET sig(Ne)/lit r_min(Ne) - 1", 308.0 / LIT["Ne"][2] - 1, 17)
val("PhET sig(Ne)/lit sigma(Ne) - 1", 308.0 / LIT["Ne"][0] - 1, 17)
val("PhET sig(Ar)/lit r_min(Ar) - 1", 376.0 / LIT["Ar"][2] - 1, 17)
val("PhET sig(Ar)/lit sigma(Ar) - 1", 376.0 / LIT["Ar"][0] - 1, 17)
val("PhET sig(O)/lit sigma(O) - 1", 200.0 / LIT["O"][0] - 1, 17)
val("PhET eps(O)/lit eps(O) - 1", 1000.0 / LIT["O"][1] - 1, 17)
val("Berthelot sqrt(35.8 x 111.84)  (K)", math.sqrt(35.8 * 111.84), 17)
val("Lorentz (308+376)/2  (pm)", 0.5 * (308.0 + 376.0), 17)
val("PhET eps(NeAr)/Berthelot - 1", 59.5 / math.sqrt(35.8 * 111.84) - 1, 17)
val("lit Ar eps / lit-alt Ar eps - 1", LIT["Ar"][1] / LIT_ALT["Ar"][1] - 1, 17)
val("kT_c/eps for Ne (45/35.7)", PHET_CRIT["Ne"] / LIT["Ne"][1], 17)
val("mean kT_c/eps", sum(CS) / 3, 17)
val("spread of kT_c/eps", (max(CS) - min(CS)) / (sum(CS) / 3), 17)
say("the outer turning point at 0.98 of the escape speed, neon at r_min+10:")
r98 = r_min(sig0) + 10.0
E98 = 0.5 * PAIR_PINS["NeNe"]["mu_pin"] * (0.98 * math.sqrt(
    -2 * V(r98, sig0, eps0) / PAIR_PINS["NeNe"]["mu_pin"])) ** 2 + V(r98, sig0, eps0)
val("  E/eps", E98 / eps0, 17)
val("  r_out (pm)", turning_points(E98, sig0, eps0)[1], 17)
say()

say("-" * 74)
say("12.  the drawn r window, and what the drag can reach")
say("-" * 74)
say("The sim draws and drags over r in [R_LO * sigma, R_HI * sigma] with")
say("R_LO = 0.72 and R_HI = 3.2.  Those two numbers are a CONTRACT — the")
say("inward end of a drag is exactly the floor — so they are pinned in")
say("absolute picometres here, not as a re-typed product of the constant,")
say("which is how the mutation sweep found every assertion on them blind.")
R_LO, R_HI = 0.72, 3.2
say("%-8s %-20s %-20s %-16s" % ("pair", "floor (pm)", "ceiling (pm)", "V(floor)/eps"))
for key, lab, a, b, s_, e_ in PAIRS:
    say("%-8s %-20.17g %-20.17g %-16.12g"
        % (key, R_LO * s_, R_HI * s_, V(R_LO * s_, s_, 1.0)))
say()
val("V(0.72 sigma)/eps  (the wall at the floor)", V(R_LO * sig0, sig0, 1.0), 17)
val("V(0.50 sigma)/eps  (the mutant's floor)", V(0.50 * sig0, sig0, 1.0), 17)
val("ratio", V(0.50 * sig0, sig0, 1.0) / V(R_LO * sig0, sig0, 1.0), 8)
say()
say("Where the drawn potential leaves the TOP of the atoms/well box: the box")
say("runs to V/eps = 2.4, and 4(u^2 - u) = 2.4 with u = (sigma/r)^6 gives")
say("u = (4 + sqrt(16 + 38.4))/8, so r/sigma = u^(-1/6).")
u_clip = (4 + math.sqrt(16 + 4 * 4 * 2.4)) / 8
val("u at the top of the box", u_clip, 17)
val("r/sigma there", u_clip ** (-1.0 / 6.0), 17)
val("  in pm, neon", sig0 * u_clip ** (-1.0 / 6.0), 17)
val("check: V/eps there (must be 2.4)", V(sig0 * u_clip ** (-1.0 / 6.0), sig0, 1.0), 12)
say("Every sample below that radius is clipped away by polyline, so moving the")
say("window FLOOR changes no pixel of the curve — only where the 261 samples")
say("fall, and what an inward drag is allowed to reach.  Measured: with the")
say("floor at 0.50 sigma, six of eight captured views hash identically and the")
say("two two-atoms views differ only in sample placement, while the drag floor")
say("moves 221.76 -> 154.00 pm for neon and the wall there goes from 177 eps")
say("to 16128 eps.  The assertions therefore pin the floor and the ceiling in")
say("pm, the first and last SAMPLE of the drawn curve, and the invariance")
say("(that the picture does not depend on the floor) deliberately.")
say()
say("the lowest r any control other than the drag can produce is the release,")
say("at r_min + rel with rel >= -20 pm:")
for key, lab, a, b, s_, e_ in PAIRS:
    say("   %-6s r_min - 20 = %-12.6f  (floor %.2f pm, so the floor is only"
        " reachable by dragging)" % (key, r_min(s_) - 20, R_LO * s_))
say()

say("=" * 74)
say("done")
say("=" * 74)

here = os.path.dirname(os.path.abspath(__file__))
io.open(os.path.join(here, "refvals.txt"), "w", encoding="utf-8").write("\n".join(OUT) + "\n")
print("\n[written refvals.txt: %d lines]" % len(OUT))
