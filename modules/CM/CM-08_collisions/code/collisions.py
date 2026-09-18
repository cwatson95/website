"""
CM-08  Collisions & scattering -- elastic and inelastic collisions, the
centre-of-mass connection, and Rutherford scattering.

Part of the physics topic network (modules/topic_network.txt, module CM-08).
Reuses ~CM-07 (`cm_velocity`, `reduced_mass`); builds on ~CM-06 (momentum) and
~CM-04 (energy); links to ~QM-18 (quantum scattering).

NOTE: CM-07 imported by relative path; becomes `from physkit...` later.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CM07 = os.path.abspath(os.path.join(_HERE, "..", "..", "CM-07_centre_of_mass", "code"))
if _CM07 not in sys.path:
    sys.path.insert(0, _CM07)

from centre_of_mass import cm_velocity, reduced_mass  # noqa: E402

__all__ = [
    "elastic_collision_1d", "inelastic_collision",
    "kinetic_energy_1d", "rutherford_angle", "rutherford_cross_section", "reduced_mass",
]


def elastic_collision_1d(m1, v1, m2, v2):
    """Final velocities of a 1-D elastic collision (conserves p and kinetic energy)."""
    M = m1 + m2
    v1p = ((m1 - m2) * v1 + 2.0 * m2 * v2) / M
    v2p = ((m2 - m1) * v2 + 2.0 * m1 * v1) / M
    return v1p, v2p


def inelastic_collision(m1, v1, m2, v2):
    """Perfectly inelastic collision: the bodies stick and move with the common
    velocity (which is exactly the centre-of-mass velocity, reused from ~CM-07)."""
    return cm_velocity([m1, m2], [v1, v2])


def kinetic_energy_1d(m, v):
    return 0.5 * m * v * v


def rutherford_angle(b, E, k):
    """Scattering angle for a repulsive 1/r^2 (Coulomb) force of strength k, given
    impact parameter b and energy E:  theta = 2 arctan( k / (2 E b) ).
    (Equivalently b = (k/2E) cot(theta/2).)"""
    return 2.0 * math.atan(k / (2.0 * E * b))


def rutherford_cross_section(theta, E, k):
    """The Rutherford differential cross-section  dsigma/dOmega = (k/4E)^2 / sin^4(theta/2)."""
    return (k / (4.0 * E)) ** 2 / math.sin(theta / 2.0) ** 4


# --- demo --------------------------------------------------------------------

def _demo():
    print("CM-08 collisions & scattering -- demo")
    print("=" * 32)
    print("equal-mass elastic head-on (v1=3,v2=-1):", elastic_collision_1d(1, 3, 1, -1), " (velocities swap)")
    print("ball off a wall (m2=1e9, v2=0, v1=2):", tuple(round(c, 4) for c in elastic_collision_1d(1, 2, 1e9, 0)), " (~ -2, ~0)")
    print("perfectly inelastic m=[2,1], v=[(4,0,0),(0,0,0)]:", inelastic_collision(2, [4, 0, 0], 1, [0, 0, 0]))

    E, k, b = 1.0, 1.0, 0.5
    th = rutherford_angle(b, E, k)
    print(f"\nRutherford: b={b}, E={E}, k={k} -> theta = {math.degrees(th):.1f} deg")
    print(f"  dsigma/dOmega(theta) = {rutherford_cross_section(th, E, k):.5f}")
    print(f"  cross-section diverges forward: dsigma/dOmega(1 deg) = {rutherford_cross_section(math.radians(1), E, k):.1f}")


if __name__ == "__main__":
    _demo()
