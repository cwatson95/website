"""
QM-08  One-dimensional problems -- wells, step & barrier, tunnelling.

The canonical solvable 1-D potentials of introductory QM, as functions you can
evaluate and cross-check.  Part of the physics topic network
(see modules/topic_network.txt, module QM-08).  Prereqs: ~QM-03 (these all solve
the time-independent Schrodinger equation, TISE); cross-links ~MA-09 (Fourier /
wave packets), ~MA-08 (PDEs), ~QM-09 (the harmonic well, next), ~QM-15 (WKB
tunnelling).

The five clusters, each a function group below:
  1. Bound states of an arbitrary well -- a finite-difference TISE eigensolver
     `bound_states(V, x)` that recovers the infinite-square-well ladder
     E_n = n^2 pi^2 hbar^2 / (2 m L^2) and the finite-well bound-state count.
  2. The delta-function well       -- exactly one bound state, E = -m alpha^2 / 2hbar^2.
  3. Free particle / wave packets  -- dispersion omega(k)=hbar k^2/2m, group vs
     phase velocity, and the spreading of a Gaussian packet.
  4. The rectangular barrier       -- transmission T(E): tunnelling for E<V0,
     oscillatory resonances for E>V0 (analytic AND transfer-matrix).
  5. The step potential            -- reflection R and transmission T with
     R+T = 1, weighted by probability current.

NATURAL UNITS.  Throughout we set  hbar = m = 1  (both stored as module constants
HBAR, MASS so the formulae read dimensionally).  In these units the infinite well
of width L has E_n = n^2 pi^2 / (2 L^2); restore SI by multiplying energies by
hbar^2/m and lengths as written.

Uses numpy for linear algebra and scipy's symmetric-tridiagonal eigensolver; every
result is checked against a closed form in test_one_dim.py.
"""

import numpy as np
from scipy.linalg import eigh_tridiagonal

__all__ = [
    "HBAR", "MASS",
    # bound states / wells
    "bound_states", "infinite_well_energy", "finite_square_well_bound_count",
    "delta_well_energy",
    # scattering
    "transmission_barrier", "reflection_barrier", "step_RT", "scatter_piecewise",
    # free particle / wave packets
    "free_particle_omega", "phase_velocity", "group_velocity",
    "gaussian_packet_sigma",
]

HBAR = 1.0      # reduced Planck constant   (natural units)
MASS = 1.0      # particle mass             (natural units)


def _trapz(y, x):
    """Trapezoid integral, tolerant of numpy version (trapezoid vs trapz)."""
    f = getattr(np, "trapezoid", None) or np.trapz
    return f(y, x)


# --- 1. bound states of an arbitrary 1-D potential ---------------------------

def bound_states(V, x, n_states=None):
    """Finite-difference eigensolver for the time-independent Schrodinger equation

        -(hbar^2 / 2m) psi'' + V(x) psi = E psi

    on the grid `x` (uniform spacing) with the potential sampled as the array `V`.
    Dirichlet walls (psi = 0) are imposed at the two endpoints, so the grid must
    extend far enough that any bound state has decayed to ~0 there.

    The second derivative is the standard 3-point stencil, giving a symmetric
    tridiagonal Hamiltonian on the interior points:

        H_ii   =  hbar^2 / (m dx^2) + V_i
        H_i,i+-1 = -hbar^2 / (2 m dx^2)

    Parameters
    ----------
    V : array_like   potential values V(x_i), same length as x.
    x : array_like   uniform grid (1-D, increasing).
    n_states : int or None
        If given, return only the lowest n_states eigenpairs (cheaper).

    Returns
    -------
    E   : (k,) ndarray   eigen-energies, ascending.
    psi : (k, N) ndarray  normalized eigenfunctions on the FULL grid `x`
          (so int |psi_n|^2 dx = 1; endpoints are exactly 0).
    """
    V = np.asarray(V, dtype=float)
    x = np.asarray(x, dtype=float)
    N = x.size
    if N < 3:
        raise ValueError("need at least 3 grid points")
    dx = (x[-1] - x[0]) / (N - 1)

    Vi = V[1:-1]                                          # interior potential
    diag = HBAR**2 / (MASS * dx**2) + Vi                  # main diagonal
    off = -HBAR**2 / (2.0 * MASS * dx**2) * np.ones(Vi.size - 1)

    if n_states is None:
        E, vecs = eigh_tridiagonal(diag, off)
    else:
        n_states = min(n_states, Vi.size)
        E, vecs = eigh_tridiagonal(diag, off, select="i",
                                   select_range=(0, n_states - 1))

    psi = np.zeros((E.size, N))
    psi[:, 1:-1] = vecs.T
    for k in range(E.size):                               # L2-normalize on x
        psi[k] /= np.sqrt(_trapz(psi[k]**2, x))
    return E, psi


