"""Tests for ST-06 moment-generating functions.  numpy + stdlib only.

Run:  python3 test_mgf.py     ->  "All N tests passed."

Each test asserts a headline analytic identity of the mgf -- normalization
M(0)=1, moments by differentiation M^{(k)}(0)=E[X^k], variance from M, the
product rule for sums of independents, closed-form additivity (binomial,
Poisson, normal, gamma), the linear-transform rule, cumulants from ln M, and
the Laplace-transform/quadrature view of the continuous mgf.
"""
import math

import numpy as np

from mgf import (
    mgf, cgf, mean, variance,
    mean_from_mgf, var_from_mgf, moment_from_mgf, cumulant_from_mgf,
    mgf_of_sum, convolve_dists, mgf_continuous,
    bernoulli_mgf, binomial_mgf, poisson_mgf, geometric_mgf,
    exponential_mgf, gamma_mgf, normal_mgf,
    bernoulli_dist, binomial_dist, poisson_dist, geometric_dist,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


# --- M(0)=1: the mgf at 0 is the total probability ---------------------------

def test_mgf_at_zero_is_one():
    for d in (bernoulli_dist(0.4), binomial_dist(10, 0.3),
              poisson_dist(2.5), geometric_dist(0.25)):
        assert _approx(mgf(0.0, *d), 1.0, tol=1e-9)
    # closed forms agree at t=0 too
    assert _approx(binomial_mgf(0.0, 7, 0.6), 1.0)
    assert _approx(poisson_mgf(0.0, 3.3), 1.0)
    assert _approx(normal_mgf(0.0, 2.0, 1.5), 1.0)


# --- mean and variance from M', M'' match the closed forms and ~ST-05 --------

def test_mean_variance_from_mgf_binomial():
    n, p = 10, 0.3
    d = binomial_dist(n, p)
    # M'(0)=mean, M''(0)-M'(0)^2=variance
    assert _approx(mean_from_mgf(*d), n * p, tol=1e-5)
    assert _approx(var_from_mgf(*d), n * p * (1 - p), tol=1e-5)
    # and they agree with the direct ~ST-05 definitions
    assert _approx(mean_from_mgf(*d), mean(*d), tol=1e-5)
    assert _approx(var_from_mgf(*d), variance(*d), tol=1e-5)


def test_geometric_mean_variance():
    p = 0.25
    d = geometric_dist(p)
    # geometric on {1,2,...}: mean 1/p, variance (1-p)/p^2
    assert _approx(mean_from_mgf(*d), 1.0 / p, tol=1e-5)
    assert _approx(var_from_mgf(*d), (1 - p) / p ** 2, tol=1e-4)
    # differentiate the closed-form mgf as a continuous function of t
    f = lambda t: geometric_mgf(t, p)
    from mgf import _central_derivative
    assert _approx(_central_derivative(f, 1, 0.0, 2e-3), 1.0 / p, tol=1e-6)


# --- raw moments by differentiation:  M^{(k)}(0) = E[X^k] ---------------------

def test_raw_moments_poisson():
    lam = 2.0
    d = poisson_dist(lam)
    # E[X]=lam, E[X^2]=lam+lam^2, E[X^3]=lam^3+3lam^2+lam
    assert _approx(moment_from_mgf(1, *d), lam, tol=1e-5)
    assert _approx(moment_from_mgf(2, *d), lam + lam ** 2, tol=1e-4)
    assert _approx(moment_from_mgf(3, *d), lam ** 3 + 3 * lam ** 2 + lam, tol=1e-2)
    # E[X^2] also equals var + mean^2
    assert _approx(moment_from_mgf(2, *d),
                   variance(*d) + mean(*d) ** 2, tol=1e-4)


# --- cumulants from ln M:  kappa_1=mean, kappa_2=var, Poisson kappa_k=lam -----

def test_cumulants_poisson():
    lam = 2.0
    d = poisson_dist(lam)
    assert _approx(cumulant_from_mgf(1, *d), lam, tol=1e-5)       # mean
    assert _approx(cumulant_from_mgf(2, *d), lam, tol=1e-4)       # variance
    assert _approx(cumulant_from_mgf(3, *d), lam, tol=1e-2)       # all == lam
    # kappa_2 really is the variance
    assert _approx(cumulant_from_mgf(2, *d), variance(*d), tol=1e-4)


def test_cumulants_additive_under_sum():
    # cumulants of independent sums add: kappa_2(X+Y) = Var X + Var Y
    d1, d2 = binomial_dist(8, 0.5), poisson_dist(3.0)
    conv = convolve_dists(d1, d2)
    assert _approx(cumulant_from_mgf(2, *conv),
                   variance(*d1) + variance(*d2), tol=1e-3)
    assert _approx(cumulant_from_mgf(1, *conv),
                   mean(*d1) + mean(*d2), tol=1e-4)


# --- the headline theorem: mgf of a sum of independents is the product -------

def test_mgf_of_sum_is_product_and_convolution():
    d1 = (np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]), np.full(6, 1.0 / 6))  # a die
    d2 = bernoulli_dist(0.4)
    conv = convolve_dists(d1, d2)
    for t in (-0.3, 0.0, 0.2, 0.7):
        prod = mgf(t, *d1) * mgf(t, *d2)
        assert _approx(mgf_of_sum(t, [d1, d2]), prod, tol=1e-12)
        # mgf of the convolved distribution equals that product (uniqueness)
        assert _approx(mgf(t, *conv), prod, tol=1e-10)
    # the convolution is a genuine probability distribution
    assert _approx(float(conv[1].sum()), 1.0, tol=1e-12)


