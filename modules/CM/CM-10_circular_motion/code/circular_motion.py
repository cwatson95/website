"""
CM-10  Centripetal & circular motion -- uniform circular motion and the
centripetal acceleration a = v^2/r, with the link back to ~CM-01's curvature.

Part of the physics topic network (modules/topic_network.txt, module CM-10).
Reuses ~CM-01 (`speed`, `curvature`, `normal_acceleration`) and ~MA-01 (`norm`);
builds on ~CM-02 (the centripetal force that produces it). For a circle of
radius R the curvature is 1/R and the inward acceleration is v^2/R = omega^2 R.

NOTE: MA-01/CM-01 imported by relative path; becomes `from physkit...` later.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA01 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-01_vector_algebra", "code"))
_CM01 = os.path.abspath(os.path.join(_HERE, "..", "..", "CM-01_kinematics", "code"))
for _p in (_MA01, _CM01):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from vector_algebra import norm  # noqa: E402

__all__ = [
    "uniform_circular", "centripetal_acceleration", "centripetal_force",
    "period", "frequency", "angular_velocity",
]


def uniform_circular(R, omega, phase=0.0):
    """Trajectory of uniform circular motion in the xy-plane: r(t)."""
    return lambda t: (R * math.cos(omega * t + phase), R * math.sin(omega * t + phase), 0.0)


def centripetal_acceleration(v, R):
    """Inward (centripetal) acceleration  a_c = v^2 / R."""
    return v * v / R


def centripetal_force(m, v, R):
    """The force needed to hold a mass on the circle:  F_c = m v^2 / R."""
    return m * v * v / R


def period(omega):
    """Period of circular motion  T = 2 pi / omega."""
    return 2.0 * math.pi / omega


def frequency(omega):
    """Frequency  f = omega / 2 pi = 1 / T."""
    return omega / (2.0 * math.pi)


def angular_velocity(T):
    """Angular velocity from the period  omega = 2 pi / T."""
    return 2.0 * math.pi / T


# --- demo --------------------------------------------------------------------

def _demo():
    from kinematics import speed, curvature, normal_acceleration   # CM-01 reuse
    print("CM-10 centripetal & circular motion -- demo")
    print("=" * 32)

    R, w = 2.0, 3.0
    v = R * w
    print(f"R={R}, omega={w}:  v = R*omega = {v}")
    print(f"  centripetal accel v^2/R = {centripetal_acceleration(v, R)}  (= omega^2 R = {w * w * R})")
    print(f"  period T = {period(w):.4f}  frequency f = {frequency(w):.4f}")

    circ = uniform_circular(R, w)
    print("\ncross-check via CM-01 on the trajectory:")
    print(f"  speed(circ)(0.6)        = {speed(circ)(0.6):.4f}   (= R*omega = {v})")
    print(f"  curvature(circ)(0.6)    = {curvature(circ)(0.6):.4f}   (= 1/R = {1 / R})")
    print(f"  normal_accel(circ)(0.6) = {normal_acceleration(circ)(0.6):.4f}   (= v^2/R = {v * v / R})")
    print(f"  |r| stays = R:           {norm(circ(0.6)):.4f}")


if __name__ == "__main__":
    _demo()
