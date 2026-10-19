#!/usr/bin/env python3
"""derive.py — the Python twin of calculus-grapher.html.

Three jobs, in this order:

  A.  READ PhET's own constants out of its minified build
      (docs/phets/calculus-grapher_en.html) with regexes, so no number in
      this file is typed from memory.  Everything it finds is printed with
      the text it was found in.

  B.  RE-DERIVE the discrete calculus this remake uses, and FALSIFY it:
        * the fundamental theorem, both ways, to machine precision;
        * every analytic curve mode's derivative and integral against the
          CLOSED FORMS (sympy/scipy), with the discretisation error measured
          and its O(dx^2) rate confirmed by halving dx;
        * the one-sided limits at every corner, which is the only honest
          statement at a point where the derivative does not exist;
        * the tangent tool's slope and the area tool's value against the
          curves they are supposed to agree with, by INDEPENDENT routes;
        * PhET's own operator pair (central difference + trapezium), which
          is NOT exactly inverse -- d/dx of its integral is the [1,2,1]/4
          smoothing of f -- proved as an identity.

  C.  PRINT reference values to 15+ digits into refvals.txt, which
      make_refs.py turns into p7_refs.js.  selfTest asserts against those
      printed lines and nothing else.

    python3 derive.py            # prints the whole report, writes refvals.txt
"""
import io
import math
import os
import re
import sys

import numpy as np
from scipy import integrate, special, optimize

HERE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'phets', 'calculus-grapher_en.html'))

REFS = []          # (name, value, note)


def ref(name, val, note=''):
    REFS.append((name, val, note))
    return val


def head(t):
    print('\n=== %s ===' % t)


# ====================================================================== #
#  A.  PhET's constants, read out of its build                           #
# ====================================================================== #
head('A  PhET constants, read out of calculus-grapher_en.html')
SRC = io.open(ORIG, encoding='utf-8', errors='replace').read()
print('source: %s  (%.2f MB)' % (ORIG, len(SRC) / 1048576))


def grab(pat, what, group=1):
    m = re.search(pat, SRC)
    assert m, 'NOT FOUND in PhET build: %s  (%s)' % (what, pat)
    return m


m = grab(r'(\w+)=new (\w+)\(0,10\),(\w+)=\1\.getLength\(\),(\w+)=\.1\*\3,(\w+)=\3\*\4;',
         'CURVE_X_RANGE / TYPICAL_Y')
XMIN, XMAX = 0.0, 10.0
XLEN = XMAX - XMIN
TYPICAL_Y = 0.1 * XLEN
print('  CURVE_X_RANGE            = (%g, %g)      %s' % (XMIN, XMAX, m.group(0)[:60]))
print('  TYPICAL_Y                = %g' % TYPICAL_Y)

NPTS = int(grab(r'numberOfPoints:\{type:"number",isValidValue:e=>e>0,defaultValue:(\d+)\}',
                'numberOfPoints').group(1))
SMOOTH_SIGMA = float(grab(r'smoothingStandardDeviation:\{type:"number",isValidValue:e=>e>0,'
                          r'defaultValue:([\d.]+)\*\w+\.CURVE_X_RANGE\.getLength\(\)\}',
                          'smoothingStandardDeviation').group(1)) * XLEN
EDGE_SLOPE = float(grab(r'edgeSlopeFactor:\{type:"number",isValidValue:e=>e>=0,'
                        r'defaultValue:([\d.]+)\*\w+\.CURVE_X_RANGE\.getLength\(\)\}',
                        'edgeSlopeFactor').group(1)) * XLEN
MAX_TILT = float(grab(r'maxTilt:\{type:"number",isValidValue:e=>e>0,defaultValue:(\d+)\}',
                      'maxTilt').group(1))
mw = grab(r'CURVE_MANIPULATION_WIDTH_RANGE=new \w+\(([\d.]+)\*\w+,([\d.]+)\*\w+,([\d.]+)\*\w+\)',
          'CURVE_MANIPULATION_WIDTH_RANGE')
W_MIN, W_MAX, W_DEF = (float(mw.group(i)) * XLEN for i in (1, 2, 3))
my = grab(r'CURVE_MANIPULATION_Y_RANGE=new \w\((-?\d+),(-?\d+)\)', 'CURVE_MANIPULATION_Y_RANGE')
Y_MIN, Y_MAX = float(my.group(1)), float(my.group(2))
ms = grab(r'SLOPE_OF_TANGENT_MODEL_RANGE=new \w\((-?\d+),(-?\d+)\)', 'SLOPE_OF_TANGENT_MODEL_RANGE')
SLOPE_MIN, SLOPE_MAX = float(ms.group(1)), float(ms.group(2))
ma = grab(r'NET_SIGNED_AREA_MODEL_RANGE=new \w\(-([\d.]+)\*\w+,([\d.]+)\*\w+\)',
          'NET_SIGNED_AREA_MODEL_RANGE')
AREA_MAX = float(ma.group(2)) * (XLEN * TYPICAL_Y)
MAX_UNDO = int(grab(r'MAX_UNDO=(\d+)', 'MAX_UNDO').group(1))
FREEFORM_W = XLEN / 40.0
grab(r'\w+=\w+\.CURVE_X_RANGE\.getLength\(\)/40', 'freeform single-click hill width')

DX = XLEN / (NPTS - 1)
print('  numberOfPoints           = %d   -> dx = %.17g' % (NPTS, DX))
print('  smoothingStandardDeviation = %.17g   (0.005 x the x range)' % SMOOTH_SIGMA)
print('  edgeSlopeFactor          = %.17g   (0.04 x the x range)' % EDGE_SLOPE)
print('  maxTilt                  = %g' % MAX_TILT)
print('  CURVE_MANIPULATION_WIDTH_RANGE = [%g, %g] default %g' % (W_MIN, W_MAX, W_DEF))
print('  CURVE_MANIPULATION_Y_RANGE     = (%g, %g)' % (Y_MIN, Y_MAX))
print('  SLOPE_OF_TANGENT_MODEL_RANGE   = (%g, %g)' % (SLOPE_MIN, SLOPE_MAX))
print('  NET_SIGNED_AREA_MODEL_RANGE    = (%g, %g)' % (-AREA_MAX, AREA_MAX))
print('  MAX_UNDO                 = %d' % MAX_UNDO)
print('  freeform click width     = %g' % FREEFORM_W)

