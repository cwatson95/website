"""Tests for EM-07 dielectrics & polarization. Reuses EM-01/EM-02 and MA-02.

Run:  python3 test_dielectrics.py     ->  "All N tests passed."
"""
import math

# own module first: chains EM-01/EM-02 (and MA-01/MA-02) onto sys.path
from dielectrics import (
    bound_surface_charge, bound_volume_charge,
    displacement_field, displacement_point_free_charge, free_charge_enclosed,
    permittivity, susceptibility_from_eps_r, polarization_linear,
    displacement_linear, capacitance_with_dielectric,
    polarized_sphere_inner_field, polarized_sphere_surface_charge,
)
from electrostatics import EPS0, coulomb_field


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-6):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_bound_surface_charge():
    P = (0.0, 0.0, 3e-6)
    assert _approx(bound_surface_charge(P, (0, 0, 1)), 3e-6, tol=1e-12)     # top face
    assert _approx(bound_surface_charge(P, (0, 0, -1)), -3e-6, tol=1e-12)   # bottom
    assert _approx(bound_surface_charge(P, (1, 0, 0)), 0.0, tol=1e-12)      # side


def test_bound_volume_charge_uniform_is_zero():
    P = lambda x, y, z: (0.0, 0.0, 2e-6)                    # uniform
    assert _approx(bound_volume_charge(P, (0.1, 0.2, 0.3)), 0.0, tol=1e-6)
    # a non-uniform P = (0,0,a z) gives rho_b = -dPz/dz = -a
    a = 1e-4
    Pz = lambda x, y, z: (0.0, 0.0, a * z)
    assert _approx(bound_volume_charge(Pz, (0, 0, 0.5)), -a, tol=1e-4)


def test_displacement_definition():
    # D = eps0 E + P pointwise
    E = lambda x, y, z: (10.0, -5.0, 2.0)
    P = lambda x, y, z: (1e-9, 0.0, -3e-9)
    D = displacement_field(E, P)
    assert _vapprox(D(0, 0, 0), (EPS0 * 10 + 1e-9, EPS0 * -5, EPS0 * 2 - 3e-9), tol=1e-15)


def test_gauss_for_D_reads_free_charge():
    # oint D.da = Q_free, independent of the (linear) medium  (Eq. 4.23)
    qf = 5e-9
    D = displacement_point_free_charge(qf)
    for R in (0.1, 0.5, 2.0):
        assert _approx(free_charge_enclosed(D, R=R), qf, tol=1e-3)


def test_linear_relations_consistent():
    # eps_r = 1 + chi_e ; and D = eps E equals eps0 E + P with P = eps0 chi_e E
    eps_r = 4.0
    assert _approx(permittivity(eps_r), EPS0 * eps_r, tol=1e-15)
    assert _approx(susceptibility_from_eps_r(eps_r), 3.0, tol=1e-15)
    E = coulomb_field([(2e-9, (0, 0, 0))])
    P = polarization_linear(eps_r, E)
    D_eps = displacement_linear(eps_r, E)
    D_sum = displacement_field(E, P)
    p = (0.1, 0.05, -0.07)
    assert _vapprox(D_eps(*p), D_sum(*p), tol=1e-12)


def test_capacitance_scales_with_eps_r():
    assert _approx(capacitance_with_dielectric(1e-11, 5.0), 5e-11, tol=1e-15)


def test_polarized_sphere_inner_field_and_total_bound_charge():
    # inner field = -P/(3 eps0)
    P = (0.0, 0.0, 1e-6)
    Ein = polarized_sphere_inner_field(P)
    assert _vapprox(Ein, (0.0, 0.0, -1e-6 / (3 * EPS0)), tol=1e-9)
    # total bound surface charge = integral of P cos(theta) over the sphere = 0
    sigma = polarized_sphere_surface_charge(1e-6)
    n = 2000
    total = 0.0
    for k in range(n):
        th = math.pi * (k + 0.5) / n
        total += sigma(th) * 2 * math.pi * math.sin(th) * (math.pi / n)   # * R^2 dropped
    assert abs(total) < 1e-9


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
