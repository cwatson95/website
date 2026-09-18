"""Tests for ST-18 the central limit theorem & approximations.

Run:  python3 test_clt.py     ->  "All N tests passed."

Each test asserts a headline analytic identity: Phi via erf and as an integral of
phi; convolution preserves total mass and adds means/variances; the standardized
cdf gap shrinks like 1/sqrt(n) and obeys the Berry-Esseen bound; the continuity
correction improves the binomial/Poisson normal approximations; and the de
Moivre-Laplace local limit.
"""
import math

import numpy as np

from clt import (
    SQRT_2PI, standard_normal_pdf, standard_normal_cdf, _integrate,
    convolve_pmf, nfold_pmf, pmf_mean, pmf_var, pmf_third_abs_moment,
    die_pmf, bernoulli_pmf_array,
    clt_cdf_max_error, clt_demo, kolmogorov_cdf_error, berry_esseen_bound,
    binom_pmf, binom_cdf, poisson_pmf, poisson_cdf,
    normal_approx_binomial, normal_approx_binomial_interval,
    de_moivre_laplace_pmf, normal_approx_poisson,
    binomial_approx_max_error, poisson_approx_max_error,
    binomial_approx_error_table, normal_approx_applicable,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_standard_normal_cdf_via_erf_and_integral():
    # Phi(0)=1/2, reflection Phi(-z)=1-Phi(z), and Phi = int_{-inf}^z phi
    assert _approx(float(standard_normal_cdf(0.0)), 0.5)
    for z in (0.3, 1.0, 1.96, 2.5):
        assert _approx(float(standard_normal_cdf(-z)),
                       1.0 - float(standard_normal_cdf(z)))
    # the limit law is the integral of its own density (continuous check)
    integ = _integrate(lambda t: float(standard_normal_pdf(t)), -40.0, 1.0, 80000)
    assert _approx(integ, float(standard_normal_cdf(1.0)), tol=1e-5)
    assert _approx(float(standard_normal_pdf(0.0)), 1.0 / SQRT_2PI)


def test_convolution_normalization_and_moments():
    # pmf of S_n = sum of n i.i.d. dice: total mass 1, mean=n*mu, var=n*sigma^2
    die = die_pmf()
    mu, var = pmf_mean(die), pmf_var(die)
    assert _approx(mu, 3.5) and _approx(var, 35.0 / 12.0)
    n = 5
    conv = nfold_pmf(die, n)
    assert _approx(float(np.sum(conv)), 1.0)
    assert _approx(pmf_mean(conv), n * mu)
    assert _approx(pmf_var(conv), n * var)          # variances add under convolution
    # convolve_pmf agrees with one step of nfold
    assert np.allclose(convolve_pmf(die, die), nfold_pmf(die, 2))


def test_clt_cdf_error_shrinks_to_zero():
    # the standardized cdf converges to Phi: max gap decreases monotonically
    die = die_pmf()
    errs = [clt_cdf_max_error(die, n) for n in (1, 2, 4, 8, 16, 32, 64)]
    for a, b in zip(errs, errs[1:]):
        assert b < a                                 # strictly shrinking
    assert errs[-1] < 1e-3                            # essentially Gaussian by n=64
    # a skewed parent (Bernoulli p=0.2) also converges
    sk = bernoulli_pmf_array(0.2)
    assert clt_cdf_max_error(sk, 64) < clt_cdf_max_error(sk, 4)


def test_clt_root_n_rate():
    # CLT rate: the gap is O(1/sqrt(n)), so error*sqrt(n) stays bounded
    die = die_pmf()
    for n, err in clt_demo(die):
        assert err * math.sqrt(n) < 0.1


def test_berry_esseen_bound_holds():
    # Kolmogorov distance <= C rho/(sigma^3 sqrt n) for every n
    die = die_pmf()
    for n in (1, 2, 4, 8, 16):
        assert kolmogorov_cdf_error(die, n) <= berry_esseen_bound(die, n)
    # the bound itself decays like 1/sqrt(n): doubling n divides it by sqrt(2)
    assert _approx(berry_esseen_bound(die, 1) / berry_esseen_bound(die, 4), 2.0)


def test_binomial_continuity_correction_helps():
    # P(X<=k) for Bin(20,0.5): continuity correction is much closer than without
    n, p = 20, 0.5
    for k in (7, 10, 13):
        exact = binom_cdf(k, n, p)
        cc = normal_approx_binomial(k, n, p, continuity=True)
        nc = normal_approx_binomial(k, n, p, continuity=False)
        assert abs(cc - exact) < abs(nc - exact)
    # the famous symmetric value: P(X<=10) ~ Phi((10.5-10)/sqrt5)
    assert _approx(normal_approx_binomial(10, 20, 0.5),
                   float(standard_normal_cdf(0.5 / math.sqrt(5.0))))
    assert _approx(binom_cdf(10, 20, 0.5), 0.5881, tol=1e-3)


def test_binomial_interval_matches_exact():
    # continuity-corrected P(a<=X<=b) ~ Phi((b+.5-mu)/s) - Phi((a-.5-mu)/s)
    n, p = 100, 0.5
    mu, s = n * p, math.sqrt(n * p * 0.5)
    approx = normal_approx_binomial_interval(40, 60, n, p)
    hand = (float(standard_normal_cdf((60 + 0.5 - mu) / s))
            - float(standard_normal_cdf((40 - 0.5 - mu) / s)))
    assert _approx(approx, hand)
    exact = binom_cdf(60, n, p) - binom_cdf(39, n, p)   # P(40<=X<=60)
    assert _approx(approx, exact, tol=2e-3)


def test_de_moivre_laplace_local():
    # local limit: P(X=k) ~ (1/sigma) phi((k-np)/sigma) near the centre
    n, p = 20, 0.5
    for k in (8, 10, 12):
        assert _approx(de_moivre_laplace_pmf(k, n, p), binom_pmf(k, n, p), tol=5e-3)
    # the local densities sum to ~1 across the support
    total = sum(de_moivre_laplace_pmf(k, n, p) for k in range(n + 1))
    assert _approx(total, 1.0, tol=1e-2)


def test_poisson_normal_approx_limit():
    # Poisson(lam) -> N(lam, lam): continuity correction helps, error -> 0
    for lam in (16.0, 64.0):
        k = int(lam)
        exact = poisson_cdf(k, lam)
        cc = normal_approx_poisson(k, lam, continuity=True)
        nc = normal_approx_poisson(k, lam, continuity=False)
        assert abs(cc - exact) < abs(nc - exact)
    # max error shrinks as lambda grows (sigma=sqrt(lam) grows)
    e4 = poisson_approx_max_error(4.0)
    e64 = poisson_approx_max_error(64.0)
    assert e64 < e4
    # ~1/sqrt(lam) rate: lam x16 roughly quarters the error
    assert poisson_approx_max_error(64.0) < 0.6 * poisson_approx_max_error(16.0)


def test_binomial_error_table_decreasing():
    # at fixed p the continuity-corrected max cdf error falls toward zero with n
    table = binomial_approx_error_table(0.5)
    errs = [e for _, e in table]
    for a, b in zip(errs, errs[1:]):
        assert b < a
    # the continuity correction beats the uncorrected approximation at every n
    for n, e_cc in table:
        assert e_cc < binomial_approx_max_error(n, 0.5, continuity=False)


def test_exact_pmf_cdf_sanity():
    # binomial and Poisson pmfs are valid; cdfs are monotone and reach 1
    assert _approx(sum(binom_pmf(k, 12, 0.3) for k in range(13)), 1.0)
    assert _approx(binom_cdf(12, 12, 0.3), 1.0)
    assert binom_cdf(5, 12, 0.3) >= binom_cdf(4, 12, 0.3)
    assert _approx(sum(poisson_pmf(k, 5.0) for k in range(60)), 1.0, tol=1e-9)
    assert poisson_cdf(7, 5.0) >= poisson_cdf(6, 5.0)
    # mean=variance signature of the Poisson lives inside the approximation
    assert _approx(poisson_pmf(0, 3.0), math.exp(-3.0))


def test_normal_approx_applicable_rule():
    # rule of thumb np>=5 and n(1-p)>=5
    assert normal_approx_applicable(20, 0.5)
    assert not normal_approx_applicable(8, 0.5)        # np=4 < 5
    assert not normal_approx_applicable(40, 0.1)       # np=4 < 5
    assert normal_approx_applicable(100, 0.05)         # np=5 ok, n(1-p)=95


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
