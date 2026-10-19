#!/usr/bin/env python3
"""derive.py -- the Python twin of charges-and-fields.html.

Re-derives every quantity the sim asserts and prints reference values to 16
significant digits.  Output goes to refvals.txt (read it IN FULL -- never
through head/tail; the selfTest's "(derive)" labels point at lines of it).

Physics: exact superposition of 3-D point-charge Coulomb potentials and fields
for charges confined to the plane z = 0 (PhET's model: "point charges of one
nano Coulomb ... the three dimensional Maxwell's equations are used, the
charges are confined to move along a two dimensional surface").

    V(r) = k sum_i q_i / |r - r_i|,   E(r) = k sum_i q_i (r - r_i) / |r - r_i|^3

Units: metres, nanocoulombs, volts, V/m.  k = 1/(4 pi eps0) with eps0 the
CODATA 2022 value from NIST (8.8541878188e-12 F/m, stored verbatim), so
k = 8.98755... V m / nC.  PhET's own constant is K_CONSTANT = 9.

Independent routes used here (the JS never sees them):
  * E against -grad V by central differences,
  * equipotential loops by POLAR ROOT FINDING (brentq on each ray) -- area and
    perimeter by adaptive quadrature -- against the JS's traced polygon,
  * field lines by scipy solve_ivp (rtol 1e-12) against the Stokes flux
    function Psi = sum q_i cos(theta_i) of a collinear configuration, and the
    closed-form arrival / escape angles that Psi implies,
  * nulls of E by scipy fsolve, classified by the in-plane Hessian of V,
  * the multipole coefficients by the tensor contraction AND by the Legendre
    series, the far-field limits taken numerically (Richardson) and exactly,
  * the tape's line integral int E.dl by scipy quad against V(A) - V(B).
"""
import math
import sys

import numpy as np
from scipy import integrate, optimize

OUT = []


def P(*a):
    s = ' '.join(str(x) for x in a)
    OUT.append(s)


def g(x):
    return '%.16g' % x


# ---------------------------------------------------------------- constants
EPS0 = 8.8541878188e-12            # F/m, CODATA 2022 (NIST, physics.nist.gov/cgi-bin/cuu/Value?ep0)
K_SI = 1.0 / (4.0 * math.pi * EPS0)
KNC = K_SI * 1e-9                  # V m / nC
K_PHET = 9.0                       # PhET's K_CONSTANT
P('# constants')
P('EPS0', g(EPS0))
P('K_SI', g(K_SI))
P('KNC', g(KNC))
P('KNC/K_PHET', g(KNC / K_PHET))
P('PhET 15 px per V/m at 128 px/m -> m per V/m', g(15.0 / 128.0))
P('PhET arrow length 40 px -> m', g(40.0 / 128.0))
P('PhET charge radius 12 px -> m', g(12.0 / 128.0))

# ---------------------------------------------------------------- presets
S3 = math.sqrt(3.0)
PRESETS = {
    'single': [(0.0, 0.0, 1.0)],
    'dipole': [(-0.5, 0.0, -1.0), (0.5, 0.0, 1.0)],
    'like': [(-0.5, 0.0, 1.0), (0.5, 0.0, 1.0)],
    'quad': [(0.5, 0.5, 1.0), (-0.5, 0.5, -1.0), (-0.5, -0.5, 1.0), (0.5, -0.5, -1.0)],
    'triangle': [(0.0, 0.75, 1.0), (-0.75 * S3 / 2, -0.375, 1.0), (0.75 * S3 / 2, -0.375, 1.0)],
    'rows': [(x, 1.0, 1.0) for x in (-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5)] +
            [(x, -1.0, -1.0) for x in (-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5)],
}
ORDER = ['single', 'dipole', 'like', 'quad', 'triangle', 'rows']


def V(ch, x, y):
    s = 0.0
    for (cx, cy, q) in ch:
        s += q / math.hypot(x - cx, y - cy)
    return KNC * s