def test_binomial_is_sum_of_bernoullis():
    n, p = 5, 0.3
    bern = bernoulli_dist(p)
    # convolve n iid Bernoulli(p) -> Binomial(n,p) pmf
    conv = bern
    for _ in range(n - 1):
        conv = convolve_dists(conv, bern)
    bv, bp = binomial_dist(n, p)
    assert np.allclose(conv[1], bp, atol=1e-12)
    # and the mgf factorizes: binomial_mgf = bernoulli_mgf^n
    for t in (-0.4, 0.0, 0.5):
        assert _approx(binomial_mgf(t, n, p), bernoulli_mgf(t, p) ** n)
        assert _approx(mgf_of_sum(t, [bern] * n), binomial_mgf(t, n, p), tol=1e-12)


# --- closed-form additivity of mgfs (uniqueness => the sum's distribution) ----

def test_poisson_additivity():
    l1, l2 = 2.0, 3.0
    for t in (-0.5, 0.0, 0.3, 0.8):
        assert _approx(poisson_mgf(t, l1) * poisson_mgf(t, l2),
                       poisson_mgf(t, l1 + l2))


def test_normal_additivity_and_moments():
    m1, s1, m2, s2 = 1.0, 2.0, -0.5, 1.5
    for t in (-0.4, 0.0, 0.3):
        prod = normal_mgf(t, m1, s1) * normal_mgf(t, m2, s2)
        summ = normal_mgf(t, m1 + m2, math.sqrt(s1 ** 2 + s2 ** 2))
        assert _approx(prod, summ)
    # mean and variance of a normal recovered by differentiating its mgf
    from mgf import _central_derivative
    f = lambda t: normal_mgf(t, m1, s1)
    mu = _central_derivative(f, 1)
    m2nd = _central_derivative(f, 2)
    assert _approx(mu, m1, tol=1e-6)
    assert _approx(m2nd - mu ** 2, s1 ** 2, tol=1e-5)


def test_gamma_is_sum_of_exponentials():
    alpha, lam = 4, 1.5
    for t in (-0.5, 0.0, 0.5, 1.0):
        # Gamma(alpha,lam) mgf = product of alpha Exp(lam) mgfs
        assert _approx(gamma_mgf(t, alpha, lam), exponential_mgf(t, lam) ** alpha)
    # exponential is Gamma with alpha=1
    assert _approx(gamma_mgf(0.7, 1, lam), exponential_mgf(0.7, lam))


# --- linear transform:  M_{aX+b}(t) = e^{bt} M_X(at) -------------------------

def test_linear_transform_rule():
    d = binomial_dist(6, 0.5)
    v, p = d
    a, b = 2.0, 3.0
    dt = (a * v + b, p)                        # distribution of aX+b
    for t in (-0.3, 0.0, 0.25, 0.6):
        assert _approx(mgf(t, *dt), math.exp(b * t) * mgf(a * t, *d), tol=1e-12)
    # consequence: mean(aX+b)=a mean + b
    assert _approx(mean(*dt), a * mean(*d) + b, tol=1e-12)
    assert _approx(variance(*dt), a ** 2 * variance(*d), tol=1e-12)


# --- uniqueness: distinct distributions have distinct mgfs -------------------

def test_uniqueness_distinguishes_distributions():
    d1 = binomial_dist(2, 0.5)                 # P=[1/4,1/2,1/4] on {0,1,2}
    d2 = (np.array([0.0, 1.0, 2.0]), np.array([0.3, 0.4, 0.3]))
    # same mean (=1) but different distributions -> mgfs must differ somewhere
    assert _approx(mean(*d1), mean(*d2))
    diff = max(abs(mgf(t, *d1) - mgf(t, *d2)) for t in (0.5, 1.0, 1.5))
    assert diff > 1e-3
    # identical distributions -> identical mgf everywhere
    same = max(abs(mgf(t, *d1) - mgf(t, *convolve_dists(bernoulli_dist(0.5),
                                                        bernoulli_dist(0.5))))
               for t in (-1.0, 0.0, 1.0))
    assert same < 1e-12


# --- continuous mgf by quadrature = the Laplace transform at s=-t (~MA-10) ----

def test_continuous_mgf_exponential():
    lam = 1.5
    pdf = lambda x: lam * math.exp(-lam * x)
    for t in (-1.0, 0.0, 0.5, 0.9):
        num = mgf_continuous(t, pdf, 0.0, 80.0, n=40000)
        assert _approx(num, exponential_mgf(t, lam), tol=1e-4)
    # Laplace transform L{f}(s)=integral_0^inf e^{-sx} f = M(-s); check at s=1
    s = 1.0
    laplace = mgf_continuous(-s, pdf, 0.0, 80.0, n=40000)
    assert _approx(laplace, lam / (lam + s), tol=1e-4)


def test_cgf_consistency():
    # K(0)=0 and K(t)=ln M(t) is finite and matches the log of the mgf
    d = poisson_dist(2.0)
    assert _approx(cgf(0.0, *d), 0.0, tol=1e-12)
    for t in (-0.4, 0.3, 0.7):
        assert _approx(cgf(t, *d), math.log(mgf(t, *d)), tol=1e-12)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
