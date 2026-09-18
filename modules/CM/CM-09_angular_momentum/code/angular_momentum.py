"""
CM-09  Angular momentum & torque -- L = r x p, N = r x F, and dL/dt = N, with the
central-force conservation law.

Part of the physics topic network (modules/topic_network.txt, module CM-09).
Reuses ~MA-01 (`cross`) and ~CM-01 (`velocity`, `acceleration` of a trajectory);
links to ~CM-11 (central forces / Kepler) and ~QM-10 (quantum angular momentum).

NOTE: MA-01/CM-01 imported by relative path; becomes `from physkit...` later.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA01 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-01_vector_algebra", "code"))
_CM01 = os.path.abspath(os.path.join(_HERE, "..", "..", "CM-01_kinematics", "code"))
for _p in (_MA01, _CM01):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from vector_algebra import cross, norm    # noqa: E402
from kinematics import velocity, acceleration  # noqa: E402

__all__ = ["angular_momentum", "torque", "angular_momentum_of", "torque_rate"]


def angular_momentum(m, r, v):
    """L = r x p = m (r x v)  (reuses MA-01 cross)."""
    return tuple(m * c for c in cross(r, v))


def torque(r, F):
    """Torque (moment of force)  N = r x F."""
    return cross(r, F)


def angular_momentum_of(m, trajectory):
    """L(t) for a moving particle of mass m on trajectory r(t): the FUNCTION
    t -> m (r(t) x v(t)), using CM-01's velocity. (Demonstrates ~CM-01 reuse.)"""
    v = velocity(trajectory)
    return lambda t: tuple(m * c for c in cross(trajectory(t), v(t)))


def torque_rate(m, trajectory, h=1e-4):
    """The torque N = r x (m a) along a trajectory, which equals dL/dt
    (using CM-01's acceleration)."""
    a = acceleration(trajectory, h)
    return lambda t: cross(trajectory(t), tuple(m * c for c in a(t)))


# --- demo --------------------------------------------------------------------

def _demo():
    import math
    print("CM-09 angular momentum & torque -- demo")
    print("=" * 32)

    print("L for m=2 at r=(1,0,0), v=(0,3,0):", angular_momentum(2, (1, 0, 0), (0, 3, 0)), " (= (0,0,6))")
    print("torque of F=(0,5,0) at r=(2,0,0):", torque((2, 0, 0), (0, 5, 0)), " (= (0,0,10))")
    print("central force (F || r) gives zero torque:", torque((2, 1, 0), (-4, -2, 0)))

    # uniform circular motion: L is constant; for a central (centripetal) force dL/dt = 0
    R, w, m = 2.0, 3.0, 1.5
    circ = lambda t: (R * math.cos(w * t), R * math.sin(w * t), 0.0)
    L = angular_momentum_of(m, circ)
    print("\ncircular motion: L(0) =", tuple(round(c, 4) for c in L(0.0)),
          " L(1) =", tuple(round(c, 4) for c in L(1.0)), " (constant = m R^2 w =", m * R * R * w, ")")
    N = torque_rate(m, circ)
    print("  torque r x (m a) =", tuple(round(c, 4) for c in N(0.7)), " (~ 0, central force)")


if __name__ == "__main__":
    _demo()
