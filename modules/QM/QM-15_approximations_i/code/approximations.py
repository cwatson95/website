"""
QM-15  Approximation methods I -- the three pillars of time-INDEPENDENT
approximation, as functions you can evaluate and cross-check against exact
diagonalization / exact spectra.

Part of the physics topic network (modules/topic_network.txt, module QM-15).
Prereqs: ~QM-05 (operators, inner products), ~QM-09 (the harmonic oscillator,
used here as the universal test bed). Cross-links: ~MA-21 (asymptotics /
perturbation series -- a PT expansion is an asymptotic series), ~CM-21
(Hamilton-Jacobi / action-angle: WKB is the hbar->0 classical limit, bridge B1,
not yet built), ~QM-08 (1-D tunnelling -- the test file imports its EXACT
rectangular-barrier T to validate the WKB exponent), ~QM-16 (time-dependent PT,
forward), ~QM-18 (Born approximation, forward).

The three pillars, each a function group below:

  1. PERTURBATION THEORY (Griffiths 3e Ch.7).  Split H = H0 + lambda*H'.
       nondegenerate:  E_n^(1) = <n|H'|n>                          (Eq. 7.9)
                       psi_n^(1) = sum_{m!=n} <m|H'|n>/(E_n-E_m) |m> (Eq. 7.13)
                       E_n^(2) = sum_{m!=n} |<m|H'|n>|^2/(E_n-E_m)   (Eq. 7.15)
       degenerate:     the first-order splittings are the EIGENVALUES of H'
                       restricted to the degenerate subspace (the "W" matrix,
                       Eq. 7.30/7.33).
       We check the truncation-error SCALING: 1st order is correct to O(lambda^2),
       through-2nd order to O(lambda^3), vs exact diagonalization of H0+lambda*H'.

  2. VARIATIONAL PRINCIPLE (Griffiths 3e Ch.8).  For ANY normalized trial state,
       <psi|H|psi> >= E_gs                                          (Eq. 8.1).
       Minimizing over a trial family gives an upper bound; a Gaussian on the
       harmonic oscillator hits E_gs exactly (Example 8.1), a Gaussian on the
       quartic well gives a tight bound from above.

  3. WKB APPROXIMATION (Griffiths 3e Ch.9).  Semi-classical wave function
       psi ~ p(x)^{-1/2} exp(+- i/hbar integral p dx),  p = sqrt(2m(E-V)).
       Bound states: Bohr-Sommerfeld quantization (two smooth turning points,
       Eq. 9.50)
           integral_{x1}^{x2} p dx = (n + 1/2) pi hbar,   n = 0,1,2,...
       (equivalently the loop integral  oint p dx = (n+1/2) 2 pi hbar = (n+1/2) h).
       This is EXACT for the harmonic oscillator and asymptotically exact (large
       n) for other wells.  Tunnelling:  T ~ exp(-2 gamma),
           gamma = (1/hbar) integral_{x1}^{x2} |p| dx,  |p| = sqrt(2m(V-E))
       over the classically forbidden region (Eq. 9.22-9.23).

NATURAL UNITS.  Throughout  hbar = m = omega = 1  (kept as module constants
HBAR, MASS so the formulae read dimensionally).  Then the oscillator spectrum is
E_n = n + 1/2 and lengths are in sqrt(hbar/m omega).

numpy does the linear algebra; scipy supplies the integrator, the root finder
and the 1-D minimizer.  Every claim is checked against a closed form or an exact
diagonalization in test_approximations.py.
"""

import math

import numpy as np
from scipy.integrate import quad
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq, minimize_scalar

__all__ = [
    "HBAR", "MASS", "OMEGA",
    # harmonic-oscillator test-bed operators (number basis)
    "ho_energies", "ho_position", "ho_matrix_power",
    # 1. nondegenerate perturbation theory
    "first_order_energy", "second_order_energy", "first_order_correction",
    "perturbed_energy", "exact_energy", "exact_spectrum",
    # 1b. degenerate perturbation theory
    "degenerate_first_order_split",
    # 2. variational principle
    "gaussian_trial", "variational_energy", "gaussian_ho_energy",
    "gaussian_variational_min", "fd_ground_energy", "fd_level",
    # 3. WKB
    "classical_momentum", "action_integral", "bohr_sommerfeld_energy",
    "barrier_action", "tunneling_probability", "tunneling_rectangular",
]

