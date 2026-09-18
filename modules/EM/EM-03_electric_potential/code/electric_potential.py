"""EM-03  Electric potential -- V, the V<->E relations, Poisson & Laplace.

Physics topic network, module EM-03 (modules/topic_network.txt).
Source: Griffiths 4e, Sect. 2.3.  Builds on ~EM-01 (point-charge fields) and
~MA-02 (line_integral for V = -int E.dl, gradient for E = -grad V, laplacian
for Poisson's equation).

Because the electrostatic field is curl-free (~EM-02), it has a scalar potential:
    V(r) = - int_ref^r E . dl        (Eq. 2.21)          -- path-independent
    E    = - grad V                   (Eq. 2.23)
    grad^2 V = - rho / eps0           (Eq. 2.24, Poisson;  = 0 in vacuum, Laplace)
The two MA-02 operators invert each other here: differentiate V to get back the
exact EM-01 field, integrate E to recover V.  V is a scalar -> superposition is
ordinary addition, which is why potential is the easier road to the field.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_EM01 = os.path.abspath(os.path.join(_HERE, "..", "..", "EM-01_electrostatics", "code"))
if _EM01 not in sys.path:
    sys.path.insert(0, _EM01)

from electrostatics import EPS0, K_E, point_charge_field, coulomb_field  # noqa: E402
from vector_calculus import line_integral, gradient, laplacian          # noqa: E402

__all__ = [
    "potential_point_charges", "potential_of_charge",
    "potential_from_field", "field_from_potential",
    "poisson_residual",
]


# --- potential of point charges (Eq. 2.29, superposition) --------------------

def potential_of_charge(q, source=(0.0, 0.0, 0.0)):
    """Potential of one point charge:  V = (1/4 pi eps0) q / r  (zero at infinity)."""
    sx, sy, sz = source

    def V(x, y, z):
        r = math.sqrt((x - sx) ** 2 + (y - sy) ** 2 + (z - sz) ** 2)
        return math.inf if r == 0.0 else K_E * q / r
    return V


def potential_point_charges(charges):
    """Superposed potential of (q, position) point charges -- scalar addition."""
    terms = [potential_of_charge(q, pos) for (q, pos) in charges]
    return lambda x, y, z: sum(V(x, y, z) for V in terms)


# --- the two field<->potential relations (Eq. 2.21, 2.23) --------------------

def potential_from_field(E, reference=(10.0, 0.0, 0.0), n=4000):
    """V(r) = - int_ref^r E . dl  along the straight segment ref -> r (Eq. 2.21).

    Returns a potential field with V(reference) = 0.  Path-independence (curl E = 0)
    is what makes the straight-line choice legitimate; reuses MA-02 line_integral.
    """
    rx, ry, rz = reference

    def V(x, y, z):
        def path(t):                                       # ref -> (x,y,z), t in [0,1]
            return (rx + t * (x - rx), ry + t * (y - ry), rz + t * (z - rz))
        return -line_integral(E, path, 0.0, 1.0, n)
    return V


def field_from_potential(V):
    """E = - grad V  (Eq. 2.23) -- MA-02 gradient, negated, as a field function."""
    g = gradient(V)

    def E(x, y, z):
        gx, gy, gz = g(x, y, z)
        return (-gx, -gy, -gz)
    return E


# --- Poisson / Laplace (Eq. 2.24-2.25) ---------------------------------------

def poisson_residual(V, rho, point):
    """Poisson check at `point`:  (grad^2 V + rho/eps0), normalized.

    In vacuum rho = 0 and this is Laplace's equation grad^2 V = 0; the returned
    number is the finite-difference residual divided by the natural curvature
    scale |V|/L^2, so truncation error reads as a pure (dimensionless) number.
    """
    x, y, z = point
    lap = laplacian(V)(x, y, z)
    resid = lap + rho / EPS0
    L = math.sqrt(x * x + y * y + z * z) or 1.0
    scale = abs(V(x, y, z)) / L ** 2
    return resid / scale if scale > 0 else resid


# --- demo --------------------------------------------------------------------

def _demo():
    print("EM-03 electric potential -- demo")
    print("=" * 32)

    q = 2e-9
    V = potential_of_charge(q)
    Eexact = point_charge_field(q)
    print("point charge q = 2 nC:")
    print(f"  V at r=0.5 m = {V(0.5, 0, 0):.4f} V   (k q / r = {K_E*q/0.5:.4f})")

    # E = -grad V recovers the EM-01 field
    Egrad = field_from_potential(V)
    p = (0.3, 0.2, -0.1)
    print("\nE = -grad V  vs  EM-01 Coulomb field at", p, ":")
    print("  -grad V =", tuple(f"{c:.3f}" for c in Egrad(*p)))
    print("  Coulomb =", tuple(f"{c:.3f}" for c in Eexact(*p)))

    # V = -int E.dl recovers the potential difference
    Vint = potential_from_field(Eexact, reference=(10.0, 0.0, 0.0))
    closed = V(*p) - V(10.0, 0.0, 0.0)
    print(f"\nV(P) - V(ref) by line integral = {Vint(*p):.5f} V   (closed form {closed:.5f})")

    # Laplace in vacuum
    print(f"\nLaplace check (vacuum):  (grad^2 V)/scale = {poisson_residual(V, 0.0, p):.2e}  (-> 0)")

    # superposition is just addition
    Vd = potential_point_charges([(q, (-0.05, 0, 0)), (-q, (0.05, 0, 0))])
    print(f"\ndipole potential on the axis at x=0.2: V = {Vd(0.2, 0, 0):.4f} V "
          f"(antisymmetric: V at x=-0.2 = {Vd(-0.2, 0, 0):.4f})")


if __name__ == "__main__":
    _demo()
