"""Tests for QM-21 entanglement -- every claim checked against a closed form.

Run directly:   python3 test_entanglement.py     (-> "All N tests passed.")
Or with pytest: pytest test_entanglement.py

Each test pins one piece of the foundations story to an analytic result:
  * the four Bell states are an orthonormal maximally-entangled basis;
  * the singlet is the rotational scalar (J=0) -- (U(x)U)|Psi-> = |Psi->;
  * separability: a PRODUCT state has a PURE reduced state (Schmidt rank 1,
    concurrence 0); a BELL state has reduced state I/2 (rank 2, concurrence 1);
  * the no-factorization theorem (Griffiths Problem 12.1);
  * the singlet correlation E(a,b) = -a.b (Griffiths Eq. 12.4);
  * CHSH: the classical/LHV bound |S| <= 2 (exhaustive over the 16 local
    deterministic strategies), and the quantum / Tsirelson bound 2 sqrt(2),
    reached at the optimal angles and never exceeded;
  * Griffiths' original 3-setting Bell inequality and its 45-degree violation;
  * no faster-than-light signaling (Alice's rho_A is independent of Bob).
"""
import numpy as np

from entanglement import (
    I2, sigma_x, sigma_y, sigma_z, ket0, ket1,
    bloch_ket, ndir, pauli_dot, measure_op, su2,
    kron, product_state, bell_state, singlet, bell_basis,
    normalize, density_matrix,
    partial_trace, purity, is_pure, schmidt_coeffs, schmidt_rank,
    is_product_state, concurrence, concurrence_spinflip,
    correlation, E_singlet, chsh_operator, chsh_value, chsh_from_angles,
    tsirelson_bound, bell_3setting, lhv_deterministic_strategies,
    no_signaling_unitary, no_signaling_measurement,
)


def _approx(x, y, rel=1e-9, abs_=1e-12):
    return abs(x - y) <= max(rel * abs(y), abs_)


def _rand_dir(rng):
    """A random unit 3-vector."""
    v = rng.standard_normal(3)
    return v / np.linalg.norm(v)


def _rand_two_qubit(rng):
    psi = rng.standard_normal(4) + 1j * rng.standard_normal(4)
    return normalize(psi)


# --- 1. single-qubit toolkit -------------------------------------------------

def test_pauli_algebra_and_measure_op():
    """The locally-built spin toolkit is right: Pauli commutators, and the
    measurement observable n.sigma is Hermitian with eigenvalues +-1 (the two
    Stern-Gerlach outcomes) for any direction."""
    assert np.allclose(sigma_x @ sigma_y - sigma_y @ sigma_x, 2j * sigma_z)
    assert np.allclose(sigma_x @ sigma_x, I2)
    rng = np.random.default_rng(0)
    for _ in range(20):
        n = _rand_dir(rng)
        M = measure_op(n)
        assert np.allclose(M, M.conj().T)                       # Hermitian
        w = np.linalg.eigvalsh(M)
        assert np.allclose(np.sort(w), [-1.0, 1.0])             # eigenvalues +-1
        assert np.allclose(M @ M, I2)                           # (n.sigma)^2 = I


# --- 2. the four Bell states -------------------------------------------------

def test_bell_states_orthonormal_basis():
    """The four Bell states form an ORTHONORMAL basis of the 2-qubit space, and
    the singlet is exactly |Psi-> = (|01>-|10>)/sqrt2 (Griffiths Eq. 12.1)."""
    B = bell_basis()
    G = np.array([[np.vdot(u, v) for v in B] for u in B])
    assert np.allclose(G, np.eye(4))                            # orthonormal
    # completeness: sum |b><b| = I
    P = sum(np.outer(b, b.conj()) for b in B)
    assert np.allclose(P, np.eye(4))
    s = 1 / np.sqrt(2)
    assert np.allclose(singlet(), np.array([0, s, -s, 0]))