# --- natural units (documented; change at your peril) ------------------------
HBAR = 1.0      # reduced Planck constant
MASS = 1.0      # particle mass
OMEGA = 1.0     # oscillator angular frequency


# =============================================================================
# Harmonic-oscillator test bed (number basis |0>,...,|D-1>)
# =============================================================================
# H0 = hbar*omega*(N + 1/2) is diagonal here with E_n^0 = n + 1/2, and the
# position operator x = sqrt(hbar/2 m omega)(a + a+) is the canonical building
# block for physically meaningful perturbations H' (x, x^2, x^4, ...).  These
# mirror ~QM-09's oscillator.py; we rebuild them locally so QM-15 stands alone.

def ho_energies(D):
    """Unperturbed oscillator energies  E_n^0 = hbar*omega*(n + 1/2),
    n = 0..D-1, as a length-D array (the diagonal of H0 in the number basis)."""
    return HBAR * OMEGA * (np.arange(D) + 0.5)


def ho_position(D):
    """Position operator  x = sqrt(hbar/(2 m omega)) (a + a+)  as a real
    symmetric D x D matrix in the number basis.  Tridiagonal: x[n-1,n] =
    x[n,n-1] = sqrt(hbar/(2 m omega)) * sqrt(n).  In natural units the prefactor
    is 1/sqrt(2)."""
    s = math.sqrt(HBAR / (2.0 * MASS * OMEGA))
    X = np.zeros((D, D))
    for n in range(1, D):
        X[n - 1, n] = X[n, n - 1] = s * math.sqrt(n)
    return X


def ho_matrix_power(D, k):
    """The operator  x^k  as a D x D matrix, x^k = ho_position(D) ** k (matrix
    power).  Use a basis a few levels larger than the states of interest, since
    each factor of x couples |n> to |n+-1> and truncation bites near the top."""
    X = ho_position(D)
    Xk = np.eye(D)
    for _ in range(k):
        Xk = Xk @ X
    return Xk


# =============================================================================
# 1. NONDEGENERATE PERTURBATION THEORY  (Griffiths Ch.7, Sec. 7.1)
# =============================================================================
# Convention: H0 is DIAGONAL with entries E0 (its own eigenbasis -- exactly the
# Griffiths set-up, where the unperturbed eigenstates are the basis).  H' is the
# perturbation matrix `Hp` in that same basis, so <m|H'|n> = Hp[m, n].

def first_order_energy(E0, Hp, n):
    """First-order energy correction  E_n^(1) = <n|H'|n> = Hp[n, n]
    (Griffiths Eq. 7.9, printed p.359 -- "the most frequently used equation in
    quantum mechanics": the shift is just the expectation value of H' in the
    unperturbed state).  Returns a real number (H' hermitian => real diagonal)."""
    return float(np.real(Hp[n, n]))


def second_order_energy(E0, Hp, n):
    """Second-order energy correction (Griffiths Eq. 7.15, printed p.363):

        E_n^(2) = sum_{m != n}  |<m|H'|n>|^2 / (E_n^0 - E_m^0).

    Each term needs a nonzero denominator -- this is exactly where degeneracy
    (E_m^0 = E_n^0) would make ordinary PT blow up and force the degenerate
    treatment below.  Note E_n^(2) <= 0 for the ground state (every denominator
    is negative): level repulsion pushes the ground state DOWN."""
    E0 = np.asarray(E0, dtype=float)
    total = 0.0
    for m in range(len(E0)):
        if m == n:
            continue
        denom = E0[n] - E0[m]
        if abs(denom) < 1e-12:
            raise ZeroDivisionError(
                "degenerate level (E_%d == E_%d): use degenerate PT" % (m, n))
        total += abs(Hp[m, n]) ** 2 / denom
    return float(np.real(total))


