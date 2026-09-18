"""
QM-21  Entanglement & foundations  --  EPR, Bell states, separability, and the
CHSH/Bell inequality as linear algebra you can evaluate and cross-check.

Part of the physics topic network (see modules/topic_network.txt, module QM-21).
Builds on ~QM-11 (two spin-1/2 qubits) and ~QM-20 (the reduced density matrix is
the entanglement diagnostic); the singlet is the J=0 state of ~QM-13. Points
forward to ~QO-05 (entangled photons / squeezing -- the photon realization of
the same Bell tests; NOT built yet, bridge noted).

This module is SELF-CONTAINED: the qubit / Pauli / Bell toolkit is built here in
numpy (we do NOT import the concurrent QM-11/QM-20 code).

The thread (Griffiths 3e, Ch. 12 "Afterword"):

  1. EPR / entangled states.  The spin-0 pion decays to the SINGLET
        |Psi^-> = (|01> - |10>)/sqrt(2)
     (Griffiths Eq. 12.1, p.567).  This is the classic *entangled* state: it
     CANNOT be written as a product |a>(x)|b> (Griffiths Problem 12.1, p.568).
     Diagnostic: the reduced state of one qubit is PURE for a product state but
     MAXIMALLY MIXED (= I/2) for a Bell state (partial_trace, purity).

  2. The four Bell states  |Phi^+->, |Psi^+-> -- a maximally entangled
     orthonormal basis of the two-qubit space.

  3. Local hidden variables & Bell.  Bell (1964) showed any LOCAL HIDDEN
     VARIABLE theory obeys an inequality that quantum mechanics violates.  The
     singlet correlation is  E(a,b) = <Psi^-|(a.sigma)(x)(b.sigma)|Psi^-> = -a.b
     (Griffiths Eq. 12.4, p.570).  Two inequalities:
        * CHSH (4 settings):  S = E(a,b) - E(a,b') + E(a',b) + E(a',b').
          Classical/LHV bound |S| <= 2; quantum (singlet, optimal angles)
          |S| = 2 sqrt(2) -- the TSIRELSON bound; |S| never exceeds 2 sqrt(2).
        * Griffiths' original 3-setting Bell inequality
          |P(a,b) - P(a,c)| <= 1 + P(b,c)   (Eq. 12.12, p.571), reproduced with
          his own 45-degree example.

  4. What it means / doesn't.  Violation => NO local hidden variables (nature is
     nonlocal).  But NO faster-than-light signaling: Alice's marginal statistics
     (her reduced rho) are independent of Bob's choice of measurement
     (no_signaling; Griffiths p.571-572, the "bug's shadow" argument).

Conventions
-----------
* States are complex 1-D numpy arrays; <phi|psi> = vdot(phi, psi) (conjugates
  the first argument); rho = |psi><psi| = outer(psi, conj(psi)).
* Natural units hbar = 1, so the spin operators are the Pauli matrices sigma
  with eigenvalues +-1 (i.e. spin +-hbar/2).  A measurement DIRECTION is a unit
  3-vector n; the observable is n.sigma (eigenvalues +-1).
* Two-qubit computational basis order: |00>, |01>, |10>, |11> (qubit A = first /
  "Alice", qubit B = second / "Bob").
"""

import numpy as np

__all__ = [
    # single-qubit toolkit
    "I2", "sigma_x", "sigma_y", "sigma_z", "ket0", "ket1",
    "bloch_ket", "ndir", "pauli_dot", "measure_op", "su2",
    # two-qubit states
    "kron", "product_state", "bell_state", "singlet", "bell_basis",
    "normalize", "density_matrix",
    # entanglement diagnostics
    "partial_trace", "purity", "is_pure", "schmidt_coeffs", "schmidt_rank",
    "is_product_state", "concurrence", "concurrence_spinflip",
    # correlations & Bell/CHSH
    "correlation", "E_singlet", "chsh_operator", "chsh_value", "chsh_from_angles",
    "tsirelson_bound", "bell_3setting", "lhv_deterministic_strategies",
    # no-signaling
    "no_signaling_unitary", "no_signaling_measurement",
]

_TOL = 1e-12

# --- single-qubit toolkit (built locally; no QM-11 import) -------------------
I2      = np.eye(2, dtype=complex)
sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
_SIGMA  = (sigma_x, sigma_y, sigma_z)

