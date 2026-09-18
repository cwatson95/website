"""
MA-16  Tensor analysis & index notation -- contravariant/covariant components,
the metric tensor g_ij, raising and lowering indices, the Einstein summation
convention, the Kronecker delta and Levi-Civita symbol, and how a vector's length
is a coordinate invariant.

Part of the physics topic network (modules/topic_network.txt, module MA-16).
Builds on ~MA-03 (curvilinear coordinates -> the metric) and ~MA-04 (matrices);
feeds ~RE-08 (tensors in special relativity), ~EM-18 (the field tensor F^{mu nu}),
~CM-13 (the inertia tensor), and the curvature machinery of ~MA-17.

Pure Python, dependency-free. Vectors/tensors are (nested) lists; the metric of a
curvilinear system is built numerically from the coordinate map's Jacobian
(g = J^T J), and determinant/inverse are done through the Levi-Civita symbol --
keeping the whole module inside index notation.
"""

import math
from itertools import permutations

__all__ = [
    "kronecker_delta", "levi_civita_symbol", "levi_civita3",
    "det_levi_civita", "cofactor_matrix", "inverse",
    "jacobian", "metric_from_map", "lower_index", "raise_index",
    "inner", "cross_via_levi_civita", "matvec", "eps_delta_identity_holds",
]


# --- the two fundamental symbols ---------------------------------------------

def kronecker_delta(n):
    """delta^i_j -- the identity (mixed) tensor in n dimensions."""
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def levi_civita_symbol(idx):
    """The permutation symbol epsilon_{i1...in}: +1 / -1 for an even / odd
    permutation of (0,...,n-1), 0 if any index repeats. Works in any dimension."""
    n = len(idx)
    if len(set(idx)) != n:
        return 0
    sign = 1
    a = list(idx)
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] > a[j]:
                sign = -sign
    return sign


def levi_civita3():
    """The 3x3x3 Levi-Civita array epsilon_{ijk}."""
    return [[[levi_civita_symbol((i, j, k)) for k in range(3)] for j in range(3)] for i in range(3)]


# --- determinant & inverse, via Levi-Civita (stays in index notation) --------

def det_levi_civita(A):
    """det A = sum_perm epsilon(perm) prod_i A[i][perm_i] -- the antisymmetric
    (Levi-Civita) definition of the determinant."""
    n = len(A)
    total = 0.0
    for p in permutations(range(n)):
        term = levi_civita_symbol(p)
        for i in range(n):
            term *= A[i][p[i]]
        total += term
    return total


def _minor(A, i, j):
    return [[A[r][c] for c in range(len(A)) if c != j] for r in range(len(A)) if r != i]


def cofactor_matrix(A):
    """C_ij = (-1)^{i+j} M_ij (the signed minors)."""
    n = len(A)
    return [[((-1) ** (i + j)) * det_levi_civita(_minor(A, i, j)) for j in range(n)] for i in range(n)]


def inverse(A):
    """A^{-1} = adj(A)/det(A) = (cofactor matrix)^T / det -- Cramer's rule."""
    d = det_levi_civita(A)
    if abs(d) < 1e-300:
        raise ValueError("singular tensor")
    C = cofactor_matrix(A)
    n = len(A)
    return [[C[j][i] / d for j in range(n)] for i in range(n)]


# --- the metric from a coordinate map ----------------------------------------

def jacobian(xmap, q, eps=1e-6):
    """J[k][i] = d x^k / d q^i for the Cartesian embedding xmap: q -> (x^1,...)."""
    n = len(q)
    m = len(xmap(q))
    J = [[0.0] * n for _ in range(m)]
    for i in range(n):
        qp, qm = list(q), list(q)
        qp[i] += eps
        qm[i] -= eps
        xp, xm = xmap(qp), xmap(qm)
        for k in range(m):
            J[k][i] = (xp[k] - xm[k]) / (2 * eps)
    return J


def metric_from_map(xmap, q):
    """g_ij = sum_k (d x^k/d q^i)(d x^k/d q^j) = (J^T J)_ij -- the induced metric of
    the curvilinear coordinates q (Cartesian embedding). Polar -> diag(1, r^2);
    spherical -> diag(1, r^2, r^2 sin^2 theta)."""
    J = jacobian(xmap, q)
    n = len(q)
    m = len(J)
    return [[sum(J[k][i] * J[k][j] for k in range(m)) for j in range(n)] for i in range(n)]


