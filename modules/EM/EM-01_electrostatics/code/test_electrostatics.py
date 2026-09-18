"""Tests for EM-01 electrostatics. Reuses MA-01 (norm) and MA-02 (curl, div).

Run:  python3 test_electrostatics.py     ->  "All N tests passed."
"""
import math

from electrostatics import (
    EPS0, K_E, ELEM_CHARGE,
    point_charge_field, coulomb_field, force_on_charge,
    field_magnitude, field_of_distribution,
)
from vector_algebra import norm                          # ~MA-01
from vector_calculus import curl, divergence            # ~MA-02 on EM fields


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-6):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_constants():
    # k = 1/(4 pi eps0) ~ 8.9875e9 N m^2 / C^2
    assert _approx(K_E, 8.9875517923e9, tol=1e-6)
    assert _approx(K_E * 4.0 * math.pi * EPS0, 1.0, tol=1e-12)


def test_point_charge_magnitude_and_direction():
    q = 3e-9
    E = point_charge_field(q)
    for r in (0.1, 0.5, 2.0):
        assert _approx(field_magnitude(E)(r, 0, 0), K_E * q / r ** 2, tol=1e-9)
    # field of a positive charge points radially outward
    ex, ey, ez = E(0.3, 0.4, 0.0)                        # r = 0.5 along (0.6,0.8,0)
    assert _vapprox((ex, ey, ez),
                    (K_E * q / 0.25 * 0.6, K_E * q / 0.25 * 0.8, 0.0), tol=1e-9)


def test_superposition_midpoint_null():
    # two equal charges -> field cancels at the midpoint
    E = coulomb_field([(2e-9, (-0.05, 0, 0)), (2e-9, (0.05, 0, 0))])
    assert _vapprox(E(0, 0, 0), (0.0, 0.0, 0.0), tol=1e-12)
    # a dipole +q at x=-a, -q at x=+a: p = q*(2a) points in -x, so on the
    # perpendicular bisector the field is antiparallel to p, i.e. along +x.
    D = coulomb_field([(1e-9, (-0.05, 0, 0)), (-1e-9, (0.05, 0, 0))])
    dx, dy, dz = D(0, 0.05, 0)
    assert dx > 0 and _approx(dy, 0.0, tol=1e-12) and _approx(dz, 0.0, tol=1e-12)


def test_force_is_qE():
    E = point_charge_field(1e-9)
    Q = -4e-9
    F = force_on_charge(Q, E)
    p = (0.2, -0.1, 0.05)
    ex, ey, ez = E(*p)
    assert _vapprox(F(*p), (Q * ex, Q * ey, Q * ez), tol=1e-12)
    # opposite charges attract: F on -Q points back toward the source at origin
    assert dot_sign(F(*p), p) < 0


def dot_sign(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def test_curl_free_and_divergence_free():
    # electrostatic field is irrotational (curl E = 0) and source-free off the
    # charge (div E = 0). The finite-difference residual must be negligible
    # compared with the natural gradient scale |E|/r, not in absolute V/m (~EM-02).
    E = point_charge_field(5e-9, (0.0, 0.0, 0.0))
    p = (0.5, 0.3, -0.4)
    r = norm(p)
    scale = field_magnitude(E)(*p) / r                  # ~ |grad E|
    assert norm(curl(E)(*p)) <= 1e-5 * scale
    assert abs(divergence(E)(*p)) <= 1e-5 * scale


def test_distribution_far_field_is_monopole():
    # a uniformly charged cube, seen from far away, -> point charge k Q / r^2
    L, rho0 = 0.004, 1e-3
    Q = rho0 * L ** 3
    E = field_of_distribution(lambda x, y, z: rho0,
                              -L / 2, L / 2, -L / 2, L / 2, -L / 2, L / 2, n=12)
    r = 0.5
    assert _approx(field_magnitude(E)(r, 0, 0), K_E * Q / r ** 2, tol=2e-3)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
