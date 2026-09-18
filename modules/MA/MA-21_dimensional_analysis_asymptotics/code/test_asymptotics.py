"""Tests for MA-21 dimensional analysis & asymptotics. Pure stdlib.

Run:  python3 test_asymptotics.py     ->  "All N tests passed."
"""
import math

from asymptotics import (
    nullspace, buckingham_pi, is_dimensionless,
    exp_integral_scaled_true, exp_integral_scaled_asymptotic, optimal_truncation,
    ln_factorial_stirling, perturbed_root, _exact_root,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_nullspace_basic():
    # M = [[1,1,1]] -> 2-dim nullspace, each vector summing to 0
    basis = nullspace([[1.0, 1.0, 1.0]])
    assert len(basis) == 2
    for v in basis:
        assert _approx(sum(v), 0.0, tol=1e-9)
    # full-rank square -> trivial nullspace
    assert nullspace([[1.0, 0.0], [0.0, 1.0]]) == []


def test_buckingham_pendulum():
    # {T_period, L, g, m} over (M,L,T): exactly one dimensionless group, = g T^2 / L
    D = [[0, 0, 0, 1], [0, 1, 1, 0], [1, 0, -2, 0]]
    groups = buckingham_pi(D)
    assert len(groups) == 1                              # n_vars 4 - rank 3
    p = groups[0]
    assert is_dimensionless(D, p)
    # normalize so the period exponent is 2; then it must be (2, -1, 1, 0) up to sign
    if abs(p[0]) > 1e-9:
        p = [e * (2.0 / p[0]) for e in p]
        assert _approx(p[1], -1.0, tol=1e-6) and _approx(p[2], 1.0, tol=1e-6) and _approx(p[3], 0.0, tol=1e-6)


def test_buckingham_reynolds():
    # {rho, U, L, mu} over (M,L,T): one group = Reynolds number rho U L / mu
    #   rho M L^-3, U L T^-1, L, mu M L^-1 T^-1
    D = [[1, 0, 0, 1],          # M
         [-3, 1, 1, -1],        # L
         [0, -1, 0, -1]]        # T
    groups = buckingham_pi(D)
    assert len(groups) == 1
    assert is_dimensionless(D, groups[0])


def test_asymptotic_optimal_truncation():
    # divergent series: error reaches a minimum near N~x then grows again, and the
    # minimum error is of order the smallest term ~ sqrt(2 pi x) e^{-x}
    for x in (5.0, 8.0, 12.0):
        bN, bErr, errs = optimal_truncation(x, Nmax=40)
        assert abs(bN - x) <= 3                          # optimal truncation ~ x terms
        assert bErr < 2.0 * math.sqrt(2 * math.pi * x) * math.exp(-x)   # ~ smallest term
        assert bErr < errs[1]                            # optimum beats early truncation
        # adding many more terms makes it worse (divergence)
        assert errs[min(2 * int(x), len(errs) - 1)] > bErr
        assert errs[-1] > bErr                           # far tail is worse than optimum


def test_asymptotic_leading_term():
    # g(x) = 1 - 1/x + O(1/x^2): so g -> 1, and the 2-term series beats the 1-term
    for x in (20.0, 50.0):
        true = exp_integral_scaled_true(x)
        assert abs(true - 1.0) < 1.0 / x                 # within the first correction
        e0 = abs(exp_integral_scaled_asymptotic(x, 0) - true)   # series = 1
        e1 = abs(exp_integral_scaled_asymptotic(x, 1) - true)   # series = 1 - 1/x
        assert e1 < e0                                   # the -1/x correction helps
    assert exp_integral_scaled_true(50.0) < 1.0          # alternating; below 1


def test_stirling_converges():
    for n in (10, 50, 200):
        exact = math.lgamma(n + 1)
        e1 = abs(ln_factorial_stirling(n, 1) - exact)
        e2 = abs(ln_factorial_stirling(n, 2) - exact)
        e3 = abs(ln_factorial_stirling(n, 3) - exact)
        assert e2 < e1 and e3 < e2                       # each correction improves it
        assert e3 / exact < 1e-6                          # < 1 ppm with the 1/(12n) term


def test_perturbation_root_order():
    # error of the order-k series is O(eps^{k+1})
    for eps in (0.1, 0.05):
        e1 = abs(perturbed_root(eps, 1) - _exact_root(eps))
        e2 = abs(perturbed_root(eps, 2) - _exact_root(eps))
        assert e2 < e1
        assert e2 < 0.6 * eps ** 3                        # O(eps^3) after 2 terms


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
