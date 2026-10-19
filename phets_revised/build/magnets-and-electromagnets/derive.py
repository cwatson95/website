#!/usr/bin/env python3
"""derive.py -- the Python twin of the magnets-and-electromagnets family
(magnets-and-electromagnets.html, magnet-and-compass.html, generator.html).

Re-derives every closed form the three pages implement, checks each against
an independent brute-force route, and prints the reference values the
selfTests assert, as lines

    REF <key> = <v1> <v2> ...

(shortest round-trip reprs, so gen_refs.py can emit them into the suite as
literals, never retyped).  Every other line is commentary, prefixed '#'.
Read the whole output (Known-bad: a reference that never appeared in output
you read is a guess wearing a citation).

Units: lengths in mm (1 PhET model px = 1 mm on these pages), fields in gauss
(PhET's unit), time in seconds.

    python3 derive.py > refvals.txt      (about a minute)
"""
import io
import json
import math
import os
import re
import sys

import numpy as np
from scipy import integrate, optimize, special

PI = math.pi
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
KEYS = set()


def REF(key, *vals):
    assert key not in KEYS, 'duplicate REF key ' + key
    KEYS.add(key)
    print('REF %s = %s' % (key, ' '.join(repr(float(v)) for v in vals)))


def say(*a):
    print('#', *a)


def check(cond, what):
    if not cond:
        raise SystemExit('derive.py CHECK FAILED: ' + what)
    say('ok  ', what)


# ---------------------------------------------------------------------------
say('=' * 74)
say('0. constants')
# ---------------------------------------------------------------------------
MU0 = 1.25663706127e-6          # N/A^2, CODATA 2022 (NIST), measured since 2019
REF('MU0', MU0)
say('mu0/(4 pi 1e-7) - 1 =', MU0 / (4 * PI * 1e-7) - 1)
G_PER_T = 1e4
L_MAG, R_MAG = 250.0, 25.0      # PhET BarMagnet size 250 x 50 (x 50): a cylinder, length 250, radius 25
B_HALF = L_MAG / 2
S_MAX = 300.0                   # PhET MAGNET_STRENGTH_RANGE (0, 300) G
A_COIL, PITCH, WIRE_R = 50.0, 16.0, 8.0     # PhET electromagnet: maxLoopArea 7854 = pi 50^2, wireWidth 16, loopSpacing 0
KAPPA = 0.01 * 25 ** 2          # PhET KinematicCompass: 0.01 sin(d) B per frame^2 at 25 frames/s -> 6.25 /(G s^2)
GAMMA = 0.08 * 25               # PhET: 0.08 omega per frame -> 2 /s
REF('KAPPA', KAPPA)
REF('GAMMA', GAMMA)
DC_VMAX, AC_VMAX, AC_F100 = 10.0, 110.0, 1.25   # PhET: the battery's +-10 V, the AC supply's 0-110 V,
REF('supply', DC_VMAX, AC_VMAX, AC_F100)        # and 2 pi/20 rad per frame at 25 frames/s = 1.25 Hz at 100 %
say('   PhET supplies: battery +-%g V, AC 0-%g V at %g Hz x (frequency %%)' % (DC_VMAX, AC_VMAX, AC_F100))
REF('coil.geom', 50.0, 16.0, 8.0, 4.0)          # PhET: loop radius (area 7854), wire width, its half, loops
REF('mag.geom', L_MAG, R_MAG, S_MAX)            # PhET: the 250 x 50 bar and its 0-300 G
E_FULL = 12e4 * 1e-4 * 1e-6 * 25    # PhET PickupCoil maxEMF 12e4 G px^2/frame, px = mm, 25 frames/s -> volts
REF('gen.efull', E_FULL)
say('PhET full-scale EMF 12e4 G px^2/frame =', E_FULL, 'V at 1 px = 1 mm, 25 frames/s')


# ---------------------------------------------------------------------------
say('=' * 74)
say('1. Bulirsch cel(kc,p,c,s) = int_0^{pi/2} (c cos^2 + s sin^2)/((cos^2 + p sin^2) sqrt(cos^2 + kc^2 sin^2))')
# ---------------------------------------------------------------------------
def cel(kc, p, c, s, errtol=1e-15):
    if kc == 0:
        return float('nan')
    k = abs(kc)
    pp, cc, ss = p, c, s
    em = 1.0
    if p > 0:
        pp = math.sqrt(p)
        ss = s / pp
    else:
        f = kc * kc
        q = 1.0 - f
        g = 1.0 - pp
        f = f - pp
        q = q * (ss - c * pp)
        pp = math.sqrt(f / g)
        cc = (c - ss) / g
        ss = -q / (g * g * pp) + cc * pp
    f = cc
    cc = cc + ss / pp
    g = k / pp
    ss = 2 * (ss + f * g)
    pp = g + pp
    g = em
    em = k + em
    kk = k
    it = 0
    while abs(g - k) > g * errtol:
        k = 2 * math.sqrt(kk)
        kk = k * em
        f = cc
        cc = cc + ss / pp
        g = kk / pp
        ss = 2 * (ss + f * g)
        pp = g + pp
        g = em
        em = k + em
        it += 1
        if it > 60:
            raise SystemExit('cel did not converge')
    return (PI / 2) * (ss + cc * em) / (em * (em + pp))


