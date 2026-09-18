"""Tests for MA-05 complex numbers. Pure stdlib.

Run:  python3 test_complex_numbers.py     ->  "All N tests passed."
"""
import math
import random

from complex_numbers import (
    modulus, argument, to_polar, from_polar, conjugate,
    euler, de_moivre, power, nth_roots, roots_of_unity,
    principal_sqrt, principal_log,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _capprox(z, w, tol=1e-9):
    return abs(z - w) <= tol * (1.0 + abs(w))


def test_polar_roundtrip():
    rng = random.Random(0)
    for _ in range(300):
        z = complex(rng.uniform(-3, 3), rng.uniform(-3, 3))
        r, th = to_polar(z)
        assert _capprox(from_polar(r, th), z)


def test_modulus_argument():
    assert _approx(modulus(complex(3, 4)), 5.0)
    assert _approx(argument(complex(0, 1)), math.pi / 2)
    assert _approx(argument(complex(-1, 0)), math.pi)
    assert _approx(argument(complex(1, 1)), math.pi / 4)


def test_euler():
    assert _capprox(euler(0.0), complex(1, 0))
    assert _capprox(euler(math.pi / 2), complex(0, 1))
    assert _capprox(euler(math.pi), complex(-1, 0))      # e^{i pi} + 1 = 0
    assert _approx(modulus(euler(1.234)), 1.0)           # always on the unit circle


def test_de_moivre():
    rng = random.Random(1)
    for _ in range(200):
        th = rng.uniform(-math.pi, math.pi)
        n = rng.randint(1, 6)
        assert _capprox(de_moivre(th, n), euler(th) ** n)         # (e^{i th})^n
        assert _capprox(de_moivre(th, n), power(euler(th), n))    # via polar power


def test_power_matches_integer_power():
    rng = random.Random(2)
    for _ in range(200):
        z = complex(rng.uniform(-2, 2), rng.uniform(-2, 2))
        n = rng.randint(2, 6)
        assert _capprox(power(z, n), z ** n, tol=1e-7)


def test_nth_roots():
    for z in (complex(8, 0), complex(1, 1), complex(-4, 3)):
        for n in (2, 3, 5):
            roots = nth_roots(z, n)
            assert len(roots) == n
            for w in roots:
                assert _capprox(w ** n, z, tol=1e-8)              # each root^n = z


def test_roots_of_unity():
    for n in range(2, 8):
        roots = roots_of_unity(n)
        assert len(roots) == n
        assert _capprox(roots[0], complex(1, 0))
        assert all(_approx(modulus(w), 1.0) for w in roots)
        assert _capprox(sum(roots), complex(0, 0), tol=1e-9)     # they sum to zero


def test_principal_branches():
    assert _capprox(principal_sqrt(complex(-1, 0)), complex(0, 1))      # sqrt(-1) = +i (principal)
    assert _capprox(principal_log(complex(-1, 0)), complex(0, math.pi))  # Log(-1) = i pi
    rng = random.Random(3)
    for _ in range(200):
        z = complex(rng.uniform(-3, 3), rng.uniform(-3, 3))
        if z == 0:
            continue
        assert _capprox(principal_sqrt(z) ** 2, z, tol=1e-8)
        # exp(Log z) = z, with exp built from the polar pieces
        lg = principal_log(z)
        assert _capprox(from_polar(math.exp(lg.real), lg.imag), z, tol=1e-8)
    # branch cut: just above vs just below the negative real axis -> arg flips sign
    above = principal_sqrt(complex(-1.0, 1e-9))
    below = principal_sqrt(complex(-1.0, -1e-9))
    assert above.imag > 0 and below.imag < 0                   # the discontinuity across the cut


def test_conjugate():
    z = complex(2, -3)
    assert conjugate(z) == complex(2, 3)
    assert _approx((z * conjugate(z)).real, modulus(z) ** 2) and _approx((z * conjugate(z)).imag, 0.0)


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
