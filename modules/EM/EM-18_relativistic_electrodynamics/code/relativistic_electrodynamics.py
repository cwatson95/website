"""EM-18  Relativistic electrodynamics -- the field tensor, transforming E & B.

Physics topic network, module EM-18 (modules/topic_network.txt).
Source: Griffiths 4e, Sect. 12.3.  Builds on ~EM-01/~EM-08 (EPS0, MU0 -> c) and
~MA-01 (dot); the tensor machinery is ~MA-16, the covariant viewpoint ~RE-08.

E and B are not separate things but components of one antisymmetric field tensor
(Eq. 12.118, with c):
    F^{0i} = E_i / c ,   F^{ij} = -eps_{ijk} B_k .
A Lorentz boost mixes them (Eq. 12.109) -- so a pure electric field in one frame
carries a magnetic field in another (magnetism is electrostatics + relativity,
Sect. 12.3.1).  Two combinations are boost-invariant:
    E . B          and        B^2 - E^2/c^2
(from F_{mn}F^{mn} and F_{mn}G^{mn}).  Covariant Maxwell reads d_mu F^{mu nu} = mu0 J^nu.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_EM01 = os.path.abspath(os.path.join(_HERE, "..", "..", "EM-01_electrostatics", "code"))
_EM08 = os.path.abspath(os.path.join(_HERE, "..", "..", "EM-08_magnetostatics", "code"))
for _p in (_EM01, _EM08):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from electrostatics import EPS0                              # noqa: E402
from magnetostatics import MU0                               # noqa: E402
from vector_algebra import dot                               # noqa: E402

C = 1.0 / math.sqrt(MU0 * EPS0)

__all__ = [
    "C", "gamma", "field_tensor", "fields_from_tensor",
    "boost_fields", "field_invariants", "is_antisymmetric",
]


def gamma(beta):
    """Lorentz factor  gamma = 1/sqrt(1 - beta^2),  beta = v/c."""
    return 1.0 / math.sqrt(1.0 - beta * beta)


# --- the field tensor F^{mu nu} (Eq. 12.118) ---------------------------------

def field_tensor(E, B, c=C):
    """Contravariant field tensor F^{mu nu} (Griffiths Eq. 12.118):
        rows/cols ordered (ct, x, y, z); F^{0i} = E_i/c, F^{ij} = -eps_ijk B_k.
    Antisymmetric 4x4 (list of lists)."""
    Ex, Ey, Ez = E
    Bx, By, Bz = B
    return [
        [0.0,      Ex / c,  Ey / c,  Ez / c],
        [-Ex / c,  0.0,     Bz,     -By],
        [-Ey / c, -Bz,      0.0,     Bx],
        [-Ez / c,  By,     -Bx,      0.0],
    ]


def fields_from_tensor(F, c=C):
    """Inverse of `field_tensor`: read (E, B) back off F^{mu nu}."""
    E = (F[0][1] * c, F[0][2] * c, F[0][3] * c)
    B = (F[2][3], F[3][1], F[1][2])               # Bx=F^{yz}, By=F^{zx}, Bz=F^{xy}
    return E, B


def is_antisymmetric(F, tol=1e-12):
    """True if F^{mu nu} = -F^{nu mu} (and the diagonal vanishes)."""
    for i in range(4):
        for j in range(4):
            if abs(F[i][j] + F[j][i]) > tol:
                return False
    return True


# --- how the fields transform under a boost (Eq. 12.109) ---------------------

def boost_fields(E, B, beta, c=C):
    """Transform (E, B) to a frame S' moving at speed v = beta c along +x
    (Griffiths Eq. 12.109):
        E'_x = E_x,            B'_x = B_x,
        E'_y = g(E_y - v B_z), B'_y = g(B_y + (v/c^2) E_z),
        E'_z = g(E_z + v B_y), B'_z = g(B_z - (v/c^2) E_y)."""
    g = gamma(beta)
    v = beta * c
    Ex, Ey, Ez = E
    Bx, By, Bz = B
    Ep = (Ex, g * (Ey - v * Bz), g * (Ez + v * By))
    Bp = (Bx, g * (By + (v / c ** 2) * Ez), g * (Bz - (v / c ** 2) * Ey))
    return Ep, Bp


# --- the Lorentz invariants (Sect. 12.3.3, Prob. 12.47) ----------------------

def field_invariants(E, B, c=C):
    """The two boost-invariant scalars of the field:
        I1 = E . B                (pseudoscalar, from F_{mn} G^{mn})
        I2 = B^2 - E^2 / c^2      (scalar, from F_{mn} F^{mn}).
    Returns (I1, I2)."""
    I1 = dot(E, B)
    I2 = dot(B, B) - dot(E, E) / c ** 2
    return I1, I2


# --- demo --------------------------------------------------------------------

def _demo():
    print("EM-18 relativistic electrodynamics -- demo")
    print("=" * 44)

    E = (0.0, 1000.0, 0.0)        # pure electric field, transverse to the boost
    B = (0.0, 0.0, 0.0)
    print(f"rest frame:  E = {E} V/m,  B = {B} T")
    F = field_tensor(E, B)
    print(f"  field tensor antisymmetric: {is_antisymmetric(F)}")
    print(f"  round-trip fields_from_tensor: {fields_from_tensor(F)[0]} , {fields_from_tensor(F)[1]}")

    beta = 0.6
    Ep, Bp = boost_fields(E, B, beta)
    print(f"\nboosted to v = {beta}c along x (gamma = {gamma(beta):.4f}):")
    print(f"  E' = {tuple(round(c,2) for c in Ep)} V/m")
    print(f"  B' = {tuple(f'{c:.3e}' for c in Bp)} T   <-- a magnetic field appears!")
    print("  (a pure E field in one frame is E and B in another: magnetism = relativity)")

    I1, I2 = field_invariants(E, B)
    I1p, I2p = field_invariants(Ep, Bp)
    print(f"\nLorentz invariants (must be unchanged):")
    print(f"  E.B:          rest {I1:.6e}   boosted {I1p:.6e}")
    print(f"  B^2 - E^2/c^2: rest {I2:.6e}   boosted {I2p:.6e}")


if __name__ == "__main__":
    _demo()