def cel_quad(kc, p, c, s):
    f = lambda t: (c * math.cos(t) ** 2 + s * math.sin(t) ** 2) / (
        (math.cos(t) ** 2 + p * math.sin(t) ** 2) * math.sqrt(math.cos(t) ** 2 + kc * kc * math.sin(t) ** 2))
    return integrate.quad(f, 0, PI / 2, epsabs=0, epsrel=1e-13, limit=400)[0]


CEL_ARGS = [(0.3, 0.7, 1.0, -1.0), (0.3, 0.09, 1.0, 0.3), (0.8, 1.0, 1.0, -1.0), (0.05, 0.0025, 1.0, 0.05),
            (0.6, 1.0, 1.0, 0.36), (0.999, 1.0, 1.0, -1.0), (0.2, 0.25, 0.5, 2.0)]
worst = 0.0
for i, args in enumerate(CEL_ARGS):
    v = cel(*args)
    q = cel_quad(*args)
    worst = max(worst, abs(v - q) / abs(q))
    REF('cel.%d' % i, *args, q)
check(worst < 1e-12, 'cel matches direct quadrature at %d argument sets (worst rel %.1e)' % (len(CEL_ARGS), worst))
for kc in [0.9, 0.5, 0.1, 1e-3, 1e-7]:
    K = cel(kc, 1, 1, 1)
    Kref = special.ellipkm1(kc * kc)      # accurate near k -> 1 (argument is 1 - m)
    E = cel(kc, 1, 1, kc * kc)
    Eref = special.ellipe(1 - kc * kc)
    REF('K.%g' % kc, kc, Kref)
    REF('E.%g' % kc, kc, Eref)
    check(abs(K / Kref - 1) < 2e-15 and abs(E / Eref - 1) < 3e-15, 'cel K and E at kc = %g vs scipy ellipkm1/ellipe' % kc)


# the Gauss-Legendre error on the first degree it cannot integrate, x^(2n):
#   E_n = 2^(2n+1) (n!)^4 / ((2n+1) ((2n)!)^2)   (the standard remainder with f^(2n) = (2n)!)
for n in [16, 24]:
    f = math.factorial
    E = 2.0 ** (2 * n + 1) * f(n) ** 4 / ((2 * n + 1) * f(2 * n) ** 2)
    x, w = np.polynomial.legendre.leggauss(n)
    meas = float(np.sum(w * x ** (2 * n))) - 2.0 / (2 * n + 1)
    REF('gl.err.%d' % n, n, E, meas)
    if n == 16:
        check(abs(meas / E + 1) < 1e-6,
              '%d-point Gauss-Legendre misses x^%d by %.4e = -(the remainder 2^(2n+1)(n!)^4/((2n+1)((2n)!)^2) = %.4e)' % (n, 2 * n, meas, E))
    else:
        say('   %d-point: the remainder for x^%d is %.3e, at the rounding level of the sum itself'
            ' (measured %.3e), so it pins nothing and is not asserted' % (n, 2 * n, E, meas))


# ---------------------------------------------------------------------------
say('=' * 74)
say('2. the bar magnet: a uniformly magnetised cylinder == an ideal solenoid carrying the')
say('   bound current K = M x n on its side wall (Amperian model: exact for B everywhere).')
say('   Derby & Olbert 2010 closed form; mu0 M = 1 here (fields scale with the strength S).')
# ---------------------------------------------------------------------------
def sol_B(rho, u, a, b):
    """ideal solenoid radius a, half-length b, axis u, centred; (B_rho, B_u) in units of mu0 n I."""
    zp, zm = u + b, u - b
    sp = math.sqrt(zp * zp + (rho + a) ** 2)
    sm = math.sqrt(zm * zm + (rho + a) ** 2)
    g = (a - rho) / (a + rho)
    kp = math.sqrt(zp * zp + (a - rho) ** 2) / sp
    km = math.sqrt(zm * zm + (a - rho) ** 2) / sm
    Br = (a / sp * cel(kp, 1, 1, -1) - a / sm * cel(km, 1, 1, -1)) / PI
    Bu = a / (a + rho) * (zp / sp * cel(kp, g * g, 1, g) - zm / sm * cel(km, g * g, 1, g)) / PI
    return Br, Bu


def sol_B_brute(rho, u, a, b):
    """Biot-Savart over the current sheet (mu0 K = 1): dB = (1/4pi) K x R / R^3 dA"""
    def dBr(p, zs):
        Rx, Ry, Rz = rho - a * math.cos(p), -a * math.sin(p), u - zs
        return math.cos(p) * Rz / (Rx * Rx + Ry * Ry + Rz * Rz) ** 1.5
    def dBz(p, zs):
        Rx, Ry, Rz = rho - a * math.cos(p), -a * math.sin(p), u - zs
        return (-math.sin(p) * Ry - math.cos(p) * Rx) / (Rx * Rx + Ry * Ry + Rz * Rz) ** 1.5
    fac = a / (4 * PI)
    Br = integrate.dblquad(dBr, -b, b, 0, 2 * PI, epsabs=1e-15, epsrel=1e-12)[0] * fac
    Bz = integrate.dblquad(dBz, -b, b, 0, 2 * PI, epsabs=1e-15, epsrel=1e-12)[0] * fac
    return Br, Bz


def sol_axis(u, a, b):
    """closed form on the axis: (1/2)[(u+b)/sqrt((u+b)^2+a^2) - (u-b)/sqrt((u-b)^2+a^2)]"""
    return 0.5 * ((u + b) / math.hypot(u + b, a) - (u - b) / math.hypot(u - b, a))


