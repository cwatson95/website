#!/usr/bin/env python3
"""derive.py — the Python twin of bending-light.html.

Re-derives, independently of the JavaScript, every closed form the sim
implements, and prints reference values to 15 significant figures for
selfTest() to assert against.  Nothing here is copied from PhET; the two
places where PhET's *model* is followed (its dispersion blend and its
s-polarised Fresnel powers) are written out from the formulas read out of the
minified build and are marked as such.

    python3 derive.py > refvals.txt 2> derive_err.txt

Sections
  1  dispersion        Sellmeier (BK7) + Edlen air + PhET's linear blend
  2  Snell             both directions, the critical angle, round trips
  3  Fresnel           s and p, R + T = 1, Brewster, past the critical angle
  4  the wave          lambda/n, c/n, phase matching, field continuity
  5  the prism         exact polygon/circle ray tracing, minimum deviation
  6  the rainbow       Descartes' stationary deviation, dispersion, Fresnel
  7  colour            CIE 1931 chromaticity of the wavelengths used
"""
import io
import math
import os
import re
import sys

import numpy as np
from scipy.optimize import brentq, minimize_scalar

OUT = []


def say(s=""):
    OUT.append(s)
    print(s)


def val(name, x, digits=15):
    if isinstance(x, (list, tuple, np.ndarray)):
        say("%-52s %s" % (name, " ".join("%.*g" % (digits, float(v)) for v in x)))
    else:
        say("%-52s %.*g" % (name, digits, float(x)))


# ====================================================================== #
#  1. dispersion                                                         #
# ====================================================================== #
# Schott BK7 Sellmeier coefficients (the standard published set; PhET's
# DispersionFunction.getSellmeierValue carries exactly these, with the C in
# square metres).  lambda in metres.
B_BK7 = (1.03961212, 0.231792344, 1.01046945)
C_BK7 = (6.00069867e-15, 2.00179144e-14, 1.03560653e-10)   # m^2  (= 0.00600069867, 0.0200179144, 103.560653 um^2)

# Edlen-type dispersion of standard air (15 C, 101.325 kPa, dry, 0.03% CO2).
# n - 1 = A1/(K1 - sigma^2) + A2/(K2 - sigma^2), sigma = 1/lambda[um].
AIR_A = (0.05792105, 0.00167917)
AIR_K = (238.0185, 57.362)

LAM_RED = 650e-9          # PhET's WAVELENGTH_RED, the reference wavelength
C_LIGHT = 299792458.0     # PhET's SPEED_OF_LIGHT, m/s


def sellmeier(lam):
    """BK7 index at wavelength lam (metres)."""
    l2 = lam * lam
    s = 1.0
    for b, c in zip(B_BK7, C_BK7):
        s += b * l2 / (l2 - c)
    return math.sqrt(s)


def air_index(lam):
    """Standard-air index at wavelength lam (metres)."""
    sig2 = (lam * 1e6) ** -2          # 1/lambda[um]^2
    return 1.0 + AIR_A[0] / (AIR_K[0] - sig2) + AIR_A[1] / (AIR_K[1] - sig2)


def blend_fraction(n_ref, lam_ref=LAM_RED):
    """PhET's linear blend weight: how much of BK7's dispersion this substance
    carries.  Clamped at zero from below, exactly as PhET clamps it."""
    a = air_index(lam_ref)
    s = (n_ref - a) / (sellmeier(lam_ref) - a)
    return max(s, 0.0)


def index_of(n_ref, lam, lam_ref=LAM_RED):
    """PhET's DispersionFunction: a substance named by its index at 650 nm has
    the dispersion of BK7 and air blended so that it passes through n_ref
    there."""
    s = blend_fraction(n_ref, lam_ref)
    return s * sellmeier(lam) + (1.0 - s) * air_index(lam)


SUBSTANCES = [("air", 1.000293), ("water", 1.333), ("glass", 1.5),
              ("diamond", 2.419), ("mysteryA", 2.419), ("mysteryB", 1.4)]

say("=" * 70)
say("1. DISPERSION  —  Sellmeier (BK7) + Edlen air + PhET's blend")
say("=" * 70)
val("sellmeier(650 nm)  [BK7]", sellmeier(650e-9))
val("sellmeier(587.5618 nm)  [BK7 n_d]", sellmeier(587.5618e-9))
val("sellmeier(486.1327 nm)  [BK7 n_F]", sellmeier(486.1327e-9))
val("sellmeier(656.2725 nm)  [BK7 n_C]", sellmeier(656.2725e-9))
nd = sellmeier(587.5618e-9)
nF = sellmeier(486.1327e-9)
nC = sellmeier(656.2725e-9)
val("BK7 Abbe number (n_d-1)/(n_F-n_C)", (nd - 1) / (nF - nC))
say("   published SCHOTT N-BK7: n_d = 1.5168, V_d = 64.17 — the fit reproduces both")
val("air_index(650 nm)", air_index(650e-9))
val("air_index(589.3 nm)", air_index(589.3e-9))
val("air_index(400 nm)", air_index(400e-9))
say("   published standard-air index at 589.3 nm: 1.0002765 (Edlen 1966)")
say()
for name, nref in SUBSTANCES:
    val("blend fraction s  [%s]" % name, blend_fraction(nref))
say()
LAM_LIST = [380, 400, 450, 500, 550, 600, 650, 700]
for name, nref in SUBSTANCES:
    row = [index_of(nref, l * 1e-9) for l in LAM_LIST]
    val("n(%s) at 380..700 nm" % name, row, 15)
say()
say("   identity: n(lambda_ref) = n_ref exactly, for every substance")
for name, nref in SUBSTANCES:
    val("n(%s, 650 nm) - n_ref" % name, index_of(nref, LAM_RED) - nref)
say()
val("water n(400) - n(700)  [dispersion span]",
    index_of(1.333, 400e-9) - index_of(1.333, 700e-9))
val("glass n(400) - n(700)", index_of(1.5, 400e-9) - index_of(1.5, 700e-9))
val("diamond n(400) - n(700)", index_of(2.419, 400e-9) - index_of(2.419, 700e-9))


# ====================================================================== #
#  2. Snell's law                                                        #
# ====================================================================== #
def refract_angle(n1, n2, th1):
    """theta_2, or None under total internal reflection."""
    s = n1 * math.sin(th1) / n2
    if abs(s) > 1.0:
        return None
    return math.asin(s)


def critical_angle(n1, n2):
    """The angle past which there is no transmitted ray, or None."""
    if n2 >= n1:
        return None
    return math.asin(n2 / n1)