ket0 = np.array([1, 0], dtype=complex)   # spin-up   along z, |0>
ket1 = np.array([0, 1], dtype=complex)   # spin-down along z, |1>


def normalize(psi):
    """Return |psi> rescaled to unit norm <psi|psi> = 1 (complex 1-D array)."""
    psi = np.asarray(psi, dtype=complex).reshape(-1)
    nrm = np.sqrt(np.vdot(psi, psi).real)
    if nrm < 1e-15:
        raise ValueError("cannot normalize a zero vector")
    return psi / nrm


def bloch_ket(theta, phi=0.0):
    """Single-qubit |+n> pointing at (theta, phi) on the Bloch sphere:
        |+n> = (cos(theta/2),  e^{i phi} sin(theta/2)),
    the +1 eigenstate of n.sigma.  theta=0 -> |0> (spin-up z)."""
    return np.array([np.cos(theta / 2.0),
                     np.exp(1j * phi) * np.sin(theta / 2.0)], dtype=complex)


def ndir(theta, phi=0.0):
    """Unit 3-vector n at polar angle theta from z, azimuth phi.  For the planar
    Bell geometry use phi=0: n(theta) = (sin theta, 0, cos theta), so the angle
    BETWEEN two such vectors is the difference of their thetas."""
    return np.array([np.sin(theta) * np.cos(phi),
                     np.sin(theta) * np.sin(phi),
                     np.cos(theta)], dtype=float)


def pauli_dot(n):
    """n.sigma = nx sigma_x + ny sigma_y + nz sigma_z for a 3-vector n (need not
    be unit)."""
    n = np.asarray(n, dtype=float)
    return n[0] * sigma_x + n[1] * sigma_y + n[2] * sigma_z


def measure_op(n):
    """Spin-1/2 measurement observable along direction n: nhat.sigma, with the
    vector normalized.  Hermitian, eigenvalues +-1 (the two SG outcomes)."""
    n = np.asarray(n, dtype=float)
    nrm = np.linalg.norm(n)
    if nrm < 1e-15:
        raise ValueError("measurement direction must be nonzero")
    return pauli_dot(n / nrm)


def su2(theta, axis=(0.0, 0.0, 1.0)):
    """A 2x2 SU(2) rotation U = cos(theta/2) I - i sin(theta/2) (nhat.sigma):
    rotation by angle theta about the unit axis.  Used to test the rotational
    invariance of the singlet (its J=0 character, ~QM-13)."""
    n = np.asarray(axis, dtype=float)
    n = n / np.linalg.norm(n)
    return np.cos(theta / 2.0) * I2 - 1j * np.sin(theta / 2.0) * pauli_dot(n)


# --- two-qubit states --------------------------------------------------------

def kron(*ops):
    """Kronecker (tensor) product of any number of vectors/matrices, left=A."""
    out = np.asarray(ops[0], dtype=complex)
    for op in ops[1:]:
        out = np.kron(out, np.asarray(op, dtype=complex))
    return out


def product_state(psiA, psiB):
    """The separable (product) two-qubit state |psiA> (x) |psiB>."""
    return kron(normalize(psiA), normalize(psiB))


def bell_state(which):
    """One of the four maximally-entangled Bell states, in the |00>,|01>,|10>,|11>
    basis:
        'Phi+' = (|00> + |11>)/sqrt2     'Phi-' = (|00> - |11>)/sqrt2
        'Psi+' = (|01> + |10>)/sqrt2     'Psi-' = (|01> - |10>)/sqrt2  (singlet)
    """
    s = 1.0 / np.sqrt(2.0)
    table = {
        "Phi+": np.array([s, 0, 0,  s], dtype=complex),
        "Phi-": np.array([s, 0, 0, -s], dtype=complex),
        "Psi+": np.array([0, s,  s, 0], dtype=complex),
        "Psi-": np.array([0, s, -s, 0], dtype=complex),
    }
    if which not in table:
        raise ValueError("Bell state must be one of %s" % list(table))
    return table[which]


def singlet():
    """The spin singlet |Psi^-> = (|01> - |10>)/sqrt2 -- the EPR/EPRB state of
    the spin-0 pion decay (Griffiths Eq. 12.1, p.567); the J=0 state (~QM-13)."""
    return bell_state("Psi-")


def bell_basis():
    """The four Bell states as an orthonormal basis, ordered
    [Phi+, Phi-, Psi+, Psi-]."""
    return [bell_state(k) for k in ("Phi+", "Phi-", "Psi+", "Psi-")]


