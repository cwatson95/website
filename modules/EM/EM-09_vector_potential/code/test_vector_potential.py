"""Tests for EM-09 vector potential. Reuses EM-08 (fields) and MA-02 (curl/div).

Run:  python3 test_vector_potential.py     ->  "All N tests passed."
"""
import math

# own module first: chains EM-08 (and MA-01/MA-02) onto sys.path
from vector_potential import (
    magnetic_dipole_moment, dipole_vector_potential, dipole_B_field_closed,
    B_from_A, coulomb_gauge_residual, wire_vector_potential,
)
from magnetostatics import MU0, infinite_wire_field
from vector_algebra import norm


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _rel_close(u, v, tol):
    """vectors close relative to |v| (good for finite-difference curls)."""
    diff = math.sqrt(sum((a - b) ** 2 for a, b in zip(u, v)))
    return diff <= tol * (norm(v) + 1e-30)


def test_magnetic_moment_is_I_times_area():
    I, area = 3.0, (0.0, 0.0, 0.02)
    assert magnetic_dipole_moment(I, area) == (0.0, 0.0, 0.06)


def test_B_equals_curl_A_for_dipole():
    # the headline identity: B = curl A reproduces the closed-form dipole field
    m = (0.0, 0.0, 4e-3)
    A = dipole_vector_potential(m)
    Bnum = B_from_A(A)
    Bexact = dipole_B_field_closed(m)
    for p in [(0.1, 0.0, 0.0), (0.0, 0.0, 0.1), (0.05, 0.05, 0.1), (-0.08, 0.03, 0.06)]:
        assert _rel_close(Bnum(*p), Bexact(*p), tol=1e-3)


def test_dipole_field_axis_bisector_ratio():
    # like the electric dipole (~EM-05): axial field is twice the equatorial, opposite sign
    m = (0.0, 0.0, 2e-3)
    B = dipole_B_field_closed(m)
    pref = MU0 / (4 * math.pi)
    d = 0.1
    assert _approx(B(0, 0, d)[2], 2 * pref * norm(m) / d ** 3, tol=1e-12)       # on axis
    assert _approx(B(d, 0, 0)[2], -pref * norm(m) / d ** 3, tol=1e-12)          # bisector


def test_coulomb_gauge_satisfied():
    # the dipole A is divergence-free
    m = (0.0, 0.0, 4e-3)
    A = dipole_vector_potential(m)
    for p in [(0.1, 0.05, 0.08), (0.07, -0.04, 0.09)]:
        assert abs(coulomb_gauge_residual(A, p)) < 1e-3


def test_wire_potential_curls_to_wire_field():
    # B = curl A of the wire's vector potential equals the EM-08 wire field
    I = 10.0
    A = wire_vector_potential(I)
    Bnum = B_from_A(A)
    Bexact = infinite_wire_field(I)
    for p in [(0.05, 0.0, 0.0), (0.03, 0.04, 0.2), (-0.06, 0.02, -0.1)]:
        assert _rel_close(Bnum(*p), Bexact(*p), tol=1e-3)


def test_dipole_A_falls_like_inverse_r_squared():
    m = (0.0, 0.0, 1e-3)
    A = dipole_vector_potential(m)
    # along x (where A is purely +/-y): |A| ~ 1/r^2
    a1 = norm(A(0.1, 0, 0))
    a2 = norm(A(0.2, 0, 0))
    assert _approx(a1 / a2, 4.0, tol=1e-6)                  # (0.2/0.1)^2 = 4


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
