"""Tests for EM-05 multipole expansion. Reuses EM-01/EM-03 and MA-01.

Run:  python3 test_multipole.py     ->  "All N tests passed."
"""
import math

# own module first: chains EM-01/EM-03 (and MA-01/MA-02) onto sys.path
from multipole import (
    monopole_moment, dipole_moment, quadrupole_moment,
    dipole_potential, dipole_field, multipole_potential,
)
from electric_potential import potential_point_charges
from electrostatics import K_E
from vector_algebra import norm


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-6):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_moments_of_a_physical_dipole():
    q, a = 2e-9, 0.01
    dip = [(q, (0, 0, a / 2)), (-q, (0, 0, -a / 2))]
    assert _approx(monopole_moment(dip), 0.0, tol=1e-20)
    assert _vapprox(dipole_moment(dip), (0.0, 0.0, q * a), tol=1e-12)


def test_dipole_moment_origin_independent_when_neutral():
    q = 1e-9
    dip = [(q, (0.1, 0, 0)), (-q, (0.0, 0, 0))]
    p1 = dipole_moment(dip)
    shifted = [(q, (0.1 + 0.3, 0.2, 0.5)), (-q, (0.0 + 0.3, 0.2, 0.5))]
    p2 = dipole_moment(shifted)
    assert _vapprox(p1, p2, tol=1e-15)                     # neutral -> p is origin-free


def test_dipole_field_axis_and_bisector():
    p = (0.0, 0.0, 3e-11)
    E = dipole_field(p)
    pm = norm(p)
    z = 0.1
    # on axis: 2 k p / r^3 along +z
    assert _vapprox(E(0, 0, z), (0.0, 0.0, 2 * K_E * pm / z ** 3), tol=1e-9)
    # on the perpendicular bisector: -k p / r^3 (antiparallel to p)
    assert _vapprox(E(z, 0, 0), (0.0, 0.0, -K_E * pm / z ** 3), tol=1e-9)


def test_dipole_potential_matches_far_field():
    # pure-dipole potential approaches the exact two-charge potential as r grows
    q, a = 1e-9, 0.004
    dip = [(q, (0, 0, a / 2)), (-q, (0, 0, -a / 2))]
    p = dipole_moment(dip)
    Vexact = potential_point_charges(dip)
    Vdip = dipole_potential(p)
    # at r = 100a the pure-dipole form is within ~0.01% of exact
    for direction in [(0, 0, 1), (1, 0, 0), (1, 1, 1)]:
        r = 100 * a
        u = norm(direction)
        pt = tuple(r * c / u for c in direction)
        assert _approx(Vdip(*pt), Vexact(*pt), tol=2e-3)


def test_expansion_converges_with_order():
    # adding the dipole term reduces the far-field error vs monopole-only
    q, a = 1e-9, 0.005
    dip = [(q, (0, 0, a / 2)), (-q, (0, 0, -a / 2))]
    Vexact = potential_point_charges(dip)
    r = 30 * a
    pt = (0, 0, r)
    err_mono = abs(multipole_potential(dip, 0)(*pt) - Vexact(*pt))
    err_dip = abs(multipole_potential(dip, 1)(*pt) - Vexact(*pt))
    # monopole term is ~0 (neutral); dipole term captures the real 1/r^2 potential
    assert err_dip < err_mono
    assert err_dip / abs(Vexact(*pt)) < 1e-2


def test_quadrupole_of_linear_quadrupole():
    # charges +q, -2q, +q on the z-axis: monopole and dipole vanish, Q_zz != 0
    q, a = 1e-9, 0.01
    cfg = [(q, (0, 0, a)), (-2 * q, (0, 0, 0)), (q, (0, 0, -a))]
    assert _approx(monopole_moment(cfg), 0.0, tol=1e-20)
    assert _vapprox(dipole_moment(cfg), (0, 0, 0), tol=1e-20)
    Q = quadrupole_moment(cfg)
    # Q_zz = sum q (3 z^2 - r^2) = sum q (2 z^2) = 2 q a^2 + 0 + 2 q a^2 = 4 q a^2
    assert _approx(Q[2][2], 4 * q * a ** 2, tol=1e-12)
    assert _approx(Q[0][0], -2 * q * a ** 2, tol=1e-12)    # traceless: Q_xx = Q_yy = -Q_zz/2


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