say()
say("=" * 70)
say("2. SNELL'S LAW  —  n1 sin(th1) = n2 sin(th2)")
say("=" * 70)
PAIRS = [("air->water", 1.000293, 1.333), ("water->air", 1.333, 1.000293),
         ("air->glass", 1.000293, 1.5), ("glass->air", 1.5, 1.000293),
         ("air->diamond", 1.000293, 2.419), ("diamond->air", 2.419, 1.000293),
         ("water->glass", 1.333, 1.5), ("glass->water", 1.5, 1.333)]
TH_LIST = [0.0, 5.0, 15.0, 30.0, 45.0, 60.0, 75.0, 89.0]
for name, n1, n2 in PAIRS:
    row = []
    for t in TH_LIST:
        r = refract_angle(n1, n2, math.radians(t))
        row.append(math.degrees(r) if r is not None else float("nan"))
    val("theta2(deg) %s at 0,5,15,30,45,60,75,89" % name, row)
say()
for name, n1, n2 in PAIRS:
    tc = critical_angle(n1, n2)
    val("critical angle (deg) %s" % name, math.degrees(tc) if tc else float("nan"))
say()
say("   at the critical angle itself the refracted ray grazes: theta2 = 90 deg exactly")
for name, n1, n2 in PAIRS:
    tc = critical_angle(n1, n2)
    if tc is None:
        continue
    r = refract_angle(n1, n2, tc)
    val("theta2(theta_c) - 90 deg  [%s]" % name, math.degrees(r) - 90.0)
say()
say("   round trip: refract there and back returns the original angle")
for name, n1, n2 in PAIRS:
    worst = 0.0
    for t in TH_LIST:
        a = refract_angle(n1, n2, math.radians(t))
        if a is None:
            continue
        b = refract_angle(n2, n1, a)
        worst = max(worst, abs(b - math.radians(t)))
    val("worst round-trip residual (rad) [%s]" % name, worst)
say()
say("   the small-angle limit: theta2 -> (n1/n2) theta1, with an O(theta^3) departure")
for th in (1e-4, 1e-3, 1e-2, 1e-1):
    a = refract_angle(1.0, 1.5, th)
    val("  [n1=1,n2=1.5] (theta2 - theta1/1.5)/theta1^3 at %g" % th,
        (a - th / 1.5) / th ** 3)
say("   the exact third-order coefficient is (r - r^3)/6 with r = n1/n2:")
r_ = 1.0 / 1.5
val("  (r - r^3)/6", (r_ - r_ ** 3) / 6.0)


# ====================================================================== #
#  3. Fresnel                                                            #
# ====================================================================== #
def fresnel(n1, n2, th1):
    """Amplitude and power coefficients for s and p polarisation.

    Past the critical angle cos(theta2) is imaginary, |r| = 1 and nothing is
    transmitted; the phase of r is the Goos-Hanchen phase and is returned too.
    """
    c1 = math.cos(th1)
    s2 = n1 * math.sin(th1) / n2
    if abs(s2) <= 1.0:
        c2 = math.sqrt(max(0.0, 1.0 - s2 * s2))
        rs = (n1 * c1 - n2 * c2) / (n1 * c1 + n2 * c2)
        rp = (n2 * c1 - n1 * c2) / (n2 * c1 + n1 * c2)
        ts = 2 * n1 * c1 / (n1 * c1 + n2 * c2)
        tp = 2 * n1 * c1 / (n2 * c1 + n1 * c2)
        Rs, Rp = rs * rs, rp * rp
        # transmitted power = (n2 cos2)/(n1 cos1) |t|^2
        k = (n2 * c2) / (n1 * c1) if c1 > 0 else 0.0
        Ts, Tp = k * ts * ts, k * tp * tp
        return dict(rs=rs, rp=rp, ts=ts, tp=tp, Rs=Rs, Rp=Rp, Ts=Ts, Tp=Tp,
                    th2=math.asin(s2), tir=False, phs=0.0, php=0.0)
    # total internal reflection: c2 = i*g
    g = math.sqrt(s2 * s2 - 1.0)
    phs = -2.0 * math.atan2(n2 * g, n1 * c1)
    php = -2.0 * math.atan2(n1 * g, n2 * c1)
    return dict(rs=1.0, rp=1.0, ts=0.0, tp=0.0, Rs=1.0, Rp=1.0, Ts=0.0, Tp=0.0,
                th2=None, tir=True, phs=phs, php=php)


def brewster(n1, n2):
    return math.atan2(n2, n1)


say()
say("=" * 70)
say("3. FRESNEL  —  s and p, R + T = 1, Brewster, past the critical angle")
say("=" * 70)
for name, n1, n2 in PAIRS:
    f = fresnel(n1, n2, 0.0)
    val("R at normal incidence [%s]" % name, f["Rs"])
    val("  ((n1-n2)/(n1+n2))^2, independently", ((n1 - n2) / (n1 + n2)) ** 2)
say()
FR_ANGLES = [0.0, 10.0, 30.0, 45.0, 56.0, 60.0, 75.0, 85.0, 89.9]
for name, n1, n2 in PAIRS[:6]:
    rs = [fresnel(n1, n2, math.radians(t))["Rs"] for t in FR_ANGLES]
    rp = [fresnel(n1, n2, math.radians(t))["Rp"] for t in FR_ANGLES]
    val("R_s [%s] at %s" % (name, FR_ANGLES), rs)
    val("R_p [%s]" % name, rp)
say()
say("   R + T = 1 exactly, at every angle, in both polarisations")
worst_s = worst_p = 0.0
for name, n1, n2 in PAIRS:
    for t in np.linspace(0.0, 89.999, 601):
        f = fresnel(n1, n2, math.radians(t))
        worst_s = max(worst_s, abs(f["Rs"] + f["Ts"] - 1.0))
        worst_p = max(worst_p, abs(f["Rp"] + f["Tp"] - 1.0))
val("worst |R_s + T_s - 1| over 8 pairs x 601 angles", worst_s)
val("worst |R_p + T_p - 1| over 8 pairs x 601 angles", worst_p)
say()
say("   Brewster's angle: R_p = 0 there, and only there")
for name, n1, n2 in PAIRS:
    tb = brewster(n1, n2)
    val("Brewster angle (deg) [%s]" % name, math.degrees(tb))
    val("  R_p at Brewster", fresnel(n1, n2, tb)["Rp"])
    val("  R_s at Brewster", fresnel(n1, n2, tb)["Rs"])
say()
say("   Brewster + refracted = 90 deg exactly (the dipole argument)")
for name, n1, n2 in PAIRS:
    tb = brewster(n1, n2)
    t2 = refract_angle(n1, n2, tb)
    val("theta_B + theta_2 - 90 deg [%s]" % name, math.degrees(tb + t2) - 90.0)
