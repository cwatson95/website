"""Tests for EM-06 conductors & capacitance. Reuses EM-01/EM-02.

Run:  python3 test_conductors_capacitance.py     ->  "All N tests passed."
"""
import math

# own module first: chains EM-01/EM-02 (and MA-01/MA-02) onto sys.path
from conductors_capacitance import (
    work_to_assemble, field_energy, field_energy_spherical,
    self_energy_uniform_sphere,
    capacitance_parallel_plate, capacitance_isolated_sphere,
    capacitance_spherical, capacitance_cylindrical,
    energy_stored, surface_pressure,
)
from electrostatics import EPS0, K_E, field_magnitude
from gauss_law import uniform_sphere_field


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_work_pairwise():
    # two charges: W = k q1 q2 / r
    q, r = 2e-9, 0.1
    W = work_to_assemble([(q, (0, 0, 0)), (q, (r, 0, 0))])
    assert _approx(W, K_E * q * q / r, tol=1e-12)
    # an equilateral triangle of side s: W = 3 k q^2 / s
    s = 0.2
    tri = [(q, (0, 0, 0)), (q, (s, 0, 0)), (q, (s / 2, s * math.sqrt(3) / 2, 0))]
    assert _approx(work_to_assemble(tri), 3 * K_E * q * q / s, tol=1e-9)


def test_field_energy_uniform_field_is_exact():
    # uniform field in a box: W = (eps0/2) E^2 * Vol  (integrand constant -> exact)
    E0 = 5000.0
    Euniform = lambda x, y, z: (0.0, 0.0, E0)
    W = field_energy(Euniform, 0, 0.1, 0, 0.2, 0, 0.05, n=6)
    vol = 0.1 * 0.2 * 0.05
    assert _approx(W, 0.5 * EPS0 * E0 ** 2 * vol, tol=1e-9)


def test_field_energy_of_sphere_matches_closed_form():
    # (eps0/2) int E^2 over all space = (3/5) k Q^2 / R  for the uniform sphere
    Q, R = 1e-9, 0.05
    Emag = lambda r: field_magnitude(uniform_sphere_field(Q, R))(r, 0, 0)
    W = field_energy_spherical(Emag, 0.0, 5000 * R, n=60000)
    assert _approx(W, self_energy_uniform_sphere(Q, R), tol=2e-3)


def test_capacitor_energy_consistency():
    # (1/2) C V^2 == (1/2) Q^2 / C  with Q = C V
    C = capacitance_parallel_plate(0.01, 1e-3)
    V = 50.0
    Q = C * V
    assert _approx(energy_stored(C, V), 0.5 * Q ** 2 / C, tol=1e-12)


def test_capacitance_formulas():
    # parallel plate
    assert _approx(capacitance_parallel_plate(0.02, 5e-4), EPS0 * 0.02 / 5e-4, tol=1e-12)
    # isolated sphere = limit of spherical capacitor as outer radius -> infinity
    a = 0.05
    assert _approx(capacitance_spherical(a, 1e7 * a), capacitance_isolated_sphere(a), tol=1e-5)
    # coax sanity: positive and grows with length
    assert capacitance_cylindrical(1e-3, 3e-3, 2.0) > capacitance_cylindrical(1e-3, 3e-3, 1.0) > 0


def test_surface_pressure_matches_field_form():
    # P = sigma^2/(2 eps0) = eps0 E^2 / 2 with E = sigma/eps0
    sigma = 2e-6
    E = sigma / EPS0
    assert _approx(surface_pressure(sigma), 0.5 * EPS0 * E ** 2, tol=1e-12)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