MAG_PTS = [(0.0, 0.0), (10.0, 30.0), (40.0, 60.0), (30.0, 140.0), (100.0, 300.0), (5.0, 124.0),
           (24.0, 0.0), (26.0, 0.0), (200.0, -90.0), (60.0, -200.0), (400.0, 0.0), (15.0, -126.0)]
worst = 0.0
for i, (rho, u) in enumerate(MAG_PTS):
    d = sol_B(rho, u, R_MAG, B_HALF)
    bf = sol_B_brute(rho, u, R_MAG, B_HALF)
    n = math.hypot(*bf)
    e = math.hypot(d[0] - bf[0], d[1] - bf[1]) / n
    worst = max(worst, e)
    REF('mag.pt.%d' % i, rho, u, bf[0], bf[1])
    say('   mag (%g, %g): closed (%.15e, %.15e)  brute (%.15e, %.15e)  |diff|/|B| %.1e' % (rho, u, d[0], d[1], bf[0], bf[1], e))
check(worst < 1e-12, 'Derby-Olbert closed form == brute-force Biot-Savart over the sheet at %d points (worst %.1e)' % (len(MAG_PTS), worst))
for u in [0.0, 60.0, 124.0, 125.0, 126.0, 300.0, -200.0]:
    cf = sol_axis(u, R_MAG, B_HALF)
    d = sol_B(0.0, u, R_MAG, B_HALF)[1]
    REF('mag.axis.%g' % u, u, cf)
    check(abs(d - cf) < 2e-15, 'on the axis the general form equals the closed form at u = %g (%.16f)' % (u, cf))
cos_alpha = B_HALF / math.hypot(B_HALF, R_MAG)
REF('mag.centre', cos_alpha)
say('   centre field / (mu0 M) = cos(alpha) = b/sqrt(b^2+R^2) =', cos_alpha)
# the side wall: B_u jumps by exactly mu0 M = 1, B_rho is continuous
for u in [0.0, 80.0, -110.0]:
    i_ = sol_B(R_MAG * (1 - 1e-9), u, R_MAG, B_HALF)
    o_ = sol_B(R_MAG * (1 + 1e-9), u, R_MAG, B_HALF)
    check(abs((i_[1] - o_[1]) - 1) < 1e-6 and abs(i_[0] - o_[0]) < 1e-6,
          'across the side wall at u = %g: B_u jumps by %.9f, B_rho by %.1e' % (u, i_[1] - o_[1], i_[0] - o_[0]))

# --- PhET's precomputed grid, read from the original (docs/phets), compared with the closed form
src = io.open(os.path.join(ROOT, 'docs', 'phets', 'magnets-and-electromagnets_en.html'), encoding='utf-8', errors='replace').read()
i0 = src.find('MAGNET_STRENGTH:1,INTERNAL_GRID_SPACING')
i0 = src.rfind('{', 0, i0)
i1 = src.find('};we.register("BarMagnetFieldData"', i0)
body = src[i0:i1 + 1]
body = re.sub(r'new [A-Za-z_$][\w$]*\.[A-Za-z_$][\w$]*\((\d+),(\d+)\)', r'[\1,\2]', body)
body = re.sub(r'([{,])([A-Z_]+):', r'\1"\2":', body)
body = re.sub(r'(?<=[\[,])\.(\d)', r'0.\1', body)
body = re.sub(r'(?<=[\[,])-\.(\d)', r'-0.\1', body)
GRID = json.loads(body)
tot_n, allerr = 0, []
for name, sp in [('INTERNAL', 5.0), ('EXTERNAL_NEAR', 5.0), ('EXTERNAL_FAR', 20.0)]:
    BX, BY = GRID['BX_' + name], GRID['BY_' + name]
    errs, worst_pt = [], None
    for i in range(len(BX)):
        for j in range(len(BX[0])):
            x, y = i * sp, j * sp
            if abs(y - R_MAG) < 1e-9 and x <= B_HALF:     # on the current sheet or its rim: two-valued / singular
                continue
            Br, Bu = sol_B(y, x, R_MAG, B_HALF)
            e = max(abs(BX[i][j] - Bu), abs(BY[i][j] - Br))
            errs.append(e)
            if worst_pt is None or e > worst_pt[0]:
                worst_pt = (e, x, y)
    errs = np.array(errs)
    tot_n += len(errs)
    allerr.extend(errs.tolist())
    REF('phet.grid.%s' % name, len(errs), np.median(errs), errs.max(), worst_pt[1], worst_pt[2])
    say('   PhET %-14s %5d points: median |diff| %.2e G per G, max %.2e at (%g, %g)' % (name, len(errs), np.median(errs), errs.max(), worst_pt[1], worst_pt[2]))
allerr = np.array(allerr)
REF('phet.grid.all', tot_n, np.median(allerr), float(np.mean(allerr < 1e-4)))
say('   all grids: %d points, median %.2e, fraction within 1e-4: %.4f' % (tot_n, np.median(allerr), np.mean(allerr < 1e-4)))
# a handful of PhET's printed values, for the page's parity check (value at PhET's printed precision)
for (name, i, j, sp, comp) in [('INTERNAL', 0, 0, 5.0, 'BX'), ('INTERNAL', 10, 3, 5.0, 'BX'), ('EXTERNAL_NEAR', 30, 10, 5.0, 'BX'),
                               ('EXTERNAL_NEAR', 30, 10, 5.0, 'BY'), ('EXTERNAL_FAR', 20, 10, 20.0, 'BX'), ('EXTERNAL_FAR', 20, 10, 20.0, 'BY')]:
    v = GRID[comp + '_' + name][i][j]
    Br, Bu = sol_B(j * sp, i * sp, R_MAG, B_HALF)
    mine = Bu if comp == 'BX' else Br
    REF('phet.sample.%s.%s.%d.%d' % (comp, name, i, j), i * sp, j * sp, v, 0 if comp == 'BX' else 1)
    say('   PhET %s_%s[%d][%d] at (%g, %g) = %r ; closed form %.10f' % (comp, name, i, j, i * sp, j * sp, v, mine))


