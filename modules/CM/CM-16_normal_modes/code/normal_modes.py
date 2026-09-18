"""
CM-16  Coupled oscillations & normal modes -- the small-oscillation eigenvalue
problem  K v = omega^2 M v.

Part of the physics topic network (modules/topic_network.txt, module CM-16).
The second headline ~MA-04 consumer: reducing the generalized eigenproblem to a
symmetric one and diagonalizing with `eig_symmetric` gives the **normal
frequencies** and **normal modes**. Builds on ~CM-15; links to ~MA-09 (each mode
is a Fourier component) and ~QM-05.

For a system  M x'' = -K x  with mass matrix M (diagonal) and stiffness matrix K
(symmetric), substitute x = v e^{i omega t}:  (K - omega^2 M) v = 0.

NOTE: MA-04 imported by relative path; becomes `from physkit...` later.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA04 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-04_linear_algebra", "code"))
if _MA04 not in sys.path:
    sys.path.insert(0, _MA04)

from linalg import eig_symmetric  # noqa: E402

__all__ = ["normal_modes", "mode_inner_product"]


def normal_modes(K, M):
    """Solve K v = omega^2 M v for a diagonal mass matrix M (given as a list of
    masses). Reduce to the symmetric eigenproblem of A = M^{-1/2} K M^{-1/2}
    (via MA-04's Jacobi eigensolver). Returns (frequencies, modes), frequencies
    ascending; modes are the physical shapes v = M^{-1/2} u (mass-orthonormal)."""
    n = len(M)
    s = [M[i] ** -0.5 for i in range(n)]
    A = [[s[i] * K[i][j] * s[j] for j in range(n)] for i in range(n)]
    vals, vecs = eig_symmetric(A)
    freqs = [(v ** 0.5 if v > 0.0 else 0.0) for v in vals]
    modes = [[s[i] * u[i] for i in range(n)] for u in vecs]
    return freqs, modes


def mode_inner_product(M, va, vb):
    """Mass-weighted inner product  va^T M vb  (normal modes are orthonormal in it)."""
    return sum(M[i] * va[i] * vb[i] for i in range(len(M)))


# --- demo --------------------------------------------------------------------

def _demo():
    import math
    print("CM-16 coupled oscillations & normal modes -- demo")
    print("=" * 32)
    # two equal masses, three identical springs (wall-m-spring-m-wall): K=[[2,-1],[-1,2]]k
    k, m = 1.0, 1.0
    K = [[2 * k, -k], [-k, 2 * k]]
    M = [m, m]
    freqs, modes = normal_modes(K, M)
    print("two equal masses, springs k=1:")
    print(f"  normal frequencies = {[round(w, 4) for w in freqs]}  (sqrt(k/m)=1, sqrt(3k/m)={math.sqrt(3):.4f})")
    print(f"  in-phase mode  (low) : {[round(c, 4) for c in modes[0]]}  (~ (1,1)/sqrt2)")
    print(f"  out-of-phase   (high): {[round(c, 4) for c in modes[1]]}  (~ (1,-1)/sqrt2)")


if __name__ == "__main__":
    _demo()