def infinite_well_energy(n, L):
    """Exact infinite-square-well energy  E_n = n^2 pi^2 hbar^2 / (2 m L^2).

    The walls confine a free particle to 0 < x < L; n = 1, 2, 3, ...  (Griffiths
    3e Sec. 2.2, p.49-50).  In natural units (hbar=m=1): E_n = n^2 pi^2 / (2 L^2).
    """
    return (n * np.pi * HBAR)**2 / (2.0 * MASS * L**2)


def finite_square_well_bound_count(V0, a):
    """Number of bound states of the symmetric finite square well

        V(x) = -V0  for |x| < a ,   V = 0  otherwise      (V0 > 0, half-width a)

    Counted from the graphical (transcendental) solution: with the strength
    parameter z0 = (a/hbar) sqrt(2 m V0), even states sit one per interval
    (n*pi, n*pi+pi/2) and odd states one per (n*pi+pi/2, (n+1)*pi).  There is
    always at least one (even) bound state.  The total equals ceil(2 z0 / pi).
    (Griffiths 3e Sec. 2.6.)
    """
    z0 = a * np.sqrt(2.0 * MASS * V0) / HBAR
    n_even = int(np.floor(z0 / np.pi)) + 1
    n_odd = (int(np.floor((z0 - np.pi / 2.0) / np.pi)) + 1) if z0 > np.pi / 2.0 else 0
    return n_even + n_odd


# --- 2. the delta-function well ----------------------------------------------

def delta_well_energy(alpha):
    """The single bound-state energy of the attractive delta well V = -alpha*delta(x):

        E = - m alpha^2 / (2 hbar^2)        (Griffiths 3e Eq. 2.132, Sec. 2.5)

    Regardless of strength alpha > 0 the delta well has *exactly one* bound state.
    In natural units E = -alpha^2 / 2.
    """
    return -(MASS * alpha**2) / (2.0 * HBAR**2)


# --- 3. free particle / wave packets -----------------------------------------

def free_particle_omega(k):
    """Free-particle dispersion  omega(k) = hbar k^2 / (2 m)  (E = hbar omega).

    Unlike a light wave (omega = c k) this is *dispersive*: different k travel at
    different speeds, which is why a matter wave packet spreads.  (Griffiths 3e
    Sec. 2.4.)
    """
    return HBAR * np.asarray(k, dtype=float)**2 / (2.0 * MASS)


def phase_velocity(k):
    """Phase velocity of a free-particle plane wave  v_p = omega/k = hbar k / 2m."""
    return HBAR * k / (2.0 * MASS)


def group_velocity(k):
    """Group velocity  v_g = d omega/dk = hbar k / m = p/m  -- the classical
    particle speed, and exactly twice the phase velocity for a free particle."""
    return HBAR * k / MASS


def gaussian_packet_sigma(t, sigma0):
    """Position width sigma_x(t) of a freely-evolving minimum-uncertainty Gaussian
    wave packet that has width sigma0 at t = 0:

        sigma_x(t) = sigma0 * sqrt( 1 + ( hbar t / (2 m sigma0^2) )^2 ).

    The packet is narrowest at t = 0 and spreads symmetrically in |t| -- the
    free-particle analogue of dispersion (Griffiths 3e Sec. 2.4, Problem 2.22).
    """
    return sigma0 * np.sqrt(1.0 + (HBAR * t / (2.0 * MASS * sigma0**2))**2)