def density_matrix(psi):
    """rho = |psi><psi| for a (normalized) pure state."""
    psi = normalize(psi)
    return np.outer(psi, psi.conj())


# --- entanglement diagnostics ------------------------------------------------

def partial_trace(rho, keep, dims=(2, 2)):
    """Partial trace of a bipartite density matrix.

    rho acts on a (dA*dB)-dim space with subsystem dims `dims=(dA,dB)`.
    `keep=0` returns rho_A = Tr_B(rho); `keep=1` returns rho_B = Tr_A(rho).

    This is the central entanglement diagnostic (the reduced density matrix of
    ~QM-20): for a PRODUCT state the kept subsystem is left in a PURE state,
    while for an ENTANGLED (e.g. Bell) state it is MIXED.  For a Bell state the
    reduced state is the maximally mixed I/2."""
    dA, dB = dims
    R = np.asarray(rho, dtype=complex).reshape(dA, dB, dA, dB)
    if keep == 0:
        return np.einsum("ijkj->ik", R)      # keep A: trace over B (axes 1,3)
    elif keep == 1:
        return np.einsum("ijil->jl", R)      # keep B: trace over A (axes 0,2)
    raise ValueError("keep must be 0 (keep A) or 1 (keep B)")


def purity(rho):
    """Tr(rho^2) in [1/d, 1].  =1 iff rho is pure; the minimum 1/d is the
    maximally mixed state (1/2 for one qubit)."""
    rho = np.asarray(rho, dtype=complex)
    return np.trace(rho @ rho).real


def is_pure(rho, tol=1e-9):
    """True iff Tr(rho^2) = 1 (a pure state)."""
    return abs(purity(rho) - 1.0) <= tol


def schmidt_coeffs(psi, dims=(2, 2)):
    """Schmidt coefficients of a bipartite pure state |psi>: the singular values
    of psi reshaped to a dA x dB matrix (descending, >=0, sum of squares = 1).
    The number of nonzero coefficients is the Schmidt rank."""
    dA, dB = dims
    M = normalize(psi).reshape(dA, dB)
    return np.linalg.svd(M, compute_uv=False)


def schmidt_rank(psi, dims=(2, 2), tol=1e-9):
    """Schmidt rank = number of nonzero Schmidt coefficients.  1 <=> the state is
    a PRODUCT (separable) state; >1 <=> entangled."""
    return int(np.sum(schmidt_coeffs(psi, dims) > tol))


def is_product_state(psi, dims=(2, 2), tol=1e-9):
    """True iff |psi> factorizes as |a>(x)|b> (Schmidt rank 1) -- equivalently the
    reduced density matrix is pure.  This is the operational form of the
    no-factorization theorem (Griffiths Problem 12.1, p.568)."""
    return schmidt_rank(psi, dims, tol) == 1


def concurrence(psi):
    """Concurrence of a TWO-QUBIT pure state psi = a|00>+b|01>+c|10>+d|11>:
        C = 2 |a d - b c|   in [0, 1].
    C=0 <=> separable; C=1 <=> maximally entangled (any Bell state).
    Equivalently C = 2 * (product of the two Schmidt coefficients)."""
    a, b, c, d = normalize(psi)
    return 2.0 * abs(a * d - b * c)


def concurrence_spinflip(psi):
    """Concurrence via the spin-flip form  C = |<psi| sigma_y(x)sigma_y |psi*>|
    (Wootters).  Equals the determinant form `concurrence` for pure 2-qubit
    states; provided as an independent cross-check."""
    psi = normalize(psi)
    flip = kron(sigma_y, sigma_y)
    return abs(np.vdot(psi, flip @ psi.conj()))


# --- correlations, CHSH, and Bell's inequality -------------------------------

def correlation(state, nA, nB):
    """Spin-spin correlation  E = <state| (nA.sigma) (x) (nB.sigma) |state>  for a
    two-qubit `state` and measurement directions nA (Alice), nB (Bob).  Real for
    any state (the operator is Hermitian).  For the SINGLET this equals -nA.nB
    (Griffiths Eq. 12.4, p.570)."""
    state = normalize(state)
    op = kron(measure_op(nA), measure_op(nB))
    val = np.vdot(state, op @ state)
    return val.real


def E_singlet(nA, nB):
    """Singlet correlation E(a,b) computed FROM the state; provided so tests can
    confirm it equals the closed form -a.b (Griffiths Eq. 12.4)."""
    return correlation(singlet(), nA, nB)


