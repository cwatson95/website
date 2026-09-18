"""
QM-14  Identical particles -- indistinguishability and the symmetrization
postulate, bosons (symmetric) vs fermions (antisymmetric), the Pauli exclusion
principle, the Slater determinant for N fermions, and the "exchange force"
(why fermions effectively repel and bosons bunch).

Part of the physics topic network (modules/topic_network.txt, module QM-14).
Builds on ~QM-05 (states as vectors, the exchange operator is just a Hermitian
operator) and ~QM-06 (measurement / expectation values).  Feeds ~SM-04 (quantum
statistics: Bose-Einstein vs Fermi-Dirac gases -- not yet built) and ~QM-12
(multi-electron atoms / the periodic table).

Griffiths & Schroeter, *Introduction to QM*, 3rd ed., Chapter 5
(Identical Particles):
  - two-particle systems; the product state Psi = psi_a(1) psi_b(2)   (Sec. 5.1, p.252)
  - the symmetrization rule: bosons symmetric (+), fermions
    antisymmetric (-) under interchange                               (Sec. 5.1.1, p.256)
  - Pauli exclusion: the antisymmetric combination of two
    IDENTICAL one-particle states is zero                             (Sec. 5.1.1, p.256)
  - the Slater determinant for completely antisymmetric N-particle
    states ("works for any number of particles")                     (Problem 5.8, p.262)
  - the exchange operator P, P^2 = 1, eigenvalues +-1, P psi = +- psi  (Sec. 5.1.4, p.264)
  - exchange forces:  <(x1-x2)^2>_+- = <(x1-x2)^2>_dist -+ 2|<x>_ab|^2 (Sec. 5.1.2, p.259-260)
  - spin & the helium ground state: symmetric spatial state needs the
    antisymmetric (singlet) spin state                               (Sec. 5.1.3, p.263)

REPRESENTATION.  A single-particle state is a vector in C^d (an orbital expressed
in some d-dimensional one-particle basis).  An N-particle state lives in the
tensor product (C^d)^(x)N = C^(d^N), with "particle k" occupying tensor slot k.
The exchange operator swaps two slots.  Symmetrization/antisymmetrization and the
Slater determinant are built directly in this space and *checked* against the
analytic facts (P psi = +-psi, normalization, vanishing on a repeated orbital).

EXCHANGE FORCE.  Worked in the position representation on a 1-D grid, using
exact one-particle orbitals (infinite square well or harmonic oscillator), so the
numbers can be compared to closed forms (Griffiths Problems 5.6 and 5.7).

Natural units throughout: for the harmonic oscillator hbar = m = omega = 1, so
the oscillator length is 1 and <x^2>_n = n + 1/2.  The infinite well uses width L
(default 1).  Every claim below is verified numerically in test_identical.py.
"""

import itertools

import numpy as np

__all__ = [
    # tensor-product machinery / exchange operator
    "tensor", "swap_operator", "apply_pair_swap", "levi_civita_sign",
    # the two ways to build an identical-particle pair
    "symmetrize", "antisymmetrize",
    # N fermions
    "slater_determinant",
    # 1-D orbitals and the exchange force
    "well_state", "ho_state", "position_moments", "exchange_dx2",
    # spin-1/2 helpers (helium / spin-statistics capstone)
    "spin_up", "spin_down", "singlet", "triplet",
    # numerics helper
    "norm",
]


# --- 0. small helpers --------------------------------------------------------

def _integrate(y, x):
    """Trapezoidal integral int y dx, robust across numpy versions
    (numpy>=2 renamed trapz -> trapezoid)."""
    f = getattr(np, "trapezoid", None) or np.trapz
    return f(y, x)


def norm(psi):
    """Euclidean norm sqrt(<psi|psi>) of a (complex) state vector."""
    psi = np.asarray(psi, dtype=complex)
    return float(np.sqrt(np.vdot(psi, psi).real))


def levi_civita_sign(perm):
    """Sign (+-1) of a permutation given as a sequence of 0..N-1, by counting
    inversions.  sgn = (-1)^(number of out-of-order pairs)."""
    p = list(perm)
    n = len(p)
    sign = 1
    for i in range(n):
        for j in range(i + 1, n):
            if p[i] > p[j]:
                sign = -sign
    return sign


# --- 1. tensor product and the exchange operator -----------------------------

def tensor(*states):
    """Tensor (Kronecker) product |a> (x) |b> (x) ... of single-particle state
    vectors -- the composite state with particle k in the k-th argument
    (Griffiths Eq. 5.9, p.252: the product wave function for noninteracting
    distinguishable particles)."""
    out = np.asarray(states[0], dtype=complex)
    for s in states[1:]:
        out = np.kron(out, np.asarray(s, dtype=complex))
    return out