# ---------------------------------------------------------------------------
say('=' * 74)
say('3. the far field of the magnet: the dipole limit, taken numerically, and the exact multipoles')
# ---------------------------------------------------------------------------
# point-dipole: B = (mu0 m/4pi r^3)(2 cos th, sin th) with mu0 m = mu0 M V = S pi R^2 L -> mu0 m/4pi = S R^2 L/4
DIP = R_MAG ** 2 * L_MAG / 4.0          # per unit S (G mm^3)
REF('mag.dip', DIP)
def q_l(l):
    f = lambda s: (B_HALF ** 2 + s * s) ** (l / 2) * special.eval_legendre(l, B_HALF / math.sqrt(B_HALF ** 2 + s * s)) * s
    return 2 * PI * integrate.quad(f, 0, R_MAG, epsabs=0, epsrel=1e-13, limit=200)[0]
Q1, Q3, Q5 = 2 * q_l(1), 2 * q_l(3), 2 * q_l(5)
check(abs(Q1 / (PI * R_MAG ** 2 * L_MAG) - 1) < 1e-13, 'the l = 1 moment of the pole-face charges is M V (mu0 m = S pi R^2 L)')
Q3cf = 2 * PI * B_HALF * R_MAG ** 2 * (B_HALF ** 2 - 0.75 * R_MAG ** 2)
check(abs(Q3 / Q3cf - 1) < 1e-13, 'the l = 3 moment closed form 2 pi b R^2 (b^2 - 3R^2/4)')
# relative octupole corrections: on the axis 2 Q3/(Q1 r^2), on the bisector -(3/2) Q3/(Q1 r^2)
C_AX, C_EQ = 2 * Q3 / Q1, -1.5 * Q3 / Q1
REF('mag.oct', C_AX, C_EQ)
say('   B/B_dip - 1 -> %.6f / r^2 on the axis, %.6f / r^2 on the bisector (r in mm)' % (C_AX, C_EQ))
def far_ratio(r, where):
    if where == 'axis':
        return sol_B(0.0, r, R_MAG, B_HALF)[1] * r ** 3 / (2 * DIP)
    return -sol_B(r, 0.0, R_MAG, B_HALF)[1] * r ** 3 / DIP
for where in ['axis', 'bis']:
    f1, f2, f4 = far_ratio(2000.0, where), far_ratio(4000.0, where), far_ratio(8000.0, where)
    r1 = (4 * f2 - f1) / 3            # remove 1/r^2
    r2 = (4 * f4 - f2) / 3
    lim = (16 * r2 - r1) / 15         # remove 1/r^4
    coef = (f1 - 1) * 2000.0 ** 2
    REF('mag.far.%s' % where, f1, f2, f4, lim, coef)
    say('   %s: r^3 B/dipole at 2, 4, 8 m = %.12f %.12f %.12f -> Richardson %.14f ; (f-1) r^2 at 2 m = %.4f' % (where, f1, f2, f4, lim, coef))
    check(abs(lim - 1) < 1e-8, 'the %s field tends to the point dipole of moment M V (limit %.2e from 1)' % (where, lim - 1))
# the deviation plotted in the far-field view, at the view's sample radii
for r in [300.0, 1000.0, 3000.0, 10000.0]:
    REF('mag.dev.%g' % r, r, far_ratio(r, 'axis') - 1, far_ratio(r, 'bis') - 1)


# ---------------------------------------------------------------------------
say('=' * 74)
say('4. a current loop (Biot-Savart), exact everywhere: K, E and the cancellation-free cel forms')
# ---------------------------------------------------------------------------
def loop_B(rho, z, a):
    """unit mu0 I; returns (B_rho, B_z, Psi) with Psi = rho A_phi the flux function (flux = 2 pi Psi)."""
    D = (a + rho) ** 2 + z * z
    kc2 = ((a - rho) ** 2 + z * z) / D
    kc = math.sqrt(kc2)
    K = cel(kc, 1, 1, 1)
    E = cel(kc, 1, 1, kc2)
    Bz = (K + (a * a - rho * rho - z * z) / ((a - rho) ** 2 + z * z) * E) / (2 * PI * math.sqrt(D))
    Br = a * z * cel(kc, 1, 1, -kc2) / (PI * D ** 1.5 * kc2)
    Psi = -a * rho / math.sqrt(D) * cel(kc, 1, 1, -1) / PI
    return Br, Bz, Psi


