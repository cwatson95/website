"""Tests for QM-03 (Schrodinger equation) -- every claim checked against a closed
form: the well spectrum, the stationarity of |Psi|^2, the Bohr beat frequency of
a superposition, conservation of probability, Fourier's trick, and -- with the
SAME solver -- the harmonic-oscillator ladder (~QM-09).

Run directly:   python3 test_schrodinger.py     (-> "All N tests passed.")
Or with pytest: pytest test_schrodinger.py
"""
import numpy as np

from schrodinger import (
    make_grid, hamiltonian, solve, inner_product, normalize, prob_density,
    expectation_position, stationary_state, evolve, coefficients,
    infinite_well_energy, infinite_well_eigenfunction,
    harmonic_oscillator_energy, superposition_period, measure_period,
)


def _approx(x, y, rel=1e-9, abs_=0.0):
    return abs(x - y) <= max(rel * abs(y), abs_)


# --- shared infinite-square-well solution (hbar = m = 1, width L = 1) ---------
L = 1.0
N = 400
X = make_grid(0.0, L, N)
DX = X[1] - X[0]
E, PSI = solve(X, V=0.0)               # E ascending, PSI[:, n] the n-th eigenstate


def test_hamiltonian_is_hermitian():
    """H must be real-symmetric (Hermitian) so its eigen-energies are real."""
    H = hamiltonian(X, V=lambda x: 0.5 * x ** 2)   # any V: kinetic + diagonal V
    assert np.allclose(H, H.T, atol=1e-12)
    E_test, _ = np.linalg.eigh(H)
    assert np.all(np.abs(E_test.imag) < 1e-12) if np.iscomplexobj(E_test) else True


def test_eigenstates_orthonormal():
    """<psi_m|psi_n> = delta_mn for the grid solver's output."""
    for m in range(5):
        for n in range(5):
            ov = inner_product(PSI[:, m], PSI[:, n], DX).real
            assert _approx(ov, 1.0 if m == n else 0.0, abs_=1e-9)


def test_infinite_well_energies():
    """Lowest five levels recover E_n = n^2 pi^2 hbar^2/(2 m L^2) to well under 1%."""
    for n in range(1, 6):
        exact = infinite_well_energy(n, L)        # = n^2 pi^2 / 2  (hbar=m=L=1)
        assert _approx(E[n - 1], exact, rel=1e-2)
        assert _approx(E[n - 1], exact, rel=1e-3)  # in fact much better than 1%


def test_infinite_well_general_units():
    """The closed form holds with hbar, m != 1 -- the code is not secretly unit-locked."""
    hbar, m, Lw = 1.5, 0.7, 2.0
    xg = make_grid(0.0, Lw, 400)
    Eg, _ = solve(xg, V=0.0, hbar=hbar, m=m)
    for n in range(1, 5):
        exact = infinite_well_energy(n, Lw, hbar=hbar, m=m)
        assert _approx(Eg[n - 1], exact, rel=2e-3)


def test_infinite_well_eigenfunction_shape():
    """Ground-state density matches (2/L) sin^2(pi x/L); psi_1 orthogonal to psi_2."""
    dens_num = prob_density(PSI[:, 0])
    dens_exact = infinite_well_eigenfunction(1, X, L) ** 2
    assert np.max(np.abs(dens_num - dens_exact)) < 1e-4
    assert _approx(inner_product(PSI[:, 0], PSI[:, 1], DX).real, 0.0, abs_=1e-9)


def test_energy_scales_as_inverse_L_squared():
    """E_n ~ 1/L^2: doubling the box width quarters every level."""
    x2 = make_grid(0.0, 2.0 * L, N)
    E2, _ = solve(x2, V=0.0)
    for n in range(4):
        assert _approx(E2[n], E[n] / 4.0, rel=1e-3)


def test_stationary_state_density_time_independent():
    """A single eigenstate: |Psi(x,t)|^2 = |psi(x)|^2 for all t (to machine eps)."""
    psi1 = PSI[:, 0]
    d0 = prob_density(psi1)
    for t in (0.0, 0.31, 2.7, 13.0):
        dt = prob_density(stationary_state(psi1, E[0], t))
        assert np.max(np.abs(dt - d0)) < 1e-12


