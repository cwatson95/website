"""Tests for EM-13 Maxwell's equations. Reuses EM-01/EM-08 and MA-02.

Run:  python3 test_maxwell_equations.py     ->  "All N tests passed."
"""
import math

# own module first: chains EM-01/EM-08 (and MA-01/MA-02) onto sys.path
from maxwell_equations import (
    EPS0, MU0, C_SI, displacement_current_density,
    plane_wave_fields, partial_t,
    gauss_E_residual, gauss_B_residual, faraday_residual, ampere_maxwell_residual,
    verify_vacuum_plane_wave,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_speed_of_light_from_constants():
    assert _approx(C_SI, 2.99792458e8, tol=1e-6)        # 1/sqrt(mu0 eps0) = c


def test_displacement_current():
    Jd = displacement_current_density((2e12, -1e12, 0.0))
    assert _approx(Jd[0], EPS0 * 2e12, tol=1e-12)
    assert _approx(Jd[1], EPS0 * -1e12, tol=1e-12)


def test_plane_wave_structure():
    # B0 = E0/c, B perpendicular to E, both transverse to propagation (+z)
    E, B, w = plane_wave_fields(3.0, 2.0, c=1.0)
    assert _approx(w, 2.0)                                # w = c k
    ex, ey, ez = E(0.1, 0.2, 0.3, 0.4)
    bx, by, bz = B(0.1, 0.2, 0.3, 0.4)
    assert ey == 0 and ez == 0                           # E along x
    assert bx == 0 and bz == 0                           # B along y (perp to E)
    # E x B points along +z (the propagation direction)
    assert ex * by > 0


def test_vacuum_plane_wave_satisfies_all_four():
    # the headline: every Maxwell residual vanishes for a vacuum plane wave
    for (point, t) in [((0.1, 0.2, 0.3), 0.4), ((1.0, -0.5, 0.7), 1.3), ((-0.3, 0.0, 2.1), -0.6)]:
        res = verify_vacuum_plane_wave(1.0, 1.0, 1.0, point, t)
        for name, r in res.items():
            assert abs(r) < 1e-4, (name, r, point, t)


def test_wrong_dispersion_breaks_ampere():
    # if w != c k the wave is NOT a Maxwell solution: build E with c=1 but
    # B with the wrong speed, and check Faraday/Ampere no longer balance.
    E, _, _ = plane_wave_fields(1.0, 1.0, c=1.0)          # w = 1
    _, Bwrong, _ = plane_wave_fields(1.0, 1.0, c=2.0)     # B0 and w mismatched
    x, y, z, t = 0.1, 0.2, 0.3, 0.4
    r = faraday_residual(E, Bwrong, x, y, z, t)
    assert r > 0.1                                        # badly violated


def test_faraday_and_ampere_individually():
    E, B, w = plane_wave_fields(2.0, 1.5, c=1.0)
    x, y, z, t = 0.4, -0.2, 0.9, 0.7
    assert faraday_residual(E, B, x, y, z, t) < 1e-4
    assert ampere_maxwell_residual(E, B, (0, 0, 0), x, y, z, t, c=1.0) < 1e-4
    assert abs(gauss_E_residual(E, 0.0, x, y, z, t)) < 1e-4
    assert abs(gauss_B_residual(B, x, y, z, t)) < 1e-4


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