def first_order_correction(E0, Hp, n):
    """First-order correction to the state (Griffiths Eq. 7.13, printed p.361):

        |psi_n^(1)> = sum_{m != n}  <m|H'|n> / (E_n^0 - E_m^0)  |m>,

    returned as the length-D coefficient vector (entry n is set to 0, the
    standard normalization choice that drops the |n> component)."""
    E0 = np.asarray(E0, dtype=float)
    D = len(E0)
    c = np.zeros(D, dtype=complex)
    for m in range(D):
        if m == n:
            continue
        denom = E0[n] - E0[m]
        if abs(denom) < 1e-12:
            raise ZeroDivisionError("degenerate level: use degenerate PT")
        c[m] = Hp[m, n] / denom
    return c


def perturbed_energy(E0, Hp, n, lam, order=2):
    """Perturbation-theory estimate of the n-th energy of  H0 + lambda*H':

        order 0:  E_n^0
        order 1:  E_n^0 + lambda E_n^(1)
        order 2:  E_n^0 + lambda E_n^(1) + lambda^2 E_n^(2)

    Compare to exact_energy(...) to see the O(lambda^2) / O(lambda^3) accuracy."""
    E0 = np.asarray(E0, dtype=float)
    E = E0[n]
    if order >= 1:
        E += lam * first_order_energy(E0, Hp, n)
    if order >= 2:
        E += lam ** 2 * second_order_energy(E0, Hp, n)
    return float(E)


def exact_spectrum(E0, Hp, lam):
    """Exact eigenvalues of  H = diag(E0) + lambda*H', ascending (machine
    precision via numpy).  This is the 'truth' the PT formulas approximate."""
    H = np.diag(np.asarray(E0, dtype=float)).astype(complex) + lam * np.asarray(Hp)
    return np.sort(np.linalg.eigvalsh(H))


def exact_energy(E0, Hp, n, lam):
    """The n-th exact eigenvalue of  diag(E0) + lambda*H'  (levels sorted
    ascending, indexed by n).  Valid as the PT reference as long as lambda is
    small enough that levels have not crossed -- the regime where PT applies."""
    return float(exact_spectrum(E0, Hp, lam)[n])


# =============================================================================
# 1b. DEGENERATE PERTURBATION THEORY  (Griffiths Sec. 7.2)
# =============================================================================

def degenerate_first_order_split(Hp, indices):
    """First-order energies of a degenerate level (Griffiths Eq. 7.30/7.33,
    printed p.370).

    When a set of unperturbed states share an energy E^0, ordinary PT fails
    (zero denominators).  The fix: the first-order corrections are the
    EIGENVALUES of the perturbation restricted to that degenerate subspace --
    the "W matrix"  W_ij = <i|H'|j>  with i, j running over `indices`.  Its
    eigenvalues are the splittings; its eigenvectors are the "good" states.

    Parameters
    ----------
    Hp : (D, D) array      full perturbation matrix in the unperturbed basis.
    indices : sequence     the rows/cols spanning the degenerate subspace.

    Returns the splittings (eigenvalues of W), ascending.
    """
    idx = np.asarray(indices, dtype=int)
    W = np.asarray(Hp)[np.ix_(idx, idx)]
    return np.sort(np.linalg.eigvalsh(W))


# =============================================================================
# 2. THE VARIATIONAL PRINCIPLE  (Griffiths Ch.8)
# =============================================================================
# <H>_psi >= E_gs for ANY normalized trial psi (Eq. 8.1, p.418).  The Rayleigh
# quotient <psi|H|psi>/<psi|psi> upper-bounds the ground-state energy; minimizing
# over a family of trial states gives the best (lowest) bound the family allows.

def gaussian_trial(b, x):
    """Normalized Gaussian trial wave function  psi_b(x) = (2b/pi)^{1/4} e^{-b x^2}
    (Griffiths Example 8.1 uses exactly this family).  b > 0 is the width
    parameter; large b = narrow."""
    return (2.0 * b / math.pi) ** 0.25 * np.exp(-b * np.asarray(x, dtype=float) ** 2)


