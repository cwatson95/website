"""Tests for ST-08 geometric & negative binomial distributions.

Asserts the headline analytic identities -- normalization, mean, variance,
mgf-derivative = mean, the memoryless property, geometric = negbinom(r=1), the
sum-of-geometrics relation, and the continuous (exponential) limit.

Run:  python3 test_geometric_negbinomial.py   ->  "All N tests passed."
"""
import math

import numpy as np

from geometric_negbinomial import (
    geometric_pmf, geometric_cdf, geometric_sf, geometric_mean, geometric_var,
    geometric_mgf, memoryless_check,
    negbinom_pmf, negbinom_mean, negbinom_var, negbinom_mgf,
)

PS = (0.2, 0.35, 0.5, 0.8)        # probabilities to sweep over


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _integrate(f, a, b, n=20000):
    """Midpoint rule -- the continuous check helper (cf. SM-06)."""
    dx = (b - a) / n
    return sum(f(a + (i + 0.5) * dx) * dx for i in range(n))


def _deriv(f, t, h=1e-5):
    return (f(t + h) - f(t - h)) / (2.0 * h)


def _deriv2(f, t, h=1e-4):
    return (f(t + h) - 2.0 * f(t) + f(t - h)) / (h * h)


# --- geometric distribution ---------------------------------------------------

def test_geometric_pmf_values():
    # explicit small values for p = 1/2: 1/2, 1/4, 1/8, ...
    for x, want in [(1, 0.5), (2, 0.25), (3, 0.125), (4, 0.0625)]:
        assert _approx(geometric_pmf(x, 0.5), want)
    # support: zero off the integers x = 1,2,3,...
    assert geometric_pmf(0, 0.5) == 0.0
    assert geometric_pmf(2.5, 0.5) == 0.0


def test_geometric_normalization():
    for p in PS:
        total = sum(geometric_pmf(x, p) for x in range(1, 4000))
        assert _approx(total, 1.0, tol=1e-9)


def test_geometric_mean_matches_series():
    for p in PS:
        m = sum(x * geometric_pmf(x, p) for x in range(1, 6000))
        assert _approx(m, geometric_mean(p), tol=1e-6)
        assert _approx(geometric_mean(p), 1.0 / p)


def test_geometric_variance_matches_series():
    for p in PS:
        mu = geometric_mean(p)
        v = sum((x - mu) ** 2 * geometric_pmf(x, p) for x in range(1, 8000))
        assert _approx(v, geometric_var(p), tol=1e-5)
        assert _approx(geometric_var(p), (1.0 - p) / p ** 2)


def test_geometric_cdf_and_survival():
    for p in PS:
        for k in (1, 3, 5, 10):
            # cdf + survival = 1, and survival = (1-p)^k
            assert _approx(geometric_cdf(k, p) + geometric_sf(k, p), 1.0)
            assert _approx(geometric_sf(k, p), (1.0 - p) ** k)
            # cdf equals the partial sum of the pmf
            partial = sum(geometric_pmf(x, p) for x in range(1, k + 1))
            assert _approx(geometric_cdf(k, p), partial)


def test_memoryless_property():
    for p in PS:
        for (m, n) in [(1, 1), (3, 4), (10, 5), (7, 2)]:
            lhs, rhs = memoryless_check(m, n, p)
            assert _approx(lhs, rhs)
            assert _approx(rhs, (1.0 - p) ** n)


def test_geometric_mgf_derivative_is_mean_and_var():
    for p in PS:
        M = lambda t: geometric_mgf(t, p)
        # M'(0) = E[X] = mean
        assert _approx(_deriv(M, 0.0), geometric_mean(p), tol=1e-5)
        # Var = M''(0) - (M'(0))^2
        ex2 = _deriv2(M, 0.0)
        var = ex2 - _deriv(M, 0.0) ** 2
        assert _approx(var, geometric_var(p), tol=1e-3)


# --- negative binomial distribution ------------------------------------------

def test_negbinom_pmf_values():
    # r=2, p=1/2: P(X=x) = (x-1) (1/2)^x, x = 2,3,4,...
    for x, want in [(2, 0.25), (3, 0.25), (4, 0.1875), (5, 0.125)]:
        assert _approx(negbinom_pmf(x, 2, 0.5), want)
    # support starts at r
    assert negbinom_pmf(1, 2, 0.5) == 0.0
    assert negbinom_pmf(3.5, 2, 0.5) == 0.0


def test_negbinom_normalization():
    for p in PS:
        for r in (1, 2, 4):
            total = sum(negbinom_pmf(x, r, p) for x in range(r, 6000))
            assert _approx(total, 1.0, tol=1e-8)


def test_negbinom_mean_and_var_series():
    for p in PS:
        for r in (1, 2, 4):
            mu = sum(x * negbinom_pmf(x, r, p) for x in range(r, 9000))
            v = sum((x - mu) ** 2 * negbinom_pmf(x, r, p) for x in range(r, 9000))
            assert _approx(mu, negbinom_mean(r, p), tol=1e-5)
            assert _approx(v, negbinom_var(r, p), tol=1e-4)
            # r times the geometric moments
            assert _approx(negbinom_mean(r, p), r * geometric_mean(p))
            assert _approx(negbinom_var(r, p), r * geometric_var(p))


def test_geometric_equals_negbinom_r1():
    for p in PS:
        for x in range(1, 50):
            assert _approx(negbinom_pmf(x, 1, p), geometric_pmf(x, p))


def test_sum_of_geometrics_is_negbinom():
    # r-fold convolution of the geometric pmf == negative binomial pmf
    p, r, N = 0.4, 3, 4000
    g = np.array([geometric_pmf(x, p) for x in range(1, N + 1)])  # index i -> x = i+1
    conv = g.copy()
    for _ in range(r - 1):
        conv = np.convolve(conv, g)
    # after r-fold convolution, conv index k -> P(sum = r + k)
    for k in range(0, 60):
        assert _approx(conv[k], negbinom_pmf(r + k, r, p), tol=1e-9)
    assert _approx(float(conv.sum()), 1.0, tol=1e-6)


def test_negbinom_mgf_power_and_mean():
    p, r = 0.45, 3
    for t in (-0.2, 0.0, 0.1, 0.3):
        assert _approx(negbinom_mgf(t, r, p), geometric_mgf(t, p) ** r)
    M = lambda t: negbinom_mgf(t, r, p)
    assert _approx(_deriv(M, 0.0), negbinom_mean(r, p), tol=1e-4)
    var = _deriv2(M, 0.0) - _deriv(M, 0.0) ** 2
    assert _approx(var, negbinom_var(r, p), tol=1e-2)


def test_exponential_limit_continuous():
    # As p -> 0 the geometric is the discrete exponential: P(pX > t) -> e^{-t},
    # and e^{-t} = \int_t^infty e^{-s} ds (the continuous _integrate check).
    for t in (0.5, 1.0, 2.0):
        exp_tail = _integrate(lambda s: math.exp(-s), t, t + 60.0)
        assert _approx(exp_tail, math.exp(-t), tol=1e-6)
        small_p = 1e-4
        geo_tail = geometric_sf(t / small_p, small_p)   # P(X > t/p) = (1-p)^{floor(t/p)}
        assert _approx(geo_tail, math.exp(-t), tol=2e-3)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
