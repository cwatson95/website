"""Tests for QM-20 density matrix -- every claim checked against a closed form.

Run directly:   python3 test_density_matrix.py     (-> "All N tests passed.")
Or with pytest: pytest test_density_matrix.py

Each test pins one fact about the density operator to an analytic result:
  * rho is Hermitian, unit-trace, positive semidefinite (a valid state),
  * purity Tr(rho^2) = 1 (pure) vs < 1 (mixed), = 1/d (maximally mixed),
  * rho^2 = rho iff pure,
  * <A> = Tr(rho A) reproduces <psi|A|psi> and the ensemble average,
  * the partial trace obeys its defining property; a Bell subsystem is I/2 (S=ln2)
    while a product subsystem stays pure (S=0)  -- the entanglement signature,
  * S = -Tr(rho ln rho): 0 (pure), ln2 (max-mixed qubit), ln d (max-mixed qudit),
    unitarily invariant,
  * ihbar rho-dot = [H,rho]: unitary evolution conserves purity & spectrum; a
    state diagonal in the energy basis is stationary; the finite-difference
    derivative matches -(i/hbar)[H,rho].
"""
import math
import numpy as np

from density_matrix import (
    sigma_x, ket0, ket1, plus, minus,
    tensor, bell_phi_plus, maximally_mixed, random_density_matrix,
    density_matrix_pure, density_matrix_mixed,
    is_hermitian, is_positive_semidefinite, trace_is_one, is_density_matrix,
    purity, is_pure, expectation, partial_trace, von_neumann_entropy,
    commutator, von_neumann_rhs, evolve,
)


def _approx(x, y, rel=1e-9, abs_=1e-9):
    return abs(x - y) <= max(rel * abs(y), abs_)


def _rand_hermitian(n, rng):
    M = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    return 0.5 * (M + M.conj().T)


def _rand_ket(n, rng):
    v = rng.standard_normal(n) + 1j * rng.standard_normal(n)
    return v / np.sqrt(np.vdot(v, v).real)


# --- 1. validity of pure and mixed density matrices --------------------------

def test_pure_state_is_valid_density_matrix():
    """A pure state rho = |psi><psi| is Hermitian, unit-trace, positive
    semidefinite (eigenvalues {1,0,...,0}), and rank 1 (Griffiths Sec.12.3.1)."""
    rng = np.random.default_rng(0)
    for d in (2, 3, 5):
        rho = density_matrix_pure(_rand_ket(d, rng))
        assert is_hermitian(rho)
        assert trace_is_one(rho)
        assert is_positive_semidefinite(rho)
        assert is_density_matrix(rho)
        w = np.linalg.eigvalsh(rho)
        assert np.all(w >= -1e-12)                       # populations >= 0
        assert _approx(float(w.max()), 1.0)              # one eigenvalue is 1
        assert _approx(float(np.sum(w > 1e-9)), 1.0)     # rank 1


def test_mixed_state_is_valid_density_matrix():
    """A statistical mixture rho = sum p_i |psi_i><psi_i| is still Hermitian,
    unit-trace, positive semidefinite (Griffiths Sec.12.3.2).  The 50/50 z-mixture
    is exactly I/2."""
    rho = density_matrix_mixed([ket0, ket1], [0.5, 0.5])
    assert is_density_matrix(rho)
    assert np.allclose(rho, maximally_mixed(2))          # 50/50 |0>,|1> = I/2
    # a generic random mixture is also a valid state
    rng = np.random.default_rng(1)
    states = [_rand_ket(4, rng) for _ in range(3)]
    p = rng.random(3); p /= p.sum()
    rho = density_matrix_mixed(states, p)
    assert is_density_matrix(rho)


def test_invalid_matrices_rejected():
    """is_density_matrix rejects non-Hermitian, wrong-trace, and indefinite
    matrices -- the three defining properties are independently enforced."""
    non_herm = np.array([[0, 1], [0, 0]], dtype=complex)
    assert not is_density_matrix(non_herm)               # not Hermitian
    assert not is_density_matrix(2.0 * density_matrix_pure(ket0))  # trace 2
    indef = np.array([[2.0, 0.0], [0.0, -1.0]], dtype=complex)     # trace 1 but
    assert trace_is_one(indef) and is_hermitian(indef)            # ... eigenvalue -1
    assert not is_positive_semidefinite(indef)
    assert not is_density_matrix(indef)