# the shape formulas themselves, confirmed present in the build
FORMS = [
    ('hill Gaussian',    r'Math\.exp\(-Math\.pow\(\(t\.x-r\.x\)/\(e/\(2\*Math\.sqrt\(2\)\)\),2\)\)'),
    ('triangle slope',   r'(\w+)=DR/\(e/2\)'),
    ('parabola curv.',   r'(\w+)=DR\*Math\.pow\(2/e,2\)'),
    ('pedestal quartic', r'Math\.exp\(-1\*\(\(e-t\)/xR\)\*\*4\)'),
    ('pedestal plateau', r'(\w+)=e-2\*xR'),
    ('sinusoid period',  r'2\*Math\.PI\*e/\w+\.CURVE_MANIPULATION_WIDTH_RANGE\.defaultValue'),
    ('sinusoid extent',  r'(\w+)=(\w+)/2\*7,(\w+)=\2/8'),
    ('sinusoid taper',   r'Math\.cos\(Math\.PI/2\*\(e\.x-t\)/Math\.abs\(i-t\)\)\*\*2'),
    ('blend threshold',  r'(\w+)\.y=(\w+)>1e-8\?\2\*(\w+)\+\(1-\2\)\*\1\.lastSavedY:\1\.lastSavedY'),
    ('smooth type',      r'\w+\.pointType=\w+>\.999\?"smooth"'),
    ('smooth kernel',    r'1/\(ER\*Math\.sqrt\(2\*Math\.PI\)\)'),
    ('smooth window',    r'for\(let \w+=this\.deltaX;\w+<=3\*ER;\w+\+=this\.deltaX\)'),
    ('region-zero tol',  r'Math\.abs\(\w+\.lastSavedY\)<\.001'),
    ('PhET derivative',  r'"number"==typeof \w+&&"number"==typeof \w+\?this\.points\[\w+\]\.y=\(\w+\+\w+\)/2'),
    ('PhET integral',    r'\.5\*\(\w+\.y\+\w+\.y\)\*\(\w+\.x-\w+\.x\)'),
    ('PhET 2nd deriv',   r'\(\w+\.getSlope\(\w+\)-\w+\.getSlope\(\w+\)\)/this\.deltaX'),
]
for name, pat in FORMS:
    mm = grab(pat, name)
    print('  %-18s %s' % (name, mm.group(0)[:78]))

for n, v, note in [('XMIN', XMIN, "PhET's CURVE_X_RANGE"), ('XMAX', XMAX, "PhET's CURVE_X_RANGE"),
                   ('NPTS', NPTS, "PhET's numberOfPoints"), ('DX', DX, 'x range / (NPTS - 1)'),
                   ('TYPICAL_Y', TYPICAL_Y, "PhET's TYPICAL_Y"),
                   ('SMOOTH_SIGMA', SMOOTH_SIGMA, "PhET's smoothingStandardDeviation"),
                   ('EDGE_SLOPE', EDGE_SLOPE, "PhET's edgeSlopeFactor"),
                   ('MAX_TILT', MAX_TILT, "PhET's maxTilt"),
                   ('W_MIN', W_MIN, "PhET's width range"), ('W_MAX', W_MAX, "PhET's width range"),
                   ('W_DEF', W_DEF, "PhET's default width"),
                   ('Y_MIN', Y_MIN, "PhET's CURVE_MANIPULATION_Y_RANGE"),
                   ('Y_MAX', Y_MAX, "PhET's CURVE_MANIPULATION_Y_RANGE"),
                   ('SLOPE_MAX', SLOPE_MAX, "PhET's tangent barometer range"),
                   ('AREA_MAX', AREA_MAX, "PhET's area barometer range"),
                   ('MAX_UNDO', MAX_UNDO, "PhET's undo depth"),
                   ('FREEFORM_W', FREEFORM_W, "PhET's single-click hill width")]:
    ref(n, v, note)

X = XMIN + np.arange(NPTS) * DX        # exactly how the JS builds it
assert abs(X[-1] - XMAX) < 1e-12


# ====================================================================== #
#  B1.  the discrete calculus                                            #
# ====================================================================== #
def idx_at(x, n=NPTS, xmin=XMIN, xlen=XLEN):
    """PhET's getClosestIndexAt: normalise, scale, round, clamp.

    PhET rounds with Utils.roundSymmetric (half AWAY FROM ZERO), which for
    the non-negative indices here is JavaScript's Math.round.  Python's
    built-in round() is banker's rounding and returns 312 for 312.5 where
    Math.round returns 313 -- a one-node difference that moved the twin's
    two-hill areas by 3.2e-7 and was found by the JS suite disagreeing with
    this file.  Do not "simplify" this back to round()."""
    t = (x - xmin) / xlen
    return int(min(max(math.floor(t * (n - 1) + 0.5), 0), n - 1))


def deriv(f, dx=DX):
    """f on nodes -> f' on CELLS.  This is the EXACT derivative of the
    piecewise-linear curve the sim draws, constant on each cell, evaluated
    at the cell midpoint."""
    return (f[1:] - f[:-1]) / dx


def integ_cells(g, dx=DX):
    """a CELL function -> its integral on the nodes (left Riemann over the
    cells, which is exact for a piecewise-constant integrand)."""
    out = np.zeros(len(g) + 1)
    out[1:] = np.cumsum(g) * dx
    return out


def integ(f, dx=DX):
    """f on nodes -> its integral on the nodes: the cumulative trapezium,
    which is the EXACT integral of the piecewise-linear curve."""
    out = np.zeros(len(f))
    out[1:] = np.cumsum(0.5 * (f[1:] + f[:-1]) * dx)
    return out


def deriv2(f, dx=DX):
    """f'' on nodes from the cell slopes.  Interior only; the two ends copy
    their neighbour, as PhET's does."""
    d = deriv(f, dx)
    out = np.zeros(len(f))
    out[1:-1] = (d[1:] - d[:-1]) / dx
    out[0] = out[1]
    out[-1] = out[-2]
    return out


def phet_deriv(f, dx=DX):
    """PhET's derivative: the mean of the two one-sided slopes, on the NODES."""
    out = np.zeros(len(f))
    out[1:-1] = 0.5 * ((f[1:-1] - f[:-2]) / dx + (f[2:] - f[1:-1]) / dx)
    out[0] = (f[1] - f[0]) / dx
    out[-1] = (f[-1] - f[-2]) / dx
    return out


head('B1  the fundamental theorem on the grid')
rng = np.random.default_rng(20260922)
ftc_max = 0.0
ftc2_max = 0.0
ftc3_max = 0.0
for trial in range(6):
    f = rng.normal(size=NPTS) * 0.7 + np.sin(3 * X) * 1.3
    # (i)  integrate the derivative -> f, up to f(0)
    back = integ_cells(deriv(f))
    ftc_max = max(ftc_max, float(np.max(np.abs(back - (f - f[0])))))
    # (ii) differentiate the cell integral -> the same cell function
    g = rng.normal(size=NPTS - 1)
    ftc2_max = max(ftc2_max, float(np.max(np.abs(deriv(integ_cells(g)) - g))))
    # (iii) differentiate the trapezium integral -> f at the cell midpoints,
    #       which for a piecewise-linear curve is the mean of the two nodes
    ftc3_max = max(ftc3_max, float(np.max(np.abs(deriv(integ(f)) - 0.5 * (f[1:] + f[:-1])))))
print('  max |int(f\') - (f - f(0))|              = %.3e   (6 random curves)' % ftc_max)
print('  max |d/dx int(g) - g|                   = %.3e' % ftc2_max)
print('  max |d/dx trap(f) - (f[i]+f[i+1])/2|    = %.3e' % ftc3_max)
assert ftc_max < 2e-12 and ftc2_max < 2e-12 and ftc3_max < 2e-12
print('  -> the two operators are inverse to each other in floating point,')
print('     and the "value" the derivative of the integral returns is f at the')
print('     cell midpoint -- which is EXACT for a piecewise-linear curve, not')
print('     an approximation (the mean value theorem, with the mean value')
print('     sitting at the midpoint of a straight segment).')
ref('FTC_BACK_TOL', 2e-12, 'int(f\') - (f - f(0)), 1251 nodes')

