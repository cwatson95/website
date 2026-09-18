"""Tests for MA-12 special functions. Pure stdlib.

Run:  python3 test_special_functions.py     ->  "All N tests passed."
"""
import math

from special_functions import (
    legendre, legendre_deriv, assoc_legendre, hermite, laguerre, bessel_j,
    legendre_generating, ode_residual,
    orthogonality_legendre, orthogonality_hermite, orthogonality_laguerre,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_legendre_closed_forms():
    for x in (-0.8, -0.2, 0.3, 0.9):
        assert _approx(legendre(0, x), 1.0)
        assert _approx(legendre(1, x), x)
        assert _approx(legendre(2, x), 0.5 * (3 * x * x - 1))
        assert _approx(legendre(3, x), 0.5 * (5 * x ** 3 - 3 * x))
        assert _approx(legendre(4, x), (35 * x ** 4 - 30 * x * x + 3) / 8)
    # endpoint values and parity
    for n in range(6):
        assert _approx(legendre(n, 1.0), 1.0)
        assert _approx(legendre(n, -1.0), (-1.0) ** n)
        assert _approx(legendre(n, -0.37), (-1) ** n * legendre(n, 0.37))


def test_legendre_derivative():
    # compare analytic recurrence derivative to a central difference
    for n in range(1, 6):
        for x in (-0.5, 0.25, 0.7):
            fd = (legendre(n, x + 1e-6) - legendre(n, x - 1e-6)) / 2e-6
            assert _approx(legendre_deriv(n, x), fd, tol=1e-4)


def test_hermite_laguerre_closed_forms():
    for x in (-1.1, 0.4, 1.3):
        assert _approx(hermite(0, x), 1.0)
        assert _approx(hermite(1, x), 2 * x)
        assert _approx(hermite(2, x), 4 * x * x - 2)
        assert _approx(hermite(3, x), 8 * x ** 3 - 12 * x)
        assert _approx(laguerre(0, x), 1.0)
        assert _approx(laguerre(1, x), 1 - x)
        assert _approx(laguerre(2, x), (x * x - 4 * x + 2) / 2)
        assert _approx(laguerre(3, x), (-x ** 3 + 9 * x * x - 18 * x + 6) / 6)


def test_assoc_legendre_reduces():
    # P_l^0 == P_l
    for l in range(5):
        for x in (-0.6, 0.1, 0.8):
            assert _approx(assoc_legendre(l, 0, x), legendre(l, x))
    # known: P_1^1 = -sqrt(1-x^2),  P_2^1 = -3x sqrt(1-x^2),  P_2^2 = 3(1-x^2)
    for x in (-0.5, 0.2, 0.7):
        s = math.sqrt(1 - x * x)
        assert _approx(assoc_legendre(1, 1, x), -s)
        assert _approx(assoc_legendre(2, 1, x), -3 * x * s)
        assert _approx(assoc_legendre(2, 2, x), 3 * (1 - x * x))


def test_bessel_integral_vs_series():
    # series J_n(x) = sum_k (-1)^k / (k! (n+k)!) (x/2)^{2k+n}
    def series(n, x, K=40):
        return sum((-1) ** k / (math.factorial(k) * math.factorial(n + k)) * (x / 2) ** (2 * k + n)
                   for k in range(K))
    for n in (0, 1, 2, 3):
        for x in (0.0, 0.7, 2.5, 5.0, 8.0):
            assert _approx(bessel_j(n, x), series(n, x), tol=1e-6)
    assert _approx(bessel_j(0, 0.0), 1.0)
    assert _approx(bessel_j(1, 0.0), 0.0)


def test_orthogonality():
    # Legendre: 2/(2n+1) delta
    for m in range(5):
        for n in range(5):
            val = orthogonality_legendre(m, n)
            assert _approx(val, 2.0 / (2 * n + 1) if m == n else 0.0, tol=1e-4)
    # Hermite: 2^n n! sqrt(pi) delta
    for m in range(4):
        for n in range(4):
            val = orthogonality_hermite(m, n)
            exp = 2 ** n * math.factorial(n) * math.sqrt(math.pi) if m == n else 0.0
            assert abs(val - exp) < 1e-3 * (1 + abs(exp))
    # Laguerre: delta
    for m in range(4):
        for n in range(4):
            val = orthogonality_laguerre(m, n)
            assert abs(val - (1.0 if m == n else 0.0)) < 2e-3


def test_ode_residuals():
    for n in range(1, 5):
        for x in (-0.4, 0.3, 0.65):
            assert abs(ode_residual("legendre", n, x)) < 1e-3
        for x in (-0.8, 0.5, 1.2):
            assert abs(ode_residual("hermite", n, x)) < 1e-2
            assert abs(ode_residual("laguerre", n, abs(x) + 0.3)) < 1e-2
        for x in (1.0, 2.5, 4.0):
            assert abs(ode_residual("bessel", n, x)) < 1e-3


def test_legendre_generating_function():
    for x in (-0.7, 0.0, 0.3, 0.9):
        for t in (0.2, 0.5, 0.8):
            s, closed = legendre_generating(x, t, nmax=60)
            assert _approx(s, closed, tol=1e-6)


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