def test_singlet_rotational_invariance_J0():
    """The singlet is the rotational SCALAR (total spin J=0, ~QM-13): for any
    SU(2) rotation U, (U(x)U)|Psi-> = |Psi->.  The other Bell states are NOT
    invariant -- that is what singles out the singlet as J=0."""
    rng = np.random.default_rng(1)
    sing = singlet()
    for _ in range(20):
        U = su2(rng.uniform(0, 2 * np.pi), axis=_rand_dir(rng))
        rotated = kron(U, U) @ sing
        assert np.allclose(rotated, sing, atol=1e-9)            # invariant
    # a triplet/Bell state is generically rotated into something different
    # (a z-rotation puts a relative phase on |00> vs |11>, so |Phi+> moves)
    U = su2(0.7, axis=(0, 0, 1))
    phi_plus = bell_state("Phi+")
    assert not np.allclose(kron(U, U) @ phi_plus, phi_plus, atol=1e-6)


# --- 3. separability via the reduced density matrix (~QM-20) ------------------

def test_product_state_reduced_is_pure():
    """A PRODUCT state factorizes: its reduced density matrix is PURE
    (purity 1), Schmidt rank 1, concurrence 0.  rho_A equals |a><a| exactly."""
    rng = np.random.default_rng(2)
    for _ in range(15):
        a = normalize(rng.standard_normal(2) + 1j * rng.standard_normal(2))
        b = normalize(rng.standard_normal(2) + 1j * rng.standard_normal(2))
        psi = product_state(a, b)
        rhoA = partial_trace(density_matrix(psi), keep=0)
        assert _approx(purity(rhoA), 1.0)
        assert is_pure(rhoA)
        assert np.allclose(rhoA, np.outer(a, a.conj()))        # = |a><a|
        assert schmidt_rank(psi) == 1
        assert is_product_state(psi)
        assert _approx(concurrence(psi), 0.0, abs_=1e-9)


def test_bell_state_reduced_is_maximally_mixed():
    """An ENTANGLED Bell state does NOT factorize: the reduced state is the
    MAXIMALLY MIXED I/2 (purity 1/2), Schmidt rank 2, concurrence 1.  This is the
    sharp separability diagnostic (Griffiths Problem 12.1)."""
    for name in ("Phi+", "Phi-", "Psi+", "Psi-"):
        psi = bell_state(name)
        rhoA = partial_trace(density_matrix(psi), keep=0)
        rhoB = partial_trace(density_matrix(psi), keep=1)
        assert np.allclose(rhoA, 0.5 * np.eye(2))              # I/2
        assert np.allclose(rhoB, 0.5 * np.eye(2))
        assert _approx(purity(rhoA), 0.5)                     # minimum purity
        assert not is_pure(rhoA)
        assert schmidt_rank(psi) == 2
        assert not is_product_state(psi)
        assert _approx(concurrence(psi), 1.0)                 # maximally entangled


def test_partial_trace_consistency():
    """Partial trace sanity: both reductions are unit-trace density matrices, and
    for a known product state they give the correct single-qubit states."""
    rng = np.random.default_rng(3)
    psi = _rand_two_qubit(rng)
    rho = density_matrix(psi)
    rhoA = partial_trace(rho, keep=0)
    rhoB = partial_trace(rho, keep=1)
    assert _approx(np.trace(rhoA).real, 1.0)
    assert _approx(np.trace(rhoB).real, 1.0)
    assert np.allclose(rhoA, rhoA.conj().T)                   # Hermitian
    # |0>(x)|+x> : Tr_B leaves |0><0|, Tr_A leaves |+x><+x|
    plus_x = normalize(ket0 + ket1)
    p = product_state(ket0, plus_x)
    assert np.allclose(partial_trace(density_matrix(p), 0), np.outer(ket0, ket0.conj()))
    assert np.allclose(partial_trace(density_matrix(p), 1), np.outer(plus_x, plus_x.conj()))
    # purity(rhoA) == purity(rhoB) for any bipartite pure state (equal Schmidt spectra)
    assert _approx(purity(rhoA), purity(rhoB))


