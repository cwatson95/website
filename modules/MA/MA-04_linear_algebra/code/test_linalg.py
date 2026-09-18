"""Tests for MA-04 linear algebra. Pure stdlib.

Run:  python3 test_linalg.py     ->  "All N tests passed."
"""
import random

from linalg import (
    identity, transpose, matmul, matvec, trace, det, solve, inverse,
    is_symmetric, eig_symmetric, reconstruct, eigvals_2x2,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-9):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def _mapprox(A, B, tol=1e-9):
    return all(_approx(A[i][j], B[i][j], tol) for i in range(len(A)) for j in range(len(A[0])))


def _rand_sym(n, rng):
    M = [[rng.uniform(-3, 3) for _ in range(n)] for _ in range(n)]
    return [[(M[i][j] + M[j][i]) / 2.0 for j in range(n)] for i in range(n)]


def test_basic_ops():
    A, B = [[1, 2], [3, 4]], [[5, 6], [7, 8]]
    assert matmul(A, B) == [[19, 22], [43, 50]]
    assert matvec(A, [1, 1]) == [3, 7]
    assert transpose(A) == [[1, 3], [2, 4]]
    assert trace(A) == 5
    assert _mapprox(matmul(A, identity(2)), A)
    assert is_symmetric([[1, 2], [2, 1]]) and not is_symmetric(A)


def test_det():
    assert _approx(det([[1, 2], [3, 4]]), -2.0)
    assert _approx(det(identity(4)), 1.0)
    assert _approx(det([[2, 0, 0], [0, 3, 0], [0, 0, 4]]), 24.0)
    assert _approx(det([[1, 2], [2, 4]]), 0.0)               # singular


def test_solve_and_inverse():
    rng = random.Random(0)
    for n in (2, 3, 4):
        for _ in range(40):
            A = [[rng.uniform(-3, 3) for _ in range(n)] for _ in range(n)]
            if abs(det(A)) < 1e-6:
                continue
            x = [rng.uniform(-3, 3) for _ in range(n)]
            b = matvec(A, x)
            assert _vapprox(solve(A, b), x, tol=1e-6)
            assert _mapprox(matmul(A, inverse(A)), identity(n), tol=1e-6)


def test_eig_known_2x2():
    S = [[2, 1], [1, 2]]
    vals, vecs = eig_symmetric(S)
    assert _vapprox(vals, [1.0, 3.0])
    for lam, v in zip(vals, vecs):
        assert _vapprox(matvec(S, v), [lam * c for c in v])


def test_eig_tridiagonal_and_reconstruct():
    S = [[2, 1, 0], [1, 2, 1], [0, 1, 2]]
    vals, vecs = eig_symmetric(S)
    assert _vapprox(vals, sorted([2 - 2 ** 0.5, 2.0, 2 + 2 ** 0.5]), tol=1e-8)
    for lam, v in zip(vals, vecs):
        assert _vapprox(matvec(S, v), [lam * c for c in v], tol=1e-8)
    for i in range(3):                                       # orthonormal eigenvectors
        for j in range(3):
            d = sum(vecs[i][k] * vecs[j][k] for k in range(3))
            assert _approx(d, 1.0 if i == j else 0.0, tol=1e-8)
    assert _mapprox(reconstruct(vals, vecs), [[float(x) for x in row] for row in S], tol=1e-8)


def test_eig_random_symmetric_invariants():
    rng = random.Random(5)
    for n in (2, 3, 4, 5):
        for _ in range(25):
            S = _rand_sym(n, rng)
            vals, vecs = eig_symmetric(S)
            assert _approx(sum(vals), trace(S), tol=1e-7)        # sum of eigenvalues = trace
            prod = 1.0
            for v in vals:
                prod *= v
            assert _approx(prod, det(S), tol=1e-6)               # product of eigenvalues = det
            for lam, v in zip(vals, vecs):
                assert _vapprox(matvec(S, v), [lam * c for c in v], tol=1e-7)


def test_eigvals_2x2():
    rot = sorted((eigvals_2x2([[0, -1], [1, 0]])), key=lambda z: z.imag)   # rotation -> +/- i
    assert abs(rot[0] - complex(0, -1)) < 1e-9 and abs(rot[1] - complex(0, 1)) < 1e-9
    sym = eigvals_2x2([[2, 1], [1, 2]])                                    # matches Jacobi: 1, 3
    assert _vapprox(sorted(z.real for z in sym), [1.0, 3.0])
    assert all(abs(z.imag) < 1e-12 for z in sym)


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
