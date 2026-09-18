"""
CM-22  Continuum mechanics & the continuity equation.

Part of the physics topic network (modules/topic_network.txt, module CM-22).
Reuses ~MA-02 (`divergence`, `gradient`). This is KEY BRIDGE B2: the same local
conservation law appears as mass here, electric charge in ~EM-13, and probability
in ~QM-04 -- only the conserved density changes.

Local conservation of mass:
    d rho/dt + div(rho v) = 0      (Eulerian form)
    D rho/Dt + rho (div v) = 0     (material/Lagrangian form),
with the material derivative D/Dt = d/dt + v . grad.

Fields are functions of (x, y, z, t): rho(...)-> scalar, v(...)-> (vx,vy,vz).

NOTE: MA-02 imported by relative path; becomes `from physkit...` later.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA02 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-02_vector_calculus", "code"))
if _MA02 not in sys.path:
    sys.path.insert(0, _MA02)

from vector_calculus import divergence, gradient  # noqa: E402

__all__ = ["continuity_residual", "material_derivative", "divergence_of_velocity"]


def continuity_residual(rho, v, x, y, z, t, h=1e-5, ht=1e-5):
    """d rho/dt + div(rho v) at (x,y,z,t).  Zero <=> mass is locally conserved."""
    drho_dt = (rho(x, y, z, t + ht) - rho(x, y, z, t - ht)) / (2.0 * ht)
    F = lambda X, Y, Z: tuple(rho(X, Y, Z, t) * c for c in v(X, Y, Z, t))
    return drho_dt + divergence(F, h)(x, y, z)


def material_derivative(f, v, x, y, z, t, h=1e-5, ht=1e-5):
    """The material (convective) derivative  Df/Dt = df/dt + v . grad f -- the rate
    of change of f following a fluid element."""
    df_dt = (f(x, y, z, t + ht) - f(x, y, z, t - ht)) / (2.0 * ht)
    g = gradient(lambda X, Y, Z: f(X, Y, Z, t), h)(x, y, z)
    vv = v(x, y, z, t)
    return df_dt + sum(vv[i] * g[i] for i in range(3))


def divergence_of_velocity(v, x, y, z, t, h=1e-5):
    """div v -- the local fractional rate of volume expansion of the flow."""
    return divergence(lambda X, Y, Z: v(X, Y, Z, t), h)(x, y, z)


# --- demo --------------------------------------------------------------------

def _demo():
    import math
    print("CM-22 continuity equation -- demo")
    print("=" * 32)

    # a density bump advected at constant velocity c -> continuity holds exactly
    c = 0.5
    rho = lambda x, y, z, t: math.exp(-(x - c * t) ** 2)
    v = lambda x, y, z, t: (c, 0.0, 0.0)
    print("travelling wave rho=exp(-(x-ct)^2), v=(c,0,0):")
    for (x, t) in ((0.3, 1.0), (1.0, 0.5), (-0.5, 2.0)):
        print(f"  continuity residual at x={x}, t={t}: {continuity_residual(rho, v, x, 0, 0, t):+.2e}  (~0)")

    # compressible flow: check the material form equals the Eulerian form
    rho2 = lambda x, y, z, t: 2.0 + 0.3 * x
    v2 = lambda x, y, z, t: (0.5 * x, 0.0, 0.0)
    x = 1.3
    euler = continuity_residual(rho2, v2, x, 0, 0, 0)
    material = (material_derivative(rho2, v2, x, 0, 0, 0)
                + rho2(x, 0, 0, 0) * divergence_of_velocity(v2, x, 0, 0, 0))
    print(f"\nmaterial form check: Eulerian {euler:.5f} vs  Drho/Dt + rho div v {material:.5f}")


if __name__ == "__main__":
    _demo()
