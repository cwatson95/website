"""
QM-20  Density matrix & open systems  --  the state of a quantum system when you
either don't know it (a statistical mixture) or only have access to part of it
(a subsystem of an entangled whole), written as a Hermitian operator rho you can
evaluate and cross-check.

Part of the physics topic network (see modules/topic_network.txt, module QM-20).
Builds on ~QM-05 (Hilbert space, Hermitian operators, the trace) and ~QM-06
(measurement statistics -- a mixed state IS an ensemble of measurement outcomes);
points forward to ~QM-21 (entanglement: the partial trace below is its operational
signature) and bridges to the unbuilt ~QO-04 (open systems / master equations,
where ihbar rho-dot = [H,rho] is generalized by Lindblad dissipators).

The story, each a function group below (Griffiths 3e, Ch. 12 "Afterword", Sec.12.3):

  1. Pure vs mixed; the density operator.
        pure :  rho = |psi><psi|
        mixed:  rho = sum_i p_i |psi_i><psi_i|        (a classical mix of kets)
     A density matrix is Hermitian, has unit trace, and is positive semidefinite
     (its eigenvalues are probabilities >= 0).        (Griffiths Sec.12.3.1-12.3.2)
     (density_matrix_pure, density_matrix_mixed, is_density_matrix, maximally_mixed)

  2. Purity.  Tr(rho^2) <= 1, with equality IFF the state is pure -- the quick
     test for purity (Griffiths Prob.12.6, p.580).  rho^2 = rho iff pure.
     (purity, is_pure)

  3. Expectation.  <A> = Tr(rho A)  reproduces <psi|A|psi> for a pure state and
     the ensemble average sum_i p_i <psi_i|A|psi_i> for a mixed one.
     (expectation)

  4. Reduced density matrix (partial trace).  A subsystem of an ENTANGLED pure
     state is itself MIXED: tracing one qubit of the Bell state |Phi+> leaves the
     other in I/2 (maximally mixed, S=ln2), while a product state's subsystem
     stays pure (S=0).  This is the operational signature of entanglement (~QM-21).
     (partial_trace)

  5. von Neumann entropy.  S = -Tr(rho ln rho) = -sum_k lambda_k ln lambda_k.
     S=0 iff pure; S=ln(d) for the maximally mixed state in d dimensions.
     (von_neumann_entropy)

  6. Time evolution.  ihbar rho-dot = [H, rho]  (the von Neumann equation,
     Griffiths Prob.12.4(b), p.577).  The closed-form solution is unitary,
     rho(t) = U rho(0) U-dagger with U = exp(-i H t / hbar); it conserves the
     spectrum of rho, hence purity AND entropy.  A rho that commutes with H is
     stationary.  Off-diagonal "coherences" decaying is decoherence (Griffiths
     Sec.12.5, p.586).
     (commutator, von_neumann_rhs, evolve)

Linear algebra via numpy/scipy (QM is complex-matrix algebra; cf. ~MA-04, ~QM-05).
Natural units hbar = 1 unless you pass hbar=... to the evolution routines.
Convention: every routine takes the STATE (rho) first, the operator second --
expectation(rho, A), von_neumann_rhs(rho, H), evolve(rho, H, t).
"""

import numpy as np
from scipy.linalg import expm

__all__ = [
    # constants / fixtures
    "HBAR", "I2", "sigma_x", "sigma_y", "sigma_z",
    "ket0", "ket1", "plus", "minus", "tensor", "bell_phi_plus",
    "maximally_mixed", "random_density_matrix",
    # building density matrices
    "density_matrix_pure", "density_matrix_mixed",
    # validity / structure
    "is_hermitian", "is_positive_semidefinite", "trace_is_one", "is_density_matrix",
    # purity
    "purity", "is_pure",
    # observables
    "expectation",
    # subsystems
    "partial_trace",
    # information
    "von_neumann_entropy",
    # dynamics
    "commutator", "von_neumann_rhs", "evolve",
]

