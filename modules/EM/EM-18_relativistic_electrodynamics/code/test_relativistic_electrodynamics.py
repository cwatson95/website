"""Tests for EM-18 relativistic electrodynamics. Reuses EM-01/EM-08 and MA-01.

Run:  python3 test_relativistic_electrodynamics.py     ->  "All N tests passed."
"""
import math

# own module first: chains EM-01/EM-08 (and MA-01/MA-02) onto sys.path
from relativistic_electrodynamics import (
    C, gamma, field_tensor, fields_from_tensor,
    boost_fields, field_invariants, is_antisymmetric,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-9):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_gamma():
    assert _approx(gamma(0.0), 1.0)
    assert _approx(gamma(0.6), 1.25)               # 1/sqrt(1-0.36) = 1/0.8
    assert _approx(gamma(0.8), 5.0 / 3.0)


def test_field_tensor_antisymmetric_and_roundtrip():
    E = (300.0, -150.0, 75.0)
    B = (0.1, -0.2, 0.05)
    F = field_tensor(E, B)
    assert is_antisymmetric(F)
    assert _approx(F[0][1], E[0] / C)              # F^{0i} = E_i/c
    assert _approx(F[1][2], B[2])                  # F^{xy} = Bz
    E2, B2 = fields_from_tensor(F)
    assert _vapprox(E2, E) and _vapprox(B2, B)     # round trip


def test_parallel_field_unchanged():
    # a boost along x leaves the x-components of E and B unchanged
    E = (500.0, 0.0, 0.0)
    B = (0.3, 0.0, 0.0)
    Ep, Bp = boost_fields(E, B, 0.7)
    assert _approx(Ep[0], E[0]) and _approx(Bp[0], B[0])


def test_pure_E_field_generates_B():
    # a transverse pure-E field acquires a magnetic field after a boost
    E = (0.0, 1000.0, 0.0)
    B = (0.0, 0.0, 0.0)
    Ep, Bp = boost_fields(E, B, 0.6)
    assert Bp[2] != 0.0                            # B'_z appears
    g, v = gamma(0.6), 0.6 * C
    assert _approx(Ep[1], g * 1000.0)
    assert _approx(Bp[2], g * (-(v / C ** 2) * 1000.0))


def test_invariants_preserved_under_boost():
    E = (300.0, -120.0, 80.0)
    B = (0.05, 0.2, -0.1)
    I1, I2 = field_invariants(E, B)
    for beta in (0.2, 0.5, 0.9, 0.99):
        Ep, Bp = boost_fields(E, B, beta)
        I1p, I2p = field_invariants(Ep, Bp)
        assert _approx(I1p, I1, tol=1e-6)          # E.B invariant
        assert _approx(I2p, I2, tol=1e-6)          # B^2 - E^2/c^2 invariant


def test_perpendicular_E_B_stays_perpendicular():
    # E.B = 0 in one frame -> 0 in all frames (an invariant)
    E = (0.0, 1000.0, 0.0)
    B = (0.0, 0.0, 2e-6)
    I1, _ = field_invariants(E, B)
    assert _approx(I1, 0.0, tol=1e-6)
    Ep, Bp = boost_fields(E, B, 0.8)
    I1p, _ = field_invariants(Ep, Bp)
    assert _approx(I1p, 0.0, tol=1e-6)


def test_boost_then_inverse_recovers_fields():
    E = (200.0, -300.0, 100.0)
    B = (0.1, 0.05, -0.2)
    Ep, Bp = boost_fields(E, B, 0.5)
    E2, B2 = boost_fields(Ep, Bp, -0.5)            # inverse boost
    assert _vapprox(E2, E, tol=1e-6) and _vapprox(B2, B, tol=1e-6)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