def loop_brute(rho, z, a):
    Dp = rho * rho + a * a + z * z
    fr = lambda p: math.cos(p) * math.expm1(-1.5 * math.log1p(-2 * a * rho * math.cos(p) / Dp))
    Br = a * z / (4 * PI) * Dp ** -1.5 * integrate.quad(fr, 0, 2 * PI, epsabs=0, epsrel=2e-14, limit=400)[0]
    fz = lambda p: (a * a - a * rho * math.cos(p)) * (Dp - 2 * a * rho * math.cos(p)) ** -1.5
    Bz = integrate.quad(fz, 0, 2 * PI, epsabs=0, epsrel=2e-14, limit=400)[0] / (4 * PI)
    fa = lambda p: math.cos(p) * math.expm1(-0.5 * math.log1p(-2 * a * rho * math.cos(p) / Dp))
    Aphi = a / (4 * PI) * Dp ** -0.5 * integrate.quad(fa, 0, 2 * PI, epsabs=0, epsrel=2e-14, limit=400)[0]
    return Br, Bz, rho * Aphi


LOOP_PTS = [(0.0, 20.0), (1e-6, 20.0), (1e-3, 20.0), (0.5, 3.0), (20.0, 10.0), (60.0, -40.0), (49.0, 1.0),
            (200.0, 150.0), (35.0, -70.0), (80.0, 0.0), (5.0, -5.0)]
worst = 0.0
for i, (rho, z) in enumerate(LOOP_PTS):
    c = loop_B(rho, z, A_COIL)
    m = loop_brute(rho, z, A_COIL)
    n = math.hypot(m[0], m[1])
    e = max(abs(c[0] - m[0]) / n, abs(c[1] - m[1]) / n, abs(c[2] - m[2]) / (abs(m[2]) + 1e-300) if rho > 0.1 else 0)
    worst = max(worst, e)
    REF('loop.pt.%d' % i, rho, z, m[0], m[1], m[2])
check(worst < 5e-14, 'loop B (K,E + cel for B_rho) and Psi (cel) == cancellation-free brute force at %d points (worst %.1e)' % (len(LOOP_PTS), worst))
# near the axis the brute force and the off-axis expansion B_rho = -(rho/2) Bz0' + (rho^3/16) Bz0''' agree
for rho in [1e-6, 1e-3]:
    z = 20.0
    s = A_COIL ** 2 + z * z
    d1 = -1.5 * A_COIL ** 2 * z * s ** -2.5
    d3 = (A_COIL ** 2 / 2) * (45 * z * s ** -3.5 - 105 * z ** 3 * s ** -4.5)
    ser = -(rho / 2) * d1 + (rho ** 3 / 16) * d3
    bf = loop_brute(rho, z, A_COIL)[0]
    check(abs(bf / ser - 1) < 1e-11, 'near the axis (rho = %g) the brute force B_rho equals the off-axis expansion (rel %.1e)' % (rho, abs(bf / ser - 1)))
# the direct K,E form for B_rho cancels near the axis: record how badly (the reason for the cel form)
def loop_Br_direct(rho, z, a):
    D = (a + rho) ** 2 + z * z
    kc2 = ((a - rho) ** 2 + z * z) / D
    kc = math.sqrt(kc2)
    K, E = cel(kc, 1, 1, 1), cel(kc, 1, 1, kc2)
    return z / (2 * PI * rho * math.sqrt(D)) * (-K + (a * a + rho * rho + z * z) / ((a - rho) ** 2 + z * z) * E)
bad = abs(loop_Br_direct(1e-6, 20.0, A_COIL) / loop_brute(1e-6, 20.0, A_COIL)[0] - 1)
REF('loop.direct_bad', bad)
say('   the textbook K,E form for B_rho is off by %.2f (relative) at rho = 1e-6 a: it is not used' % bad)
for z in [0.0, 30.0, -70.0, 400.0]:
    cf = A_COIL ** 2 / (2 * (A_COIL ** 2 + z * z) ** 1.5)
    REF('loop.axis.%g' % z, z, cf)
    check(abs(loop_B(0.0, z, A_COIL)[1] - cf) < 1e-17, 'on the axis the loop field is a^2/(2(a^2+z^2)^1.5) at z = %g' % z)
# flux through the loop's own plane inside radius r: Psi(r,0) vs int_0^r Bz rho drho
for r in [10.0, 30.0, 42.0]:
    q = integrate.quad(lambda x: loop_B(x, 0.0, A_COIL)[1] * x, 0, r, epsabs=0, epsrel=1e-13)[0]
    check(abs(loop_B(r, 0.0, A_COIL)[2] / q - 1) < 1e-12, 'Psi(%g, 0) equals the quadrature of B_z rho' % r)

say('-' * 60)
say('   the electromagnet: N loops, radius 50, pitch 16 (PhET: wire width 16, loop spacing 0)')
def coil_x(N):
    return [(k - (N - 1) / 2) * PITCH for k in range(N)]
def coil_B(rho, x, N):
    br = bz = ps = 0.0
    for xk in coil_x(N):
        a_, b_, c_ = loop_B(rho, x - xk, A_COIL)
        br += a_; bz += b_; ps += c_
    return br, bz, ps
# calibration: 4 loops at full current make PhET's maximum, 300 G, at the centre
Bc4 = coil_B(0.0, 0.0, 4)[1]            # per unit mu0 I, 1/mm
I_MAX = S_MAX / G_PER_T / (MU0 * Bc4 * 1e3)   # amps: B[T] = mu0 I (1/mm -> 1/m: *1e3)
REF('coil.Imax', I_MAX)
say('   full current I_max = %.10f A gives 300 G at the centre of 4 loops' % I_MAX)
for N in [1, 2, 3, 4]:
    bc = coil_B(0.0, 0.0, N)[1] * MU0 * 1e3 * I_MAX * G_PER_T
    REF('coil.centre.%d' % N, bc)
    say('   N = %d: centre field at full current %.10f G (PhET: %g G)' % (N, bc, 75 * N))
