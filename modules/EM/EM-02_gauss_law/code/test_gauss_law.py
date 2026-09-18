"""Tests for EM-02 Gauss's law. Reuses EM-01 (fields) and MA-02 (surface_flux).

Run:  python3 test_gauss_law.py     ->  "All N tests passed."
"""
import math

# import the module under test first: it chains EM-01 (and MA-01/MA-02) onto sys.path
from gauss_law import (
    flux_through_sphere, enclosed_charge, gauss_residual,
    uniform_sphere_field, line_charge_field, plane_sheet_field,
)
from electrostatics import EPS0, K_E, point_charge_field, coulomb_field, field_magnitude


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_point_charge_flux_is_q_over_eps0():
    # Gauss: flux through ANY enclosing sphere = q/eps0, independent of radius.
    q = 3e-9
    E = point_charge_field(q)
    for R in (0.2, 1.0, 5.0):
        assert _approx(EPS0 * flux_through_sphere(E, (0, 0, 0), R), q, tol=1e-3)


def test_flux_independent_of_center_offset():
    # charge off-center but still inside -> still q/eps0
    q = 1e-9
    E = point_charge_field(q, (0.1, -0.05, 0.05))
    assert _approx(enclosed_charge(E, (0, 0, 0), 1.0), q, tol=1e-3)


def test_charge_outside_gives_zero_flux():
    q = 2e-9
    E = point_charge_field(q, (3.0, 0.0, 0.0))             # well outside R=1
    assert abs(EPS0 * flux_through_sphere(E, (0, 0, 0), 1.0)) < 1e-3 * q


def test_superposition_of_flux():
    # net flux counts only enclosed charge: +q inside, -q/2 inside, +5q outside
    q = 1e-9
    E = coulomb_field([(q, (0.1, 0, 0)), (-0.5 * q, (0, 0.2, 0)), (5 * q, (10.0, 0, 0))])
    assert _approx(enclosed_charge(E, (0, 0, 0), 1.0), 0.5 * q, tol=2e-3)


def test_uniform_sphere_inside_outside():
    Q, R = 4e-9, 0.2
    E = uniform_sphere_field(Q, R)
    # outside: point charge
    assert _approx(field_magnitude(E)(3 * R, 0, 0), K_E * Q / (3 * R) ** 2, tol=1e-9)
    # inside: linear in r
    assert _approx(field_magnitude(E)(0.5 * R, 0, 0), K_E * Q * (0.5 * R) / R ** 3, tol=1e-9)
    # continuous at the surface
    assert _approx(field_magnitude(E)(R * (1 - 1e-9), 0, 0),
                   field_magnitude(E)(R * (1 + 1e-9), 0, 0), tol=1e-4)


def test_differential_gauss_inside_sphere():
    # div E = rho/eps0 inside a uniform sphere (Eq. 2.16)
    Q, R = 4e-9, 0.2
    E = uniform_sphere_field(Q, R)
    rho = Q / ((4.0 / 3.0) * math.pi * R ** 3)
    assert abs(gauss_residual(E, rho, (R / 3, R / 5, -R / 4))) < 1e-3


def test_line_charge_falls_like_inverse_s():
    lam = 2e-9
    E = line_charge_field(lam)
    for s in (0.05, 0.1, 0.4):
        assert _approx(field_magnitude(E)(s, 0, 0), lam / (2 * math.pi * EPS0 * s), tol=1e-12)
    # purely radial (no z-component on the z-axis-perp plane)
    assert _approx(E(0.1, 0.0, 0.7)[2], 0.0, tol=1e-12)


def test_plane_sheet_uniform_and_jump():
    sigma = 1e-9
    E = plane_sheet_field(sigma)
    # uniform magnitude sigma/2eps0, independent of distance
    assert _approx(E(0, 0, 0.5)[2], sigma / (2 * EPS0), tol=1e-12)
    assert _approx(E(1, 2, 3.0)[2], sigma / (2 * EPS0), tol=1e-12)
    # discontinuity sigma/eps0 across the sheet
    jump = E(0, 0, 1e-9)[2] - E(0, 0, -1e-9)[2]
    assert _approx(jump, sigma / EPS0, tol=1e-12)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
