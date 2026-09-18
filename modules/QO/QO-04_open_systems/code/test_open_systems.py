"""Tests for QO-04 open quantum systems (Lindblad master equation & decoherence).

Run:  python3 test_open_systems.py     ->  "All N tests passed."
"""
import numpy as np

from open_systems import (
    I2, sigma_x, sigma_z, sigma_minus, sigma_plus, ket_e, ket_g, proj_e,
    density_matrix, populations, excited_population, coherence,
    is_hermitian, is_positive_semidefinite, is_density_matrix,
    commutator, lindblad_rhs, evolve_lindblad,
    two_level_hamiltonian, spontaneous_emission_op, dephasing_op,
    steady_state_excited_population,
)

GAMMA = 1.0
PLUS = (ket_e + ket_g) / np.sqrt(2.0)        # (|e>+|g>)/sqrt2, equal coherence


def _fit_rate(t, sig):
    sig = np.asarray(sig, float)
    m = sig > 1e-7 * sig.max()
    return -np.polyfit(np.asarray(t, float)[m], np.log(sig[m]), 1)[0]


def test_ladder_operators_consistent():
    # sigma^- lowers |e> to |g>; sigma^+ is its dagger; sigma^+ sigma^- = |e><e|
    assert np.allclose(sigma_minus @ ket_e, ket_g)
    assert np.allclose(sigma_minus @ ket_g, np.zeros(2))
    assert np.allclose(sigma_plus, sigma_minus.conj().T)
    assert np.allclose(sigma_plus @ sigma_minus, proj_e)
    assert np.allclose(sigma_z, np.diag([1.0, -1.0]))


def test_density_matrix_is_valid_state():
    rho = density_matrix(PLUS)
    assert is_density_matrix(rho)                      # Hermitian, Tr=1, PSD
    assert abs(np.trace(rho) - 1.0) < 1e-12
    assert np.allclose(populations(rho), [0.5, 0.5])   # equal populations
    assert abs(coherence(rho) - 0.5) < 1e-12           # full coherence


def test_lindblad_generator_is_trace_preserving():
    # Tr(rho-dot) = 0 for any rho => Tr rho is conserved (CPTP).
    rho = density_matrix([0.6 + 0.2j, 0.7])
    H = two_level_hamiltonian(1.3, 0.4)
    drho = lindblad_rhs(rho, H, [spontaneous_emission_op(GAMMA),
                                 dephasing_op(0.5)])
    assert abs(np.trace(drho)) < 1e-12


def test_lindblad_generator_is_hermiticity_preserving():
    # rho-dot is Hermitian when rho is, so rho stays Hermitian.
    rho = density_matrix([0.6 + 0.2j, 0.7])
    H = two_level_hamiltonian(1.3, 0.4)
    drho = lindblad_rhs(rho, H, [spontaneous_emission_op(GAMMA)])
    assert is_hermitian(drho)


def test_undriven_rhs_reduces_to_von_neumann():
    # With no collapse operators the master equation is just ihbar rho-dot=[H,rho].
    rho = density_matrix(PLUS)
    H = two_level_hamiltonian(1.0, 0.3)
    assert np.allclose(lindblad_rhs(rho, H, []), -1j * commutator(H, rho))


def test_trace_conserved_under_evolution():
    rho0 = density_matrix(PLUS)
    t = np.linspace(0.0, 6.0, 200)
    rhos = evolve_lindblad(rho0, np.zeros((2, 2)),
                           [spontaneous_emission_op(GAMMA)], t)
    traces = np.array([np.trace(r).real for r in rhos])
    assert np.max(np.abs(traces - 1.0)) < 1e-8


def test_excited_population_decays_at_gamma():
    # start in |e>: rho_ee(t) = e^{-gamma t} exactly (the T1 process).
    t = np.linspace(0.0, 6.0, 400)
    rhos = evolve_lindblad(density_matrix(ket_e), np.zeros((2, 2)),
                           [spontaneous_emission_op(GAMMA)], t)
    pe = np.array([excited_population(r) for r in rhos])
    assert np.max(np.abs(pe - np.exp(-GAMMA * t))) < 1e-6     # closed form
    assert abs(_fit_rate(t, pe) - GAMMA) < 1e-3               # extracted rate


