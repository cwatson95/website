#!/usr/bin/env python3
"""derive.py — the Python twin of models-of-the-hydrogen-atom.html.

Re-derives every closed form the sim implements and prints reference values to
>= 12 digits.  Those printed lines (refvals.txt) are what selfTest asserts,
labelled (scipy) / (sympy) / (python).  Nothing here is quoted from memory:
CODATA 2022 comes from scipy.constants, the hydrogen radial functions from
scipy.special.genlaguerre, the spherical harmonics from scipy.special.sph_harm_y,
and every clever evaluation is checked against a brute-force one.

Sections
  1  constants, Bohr energies and radii (infinite and reduced mass)
  2  every transition wavelength; the five series; PhET's rounded table
  3  de Broglie: n*lambda_dB = 2*pi*r_n
  4  Schrodinger: normalisation, nodes, <r>, |psi|^2, the projected column
  5  Einstein A coefficients, lifetimes, branching ratios (exact + quad + sympy)
  6  PhET's own stochastic model: the transition-strength table, the (n,l,m)
     walk, and the mulberry32 PRNG the JS uses (bit-identical here)
  7  air wavelengths (Edlen 1966) against the conventional measured lines

Run:  python3 derive.py > refvals.txt
"""
import math
import sys

import numpy as np
import scipy.constants as C
from scipy.integrate import quad
from scipy.special import genlaguerre, factorial, lpmv, sph_harm_y

OUT = []


def P(label, value, digits=14):
    """Print one reference line.  Read the whole block; never through head/tail."""
    if isinstance(value, float):
        s = "%.*g" % (digits, value)
    else:
        s = str(value)
    line = "%-58s %s" % (label, s)
    OUT.append(line)
    print(line)


def H(title):
    line = "\n===== %s =====" % title
    OUT.append(line)
    print(line)


# ======================================================================
# 1.  constants
# ======================================================================
H("1. constants (scipy.constants, CODATA 2022)")
Rinf = C.value("Rydberg constant")                 # m^-1
Ryd_eV = C.value("Rydberg constant times hc in eV")  # eV
a0 = C.value("Bohr radius")                        # m
alpha = C.value("fine-structure constant")
c = C.c
h = C.h
hbar = C.hbar
me = C.m_e
mp = C.m_p
e = C.e
eps0 = C.epsilon_0
Eh = C.value("Hartree energy")
t_au = hbar / Eh                                   # atomic unit of time, s
P("R_inf (m^-1)", Rinf)
P("R_inf*h*c (eV)", Ryd_eV)
P("a_0 (m)", a0)
P("alpha", alpha)
P("Hartree energy (J)", Eh)
P("atomic unit of time (s)", t_au)
P("m_e/m_p", me / mp)
P("m_e (kg)", me)
P("h (J s)", h)
P("c (m/s)", c)
# a_0, alpha and m_e are three separately rounded CODATA values, so the
# identity a_0 = hbar/(m_e alpha c) does NOT hold to machine precision here.
P("a_0 - hbar/(m_e alpha c), relative", (hbar / (me * alpha * c) - a0) / a0)

# reduced mass of the electron-proton system
mu = me * mp / (me + mp)
RH = Rinf * mu / me
RH_eV = Ryd_eV * mu / me
aH = a0 * me / mu
P("mu/m_e", mu / me)
P("R_H (m^-1)", RH)
P("R_H*h*c (eV)", RH_eV)
P("a_H = a_0 m_e/mu (m)", aH)
# cross-check: R_H = mu e^4 / (8 eps0^2 h^3 c), built from first principles
RH_direct = mu * e ** 4 / (8 * eps0 ** 2 * h ** 3 * c)
P("R_H from mu e^4/(8 eps0^2 h^3 c)", RH_direct)
P("  rel. difference vs scipy chain", abs(RH_direct - RH) / RH)

H("1b. Bohr energies and radii")
for n in range(1, 13):
    P("E_%d (eV, infinite mass)" % n, -Ryd_eV / n ** 2)
for n in range(1, 13):
    P("E_%d (eV, reduced mass)" % n, -RH_eV / n ** 2)
for n in range(1, 13):
    P("r_%d (m) = n^2 a_0" % n, n * n * a0)
for n in range(1, 7):
    # speed v_n = alpha c / n ; classical orbital period
    P("v_%d (m/s) = alpha c/n" % n, alpha * c / n)
P("r_1 in pm", a0 * 1e12)
P("E_1 - E_inf ionisation (eV, reduced mass)", RH_eV)
# virial: <T> = -E, <V> = 2E
P("virial <V>/<T> at n=1", (2 * (-RH_eV)) / (RH_eV))

# ======================================================================
# 2.  transition wavelengths
# ======================================================================
H("2. transition wavelengths (vacuum, reduced mass)")


def lam_vac(n1, n2):
    """vacuum wavelength in nm of the n2 -> n1 transition (n2 > n1)"""
    return 1e9 / (RH * (1.0 / n1 ** 2 - 1.0 / n2 ** 2))


def lam_vac_inf(n1, n2):
    return 1e9 / (Rinf * (1.0 / n1 ** 2 - 1.0 / n2 ** 2))


