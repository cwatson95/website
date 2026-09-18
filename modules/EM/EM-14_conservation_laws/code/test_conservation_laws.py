"""Tests for EM-14 conservation laws. Reuses EM-01/EM-08 and MA-01.

Run:  python3 test_conservation_laws.py     ->  "All N tests passed."
"""
import math

# own module first: chains EM-01/EM-08 (and MA-01/MA-02) onto sys.path
from conservation_laws import (
    EPS0, MU0, C,
    poynting_vector, energy_density, momentum_density,
    maxwell_stress_tensor, radiation_pressure, plane_wave_snapshot,
)
from vector_algebra import dot, norm


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_poynting_points_along_propagation():
    # E along x, B along y -> S along +z
    E = lambda x, y, z: (500.0, 0.0, 0.0)
    B = lambda x, y, z: (0.0, 500.0 / C, 0.0)
    S = poynting_vector(E, B)(0, 0, 0)
    assert S[0] == 0 and S[1] == 0 and S[2] > 0
    assert _approx(S[2], 500.0 * (500.0 / C) / MU0)


def test_plane_wave_equipartition():
    # electric and magnetic energy densities are equal when B = E/c
    E, B = plane_wave_snapshot(800.0, k=0.0)
    e = E(0, 0, 0)
    b = B(0, 0, 0)
    uE = 0.5 * EPS0 * dot(e, e)
    uB = dot(b, b) / (2 * MU0)
    assert _approx(uE, uB)


def test_S_equals_c_times_u():
    # for a plane wave, energy flux = c * energy density
    E, B = plane_wave_snapshot(1234.0, k=0.0)
    S = poynting_vector(E, B)
    u = energy_density(E, B)
    p = (0.1, 0.2, 0.3)
    assert _approx(norm(S(*p)), C * u(*p))


def test_momentum_density_is_S_over_c2():
    E, B = plane_wave_snapshot(600.0, k=0.0)
    S = poynting_vector(E, B)
    g = momentum_density(E, B)
    p = (0, 0, 0)
    assert _approx(norm(g(*p)), norm(S(*p)) / C ** 2)
    # and |g| = u/c
    u = energy_density(E, B)
    assert _approx(norm(g(*p)), u(*p) / C)


def test_radiation_pressure():
    Smag = 1361.0                                   # solar constant, W/m^2
    assert _approx(radiation_pressure(Smag), Smag / C)
    assert _approx(radiation_pressure(Smag, reflected=True), 2 * Smag / C)


def test_stress_tensor_symmetric_and_Tzz():
    E, B = plane_wave_snapshot(700.0, k=0.0)
    T = maxwell_stress_tensor(E, B)(0, 0, 0)
    # symmetric
    for i in range(3):
        for j in range(3):
            assert _approx(T[i][j], T[j][i])
    # for a +z wave, T_zz = -(energy density)  (the pressure pushing along z)
    u = energy_density(E, B)(0, 0, 0)
    assert _approx(T[2][2], -u)


def test_static_field_has_no_poynting_flux():
    # a purely electrostatic (or magnetostatic) field carries no energy flow
    E = lambda x, y, z: (100.0, 50.0, -20.0)
    Bzero = lambda x, y, z: (0.0, 0.0, 0.0)
    assert norm(poynting_vector(E, Bzero)(0, 0, 0)) == 0.0


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