def test_schmidt_coefficients():
    """Schmidt coefficients: nonneg, sum of squares = 1; rank 1 <=> product,
    rank 2 <=> entangled; reduced-state purity = sum of 4th powers."""
    rng = np.random.default_rng(4)
    for _ in range(10):
        psi = _rand_two_qubit(rng)
        s = schmidt_coeffs(psi)
        assert np.all(s >= -1e-12)
        assert _approx(float(np.sum(s ** 2)), 1.0)
        # purity of the reduced state = sum lambda_i^4
        rhoA = partial_trace(density_matrix(psi), 0)
        assert _approx(purity(rhoA), float(np.sum(s ** 4)))
    assert schmidt_rank(product_state(ket0, ket1)) == 1
    assert schmidt_rank(singlet()) == 2


# --- 4. concurrence & the no-factorization theorem ---------------------------

def test_concurrence_two_forms_agree():
    """The determinant concurrence C = 2|ad-bc| equals Wootters' spin-flip form
    |<psi|sy(x)sy|psi*>| for any pure 2-qubit state; both lie in [0,1]."""
    rng = np.random.default_rng(5)
    for _ in range(30):
        psi = _rand_two_qubit(rng)
        c1, c2 = concurrence(psi), concurrence_spinflip(psi)
        assert _approx(c1, c2, abs_=1e-9)
        assert -1e-9 <= c1 <= 1.0 + 1e-9


def test_no_factorization_theorem():
    """Griffiths Problem 12.1: the state alpha|01> + beta|10> is a PRODUCT state
    iff alpha=0 or beta=0; otherwise it cannot be factored.  Concurrence is
    C = 2|alpha beta|, which is 0 exactly on those two degenerate cases and >0
    for any genuine superposition -- a numerical proof of the theorem."""
    # genuine superpositions are entangled (cannot factor)
    for alpha in (0.5, 0.8, 1 / np.sqrt(2), 0.3 + 0.4j):
        beta = np.sqrt(max(0.0, 1 - abs(alpha) ** 2))
        psi = normalize(np.array([0, alpha, beta, 0], dtype=complex))
        if abs(alpha) > 1e-9 and beta > 1e-9:
            assert concurrence(psi) > 1e-6
            assert not is_product_state(psi)
            assert _approx(concurrence(psi), 2 * abs(alpha) * beta /
                           (abs(alpha) ** 2 + beta ** 2))
    # the degenerate endpoints DO factor: |01> and |10>
    assert is_product_state(np.array([0, 1, 0, 0], dtype=complex))   # |01>
    assert is_product_state(np.array([0, 0, 1, 0], dtype=complex))   # |10>


# --- 5. the singlet correlation E(a,b) = -a.b --------------------------------

def test_singlet_correlation_is_minus_a_dot_b():
    """Singlet correlation  E(a,b) = <Psi-|(a.sigma)(x)(b.sigma)|Psi-> = -a.b
    (Griffiths Eq. 12.4, p.570).  Checked for many random directions, including
    the perfect (anti)correlation at b = +-a."""
    rng = np.random.default_rng(6)
    for _ in range(50):
        a, b = _rand_dir(rng), _rand_dir(rng)
        assert _approx(E_singlet(a, b), -float(np.dot(a, b)), abs_=1e-9)
    a = _rand_dir(rng)
    assert _approx(E_singlet(a, a), -1.0)          # parallel: perfect anti-corr
    assert _approx(E_singlet(a, -a), +1.0)         # anti-parallel: perfect corr
    # correlation is real for any (possibly entangled) state & directions
    psi = _rand_two_qubit(rng)
    assert abs(np.imag(np.vdot(psi, chsh_operator(ndir(0.0), ndir(1.0),
                                                  ndir(0.5), ndir(1.5)) @ psi))) < 1e-9


# --- 6. CHSH: classical bound, Tsirelson bound -------------------------------