def swap_operator(d):
    """Exchange operator P_12 on the two-particle space C^d (x) C^d
    (Griffiths Sec. 5.1.4, Eq. 5.30, p.264).  It swaps the two factors:

        P_12 ( |i> (x) |j> ) = |j> (x) |i>.

    P_12 is a real symmetric permutation matrix with P_12^2 = I, so its
    eigenvalues are +-1 (the symmetric and antisymmetric subspaces)."""
    P = np.zeros((d * d, d * d))
    for i in range(d):
        for j in range(d):
            P[j * d + i, i * d + j] = 1.0   # row |j>|i>  <-  col |i>|j>
    return P


def apply_pair_swap(state, d, N, p, q):
    """Apply the exchange of particles p and q (0-based tensor slots) to an
    N-particle state in (C^d)^(x)N, returned as a flat vector.  Used to test the
    total antisymmetry of the Slater determinant under ANY pair interchange
    (Griffiths Eq. 5.34, p.264: antisymmetry under interchange of any two)."""
    arr = np.asarray(state, dtype=complex).reshape((d,) * N)
    arr = np.swapaxes(arr, p, q)
    return arr.reshape(-1)


# --- 2. the two-particle symmetric / antisymmetric combinations --------------

def symmetrize(a, b, tol=1e-12):
    """BOSON two-particle state: the normalized symmetric combination

        |a,b>_+  =  ( |a>(x)|b> + |b>(x)|a> ) / N      (Griffiths Eq. 5.17, +).

    Symmetric under exchange: P_12 |a,b>_+ = + |a,b>_+.  For a == b this is just
    the (normalized) |a>(x)|a> -- two bosons MAY share a state."""
    a = np.asarray(a, dtype=complex)
    b = np.asarray(b, dtype=complex)
    v = np.kron(a, b) + np.kron(b, a)
    nv = norm(v)
    return v / nv if nv > tol else v


def antisymmetrize(a, b, tol=1e-12):
    """FERMION two-particle state: the normalized antisymmetric combination

        |a,b>_-  =  ( |a>(x)|b> - |b>(x)|a> ) / N      (Griffiths Eq. 5.17, -).

    Antisymmetric under exchange: P_12 |a,b>_- = - |a,b>_-.  If a == b the vector
    is identically ZERO -- the Pauli exclusion principle (Griffiths p.256): two
    identical fermions cannot occupy the same one-particle state.  The zero
    vector is returned as-is (not normalized)."""
    a = np.asarray(a, dtype=complex)
    b = np.asarray(b, dtype=complex)
    v = np.kron(a, b) - np.kron(b, a)
    nv = norm(v)
    return v / nv if nv > tol else v


# --- 3. the Slater determinant: N fermions -----------------------------------

def slater_determinant(orbitals, normalize_state=True, tol=1e-12):
    """Totally antisymmetric N-particle state built from N single-particle
    orbitals (Griffiths Problem 5.8, p.262 -- the Slater determinant trick,
    which "works for any number of particles"):

        |Psi> = (1/sqrt(N!)) sum_{sigma in S_N} sgn(sigma)
                     |phi_{sigma(0)}> (x) ... (x) |phi_{sigma(N-1)}>.

    Equivalently the antisymmetrizer applied to phi_0 (x) ... (x) phi_{N-1}, the
    tensor-space form of the determinant det[ phi_i in slot j ].  Properties
    (all tested):
      * antisymmetric under interchange of ANY two particles (any pair swap
        flips the sign), hence obeys the Pauli principle;
      * VANISHES (zero vector) if any two orbitals coincide -- two rows equal;
      * for ORTHONORMAL orbitals the raw (unnormalized) norm is exactly
        sqrt(N!), so dividing by it gives a unit state.

    Parameters
    ----------
    orbitals : sequence of N vectors, each length d (the one-particle dimension).
    normalize_state : if True (default) return the unit-norm state; if False
        return the raw antisymmetric sum (whose norm is sqrt(N!) for an
        orthonormal set -- used to check the normalization claim).
    """
    orbs = [np.asarray(o, dtype=complex) for o in orbitals]
    N = len(orbs)
    if N == 0:
        raise ValueError("need at least one orbital")
    d = orbs[0].shape[0]
    if any(o.shape != (d,) for o in orbs):
        raise ValueError("all orbitals must be vectors of the same length d")

    psi = np.zeros(d ** N, dtype=complex)
    for perm in itertools.permutations(range(N)):
        sign = levi_civita_sign(perm)
        term = orbs[perm[0]]
        for k in range(1, N):
            term = np.kron(term, orbs[perm[k]])
        psi += sign * term

    if normalize_state:
        nv = norm(psi)
        if nv > tol:
            psi = psi / nv
    return psi