# --- 2. purity: Tr(rho^2) = 1 (pure) vs < 1 (mixed) --------------------------

def test_purity_pure_vs_mixed():
    """Tr(rho^2) = 1 iff pure; < 1 if mixed; minimum 1/d at the maximally mixed
    state I/d (Griffiths Prob.12.6(b), p.580).  Purity stays within [1/d, 1]."""
    assert _approx(purity(density_matrix_pure(plus)), 1.0)
    assert is_pure(density_matrix_pure(_rand_ket(4, np.random.default_rng(2))))
    rho_mix = density_matrix_mixed([ket0, ket1], [0.5, 0.5])
    assert purity(rho_mix) < 1.0
    assert _approx(purity(rho_mix), 0.5)                 # I/2 -> 1/2
    for d in (2, 3, 4, 7):
        assert _approx(purity(maximally_mixed(d)), 1.0 / d)   # min purity 1/d
    rng = np.random.default_rng(3)
    for d in (2, 4, 6):                                   # bounds hold for random states
        g = purity(random_density_matrix(d, rank=d, seed=int(rng.integers(1 << 30))))
        assert 1.0 / d - 1e-9 <= g <= 1.0 + 1e-9


def test_idempotent_iff_pure():
    """rho^2 = rho IFF the state is pure (Griffiths Prob.12.6(c)) -- a projector is
    idempotent, a genuine mixture is not."""
    rho_pure = density_matrix_pure(_rand_ket(3, np.random.default_rng(4)))
    assert np.allclose(rho_pure @ rho_pure, rho_pure)    # idempotent
    rho_mix = maximally_mixed(3)
    assert not np.allclose(rho_mix @ rho_mix, rho_mix)   # I/3 squared = I/9 != I/3
    assert is_pure(rho_pure) and not is_pure(rho_mix)


# --- 3. expectation <A> = Tr(rho A) ------------------------------------------

def test_expectation_pure_equals_braket():
    """For a pure state, <A> = Tr(rho A) = <psi|A|psi> (the ~QM-06 expectation),
    and it is real for a Hermitian observable A."""
    rng = np.random.default_rng(5)
    for d in (2, 3, 5):
        psi = _rand_ket(d, rng)
        A = _rand_hermitian(d, rng)
        rho = density_matrix_pure(psi)
        braket = np.vdot(psi, A @ psi)
        assert _approx(braket.imag, 0.0)                 # real for Hermitian A
        assert _approx(expectation(rho, A), braket.real)
    # concrete: <sigma_x> = +1 in |+>, 0 in I/2
    assert _approx(expectation(density_matrix_pure(plus), sigma_x), 1.0)
    assert _approx(expectation(maximally_mixed(2), sigma_x), 0.0)


def test_expectation_mixed_is_ensemble_average():
    """For a mixture, <A> = Tr(rho A) = sum_i p_i <psi_i|A|psi_i> -- the average
    over an ensemble that is NOT identically prepared (Griffiths Eq.12.28).  This
    is the bridge to ~QM-06: a mixed state packages measurement statistics."""
    rng = np.random.default_rng(6)
    d = 4
    states = [_rand_ket(d, rng) for _ in range(3)]
    p = rng.random(3); p /= p.sum()
    A = _rand_hermitian(d, rng)
    rho = density_matrix_mixed(states, p)
    ensemble = sum(pi * np.vdot(s, A @ s).real for s, pi in zip(states, p))
    assert _approx(expectation(rho, A), ensemble)


# --- 4. reduced density matrix (partial trace) -------------------------------

