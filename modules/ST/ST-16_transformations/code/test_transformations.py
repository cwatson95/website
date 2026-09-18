"""Tests for ST-16 transformations of random variables.

Run:  python3 test_transformations.py     ->  "All N tests passed."
Asserts the headline analytic identities of L22-L24: change-of-variables,
the cdf method, convolution -> triangular / gamma, the 2-D Jacobian, and the
probability integral transform.
"""
import math

import numpy as np

from transformations import (
    _integrate, _diff, uniform_pdf, exp_pdf, exp_cdf, exp_quantile,
    linear_pdf, linear_quantile, gamma_pdf, triangular_pdf, normal_pdf,
    normal_cdf, cdf_of_Y, pdf_of_Y_cdf_method, change_of_variables_1d,
    jacobian_det_2d, jacobian_transform_2d, convolution,
    sum_two_uniforms_pdf, sum_n_exponentials_pdf,
    probability_integral_transform_pdf,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


# --- the target densities are genuine probability densities ------------------

def test_target_densities_normalized():
    assert _approx(_integrate(uniform_pdf, -1.0, 2.0), 1.0, tol=1e-4)
    assert _approx(_integrate(lambda x: exp_pdf(x, 1.5), 0.0, 40.0), 1.0, tol=1e-4)
    assert _approx(_integrate(lambda x: gamma_pdf(x, 3.0, 1.0), 0.0, 60.0), 1.0, tol=1e-4)
    assert _approx(_integrate(triangular_pdf, 0.0, 2.0), 1.0, tol=1e-4)
    assert _approx(_integrate(linear_pdf, 0.0, 1.0), 1.0, tol=1e-5)
    assert _approx(_integrate(normal_pdf, -10.0, 10.0), 1.0, tol=1e-4)


def test_gamma_mean_and_variance():
    # Gamma(k,rate): mean = k/rate, variance = k/rate^2
    k, rate = 3.0, 1.5
    m = _integrate(lambda x: x * gamma_pdf(x, k, rate), 0.0, 80.0)
    m2 = _integrate(lambda x: x * x * gamma_pdf(x, k, rate), 0.0, 80.0)
    assert _approx(m, k / rate, tol=1e-3)
    assert _approx(m2 - m * m, k / rate ** 2, tol=1e-3)


# --- the cdf (distribution-function) method ----------------------------------

def test_cdf_method_square_uniform():
    # X~U(0,1), Y=X^2 => F_Y(y)=sqrt(y), f_Y(y)=1/(2 sqrt y)
    for y in (0.16, 0.36, 0.64):
        F = cdf_of_Y(uniform_pdf, lambda x: x * x, y, 0.0, 1.0)
        assert _approx(F, math.sqrt(y), tol=2e-3)
        f = pdf_of_Y_cdf_method(uniform_pdf, lambda x: x * x, y, 0.0, 1.0)
        assert _approx(f, 1.0 / (2.0 * math.sqrt(y)), tol=2e-2)


def test_cdf_method_normal_square_is_chisquare():
    # X~N(0,1), Y=X^2 ~ chi-square(1) = Gamma(1/2,1/2)  (the ~ST-17 result)
    for y in (0.5, 1.0, 2.0):
        f = pdf_of_Y_cdf_method(normal_pdf, lambda x: x * x, y, -12.0, 12.0)
        chi1 = float(gamma_pdf(y, 0.5, 0.5))
        assert _approx(f, chi1, tol=2e-2)
        # explicit closed form 1/sqrt(2 pi y) e^{-y/2}
        assert _approx(chi1, math.exp(-y / 2.0) / math.sqrt(2.0 * math.pi * y), tol=1e-9)


# --- change of variables for a monotone g -----------------------------------

def test_change_of_variables_recovers_exponential():
    # X~U(0,1), Y=-ln(X)/rate => Y~Exp(rate);  f_Y(y)=f_X(e^{-rate y})*rate e^{-rate y}
    rate = 1.5
    for y in (0.1, 0.7, 2.0, 4.0):
        fY = change_of_variables_1d(uniform_pdf,
                                    lambda yy: math.exp(-rate * yy),
                                    lambda yy: -rate * math.exp(-rate * yy), y)
        assert _approx(fY, float(exp_pdf(y, rate)), tol=1e-9)


def test_change_of_variables_equals_differentiated_cdf():
    # the formula IS d/dy F_Y; check against numeric derivative of the true cdf
    rate = 1.5
    FY = lambda y: float(exp_cdf(y, rate))
    for y in (0.3, 1.0, 2.5):
        fY = change_of_variables_1d(uniform_pdf,
                                    lambda yy: math.exp(-rate * yy),
                                    lambda yy: -rate * math.exp(-rate * yy), y)
        assert _approx(fY, _diff(FY, y), tol=1e-4)


# --- sums of independent variables = convolution -----------------------------

def test_sum_two_uniforms_is_triangular():
    for z in (0.3, 0.7, 1.0, 1.4, 1.8):
        c = convolution(uniform_pdf, uniform_pdf, z, 0.0, 1.0)
        assert _approx(c, float(sum_two_uniforms_pdf(z)), tol=2e-3)
    # peak value f(1)=1 and the convolution integrates to 1
    assert _approx(convolution(uniform_pdf, uniform_pdf, 1.0, 0.0, 1.0), 1.0, tol=2e-3)
    total = _integrate(lambda z: triangular_pdf(z), 0.0, 2.0)
    assert _approx(total, 1.0, tol=1e-4)


def test_sum_of_exponentials_is_gamma():
    rate = 1.0
    g2 = lambda zz: gamma_pdf(zz, 2.0, rate)
    for z in (0.5, 1.5, 3.0, 5.0):
        two = convolution(lambda t: exp_pdf(t, rate), lambda t: exp_pdf(t, rate),
                          z, 0.0, z)
        assert _approx(two, float(sum_n_exponentials_pdf(z, 2, rate)), tol=3e-3)
        three = convolution(g2, lambda t: exp_pdf(t, rate), z, 0.0, z)
        assert _approx(three, float(sum_n_exponentials_pdf(z, 3, rate)), tol=3e-3)


def test_convolution_preserves_normalization():
    # the convolution of two densities is itself a density (integrates to 1)
    rate = 1.0
    f_sum = lambda z: convolution(lambda t: exp_pdf(t, rate),
                                  lambda t: exp_pdf(t, rate), z, 0.0, z)
    assert _approx(_integrate(np.vectorize(f_sum), 0.0, 40.0, n=2000), 1.0, tol=2e-3)


# --- 2-D Jacobian transformation ---------------------------------------------

def test_jacobian_det_matches_analytic():
    # map x=uv, y=u(1-v) has J = -u
    inv = lambda u, v: (u * v, u * (1.0 - v))
    for (u, v) in ((1.5, 0.3), (2.0, 0.7), (0.8, 0.5)):
        assert _approx(jacobian_det_2d(inv, u, v), -u, tol=1e-6)


def test_jacobian_transform_exp_to_gamma_times_uniform():
    # X,Y ~ Exp(1) iid;  U=X+Y ~ Gamma(2,1), V=X/(X+Y) ~ U(0,1), independent
    # f_UV(u,v) = f_XY(uv,u(1-v))*|J| = u e^{-u} = Gamma2(u) * 1
    fXY = lambda x, y: float(exp_pdf(x, 1.0)) * float(exp_pdf(y, 1.0))
    inv = lambda u, v: (u * v, u * (1.0 - v))
    for (u, v) in ((1.5, 0.3), (2.0, 0.7), (3.0, 0.5)):
        f = jacobian_transform_2d(fXY, inv, u, v)
        assert _approx(f, u * math.exp(-u), tol=1e-4)
        # factorizes as marginal_U(u) * marginal_V(v)
        assert _approx(f, float(gamma_pdf(u, 2.0, 1.0)) * float(uniform_pdf(v)), tol=1e-4)


def test_jacobian_marginal_of_U_is_gamma2():
    # integrate the joint over v in (0,1) -> Gamma(2,1) marginal of U
    fXY = lambda x, y: float(exp_pdf(x, 1.0)) * float(exp_pdf(y, 1.0))
    inv = lambda u, v: (u * v, u * (1.0 - v))
    for u in (1.0, 2.5):
        marg = _integrate(np.vectorize(
            lambda v: jacobian_transform_2d(fXY, inv, u, v)), 1e-4, 1.0 - 1e-4, n=400)
        assert _approx(marg, float(gamma_pdf(u, 2.0, 1.0)), tol=1e-3)


# --- probability integral transform ------------------------------------------

def test_probability_integral_transform_is_uniform():
    # U = F_X(X) has density 1 on (0,1), for several base laws X
    for u in (0.1, 0.35, 0.6, 0.9):
        d_exp = probability_integral_transform_pdf(
            lambda x: exp_pdf(x, 2.0), lambda uu: float(exp_quantile(uu, 2.0)), u)
        assert _approx(d_exp, 1.0, tol=1e-4)
        d_lin = probability_integral_transform_pdf(
            linear_pdf, lambda uu: float(linear_quantile(uu)), u)
        assert _approx(d_lin, 1.0, tol=1e-4)


def test_inverse_transform_sampling_consistency():
    # X = F^{-1}(U) with U~U(0,1) reproduces the target cdf: F_X(F^{-1}(u))=u
    for u in (0.2, 0.5, 0.8):
        x = exp_quantile(u, 2.0)
        assert _approx(float(exp_cdf(x, 2.0)), u, tol=1e-9)


def test_normal_cdf_derivative_is_pdf():
    # sanity bridge: d/dx Phi(x) = phi(x)
    for x in (-1.0, 0.0, 0.5, 1.7):
        assert _approx(_diff(normal_cdf, x), float(normal_pdf(x)), tol=1e-6)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
