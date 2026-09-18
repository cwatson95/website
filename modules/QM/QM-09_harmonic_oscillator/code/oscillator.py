"""
QM-09  The quantum harmonic oscillator -- the two standard solutions of

        H = p^2/(2m) + (1/2) m omega^2 x^2

    placed side by side and cross-checked against each other.

Part of the physics topic network (modules/topic_network.txt, module QM-09).
Builds on ~QM-05 (operators/commutators) and ~MA-12 (Hermite polynomials, which
this file IMPORTS by relative path). Key bridge B6 of the network:
    ~CM-15 (classical SHM)  ->  QM-09 (quantum SHO)  ->  ~QF-01 (a field is
    infinitely many oscillators).  CM-15/QF-01 are forward references: the bridge
    connects when those modules land; nothing here imports them.

------------------------------------------------------------------------------
Two methods (Griffiths & Schroeter, *Intro to QM* 3e, Sec. 2.3, printed p.57):

  1. ALGEBRAIC (ladder operators), Sec. 2.3.1 (p.59).  Factor H with
        a  = sqrt(m omega/2 hbar) (x + i p/(m omega))   (lowering / annihilation)
        a+ = sqrt(m omega/2 hbar) (x - i p/(m omega))   (raising / creation)
     From [x,p]=i hbar (canonical commutation relation, p.60) one gets
        [a, a+] = 1,   N = a+ a = diag(0,1,2,...),   H = hbar omega (N + 1/2),
     hence the spectrum  E_n = hbar omega (n + 1/2)  with a zero-point energy
     hbar omega/2, and the ladder relations
        a+|n> = sqrt(n+1) |n+1>,   a|n> = sqrt(n) |n-1>,   a|0> = 0.
     We realise a, a+ as matrices in the truncated number basis {|0>,...,|D-1>}.

  2. ANALYTIC (power series -> Hermite), Sec. 2.3.2 (p.67).  Solving the TISE
     directly in the dimensionless variable xi = sqrt(m omega/hbar) x gives the
     Hermite-Gaussian eigenfunctions (Griffiths Eq. 2.85, p.71)
        psi_n(x) = (m omega/pi hbar)^{1/4} (1/sqrt(2^n n!)) H_n(xi) e^{-xi^2/2}.

Both routes give the same spectrum E_n = hbar omega (n + 1/2); the module proves
that numerically.

------------------------------------------------------------------------------
Units.  We work in NATURAL OSCILLATOR UNITS  hbar = m = omega = 1  (so energies
are measured in units of hbar*omega and lengths in sqrt(hbar/m omega)).  Then
xi = x, E_n = n + 1/2, and psi_n(x) = pi^{-1/4} (2^n n!)^{-1/2} H_n(x) e^{-x^2/2}.
The constants HBAR, M, OMEGA below are kept explicit so every formula is written
in physical form and would stay correct if you changed them.

numpy does the linear algebra; scipy.integrate.simpson does the orthonormality
integrals.  Every claim is checked against a closed form in test_oscillator.py.
"""

import math
import os
import sys

import numpy as np

# --- cross-link ~MA-12: import the physicists' Hermite polynomial H_n(x). -----
# Relative-path import (same pattern CM-01 uses for MA-01); becomes
# `from physkit.special_functions import hermite` once a shared package exists.
# MA-12's API is `hermite(n, x)` (scalar x) -- read its code before importing.
_HERE = os.path.dirname(os.path.abspath(__file__))
_MA12 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA",
                                     "MA-12_special_functions", "code"))
if _MA12 not in sys.path:
    sys.path.insert(0, _MA12)
from special_functions import hermite  # noqa: E402  (physicists' H_n; numpy.polynomial.hermite is an equivalent fallback)

__all__ = [
    # units
    "HBAR", "M", "OMEGA", "energy", "zero_point_energy",
    # algebraic method (matrices in the truncated number basis)
    "annihilation", "creation", "number_operator", "hamiltonian_matrix",
    "position_operator", "momentum_operator", "hamiltonian_from_xp",
    "commutator", "basis_vector", "algebraic_spectrum",
    # analytic method (Hermite-Gaussian eigenfunctions)
    "xi", "psi", "ground_state", "overlap",
    "fd_hamiltonian", "fd_spectrum", "fd_residual",
]

# --- natural oscillator units (documented; change at your peril) --------------
HBAR = 1.0     # reduced Planck constant
M = 1.0        # particle mass
OMEGA = 1.0    # angular frequency


def energy(n):
    """Exact eigenenergy  E_n = hbar*omega*(n + 1/2)  (Griffiths Eq. 2.62, p.62).
    The same spectrum falls out of BOTH methods below."""
    return HBAR * OMEGA * (n + 0.5)


def zero_point_energy():
    """Ground-state energy  E_0 = hbar*omega/2: the oscillator cannot sit still
    (a consequence of x,p not commuting). Griffiths p.62."""
    return 0.5 * HBAR * OMEGA


