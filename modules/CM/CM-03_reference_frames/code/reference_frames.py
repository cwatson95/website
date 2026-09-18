"""
CM-03  Reference frames -- Galilean transformations between inertial frames, and
the centre-of-mass (C) frame.

Part of the physics topic network (modules/topic_network.txt, module CM-03).
Pure vector arithmetic (pairs with ~MA-01); links to ~RE-01 (where the Galilean
rule fails) and ~CM-07/~CM-08 (the CM frame for collisions).

A Galilean boost to a frame moving at constant velocity V (coincident origins at
t=0):  r' = r - V t,  v' = v - V,  with time and acceleration unchanged.
Pure stdlib.
"""

__all__ = [
    "galilean_position", "galilean_velocity", "relative_velocity",
    "cm_velocity", "to_cm_frame", "total_momentum",
]


def galilean_position(r, V, t):
    """Position in a frame moving at constant velocity V (origins coincide at t=0)."""
    return [r[i] - V[i] * t for i in range(3)]


def galilean_velocity(v, V):
    """Velocity transform between inertial frames:  v' = v - V."""
    return [v[i] - V[i] for i in range(3)]


def relative_velocity(v_a, v_b):
    """Velocity of A as seen from B:  v_A - v_B  (antisymmetric)."""
    return [v_a[i] - v_b[i] for i in range(3)]


def total_momentum(masses, velocities):
    """Total linear momentum sum_i m_i v_i."""
    P = [0.0, 0.0, 0.0]
    for m, v in zip(masses, velocities):
        for i in range(3):
            P[i] += m * v[i]
    return P


def cm_velocity(masses, velocities):
    """Velocity of the centre of mass:  V_cm = (sum m_i v_i) / (sum m_i)."""
    M = sum(masses)
    P = total_momentum(masses, velocities)
    return [P[i] / M for i in range(3)]


def to_cm_frame(masses, velocities):
    """Velocities seen in the centre-of-mass frame (total momentum there is zero)."""
    V = cm_velocity(masses, velocities)
    return [galilean_velocity(v, V) for v in velocities]


# --- demo --------------------------------------------------------------------

def _demo():
    print("CM-03 reference frames -- demo")
    print("=" * 32)

    v = [3.0, 0.0, 0.0]
    V = [1.0, 0.0, 0.0]
    print("galilean velocity:  v=(3,0,0) seen from a frame moving at (1,0,0) ->", galilean_velocity(v, V))

    masses = [2.0, 1.0]
    vels = [[1.0, 0.0, 0.0], [-2.0, 0.0, 0.0]]
    print("\ntwo bodies m=[2,1], v=[(1,0,0),(-2,0,0)]:")
    print("  V_cm           =", cm_velocity(masses, vels))
    print("  velocities in C-frame =", to_cm_frame(masses, vels))
    print("  total P in C-frame    =", [round(c, 12) for c in total_momentum(masses, to_cm_frame(masses, vels))], "(= 0)")


if __name__ == "__main__":
    _demo()