# --- raising / lowering / contraction ----------------------------------------

def lower_index(g, v_up):
    """v_i = g_ij v^j  (lower a contravariant vector with the metric)."""
    n = len(g)
    return [sum(g[i][j] * v_up[j] for j in range(n)) for i in range(n)]


def raise_index(g_inv, v_low):
    """v^i = g^ij v_j  (raise a covariant vector with the inverse metric)."""
    n = len(g_inv)
    return [sum(g_inv[i][j] * v_low[j] for j in range(n)) for i in range(n)]


def inner(g, u_up, v_up):
    """Invariant inner product  <u,v> = g_ij u^i v^j."""
    n = len(g)
    return sum(g[i][j] * u_up[i] * v_up[j] for i in range(n) for j in range(n))


def matvec(A, x):
    return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]


def cross_via_levi_civita(a, b):
    """(a x b)^i = epsilon^{ijk} a_j b_k in 3-D -- the cross product as a
    Levi-Civita contraction (Cartesian metric)."""
    return [sum(levi_civita_symbol((i, j, k)) * a[j] * b[k]
                for j in range(3) for k in range(3)) for i in range(3)]


def eps_delta_identity_holds(tol=1e-12):
    """Check the workhorse identity  sum_i eps_{ijk} eps_{ilm} = d_jl d_km - d_jm d_kl."""
    d = kronecker_delta(3)
    for j in range(3):
        for k in range(3):
            for l in range(3):
                for m in range(3):
                    lhs = sum(levi_civita_symbol((i, j, k)) * levi_civita_symbol((i, l, m)) for i in range(3))
                    rhs = d[j][l] * d[k][m] - d[j][m] * d[k][l]
                    if abs(lhs - rhs) > tol:
                        return False
    return True


# --- demo --------------------------------------------------------------------

def _polar(q):
    r, th = q
    return [r * math.cos(th), r * math.sin(th)]


def _spherical(q):
    r, th, ph = q
    return [r * math.sin(th) * math.cos(ph), r * math.sin(th) * math.sin(ph), r * math.cos(th)]


def _demo():
    print("MA-16 tensor analysis -- demo")
    print("=" * 31)

    print("\nmetric from the coordinate map  g = J^T J:")
    gp = metric_from_map(_polar, [2.0, 0.7])
    print(f"  polar at r=2:      g = {[[round(x,4) for x in row] for row in gp]}  (-> diag(1, r^2=4))")
    gs = metric_from_map(_spherical, [1.5, 0.9, 0.4])
    print(f"  spherical r=1.5,th=0.9: g = {[[round(x,4) for x in row] for row in gs]}")
    print(f"    expect diag(1, r^2={1.5**2:.3f}, r^2 sin^2 th={1.5**2*math.sin(0.9)**2:.3f})")

    print("\nlength is coordinate-invariant:")
    r, th = 2.0, 0.7
    v_up = [0.3, 0.25]                                   # contravariant comps in polar
    J = jacobian(_polar, [r, th])
    V_cart = matvec(J, v_up)                             # same vector, Cartesian comps
    print(f"  g_ij v^i v^j (polar) = {inner(gp, v_up, v_up):.6f}")
    print(f"  |V|^2 in Cartesian   = {sum(c*c for c in V_cart):.6f}")

    print("\nlower then raise returns the vector  (g^ik g_kj = delta):")
    g_inv = inverse(gp)
    v_low = lower_index(gp, v_up)                        # v_i = g_ij v^j
    back = raise_index(g_inv, v_low)                     # v^i = g^ij v_j
    print(f"  v^i = {[round(x,6) for x in v_up]}  ->  v_i = {[round(x,6) for x in v_low]}  ->  back {[round(x,6) for x in back]}")

    print("\nLevi-Civita: cross product and determinant")
    a, b = [1.0, 2.0, 3.0], [4.0, 5.0, 6.0]
    print(f"  a x b via epsilon = {cross_via_levi_civita(a, b)}  (= [-3, 6, -3])")
    A = [[2.0, 1.0, 0.0], [1.0, 3.0, 1.0], [0.0, 1.0, 2.0]]
    print(f"  det via epsilon   = {det_levi_civita(A):.4f}")
    print(f"  eps-delta identity sum_i eps_ijk eps_ilm = d_jl d_km - d_jm d_kl ? {eps_delta_identity_holds()}")


if __name__ == "__main__":
    _demo()
