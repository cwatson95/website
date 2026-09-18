"""
QM-12  Central potentials and the hydrogen atom -- separation in spherical
coordinates, the radial equation with its centrifugal barrier, and the Coulomb
problem solved two ways: a finite-difference eigensolver that recovers the Bohr
spectrum E_n = -1/(2 n^2), and the exact closed-form radial functions R_nl built
from the associated Laguerre polynomials.

Part of the physics topic network (see modules/topic_network.txt, module QM-12).
Builds on ~QM-03 (the time-independent Schrodinger equation), ~QM-10 (the angular
factor Y_l^m: the full orbital is psi = R_nl(r) Y_l^m(theta,phi)), and ~MA-12
(Laguerre / Legendre special functions).  It is the quantum image of the classical
Kepler / central-force problem ~CM-11 (bridge B4, the 1/r potential -- connects
once CM-11 is built), and feeds ~QM-17 (fine structure: relativistic + spin-orbit
corrections to the levels found here) and ~QM-21 (perturbation theory).

ATOMIC (HARTREE) UNITS.  Throughout we set

        hbar = m_e = e = 4 pi eps0 = 1,

so the Bohr radius a0 = 4 pi eps0 hbar^2 / (m_e e^2) = 1 (lengths are in a0) and
energies are in hartrees, 1 Ha = 27.211386 eV.  In these units:
  * the Coulomb potential is simply  V(r) = -1/r,
  * the bound energies are  E_n = -1/(2 n^2)  Ha   (E_1 = -0.5 Ha = -13.6 eV),
  * the ground-state radial function is  R_10(r) = 2 e^{-r},  and  <r>_10 = 3/2.
Multiply any energy by HARTREE_EV to read it in eV.

The story, each a function group below:
  1. Spectrum        -- E_n = -1/(2 n^2): coulomb_energy / coulomb_energy_eV.
  2. Quantum numbers -- (n, l, m) with l = 0..n-1, m = -l..l; the n^2 degeneracy.
  3. Radial equation -- effective_potential (Coulomb + centrifugal barrier) and a
                        finite-difference solver radial_solve(l) that recovers E_n.
  4. Radial functions-- R_nl(r) from the associated Laguerre L_{n-l-1}^{2l+1}
                        (scipy; the alpha>0 generalization of ~MA-12's Laguerre):
                        normalization, the n-l-1 radial nodes, and <r>.

numpy + scipy (scipy.special.eval_genlaguerre for the associated Laguerre, and
scipy.linalg.eigh_tridiagonal for the radial eigenproblem).  Every claim is
checked against a closed form in test_hydrogen.py.

Reference: Griffiths & Schroeter, Introduction to QM, 3rd ed., Sec. 4.1.3 (the
radial equation, p.180), Sec. 4.2 (the hydrogen atom, p.185), Eq. 4.70 (E_n,
p.189), Eqs. 4.87-4.89 (R_nl, p.192).  See ../refs.md for page-verified citations.
"""

import math

import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.special import eval_genlaguerre

__all__ = [
    "HARTREE_EV", "BOHR_RADIUS",
    # 1. spectrum
    "coulomb_energy", "coulomb_energy_eV",
    # 2. quantum numbers and degeneracy
    "allowed_l", "m_values", "degeneracy", "count_states",
    # 3. the radial equation (finite difference)
    "effective_potential", "radial_solve",
    # 4. radial wave functions (associated Laguerre)
    "generalized_laguerre", "radial_wavefunction", "radial_probability",
    "radial_norm", "count_radial_nodes", "expectation_r", "expectation_r_closed",
]

HARTREE_EV = 27.211386245988      # 1 hartree in eV (CODATA 2018); E_1 = -13.6 eV
BOHR_RADIUS = 1.0                 # a0 = 1 in atomic units (the length unit itself)


# --- 1. the Coulomb spectrum -------------------------------------------------

def coulomb_energy(n):
    """Bound-state energy of hydrogen in hartrees:  E_n = -1 / (2 n^2).

    This is the Bohr formula (Griffiths 3e Eq. 4.70, p.189), here in atomic units
    where it loses every constant.  The energy depends ONLY on the principal
    quantum number n = 1, 2, 3, ... -- not on l or m (the n^2-fold degeneracy)."""
    n = int(n)
    if n < 1:
        raise ValueError("principal quantum number n must be a positive integer")
    return -1.0 / (2.0 * n * n)