# =============================================================================
# 1. ALGEBRAIC METHOD -- ladder operators as matrices in the number basis
# =============================================================================
# We truncate the (infinite) Hilbert space to the lowest D levels {|0>,...,|D-1>}.
# In this basis the lowering operator has matrix elements <m|a|n> = sqrt(n)
# delta_{m, n-1}: a single nonzero superdiagonal sqrt(1), sqrt(2), ..., sqrt(D-1).
# Truncation is exact for a+a (lowering can't leave the bottom) but NOT for a a+:
# a+|D-1> = sqrt(D)|D> falls off the top and is dropped, so the last entry of
# [a, a+] is wrong by construction -- see commutator() / the tests, which handle
# this honestly rather than hiding it.

def annihilation(D):
    """Lowering (annihilation) operator a as a D x D matrix in the number basis.
    a|n> = sqrt(n)|n-1>, so a[n-1, n] = sqrt(n) for n = 1..D-1."""
    a = np.zeros((D, D), dtype=complex)
    for n in range(1, D):
        a[n - 1, n] = math.sqrt(n)
    return a


def creation(D):
    """Raising (creation) operator a+ = a^dagger as a D x D matrix.
    a+|n> = sqrt(n+1)|n+1>.  Hermitian conjugate of `annihilation` (Griffiths
    p.63: a+ is the adjoint of a)."""
    return annihilation(D).conj().T


def number_operator(D):
    """Number operator  N = a+ a = diag(0, 1, 2, ..., D-1).
    Counts quanta; its eigenvalue n labels the rung of the ladder."""
    return creation(D) @ annihilation(D)


def hamiltonian_matrix(D):
    """Hamiltonian  H = hbar*omega*(N + 1/2)  as a D x D matrix.
    Diagonal, with eigenvalues E_n = hbar*omega*(n + 1/2)."""
    return HBAR * OMEGA * (number_operator(D) + 0.5 * np.eye(D))


def position_operator(D):
    """Position operator  x = sqrt(hbar/(2 m omega)) (a + a+)  as a matrix.
    Truncated in the last row/col (inherits the a a+ defect)."""
    s = math.sqrt(HBAR / (2.0 * M * OMEGA))
    return s * (annihilation(D) + creation(D))


def momentum_operator(D):
    """Momentum operator  p = i sqrt(hbar m omega/2) (a+ - a)  as a matrix."""
    s = math.sqrt(HBAR * M * OMEGA / 2.0)
    return 1j * s * (creation(D) - annihilation(D))


def hamiltonian_from_xp(D):
    """H built the 'physical' way, H = p^2/(2m) + (1/2) m omega^2 x^2, from the
    x and p matrices.  Equals `hamiltonian_matrix(D)` on the interior; the last
    row/col carries the truncation artifact (see the tests)."""
    x = position_operator(D)
    p = momentum_operator(D)
    return (p @ p) / (2.0 * M) + 0.5 * M * OMEGA ** 2 * (x @ x)


def commutator(A, B):
    """Operator commutator  [A, B] = A B - B A.

    For a, a+ the exact result is the identity, [a, a+] = 1 (Griffiths p.60).
    No FINITE matrices can satisfy that, though: tr([A,B]) = 0 always, while
    tr(I) = D.  In the truncated basis the whole defect lands in one corner --
    [a, a+] = diag(1, 1, ..., 1, -(D-1)) -- so the relation holds on the interior
    and the bottom-right entry absorbs the truncation.  The tests check both."""
    return A @ B - B @ A


def basis_vector(n, D):
    """Number eigenstate |n> as a length-D column (1 in slot n, else 0)."""
    e = np.zeros(D, dtype=complex)
    e[n] = 1.0
    return e


def algebraic_spectrum(D):
    """Eigenvalues of the matrix Hamiltonian, sorted ascending.
    Returns E_n = hbar*omega*(n + 1/2) for n = 0..D-1 (genuinely diagonalised,
    not just read off, so it is a real cross-check against the analytic FD
    spectrum)."""
    return np.sort(np.linalg.eigvalsh(hamiltonian_matrix(D)))


# =============================================================================
# 2. ANALYTIC METHOD -- Hermite-Gaussian eigenfunctions of the TISE
# =============================================================================

def xi(x):
    """Dimensionless oscillator coordinate  xi = sqrt(m omega/hbar) x
    (Griffiths Eq. 2.71, p.67).  In natural units xi = x."""
    return math.sqrt(M * OMEGA / HBAR) * np.asarray(x, dtype=float)


def psi(n, x):
    """Normalised energy eigenfunction (Griffiths Eq. 2.85, p.71):

        psi_n(x) = (m omega/pi hbar)^{1/4} (1/sqrt(2^n n!)) H_n(xi) e^{-xi^2/2},
        xi = sqrt(m omega/hbar) x.

    H_n is the physicists' Hermite polynomial, imported from ~MA-12.  Accepts a
    scalar or a numpy array; returns the same shape."""
    xa = np.asarray(x, dtype=float)
    xs = xi(xa)
    Hn = np.vectorize(lambda t: hermite(n, float(t)))(xs)
    norm = (M * OMEGA / (math.pi * HBAR)) ** 0.25 / math.sqrt(2.0 ** n * math.factorial(n))
    out = norm * Hn * np.exp(-xs * xs / 2.0)
    return float(out) if xa.ndim == 0 else out


