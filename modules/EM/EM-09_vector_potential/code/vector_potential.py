"""EM-09  Magnetic vector potential -- B = curl A, the Coulomb gauge, m.

Physics topic network, module EM-09 (modules/topic_network.txt).
Source: Griffiths 4e, Sect. 5.4.  Builds on ~EM-08 (the wire/loop fields it must
reproduce) and ~MA-02 (curl to take B = curl A, divergence to test the gauge).

Because div B = 0 (~EM-08), B derives from a vector potential:
    B = curl A          (Eq. 5.59),   with the gauge freedom A -> A + grad lambda.
The Coulomb gauge div A = 0 (Eq. 5.61) makes grad^2 A = -mu0 J (Eq. 5.63), the
vector Poisson equation.  A magnetic dipole m = I a (Eq. 5.86) has
    A_dip = (mu0 / 4 pi) m x rhat / r^2     (Eq. 5.85),
whose curl is the dipole B field -- structurally identical to the electric
dipole of ~EM-05 with (1/4 pi eps0, p) -> (mu0/4 pi, m).
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_EM08 = os.path.abspath(os.path.join(_HERE, "..", "..", "EM-08_magnetostatics", "code"))
if _EM08 not in sys.path:
    sys.path.insert(0, _EM08)

from magnetostatics import MU0, infinite_wire_field          # noqa: E402
from vector_algebra import cross, dot, norm, unit            # noqa: E402
from vector_calculus import curl, divergence                 # noqa: E402

__all__ = [
    "magnetic_dipole_moment", "dipole_vector_potential", "dipole_B_field_closed",
    "B_from_A", "coulomb_gauge_residual", "wire_vector_potential",
]


# --- the magnetic moment (Eq. 5.86) ------------------------------------------

def magnetic_dipole_moment(I, area_vector):
    """Magnetic dipole moment  m = I a  (current x oriented area), a 3-tuple."""
    return tuple(I * c for c in area_vector)


# --- the dipole vector potential and its field (Eq. 5.85) --------------------

def dipole_vector_potential(m):
    """A of a magnetic dipole m at the origin (Eq. 5.85):
        A = (mu0 / 4 pi) (m x rhat) / r^2 = (mu0/4pi)(m x r)/r^3."""
    pref = MU0 / (4.0 * math.pi)

    def A(x, y, z):
        r = norm((x, y, z))
        if r == 0.0:
            return (0.0, 0.0, 0.0)
        mxr = cross(m, (x, y, z))
        return tuple(pref * c / r ** 3 for c in mxr)
    return A


def dipole_B_field_closed(m):
    """Closed-form dipole field (curl of A_dip):
        B = (mu0 / 4 pi) (1/r^3) [ 3 (m.rhat) rhat - m ]   (cf. ~EM-05 Eq. 3.104)."""
    pref = MU0 / (4.0 * math.pi)

    def B(x, y, z):
        rv = (x, y, z)
        r = norm(rv)
        if r == 0.0:
            return (math.inf, math.inf, math.inf)
        rh = unit(rv)
        mr = dot(m, rh)
        return tuple(pref / r ** 3 * (3.0 * mr * rh[i] - m[i]) for i in range(3))
    return B


# --- B = curl A, and the gauge condition (Eq. 5.59, 5.61) --------------------

def B_from_A(A):
    """B = curl A  (Eq. 5.59) -- MA-02 curl applied to the vector potential."""
    return curl(A)


def coulomb_gauge_residual(A, point):
    """Coulomb-gauge check  div A = 0 (Eq. 5.61), normalized by |A|/r so the
    finite-difference residual reads as a pure number."""
    x, y, z = point
    r = norm(point) or 1.0
    scale = norm(A(x, y, z)) / r
    d = divergence(A)(x, y, z)
    return d / scale if scale > 0 else d


# --- the infinite wire, as a vector-potential problem (Sect. 5.4.1) ----------

def wire_vector_potential(I, s0=1.0):
    """A of an infinite straight wire on the z-axis:  A = - (mu0 I / 2 pi) ln(s/s0) zhat
    (s = cylindrical radius).  Its curl is the EM-08 wire field, independent of s0."""
    c = MU0 * I / (2.0 * math.pi)

    def A(x, y, z):
        s = math.sqrt(x * x + y * y)
        if s == 0.0:
            return (0.0, 0.0, 0.0)
        return (0.0, 0.0, -c * math.log(s / s0))
    return A


# --- demo --------------------------------------------------------------------

def _demo():
    print("EM-09 magnetic vector potential -- demo")
    print("=" * 40)

    # a small current loop = a magnetic dipole
    I, R = 3.0, 0.02
    m = magnetic_dipole_moment(I, (0.0, 0.0, math.pi * R ** 2))    # m = I * area zhat
    print(f"loop I={I} A, R={R} m  ->  m = {tuple(f'{c:.3e}' for c in m)} A m^2")

    A = dipole_vector_potential(m)
    B_num = B_from_A(A)
    B_exact = dipole_B_field_closed(m)
    print("\nB = curl A  vs  closed-form dipole field:")
    for p in [(0.1, 0.0, 0.0), (0.05, 0.05, 0.1)]:
        bn, be = B_num(*p), B_exact(*p)
        print(f"  at {p}:")
        print(f"    curl A     = {tuple(f'{c:.3e}' for c in bn)}")
        print(f"    closed form= {tuple(f'{c:.3e}' for c in be)}")
    print(f"\nCoulomb gauge: (div A)/scale = {coulomb_gauge_residual(A, (0.1, 0.05, 0.08)):.2e}  (-> 0)")

    # the infinite wire from its vector potential
    Iw = 10.0
    Aw = wire_vector_potential(Iw)
    Bw_num = B_from_A(Aw)
    Bw_exact = infinite_wire_field(Iw)
    p = (0.05, 0.0, 0.0)
    print(f"\ninfinite wire I={Iw} A:  B = curl A  vs  EM-08 field at {p}:")
    print(f"  curl A   = {tuple(f'{c:.4e}' for c in Bw_num(*p))}")
    print(f"  EM-08    = {tuple(f'{c:.4e}' for c in Bw_exact(*p))}")


if __name__ == "__main__":
    _demo()
