"""
CM-12  Non-inertial (rotating) frames -- the centrifugal and Coriolis
accelerations.

Part of the physics topic network (modules/topic_network.txt, module CM-12).
Reuses ~MA-01 (`cross`); builds on ~CM-03 (frames) and ~CM-10 (circular motion).

In a frame rotating at angular velocity omega, a particle feels fictitious
accelerations in addition to the real force/m:
    a_inertial = a_rot + 2 omega x v_rot + omega x (omega x r) + omega_dot x r,
so the apparent (rotating-frame) acceleration carries the **centrifugal** term
-omega x (omega x r) and the **Coriolis** term -2 omega x v_rot.

NOTE: MA-01 imported by relative path; becomes `from physkit...` later.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA01 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-01_vector_algebra", "code"))
if _MA01 not in sys.path:
    sys.path.insert(0, _MA01)

from vector_algebra import cross, dot, norm  # noqa: E402

__all__ = [
    "centrifugal_acceleration", "coriolis_acceleration",
    "centrifugal_force", "coriolis_force", "euler_acceleration",
]


def centrifugal_acceleration(omega, r):
    """-omega x (omega x r): points outward, magnitude omega^2 * (perp distance)."""
    return tuple(-c for c in cross(omega, cross(omega, r)))


def coriolis_acceleration(omega, v):
    """-2 omega x v: perpendicular to both omega and the rotating-frame velocity v."""
    return tuple(-2.0 * c for c in cross(omega, v))


def euler_acceleration(omega_dot, r):
    """-omega_dot x r: the azimuthal (Euler) term when the rotation rate changes."""
    return tuple(-c for c in cross(omega_dot, r))


def centrifugal_force(m, omega, r):
    return tuple(m * c for c in centrifugal_acceleration(omega, r))


def coriolis_force(m, omega, v):
    return tuple(m * c for c in coriolis_acceleration(omega, v))


# --- demo --------------------------------------------------------------------

def _demo():
    print("CM-12 rotating frames -- demo")
    print("=" * 32)
    omega = (0.0, 0.0, 2.0)                       # spin about z
    r = (3.0, 0.0, 0.0)
    ac = centrifugal_acceleration(omega, r)
    print("centrifugal at r=(3,0,0), omega=2 z:", tuple(round(c, 4) for c in ac),
          " (outward, |a|=omega^2 rho =", 2.0 ** 2 * 3.0, ")")
    v = (0.0, 1.0, 0.0)
    acor = coriolis_acceleration(omega, v)
    print("Coriolis for v=(0,1,0):", tuple(round(c, 4) for c in acor),
          " perp to omega? ", round(dot(acor, omega), 12), " perp to v?", round(dot(acor, v), 12))


if __name__ == "__main__":
    _demo()