def ground_state(x):
    """Closed-form ground state  psi_0(x) = (m omega/pi hbar)^{1/4} e^{-xi^2/2}
    (the H_0 = 1 case; a pure Gaussian).  Griffiths Eq. 2.60, p.62."""
    xs = xi(x)
    return (M * OMEGA / (math.pi * HBAR)) ** 0.25 * np.exp(-xs * xs / 2.0)


def overlap(m, n, L=12.0, N=4001):
    """Overlap integral  <psi_m|psi_n> = integral psi_m(x) psi_n(x) dx  on
    [-L, L] by Simpson's rule.  Equals the Kronecker delta delta_{mn}
    (orthonormality, Griffiths Eq. 2.67, p.64)."""
    from scipy.integrate import simpson
    x = np.linspace(-L, L, N)
    return float(simpson(psi(m, x) * psi(n, x), x=x))


def fd_hamiltonian(x):
    """Finite-difference Hamiltonian matrix on grid `x` (uniform spacing):

        H = -(hbar^2/2m) d^2/dx^2 + (1/2) m omega^2 x^2,

    with the Laplacian as the standard 3-point stencil (Dirichlet box).  Used to
    solve the TISE numerically and to check that the analytic psi_n are its
    eigenvectors with eigenvalue E_n."""
    x = np.asarray(x, dtype=float)
    dx = x[1] - x[0]
    kin = HBAR ** 2 / (2.0 * M * dx ** 2)
    main = 2.0 * kin + 0.5 * M * OMEGA ** 2 * x ** 2
    off = -kin * np.ones(len(x) - 1)
    return np.diag(main) + np.diag(off, 1) + np.diag(off, -1)


def fd_spectrum(L=10.0, N=801, k=6):
    """Lowest `k` eigenvalues of the finite-difference Hamiltonian on [-L, L].
    Converges to E_n = hbar*omega*(n + 1/2) -- the analytic method's spectrum,
    obtained with no reference to ladder operators."""
    x = np.linspace(-L, L, N)
    ev = np.sort(np.linalg.eigvalsh(fd_hamiltonian(x)))
    return ev[:k]


def fd_residual(n, L=10.0, N=1201):
    """Relative residual ||H_fd psi_n - E_n psi_n|| / ||psi_n|| on the grid
    interior, where psi_n is the ANALYTIC eigenfunction sampled on the grid and
    E_n = hbar*omega*(n + 1/2).  ~0 confirms each Hermite-Gaussian solves the
    (discretised) Schrodinger equation.  Small and shrinking with dx."""
    x = np.linspace(-L, L, N)
    v = psi(n, x)
    H = fd_hamiltonian(x)
    r = H @ v - energy(n) * v
    interior = slice(5, -5)   # drop the Dirichlet boundary, where the stencil bites
    return float(np.linalg.norm(r[interior]) / np.linalg.norm(v[interior]))


# =============================================================================
# demo
# =============================================================================

def _demo():
    print("QM-09  Quantum harmonic oscillator  (hbar = m = omega = 1)\n")
    D = 8
    print("ALGEBRAIC METHOD  (ladder operators, %d-level number basis)" % D)
    print("  N = a+a diagonal :", np.round(np.diag(number_operator(D)).real, 3))
    print("  H eigenvalues    :", np.round(algebraic_spectrum(D), 3),
          " <- E_n = n + 1/2")
    print("  zero-point energy: E_0 =", zero_point_energy())
    comm = commutator(annihilation(D), creation(D))
    print("  [a,a+] diagonal  :", np.round(np.diag(comm).real, 3),
          " (interior = 1; corner = -(D-1) is the truncation artifact)")
    print("  trace[a,a+]      :", round(np.trace(comm).real, 12),
          " (must be 0 for any finite matrices)")
    print("  a+|2> = sqrt(3)|3>?  ->",
          np.round((creation(D) @ basis_vector(2, D)).real, 4),
          " sqrt(3) =", round(math.sqrt(3), 4))
    print("  a|0> = 0?           ->",
          np.allclose(annihilation(D) @ basis_vector(0, D), 0))

    print("\nANALYTIC METHOD  (Hermite-Gaussian psi_n, H_n imported from MA-12)")
    print("  <psi_m|psi_n> (orthonormality), m,n = 0..3:")
    for m in range(4):
        print("    ", [round(overlap(m, n), 4) for n in range(4)])
    print("  FD residual ||H psi_n - E_n psi_n|| (n=0..4):",
          [float("%.1e" % fd_residual(n)) for n in range(5)])

    print("\nCROSS-CHECK  (both methods, same spectrum):")
    print("  algebraic E_n:", np.round(algebraic_spectrum(D)[:6], 4))
    print("  analytic  E_n:", np.round(fd_spectrum(k=6), 4))


if __name__ == "__main__":
    _demo()
