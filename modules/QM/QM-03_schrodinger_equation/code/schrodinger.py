"""
QM-03  The Schrodinger equation  --  the dynamical law of quantum mechanics and
the structure of its solutions, built and evolved on a grid.

Part of the physics topic network (modules/topic_network.txt, module QM-03).
It sits between ~QM-02 (the wavefunction Psi and the Born rule |Psi|^2 -- the
object we evolve here) and ~QM-08 / ~QM-09 (the 1-D solutions and the harmonic
oscillator).  The analytic engine -- seek product solutions psi(x)T(t), then
patch them back together -- is separation of variables, ~MA-08.

The story, made computational:

  * Time-DEPENDENT Schrodinger equation (TDSE)        i hbar dPsi/dt = H Psi,
        with  H = -hbar^2/2m d^2/dx^2 + V(x).            [Griffiths 3e Sec.1.1, p.16]

  * Separation  Psi(x,t) = psi(x) exp(-i E t/hbar)  turns the TDSE into the
    time-INDEPENDENT Schrodinger equation (TISE), an eigenvalue problem
        H psi = E psi.                                    [Griffiths 3e Sec.2.1, p.43]

  * A single separable solution is a STATIONARY STATE: its phase rotates but
    |Psi(x,t)|^2 = |psi(x)|^2 is frozen -- nothing observable changes in time.

  * The general solution is a SUPERPOSITION
        Psi(x,t) = sum_n c_n psi_n(x) exp(-i E_n t/hbar).
    The c_n are fixed by the initial state (Psi(x,0) = sum_n c_n psi_n, recovered
    by "Fourier's trick" c_n = <psi_n|Psi0>); |c_n|^2 is the probability of
    measuring energy E_n; and the INTERFERENCE between two terms beats at the
    Bohr angular frequency omega = (E_m - E_n)/hbar.

NATURAL UNITS.  We work in hbar = m = 1.  They survive as function arguments
defaulting to 1.0, so the closed form  E_n = n^2 pi^2 hbar^2 / (2 m L^2)  can
still be exercised with other values (see the tests).  With hbar = m = 1 the
infinite well of width L has E_n = n^2 pi^2 / (2 L^2); length is in the grid's
unit and energy in the matching hbar^2/(m * length^2).

The Hamiltonian is assembled by finite differences (a 3-point Laplacian with
Dirichlet walls) and diagonalised with numpy.linalg.eigh, so every statement
above is checked against its closed form in test_schrodinger.py rather than
asserted.
"""

import numpy as np

__all__ = [
    # grid + operators
    "make_grid", "second_derivative_matrix", "hamiltonian", "solve",
    # inner products / states
    "inner_product", "normalize", "prob_density", "expectation_position",
    # dynamics
    "stationary_state", "evolve", "coefficients",
    # closed forms / helpers
    "infinite_well_energy", "infinite_well_eigenfunction",
    "harmonic_oscillator_energy", "bohr_frequency", "superposition_period",
    "measure_period",
]


# --- grid and the finite-difference Hamiltonian ------------------------------

def make_grid(x_min, x_max, N):
    """N interior sample points of the interval [x_min, x_max].

    Spacing is uniform, dx = (x_max - x_min)/(N+1), and the two ENDPOINTS are the
    excluded Dirichlet walls where psi = 0.  Returns the length-N array of
    interior points x_i = x_min + i*dx, i = 1..N.  (For the infinite square well
    of width L use make_grid(0, L, N): the walls then sit exactly at 0 and L.)
    """
    dx = (x_max - x_min) / (N + 1)
    return x_min + dx * np.arange(1, N + 1)


def second_derivative_matrix(N, dx):
    """The 3-point finite-difference second-derivative operator d^2/dx^2 as an
    (N, N) matrix with Dirichlet boundary conditions (psi = 0 just outside).

        (d^2 psi/dx^2)_i ~ (psi_{i+1} - 2 psi_i + psi_{i-1}) / dx^2

    i.e. tridiagonal(1, -2, 1)/dx^2.  Symmetric, so H built from it is Hermitian.
    """
    main = -2.0 * np.ones(N)
    off = np.ones(N - 1)
    return (np.diag(main) + np.diag(off, 1) + np.diag(off, -1)) / dx ** 2


def hamiltonian(x, V, hbar=1.0, m=1.0):
    """Assemble  H = -hbar^2/(2m) d^2/dx^2 + V(x)  on the uniform grid x.

    `V` may be a callable V(x) (evaluated on the grid) or an array of the same
    length as x.  Returns the (N, N) real-symmetric Hamiltonian matrix.  The
    infinite-square-well limit is the default V = 0 with the walls supplied by
    the Dirichlet grid (see make_grid).
    """
    x = np.asarray(x, float)
    N = len(x)
    dx = x[1] - x[0]
    T = -(hbar ** 2) / (2.0 * m) * second_derivative_matrix(N, dx)
    Vvals = np.asarray(V(x) if callable(V) else V, float)
    return T + np.diag(Vvals)