# --- 4. one-particle 1-D orbitals (for the exchange force) -------------------

def well_state(n, x, L=1.0):
    """n-th infinite-square-well eigenfunction on [0, L] (Griffiths Eq. 2.28):

        psi_n(x) = sqrt(2/L) sin(n pi x / L),   n = 1, 2, 3, ...

    Returned sampled on the grid x.  <x>_n = L/2 and
    <x^2>_n = L^2 (1/3 - 1/(2 n^2 pi^2))."""
    return np.sqrt(2.0 / L) * np.sin(n * np.pi * x / L)


def ho_state(n, x):
    """n-th harmonic-oscillator eigenfunction in natural units hbar = m = omega
    = 1 (so the oscillator length is 1), n = 0, 1, 2, ...:

        psi_n(x) = (2^n n! sqrt(pi))^{-1/2} H_n(x) exp(-x^2/2),

    with H_n the physicists' Hermite polynomials (built here by the recurrence
    H_0 = 1, H_1 = 2x, H_{k+1} = 2x H_k - 2k H_{k-1}, so no SciPy dependency).
    <x>_n = 0 and <x^2>_n = n + 1/2."""
    x = np.asarray(x, dtype=float)
    H0 = np.ones_like(x)
    if n == 0:
        Hn = H0
    else:
        Hkm1, Hk = H0, 2.0 * x
        for k in range(1, n):
            Hkm1, Hk = Hk, 2.0 * x * Hk - 2.0 * k * Hkm1
        Hn = Hk
    import math
    pref = 1.0 / np.sqrt((2.0 ** n) * math.factorial(n) * np.sqrt(np.pi))
    return pref * Hn * np.exp(-x * x / 2.0)


# --- 5. the exchange force ----------------------------------------------------

def position_moments(psi_a, psi_b, x):
    """One- and two-orbital position matrix elements needed for the exchange
    force, computed by trapezoidal quadrature on the grid x (orbitals are
    renormalized on the grid first, so <a|a> = <b|b> = 1 exactly):

        <x>_a   = int psi_a* x  psi_a dx        <x^2>_a = int psi_a* x^2 psi_a dx
        <x>_b, <x^2>_b   (likewise)
        <x>_ab  = int psi_a* x  psi_b dx         (Griffiths Eq. 5.24, p.260)

    Returns a dict.  For real orbitals <x>_ab is real."""
    x = np.asarray(x, dtype=float)
    a = np.asarray(psi_a, dtype=complex)
    b = np.asarray(psi_b, dtype=complex)
    a = a / np.sqrt(_integrate(np.conj(a) * a, x).real)
    b = b / np.sqrt(_integrate(np.conj(b) * b, x).real)

    def me(f, op, g):
        return complex(_integrate(np.conj(f) * op * g, x))

    return {
        "x_a":   me(a, x, a).real,
        "x2_a":  me(a, x * x, a).real,
        "x_b":   me(b, x, b).real,
        "x2_b":  me(b, x * x, b).real,
        "x_ab":  me(a, x, b),          # complex in general; real for real orbitals
    }


def exchange_dx2(psi_a, psi_b, x):
    """Expectation of the squared separation <(x1 - x2)^2> for two particles in
    orbitals a and b, in the distinguishable, boson and fermion cases
    (Griffiths Sec. 5.1.2, Eqs. 5.23 & 5.25, p.259-260):

        distinguishable:  <(Dx)^2>      = <x^2>_a + <x^2>_b - 2 <x>_a <x>_b
        boson  (sym, +):  <(Dx)^2>_+    = <(Dx)^2> - 2 |<x>_ab|^2
        fermion(anti,-):  <(Dx)^2>_-    = <(Dx)^2> + 2 |<x>_ab|^2

    The whole effect is the single EXCHANGE TERM  -+ 2 |<x>_ab|^2 (Eq. 5.26):
    bosons end up closer together, fermions farther apart, than distinguishable
    particles in the same two states -- the "exchange force."  It vanishes unless
    the orbitals overlap (<x>_ab = 0 -> all three equal).  Returns a dict."""
    m = position_moments(psi_a, psi_b, x)
    distinguishable = m["x2_a"] + m["x2_b"] - 2.0 * m["x_a"] * m["x_b"]
    exch = 2.0 * abs(m["x_ab"]) ** 2
    return {
        "distinguishable": distinguishable,
        "boson":           distinguishable - exch,   # + sign in 5.17 -> closer
        "fermion":         distinguishable + exch,   # - sign in 5.17 -> farther
        "exchange_term":   exch,
        "x_ab":            m["x_ab"],
    }


