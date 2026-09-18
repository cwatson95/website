"""
QO-01  Classical & quantized light -- a single field mode as a quantum oscillator,
       its Fock (number) states, quadratures, and coherent states.

Part of the physics topic network (modules/topic_network.txt, module QO-01).
This is KEY BRIDGE B6 of the network in its optics form:

    ~CM-15 (classical SHM) -> ~QM-09 (quantum SHO) -> QO-01 (one EM field MODE is
    a quantum SHO; a, a+ become photon annihilation/creation) -> ~QF-01 (the full
    field is infinitely many such oscillators, one per mode).

A single mode of the electromagnetic field has Hamiltonian
    H = hbar omega (a+ a + 1/2) = hbar omega (n + 1/2),
identical in form to ~QM-09's oscillator.  The eigenstates are the FOCK (number)
states |n> (n photons, energy (n+1/2) hbar omega, with a vacuum zero-point energy
hbar omega/2).  The COHERENT states |alpha> are the eigenstates of a,
    a|alpha> = alpha|alpha>,    |alpha> = e^{-|alpha|^2/2} sum_n alpha^n/sqrt(n!) |n>,
the "most classical" light: Poissonian photon statistics (<n> = |alpha|^2,
Delta n = sqrt<n>, Mandel Q = 0) and minimum-uncertainty, vacuum-level quadrature
noise (Delta X Delta P = 1/4).

------------------------------------------------------------------------------
Reference: M. O. Scully & M. S. Zubairy, *Quantum Optics* (Cambridge, 1997):
  Sec. 1.1 (quantization of the free EM field), Sec. 1.2 (Fock or number states),
  Sec. 2.2-2.4 (coherent states: eigenstates of a, and their properties).
  Cited at section level (see refs.md); page offsets are not pinned here.

------------------------------------------------------------------------------
Units.  Natural single-mode oscillator units  hbar = omega = 1, so energies are
in units of hbar*omega and E_n = n + 1/2.  Operators are realised as matrices in
the number basis {|0>, ..., |N-1>} TRUNCATED to N levels; results away from the
top of the ladder (n << N) are exact to machine precision.  numpy only; no SciPy,
no sibling-module imports.
"""

import math

import numpy as np

__all__ = [
    # units / spectrum
    "HBAR", "OMEGA", "energy", "zero_point_energy",
    # ladder operators and number basis (the quantized mode = a SHO, ~QM-09)
    "annihilation", "creation", "number", "commutator", "fock_state", "expectation",
    # coherent states (eigenstates of a)
    "coherent_state",
    # photon statistics
    "photon_distribution", "mean_n", "var_n", "mandel_q",
    # quadratures and their fluctuations
    "quadrature_x", "quadrature_p", "quadrature_variance",
]

# --- natural single-mode units ----------------------------------------------
HBAR = 1.0     # reduced Planck constant
OMEGA = 1.0    # mode angular frequency


def energy(n):
    """Eigenenergy of the n-photon Fock state, E_n = hbar*omega*(n + 1/2)
    (Scully & Zubairy Sec. 1.2).  Same spectrum as the ~QM-09 oscillator."""
    return HBAR * OMEGA * (n + 0.5)


def zero_point_energy():
    """Vacuum (zero-point) energy E_0 = hbar*omega/2: the field mode fluctuates
    even with zero photons (forced by [a, a+] = 1).  Scully & Zubairy Sec. 1.1."""
    return 0.5 * HBAR * OMEGA


# =============================================================================
# 1. The quantized mode: ladder operators in the truncated number basis
# =============================================================================
# In the number basis the lowering operator has <m|a|n> = sqrt(n) delta_{m,n-1}:
# a single superdiagonal sqrt(1), sqrt(2), ..., sqrt(N-1).  a+ is its adjoint.
# Truncation to N levels is exact for a+a (lowering never needs the rung above the
# top) but NOT for a a+, so [a, a+] = diag(1, ..., 1, -(N-1)): identity on the
# interior, the whole defect parked in the bottom-right corner (same artifact as
# ~QM-09; the tests check the interior and the corner explicitly).

def annihilation(N):
    """Photon annihilation (lowering) operator a as an N x N matrix in the number
    basis:  a|n> = sqrt(n)|n-1>,  so a[n-1, n] = sqrt(n) for n = 1..N-1."""
    a = np.zeros((N, N), dtype=complex)
    for n in range(1, N):
        a[n - 1, n] = math.sqrt(n)
    return a


