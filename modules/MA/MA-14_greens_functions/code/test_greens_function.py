"""Tests for MA-14 Green's functions. Pure stdlib.

Run:  python3 test_greens_function.py     ->  "All N tests passed."
"""
import math

from greens_function import (
    green_dirichlet, green_helmholtz, solve_bvp_greens, solve_bvp_direct,
    green_series, causal_green_oscillator, solve_oscillator_greens, rk4_oscillator,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_green_symmetry():
    # self-adjoint operator -> symmetric Green's function G(x,xi)=G(xi,x)
    for x, xi in [(0.2, 0.7), (0.5, 0.9), (0.33, 0.33)]:
        assert _approx(green_dirichlet(x, xi), green_dirichlet(xi, x))
        assert _approx(green_helmholtz(x, xi, 2.0), green_helmholtz(xi, x, 2.0))


def test_green_boundary_and_kink():
    # G vanishes at the endpoints in each argument
    for xi in (0.2, 0.5, 0.8):
        assert _approx(green_dirichlet(0.0, xi), 0.0)
        assert _approx(green_dirichlet(1.0, xi), 0.0)
    # the slope of G in x jumps by -1 across x=xi (the delta source)
    xi, e = 0.6, 1e-5
    left = (green_dirichlet(xi - e, xi) - green_dirichlet(xi - 3 * e, xi)) / (2 * e)
    right = (green_dirichlet(xi + 3 * e, xi) - green_dirichlet(xi + e, xi)) / (2 * e)
    assert _approx(right - left, -1.0, tol=1e-3)


def test_bvp_against_exact():
    xs = [0.1 * i for i in range(1, 10)]
    # f = sin(pi x) -> u = sin(pi x)/pi^2
    ug = solve_bvp_greens(lambda x: math.sin(math.pi * x), xs)
    for x, u in zip(xs, ug):
        assert _approx(u, math.sin(math.pi * x) / math.pi ** 2, tol=1e-5)
    # f = 1 -> u = x(1-x)/2
    ug = solve_bvp_greens(lambda x: 1.0, xs)
    for x, u in zip(xs, ug):
        assert _approx(u, x * (1 - x) / 2.0, tol=1e-5)


def test_bvp_greens_matches_direct():
    f = lambda x: math.exp(x) * (1.0 + x)        # arbitrary smooth source
    xd, ud = solve_bvp_direct(f, 49)
    ug = solve_bvp_greens(f, xd)
    assert max(abs(a - b) for a, b in zip(ug, ud)) < 1e-3


def test_helmholtz_matches_direct():
    f = lambda x: x * (1.0 - x)
    for k in (1.0, 3.0, 5.0):
        xd, ud = solve_bvp_direct(f, 49, k=k)
        ug = solve_bvp_greens(f, xd, k=k)
        assert max(abs(a - b) for a, b in zip(ug, ud)) < 1e-3


def test_eigenfunction_series_converges():
    # 2 sin(n pi x) sin(n pi xi)/(n pi)^2 -> the closed-form tent
    for x, xi in [(0.3, 0.7), (0.5, 0.25), (0.8, 0.4)]:
        closed = green_dirichlet(x, xi)
        s10 = green_series(x, xi, 10)
        s2000 = green_series(x, xi, 2000)
        assert abs(s2000 - closed) < abs(s10 - closed)       # converging
        assert abs(s2000 - closed) < 2e-3                    # and close


def test_propagator_against_rk4():
    for omega in (1.0, 2.0, 3.5):
        for fdrive in (lambda t: 1.0, lambda t: math.cos(0.7 * t), lambda t: math.exp(-0.3 * t)):
            for t in (0.7, 2.0, 5.0):
                g = solve_oscillator_greens(fdrive, t, omega)
                r = rk4_oscillator(fdrive, t, omega)
                assert abs(g - r) < 1e-4


def test_propagator_step_closed_form():
    # f = 1 -> y = (1 - cos omega t)/omega^2
    omega = 2.0
    for t in (0.5, 1.5, 3.0):
        y = solve_oscillator_greens(lambda tau: 1.0, t, omega)
        assert _approx(y, (1 - math.cos(omega * t)) / omega ** 2, tol=1e-5)


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