head('B2  PhET\'s pair is not exactly inverse: the [1,2,1]/4 identity')
worst = 0.0
for trial in range(6):
    f = rng.normal(size=NPTS) * 0.9
    pd = phet_deriv(integ(f))
    want = 0.25 * (f[:-2] + 2 * f[1:-1] + f[2:])
    worst = max(worst, float(np.max(np.abs(pd[1:-1] - want))))
print('  max |D_central(I_trap(f))[i] - (f[i-1]+2f[i]+f[i+1])/4| = %.3e' % worst)
assert worst < 2e-12
print('  So PhET\'s central difference of its trapezium integral returns the')
print('  [1,2,1]/4 smoothing of f, not f.  The difference is O(dx^2 f") and is')
print('  invisible on its graphs; it is named here because this remake chose the')
print('  staggered pair instead, for which the theorem is exact.')
ref('PHET_SMOOTHER_TOL', 2e-12, 'D_central(I_trap(f)) = [1,2,1]/4 f')


# ====================================================================== #
#  B3.  the curve-manipulation modes, exactly as PhET defines them       #
# ====================================================================== #
def region_zero(fs, a, b, x=None):
    x = X if x is None else x
    sel = (x >= a) & (x <= b)
    return bool(np.all(np.abs(fs[sel]) < 0.001)) if sel.any() else True


def manipulate(fs, mode, w, x0, y, x=None, npts=None, dx=None):
    """PhET's TransformedCurve, one shape at a time, from a SAVED curve fs."""
    x = X if x is None else x
    npts = NPTS if npts is None else npts
    dx = DX if dx is None else dx
    i0 = idx_at(x0, npts)
    xc = x[i0]
    f = fs.copy()
    corner = np.zeros(npts, dtype=bool)
    if mode == 'hill':
        P = np.exp(-((x - xc) / (w / (2 * math.sqrt(2)))) ** 2)
        f = np.where(P > 1e-8, P * y + (1 - P) * fs, fs)
    elif mode == 'pedestal':
        e = EDGE_SLOPE
        s = w - 2 * e
        inner = np.abs(x - xc) < s / 2
        left = np.exp(-(((x - (xc - s / 2)) / e) ** 4))
        right = np.exp(-(((x - (xc + s / 2)) / e) ** 4))
        P = np.where(inner, 1.0, np.where(x <= xc, left, right))
        f = np.where(P > 1e-8, P * y + (1 - P) * fs, fs)
    elif mode in ('triangle', 'parabola'):
        delta = y - fs[i0]
        if mode == 'triangle':
            s = TYPICAL_Y / (w / 2)
            g = y - np.sign(delta) * s * np.abs(x - xc)
        else:
            s = TYPICAL_Y * (2.0 / w) ** 2
            g = y - np.sign(delta) * s * (x - xc) ** 2
        take = (g > fs) if delta > 0 else (g < fs)
        f = np.where(take, g, fs)
        sw = np.flatnonzero(take[1:] != take[:-1])
        corner[sw] = True
        corner[sw + 1] = True
        if mode == 'triangle':
            corner[i0] = True
            corner[min(i0 + 1, npts - 1)] = True
    elif mode == 'sinusoid':
        lam = 2 * math.pi * w / W_DEF
        o = lam / 2 * 7
        a = lam / 8
        lr = xc + o / 2
        hl = xc - o / 2
        c = lr if lr > XMAX else x[idx_at(lr, npts)]
        u = hl if hl < XMIN else x[idx_at(hl, npts)]
        d = c - a
        p = u + a
        gz = region_zero(fs, u, p, x)
        mz = region_zero(fs, d, c, x)
        T = np.zeros(npts)
        T[(x >= p) & (x <= d)] = 1.0
        sl = (x > u) & (x < p)
        T[sl] = 1.0 if gz else np.cos(math.pi / 2 * (x[sl] - p) / abs(u - p)) ** 2
        sr = (x > d) & (x < c)
        T[sr] = 1.0 if mz else np.cos(math.pi / 2 * (x[sr] - d) / abs(c - d)) ** 2
        f = T * (y * np.cos(2 * math.pi * (xc - x) / lam)) + (1 - T) * fs
        if gz and hl > XMIN:
            k = idx_at(u, npts)
            corner[k] = True
            corner[min(k + 1, npts - 1)] = True
        if mz and lr < XMAX:
            k = idx_at(c, npts)
            corner[k] = True
            corner[max(k - 1, 0)] = True
    elif mode == 'tilt':
        r = xc - x[0]
        if r != 0:
            slope = (y - fs[0]) / r
            if abs(slope) < MAX_TILT:
                t = (y - fs[i0]) / r
                f = fs + t * (x - x[0])
    elif mode == 'shift':
        f = fs + (y - fs[i0])
    else:
        raise ValueError(mode)
    return f, corner