SERIES = {1: "Lyman", 2: "Balmer", 3: "Paschen", 4: "Brackett", 5: "Pfund", 6: "Humphreys"}
for n1 in range(1, 7):
    for n2 in range(n1 + 1, min(n1 + 6, 12) + 1):
        P("lambda(%d->%d) %s nm" % (n2, n1, SERIES[n1]), lam_vac(n1, n2))
    P("lambda(inf->%d) %s limit nm" % (n1, SERIES[n1]), 1e9 / (RH / n1 ** 2))

# independent route: photon energy in eV, then lambda = hc/E
H("2b. cross-check via E = hc/lambda")
hc_eV_nm = h * c / e * 1e9
P("hc (eV nm)", hc_eV_nm)
for (n1, n2) in [(1, 2), (2, 3), (2, 4), (3, 4), (1, 6)]:
    dE = RH_eV * (1.0 / n1 ** 2 - 1.0 / n2 ** 2)
    P("lambda(%d->%d) from hc/dE, nm" % (n2, n1), hc_eV_nm / dE)
    P("  rel diff vs 1/(R_H dnu)", abs(hc_eV_nm / dE - lam_vac(n1, n2)) / lam_vac(n1, n2))

H("2c. PhET's own table: round(1240/(13.6*(1/n1^2-1/n2^2)))")
phet_tbl = {}
for n1 in range(1, 6):
    for n2 in range(6, n1, -1):
        w = round(1240.0 / (13.6 * (1.0 / n1 ** 2 - 1.0 / n2 ** 2)))
        phet_tbl[(n1, n2)] = w
        P("PhET lambda(%d->%d) nm (integer)" % (n2, n1), w)
        P("  exact vacuum nm", lam_vac(n1, n2))
        P("  PhET/exact - 1", w / lam_vac(n1, n2) - 1.0)
uvs = sorted(w for w in phet_tbl.values() if w < 380)
viss = sorted(w for w in phet_tbl.values() if 380 <= w <= 780)
irs = sorted(w for w in phet_tbl.values() if w > 780)
P("PhET UV wavelengths", uvs)
P("PhET visible wavelengths", viss)
P("PhET IR wavelengths", irs)
P("PhET number of transitions (n=1..6)", len(phet_tbl))

# ======================================================================
# 3.  de Broglie
# ======================================================================
H("3. de Broglie standing wave: n lambda_dB = 2 pi r_n")
for n in range(1, 7):
    v = alpha * c / n
    lam_dB = h / (me * v)
    P("lambda_dB(n=%d) (m)" % n, lam_dB)
    P("  n*lambda_dB / (2 pi r_n) - 1", n * lam_dB / (2 * math.pi * n * n * a0) - 1.0)
# the identity, written out: lambda_dB = h/(m alpha c/n) and 2 pi r_n = 2 pi n^2 a0
# with a0 = hbar/(m alpha c) => 2 pi n^2 hbar/(m alpha c) = n * h n /(m alpha c) . ok
P("a_0 from hbar/(m_e alpha c) (m)", hbar / (me * alpha * c))
P("  rel diff vs scipy a_0", abs(hbar / (me * alpha * c) - a0) / a0)

# ======================================================================
# 4.  Schrodinger
# ======================================================================
H("4. hydrogen wavefunctions (a_0 = 1 throughout)")


def Rnl_scipy(n, l, r):
    """R_nl(r) in units a_0^{-3/2}, scipy's genlaguerre."""
    rho = 2.0 * r / n
    norm = math.sqrt((2.0 / n) ** 3 * factorial(n - l - 1) / (2.0 * n * factorial(n + l)))
    return norm * np.exp(-rho / 2.0) * rho ** l * genlaguerre(n - l - 1, 2 * l + 1)(rho)


def Rnl_poly(n, l):
    """R_nl(r) = exp(-r/n) * sum_k coef[k] r^k  — the coefficients, exactly.
    L_{n-l-1}^{2l+1}(rho) = sum_{k} (-1)^k C(n+l, n-l-1-k) rho^k / k!"""
    norm = math.sqrt((2.0 / n) ** 3 * factorial(n - l - 1) / (2.0 * n * factorial(n + l)))
    coef = [0.0] * (n)               # powers r^l .. r^{n-1}
    for k in range(0, n - l):
        cb = math.comb(n + l, n - l - 1 - k)
        term = (-1) ** k * cb / math.factorial(k) * (2.0 / n) ** k
        coef[l + k] += norm * (2.0 / n) ** l * term
    return coef                       # multiply by exp(-r/n)


def Rnl_from_poly(n, l, r):
    co = Rnl_poly(n, l)
    s = 0.0
    for k in range(len(co) - 1, -1, -1):
        s = s * r + co[k]
    return s * math.exp(-r / n)


H("4a. normalisation  int R_nl^2 r^2 dr = 1")
for (n, l) in [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2), (4, 2), (5, 1), (6, 5)]:
    val = quad(lambda r: Rnl_scipy(n, l, r) ** 2 * r * r, 0, 400, limit=400)[0]
    P("int R_%d%d^2 r^2 dr (scipy quad)" % (n, l), val)
    # the polynomial form must agree with scipy's genlaguerre
    rs = np.linspace(1e-6, 60, 41)
    d = max(abs(Rnl_from_poly(n, l, float(r)) - Rnl_scipy(n, l, float(r))) for r in rs)
    P("  max|poly - genlaguerre| over r in [0,60]", d)

