"""Tests for PK-01 kinetic description (distribution functions, Vlasov & Boltzmann).

Run:  python3 test_kinetic_description.py     ->  "All N tests passed."
"""
import numpy as np

from kinetic_description import (
    K_B, EPS0, M_E, E_CHARGE,
    maxwellian, thermal_speed, plasma_frequency, debye_length,
    plasma_parameter, free_stream, vlasov_residual,
)

N = 1.0e18                      # number density [/m^3]
T = 1.0 * E_CHARGE / K_B        # 1 eV in kelvin (11604.5 K)


def _phase_space_grid(Nx=128, Nv=96, L=2.0 * np.pi, vmax=6.0):
    x = np.linspace(0.0, L, Nx, endpoint=False)
    v = np.linspace(-vmax, vmax, Nv)
    M = np.exp(-v ** 2 / 2.0)                    # Maxwellian in v (v_T = 1)
    g = 1.0 + 0.3 * np.cos(x)                    # density perturbation in x
    f0 = M[:, None] * g[None, :]                 # (Nv, Nx)
    return x, v, f0


# --- the Maxwellian distribution and its velocity moments --------------------

def test_maxwellian_matches_closed_form_and_peaks_at_zero():
    # value matches n (m/2 pi kT)^{3/2} exp(-m v^2/2kT); monotone decreasing in |v|
    vth = thermal_speed(T, M_E)
    a = M_E / (2.0 * np.pi * K_B * T)
    assert np.isclose(maxwellian(0.0, N, T, M_E), N * a ** 1.5)
    f0 = maxwellian(0.0, N, T, M_E)
    assert f0 > maxwellian(vth, N, T, M_E) > maxwellian(3.0 * vth, N, T, M_E)
    # value at v = v_T is down by exp(-1/2)
    assert np.isclose(maxwellian(vth, N, T, M_E) / f0, np.exp(-0.5))


def test_maxwellian_zeroth_moment_is_number_density():
    # INT f d^3v = INT_0^inf f(v) 4 pi v^2 dv = n
    vth = thermal_speed(T, M_E)
    v = np.linspace(0.0, 10.0 * vth, 200000)
    f = maxwellian(v, N, T, M_E)
    n_int = np.trapezoid(f * 4.0 * np.pi * v ** 2, v)
    assert abs(n_int / N - 1.0) < 1e-3


def test_maxwellian_pressure_and_energy_moments():
    # second moments: p = (m/3) INT v^2 f d^3v = n kT;  INT (1/2 m v^2) f = (3/2) n kT
    vth = thermal_speed(T, M_E)
    v = np.linspace(0.0, 12.0 * vth, 300000)
    f = maxwellian(v, N, T, M_E)
    jac = 4.0 * np.pi * v ** 2
    p = (M_E / 3.0) * np.trapezoid(v ** 2 * f * jac, v)
    energy = np.trapezoid(0.5 * M_E * v ** 2 * f * jac, v)
    assert abs(p / (N * K_B * T) - 1.0) < 1e-3            # ideal-gas pressure
    assert abs(energy / (1.5 * N * K_B * T) - 1.0) < 1e-3  # equipartition (~SM-06)


def test_thermal_speed_formula():
    assert np.isclose(thermal_speed(T, M_E), np.sqrt(K_B * T / M_E))
    # 3-D rms speed is sqrt(3) v_T
    assert np.isclose(np.sqrt(3.0) * thermal_speed(T, M_E),
                      np.sqrt(3.0 * K_B * T / M_E))


# --- collective scales -------------------------------------------------------

def test_plasma_frequency_formula_and_scaling():
    assert np.isclose(plasma_frequency(N), np.sqrt(N * E_CHARGE ** 2 / (EPS0 * M_E)))
    # omega_p ~ sqrt(n)
    assert np.isclose(plasma_frequency(4.0 * N) / plasma_frequency(N), 2.0)
    # representative plasma: ~5.6e10 rad/s (f_p ~ 9 GHz)
    assert 5.0e10 < plasma_frequency(N) < 6.0e10


def test_debye_length_formula_and_scaling():
    assert np.isclose(debye_length(N, T), np.sqrt(EPS0 * K_B * T / (N * E_CHARGE ** 2)))
    # lambda_D ~ sqrt(T/n)
    assert np.isclose(debye_length(N, 4.0 * T) / debye_length(N, T), 2.0)
    assert np.isclose(debye_length(4.0 * N, T) / debye_length(N, T), 0.5)
    # representative plasma: ~7.4 micron
    assert 7.0e-6 < debye_length(N, T) < 8.0e-6


def test_debye_equals_thermal_speed_over_plasma_frequency():
    # the identity lambda_D = v_T / omega_p  (Mi Eq. A.6), electrons
    assert np.isclose(debye_length(N, T), thermal_speed(T, M_E) / plasma_frequency(N))


def test_plasma_parameter_weakly_coupled():
    Lam = plasma_parameter(N, T)
    assert np.isclose(Lam, N * debye_length(N, T) ** 3)
    assert Lam > 1.0                                     # weakly coupled
    assert 300.0 < Lam < 600.0                           # ~411 for this plasma
    # Lambda ~ T^{3/2} / sqrt(n):  hotter/thinner plasma is more ideal
    assert plasma_parameter(N, 4.0 * T) > Lam


# --- phase-space continuity (Vlasov / Liouville, KEY BRIDGE B2) --------------

def test_vlasov_residual_small_under_free_streaming():
    # df/dt + v df/dx = 0 to discretization error: residual << the streaming term
    x, v, f0 = _phase_space_grid()
    dt = 1.0e-3
    f1 = free_stream(f0, x, v, dt)
    res = vlasov_residual(f0, f1, x, v, dt)
    dx = x[1] - x[0]
    stream = v[:, None] * (np.roll(f0, -1, 1) - np.roll(f0, 1, 1)) / (2.0 * dx)
    assert np.max(np.abs(res)) < 1e-2 * np.max(np.abs(stream))


def test_free_streaming_shears_phase_space_conserving_marginals():
    # streaming only TRANSPORTS f (Liouville): total number and the velocity
    # marginal INT f dx are invariant, yet phase space genuinely shears (f changes).
    x, v, f0 = _phase_space_grid()
    f1 = free_stream(f0, x, v, 5.0e-3)
    assert np.isclose(f0.sum(), f1.sum(), rtol=1e-10)             # total number
    assert np.allclose(f0.sum(axis=1), f1.sum(axis=1), atol=1e-9)  # INT f dx per v frozen
    assert not np.allclose(f0, f1, atol=1e-4)                     # but f(x,v) is sheared


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