def coulomb_energy_eV(n):
    """The same level in electron-volts: E_n = -13.606 / n^2 eV (E_1 = -13.6 eV,
    the ionization energy of hydrogen).  Just coulomb_energy(n) * HARTREE_EV."""
    return coulomb_energy(n) * HARTREE_EV


# --- 2. quantum numbers (n, l, m) and the degeneracy -------------------------

def allowed_l(n):
    """The orbital quantum numbers allowed for principal n:  l = 0, 1, ..., n-1.
    The constraint l < n comes from the termination of the radial power series
    (Griffiths 3e p.191): there are exactly n of them."""
    n = int(n)
    if n < 1:
        raise ValueError("n must be a positive integer")
    return list(range(n))


def m_values(l):
    """The magnetic quantum numbers for orbital l:  m = -l, ..., 0, ..., +l
    (2l+1 of them) -- the L_z projections from ~QM-10 (Griffiths Eq. 4.29)."""
    l = int(l)
    if l < 0:
        raise ValueError("l must be a non-negative integer")
    return list(range(-l, l + 1))


def degeneracy(n):
    """Total number of states sharing the energy E_n: the closed form n^2.
    (Counting includes the 2l+1 m-values for each l = 0..n-1; spin would double
    it, but that is ~QM-11 / ~QM-17.)  Griffiths 3e p.191."""
    n = int(n)
    return n * n


def count_states(n):
    """The same degeneracy obtained by *explicit summation*
        sum_{l=0}^{n-1} (2l+1)
    so the test can confirm it equals the closed form n^2 (Griffiths 3e p.191)."""
    return sum(2 * l + 1 for l in allowed_l(n))


# --- 3. the radial equation and its finite-difference solution ---------------

def effective_potential(r, l):
    """The effective radial potential for the Coulomb problem (atomic units):

        V_eff(r) = -1/r  +  l(l+1) / (2 r^2).

    The first term is the attractive Coulomb well V(r) = -1/r; the second is the
    repulsive *centrifugal barrier* l(l+1)/2r^2 that appears for l > 0 and throws
    the particle away from the origin (Griffiths 3e Sec. 4.1.3, p.180).  Writing
    u(r) = r R(r) turns the 3-D radial equation into a 1-D Schrodinger equation
    with this potential."""
    r = np.asarray(r, dtype=float)
    return -1.0 / r + l * (l + 1) / (2.0 * r * r)


def radial_solve(l, n_states=4, r_max=100.0, n_grid=10000):
    """Finite-difference solution of the radial equation for the Coulomb potential.

    With u(r) = r R(r) the radial equation (Griffiths 3e Eq. 4.37/4.53) becomes a
    1-D Schrodinger equation on the half-line, in atomic units

        -(1/2) u''(r) + [ -1/r + l(l+1)/(2 r^2) ] u(r) = E u(r),

    equivalently  u'' = [ l(l+1)/r^2 - 2/r - 2E ] u,  with u(0) = 0 and u -> 0 as
    r -> infinity.  We discretize u on a uniform grid r_i = i*dr, i = 1..n_grid
    (Dirichlet walls u = 0 at r = 0 and at r = r_max), with the 3-point second
    derivative.  The Hamiltonian is symmetric tridiagonal (hbar = m = 1):

        H_ii    =  1/dr^2  +  V_eff(r_i)
        H_i,i+-1 = -1/(2 dr^2)

    and scipy.linalg.eigh_tridiagonal returns the lowest n_states eigenpairs.

    Parameters
    ----------
    l : int            orbital quantum number (>= 0).
    n_states : int     how many lowest eigenstates to return.
    r_max : float      box size in a0 (must exceed the spatial extent ~ n^2 a0).
    n_grid : int       interior grid points (resolution dr = r_max/(n_grid+1)).

    Returns
    -------
    E : (n_states,) ndarray   eigen-energies in hartrees, ascending.  The k-th
        bound state (k = 0, 1, ...) has principal quantum number n = l + 1 + k, so
        these recover E_n = -1/(2 n^2) (E_1 = -0.5 Ha for l=0).
    r : (n_grid,) ndarray      the radial grid.
    U : (n_states, n_grid) ndarray   the normalized radial factors u_n(r) = r R_nl(r)
        (so that int |u|^2 dr = 1; up to an overall sign).
    """
    l = int(l)
    if l < 0:
        raise ValueError("l must be a non-negative integer")
    if n_states < 1:
        raise ValueError("n_states must be >= 1")

    dr = r_max / (n_grid + 1)
    r = dr * np.arange(1, n_grid + 1)              # r = dr, 2dr, ..., n_grid*dr
    Veff = effective_potential(r, l)
    kin = 1.0 / (2.0 * dr * dr)                    # -(1/2) u'' stencil prefactor
    diag = 2.0 * kin + Veff
    off = -kin * np.ones(n_grid - 1)

    n_states = min(n_states, n_grid)
    E, vecs = eigh_tridiagonal(diag, off, select="i",
                               select_range=(0, n_states - 1))
    U = vecs.T.copy()
    for k in range(E.size):                        # L2-normalize: int |u|^2 dr = 1
        U[k] /= np.sqrt(_trapz(U[k] ** 2, r))
    return E, r, U


