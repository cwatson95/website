"""Tests for QO-02 atom-field interaction (Rabi & Jaynes-Cummings).

Self-contained: numpy/scipy only, no sibling imports.
Run:  python3 test_atom_field.py     ->  "All N tests passed."
"""
import numpy as np
from scipy.linalg import expm

from atom_field import (
    I2, sigma_z, sigma_plus, sigma_minus, ket_e, ket_g,
    generalized_rabi, rabi_excited_population, two_level_hamiltonian,
    annihilation, number_operator, coherent_state,
    jcm_hamiltonian, dressed_energies, vacuum_rabi_splitting,
    jcm_inversion, resonant_inversion_series, collapse_time, revival_time,
)


# --- 1. the two-level atom (~QM-11) ------------------------------------------

def test_atom_pauli_algebra():
    # sigma^+ = |e><g| raises g -> e, sigma^- lowers e -> g
    assert np.allclose(sigma_plus @ ket_g, ket_e)
    assert np.allclose(sigma_minus @ ket_e, ket_g)
    assert np.allclose(sigma_plus @ ket_e, 0.0)
    assert np.allclose(sigma_minus @ ket_g, 0.0)
    # sigma^+ sigma^- = |e><e|, sigma^- sigma^+ = |g><g|
    assert np.allclose(sigma_plus @ sigma_minus, np.diag([1.0, 0.0]))
    assert np.allclose(sigma_minus @ sigma_plus, np.diag([0.0, 1.0]))
    # commutator / anticommutator close the algebra
    assert np.allclose(sigma_plus @ sigma_minus - sigma_minus @ sigma_plus, sigma_z)
    assert np.allclose(sigma_plus @ sigma_minus + sigma_minus @ sigma_plus, I2)
    # sigma^± = (sigma_x ± i sigma_y)/2 -- the Pauli ladder of ~QM-11
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    assert np.allclose(sigma_plus, 0.5 * (sx + 1j * sy))
    assert np.allclose(sigma_minus, 0.5 * (sx - 1j * sy))


# --- 2. semiclassical Rabi oscillations --------------------------------------

def test_generalized_rabi_formula():
    assert np.isclose(generalized_rabi(3.0, 4.0), 5.0)       # 3-4-5
    assert np.isclose(generalized_rabi(2.0, 0.0), 2.0)       # on resonance -> Om
    assert np.isclose(generalized_rabi(0.0, 1.7), 1.7)


def test_rabi_resonant_inversion_and_return():
    Om = 1.3
    # on resonance P_e = sin^2(Om t/2): 0 at start, 1 at Om t = pi, 0 at Om t = 2 pi
    assert np.isclose(rabi_excited_population(0.0, Om, 0.0), 0.0)
    assert np.isclose(rabi_excited_population(np.pi / Om, Om, 0.0), 1.0)     # pi-pulse
    assert np.isclose(rabi_excited_population(2 * np.pi / Om, Om, 0.0), 0.0)  # return
    assert np.isclose(rabi_excited_population(np.pi / (2 * Om), Om, 0.0), 0.5)
    # closed form equals sin^2(Om t/2) elementwise
    t = np.linspace(0, 4 * np.pi / Om, 50)
    assert np.allclose(rabi_excited_population(t, Om, 0.0), np.sin(Om * t / 2) ** 2)


def test_rabi_detuned_saturation():
    Om, d = 1.0, 1.5
    OmR = generalized_rabi(Om, d)
    # off resonance the flop saturates at Om^2/(Om^2+d^2) < 1
    amp = Om ** 2 / (Om ** 2 + d ** 2)
    assert amp < 1.0
    # the peak (at Om_R t = pi) equals that saturated amplitude
    assert np.isclose(rabi_excited_population(np.pi / OmR, Om, d), amp)
    # P_e never exceeds it, and oscillates faster than the resonant case
    t = np.linspace(0, 20, 2000)
    assert np.max(rabi_excited_population(t, Om, d)) <= amp + 1e-9
    assert np.isclose(rabi_excited_population(np.pi / OmR, 1.0, 1.5), 1.0 / 3.25)


def test_rabi_matches_two_level_evolution():
    # genuine time evolution of |g> under the RWA 2x2 H reproduces the formula
    for Om, d in [(1.0, 0.0), (1.0, 0.7), (0.8, -1.3), (1.5, 2.0)]:
        H = two_level_hamiltonian(Om, d)
        for t in np.linspace(0.3, 6.0, 12):
            psi = expm(-1j * H * t) @ ket_g
            p_e = abs(np.vdot(ket_e, psi)) ** 2
            assert np.isclose(p_e, rabi_excited_population(t, Om, d), atol=1e-9)


# --- 3. field operators and coherent states ----------------------------------

def test_field_operators_and_commutator():
    N = 8
    a = annihilation(N)
    adag = a.conj().T
    # a|n> = sqrt(n)|n-1>
    e3 = np.zeros(N, dtype=complex); e3[3] = 1.0
    assert np.allclose(a @ e3, np.sqrt(3.0) * np.eye(N)[2])
    assert np.allclose(a @ np.eye(N)[0], 0.0)               # a|0> = 0
    # a^dag a is the number operator diag(0..N-1)
    assert np.allclose(adag @ a, number_operator(N))
    # [a, a^dag] = I on the (resolved) top-left block (1 except the truncated corner)
    comm = a @ adag - adag @ a
    assert np.allclose(np.diag(comm)[:-1], 1.0)
    assert np.isclose(np.diag(comm)[-1], -(N - 1))          # truncation defect