H("4b. R_nl at spot radii (a_0 = 1)")
SPOTS = [(1, 0, 0.5), (1, 0, 1.0), (1, 0, 2.0), (2, 0, 1.0), (2, 0, 2.0), (2, 0, 4.0),
         (2, 1, 2.0), (2, 1, 4.0), (3, 0, 3.0), (3, 1, 6.0), (3, 2, 9.0),
         (4, 1, 8.0), (5, 3, 20.0), (6, 0, 12.0), (6, 5, 30.0)]
for (n, l, r) in SPOTS:
    P("R_%d%d(%.1f)" % (n, l, r), float(Rnl_scipy(n, l, r)))

H("4c. radial nodes (n-l-1) and <r>, <r^2>")
for (n, l) in [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2), (4, 0), (4, 3), (5, 2), (6, 1)]:
    # count sign changes of R on (0, 60] with a fine grid, then refine by bisection
    rs = np.linspace(1e-9, 40 + 12 * n, 400000)
    v = Rnl_scipy(n, l, rs)
    sgn = np.sign(v)
    nz = int(np.sum(sgn[1:] * sgn[:-1] < 0))
    P("radial nodes R_%d%d (counted)" % (n, l), nz)
    P("  n-l-1", n - l - 1)
    r1 = quad(lambda r: Rnl_scipy(n, l, r) ** 2 * r ** 3, 0, 600, limit=600)[0]
    r2 = quad(lambda r: Rnl_scipy(n, l, r) ** 2 * r ** 4, 0, 600, limit=600)[0]
    P("  <r>_%d%d (quad)" % (n, l), r1)
    P("  <r> closed form (3n^2-l(l+1))/2", (3 * n * n - l * (l + 1)) / 2.0)
    P("  <r^2>_%d%d (quad)" % (n, l), r2)
    P("  <r^2> closed form n^2(5n^2+1-3l(l+1))/2", n * n * (5 * n * n + 1 - 3 * l * (l + 1)) / 2.0)
    P("  <1/r> (quad)", quad(lambda r: Rnl_scipy(n, l, r) ** 2 * r, 0, 600, limit=600)[0])
    P("  <1/r> closed form 1/n^2", 1.0 / n ** 2)

H("4d. angular part |Y_lm|^2  (scipy.special.sph_harm_y)")
for (l, m) in [(0, 0), (1, 0), (1, 1), (2, 0), (2, 1), (2, 2), (3, 0), (3, 2), (5, 3)]:
    nrm = quad(lambda th: abs(sph_harm_y(l, m, th, 0.0)) ** 2 * 2 * math.pi * math.sin(th),
               0, math.pi, limit=400)[0]
    P("int |Y_%d%d|^2 dOmega (scipy)" % (l, m), nrm)
    for cth in (0.0, 0.3, 0.7, 1.0):
        th = math.acos(cth)
        y = abs(sph_harm_y(l, m, th, 0.0)) ** 2
        # the same thing from lpmv, which is what the JS implements
        pm = lpmv(m, l, cth)
        y2 = (2 * l + 1) / (4 * math.pi) * factorial(l - m) / factorial(l + m) * pm * pm
        P("  |Y_%d%d|^2 at cos th=%.1f" % (l, m, cth), float(y))
        P("    lpmv route - scipy route", float(y2 - y))
    # angular nodes: zeros of P_l^m in cos th on (-1,1) = l - m
    # an EVEN number of samples, so cos th = 0 (a node of every odd l - m) is
    # never sampled exactly: a sampled zero makes sign(a)*sign(b) = 0, and the
    # < 0 test then misses that node entirely (P_1^0 counted 0 nodes instead of 1).
    cs = np.linspace(-0.999999, 0.999999, 200000)
    pv = lpmv(m, l, cs)
    P("  angular nodes of P_%d^%d counted" % (l, m), int(np.sum(np.sign(pv[1:]) * np.sign(pv[:-1]) < 0)))
    P("    l - m", l - m)

H("4e. |psi_nlm|^2 at spot points (a_0 = 1, cartesian x,y,z)")
def psi_sq(n, l, m, x, y, z):
    r = math.sqrt(x * x + y * y + z * z)
    if r == 0.0:
        cth = 1.0
    else:
        cth = z / r
    th = math.acos(max(-1.0, min(1.0, cth)))
    return float(Rnl_scipy(n, l, r) ** 2 * abs(sph_harm_y(l, m, th, 0.0)) ** 2)


PSPOTS = [(1, 0, 0, 0.0, 0.0, 1.0), (1, 0, 0, 0.6, 0.0, 0.8), (2, 0, 0, 0.0, 0.0, 3.0),
          (2, 1, 0, 0.0, 0.0, 4.0), (2, 1, 1, 4.0, 0.0, 0.0), (3, 2, 0, 0.0, 0.0, 6.0),
          (3, 2, 1, 5.0, 0.0, 5.0), (3, 2, 2, 7.0, 0.0, 0.0), (4, 3, 1, 8.0, 0.0, 8.0),
          (6, 0, 0, 0.0, 0.0, 20.0)]
for (n, l, m, x, y, z) in PSPOTS:
    P("|psi_%d%d%d|^2 at (%.1f,%.1f,%.1f)" % (n, l, m, x, y, z), psi_sq(n, l, m, x, y, z))

H("4f. projected column density  rho(x,z) = int |psi|^2 dy   (the drawn cloud)")
def column(n, l, m, x, z, ymax=None):
    if ymax is None:
        ymax = 30.0 + 14.0 * n * n
    f = lambda y: psi_sq(n, l, m, x, y, z)
    return 2.0 * quad(f, 0.0, ymax, limit=800)[0]