def creation(N):
    """Photon creation (raising) operator a+ = a^dagger as an N x N matrix:
    a+|n> = sqrt(n+1)|n+1>.  Hermitian conjugate of `annihilation`."""
    return annihilation(N).conj().T


def number(N):
    """Number operator  n = a+ a = diag(0, 1, 2, ..., N-1)  -- counts photons.
    Exact under truncation.  Its eigenvalue n labels the Fock state |n>."""
    return creation(N) @ annihilation(N)


def commutator(A, B):
    """Operator commutator  [A, B] = A B - B A.  For the ladder operators the
    exact relation is [a, a+] = 1; no finite matrices can satisfy that
    (tr[A,B] = 0 always, tr(I) = N), so truncation gives
    [a, a+] = diag(1, ..., 1, -(N-1)) -- identity on the interior."""
    return A @ B - B @ A


def fock_state(n, N):
    """Fock (number) eigenstate |n> as a length-N column (1 in slot n, else 0).
    The |n> are orthonormal, <m|n> = delta_{mn}, and carry n photons."""
    if not 0 <= n < N:
        raise ValueError("need 0 <= n < N")
    psi = np.zeros(N, dtype=complex)
    psi[n] = 1.0
    return psi


def expectation(op, state):
    """Expectation value  <state|op|state> / <state|state>  (real part).
    Used for <n>, <X>, <X^2>, ... of any state in the truncated basis."""
    state = np.asarray(state, dtype=complex)
    nrm = np.vdot(state, state).real
    return float(np.vdot(state, op @ state).real / nrm)


# =============================================================================
# 2. Coherent states -- eigenstates of a (Scully & Zubairy Sec. 2.2)
# =============================================================================

def coherent_state(alpha, N):
    """Coherent state |alpha> in the truncated N-level number basis, built from
    the analytic series (Scully & Zubairy Sec. 2.2)

        |alpha> = e^{-|alpha|^2/2} sum_{n=0}^{inf} alpha^n / sqrt(n!) |n>,

    evaluated with the numerically stable recurrence c_n = c_{n-1} * alpha/sqrt(n)
    (so no overflowing factorials), then RENORMALISED to unit length to absorb the
    tiny probability lost beyond level N-1.  It is the eigenstate of a with
    eigenvalue alpha:  a|alpha> = alpha|alpha> (exact away from the truncation)."""
    alpha = complex(alpha)
    c = np.zeros(N, dtype=complex)
    c[0] = math.exp(-0.5 * abs(alpha) ** 2)
    for n in range(1, N):
        c[n] = c[n - 1] * alpha / math.sqrt(n)
    norm = math.sqrt(float(np.vdot(c, c).real))
    return c / norm


# =============================================================================
# 3. Photon statistics
# =============================================================================

def photon_distribution(state):
    """Photon-number distribution  P(n) = |<n|state>|^2  (an array over n).
    For a coherent state this is Poissonian, P(n) = e^{-<n>} <n>^n / n!."""
    state = np.asarray(state, dtype=complex)
    return np.abs(state) ** 2


def mean_n(state):
    """Mean photon number  <n> = sum_n n P(n) = <state|n|state>."""
    p = photon_distribution(state)
    n = np.arange(p.shape[0])
    return float(np.sum(n * p) / np.sum(p))


def var_n(state):
    """Photon-number variance  (Delta n)^2 = <n^2> - <n>^2.
    Poissonian (coherent) light has (Delta n)^2 = <n>; Fock states have 0."""
    p = photon_distribution(state)
    p = p / np.sum(p)
    n = np.arange(p.shape[0])
    m1 = float(np.sum(n * p))
    m2 = float(np.sum(n * n * p))
    return m2 - m1 * m1


def mandel_q(state):
    """Mandel Q parameter  Q = ((Delta n)^2 - <n>) / <n>.  Q = 0 is Poissonian
    (coherent), Q < 0 sub-Poissonian (nonclassical, e.g. Fock), Q > 0 super-
    Poissonian (e.g. thermal).  Returns 0.0 for the vacuum (<n> = 0)."""
    m = mean_n(state)
    if m <= 0.0:
        return 0.0
    return (var_n(state) - m) / m