def test_coherent_state_poissonian():
    alpha, N = 2.0, 40
    c = coherent_state(alpha, N)
    nbar = abs(alpha) ** 2
    assert np.isclose(np.linalg.norm(c), 1.0)
    # eigenstate of a: a|alpha> = alpha|alpha> (up to truncation, negligible here)
    assert np.allclose(annihilation(N) @ c, alpha * c, atol=1e-8)
    # mean photon number = nbar
    n = np.arange(N)
    assert np.isclose((n * np.abs(c) ** 2).sum(), nbar, atol=1e-6)
    # Poissonian statistics P_n = e^{-nbar} nbar^n / n!
    from math import exp, factorial
    Pn = np.abs(c) ** 2
    for k in (0, 1, 2, 4, 8):
        assert np.isclose(Pn[k], exp(-nbar) * nbar ** k / factorial(k), atol=1e-8)


# --- Jaynes-Cummings model ---------------------------------------------------

def test_jcm_hamiltonian_hermitian_and_excitation_conserved():
    wc, wa, g, N = 5.0, 5.3, 0.9, 10
    H = jcm_hamiltonian(wc, wa, g, N)
    assert H.shape == (2 * N, 2 * N)
    assert np.allclose(H, H.conj().T)                       # Hermitian
    # excitation number Nexc = a^dag a + |e><e| is conserved: [H, Nexc] = 0
    a = annihilation(N)
    Nexc = np.kron(I2, a.conj().T @ a) + np.kron(sigma_plus @ sigma_minus, np.eye(N))
    assert np.allclose(H @ Nexc - Nexc @ H, 0.0, atol=1e-10)


def test_dressed_energies_match_block_and_vacuum_rabi():
    wc, wa, g, N = 4.0, 5.1, 0.8, 12
    d = wa - wc
    H = jcm_hamiltonian(wc, wa, g, N)
    for n in range(N - 1):                                  # |g,n+1> stays in range
        idx = [n, N + n + 1]                                # |e,n>, |g,n+1>
        block = H[np.ix_(idx, idx)]
        ev = np.sort(np.linalg.eigvalsh(block))
        assert np.allclose(ev, np.sort(dressed_energies(n, d, g, wc)), atol=1e-10)
    # resonant gap is 2 g sqrt(n+1); n=0 is the vacuum Rabi splitting 2g
    for n in range(5):
        Em, Ep = dressed_energies(n, 0.0, g, wc)
        assert np.isclose(Ep - Em, 2.0 * g * np.sqrt(n + 1))
    assert np.isclose(vacuum_rabi_splitting(g), 2.0 * g)
    Em0, Ep0 = dressed_energies(0, 0.0, g, wc)
    assert np.isclose(Ep0 - Em0, vacuum_rabi_splitting(g))


def test_jcm_inversion_initial_and_unitary():
    wc, wa, g, alpha, N = 5.0, 5.0, 1.0, 3.0, 40
    # atom starts fully excited: <sigma_z>(0) = +1
    assert np.isclose(jcm_inversion(0.0, wc, wa, g, alpha, N), 1.0, atol=1e-9)
    # |<sigma_z>| <= 1 always (sigma_z has eigenvalues +-1) -- a unitarity witness
    t = np.linspace(0, 30, 300)
    W = jcm_inversion(t, wc, 5.4, g, alpha, N)              # detuned, full sweep
    assert np.max(np.abs(W)) <= 1.0 + 1e-9
    # the propagator exp(-iHt) is exactly unitary
    H = jcm_hamiltonian(wc, wa, g, N)
    U = expm(-1j * H * 1.7)
    assert np.allclose(U.conj().T @ U, np.eye(2 * N), atol=1e-9)


def test_collapse_and_revival():
    wc, wa, g, alpha, N = 5.0, 5.0, 1.0, 4.0, 60            # resonant, nbar = 16
    nbar = abs(alpha) ** 2
    tr = revival_time(g, nbar)
    # starts excited
    assert np.isclose(jcm_inversion(0.0, wc, wa, g, alpha, N), 1.0, atol=1e-9)
    # COLLAPSE: deep in the plateau the inversion is near zero
    t_plateau = np.array([8.0, 10.0, 12.0, 14.0, 16.0])
    Wp = jcm_inversion(t_plateau, wc, wa, g, alpha, N)
    assert np.max(np.abs(Wp)) < 0.1
    # REVIVAL: the inversion partially re-grows around t_r
    t_rev = np.linspace(tr - 4.0, tr + 4.0, 61)
    Wr = jcm_inversion(t_rev, wc, wa, g, alpha, N)
    assert np.max(np.abs(Wr)) > 0.3
    assert np.max(np.abs(Wr)) > 3.0 * np.max(np.abs(Wp))   # revival >> collapsed
    # the numerical evolution matches the closed-form Poisson sum on resonance
    t = np.linspace(0, tr + 4.0, 200)
    assert np.allclose(jcm_inversion(t, wc, wa, g, alpha, N),
                       resonant_inversion_series(t, g, alpha, N), atol=1e-9)


def test_collapse_revival_times_formulas():
    assert np.isclose(collapse_time(2.0), np.sqrt(2.0) / 2.0)
    # t_c independent of nbar; t_r = 2 pi sqrt(nbar)/g grows with the field
    assert np.isclose(revival_time(1.0, 16.0), 2 * np.pi * 4.0)
    assert np.isclose(revival_time(1.0, 25.0), 2 * np.pi * 5.0)
    assert revival_time(1.0, 25.0) > revival_time(1.0, 16.0)
    # t_r / t_c ~ pi sqrt(2 nbar): a long flat collapse for a strong field
    assert np.isclose(revival_time(1.0, 16.0) / collapse_time(1.0),
                      np.pi * np.sqrt(2.0 * 16.0))


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