# --- 4. the rectangular barrier ----------------------------------------------

def transmission_barrier(E, V0, a):
    """Transmission coefficient T(E) through a rectangular barrier of height V0>0
    and width a (occupying 0 < x < a), with V = 0 on both sides.

    Three regimes (Griffiths 3e Problem 2.33):

      E < V0  (tunnelling):  kappa = sqrt(2 m (V0-E)) / hbar
          T = [ 1 + V0^2 sinh^2(kappa a) / (4 E (V0-E)) ]^-1   > 0
      E = V0:
          T = [ 1 + m V0 a^2 / (2 hbar^2) ]^-1                 (sinh -> linear limit)
      E > V0  (over-barrier):  k2 = sqrt(2 m (E-V0)) / hbar
          T = [ 1 + V0^2 sin^2(k2 a) / (4 E (E-V0)) ]^-1

    For E < V0 T is exponentially small but never zero -- quantum tunnelling.
    For E > V0 T oscillates and hits perfect transmission T = 1 at the
    resonances k2 a = n*pi (the barrier becomes "transparent").
    """
    E = float(E)
    if E <= 0.0:
        raise ValueError("E must be positive")
    if abs(E - V0) <= 1e-12 * max(abs(V0), 1.0):
        return 1.0 / (1.0 + MASS * V0 * a**2 / (2.0 * HBAR**2))
    if E < V0:
        kappa = np.sqrt(2.0 * MASS * (V0 - E)) / HBAR
        denom = 1.0 + (V0**2 * np.sinh(kappa * a)**2) / (4.0 * E * (V0 - E))
    else:
        k2 = np.sqrt(2.0 * MASS * (E - V0)) / HBAR
        denom = 1.0 + (V0**2 * np.sin(k2 * a)**2) / (4.0 * E * (E - V0))
    return 1.0 / denom


def reflection_barrier(E, V0, a):
    """Reflection coefficient of the rectangular barrier, R = 1 - T (the medium is
    identical on both sides, so probability current gives simply R + T = 1)."""
    return 1.0 - transmission_barrier(E, V0, a)


# --- 5. the step potential ---------------------------------------------------

def step_RT(E, V0):
    """Reflection and transmission for the step  V = 0 (x<0),  V = V0 (x>0).

    For E > V0, with k1 = sqrt(2mE)/hbar and k2 = sqrt(2m(E-V0))/hbar,

        R = ((k1 - k2)/(k1 + k2))^2 ,   T = 4 k1 k2 / (k1 + k2)^2 ,   R + T = 1.

    T is *current-weighted* (T = (k2/k1)|t|^2): the transmitted wave moves at a
    different speed, so |t|^2 alone is not the transmission probability.  For
    E <= V0 the wave is evanescent on the right -- total reflection R = 1, T = 0.
    (Griffiths 3e Problem 2.34.)
    """
    E = float(E)
    if E <= 0.0:
        raise ValueError("E must be positive")
    if E <= V0:
        return (1.0, 0.0)
    k1 = np.sqrt(2.0 * MASS * E) / HBAR
    k2 = np.sqrt(2.0 * MASS * (E - V0)) / HBAR
    R = ((k1 - k2) / (k1 + k2))**2
    T = 4.0 * k1 * k2 / (k1 + k2)**2
    return (R, T)


# --- general transfer-matrix scattering solver (verifies the analytic forms) --

def _interface_W(k, x):
    """Wave-matching matrix W(k,x) such that [psi(x), psi'(x)]^T = W(k,x) [A, B]^T
    for psi = A e^{ikx} + B e^{-ikx}.  k may be complex (evanescent regions)."""
    e_p = np.exp(1j * k * x)
    e_m = np.exp(-1j * k * x)
    return np.array([[e_p, e_m],
                     [1j * k * e_p, -1j * k * e_m]], dtype=complex)