def E(ch, x, y):
    ex = ey = 0.0
    for (cx, cy, q) in ch:
        dx, dy = x - cx, y - cy
        r2 = dx * dx + dy * dy
        r3 = r2 * math.sqrt(r2)
        ex += q * dx / r3
        ey += q * dy / r3
    return KNC * ex, KNC * ey


def J(ch, x, y):
    """Jacobian dE_a/dx_b (symmetric; = minus the Hessian of V)."""
    a = b = c = 0.0
    for (cx, cy, q) in ch:
        dx, dy = x - cx, y - cy
        r2 = dx * dx + dy * dy
        r = math.sqrt(r2)
        r3, r5 = r2 * r, r2 * r2 * r
        a += q * (1.0 / r3 - 3.0 * dx * dx / r5)
        b += q * (-3.0 * dx * dy / r5)
        c += q * (1.0 / r3 - 3.0 * dy * dy / r5)
    return KNC * a, KNC * b, KNC * c


PROBES = [(1.3, 0.7), (-2.1, 1.1), (0.2, -0.9), (3.5, 2.2), (-0.35, 0.05)]

P('')
P('# V and E at the probes: preset, probe index, V, Ex, Ey, |E|, angle(deg)')
for i, (x, y) in enumerate(PROBES):
    P('PROBE', i, g(x), g(y))
for nm in ORDER:
    ch = PRESETS[nm]
    for i, (x, y) in enumerate(PROBES):
        v = V(ch, x, y)
        ex, ey = E(ch, x, y)
        P('VE', nm, i, g(v), g(ex), g(ey), g(math.hypot(ex, ey)), g(math.degrees(math.atan2(ey, ex))))

# E = -grad V, central differences (an independent route to E)
P('')
P('# E against -grad V (central differences, h = 1e-6): max relative disagreement per preset')
for nm in ORDER:
    ch = PRESETS[nm]
    worst = 0.0
    for (x, y) in PROBES:
        h = 1e-6
        gx = -(V(ch, x + h, y) - V(ch, x - h, y)) / (2 * h)
        gy = -(V(ch, x, y + h) - V(ch, x, y - h)) / (2 * h)
        ex, ey = E(ch, x, y)
        worst = max(worst, math.hypot(gx - ex, gy - ey) / math.hypot(ex, ey))
    P('GRADCHECK', nm, '%.3e' % worst)
    assert worst < 1e-6, nm
# the Jacobian against finite differences of E
for nm in ORDER:
    ch = PRESETS[nm]
    worst = 0.0
    for (x, y) in PROBES:
        h = 1e-6
        a, b, c = J(ch, x, y)
        exp_, eyp = E(ch, x + h, y)
        exm, eym = E(ch, x - h, y)
        a2, b2 = (exp_ - exm) / (2 * h), (eyp - eym) / (2 * h)
        exq, eyq = E(ch, x, y + h)
        exn, eyn = E(ch, x, y - h)
        b3, c2 = (exq - exn) / (2 * h), (eyq - eyn) / (2 * h)
        sc = max(abs(a), abs(b), abs(c))
        worst = max(worst, abs(a - a2) / sc, abs(b - b2) / sc, abs(b - b3) / sc, abs(c - c2) / sc)
    P('JACCHECK', nm, '%.3e' % worst)
    assert worst < 1e-6, nm

# ---------------------------------------------------------------- equipotentials by polar root finding


def V_vec(ch, xs, ys):
    s = np.zeros_like(xs)
    for (cx, cy, q) in ch:
        s += q / np.hypot(xs - cx, ys - cy)
    return KNC * s


