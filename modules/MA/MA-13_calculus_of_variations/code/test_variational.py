"""Tests for MA-13 calculus of variations. Pure stdlib.

Run:  python3 test_variational.py     ->  "All N tests passed."
"""
import math

from variational import (
    functional, euler_lagrange_residual, beltrami, minimize_path,
    cycloid_brachistochrone, catenary,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


ARCLEN = lambda x, y, p: math.sqrt(1 + p * p)


def test_functional_value():
    # straight line y=x from (0,0)-(1,1): arclength = sqrt(2)
    xs = [i / 10 for i in range(11)]
    ys = list(xs)
    assert _approx(functional(ARCLEN, xs, ys), math.sqrt(2), tol=1e-9)
    # a bent path is strictly longer
    bent = [y + 0.2 * math.sin(math.pi * x) for x, y in zip(xs, ys)]
    assert functional(ARCLEN, xs, bent) > math.sqrt(2) + 1e-3


def test_straight_line_is_extremal():
    # EL residual ~0 along y=x for the arclength functional
    xs = [i / 12 for i in range(13)]
    ys = list(xs)
    res = euler_lagrange_residual(ARCLEN, xs, ys)
    assert max(abs(r) for r in res) < 1e-6


def test_minimizer_recovers_geodesic():
    # start bent, relax to the straight line
    xs, ys = minimize_path(ARCLEN, 0.0, 0.0, 1.0, 1.0, N=15)
    for x, y in zip(xs, ys):
        assert abs(y - x) < 1e-3
    assert _approx(functional(ARCLEN, xs, ys), math.sqrt(2), tol=1e-4)
    res = euler_lagrange_residual(ARCLEN, xs, ys)
    assert max(abs(r) for r in res) < 1e-3


def test_minimizer_handles_slanted_endpoints():
    # geodesic between (0,1) and (2,4) is the straight line y = 1 + 1.5 x
    xs, ys = minimize_path(ARCLEN, 0.0, 1.0, 2.0, 4.0, N=15)
    for x, y in zip(xs, ys):
        assert abs(y - (1.0 + 1.5 * x)) < 2e-3


def test_beltrami_brachistochrone_constant():
    # L = sqrt((1+y'^2)/y); on the cycloid B = 1/sqrt(2a) (constant), using the
    # EXACT slope y' = sin t/(1-cos t) -- the Beltrami theorem is about the true
    # extremal, so a secant-slope approximation is not what is being tested.
    L = lambda x, y, p: math.sqrt((1 + p * p) / y)
    a = 1.0
    th = [0.3 + 0.25 * k for k in range(1, 12)]
    xb, yb = cycloid_brachistochrone(a, th)
    target = 1.0 / math.sqrt(2 * a)
    Bvals = [beltrami(L, xb[k], yb[k], math.sin(th[k]) / (1 - math.cos(th[k])))
             for k in range(len(th))]
    for B in Bvals:
        assert abs(B - target) < 1e-5
    assert (max(Bvals) - min(Bvals)) < 1e-5


def test_beltrami_catenary_constant():
    # L = y sqrt(1+y'^2); on y=c cosh(x/c) the Beltrami integral B = c, using the
    # exact slope y' = sinh(x/c)
    L = lambda x, y, p: y * math.sqrt(1 + p * p)
    c = 1.3
    xc = [-1.2 + 0.3 * k for k in range(9)]
    yc = catenary(c, xc)
    for k in range(len(xc)):
        assert abs(beltrami(L, xc[k], yc[k], math.sinh(xc[k] / c)) - c) < 1e-5


def test_beltrami_definition():
    # B = L - p L_p; check against an exact partial for L = sqrt(1+p^2)
    #   L_p = p/sqrt(1+p^2),  B = 1/sqrt(1+p^2)
    for p in (-1.5, 0.0, 0.8, 2.0):
        assert _approx(beltrami(ARCLEN, 0.0, 1.0, p), 1.0 / math.sqrt(1 + p * p), tol=1e-5)


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
