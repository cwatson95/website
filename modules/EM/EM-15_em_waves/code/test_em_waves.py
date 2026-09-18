"""Tests for EM-15 electromagnetic waves. Reuses EM-01/EM-08 and MA-01/MA-02.

Run:  python3 test_em_waves.py     ->  "All N tests passed."
"""
import math

# own module first: chains EM-01/EM-08 (and MA-01/MA-02) onto sys.path
from em_waves import (
    C, refractive_index, phase_velocity, wavelength,
    transverse_B, is_transverse,
    fresnel_normal, reflectance, transmittance,
    scalar_plane_wave, wave_equation_residual, classify_polarization,
)
from vector_algebra import dot, norm


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_index_and_velocity():
    assert _approx(refractive_index(2.25), 1.5)            # glass
    assert _approx(phase_velocity(2.25), C / 1.5)
    assert _approx(refractive_index(1.0), 1.0)             # vacuum


def test_transverse_B_relation():
    # B = (1/c) khat x E: perpendicular to E and k, magnitude |E|/c
    E0 = (1000.0, 0.0, 0.0)
    khat = (0.0, 0.0, 1.0)
    B0 = transverse_B(E0, khat)
    assert _approx(norm(B0), norm(E0) / C)
    assert is_transverse(E0, khat) and is_transverse(B0, khat)
    assert _approx(dot(E0, B0), 0.0)                       # E perp B
    # B0 should be along +y for E along x, k along z
    assert B0[1] > 0 and _approx(B0[0], 0.0) and _approx(B0[2], 0.0)


def test_fresnel_energy_conservation():
    # R + T = 1 at every interface (no absorption)
    for (n1, n2) in [(1.0, 1.5), (1.5, 1.0), (1.0, 2.4), (1.33, 1.0)]:
        R, T = reflectance(n1, n2), transmittance(n1, n2)
        assert _approx(R + T, 1.0, tol=1e-12)


def test_fresnel_known_values():
    # air -> glass: ~4% reflected
    R = reflectance(1.0, 1.5)
    assert _approx(R, ((1.0 - 1.5) / (1.0 + 1.5)) ** 2)    # = 0.04
    assert _approx(R, 0.04)
    # reflection off a denser medium flips sign of r (phase shift pi)
    r_into, _ = fresnel_normal(1.0, 1.5)
    r_outof, _ = fresnel_normal(1.5, 1.0)
    assert r_into < 0 < r_outof
    assert _approx(reflectance(1.0, 1.5), reflectance(1.5, 1.0))   # |r|^2 same both ways


def test_wave_equation_satisfied_when_dispersion_holds():
    # omega = v k -> residual ~ 0; wrong speed -> residual large
    k, v = 1.0, 1.0
    f = scalar_plane_wave(k, v * k)
    for (x, y, z, t) in [(0.1, 0.2, 0.3, 0.4), (1.0, -0.5, 0.7, 1.3)]:
        assert abs(wave_equation_residual(f, v, x, y, z, t)) < 1e-3
    # a wave with omega = vk but tested against the wrong speed v' fails
    assert abs(wave_equation_residual(f, 2.0, 0.1, 0.2, 0.3, 0.4)) > 0.1


def test_dispersion_relation():
    # lambda = 2 pi v / omega, and omega = v k
    omega, v = 3e15, C
    lam = wavelength(omega, v)
    k = 2 * math.pi / lam
    assert _approx(omega, v * k, tol=1e-9)


def test_polarization_classes():
    assert classify_polarization(1.0, 1.0, math.pi / 2) == "circular"
    assert classify_polarization(1.0, 1.0, -math.pi / 2) == "circular"
    assert classify_polarization(1.0, 1.0, 0.0) == "linear"
    assert classify_polarization(1.0, 1.0, math.pi) == "linear"
    assert classify_polarization(2.0, 1.0, math.pi / 2) == "elliptical"
    assert classify_polarization(1.0, 0.0, math.pi / 2) == "linear"   # one component


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