def polar_loop(ch, cx, cy, V0, rmax):
    """r(phi) of the level set V = V0 on rays from (cx, cy), one crossing per ray
    (asserted by a dense vectorised scan).  Returns r(phi) as a callable."""
    rs = np.linspace(1e-4, rmax, 4001)

    def f(r, ph):
        return V(ch, cx + r * math.cos(ph), cy + r * math.sin(ph)) - V0

    def r_of(ph):
        vals = V_vec(ch, cx + rs * math.cos(ph), cy + rs * math.sin(ph)) - V0
        sg = vals > 0
        cross = np.nonzero(sg[:-1] != sg[1:])[0]
        assert len(cross) == 1, (ph, len(cross))
        k = int(cross[0])
        return optimize.brentq(lambda r: f(r, ph), rs[k], rs[k + 1], xtol=1e-15, rtol=1e-15, maxiter=200)
    return r_of


def loop_area_perimeter(r_of):
    # area = 1/2 int r^2 dphi ; perimeter = int sqrt(r^2 + r'^2) dphi, r' by a
    # 4th-order central difference of the root (step 1e-5)
    def rp(ph):
        h = 1e-4
        return (-r_of(ph + 2 * h) + 8 * r_of(ph + h) - 8 * r_of(ph - h) + r_of(ph - 2 * h)) / (12 * h)
    A = integrate.quad(lambda ph: 0.5 * r_of(ph) ** 2, 0, 2 * math.pi, epsabs=1e-13, epsrel=1e-12, limit=400)[0]
    Lp = integrate.quad(lambda ph: math.hypot(r_of(ph), rp(ph)), 0, 2 * math.pi, epsabs=1e-11, epsrel=1e-10, limit=400)[0]
    return A, Lp


P('')
P('# equipotential loops (polar brentq + adaptive quad): name, seed, centre, V0, area, perimeter, extra')
LOOPS = [
    ('single_r1', 'single', (1.0, 0.0), (0.0, 0.0), 3.0),
    ('dipole_09', 'dipole', (0.9, 0.0), (0.5, 0.0), 1.2),
    ('quad_08', 'quad', (0.8, 0.8), (0.5, 0.5), 0.6),
    ('like_04', 'like', (0.0, 0.4), (0.0, 0.0), 2.5),
    ('tri_005', 'triangle', (0.0, 0.05), (0.0, 0.0), 0.3),
]
for (nm, pre, seed, cen, rmax) in LOOPS:
    ch = PRESETS[pre]
    V0 = V(ch, seed[0], seed[1])
    r_of = polar_loop(ch, cen[0], cen[1], V0, rmax)
    A, Lp = loop_area_perimeter(r_of)
    # the loop's extreme y (max over phi of r sin phi + cy) and extreme x
    phs = np.linspace(0, 2 * math.pi, 2001)
    ys = [cen[1] + r_of(p) * math.sin(p) for p in phs]
    xs = [cen[0] + r_of(p) * math.cos(p) for p in phs]
    k = int(np.argmax(ys))
    ymax = -optimize.minimize_scalar(lambda p: -(cen[1] + r_of(p) * math.sin(p)),
                                     bracket=(phs[max(k - 1, 0)], phs[k], phs[min(k + 1, 2000)]),
                                     tol=1e-12).fun
    kx = int(np.argmin(xs))
    xmin = optimize.minimize_scalar(lambda p: cen[0] + r_of(p) * math.cos(p),
                                    bracket=(phs[max(kx - 1, 0)], phs[kx], phs[min(kx + 1, 2000)]),
                                    tol=1e-12).fun
    P('LOOP', nm, pre, g(seed[0]), g(seed[1]), g(V0), g(A), g(Lp), 'ymax', g(ymax), 'xmin', g(xmin))
# the single-charge loop is a circle: area pi, perimeter 2 pi
P('CIRCLE_CHECK', g(math.pi), g(2 * math.pi))

# the dipole's left axis crossing of the 0.9 loop, closed form route: solve on the axis
ch = PRESETS['dipole']
V0 = V(ch, 0.9, 0.0)
xl = optimize.brentq(lambda x: V(ch, x, 0.0) - V0, -0.49, 0.49, xtol=1e-15)
P('DIPOLE09_AXIS_LEFT', g(xl))

