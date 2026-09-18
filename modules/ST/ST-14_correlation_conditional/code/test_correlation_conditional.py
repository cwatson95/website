"""Tests for ST-14 correlation & conditional distributions.

Run:  python3 test_correlation_conditional.py     ->  "All N tests passed."
"""
import math

import numpy as np

from correlation_conditional import (
    Joint, marginal_x, marginal_y, mean_x, mean_y, mean_xy, var_x, var_y,
    std_x, std_y, covariance, correlation, covariance_matrix, conditional_pmf,
    conditional_expectation, regression_function, law_of_total_expectation,
    regression_line, best_linear_predictor, product_joint, is_independent,
    demo_joint, uncorrelated_dependent_example, linear_dependence_example,
    regression_to_mean_example, cont_mean_x, cont_mean_y, cont_var_x,
    cont_covariance, cont_correlation, cont_conditional_expectation,
    cont_total_expectation, _integrate2,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


# --- discrete machinery (the demo joint f(x,y)=(x+y)/32) ---------------------

def test_marginals_are_valid_pmfs():
    j = demo_joint()
    assert _approx(j.P.sum(), 1.0)
    assert _approx(marginal_x(j).sum(), 1.0)
    assert _approx(marginal_y(j).sum(), 1.0)
    assert np.all(marginal_x(j) >= 0) and np.all(marginal_y(j) >= 0)
    # the closed-form marginals f_X = [7/16, 9/16], f_Y(y) = (3+2y)/32
    assert _approx(marginal_x(j)[0], 7 / 16) and _approx(marginal_x(j)[1], 9 / 16)
    assert _approx(marginal_y(j)[2], 9 / 32)


def test_covariance_two_formulas_agree():
    j = demo_joint()
    # Cov = E[XY] - E[X]E[Y]
    cov = covariance(j)
    assert _approx(cov, mean_xy(j) - mean_x(j) * mean_y(j))
    # Cov = E[(X-mu_X)(Y-mu_Y)] computed directly over the grid
    mx, my = mean_x(j), mean_y(j)
    direct = 0.0
    for i, x in enumerate(j.xs):
        for k, y in enumerate(j.ys):
            direct += (x - mx) * (y - my) * j.P[i, k]
    assert _approx(cov, direct)
    # exact value -5/256 for this joint
    assert _approx(cov, -5 / 256)


def test_covariance_of_X_with_itself_is_variance():
    # Y = X gives a joint on the diagonal; Cov(X,X)=Var(X), rho=+1
    xs = np.array([0.0, 1.0, 2.0, 3.0])
    p = np.array([0.1, 0.4, 0.3, 0.2])
    P = np.diag(p)
    j = Joint(xs, xs, P)
    assert _approx(covariance(j), var_x(j))
    assert _approx(correlation(j), 1.0)


def test_correlation_definition_and_cauchy_schwarz():
    j = demo_joint()
    rho = correlation(j)
    assert _approx(rho, covariance(j) / (std_x(j) * std_y(j)))
    assert abs(rho) <= 1.0 + 1e-12
    # Cauchy-Schwarz equality at perfect linear dependence: rho = sign(slope)
    assert _approx(correlation(linear_dependence_example(2.0, 1.0)), 1.0)
    assert _approx(correlation(linear_dependence_example(-3.0, 5.0)), -1.0)


def test_covariance_matrix_psd_iff_rho_bound():
    # det(Sigma) = VarX VarY - Cov^2 = VarX VarY (1 - rho^2) >= 0
    for j in (demo_joint(), uncorrelated_dependent_example(),
              regression_to_mean_example()):
        Sig = covariance_matrix(j)
        assert _approx(Sig[0, 1], Sig[1, 0])           # symmetric
        det = Sig[0, 0] * Sig[1, 1] - Sig[0, 1] ** 2
        rho = correlation(j)
        assert _approx(det, var_x(j) * var_y(j) * (1.0 - rho ** 2))
        assert det >= -1e-12                           # PSD <=> |rho|<=1


def test_independence_implies_zero_correlation():
    j = product_joint([0, 1, 2], [0.2, 0.5, 0.3], [10, 20], [0.4, 0.6])
    assert is_independent(j)
    assert _approx(covariance(j), 0.0)
    assert _approx(correlation(j), 0.0)


def test_uncorrelated_but_dependent_counterexample():
    # converse is FALSE: rho = 0 yet X, Y dependent
    u = uncorrelated_dependent_example()
    assert _approx(covariance(u), 0.0)
    assert _approx(correlation(u), 0.0)
    assert not is_independent(u)
    # the conditional mean is not constant -> Y genuinely depends on X
    assert _approx(conditional_expectation(u, -1), 1.0)
    assert _approx(conditional_expectation(u, 0), 0.0)
    assert _approx(conditional_expectation(u, 1), 1.0)
    # rho=0 makes the least-squares line flat even though E[Y|X] varies
    a, b = regression_line(u)
    assert _approx(b, 0.0)


def test_conditional_pmf_is_a_valid_distribution():
    j = demo_joint()
    ys, p = conditional_pmf(j, 1)
    assert _approx(p.sum(), 1.0)
    assert np.all(p >= 0)
    # closed form f(y|X=1) = (1+y)/14
    assert np.all([_approx(p[k], (1 + ys[k]) / 14) for k in range(ys.size)])


def test_conditional_expectation_values():
    j = demo_joint()
    assert _approx(conditional_expectation(j, 1), 20 / 7)
    assert _approx(conditional_expectation(j, 2), 25 / 9)
    xs, g = regression_function(j)
    assert _approx(g[0], 20 / 7) and _approx(g[1], 25 / 9)


def test_law_of_total_expectation():
    # E[E[Y|X]] = E[Y] on several laws (the tower property)
    for j in (demo_joint(), uncorrelated_dependent_example(),
              regression_to_mean_example(),
              product_joint([1, 2], [0.5, 0.5], [3, 4, 5], [0.2, 0.3, 0.5])):
        assert _approx(law_of_total_expectation(j), mean_y(j))


def test_regression_line_through_means_and_slope():
    j = demo_joint()
    a, b = regression_line(j)
    # passes through (mu_X, mu_Y)
    assert _approx(a + b * mean_x(j), mean_y(j))
    assert _approx(best_linear_predictor(j, mean_x(j)), mean_y(j))
    # slope = Cov/Var(X) = rho sigma_Y/sigma_X = -5/63
    assert _approx(b, covariance(j) / var_x(j))
    assert _approx(b, correlation(j) * std_y(j) / std_x(j))
    assert _approx(b, -5 / 63)
    # with two X-support points the line hits both conditional means exactly
    assert _approx(best_linear_predictor(j, 1), conditional_expectation(j, 1))
    assert _approx(best_linear_predictor(j, 2), conditional_expectation(j, 2))


def test_regression_to_the_mean():
    r = regression_to_mean_example()
    assert _approx(mean_x(r), mean_y(r))
    assert _approx(std_x(r), std_y(r))
    rho = correlation(r)
    assert _approx(rho, 0.6)
    # an extreme X (deviation +1) predicts a milder Y deviation (rho*1 = 0.6)
    pred_dev = best_linear_predictor(r, 1.0) - mean_y(r)
    x_dev = 1.0 - mean_x(r)
    assert _approx(pred_dev, rho * x_dev)
    assert abs(pred_dev) < abs(x_dev)        # pulled toward the mean


# --- continuous law f(x,y)=x+y on the unit square ----------------------------

def test_continuous_density_normalized():
    f = lambda x, y: x + y
    assert _approx(_integrate2(f, 0, 1, 0, 1), 1.0, tol=1e-6)


def test_continuous_moments_covariance_correlation():
    f = lambda x, y: x + y
    bd = (0.0, 1.0, 0.0, 1.0)
    assert _approx(cont_mean_x(f, bd), 7 / 12, tol=1e-5)
    assert _approx(cont_mean_y(f, bd), 7 / 12, tol=1e-5)
    assert _approx(cont_var_x(f, bd), 11 / 144, tol=1e-5)
    assert _approx(cont_covariance(f, bd), -1 / 144, tol=1e-5)
    assert _approx(cont_correlation(f, bd), -1 / 11, tol=1e-4)
    assert abs(cont_correlation(f, bd)) <= 1.0


def test_continuous_conditional_and_tower():
    f = lambda x, y: x + y
    bd = (0.0, 1.0, 0.0, 1.0)
    # regression function E[Y|X=x] = (x/2 + 1/3)/(x + 1/2) -- nonlinear in x
    for x in (0.0, 0.5, 1.0):
        closed = (x / 2 + 1 / 3) / (x + 1 / 2)
        assert _approx(cont_conditional_expectation(f, x, bd), closed, tol=1e-5)
    # law of total expectation E[E[Y|X]] = E[Y] = 7/12
    assert _approx(cont_total_expectation(f, bd), cont_mean_y(f, bd), tol=1e-4)
    assert _approx(cont_total_expectation(f, bd), 7 / 12, tol=1e-4)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