def test_chsh_classical_bound_exhaustive():
    """The CLASSICAL / local-hidden-variable bound |S| <= 2 (Bell/CHSH).  A local
    deterministic strategy gives |S| = 2 for EVERY assignment (one of B+-B' is 0,
    the other +-2), and any LHV theory is a mixture of these 16 vertices, so the
    LHV maximum of |S| is exactly 2."""
    S = lhv_deterministic_strategies()
    assert np.all(np.abs(S) <= 2.0 + 1e-12)        # never exceeds 2
    assert _approx(float(np.max(np.abs(S))), 2.0)  # and saturates 2
    assert set(np.round(S).astype(int)) <= {-2, 0, 2}
    # an arbitrary probability mixture (a general LHV theory) still obeys |S|<=2
    rng = np.random.default_rng(7)
    for _ in range(200):
        w = rng.random(16)
        w /= w.sum()
        assert abs(float(np.dot(w, S))) <= 2.0 + 1e-12


def test_chsh_physical_lhv_model_below_2():
    """A concrete physical LOCAL hidden-variable model -- shared random vector
    lambda, A(a)=sign(a.lambda), B(b)=-sign(b.lambda) -- estimated by Monte Carlo
    stays at/under the classical bound 2 and FAR below the quantum 2 sqrt2: no
    local model can reproduce the quantum correlations."""
    rng = np.random.default_rng(8)
    N = 40000
    lam = rng.standard_normal((N, 3))
    lam /= np.linalg.norm(lam, axis=1, keepdims=True)
    d2r = np.pi / 180.0
    dirs = {k: ndir(v * d2r) for k, v in
            dict(a=0, ap=90, b=45, bp=135).items()}

    def E(x, y):
        return float(np.mean(np.sign(lam @ dirs[x]) * (-np.sign(lam @ dirs[y]))))

    S = E("a", "b") - E("a", "bp") + E("ap", "b") + E("ap", "bp")
    assert abs(S) <= 2.0 + 0.05                    # classical bound (+ MC noise)
    assert abs(S) < 2.4                            # nowhere near Tsirelson 2.83


def test_chsh_quantum_violation_at_optimal_angles():
    """Quantum mechanics VIOLATES the classical bound: for the singlet at the
    optimal spin-1/2 angles (a,a',b,b') = (0,90,45,135) deg, |S| = 2 sqrt(2),
    the Tsirelson bound -- decisively above 2."""
    S = chsh_from_angles(singlet(), 0, 90, 45, 135)
    assert _approx(S, -tsirelson_bound())          # = -2 sqrt2
    assert abs(S) > 2.0                             # violates classical bound
    assert _approx(abs(S), tsirelson_bound())      # saturates Tsirelson
    # the equivalent operator's largest eigenvalue is also 2 sqrt2
    Bop = chsh_operator(ndir(0.0), ndir(np.pi / 2),
                        ndir(np.pi / 4), ndir(3 * np.pi / 4))
    assert _approx(float(np.max(np.abs(np.linalg.eigvalsh(Bop)))),
                   tsirelson_bound())


def test_chsh_never_exceeds_tsirelson():
    """The TSIRELSON bound: |S| <= 2 sqrt2 for the singlet over MANY random
    (non-coplanar) angle sets -- quantum mechanics cannot beat 2 sqrt2 either.
    Also verified at the operator level: ||B|| <= 2 sqrt2 for any settings and
    hence <B> <= 2 sqrt2 for ANY state."""
    rng = np.random.default_rng(9)
    Tb = tsirelson_bound()
    worst = 0.0
    for _ in range(2000):
        a, ap, b, bp = (_rand_dir(rng) for _ in range(4))
        S = chsh_value(singlet(), a, ap, b, bp)
        assert abs(S) <= Tb + 1e-9
        worst = max(worst, abs(S))
        # operator norm bound holds for EVERY state, not just the singlet
        Bop = chsh_operator(a, ap, b, bp)
        assert np.max(np.abs(np.linalg.eigvalsh(Bop))) <= Tb + 1e-9
        psi = _rand_two_qubit(rng) if _ % 200 == 0 else None
        if psi is not None:
            assert abs(chsh_value(psi, a, ap, b, bp)) <= Tb + 1e-9
    assert worst > 2.0                              # random search does find violations


