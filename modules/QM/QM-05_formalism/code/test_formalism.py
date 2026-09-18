"""Tests for QM-05 formalism -- every claim is checked against a closed form.

Run directly:   python3 test_formalism.py     (-> "All N tests passed.")
Or with pytest: pytest test_formalism.py

The headline result -- the canonical commutator -- is tested HONESTLY: [x,p]
equals i*hbar only on the interior block of a finite-dimensional truncation, and
the bottom-right corner / zero-trace mismatch is verified to be exactly the
predicted artifact (no finite matrices can satisfy [x,p] = i*hbar).
"""
import os
import sys

import numpy as np

from formalism import (
    HBAR,
    inner_product, norm, normalize, dagger, projector,
    is_hermitian, expectation,
    spectral_decomposition, reconstruct_from_spectrum,
    commutator,
    annihilation, creation, number_operator,
    position_operator, momentum_operator, canonical_commutator,
    random_hermitian, random_matrix, haar_unitary,
)


def _close(A, B, tol=1e-9):
    return np.allclose(np.asarray(A), np.asarray(B), atol=tol, rtol=0.0)


# --- 1. Hilbert space / inner product ----------------------------------------

def test_inner_product_conjugate_symmetry():
    """<phi|psi> = conj(<psi|phi>)  (Griffiths Eq. 3.8, p.120)."""
    phi = np.array([1.0, 2j, 3.0 - 1j])
    psi = np.array([1j, 1.0, 2.0])
    assert abs(inner_product(phi, psi) - np.conj(inner_product(psi, phi))) < 1e-12


def test_inner_product_sesquilinearity():
    """Conjugate-linear in the bra, linear in the ket."""
    phi = np.array([1.0, 1j, 2.0])
    psi = np.array([2.0, -1j, 1.0])
    c = 2.0 + 3.0j
    assert abs(inner_product(c * phi, psi) - np.conj(c) * inner_product(phi, psi)) < 1e-12
    assert abs(inner_product(phi, c * psi) - c * inner_product(phi, psi)) < 1e-12


def test_norm_real_nonnegative_and_value():
    """<psi|psi> is real, >=0, and ||(1,i,1)|| = sqrt(3)."""
    psi = np.array([1.0, 1j, 1.0])
    ip = inner_product(psi, psi)
    assert abs(ip.imag) < 1e-12 and ip.real > 0
    assert abs(norm(psi) - np.sqrt(3.0)) < 1e-12
    assert abs(norm(normalize(psi)) - 1.0) < 1e-12


# --- 2. dagger / Dirac notation ----------------------------------------------

def test_dagger_involution_and_reversal():
    """(A-dagger)-dagger = A  and  (A B)-dagger = B-dagger A-dagger
    (Griffiths Problem 3.5(b), p.124)."""
    A = random_matrix(5, seed=10)
    B = random_matrix(5, seed=11)
    assert _close(dagger(dagger(A)), A)
    assert _close(dagger(A @ B), dagger(B) @ dagger(A))


def test_projector_is_hermitian_idempotent():
    """P = |psi><psi|/<psi|psi> obeys P = P-dagger, P^2 = P, P|psi> = |psi>
    (Griffiths Sec. 3.6, p.152)."""
    psi = np.array([1.0, 2j, -1.0, 3.0])
    P = projector(psi)
    assert is_hermitian(P)
    assert _close(P @ P, P)
    assert _close(P @ psi, psi)              # psi already lies in the ray
    assert abs(np.trace(P) - 1.0) < 1e-12    # rank-1 projector


def test_resolution_of_identity():
    """Dirac completeness: for an orthonormal basis {|n>}, sum_n |n><n| = I
    (Griffiths Eq. 3.93, p.152)."""
    V = haar_unitary(6, seed=12)             # columns = orthonormal basis
    S = np.zeros((6, 6), dtype=complex)
    for n in range(6):
        S += projector(V[:, n])
    assert _close(S, np.eye(6))


# --- 3. Hermitian operators = observables ------------------------------------

def test_is_hermitian():
    """random_hermitian is Hermitian; a generic matrix is not; x, p, H are."""
    assert is_hermitian(random_hermitian(5, seed=20))
    assert not is_hermitian(random_matrix(5, seed=21))
    N = 7
    assert is_hermitian(position_operator(N))
    assert is_hermitian(momentum_operator(N))
    # H = (p^2 + x^2)/2 is Hermitian (the oscillator Hamiltonian, on the interior)
    x, p = position_operator(N), momentum_operator(N)
    H = (p @ p + x @ x) / 2.0
    assert is_hermitian(H)


