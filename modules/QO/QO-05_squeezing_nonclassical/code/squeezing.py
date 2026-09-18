"""QO-05  Squeezing & nonclassical light -- squeezed & entangled photons.

Physics topic network, module QO-05 (modules/topic_network.txt).  Source:
Scully & Zubairy, *Quantum Optics* (Cambridge, 1997):
  * Ch. 2 (coherent & squeezed states): quadratures, the squeeze operator
    S(xi) and its quadrature variances -- Sects. 2.5-2.8, esp. 2.7-2.7.1;
  * Sect. 4.4.4: photon antibunching, Poissonian & sub-Poissonian light
    (the g^(2)(0) and Mandel-Q nonclassicality tests);
  * Ch. 16 (squeezing via nonlinear optics): degenerate parametric
    amplification, the chi^(2) source of squeezed light (-> ~QO-06);
  * Ch. 18 (EPR, hidden variables, Bell): the two-mode/EPR correlations (-> ~QM-21).
Builds on ~QO-01 (coherent/Fock states) and the ~QM-09 ladder operators a, a+.

------------------------------------------------------------------------------
The single-mode field is one harmonic oscillator (~QM-09).  Split it into two
Hermitian QUADRATURES (hbar = 1 throughout)

    X1 = (a + a+)/2 ,   X2 = (a - a+)/(2i) ,   [X1, X2] = i/2 ,

so the Heisenberg bound is  Var X1 * Var X2 >= 1/16.  Vacuum and coherent states
sit AT the bound with Var X1 = Var X2 = 1/4 -- the standard quantum limit (SQL).

The SQUEEZE operator (xi = r e^{i phi})

    S(xi) = exp[ (1/2)( xi* a^2 - xi a+^2 ) ] ,    S+(xi) a S(xi) = a cosh r - a+ e^{i phi} sinh r,

drives the squeezed vacuum |xi> = S(xi)|0>.  For phi = 0 it deflates one
quadrature and inflates the other while staying on the bound:

    Var X1 = (1/4) e^{-2r} ,   Var X2 = (1/4) e^{+2r} ,   product = 1/16.

One quadrature is pushed BELOW the vacuum fluctuation 1/4 (the resource for
sub-SQL interferometry) at the unavoidable cost of the conjugate one.

Nonclassicality wears several faces.  The squeezed vacuum is built from PAIRS of
photons, so it contains ONLY EVEN photon numbers, with mean <n> = sinh^2 r; yet
its photon statistics are super-Poissonian (g^(2)(0) > 1).  Sub-Poissonian /
antibunched light (g^(2)(0) < 1, Mandel Q < 0) -- e.g. a Fock state -- is a
DIFFERENT nonclassical signature.  Two-mode squeezing S2 = exp(xi* a b - xi a+ b+)
entangles two modes into the EPR state sech r * sum_n tanh^n r |n,n>, with
photon-number-correlated, sub-SQL joint quadratures (-> ~QM-21).

Truncated Fock basis: a, a+ are N x N (default N = 80).  S(xi) = expm(M) with M
anti-Hermitian is unitary to machine precision; the *physics* is faithful only if
the true state's population above level N is negligible -- since the squeezed
vacuum lives on even photons up to ~ a few * sinh^2 r, N must be large enough
(N = 80 covers r <~ 1.3 here).  expm does the work; numpy the linear algebra.
"""

import numpy as np
from scipy.linalg import expm

__all__ = [
    "DEFAULT_N", "TWO_MODE_N",
    # operators & basis states
    "annihilation", "creation", "quadrature_operators",
    "vacuum_state", "fock_state", "coherent_state",
    # single-mode squeezing
    "squeeze_operator", "squeezed_vacuum",
    "quadrature_variances", "photon_distribution",
    "mean_photon", "mean_photon_number",
    # photon-statistics nonclassicality tests
    "g2_zero", "mandel_q",
    # two-mode squeezing & EPR
    "two_mode_squeeze_operator", "two_mode_squeezed_vacuum",
    "two_mode_photon_distribution", "epr_variances",
]

DEFAULT_N = 80      # single-mode Fock truncation (even photons up to ~ N)
TWO_MODE_N = 16     # per-mode truncation for two-mode work (N^2 = 256 states)