say()
say("   past the critical angle: R = 1 exactly in both polarisations")
for name, n1, n2 in PAIRS:
    tc = critical_angle(n1, n2)
    if tc is None:
        continue
    for extra in (1e-9, 0.01, 0.2):
        th = tc + extra
        if th >= math.pi / 2:
            continue
        f = fresnel(n1, n2, th)
        val("R_s, R_p at theta_c + %g [%s]" % (extra, name), [f["Rs"], f["Rp"]])
say()
say("   AT the critical angle R = 1 too (grazing emergence carries no power)")
for name, n1, n2 in PAIRS:
    tc = critical_angle(n1, n2)
    if tc is None:
        continue
    f = fresnel(n1, n2, tc)
    val("R_s, R_p, T_s, T_p at theta_c [%s]" % name,
        [f["Rs"], f["Rp"], f["Ts"], f["Tp"]])
say()
say("   grazing incidence: R -> 1 from below in both polarisations")
for name, n1, n2 in PAIRS[:4]:
    f = fresnel(n1, n2, math.radians(89.999))
    val("R_s, R_p at 89.999 deg [%s]" % name, [f["Rs"], f["Rp"]])
say()
say("   the unpolarised average, and PhET's own choice (it shows R_s alone)")
for t in (0.0, 30.0, 45.0, 60.0):
    f = fresnel(1.000293, 1.333, math.radians(t))
    val("air->water at %g deg: R_s, R_p, (R_s+R_p)/2" % t,
        [f["Rs"], f["Rp"], 0.5 * (f["Rs"] + f["Rp"])])
say()
say("   the total-internal-reflection phase (Goos-Hanchen), glass->air")
for t in (45.0, 60.0, 80.0):
    f = fresnel(1.5, 1.000293, math.radians(t))
    if f["tir"]:
        val("phase of r_s, r_p at %g deg (rad)" % t, [f["phs"], f["php"]])


# ====================================================================== #
#  4. the wave                                                           #
# ====================================================================== #
say()
say("=" * 70)
say("4. THE WAVE  —  lambda/n, c/n, phase matching, field continuity")
say("=" * 70)
for name, nref in SUBSTANCES:
    n = index_of(nref, LAM_RED)
    val("650 nm in %s: lambda (nm), v/c, v (m/s)" % name,
        [650.0 / n, 1.0 / n, C_LIGHT / n])
say()
val("frequency of 650 nm light (Hz)", C_LIGHT / LAM_RED)
say("   the frequency is the same on both sides; only lambda and v change")
say()
say("   phase matching: the crest spacing ALONG the boundary is equal on both")
say("   sides, lambda1/sin th1 = lambda2/sin th2 — which IS Snell's law")
worst = 0.0
for name, n1, n2 in PAIRS:
    for t in (5.0, 20.0, 40.0, 60.0, 80.0):
        th1 = math.radians(t)
        th2 = refract_angle(n1, n2, th1)
        if th2 is None:
            continue
        l1, l2 = 650.0 / n1, 650.0 / n2
        worst = max(worst, abs(l1 / math.sin(th1) - l2 / math.sin(th2)) / (l1 / math.sin(th1)))
val("worst relative crest-spacing mismatch", worst)
say()
say("   s-polarised field continuity across the boundary, exactly:")
say("     E tangential:  1 + r_s = t_s")
say("     H tangential:  n1 cos th1 (1 - r_s) = n2 cos th2 t_s")
we = wh = 0.0
for name, n1, n2 in PAIRS:
    for t in np.linspace(0.0, 85.0, 86):
        f = fresnel(n1, n2, math.radians(t))
        if f["tir"]:
            continue
        we = max(we, abs(1.0 + f["rs"] - f["ts"]))
        c1, c2 = math.cos(math.radians(t)), math.cos(f["th2"])
        wh = max(wh, abs(n1 * c1 * (1 - f["rs"]) - n2 * c2 * f["ts"]))
val("worst |1 + r_s - t_s|", we)
val("worst H-continuity residual", wh)
say()
say("   THE WORLD'S WAVENUMBER.  One world unit is one RED wavelength in vacuum,")
say("   so a wave of vacuum wavelength lam has k0 = 2 pi (650/lam) per unit.")
say("   At 650 nm that is 2 pi whichever way round the ratio is written, which")
say("   is why every assertion taken there is blind to it.")
for lam in (380.0, 400.0, 500.0, 650.0, 700.0):
    val("k0 per world unit at %g nm" % lam, 2 * math.pi * 650.0 / lam)
say()
say("   the standing-wave fringe period in y is pi/(k0 n1 cos th1), in world units")
for name, n1, n2, tdeg, lam in (("air->water 45 deg, 650 nm", 1.000293, 1.333, 45.0, 650.0),
                                ("air->water 45 deg, 400 nm", 1.000293, 1.333, 45.0, 400.0),
                                ("glass->air 70 deg, 500 nm", 1.5, 1.000293, 70.0, 500.0)):
    k0 = 2 * math.pi * 650.0 / lam
    n1l = index_of(n1, lam * 1e-9)
    val("fringe period (world units) [%s]" % name,
        math.pi / (k0 * n1l * math.cos(math.radians(tdeg))))
say()
say("   the crest spacing ALONG the boundary, in world units: 2 pi/k_x with")
say("   k_x = k0 n1 sin th1")
for name, n1, tdeg, lam in (("air 45 deg, 650 nm", 1.000293, 45.0, 650.0),
                            ("air 45 deg, 400 nm", 1.000293, 45.0, 400.0),
                            ("glass 70 deg, 500 nm", 1.5, 70.0, 500.0)):
    k0 = 2 * math.pi * 650.0 / lam
    n1l = index_of(n1, lam * 1e-9)
    val("crest spacing (world units) [%s]" % name,
        2 * math.pi / (k0 * n1l * math.sin(math.radians(tdeg))))
say()
say("   THE EVANESCENT DECAY CONSTANT, past the critical angle:")
say("     kappa = k0 sqrt(n1^2 sin^2 th1 - n2^2),  1/kappa in nanometres")
for name, n1r, n2r in (("glass->air", 1.5, 1.000293), ("water->air", 1.333, 1.000293),
                       ("diamond->air", 2.419, 1.000293)):
    for lam in (650.0, 450.0):
        n1l, n2l = index_of(n1r, lam * 1e-9), index_of(n2r, lam * 1e-9)
        tc = critical_angle(n1l, n2l)
        row, rowlen = [], []
        for tdeg in (45.0, 60.0, 80.0):
            th = math.radians(tdeg)
            if th <= tc:
                row.append(float("nan"))
                rowlen.append(float("nan"))
                continue
            kap_over_k0 = math.sqrt((n1l * math.sin(th)) ** 2 - n2l * n2l)
            k0 = 2 * math.pi * 650.0 / lam
            row.append(kap_over_k0)
            # 1/kappa in nm: kappa = (2 pi/lam[nm]) * kap_over_k0
            rowlen.append(lam / (2 * math.pi * kap_over_k0))
        val("kappa/k0 at 45, 60, 80 deg [%s, %g nm]" % (name, lam), row)
        val("  1/kappa (nm)", rowlen)