CSPOTS = [(1, 0, 0, 0.0, 0.5), (1, 0, 0, 1.0, 1.0), (2, 1, 0, 0.0, 4.0), (2, 1, 1, 3.0, 0.0),
          (3, 2, 0, 0.0, 8.0), (3, 2, 2, 9.0, 0.0), (4, 1, 0, 0.0, 10.0)]
for (n, l, m, x, z) in CSPOTS:
    P("column(%d,%d,%d; x=%.1f z=%.1f)" % (n, l, m, x, z), column(n, l, m, x, z))
# brute-force midpoint sum as the independent route on one of them
n, l, m, x, z = 2, 1, 0, 0.0, 4.0
ys = np.linspace(-60, 60, 200001)
bf = float(np.trapezoid([psi_sq(n, l, m, x, yy, z) for yy in ys], ys))
P("column(2,1,0; 0,4) brute-force trapezoid 200001 pts", bf)
P("  quad - brute", column(2, 1, 0, 0.0, 4.0) - bf)

# ======================================================================
# 5.  Einstein A coefficients
# ======================================================================
H("5. dipole radial integrals and Einstein A coefficients")


def radial_dipole_exact(n1, l1, n2, l2):
    """int_0^inf R_{n1 l1}(r) r R_{n2 l2}(r) r^2 dr, in a_0.
    Exact: both R are (poly in r) * exp(-r/n), so the integrand is a polynomial
    times exp(-s r) with s = 1/n1 + 1/n2, and int r^k e^{-sr} = k!/s^{k+1}."""
    c1, c2 = Rnl_poly(n1, l1), Rnl_poly(n2, l2)
    s = 1.0 / n1 + 1.0 / n2
    tot = 0.0
    for i, a in enumerate(c1):
        if a == 0.0:
            continue
        for j, b in enumerate(c2):
            if b == 0.0:
                continue
            k = i + j + 3
            tot += a * b * math.factorial(k) / s ** (k + 1)
    return tot


def radial_dipole_quad(n1, l1, n2, l2):
    return quad(lambda r: Rnl_scipy(n1, l1, r) * Rnl_scipy(n2, l2, r) * r ** 3,
                0, 1200, limit=2000)[0]


def einstein_A(nu, lu, nl_, ll):
    """A(n_u l_u -> n_l l_l) in s^-1, averaged over m_u and summed over m_l."""
    if abs(lu - ll) != 1 or nu <= nl_:
        return 0.0
    w = (0.5 / nl_ ** 2 - 0.5 / nu ** 2)          # omega in Hartree (atomic units)
    R = radial_dipole_exact(nu, lu, nl_, ll)
    lmax = max(lu, ll)
    A_au = (4.0 / 3.0) * alpha ** 3 * w ** 3 * (lmax / (2.0 * lu + 1.0)) * R * R
    return A_au / t_au


PAIRS = [(2, 1, 1, 0), (3, 1, 1, 0), (4, 1, 1, 0), (5, 1, 1, 0), (6, 1, 1, 0),
         (3, 0, 2, 1), (3, 2, 2, 1), (3, 1, 2, 0), (4, 0, 2, 1), (4, 2, 2, 1),
         (4, 1, 2, 0), (4, 1, 3, 0), (4, 3, 3, 2), (5, 2, 3, 1), (6, 1, 5, 0)]
for (nu, lu, nl_, ll) in PAIRS:
    Rx = radial_dipole_exact(nu, lu, nl_, ll)
    Rq = radial_dipole_quad(nu, lu, nl_, ll)
    P("R(%d%d -> %d%d) exact series" % (nu, lu, nl_, ll), Rx)
    P("  scipy quad", Rq)
    P("  rel diff", abs(Rx - Rq) / abs(Rq))
    P("A(%d%d -> %d%d) s^-1" % (nu, lu, nl_, ll), einstein_A(nu, lu, nl_, ll))

H("5b. total decay rates and lifetimes")
STATES = [(2, 0), (2, 1), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (4, 3),
          (5, 0), (5, 1), (5, 2), (6, 1)]
for (n, l) in STATES:
    tot = 0.0
    for np_ in range(1, n):
        for lp in (l - 1, l + 1):
            if lp < 0 or lp > np_ - 1:
                continue
            tot += einstein_A(n, l, np_, lp)
    P("Gamma(%d%d) total s^-1" % (n, l), tot)
    P("  tau(%d%d) ns" % (n, l), 1e9 / tot if tot > 0 else float("inf"))

H("5c. branching by lower n, averaged over l with the statistical weight (2l+1)")
# The quantity PhET's chooseLower_n approximates: given an excited n, how does
# the decay distribute over the lower n?  Take the l-averaged rate.
for n in range(2, 7):
    ws = []
    for np_ in range(1, n):
        num = 0.0
        den = 0.0
        for l in range(0, n):
            g = 2 * l + 1
            den += g
            for lp in (l - 1, l + 1):
                if lp < 0 or lp > np_ - 1:
                    continue
                num += g * einstein_A(n, l, np_, lp)
        ws.append(num / den)
    tot = sum(ws)
    P("n=%d l-averaged rates to n'=1..%d (s^-1)" % (n, n - 1), ["%.6g" % w for w in ws])
    P("  branching fractions", ["%.8f" % (w / tot) for w in ws])
    P("  total l-averaged rate s^-1", tot)

