"""EM-06  Conductors & capacitance -- electrostatic energy two ways, capacitors.

Physics topic network, module EM-06 (modules/topic_network.txt).
Source: Griffiths 4e, Sect. 2.4 (energy) and 2.5 (conductors, capacitors).
Builds on ~EM-01 (fields) and ~EM-02 (the uniform-sphere field).

Energy lives either in the charges or in the field, and the two pictures agree:
    W = (1/2) sum_i q_i V_i              (Eq. 2.42, charge picture)
    W = (eps0/2) int |E|^2 dtau          (Eq. 2.45, field picture)
A conductor is an equipotential whose surface charge feels an outward pressure
P = eps0 E^2 / 2 (Eq. 2.51); a capacitor stores W = (1/2) C V^2 (Eq. 2.55).
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_EM01 = os.path.abspath(os.path.join(_HERE, "..", "..", "EM-01_electrostatics", "code"))
_EM02 = os.path.abspath(os.path.join(_HERE, "..", "..", "EM-02_gauss_law", "code"))
for _p in (_EM01, _EM02):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from electrostatics import EPS0, K_E, field_magnitude         # noqa: E402
from gauss_law import uniform_sphere_field                    # noqa: E402

__all__ = [
    "work_to_assemble", "field_energy_density", "field_energy",
    "field_energy_spherical", "self_energy_uniform_sphere",
    "capacitance_parallel_plate", "capacitance_isolated_sphere",
    "capacitance_spherical", "capacitance_cylindrical",
    "energy_stored", "surface_pressure",
]


# --- energy: the charge picture (Eq. 2.42) -----------------------------------

def work_to_assemble(charges):
    """Work to assemble point charges (Eq. 2.42), as the pairwise sum
        W = (1/4 pi eps0) sum_{i<j} q_i q_j / r_ij ,
    which is the finite (1/2) sum_i q_i V_i with self-energy excluded."""
    cs = list(charges)
    W = 0.0
    for i in range(len(cs)):
        qi, ri = cs[i]
        for j in range(i + 1, len(cs)):
            qj, rj = cs[j]
            d = math.sqrt(sum((ri[k] - rj[k]) ** 2 for k in range(3)))
            W += K_E * qi * qj / d
    return W


# --- energy: the field picture (Eq. 2.45) ------------------------------------

def field_energy_density(E):
    """Energy density u = (eps0/2) |E|^2  as a scalar field (reuses EM-01 norm)."""
    mag = field_magnitude(E)
    return lambda x, y, z: 0.5 * EPS0 * mag(x, y, z) ** 2


def field_energy(E, x0, x1, y0, y1, z0, z1, n=20):
    """W = (eps0/2) int |E|^2 dtau over a box, by midpoint quadrature.
    Exact for a uniform field (e.g. between capacitor plates)."""
    u = field_energy_density(E)
    dx, dy, dz = (x1 - x0) / n, (y1 - y0) / n, (z1 - z0) / n
    dV = dx * dy * dz
    total = 0.0
    for i in range(n):
        xs = x0 + (i + 0.5) * dx
        for j in range(n):
            ys = y0 + (j + 0.5) * dy
            for k in range(n):
                zs = z0 + (k + 0.5) * dz
                total += u(xs, ys, zs) * dV
    return total


def field_energy_spherical(Emag, r0, r1, n=20000):
    """W = (eps0/2) int |E(r)|^2 4 pi r^2 dr  for a radial field, 1-D quadrature.
    Lets the energy integral run out to large r cheaply (the 1/r^4 tail)."""
    dr = (r1 - r0) / n
    total = 0.0
    for i in range(n):
        r = r0 + (i + 0.5) * dr
        total += 0.5 * EPS0 * Emag(r) ** 2 * 4.0 * math.pi * r * r * dr
    return total


def self_energy_uniform_sphere(Q, R):
    """Closed-form field energy of a uniformly charged solid sphere (Eq. 2.45
    worked for the uniform sphere):  W = (3/5)(1/4 pi eps0) Q^2 / R."""
    return 0.6 * K_E * Q * Q / R


# --- capacitance of the standard geometries (Sect. 2.5.4) --------------------

def capacitance_parallel_plate(A, d):
    """Parallel-plate capacitor (Eq. 2.54):  C = eps0 A / d."""
    return EPS0 * A / d


def capacitance_isolated_sphere(R):
    """Isolated conducting sphere:  C = 4 pi eps0 R."""
    return 4.0 * math.pi * EPS0 * R


def capacitance_spherical(a, b):
    """Spherical capacitor, inner radius a, outer b > a:  C = 4 pi eps0 a b /(b-a).
    Reduces to the isolated sphere 4 pi eps0 a as b -> infinity."""
    return 4.0 * math.pi * EPS0 * a * b / (b - a)


def capacitance_cylindrical(a, b, L):
    """Coaxial cylinders, radii a < b, length L:  C = 2 pi eps0 L / ln(b/a)."""
    return 2.0 * math.pi * EPS0 * L / math.log(b / a)


# --- capacitor energy and surface pressure -----------------------------------

def energy_stored(C, V):
    """Energy in a charged capacitor (Eq. 2.55):  W = (1/2) C V^2."""
    return 0.5 * C * V * V


def surface_pressure(sigma):
    """Outward electrostatic pressure on a conductor surface (Eq. 2.51):
        P = sigma^2 / (2 eps0) = eps0 E^2 / 2,   with E = sigma/eps0 just outside."""
    return sigma * sigma / (2.0 * EPS0)


# --- demo --------------------------------------------------------------------

def _demo():
    print("EM-06 conductors & capacitance -- demo")
    print("=" * 40)

    # energy two ways for a uniform sphere
    Q, R = 1e-9, 0.05
    Emag = lambda r: field_magnitude(uniform_sphere_field(Q, R))(r, 0, 0)
    Wfield = field_energy_spherical(Emag, 0.0, 2000 * R)
    Wclosed = self_energy_uniform_sphere(Q, R)
    print(f"uniform sphere Q={Q:.0e} C, R={R} m:")
    print(f"  field-energy integral (eps0/2 int E^2) = {Wfield:.5e} J")
    print(f"  closed form (3/5) k Q^2 / R            = {Wclosed:.5e} J")

    # parallel-plate capacitor: field energy == (1/2) C V^2
    A, d, V = 0.01, 1e-3, 12.0
    C = capacitance_parallel_plate(A, d)
    Efield = V / d
    Euniform = lambda x, y, z: (0.0, 0.0, Efield)
    side = math.sqrt(A)
    Wbox = field_energy(Euniform, 0, side, 0, side, 0, d, n=8)
    print(f"\nparallel plate A={A} m^2, d={d} m, V={V} V:")
    print(f"  C = eps0 A/d = {C:.4e} F     (1/2)CV^2 = {energy_stored(C, V):.4e} J")
    print(f"  field energy in the gap     = {Wbox:.4e} J")

    print("\ncapacitances:")
    print(f"  isolated sphere R=5cm: C = {capacitance_isolated_sphere(0.05):.4e} F")
    print(f"  coax a=1mm b=3mm L=1m: C = {capacitance_cylindrical(1e-3, 3e-3, 1.0):.4e} F")

    sigma = 1e-6
    print(f"\nconductor surface sigma={sigma:.0e}: outward pressure = {surface_pressure(sigma):.4e} Pa")


if __name__ == "__main__":
    _demo()
