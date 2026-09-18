"""Tests for EM-11 induction. Reuses EM-08 (MU0) and MA-02 (surface_flux).

Run:  python3 test_induction.py     ->  "All N tests passed."
"""
import math

# own module first: chains EM-08 (and MA-01/MA-02) onto sys.path
from induction import (
    flat_loop_surface, magnetic_flux, faraday_emf, lenz_sign, motional_emf,
    solenoid_inductance, mutual_inductance_solenoids,
    energy_in_inductor, magnetic_energy_density, magnetic_field_energy_solenoid,
)
from magnetostatics import MU0


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_uniform_flux_through_loop():
    # Phi = B . A for a flat 1 m^2 loop in a uniform field B0 zhat
    B0 = 0.4
    B = lambda x, y, z: (0.0, 0.0, B0)
    surf = flat_loop_surface(0.0, 1.0, 0.0, 1.0, 0.0)
    assert _approx(magnetic_flux(B, surf), B0 * 1.0, tol=1e-6)
    # a half-area loop gets half the flux
    surf2 = flat_loop_surface(0.0, 0.5, 0.0, 1.0, 0.0)
    assert _approx(magnetic_flux(B, surf2), B0 * 0.5, tol=1e-6)


def test_faraday_sinusoid():
    # Phi(t) = B0 A sin(wt) -> EMF = -B0 A w cos(wt)
    B0, A, w = 0.5, 0.01, 100.0
    flux = lambda t: B0 * A * math.sin(w * t)
    for t in (0.0, 0.003, 0.0157):
        assert _approx(faraday_emf(flux, t), -B0 * A * w * math.cos(w * t), tol=1e-4)


def test_lenz_sign():
    assert lenz_sign(+2.0) == -1          # rising flux -> opposing (negative) EMF
    assert lenz_sign(-2.0) == +1
    assert lenz_sign(0.0) == 0


def test_motional_emf():
    assert _approx(motional_emf(0.3, 2.0, 0.5), 0.3, tol=1e-12)


def test_inductance_formulas_and_symmetry():
    N, A, l = 500, 2e-4, 0.15
    L = solenoid_inductance(N, A, l)
    assert _approx(L, MU0 * N ** 2 * A / l, tol=1e-12)
    # mutual inductance is symmetric
    assert _approx(mutual_inductance_solenoids(300, 700, A, l),
                   mutual_inductance_solenoids(700, 300, A, l), tol=1e-15)


def test_energy_two_pictures():
    # (1/2) L I^2  ==  (1/2 mu0) int B^2 dtau   for a solenoid
    N, A, l, I = 1000, 1e-4, 0.2, 3.0
    L = solenoid_inductance(N, A, l)
    W_circuit = energy_in_inductor(L, I)
    W_field = magnetic_field_energy_solenoid(N, A, l, I)
    assert _approx(W_circuit, W_field, tol=1e-9)


def test_magnetic_energy_density():
    B = lambda x, y, z: (0.0, 0.0, 1.2)
    u = magnetic_energy_density(B)
    assert _approx(u(0, 0, 0), 1.2 ** 2 / (2 * MU0), tol=1e-9)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
