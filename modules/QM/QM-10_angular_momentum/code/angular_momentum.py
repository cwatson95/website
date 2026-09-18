"""
QM-10  Angular momentum -- the orbital observable L = r x p promoted to operators,
its closed commutator algebra, and the eigenstates that algebra forces into being.

Part of the physics topic network (see modules/topic_network.txt, module QM-10).
Builds on ~MA-12 (associated Legendre / spherical harmonics; imported below) and
is the quantum image of ~CM-09 (classical L = r x p, torque -- bridge B3, which
connects once CM-09 is built). Feeds ~QM-11 (spin: the HALF-INTEGER reps built
here have matrices but no Y_l^m), ~QM-12 (hydrogen, where Y_l^m is the angular
factor), ~QM-13 (addition of angular momenta), and ~CM-13 (inertia tensor).

The story, each a function group below:
  1. The algebra        -- [L_i, L_j] = i hbar eps_ijk L_k.  Everything follows.
  2. Matrix reps        -- for each l (dim 2l+1): L_z = diag(m), the ladder
                           operators L_pm with elements hbar*sqrt(l(l+1)-m(m+-1)),
                           then L_x, L_y, L^2.  Built so the algebra holds EXACTLY
                           in floating point (a clean contrast to ~QM-05's x, p,
                           which only close on a truncated basis).
  3. Spectrum           -- L^2 -> hbar^2 l(l+1),  L_z -> hbar m,  m = -l..+l.
  4. Position space      -- the spherical harmonics Y_l^m(theta,phi): the
                           simultaneous eigenfunctions of L^2 and L_z = -i hbar d/dphi.

UNITS: natural units  hbar = 1  throughout (set HBAR below; the hbar factors are
carried symbolically so that L_z = hbar*diag(m), L^2 = hbar^2 l(l+1) I, and
[L_x,L_y] = i hbar L_z all read off literally).  numpy supplies the linear
algebra; ~MA-12's assoc_legendre supplies the angular functions.

Reference: Griffiths & Schroeter, Introduction to QM, 3rd ed., Sec. 4.3
(eigenvalues, p.201-206) and Sec. 4.1.2 / 4.3.2 (spherical harmonics, p.176-178,
208).  See ../refs.md for page-verified citations.
"""

import math
import os
import sys

import numpy as np

# ~MA-12 (associated Legendre) by relative path -- mirrors how CM-01 imports
# MA-01.  Once a shared `physkit` package exists this becomes
#     from physkit.special_functions import assoc_legendre
_HERE = os.path.dirname(os.path.abspath(__file__))
_MA12 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA",
                                     "MA-12_special_functions", "code"))
if _MA12 not in sys.path:
    sys.path.insert(0, _MA12)

from special_functions import assoc_legendre  # noqa: E402

__all__ = [
    "HBAR",
    # bookkeeping
    "dim", "m_values", "ladder_coeff", "casimir_eigenvalue",
    # matrix representation
    "Lz", "L_plus", "L_minus", "Lx", "Ly", "L_squared",
    "angular_momentum_set", "commutator",
    # position-space eigenfunctions
    "spherical_harmonic", "sphere_inner_product", "Lz_on_Y",
]

HBAR = 1.0   # natural units; restore SI by setting HBAR = 1.054571817e-34


# --- 0. bookkeeping ----------------------------------------------------------

def dim(l):
    """Dimension of the spin-l representation: 2l+1 (an integer for integer OR
    half-integer l).  l=1/2 -> 2, l=1 -> 3, l=3/2 -> 4, l=2 -> 5."""
    return int(round(2 * l + 1))


def m_values(l):
    """The magnetic quantum numbers for a given l, top rung first:
    m = l, l-1, ..., -l  (a numpy array of length 2l+1).  These are exactly the
    L_z eigenvalues in units of hbar (Griffiths 3e Eq. 4.119, p.205)."""
    n = dim(l)
    return np.array([l - k for k in range(n)], dtype=float)


def ladder_coeff(l, m, sign=+1):
    """Matrix element of the raising (sign=+1) / lowering (sign=-1) operator:

        <l, m+-1| L_pm |l, m> = hbar * sqrt( l(l+1) - m(m+-1) ).

    Vanishes at the top rung (sign=+1, m=l) and bottom rung (sign=-1, m=-l),
    which is what truncates the ladder.  (Griffiths 3e Problem 4.21, p.206.)"""
    return HBAR * math.sqrt(max(0.0, l * (l + 1) - m * (m + sign)))


def casimir_eigenvalue(l):
    """The single eigenvalue of L^2 on the whole l-multiplet: hbar^2 l(l+1).
    (Griffiths 3e Eq. 4.118, p.205.)"""
    return HBAR ** 2 * l * (l + 1)


