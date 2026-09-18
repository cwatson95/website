"""
CM-04  Work & energy -- kinetic energy, the work integral, and the work-energy
theorem  W = Delta T.

Part of the physics topic network (modules/topic_network.txt, module CM-04).
Reuses ~MA-02 (`line_integral` IS the work integral) and ~MA-01 (`dot`); feeds
~CM-05 (potential energy) and ~CM-08 (collisions, energy bookkeeping).

A force field is F(x, y, z) -> (Fx, Fy, Fz); a path is gamma(t) -> (x, y, z).

NOTE: MA-01/MA-02 imported by relative path; becomes `from physkit...` later.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
for _rel in ("MA-01_vector_algebra", "MA-02_vector_calculus"):
    _p = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", _rel, "code"))
    if _p not in sys.path:
        sys.path.insert(0, _p)

from vector_algebra import dot            # noqa: E402
from vector_calculus import line_integral  # noqa: E402

__all__ = ["kinetic_energy", "work", "power"]


def kinetic_energy(m, v):
    """T = 1/2 m |v|^2 = 1/2 m (v . v)."""
    return 0.5 * m * dot(v, v)


def work(force_field, path, a, b, n=2000):
    """Work done by a force field along a path:  W = integral F . dl  (= MA-02 line integral)."""
    return line_integral(force_field, path, a, b, n)


def power(F, v):
    """Instantaneous power  P = F . v."""
    return dot(F, v)


# --- demo --------------------------------------------------------------------

def _demo():
    print("CM-04 work & energy -- demo")
    print("=" * 32)
    print("T for m=2, v=(3,0,4):", kinetic_energy(2.0, (3.0, 0.0, 4.0)), "  (= 1/2*2*25 = 25)")

    # constant force along a straight push: W = F . displacement
    F = (2.0, 0.0, 0.0)
    push = lambda s: (5.0 * s, 0.0, 0.0)            # (0,0,0) -> (5,0,0)
    print("W by F=(2,0,0) over 5 m:", round(work(lambda x, y, z: F, push, 0.0, 1.0), 6), "  (= 10)")

    # work-energy theorem: particle from rest under constant force, F=(3,0,0), m=2
    F0, m = 3.0, 2.0
    a = F0 / m
    T = 2.0
    path = lambda s: (0.5 * a * s * s, 0.0, 0.0)    # x(s) for s in [0, T]
    W = work(lambda x, y, z: (F0, 0.0, 0.0), path, 0.0, T)
    vT = a * T
    print(f"work-energy: W = {W:.5f}  vs  Delta T = {kinetic_energy(m, (vT, 0, 0)):.5f}")


if __name__ == "__main__":
    _demo()
