"""Tests for MA-07 ODEs. Reuses MA-04 (imported transitively).

Run:  python3 test_ode.py     ->  "All N tests passed."
"""
import math

from ode import (
    integrate, euler_step, rk4_step, second_order_system,
    linear_rhs, linear_evolve_symmetric,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-9):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_exponential():
    ts, ys = integrate(lambda t, y: [y[0]], [1.0], 0.0, 1.0, 1000)
    assert _approx(ys[-1][0], math.e, tol=1e-7)                         # y'=y -> e^t
    ts, ys = integrate(lambda t, y: [-2.0 * y[0]], [1.0], 0.0, 1.0, 1000)
    assert _approx(ys[-1][0], math.exp(-2.0), tol=1e-7)                 # y'=-2y -> e^{-2t}


def test_rk4_beats_euler():
    rhs = lambda t, y: [y[0]]
    # error of one method at t=1 vs e, coarse grid
    _, ye = integrate(rhs, [1.0], 0.0, 1.0, 20, method=euler_step)
    _, yr = integrate(rhs, [1.0], 0.0, 1.0, 20, method=rk4_step)
    assert abs(yr[-1][0] - math.e) < abs(ye[-1][0] - math.e)            # RK4 far more accurate


def test_simple_harmonic_oscillator():
    f = second_order_system(lambda t, y, v: -y)                        # y'' = -y -> cos t
    for T, y_exp, v_exp in [(math.pi / 2, 0.0, -1.0), (math.pi, -1.0, 0.0), (2 * math.pi, 1.0, 0.0)]:
        ts, ys = integrate(f, [1.0, 0.0], 0.0, T, 4000)
        assert _approx(ys[-1][0], y_exp, tol=1e-5)                     # y(T) = cos T
        assert _approx(ys[-1][1], v_exp, tol=1e-5)                     # y'(T) = -sin T


def test_damped_oscillator_decays():
    f = second_order_system(lambda t, y, v: -0.4 * v - y)             # y'' + 0.4 y' + y = 0
    ts, ys = integrate(f, [1.0, 0.0], 0.0, 30.0, 6000)
    assert abs(ys[-1][0]) < 0.05 and abs(ys[-1][1]) < 0.05            # energy bled away


def test_linear_system_eigen_vs_rk4():
    A = [[0.0, 1.0], [1.0, 0.0]]                                       # symmetric, eigenvalues +/-1
    x0 = [1.0, 0.0]
    assert _vapprox(linear_evolve_symmetric(A, x0, 0.0), x0)           # t=0 -> x0
    for T in (0.3, 0.7, 1.5):
        exact = linear_evolve_symmetric(A, x0, T)
        ts, xs = integrate(linear_rhs(A), x0, 0.0, T, 3000)
        assert _vapprox(exact, xs[-1], tol=1e-5)                       # diagonalization == RK4
    # closed form for this A: e^{At} x0 = (cosh t, sinh t)
    T = 0.9
    ex = linear_evolve_symmetric(A, x0, T)
    assert _approx(ex[0], math.cosh(T)) and _approx(ex[1], math.sinh(T))


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