# --- 1./2. matrix representation (dimension 2l+1) ----------------------------

def Lz(l):
    """L_z as a diagonal (2l+1)x(2l+1) matrix, L_z = hbar * diag(l, ..., -l).
    Its spectrum {-l, ..., +l} is the set of allowed projections of L on the z
    axis (Griffiths 3e Eq. 4.119, p.205)."""
    return HBAR * np.diag(m_values(l)).astype(complex)


def L_plus(l):
    """Raising operator L_+ = L_x + i L_y as a matrix.  In the basis ordered
    m = l, l-1, ..., -l it is the super-diagonal carrying ladder_coeff(l,m,+1):
    it sends |l,m> -> |l,m+1> and annihilates the top rung |l,l>."""
    m = m_values(l)
    n = len(m)
    M = np.zeros((n, n), dtype=complex)
    for j in range(n):                         # column = state |l, m[j]>
        if j - 1 >= 0:                         # row of |l, m[j]+1> (one rung up)
            M[j - 1, j] = ladder_coeff(l, m[j], +1)
    return M


def L_minus(l):
    """Lowering operator L_- = L_x - i L_y as a matrix: the sub-diagonal carrying
    ladder_coeff(l,m,-1); sends |l,m> -> |l,m-1> and annihilates |l,-l>.
    L_- is the Hermitian conjugate of L_+ (checked in the tests)."""
    m = m_values(l)
    n = len(m)
    M = np.zeros((n, n), dtype=complex)
    for j in range(n):
        if j + 1 < n:                          # row of |l, m[j]-1> (one rung down)
            M[j + 1, j] = ladder_coeff(l, m[j], -1)
    return M


def Lx(l):
    """L_x = (L_+ + L_-) / 2.  Hermitian; for l=1/2, 2*L_x is the Pauli matrix."""
    return (L_plus(l) + L_minus(l)) / 2.0


def Ly(l):
    """L_y = (L_+ - L_-) / 2i.  Hermitian; for l=1/2, 2*L_y is the Pauli matrix."""
    return (L_plus(l) - L_minus(l)) / 2.0j


def L_squared(l):
    """The Casimir L^2 = L_x^2 + L_y^2 + L_z^2.  Equals hbar^2 l(l+1) times the
    identity -- the whole multiplet shares one value of total angular momentum
    (verified exactly in the tests; Griffiths 3e Eq. 4.118, p.205)."""
    x, y, z = Lx(l), Ly(l), Lz(l)
    return x @ x + y @ y + z @ z


def angular_momentum_set(l):
    """Convenience: all five operators (and the m list) for a given l as a dict
    with keys 'Lx','Ly','Lz','L+','L-','L2','m'."""
    return {"Lx": Lx(l), "Ly": Ly(l), "Lz": Lz(l),
            "L+": L_plus(l), "L-": L_minus(l), "L2": L_squared(l),
            "m": m_values(l)}


def commutator(A, B):
    """[A, B] = A B - B A  for two matrices."""
    return A @ B - B @ A


# --- 4. position-space eigenfunctions: spherical harmonics -------------------

def spherical_harmonic(l, m, theta, phi):
    """Spherical harmonic Y_l^m(theta, phi): the position-space simultaneous
    eigenfunction of L^2 and L_z (Griffiths 3e Eq. 4.32, p.178).  theta is the
    polar angle [0, pi], phi the azimuth [0, 2pi); both may be numpy arrays.

        Y_l^m = N_l^m P_l^m(cos theta) e^{i m phi},  m >= 0
        Y_l^{-m} = (-1)^m conj(Y_l^m)
        N_l^m = sqrt( (2l+1)/(4 pi) * (l-m)!/(l+m)! )

    P_l^m (with the Condon-Shortley phase) comes from ~MA-12's assoc_legendre, so
    this matches scipy.special.sph_harm_y (checked in the tests).

    Only INTEGER l have spherical harmonics: single-valuedness of e^{i m phi}
    under phi -> phi + 2pi forces m, hence l, to be an integer (Griffiths 3e
    Eq. 4.22, p.176).  The half-integer reps of the algebra (spin, ~QM-11) live
    only as matrices, with no wavefunction here -- hence the ValueError."""
    if abs(l - round(l)) > 1e-12:
        raise ValueError("spherical harmonics exist only for integer l "
                         "(half-integer l is spin -> ~QM-11, matrices only)")
    l = int(round(l))
    am = abs(int(round(m)))
    theta = np.asarray(theta, dtype=float)
    phi = np.asarray(phi, dtype=float)
    norm = math.sqrt((2 * l + 1) / (4.0 * math.pi)
                     * math.factorial(l - am) / math.factorial(l + am))
    cos_t = np.cos(theta)
    P = np.vectorize(lambda x: assoc_legendre(l, am, x))(cos_t)
    val = norm * P * np.exp(1j * am * phi)
    if m < 0:
        val = (-1) ** am * np.conj(val)
    return val