say()
say("   and the same quantity as n2 sqrt(s2^2 - 1) with s2 = n1 sin th1/n2 --")
say("   the form the code uses -- agrees identically:")
worst_kap = 0.0
for n1r, n2r in ((1.5, 1.000293), (1.333, 1.000293), (2.419, 1.000293), (1.5, 1.333)):
    n1l, n2l = index_of(n1r, LAM_RED), index_of(n2r, LAM_RED)
    tc = critical_angle(n1l, n2l)
    for tdeg in np.linspace(math.degrees(tc) + 0.01, 89.9, 40):
        th = math.radians(tdeg)
        s2 = n1l * math.sin(th) / n2l
        worst_kap = max(worst_kap, abs(n2l * math.sqrt(s2 * s2 - 1)
                                       - math.sqrt((n1l * math.sin(th)) ** 2 - n2l * n2l)))
val("worst |n2 sqrt(s2^2-1) - sqrt(n1^2 sin^2 - n2^2)|", worst_kap)
say()
say("   BELOW the critical angle there is no decay at all: the transmitted")
say("   amplitude is the same at every depth, which is a contract the drawing")
say("   depends on and which no ratio of the field to itself can see.")
say()
say("   PhET's wave view refuses angles past MAX_ANGLE_IN_WAVE_MODE = 3.0194 rad")
val("3.0194 rad in degrees", math.degrees(3.0194))
val("  i.e. the laser stops this far from the boundary (deg)", 180 - math.degrees(3.0194))


# ====================================================================== #
#  5. the prism                                                          #
# ====================================================================== #
EPS = 1e-12


def poly_hit(p, d, pts):
    """Nearest forward hit of ray p + t d with a closed polygon.  Returns
    (t, normal) with the normal pointing OUT of the polygon (pts CCW)."""
    best_t, best_n = None, None
    m = len(pts)
    for i in range(m):
        a, b = pts[i], pts[(i + 1) % m]
        ex, ey = b[0] - a[0], b[1] - a[1]
        den = d[0] * ey - d[1] * ex
        if abs(den) < 1e-15:
            continue
        qx, qy = a[0] - p[0], a[1] - p[1]
        t = (qx * ey - qy * ex) / den
        u = (qx * d[1] - qy * d[0]) / den
        if t > 1e-9 and -1e-12 <= u <= 1 + 1e-12:
            if best_t is None or t < best_t:
                # CCW polygon: the outward normal of edge a->b is (ey, -ex)
                L = math.hypot(ex, ey)
                best_t, best_n = t, (ey / L, -ex / L)
    return best_t, best_n


def circle_hit(p, d, c, r, half=None):
    """Nearest forward hit with a circle of centre c, radius r.  If `half` is
    given it is a unit vector; only the arc with (hit-c).half > 0 counts."""
    ox, oy = p[0] - c[0], p[1] - c[1]
    a = d[0] * d[0] + d[1] * d[1]
    b = 2 * (ox * d[0] + oy * d[1])
    cc = ox * ox + oy * oy - r * r
    disc = b * b - 4 * a * cc
    if disc < 0:
        return None, None
    sq = math.sqrt(disc)
    # numerically stable roots
    q = -0.5 * (b + math.copysign(sq, b))
    roots = sorted([q / a, cc / q]) if abs(q) > 1e-300 else sorted([(-b - sq) / (2 * a), (-b + sq) / (2 * a)])
    for t in roots:
        if t > 1e-9:
            hx, hy = p[0] + t * d[0], p[1] + t * d[1]
            if half is not None and (hx - c[0]) * half[0] + (hy - c[1]) * half[1] <= 0:
                continue
            L = math.hypot(hx - c[0], hy - c[1])
            return t, ((hx - c[0]) / L, (hy - c[1]) / L)
    return None, None


def shape_hit(shape, p, d):
    if shape["kind"] == "poly":
        return poly_hit(p, d, shape["pts"])
    if shape["kind"] == "circle":
        return circle_hit(p, d, shape["c"], shape["r"])
    if shape["kind"] == "semi":
        # the flat face as a single segment, outward normal -half; the curved
        # face is the half of the circle on the `half` side
        t1, n1 = None, None
        ax, ay = shape["a"]
        bx, by = shape["b"]
        ex, ey = bx - ax, by - ay
        den = d[0] * ey - d[1] * ex
        if abs(den) > 1e-15:
            qx, qy = ax - p[0], ay - p[1]
            t = (qx * ey - qy * ex) / den
            u = (qx * d[1] - qy * d[0]) / den
            if t > 1e-9 and -1e-12 <= u <= 1 + 1e-12:
                t1, n1 = t, (-shape["half"][0], -shape["half"][1])
        t2, n2 = circle_hit(p, d, shape["c"], shape["r"], shape["half"])
        if t1 is None:
            return t2, n2
        if t2 is None:
            return t1, n1
        return (t1, n1) if t1 < t2 else (t2, n2)
    raise ValueError(shape["kind"])