# the like pair's saddle level and the seed below it
chl = PRESETS['like']
P('LIKE_SADDLE_V', g(V(chl, 0.0, 0.0)), 'seed_0.4_V', g(V(chl, 0.0, 0.4)))

# ---------------------------------------------------------------- field lines


def unitE(ch, s, sgn=1.0):
    ex, ey = E(ch, s[0], s[1])
    m = math.hypot(ex, ey)
    return [sgn * ex / m, sgn * ey / m]


def psi_axis_x(ch, x, y):
    """Stokes flux function of a configuration on the x axis: sum q_i cos(theta_i)."""
    s = 0.0
    for (cx, cy, q) in ch:
        s += q * (x - cx) / math.hypot(x - cx, y - cy)
    return s


def trace_ivp(ch, x0, y0, sgn, stop, smax):
    ev = lambda s, u: stop(u)
    ev.terminal = True
    sol = integrate.solve_ivp(lambda s, u: unitE(ch, u, sgn), (0, smax), [x0, y0], method='DOP853',
                              rtol=1e-12, atol=1e-13, events=ev, dense_output=False, max_step=0.05)
    return sol.y[:, -1]


P('')
P('# field lines, dipole (+ at (0.5,0), - at (-0.5,0)): Psi = (x-0.5)/r+ - (x+0.5)/r- is conserved;')
P('# a line leaving + at alpha from the +x axis arrives at - at alpha from the -x axis (exact, 3-D axisymmetry)')
chd = PRESETS['dipole']
RS = 0.02
for adeg in (22.5, 67.5, 112.5, 157.5):
    a = math.radians(adeg)
    x0, y0 = 0.5 + RS * math.cos(a), RS * math.sin(a)
    psi0 = psi_axis_x(chd, x0, y0)
    end = trace_ivp(chd, x0, y0, 1.0, lambda u: math.hypot(u[0] + 0.5, u[1]) - RS, 400.0)
    psi1 = psi_axis_x(chd, end[0], end[1])
    arr = math.atan2(end[1], -(end[0] + 0.5))           # angle from the -x axis at the - charge
    # exact arrival from Psi: near - , Psi = (x-0.5)/r+ - cos(beta_from_+x)
    P('DIPLINE', g(adeg), 'psi0', g(psi0), 'psi_end', g(psi1), 'arrive_deg', g(math.degrees(arr)))

P('')
P('# field lines, like pair (+1 at (+-0.5,0)): escape direction cos(th_inf) = (1 + cos alpha)/2 (exact)')
chl = PRESETS['like']
for adeg in (30.0, 90.0, 150.0):
    a = math.radians(adeg)
    x0, y0 = 0.5 + RS * math.cos(a), RS * math.sin(a)
    end = trace_ivp(chl, x0, y0, 1.0, lambda u: math.hypot(u[0], u[1]) - 1000.0, 5000.0)
    th_num = math.degrees(math.atan2(end[1], end[0]))
    psi0 = psi_axis_x(chl, x0, y0)
    th_exact = math.degrees(math.acos((1 + math.cos(a)) / 2))
    th_psi = math.degrees(math.acos(psi0 / 2))                 # from the seed's own Psi
    P('LIKELINE', g(adeg), 'th_formula', g(th_exact), 'th_from_seed_psi', g(th_psi), 'th_at_1000m', g(th_num))

# ---------------------------------------------------------------- nulls of E


