"""EM-10  Magnetic materials -- magnetization, bound currents, the H field.

Physics topic network, module EM-10 (modules/topic_network.txt).
Source: Griffiths 4e, Ch. 6.  Builds on ~EM-08 (mu0, the magnetostatic laws) and
~MA-01 / ~MA-02 (cross for K_b, curl for J_b).

A magnetized object carries bound currents
    J_b = curl M     (Eq. 6.13)        K_b = M x nhat   (Eq. 6.14),
the magnetic mirror of ~EM-07's bound charge.  Folding them into Ampere's law
defines the auxiliary field
    H = B/mu0 - M    (Eq. 6.18)   ->   oint H.dl = I_free,enc   (Eq. 6.20),
sourced by free current alone.  Linear media give M = chi_m H, B = mu H with
mu = mu0(1 + chi_m) (Eq. 6.29-6.33); ferromagnets instead show hysteresis.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_EM08 = os.path.abspath(os.path.join(_HERE, "..", "..", "EM-08_magnetostatics", "code"))
if _EM08 not in sys.path:
    sys.path.insert(0, _EM08)

from magnetostatics import MU0                              # noqa: E402
from vector_algebra import cross, norm                      # noqa: E402
from vector_calculus import curl                            # noqa: E402

__all__ = [
    "bound_volume_current", "bound_surface_current", "auxiliary_field_H",
    "magnetization_linear", "permeability", "B_linear", "classify_material",
    "magnetized_sphere_inner_B", "magnetized_sphere_inner_H",
    "hysteresis_branches", "remanence", "coercivity",
]


# --- bound currents (Eq. 6.13-6.14) ------------------------------------------

def bound_volume_current(M_field, point):
    """Bound volume current density  J_b = curl M  (Eq. 6.13), via MA-02 curl.
    Zero wherever M is uniform."""
    x, y, z = point
    return curl(M_field)(x, y, z)


def bound_surface_current(M, normal):
    """Bound surface current density  K_b = M x nhat  (Eq. 6.14), via MA-01 cross.
    For a cylinder uniformly magnetized along its axis this is M phi-hat -- the
    object is equivalent to a solenoid."""
    return cross(M, normal)


# --- the auxiliary field H (Eq. 6.18) ----------------------------------------

def auxiliary_field_H(B, M):
    """H = B/mu0 - M  (Eq. 6.18), from field functions B and M."""
    def H(x, y, z):
        bx, by, bz = B(x, y, z)
        mx, my, mz = M(x, y, z)
        return (bx / MU0 - mx, by / MU0 - my, bz / MU0 - mz)
    return H


# --- linear media (Eq. 6.29-6.33) --------------------------------------------

def magnetization_linear(chi_m, H):
    """M = chi_m H  for a linear magnetic medium (Eq. 6.29)."""
    return lambda x, y, z: tuple(chi_m * c for c in H(x, y, z))


def permeability(chi_m):
    """Permeability  mu = mu0 (1 + chi_m)  (Eq. 6.33)."""
    return MU0 * (1.0 + chi_m)


def B_linear(chi_m, H):
    """B = mu H  for a linear medium (Eq. 6.31)."""
    mu = permeability(chi_m)
    return lambda x, y, z: tuple(mu * c for c in H(x, y, z))


def classify_material(chi_m):
    """Name the magnetic class from the susceptibility sign/size (Sect. 6.4):
    chi_m < 0 diamagnetic; small chi_m > 0 paramagnetic; large/nonlinear ferromagnetic."""
    if chi_m < 0.0:
        return "diamagnetic"
    if chi_m < 1.0:
        return "paramagnetic"
    return "ferromagnetic"


# --- the uniformly magnetized sphere (Sect. 6.2 example) ---------------------

def magnetized_sphere_inner_B(M):
    """Uniform B INSIDE a uniformly magnetized sphere:  B = (2/3) mu0 M (Eq. 6.16)."""
    return tuple((2.0 / 3.0) * MU0 * c for c in M)


def magnetized_sphere_inner_H(M):
    """Uniform H inside the same sphere:  H = B/mu0 - M = - M/3  (the demagnetizing field)."""
    return tuple(-c / 3.0 for c in M)


# --- ferromagnetism: a toy hysteresis loop (Sect. 6.4.2) ---------------------

def hysteresis_branches(Ms, Hc, width):
    """Two-branch tanh model of a hysteresis loop.

    Returns (M_up, M_down): the ascending branch (field increasing) is shifted to
    +Hc, the descending branch to -Hc, so the loop is open -- the signature of a
    ferromagnet (history-dependent M).  Ms = saturation, Hc ~ coercivity scale.
    """
    M_up = lambda H: Ms * math.tanh((H - Hc) / width)       # field swept upward
    M_down = lambda H: Ms * math.tanh((H + Hc) / width)     # field swept downward
    return M_up, M_down


def remanence(Ms, Hc, width):
    """Remanent magnetization: |M| left at H = 0 (descending branch)."""
    _, M_down = hysteresis_branches(Ms, Hc, width)
    return abs(M_down(0.0))


def coercivity(Ms, Hc, width):
    """Coercive field: the H at which the descending-branch M crosses zero (= -Hc)."""
    return Hc


# --- demo --------------------------------------------------------------------

def _demo():
    print("EM-10 magnetic materials -- demo")
    print("=" * 34)

    # bound currents of a magnetized cylinder, M = M zhat
    Mz = 1e4
    M_uniform = lambda x, y, z: (0.0, 0.0, Mz)
    print(f"uniformly magnetized cylinder, M = {Mz:.0e} A/m zhat:")
    print(f"  J_b = curl M (interior) = {tuple(round(c,3) for c in bound_volume_current(M_uniform,(0.1,0.2,0.0)))}  (= 0, uniform)")
    Kb = bound_surface_current((0, 0, Mz), (1, 0, 0))       # side surface, nhat = s-hat
    print(f"  K_b = M x nhat (side)   = {Kb}  (= M phi-hat, |K_b| = {norm(Kb):.0e} = M -> a solenoid)")

    # non-uniform M does carry volume current: M = (-a y, a x, 0) -> J_b = 2a zhat
    a = 5.0
    M_rot = lambda x, y, z: (-a * y, a * x, 0.0)
    print(f"  swirling M=(-a y, a x,0), a={a}: J_b = {tuple(round(c,3) for c in bound_volume_current(M_rot,(0.3,0.1,0.0)))}  (= 2a zhat = {2*a})")

    # linear media
    print("\nlinear media (chi_m):")
    for chi in (-1.7e-5, 2.5e-4, 5500.0):
        print(f"  chi_m = {chi:>10}: {classify_material(chi):>13}, mu/mu0 = {permeability(chi)/MU0:.4g}")

    # uniformly magnetized sphere
    Msph = (0.0, 0.0, 8e5)
    Bin = magnetized_sphere_inner_B(Msph)
    Hin = magnetized_sphere_inner_H(Msph)
    print(f"\nmagnetized sphere M=8e5 zhat:")
    print(f"  B_in = (2/3)mu0 M = {Bin[2]:.4e} T     H_in = -M/3 = {Hin[2]:.4e} A/m")
    print(f"  check B = mu0(H+M): {MU0*(Hin[2]+Msph[2]):.4e} T  (matches B_in)")

    # hysteresis
    Ms, Hc, w = 8e5, 5e3, 2e3
    print(f"\nferromagnet hysteresis (Ms={Ms:.0e}, Hc={Hc:.0e}):")
    print(f"  remanence M_r = {remanence(Ms,Hc,w):.3e} A/m  (M left at H=0)")
    print(f"  coercivity H_c = {coercivity(Ms,Hc,w):.3e} A/m  (H to demagnetize)")


if __name__ == "__main__":
    _demo()