HBAR = 1.0  # natural units; pass hbar=... to evolution routines for SI numbers

# --- spin-1/2 / qubit toolkit (the canonical 2-level examples) ---------------
I2      = np.eye(2, dtype=complex)
sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)

ket0  = np.array([1, 0], dtype=complex)              # |0> = spin up along z
ket1  = np.array([0, 1], dtype=complex)              # |1> = spin down along z
plus  = np.array([1, 1], dtype=complex) / np.sqrt(2)   # |+> = spin up along x
minus = np.array([1, -1], dtype=complex) / np.sqrt(2)  # |-> = spin down along x

_TOL = 1e-9


# --- 0. small helpers --------------------------------------------------------

def _as_matrix(A):
    return np.asarray(A, dtype=complex)


def _normalize(psi):
    """Return a ket scaled to unit norm <psi|psi> = 1 (column-flattened)."""
    psi = np.asarray(psi, dtype=complex).reshape(-1)
    nrm = np.sqrt(np.vdot(psi, psi).real)
    if nrm < _TOL:
        raise ValueError("zero (or near-zero) vector cannot be normalized")
    return psi / nrm


def tensor(*ops):
    """Kronecker (tensor) product of kets or operators: tensor(A, B, C) = A x B x C.

    Lets you build composite-system states/operators, e.g. tensor(ket0, plus) is
    |0> x |+> on a two-qubit space, and tensor(A, I2) lifts a one-qubit observable
    A to act on qubit 0 of a two-qubit system (~QM-21)."""
    out = np.array([[1.0 + 0j]])
    for o in ops:
        out = np.kron(out, np.asarray(o, dtype=complex))
    return np.squeeze(out)


def bell_phi_plus():
    """The Bell state |Phi+> = (|00> + |11>)/sqrt(2): a maximally entangled pure
    two-qubit state.  Its single-qubit reductions are maximally mixed (I/2) --
    the canonical demonstration that a subsystem of an entangled pure state is
    mixed (see partial_trace; Griffiths Sec.12.3.3, p.582)."""
    v = np.zeros(4, dtype=complex)
    v[0] = v[3] = 1.0 / np.sqrt(2.0)
    return v


def maximally_mixed(d):
    """The maximally mixed state in d dimensions, rho = I/d (uniform ignorance).
    Purity 1/d (the minimum) and von Neumann entropy ln(d) (the maximum)."""
    return np.eye(d, dtype=complex) / d


def random_density_matrix(d, rank=None, seed=None):
    """A random valid density matrix of dimension d and given `rank` (default d):
    rho = G G-dagger / Tr(G G-dagger) with G a d x rank complex Gaussian.  This is
    automatically Hermitian, positive semidefinite, and unit-trace.  rank=1 gives
    a (random) pure state; rank>1 a mixed one."""
    rng = np.random.default_rng(seed)
    r = d if rank is None else rank
    G = rng.standard_normal((d, r)) + 1j * rng.standard_normal((d, r))
    M = G @ G.conj().T
    return M / np.trace(M).real


# --- 1. building density matrices --------------------------------------------

def density_matrix_pure(psi):
    """Density operator of a PURE state: rho = |psi><psi| (psi normalized first).

        rho = |psi><psi| / <psi|psi>

    A pure state is one for which we know the ket exactly (Griffiths Sec.12.3.1,
    p.576).  The result is a rank-1 projector: Hermitian, unit-trace, idempotent
    (rho^2 = rho), with purity Tr(rho^2) = 1."""
    psi = _normalize(psi)
    return np.outer(psi, psi.conj())