def nulls(ch, box, grid=(41, 27)):
    found = []
    for x in np.linspace(box[0], box[1], grid[0]):
        for y in np.linspace(box[2], box[3], grid[1]):
            if min(math.hypot(x - c[0], y - c[1]) for c in ch) < 0.05:
                continue
            sol, info, ier, msg = optimize.fsolve(lambda u: E(ch, u[0], u[1]), [x, y], full_output=True, xtol=1e-14)
            if ier != 1:
                continue
            ex, ey = E(ch, sol[0], sol[1])
            if math.hypot(ex, ey) > 1e-9:
                continue
            if not (box[0] - 1e-9 <= sol[0] <= box[1] + 1e-9 and box[2] - 1e-9 <= sol[1] <= box[3] + 1e-9):
                continue
            if min(math.hypot(sol[0] - c[0], sol[1] - c[1]) for c in ch) < 0.02:
                continue
            if all(math.hypot(sol[0] - f[0], sol[1] - f[1]) > 1e-7 for f in found):
                found.append((sol[0], sol[1]))
    out = []
    for (x, y) in sorted(found):
        a, b, c = J(ch, x, y)                  # Hessian of V = -J
        hxx, hxy, hyy = -a, -b, -c
        det = hxx * hyy - hxy * hxy
        kind = 'saddle' if det < 0 else ('min' if hxx + hyy > 0 else 'max')
        out.append((x, y, V(ch, x, y), kind, hxx + hyy))
    return out


P('')
P('# nulls of E inside [-4,4]x[-2.5,2.5] (fsolve from a 41x27 grid): preset, x, y, V, kind, in-plane Laplacian')
BOX = (-4.0, 4.0, -2.5, 2.5)
for nm in ORDER:
    ns = nulls(PRESETS[nm], BOX)
    P('NULLCOUNT', nm, len(ns))
    for (x, y, v, kind, lap) in ns:
        P('NULL', nm, g(x), g(y), g(v), kind, g(lap))
# the triangle's saddle on the -y axis, by brentq on E_y(0, y)
cht = PRESETS['triangle']
ys = optimize.brentq(lambda y: E(cht, 0.0, y)[1], -0.374, -0.01, xtol=1e-15)
P('TRI_SADDLE_Y', g(ys))

# ---------------------------------------------------------------- multipoles


def centre(ch):
    Q = sum(c[2] for c in ch)
    if abs(Q) > 1e-12:
        return (sum(c[2] * c[0] for c in ch) / Q, sum(c[2] * c[1] for c in ch) / Q)
    return (sum(c[0] for c in ch) / len(ch), sum(c[1] for c in ch) / len(ch))


def moments(ch):
    cx, cy = centre(ch)
    Q = sum(c[2] for c in ch)
    px = sum(c[2] * (c[0] - cx) for c in ch)
    py = sum(c[2] * (c[1] - cy) for c in ch)
    qxx = qxy = qyy = 0.0
    for (x, y, q) in ch:
        dx, dy = x - cx, y - cy
        d2 = dx * dx + dy * dy
        qxx += q * (3 * dx * dx - d2)
        qxy += q * (3 * dx * dy)
        qyy += q * (3 * dy * dy - d2)
    return (cx, cy), Q, (px, py), (qxx, qxy, qyy)


def legendre(lmax, x):
    p = [1.0, x]
    for l in range(1, lmax):
        p.append(((2 * l + 1) * x * p[l] - l * p[l - 1]) / (l + 1))
    return p[:lmax + 1]


def series_coeffs(ch, th, lmax):
    """c_l with V(c + r n) = sum_l c_l / r^(l+1) (r > max |d_i|), Legendre route."""
    cx, cy = centre(ch)
    n = (math.cos(th), math.sin(th))
    cs = [0.0] * (lmax + 1)
    for (x, y, q) in ch:
        dx, dy = x - cx, y - cy
        d = math.hypot(dx, dy)
        if d == 0.0:
            cs[0] += KNC * q
            continue
        cg = (dx * n[0] + dy * n[1]) / d
        pl = legendre(lmax, cg)
        for l in range(lmax + 1):
            cs[l] += KNC * q * d ** l * pl[l]
    return cs


P('')
P('# multipoles about the expansion centre (centre of charge if Q != 0, else the mean position)')
P('# preset, cx, cy, Q, px, py, Qxx, Qxy, Qyy')
for nm in ORDER:
    (cx, cy), Q, (px, py), (qxx, qxy, qyy) = moments(PRESETS[nm])
    P('MOM', nm, g(cx), g(cy), g(Q), g(px), g(py), g(qxx), g(qxy), g(qyy))

