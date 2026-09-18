"""Tests for QF-05  QFT in curved spacetime -- Hawking & Unruh effects.

Run:  python3 test_curved_spacetime.py     ->  "All N tests passed."
"""
import numpy as np

from curved_spacetime import (
    HBAR, C, K_B, G, M_SUN,
    schwarzschild_radius, surface_gravity,
    unruh_temperature, hawking_temperature,
    bose_occupation, fermi_occupation,
    bogoliubov_check, particle_number, squeeze_to_bogoliubov,
    thermal_beta_squared, unruh_beta_ratio, unruh_occupation,
    evaporation_lifetime,
)


def _rel(x, y):
    return abs(x - y) / (1.0 + abs(y))


# --- Unruh temperature -------------------------------------------------------

def test_unruh_temperature_linear_in_acceleration():
    a = 1.0e20
    # closed form and the canonical ~0.405 K at a = 1e20 m/s^2
    assert _rel(unruh_temperature(a), HBAR * a / (2 * np.pi * C * K_B)) < 1e-12
    assert abs(unruh_temperature(a) - 0.4055) < 1e-3
    # strictly linear: T_U(c*a) = c*T_U(a)
    assert _rel(unruh_temperature(3 * a), 3 * unruh_temperature(a)) < 1e-12
    assert _rel(unruh_temperature(0.5 * a), 0.5 * unruh_temperature(a)) < 1e-12
    # everyday acceleration -> absurdly tiny temperature
    assert unruh_temperature(9.81) < 1e-19


# --- Hawking temperature -----------------------------------------------------

def test_hawking_temperature_inverse_mass():
    # solar-mass black hole is ~6.17e-8 K (colder than the CMB)
    T = hawking_temperature(M_SUN)
    assert _rel(T, HBAR * C ** 3 / (8 * np.pi * G * M_SUN * K_B)) < 1e-12
    assert 5e-8 < T < 7e-8
    # T_H ~ 1/M : doubling the mass halves the temperature
    assert _rel(hawking_temperature(2 * M_SUN), 0.5 * T) < 1e-12


def test_hawking_via_surface_gravity_and_radius():
    # r_s = 2GM/c^2 ~ 2.95 km for the Sun; kappa = c^2/(2 r_s)
    assert _rel(schwarzschild_radius(M_SUN), 2 * G * M_SUN / C ** 2) < 1e-12
    assert abs(schwarzschild_radius(M_SUN) - 2953.0) < 5.0          # metres
    assert _rel(surface_gravity(M_SUN), C ** 2 / (2 * schwarzschild_radius(M_SUN))) < 1e-12
    # T_H = hbar kappa / (2 pi c k_B) must equal the direct formula
    T_kappa = HBAR * surface_gravity(M_SUN) / (2 * np.pi * C * K_B)
    assert _rel(T_kappa, hawking_temperature(M_SUN)) < 1e-12


def test_one_kilogram_black_hole_is_blazing_hot():
    # T_H ~ 1/M makes a light hole enormously hot (~1.2e23 K)
    T = hawking_temperature(1.0)
    assert T > 1e22
    assert _rel(T, 1.227e23) < 1e-2


# --- Planck / thermal occupation ---------------------------------------------

def test_bose_occupation_limits():
    T = 1.0
    # high-T / low-frequency (x << 1): Rayleigh-Jeans  <n> ~ k_B T / hbar omega
    w_lo = 1e7
    x = HBAR * w_lo / (K_B * T)
    assert _rel(bose_occupation(w_lo, T), 1.0 / x) < 1e-3
    # low-T / high-frequency (x >> 1): exponentially suppressed, <n> ~ exp(-x)
    w_hi = K_B * T * 30 / HBAR            # x = 30
    assert bose_occupation(w_hi, T) < 1e-12
    # monotonically falling with frequency
    assert bose_occupation(2 * w_lo, T) < bose_occupation(w_lo, T)


def test_fermi_occupation_bounded():
    T, w = 1.0, 1e10
    nF = fermi_occupation(w, T)
    assert 0.0 < nF <= 0.5
    # at the "chemical-potential" energy hbar w -> 0 the occupation is 1/2
    assert _rel(fermi_occupation(1e-30, T), 0.5) < 1e-6
    # fermions are always less occupied than bosons at the same (omega, T)
    assert fermi_occupation(w, T) < bose_occupation(w, T)