def solve(x, V=0.0, hbar=1.0, m=1.0):
    """Solve the TISE  H psi = E psi  on the grid x.

    Returns (E, psi) where E is the ascending array of eigen-energies and psi is
    the (N, K) matrix whose column psi[:, n] is the n-th eigenstate, normalised
    so that the discrete integral  sum_i |psi_i|^2 dx = 1  (eigh returns unit
    Euclidean norm; dividing by sqrt(dx) converts that to unit L^2 norm).  The
    eigenstates are automatically orthonormal: <psi_m|psi_n> = delta_mn.
    """
    x = np.asarray(x, float)
    if not callable(V) and np.isscalar(V):
        V = np.full(len(x), float(V))
    H = hamiltonian(x, V, hbar, m)
    E, vecs = np.linalg.eigh(H)          # ascending, columns orthonormal (Euclid.)
    dx = x[1] - x[0]
    return E, vecs / np.sqrt(dx)


# --- inner products, densities, observables ----------------------------------

def inner_product(f, g, dx):
    """The L^2 inner product  <f|g> = integral conj(f) g dx  on a uniform grid,
    as the rectangle sum  sum_i conj(f_i) g_i dx.  (This is exactly the norm
    `solve` normalises to, so orthonormality of its output is machine-precise.)
    """
    return np.sum(np.conj(f) * g) * dx


def normalize(psi, dx):
    """Rescale psi so that <psi|psi> = 1 under the grid inner product."""
    return psi / np.sqrt(inner_product(psi, psi, dx).real)


def prob_density(Psi):
    """Born probability density  |Psi|^2  (~QM-02)."""
    return np.abs(Psi) ** 2


def expectation_position(Psi, x):
    """<x> = integral x |Psi|^2 dx for a (normalised) state on the grid x."""
    x = np.asarray(x, float)
    dx = x[1] - x[0]
    p = prob_density(Psi)
    return float(np.sum(x * p) * dx / (np.sum(p) * dx))


# --- time evolution: stationary states and superpositions --------------------

def stationary_state(psi_n, E_n, t, hbar=1.0):
    """Evolve a single eigenstate:  Psi(x,t) = psi_n(x) exp(-i E_n t/hbar).

    Only the global phase turns, so |Psi(x,t)|^2 = |psi_n(x)|^2 is independent of
    t -- the hallmark of a STATIONARY STATE.  Returns a complex array.
    """
    return np.asarray(psi_n, complex) * np.exp(-1j * E_n * t / hbar)


def evolve(E, psi, coeffs, t, hbar=1.0):
    """The general solution of the TDSE for a separable spectrum:

        Psi(x,t) = sum_n c_n psi_n(x) exp(-i E_n t/hbar).

    `psi` is the (N, K) eigenstate matrix (columns from `solve`), `E` the K
    energies, `coeffs` the K coefficients c_n.  Each term keeps its shape and
    only its phase advances, at rate E_n/hbar; the observable motion in |Psi|^2
    comes entirely from the BEATS between terms of different E_n.
    """
    E = np.asarray(E, float)
    coeffs = np.asarray(coeffs, complex)
    phases = np.exp(-1j * E * t / hbar)
    return np.asarray(psi, complex) @ (coeffs * phases)


def coefficients(psi, Psi0, dx):
    """Fourier's trick: project an initial state onto the eigenbasis,

        c_n = <psi_n | Psi0> = integral conj(psi_n) Psi0 dx.

    `psi` is the (N, K) eigenstate matrix; returns the length-K coefficient
    vector.  Because the psi_n are orthonormal, Psi0 = psi @ c reconstructs the
    input and sum |c_n|^2 = <Psi0|Psi0> (Parseval).
    """
    return (np.conj(np.asarray(psi).T) @ np.asarray(Psi0)) * dx


# --- closed forms (for cross-checking the grid solver) -----------------------

def infinite_well_energy(n, L, hbar=1.0, m=1.0):
    """Exact infinite-square-well levels  E_n = n^2 pi^2 hbar^2 / (2 m L^2)
    (n = 1, 2, 3, ...).  [Griffiths 3e Sec.2.2.]"""
    return (n ** 2) * (np.pi ** 2) * (hbar ** 2) / (2.0 * m * L ** 2)


def infinite_well_eigenfunction(n, x, L):
    """Exact well eigenfunction  psi_n(x) = sqrt(2/L) sin(n pi x / L)  on [0, L]."""
    return np.sqrt(2.0 / L) * np.sin(n * np.pi * np.asarray(x, float) / L)