# --- ladder operators & quadratures (the ~QM-09 algebra) ---------------------

def annihilation(N=DEFAULT_N):
    """Annihilation operator a as an N x N matrix in the Fock basis {|0>,...,|N-1>}:
    a|n> = sqrt(n)|n-1>, so a has the single superdiagonal sqrt(1),...,sqrt(N-1)."""
    return np.diag(np.sqrt(np.arange(1, N, dtype=float)), k=1).astype(complex)


def creation(N=DEFAULT_N):
    """Creation operator a+ = a^dagger (the Hermitian conjugate of `annihilation`):
    a+|n> = sqrt(n+1)|n+1>."""
    return annihilation(N).conj().T


def quadrature_operators(N=DEFAULT_N):
    """The two field quadratures (Scully-Zubairy Sect. 2.7.1)

        X1 = (a + a+)/2 ,    X2 = (a - a+)/(2i) ,

    Hermitian, with [X1, X2] = i/2 so that Var X1 * Var X2 >= 1/16.  Returns
    (X1, X2) as N x N matrices."""
    a = annihilation(N)
    ad = a.conj().T
    X1 = 0.5 * (a + ad)
    X2 = (a - ad) / 2.0j
    return X1, X2


# --- reference states --------------------------------------------------------

def vacuum_state(N=DEFAULT_N):
    """The vacuum |0> as a length-N column (1 in slot 0)."""
    psi = np.zeros(N, dtype=complex)
    psi[0] = 1.0
    return psi


def fock_state(n, N=DEFAULT_N):
    """Number (Fock) state |n> as a length-N column."""
    psi = np.zeros(N, dtype=complex)
    psi[n] = 1.0
    return psi


def coherent_state(alpha, N=DEFAULT_N):
    """Coherent state |alpha> = e^{-|alpha|^2/2} sum_n alpha^n/sqrt(n!) |n>
    (~QO-01), built by the stable recurrence c_n = c_{n-1} * alpha/sqrt(n).
    Poissonian photon statistics: g^(2)(0) = 1, Mandel Q = 0."""
    c = np.zeros(N, dtype=complex)
    c[0] = np.exp(-0.5 * abs(alpha) ** 2)
    for n in range(1, N):
        c[n] = c[n - 1] * alpha / np.sqrt(n)
    return c


# --- single-mode squeezing (Scully-Zubairy Sect. 2.7) ------------------------

def squeeze_operator(r, N=DEFAULT_N, phi=0.0):
    """Single-mode squeeze operator (Scully-Zubairy Eq. 2.7.1)

        S(xi) = exp[ (1/2)( xi* a^2 - xi a+^2 ) ] ,    xi = r e^{i phi},

    realised as the matrix exponential of the anti-Hermitian generator
    M = (1/2)(xi* a^2 - xi a+^2).  expm(M) is unitary to machine precision.
    For phi = 0 it squeezes X1 (deflates Var X1, inflates Var X2)."""
    xi = r * np.exp(1j * phi)
    a2 = annihilation(N) @ annihilation(N)          # a^2
    ad2 = a2.conj().T                               # (a+)^2
    M = 0.5 * (np.conj(xi) * a2 - xi * ad2)
    return expm(M)


def squeezed_vacuum(r, N=DEFAULT_N, phi=0.0):
    """Squeezed vacuum |xi> = S(xi)|0> (Scully-Zubairy Sect. 2.7).  Contains only
    even photon numbers, with <n> = sinh^2 r; r = 0 returns the bare vacuum."""
    return squeeze_operator(r, N, phi) @ vacuum_state(N)


def quadrature_variances(state):
    """Return (Var X1, Var X2) for a state vector in the Fock basis, with
    X1 = (a+a+)/2, X2 = (a-a+)/2i.  For the squeezed vacuum (phi = 0) these are
    (1/4) e^{-2r} and (1/4) e^{+2r}; for vacuum/coherent both equal 1/4 (SQL)."""
    N = len(state)
    X1, X2 = quadrature_operators(N)
    bra = state.conj()

    def _var(X):
        mean = bra @ (X @ state)
        mean2 = bra @ (X @ (X @ state))
        return float((mean2 - mean * mean).real)

    return _var(X1), _var(X2)


