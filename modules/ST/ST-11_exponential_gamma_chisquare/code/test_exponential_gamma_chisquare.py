"""Tests for ST-11 exponential, gamma & chi-square.  Self-contained (no siblings).

Run:  python3 test_exponential_gamma_chisquare.py   ->  "All N tests passed."
"""
import math

from exponential_gamma_chisquare import (
    gamma_function, gamma_lanczos,
    exponential_pdf, exponential_cdf, exponential_mean, exponential_var,
    exponential_mgf, exp_memoryless_check,
    gamma_pdf, gamma_cdf, gamma_mean, gamma_var, gamma_mgf,
    chi2_pdf, chi2_cdf, chi2_mean, chi2_var, chi2_mgf,
    convolve_two_exponentials_pdf, simulate_sum_of_exponentials,
    lower_incomplete_gamma_regularized,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _integrate(f, a, b, n=20000):
    dx = (b - a) / n
    return sum(f(a + (i + 0.5) * dx) * dx for i in range(n))


def _mgf_moments(M, h=1e-4):
    """Numerical M'(0) and M''(0) by central differences."""
    m1 = (M(h) - M(-h)) / (2.0 * h)
    m2 = (M(h) - 2.0 * M(0.0) + M(-h)) / (h * h)
    return m1, m2


# --- the gamma function ------------------------------------------------------

def test_gamma_factorial_and_half():
    # Gamma(n) = (n-1)!  and  Gamma(1/2) = sqrt(pi)
    for n in (1, 2, 3, 4, 5, 6):
        assert _approx(gamma_function(n), math.factorial(n - 1))
    assert _approx(gamma_function(0.5), math.sqrt(math.pi))


def test_gamma_recursion():
    # Gamma(a+1) = a Gamma(a) for non-integer arguments too
    for a in (0.3, 0.5, 1.7, 2.4, 4.9):
        assert _approx(gamma_function(a + 1.0), a * gamma_function(a))


def test_gamma_lanczos_matches():
    for z in (0.25, 0.5, 1.0, 1.5, 3.0, 5.7, 8.2):
        assert _approx(gamma_lanczos(z), math.gamma(z), tol=1e-10)


# --- exponential -------------------------------------------------------------

def test_exponential_normalizes():
    lam = 0.7
    total = _integrate(lambda x: exponential_pdf(x, lam), 0.0, 200.0)
    assert _approx(total, 1.0, tol=1e-5)


def test_exponential_mean_var_by_integration():
    lam = 0.7
    m = _integrate(lambda x: x * exponential_pdf(x, lam), 0.0, 300.0)
    m2 = _integrate(lambda x: x * x * exponential_pdf(x, lam), 0.0, 300.0)
    assert _approx(m, exponential_mean(lam), tol=1e-4)        # 1/lam
    assert _approx(m2 - m * m, exponential_var(lam), tol=1e-3)  # 1/lam^2


def test_exponential_cdf_closed_form():
    lam = 1.3
    for x in (0.0, 0.5, 1.0, 3.0):
        assert _approx(exponential_cdf(x, lam), 1.0 - math.exp(-lam * x))
    # cdf = integral of pdf, and -> 1 in the tail
    assert _approx(exponential_cdf(2.0, lam),
                   _integrate(lambda x: exponential_pdf(x, lam), 0.0, 2.0), tol=1e-4)
    assert _approx(exponential_cdf(50.0, lam), 1.0, tol=1e-9)


def test_exponential_mgf_gives_mean_and_var():
    lam = 1.5
    m1, m2 = _mgf_moments(lambda t: exponential_mgf(t, lam))
    assert _approx(m1, exponential_mean(lam), tol=1e-4)         # M'(0) = mean
    assert _approx(m2 - m1 * m1, exponential_var(lam), tol=1e-3)  # Var = M''(0)-M'(0)^2


def test_exponential_memoryless():
    lam = 0.4
    cond, marg = exp_memoryless_check(3.0, 2.0, lam)
    assert _approx(cond, marg)                 # P(X>s+t|X>s) = P(X>t)
    assert _approx(marg, math.exp(-lam * 2.0))


# --- gamma -------------------------------------------------------------------

def test_gamma_reduces_to_exponential():
    # shape a = 1 gives the exponential with rate 1/theta
    theta, lam = 2.5, 1.0 / 2.5
    for x in (0.3, 1.0, 4.0, 9.0):
        assert _approx(gamma_pdf(x, 1.0, theta), exponential_pdf(x, lam))


def test_gamma_normalizes():
    a, th = 3.0, 2.0
    total = _integrate(lambda x: gamma_pdf(x, a, th), 0.0, 120.0)
    assert _approx(total, 1.0, tol=1e-4)


def test_gamma_mean_var_by_integration():
    a, th = 3.0, 2.0
    m = _integrate(lambda x: x * gamma_pdf(x, a, th), 0.0, 160.0)
    m2 = _integrate(lambda x: x * x * gamma_pdf(x, a, th), 0.0, 160.0)
    assert _approx(m, gamma_mean(a, th), tol=1e-4)          # a theta = 6
    assert _approx(m2 - m * m, gamma_var(a, th), tol=1e-3)  # a theta^2 = 12


def test_gamma_mgf_gives_mean_and_var():
    a, th = 3.0, 2.0
    m1, m2 = _mgf_moments(lambda t: gamma_mgf(t, a, th))
    assert _approx(m1, gamma_mean(a, th), tol=1e-4)
    assert _approx(m2 - m1 * m1, gamma_var(a, th), tol=1e-3)


def test_gamma_cdf_consistency():
    a, th = 3.0, 2.0
    # cdf equals the integral of the pdf
    assert _approx(gamma_cdf(6.0, a, th),
                   _integrate(lambda x: gamma_pdf(x, a, th), 0.0, 6.0), tol=1e-4)
    # for a = 1 the cdf reduces to the exponential 1 - e^{-x/theta}
    for x in (0.5, 2.0, 5.0):
        assert _approx(gamma_cdf(x, 1.0, th), 1.0 - math.exp(-x / th), tol=1e-8)
    # regularized lower incomplete gamma is monotone in [0,1]
    assert lower_incomplete_gamma_regularized(a, 1.0) < lower_incomplete_gamma_regularized(a, 10.0)


# --- sum of exponentials is gamma --------------------------------------------

def test_sum_of_two_exponentials_is_gamma():
    lam, th = 0.8, 1.0 / 0.8
    # closed-form convolution lam^2 x e^{-lam x} equals gamma(a=2, theta=1/lam)
    for x in (0.5, 2.0, 5.0):
        assert _approx(convolve_two_exponentials_pdf(x, lam), gamma_pdf(x, 2.0, th))
    # and it integrates to 1
    total = _integrate(lambda x: convolve_two_exponentials_pdf(x, lam), 0.0, 100.0)
    assert _approx(total, 1.0, tol=1e-4)


def test_sum_of_exponentials_mgf_identity():
    # mgf of a sum of a iid Exp(scale theta) = product = (1-theta t)^{-a} = gamma mgf
    a, th, t = 4.0, 1.5, 0.2
    exp_mgf = exponential_mgf(t, 1.0 / th)            # one exponential, rate 1/theta
    assert _approx(exp_mgf ** a, gamma_mgf(t, a, th))


def test_sum_of_exponentials_monte_carlo():
    a, th = 3.0, 2.0
    sm, sv = simulate_sum_of_exponentials(a, th, n=200000, seed=0)
    assert _approx(sm, gamma_mean(a, th), tol=0.02)   # -> a theta = 6
    assert _approx(sv, gamma_var(a, th), tol=0.05)    # -> a theta^2 = 12


# --- chi-square --------------------------------------------------------------

def test_chi2_is_gamma_half_two():
    r = 5
    for x in (0.5, 2.0, 7.0, 12.0):
        assert _approx(chi2_pdf(x, r), gamma_pdf(x, r / 2.0, 2.0))


def test_chi2_mean_var():
    for r in (1, 2, 4, 7, 10):
        assert _approx(chi2_mean(r), r)        # mean = r
        assert _approx(chi2_var(r), 2.0 * r)   # var  = 2r
    # check against gamma(r/2, 2): a theta = r, a theta^2 = 2r
    assert _approx(gamma_mean(4 / 2.0, 2.0), chi2_mean(4))
    assert _approx(gamma_var(4 / 2.0, 2.0), chi2_var(4))


def test_chi2_mgf_gives_mean_and_var():
    r = 6
    m1, m2 = _mgf_moments(lambda t: chi2_mgf(t, r))
    assert _approx(m1, chi2_mean(r), tol=1e-4)
    assert _approx(m2 - m1 * m1, chi2_var(r), tol=1e-3)


def test_chi2_two_df_is_exponential_mean_two():
    # chi^2_2 = gamma(1, 2) = exponential with rate 1/2 (mean 2)
    for x in (0.5, 2.0, 6.0):
        assert _approx(chi2_pdf(x, 2), exponential_pdf(x, 0.5))
        assert _approx(chi2_cdf(x, 2), 1.0 - math.exp(-x / 2.0), tol=1e-8)


def test_chi2_normalizes():
    total = _integrate(lambda x: chi2_pdf(x, 4), 0.0, 120.0)
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
