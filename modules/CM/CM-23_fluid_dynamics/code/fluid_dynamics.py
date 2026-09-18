"""
CM-23  Fluid dynamics -- vorticity, incompressibility, and Bernoulli's equation.

Part of the physics topic network (modules/topic_network.txt, module CM-23).
Reuses ~MA-02 (`curl`, `divergence`, `gradient`); builds on ~CM-22 (continuity).
Links to ~PK-03 (plasma fluid description).

A steady velocity field is v(x, y, z) -> (vx, vy, vz). The **vorticity** omega =
curl v measures local rotation; **incompressible** flow has div v = 0;
**Bernoulli's** quantity 1/2 v^2 + p/rho + g z is constant along a streamline for
steady, incompressible, irrotational flow.

NOTE: MA-02 imported by relative path; becomes `from physkit...` later.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA02 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-02_vector_calculus", "code"))
if _MA02 not in sys.path:
    sys.path.insert(0, _MA02)

from vector_calculus import curl, divergence  # noqa: E402

__all__ = ["vorticity", "is_incompressible", "is_irrotational", "bernoulli_constant"]


def vorticity(v):
    """The vorticity field  omega = curl v  (twice the local angular velocity)."""
    return curl(v)


def is_incompressible(v, point=(0.31, 0.22, 0.13), h=1e-5, tol=1e-4):
    """True if div v = 0 at the test point (volume-preserving flow)."""
    return abs(divergence(v, h)(*point)) < tol


def is_irrotational(v, point=(0.31, 0.22, 0.13), h=1e-5, tol=1e-4):
    """True if curl v = 0 at the test point (flow derivable from a potential)."""
    cx, cy, cz = curl(v, h)(*point)
    return (cx * cx + cy * cy + cz * cz) ** 0.5 < tol


def bernoulli_constant(speed, p, rho, z, g=9.81):
    """Bernoulli's constant  1/2 v^2 + p/rho + g z  along a streamline."""
    return 0.5 * speed * speed + p / rho + g * z


# --- demo --------------------------------------------------------------------

def _demo():
    print("CM-23 fluid dynamics -- demo")
    print("=" * 32)
    Omega = 1.5
    rigid = lambda x, y, z: (-Omega * y, Omega * x, 0.0)        # rigid rotation
    print("rigid rotation v=(-Omega y, Omega x, 0):")
    print("  vorticity at (1,0,0) =", tuple(round(c, 4) for c in vorticity(rigid)(1, 0, 0)), " (= (0,0,2 Omega))")
    print("  incompressible?", is_incompressible(rigid), "  irrotational?", is_irrotational(rigid))

    pot = lambda x, y, z: (2 * x, -2 * y, 0.0)                  # v = grad(x^2 - y^2)
    print("\npotential flow v=grad(x^2-y^2):")
    print("  irrotational?", is_irrotational(pot), "  incompressible?", is_incompressible(pot))

    print("\nBernoulli 1/2 v^2 + p/rho + g z:", round(bernoulli_constant(3.0, 1e5, 1000.0, 2.0), 3))


if __name__ == "__main__":
    _demo()