# the continuous solenoid limit: N loops at the midpoints of N cells of a length-l sheet -> sheet as O(p^2)
l_sheet = 64.0
exact = sol_axis(0.0, A_COIL, l_sheet / 2)
errs = []
for N in [4, 8, 16, 32]:
    p = l_sheet / N
    s_ = sum(A_COIL ** 2 / (2 * (A_COIL ** 2 + xk ** 2) ** 1.5) for xk in [(k - (N - 1) / 2) * p for k in range(N)]) * p
    errs.append(s_ - exact)
    REF('coil.midpt.%d' % N, N, s_, exact)
rates = [errs[i] / errs[i + 1] for i in range(3)]
say('   loop sum -> continuous sheet (mu0 n I = 1): errors %s, ratios %s' % (['%.3e' % e for e in errs], ['%.6f' % r for r in rates]))
check(abs(rates[-1] - 4) < 0.005 and abs(rates[0] - 4) > abs(rates[1] - 4) > abs(rates[2] - 4),
      'the N-loop coil tends to the continuous solenoid as the midpoint rule: error ratios per halving -> 4 (O(p^2))')


# ---------------------------------------------------------------------------
say('=' * 74)
say('5. field lines: equal-flux seeds at the mid-plane, and where each line crosses it again outside')
# ---------------------------------------------------------------------------
def psi_mag_mid(r):
    """Psi(r, 0) = int_0^r B_u(rho, 0) rho drho for the magnet (mu0 M = 1), split at the wall"""
    f = lambda x: sol_B(x, 0.0, R_MAG, B_HALF)[1] * x
    if r <= R_MAG:
        return integrate.quad(f, 0, r, epsabs=0, epsrel=1e-13, limit=200)[0]
    return (integrate.quad(f, 0, R_MAG, epsabs=0, epsrel=1e-13, limit=200)[0]
            + integrate.quad(f, R_MAG, r, epsabs=0, epsrel=1e-13, limit=400)[0])
PMAX = psi_mag_mid(R_MAG)
REF('lines.mag.psimax', PMAX)
N_MAG_LINES = 10
for i in range(1, N_MAG_LINES + 1):
    t = i * PMAX / (N_MAG_LINES + 1)
    r_in = optimize.brentq(lambda r: psi_mag_mid(r) - t, 1e-12, R_MAG, xtol=1e-15, rtol=1e-15)
    r_out = optimize.brentq(lambda r: psi_mag_mid(r) - t, R_MAG * (1 + 1e-12), 1e7, xtol=1e-12, rtol=1e-15)
    REF('lines.mag.%d' % i, t, r_in, r_out)
say('   the magnet: Psi_max = %.12f (the flux through the mid cross-section / 2 pi)' % PMAX)
N_COIL_LINES = 8
for N in [1, 2, 3, 4]:
    pm = coil_B(A_COIL - WIRE_R, 0.0, N)[2]
    REF('lines.coil.%d.psimax' % N, pm)
    for i in range(1, N_COIL_LINES + 1):
        t = i * pm / (N_COIL_LINES + 1)
        r_in = optimize.brentq(lambda r: coil_B(r, 0.0, N)[2] - t, 1e-9, A_COIL - WIRE_R, xtol=1e-15, rtol=1e-15)
        r_out = optimize.brentq(lambda r: coil_B(r, 0.0, N)[2] - t, A_COIL + WIRE_R, 1e7, xtol=1e-12, rtol=1e-15)
        REF('lines.coil.%d.%d' % (N, i), t, r_in, r_out)


# ---------------------------------------------------------------------------
say('=' * 74)
say('6. the compass: a damped rotor  phi\'\' = kappa |B| sin(theta_B - phi) - gamma phi\'  (modelled)')
# ---------------------------------------------------------------------------
def rotor_rhs(t, y, B, th, kap, gam):
    return [y[1], kap * B * math.sin(th - y[0]) - gam * y[1]]
for (B, phi0, gam, tag) in [(5.0, 2.5, GAMMA, 'big'), (40.0, 1.0, GAMMA, 'strong'), (0.1, 1.2, GAMMA, 'over')]:
    ts = [0.25, 0.5, 1.0, 2.0, 4.0]
    sol = integrate.solve_ivp(rotor_rhs, (0, 4.0), [phi0, 0.0], args=(B, 0.0, KAPPA, gam), rtol=1e-12, atol=1e-14,
                              method='DOP853', dense_output=True)
    for t in ts:
        y = sol.sol(t)
        REF('rotor.%s.%g' % (tag, t), B, phi0, gam, t, y[0], y[1])
# the linear (small-angle) closed form, and the undamped large-amplitude period 4 K(sin(phi0/2))/omega0
B, th0 = 5.0, 1e-3
w0 = math.sqrt(KAPPA * B)
wd = math.sqrt(w0 * w0 - GAMMA * GAMMA / 4)
for t in [0.3, 1.1, 2.9]:
    lin = th0 * math.exp(-GAMMA * t / 2) * (math.cos(wd * t) + GAMMA / (2 * wd) * math.sin(wd * t))
    REF('rotor.lin.%g' % t, B, th0, t, lin)