def photon_distribution(state):
    """Photon-number distribution P(n) = |<n|state>|^2 (length-N real array)."""
    return np.abs(state) ** 2


def mean_photon(r):
    """Closed-form mean photon number of the squeezed vacuum, <n> = sinh^2 r
    (Scully-Zubairy Sect. 2.7)."""
    return float(np.sinh(r) ** 2)


def mean_photon_number(state):
    """Numerical mean photon number <n> = sum_n n P(n) for a Fock-basis state."""
    n = np.arange(len(state))
    return float(np.sum(n * np.abs(state) ** 2))


# --- photon-statistics nonclassicality (Scully-Zubairy Sect. 4.4.4) ----------

def g2_zero(state):
    """Zero-delay second-order coherence

        g^(2)(0) = <a+ a+ a a> / <a+ a>^2 = <n(n-1)> / <n>^2 .

    g^(2)(0) < 1 is sub-Poissonian / antibunched (nonclassical: Fock |1> gives 0);
    = 1 is coherent (Poissonian); > 1 is bunched/super-Poissonian -- the squeezed
    vacuum has g^(2)(0) = 3 + 1/sinh^2 r > 1 despite being highly nonclassical."""
    N = len(state)
    a = annihilation(N)
    ad = a.conj().T
    bra = state.conj()
    n_mean = (bra @ (ad @ (a @ state))).real
    if n_mean <= 1e-15:
        return float("nan")
    g2_num = (bra @ (ad @ (ad @ (a @ (a @ state))))).real
    return float(g2_num / n_mean ** 2)


def mandel_q(state):
    """Mandel Q = (Var n - <n>)/<n> = <n>(g^(2)(0) - 1).  Q < 0 sub-Poissonian
    (nonclassical), Q = 0 coherent, Q > 0 super-Poissonian."""
    N = len(state)
    a = annihilation(N)
    ad = a.conj().T
    n_op = ad @ a
    bra = state.conj()
    n_mean = (bra @ (n_op @ state)).real
    if n_mean <= 1e-15:
        return float("nan")
    n2 = (bra @ (n_op @ (n_op @ state))).real
    return float((n2 - n_mean ** 2 - n_mean) / n_mean)


# --- two-mode squeezing & EPR entanglement (Scully-Zubairy Ch. 16, 18) -------

def two_mode_squeeze_operator(r, N=TWO_MODE_N, phi=0.0):
    """Two-mode squeeze operator (the degenerate-down-conversion generator,
    Scully-Zubairy Ch. 16)

        S2(xi) = exp( xi* a b - xi a+ b+ ) ,    xi = r e^{i phi},

    on the N^2-dimensional product space (mode a (x) mode b), with
    a -> kron(a, I), b -> kron(I, a)."""
    a = annihilation(N)
    I = np.eye(N, dtype=complex)
    A = np.kron(a, I)               # mode-a annihilation
    B = np.kron(I, a)               # mode-b annihilation
    xi = r * np.exp(1j * phi)
    M = np.conj(xi) * (A @ B) - xi * (A.conj().T @ B.conj().T)
    return expm(M)


def two_mode_squeezed_vacuum(r, N=TWO_MODE_N, phi=0.0):
    """Two-mode squeezed vacuum |TMSV> = S2(xi)|0,0>
        = sech r * sum_n (-e^{i phi} tanh r)^n |n, n>   (Scully-Zubairy Ch. 16).
    Perfectly photon-number-correlated; the canonical EPR/entangled-photon state
    of ~QM-21, produced by parametric down-conversion (~QO-06)."""
    S2 = two_mode_squeeze_operator(r, N, phi)
    vac = np.kron(vacuum_state(N), vacuum_state(N))
    return S2 @ vac


def two_mode_photon_distribution(state, N=TWO_MODE_N):
    """Joint distribution P(n_a, n_b) = |<n_a, n_b|state>|^2 as an N x N array.
    For the TMSV it is diagonal (n_a = n_b always)."""
    return (np.abs(state) ** 2).reshape(N, N)


