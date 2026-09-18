"""Tests for ST-07 the binomial distribution.

Asserts the headline analytic identities of Bin(n,p): the pmf is a valid pmf
(nonnegative, sums to 1 via the binomial theorem), the closed-form mean np and
variance np(1-p) reproduce the definitional sums, M(0)=1 with M'(0)=mean and
M''(0)-M'(0)^2=variance, the pgf gives the factorial moments, the mode is the
argmax, the sum of independent binomials with common p is binomial, and the
Poisson (~ST-09) and normal (~ST-18) limits hold.

Run:  python3 test_binomial.py     ->  "All N tests passed."
"""

import math

from binomial import (
    bernoulli_pmf, bernoulli_mean, bernoulli_var,
    binom_pmf, binom_cdf, binom_mean, binom_var, binom_std, binom_skewness,
    binom_mgf, binom_pgf, binom_mode, sum_two_binomials_pmf,
    _deriv1, _deriv2, _poisson_pmf, _normal_pdf,
)

# a spread of (n,p) cases used across the tests
CASES = [(1, 0.5), (5, 0.3), (8, 0.5), (10, 0.35), (12, 0.7), (20, 0.4), (30, 0.9)]


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


# --- Bernoulli is the n=1 binomial -------------------------------------------

def test_bernoulli_is_binom_n1():
    for p in (0.0, 0.2, 0.5, 0.8, 1.0):
        assert _approx(bernoulli_pmf(0, p), binom_pmf(0, 1, p))
        assert _approx(bernoulli_pmf(1, p), binom_pmf(1, 1, p))
        assert _approx(bernoulli_pmf(0, p) + bernoulli_pmf(1, p), 1.0)
        # Bernoulli mean p, variance p(1-p), matching the binomial formulas at n=1
        assert _approx(bernoulli_mean(p), binom_mean(1, p))
        assert _approx(bernoulli_var(p), binom_var(1, p))


# --- the pmf is a valid pmf (binomial theorem) -------------------------------

def test_pmf_nonnegative_and_zero_outside_support():
    for n, p in CASES:
        for k in range(0, n + 1):
            assert binom_pmf(k, n, p) >= 0.0
        assert binom_pmf(-1, n, p) == 0.0
        assert binom_pmf(n + 1, n, p) == 0.0


def test_pmf_sums_to_one():
    # sum_k C(n,k) p^k q^{n-k} = (p+q)^n = 1
    for n, p in CASES:
        total = sum(binom_pmf(k, n, p) for k in range(0, n + 1))
        assert _approx(total, 1.0)


# --- mean and variance: closed form == definitional sum ----------------------

def test_mean_equals_np():
    for n, p in CASES:
        m = sum(k * binom_pmf(k, n, p) for k in range(0, n + 1))
        assert _approx(m, binom_mean(n, p))
        assert _approx(binom_mean(n, p), n * p)


def test_variance_equals_npq():
    for n, p in CASES:
        m = binom_mean(n, p)
        v = sum((k - m) ** 2 * binom_pmf(k, n, p) for k in range(0, n + 1))
        assert _approx(v, binom_var(n, p))
        assert _approx(binom_var(n, p), n * p * (1.0 - p))
        # E[X^2] - (E[X])^2 form as well
        ex2 = sum(k * k * binom_pmf(k, n, p) for k in range(0, n + 1))
        assert _approx(ex2 - m * m, binom_var(n, p))
        assert _approx(binom_std(n, p), math.sqrt(binom_var(n, p)))


# --- cdf ---------------------------------------------------------------------

def test_cdf_monotone_endpoints_and_pmf_link():
    for n, p in CASES:
        prev = -1.0
        for k in range(0, n + 1):
            c = binom_cdf(k, n, p)
            assert c >= prev - 1e-15          # nondecreasing
            prev = c
            # F(k) - F(k-1) = P(X=k)
            assert _approx(binom_cdf(k, n, p) - binom_cdf(k - 1, n, p),
                           binom_pmf(k, n, p))
        assert _approx(binom_cdf(n, n, p), 1.0)
        assert binom_cdf(-1, n, p) == 0.0


# --- mgf: value and moments by differentiation -------------------------------

def test_mgf_value_and_derivatives():
    for n, p in CASES:
        M = lambda t: binom_mgf(t, n, p)
        assert _approx(M(0.0), 1.0)                       # M(0)=1 always
        # M'(0) = E[X] = np
        assert _approx(_deriv1(M, 0.0), binom_mean(n, p), tol=1e-5)
        # M''(0) = E[X^2] = npq + (np)^2
        ex2 = binom_var(n, p) + binom_mean(n, p) ** 2
        assert _approx(_deriv2(M, 0.0), ex2, tol=1e-4)
        # Var = M''(0) - M'(0)^2
        var_mgf = _deriv2(M, 0.0) - _deriv1(M, 0.0) ** 2
        assert _approx(var_mgf, binom_var(n, p), tol=1e-4)


