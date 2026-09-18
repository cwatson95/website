"""EM-07  Dielectrics & polarization -- bound charge, the D field, linear media.

Physics topic network, module EM-07 (modules/topic_network.txt).
Source: Griffiths 4e, Ch. 4.  Builds on ~EM-01 (Coulomb field), ~EM-02 (flux),
and ~MA-02 (divergence for the bound volume charge).

A polarized dielectric carries bound charge
    sigma_b = P . nhat        (Eq. 4.11)        rho_b = - div P   (Eq. 4.12)
which is real charge that sources E.  Folding it into Gauss's law defines the
electric displacement
    D = eps0 E + P            (Eq. 4.21)   ->   oint D . da = Q_free   (Eq. 4.23),
so D is sourced by FREE charge alone.  In a linear dielectric P = eps0 chi_e E,
hence D = eps E with eps = eps0(1 + chi_e) (Eq. 4.30-4.34).
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

from electrostatics import EPS0, K_E, coulomb_field            # noqa: E402
from gauss_law import flux_through_sphere                      # noqa: E402
from vector_algebra import dot, norm                           # noqa: E402
from vector_calculus import divergence                         # noqa: E402

__all__ = [
    "bound_surface_charge", "bound_volume_charge",
    "displacement_field", "displacement_point_free_charge", "free_charge_enclosed",
    "permittivity", "susceptibility_from_eps_r", "polarization_linear",
    "displacement_linear", "capacitance_with_dielectric",
    "polarized_sphere_inner_field", "polarized_sphere_surface_charge",
]


# --- bound charge (Eq. 4.11-4.12) --------------------------------------------

def bound_surface_charge(P, normal):
    """Bound surface density  sigma_b = P . nhat  (Eq. 4.11).
    P and normal are 3-tuples (P constant over the face)."""
    return dot(P, normal)


def bound_volume_charge(P_field, point):
    """Bound volume density  rho_b = - div P  (Eq. 4.12), via MA-02 divergence.
    Zero wherever P is uniform."""
    x, y, z = point
    return -divergence(P_field)(x, y, z)


# --- the displacement field D = eps0 E + P (Eq. 4.21, 4.23) ------------------

def displacement_field(E, P):
    """D = eps0 E + P  as a field function, from field functions E and P."""
    def D(x, y, z):
        ex, ey, ez = E(x, y, z)
        px, py, pz = P(x, y, z)
        return (EPS0 * ex + px, EPS0 * ey + py, EPS0 * ez + pz)
    return D


def displacement_point_free_charge(q_free):
    """D of a free point charge embedded in (linear, homogeneous) dielectric:
        D = q_free / (4 pi r^2) rhat   -- independent of the medium.
    Built by rescaling the EM-01 vacuum Coulomb field by eps0."""
    Evac = coulomb_field([(q_free, (0.0, 0.0, 0.0))])

    def D(x, y, z):
        ex, ey, ez = Evac(x, y, z)
        return (EPS0 * ex, EPS0 * ey, EPS0 * ez)
    return D


def free_charge_enclosed(D, center=(0.0, 0.0, 0.0), R=1.0, n=80):
    """Free charge inside a sphere, from Gauss for D:  Q_free = oint D . da
    (Eq. 4.23). Reuses EM-02's flux integral on the D field."""
    return flux_through_sphere(D, center, R, n)


# --- linear dielectrics (Eq. 4.30-4.34) --------------------------------------

def permittivity(eps_r):
    """Permittivity from the dielectric constant:  eps = eps0 eps_r."""
    return EPS0 * eps_r


def susceptibility_from_eps_r(eps_r):
    """Electric susceptibility:  chi_e = eps_r - 1  (Eq. 4.34)."""
    return eps_r - 1.0


def polarization_linear(eps_r, E):
    """P = eps0 chi_e E  for a linear dielectric (Eq. 4.30)."""
    chi = susceptibility_from_eps_r(eps_r)

    def P(x, y, z):
        ex, ey, ez = E(x, y, z)
        return (EPS0 * chi * ex, EPS0 * chi * ey, EPS0 * chi * ez)
    return P


def displacement_linear(eps_r, E):
    """D = eps E  for a linear dielectric (Eq. 4.32)."""
    eps = permittivity(eps_r)
    return lambda x, y, z: tuple(eps * c for c in E(x, y, z))


def capacitance_with_dielectric(C_vacuum, eps_r):
    """Filling a capacitor with a linear dielectric multiplies C by eps_r."""
    return eps_r * C_vacuum


# --- the uniformly polarized sphere (Sect. 4.2 example) ----------------------

def polarized_sphere_inner_field(P):
    """Uniform field INSIDE a uniformly polarized sphere:  E = - P / (3 eps0).
    A constant field opposing P (the classic depolarizing field)."""
    return tuple(-c / (3.0 * EPS0) for c in P)


def polarized_sphere_surface_charge(P_mag):
    """Bound surface charge on a uniformly polarized sphere (P along z):
        sigma_b(theta) = P cos(theta)  (Eq. 4.11 with nhat = rhat)."""
    return lambda theta: P_mag * math.cos(theta)


# --- demo --------------------------------------------------------------------

def _demo():
    print("EM-07 dielectrics & polarization -- demo")
    print("=" * 42)

    # uniformly polarized slab: bound charge only on the faces
    P = (0.0, 0.0, 2e-6)
    print("uniformly polarized slab, P = 2e-6 zhat C/m^2:")
    print(f"  sigma_b on top face (n=+z)    = {bound_surface_charge(P, (0,0,1)):.2e} C/m^2  (= +P)")
    print(f"  sigma_b on bottom face (n=-z) = {bound_surface_charge(P, (0,0,-1)):.2e} C/m^2  (= -P)")
    Pfield = lambda x, y, z: P
    print(f"  rho_b = -div P inside         = {bound_volume_charge(Pfield, (0.1, 0.2, 0.3)):.2e}  (= 0, uniform)")

    # Gauss for D: free point charge in a dielectric
    qf = 5e-9
    D = displacement_point_free_charge(qf)
    print(f"\nfree charge q_f = 5 nC in a dielectric:")
    print(f"  oint D.da through a sphere = {free_charge_enclosed(D, R=0.2):.4e} C  (= q_f, medium-independent)")

    # linear dielectric relations
    eps_r = 4.0
    print(f"\nlinear dielectric eps_r = {eps_r}:")
    print(f"  chi_e = eps_r - 1 = {susceptibility_from_eps_r(eps_r)}")
    E = coulomb_field([(qf, (0, 0, 0))])
    p = (0.1, 0, 0)
    Plin, Dlin = polarization_linear(eps_r, E), displacement_linear(eps_r, E)
    Dchk = displacement_field(E, Plin)                     # eps0 E + P should equal eps E
    print(f"  D = eps E      at {p}: {Dlin(*p)[0]:.4e}")
    print(f"  D = eps0 E + P at {p}: {Dchk(*p)[0]:.4e}  (consistent)")

    # uniformly polarized sphere
    Psph = (0.0, 0.0, 1e-6)
    print(f"\nuniformly polarized sphere, P=1e-6 zhat:")
    print(f"  inner field E = -P/3eps0 = {polarized_sphere_inner_field(Psph)[2]:.4e} V/m (along -z)")


if __name__ == "__main__":
    _demo()
