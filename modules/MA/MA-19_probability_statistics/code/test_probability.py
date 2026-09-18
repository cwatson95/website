"""Tests for MA-19 probability & statistics. Pure stdlib.

Run:  python3 test_probability.py     ->  "All N tests passed."
"""
import math
import random

from probability import (
    binomial_pmf, poisson_pmf, normal_pdf, normal_cdf, exponential_pdf,
    mean_var, sample_moments, sample_normal, sample_uniform_sum,
    error_propagation, least_squares_line, covariance, correlation,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _simpson(f, a, b, N=4000):
    if N % 2:
        N += 1
    h = (b - a) / N
    s = f(a) + f(b)
    for i in range(1, N):
        s += (4.0 if i % 2 else 2.0) * f(a + i * h)
    return s * h / 3.0


def test_normalization():
    assert _approx(sum(binomial_pmf(k, 12, 0.4) for k in range(13)), 1.0, tol=1e-9)
    assert _approx(sum(poisson_pmf(k, 4.0) for k in range(60)), 1.0, tol=1e-9)
    assert _approx(_simpson(lambda x: normal_pdf(x, 1.0, 2.0), -25, 27), 1.0, tol=1e-6)
    assert _approx(_simpson(lambda x: exponential_pdf(x, 1.5), 0, 60), 1.0, tol=1e-5)


def test_closed_form_moments_from_pmf():
    # binomial mean = np, var = np(1-p) computed directly from the pmf
    n, p = 12, 0.4
    mean = sum(k * binomial_pmf(k, n, p) for k in range(n + 1))
    var = sum((k - mean) ** 2 * binomial_pmf(k, n, p) for k in range(n + 1))
    assert _approx(mean, n * p) and _approx(var, n * p * (1 - p))
    # poisson mean = var = lam
    lam = 4.0
    pm = sum(k * poisson_pmf(k, lam) for k in range(80))
    pv = sum((k - pm) ** 2 * poisson_pmf(k, lam) for k in range(80))
    assert _approx(pm, lam, tol=1e-6) and _approx(pv, lam, tol=1e-6)


def test_normal_cdf():
    assert _approx(normal_cdf(0.0), 0.5)
    assert _approx(normal_cdf(1.0) - normal_cdf(-1.0), 0.6826894921, tol=1e-6)   # 1 sigma
    assert _approx(normal_cdf(2.0) - normal_cdf(-2.0), 0.9544997361, tol=1e-6)   # 2 sigma


def test_binomial_to_poisson():
    # binomial(n, lam/n) -> poisson(lam) as n -> inf
    lam = 2.5
    for k in (0, 1, 3, 5):
        e10 = abs(binomial_pmf(k, 10, lam / 10) - poisson_pmf(k, lam))
        e1000 = abs(binomial_pmf(k, 1000, lam / 1000) - poisson_pmf(k, lam))
        assert e1000 < e10
        assert e1000 < 1e-3


def test_sample_moments_converge():
    rng = random.Random(7)
    xs = sample_normal(1.0, 2.0, 60000, rng)
    m, v, sk, ku = sample_moments(xs)
    assert _approx(m, 1.0, tol=3e-2)
    assert _approx(v, 4.0, tol=4e-2)
    assert abs(sk) < 0.05 and abs(ku) < 0.1


def test_clt():
    rng = random.Random(11)
    xs = sample_uniform_sum(12, 60000, rng)          # -> N(0,1)
    m, v, sk, ku = sample_moments(xs)
    assert abs(m) < 0.02 and _approx(v, 1.0, tol=2e-2) and abs(sk) < 0.05
    for x in (-1.0, 0.0, 0.5, 1.5):
        emp = sum(1 for z in xs if z <= x) / len(xs)
        assert abs(emp - normal_cdf(x)) < 0.01


def test_error_propagation():
    # f = x*y  ->  (sigma_f/f)^2 = (sx/x)^2 + (sy/y)^2
    f = lambda v: v[0] * v[1]
    val, sig = error_propagation(f, [4.0, 5.0], [0.1, 0.2])
    rel = math.sqrt((0.1 / 4) ** 2 + (0.2 / 5) ** 2)
    assert _approx(val, 20.0) and _approx(sig / val, rel, tol=1e-4)
    # f = x + y  ->  sigma_f^2 = sx^2 + sy^2
    val, sig = error_propagation(lambda v: v[0] + v[1], [3.0, 7.0], [0.3, 0.4])
    assert _approx(sig, math.sqrt(0.3 ** 2 + 0.4 ** 2), tol=1e-4)


def test_least_squares_recovers_line():
    rng = random.Random(3)
    xd = [i * 0.5 for i in range(40)]
    yd = [2.0 + 3.0 * x + rng.gauss(0, 0.2) for x in xd]
    b, a, sb, sa = least_squares_line(xd, yd)
    assert _approx(b, 3.0, tol=0.05) and _approx(a, 2.0, tol=0.1)
    assert sb > 0 and sa > 0 and abs(b - 3.0) < 3 * sb     # within ~3 sigma


def test_covariance_correlation():
    xs = [1, 2, 3, 4, 5]
    ys = [2, 4, 6, 8, 10]                                  # perfectly correlated
    assert _approx(correlation(xs, ys), 1.0)
    assert _approx(correlation(xs, [10, 8, 6, 4, 2]), -1.0)
    assert _approx(covariance(xs, xs), covariance(xs, xs))  # var(x) consistency


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
