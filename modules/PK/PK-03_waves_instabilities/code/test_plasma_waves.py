"""Tests for PK-03 plasma waves & instabilities.

Run:  python3 test_plasma_waves.py     ->  "All N tests passed."
"""
import numpy as np

from plasma_waves import (
    EPS0, ELEM_CHARGE, ELECTRON_MASS, PROTON_MASS, K_B,
    plasma_frequency, debye_length, thermal_speed,
    bohm_gross, ion_acoustic, landau_damping_rate, two_stream_growth_rate,
)

# fiducial plasma
N = 1.0e18          # density      [1/m^3]
T = 1.0e4           # temperature  [K]
E = ELEM_CHARGE
ME = ELECTRON_MASS
MI = PROTON_MASS


def test_scales_and_relations():
    wp = plasma_frequency(N, E, ME)
    lD = debye_length(N, T, E)
    vth = thermal_speed(T, ME)
    # closed forms
    assert np.isclose(wp, np.sqrt(N * E ** 2 / (EPS0 * ME)))
    assert np.isclose(lD, np.sqrt(EPS0 * K_B * T / (N * E ** 2)))
    assert np.isclose(vth, np.sqrt(K_B * T / ME))
    # the key identity lam_D = v_th / w_p
    assert np.isclose(lD, vth / wp)
    # scalings: w_p ~ sqrt(n), lam_D ~ sqrt(T)
    assert np.isclose(plasma_frequency(4 * N, E, ME), 2 * wp)
    assert np.isclose(debye_length(N, 4 * T, E), 2 * lD)


def test_bohm_gross_cold_limit_and_form():
    wp = plasma_frequency(N, E, ME)
    vth = thermal_speed(T, ME)
    lD = debye_length(N, T, E)
    # cold limit: as k -> 0, w -> w_p
    assert np.isclose(bohm_gross(1e-6 / lD, N, T, ME), wp, rtol=1e-6)
    # exact pressure form  w^2 = w_p^2 + 3 k^2 v_th^2
    k = 0.3 / lD
    assert np.isclose(bohm_gross(k, N, T, ME) ** 2, wp ** 2 + 3 * (k * vth) ** 2)
    # equivalent lambda form  w^2 = w_p^2 (1 + 3 (k lam_D)^2)
    assert np.isclose(bohm_gross(k, N, T, ME) ** 2, wp ** 2 * (1 + 3 * (k * lD) ** 2))
    # monotonic increasing, always above the cutoff
    ks = np.array([0.0, 0.1, 0.2, 0.4]) / lD
    w = bohm_gross(ks, N, T, ME)
    assert np.all(np.diff(w) > 0)
    assert np.all(w >= wp - 1e-3)


def test_ion_acoustic_sound_limit_and_saturation():
    lD = debye_length(N, T, E)
    cs = np.sqrt(K_B * T / MI)
    # long-wavelength sound limit: w/k -> c_s as k lam_D -> 0
    k_small = 1e-4 / lD
    assert np.isclose(ion_acoustic(k_small, T, N, MI) / k_small, cs, rtol=1e-6)
    # exact closed form
    k = 0.5 / lD
    assert np.isclose(ion_acoustic(k, T, N, MI), k * cs / np.sqrt(1 + (k * lD) ** 2))
    # dispersion bends DOWN: phase speed w/k decreases with k
    ks = np.array([0.2, 0.6, 1.0, 2.0]) / lD
    vph = ion_acoustic(ks, T, N, MI) / ks
    assert np.all(np.diff(vph) < 0)
    assert np.all(vph < cs)
    # short-wavelength saturation: w -> ion plasma frequency w_pi = c_s/lam_D
    w_pi = plasma_frequency(N, E, MI)
    assert np.isclose(ion_acoustic(1e4 / lD, T, N, MI), w_pi, rtol=1e-3)
    assert np.isclose(cs / lD, w_pi, rtol=1e-9)


def test_ion_acoustic_is_slow_compared_to_electrons():
    # the sound speed is tiny vs the electron thermal speed: c_s/v_th,e = sqrt(me/mi)
    cs = np.sqrt(K_B * T / MI)
    vth_e = thermal_speed(T, ME)
    assert np.isclose(cs / vth_e, np.sqrt(ME / MI))
    assert cs / vth_e < 0.05


def test_landau_damping_sign_and_monotonicity():
    lD = debye_length(N, T, E)
    wp = plasma_frequency(N, E, ME)
    # damping: gamma < 0
    for kld in (0.2, 0.3, 0.4, 0.5):
        assert landau_damping_rate(kld / lD, N, T, ME) < 0
    # closed form check
    kld = 0.35
    k = kld / lD
    expect = -wp * np.sqrt(np.pi / 8.0) * kld ** (-3) * np.exp(-1.0 / (2 * kld ** 2) - 1.5)
    assert np.isclose(landau_damping_rate(k, N, T, ME), expect)
    # |gamma| grows with k lam_D (resonance moves from the tail into the bulk)
    mags = [abs(landau_damping_rate(kld / lD, N, T, ME)) for kld in (0.2, 0.3, 0.4, 0.5)]
    assert all(b > a for a, b in zip(mags, mags[1:]))
    # exponentially weak at small k lam_D
    assert abs(landau_damping_rate(0.15 / lD, N, T, ME)) / wp < 1e-4


def test_two_stream_unstable_band():
    wp = plasma_frequency(N, E, ME)
    v0 = 5.0 * thermal_speed(T, ME)
    # inside the band (k v0 < w_p): growing mode, Im w > 0
    k_in = 0.5 * wp / v0
    assert two_stream_growth_rate(k_in, N, ME, v0) > 0
    # outside the band (k v0 > w_p): stable, growth clipped to 0
    k_out = 1.5 * wp / v0
    assert two_stream_growth_rate(k_out, N, ME, v0) == 0.0
    # band edge: marginal
    assert two_stream_growth_rate(1.001 * wp / v0, N, ME, v0) == 0.0


def test_two_stream_peak_growth_value_and_location():
    wp = plasma_frequency(N, E, ME)
    v0 = 5.0 * thermal_speed(T, ME)
    kgrid = np.linspace(1e-3, 1.2, 4000) * wp / v0
    g = np.array([two_stream_growth_rate(k, N, ME, v0) for k in kgrid])
    jmax = int(np.argmax(g))
    # peak growth  gamma_max = w_p / sqrt(8)
    assert np.isclose(g[jmax] / wp, 1.0 / np.sqrt(8.0), rtol=1e-2)
    # at  k v0 = sqrt(3/8) w_p
    assert np.isclose(kgrid[jmax] * v0 / wp, np.sqrt(3.0 / 8.0), rtol=1e-2)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