# every charged preset has sum(q y) = 0 (and single/like/triangle sum(q x) = 0), so a
# centre of charge computed wrongly in y (or x) would still come out 0 for all of them:
# an asymmetric charged set where the right and wrong centres differ -- with Q = 2,
# not 1: dividing by Q = 1 changes nothing, which would hide the same mutant again
ASYM = [(0.3, 0.8, 1.0), (-0.4, -0.2, 1.0), (1.1, -0.6, 1.0), (-0.9, 0.5, -1.0)]
(cx, cy), Q, (px, py), (qxx, qxy, qyy) = moments(ASYM)
P('ASYM_MOM', g(cx), g(cy), g(Q), g(px), g(py), g(qxx), g(qxy), g(qyy))
P('ASYM_SER30', ' '.join(g(c) for c in series_coeffs(ASYM, math.radians(30.0), 4)))

P('')
P('# Legendre-series coefficients along rays: preset, theta(deg), c0..c4 ; and the tensor route for c0..c2')
for nm in ORDER:
    ch = PRESETS[nm]
    (cx, cy), Q, (px, py), (qxx, qxy, qyy) = moments(ch)
    for tdeg in (0.0, 30.0, 90.0, 137.0):
        th = math.radians(tdeg)
        n = (math.cos(th), math.sin(th))
        cs = series_coeffs(ch, th, 4)
        t0 = KNC * Q
        t1 = KNC * (px * n[0] + py * n[1])
        t2 = KNC * 0.5 * (qxx * n[0] ** 2 + 2 * qxy * n[0] * n[1] + qyy * n[1] ** 2)
        assert abs(cs[0] - t0) < 1e-12 * max(1, abs(t0))
        assert abs(cs[1] - t1) < 1e-12 * max(1, abs(t1)), (nm, tdeg, cs[1], t1)
        assert abs(cs[2] - t2) < 1e-12 * max(1, abs(t2)), (nm, tdeg, cs[2], t2)
        P('SER', nm, g(tdeg), ' '.join(g(c) for c in cs))

P('')
P('# far-field limits taken numerically: f(r) = r^(l0+1) V(c + r n); Richardson (4 f(2r) - f(r))/3 at r = 50')
P('# (the first correction is 2 orders down for the symmetric dipole and the square quadrupole, 2 for the like pair)')
FAR = [('dipole', 30.0, 1), ('quad', 30.0, 2), ('like', 30.0, 0), ('rows', 60.0, 1), ('triangle', 20.0, 0)]
for (nm, tdeg, l0) in FAR:
    ch = PRESETS[nm]
    cx, cy = centre(ch)
    th = math.radians(tdeg)
    n = (math.cos(th), math.sin(th))

    def f(r):
        return r ** (l0 + 1) * V(ch, cx + r * n[0], cy + r * n[1])
    cs = series_coeffs(ch, th, 6)
    fr = [f(r) for r in (25.0, 50.0, 100.0, 200.0)]
    rich = (4 * f(100.0) - f(50.0)) / 3
    rate = (f(50.0) - cs[l0]) / (f(100.0) - cs[l0])
    P('FAR', nm, g(tdeg), l0, 'limit', g(cs[l0]), 'f25', g(fr[0]), 'f50', g(fr[1]), 'f100', g(fr[2]),
      'rich50_100', g(rich), 'rate', g(rate))
