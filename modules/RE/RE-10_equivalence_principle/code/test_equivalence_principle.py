"""Tests for RE-10 the equivalence principle.

Run directly:   python3 test_equivalence_principle.py   (-> "All N tests passed.")
Or with pytest: pytest test_equivalence_principle.py

The checks are property-based and use real physics: the redshift's sign and the
Pound-Rebka magnitude; the numerical IDENTITY of an accelerated frame and a
gravitational field (the equivalence itself); the consistency of redshift with
clock rates; the 1/r^3 tidal field that free fall cannot remove; and the Eotvos
figure of merit for the universality of free fall.
"""
import math
import random

from equivalence_principle import (
    C, G_NEWTON, STD_GRAVITY,
    grav_redshift, redshift_uniform_field, pound_rebka,
    accelerated_frame_redshift, grav_time_dilation,
    rindler_horizon, light_deflection_elevator,
    tidal_acceleration, eotvos_parameter,
)

TOL = 1e-12


def _approx(x, y, tol=TOL):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_grav_redshift_sign_and_magnitude():
    """Climbing OUT (delta_phi>0) reddens (negative); falling in blueshifts."""
    rng = random.Random(0)
    assert _approx(grav_redshift(0.0), 0.0)               # flat potential, no shift
    for _ in range(300):
        dphi = rng.uniform(1.0, 1e7)                      # photon climbs out
        assert grav_redshift(dphi) < 0.0                  # ... and is redshifted
        assert grav_redshift(-dphi) > 0.0                 # falling in -> blueshift
        assert _approx(grav_redshift(dphi), -dphi / C ** 2)
        assert _approx(abs(grav_redshift(dphi)), abs(grav_redshift(-dphi)))


def test_uniform_field_is_potential_redshift():
    """A uniform field of height h is just the potential gain Delta Phi = g h."""
    rng = random.Random(1)
    for _ in range(300):
        g = rng.uniform(0.1, 30.0)
        h = rng.uniform(1.0, 1e4)
        assert _approx(redshift_uniform_field(g, h), grav_redshift(g * h))
        assert _approx(redshift_uniform_field(g, h), -g * h / C ** 2)
        assert redshift_uniform_field(g, h) < 0.0          # rising light reddens


def test_equivalence_accelerated_equals_field():
    """THE equivalence: a rocket at a is numerically a field g = a (Zee V.2)."""
    rng = random.Random(2)
    for _ in range(500):
        a = rng.uniform(0.01, 1e3)
        h = rng.uniform(0.1, 1e4)
        assert _approx(accelerated_frame_redshift(a, h),
                       redshift_uniform_field(a, h))        # indistinguishable
        assert _approx(accelerated_frame_redshift(a, h), -a * h / C ** 2)


def test_pound_rebka_value_and_scaling():
    """The 22.5 m Harvard tower gives ~2.45e-15, linear in h, = field magnitude."""
    pr = pound_rebka()                                      # defaults: 22.5 m, g0
    assert abs(pr - 2.45e-15) <= 0.03 * 2.45e-15           # within a few percent
    assert _approx(pr, STD_GRAVITY * 22.5 / C ** 2)
    assert _approx(pr, abs(redshift_uniform_field(STD_GRAVITY, 22.5)))
    assert _approx(pound_rebka(h=45.0), 2.0 * pound_rebka(h=22.5))   # linear in h


def test_grav_time_dilation_lower_clock_slower():
    """A deeper (lower Phi) clock runs slow: ratio < 1; equal potentials -> 1."""
    rng = random.Random(3)
    assert _approx(grav_time_dilation(-5.0, -5.0), 1.0)    # same shelf -> no defect
    for _ in range(400):
        phi_up = rng.uniform(-1e7, -1.0)
        phi_lo = phi_up - rng.uniform(1.0, 1e7)            # strictly deeper
        ratio = grav_time_dilation(phi_lo, phi_up)
        assert ratio < 1.0                                 # lower clock ticks slow
        assert _approx(ratio, 1.0 + (phi_lo - phi_up) / C ** 2)


def test_redshift_timedilation_consistency():
    """Redshift IS the lower clock falling behind the upper one (one physics)."""
    rng = random.Random(4)
    for _ in range(400):
        phi_lo = rng.uniform(-1e7, -1.0)
        phi_up = phi_lo + rng.uniform(1.0, 1e7)            # receiver higher up
        # photon emitted low, received high: delta_phi = Phi_up - Phi_lo > 0
        red = grav_redshift(phi_up - phi_lo)
        rate_defect = grav_time_dilation(phi_lo, phi_up) - 1.0
        assert _approx(red, rate_defect)                   # redshift == clock defect