# ---- the closed forms -------------------------------------------------- #
def closed(mode, w, xc, y):
    """(g, gp, G) for a shape laid on an EMPTY curve: the value, the exact
    derivative, and the exact integral from XMIN.  G is elementary where one
    exists and quadrature of g where it is not (the pedestal)."""
    if mode == 'hill':
        a = 8.0 / w ** 2                                     # exp(-a u^2)
        k = 0.5 * math.sqrt(math.pi / a)
        def g(t):
            return y * np.exp(-a * (t - xc) ** 2)
        def gp(t):
            return -2 * a * (t - xc) * y * np.exp(-a * (t - xc) ** 2)
        def G(t):
            return y * k * (special.erf(math.sqrt(a) * (t - xc))
                            - special.erf(math.sqrt(a) * (XMIN - xc)))
        return g, gp, G, []
    if mode == 'triangle':
        s = TYPICAL_Y / (w / 2) * (1 if y > 0 else -1)
        r = abs(y) / abs(s)
        def g(t):
            return np.where(np.abs(t - xc) < r, y - s * np.abs(t - xc), 0.0)
        def gp(t):
            return np.where(np.abs(t - xc) < r, -s * np.sign(t - xc), 0.0)
        def G(t):
            t = np.asarray(t, dtype=float)
            u = np.clip(t - xc, -r, r)
            lo = max(XMIN - xc, -r)
            def prim(uu):
                return y * uu - s * np.sign(uu) * uu ** 2 / 2
            return prim(u) - prim(lo)
        return g, gp, G, [xc - r, xc, xc + r]
    if mode == 'parabola':
        s = TYPICAL_Y * (2.0 / w) ** 2 * (1 if y > 0 else -1)
        r = math.sqrt(abs(y) / abs(s))
        def g(t):
            return np.where(np.abs(t - xc) < r, y - s * (t - xc) ** 2, 0.0)
        def gp(t):
            return np.where(np.abs(t - xc) < r, -2 * s * (t - xc), 0.0)
        def G(t):
            t = np.asarray(t, dtype=float)
            u = np.clip(t - xc, -r, r)
            lo = max(XMIN - xc, -r)
            def prim(uu):
                return y * uu - s * uu ** 3 / 3
            return prim(u) - prim(lo)
        return g, gp, G, [xc - r, xc + r]
    if mode == 'pedestal':
        e = EDGE_SLOPE
        half = (w - 2 * e) / 2
        def P(t):
            a = np.abs(t - xc)
            return np.where(a < half, 1.0, np.exp(-(((a - half) / e) ** 4)))
        def g(t):
            return y * P(t)
        def gp(t):
            a = np.abs(t - xc)
            q = (a - half) / e
            return np.where(a < half, 0.0,
                            y * (-4 * q ** 3 / e) * np.exp(-(q ** 4)) * np.sign(t - xc))
        # closed form: int_0^T exp(-s^4) ds = gamma(1/4) P(1/4, T^4) / 4
        gam = special.gamma(0.25) / 4.0
        def G(t):
            t = np.atleast_1d(np.asarray(t, dtype=float))
            out = np.empty_like(t)
            for i, tv in enumerate(t):
                out[i] = integrate.quad(lambda z: float(g(np.array([z]))[0]), XMIN, tv,
                                        points=[xc - half, xc, xc + half], limit=200)[0]
            return out if out.size > 1 else float(out[0])
        def Gclosed(t):
            """the same integral in closed form, for the tail pieces."""
            t = float(t)
            def tail(a):           # int over |u| from half to half+a of exp(-((u-half)/e)^4)
                return e * gam * special.gammainc(0.25, (a / e) ** 4)
            def H(u):
                if u <= -half:
                    return -half - tail(-u - half)
                if u <= half:
                    return u
                return half + tail(u - half)
            return y * (H(t - xc) - H(XMIN - xc))
        return g, gp, G, [], Gclosed
    if mode == 'sinusoid':
        lam = 2 * math.pi * w / W_DEF
        o = lam / 2 * 7
        lr = xc + o / 2
        hl = xc - o / 2
        c = lr if lr > XMAX else X[idx_at(lr)]
        u = hl if hl < XMIN else X[idx_at(hl)]
        k = 2 * math.pi / lam
        def g(t):
            return np.where((t > u) & (t < c), y * np.cos(k * (xc - t)), 0.0)
        def gp(t):
            # d/dt [y cos(k(xc - t))] = + y k sin(k(xc - t)).  The sign was
            # wrong on the first pass and the closed-form check caught it at
            # 2.000 = twice the slope amplitude y k.
            return np.where((t > u) & (t < c), y * k * np.sin(k * (xc - t)), 0.0)
        def G(t):
            t = np.asarray(t, dtype=float)
            tt = np.clip(t, u, c)
            lo = min(max(XMIN, u), c)
            def prim(z):
                return -y / k * np.sin(k * (xc - z))
            return prim(tt) - prim(lo)
        return g, gp, G, [u, c]
    raise ValueError(mode)


head('B3  the five analytic modes against their closed forms')
print('  dx = %.6g.  The cell derivative is the EXACT derivative of the drawn' % DX)
print('  piecewise-linear curve; against the SMOOTH shape it carries the')
print('  Euler-Maclaurin term g\'\'\'(x) dx^2/24, and the trapezium integral carries')
print('  -(g\'(b) - g\'(a)) dx^2/12.  Both are measured, not assumed.')
MODES = [('hill', W_DEF, 3.0, 1.5), ('triangle', W_DEF, 4.0, 1.5),
         ('pedestal', 3.0, 5.0, 1.2), ('parabola', 2.5, 6.0, -1.4),
         ('sinusoid', 2.0, 5.0, 1.0)]
zero = np.zeros(NPTS)
errtab = {}
for mode, w, x0, y in MODES:
    f, corner = manipulate(zero, mode, w, x0, y)
    got = closed(mode, w, X[idx_at(x0)], y)
    g, gp, G = got[0], got[1], got[2]
    breaks = got[3]
    d = deriv(f)
    xm = X[:-1] + DX / 2
    F = integ(f)
    # exclude the cells that straddle a corner or the 1e-8 blend edge
    keep = np.ones(NPTS - 1, dtype=bool)
    for b in breaks:
        keep &= np.abs(xm - b) > 2 * DX
    if mode in ('hill', 'pedestal'):          # PhET's 1e-8 cut makes a tiny step
        keep &= np.abs(g(xm)) > 1e-6 * abs(y)
    ed = float(np.max(np.abs(d[keep] - gp(xm[keep]))))
    keepF = np.ones(NPTS, dtype=bool)
    for b in breaks:
        keepF &= np.abs(X - b) > 2 * DX
    if mode == 'pedestal':
        Gx = np.array([got[4](t) for t in X])
        chk = float(np.max(np.abs(Gx[::125] - np.atleast_1d(G(X[::125])))))
        print('  pedestal: closed form (incomplete gamma) vs quadrature: %.2e' % chk)
        assert chk < 1e-10
    else:
        Gx = np.atleast_1d(G(X))
    eF = float(np.max(np.abs(F[keepF] - Gx[keepF])))
    errtab[mode] = (ed, eF)
    print('  %-9s w=%.2f x0=%.2f y=%+.2f :  max|f\'-g\'| = %.3e   max|F-G| = %.3e'
          % (mode, w, x0, y, ed, eF))
    ref('ERR_D_' + mode.upper(), ed, 'max |cell derivative - closed form| at PhET\'s grid')
    ref('ERR_I_' + mode.upper(), eF, 'max |trapezium - closed form| at PhET\'s grid')

print('\n  the triangle and the parabola are special:')
f, _ = manipulate(zero, 'triangle', W_DEF, 4.0, 1.5)
g, gp, G, breaks = closed('triangle', W_DEF, X[idx_at(4.0)], 1.5)
d = deriv(f)
xm = X[:-1] + DX / 2
keep = np.ones(NPTS - 1, dtype=bool)
for b in breaks:
    keep &= np.abs(xm - b) > 1.01 * DX
tri_d = float(np.max(np.abs(d[keep] - gp(xm[keep]))))
tri_i = float(np.max(np.abs(integ(f) - np.atleast_1d(G(X)))))
s_tri = TYPICAL_Y / (W_DEF / 2)
bound = 2 * s_tri * DX ** 2 / 8            # one per junction, worst offset dx/2
print('    triangle  (piecewise LINEAR): derivative exact to %.2e' % tri_d)
print('    its integral is the EXACT integral of the drawn curve; against the')
print('    ideal triangle it differs by %.3e, which is not a quadrature error at' % tri_i)
print('    all but the two junction cells: the sampled curve runs to zero over a')
print('    whole cell instead of stopping at the junction, worth s d (dx - d) / 2')
print('    per junction, at most 2 x s dx^2 / 8 = %.3e.' % bound)
assert tri_d < 1e-12 and tri_i < bound * 1.001
ref('TRI_D_EXACT', tri_d, 'a piecewise-linear curve: the cell derivative is exact')
ref('TRI_I_JUNCTION', tri_i, 'trapezium vs the ideal triangle: the two junction cells')
ref('TRI_I_BOUND', bound, '2 s dx^2 / 8, the worst-case junction-cell area')

