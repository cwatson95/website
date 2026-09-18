"""Tests for ST-12 the normal distribution.

Run:  python3 test_normal.py     ->  "All N tests passed."

Each test asserts a headline analytic identity of N(mu, sigma^2): the Gaussian
integral, normalization, mean = mu, variance = sigma^2, standardization,
Phi via erf, mgf = exp(mu t + sigma^2 t^2/2) generating the moments, the inverse
cdf, and the 68-95-99.7 rule.
"""
import math

from normal import (
    SQRT_2PI, normal_pdf, standard_normal_pdf, standardize, standard_normal_cdf,
    normal_cdf, normal_interval_prob, gaussian_integral_check,
    normal_mean_by_integration, normal_variance_by_integration, normal_mgf,
    mgf_moment, probit, normal_quantile, empirical_rule, _integrate,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_gaussian_integral_equals_sqrt_2pi():
    # int exp(-x^2/2) dx = sqrt(2 pi); and the pdf prefactor is its reciprocal
    assert _approx(gaussian_integral_check(), SQRT_2PI, tol=1e-6)
    assert _approx(SQRT_2PI, math.sqrt(2.0 * math.pi))
    assert _approx(float(standard_normal_pdf(0.0)), 1.0 / SQRT_2PI)


def test_pdf_normalizes_to_one():
    # int f(x) dx = 1 for a non-standard normal
    mu, sigma = 3.0, 2.0
    total = _integrate(lambda x: float(normal_pdf(x, mu, sigma)),
                       mu - 14 * sigma, mu + 14 * sigma, 60000)
    assert _approx(total, 1.0, tol=1e-6)


def test_pdf_peaks_at_mean_and_is_symmetric():
    mu, sigma = 1.5, 0.7
    peak = float(normal_pdf(mu, mu, sigma))
    assert peak > float(normal_pdf(mu + sigma, mu, sigma))
    assert peak > float(normal_pdf(mu - sigma, mu, sigma))
    # symmetry f(mu+d) = f(mu-d), and peak height = 1/(sigma sqrt(2pi))
    assert _approx(float(normal_pdf(mu + 0.9, mu, sigma)),
                   float(normal_pdf(mu - 0.9, mu, sigma)))
    assert _approx(peak, 1.0 / (sigma * SQRT_2PI))


def test_standardization_reduces_to_standard_normal():
    # f(x; mu, sigma) = (1/sigma) phi(z),  F(x; mu, sigma) = Phi(z)
    mu, sigma, x = -2.0, 3.0, 4.0
    z = standardize(x, mu, sigma)
    assert _approx(z, (x - mu) / sigma)
    assert _approx(float(normal_pdf(x, mu, sigma)),
                   float(standard_normal_pdf(z)) / sigma)
    assert _approx(float(normal_cdf(x, mu, sigma)),
                   float(standard_normal_cdf(z)))


def test_standard_normal_cdf_via_erf():
    # Phi(0) = 1/2, the symmetry Phi(-z) = 1 - Phi(z), and 1.96 ~ 0.975
    assert _approx(float(standard_normal_cdf(0.0)), 0.5)
    for z in (0.3, 1.0, 2.5):
        assert _approx(float(standard_normal_cdf(-z)),
                       1.0 - float(standard_normal_cdf(z)))
    assert _approx(float(standard_normal_cdf(1.959963985)), 0.975, tol=1e-7)


def test_cdf_is_integral_of_pdf():
    # F(x) = int_{-inf}^x f(t) dt  (compare numeric integral to erf-based cdf)
    mu, sigma, x = 0.5, 1.4, 1.3
    numeric = _integrate(lambda t: float(normal_pdf(t, mu, sigma)),
                         mu - 14 * sigma, x, 40000)
    assert _approx(numeric, float(normal_cdf(x, mu, sigma)), tol=1e-5)
    # interval probability = difference of cdf values
    assert _approx(float(normal_interval_prob(0.0, 1.0, mu, sigma)),
                   float(normal_cdf(1.0, mu, sigma)) - float(normal_cdf(0.0, mu, sigma)))


def test_mean_and_variance_by_integration():
    mu, sigma = 3.0, 2.0
    assert _approx(normal_mean_by_integration(mu, sigma), mu, tol=1e-5)
    assert _approx(normal_variance_by_integration(mu, sigma), sigma ** 2, tol=1e-4)


def test_mgf_value_and_generated_moments():
    mu, sigma = 3.0, 2.0
    # M(0) = 1 always
    assert _approx(float(normal_mgf(0.0, mu, sigma)), 1.0)
    # M'(0) = E[X] = mu ; M''(0) = E[X^2] = mu^2 + sigma^2 ; var = E[X^2]-mu^2
    assert _approx(mgf_moment(1, mu, sigma), mu, tol=1e-5)
    assert _approx(mgf_moment(2, mu, sigma), mu ** 2 + sigma ** 2, tol=1e-4)
    var = mgf_moment(2, mu, sigma) - mgf_moment(1, mu, sigma) ** 2
    assert _approx(var, sigma ** 2, tol=1e-3)


def test_mgf_factorizes_under_standardization():
    # M_X(t) = exp(mu t) M_Z(sigma t), with M_Z(s) = exp(s^2/2)
    mu, sigma, t = 1.0, 2.5, 0.4
    lhs = float(normal_mgf(t, mu, sigma))
    rhs = math.exp(mu * t) * float(normal_mgf(sigma * t, 0.0, 1.0))
    assert _approx(lhs, rhs)
    assert _approx(float(normal_mgf(t, 0.0, 1.0)), math.exp(0.5 * t * t))


def test_probit_inverts_the_cdf():
    # Phi(Phi^{-1}(p)) = p ; Phi^{-1}(1/2) = 0 ; odd symmetry of the quantile
    assert _approx(probit(0.5), 0.0, tol=1e-9)
    for p in (0.1, 0.25, 0.975, 0.999):
        assert _approx(float(standard_normal_cdf(probit(p))), p, tol=1e-9)
    assert _approx(probit(0.25), -probit(0.75), tol=1e-9)
    # IQ-style quantile: N(100,15^2) 97.5th percentile ~ 100 + 1.96*15
    assert _approx(normal_quantile(0.975, 100.0, 15.0),
                   100.0 + probit(0.975) * 15.0)


def test_empirical_rule_68_95_997():
    assert _approx(empirical_rule(1), 0.6827, tol=1e-3)
    assert _approx(empirical_rule(2), 0.9545, tol=1e-3)
    assert _approx(empirical_rule(3), 0.9973, tol=1e-3)
    # consistency with the cdf:  2 Phi(k) - 1
    for k in (1, 2, 3):
        assert _approx(empirical_rule(k), 2 * float(standard_normal_cdf(k)) - 1.0)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
