"""Tests for MA-11 Sturm-Liouville theory. Pure stdlib.

Run:  python3 test_sturm_liouville.py     ->  "All N tests passed."
"""
import math

from sturm_liouville import (
    sl_tridiagonal, sturm_count, tridiag_eigenvalues, tridiag_eigenvector,
    sl_eigenpairs, inner_w, rayleigh_quotient, expand, reconstruct,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_sturm_count_monotone():
    # diag 2, offdiag -1 (5x5): eigenvalues 2-2cos(k pi/6), all in (0,4)
    d = [2.0] * 5
    e = [-1.0] * 4
    assert sturm_count(d, e, -1.0) == 0          # none below the spectrum
    assert sturm_count(d, e, 5.0) == 5           # all below 5
    # count is nondecreasing in mu
    prev = -1
    for mu in [x * 0.5 for x in range(0, 9)]:
        c = sturm_count(d, e, mu)
        assert c >= prev
        prev = c


def test_eigenvalues_match_analytic_FD():
    # the FD matrix for -y'' on [0,pi] has EXACT eigenvalues
    #   lam_n = (4/h^2) sin^2(n pi / (2(N+1)))   and eigenvectors sin(n pi j/(N+1))
    N = 60
    d, e, wv, xs, h = sl_tridiagonal(1.0, 0.0, 1.0, 0.0, math.pi, N)
    lams = tridiag_eigenvalues(d, e)
    for n in range(1, N + 1):
        exact = (4.0 / h ** 2) * math.sin(n * math.pi / (2 * (N + 1))) ** 2
        assert _approx(lams[n - 1], exact, tol=1e-7)


def test_eigenvalues_approach_continuum():
    # lam_n -> n^2 on [0,pi] as the grid refines (O(h^2) error, low modes)
    lams, ys, xs, wv, h = sl_eigenpairs(1.0, 0.0, 1.0, 0.0, math.pi, 200, 5)
    for n in range(1, 6):
        assert abs(lams[n - 1] - n * n) < 0.02 * n * n     # well within O(h^2)


def test_eigenvectors_are_sines_and_orthonormal():
    N = 120
    lams, ys, xs, wv, h = sl_eigenpairs(1.0, 0.0, 1.0, 0.0, math.pi, N, 6)
    # each computed eigenvector aligns with sin(n x) (overlap ~ 1)
    for n in range(1, 7):
        ana = [math.sin(n * x) for x in xs]
        na = math.sqrt(sum(a * a for a in ana))
        nu = math.sqrt(sum(v * v for v in ys[n - 1]))
        overlap = abs(sum(ys[n - 1][j] * ana[j] for j in range(N))) / (na * nu)
        assert overlap > 0.9999
    # discrete w-orthogonality between distinct modes
    for m in range(6):
        for n in range(6):
            ip = inner_w(ys[m], ys[n], wv, h)
            if m != n:
                norm = math.sqrt(inner_w(ys[m], ys[m], wv, h) * inner_w(ys[n], ys[n], wv, h))
                assert abs(ip) / norm < 1e-6


def test_rayleigh_bounds_ground_state():
    # trial x(pi-x) gives R = 10/pi^2 ~ 1.0132 >= lambda_min ~ 1
    L = math.pi
    N = 200
    lams, ys, xs, wv, h = sl_eigenpairs(1.0, 0.0, 1.0, 0.0, L, N, 1)
    trial = [x * (L - x) for x in xs]
    R = rayleigh_quotient(1.0, 0.0, 1.0, trial, 0.0, L)
    assert _approx(R, 10.0 / math.pi ** 2, tol=1e-3)
    assert R >= lams[0] - 1e-9                              # variational bound


def test_completeness_parseval():
    # full eigenbasis reconstructs any grid function exactly; Parseval holds
    N = 40
    lams, ys, xs, wv, h = sl_eigenpairs(1.0, 0.0, 1.0, 0.0, math.pi, N, N)
    f = [x * (math.pi - x) for x in xs]
    c = expand(f, ys, wv, h)
    rec = reconstruct(c, ys)
    assert all(_approx(rec[j], f[j], tol=1e-6) for j in range(N))
    e_f = inner_w(f, f, wv, h)
    e_c = sum(c[n] ** 2 * inner_w(ys[n], ys[n], wv, h) for n in range(N))
    assert _approx(e_f, e_c, tol=1e-6)


def test_weighted_problem_runs():
    # a nonconstant weight should still give a real, ordered spectrum
    w = lambda x: 1.0 + 0.5 * x
    lams, ys, xs, wv, h = sl_eigenpairs(1.0, 0.0, w, 0.0, 1.0, 80, 4)
    assert all(lams[i] < lams[i + 1] for i in range(3))    # ascending, real
    assert lams[0] > 0.0


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