def _gauss_legendre(n):
    """Nodes/weights for Gauss-Legendre quadrature on [-1, 1]."""
    return np.polynomial.legendre.leggauss(n)


def sphere_inner_product(l1, m1, l2, m2, n_theta=24, n_phi=40):
    """The L^2(sphere) inner product

        <Y_{l1}^{m1} | Y_{l2}^{m2}> = int conj(Y1) Y2 sin(theta) dtheta dphi

    evaluated numerically: Gauss-Legendre in x = cos(theta) (exact for the
    polynomial theta-part) and a uniform grid in phi (exact for the e^{i k phi}
    azimuthal modes).  Should equal delta_{l1 l2} delta_{m1 m2} -- the
    orthonormality of the spherical harmonics (Griffiths 3e Eq. 4.33, p.178)."""
    xg, wg = _gauss_legendre(n_theta)
    phis = np.linspace(0.0, 2.0 * math.pi, n_phi, endpoint=False)
    dphi = 2.0 * math.pi / n_phi
    theta = np.arccos(xg)                       # x = cos theta ; sin th dth = -dx
    total = 0.0 + 0.0j
    for th, w in zip(theta, wg):
        y1 = spherical_harmonic(l1, m1, th, phis)
        y2 = spherical_harmonic(l2, m2, th, phis)
        total += w * np.sum(np.conj(y1) * y2) * dphi
    return total


def Lz_on_Y(l, m, theta, phi, h=1e-5):
    """Apply the position-space operator  L_z = -i hbar d/dphi  to Y_l^m at
    (theta, phi), by a central finite difference in phi.  Returns the array
    (-i hbar)(Y(phi+h) - Y(phi-h))/2h, which must equal hbar*m * Y_l^m -- i.e.
    Y_l^m is an L_z eigenfunction with eigenvalue hbar*m (Griffiths 3e Eq. 4.129,
    p.208).  Verified against m*Y in the tests."""
    fwd = spherical_harmonic(l, m, theta, phi + h)
    bwd = spherical_harmonic(l, m, theta, phi - h)
    return -1j * HBAR * (fwd - bwd) / (2.0 * h)


# --- demo --------------------------------------------------------------------

def _demo():
    np.set_printoptions(precision=3, suppress=True)
    print("QM-10 Angular momentum -- the algebra builds the spectrum\n")

    print("Matrix representation (hbar = 1):")
    for l in (0.5, 1.0, 1.5, 2.0):
        z = Lz(l)
        c = commutator(Lx(l), Ly(l))
        ok_alg = np.allclose(c, 1j * HBAR * z)
        ok_cas = np.allclose(L_squared(l), casimir_eigenvalue(l) * np.eye(dim(l)))
        spec = np.sort(np.linalg.eigvalsh(z).real)
        print(f"  l={l:>3}: dim {dim(l)}, L_z spectrum {spec},"
              f"  [Lx,Ly]=ihL_z {ok_alg},  L^2={l*(l+1):.2f}*I {ok_cas}")

    print("\n  l=1/2 is exactly spin-1/2:  2*L_x, 2*L_y, 2*L_z are the Pauli matrices")
    print("   2*L_y =\n", 2 * Ly(0.5))

    print("\nSpherical harmonics Y_l^m (integer l only -- e^{im phi} must close):")
    print("  Y_0^0 = %.5f (constant 1/sqrt(4pi) = %.5f)"
          % (spherical_harmonic(0, 0, 0.7, 1.1).real, 1.0 / math.sqrt(4 * math.pi)))
    print("  orthonormality  <Y_2^1|Y_2^1>  = %.6f   (expect 1)"
          % sphere_inner_product(2, 1, 2, 1).real)
    print("  orthogonality   <Y_1^0|Y_2^0>  = %.1e   (expect 0)"
          % abs(sphere_inner_product(1, 0, 2, 0)))
    lz = Lz_on_Y(3, -2, 0.6, 0.9)
    print("  L_z = -i hbar d/dphi  on Y_3^{-2}:  %.4f  vs  m*Y = %.4f"
          % (lz.real, (-2) * spherical_harmonic(3, -2, 0.6, 0.9).real))


if __name__ == "__main__":
    _demo()