# ======================================================================
# 6.  PhET's own stochastic model
# ======================================================================
H("6. PhET's transition-strength table and the (n,l,m) walk")
PHET_W = [[], [12.53], [3.34, 0.87], [1.36, 0.24, 0.07],
          [0.69, 0.11, 0.0, 0.04], [0.39, 0.06, 0.02, 0.0, 0.0]]
for n in range(2, 7):
    row = PHET_W[n - 1]
    tot = sum(row)
    P("PhET weights from n=%d" % n, row)
    P("  normalised", ["%.8f" % (w / tot) for w in row])
    # what the true l-averaged branching says for the same n
P("PhET weight 12.53 vs 2*A(2p->1s)/1e8", 2 * einstein_A(2, 1, 1, 0) / 1e8)
P("PhET weight  3.34 vs 2*A(3p->1s)/1e8", 2 * einstein_A(3, 1, 1, 0) / 1e8)
P("PhET weight  1.36 vs 2*A(4p->1s)/1e8", 2 * einstein_A(4, 1, 1, 0) / 1e8)
P("PhET weight  0.69 vs 2*A(5p->1s)/1e8", 2 * einstein_A(5, 1, 1, 0) / 1e8)
P("PhET weight  0.39 vs 2*A(6p->1s)/1e8", 2 * einstein_A(6, 1, 1, 0) / 1e8)


# --- mulberry32, bit-identical to the JS in the sim ---------------------
# JS:  a = a + 0x6D2B79F5 | 0;
#      let t = Math.imul(a ^ a >>> 15, 1 | a);
#      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
#      return ((t ^ t >>> 14) >>> 0) / 4294967296;
# '+' binds tighter than '^', so the middle line is (t + imul(...)) ^ t — an
# easy thing to drop, and dropping it gives a different, equally plausible
# stream.  Everything below is kept UNSIGNED: Math.imul takes the low 32 bits
# of each operand whatever their sign, and every JS bit operator coerces to
# int32, so the unsigned bit patterns agree step for step.
M32 = 0xFFFFFFFF


def imul32(a, b):
    return (a * b) & M32


def mulberry32_seq(seed, count):
    a = seed & M32
    out = []
    for _ in range(count):
        a = (a + 0x6D2B79F5) & M32
        t = imul32(a ^ (a >> 15), 1 | a)
        t = ((t + imul32(t ^ (t >> 7), 61 | t)) & M32) ^ t
        out.append(((t ^ (t >> 14)) & M32) / 4294967296.0)
    return out


H("6b. mulberry32(12345) — the JS PRNG, bit-identical")
seq = mulberry32_seq(12345, 12)
for i, v in enumerate(seq):
    P("mulberry32(12345)[%d]" % i, v)
seq2 = mulberry32_seq(2026, 6)
for i, v in enumerate(seq2):
    P("mulberry32(2026)[%d]" % i, v)
big = mulberry32_seq(7, 200000)
P("mulberry32(7) mean over 2e5", float(np.mean(big)))
P("mulberry32(7) variance over 2e5", float(np.var(big)))
P("mulberry32(7) min, max", (min(big), max(big)))


# --- PhET's chooseLower_n, choose_l, choose_m, as a Markov chain --------
def phet_choose_lower_n_dist(n, l):
    """The exact distribution PhET's chooseLower_n draws from."""
    if n == 1:
        return {}
    if n == 2:
        return {} if l == 0 else {1: 1.0}
    lo = 2 if l == 0 else l
    hi = n - 1
    ws = {}
    tot = 0.0
    for i in range(lo, hi + 1):
        w = PHET_W[n - 1][i - 1]
        ws[i] = w
        tot += w
    if tot == 0:
        return {}
    return {k: v / tot for k, v in ws.items() if v > 0}


H("6c. PhET chooseLower_n distributions (n, l) -> {n': p}")
for n in range(2, 7):
    for l in range(0, n):
        d = phet_choose_lower_n_dist(n, l)
        P("PhET P(n'|n=%d,l=%d)" % (n, l), {k: round(v, 10) for k, v in d.items()})


def phet_choose_l_list(l, n_new):
    """choose_l: 0 -> 1; l == n_new or l == n_new-1 -> l-1; else 50/50 l+-1.
    An ORDERED list, matching the JS exactly: both sides feed it to the same
    weighted() and must therefore agree on the order as well as the weights."""
    if l == 0:
        return [(1, 1.0)]
    if l == n_new or l == n_new - 1:
        return [(l - 1, 1.0)]
    return [(l + 1, 0.5), (l - 1, 0.5)]


def phet_choose_m_list(m, l_new):
    if l_new == 0:
        return [(0, 1.0)]
    if m > l_new:
        return [(l_new, 1.0)]
    if m < -l_new:
        return [(-l_new, 1.0)]
    if m == l_new:
        return [(m, 0.5), (m - 1, 0.5)]
    if m == -l_new:
        return [(m, 0.5), (m + 1, 0.5)]
    return [(m + 1, 1.0 / 3), (m - 1, 1.0 / 3), (m, 1.0 / 3)]


def phet_choose_l_dist(l, n_new):
    return dict(phet_choose_l_list(l, n_new))


def phet_choose_m_dist(m, l_new):
    return dict(phet_choose_m_list(m, l_new))