def test_coherence_decays_at_half_gamma():
    # start in |+>: |rho_eg(t)| = 0.5 e^{-(gamma/2) t}  -> T2 = 2 T1.
    t = np.linspace(0.0, 6.0, 400)
    rhos = evolve_lindblad(density_matrix(PLUS), np.zeros((2, 2)),
                           [spontaneous_emission_op(GAMMA)], t)
    coh = np.array([abs(coherence(r)) for r in rhos])
    assert np.max(np.abs(coh - 0.5 * np.exp(-0.5 * GAMMA * t))) < 1e-6
    assert abs(_fit_rate(t, coh) - GAMMA / 2.0) < 1e-3


def test_T2_dephasing_relation():
    # emission + pure dephasing: 1/T2 = 1/(2 T1) + 1/T_phi
    gamma_phi = 0.8
    t = np.linspace(0.0, 5.0, 400)
    rhos = evolve_lindblad(density_matrix(PLUS), np.zeros((2, 2)),
                           [spontaneous_emission_op(GAMMA),
                            dephasing_op(gamma_phi)], t)
    coh = np.array([abs(coherence(r)) for r in rhos])
    rate = _fit_rate(t, coh)
    predicted = GAMMA / 2.0 + gamma_phi          # 1/(2T1) + 1/T_phi
    assert abs(rate - predicted) < 1e-3
    # pure dephasing must NOT change populations
    pe = np.array([excited_population(r) for r in rhos])
    assert np.max(np.abs(pe - 0.5 * np.exp(-GAMMA * t))) < 1e-6


def test_state_stays_positive_semidefinite():
    # a nontrivial driven+damped trajectory stays a valid density matrix.
    t = np.linspace(0.0, 20.0, 400)
    H = two_level_hamiltonian(3.0, 1.0)
    rhos = evolve_lindblad(density_matrix(ket_g), H,
                           [spontaneous_emission_op(GAMMA)], t)
    for r in rhos:
        assert is_positive_semidefinite(r, tol=1e-8)
        assert np.linalg.eigvalsh(r).min() > -1e-8


def test_undriven_steady_state_is_ground():
    # no drive: the unique steady state is |g><g| (everything decays down).
    t = np.linspace(0.0, 40.0, 200)
    rhos = evolve_lindblad(density_matrix(PLUS), np.zeros((2, 2)),
                           [spontaneous_emission_op(GAMMA)], t)
    rho_ss = rhos[-1]
    assert excited_population(rho_ss) < 1e-6
    assert abs(coherence(rho_ss)) < 1e-6
    assert np.allclose(rho_ss, density_matrix(ket_g), atol=1e-6)


def test_driven_steady_state_matches_optical_bloch():
    # driven + damped -> the saturated optical-Bloch steady state.
    t = np.linspace(0.0, 60.0, 600)
    L = spontaneous_emission_op(GAMMA)
    for Omega, Delta in [(2.0, 0.0), (2.0, 1.5), (5.0, -0.7)]:
        H = two_level_hamiltonian(Omega, Delta)
        traj = evolve_lindblad(density_matrix(ket_g), H, [L], t)
        sim = excited_population(traj[-1])
        ana = steady_state_excited_population(Omega, GAMMA, Delta)
        assert abs(sim - ana) < 1e-4


def test_steady_state_saturates_at_one_half():
    # rho_ee^ss rises monotonically in Omega toward 1/2 (never inverts).
    ss = [steady_state_excited_population(O, GAMMA, 0.0)
          for O in [0.5, 1.0, 2.0, 5.0, 50.0]]
    assert all(b > a for a, b in zip(ss, ss[1:]))      # monotonic increasing
    assert ss[-1] < 0.5 and ss[-1] > 0.49              # approaches but < 1/2
    assert steady_state_excited_population(1e8, GAMMA) > 0.4999


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