# --- 4. the closed-form radial wave functions R_nl ---------------------------

def generalized_laguerre(k, alpha, x):
    """The generalized (associated) Laguerre polynomial L_k^{(alpha)}(x), via
    scipy.special.eval_genlaguerre.  This is the alpha > 0 generalization of the
    ordinary Laguerre polynomial L_k = L_k^{(0)} that ~MA-12 builds from its
    recurrence: indeed L_k^{(0)} == MA-12's laguerre(k, .) (verified in the
    tests).  For hydrogen the relevant one is L_{n-l-1}^{(2l+1)} (Griffiths 3e
    Eq. 4.88, p.192)."""
    return eval_genlaguerre(k, alpha, x)


def radial_wavefunction(n, l, r):
    """The normalized hydrogen radial wave function R_nl(r) in atomic units
    (a0 = 1), Griffiths 3e Eq. 4.89, p.192:

        R_nl(r) = sqrt[ (2/n)^3 (n-l-1)! / (2n (n+l)!) ]
                  * e^{-r/n} (2r/n)^l  L_{n-l-1}^{2l+1}(2r/n).

    Requires the integers 0 <= l <= n-1.  Examples: R_10 = 2 e^{-r};
    R_20 = (1/(2 sqrt2))(2 - r) e^{-r/2}.  The full orbital is
    psi_nlm = R_nl(r) Y_l^m(theta, phi) with the angular factor from ~QM-10."""
    n, l = int(n), int(l)
    if not (0 <= l <= n - 1):
        raise ValueError("need integer quantum numbers with 0 <= l <= n-1")
    r = np.asarray(r, dtype=float)
    norm = math.sqrt((2.0 / n) ** 3 * math.factorial(n - l - 1)
                     / (2.0 * n * math.factorial(n + l)))
    rho = 2.0 * r / n
    return norm * np.exp(-r / n) * rho ** l * eval_genlaguerre(n - l - 1, 2 * l + 1, rho)


def radial_probability(n, l, r):
    """The radial probability density  P(r) = r^2 |R_nl(r)|^2, i.e. the
    probability per unit r of finding the electron at radius r (integrating the
    full |psi|^2 over the angles).  int_0^inf P(r) dr = 1.  Its maximum for the
    ground state sits at r = a0 = 1 -- the Bohr radius as the *most probable*
    radius (Griffiths 3e Problem 4.16)."""
    R = radial_wavefunction(n, l, r)
    r = np.asarray(r, dtype=float)
    return r * r * R * R


def _r_grid(n, r_max=None, n_grid=200001):
    """A fine integration grid on (0, r_max]; r_max auto-scales with n (the orbital
    spreads as ~ n^2 a0) so norms and moments converge."""
    if r_max is None:
        r_max = 30.0 * n + 20.0
    return np.linspace(r_max / n_grid, r_max, n_grid)


def _trapz(y, x):
    """Trapezoid integral, tolerant of the numpy trapezoid/trapz rename."""
    f = getattr(np, "trapezoid", None) or np.trapz
    return f(y, x)