f, _ = manipulate(zero, 'parabola', 2.5, 6.0, -1.4)
g, gp, G, breaks = closed('parabola', 2.5, X[idx_at(6.0)], -1.4)
d = deriv(f)
keep = np.ones(NPTS - 1, dtype=bool)
for b in breaks:
    keep &= np.abs(xm - b) > 1.01 * DX
par_d = float(np.max(np.abs(d[keep] - gp(xm[keep]))))
print('    parabola  (QUADRATIC): the cell derivative is exact to %.2e,' % par_d)
assert par_d < 1e-12
ref('PAR_D_EXACT', par_d, 'a quadratic: the cell-centred difference is exact')
# and its trapezium error is EXACTLY the Euler-Maclaurin term
s_par = TYPICAL_Y * (2.0 / 2.5) ** 2 * (-1)
xa, xb = 5.4, 6.4
ia, ib = idx_at(xa), idx_at(xb)
trap_ab = integ(f)[ib] - integ(f)[ia]
exact_ab = float(np.atleast_1d(G(X[ib]))[0] - np.atleast_1d(G(X[ia]))[0])
# Euler-Maclaurin: T - I = +h^2/12 (g'(b) - g'(a)) + O(h^4).  The sign was
# written the other way round on the first pass and this check caught it.
em = DX ** 2 / 12 * (gp(np.array([X[ib]]))[0] - gp(np.array([X[ia]]))[0])
print('              and over [%.3f, %.3f] its trapezium error is %.6e' % (X[ia], X[ib], trap_ab - exact_ab))
print('              against the Euler-Maclaurin term +dx^2/12 (g\'(b)-g\'(a)) = %.6e' % em)
print('              difference %.3e  -- the expansion TERMINATES for a quadratic'
      % abs((trap_ab - exact_ab) - em))
assert abs((trap_ab - exact_ab) - em) < 1e-15
ref('PAR_TRAP_ERR', trap_ab - exact_ab, 'trapezium error over [5.4, 6.4] of the parabola')
ref('PAR_EM_TERM', em, '+dx^2/12 (g\'(b) - g\'(a)), the exact Euler-Maclaurin term')
ref('PAR_XA', X[ia], '')
ref('PAR_XB', X[ib], '')

head('B4  the discretisation error is O(dx^2): halve dx, quarter the error')
for mode, w, x0, y in [('hill', W_DEF, 3.0, 1.5), ('sinusoid', 2.0, 5.0, 1.0),
                       ('pedestal', 3.0, 5.0, 1.2)]:
    row = []
    for mult in (1, 2, 4, 8):
        n = (NPTS - 1) * mult + 1
        dx = XLEN / (n - 1)
        xx = XMIN + np.arange(n) * dx
        f, _ = manipulate(np.zeros(n), mode, w, x0, y, x=xx, npts=n, dx=dx)
        got = closed(mode, w, xx[idx_at(x0, n)], y)
        g, gp = got[0], got[1]
        d = (f[1:] - f[:-1]) / dx
        xm = xx[:-1] + dx / 2
        keep = np.abs(g(xm)) > 1e-6 * abs(y)
        row.append(float(np.max(np.abs(d[keep] - gp(xm[keep])))))
    ratios = [row[i] / row[i + 1] for i in range(3)]
    print('  %-9s errors %s   ratios %s' % (mode, ' '.join('%.3e' % v for v in row),
                                            ' '.join('%.3f' % r for r in ratios)))
    assert all(3.7 < r < 4.3 for r in ratios), ratios
    ref('RATE_' + mode.upper(), ratios[-1], 'error ratio on halving dx (4 = second order)')


# ====================================================================== #
#  B5.  corners: what the derivative does where it does not exist        #
# ====================================================================== #
head('B5  corners, and the one-sided limits')
w, x0, y = W_DEF, 4.0, 1.5
f, corner = manipulate(zero, 'triangle', w, x0, y)
xc = X[idx_at(x0)]
s = TYPICAL_Y / (w / 2)
d = deriv(f)
i0 = idx_at(x0)
print('  triangle, w = %g, apex at x = %.3f, height %.2f' % (w, xc, y))
print('    slope of the cell just LEFT of the apex   = %+.17g' % d[i0 - 1])
print('    slope of the cell just RIGHT of the apex  = %+.17g' % d[i0])
print('    closed form  +/- TYPICAL_Y/(w/2)          = %+.17g' % s)
assert abs(d[i0 - 1] - s) < 1e-13 and abs(d[i0] + s) < 1e-13
print('    the two one-sided limits differ by %.17g; no value exists at the apex.' % (2 * s))
ref('TRI_SLOPE', s, 'triangle one-sided slope TYPICAL_Y/(w/2) at w = 2')
# the delta in f'' : its integral over a window around the apex IS the jump
d2 = deriv2(f)
lo, hi = i0 - 40, i0 + 40
area = float(np.sum(d2[lo:hi + 1]) * DX)
print('    integral of f" over 81 nodes about the apex = %+.17g' % area)
print('    = slope(right cell) - slope(left cell) = %+.17g  (exact: telescoping)'
      % (d[hi] - d[lo - 1]))
assert abs(area - (d[hi] - d[lo - 1])) < 1e-12
ref('TRI_D2_AREA', area, 'int f" over 81 nodes about the triangle apex = the slope jump')
# the junctions where the triangle meets the flat curve
r = y / s
print('    the junctions sit at x = %.5f and %.5f (y/s from the apex)' % (xc - r, xc + r))
print('    there the slope jumps from %+.4f to 0 and from %+.4f to 0' % (s, -s))
ref('TRI_JUNCTION_L', xc - r, 'left junction of the default triangle')
ref('TRI_JUNCTION_R', xc + r, 'right junction')

w2, x2, y2 = 2.5, 6.0, -1.4
f2, _ = manipulate(zero, 'parabola', w2, x2, y2)
xc2 = X[idx_at(x2)]
s2 = TYPICAL_Y * (2.0 / w2) ** 2
r2 = math.sqrt(abs(y2) / s2)
jump = 2 * math.sqrt(s2 * abs(y2))
d = deriv(f2)
print('  parabola, w = %g, vertex at x = %.3f, depth %.2f' % (w2, xc2, y2))
print('    the vertex is SMOOTH (slope 0); the corners are at the junctions')
print('    x = %.5f and %.5f, where the slope jumps by %.17g' % (xc2 - r2, xc2 + r2, jump))
jl = idx_at(xc2 - r2)
meas_jump = abs(d[jl + 1] - d[jl - 2])
print('    measured jump across the left junction  = %.17g' % meas_jump)
print('    (short of the closed form by %.4f: the junction falls INSIDE a cell,'
      % (jump - meas_jump))
print('     so the nearest clean cell is ~1.5 dx in and the parabola\'s slope')
print('     there is already 2 s (1.5 dx) = %.4f smaller.  A corner\'s position'
      % (2 * s2 * 1.5 * DX))
print('     is only known to one cell; its one-sided LIMITS are not.)')
ref('PAR_JUMP_MEAS', meas_jump, 'measured across the left junction, 1.5 dx off the corner')
ref('PAR_JUMP', jump, 'parabola slope jump at a junction, 2 sqrt(s|y|)')
ref('PAR_JUNCTION_L', xc2 - r2, '')
ref('PAR_JUNCTION_R', xc2 + r2, '')

