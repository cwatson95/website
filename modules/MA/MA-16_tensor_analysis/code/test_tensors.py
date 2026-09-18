"""Tests for MA-16 tensor analysis. Pure stdlib.

Run:  python3 test_tensors.py     ->  "All N tests passed."
"""
import math

from tensors import (
    kronecker_delta, levi_civita_symbol, levi_civita3, det_levi_civita,
    cofactor_matrix, inverse, jacobian, metric_from_map, lower_index, raise_index,
    inner, cross_via_levi_civita, matvec, eps_delta_identity_holds,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _polar(q):
    r, th = q
    return [r * math.cos(th), r * math.sin(th)]


def _spherical(q):
    r, th, ph = q
    return [r * math.sin(th) * math.cos(ph), r * math.sin(th) * math.sin(ph), r * math.cos(th)]


def test_symbols():
    assert levi_civita_symbol((0, 1, 2)) == 1
    assert levi_civita_symbol((1, 0, 2)) == -1
    assert levi_civita_symbol((2, 0, 1)) == 1
    assert levi_civita_symbol((0, 0, 1)) == 0
    eps = levi_civita3()
    assert eps[0][1][2] == 1 and eps[2][1][0] == -1 and eps[1][1][2] == 0
    assert kronecker_delta(3) == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


def test_eps_delta_identity():
    assert eps_delta_identity_holds()


def test_determinant_via_levi_civita():
    assert _approx(det_levi_civita([[1, 2], [3, 4]]), -2.0)
    assert _approx(det_levi_civita([[2, 1, 0], [1, 3, 1], [0, 1, 2]]), 8.0)
    assert _approx(det_levi_civita(kronecker_delta(4)), 1.0)


def test_inverse_is_inverse():
    for A in ([[4.0, 3.0], [6.0, 3.0]], [[2.0, 1.0, 0.0], [1.0, 3.0, 1.0], [0.0, 1.0, 2.0]]):
        Ai = inverse(A)
        n = len(A)
        prod = [[sum(A[i][k] * Ai[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(n):
                assert _approx(prod[i][j], 1.0 if i == j else 0.0, tol=1e-9)


def test_cross_matches_elementary():
    a, b = [1.0, 2.0, 3.0], [4.0, 5.0, 6.0]
    elem = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
    assert cross_via_levi_civita(a, b) == elem == [-3.0, 6.0, -3.0]


def test_metric_polar_and_spherical():
    r, th = 2.3, 0.6
    g = metric_from_map(_polar, [r, th])
    assert _approx(g[0][0], 1.0) and _approx(g[1][1], r * r)
    assert _approx(g[0][1], 0.0, tol=1e-6) and _approx(g[1][0], 0.0, tol=1e-6)
    r, th, ph = 1.5, 0.9, 0.4
    gs = metric_from_map(_spherical, [r, th, ph])
    assert _approx(gs[0][0], 1.0, tol=1e-4)
    assert _approx(gs[1][1], r * r, tol=1e-4)
    assert _approx(gs[2][2], r * r * math.sin(th) ** 2, tol=1e-4)


def test_length_is_invariant():
    # contravariant comps in polar; same vector's Cartesian comps via the Jacobian
    r, th = 2.0, 0.7
    g = metric_from_map(_polar, [r, th])
    J = jacobian(_polar, [r, th])
    for v_up in ([0.3, 0.25], [-0.4, 0.1], [0.0, 0.5]):
        V = matvec(J, v_up)
        assert _approx(inner(g, v_up, v_up), sum(c * c for c in V), tol=1e-5)


def test_raise_lower_roundtrip():
    r, th = 2.0, 0.7
    g = metric_from_map(_polar, [r, th])
    g_inv = inverse(g)
    # g^ik g_kj = delta
    n = 2
    prod = [[sum(g_inv[i][k] * g[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            assert _approx(prod[i][j], 1.0 if i == j else 0.0, tol=1e-6)
    for v_up in ([0.3, 0.25], [1.0, -0.5]):
        assert all(_approx(a, b, tol=1e-6) for a, b in zip(raise_index(g_inv, lower_index(g, v_up)), v_up))


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