def test_hermitian_has_real_expectation_values():
    """The defining property: <psi|A|psi> is real for Hermitian A, generally
    complex otherwise (Griffiths Eqs. 3.13-3.15, p.123)."""
    A = random_hermitian(5, seed=22)
    psi = random_matrix(5, seed=23)[:, 0]
    assert abs(expectation(A, psi).imag) < 1e-12
    B = random_matrix(5, seed=24)            # non-Hermitian
    assert abs(expectation(B, psi).imag) > 1e-6


# --- 4. commutator algebra ---------------------------------------------------

def test_commutator_definition_and_antisymmetry():
    """[A,B] = AB - BA = -[B,A]  (Griffiths Eq. 2.48, p.59)."""
    A = random_matrix(5, seed=30)
    B = random_matrix(5, seed=31)
    assert _close(commutator(A, B), A @ B - B @ A)
    assert _close(commutator(A, B), -commutator(B, A))
    assert _close(commutator(A, A), np.zeros((5, 5)))


def test_jacobi_identity():
    """[A,[B,C]] + [B,[C,A]] + [C,[A,B]] = 0 for ANY matrices (Lie algebra)."""
    A = random_matrix(6, seed=32)
    B = random_matrix(6, seed=33)
    C = random_matrix(6, seed=34)
    J = (commutator(A, commutator(B, C))
         + commutator(B, commutator(C, A))
         + commutator(C, commutator(A, B)))
    assert _close(J, np.zeros((6, 6)), tol=1e-8)


def test_commutator_of_hermitians_is_anti_hermitian():
    """[A,B] of two Hermitian operators is anti-Hermitian, so i[A,B] is
    Hermitian -- this is why the commutator in the uncertainty principle
    carries its own factor of i (Griffiths p.139)."""
    A = random_hermitian(5, seed=35)
    B = random_hermitian(5, seed=36)
    C = commutator(A, B)
    assert _close(dagger(C), -C)             # anti-Hermitian
    assert is_hermitian(1j * C)              # i[A,B] is a legitimate observable


# --- 5. spectral theorem -----------------------------------------------------

def test_spectral_theorem_real_eigenvalues():
    """Theorem 1 (Griffiths p.128): eigenvalues of a Hermitian operator are
    real, even though the matrix is complex."""
    w, _ = spectral_decomposition(random_hermitian(8, seed=40))
    assert np.allclose(w.imag, 0.0)
    assert w.dtype == np.float64           # eigh returns real eigenvalues


def test_spectral_theorem_orthonormal_eigenvectors():
    """Theorem 2 (Griffiths p.128): eigenvectors are orthonormal, V-dagger V = I,
    and A v_n = lambda_n v_n for each one."""
    A = random_hermitian(8, seed=41)
    w, V = spectral_decomposition(A)
    assert _close(dagger(V) @ V, np.eye(8))
    for n in range(8):
        assert _close(A @ V[:, n], w[n] * V[:, n])


def test_spectral_reconstruction():
    """A = sum_n lambda_n |n><n|  rebuilds the operator (Griffiths p.152)."""
    A = random_hermitian(8, seed=42)
    w, V = spectral_decomposition(A)
    assert _close(reconstruct_from_spectrum(w, V), A)
    # ... and equivalently A = V diag(w) V-dagger
    assert _close(V @ np.diag(w) @ dagger(V), A)


# --- 6. compatible vs incompatible observables -------------------------------

def test_compatible_observables_share_eigenbasis():
    """Two Hermitian matrices built from a COMMON eigenbasis commute and are
    simultaneously diagonal in that basis (Griffiths p.139)."""
    U = haar_unitary(5, seed=50)
    da = np.array([1.0, 2.0, 3.0, 4.0, 5.0])      # distinct -> nondegenerate
    db = np.array([-2.0, 0.5, 7.0, 1.0, 3.0])
    A = U @ np.diag(da) @ dagger(U)
    B = U @ np.diag(db) @ dagger(U)
    assert is_hermitian(A) and is_hermitian(B)
    assert _close(commutator(A, B), np.zeros((5, 5)), tol=1e-9)   # they commute
    # A's own eigenvectors (from eigh) must also diagonalize B:
    _, VA = spectral_decomposition(A)
    Bdiag = dagger(VA) @ B @ VA
    off = Bdiag - np.diag(np.diag(Bdiag))
    assert np.linalg.norm(off) < 1e-8           # B is diagonal in A's eigenbasis


def test_incompatible_observables_do_not_share_eigenbasis():
    """Two non-commuting Hermitian matrices: [A,B] != 0 and A's eigenbasis does
    NOT diagonalize B (Griffiths p.139, 'incompatible observables')."""
    A = random_hermitian(5, seed=51)
    B = random_hermitian(5, seed=52)
    assert np.linalg.norm(commutator(A, B)) > 1e-3      # genuinely don't commute
    _, VA = spectral_decomposition(A)
    Bdiag = dagger(VA) @ B @ VA
    off = Bdiag - np.diag(np.diag(Bdiag))
    assert np.linalg.norm(off) > 1e-2           # large off-diagonal: no shared basis