def epr_variances(r, N=TWO_MODE_N, phi=0.0):
    """EPR joint-quadrature variances of the two-mode squeezed vacuum:

        Var(X_a + X_b)  and  Var(Y_a - Y_b),

    with X = (c+c+)/2, Y = (c-c+)/2i for each mode.  Both equal (1/2) e^{-2r},
    falling BELOW the separable / vacuum bound 1/2 -- the continuous-variable EPR
    correlation (-> ~QM-21).  Returns (Var(X_a+X_b), Var(Y_a-Y_b))."""
    a = annihilation(N)
    I = np.eye(N, dtype=complex)
    A = np.kron(a, I)
    B = np.kron(I, a)
    Ad, Bd = A.conj().T, B.conj().T
    Xa, Xb = 0.5 * (A + Ad), 0.5 * (B + Bd)
    Ya, Yb = (A - Ad) / 2.0j, (B - Bd) / 2.0j
    psi = two_mode_squeezed_vacuum(r, N, phi)
    bra = psi.conj()

    def _var(O):
        mean = bra @ (O @ psi)
        mean2 = bra @ (O @ (O @ psi))
        return float((mean2 - mean * mean).real)

    return _var(Xa + Xb), _var(Ya - Yb)


# --- demo --------------------------------------------------------------------

def _demo():
    print("QO-05  Squeezing & nonclassical light  (hbar = 1)")
    print("=" * 60)

    print("\nVacuum / SQL:  Var X1, Var X2 (squeezed vacuum r, phi=0)")
    print("   r     Var X1=1/4 e^-2r   Var X2=1/4 e^+2r   product    <n>=sinh^2 r")
    for r in (0.0, 0.3, 0.6, 1.0, 1.2):
        sv = squeezed_vacuum(r)
        v1, v2 = quadrature_variances(sv)
        nbar = mean_photon_number(sv)
        print("  %.1f   %12.6f      %12.6f   %9.6f   %.6f  (exact %.6f)"
              % (r, v1, v2, v1 * v2, nbar, mean_photon(r)))
    print("   -> one quadrature dives below the vacuum 1/4; product pinned at 1/16.")

    print("\nOnly even photons populated (squeezed vacuum, r = 0.8):")
    P = photon_distribution(squeezed_vacuum(0.8))
    print("   P(0..6) =", np.round(P[:7], 5))
    print("   sum of ODD-n probabilities = %.2e  (-> 0: photons come in pairs)"
          % P[1::2].sum())

    print("\nNonclassicality faces -- g^(2)(0) and Mandel Q:")
    print("   Fock |1>        : g2(0) = %.3f , Q = %+.3f   (antibunched, sub-Poissonian)"
          % (g2_zero(fock_state(1)), mandel_q(fock_state(1))))
    print("   coherent |a=2>  : g2(0) = %.3f , Q = %+.3f   (Poissonian / classical)"
          % (g2_zero(coherent_state(2.0)), mandel_q(coherent_state(2.0))))
    sv = squeezed_vacuum(0.8)
    print("   squeezed vac r=.8: g2(0) = %.3f , Q = %+.3f   (super-Poissonian: 3+1/sinh^2 r = %.3f)"
          % (g2_zero(sv), mandel_q(sv), 3.0 + 1.0 / np.sinh(0.8) ** 2))

    print("\nTwo-mode squeezing & EPR (per-mode <n>, joint-quadrature variances):")
    for r in (0.3, 0.6, 0.9):
        tmsv = two_mode_squeezed_vacuum(r)
        Pab = two_mode_photon_distribution(tmsv)
        na = float(np.sum(np.arange(Pab.shape[0])[:, None] * Pab))
        vx, vy = epr_variances(r)
        print("   r=%.1f : <n_a>=%.4f (=sinh^2 r=%.4f) ; Var(Xa+Xb)=Var(Ya-Yb)=%.5f"
              "  (< SQL 0.5 = 1/2 e^-2r=%.5f)"
              % (r, na, np.sinh(r) ** 2, vx, 0.5 * np.exp(-2 * r)))
    print("   -> photon-number correlated |n,n>, sub-SQL EPR quadratures (~QM-21).")


if __name__ == "__main__":
    _demo()