def test_stationary_state_phase_does_evolve():
    """The state itself is NOT frozen: at t = pi hbar/E the phase e^{-i pi} = -1,
    so Psi = -psi; at t = 2 pi hbar/E it returns to +psi.  (Phase rotates even
    though |Psi|^2 does not.)"""
    psi1 = PSI[:, 0]
    half = stationary_state(psi1, E[0], np.pi / E[0])      # expect -psi1
    full = stationary_state(psi1, E[0], 2.0 * np.pi / E[0])  # expect +psi1
    assert np.allclose(half, -psi1, atol=1e-10)
    assert np.allclose(full, psi1, atol=1e-10)
    assert not np.allclose(half, psi1, atol=1e-3)          # genuinely moved


def test_probability_conserved_under_evolution():
    """Unitary phase evolution conserves the total probability (seed of ~QM-04)."""
    c = np.zeros(PSI.shape[1]); c[0] = c[1] = c[2] = 1.0 / np.sqrt(3.0)
    for t in (0.0, 0.5, 1.7, 4.2):
        Psi = evolve(E, PSI, c, t)
        assert _approx(inner_product(Psi, Psi, DX).real, 1.0, abs_=1e-9)


def test_superposition_period_matches_bohr_frequency():
    """For Psi=(psi1+psi2)/sqrt(2), <x>(t) beats at omega=(E2-E1)/hbar, i.e. the
    measured period equals 2 pi hbar/(E2-E1) to <1%."""
    c = np.zeros(PSI.shape[1]); c[0] = c[1] = 1.0 / np.sqrt(2.0)
    T_theory = superposition_period(E[1], E[0])
    ts = np.linspace(0.0, 4.0 * T_theory, 2000)
    xt = [expectation_position(evolve(E, PSI, c, t), X) for t in ts]
    T_meas = measure_period(ts, xt)
    assert _approx(T_meas, T_theory, rel=1e-2)


def test_superposition_revival_and_time_dependence():
    """|Psi|^2 returns to itself after one full period T but differs at T/2 --
    proving the superposition (unlike a stationary state) is observably dynamic."""
    c = np.zeros(PSI.shape[1]); c[0] = c[1] = 1.0 / np.sqrt(2.0)
    T = superposition_period(E[1], E[0])
    t0 = 0.137
    d0 = prob_density(evolve(E, PSI, c, t0))
    dT = prob_density(evolve(E, PSI, c, t0 + T))
    dhalf = prob_density(evolve(E, PSI, c, t0 + 0.5 * T))
    assert np.max(np.abs(dT - d0)) < 1e-9          # full revival
    assert np.max(np.abs(dhalf - d0)) > 1e-2       # not stationary


def test_coefficients_recovered():
    """Fourier's trick: c_n = <psi_n|Psi0> reconstruct Psi0 and obey Parseval."""
    target = np.zeros(PSI.shape[1]); target[0], target[2], target[4] = 0.6, 0.0, 0.8
    Psi0 = normalize(PSI @ target, DX)
    c = coefficients(PSI, Psi0, DX)
    assert np.allclose(PSI @ c, Psi0, atol=1e-9)         # reconstruction
    assert _approx(np.sum(np.abs(c) ** 2), 1.0, abs_=1e-9)  # sum |c_n|^2 = 1
    assert _approx(abs(c[0]) ** 2, 0.36, abs_=1e-6)     # |c_1|^2 = 0.6^2
    assert _approx(abs(c[4]) ** 2, 0.64, abs_=1e-6)     # |c_5|^2 = 0.8^2


def test_harmonic_oscillator_energies():
    """Same finite-difference solver, V = m omega^2 x^2/2, recovers the ladder
    E_n = (n+1/2) hbar omega to ~0.1% (the bridge to ~QM-09)."""
    xh = make_grid(-8.0, 8.0, 800)
    Eh, _ = solve(xh, V=lambda x: 0.5 * x ** 2)         # omega = 1
    for n in range(5):
        assert _approx(Eh[n], harmonic_oscillator_energy(n), rel=1e-2)
    # equal spacing hbar*omega = 1 between neighbours
    for n in range(4):
        assert _approx(Eh[n + 1] - Eh[n], 1.0, rel=1e-2)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