def test_mgf_is_product_of_bernoulli_mgfs():
    # (q + p e^t)^n = [ (q + p e^t)^1 ]^n  -- sum of n iid Bernoulli mgfs multiply
    for n, p in CASES:
        for t in (-0.3, 0.0, 0.4, 1.1):
            assert _approx(binom_mgf(t, n, p), binom_mgf(t, 1, p) ** n)


# --- pgf: factorial moments --------------------------------------------------

def test_pgf_normalization_and_factorial_moments():
    for n, p in CASES:
        G = lambda s: binom_pgf(s, n, p)
        assert _approx(G(1.0), 1.0)                       # G(1)=sum pmf=1
        assert _approx(G(0.0), (1.0 - p) ** n)            # G(0)=P(X=0)=q^n
        # G'(1) = E[X] = np
        assert _approx(_deriv1(G, 1.0), binom_mean(n, p), tol=1e-5)
        # G''(1) = E[X(X-1)] = n(n-1)p^2 ; then Var = G''(1)+G'(1)-G'(1)^2
        g2 = _deriv2(G, 1.0)
        assert _approx(g2, n * (n - 1) * p * p, tol=1e-3)
        var_pgf = g2 + _deriv1(G, 1.0) - _deriv1(G, 1.0) ** 2
        assert _approx(var_pgf, binom_var(n, p), tol=1e-3)


# --- mode is the argmax ------------------------------------------------------

def test_mode_is_argmax():
    for n, p in CASES:
        m = binom_mode(n, p)
        assert 0 <= m <= n
        pm = binom_pmf(m, n, p)
        # the mode is at least as likely as either neighbour
        assert pm >= binom_pmf(m - 1, n, p) - 1e-15
        assert pm >= binom_pmf(m + 1, n, p) - 1e-15
        # brute-force argmax agrees with floor((n+1)p) up to ties
        kbest = max(range(0, n + 1), key=lambda k: binom_pmf(k, n, p))
        assert _approx(binom_pmf(kbest, n, p), pm)


# --- skewness: symmetric at p=1/2, signs otherwise ---------------------------

def test_skewness_sign():
    assert _approx(binom_skewness(10, 0.5), 0.0)          # symmetric
    assert binom_skewness(10, 0.2) > 0.0                  # right-skewed, p<1/2
    assert binom_skewness(10, 0.8) < 0.0                  # left-skewed, p>1/2


# --- additivity: sum of independent binomials (common p) ---------------------

def test_sum_of_binomials_is_binomial():
    p = 0.4
    for n1, n2 in [(3, 4), (5, 5), (2, 7), (6, 9)]:
        for k in range(0, n1 + n2 + 1):
            assert _approx(sum_two_binomials_pmf(k, n1, n2, p),
                           binom_pmf(k, n1 + n2, p))
        # mean and variance add
        assert _approx(binom_mean(n1, p) + binom_mean(n2, p),
                       binom_mean(n1 + n2, p))
        assert _approx(binom_var(n1, p) + binom_var(n2, p),
                       binom_var(n1 + n2, p))


# --- Poisson limit (~ST-09) --------------------------------------------------

def test_poisson_limit():
    lam = 2.5
    errs = []
    for n in (50, 500, 5000):
        p = lam / n
        e = max(abs(binom_pmf(k, n, p) - _poisson_pmf(k, lam)) for k in range(0, 12))
        errs.append(e)
    # error shrinks ~1/n and the finest grid is tight
    assert errs[0] > errs[1] > errs[2]
    assert errs[-1] < 1e-3


# --- normal / de Moivre-Laplace limit (~ST-18) -------------------------------

def test_normal_approximation_near_peak():
    n, p = 100, 0.5
    mu, sig = binom_mean(n, p), binom_std(n, p)
    for k in (45, 48, 50, 52, 55):
        assert _approx(binom_pmf(k, n, p), _normal_pdf(k, mu, sig), tol=3e-3)


# --- midpoint integrator sanity (used for continuous downstream checks) ------

def test_integrator_normalizes_a_pdf():
    from binomial import _integrate
    mu, sig = 5.0, 2.0
    total = _integrate(lambda x: _normal_pdf(x, mu, sig), mu - 12 * sig, mu + 12 * sig)
    assert _approx(total, 1.0, tol=1e-4)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