# --- 6. spin-1/2 helpers: the helium ground state / spin-statistics ----------

def spin_up():
    """The spin-up one-particle (spin) state |up> = (1, 0)."""
    return np.array([1.0, 0.0], dtype=complex)


def spin_down():
    """The spin-down one-particle (spin) state |down> = (0, 1)."""
    return np.array([0.0, 1.0], dtype=complex)


def singlet():
    """Two-spin singlet (|up,down> - |down,up>)/sqrt(2) (Griffiths Eq. 4.176):
    the ANTISYMMETRIC spin state, total spin 0.  Equal to antisymmetrize(up,down).
    It is the spin partner of a SYMMETRIC spatial state -- e.g. the two 1s
    electrons of helium in its ground state (Griffiths Sec. 5.1.3, p.263)."""
    return antisymmetrize(spin_up(), spin_down())


def triplet():
    """The three SYMMETRIC two-spin (triplet) states, total spin 1
    (Griffiths Eq. 4.175): |up,up>, (|up,down>+|down,up>)/sqrt(2), |down,down>.
    Returned as a list of three vectors.  Each is +1 under exchange."""
    return [
        tensor(spin_up(), spin_up()),
        symmetrize(spin_up(), spin_down()),
        tensor(spin_down(), spin_down()),
    ]


# --- demo --------------------------------------------------------------------

def _demo():
    np.set_printoptions(precision=4, suppress=True)
    print("QM-14  Identical particles -- symmetrization, Pauli, exchange force\n")

    # two orthonormal one-particle states in C^2
    a = np.array([1.0, 0.0])
    b = np.array([0.0, 1.0])
    P = swap_operator(2)
    sym = symmetrize(a, b)
    anti = antisymmetrize(a, b)
    print("Two orthonormal orbitals a=(1,0), b=(0,1) in C^2:")
    print("  boson  |a,b>_+ =", sym.real, " P_12 eigenvalue:",
          round(float(np.vdot(sym, P @ sym).real), 6), "(symmetric)")
    print("  fermion|a,b>_- =", anti.real, " P_12 eigenvalue:",
          round(float(np.vdot(anti, P @ anti).real), 6), "(antisymmetric)")
    print("  Pauli: antisymmetrize(a, a) =", antisymmetrize(a, a).real,
          " (the zero vector)\n")

    print("Slater determinant of N=3 orthonormal orbitals (in C^3):")
    e = np.eye(3)
    Psi = slater_determinant([e[0], e[1], e[2]])
    raw = slater_determinant([e[0], e[1], e[2]], normalize_state=False)
    print("  ||raw|| =", round(norm(raw), 6), "= sqrt(3!) =", round(np.sqrt(6), 6))
    sw = apply_pair_swap(Psi, 3, 3, 0, 1)
    print("  swap particles 0<->1 gives -Psi? ",
          np.allclose(sw, -Psi))
    Psi0 = slater_determinant([e[0], e[1], e[0]])   # repeated orbital
    print("  two equal orbitals -> ||Psi|| =", round(norm(Psi0), 12),
          "(Pauli: vanishes)\n")

    print("Exchange force, infinite well, orbitals n=1 and n=2 (L=1):")
    x = np.linspace(0.0, 1.0, 4001)
    res = exchange_dx2(well_state(1, x), well_state(2, x), x)
    print("  <(Dx)^2>  boson=%.5f  <  distinguishable=%.5f  <  fermion=%.5f"
          % (res["boson"], res["distinguishable"], res["fermion"]))
    print("  exchange term 2|<x>_ab|^2 = %.5f  (bosons bunch, fermions avoid)\n"
          % res["exchange_term"])

    print("Helium ground state / spin-statistics:")
    s = singlet()
    print("  spin singlet is antisymmetric? P_12 eigenvalue =",
          round(float(np.vdot(s, swap_operator(2) @ s).real), 6))
    print("  -> pairs with the SYMMETRIC spatial 1s^2 state, so the FULL "
          "two-electron\n     state is antisymmetric (Pauli satisfied with both "
          "electrons in 1s).")


if __name__ == "__main__":
    _demo()