def inside(shape, p):
    if shape["kind"] == "poly":
        pts, c = shape["pts"], 0
        m = len(pts)
        for i in range(m):
            a, b = pts[i], pts[(i + 1) % m]
            if (a[1] > p[1]) != (b[1] > p[1]):
                x = a[0] + (p[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
                if x > p[0]:
                    c += 1
        return c % 2 == 1
    if shape["kind"] == "circle":
        return math.hypot(p[0] - shape["c"][0], p[1] - shape["c"][1]) < shape["r"]
    if shape["kind"] == "semi":
        dx, dy = p[0] - shape["c"][0], p[1] - shape["c"][1]
        return math.hypot(dx, dy) < shape["r"] and dx * shape["half"][0] + dy * shape["half"][1] > 0
    raise ValueError(shape["kind"])


def vec_refract(d, nrm, n1, n2):
    """Vector Snell.  `nrm` points out of the medium the ray is leaving side of;
    returns the unit transmitted direction, or None under TIR."""
    eta = n1 / n2
    ci = -(d[0] * nrm[0] + d[1] * nrm[1])
    k = 1.0 - eta * eta * (1.0 - ci * ci)
    if k < 0.0:
        return None
    s = eta * ci - math.sqrt(k)
    return (eta * d[0] + s * nrm[0], eta * d[1] + s * nrm[1])


def vec_reflect(d, nrm):
    dn = d[0] * nrm[0] + d[1] * nrm[1]
    return (d[0] - 2 * dn * nrm[0], d[1] - 2 * dn * nrm[1])


def trace(shape, p, d, n_out, n_in, max_steps=50, power_min=0.001,
          reflections=True, reach=40.0):
    """Trace one ray through one shape.  Returns the list of segments
    [(x0,y0,x1,y1,power)], the exit direction of the strongest branch, and the
    total optical path length of the primary branch."""
    segs = []
    stack = [(p, d, 1.0, inside(shape, p), 0, True)]
    exit_dir, exit_pt, primary_path = None, None, 0.0
    steps = 0
    while stack and steps < max_steps:
        steps += 1
        pos, dir_, pw, ins, depth, primary = stack.pop(0)
        if pw < power_min or depth > 12:
            continue
        t, nrm = shape_hit(shape, pos, dir_)
        if t is None:
            end = (pos[0] + reach * dir_[0], pos[1] + reach * dir_[1])
            segs.append((pos[0], pos[1], end[0], end[1], pw))
            if primary and exit_dir is None:
                exit_dir, exit_pt = dir_, pos
            continue
        hit = (pos[0] + t * dir_[0], pos[1] + t * dir_[1])
        segs.append((pos[0], pos[1], hit[0], hit[1], pw))
        if primary:
            primary_path += t * (n_in if ins else n_out)
        n1 = n_in if ins else n_out
        n2 = n_out if ins else n_in
        # the surface normal must point back against the incoming ray
        nn = nrm if (dir_[0] * nrm[0] + dir_[1] * nrm[1]) < 0 else (-nrm[0], -nrm[1])
        cos1 = -(dir_[0] * nn[0] + dir_[1] * nn[1])
        th1 = math.acos(min(1.0, max(-1.0, cos1)))
        f = fresnel(n1, n2, th1)
        R = 0.5 * (f["Rs"] + f["Rp"])
        td = vec_refract(dir_, nn, n1, n2)
        rd = vec_reflect(dir_, nn)
        off = 1e-9
        if td is None:
            stack.append(((hit[0] + off * rd[0], hit[1] + off * rd[1]), rd, pw, ins, depth + 1, primary))
        else:
            stack.append(((hit[0] + off * td[0], hit[1] + off * td[1]), td, pw * (1 - R), not ins, depth + 1, primary))
            if reflections and pw * R >= power_min:
                stack.append(((hit[0] + off * rd[0], hit[1] + off * rd[1]), rd, pw * R, ins, depth + 1, False))
    return segs, exit_dir, exit_pt, primary_path, steps


T_CHAR = 10 * LAM_RED / LAM_RED     # PhET's prisms are 10 red wavelengths across;
# the sim works in units of the red wavelength, so t = 10 in those units.
T_UNIT = 10.0
R_UNIT = T_UNIT / 2


def prism_shapes():
    t, i_ = T_UNIT, R_UNIT
    return {
        "triangle": dict(kind="poly", pts=[(-t / 2, -t / (2 * math.sqrt(3))),
                                           (t / 2, -t / (2 * math.sqrt(3))),
                                           (0.0, t / math.sqrt(3))]),
        "trapezoid": dict(kind="poly", pts=[(-t / 2, -t * math.sqrt(3) / 4),
                                            (t / 2, -t * math.sqrt(3) / 4),
                                            (t / 4, t * math.sqrt(3) / 4),
                                            (-t / 4, t * math.sqrt(3) / 4)]),
        "square": dict(kind="poly", pts=[(-t / 2, -t / 2), (t / 2, -t / 2),
                                         (t / 2, t / 2), (-t / 2, t / 2)]),
        "circle": dict(kind="circle", c=(0.0, 0.0), r=i_),
        "semicircle": dict(kind="semi", c=(0.0, 0.0), r=i_, a=(0.0, -i_), b=(0.0, i_),
                           half=(-1.0, 0.0)),
    }


say()
say("=" * 70)
say("5. THE PRISM  —  exact polygon/circle tracing, and minimum deviation")
say("=" * 70)
say("   PhET's prism prototypes, in units of the red wavelength (t = 10):")
SH = prism_shapes()
for k in ("triangle", "trapezoid", "square"):
    say("     %-10s %s" % (k, ["(%.12g, %.12g)" % p for p in SH[k]["pts"]]))
say("     circle     centre (0,0)  r = %.12g" % R_UNIT)
say("     semicircle flat face on x = 0, curved half on x < 0, r = %.12g" % R_UNIT)
say()
say("   an equilateral prism: the exact minimum-deviation law")
say("     n = sin((A + D_min)/2) / sin(A/2)      A = 60 deg")


def prism_deviation(n1, n2, A, th1):
    """Deviation of a ray through a prism of apex angle A, entering at th1."""
    r1 = math.asin(n1 * math.sin(th1) / n2)
    r2 = A - r1
    s = n2 * math.sin(r2) / n1
    if abs(s) > 1:
        return None
    th2 = math.asin(s)
    return th1 + th2 - A


A60 = math.radians(60.0)
for name, nref in (("glass", 1.5), ("water", 1.333), ("diamond", 2.419)):
    n2 = index_of(nref, LAM_RED)
    n1 = index_of(1.000293, LAM_RED)
    arg = n2 / n1 * math.sin(A60 / 2)
    if abs(arg) > 1.0:
        val("D_min [%s]: no symmetric passage, sin((A+D)/2) would be" % name, arg)
        say("     a 60 deg prism of this index traps the ray: the maximum apex")
        say("     angle that transmits is 2 theta_c =")
        val("  2 theta_c (deg) [%s]" % name, 2 * math.degrees(critical_angle(n2, n1)))
        continue
    Dmin_closed = 2 * math.asin(arg) - A60
    # independent: minimise the deviation numerically
    lo = math.degrees(math.asin(max(-1.0, min(1.0, n2 / n1 * math.sin(A60 - math.asin(min(1.0, n1 / n2)))))))
    res = minimize_scalar(lambda t: prism_deviation(n1, n2, A60, t),
                          bounds=(math.radians(25), math.radians(85)), method="bounded",
                          options={"xatol": 1e-14})
    val("D_min (deg) [%s] closed form" % name, math.degrees(Dmin_closed))
    val("  minimize_scalar", math.degrees(res.fun))
    val("  theta1 at minimum (deg)", math.degrees(res.x))
    val("  symmetric-passage theta1 (deg)", math.degrees((A60 + Dmin_closed) / 2))
say()
say("   the traced ray must reproduce it: trace a ray through the triangle at")
say("   the symmetric angle and measure its deviation")


def trace_triangle_deviation(n_env, n_pr, th1):
    """Enter the left face of PhET's equilateral triangle at th1 and return the
    deviation of the emergent ray, by tracing."""
    tri = SH["triangle"]
    pts = tri["pts"]
    # left face runs from the apex (0, t/sqrt3) down to (-t/2, -t/(2 sqrt3))
    apex, bl = pts[2], pts[0]
    mid = (0.5 * (apex[0] + bl[0]), 0.5 * (apex[1] + bl[1]))
    ex, ey = bl[0] - apex[0], bl[1] - apex[1]
    L = math.hypot(ex, ey)
    out = (ey / L, -ex / L)          # outward normal of a CCW polygon's edge
    # an incoming direction making th1 with the INWARD normal
    inw = (-out[0], -out[1])
    ca, sa = math.cos(th1), math.sin(th1)
    d = (inw[0] * ca - inw[1] * sa, inw[0] * sa + inw[1] * ca)
    start = (mid[0] - 6 * d[0], mid[1] - 6 * d[1])
    segs, ed, ep, path, nst = trace(tri, start, d, n_env, n_pr, reflections=False)
    if ed is None:
        return None, segs
    dev = math.atan2(d[0] * ed[1] - d[1] * ed[0], d[0] * ed[0] + d[1] * ed[1])
    return abs(dev), segs


n_env = index_of(1.000293, LAM_RED)
for name, nref in (("glass", 1.5), ("water", 1.333)):
    n_pr = index_of(nref, LAM_RED)
    Dmin = 2 * math.asin(n_pr / n_env * math.sin(A60 / 2)) - A60
    th_sym = (A60 + Dmin) / 2
    dev, segs = trace_triangle_deviation(n_env, n_pr, th_sym)
    val("traced deviation at symmetric passage (deg) [%s]" % name, math.degrees(dev))
    val("  closed-form D_min (deg)", math.degrees(Dmin))
    val("  residual (deg)", math.degrees(dev - Dmin))
    val("  segments traced", len(segs))
say()
say("   and off the symmetric angle the traced deviation still matches the")
say("   two-surface closed form exactly")
for name, nref in (("glass", 1.5),):
    n_pr = index_of(nref, LAM_RED)
    for tdeg in (35.0, 45.0, 55.0, 65.0):
        th1 = math.radians(tdeg)
        dev, _ = trace_triangle_deviation(n_env, n_pr, th1)
        cf = prism_deviation(n_env, n_pr, A60, th1)
        val("theta1=%g: traced, closed form, residual (deg)" % tdeg,
            [math.degrees(dev), math.degrees(cf), math.degrees(dev - cf)])
say()
say("   dispersion through the triangle: the angular spread of white light")
for name, nref in (("glass", 1.5), ("water", 1.333), ("diamond", 2.419)):
    th1 = math.radians(45.0)
    devs = []
    for lam in (400.0, 650.0, 700.0):
        n_pr = index_of(nref, lam * 1e-9)
        ne = index_of(1.000293, lam * 1e-9)
        d = prism_deviation(ne, n_pr, A60, th1)
        devs.append(math.degrees(d) if d is not None else float("nan"))
    val("deviation at 400, 650, 700 nm (deg) [%s]" % name, devs)
    val("  violet - red spread (deg)", devs[0] - devs[2])
say()
say("   the circle: a ray through the centre is undeviated (the normal is radial)")
circ = SH["circle"]
segs, ed, ep, path, nst = trace(circ, (-9.0, 0.0), (1.0, 0.0), n_env,
                           index_of(1.5, LAM_RED), reflections=False)
val("exit direction through the centre of the circle", list(ed))
val("  segments", len(segs))
say()
say("   the square at 45 deg: enters the left face, and the exit ray is")
say("   PARALLEL to the incident one (a slab displaces, it does not deviate)")
sq = SH["square"]
th_in = math.radians(45.0)
d_in = (math.cos(-th_in), math.sin(-th_in))
segs, ed, ep, path, nst = trace(sq, (-12.0, 10.0), d_in, n_env,
                           index_of(1.5, LAM_RED), reflections=False)
if ed:
    ang = math.degrees(math.atan2(d_in[0] * ed[1] - d_in[1] * ed[0],
                                  d_in[0] * ed[0] + d_in[1] * ed[1]))
    val("slab: angle between entry and exit directions (deg)", ang)
    val("  segments", len(segs))
say()
say("   total internal reflection inside the triangle: a diamond prism traps")
say("   the ray (critical angle 24.4 deg against air, apex faces at 60 deg)")
n_dia = index_of(2.419, LAM_RED)
val("critical angle diamond->air (deg)", math.degrees(critical_angle(n_dia, n_env)))
dev_d, segs_d = trace_triangle_deviation(n_env, n_dia, math.radians(45.0))
val("diamond triangle at 45 deg: segments traced", len(segs_d))
val("  a 60 deg apex exceeds 2 theta_c = ", 2 * math.degrees(critical_angle(n_dia, n_env)))
say()
say("   the trapezoid and the semicircle draw and terminate")
for k in ("trapezoid", "semicircle"):
    segs, ed, ep, path, nst = trace(SH[k], (-14.0, 1.3), (1.0, -0.12), n_env,
                               index_of(1.5, LAM_RED), reflections=True)
    val("%s: segments, exit dir" % k, [len(segs)] + (list(ed) if ed else [float("nan")] * 2))
say()
say("   a ray aimed at the CENTRE of the semicircle crosses the curved face")
say("   undeviated (the normal there is radial) and meets the flat face at the")
say("   centre, where it refracts by Snell with the flat face's normal")
semi = SH["semicircle"]
n_gl = index_of(1.5, LAM_RED)
d_aim = (math.cos(math.radians(-20.0)), math.sin(math.radians(-20.0)))
start = (-12 * d_aim[0], -12 * d_aim[1])
segs, ed, ep, path, nst = trace(semi, start, d_aim, n_env, n_gl, reflections=False)
val("semicircle aimed at the centre: exit direction", list(ed))
val("  its angle to the x axis (deg)", math.degrees(math.atan2(ed[1], ed[0])))
val("  Snell at the flat face (normal +x): theta1, theta2 (deg)",
    [20.0, math.degrees(math.asin(n_gl * math.sin(math.radians(20.0)) / n_env))])
val("  segments", len(segs))
say()
say("   traced-ray reference values, for the JavaScript twin to reproduce")
REF_TRACES = [("triangle glass 45", "triangle", 1.5, (-12.0, 4.0), (0.9, -0.2)),
              ("square glass 30", "square", 1.5, (-12.0, 6.0), (0.95, -0.35)),
              ("circle water 0.3", "circle", 1.333, (-12.0, 2.2), (1.0, 0.0)),
              ("trapezoid glass", "trapezoid", 1.5, (-14.0, 1.3), (1.0, -0.12)),
              ("semicircle glass", "semicircle", 1.5, (-14.0, 1.3), (1.0, -0.12))]
for label, shname, nref, p0, d0 in REF_TRACES:
    L = math.hypot(d0[0], d0[1])
    d0u = (d0[0] / L, d0[1] / L)
    segs, ed, ep, path, nst = trace(SH[shname], p0, d0u, n_env, index_of(nref, LAM_RED),
                               reflections=True)
    tot = sum(math.hypot(s[2] - s[0], s[3] - s[1]) for s in segs)
    val("%s: nsegs, total drawn length, sum of powers" % label,
        [len(segs), tot, sum(s[4] for s in segs)])
    if ed:
        val("  exit direction", list(ed))
    val("  first three segment endpoints",
        [c for s in segs[:3] for c in s[:4]])
say()
say("   the same traces with the partial reflections switched off")
for label, shname, nref, p0, d0 in REF_TRACES:
    L = math.hypot(d0[0], d0[1])
    d0u = (d0[0] / L, d0[1] / L)
    segs, ed, ep, path, nst = trace(SH[shname], p0, d0u, n_env, index_of(nref, LAM_RED),
                               reflections=False)
    tot = sum(math.hypot(s[2] - s[0], s[3] - s[1]) for s in segs)
    val("%s: nsegs, total length" % label, [len(segs), tot])
say()
say("   a slab displaces the beam sideways by t sin(th1 - th2)/cos(th2)")
for tdeg in (20.0, 45.0, 70.0):
    th1 = math.radians(tdeg)
    n2 = index_of(1.5, LAM_RED)
    th2 = refract_angle(n_env, n2, th1)
    t_slab = T_UNIT
    val("slab offset at %g deg (units of t)" % tdeg,
        t_slab * math.sin(th1 - th2) / math.cos(th2))
    val("  theta2 (deg)", math.degrees(th2))
say()
say("   the busiest configuration the controls can reach, with the partial")
say("   reflections on: it must stay inside PhET's 50-step limit")
for label, shname, nref, p0, d0 in [("circle glass, y = 3, tilt 10 deg", "circle", 1.5,
                                     (-11.5, 3.0), (math.cos(math.radians(10)), math.sin(math.radians(10)))),
                                    ("square diamond, y = 1.3, tilt 18.5", "square", 2.419,
                                     (-11.5, 1.3), (math.cos(math.radians(18.5)), math.sin(math.radians(18.5))))]:
    segs, ed, ep, path, nst = trace(SH[shname], p0, d0, n_env, index_of(nref, LAM_RED),
                                    reflections=True, reach=46.0)
    tot = sum(math.hypot(g[2] - g[0], g[3] - g[1]) for g in segs)
    val("%s: steps, segments, total length" % label, [nst, len(segs), tot])
say()
say("   inside() agrees with a ray-parity test on all five shapes")
for k, sh in SH.items():
    pts_in = [(0.0, 0.0), (0.1, 0.1)]
    pts_out = [(20.0, 20.0), (-20.0, 0.0)]
    ok_in = all(inside(sh, p) for p in pts_in) if k != "semicircle" else \
        all(inside(sh, (-abs(p[0]) - 0.05, p[1])) for p in pts_in)
    ok_out = all(not inside(sh, p) for p in pts_out)
    say("     %-10s inside near centre: %s   outside far away: %s" % (k, ok_in, ok_out))


# ====================================================================== #
#  6. the rainbow                                                        #
# ====================================================================== #
say()
say("=" * 70)
say("6. THE RAINBOW  —  Descartes' stationary deviation")
say("=" * 70)
say("   k internal reflections: D(th) = 2 th - 2(k+1) asin(sin th / n) + k pi")
say("   dD/dth = 0  <=>  cos^2 th = (n^2 - 1)/(k^2 + 2k)")
say("   n here is the RELATIVE index n_water/n_air, which is what Snell's law")
say("   at the drop's surface actually carries")


def rain_dev(n, k, th):
    return 2 * th - 2 * (k + 1) * math.asin(math.sin(th) / n) + k * math.pi


def rain_theta(n, k):
    c2 = (n * n - 1.0) / (k * k + 2.0 * k)
    if c2 < 0 or c2 > 1:
        return None
    return math.acos(math.sqrt(c2))


say("   D is stationary (a minimum) for every k; the angular radius of the bow")
say("   about the antisolar point is |180 - D|")
def n_rel(lam_nm):
    return index_of(1.333, lam_nm * 1e-9) / index_of(1.000293, lam_nm * 1e-9)


val("relative index of water at 650 nm", n_rel(650.0))
for k in (1, 2, 3):
    n = n_rel(650.0)
    th = rain_theta(n, k)
    D = rain_dev(n, k, th)
    res = minimize_scalar(lambda t: rain_dev(n, k, t),
                          bounds=(1e-6, math.pi / 2 - 1e-6), method="bounded",
                          options={"xatol": 1e-14})
    val("k=%d: impact angle th_i (deg)" % k, math.degrees(th))
    val("  deviation D (deg)", math.degrees(D))
    val("  bow angular radius |180 - D| (deg)", abs(180.0 - math.degrees(D)))
    val("  numerical stationary th_i (deg)", math.degrees(res.x))
    val("  residual against the closed form (deg)", math.degrees(res.x - th))
    val("  dD/dth at the closed-form angle (finite difference)",
        (rain_dev(n, k, th + 1e-6) - rain_dev(n, k, th - 1e-6)) / 2e-6)
say()
say("   the primary bow at 650 nm and 400 nm — the colours of the bow")
for k, kn in ((1, "primary"), (2, "secondary")):
    row = []
    for lam in (400.0, 500.0, 600.0, 650.0, 700.0):
        n = n_rel(lam)
        th = rain_theta(n, k)
        D = rain_dev(n, k, th)
        row.append(abs(180.0 - math.degrees(D)))
    val("%s bow angle (deg) at 400,500,600,650,700 nm" % kn, row)
    val("  width violet->red (deg)", row[-1] - row[0])
say()
say("   Alexander's dark band lies between the two bows")
n = n_rel(650.0)
p1 = abs(180.0 - math.degrees(rain_dev(n, 1, rain_theta(n, 1))))
p2 = abs(math.degrees(rain_dev(n, 2, rain_theta(n, 2))) - 180.0)
val("primary, secondary, gap (deg)", [p1, p2, p2 - p1])
say()
say("   the Fresnel weight along the primary path: T(in) R(internal) T(out)")
n_w = index_of(1.333, LAM_RED)
th = rain_theta(n, 1)
f_in = fresnel(n_env, n_w, th)
th_r = math.asin(n_env * math.sin(th) / n_w)
f_int = fresnel(n_w, n_env, th_r)
w = 0.5 * (f_in["Ts"] + f_in["Tp"]) * 0.5 * (f_int["Rs"] + f_int["Rp"]) \
    * 0.5 * (f_int["Ts"] + f_int["Tp"])
val("primary-bow Fresnel throughput (unpolarised)", w)
val("  T at entry, R internal, T at exit",
    [0.5 * (f_in["Ts"] + f_in["Tp"]), 0.5 * (f_int["Rs"] + f_int["Rp"]),
     0.5 * (f_int["Ts"] + f_int["Tp"])])
say()
say("   the internal angle never reaches the critical angle, so the bow is")
say("   made by a PARTIAL reflection — that is why it is faint")
val("internal incidence (deg)", math.degrees(th_r))
val("critical angle water->air (deg)", math.degrees(critical_angle(n_w, n_env)))
say()
say("   s and p separately at the primary bow: the bow is strongly polarised")
val("R_s, R_p at the internal bounce", [f_int["Rs"], f_int["Rp"]])
val("Brewster angle water->air (deg)", math.degrees(brewster(n_w, n_env)))
say()
say("   TWO EXACT IDENTITIES at the stationary ray, worth more than the")
say("   numbers above because they hold for EVERY index:")
say("     the stationary condition is n cos th_r = (k+1) cos th_i, so at the")
say("     internal bounce n1 c1 = (k+1) n2 c2 and therefore")
say("       R_s = (k/(k+2))^2         (independent of n!)")
say("       R_p = (((k+1) - m^2)/((k+1) + m^2))^2 ,  m = n_water/n_air")
for k in (1, 2, 3):
    nr = n_rel(650.0)
    thk = rain_theta(nr, k)
    thrk = math.asin(n_env * math.sin(thk) / n_w)
    fk = fresnel(n_w, n_env, thrk)
    val("k=%d: R_s measured, (k/(k+2))^2" % k, [fk["Rs"], (k / (k + 2.0)) ** 2])
    val("k=%d: R_p measured, closed form" % k,
        [fk["Rp"], (((k + 1) - nr * nr) / ((k + 1) + nr * nr)) ** 2])
say()
say("   and reversibility: T(1->2 at th1) = T(2->1 at th2), exactly")
worst_rev = 0.0
for name, n1, n2 in PAIRS:
    for t in np.linspace(0.0, 85.0, 86):
        f = fresnel(n1, n2, math.radians(t))
        if f["tir"]:
            continue
        g = fresnel(n2, n1, f["th2"])
        worst_rev = max(worst_rev, abs(f["Ts"] - g["Ts"]), abs(f["Tp"] - g["Tp"]))
val("worst |T(1->2) - T(2->1)| over 8 pairs x 86 angles", worst_rev)
say()
say("   the rainbow's Fresnel throughput at k = 1, 2 and 3")
for k in (1, 2, 3):
    nr = n_rel(650.0)
    thk = rain_theta(nr, k)
    thrk = math.asin(n_env * math.sin(thk) / n_w)
    fin = fresnel(n_env, n_w, thk)
    fint = fresnel(n_w, n_env, thrk)
    for pol, pick in (("unpol", None), ("s", "s"), ("p", "p")):
        T1 = 0.5 * (fin["Ts"] + fin["Tp"]) if pick is None else fin["T" + pick]
        Rr = 0.5 * (fint["Rs"] + fint["Rp"]) if pick is None else fint["R" + pick]
        T2 = 0.5 * (fint["Ts"] + fint["Tp"]) if pick is None else fint["T" + pick]
        val("k=%d throughput (%s)" % (k, pol), T1 * Rr ** k * T2)


# ====================================================================== #
#  7. colour                                                             #
# ====================================================================== #
say()
say("=" * 70)
say("7. COLOUR  —  the CIE 1931 2-degree observer")
say("=" * 70)
say("   The CIE table the sim carries is read back OUT of p2_cie.js here and")
say("   the colour of a wavelength recomputed in Python, so the JavaScript")
say("   colour path is checked against an independent evaluation of the same")
say("   published numbers rather than against itself.")
CIE_SRC = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "p2_cie.js"), encoding="utf-8").read()
CIE = []
for m in re.finditer(r"\[(\d{3}),([\d.eE+-]+),([\d.eE+-]+),([\d.eE+-]+)\]", CIE_SRC):
    CIE.append((int(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))))
