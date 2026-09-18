"""EM-01  Electrostatics -- Coulomb's law, the electric field, superposition.

Physics topic network, module EM-01 (modules/topic_network.txt).
Source: Griffiths, *Introduction to Electrodynamics*, 4th ed., Sect. 2.1.
Builds on ~MA-01 (vector algebra: norm, unit, cross, dot).

A field is returned as a FUNCTION  E(x, y, z) -> (Ex, Ey, Ez), exactly the
MA-02 convention -- so MA-02's differential operators act on these fields with
no glue code:  curl(E) == 0  and  divergence(E) == 0 in vacuum are the curl-E
and divergence-E theorems of ~EM-02, checked here against the same E.

A "charge" is a pair  (q, position)  with q in coulombs and position a 3-tuple
in metres (SI throughout).

NOTE: MA-01 / MA-02 are imported by relative path (becomes `from physkit...`
once a shared package exists). This module also puts MA-02 on sys.path so
importers can `from vector_calculus import curl, divergence`.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA01 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-01_vector_algebra", "code"))
_MA02 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-02_vector_calculus", "code"))
for _p in (_MA01, _MA02):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from vector_algebra import norm, unit, dot  # noqa: E402

__all__ = [
    "EPS0", "K_E", "ELEM_CHARGE",
    "point_charge_field", "coulomb_field", "force_on_charge",
    "field_magnitude", "field_line_direction", "field_of_distribution",
]

# --- physical constants (SI, CODATA) -----------------------------------------
EPS0 = 8.8541878128e-12              # vacuum permittivity  [C^2 N^-1 m^-2]
K_E = 1.0 / (4.0 * math.pi * EPS0)   # Coulomb constant ~ 8.9875e9 [N m^2 C^-2]
ELEM_CHARGE = 1.602176634e-19        # elementary charge e  [C]


# --- the electric field of point charges (Griffiths Eq. 2.3-2.4) -------------

def point_charge_field(q, source=(0.0, 0.0, 0.0)):
    """E of a single point charge q at `source`.

    Coulomb / Eq. 2.4 :  E(r) = (1/4 pi eps0) q / r^2  rhat ,  r = field - source.
    Returns a field function E(x, y, z) -> (Ex, Ey, Ez); +/-inf at the charge.
    """
    sx, sy, sz = source

    def E(x, y, z):
        rx, ry, rz = x - sx, y - sy, z - sz
        r2 = rx * rx + ry * ry + rz * rz
        if r2 == 0.0:
            inf = float("inf")
            return (math.copysign(inf, q) if q else 0.0,) * 3
        r = math.sqrt(r2)
        c = K_E * q / (r2 * r)        # k q / r^3, so c * r_vec = k q / r^2 * rhat
        return (c * rx, c * ry, c * rz)
    return E


def coulomb_field(charges):
    """Superposed field of an iterable of (q, position) point charges (Eq. 2.4).

    Superposition is just the vector sum of the individual point-charge fields.
    """
    fields = [point_charge_field(q, pos) for (q, pos) in charges]

    def E(x, y, z):
        ex = ey = ez = 0.0
        for f in fields:
            fx, fy, fz = f(x, y, z)
            ex += fx
            ey += fy
            ez += fz
        return (ex, ey, ez)
    return E


def force_on_charge(Q, E):
    """Force on a test charge Q sitting in field E:  F = Q E   (Eq. 2.3).

    `E` is a field function; returns the force field F(x, y, z) -> (Fx, Fy, Fz).
    """
    def F(x, y, z):
        ex, ey, ez = E(x, y, z)
        return (Q * ex, Q * ey, Q * ez)
    return F


# --- derived scalar / direction fields (reuse MA-01) -------------------------

def field_magnitude(E):
    """|E|(x, y, z) as a scalar field -- MA-01 `norm` applied to the field."""
    return lambda x, y, z: norm(E(x, y, z))


def field_line_direction(E):
    """Unit field-line direction Ehat = E/|E| -- MA-01 `unit` applied to E."""
    return lambda x, y, z: unit(E(x, y, z))


# --- continuous charge distributions (Griffiths Eq. 2.8) ---------------------

def field_of_distribution(rho, x0, x1, y0, y1, z0, z1, n=16):
    """E of a continuous density rho(x,y,z) over a box, by midpoint quadrature
    of Eq. 2.8:  E = (1/4 pi eps0) int rhat / r^2  rho dtau'.

    Implemented by lumping each cell into a point charge q = rho*dV and reusing
    `coulomb_field` -- coarse, but converges to a point charge k Q / r^2 far away
    (this is the shell-theorem / monopole limit tested in test_electrostatics).
    """
    dx, dy, dz = (x1 - x0) / n, (y1 - y0) / n, (z1 - z0) / n
    dV = dx * dy * dz
    charges = []
    for i in range(n):
        xs = x0 + (i + 0.5) * dx
        for j in range(n):
            ys = y0 + (j + 0.5) * dy
            for k in range(n):
                zs = z0 + (k + 0.5) * dz
                q = rho(xs, ys, zs) * dV
                if q != 0.0:
                    charges.append((q, (xs, ys, zs)))
    return coulomb_field(charges)


# --- demo --------------------------------------------------------------------

def _demo():
    from vector_calculus import curl, divergence    # ~MA-02, acting on EM fields
    print("EM-01 electrostatics -- demo")
    print("=" * 32)

    # one proton: field at the Bohr radius
    a0 = 5.29177e-11
    Ep = point_charge_field(ELEM_CHARGE)
    print("proton field at a0 = 5.29e-11 m:")
    print(f"  |E| = {field_magnitude(Ep)(a0, 0, 0):.3e} V/m   (= k e / a0^2 = {K_E*ELEM_CHARGE/a0**2:.3e})")

    # superposition: two equal charges -> zero field at the midpoint
    pair = coulomb_field([(1e-9, (-0.01, 0, 0)), (1e-9, (0.01, 0, 0))])
    print("\ntwo equal +1 nC charges at x = +/-1 cm:")
    print("  E at midpoint =", tuple(round(c, 9) for c in pair(0, 0, 0)), " (= 0 by symmetry)")

    # the field is curl-free and divergence-free away from the charges (~EM-02).
    # Report the residual relative to the gradient scale |E|/r (a pure number).
    q1 = point_charge_field(2e-9, (0.0, 0.0, 0.0))
    p = (0.4, 0.3, -0.2)
    scale = field_magnitude(q1)(*p) / norm(p)
    print("\nstructure of a point-charge field at", p, "(~EM-02):")
    print(f"  |curl E| / (|E|/r) = {norm(curl(q1)(*p)) / scale:.2e}   (-> 0, irrotational)")
    print(f"  |div  E| / (|E|/r) = {abs(divergence(q1)(*p)) / scale:.2e}   (-> 0, charge-free / Laplace)")

    # continuous: a small uniformly charged cube looks like a point charge far off
    L, rho0 = 0.002, 1e-3
    Q = rho0 * L ** 3
    Ecube = field_of_distribution(lambda x, y, z: rho0, -L / 2, L / 2, -L / 2, L / 2, -L / 2, L / 2, n=12)
    r = 0.2
    got = field_magnitude(Ecube)(r, 0, 0)
    print(f"\nuniform cube (Q = {Q:.2e} C) at r = {r} m:")
    print(f"  |E| = {got:.4e}   point-charge k Q / r^2 = {K_E*Q/r**2:.4e}")


if __name__ == "__main__":
    _demo()