def variational_energy(psi, x, V):
    """Rayleigh quotient  <psi|H|psi> / <psi|psi>  on a grid, with

        <T> = (hbar^2/2m) integral |psi'|^2 dx        (>= 0, by parts)
        <V> = integral V |psi|^2 dx

    for real `psi` sampled on the uniform grid `x`, potential array `V`.  By the
    variational principle this is an UPPER BOUND on the ground-state energy
    (Griffiths Eq. 8.1).  The |psi'|^2 form of <T> (rather than -psi*psi'') is
    positive by construction and numerically gentler."""
    x = np.asarray(x, dtype=float)
    psi = np.asarray(psi, dtype=float)
    V = np.asarray(V, dtype=float)
    norm = np.trapezoid(psi ** 2, x)
    dpsi = np.gradient(psi, x)
    T = HBAR ** 2 / (2.0 * MASS) * np.trapezoid(dpsi ** 2, x)
    Vexp = np.trapezoid(V * psi ** 2, x)
    return float((T + Vexp) / norm)


def gaussian_ho_energy(b):
    """Closed-form <H> for the Gaussian trial on the oscillator V = 1/2 m w^2 x^2
    (Griffiths Eq. 8.4-8.7).  In natural units

        <H>(b) = <T> + <V> = b/2 + 1/(8b),

    minimized at b = m w/(2 hbar) = 1/2 giving <H> = 1/2 hbar w = E_0 EXACTLY --
    because the trial family happens to contain the true ground state."""
    return HBAR ** 2 * b / (2.0 * MASS) + MASS * OMEGA ** 2 / (8.0 * b)


def gaussian_variational_min(V, x, b_bracket=(0.05, 0.5, 5.0)):
    """Minimize the Gaussian Rayleigh quotient over the width b for an arbitrary
    potential `V` (callable V(x) or array on `x`).  Returns (E_min, b_opt): the
    tightest variational upper bound the Gaussian family gives, and where."""
    x = np.asarray(x, dtype=float)
    Varr = V(x) if callable(V) else np.asarray(V, dtype=float)

    def f(b):
        if b <= 0:
            return np.inf
        return variational_energy(gaussian_trial(b, x), x, Varr)

    res = minimize_scalar(f, bracket=b_bracket)
    return float(res.fun), float(res.x)


def fd_ground_energy(V, x):
    """Exact (finite-difference) ground-state energy of -hbar^2/2m d^2/dx^2 + V
    on grid `x` -- the 'truth' the variational bound must lie ABOVE.  `V` is a
    callable or an array on `x`."""
    return fd_level(V, x, 0)


def fd_level(V, x, n):
    """The n-th finite-difference eigenenergy on grid `x` (Dirichlet box), for a
    callable or array potential `V`.  3-point Laplacian stencil; converges to the
    true spectrum as the grid refines.  Used as the exact reference for both the
    variational bound and the WKB spectra."""
    x = np.asarray(x, dtype=float)
    Varr = V(x) if callable(V) else np.asarray(V, dtype=float)
    dx = x[1] - x[0]
    kin = HBAR ** 2 / (2.0 * MASS * dx ** 2)
    diag = 2.0 * kin + Varr[1:-1]
    off = -kin * np.ones(len(x) - 3)
    ev = eigh_tridiagonal(diag, off, select="i", select_range=(n, n))[0]
    return float(ev[0])


# =============================================================================
# 3. THE WKB APPROXIMATION  (Griffiths Ch.9)
# =============================================================================

def classical_momentum(E, V):
    """Classical momentum magnitude  p(x) = sqrt(2 m (E - V))  (Griffiths Eq. 9.2,
    p.450).  Real in the classically allowed region E > V; we return
    sqrt(2 m max(E - V, 0)) so it is 0 (not NaN) in the forbidden region -- which
    lets the action integral run over a fixed interval without locating turning
    points by hand."""
    return np.sqrt(2.0 * MASS * np.maximum(E - np.asarray(V, dtype=float), 0.0))


def action_integral(V, E, x_lo, x_hi):
    """The classical action  integral_{x1}^{x2} p(x) dx  between the turning
    points, computed as  integral_{x_lo}^{x_hi} sqrt(2 m max(E - V, 0)) dx  over
    any bracket [x_lo, x_hi] that CONTAINS the classically allowed region (the
    max() zeroes the integrand outside it, so the turning points need not be
    found explicitly).  `V` is a callable V(x)."""
    integrand = lambda x: math.sqrt(2.0 * MASS * max(E - V(x), 0.0))
    val, _ = quad(integrand, x_lo, x_hi, limit=400)
    return val


