"""Tests for PK-02 fluid & MHD description.

Run:  python3 test_fluid_mhd.py     ->  "All N tests passed."
"""
import numpy as np

from fluid_mhd import (
    MU0, K_B, M_P,
    moments_of_maxwellian,
    sound_speed, alfven_speed, fast_magnetosonic_speed,
    magnetic_pressure, plasma_beta,
    continuity_residual,
)


def test_moments_recover_density_velocity_pressure():
    # 0th/1st/2nd velocity moments of a drifting Maxwellian return (n, u, n k_B T)
    n, u, T, m = 1.0e19, (1.0e5, 0.0, 0.0), 1.0e5, M_P
    n_rec, u_rec, p_rec = moments_of_maxwellian(n, u, T, m)
    assert abs(n_rec / n - 1.0) < 1e-6                       # 0th moment -> n
    assert abs(u_rec[0] - u[0]) < 1e-3 * u[0]                # 1st moment -> u_x
    assert abs(u_rec[1]) < 1.0 and abs(u_rec[2]) < 1.0       # no transverse drift
    assert abs(p_rec / (n * K_B * T) - 1.0) < 1e-6           # 2nd moment -> n k_B T


def test_moments_zero_drift_isotropic():
    # with u = 0 the mean velocity vanishes and p = n k_B T still holds
    n, T, m = 5.0e18, 3.0e5, M_P
    n_rec, u_rec, p_rec = moments_of_maxwellian(n, (0.0, 0.0, 0.0), T, m)
    assert np.max(np.abs(u_rec)) < 1e-3 * np.sqrt(K_B * T / m)
    assert abs(p_rec - n * K_B * T) < 1e-6 * n * K_B * T


def test_pressure_scales_with_temperature():
    # ideal-gas closure p = n k_B T: doubling T doubles the recovered pressure
    n, m = 1.0e19, M_P
    _, _, p1 = moments_of_maxwellian(n, (0.0, 0.0, 0.0), 1.0e5, m)
    _, _, p2 = moments_of_maxwellian(n, (0.0, 0.0, 0.0), 2.0e5, m)
    assert abs(p2 / p1 - 2.0) < 1e-4


def test_sound_speed_formula_and_scaling():
    gamma, p, rho = 5.0 / 3.0, 160.0, 1.67e-8
    assert np.isclose(sound_speed(gamma, p, rho), np.sqrt(gamma * p / rho))
    # c_s ~ sqrt(p): quadrupling pressure doubles the sound speed
    assert np.isclose(sound_speed(gamma, 4 * p, rho) / sound_speed(gamma, p, rho), 2.0)


def test_alfven_speed_formula_and_scaling():
    B, rho = 1.0, 1.67e-8
    assert np.isclose(alfven_speed(B, rho), B / np.sqrt(MU0 * rho))
    # v_A ~ B and v_A ~ 1/sqrt(rho)
    assert np.isclose(alfven_speed(2 * B, rho) / alfven_speed(B, rho), 2.0)
    assert np.isclose(alfven_speed(B, 4 * rho) / alfven_speed(B, rho), 0.5)


def test_fast_magnetosonic_is_quadrature_sum():
    c_s, v_A = 1.26e5, 6.9e6
    v_f = fast_magnetosonic_speed(c_s, v_A)
    assert np.isclose(v_f, np.hypot(c_s, v_A))
    # the fast speed bounds both component speeds
    assert v_f >= c_s and v_f >= v_A
    # pure-sound and pure-Alfven limits
    assert np.isclose(fast_magnetosonic_speed(c_s, 0.0), c_s)
    assert np.isclose(fast_magnetosonic_speed(0.0, v_A), v_A)


def test_magnetic_pressure():
    B = 1.0
    assert np.isclose(magnetic_pressure(B), B ** 2 / (2.0 * MU0))
    # magnetic pressure ~ B^2
    assert np.isclose(magnetic_pressure(3 * B) / magnetic_pressure(B), 9.0)


def test_plasma_beta_is_thermal_over_magnetic_pressure():
    n, T, B = 1.0e19, 1.16e6, 1.0
    beta = plasma_beta(n, T, B)
    assert np.isclose(beta, (n * K_B * T) / magnetic_pressure(B))
    assert beta < 1.0                                         # magnetically dominated
    # beta ~ n T and beta ~ 1/B^2
    assert np.isclose(plasma_beta(2 * n, T, B) / beta, 2.0)
    assert np.isclose(plasma_beta(n, T, 2 * B) / beta, 0.25)


def test_beta_equals_two_mu0_p_over_B2():
    # closed-form cross-check  beta = 2 mu0 n k_B T / B^2
    n, T, B = 3.0e18, 5.0e5, 0.5
    assert np.isclose(plasma_beta(n, T, B), 2.0 * MU0 * n * K_B * T / B ** 2)


def test_continuity_residual_vanishes_for_advected_density():
    # 0th-moment law: d rho/dt + d(rho u)/dx = 0 for a rigid travelling wave
    x = np.linspace(-20.0, 20.0, 400)
    dx = x[1] - x[0]
    u, dt = 0.5, 1e-3
    bump = lambda xx: np.exp(-(xx) ** 2)
    rho0 = bump(x)
    rho1 = bump(x - u * dt)
    res = continuity_residual(rho0, rho1, u, dx, dt)
    drho_dt = (rho1 - rho0) / dt
    # residual is tiny compared with the (large) individual time-derivative term
    assert np.max(np.abs(res)) < 1e-2 * np.max(np.abs(drho_dt))


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