def chsh_operator(a, ap, b, bp):
    """The CHSH operator
        B = (a.sigma)(x)(b.sigma) - (a.sigma)(x)(b'.sigma)
          + (a'.sigma)(x)(b.sigma) + (a'.sigma)(x)(b'.sigma)
    a, a' are Alice's two settings; b, b' Bob's.  Its operator norm is <= 2 sqrt2
    (Tsirelson), so <B> for ANY state never exceeds the Tsirelson bound."""
    A, Ap = measure_op(a), measure_op(ap)
    B, Bp = measure_op(b), measure_op(bp)
    return (kron(A, B) - kron(A, Bp) + kron(Ap, B) + kron(Ap, Bp))


def chsh_value(state, a, ap, b, bp):
    """CHSH quantity S = E(a,b) - E(a,b') + E(a',b) + E(a',b') for `state`.
    Classical/LHV theories obey |S| <= 2; quantum mechanics allows up to
    |S| = 2 sqrt(2) (Tsirelson)."""
    state = normalize(state)
    return np.vdot(state, chsh_operator(a, ap, b, bp) @ state).real


def chsh_from_angles(state, deg_a, deg_ap, deg_b, deg_bp):
    """Convenience: CHSH value with the four planar directions given as angles in
    DEGREES (n(theta) = (sin theta, 0, cos theta)).  The spin-1/2 singlet's
    optimal angles are (a,a',b,b') = (0, 90, 45, 135) deg, giving |S| = 2 sqrt2.

    (For the equivalent PHOTON-polarization test the analyzer angles are halved
    to 0, 45, 22.5, 67.5 deg, because the polarization correlation goes as
    cos 2theta -- those are the famous Aspect angles; see ~QO-05.)"""
    d2r = np.pi / 180.0
    return chsh_value(state,
                      ndir(deg_a * d2r), ndir(deg_ap * d2r),
                      ndir(deg_b * d2r), ndir(deg_bp * d2r))


def tsirelson_bound():
    """The Tsirelson (quantum) bound on |S|: 2 sqrt(2) ~ 2.828."""
    return 2.0 * np.sqrt(2.0)


def bell_3setting(a, b, c, state=None):
    """Griffiths' original three-setting Bell inequality (Eq. 12.12, p.571):
        |P(a,b) - P(a,c)|  <=  1 + P(b,c),
    where P is the singlet correlation E.  Returns (lhs, rhs); a LOCAL HIDDEN
    VARIABLE theory has lhs <= rhs, quantum mechanics can violate it (lhs > rhs).
    `state` defaults to the singlet."""
    if state is None:
        state = singlet()
    Pab = correlation(state, a, b)
    Pac = correlation(state, a, c)
    Pbc = correlation(state, b, c)
    return abs(Pab - Pac), 1.0 + Pbc


def lhv_deterministic_strategies():
    """Enumerate all 16 LOCAL DETERMINISTIC strategies for CHSH and return their
    S values.  A local strategy assigns Alice outcomes (A for setting a, A' for
    a') and Bob outcomes (B, B'), each in {+1,-1}, INDEPENDENT of the other
    wing.  Any local hidden variable theory is a probability mixture of these 16
    vertices, and S is linear in that mixture, so the LHV maximum of |S| is the
    maximum over these vertices -- which is exactly 2 (the classical bound).
    E(x,y) for a deterministic strategy is just the product of the assigned
    outcomes."""
    out = []
    for A in (1, -1):
        for Ap in (1, -1):
            for B in (1, -1):
                for Bp in (1, -1):
                    S = A * B - A * Bp + Ap * B + Ap * Bp
                    out.append(float(S))
    return np.array(out)


# --- no faster-than-light signaling ------------------------------------------

def no_signaling_unitary(state, U_bob):
    """Alice's reduced state is unchanged when Bob applies a local unitary U_bob
    (his choice of measurement basis) on his qubit:
        rho_A = Tr_B[ (I (x) U) rho (I (x) U^dagger) ] = Tr_B[rho].
    Returns (rhoA_before, rhoA_after); they are equal -- Bob cannot signal to
    Alice by choosing his measurement (Griffiths p.571-572)."""
    state = normalize(state)
    rho = density_matrix(state)
    rhoA_before = partial_trace(rho, keep=0)
    full_U = kron(I2, U_bob)
    rho_after = full_U @ rho @ full_U.conj().T
    rhoA_after = partial_trace(rho_after, keep=0)
    return rhoA_before, rhoA_after