def bohr_sommerfeld_energy(V, n, x_lo, x_hi, gamma=0.5, E_lo=1e-9, E_hi=1e4):
    """Bohr-Sommerfeld / WKB quantized energy: solve

        integral_{x1}^{x2} p(x) dx = (n + gamma) * pi * hbar

    for E (Griffiths Eq. 9.50, p.465).  The constant `gamma` encodes the turning
    points (the connection formulas):
        gamma = 1/2  -> two smooth turning points  (the generic well; Eq. 9.50),
        gamma = 3/4  -> one vertical wall + one smooth turn (Eq. 9.48),
        gamma = 1    -> two vertical walls         (Eq. 9.17).
    n = 0, 1, 2, ... labels the level.  The action is monotonically increasing in
    E, so a bracketed root exists and is unique.  Returns the WKB energy E_n.

    Exact for the harmonic oscillator (gamma = 1/2); asymptotically exact (large
    n) otherwise."""
    target = (n + gamma) * math.pi * HBAR
    f = lambda E: action_integral(V, E, x_lo, x_hi) - target
    return brentq(f, E_lo, E_hi, xtol=1e-10, rtol=1e-12)


def barrier_action(V, E, x_lo, x_hi):
    """The tunnelling exponent's integral  gamma = (1/hbar) integral |p| dx  over
    the classically FORBIDDEN region (Griffiths Eq. 9.23, p.456):

        gamma = (1/hbar) integral_{x1}^{x2} sqrt(2 m (V - E)) dx,

    here computed as (1/hbar) integral_{x_lo}^{x_hi} sqrt(2 m max(V - E, 0)) dx
    over a bracket spanning the barrier (max() zeroes it where V < E)."""
    integrand = lambda x: math.sqrt(2.0 * MASS * max(V(x) - E, 0.0))
    val, _ = quad(integrand, x_lo, x_hi, limit=400)
    return val / HBAR


def tunneling_probability(V, E, x_lo, x_hi):
    """WKB transmission probability through a barrier (Griffiths Eq. 9.22):

        T ~ exp(-2 gamma),   gamma = barrier_action(V, E, ...).

    Captures the dominant exponential suppression; it omits the O(1) prefactor
    that the exact matching supplies (the test compares this to ~QM-08's exact
    rectangular-barrier T and shows they share the SAME exponent)."""
    return math.exp(-2.0 * barrier_action(V, E, x_lo, x_hi))


def tunneling_rectangular(E, V0, a):
    """Closed-form WKB transmission for a rectangular barrier of height V0 > E,
    width a:  the forbidden-region momentum is constant, |p| = sqrt(2m(V0-E)), so

        gamma = kappa a,  kappa = sqrt(2 m (V0 - E))/hbar,   T_WKB = exp(-2 kappa a).

    This is the WKB analogue of ~QM-08's exact transmission_barrier; both decay
    as exp(-2 kappa a), differing only by an O(1) prefactor (validated in the
    tests)."""
    kappa = math.sqrt(2.0 * MASS * (V0 - E)) / HBAR
    return math.exp(-2.0 * kappa * a)


# =============================================================================
# demo
# =============================================================================