# --- Bogoliubov normalization & particle creation ----------------------------

def test_bogoliubov_normalization_single_and_multimode():
    # single-mode squeeze: cosh^2 r - sinh^2 r = 1 for any r
    for r in (0.0, 0.4, 1.3, 2.7):
        a, b = squeeze_to_bogoliubov(r)
        assert _rel(bogoliubov_check(a, b), 1.0) < 1e-12
        assert _rel(particle_number(b), np.sinh(r) ** 2) < 1e-12
    # a hand-built multimode output mode: sum|alpha|^2 - sum|beta|^2 = 1
    beta = np.array([0.3, 0.5j, 0.2 - 0.1j])
    s = np.sum(np.abs(beta) ** 2)
    alpha = np.full(3, np.sqrt((1.0 + s) / 3.0), dtype=complex)
    assert _rel(bogoliubov_check(alpha, beta), 1.0) < 1e-12
    # zero mixing (beta = 0) -> no particles, vacuum is shared
    assert particle_number(np.zeros(5)) == 0.0


def test_particle_number_grows_with_squeezing():
    n0 = particle_number(squeeze_to_bogoliubov(0.5)[1])
    n1 = particle_number(squeeze_to_bogoliubov(1.5)[1])
    assert n1 > n0 > 0.0


# --- the spectrum is Planckian (the central result) --------------------------

def test_thermal_beta_squared_is_planck():
    T = 1.0
    # frequencies chosen so x = hbar w / k_B T spans ~0.5 .. 8 (resolved tail)
    w = np.array([0.5, 1.0, 2.0, 5.0, 8.0]) * K_B * T / HBAR
    # the |beta_w|^2 spectrum builder IS the Bose/Planck factor
    assert np.allclose(thermal_beta_squared(w, T, "bose"), bose_occupation(w, T))
    assert np.allclose(thermal_beta_squared(w, T, "fermi"), fermi_occupation(w, T))
    # bosonic spectrum strictly exceeds the fermionic one
    assert np.all(thermal_beta_squared(w, T, "bose") > thermal_beta_squared(w, T, "fermi"))


def test_unruh_spectrum_is_thermal_at_T_U():
    # THE key statement: the Bogoliubov occupation of a Rindler mode equals the
    # Bose factor at the Unruh temperature -> the accelerated vacuum is thermal.
    a = 1.0e20
    T_U = unruh_temperature(a)
    for w in (1e9, 1e10, 5e10, 2e11):
        nB = unruh_occupation(w, a)
        assert _rel(nB, bose_occupation(w, T_U)) < 1e-9
        # detailed balance:  |beta|^2/|alpha|^2 = exp(-2 pi c w/a) = N/(N+1)
        assert _rel(unruh_beta_ratio(w, a), nB / (nB + 1.0)) < 1e-9


def test_squeezing_reproduces_unruh_occupation():
    # a horizon as a two-mode squeezer: tanh r = exp(-pi c w / a) gives the thermal <N>
    a = 1.0e20
    for w in (1e10, 5e10, 1e11):
        ratio = unruh_beta_ratio(w, a)            # = tanh^2 r
        r = np.arctanh(np.sqrt(ratio))
        alpha, beta = squeeze_to_bogoliubov(r)
        assert _rel(bogoliubov_check(alpha, beta), 1.0) < 1e-9
        assert _rel(particle_number(beta), unruh_occupation(w, a)) < 1e-9


# --- evaporation -------------------------------------------------------------

def test_evaporation_lifetime_scales_as_mass_cubed():
    tau = evaporation_lifetime(M_SUN)
    # closed form and the canonical ~6.6e74 s (~2.1e67 yr) for a solar mass
    assert _rel(tau, 5120 * np.pi * G ** 2 * M_SUN ** 3 / (HBAR * C ** 4)) < 1e-12
    assert _rel(tau, 6.62e74) < 5e-3
    assert _rel(tau / 3.15576e7, 2.1e67) < 1e-2          # years
    # tau ~ M^3
    assert _rel(evaporation_lifetime(2 * M_SUN), 8.0 * tau) < 1e-12
    assert _rel(evaporation_lifetime(10 * M_SUN), 1000.0 * tau) < 1e-12


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