# =============================================================================
# 4. Quadratures and vacuum fluctuations (Scully & Zubairy Sec. 2.3-2.4)
# =============================================================================
# The dimensionless field quadratures are the "position" and "momentum" of the
# mode:  X = (a + a+)/2,  P = (a - a+)/2i,  with [X, P] = i/2, hence the
# Heisenberg bound  Delta X Delta P >= 1/4.  The vacuum (and every coherent state)
# saturates it with EQUAL noise Delta X = Delta P = 1/2 -- the hallmark of the
# "most classical" light (squeezing, ~QO-05, breaks that equality).

def quadrature_x(N):
    """Amplitude quadrature  X = (a + a+)/2  as an N x N Hermitian matrix."""
    return 0.5 * (annihilation(N) + creation(N))


def quadrature_p(N):
    """Phase quadrature  P = (a - a+)/(2i)  as an N x N Hermitian matrix."""
    return (annihilation(N) - creation(N)) / 2j


def quadrature_variance(state):
    """Return (Var X, Var P) for `state`, with Var X = <X^2> - <X>^2 (likewise P).
    Vacuum and coherent states give (1/4, 1/4) and so saturate Delta X Delta P =
    1/4; a Fock state |n> gives ((2n+1)/4, (2n+1)/4)."""
    state = np.asarray(state, dtype=complex)
    N = state.shape[0]
    X, P = quadrature_x(N), quadrature_p(N)
    var_x = expectation(X @ X, state) - expectation(X, state) ** 2
    var_p = expectation(P @ P, state) - expectation(P, state) ** 2
    return var_x, var_p


# =============================================================================
# demo
# =============================================================================

def _demo():
    print("QO-01  Classical & quantized light  (hbar = omega = 1)\n")
    N = 60

    print("THE MODE IS AN OSCILLATOR  (Fock basis, N = %d levels)" % N)
    print("  number operator n = a+a diagonal :", np.round(np.diag(number(8)).real, 3))
    print("  E_n = hbar*omega*(n+1/2), vacuum E_0 =", zero_point_energy(),
          " (zero-point energy)")
    comm = commutator(annihilation(8), creation(8))
    print("  [a,a+] diagonal :", np.round(np.diag(comm).real, 3),
          " (interior = 1; corner = -(N-1) truncation artifact)")
    a, ad = annihilation(N), creation(N)
    print("  a+|2> = sqrt(3)|3>? ->", np.round(np.abs((ad @ fock_state(2, N))[3]), 4),
          " sqrt(3) =", round(math.sqrt(3), 4))

    print("\nCOHERENT STATE  |alpha>,  alpha = 2.0  (so <n> should be |alpha|^2 = 4)")
    alpha = 2.0
    coh = coherent_state(alpha, N)
    resid = np.linalg.norm(a @ coh - alpha * coh)
    print("  eigenstate of a:  ||a|alpha> - alpha|alpha>|| = %.2e  (a|alpha>=alpha|alpha>)" % resid)
    nbar = mean_n(coh)
    dn = math.sqrt(var_n(coh))
    print("  <n>      = %.6f      (= |alpha|^2 = %.1f)" % (nbar, abs(alpha) ** 2))
    print("  Delta n  = %.6f      (= sqrt(<n>) = |alpha| = %.4f,  Poissonian)"
          % (dn, abs(alpha)))
    print("  Mandel Q = %.2e   (~ 0: Poissonian, the 'most classical' light)" % mandel_q(coh))
    P = photon_distribution(coh)
    poisson = [math.exp(-abs(alpha) ** 2) * abs(alpha) ** (2 * n) / math.factorial(n) for n in range(7)]
    print("  P(n), n=0..6 :", np.round(P[:7], 4))
    print("  Poisson      :", np.round(poisson, 4), " (match)")
    vx, vp = quadrature_variance(coh)
    print("  quadratures  : Var X = %.4f, Var P = %.4f  (= 1/4 each: vacuum-level noise)"
          % (vx, vp))

    print("\nVACUUM  |0>  (zero photons, irreducible fluctuations)")
    vac = fock_state(0, N)
    vx, vp = quadrature_variance(vac)
    print("  Var X = %.4f,  Var P = %.4f" % (vx, vp))
    print("  Delta X * Delta P = %.4f   (= 1/4: minimum-uncertainty, the Heisenberg floor)"
          % (math.sqrt(vx) * math.sqrt(vp)))


if __name__ == "__main__":
    _demo()