def _demo():
    print("QM-15  Approximation methods I  (hbar = m = omega = 1)\n")

    # ---- 1. nondegenerate PT: anharmonic x^2 perturbation of the oscillator --
    D = 40
    E0 = ho_energies(D)
    Hp = ho_matrix_power(D, 2)               # H' = x^2
    print("1. NONDEGENERATE PT   H = H0 + lambda x^2  (test bed: oscillator)")
    print("   E_n^(1) = <n|x^2|n>  (should be n+1/2):",
          [round(first_order_energy(E0, Hp, n), 4) for n in range(4)])
    print("   E_n^(2)              (should be -(n+1/2)/2):",
          [round(second_order_energy(E0, Hp, n), 4) for n in range(4)])
    print("   accuracy vs exact diagonalization, ground state:")
    print("     lambda   |E0+lE1 - exact|    |E0+lE1+l^2E2 - exact|")
    prev1 = prev2 = None
    for lam in (0.1, 0.05, 0.025):
        ex = exact_energy(E0, Hp, 0, lam)
        e1 = abs(perturbed_energy(E0, Hp, 0, lam, order=1) - ex)
        e2 = abs(perturbed_energy(E0, Hp, 0, lam, order=2) - ex)
        r1 = "" if prev1 is None else "  (x%.1f)" % (prev1 / e1)
        r2 = "" if prev2 is None else "  (x%.1f)" % (prev2 / e2)
        print("     %.3f    %.3e%s        %.3e%s" % (lam, e1, r1, e2, r2))
        prev1, prev2 = e1, e2
    print("     -> 1st-order error /4 each halving (O(l^2)); through-2nd /8 (O(l^3)).")

    # ---- 1b. degenerate PT ---------------------------------------------------
    print("\n1b. DEGENERATE PT   two-fold degenerate level, H' lifts it")
    E0d = np.array([2.0, 2.0, 5.0, 9.0])
    Hpd = np.array([[0.3, 0.4, 0.1, 0.0],
                    [0.4, -0.2, 0.0, 0.2],
                    [0.1, 0.0, 1.0, 0.0],
                    [0.0, 0.2, 0.0, 2.0]])
    split = degenerate_first_order_split(Hpd, [0, 1])
    lam = 1e-5
    ex = exact_spectrum(E0d, Hpd, lam)[:2]
    print("   W-eigenvalues (subspace H'):      ", np.round(split, 5))
    print("   (exact split)/lambda  (lam->0):   ", np.round(np.sort((ex - 2.0) / lam), 5))
    print("   naive diagonal {H'_00, H'_11}:    ", np.round(np.sort([Hpd[0, 0], Hpd[1, 1]]), 5),
          " <- WRONG (must diagonalize the block)")

    # ---- 2. variational ------------------------------------------------------
    print("\n2. VARIATIONAL PRINCIPLE   <H> >= E_gs for any trial state")
    x = np.linspace(-12.0, 12.0, 6001)
    Emin_ho, b_ho = gaussian_variational_min(lambda t: 0.5 * t ** 2, x)
    print("   oscillator  V=x^2/2 : Gaussian min <H> = %.6f at b = %.4f  (exact 0.5)"
          % (Emin_ho, b_ho))
    Emin_q, b_q = gaussian_variational_min(lambda t: 0.25 * t ** 4, x)
    Egs_q = fd_ground_energy(lambda t: 0.25 * t ** 4, np.linspace(-8, 8, 2000))
    print("   quartic     V=x^4/4 : Gaussian min <H> = %.5f  >=  exact E_gs = %.5f  (bound holds: %s)"
          % (Emin_q, Egs_q, Emin_q >= Egs_q))

    # ---- 3. WKB --------------------------------------------------------------
    print("\n3. WKB APPROXIMATION")
    print("   Bohr-Sommerfeld (n+1/2)pi*hbar, oscillator  ->  E_n = n+1/2 EXACTLY:")
    for n in range(4):
        E = bohr_sommerfeld_energy(lambda t: 0.5 * t ** 2, n, -60, 60)
        print("     n=%d : WKB %.6f   exact %.1f" % (n, E, n + 0.5))
    print("   quartic V=x^4/4: WKB approaches exact as n grows (semiclassical):")
    xfd = np.linspace(-8, 8, 2500)
    for n in range(4):
        E = bohr_sommerfeld_energy(lambda t: 0.25 * t ** 4, n, -30, 30)
        Ef = fd_level(lambda t: 0.25 * t ** 4, xfd, n)
        print("     n=%d : WKB %.4f   exact %.4f   (%.2f%%)"
              % (n, E, Ef, 100 * abs(E - Ef) / Ef))
    print("   tunnelling through a rectangular barrier (V0=10, E=2):")
    print("     width a :  T_WKB = exp(-2 kappa a)")
    for a in (1.0, 2.0, 3.0, 5.0):
        print("      %4.1f   :  %.3e" % (a, tunneling_rectangular(2.0, 10.0, a)))
    print("     -> same exponential exp(-2 kappa a) as ~QM-08's exact T (see tests).")


if __name__ == "__main__":
    _demo()