H("6d. PhET choose_l / choose_m distributions")
for (l, nn) in [(0, 3), (1, 3), (2, 3), (1, 2), (2, 4), (3, 5)]:
    P("PhET P(l'|l=%d, n'=%d)" % (l, nn), phet_choose_l_list(l, nn))
for (m, ln) in [(0, 0), (0, 1), (1, 1), (-1, 1), (2, 1), (-2, 1), (0, 2), (1, 2), (2, 2), (-2, 2)]:
    P("PhET P(m'|m=%d, l'=%d)" % (m, ln), [(k, round(v, 10)) for k, v in phet_choose_m_list(m, ln)])


def valid_state(n, l, m):
    return 1 <= n <= 6 and 0 <= l <= n - 1 and -l <= m <= l


def phet_next_state_dist(n, l, m, n_new):
    """getNextState: choose l', choose m', and if the transition is not allowed
    (|dl| == 1 and |dm| <= 1 and n != n') fall back to (1,0,0)."""
    out = {}
    for lp, pl in phet_choose_l_list(l, n_new):
        for mp, pm in phet_choose_m_list(m, lp):
            ok = (valid_state(n, l, m) and valid_state(n_new, lp, mp) and n != n_new
                  and abs(l - lp) == 1 and abs(m - mp) <= 1)
            key = (n_new, lp, mp) if ok else (1, 0, 0)
            out[key] = out.get(key, 0.0) + pl * pm
    return out


H("6e. PhET getNextState distributions")
for (n, l, m, nn) in [(3, 1, 0, 2), (3, 2, 1, 2), (4, 1, -1, 2), (6, 0, 0, 3), (2, 1, 1, 1)]:
    d = phet_next_state_dist(n, l, m, nn)
    P("PhET P(next|%d,%d,%d -> n'=%d)" % (n, l, m, nn), {k: round(v, 10) for k, v in sorted(d.items())})

H("6f. PhET's drawn orbit radii and energy-diagram heights")
PHET_R = [15, 44, 81, 124, 174, 233]
P("PhET orbit radii (view units)", PHET_R)
P("  true n^2 scaled to r_1=15", [15 * n * n for n in range(1, 7)])
P("  PhET r_n / (n^2 r_1)", ["%.6f" % (PHET_R[n - 1] / (15.0 * n * n)) for n in range(1, 7)])
PHET_E = [0.025, 0.6, 0.73, 0.81, 0.86, 0.9]
P("PhET energy-diagram fractions", PHET_E)
P("  true (1 - 1/n^2)", ["%.10f" % (1 - 1.0 / n ** 2) for n in range(1, 7)])
P("PhET a_n = r_n/n^2 (view units)", ["%.8f" % (PHET_R[n - 1] / n ** 2) for n in range(1, 7)])

H("6g. PhET's other model constants (read from the minified build 1.0.9)")
P("Photon SPEED (view units/s)", 300)
P("Photon RADIUS", 15)
P("Electron RADIUS", 5)
P("ZoomedInBox SIDE_LENGTH", 475)
P("dt between emitted photons = 475/300/20 s", 475.0 / 300.0 / 20.0)
P("photons per second from the source", 1.0 / (475.0 / 300.0 / 20.0))
P("BilliardBall RADIUS", 30)
P("PlumPudding RADIUS", 35)
P("PlumPudding emission wavelength nm", 150)
P("PlumPudding absorb probability", 0.5)
P("PlumPudding emit probability per step", 0.1)
P("Bohr ELECTRON_ANGLE_DELTA deg/s", 480)
P("Bohr spontaneous-emission probability", 0.5)
P("Bohr min time in state before absorbing (s)", 0.75)
P("Bohr min time in state before emitting (s)", 1.0)
P("ClassicalSolarSystem start radius", 150)
P("ClassicalSolarSystem initial angular speed deg/s", 600)
P("ClassicalSolarSystem radius loss per second", 220)
P("ClassicalSolarSystem angular speed growth per step", 1.008)
P("ClassicalSolarSystem destroyed radius", 5)
P("de Broglie 3-D y scale", 0.35)
P("de Broglie brightness ring thickness", 3)
P("white light: fraction aimed at n=1 absorption lines", 0.4)
P("monochromatic wavelength range nm", (92, 780))
P("metastable state", (2, 0, 0))
P("metastable re-excite interval s", 2.0)
P("max spectrometer snapshots", 4)
P("time scales fast/normal/slow", (3, 1, 0.25))
# classical solar system: how long until the electron hits the proton, at dt
for dt in (1.0 / 60.0, 0.1):
    r = 150.0
    tt = 0.0
    steps = 0
    while r > 5.0 and steps < 200000:
        r -= 220.0 * dt
        tt += dt
        steps += 1
    P("PhET classical collapse time at dt=%.5f s" % dt, tt)
    P("  steps", steps)

# ======================================================================
# 7.  air wavelengths
# ======================================================================
H("7. vacuum -> standard air (Edlen 1966, Metrologia 2, 71)")


def n_air_edlen1966(lam_um):
    """Refractive index of standard dry air (15 C, 101325 Pa, 0.03% CO2).
    Edlen 1966 eq. (1):  (n-1)*1e8 = 8342.13 + 2406030/(130-s^2) + 15997/(38.9-s^2)
    with s = 1/lambda_vac in um^-1."""
    s2 = (1.0 / lam_um) ** 2
    return 1.0 + 1e-8 * (8342.13 + 2406030.0 / (130.0 - s2) + 15997.0 / (38.9 - s2))


