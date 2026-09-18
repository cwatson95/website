"""
CM-19  Hamiltonian mechanics -- the Hamiltonian H(q, p), Hamilton's equations,
and phase-space flow.

Part of the physics topic network (modules/topic_network.txt, module CM-19).
Reuses ~MA-07 (the integrator); the Legendre transform connects to ~CM-17
(Lagrangian); feeds ~CM-20 (Poisson brackets) and ~QM-05 (the quantum analogue).

From the Lagrangian, H = p qdot - L is a function of (q, p), and the dynamics
become the first-order, symmetric **Hamilton's equations**
    qdot = +dH/dp,    pdot = -dH/dq.

NOTE: MA-07 imported by relative path; becomes `from physkit...` later.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA07 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-07_ode", "code"))
if _MA07 not in sys.path:
    sys.path.insert(0, _MA07)

from ode import integrate  # noqa: E402

__all__ = ["hamilton_rhs", "integrate_hamilton", "hamiltonian_from_potential"]


def hamilton_rhs(H, h=1e-6):
    """Hamilton's equations as a first-order RHS on the phase point [q, p]:
       qdot = dH/dp,  pdot = -dH/dq   (1 DOF, autonomous H(q, p))."""
    def rhs(t, y):
        q, p = y
        dHdp = (H(q, p + h) - H(q, p - h)) / (2.0 * h)
        dHdq = (H(q + h, p) - H(q - h, p)) / (2.0 * h)
        return [dHdp, -dHdq]
    return rhs


def integrate_hamilton(H, q0, p0, t0, t1, n):
    """Integrate the phase-space flow of H. Returns (ts, [q, p] states)."""
    return integrate(hamilton_rhs(H), [q0, p0], t0, t1, n)


def hamiltonian_from_potential(m, V):
    """Legendre transform of L = 1/2 m qdot^2 - V(q):  H(q, p) = p^2/(2m) + V(q)."""
    return lambda q, p: p * p / (2.0 * m) + V(q)


# --- demo --------------------------------------------------------------------

def _demo():
    import math
    print("CM-19 Hamiltonian mechanics -- demo")
    print("=" * 32)
    w = 2.0
    H = hamiltonian_from_potential(1.0, lambda q: 0.5 * w * w * q * q)   # SHO, m=1
    ts, ys = integrate_hamilton(H, 1.0, 0.0, 0.0, 2 * math.pi, 8000)
    print("SHO H = p^2/2 + 1/2 w^2 q^2 (w=2), start (q,p)=(1,0):")
    print(f"  q(pi/2) = {ys[len(ys) // 4][0]:+.5f}  (cos(2*pi/2)=cos(pi)... sampled)")
    print(f"  H: {H(*ys[0]):.6f} -> {H(*ys[-1]):.6f}  (conserved energy = 1/2 w^2 = 2)")
    # phase-space orbit is a closed ellipse p^2 + w^2 q^2 = w^2
    vals = [s[1] ** 2 + w * w * s[0] ** 2 for s in ys[::500]]
    print(f"  p^2 + w^2 q^2 along orbit: {[round(v, 4) for v in vals]}  (= w^2 = 4)")


if __name__ == "__main__":
    _demo()
