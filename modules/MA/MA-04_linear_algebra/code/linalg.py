"""
MA-04  Linear algebra -- matrices, determinants, linear solves, and the
eigenvalue problem (symmetric/Hermitian via Jacobi rotations).

Part of the physics topic network (modules/topic_network.txt, module MA-04).
Feeds ~CM-13 (inertia tensor -> principal axes), ~CM-16 (normal modes),
~QM-05/06 (observables as Hermitian operators, diagonalization).

Pure Python, dependency-free. Matrices are lists of rows (list of lists);
vectors are lists/tuples. For large/general (non-symmetric, complex) problems
use numpy.linalg; this module is the transparent, self-contained version that
shows how diagonalization actually works.
"""

import cmath
import math

__all__ = [
    "identity", "transpose", "matmul", "matvec", "trace",
    "det", "solve", "inverse", "is_symmetric",
    "eig_symmetric", "reconstruct", "eigvals_2x2",
]


# --- basic operations --------------------------------------------------------

def identity(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def transpose(A):
    return [list(col) for col in zip(*A)]


def matmul(A, B):
    """Matrix product A @ B."""
    k = len(B)
    return [[sum(A[i][p] * B[p][j] for p in range(k)) for j in range(len(B[0]))]
            for i in range(len(A))]


def matvec(A, x):
    """Matrix-vector product A x."""
    return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


# --- determinant / solve / inverse  (Gaussian elimination, partial pivot) ----

def det(A):
    """Determinant via Gaussian elimination with partial pivoting."""
    n = len(A)
    M = [row[:] for row in A]
    sign, d = 1.0, 1.0
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-15:
            return 0.0
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
            sign = -sign
        d *= M[col][col]
        for r in range(col + 1, n):
            f = M[r][col] / M[col][col]
            for c in range(col, n):
                M[r][c] -= f * M[col][c]
    return sign * d


def solve(A, b):
    """Solve A x = b by Gauss-Jordan elimination with partial pivoting."""
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-15:
            raise ValueError("singular matrix")
        M[col], M[piv] = M[piv], M[col]
        pivot = M[col][col]
        for r in range(n):
            if r != col:
                f = M[r][col] / pivot
                for c in range(col, n + 1):
                    M[r][c] -= f * M[col][c]
    return [M[i][n] / M[i][i] for i in range(n)]


def inverse(A):
    """Matrix inverse (columns = solutions of A x = e_j)."""
    n = len(A)
    cols = [solve(A, [1.0 if i == j else 0.0 for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def is_symmetric(A, tol=1e-9):
    n = len(A)
    return all(abs(A[i][j] - A[j][i]) <= tol for i in range(n) for j in range(n))


# --- symmetric eigenproblem: the Jacobi rotation algorithm -------------------

def eig_symmetric(A, tol=1e-13, max_sweeps=100):
    """Eigenvalues & eigenvectors of a real SYMMETRIC matrix by cyclic Jacobi
    rotations. Returns (eigenvalues, eigenvectors) sorted by ascending value;
    eigenvectors is a list of orthonormal column vectors with A v = lambda v.
    """
    n = len(A)
    a = [row[:] for row in A]
    V = identity(n)
    for _ in range(max_sweeps):
        off = math.sqrt(sum(a[p][q] ** 2 for p in range(n) for q in range(p + 1, n)))
        if off <= tol:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                app, aqq, apq = a[p][p], a[q][q], a[p][q]
                a[p][p] = c * c * app - 2.0 * s * c * apq + s * s * aqq
                a[q][q] = s * s * app + 2.0 * s * c * apq + c * c * aqq
                a[p][q] = a[q][p] = 0.0
                for k in range(n):
                    if k != p and k != q:
                        akp, akq = a[k][p], a[k][q]
                        a[k][p] = a[p][k] = c * akp - s * akq
                        a[k][q] = a[q][k] = s * akp + c * akq
                for k in range(n):
                    vkp, vkq = V[k][p], V[k][q]
                    V[k][p] = c * vkp - s * vkq
                    V[k][q] = s * vkp + c * vkq
    vals = [a[i][i] for i in range(n)]
    vecs = [[V[k][j] for k in range(n)] for j in range(n)]   # column j = eigenvector j
    order = sorted(range(n), key=lambda i: vals[i])
    return [vals[i] for i in order], [vecs[i] for i in order]


def reconstruct(vals, vecs):
    """Rebuild A = Q diag(vals) Q^T from eigenvalues and eigenvectors (columns)."""
    n = len(vals)
    Q = [[vecs[j][i] for j in range(n)] for i in range(n)]   # columns = eigenvectors
    Lam = [[vals[i] if i == j else 0.0 for j in range(n)] for i in range(n)]
    return matmul(matmul(Q, Lam), transpose(Q))


def eigvals_2x2(A):
    """The two eigenvalues of a 2x2 matrix (may be complex) from the
    characteristic polynomial lambda^2 - (tr)lambda + det = 0."""
    tr = A[0][0] + A[1][1]
    de = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    disc = cmath.sqrt(tr * tr - 4.0 * de)
    return ((tr + disc) / 2.0, (tr - disc) / 2.0)


# --- demo --------------------------------------------------------------------

def _demo():
    print("MA-04 linear algebra -- demo")
    print("=" * 32)

    A = [[4.0, 3.0], [6.0, 3.0]]
    print("A =", A, " det =", det(A))
    b = [10.0, 12.0]
    x = solve(A, b)
    print("solve A x = [10,12]:", [round(v, 6) for v in x], " check A x =", [round(v, 6) for v in matvec(A, x)])
    print("A^-1 =", [[round(v, 6) for v in row] for row in inverse(A)])

    print("\nsymmetric eigenproblem (Jacobi):")
    S = [[2.0, 1.0, 0.0], [1.0, 2.0, 1.0], [0.0, 1.0, 2.0]]   # eigenvalues 2, 2±sqrt2
    vals, vecs = eig_symmetric(S)
    print("  eigenvalues =", [round(v, 6) for v in vals], " (exact 2-sqrt2, 2, 2+sqrt2 =",
          [round(2 - 2 ** 0.5, 6), 2.0, round(2 + 2 ** 0.5, 6)], ")")
    Av = matvec(S, vecs[0])
    print("  A v0 =", [round(v, 6) for v in Av], " lambda0 v0 =", [round(vals[0] * c, 6) for c in vecs[0]])
    R = reconstruct(vals, vecs)
    print("  reconstruct Q L Q^T == A ?", all(abs(R[i][j] - S[i][j]) < 1e-9 for i in range(3) for j in range(3)))

    print("\ncomplex eigenvalues of a 90-degree rotation:")
    Rot = [[0.0, -1.0], [1.0, 0.0]]
    print("  eigvals_2x2 =", tuple(complex(round(z.real, 6), round(z.imag, 6)) for z in eigvals_2x2(Rot)),
          " (= +/- i)")


if __name__ == "__main__":
    _demo()