# --- 7. Griffiths' original 3-setting Bell inequality ------------------------

def test_griffiths_3setting_bell_violation():
    """Griffiths' Bell inequality |P(a,b)-P(a,c)| <= 1+P(b,c) (Eq. 12.12, p.571).
    His own example: a, b, c coplanar with a _|_ b and c at 45 deg to both gives
        |0 - (-1/sqrt2)| = 0.707  vs  1 + (-1/sqrt2) = 0.293,
    so 0.707 <= 0.293 is FALSE -- quantum mechanics violates Bell.  A local
    deterministic strategy, by contrast, always satisfies it."""
    a, b, c = ndir(0.0), ndir(np.pi / 2), ndir(np.pi / 4)
    lhs, rhs = bell_3setting(a, b, c)
    assert _approx(lhs, 1 / np.sqrt(2), abs_=1e-9)     # 0.707
    assert _approx(rhs, 1 - 1 / np.sqrt(2), abs_=1e-9) # 0.293
    assert lhs > rhs                                    # the violation
    # By contrast a local hidden-variable theory always SATISFIES it.  With the
    # perfect anti-correlation B(d,lam) = -A(d,lam), the LHV correlation is
    # P(x,y) = -<A(x)A(y)>; for a single shared response (alpha,beta,gamma in
    # {+-1} to a,b,c) this gives |P(a,b)-P(a,c)| = |gamma-beta| <= 1-beta*gamma
    # = 1+P(b,c) (Griffiths Eqs. 12.8-12.12), and any rho(lam) is a mixture.
    for al in (1, -1):
        for be in (1, -1):
            for ga in (1, -1):
                Pab, Pac, Pbc = -al * be, -al * ga, -be * ga
                assert abs(Pab - Pac) <= 1 + Pbc + 1e-12


# --- 8. no faster-than-light signaling ---------------------------------------

def test_no_signaling_under_bob_unitary():
    """Alice's reduced state is INDEPENDENT of Bob's choice of local unitary
    (his measurement basis): rho_A = Tr_B[(I(x)U) rho (I(x)U^dagger)] = Tr_B[rho]
    for any U.  Bob cannot signal to Alice (Griffiths p.571-572)."""
    rng = np.random.default_rng(10)
    for state in (singlet(), bell_state("Phi+"), _rand_two_qubit(rng)):
        for _ in range(10):
            U = su2(rng.uniform(0, 2 * np.pi), axis=_rand_dir(rng))
            before, after = no_signaling_unitary(state, U)
            assert np.allclose(before, after, atol=1e-12)


def test_no_signaling_under_bob_measurement():
    """Operational no-signaling: when Bob MEASURES (non-selectively) in ANY basis
    and outcomes are averaged, Alice's marginal rho_A is unchanged.  For a Bell
    state rho_A stays I/2 no matter what (or whether) Bob measures -- so Alice's
    local statistics carry no information about Bob's setting."""
    rng = np.random.default_rng(11)
    for state in (singlet(), bell_state("Psi+"), _rand_two_qubit(rng)):
        for _ in range(10):
            basis_U = su2(rng.uniform(0, 2 * np.pi), axis=_rand_dir(rng))
            before, after = no_signaling_measurement(state, basis_U)
            assert np.allclose(before, after, atol=1e-12)
    # Bell state: rho_A is I/2 regardless of Bob's basis
    for _ in range(5):
        U = su2(rng.uniform(0, 2 * np.pi), axis=_rand_dir(rng))
        _, after = no_signaling_measurement(singlet(), U)
        assert np.allclose(after, 0.5 * np.eye(2), atol=1e-12)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