# NIST, Handbook of Basic Atomic Spectroscopic Data, "Strong Lines of
# Hydrogen (H I)", https://physics.nist.gov/PhysRefData/Handbook/Tables/
# hydrogentable2.htm — fetched 2026-09-21, every printed row, in angstroms.
# NIST prints Lyman in VACUUM (below 2000 A) and everything else in AIR.
# Where a line is resolved into fine-structure components the strongest
# (largest intensity) is kept and the others are listed beside it.
NIST_VAC = [(15, 926.2256), (20, 930.7482), (30, 937.8034), (50, 949.7430),
            (100, 972.5367), (300, 1025.7222), (1000, 1215.66824), (500, 1215.67364)]
NIST_AIR = [(5, 3835.384), (6, 3889.049), (8, 3970.072), (15, 4101.74), (30, 4340.462),
            (30, 4861.2786), (10, 4861.2870), (60, 4861.3615),
            (90, 6562.7110), (30, 6562.7248), (180, 6562.8518),
            (5, 9545.97), (7, 10049.4), (12, 10938.1), (20, 12818.07), (40, 18751.01),
            (5, 21655.3), (8, 26251.5), (15, 40511.6), (4, 46525.1), (6, 74578), (3, 123685)]
P("NIST vacuum rows (intensity, A)", NIST_VAC)
P("NIST air rows (intensity, A)", NIST_AIR)


def nearest_transition(lam_nm, vacuum):
    """(n1, n2) whose computed wavelength is nearest to lam_nm."""
    best, bd = None, 1e99
    for n1 in range(1, 9):
        for n2 in range(n1 + 1, 16):
            lv = lam_vac(n1, n2)
            pred = lv if vacuum else lv / n_air_edlen1966(lv * 1e-3)
            if abs(pred - lam_nm) < bd:
                bd, best = abs(pred - lam_nm), (n1, n2)
    return best


H("7a. NIST vacuum lines (Lyman)")
for inten, ang in NIST_VAC:
    obs = ang / 10.0
    n1, n2 = nearest_transition(obs, True)
    pred = lam_vac(n1, n2)
    P("NIST %10.5f A  (I=%d)  -> %d->%d, obs nm" % (ang, inten, n2, n1), obs)
    P("  this model, vacuum nm", pred)
    P("  (model-obs)/obs", (pred - obs) / obs)
H("7b. NIST air lines (Balmer and beyond), Edlen 1966 vacuum->air")
for inten, ang in NIST_AIR:
    obs = ang / 10.0
    n1, n2 = nearest_transition(obs, False)
    lv = lam_vac(n1, n2)
    na = n_air_edlen1966(lv * 1e-3)
    pred = lv / na
    P("NIST %10.4f A  (I=%d)  -> %d->%d, obs air nm" % (ang, inten, n2, n1), obs)
    P("  this model, vacuum nm", lv)
    P("  n_air (Edlen 1966)", na)
    P("  this model, air nm", pred)
    P("  (model-obs)/obs", (pred - obs) / obs)
H("7c. the size of the residual: it is the relativistic (Dirac) correction")
P("alpha^2/4 (the 1s relativistic shift, relative)", alpha ** 2 / 4)
P("alpha^2 (relative)", alpha ** 2)
P("H-alpha strongest NIST component, air nm", 6562.8518 / 10.0)
lv = lam_vac(2, 3)
P("  this model air nm", lv / n_air_edlen1966(lv * 1e-3))
P("  residual / observed", (lv / n_air_edlen1966(lv * 1e-3) - 656.28518) / 656.28518)
P("H-alpha NIST component spread, nm", (6562.8518 - 6562.7110) / 10.0)
P("n_air at H-alpha vacuum (Edlen 1966)", n_air_edlen1966(lam_vac(2, 3) * 1e-3))
P("lambda_air(3->2) nm", lam_vac(2, 3) / n_air_edlen1966(lam_vac(2, 3) * 1e-3))
P("n_air at 400 nm", n_air_edlen1966(0.4))
P("n_air at 700 nm", n_air_edlen1966(0.7))
P("Lyman-alpha NIST components, vacuum nm", (121.566824, 121.567364))
P("  this model vacuum nm", lam_vac(1, 2))
P("  residual / observed (vs the stronger)", (lam_vac(1, 2) - 121.566824) / 121.566824)
P("fine-structure splitting scale at n=2: alpha^2 E_2 (eV)", alpha ** 2 * RH_eV / 4)
P("  as a fraction of the H-alpha photon energy", alpha ** 2 * RH_eV / 4 / (RH_eV * (1 / 4 - 1 / 9)))
P("  in nm at H-alpha", lam_vac(2, 3) * alpha ** 2 * RH_eV / 4 / (RH_eV * (1 / 4 - 1 / 9)))

# ======================================================================
# 8.  the spectrometer / series layout the sim draws
# ======================================================================
H("8. series layout")
for n1 in range(1, 6):
    lo = lam_vac(n1, n1 + 1)
    hi = 1e9 / (RH / n1 ** 2)
    P("%s series: longest nm" % SERIES[n1], lo)
    P("  limit nm", hi)
P("visible window 380-750 nm", "Balmer lines inside:")
for n2 in range(3, 13):
    lv = lam_vac(2, n2)
    if 380 <= lv <= 750:
        P("  Balmer %d->2 nm" % n2, lv)