def scatter_piecewise(E, V_list, x_list):
    """Exact scattering off any piecewise-constant 1-D potential, by the transfer
    matrix method.  Reproduces the analytic barrier and step coefficients and
    extends them to arbitrary stacks of segments (double barriers, wells, ...).

    Parameters
    ----------
    E : float          incident energy ( > V of the leftmost and rightmost regions).
    V_list : sequence  potential in each region, left to right (length n_reg).
    x_list : sequence  the n_reg - 1 interface positions (increasing).

    Returns (T, R), the transmission and reflection probabilities, current-weighted
    so that T + R = 1 whenever both asymptotic regions are classically allowed.

    Wave in region j:  psi = A_j e^{i k_j x} + B_j e^{-i k_j x},
    k_j = sqrt(2 m (E - V_j)) / hbar (complex where E < V_j).  Continuity of psi
    and psi' at each interface gives [A_j,B_j] = W_j^{-1} W_{j+1} [A_{j+1},B_{j+1}];
    the product M maps the outgoing (transmitted, B=0) amplitudes to the incident.
    """
    V_list = list(V_list)
    x_list = list(x_list)
    if len(x_list) != len(V_list) - 1:
        raise ValueError("need exactly one interface between each pair of regions")
    ks = [np.sqrt(complex(2.0 * MASS * (E - V))) / HBAR for V in V_list]

    M = np.eye(2, dtype=complex)
    for j, x in enumerate(x_list):
        M = M @ (np.linalg.inv(_interface_W(ks[j], x)) @ _interface_W(ks[j + 1], x))

    t = 1.0 / M[0, 0]              # [A0,B0] = M [t,0];  A0 = 1 incident
    r = M[1, 0] / M[0, 0]
    k0, kn = ks[0].real, ks[-1].real
    T = (kn / k0) * abs(t)**2 if k0 != 0.0 else 0.0
    R = abs(r)**2
    return (T, R)


# --- demo --------------------------------------------------------------------

def _demo():
    print("QM-08  One-dimensional problems  (hbar = m = 1)\n")

    print("Infinite square well, L = 1:  E_n = n^2 pi^2 / 2")
    x = np.linspace(0.0, 1.0, 1201)
    E, _ = bound_states(np.zeros_like(x), x, n_states=4)
    for n in range(1, 4):
        print("  n=%d:  FD %.4f   exact %.4f" % (n, E[n - 1], infinite_well_energy(n, 1.0)))

    print("\nFinite square well, V0 = 15, half-width a = 1:")
    print("  bound-state count (analytic) =", finite_square_well_bound_count(15.0, 1.0))
    X = np.linspace(-20.0, 20.0, 4001)
    Vw = np.where(np.abs(X) < 1.0, -15.0, 0.0)
    Ew, _ = bound_states(Vw, X, n_states=8)
    bound = Ew[(Ew < 0.0)]
    print("  FD energies < 0 (below well top):", np.round(bound, 3))

    print("\nDelta well, alpha = 2:  E = -alpha^2/2 = %.3f (exactly ONE bound state)"
          % delta_well_energy(2.0))

    print("\nRectangular barrier, V0 = 10, E = 5 (tunnelling, E < V0):")
    print("  width a :   T(E)")
    for a in (0.2, 0.5, 1.0, 2.0, 3.0):
        print("   %4.1f   : %.3e" % (a, transmission_barrier(5.0, 10.0, a)))
    print("  -> T falls off ~ exp(-2 kappa a): the tunnelling probability.")

    print("\nOver-barrier resonances (V0 = 10, a = 1):  T = 1 at k2*a = n*pi")
    for E_ in (10.5, 12.0, 14.93, 20.0):
        print("   E=%5.2f : T = %.4f" % (E_, transmission_barrier(E_, 10.0, 1.0)))

    print("\nStep potential, V0 = 1:")
    for E_ in (0.5, 1.5, 4.0, 100.0):
        R, T = step_RT(E_, 1.0)
        print("   E=%6.1f : R=%.4f  T=%.4f  R+T=%.4f" % (E_, R, T, R + T))


if __name__ == "__main__":
    _demo()