CIE.sort()
val("rows parsed from p2_cie.js, first, last", [len(CIE), CIE[0][0], CIE[-1][0]])
SRGB_M = ((3.2406, -1.5372, -0.4986), (-0.9689, 1.8758, 0.0415), (0.0557, -0.2040, 1.0570))


def cmf_at(nm):
    f = (nm - 360) / 5.0
    i = min(len(CIE) - 2, int(math.floor(f)))
    t = f - i
    a, b = CIE[i], CIE[i + 1]
    return [a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t, a[3] + (b[3] - a[3]) * t]


def xyz_to_lin(c):
    return [SRGB_M[r][0] * c[0] + SRGB_M[r][1] * c[1] + SRGB_M[r][2] * c[2] for r in range(3)]


def srgb_gamma(u):
    u = min(max(u, 0.0), 1.0)
    return 12.92 * u if u <= 0.0031308 else 1.055 * u ** (1 / 2.4) - 0.055


def mono_linear(nm):
    v = xyz_to_lin(cmf_at(nm))
    lo = min(v)
    if lo < 0:
        v = [u - lo for u in v]
    mx = max(v)
    return [u / mx for u in v] if mx > 0 else [0.0, 0.0, 0.0]


def mono_level(nm):
    return math.sqrt(min(1.0, 4 * cmf_at(nm)[1]))