def test_partial_trace_defining_property():
    """The defining property of the reduced state:  Tr[(A x I) rho_AB] =
    Tr[A rho_A].  rho_A reproduces every measurement confined to subsystem A."""
    rng = np.random.default_rng(7)
    dims = [2, 3]                                          # qubit (x) qutrit
    rho = random_density_matrix(dims[0] * dims[1], seed=11)
    A = _rand_hermitian(dims[0], rng)                     # observable on subsystem 0
    B = _rand_hermitian(dims[1], rng)                     # observable on subsystem 1
    rhoA = partial_trace(rho, dims, keep=0)
    rhoB = partial_trace(rho, dims, keep=1)
    assert is_density_matrix(rhoA) and is_density_matrix(rhoB)
    assert _approx(expectation(rho, tensor(A, np.eye(dims[1]))), expectation(rhoA, A))
    assert _approx(expectation(rho, tensor(np.eye(dims[0]), B)), expectation(rhoB, B))


def test_bell_subsystem_is_maximally_mixed():
    """ENTANGLEMENT SIGNATURE (bridge to ~QM-21): the global Bell state |Phi+> is
    PURE (S=0), yet each single-qubit reduction is the MAXIMALLY MIXED I/2
    (purity 1/2, S=ln2).  A subsystem of an entangled pure state is mixed
    (Griffiths Sec.12.3.3, p.582)."""
    rho_bell = density_matrix_pure(bell_phi_plus())
    assert is_pure(rho_bell)                              # global state is pure
    assert _approx(von_neumann_entropy(rho_bell), 0.0, abs_=1e-9)
    for keep in (0, 1):
        red = partial_trace(rho_bell, [2, 2], keep=keep)
        assert np.allclose(red, maximally_mixed(2))       # = I/2
        assert _approx(purity(red), 0.5)
        assert _approx(von_neumann_entropy(red), math.log(2.0))


def test_product_subsystem_stays_pure():
    """A PRODUCT (unentangled) pure state |a> x |b> has pure reductions (S=0): the
    reduced state of subsystem A is exactly |a><a|.  No entanglement, no mixing."""
    a, b = plus, ket0
    rho = density_matrix_pure(tensor(a, b))
    rhoA = partial_trace(rho, [2, 2], keep=0)
    rhoB = partial_trace(rho, [2, 2], keep=1)
    assert np.allclose(rhoA, density_matrix_pure(a))      # reduced A = |a><a|
    assert np.allclose(rhoB, density_matrix_pure(b))
    assert is_pure(rhoA) and is_pure(rhoB)
    assert _approx(von_neumann_entropy(rhoA), 0.0, abs_=1e-9)


def test_partial_trace_recovers_full_trace():
    """Sanity: tracing out everything gives Tr(rho) = 1, and the reductions are
    consistent (Tr rho_A = Tr rho_B = 1) for any bipartite state."""
    rho = random_density_matrix(6, seed=13)
    assert _approx(float(np.trace(partial_trace(rho, [2, 3], keep=0)).real), 1.0)
    assert _approx(float(np.trace(partial_trace(rho, [2, 3], keep=1)).real), 1.0)


# --- 5. von Neumann entropy --------------------------------------------------

def test_entropy_pure_zero_mixed_positive():
    """S = -Tr(rho ln rho) = 0 IFF the state is pure; > 0 for any mixture."""
    assert _approx(von_neumann_entropy(density_matrix_pure(minus)), 0.0, abs_=1e-9)
    rho_mix = density_matrix_mixed([ket0, ket1], [0.5, 0.5])
    assert von_neumann_entropy(rho_mix) > 0.0


def test_entropy_maximally_mixed_is_log_d():
    """S(I/d) = ln d is the MAXIMUM entropy (uniform populations).  Qubit -> ln2;
    in bits (base 2) the maximally mixed qubit has S = 1."""
    assert _approx(von_neumann_entropy(maximally_mixed(2)), math.log(2.0))
    for d in (2, 3, 5, 8):
        assert _approx(von_neumann_entropy(maximally_mixed(d)), math.log(d))
    assert _approx(von_neumann_entropy(maximally_mixed(2), base=2), 1.0)  # 1 bit