for phi0 in [0.5, 2.0, 3.0]:
    T = 4 * special.ellipk(math.sin(phi0 / 2) ** 2) / w0
    sol = integrate.solve_ivp(lambda t, y: [y[1], -KAPPA * B * math.sin(y[0])], (0, 3 * T), [phi0, 0.0], rtol=1e-12, atol=1e-14,
                              method='DOP853', events=lambda t, y: y[0])
    zc = sol.t_events[0]
    Tnum = 2 * (zc[2] - zc[1])
    REF('rotor.period.%g' % phi0, B, phi0, T)
    check(abs(Tnum / T - 1) < 1e-9, 'undamped period at %g rad: 4K(sin(phi0/2))/omega0 = %.12f s (solve_ivp %.12f)' % (phi0, T, Tnum))
REF('rotor.Bcrit', GAMMA ** 2 / (4 * KAPPA))
say('   critical damping at |B| = gamma^2/(4 kappa) = %.6f G' % (GAMMA ** 2 / (4 * KAPPA)))


# ---------------------------------------------------------------------------
say('=' * 74)
say('7. the generator: flux of the turbine magnet through the pickup coil, EMF = -N dPhi/dt')
# ---------------------------------------------------------------------------
LAYOUT_H = 618.0
CM = (285.0, LAYOUT_H - 375.0)        # PhET GeneratorScreenModel turbine position (y flipped)
CC = (520.0, LAYOUT_H - 375.0)        # PhET pickup coil position
MAX_AREA = 70685.0                    # PhET pickup coil maxLoopArea (radius 150)
REF('gen.geom', CM[0], CM[1], CC[0], CC[1], MAX_AREA)

def magB3(P, th, c=CM):
    ax = (math.cos(th), math.sin(th), 0.0)
    rel = (P[0] - c[0], P[1] - c[1], P[2])
    u = rel[0] * ax[0] + rel[1] * ax[1]
    v = (rel[0] - u * ax[0], rel[1] - u * ax[1], rel[2])
    rho = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
    Br, Bu = sol_B(rho, u, R_MAG, B_HALF)
    if rho > 0:
        return tuple(Bu * ax[i] + Br * v[i] / rho for i in range(3))
    return tuple(Bu * ax[i] for i in range(3))

def flux_ref(th, rc):
    f = lambda s, psi: magB3((CC[0], CC[1] + s * math.cos(psi), s * math.sin(psi)), th)[0] * s
    return integrate.dblquad(f, 0, 2 * PI, 0, rc, epsabs=1e-13, epsrel=1e-13)[0]

GLX, GLW = np.polynomial.legendre.leggauss(16)
def flux_gl(th, rc, npsi=32):
    tot = 0.0
    for xi, wi in zip(GLX, GLW):
        s = 0.5 * rc * (xi + 1)
        acc = sum(magB3((CC[0], CC[1] + s * math.cos(2 * PI * j / npsi), s * math.sin(2 * PI * j / npsi)), th)[0] for j in range(npsi))
        tot += 0.5 * rc * wi * s * acc * 2 * PI / npsi
    return tot

def flux_phet(th, rc, sp=5.0):
    n = int(math.floor(rc / sp))
    ys = [0.0] + [k * sp for k in range(1, n + 1)] + [-k * sp for k in range(1, n + 1)]
    return sum(magB3((CC[0], CC[1] + y, 0.0), th)[0] * 2 * math.sqrt(abs(rc * rc - y * y)) * sp for y in ys)