def css_of(nm, k=1.0):
    v = mono_linear(nm)
    return "rgb(%d,%d,%d)" % tuple(int(round(255 * srgb_gamma(u * k))) for u in v)


say()
for nm in (400, 450, 500, 550, 600, 650, 690, 700):
    val("monoLinear(%d)" % nm, mono_linear(nm))
say()
for nm in (400, 450, 500, 550, 600, 650, 690, 700):
    say("%-52s %s" % ("cssOfLinear(monoLinear(%d), 1)" % nm, css_of(nm)))
say()
for nm in (450, 550, 650):
    say("%-52s %s" % ("cssOfLinear(monoLinear(%d), 0.25)" % nm, css_of(nm, 0.25)))
say()
for nm in (400, 450, 500, 555, 600, 650, 700):
    val("monoLevel(%d)" % nm, mono_level(nm))
say()
say("   PhET's white light is _.range(400, 700, 10) = 30 wavelengths,")
say("   400, 410, ..., 690 nm.  This file uses the same set.")
WL = list(range(400, 700, 10))
val("count, first, last", [len(WL), WL[0], WL[-1]])
say()
say("   sanity: 555 nm is the peak of the photopic response (ybar = 1)")
say("   (the CIE table itself is embedded in the sim from the CIE's own file")
say("    via build/blackbody-spectrum; nothing is re-typed here)")

with open("refvals.txt", "w") as fh:
    fh.write("\n".join(OUT) + "\n")
sys.stderr.write("derive.py finished: %d lines\n" % len(OUT))