f3, _ = manipulate(zero, 'sinusoid', 2.0, 5.0, 1.0)
lam = 2 * math.pi * 2.0 / W_DEF
ends = closed('sinusoid', 2.0, X[idx_at(5.0)], 1.0)[3]
print('  sinusoid on an EMPTY curve: PhET drops the taper when the region it')
print('    would blend into is zero, so the packet ends in two corners at')
print('    x = %.5f and %.5f, each a slope jump of %.17g' % (ends[0], ends[1], 2 * math.pi / lam))
ref('SIN_LAMBDA', lam, 'sinusoid period 2 pi w / W_DEF')
ref('SIN_END_L', ends[0], 'left end of the sinusoid packet at w = 2, x0 = 5')
ref('SIN_END_R', ends[1], 'right end')
ref('SIN_END_SLOPE', 2 * math.pi / lam * 1.0, 'slope magnitude at the packet ends, y k')

print('  hill and pedestal have NO corner:')
fh, _ = manipulate(zero, 'hill', W_DEF, 3.0, 1.5)
dh = deriv(fh)
print('    hill      max |slope change between neighbouring cells| = %.3e'
      % float(np.max(np.abs(np.diff(dh)))))
fp, _ = manipulate(zero, 'pedestal', 3.0, 5.0, 1.2)
dp = deriv(fp)
print('    pedestal  max |slope change between neighbouring cells| = %.3e'
      % float(np.max(np.abs(np.diff(dp)))))
print('    (PhET calls them "smooth transitions"; the pedestal join is C3 -- the')
print('     quartic exp(-u^4) has value 1 and zero first, second and third')
print('     derivatives at u = 0, so only f"" jumps there.)')
ref('HILL_MAX_DSLOPE', float(np.max(np.abs(np.diff(dh)))), 'hill: neighbouring cell slopes differ by')
ref('PED_MAX_DSLOPE', float(np.max(np.abs(np.diff(dp)))), 'pedestal: the same')
ref('TRI_MAX_DSLOPE', float(np.max(np.abs(np.diff(deriv(f))))), 'triangle: the same, at a corner')


# ====================================================================== #
#  B6.  the tangent tool and the area tool                               #
# ====================================================================== #
def tangent_slope(f, x):
    i = min(max(int(math.floor((x - XMIN) / DX)), 0), NPTS - 2)
    return (f[i + 1] - f[i]) / DX, i


def signed_areas(f, xend):
    """positive and negative area between the curve and y = 0, from XMIN to
    xend, each cell split at its zero crossing.  A DIFFERENT route from the
    cumulative trapezium, so the two agreeing is a real check."""
    pos = neg = 0.0
    i = 0
    while i < NPTS - 1 and X[i + 1] <= xend + 1e-15:
        a, b = f[i], f[i + 1]
        if a * b < 0:
            t = a / (a - b)
            A1 = 0.5 * a * (t * DX)
            A2 = 0.5 * b * ((1 - t) * DX)
            for A in (A1, A2):
                if A >= 0:
                    pos += A
                else:
                    neg += -A
        else:
            A = 0.5 * (a + b) * DX
            if A >= 0:
                pos += A
            else:
                neg += -A
        i += 1
    if i < NPTS - 1 and xend > X[i]:
        t = (xend - X[i]) / DX
        b = f[i] + t * (f[i + 1] - f[i])
        a = f[i]
        if a * b < 0:
            tz = a / (a - b)
            A1 = 0.5 * a * (tz * t * DX)
            A2 = 0.5 * b * ((1 - tz) * t * DX)
            parts = (A1, A2)
        else:
            parts = (0.5 * (a + b) * t * DX,)
        for A in parts:
            if A >= 0:
                pos += A
            else:
                neg += -A
    return pos, neg, pos - neg


head('B5b  the sinusoid: its packet ends, and the taper it uses on a non-empty curve')
# the first mutation sweep let "seven half-periods -> five" and "taper lambda/8
# -> lambda/4" survive, because every sinusoid test used a width whose packet
# is wider than the whole domain (so the ends are outside it) and an EMPTY base
# (so PhET drops the taper).  Both are pinned here at a width that fits.
wn, xn, yn = 0.6, 5.0, 1.0
fn, cn = manipulate(zero, 'sinusoid', wn, xn, yn)
lam_n = 2 * math.pi * wn / W_DEF
ends_n = closed('sinusoid', wn, X[idx_at(xn)], yn)[3]
print('  w = %g: lambda = %.17g, packet 3.5 lambda wide' % (wn, lam_n))
print('    ends at %.17g and %.17g  (span/lambda = %.6f half-periods)'
      % (ends_n[0], ends_n[1], 2 * (ends_n[1] - ends_n[0]) / lam_n))
assert abs(2 * (ends_n[1] - ends_n[0]) / lam_n - 7) < 0.01
ref('SIN_NARROW_LAM', lam_n, 'the narrow sinusoid period 2 pi w / W_DEF at w = 0.6')
ref('SIN_NARROW_L', ends_n[0], 'and its left end, snapped to a node')
ref('SIN_NARROW_R', ends_n[1], 'and its right end')
ref('SIN_NARROW_AREA', float(integ(fn)[-1]), 'and the signed area it puts on an empty curve')
# the taper: on a curve that is NOT zero, PhET blends with cos^2 over lambda/8
base = manipulate(zero, 'shift', 1.0, 5.0, 1.0)[0]
assert abs(base.max() - 1.0) < 1e-15 and abs(base.min() - 1.0) < 1e-15
ft, _ = manipulate(base, 'sinusoid', wn, xn, 0.8)
a_n = lam_n / 8
xt = ends_n[0] + a_n / 2
it = idx_at(xt)
print('    on a constant-1 curve the taper band is %.4f wide; at x = %.17g'
      % (a_n, X[it]))
print('      the blended value is %.17g (the base is 1, the wave %.17g)'
      % (ft[it], 0.8 * math.cos(2 * math.pi * (X[idx_at(xn)] - X[it]) / lam_n)))
assert abs(ft[it] - 1.0) > 1e-3 and abs(ft[it] - 0.8 * math.cos(2 * math.pi * (X[idx_at(xn)] - X[it]) / lam_n)) > 1e-3
ref('SIN_TAPER_X', float(X[it]), 'a node inside the left cos^2 taper band')
ref('SIN_TAPER_F', float(ft[it]), 'the blended value there, base 1 and wave 0.8')
ref('SIN_TAPER_A', a_n, 'the taper width lambda/8')

head('B5c  the second difference at the ends, on a curve that is curved there')
fw, _ = manipulate(zero, 'sinusoid', 5.0, 5.0, 1.0)
d2w = deriv2(fw)
print('  a w = 5 sinusoid spans the whole range: f"(0) = %.17g, f"(dx) = %.17g'
      % (d2w[0], d2w[1]))
assert abs(d2w[1]) > 0.01
ref('WIDE_SIN_D2_0', float(d2w[0]), 'f" at the first node of a w = 5 sinusoid (copied from its neighbour)')
ref('WIDE_SIN_D2_END', float(d2w[-1]), 'and at the last')