def harmonic_oscillator_energy(n, omega=1.0, hbar=1.0):
    """Exact oscillator levels  E_n = (n + 1/2) hbar omega  (n = 0, 1, 2, ...),
    the cross-check used by ~QM-09."""
    return (n + 0.5) * hbar * omega


def bohr_frequency(E_m, E_n, hbar=1.0):
    """Beat (Bohr) angular frequency of a two-level superposition,
    omega = (E_m - E_n)/hbar."""
    return (E_m - E_n) / hbar


def superposition_period(E_m, E_n, hbar=1.0):
    """Period of the |Psi|^2 oscillation for a two-term superposition,
    T = 2 pi / |omega| = 2 pi hbar / |E_m - E_n|."""
    return 2.0 * np.pi * hbar / abs(E_m - E_n)


def measure_period(ts, signal):
    """Estimate the period of an oscillating real signal numerically.

    Averages the spacing between successive UPWARD zero-crossings of
    (signal - mean(signal)), using linear interpolation for sub-step accuracy.
    Returns nan if fewer than two crossings are found.  Used to confirm that the
    measured beat period of <x>(t) equals 2 pi hbar/(E2 - E1).
    """
    ts = np.asarray(ts, float)
    s = np.asarray(signal, float) - np.mean(signal)
    crossings = []
    for i in range(len(s) - 1):
        if s[i] <= 0.0 < s[i + 1]:                  # upward crossing in (i, i+1]
            frac = -s[i] / (s[i + 1] - s[i])
            crossings.append(ts[i] + frac * (ts[i + 1] - ts[i]))
    if len(crossings) < 2:
        return float("nan")
    return float(np.mean(np.diff(crossings)))


# --- demo --------------------------------------------------------------------

def _demo():
    print("QM-03  Schrodinger equation -- solving and evolving Psi on a grid")
    print("=" * 66)
    print("(natural units hbar = m = 1)\n")

    # 1. infinite square well: TISE eigenvalues vs the closed form
    L, N = 1.0, 400
    x = make_grid(0.0, L, N)
    E, psi = solve(x, V=0.0)
    print("Infinite square well, width L = 1   E_n = n^2 pi^2 / (2 L^2):")
    print("  n   numeric E_n     exact E_n     rel.err")
    for n in range(1, 6):
        exact = infinite_well_energy(n, L)
        print("  %d   %11.6f   %11.6f   %.2e"
              % (n, E[n - 1], exact, abs(E[n - 1] - exact) / exact))

    dx = x[1] - x[0]
    # 2. stationary state: |Psi|^2 does not move
    psi1 = psi[:, 0]
    dens = [prob_density(stationary_state(psi1, E[0], t)) for t in (0.0, 0.7, 3.3)]
    drift = max(np.max(np.abs(dens[k] - dens[0])) for k in (1, 2))
    print("\nStationary state (n=1): max change of |Psi|^2 over t in {0,0.7,3.3}")
    print("  = %.2e  (a stationary state is observationally frozen)" % drift)

    # 3. superposition (psi1 + psi2)/sqrt(2): |Psi|^2 beats at omega=(E2-E1)/hbar
    c = np.zeros(psi.shape[1]); c[0] = c[1] = 1.0 / np.sqrt(2.0)
    T_theory = superposition_period(E[1], E[0])
    ts = np.linspace(0.0, 4.0 * T_theory, 2000)
    xt = [expectation_position(evolve(E, psi, c, t), x) for t in ts]
    T_meas = measure_period(ts, xt)
    print("\nSuperposition (psi1+psi2)/sqrt(2): <x>(t) oscillation period")
    print("  measured T = %.5f   theory 2 pi/(E2-E1) = %.5f   rel.err %.2e"
          % (T_meas, T_theory, abs(T_meas - T_theory) / T_theory))

    # 4. role of the c_n: build an arbitrary state, recover its coefficients
    Psi0 = normalize(0.6 * psi[:, 0] + 0.8 * psi[:, 2], dx)
    cn = coefficients(psi, Psi0, dx)
    print("\nFourier's trick on Psi0 = (0.6 psi1 + 0.8 psi3)/norm:")
    print("  |c_1|^2=%.3f  |c_3|^2=%.3f  sum|c_n|^2=%.6f  (energy probabilities)"
          % (abs(cn[0]) ** 2, abs(cn[2]) ** 2, np.sum(np.abs(cn) ** 2)))

    # 5. same solver, harmonic oscillator (seed of ~QM-09)
    xh = make_grid(-8.0, 8.0, 800)
    Eh, _ = solve(xh, V=lambda xx: 0.5 * xx ** 2)
    print("\nSame solver, V = x^2/2 (harmonic oscillator, ~QM-09): E_n = n+1/2")
    print("  " + "  ".join("E_%d=%.4f" % (n, Eh[n]) for n in range(5)))


if __name__ == "__main__":
    _demo()
