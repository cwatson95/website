"""Tests for CM-08 collisions & scattering. Reuses CM-07 (imported transitively).

Run:  python3 test_collisions.py     ->  "All N tests passed."
"""
import math

from collisions import (
    elastic_collision_1d, inelastic_collision, kinetic_energy_1d,
    rutherford_angle, rutherford_cross_section,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_elastic_conserves_p_and_KE():
    cases = [(1.0, 3.0, 1.0, -1.0), (2.0, 5.0, 3.0, -2.0), (0.5, 0.0, 4.0, 1.0)]
    for m1, v1, m2, v2 in cases:
        v1p, v2p = elastic_collision_1d(m1, v1, m2, v2)
        assert _approx(m1 * v1p + m2 * v2p, m1 * v1 + m2 * v2)                       # momentum
        assert _approx(kinetic_energy_1d(m1, v1p) + kinetic_energy_1d(m2, v2p),
                       kinetic_energy_1d(m1, v1) + kinetic_energy_1d(m2, v2))        # kinetic energy


def test_equal_mass_exchange():
    v1p, v2p = elastic_collision_1d(2.0, 5.0, 2.0, -1.0)
    assert _approx(v1p, -1.0) and _approx(v2p, 5.0)                                  # velocities swap


def test_heavy_wall_reflects():
    v1p, v2p = elastic_collision_1d(1.0, 2.0, 1e12, 0.0)
    assert _approx(v1p, -2.0, tol=1e-6) and abs(v2p) < 1e-6                          # bounce back


def test_inelastic_conserves_p_loses_KE():
    m1, v1, m2, v2 = 2.0, [4.0, 0.0, 0.0], 1.0, [0.0, 0.0, 0.0]
    vc = inelastic_collision(m1, v1, m2, v2)
    assert _approx(vc[0], (m1 * v1[0] + m2 * v2[0]) / (m1 + m2))                      # = CM velocity
    Pbefore = m1 * v1[0] + m2 * v2[0]
    Pafter = (m1 + m2) * vc[0]
    assert _approx(Pbefore, Pafter)                                                  # momentum conserved
    KE_before = kinetic_energy_1d(m1, v1[0]) + kinetic_energy_1d(m2, v2[0])
    KE_after = kinetic_energy_1d(m1 + m2, vc[0])
    assert KE_after < KE_before                                                      # energy lost


def test_rutherford_angle_inverse():
    # theta = 2 atan(k/2Eb)  <=>  b = (k/2E) cot(theta/2)
    E, k = 1.0, 1.0
    for b in (0.2, 0.5, 1.0, 3.0):
        th = rutherford_angle(b, E, k)
        b_back = (k / (2.0 * E)) / math.tan(th / 2.0)
        assert _approx(b_back, b, tol=1e-9)
    # b=0.5, E=k=1 -> exactly 90 degrees
    assert _approx(rutherford_angle(0.5, 1.0, 1.0), math.pi / 2)


def test_rutherford_cross_section_forward_divergence():
    E, k = 2.0, 1.5
    near = rutherford_cross_section(math.radians(1), E, k)
    wide = rutherford_cross_section(math.radians(90), E, k)
    assert near > wide and near > 1e4                                               # diverges as theta->0
    # explicit value check at 90 deg: (k/4E)^2 / sin^4(45)
    assert _approx(rutherford_cross_section(math.pi / 2, E, k), (k / (4 * E)) ** 2 / (0.5 ** 2))


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