head('B6  the tangent tool and the area tool, by independent routes')
curve = manipulate(manipulate(zero, 'hill', 2.0, 3.2, 1.6)[0], 'triangle', 2.4, 6.8, -1.2)[0]
d = deriv(curve)
F = integ(curve)
worst_t = 0.0
for xq in [0.37, 1.5, 2.9, 3.2, 4.4, 5.0, 6.13, 6.8, 7.77, 9.42]:
    sl, i = tangent_slope(curve, xq)
    worst_t = max(worst_t, abs(sl - d[i]))
    # the drawn tangent line must pass through the two nodes of its own cell
    y_at = curve[i] + sl * (X[i] - X[i])
    assert abs(y_at - curve[i]) < 1e-15
    assert abs((curve[i] + sl * DX) - curve[i + 1]) < 1e-13
print('  tangent slope == the derivative curve at the same x, worst %.2e over 10 x' % worst_t)
print('  and the drawn tangent line passes through both nodes of its cell exactly.')
worst_a = 0.0
for xq in [0.5, 2.0, 3.2, 4.0, 5.55, 6.8, 8.0, 10.0]:
    pos, neg, net = signed_areas(curve, xq)
    i = int(math.floor((xq - XMIN) / DX + 1e-12))
    i = min(i, NPTS - 2)
    t = (xq - X[i]) / DX
    yv = curve[i] + t * (curve[i + 1] - curve[i])
    Fx = F[i] + 0.5 * (curve[i] + yv) * (t * DX)
    worst_a = max(worst_a, abs(net - Fx))
print('  net signed area (split at every zero crossing) == the integral curve,')
print('  worst %.2e over 8 endpoints.' % worst_a)
assert worst_t < 1e-14 and worst_a < 1e-12
pos, neg, net = signed_areas(curve, 10.0)
print('  over the whole range the default curve has  +%.17g  -%.17g  net %.17g'
      % (pos, neg, net))
ref('TANGENT_TOL', worst_t, 'tangent slope vs derivative curve')
ref('AREA_TOL', worst_a, 'split-at-zeros area vs integral curve')
ref('DEF_AREA_POS', pos, 'default curve: area above the axis')
ref('DEF_AREA_NEG', neg, 'default curve: area below the axis')
ref('DEF_AREA_NET', net, 'default curve: net signed area over 0..10')
ref('DEF_F_MAX', float(np.max(curve)), 'default curve: the largest f')
ref('DEF_F_MIN', float(np.min(curve)), 'default curve: the smallest f')
ref('DEF_D_MAX', float(np.max(d)), 'default curve: the largest slope')
ref('DEF_D_MIN', float(np.min(d)), 'default curve: the smallest slope')
for xq in (2.0, 3.2, 5.0, 6.8, 8.0):
    i = idx_at(xq)
    ref('DEF_F_AT_%d' % round(xq * 10), float(curve[i]), 'default curve f(%.1f)' % X[i])
    ref('DEF_I_AT_%d' % round(xq * 10), float(F[i]), 'default curve int_0^%.1f f' % X[i])
ref('DEF_D_AT_32', float(d[idx_at(3.2)]), 'default curve f\' on the cell right of 3.2')


# ====================================================================== #
#  B7.  PhET's smoothing                                                 #
# ====================================================================== #
def smooth(f, sigma=SMOOTH_SIGMA, dx=DX, want=None):
    n = len(f)
    w0 = 1.0 / (sigma * math.sqrt(2 * math.pi))
    kern = lambda t: w0 * math.exp(-0.5 * (t / sigma) ** 2)
    K = 0
    while (K + 1) * dx <= 3 * sigma + 1e-12:
        K += 1
    out = np.empty(n)
    idx = np.arange(n)
    tot = kern(0.0)
    acc = f * kern(0.0)
    for k in range(1, K + 1):
        s = kern(k * dx)
        tot += 2 * s
        acc = acc + s * f[np.clip(idx + k, 0, n - 1)] + s * f[np.clip(idx - k, 0, n - 1)]
    out = acc / tot
    if want == 'weights':
        return w0, tot, K
    return out, K


head('B7  PhET\'s smoothing operator')
sm, K = smooth(np.ones(NPTS))
print('  kernel: Gaussian sigma = %g, truncated at 3 sigma, sampled every dx' % SMOOTH_SIGMA)
print('  -> %d taps each side (3 sigma / dx = %.3f)' % (K, 3 * SMOOTH_SIGMA / DX))
print('  a constant is preserved to %.2e (the weights are renormalised)'
      % float(np.max(np.abs(sm - 1))))
assert float(np.max(np.abs(sm - 1))) < 1e-15
ref('SMOOTH_TAPS', K, 'taps each side: floor(3 sigma / dx)')
w0k, totk, _ = smooth(np.ones(NPTS), want='weights')
print('  peak weight 1/(sigma sqrt(2 pi)) = %.17g, weights sum to %.17g'
      % (w0k, totk))
ref('SMOOTH_W0', w0k, "PhET's kernel peak weight 1/(sigma sqrt(2 pi))")
ref('SMOOTH_TOT', totk, 'and the sum of the 37 sampled weights')
fh, _ = manipulate(zero, 'hill', W_DEF, 5.0, 1.5)
sh, _ = smooth(fh)
print('  a hill of width %g (a Gaussian of sd w/4 = %g) smoothed:' % (W_DEF, W_DEF / 4))
print('    peak %.17g -> %.17g   (ratio %.17g)'
      % (float(np.max(fh)), float(np.max(sh)), float(np.max(sh) / np.max(fh))))
sig_h = W_DEF / 4
print('    an untruncated Gaussian kernel would give sd sqrt(%g^2 + %g^2) = %.8g,'
      % (sig_h, SMOOTH_SIGMA, math.hypot(sig_h, SMOOTH_SIGMA)))
print('    so a peak ratio of %.8g; the truncated, renormalised, sampled kernel'
      % (sig_h / math.hypot(sig_h, SMOOTH_SIGMA)))
print('    gives %.8g -- the difference is the truncation, and it is measured.'
      % float(np.max(sh) / np.max(fh)))
print('    the area is preserved to %.3e'
      % abs(float(np.sum(sh) * DX - np.sum(fh) * DX)))
ref('SMOOTH_HILL_PEAK', float(np.max(sh)), 'a w=2 hill of height 1.5 after one smooth')
ref('SMOOTH_HILL_RATIO', float(np.max(sh) / np.max(fh)), 'and the peak ratio')
ref('SMOOTH_GAUSS_RATIO', sig_h / math.hypot(sig_h, SMOOTH_SIGMA),
    'the untruncated-kernel prediction sigma_h / sqrt(sigma_h^2 + sigma_s^2)')
ref('SMOOTH_AREA_DRIFT', abs(float(np.sum(sh) * DX - np.sum(fh) * DX)),
    'area change from one smoothing of an interior bump')

ft, _ = manipulate(zero, 'triangle', W_DEF, 5.0, 1.5)
st_, _ = smooth(ft)
dt_ = deriv(st_)
i0 = idx_at(5.0)
print('  a triangle apex, smoothed: the cell slopes either side of the apex go')
print('    from %+.6f / %+.6f to %+.6f / %+.6f' %
      (deriv(ft)[i0 - 1], deriv(ft)[i0], dt_[i0 - 1], dt_[i0]))
