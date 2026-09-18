"""
QM-05  Formalism -- the linear-algebra skeleton of quantum mechanics:
Hilbert space, the Dirac bra-ket inner product, linear operators and their
matrix representation, Hermitian operators as observables (the spectral
theorem), commutators, and the canonical commutator [x,p] = i hbar.

Part of the physics topic network (modules/topic_network.txt, module QM-05).
Builds on ~MA-04 (vector spaces, matrices, eigenvalues/eigenvectors,
diagonalization). Feeds ~QM-06 (measurement: eigenvalues are outcomes,
|<n|psi>|^2 are probabilities), ~QM-09 (ladder operators), and is the quantum
half of bridge B7, ~CM-20 (Poisson bracket {A,B} -> (1/i hbar)[A,B]).

Griffiths & Schroeter, *Introduction to QM*, 3rd ed., Chapter 3 (and the
ladder-operator / commutator material of Chapter 2):
  - states are abstract vectors, observables are operators; "the natural
    language of quantum mechanics is linear algebra"          (Sec. 3.1, p.119)
  - inner product <f|g>, orthonormal & complete sets          (Sec. 3.1, p.120)
  - Hermitian operators: <Q> real  <=>  Q = Q-dagger          (Sec. 3.2, p.123)
  - real eigenvalues; eigenvectors of distinct eigenvalues
    are orthogonal (the spectral theorem)                     (Sec. 3.3, p.128)
  - commutator [A,B] = AB - BA                                (Eq. 2.48, p.59)
  - canonical commutation relation [x,p] = i hbar             (Eq. 2.52, p.60)
  - compatible (commuting) observables admit a common set of
    eigenvectors; incompatible ones do not                    (Sec. 3.5, p.139)
  - Dirac notation: bra, ket, dual space, projector |n><n|,
    completeness  sum_n |n><n| = I                            (Sec. 3.6, p.152)

numpy is used because QM is genuinely complex-matrix algebra (Hermitian, not
just real-symmetric -- the canonical commutator is purely imaginary). The
pure-Python real-symmetric Jacobi eigensolver of ~MA-04 is the transparent
version; for a real-symmetric observable the two agree (see the cross-check in
test_formalism.py). Every claim below is checked against a closed form there.
"""

import numpy as np

__all__ = [
    "HBAR",
    # Hilbert space & Dirac notation
    "inner_product", "norm", "normalize", "dagger", "projector",
    # operators / observables
    "is_hermitian", "expectation",
    "spectral_decomposition", "reconstruct_from_spectrum",
    # commutators
    "commutator",
    # canonical (harmonic-oscillator) operators
    "annihilation", "creation", "number_operator",
    "position_operator", "momentum_operator", "canonical_commutator",
    # helpers for randomized self-tests
    "random_hermitian", "random_matrix", "haar_unitary",
]

# Default reduced Planck constant.  Natural units (hbar = 1) make the canonical
# commutator read cleanly as [x,p] = i*I on the interior; pass the physical
# value 1.054571817e-34 J s to the operator builders if you want SI numbers.
HBAR = 1.0


# --- 1. Hilbert space: the inner product and Dirac notation ------------------

def inner_product(phi, psi):
    """Dirac inner product  <phi|psi> = sum_i conj(phi_i) * psi_i  (Griffiths

    Sec. 3.1, Eq. 3.6, p.120).  Physics convention: the BRA (first argument) is
    complex-conjugated, so the form is conjugate-linear in phi and linear in psi
    and obeys <phi|psi> = conj(<psi|phi>).  Returns a (complex) scalar."""
    phi = np.asarray(phi, dtype=complex)
    psi = np.asarray(psi, dtype=complex)
    # np.vdot conjugates its FIRST argument -- exactly the bra <phi|.
    return complex(np.vdot(phi, psi))


def norm(psi):
    """Norm  ||psi|| = sqrt(<psi|psi>).  <psi|psi> is real and non-negative, so
    the square root is real (Griffiths p.120)."""
    return float(np.sqrt(inner_product(psi, psi).real))


def normalize(psi):
    """Return psi scaled to unit norm (a 'normalized' state, Griffiths p.120)."""
    psi = np.asarray(psi, dtype=complex)
    return psi / norm(psi)


def dagger(A):
    """Hermitian conjugate (adjoint) A-dagger = conjugate transpose.  For a
    column ket this is the row bra; for an operator it is the adjoint
    (Griffiths calls a-/+ the hermitian conjugate of a+/-, p.63)."""
    return np.asarray(A, dtype=complex).conj().T


def projector(psi):
    """Projection operator onto the ray spanned by |psi>:  P = |psi><psi| /
    <psi|psi>  (Griffiths Sec. 3.6, Eq. 3.92, p.152).  P is Hermitian and
    idempotent (P^2 = P)."""
    psi = np.asarray(psi, dtype=complex).reshape(-1, 1)
    nrm2 = float((psi.conj().T @ psi).real)
    return (psi @ psi.conj().T) / nrm2


