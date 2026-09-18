"""Tests for CM-21 Hamilton-Jacobi & action-angle. Reuses MA-07 transitively.

Run:  python3 test_hamilton_jacobi.py     ->  "All N tests passed."
"""
import math

from hamilton_jacobi import action_variable, period, frequency, turning_points


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_turning_points():
    V = lambda q: 0.5 * q * q
    a, b = turning_points(V, 1.0, -10, 10)                  # 1/2 q^2 = 1 -> q = +/- sqrt2
    assert _approx(a, -math.sqrt(2)) and _approx(b, math.sqrt(2))


def test_sho_action_variable():
    w, m = 2.0, 1.0
    V = lambda q: 0.5 * m * w * w * q * q
    for E in (1.0, 2.0, 4.0):
        assert _approx(action_variable(V, m, E, -10, 10), 2 * math.pi * E / w, tol=1e-2)   # J = 2 pi E/w


def test_sho_isochronous():
    w, m = 2.0, 1.0
    V = lambda q: 0.5 * m * w * w * q * q
    for E in (0.5, 1.0, 2.0, 4.0):
        assert _approx(period(V, m, E, -10, 10), 2 * math.pi / w, tol=1e-5)   # T = 2 pi/w, independent of E
    assert _approx(frequency(V, m, 1.0, -10, 10), w, tol=1e-5)


def test_pendulum_is_anharmonic():
    V = lambda q: 1.0 - math.cos(q)                         # m=g=l=1, omega0=1
    assert _approx(period(V, 1.0, 0.01, -3.1, 3.1), 2 * math.pi, tol=2e-2)   # small amplitude -> 2 pi
    T_small = period(V, 1.0, 0.05, -3.1, 3.1)
    T_large = period(V, 1.0, 1.5, -3.1, 3.1)
    assert T_large > T_small + 0.1                          # period grows with amplitude


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