print('    the corner is rounded over about 6 sigma = %.3f in x' % (6 * SMOOTH_SIGMA))
ref('SMOOTH_TRI_SLOPE', float(dt_[i0 - 1]), 'triangle apex: cell slope left of it after smoothing')
ref('SMOOTH_TRI_PEAK', float(np.max(st_)), 'and the rounded peak')


# ====================================================================== #
#  B8.  tilt and shift                                                   #
# ====================================================================== #
head('B8  tilt and shift')
base = manipulate(zero, 'hill', 2.0, 3.0, 1.0)[0]
ft = manipulate(base, 'tilt', 0, 8.0, 1.6)[0]
print('  tilt: pinned at the left edge, so f(0) is unchanged: %.3e'
      % abs(ft[0] - base[0]))
print('        and the dragged point lands exactly on the pointer: %.3e'
      % abs(ft[idx_at(8.0)] - 1.6))
assert abs(ft[0] - base[0]) < 1e-15 and abs(ft[idx_at(8.0)] - 1.6) < 1e-14
dslope = deriv(ft) - deriv(base)
print('        every cell slope changes by the same amount, spread %.3e'
      % float(np.ptp(dslope)))
ref('TILT_SLOPE_ADD', float(np.mean(dslope)), 'tilt to (8, 1.6) adds this to every slope')
print('  tilt refuses a slope of magnitude %g or more (PhET\'s maxTilt)' % MAX_TILT)
steep = manipulate(base, 'tilt', 0, 0.04, 2.0)[0]
print('        a drag to (0.04, 2.0) asks for slope %.1f -> refused: %s'
      % ((2.0 - base[0]) / X[idx_at(0.04)], bool(np.allclose(steep, base))))
assert np.allclose(steep, base)
fs_ = manipulate(base, 'shift', 0, 3.0, -0.5)[0]
print('  shift: the whole curve moves rigidly; every slope is unchanged: %.3e'
      % float(np.max(np.abs(deriv(fs_) - deriv(base)))))
print('         (not 0: a slope is a difference of order-1 numbers divided by')
print('          dx = %g, so one ulp of f is %.1e of slope)' % (DX, 2.3e-16 / DX))
print('         and the integral gains exactly delta * x: %.3e'
      % float(np.max(np.abs((integ(fs_) - integ(base)) - (fs_[0] - base[0]) * X))))
assert float(np.max(np.abs(deriv(fs_) - deriv(base)))) < 1e-12
ref('SHIFT_DELTA', float(fs_[0] - base[0]), 'shift of the default hill to (3, -0.5)')


# ====================================================================== #
#  B9.  the erf this file needs in JavaScript                            #
# ====================================================================== #
head('B9  erf: the series the JS uses, against scipy')


def erf_series(z):
    """erf(z) = (2 z / sqrt(pi)) exp(-z^2) sum_n (2 z^2)^n / (1.3.5...(2n+1)).
    All terms positive: no cancellation, unlike the alternating Maclaurin
    series.  This is what p2_calculus.js implements."""
    if z < 0:
        return -erf_series(-z)
    if z > 6:
        return 1.0
    t = 1.0
    s = 1.0
    for n in range(1, 200):
        t *= 2 * z * z / (2 * n + 1)
        s += t
        if t < 1e-18 * s:
            break
    return 2 * z / math.sqrt(math.pi) * math.exp(-z * z) * s


worst = 0.0
for z in np.concatenate([np.linspace(0, 6, 601), -np.linspace(0, 6, 601)]):
    worst = max(worst, abs(erf_series(float(z)) - special.erf(z)))
print('  max |erf_series - scipy.special.erf| over -6..6 = %.3e' % worst)
assert worst < 3e-15
ref('ERF_TOL', worst, 'the all-positive series vs scipy over -6..6')
for zz in (0.25, 1.0, 2.0, 3.5):
    ref('ERF_%d' % round(zz * 100), float(special.erf(zz)), 'scipy erf(%.2f)' % zz)


# ====================================================================== #
#  B10.  the default curve, the reference shapes, and view numbers       #
# ====================================================================== #
head('B10  numbers the views print')
F = integ(curve)
d = deriv(curve)
d2 = deriv2(curve)
print('  the file opens with a hill (w 2.0, x 3.2, y +1.6) then a triangle')
print('  (w 2.4, x 6.8, y -1.2) laid on an empty curve, because a flat curve')
print('  makes every one of these views blank.  PhET opens flat; "erase" here')
print('  gives exactly that.')
print('  f      in [%.6f, %.6f]' % (curve.min(), curve.max()))
print("  f'     in [%.6f, %.6f]" % (d.min(), d.max()))
print('  f"     in [%.4f, %.4f]' % (d2.min(), d2.max()))
print('  int f  in [%.6f, %.6f], net %.6f' % (F.min(), F.max(), F[-1]))
ref('DEF_I_END', float(F[-1]), 'default curve: int_0^10 f')
ref('DEF_D2_MAX', float(np.max(np.abs(d2))), 'default curve: max |f"| (the triangle apex)')

# the pure reference shapes the analysis views use
for mode, w, x0, y in MODES:
    f, _ = manipulate(zero, mode, w, x0, y)
    ref('REFSHAPE_%s_PEAK' % mode.upper(), float(f[idx_at(x0)]), '%s at its centre' % mode)
    ref('REFSHAPE_%s_AREA' % mode.upper(), float(integ(f)[-1]), 'total signed area of the %s' % mode)
    got = closed(mode, w, X[idx_at(x0)], y)
    if mode == 'pedestal':
        exact = got[4](XMAX)
    else:
        exact = float(np.atleast_1d(got[2](np.array([XMAX])))[0])
    ref('REFSHAPE_%s_AREA_EXACT' % mode.upper(), exact, 'and the closed form for it')

# a curve with a hand-picked zero crossing, for the area tool's two colours
cross = manipulate(manipulate(zero, 'hill', 2.0, 2.5, 1.2)[0], 'hill', 2.0, 7.0, -1.0)[0]
pos, neg, net = signed_areas(cross, XMAX)
print('  the two-hill test curve: +%.9f  -%.9f  net %.9f' % (pos, neg, net))
ref('CROSS_POS', pos, 'two-hill curve: area above the axis')
ref('CROSS_NEG', neg, 'two-hill curve: area below')
ref('CROSS_NET', net, 'two-hill curve: net')

head('C  reference values written to refvals.txt')
lines = []
seen = set()
for name, val, note in REFS:
    assert name not in seen, 'duplicate reference name ' + name
    seen.add(name)
    if isinstance(val, bool):
        sval = 'true' if val else 'false'
    elif isinstance(val, int):
        sval = str(val)
    else:
        sval = repr(float(val))
    lines.append('%-26s %s%s' % (name, sval, ('   # ' + note) if note else ''))
io.open(os.path.join(HERE, 'refvals.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('  %d reference values -> refvals.txt' % len(REFS))
for ln in lines:
    print('  ' + ln)
print('\nderive.py: all assertions passed.')