# --- 2. Operators and observables (Hermitian) --------------------------------

def is_hermitian(A, tol=1e-10):
    """True iff A == A-dagger.  An operator represents an observable precisely
    when it is Hermitian, because that is what forces real expectation values
    (Griffiths Sec. 3.2.1, Eqs. 3.16-3.17, p.123)."""
    A = np.asarray(A, dtype=complex)
    return bool(np.allclose(A, dagger(A), atol=tol, rtol=0.0))


def expectation(A, psi):
    """Expectation value  <A> = <psi|A|psi> / <psi|psi>  (Griffiths Eq. 3.13,
    p.123).  For Hermitian A this is guaranteed real -- the reason observables
    are Hermitian."""
    A = np.asarray(A, dtype=complex)
    psi = np.asarray(psi, dtype=complex)
    return inner_product(psi, A @ psi) / inner_product(psi, psi).real


def spectral_decomposition(A):
    """Spectral theorem for a Hermitian matrix (Griffiths Sec. 3.3, p.128):
    returns (eigvals, eigvecs) with eigvals REAL (ascending) and eigvecs an
    ORTHONORMAL set, supplied as the COLUMNS of the returned matrix, with
    A @ eigvecs[:,n] = eigvals[n] * eigvecs[:,n].

    Uses numpy.linalg.eigh, which assumes A is Hermitian.  (~MA-04's
    eig_symmetric is the pure-Python real-symmetric analogue.)"""
    A = np.asarray(A, dtype=complex)
    eigvals, eigvecs = np.linalg.eigh(A)        # eigh -> real ascending vals
    return eigvals, eigvecs


def reconstruct_from_spectrum(eigvals, eigvecs):
    """Rebuild the operator from its spectral resolution

        A = sum_n  lambda_n |n><n|

    (Griffiths Sec. 3.6, projector form, p.152).  `eigvecs` are columns |n>."""
    V = np.asarray(eigvecs, dtype=complex)
    w = np.asarray(eigvals, dtype=complex)
    n = V.shape[0]
    A = np.zeros((n, n), dtype=complex)
    for k in range(len(w)):
        ket = V[:, k].reshape(-1, 1)            # |k>
        A += w[k] * (ket @ ket.conj().T)        # lambda_k |k><k|
    return A


# --- 3. Commutators ----------------------------------------------------------

def commutator(A, B):
    """Commutator  [A,B] = A B - B A  (Griffiths Eq. 2.48, p.59).  It measures
    how badly two operators fail to commute; it vanishes iff they share a
    complete set of eigenvectors (compatible observables, p.139)."""
    A = np.asarray(A, dtype=complex)
    B = np.asarray(B, dtype=complex)
    return A @ B - B @ A


# --- 4. The canonical commutator in the number basis -------------------------
#
# In the harmonic-oscillator number basis |0>,|1>,...,|N-1| the ladder operators
# are (Griffiths Sec. 2.3.1, p.59-65)
#       a |n>  = sqrt(n)   |n-1>        (lowering / annihilation)
#       a+|n>  = sqrt(n+1) |n+1>        (raising  / creation, = a-dagger, p.63)
# and the position / momentum operators are
#       x =      sqrt(hbar/2 m w) (a + a+)
#       p = i*sqrt(hbar m w / 2)  (a+ - a).
# In INFINITE dimensions [a,a+] = I and one finds [x,p] = i hbar I exactly.
#
# In a FINITE N-level truncation this CANNOT hold exactly, and the code is
# honest about it.  a+ a = diag(0,1,...,N-1) is exact, but a a+ loses its top
# rung (a+|N-1> would land on the discarded |N>), so
#       [a,a+] = I - N |N-1><N-1|,
# i.e. it is the identity everywhere EXCEPT the bottom-right corner, which reads
# 1 - N instead of 1.  Therefore
#       [x,p] = i hbar (I - N |N-1><N-1|),
# which equals i hbar exactly on the (N-1)-dimensional INTERIOR block but reads
# -i hbar (N-1) in the corner.  This is not numerical noise: the trace of any
# commutator of finite matrices is 0 (tr(AB)=tr(BA)), whereas tr(i hbar I) =
# i hbar N != 0, so NO pair of finite matrices can satisfy [x,p] = i hbar
# (Wintner-Wielandt).  We therefore test ONLY the interior block, and separately
# assert that the corner / trace mismatch is exactly the predicted artifact.

def annihilation(N):
    """Lowering operator a (N x N) in the number basis:  a|n> = sqrt(n)|n-1>.
    Nonzero entries sit on the super-diagonal: a[n-1, n] = sqrt(n)."""
    a = np.zeros((N, N), dtype=complex)
    for n in range(1, N):
        a[n - 1, n] = np.sqrt(n)
    return a


def creation(N):
    """Raising operator a+ = a-dagger (Griffiths p.63):  a+|n> = sqrt(n+1)|n+1>."""
    return dagger(annihilation(N))