def test_entropy_unitarily_invariant():
    """S depends only on the spectrum of rho, so it is invariant under unitary
    evolution: S(U rho U-dagger) = S(rho)."""
    rng = np.random.default_rng(8)
    rho = random_density_matrix(4, rank=3, seed=21)
    H = _rand_hermitian(4, rng)
    assert _approx(von_neumann_entropy(evolve(rho, H, 1.3)),
                   von_neumann_entropy(rho))


# --- 6. dynamics: the von Neumann equation -----------------------------------

def test_unitary_evolution_conserves_purity_and_trace():
    """Under ihbar rho-dot = [H, rho] the evolution rho(t) = U rho U-dagger is
    unitary: it conserves Tr(rho)=1 AND the spectrum, hence purity.  A PURE state
    stays pure for all time (Tr rho^2 = 1 conserved)."""
    rng = np.random.default_rng(9)
    H = _rand_hermitian(4, rng)
    rho0 = density_matrix_pure(_rand_ket(4, rng))         # pure
    for t in (0.0, 0.5, 1.7, 4.2):
        rt = evolve(rho0, H, t)
        assert is_density_matrix(rt)
        assert _approx(purity(rt), 1.0)                  # pure stays pure
        assert _approx(float(np.trace(rt).real), 1.0)
    # a mixed state keeps its eigenvalue spectrum (so purity & entropy fixed)
    rho_m = random_density_matrix(4, rank=4, seed=31)
    w0 = np.sort(np.linalg.eigvalsh(rho_m))
    wt = np.sort(np.linalg.eigvalsh(evolve(rho_m, H, 2.0)))
    assert np.allclose(w0, wt)
    assert _approx(purity(evolve(rho_m, H, 2.0)), purity(rho_m))


def test_von_neumann_equation_finite_difference():
    """The evolved rho(t) actually satisfies ihbar rho-dot = [H, rho]: compare a
    central finite-difference d rho/dt to -(i/hbar)[H, rho(t)] = von_neumann_rhs."""
    rng = np.random.default_rng(10)
    H = _rand_hermitian(3, rng)
    rho0 = random_density_matrix(3, seed=41)
    hbar = 1.0
    t, dt = 0.8, 1e-6
    drho = (evolve(rho0, H, t + dt, hbar) - evolve(rho0, H, t - dt, hbar)) / (2 * dt)
    rhs = von_neumann_rhs(evolve(rho0, H, t, hbar), H, hbar)
    assert np.allclose(drho, rhs, atol=1e-6)
    # equivalently ihbar rho-dot = [H, rho]
    assert np.allclose(1j * hbar * drho, commutator(H, evolve(rho0, H, t, hbar)),
                       atol=1e-6)


def test_stationary_state_commutes_with_H():
    """A state STATIONARY under H is exactly one that COMMUTES with H ([H,rho]=0):
    then von_neumann_rhs = 0 and rho(t) = rho(0).  A mixture of energy eigenstates
    is stationary; a state with off-diagonal energy coherences is not (its
    coherences rotate -- the seed of decoherence, Griffiths Sec.12.5)."""
    rng = np.random.default_rng(11)
    H = _rand_hermitian(4, rng)
    w, V = np.linalg.eigh(H)                              # energy eigenbasis
    # rho diagonal in the energy basis: mixture of eigenstates -> commutes with H
    p = rng.random(4); p /= p.sum()
    rho_stat = sum(pi * np.outer(V[:, k], V[:, k].conj()) for k, pi in enumerate(p))
    assert np.allclose(commutator(H, rho_stat), 0.0, atol=1e-9)
    assert np.allclose(von_neumann_rhs(rho_stat, H), 0.0, atol=1e-9)
    assert np.allclose(evolve(rho_stat, H, 3.3), rho_stat, atol=1e-9)  # unchanged
    # a non-commuting state genuinely evolves
    rho_dyn = density_matrix_pure(V[:, 0] + V[:, 1])      # coherent superposition
    assert not np.allclose(commutator(H, rho_dyn), 0.0, atol=1e-6)
    assert not np.allclose(evolve(rho_dyn, H, 1.0), rho_dyn, atol=1e-3)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
