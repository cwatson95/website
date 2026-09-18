"""
CM-06  Linear momentum -- p = m v, impulse J = integral F dt, and conservation
of total momentum.

Part of the physics topic network (modules/topic_network.txt, module CM-06).
Pure vector arithmetic; links to ~CM-02 (impulse = Delta p from F=dp/dt),
~CM-07 (centre of mass), ~CM-08 (collisions). Pure stdlib.
"""

__all__ = ["momentum", "total_momentum", "impulse"]


def momentum(m, v):
    """Linear momentum  p = m v."""
    return [m * v[i] for i in range(3)]


def total_momentum(masses, velocities):
    """Total momentum of a system,  P = sum_i m_i v_i."""
    P = [0.0, 0.0, 0.0]
    for m, v in zip(masses, velocities):
        for i in range(3):
            P[i] += m * v[i]
    return P


def impulse(force, t0, t1, n=2000):
    """Impulse  J = integral_{t0}^{t1} F(t) dt  (trapezoidal). By Newton's 2nd law
    this equals the change in momentum, Delta p. `force` is force(t) -> vector."""
    dt = (t1 - t0) / n
    J = [0.0, 0.0, 0.0]
    for k in range(n + 1):
        w = 0.5 if k in (0, n) else 1.0
        Ft = force(t0 + k * dt)
        for i in range(3):
            J[i] += w * Ft[i]
    return [j * dt for j in J]


# --- demo --------------------------------------------------------------------

def _demo():
    print("CM-06 linear momentum -- demo")
    print("=" * 32)
    print("p for m=2, v=(3,0,-1):", momentum(2.0, (3.0, 0.0, -1.0)))
    print("total P of m=[2,1], v=[(1,0,0),(-2,0,0)]:", total_momentum([2.0, 1.0], [[1, 0, 0], [-2, 0, 0]]))

    # impulse of a constant force, and of a time-varying force
    print("J of F=(3,0,0) over [0,2]:", [round(c, 6) for c in impulse(lambda t: (3.0, 0.0, 0.0), 0.0, 2.0)], "(= (6,0,0))")
    print("J of F=(t,0,0) over [0,2]:", [round(c, 6) for c in impulse(lambda t: (t, 0.0, 0.0), 0.0, 2.0)], "(= (2,0,0))")

    # Newton's third law: equal & opposite internal impulses -> total P conserved
    f = lambda t: (5.0 * t, 0.0, 0.0)
    J1 = impulse(f, 0.0, 1.0)
    J2 = impulse(lambda t: [-c for c in f(t)], 0.0, 1.0)
    print("internal J1 + J2 =", [round(J1[i] + J2[i], 12) for i in range(3)], "(= 0, momentum conserved)")


if __name__ == "__main__":
    _demo()