def number_operator(N):
    """Number operator  N_hat = a+ a = diag(0,1,...,N-1).  This one IS exact in
    the truncation (no rung is lost from a+ a)."""
    return creation(N) @ annihilation(N)


def position_operator(N, hbar=None, m=1.0, omega=1.0):
    """Position operator in the N-level number basis,
        x = sqrt(hbar / (2 m omega)) (a + a+),
    Hermitian because a + a+ is.  hbar defaults to module HBAR (=1)."""
    if hbar is None:
        hbar = HBAR
    a = annihilation(N)
    return np.sqrt(hbar / (2.0 * m * omega)) * (a + dagger(a))


def momentum_operator(N, hbar=None, m=1.0, omega=1.0):
    """Momentum operator in the N-level number basis,
        p = i sqrt(hbar m omega / 2) (a+ - a),
    Hermitian because i(a+ - a) is.  hbar defaults to module HBAR (=1)."""
    if hbar is None:
        hbar = HBAR
    a = annihilation(N)
    return 1j * np.sqrt(hbar * m * omega / 2.0) * (dagger(a) - a)


def canonical_commutator(N, hbar=None, m=1.0, omega=1.0):
    """The matrix  [x,p]  in the N-level number basis.  Equals  i hbar  on the
    (N-1)-dim interior block and  -i hbar (N-1)  in the bottom-right corner
    (the truncation artifact -- see the block comment above)."""
    if hbar is None:
        hbar = HBAR
    x = position_operator(N, hbar, m, omega)
    p = momentum_operator(N, hbar, m, omega)
    return commutator(x, p)


# --- helpers for randomized self-tests ---------------------------------------

def random_matrix(n, seed=None):
    """A random complex n x n matrix (generally non-Hermitian, non-normal)."""
    rng = np.random.default_rng(seed)
    return rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))


def random_hermitian(n, seed=None):
    """A random Hermitian n x n matrix  (M + M-dagger)/2 -- a legitimate
    observable, with real eigenvalues and orthonormal eigenvectors."""
    M = random_matrix(n, seed)
    return (M + dagger(M)) / 2.0


def haar_unitary(n, seed=None):
    """A random unitary matrix (columns = an orthonormal basis), from the QR
    decomposition of a complex Gaussian matrix.  Used to build two operators
    that share an eigenbasis (compatible observables)."""
    M = random_matrix(n, seed)
    Q, R = np.linalg.qr(M)
    # fix the phases so Q is Haar-distributed (and deterministic)
    ph = np.diag(R) / np.abs(np.diag(R))
    return Q * ph.conj()


# --- demo --------------------------------------------------------------------

def _demo():
    np.set_printoptions(precision=3, suppress=True)
    print("QM-05 Formalism -- the linear algebra of quantum mechanics\n")

    print("Dirac inner product <phi|psi> (bra is conjugated):")
    phi = np.array([1.0, 1j])
    psi = np.array([1.0, 2.0])
    print("  <phi|psi> =", inner_product(phi, psi),
          "  <psi|phi> =", inner_product(psi, phi), " (complex conjugates)")
    print("  ||(1, i, 1)|| =", round(norm([1.0, 1j, 1.0]), 6), "= sqrt(3)\n")

    print("Spectral theorem for a random Hermitian observable (n=4):")
    A = random_hermitian(4, seed=0)
    w, V = spectral_decomposition(A)
    print("  eigenvalues (real):", np.round(w, 4))
    print("  eigenvectors orthonormal?  V-dagger V = I :",
          np.allclose(dagger(V) @ V, np.eye(4)))
    print("  A = sum_n lambda_n |n><n| reconstructs A :",
          np.allclose(reconstruct_from_spectrum(w, V), A), "\n")

    print("Compatible vs incompatible observables:")
    U = haar_unitary(4, seed=1)
    A1 = U @ np.diag([1.0, 2.0, 3.0, 4.0]) @ dagger(U)
    B1 = U @ np.diag([5.0, 6.0, 7.0, 8.0]) @ dagger(U)   # same eigenbasis U
    print("  commuting pair:   ||[A,B]|| =", round(np.linalg.norm(commutator(A1, B1)), 12))
    B2 = random_hermitian(4, seed=2)
    print("  generic pair:     ||[A,B]|| =", round(np.linalg.norm(commutator(A1, B2)), 4),
          "(not zero -> no shared eigenbasis)\n")

    print("Canonical commutator [x,p] in the N=6 number basis (hbar=1):")
    C = canonical_commutator(6)
    print("  diagonal of [x,p]/i =", np.round(np.diag(C).imag, 6))
    print("  -> i on the interior, but the last entry is the truncation artifact")
    print("  trace[x,p] =", round(np.trace(C).imag, 12),
          "i   (must be 0; tr(i hbar I) would be 6i) -- why finite [x,p]=i hbar is impossible")


if __name__ == "__main__":
    _demo()
