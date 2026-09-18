"""Tests for MA-20 numerical methods. Pure stdlib.

Run:  python3 test_numerical.py     ->  "All N tests passed."
"""
import math

from numerical import (
    trapezoid, simpson, gauss_legendre, quad_order,
    bisection, newton, secant, euler, rk4, ode_order,
    power_iteration, lagrange_interp,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_quadrature_values():
    assert _approx(simpson(math.exp, 0, 1, 100), math.e - 1, tol=1e-9)
    assert _approx(simpson(math.sin, 0, math.pi, 1000), 2.0, tol=1e-10)   # O(h^4), wider interval
    assert _approx(trapezoid(lambda x: 3 * x * x, 0, 2, 100000), 8.0, tol=1e-6)


def test_gauss_exact_for_polynomials():
    # n-node Gauss is exact for degree <= 2n-1
    # 2-node exact through cubics:
    for c in ([1, 0, 0, 0], [0, 0, 0, 1], [1, -2, 3, -1]):
        poly = lambda x: c[0] + c[1] * x + c[2] * x ** 2 + c[3] * x ** 3
        exact = c[0] * 2 + c[2] * 2 / 3.0          # int_{-1}^1 (odd terms vanish)
        assert _approx(gauss_legendre(poly, -1, 1, 2, 1), exact, tol=1e-12)
    # 3-node exact through quintics:
    quint = lambda x: 1 + 2 * x ** 2 + 4 * x ** 4
    exact = 2 + 2 * 2 / 3.0 + 4 * 2 / 5.0
    assert _approx(gauss_legendre(quint, -1, 1, 3, 1), exact, tol=1e-12)


def test_convergence_orders():
    f = math.exp
    assert abs(quad_order(trapezoid, f, 0, 1, math.e - 1) - 2.0) < 0.1
    assert abs(quad_order(simpson, f, 0, 1, math.e - 1) - 4.0) < 0.1


def test_root_finders():
    for solver in (
        lambda: newton(lambda x: x * x - 2, lambda x: 2 * x, 1.0)[0],
        lambda: bisection(lambda x: x * x - 2, 0, 2),
        lambda: secant(lambda x: x * x - 2, 1, 2),
    ):
        assert _approx(solver(), math.sqrt(2), tol=1e-10)
    # a transcendental root: cos x = x
    r, _ = newton(lambda x: math.cos(x) - x, lambda x: -math.sin(x) - 1, 0.5)
    assert _approx(math.cos(r), r, tol=1e-10)


def test_newton_quadratic_convergence():
    # the error should roughly square each step: e_{k+1} ~ C e_k^2
    _, hist = newton(lambda x: x * x - 2, lambda x: 2 * x, 1.5)
    errs = [abs(x - math.sqrt(2)) for x in hist]
    # find consecutive ratios e_{k+1}/e_k^2 -- bounded (quadratic), not growing
    ratios = [errs[k + 1] / errs[k] ** 2 for k in range(len(errs) - 1) if errs[k] > 1e-8]
    assert len(ratios) >= 2
    assert max(ratios) < 1.0                      # |e_{k+1}| < |e_k|^2 here


def test_ode_orders():
    fode = lambda t, y: y                          # y' = y, y(1) = e
    assert abs(ode_order(euler, fode, 1.0, 1.0, math.e) - 1.0) < 0.15
    assert abs(ode_order(rk4, fode, 1.0, 1.0, math.e) - 4.0) < 0.2
    # decaying oscillator-ish: y' = -2 y, y(1) = e^{-2}
    fdec = lambda t, y: -2 * y
    assert _approx(rk4(fdec, 1.0, 1.0, 200), math.exp(-2), tol=1e-7)


def test_power_iteration():
    A = [[2.0, 1.0, 0.0], [1.0, 2.0, 1.0], [0.0, 1.0, 2.0]]   # eigenvalues 2, 2 +/- sqrt2
    lam, vec = power_iteration(A)
    assert _approx(lam, 2 + math.sqrt(2), tol=1e-8)
    # check A v = lam v
    Av = [sum(A[i][j] * vec[j] for j in range(3)) for i in range(3)]
    assert all(_approx(Av[i], lam * vec[i], tol=1e-6) for i in range(3))


def test_lagrange_interpolation():
    # exact recovery of a cubic at off-node points
    poly = lambda x: 2 - x + 0.5 * x ** 2 - 0.3 * x ** 3
    xs = [0, 1, 2, 3]
    ys = [poly(x) for x in xs]
    for xq in (0.5, 1.7, 2.9):
        assert _approx(lagrange_interp(xs, ys, xq), poly(xq), tol=1e-9)
    # passes through the nodes exactly
    for x, y in zip(xs, ys):
        assert _approx(lagrange_interp(xs, ys, x), y)


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