def test_rindler_horizon():
    """Horizon d = c^2/a, monotone decreasing, -> infinity as a -> 0."""
    rng = random.Random(5)
    assert rindler_horizon(0.0) == math.inf               # inertial: no horizon
    for _ in range(300):
        a = rng.uniform(1e-3, 1e4)
        assert _approx(rindler_horizon(a), C ** 2 / a)
        assert _approx(rindler_horizon(a) * a, C ** 2)     # d*a = c^2
    # smaller acceleration -> more distant horizon; vanishing a -> diverges
    assert rindler_horizon(1.0) > rindler_horizon(2.0)
    assert rindler_horizon(1e-9) > 1e20
    assert _approx(rindler_horizon(STD_GRAVITY), C ** 2 / STD_GRAVITY)


def test_light_deflection_elevator():
    """drop = (1/2) g (L/c)^2, angle = g L/c^2, and drop = (1/2) L * angle."""
    rng = random.Random(6)
    for _ in range(300):
        g = rng.uniform(0.1, 1e3)
        L = rng.uniform(0.1, 1e3)
        drop, angle = light_deflection_elevator(g, L)
        assert _approx(drop, 0.5 * g * (L / C) ** 2)
        assert _approx(angle, g * L / C ** 2)
        assert _approx(drop, 0.5 * L * angle)              # geometry ties them
        assert drop > 0.0 and angle > 0.0                  # light always "falls"
    # angle is linear in g, drop is quadratic in L
    d1, a1 = light_deflection_elevator(1.0, 1.0)
    d2, a2 = light_deflection_elevator(2.0, 1.0)
    assert _approx(a2, 2.0 * a1)
    d3, _ = light_deflection_elevator(1.0, 3.0)
    assert _approx(d3, 9.0 * d1)


def test_tidal_acceleration_scaling():
    """Tidal stretch ~ 1/r^3, ~ dr, matches 2GM dr/r^3 (Earth value sane)."""
    rng = random.Random(7)
    for _ in range(300):
        M = rng.uniform(1e20, 1e30)
        r = rng.uniform(1e6, 1e9)
        dr = rng.uniform(0.1, 100.0)
        assert _approx(tidal_acceleration(M, r, dr), 2.0 * G_NEWTON * M / r ** 3 * dr)
        assert _approx(tidal_acceleration(M, 2.0 * r, dr),
                       tidal_acceleration(M, r, dr) / 8.0)     # 1/r^3
        assert _approx(tidal_acceleration(M, r, 2.0 * dr),
                       2.0 * tidal_acceleration(M, r, dr))     # linear in dr
    # order-of-magnitude sanity: 1 m apart at Earth's surface
    M_E, R_E = 5.972e24, 6.371e6
    t = tidal_acceleration(M_E, R_E, 1.0)
    assert 1e-6 < t < 1e-5


def test_tidal_curvature_is_irreducible():
    """The point of the module: free fall removes g, never the tidal remainder.

    The uniform local field g = GM/r^2 is huge yet locally transformable away;
    the tidal difference -> 0 as the separation dr -> 0 but is strictly nonzero
    for any finite dr -- that irreducible piece is real curvature (RE-11).
    """
    M, r = 5.972e24, 6.371e6
    assert _approx(tidal_acceleration(M, r, 0.0), 0.0)        # vanishes at dr=0
    for dr in (1e-3, 1.0, 1e3):
        assert tidal_acceleration(M, r, dr) > 0.0            # but real if finite
    # the local field that free fall DOES remove dwarfs the tidal remainder
    local_g = G_NEWTON * M / r ** 2
    assert local_g > 1e6 * tidal_acceleration(M, r, 1.0)


def test_eotvos_parameter():
    """eta = 0 iff free fall is universal; symmetric; >0 measures violation."""
    rng = random.Random(8)
    for _ in range(300):
        a = rng.uniform(0.5, 20.0)
        assert _approx(eotvos_parameter(a, a), 0.0)          # UFF holds -> 0
        eps = rng.uniform(1e-15, 1e-3)
        a2 = a * (1.0 + eps)
        eta = eotvos_parameter(a, a2)
        assert eta > 0.0                                     # any difference shows
        assert _approx(eta, eotvos_parameter(a2, a))         # symmetric
        assert _approx(eta, 2.0 * abs(a - a2) / (a + a2))
    # a clean 1e-13 fractional difference reads back as eta ~ 1e-13
    assert _approx(eotvos_parameter(1.0, 1.0 + 1e-13), 1e-13, tol=1e-3)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