# the dipole limit in closed form: k p cos(theta), p = 1 nC m along +x
P('DIPOLE_CLOSED', g(KNC * 1.0 * math.cos(math.radians(30.0))))
# the square quadrupole: V ~ k (1/2) n.Q.n / r^3 with Qxy = 3 sum q x y = 3 (0.25+0.25+0.25+0.25) = 3
P('QUAD_CLOSED', g(KNC * 0.5 * 2 * 3.0 * math.cos(math.radians(30)) * math.sin(math.radians(30))))
# the series converges to V beyond max |d_i|: partial sum to l = 40 at r = 2 max|d|
for nm in ('dipole', 'quad', 'rows'):
    ch = PRESETS[nm]
    cx, cy = centre(ch)
    dmax = max(math.hypot(c[0] - cx, c[1] - cy) for c in ch)
    th = math.radians(137.0)
    r = 2.0 * dmax
    cs = series_coeffs(ch, th, 60)
    ps = sum(cs[l] / r ** (l + 1) for l in range(61))
    ex = V(ch, cx + r * math.cos(th), cy + r * math.sin(th))
    P('SERIES_CONV', nm, 'dmax', g(dmax), 'r', g(r), 'partial60', g(ps), 'exact', g(ex), 'rel', '%.2e' % (abs(ps - ex) / abs(ex)))

# ---------------------------------------------------------------- the tape: int E.dl = V(A) - V(B)
P('')
P('# the tape: line integral of E from A to B against V(A) - V(B)')
TAPES = [('dipole', (-1.5, 1.0), (2.0, -1.3)), ('rows', (-2.0, -0.3), (1.7, 0.4)), ('quad', (-1.0, -1.2), (1.3, 0.9))]
for (nm, A, B) in TAPES:
    ch = PRESETS[nm]
    L = math.hypot(B[0] - A[0], B[1] - A[1])
    t = ((B[0] - A[0]) / L, (B[1] - A[1]) / L)
    I = integrate.quad(lambda s: (lambda e: e[0] * t[0] + e[1] * t[1])(E(ch, A[0] + s * t[0], A[1] + s * t[1])),
                       0, L, epsabs=1e-12, epsrel=1e-12, limit=400)[0]
    def seg_dist(c):
        s_ = max(0.0, min(L, (c[0] - A[0]) * t[0] + (c[1] - A[1]) * t[1]))
        return math.hypot(A[0] + s_ * t[0] - c[0], A[1] + s_ * t[1] - c[1])
    dmin = min(seg_dist(c) for c in ch)
    P('TAPE', nm, 'A', g(A[0]), g(A[1]), 'B', g(B[0]), g(B[1]), 'length', g(L), 'int', g(I), 'VA_minus_VB', g(V(ch, A[0], A[1]) - V(ch, B[0], B[1])),
      'closest_approach', g(dmin))

# ---------------------------------------------------------------- superposition at a probe
P('')
P('# superposition, rows preset at (0.3, 0.2): per-charge V_i, E_i (first three and the sums)')
ch = PRESETS['rows']
x, y = 0.3, 0.2
sv, sx, sy = 0.0, 0.0, 0.0
for i, c in enumerate(ch):
    vi = V([c], x, y)
    ei = E([c], x, y)
    sv += vi
    sx += ei[0]
    sy += ei[1]
    if i < 3 or i == 10:
        P('SUP', i, g(vi), g(ei[0]), g(ei[1]))
P('SUPSUM', g(sv), g(sx), g(sy), 'direct', g(V(ch, x, y)), g(E(ch, x, y)[0]), g(E(ch, x, y)[1]))

# ---------------------------------------------------------------- the field between the rows
P('')
P('# rows: the field at the centre and its uniformity along x between the rows (|E(x,0)|/|E(0,0)|)')
e0 = E(ch, 0.0, 0.0)
P('ROWS_E0', g(e0[0]), g(e0[1]))
for xx in (0.5, 1.0, 1.5, 2.5):
    e = E(ch, xx, 0.0)
    P('ROWS_UNIF', g(xx), g(math.hypot(e[0], e[1]) / math.hypot(e0[0], e0[1])))

# ---------------------------------------------------------------- PhET-rule values
P('')
P('# PhET readings for comparison: V at 1 m from +1 nC with K = 9, and here')
P('PHET_V1M', g(K_PHET), 'HERE', g(KNC))

io_path = sys.argv[1] if len(sys.argv) > 1 else 'refvals.txt'
with open(io_path, 'w') as fh:
    fh.write('\n'.join(OUT) + '\n')
print('\n'.join(OUT))