# ======================================================================
# 9.  the seeded cascade — the ensemble the JS must reproduce exactly
# ======================================================================
H("9. seeded cascades (mulberry32); the JS runs the identical algorithm")


class RNG(object):
    def __init__(self, seed):
        self.a = seed & M32

    def next(self):
        self.a = (self.a + 0x6D2B79F5) & M32
        t = imul32(self.a ^ (self.a >> 15), 1 | self.a)
        t = ((t + imul32(t ^ (t >> 7), 61 | t)) & M32) ^ t
        return ((t ^ (t >> 14)) & M32) / 4294967296.0

    def int_below(self, k):
        return min(k - 1, int(self.next() * k))

    def weighted(self, items):
        """items = [(value, weight)]; PhET's chooseWeightedValue, cumulative."""
        tot = sum(w for _, w in items)
        if tot <= 0:
            return None
        r = self.next()
        acc = 0.0
        for v, w in items:
            acc += w / tot
            if r <= acc:
                return v
        return items[-1][0]


def cascade_bohr(rng, n):
    """PhET's Bohr: the lower n is uniform on 1..n-1.  Returns the list of
    (n_from, n_to) hops down to the ground state."""
    hops = []
    while n > 1:
        nl = 1 + rng.int_below(n - 1)
        hops.append((n, nl))
        n = nl
    return hops


def cascade_schrodinger(rng, n, l, m):
    """PhET's Schrodinger: chooseLower_n on the weight table, then choose_l and
    choose_m, with the (1,0,0) fallback.  A 2s state is a dead end (metastable)
    and the walk stops there."""
    hops = []
    guard = 0
    while guard < 200:
        guard += 1
        d = phet_choose_lower_n_dist(n, l)
        if not d:
            break
        nn = rng.weighted(sorted(d.items()))
        lp = rng.weighted(phet_choose_l_list(l, nn))
        mp = rng.weighted(phet_choose_m_list(m, lp))
        ok = (valid_state(n, l, m) and valid_state(nn, lp, mp) and n != nn
              and abs(l - lp) == 1 and abs(m - mp) <= 1)
        if not ok:
            nn, lp, mp = 1, 0, 0
        hops.append((n, nn))
        n, l, m = nn, lp, mp
        if n == 1:
            break
    return hops


for start in (6, 5, 4, 3, 2):
    rng = RNG(20260921)
    counts = {}
    TR = 40000
    hops_tot = 0
    for _ in range(TR):
        for (a, b) in cascade_bohr(rng, start):
            counts[(b, a)] = counts.get((b, a), 0) + 1
            hops_tot += 1
    P("Bohr cascade from n=%d, %d trials, hops" % (start, TR), hops_tot)
    P("  mean hops per cascade", hops_tot / TR)
    for k in sorted(counts):
        P("  emissions %d->%d" % (k[1], k[0]), counts[k])
    P("  Balmer (->2) fraction of all", sum(v for k, v in counts.items() if k[0] == 2) / hops_tot)
    P("  Lyman  (->1) fraction of all", sum(v for k, v in counts.items() if k[0] == 1) / hops_tot)

for (n0, l0, m0) in [(6, 1, 0), (5, 2, 1), (4, 3, -2), (3, 0, 0)]:
    rng = RNG(777)
    counts = {}
    TR = 40000
    hops_tot = 0
    stuck = 0
    for _ in range(TR):
        hs = cascade_schrodinger(rng, n0, l0, m0)
        for (a, b) in hs:
            counts[(b, a)] = counts.get((b, a), 0) + 1
            hops_tot += 1
        if not hs or hs[-1][1] != 1:
            stuck += 1
    P("Schrodinger cascade from (%d,%d,%d), %d trials, hops" % (n0, l0, m0, TR), hops_tot)
    P("  mean hops per cascade", hops_tot / TR)
    P("  cascades that did not reach n=1 (metastable 2s)", stuck)
    for k in sorted(counts):
        P("  emissions %d->%d" % (k[1], k[0]), counts[k])

H("9b. the first hop matches the exact distribution")
for (n0, l0) in [(3, 1), (4, 1), (5, 1), (6, 1)]:
    exact = phet_choose_lower_n_dist(n0, l0)
    rng = RNG(31415)
    TR = 200000
    hist = {}
    for _ in range(TR):
        nn = rng.weighted(sorted(exact.items()))
        hist[nn] = hist.get(nn, 0) + 1
    for k in sorted(exact):
        f = hist.get(k, 0) / TR
        se = math.sqrt(exact[k] * (1 - exact[k]) / TR)
        P("(n=%d,l=%d) -> n'=%d: measured, exact, z" % (n0, l0, k),
          (round(f, 8), round(exact[k], 8), round((f - exact[k]) / se, 4)))

H("9c. Bohr uniform lower-n: measured vs 1/(n-1)")
for n0 in (3, 4, 5, 6):
    rng = RNG(2718)
    TR = 200000
    hist = {}
    for _ in range(TR):
        nl = 1 + rng.int_below(n0 - 1)
        hist[nl] = hist.get(nl, 0) + 1
    for k in sorted(hist):
        f = hist[k] / TR
        p = 1.0 / (n0 - 1)
        se = math.sqrt(p * (1 - p) / TR)
        P("Bohr n=%d -> n'=%d: measured, exact, z" % (n0, k),
          (round(f, 8), round(p, 8), round((f - p) / se, 4)))

print("\n%d reference lines" % len(OUT), file=sys.stderr)
