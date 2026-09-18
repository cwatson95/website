"""
CM-02  Equation of motion -- Newton's second law as an ODE, integrated for the
trajectory of a particle under a force.

Part of the physics topic network (modules/topic_network.txt, module CM-02).
Reuses ~MA-07 (the RK4 integrator) and the kinematics of ~CM-01; feeds ~CM-04
(work-energy), ~CM-05 (potential energy), ~CM-06 (momentum).

Newton's 2nd law  m d^2 r/dt^2 = F(t, r, v)  is a second-order ODE. We pack the
state as y = [x, y, z, vx, vy, vz] and hand d y/dt = [v, F/m] to MA-07's
`integrate`. A `force` is a callable force(t, r, v) -> (Fx, Fy, Fz).

NOTE: MA-07 imported by relative path; becomes `from physkit...` later.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA07 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-07_ode", "code"))
if _MA07 not in sys.path:
    sys.path.insert(0, _MA07)

from ode import integrate  # noqa: E402

__all__ = [
    "newton_rhs", "trajectory",
    "constant_force", "uniform_gravity", "spring_force", "linear_drag", "sum_forces",
]


def newton_rhs(force, mass):
    """The first-order RHS for m r'' = F: state [r, v] -> [v, F/m]."""
    def rhs(t, y):
        r, v = y[0:3], y[3:6]
        F = force(t, r, v)
        return [v[0], v[1], v[2], F[0] / mass, F[1] / mass, F[2] / mass]
    return rhs


def trajectory(force, mass, r0, v0, t0, t1, n):
    """Integrate the equation of motion. Returns (ts, rs, vs) with rs, vs lists of 3-vectors."""
    ts, ys = integrate(newton_rhs(force, mass), list(r0) + list(v0), t0, t1, n)
    return ts, [y[0:3] for y in ys], [y[3:6] for y in ys]


# --- a small library of forces (each returns force(t, r, v) -> vector) -------

def constant_force(F):
    """A constant applied force F."""
    return lambda t, r, v: list(F)


def uniform_gravity(mass, g=9.81, direction=(0.0, 0.0, -1.0)):
    """Weight m g in the given direction (default -z)."""
    return lambda t, r, v: [mass * g * d for d in direction]


def spring_force(k, r_eq=(0.0, 0.0, 0.0)):
    """Hooke's law about r_eq:  F = -k (r - r_eq)."""
    return lambda t, r, v: [-k * (r[i] - r_eq[i]) for i in range(3)]


def linear_drag(b):
    """Linear (Stokes) drag  F = -b v."""
    return lambda t, r, v: [-b * v[i] for i in range(3)]


def sum_forces(*forces):
    """Free-body: the net force is the sum of several forces."""
    def net(t, r, v):
        total = [0.0, 0.0, 0.0]
        for f in forces:
            F = f(t, r, v)
            for i in range(3):
                total[i] += F[i]
        return total
    return net


# --- demo --------------------------------------------------------------------

def _demo():
    import math
    print("CM-02 equation of motion -- demo")
    print("=" * 32)

    m = 2.0
    ts, rs, vs = trajectory(uniform_gravity(m), m, (0, 0, 0), (10, 0, 10), 0.0, 2.0, 1000)
    print("projectile (m=2, v0=(10,0,10)):  r(2s) =", tuple(round(c, 3) for c in rs[-1]))

    k = 8.0
    m = 0.5
    ts, rs, vs = trajectory(spring_force(k), m, (1, 0, 0), (0, 0, 0), 0.0, 5.0, 4000)
    w = math.sqrt(k / m)
    print(f"spring (k=8,m=0.5,w={w:.3f}):  x(5s) numeric {rs[-1][0]:.4f}  vs cos(w*5) {math.cos(w*5):.4f}")

    ts, rs, vs = trajectory(sum_forces(uniform_gravity(1.0), linear_drag(0.5)), 1.0,
                            (0, 0, 0), (0, 0, 0), 0.0, 30.0, 4000)
    print(f"falling with drag: terminal v_z = {vs[-1][2]:.4f}  (expect -m g/b = {-9.81 / 0.5:.4f})")


if __name__ == "__main__":
    _demo()