def radial_norm(n, l, r_max=None, n_grid=200001):
    """Numerically integrate  int_0^inf |R_nl|^2 r^2 dr  -- must equal 1 (the R_nl
    are normalized, Griffiths 3e Eq. 4.31).  A direct check that the closed-form
    normalization constant in radial_wavefunction is correct."""
    r = _r_grid(n, r_max, n_grid)
    return _trapz(radial_probability(n, l, r), r)


def count_radial_nodes(n, l, r_max=None, n_grid=200001):
    """Count the radial nodes of R_nl -- the interior zeros where R changes sign.
    The result is n - l - 1 (Griffiths 3e p.195): the node count is what visually
    distinguishes orbitals of the same energy.  (The l>0 vanishing at r=0 is a
    boundary, not a node; the (2r/n)^l factor keeps R one-signed near the origin,
    so it is not counted.)"""
    r = _r_grid(n, r_max, n_grid)
    s = np.sign(radial_wavefunction(n, l, r))
    s = s[s != 0]
    return int(np.sum(np.diff(s) != 0))


def expectation_r(n, l, r_max=None, n_grid=400001):
    """The expectation value <r> = int_0^inf r |R_nl|^2 r^2 dr (atomic units, a0).
    For the ground state <r>_10 = 3/2 (Griffiths 3e Problem 4.15a): the electron's
    mean radius is 1.5 Bohr radii, NOT a0 (a0 is the *most probable* radius)."""
    r = _r_grid(n, r_max, n_grid)
    return _trapz(r * radial_probability(n, l, r), r)


def expectation_r_closed(n, l):
    """Closed form for the mean radius (Griffiths 3e Eq. 4.95 region / standard):

        <r>_nl = (1/2) [ 3 n^2 - l(l+1) ]   a0.

    Ground state -> 3/2; it grows like n^2, the quantum echo of the Kepler orbit
    size of ~CM-11.  expectation_r matches this (checked in the tests)."""
    n, l = int(n), int(l)
    return 0.5 * (3 * n * n - l * (l + 1))


# --- demo --------------------------------------------------------------------

def _demo():
    np.set_printoptions(precision=4, suppress=True)
    print("QM-12 Hydrogen atom  (atomic units: hbar = m = e = 4*pi*eps0 = 1)\n")

    print("1. Energy ladder  E_n = -1/(2 n^2):")
    print("   n   E_n [Ha]    E_n [eV]   degeneracy n^2")
    for n in range(1, 6):
        print("   %d  %9.5f  %9.4f        %d"
              % (n, coulomb_energy(n), coulomb_energy_eV(n), degeneracy(n)))
    print("   ground-state (ionization) energy = %.4f eV" % coulomb_energy_eV(1))

    print("\n2. Quantum numbers (n,l,m), l = 0..n-1:")
    for n in range(1, 4):
        ls = allowed_l(n)
        tot = count_states(n)
        print("   n=%d: l in %s   sum(2l+1) = %d = n^2 = %d"
              % (n, ls, tot, degeneracy(n)))

    print("\n3. Radial equation solved by finite difference -> Bohr spectrum:")
    for l in (0, 1, 2):
        E, r, U = radial_solve(l, n_states=3)
        line = "   l=%d:" % l
        for k in range(3):
            n = l + 1 + k
            line += "  n=%d E_fd=%.5f (exact %.5f)" % (n, E[k], coulomb_energy(n))
        print(line)

    print("\n4. Radial wave functions R_nl  (norm, nodes = n-l-1, <r>):")
    print("   state   norm     nodes(n-l-1)   <r>     closed (3n^2-l(l+1))/2")
    for (n, l) in [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2)]:
        print("   R_%d%d   %.5f     %d (%d)        %6.3f   %6.3f"
              % (n, l, radial_norm(n, l), count_radial_nodes(n, l), n - l - 1,
                 expectation_r(n, l), expectation_r_closed(n, l)))

    print("\n   Radial density P(r)=r^2|R_10|^2 peaks at the Bohr radius r=a0=1:")
    r = np.linspace(0.05, 6.0, 25)
    P = radial_probability(1, 0, r)
    rpk = r[np.argmax(P)]
    print("   most probable r ~ %.2f a0   (mean <r> = %.2f a0)"
          % (rpk, expectation_r(1, 0)))


if __name__ == "__main__":
    _demo()