def density_matrix_mixed(states, probs):
    """Density operator of a statistical MIXTURE of (not necessarily orthogonal)
    pure states |psi_i> with classical probabilities p_i:

        rho = sum_i p_i |psi_i><psi_i|              (Griffiths Sec.12.3.2, p.579)

    Each |psi_i> is normalized internally; the p_i must be non-negative and sum to
    1 (they are 'like any probabilities', Griffiths Eq.12.30).  This is the state
    of a system that is in |psi_i> with probability p_i but we don't know which --
    the ensemble of ~QM-06's measurement statistics, packaged as one operator.
    Generically Tr(rho^2) < 1 (mixed)."""
    probs = np.asarray(probs, dtype=float)
    if np.any(probs < -1e-12):
        raise ValueError("probabilities must be non-negative")
    if abs(probs.sum() - 1.0) > 1e-9:
        raise ValueError("probabilities must sum to 1 (got %.12g)" % probs.sum())
    if len(states) != len(probs):
        raise ValueError("need one probability per state")
    d = len(_normalize(states[0]))
    rho = np.zeros((d, d), dtype=complex)
    for psi, p in zip(states, probs):
        v = _normalize(psi)
        rho += p * np.outer(v, v.conj())
    return rho


# --- 2. validity: Hermitian, unit-trace, positive semidefinite ---------------

def is_hermitian(A, tol=1e-9):
    """True iff A = A-dagger.  A density operator must be Hermitian so that its
    eigenvalues (the populations) are real (Griffiths Sec.12.3.1)."""
    A = _as_matrix(A)
    return A.ndim == 2 and A.shape[0] == A.shape[1] and \
        np.allclose(A, A.conj().T, atol=tol)


def is_positive_semidefinite(A, tol=1e-9):
    """True iff A is Hermitian with all eigenvalues >= 0.  For a density operator
    this says the populations are genuine probabilities (>= 0); together with
    Tr rho = 1 it is what makes rho a state."""
    if not is_hermitian(A, tol):
        return False
    w = np.linalg.eigvalsh(_as_matrix(A)).real
    return bool(np.all(w >= -tol))


def trace_is_one(A, tol=1e-9):
    """True iff Tr(A) = 1 -- the normalization of a density operator
    (Griffiths Eq.12.18 / 12.32: the populations sum to 1)."""
    return abs(np.trace(_as_matrix(A)) - 1.0) <= tol


def is_density_matrix(A, tol=1e-9):
    """True iff A is a legitimate density operator: Hermitian, unit-trace, and
    positive semidefinite (Griffiths Sec.12.3.1-12.3.2).  These three properties
    are exactly the quantum analogue of a classical probability distribution."""
    return is_hermitian(A, tol) and trace_is_one(A, tol) \
        and is_positive_semidefinite(A, tol)


# --- 3. purity ---------------------------------------------------------------

def purity(rho):
    """Purity  gamma = Tr(rho^2),  a real number in [1/d, 1].

    Tr(rho^2) = 1 IFF the state is pure; Tr(rho^2) < 1 for a mixed state, with the
    minimum 1/d at the maximally mixed state I/d (Griffiths Prob.12.6(b), p.580).
    So purity is the one-number test for 'pure vs mixed'."""
    rho = _as_matrix(rho)
    return float(np.trace(rho @ rho).real)


def is_pure(rho, tol=1e-9):
    """True iff rho is a pure state, i.e. Tr(rho^2) = 1 (equivalently rho^2 = rho,
    Griffiths Prob.12.6(c)).  'a quick way to test whether the state is pure'
    (Griffiths Sec.12.3.2, p.579)."""
    return abs(purity(rho) - 1.0) <= tol


# --- 4. expectation values ---------------------------------------------------

def expectation(rho, A):
    """Expectation value of observable A in the state rho:

        <A> = Tr(rho A)                              (Griffiths Eq.12.20 / 12.29)

    For a PURE state rho = |psi><psi| this equals <psi|A|psi> (the ~QM-06 value);
    for a MIXED state it equals the ensemble average sum_i p_i <psi_i|A|psi_i>.
    For a Hermitian observable the result is real, and is returned as a float;
    otherwise the (complex) trace is returned."""
    rho = _as_matrix(rho)
    A = _as_matrix(A)
    val = np.trace(rho @ A)
    if abs(val.imag) <= 1e-12 + 1e-9 * abs(val.real):
        return float(val.real)
    return complex(val)


