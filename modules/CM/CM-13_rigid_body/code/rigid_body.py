"""
CM-13  Rigid-body dynamics -- the moment-of-inertia tensor, and its principal
axes & principal moments via diagonalization.

Part of the physics topic network (modules/topic_network.txt, module CM-13).
This is the headline ~MA-04 consumer: the inertia tensor is real symmetric, so
its eigenvectors are the **principal axes** and its eigenvalues the **principal
moments** -- exactly `eig_symmetric`. Builds on ~CM-09 (angular momentum); feeds
~CM-14 (Euler's equations).

NOTE: MA-01/MA-04 imported by relative path; becomes `from physkit...` later.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA01 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-01_vector_algebra", "code"))
_MA04 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-04_linear_algebra", "code"))
for _p in (_MA01, _MA04):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from vector_algebra import norm           # noqa: E402
from linalg import eig_symmetric, matvec  # noqa: E402

__all__ = [
    "inertia_tensor", "principal_axes", "moment_about_axis",
    "angular_momentum", "rotational_kinetic_energy", "parallel_axis",
]


def inertia_tensor(masses, positions):
    """The inertia tensor about the origin:  I_ij = sum_a m_a (r_a^2 delta_ij - r_i r_j)."""
    I = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    for m, r in zip(masses, positions):
        r2 = r[0] * r[0] + r[1] * r[1] + r[2] * r[2]
        for i in range(3):
            for j in range(3):
                I[i][j] += m * ((r2 if i == j else 0.0) - r[i] * r[j])
    return I


def principal_axes(I):
    """Principal moments (eigenvalues) and principal axes (orthonormal eigenvectors)
    of the symmetric inertia tensor -- via MA-04's Jacobi eigensolver. Returns
    (moments, axes) with moments ascending."""
    return eig_symmetric(I)


def moment_about_axis(I, axis):
    """Scalar moment of inertia about a unit axis n:  I_n = n . I . n."""
    n = norm(axis)
    u = [axis[i] / n for i in range(3)]
    Iu = matvec(I, u)
    return sum(u[i] * Iu[i] for i in range(3))


def angular_momentum(I, omega):
    """L = I omega (in general not parallel to omega -- only along a principal axis)."""
    return matvec(I, omega)


def rotational_kinetic_energy(I, omega):
    """T = 1/2 omega . I omega = 1/2 omega . L."""
    L = matvec(I, omega)
    return 0.5 * sum(omega[i] * L[i] for i in range(3))


def parallel_axis(I_cm, M, d):
    """Parallel-axis theorem for the full tensor: shift from the CM by displacement d,
    I = I_cm + M (|d|^2 delta_ij - d_i d_j)."""
    d2 = d[0] * d[0] + d[1] * d[1] + d[2] * d[2]
    return [[I_cm[i][j] + M * ((d2 if i == j else 0.0) - d[i] * d[j]) for j in range(3)] for i in range(3)]


# --- demo --------------------------------------------------------------------

def _demo():
    print("CM-13 rigid-body dynamics -- demo")
    print("=" * 32)
    # 4 equal masses on the x and y axes -> I = diag(2,2,4) ma^2
    m, a = 1.0, 1.0
    pts = [(a, 0, 0), (-a, 0, 0), (0, a, 0), (0, -a, 0)]
    I = inertia_tensor([m] * 4, pts)
    print("inertia tensor (4 masses on axes):")
    for row in I:
        print("  ", [round(c, 4) for c in row])
    moments, axes = principal_axes(I)
    print("principal moments (eigenvalues):", [round(c, 4) for c in moments], " (= 2,2,4 ma^2)")
    print("moment about z-axis:", round(moment_about_axis(I, (0, 0, 1)), 4), " (= I_zz = 4)")

    omega = (0.0, 0.0, 3.0)                         # along a principal axis
    L = angular_momentum(I, omega)
    print("L for omega=(0,0,3):", [round(c, 4) for c in L], " (parallel to omega along principal axis)")
    print("rotational KE:", round(rotational_kinetic_energy(I, omega), 4), " (= 1/2 I_zz omega^2 = 18)")


if __name__ == "__main__":
    _demo()
