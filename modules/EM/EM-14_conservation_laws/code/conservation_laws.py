"""EM-14  EM conservation laws -- Poynting vector, field momentum, stress tensor.

Physics topic network, module EM-14 (modules/topic_network.txt).
Source: Griffiths 4e, Sect. 8.1-8.2.  Builds on ~EM-01 (EPS0), ~EM-08 (MU0),
~MA-01 (cross).  The electromagnetic field carries energy, momentum, and angular
momentum, and the bookkeeping closes (a continuity equation, KEY BRIDGE B2):

    u = (eps0/2)|E|^2 + (1/2 mu0)|B|^2                       (energy density, Eq. 8.13)
    S = (1/mu0) (E x B)                                      (energy flux, Eq. 8.10)
    g = eps0 (E x B) = S / c^2                               (momentum density, Eq. 8.30)
    T_ij = eps0(E_i E_j - 1/2 d_ij E^2) + (1/mu0)(B_i B_j - 1/2 d_ij B^2)   (stress, Eq. 8.19)

For a plane wave these collapse to S = c u and g = u/c, and an absorbing surface
feels a radiation pressure S/c (2S/c if it reflects).
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
from vector_algebra import cross, dot, norm                  # noqa: E402

C = 1.0 / math.sqrt(MU0 * EPS0)

__all__ = [
    "EPS0", "MU0", "C",
    "poynting_vector", "energy_density", "momentum_density",
    "maxwell_stress_tensor", "radiation_pressure", "plane_wave_snapshot",
]


# --- the densities and fluxes (Eq. 8.10, 8.13, 8.19, 8.30) -------------------

def poynting_vector(E, B):
    """Energy flux  S = (1/mu0)(E x B)  as a field function (reuses MA-01 cross)."""
    def S(x, y, z):
        return tuple(c / MU0 for c in cross(E(x, y, z), B(x, y, z)))
    return S


def energy_density(E, B):
    """Field energy density  u = (eps0/2)|E|^2 + (1/2 mu0)|B|^2  (Eq. 8.13)."""
    def u(x, y, z):
        e2 = dot(E(x, y, z), E(x, y, z))
        b2 = dot(B(x, y, z), B(x, y, z))
        return 0.5 * EPS0 * e2 + b2 / (2.0 * MU0)
    return u


def momentum_density(E, B):
    """Field momentum density  g = eps0 (E x B) = S / c^2  (Eq. 8.30)."""
    def g(x, y, z):
        return tuple(EPS0 * c for c in cross(E(x, y, z), B(x, y, z)))
    return g


def maxwell_stress_tensor(E, B):
    """Maxwell stress tensor T_ij (Eq. 8.19), as a field returning a 3x3 list.
    -T . da is the momentum per unit time crossing the surface element da."""
    def T(x, y, z):
        e = E(x, y, z)
        b = B(x, y, z)
        e2 = dot(e, e)
        b2 = dot(b, b)
        out = [[0.0] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                d = 1.0 if i == j else 0.0
                out[i][j] = (EPS0 * (e[i] * e[j] - 0.5 * d * e2)
                             + (b[i] * b[j] - 0.5 * d * b2) / MU0)
        return out
    return T


def radiation_pressure(S_mag, reflected=False):
    """Radiation pressure on a surface from a beam of intensity S_mag:
        P = S/c  (perfect absorber),   2S/c  (perfect reflector)."""
    return (2.0 if reflected else 1.0) * S_mag / C


# --- a plane-wave snapshot (E along x, B along y, B0 = E0/c) ------------------

def plane_wave_snapshot(E0, k, z_phase=0.0, c=C):
    """Snapshot fields of a +z plane wave at one instant (phase kz fixed):
        E = E0 cos(kz) xhat ,  B = (E0/c) cos(kz) yhat.  Returns (E, B)."""
    def E(x, y, z):
        return (E0 * math.cos(k * z + z_phase), 0.0, 0.0)

    def B(x, y, z):
        return (0.0, (E0 / c) * math.cos(k * z + z_phase), 0.0)
    return E, B


# --- demo --------------------------------------------------------------------

def _demo():
    print("EM-14 EM conservation laws -- demo")
    print("=" * 36)

    # a sunlight-strength plane wave: E0 ~ 1000 V/m
    E0 = 1000.0
    E, B = plane_wave_snapshot(E0, k=0.0)        # uniform snapshot at a crest
    S = poynting_vector(E, B)
    u = energy_density(E, B)
    g = momentum_density(E, B)
    p = (0.0, 0.0, 0.0)

    Smag, uval, gmag = norm(S(*p)), u(*p), norm(g(*p))
    print(f"plane wave E0 = {E0} V/m  (B0 = E0/c = {E0/C:.3e} T):")
    print(f"  S = (1/mu0) E x B = {S(*p)}  |S| = {Smag:.4e} W/m^2  (along +z)")
    print(f"  u = {uval:.4e} J/m^3     check S = c u: {C*uval:.4e}  (match)")
    print(f"  g = S/c^2: |g| = {gmag:.4e} kg/(m^2 s)   check u/c: {uval/C:.4e}")
    print(f"  radiation pressure: absorber {radiation_pressure(Smag):.4e} Pa, "
          f"reflector {radiation_pressure(Smag, True):.4e} Pa")

    # electric and magnetic energy are equal in a wave
    eE = 0.5 * EPS0 * E0 ** 2
    eB = (E0 / C) ** 2 / (2 * MU0)
    print(f"\nequipartition: electric u_E = {eE:.4e} = magnetic u_B = {eB:.4e}")

    # stress tensor: T_zz is the momentum flux along propagation
    T = maxwell_stress_tensor(E, B)(*p)
    print(f"\nMaxwell stress tensor T_zz = {T[2][2]:.4e}  (= -u, the radiation pressure term)")


if __name__ == "__main__":
    _demo()
