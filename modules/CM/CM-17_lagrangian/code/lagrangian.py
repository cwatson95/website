"""
CM-17  Lagrangian mechanics -- generalized coordinates, the Euler-Lagrange
equation, conjugate momenta, and the Jacobi energy.

Part of the physics topic network (modules/topic_network.txt, module CM-17).
Reuses ~MA-13 (`euler_lagrange_residual` -- the variational machinery IS
Lagrangian mechanics with t,q,q' for x,y,y') and ~MA-07 (integrator). Feeds
~CM-18 (Noether), ~CM-19 (Hamiltonian via Legendre).

A (1-DOF) Lagrangian is L(t, q, qdot). The Euler-Lagrange equation
   d/dt (dL/dqdot) - dL/dq = 0
is Newton's law in any coordinates; its residual is ~0 along a true trajectory.

NOTE: MA-13/MA-07 imported by relative path; becomes `from physkit...` later.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA13 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-13_calculus_of_variations", "code"))
_MA07 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-07_ode", "code"))
for _p in (_MA13, _MA07):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from variational import euler_lagrange_residual  # noqa: E402
from ode import integrate                        # noqa: E402

__all__ = [
    "el_residual", "generalized_momentum", "jacobi_energy", "integrate_eom",
]


def el_residual(L, ts, qs):
    """Euler-Lagrange residual at the interior nodes of a sampled trajectory q(t).
    L(t, q, qdot) is the mechanics Lagrangian (passed straight to MA-13). ~0 on a
    true path; large on a wrong one."""
    return euler_lagrange_residual(L, ts, qs)


def generalized_momentum(L, t, q, qdot, h=1e-6):
    """The conjugate (canonical) momentum  p = dL/dqdot."""
    return (L(t, q, qdot + h) - L(t, q, qdot - h)) / (2.0 * h)


def jacobi_energy(L, t, q, qdot, h=1e-6):
    """Jacobi energy integral  h = qdot (dL/dqdot) - L. For L = T - V this is T + V,
    and it is the Hamiltonian of ~CM-19."""
    return qdot * generalized_momentum(L, t, q, qdot, h) - L(t, q, qdot)


def integrate_eom(qddot, q0, qdot0, t0, t1, n):
    """Integrate a 1-DOF equation of motion qddot = f(t, q, qdot) (the EL equation
    solved for the acceleration), reusing MA-07. Returns (ts, [q, qdot] states)."""
    return integrate(lambda t, y: [y[1], qddot(t, y[0], y[1])], [q0, qdot0], t0, t1, n)


# --- demo --------------------------------------------------------------------

def _demo():
    import math
    print("CM-17 Lagrangian mechanics -- demo")
    print("=" * 32)

    w = 2.0
    L = lambda t, q, p: 0.5 * p * p - 0.5 * w * w * q * q          # SHO, m=1
    N = 400
    ts = [i * (2 * math.pi / w) / N for i in range(N + 1)]
    qs = [math.cos(w * t) for t in ts]
    print("SHO L = 1/2 q'^2 - 1/2 w^2 q^2, true q=cos(wt):")
    print(f"  max |EL residual| on true path = {max(abs(r) for r in el_residual(L, ts, qs)):.2e}  (~0)")
    print(f"  conjugate momentum p = dL/dq' at q'=3: {generalized_momentum(L, 0, 0, 3.0):.4f}  (= 3)")
    print(f"  Jacobi energy at q=1,q'=0: {jacobi_energy(L, 0, 1.0, 0.0):.4f}  (= 1/2 w^2 = 2)")

    # pendulum, derived EL equation theta'' = -(g/l) sin theta
    g, l = 9.81, 1.0
    Lp = lambda t, q, p: 0.5 * l * l * p * p + g * l * math.cos(q)
    ts, ys = integrate_eom(lambda t, q, qd: -(g / l) * math.sin(q), 0.5, 0.0, 0.0, 3.0, 3000)
    res = el_residual(Lp, ts, [s[0] for s in ys])
    print(f"\npendulum: max |EL residual| on the integrated trajectory = {max(abs(r) for r in res):.2e}")


if __name__ == "__main__":
    _demo()
