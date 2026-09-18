"""Tests for ST-10 continuous random variables.  Self-contained (numpy/stdlib only).

Run:  python3 test_continuous_rv.py     ->  "All N tests passed."
"""
import math

from continuous_rv import (
    _integrate, pdf_is_normalized, cdf_from_pdf, prob_between,
    expectation_continuous, expectation_of, moment_continuous,
    variance_continuous, quantile, median_continuous,
    uniform_pdf, uniform_cdf, uniform_mean, uniform_var,
    uniform_quantile, point_mass_pdf,
)

A, B = 2.0, 8.0                      # a uniform on [2,8]
UF = lambda x: uniform_pdf(x, A, B)  # its pdf
UC = lambda x: uniform_cdf(x, A, B)  # its cdf
LIN = lambda x: 2.0 * x              # generic pdf f(x)=2x on [0,1]; cdf F(x)=x^2
LINC = lambda x: x * x


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_uniform_pdf_normalized():
    # total-probability axiom: integral of f over the support is 1
    assert pdf_is_normalized(UF, A, B)
    assert _approx(_integrate(UF, A, B), 1.0, tol=1e-9)
    # the linear pdf 2x on [0,1] is also a valid density
    assert pdf_is_normalized(LIN, 0.0, 1.0)


def test_uniform_cdf_endpoints_monotone():
    # F runs 0 -> 1 across the support, hits 1/2 at the midpoint, and is monotone
    assert _approx(uniform_cdf(A, A, B), 0.0)
    assert _approx(uniform_cdf(B, A, B), 1.0)
    assert _approx(uniform_cdf(0.5 * (A + B), A, B), 0.5)
    assert uniform_cdf(3.0, A, B) < uniform_cdf(6.0, A, B)
    # clamps outside the support
    assert uniform_cdf(A - 1.0, A, B) == 0.0 and uniform_cdf(B + 1.0, A, B) == 1.0


def test_cdf_is_integral_of_pdf():
    # F(x) = integral_a^x f  agrees with the closed-form uniform cdf
    for x in (2.0, 3.5, 5.0, 6.75, 8.0):
        assert _approx(cdf_from_pdf(UF, x, A), uniform_cdf(x, A, B), tol=1e-9)


def test_pdf_is_derivative_of_cdf():
    # f = F': central difference of the integrated cdf returns the pdf (here 2x)
    Fnum = lambda x: cdf_from_pdf(LIN, x, 0.0)
    h = 1e-3
    for x in (0.25, 0.5, 0.8):
        deriv = (Fnum(x + h) - Fnum(x - h)) / (2.0 * h)
        assert _approx(deriv, LIN(x), tol=1e-6)


def test_prob_between_and_point_has_zero_prob():
    # P(lo<X<hi) = F(hi)-F(lo)
    assert _approx(prob_between(UF, 3.0, 5.0), UC(5.0) - UC(3.0), tol=1e-9)
    assert _approx(prob_between(UF, 3.0, 5.0), 2.0 / 6.0, tol=1e-9)
    # P(X = c) = 0 for a continuous RV (zero-width interval)
    assert _approx(prob_between(UF, 5.0, 5.0), 0.0)
    assert _approx(prob_between(LIN, 0.4, 0.4), 0.0)


def test_uniform_mean_variance_formulas():
    # closed forms (a+b)/2 and (b-a)^2/12 ...
    assert _approx(uniform_mean(A, B), 5.0)
    assert _approx(uniform_var(A, B), 36.0 / 12.0)
    # ... agree with the defining integrals
    assert _approx(expectation_continuous(UF, A, B), uniform_mean(A, B), tol=1e-6)
    assert _approx(variance_continuous(UF, A, B), uniform_var(A, B), tol=1e-4)
    # E[X^2] = Var + mean^2 (shortcut identity)
    m2 = moment_continuous(UF, A, B, 2)
    assert _approx(m2, uniform_var(A, B) + uniform_mean(A, B) ** 2, tol=1e-4)


def test_generic_pdf_2x_moments():
    # f(x)=2x on [0,1]: mean 2/3, E[X^2]=1/2, var 1/18, and F(1/2)=1/4
    assert _approx(expectation_continuous(LIN, 0.0, 1.0), 2.0 / 3.0, tol=1e-6)
    assert _approx(moment_continuous(LIN, 0.0, 1.0, 2), 0.5, tol=1e-6)
    assert _approx(variance_continuous(LIN, 0.0, 1.0), 1.0 / 18.0, tol=1e-5)
    assert _approx(cdf_from_pdf(LIN, 0.5, 0.0), 0.25, tol=1e-9)
    # LOTUS sanity: E[X] via expectation_of(g=id) equals the direct mean
    assert _approx(expectation_of(lambda x: x, LIN, 0.0, 1.0),
                   expectation_continuous(LIN, 0.0, 1.0), tol=1e-9)


def test_quantile_inverts_cdf():
    # F(quantile(F,p)) = p for the uniform and the 2x (F=x^2) laws
    for p in (0.1, 0.37, 0.5, 0.9):
        xp = quantile(UC, p, A, B)
        assert _approx(UC(xp), p, tol=1e-8)
        yp = quantile(LINC, p, 0.0, 1.0)
        assert _approx(LINC(yp), p, tol=1e-8)
    # the 0.25 quantile of f=2x is sqrt(0.25)=1/2
    assert _approx(quantile(LINC, 0.25, 0.0, 1.0), 0.5, tol=1e-8)


def test_uniform_quantile_and_median():
    # closed-form percentile a+p(b-a) matches bisection on the cdf
    for p in (0.05, 0.25, 0.5, 0.75, 0.95):
        assert _approx(uniform_quantile(p, A, B), A + p * (B - A))
        assert _approx(uniform_quantile(p, A, B), quantile(UC, p, A, B), tol=1e-8)
    # median of a (symmetric) uniform is its mean
    assert _approx(median_continuous(UC, A, B), uniform_mean(A, B), tol=1e-8)


def test_point_mass_delta_limit():
    # nascent-delta box density: normalized, symmetric mean -> c, Var = eps^2/3 -> 0
    c = 4.0
    prev_var = None
    for eps in (0.5, 0.1, 0.01):
        pm = lambda x, e=eps: point_mass_pdf(x, c, e)
        assert pdf_is_normalized(pm, c - eps, c + eps)
        assert _approx(expectation_continuous(pm, c - eps, c + eps), c, tol=1e-6)
        var = variance_continuous(pm, c - eps, c + eps)
        assert _approx(var, eps ** 2 / 3.0, tol=1e-4)
        if prev_var is not None:
            assert var < prev_var          # variance shrinks toward the point mass
        prev_var = var


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