GEN_TH = [0.0, 0.3, 0.9, 1.3, 2.2, 4.0]
for pct in [20, 50, 100]:
    rc = math.sqrt(pct / 100 * MAX_AREA / PI)
    worst = 0.0
    for j, th in enumerate(GEN_TH):
        ref = flux_ref(th, rc)
        gl = flux_gl(th, rc)
        worst = max(worst, abs(gl - ref) / 400.0)
        REF('gen.flux.%d.%d' % (pct, j), pct, rc, th, ref)
    check(worst < 1e-13, 'the 16 x 32 disc rule matches dblquad for a %d%% coil (worst %.1e of the peak flux)' % (pct, worst))
    # Fourier analysis over one turn (only odd harmonics survive: Phi(th + pi) = -Phi(th), Phi even)
    M = 256
    F = np.array([flux_gl(2 * PI * j / M, rc) for j in range(M)])
    C = np.fft.rfft(F) / M
    a_k = 2 * C.real
    b_k = -2 * C.imag
    even_max = max(abs(a_k[k]) for k in range(0, 40, 2))
    sin_max = max(abs(b_k[k]) for k in range(1, 40))
    check(even_max < 1e-11 and sin_max < 1e-11, '%d%%: no even harmonics (%.1e) and no sine terms (%.1e): Phi is even with Phi(th+pi) = -Phi(th)' % (pct, even_max, sin_max))
    REF('gen.harm.%d' % pct, *[a_k[k] for k in (1, 3, 5, 7, 9, 11)])
    kk = np.arange(len(C))
    dF = np.fft.irfft(1j * kk * np.fft.rfft(F), n=M)       # dPhi/dth
    emf = -dF                                              # EMF / (N omega S), per unit strength
    # refine the peak on [0, pi/2] by maximising the Fourier series
    ser = lambda th: sum(k * a_k[k] * math.sin(k * th) for k in range(1, 60, 2))
    jmax = int(np.argmax(emf[:M // 4 + 1]))
    res = optimize.minimize_scalar(lambda th: -ser(th), bounds=(max(0.0, 2 * PI * (jmax - 2) / M), 2 * PI * (jmax + 2) / M), method='bounded',
                                   options={'xatol': 1e-13})
    th_pk, e_pk = res.x, ser(res.x)
    REF('gen.peak.%d' % pct, th_pk, e_pk, ser(PI / 2), max(abs(F)))
    ph0 = flux_phet(0.0, rc)
    REF('gen.phet.%d' % pct, ph0, F[0], ph0 / F[0])
    say('   %3d%% (radius %.4f mm): Phi(0) = %.10f G mm^2 per G; harmonics a1..a11 %s' % (pct, rc, F[0], ' '.join('%.4e' % a_k[k] for k in (1, 3, 5, 7, 9, 11))))
    say('        EMF/(N w S) peaks at th = %.6f rad = %.4f deg, value %.10f; at 90 deg %.10f (%.4f of the peak); PhET line sample / area integral at th = 0: %.6f' % (
        th_pk, th_pk * 180 / PI, e_pk, ser(PI / 2), ser(PI / 2) / e_pk, ph0 / F[0]))
    if pct == 50:
        # volts at PhET's defaults with the wheel at full flow: S = 225 G, N = 2, omega = 2 pi
        v = e_pk * 225.0 * 1e-4 * 1e-6 * 2 * 2 * PI
        REF('gen.volts.default', v, v / E_FULL)
        say('        peak EMF at 75%% strength, 2 loops, 60 rpm = %.6e V = %.4f of PhET\'s full scale' % (v, v / E_FULL))

# PhET's Generator model ties a drag factor to the pickup coil's size: rpm = flow/100 x
# (1 - drag) x 60, drag = strength/100 x a linear ramp in N x area from (N_min A_min) to
# (N_max A_max).  Phenomenological (a real back-torque needs the circuit's resistance), but
# it is PhET's, so it is pinned here rather than typed into the page.
DRAG_MAX = 0.2
NA_LO = 0.2 * MAX_AREA
NA_HI = 4 * MAX_AREA
DRAG_LO = NA_LO / NA_HI * DRAG_MAX


def drag_f(N, area_pct, pct):
    na = N * area_pct / 100.0 * MAX_AREA
    return pct / 100.0 * (DRAG_LO + (DRAG_MAX - DRAG_LO) * (na - NA_LO) / (NA_HI - NA_LO))


check(abs(DRAG_LO - 0.01) < 1e-16, "the smallest coil's drag is exactly 0.01 (1 x 20%% of the area is a twentieth of 4 x 100%%)")
check(abs(drag_f(4, 100, 100) - DRAG_MAX) < 1e-16, 'and the largest at full strength is PhET\'s maximum, 0.2')
REF('gen.drag', NA_LO, NA_HI, DRAG_LO, DRAG_MAX)
REF('gen.drag.default', drag_f(2, 50, 75), (1 - drag_f(2, 50, 75)) * 60)
say('   drag at the defaults (2 loops, 50%% area, 75%% strength) = %.6f, so full flow turns the wheel at %.4f rpm'
    % (drag_f(2, 50, 75), (1 - drag_f(2, 50, 75)) * 60))

say('=' * 74)
say('8. the field meter: readings at world points for the pages\' default layouts (1 PhET px = 1 mm, y up)')
# ---------------------------------------------------------------------------
def mag_world(px, py, cx, cy, ang, S):
    B = magB3((px, py, 0.0), ang, c=(cx, cy))
    return S * B[0], S * B[1]
for (px, py, ang, tag) in [(560.0, 380.0, 0.0, 'a'), (300.0, 250.0, 0.0, 'b'), (560.0, 380.0, PI, 'flip'), (433.0, 340.0, 0.0, 'inside'),
                           (430.0 + 125.0 + 3.0, 333.0 + 20.0, 0.0, 'nearrim')]:
    bx, by = mag_world(px, py, 430.0, 333.0, ang, 225.0)
    REF('meter.bar.%s' % tag, px, py, ang, bx, by)
    say('   bar magnet at (430, 333), %g rad, 225 G: B(%g, %g) = (%.12f, %.12f) G, |B| %.10f, theta %.6f deg' % (ang, px, py, bx, by, math.hypot(bx, by), math.degrees(math.atan2(by, bx))))
bxa, bya = mag_world(560.0, 380.0, 430.0, 333.0, 0.0, 225.0)
bxf, byf = mag_world(560.0, 380.0, 430.0, 333.0, PI, 225.0)
check(abs(bxa + bxf) < 1e-12 and abs(bya + byf) < 1e-12, 'flipping the magnet about its centre reverses the field at every point')
def coil_world(px, py, cx, cy, N, I):
    br = bz = 0.0
    rho = abs(py - cy)
    for xk in coil_x(N):
        a_, b_, c_ = loop_B(rho, px - cx - xk, A_COIL)
        br += a_; bz += b_
    k = MU0 * I * 1e3 * G_PER_T
    return k * bz, (k * br * (1 if py >= cy else -1)) if rho > 0 else 0.0
for (px, py, N, frac, tag) in [(500.0, 300.0, 4, 1.0, 'a'), (400.0, 330.0, 4, 1.0, 'above'), (330.0, 200.0, 2, -0.35, 'b'), (400.0, 218.0, 1, 0.5, 'centre1')]:
    I = I_MAX * frac
    bx, by = coil_world(px, py, 400.0, 218.0, N, I)
    REF('meter.em.%s' % tag, px, py, N, I, bx, by)
    say('   coil at (400, 218), N = %d, I = %.6f A: B(%g, %g) = (%.12f, %.12f) G' % (N, I, px, py, bx, by))

say('=' * 74)
say('done: %d REF lines' % len(KEYS))