# --- 7. ladder operators and the canonical commutator ------------------------

def test_ladder_relations():
    """a|n> = sqrt(n)|n-1>, a+|n> = sqrt(n+1)|n+1>, a+ = a-dagger, and
    a+ a = number operator = diag(0,...,N-1) EXACTLY (Griffiths Sec. 2.3.1)."""
    N = 6
    a, ad = annihilation(N), creation(N)
    assert _close(ad, dagger(a))
    e2 = np.eye(N)[:, 2]                          # |2>
    assert _close(a @ e2, np.sqrt(2.0) * np.eye(N)[:, 1])     # a|2> = sqrt2 |1>
    assert _close(ad @ e2, np.sqrt(3.0) * np.eye(N)[:, 3])    # a+|2> = sqrt3 |3>
    assert _close(a @ np.eye(N)[:, 0], np.zeros(N))           # a|0> = 0
    assert _close(number_operator(N), np.diag(np.arange(N)))  # exact


def test_canonical_commutator_holds_on_interior():
    """[x,p] = i*hbar on the (N-1)-dim INTERIOR block of the truncation
    (Griffiths Eq. 2.52, p.60).  Off-diagonal entries vanish there too."""
    N = 8
    C = canonical_commutator(N)                  # hbar = 1
    interior = C[:N - 1, :N - 1]
    assert _close(interior, 1j * HBAR * np.eye(N - 1), tol=1e-10)
    # the same holds for a physical hbar:
    hbar = 1.054571817e-34
    Cphys = canonical_commutator(N, hbar=hbar)
    assert _close(Cphys[:N - 1, :N - 1], 1j * hbar * np.eye(N - 1),
                  tol=1e-10 * hbar)


def test_canonical_commutator_truncation_artifact():
    """HONEST finite-dimensional caveat: [x,p] CANNOT equal i*hbar everywhere.
    The corner reads -i*hbar*(N-1), and tr[x,p] = 0 while tr(i*hbar*I) = i*hbar*N.
    No finite matrices satisfy [x,p] = i*hbar (Wintner-Wielandt)."""
    N = 8
    C = canonical_commutator(N)                  # hbar = 1
    # trace of ANY commutator of finite matrices is zero:
    assert abs(np.trace(C)) < 1e-9
    # ... whereas i*hbar*I would have trace i*hbar*N = 8i, so they cannot match:
    assert abs(np.trace(1j * HBAR * np.eye(N)) - np.trace(C)) > 1.0
    # the single offending element is exactly the predicted corner artifact:
    assert abs(C[N - 1, N - 1] - 1j * HBAR * (1 - N)) < 1e-9
    # and it is NOT i*hbar (so we never claim a false exact identity):
    assert abs(C[N - 1, N - 1] - 1j * HBAR) > 1.0
    # the deviation from i*hbar*I is ONLY in that corner (interior is perfect):
    deviation = C - 1j * HBAR * np.eye(N)
    assert abs(deviation[N - 1, N - 1]) > 1.0
    deviation[N - 1, N - 1] = 0.0
    assert np.linalg.norm(deviation) < 1e-9


# --- 8. cross-link: ~MA-04 pure-Python real-symmetric eigensolver ------------

def test_cross_check_MA04_eigensolver():
    """~MA-04 (linear algebra) ships a transparent pure-Python Jacobi solver for
    REAL-symmetric matrices.  For a real-symmetric observable it must agree with
    numpy.linalg.eigh used here: same eigenvalues, and A = Q L Q^T reconstructs.
    (Imported by relative path, following the CM-01 -> MA-01 convention.)"""
    here = os.path.dirname(os.path.abspath(__file__))
    ma04 = os.path.abspath(os.path.join(here, "..", "..", "..", "MA",
                                        "MA-04_linear_algebra", "code"))
    if ma04 not in sys.path:
        sys.path.insert(0, ma04)
    from linalg import eig_symmetric, reconstruct      # noqa: E402

    # a real-symmetric observable (a special case of Hermitian)
    S = [[2.0, 1.0, 0.0], [1.0, 2.0, 1.0], [0.0, 1.0, 2.0]]   # eigvals 2, 2+-sqrt2
    vals_ma, vecs_ma = eig_symmetric(S)
    vals_np, _ = spectral_decomposition(np.array(S, dtype=complex))
    assert _close(sorted(vals_ma), sorted(vals_np.real), tol=1e-8)
    assert _close(reconstruct(vals_ma, vecs_ma), S, tol=1e-8)
    # closed-form eigenvalues:
    assert _close(sorted(vals_np.real), [2 - np.sqrt(2), 2.0, 2 + np.sqrt(2)], tol=1e-8)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
