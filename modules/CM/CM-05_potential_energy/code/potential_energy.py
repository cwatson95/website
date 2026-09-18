"""
CM-05  Conservative forces & potential energy -- F = -grad U, the test for a
conservative force, total mechanical energy, and the stability of equilibria.

Part of the physics topic network (modules/topic_network.txt, module CM-05).
Reuses ~MA-02 (`gradient`, `curl`) and ~MA-01 (`dot`); builds on ~CM-04 (kinetic
energy); feeds ~CM-11 (effective potential / orbits).

A scalar potential is U(x, y, z) -> number; a force field is F(x, y, z) -> vector.

NOTE: MA-01/MA-02 imported by relative path; becomes `from physkit...` later.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
for _rel in ("MA-01_vector_algebra", "MA-02_vector_calculus"):
    _p = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", _rel, "code"))
    if _p not in sys.path:
        sys.path.insert(0, _p)

from vector_algebra import dot          # noqa: E402
from vector_calculus import gradient, curl  # noqa: E402

__all__ = [
    "force_from_potential", "is_conservative", "total_energy",
    "is_equilibrium", "is_stable",
]


def force_from_potential(U, h=1e-5):
    """The conservative force of a potential:  F = -grad U  (a force field)."""
    g = gradient(U, h)
    return lambda x, y, z: tuple(-c for c in g(x, y, z))


def is_conservative(F, point=(0.11, 0.23, 0.37), h=1e-5, tol=1e-4):
    """A force field is conservative iff curl F = 0 (here, tested at a point)."""
    cx, cy, cz = curl(F, h)(*point)
    return (cx * cx + cy * cy + cz * cz) ** 0.5 < tol


def total_energy(m, v, U, r):
    """Mechanical energy  E = 1/2 m |v|^2 + U(r)."""
    return 0.5 * m * dot(v, v) + U(*r)


# --- 1-D equilibria & their stability ----------------------------------------

def _d(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2.0 * h)


def _dd(f, x, h=1e-4):
    return (f(x + h) - 2.0 * f(x) + f(x - h)) / (h * h)


def is_equilibrium(U1d, x, tol=1e-4):
    """An equilibrium of a 1-D potential is where U'(x) = 0 (no force)."""
    return abs(_d(U1d, x)) < tol


def is_stable(U1d, x):
    """Stable iff the potential curves upward there:  U''(x) > 0 (a minimum)."""
    return _dd(U1d, x) > 0.0


# --- demo --------------------------------------------------------------------

def _demo():
    import math
    print("CM-05 potential energy -- demo")
    print("=" * 32)

    k = 3.0
    U = lambda x, y, z: 0.5 * k * (x * x + y * y + z * z)            # isotropic spring
    F = force_from_potential(U)
    print("F = -grad U for U=1/2 k r^2 at (1,2,3):", tuple(round(c, 4) for c in F(1, 2, 3)), " (= -k r)")
    print("conservative (curl F = 0)?", is_conservative(F))
    print("rotational field (-y,x,0) conservative?", is_conservative(lambda x, y, z: (-y, x, 0.0)))

    # energy conservation for a 1-D oscillator
    m, kk, A = 1.0, 4.0, 1.0
    w = math.sqrt(kk / m)
    Usp = lambda x, y, z: 0.5 * kk * (x * x + y * y + z * z)
    E = [total_energy(m, (-A * w * math.sin(w * t), 0, 0), Usp, (A * math.cos(w * t), 0, 0))
         for t in (0.0, 0.3, 0.9, 1.7)]
    print("oscillator energy at 4 times:", [round(e, 6) for e in E], " (constant = 1/2 k A^2 = 2)")

    Uw = lambda x: x ** 4 - 2.0 * x ** 2                              # double well
    print("double well x^4-2x^2: equilibria at -1,0,1 ->",
          [is_equilibrium(Uw, x) for x in (-1.0, 0.0, 1.0)],
          " stable? ->", [is_stable(Uw, x) for x in (-1.0, 0.0, 1.0)])


if __name__ == "__main__":
    _demo()
