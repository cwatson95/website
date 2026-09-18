"""Tests for QM-04 probability current & continuity.

Run:  python3 test_probability_current.py     ->  "All N tests passed."
"""
import numpy as np

from probability_current import (
    prob_density, prob_current, total_probability, mean_velocity,
    plane_wave, gaussian_packet, free_step, continuity_residual,
)


def _grid(L=80.0, n=2048):
    x = np.linspace(-L / 2, L / 2, n, endpoint=False)
    return x, x[1] - x[0]


def test_plane_wave_current_is_rho_times_velocity():
    # j = rho * v with v = hbar k / m = k (natural units); FD gives ~1% accuracy
    x, dx = _grid()
    k = 1.5
    psi = plane_wave(x, k, amp=2.0)
    j = prob_current(psi, dx)
    rho = prob_density(psi)
    assert np.allclose(rho, 4.0)                       # |A|^2
    assert abs(j.mean() / rho.mean() - k) < 1e-2 * k   # j/rho = v = k


def test_current_reverses_with_momentum():
    x, dx = _grid()
    jp = prob_current(plane_wave(x, +1.5), dx).mean()
    jm = prob_current(plane_wave(x, -1.5), dx).mean()
    assert jp > 0 and jm < 0
    assert abs(jp + jm) < 1e-6                          # j(-k) = -j(k)


def test_real_stationary_state_has_zero_current():
    # a real wavefunction (standing wave / bound eigenstate) carries no current
    x, dx = _grid()
    psi = np.cos(1.5 * x).astype(complex)
    assert np.max(np.abs(prob_current(psi, dx))) < 1e-12


def test_two_current_formulas_agree():
    # (hbar/m) Im(psi* grad psi)  ==  (i hbar/2m)(psi grad psi* - psi* grad psi)
    x, dx = _grid()
    psi = gaussian_packet(x, x0=-5.0, k0=1.3, sigma=2.0)
    grad = np.gradient(psi, dx)
    j_a = np.imag(np.conj(psi) * grad)
    j_b = (0.5j) * (psi * np.conj(grad) - np.conj(psi) * grad)
    assert np.allclose(j_a, np.real(j_b), atol=1e-12)
    assert np.max(np.abs(np.imag(j_b))) < 1e-12         # the current is real


def test_continuity_holds_for_free_evolution():
    # d rho/dt + d j/dx = 0 to discretization error: residual << the term itself
    x, dx = _grid()
    psi0 = gaussian_packet(x, x0=-10.0, k0=2.0, sigma=2.0)
    dt = 2e-3
    psi1 = free_step(psi0, dx, dt)
    res = continuity_residual(psi0, psi1, dx, dt)
    drho_dt = (prob_density(psi1) - prob_density(psi0)) / dt
    assert np.max(np.abs(res)) < 1e-2 * np.max(np.abs(drho_dt))


def test_normalization_conserved_under_free_evolution():
    # global conservation: d/dt integral|psi|^2 = 0  (ties to ~QM-02)
    x, dx = _grid()
    psi = gaussian_packet(x, x0=-10.0, k0=2.0, sigma=2.0)
    p0 = total_probability(psi, dx)
    for _ in range(50):
        psi = free_step(psi, dx, 2e-3)
    assert abs(total_probability(psi, dx) - p0) < 1e-9
    assert abs(p0 - 1.0) < 1e-6                          # packet was normalized


def test_mean_velocity_is_group_velocity():
    x, dx = _grid()
    k0 = 2.0
    psi = gaussian_packet(x, x0=-10.0, k0=k0, sigma=2.0)
    assert abs(mean_velocity(psi, dx) - k0) < 1e-2 * k0


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