def no_signaling_measurement(state, basis_U):
    """Alice's reduced state is unchanged when Bob MEASURES (non-selectively) in
    an arbitrary basis defined by the unitary basis_U on his qubit:
        rho' = sum_k (I (x) P_k) rho (I (x) P_k),  P_k = U|k><k|U^dagger,
        rho_A' = Tr_B(rho') = Tr_B(rho) = rho_A.
    Averaging over Bob's outcomes leaves Alice's marginal statistics untouched --
    the operational statement of no-signaling.  Returns (rhoA_before,
    rhoA_after)."""
    state = normalize(state)
    rho = density_matrix(state)
    rhoA_before = partial_trace(rho, keep=0)
    rho_post = np.zeros_like(rho)
    for k in range(2):
        proj = np.outer(basis_U[:, k], basis_U[:, k].conj())   # P_k on Bob
        Pk = kron(I2, proj)
        rho_post += Pk @ rho @ Pk
    rhoA_after = partial_trace(rho_post, keep=0)
    return rhoA_before, rhoA_after


# --- demo --------------------------------------------------------------------

def _demo():
    print("QM-21  Entanglement & foundations -- the CHSH violation\n")

    print("Separability (reduced state of qubit A):")
    prod = product_state(ket0, ket1)               # |0>(x)|1|, a product state
    sing = singlet()
    rA_prod = partial_trace(density_matrix(prod), keep=0)
    rA_sing = partial_trace(density_matrix(sing), keep=0)
    print("   product |0>|1> : purity(rho_A) = %.3f, Schmidt rank %d, C = %.3f"
          % (purity(rA_prod), schmidt_rank(prod), concurrence(prod)))
    print("   singlet |Psi-> : purity(rho_A) = %.3f, Schmidt rank %d, C = %.3f"
          % (purity(rA_sing), schmidt_rank(sing), concurrence(sing)))
    print("   singlet rho_A =\n", np.round(rA_sing.real, 3),
          "  (= I/2, maximally mixed)\n")

    print("Singlet correlation  E(a,b) = -a.b  (Griffiths Eq. 12.4):")
    z, x = ndir(0.0), ndir(np.pi / 2)
    print("   E(z,z) = %+.3f   (-z.z = -1, perfect anti-correlation)"
          % E_singlet(z, z))
    print("   E(z,x) = %+.3f   (-z.x =  0, uncorrelated)\n" % E_singlet(z, x))

    print("CHSH  S = E(a,b) - E(a,b') + E(a',b) + E(a',b')   |  classical |S|<=2")
    print("   %-22s   S          verdict" % "angles a,a',b,b' (deg)")
    rows = [("optimal  0,90,45,135", (0, 90, 45, 135)),
            ("parallel 0, 0, 0,  0", (0, 0, 0, 0)),
            ("tilt    0,90,30,120", (0, 90, 30, 120)),
            ("tilt    0,60,30, 90", (0, 60, 30, 90))]
    for label, ang in rows:
        S = chsh_from_angles(singlet(), *ang)
        verdict = "VIOLATES (>2)" if abs(S) > 2 + 1e-9 else "classical (<=2)"
        print("   %-22s  %+.4f   %s" % (label, S, verdict))
    print("   Tsirelson bound 2*sqrt2 = %.4f (the quantum maximum)\n"
          % tsirelson_bound())

    print("Griffiths' 3-setting Bell inequality |P(a,b)-P(a,c)| <= 1+P(b,c)"
          " (Eq. 12.12):")
    a, b, c = ndir(0.0), ndir(np.pi / 2), ndir(np.pi / 4)   # a _|_ b, c at 45 deg
    lhs, rhs = bell_3setting(a, b, c)
    print("   a _|_ b, c at 45 deg:  %.3f <= %.3f ?  %s  (QM violates Bell)\n"
          % (lhs, rhs, "yes" if lhs <= rhs + 1e-9 else "NO"))

    print("No signaling: Bob measures in a tilted basis; Alice's rho_A:")
    U = su2(0.9, axis=(1, 0, 0))
    before, after = no_signaling_measurement(singlet(), U)
    print("   max|rho_A(after Bob) - rho_A(before)| = %.2e  (-> Bob cannot signal)"
          % np.max(np.abs(after - before)))


if __name__ == "__main__":
    _demo()