# --- 5. subsystems: the reduced density matrix (partial trace) ----------------

def partial_trace(rho, dims, keep):
    """Reduced density matrix of the kept subsystem(s), by tracing out the rest.

        rho_A = Tr_B(rho_AB)                          (Griffiths Sec.12.3.3, p.582)

    `dims`  is the list of subsystem dimensions, e.g. [2, 2] for two qubits;
    `keep`  is the index (or list of indices) of the subsystem(s) to RETAIN.
    The defining property is  Tr[(A_kept x I_rest) rho] = Tr[A_kept rho_kept],
    i.e. rho_kept reproduces every measurement confined to the kept subsystem.

    The headline fact (the operational signature of entanglement, ~QM-21): the
    reduced state of a subsystem of an ENTANGLED pure state is MIXED.  Tracing one
    qubit of the Bell state |Phi+> gives I/2 (maximally mixed), even though the
    global state is pure -- see the demo and tests."""
    dims = list(dims)
    n = len(dims)
    if isinstance(keep, (int, np.integer)):
        keep = [int(keep)]
    keep = list(keep)
    rho = _as_matrix(rho).reshape(dims + dims)        # 2n axes: rows then cols
    row = [chr(ord('a') + i) for i in range(n)]       # row labels
    col = [chr(ord('A') + i) for i in range(n)]       # col labels
    for i in range(n):                                 # traced subsystems: row==col
        if i not in keep:
            col[i] = row[i]
    sub_in = ''.join(row) + ''.join(col)
    sub_out = ''.join(row[i] for i in keep) + ''.join(col[i] for i in keep)
    reduced = np.einsum(sub_in + '->' + sub_out, rho)
    d_keep = int(np.prod([dims[i] for i in keep])) if keep else 1
    return reduced.reshape(d_keep, d_keep)


# --- 6. von Neumann entropy --------------------------------------------------

def von_neumann_entropy(rho, base=None):
    """von Neumann entropy  S(rho) = -Tr(rho ln rho) = -sum_k lambda_k ln lambda_k,
    where {lambda_k} are the eigenvalues of rho (its 'populations').

    Conventions: 0 ln 0 = 0; the default is the NATURAL log (nats), so the
    maximally mixed qubit gives S = ln 2; pass base=2 for bits (then it is 1).
    S = 0 IFF the state is pure; S is maximal, ln(d), at the maximally mixed state.
    S is the quantum Shannon entropy of the population distribution and is
    invariant under unitary evolution (the spectrum of rho is conserved)."""
    w = np.linalg.eigvalsh(_as_matrix(rho)).real
    w = w[w > 1e-12]                                   # drop ~0 eigenvalues (0 ln 0 = 0)
    S = float(-np.sum(w * np.log(w)))
    if abs(S) < 1e-12:                                  # S >= 0 exactly; kill round-off
        S = 0.0
    if base is not None:
        S /= np.log(base)
    return S


# --- 7. dynamics: the von Neumann equation -----------------------------------

def commutator(A, B):
    """Commutator [A, B] = A B - B A.  rho is stationary iff [H, rho] = 0, i.e.
    iff rho is diagonal in the energy eigenbasis (Griffiths Prob.12.4(b))."""
    A = _as_matrix(A)
    B = _as_matrix(B)
    return A @ B - B @ A


def von_neumann_rhs(rho, H, hbar=None):
    """Right-hand side of the von Neumann equation, d rho/dt:

        ihbar rho-dot = [H, rho]   =>   rho-dot = -(i/hbar) [H, rho]

    (Griffiths Prob.12.4(b), p.577: 'the Schrodinger equation, expressed in terms
    of rho').  This is the density-matrix form of the Schrodinger equation; in an
    OPEN system (~QO-04) extra Lindblad terms are added to model dissipation."""
    if hbar is None:
        hbar = HBAR
    return -1j / hbar * commutator(H, rho)


