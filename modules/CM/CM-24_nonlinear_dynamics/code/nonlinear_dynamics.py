"""
CM-24  Nonlinear dynamics & chaos -- fixed points and their stability, limit
cycles, and sensitive dependence.

Part of the physics topic network (modules/topic_network.txt, module CM-24).
This is the mechanics application of ~MA-22 (dynamical systems): we build the
Jacobian of a physical flow and reuse `classify_equilibrium`; we integrate with
~MA-07; and the chaos diagnostic reuses MA-22's logistic-map Lyapunov exponent.

A planar flow is f(x, y) -> (xdot, ydot).

NOTE: MA-22/MA-07 imported by relative path; becomes `from physkit...` later.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA22 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-22_topology_dynamical_systems", "code"))
_MA07 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-07_ode", "code"))
for _p in (_MA22, _MA07):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from topo_dynamics import classify_equilibrium, lyapunov_logistic  # noqa: E402
from ode import integrate                                          # noqa: E402

__all__ = [
    "jacobian", "classify_fixed_point", "integrate_flow",
    "pendulum_flow", "van_der_pol", "lyapunov_logistic",
]


def jacobian(f, point, h=1e-6):
    """The 2x2 Jacobian of a planar flow f at `point` (numerical)."""
    x, y = point
    fxp, fxm = f(x + h, y), f(x - h, y)
    fyp, fym = f(x, y + h), f(x, y - h)
    return [[(fxp[0] - fxm[0]) / (2 * h), (fyp[0] - fym[0]) / (2 * h)],
            [(fxp[1] - fxm[1]) / (2 * h), (fyp[1] - fym[1]) / (2 * h)]]


def classify_fixed_point(f, point):
    """Linear-stability type of a fixed point, by reusing MA-22's
    `classify_equilibrium` on the numerical Jacobian."""
    return classify_equilibrium(jacobian(f, point))


def integrate_flow(f, p0, t0, t1, n):
    """Integrate dx/dt = f(x, y) with MA-07's RK4. Returns (ts, states)."""
    return integrate(lambda t, y: list(f(y[0], y[1])), list(p0), t0, t1, n)


def pendulum_flow(gamma=0.0):
    """Damped-pendulum flow (g=l=1):  theta' = omega,  omega' = -sin(theta) - gamma omega."""
    return lambda theta, omega: (omega, -math.sin(theta) - gamma * omega)


def van_der_pol(mu):
    """Van der Pol oscillator:  x' = y,  y' = mu (1 - x^2) y - x  (a limit cycle for mu>0)."""
    return lambda x, y: (y, mu * (1.0 - x * x) * y - x)


# --- demo --------------------------------------------------------------------

def _demo():
    print("CM-24 nonlinear dynamics & chaos -- demo")
    print("=" * 32)
    print("undamped pendulum fixed points:")
    print("  (0,0):", classify_fixed_point(pendulum_flow(0.0), (0.0, 0.0)),
          "   (pi,0):", classify_fixed_point(pendulum_flow(0.0), (math.pi, 0.0)))
    print("damped pendulum (gamma=0.5):")
    print("  (0,0):", classify_fixed_point(pendulum_flow(0.5), (0.0, 0.0)),
          "   (pi,0):", classify_fixed_point(pendulum_flow(0.5), (math.pi, 0.0)))

    f = van_der_pol(1.0)
    amps = []
    for start in ((0.1, 0.0), (3.0, 0.0)):
        ts, ys = integrate_flow(f, start, 0.0, 60.0, 12000)
        amps.append(max(abs(s[0]) for s in ys[-3000:]))
    print(f"\nvan der Pol limit cycle: amplitude from (0.1,0) = {amps[0]:.3f}, from (3,0) = {amps[1]:.3f}  (both ~2)")

    print(f"\nlogistic map at r=4 (reuse MA-22): Lyapunov exponent = {lyapunov_logistic(4.0):.4f}  (ln 2 = {math.log(2):.4f}, chaotic)")


if __name__ == "__main__":
    _demo()