def evolve(rho, H, t, hbar=None):
    """Exact unitary evolution of rho under a time-independent H for time t:

        rho(t) = U rho(0) U-dagger,     U = exp(-i H t / hbar)

    -- the closed-form solution of ihbar rho-dot = [H, rho].  Unitary evolution
    conserves the SPECTRUM of rho, hence both purity Tr(rho^2) and the entropy
    S(rho); a pure state stays pure forever.  (Irreversible loss of purity --
    decoherence -- needs the open-system terms of ~QO-04.)"""
    if hbar is None:
        hbar = HBAR
    U = expm(-1j * _as_matrix(H) * t / hbar)
    rho = _as_matrix(rho)
    return U @ rho @ U.conj().T


# --- demo --------------------------------------------------------------------

def _demo():
    np.set_printoptions(precision=4, suppress=True)
    print("QM-20  Density matrix & open systems\n")

    print("1) Pure vs mixed  (qubit):")
    rho_pure = density_matrix_pure(plus)                       # |+><+|
    rho_mixed = density_matrix_mixed([ket0, ket1], [0.5, 0.5])  # 50/50 z-mixture = I/2
    print("   pure  |+><+|:  Tr =", round(np.trace(rho_pure).real, 3),
          " purity =", round(purity(rho_pure), 3),
          " pure?", is_pure(rho_pure))
    print("   mixed 50/50 :  Tr =", round(np.trace(rho_mixed).real, 3),
          " purity =", round(purity(rho_mixed), 3),
          " pure?", is_pure(rho_mixed), " (= I/2)")
    print("   both valid density matrices?",
          is_density_matrix(rho_pure), is_density_matrix(rho_mixed), "\n")

    print("2) Expectation <sigma_x>:  pure |+> is determinate (+1), mix is 0:")
    print("   Tr(rho_pure  sigma_x) =", round(expectation(rho_pure, sigma_x), 3),
          " = <+|sigma_x|+>")
    print("   Tr(rho_mixed sigma_x) =", round(expectation(rho_mixed, sigma_x), 3), "\n")

    print("3) Entanglement via the partial trace (Bell state |Phi+>):")
    rho_bell = density_matrix_pure(bell_phi_plus())
    print("   global state pure? ", is_pure(rho_bell),
          "  S_global =", round(von_neumann_entropy(rho_bell), 4))
    rhoA = partial_trace(rho_bell, [2, 2], keep=0)
    print("   reduced qubit A =\n", np.round(rhoA.real, 4))
    print("   -> maximally mixed: purity =", round(purity(rhoA), 4),
          " S_A =", round(von_neumann_entropy(rhoA), 4), "= ln2")
    rho_prod = density_matrix_pure(tensor(ket0, plus))         # product |0>|+>
    print("   product state |0>|+>: reduced A purity =",
          round(purity(partial_trace(rho_prod, [2, 2], 0)), 4),
          " S_A =", round(von_neumann_entropy(partial_trace(rho_prod, [2, 2], 0)), 4),
          "(stays pure)\n")

    print("4) von Neumann evolution  ihbar rho-dot = [H, rho]  (H = sigma_x):")
    H = sigma_x
    rho_t = evolve(rho_pure, H, t=0.7)
    print("   purity conserved under unitary evolution:",
          round(purity(rho_t), 6), "(pure stays pure)")
    rho_z = density_matrix_pure(ket0)                          # |0><0|, NOT stationary
    print("   |0><0| with H=sigma_x: ||[H,rho]|| =",
          round(np.linalg.norm(commutator(H, rho_z)), 4), "-> evolves")
    therm = density_matrix_mixed([ket0, ket1], [0.7, 0.3])     # diagonal in H=sigma_z basis
    print("   diag-in-H state with H=sigma_z: ||[H,rho]|| =",
          round(np.linalg.norm(commutator(sigma_z, therm)), 12), "-> stationary")


if __name__ == "__main__":
    _demo()
