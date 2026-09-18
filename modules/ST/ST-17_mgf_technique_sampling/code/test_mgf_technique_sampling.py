"""Tests for ST-17 the MGF technique & normal sampling distributions.

Run:  python3 test_mgf_technique_sampling.py     ->  "All N tests passed."

Each test asserts a headline analytic identity: the product rule for mgfs of
independent sums (normals/gammas/chi-squares add their parameters), Z^2 ~ chi^2_1,
the sampling distribution of the mean Xbar ~ N(mu, sigma^2/n), the standardized
mean is exactly N(0,1), the Student-t density (normalization, mean, variance,
and the t_r -> N(0,1) limit), and the Snedecor-F density (normalization, mean,
and T^2 ~ F_{1,r}).
"""
import math

from mgf_technique_sampling import (
    normal_mgf, gamma_mgf, chi2_mgf,
    standard_normal_pdf, normal_pdf, gamma_pdf, chi2_pdf, beta_function,
    product_of_normal_mgfs, sum_of_normals_via_mgf,
    mgf_of_linear_combination_normals, linear_combination_of_normals,
    product_of_gamma_mgfs, sum_of_gammas_via_mgf,
    product_of_chi2_mgfs, sum_of_chisquares, square_of_standard_normal_pdf,
    sampling_dist_of_mean, standardized_mean_mgf, sample_variance_chi2_df,
    students_t_pdf, students_t_mean, students_t_var,
    f_pdf, f_mean, f_var, t_squared_pdf, _integrate,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


# === (A) the mgf technique ===================================================

def test_sum_of_normals_is_normal():
    # prod of normal mgfs == mgf of N(sum mu, sum var); params add
    means, variances = [1.0, -0.5, 2.0], [4.0, 2.25, 1.0]
    mu_s, var_s = sum_of_normals_via_mgf(means, variances)
    assert _approx(mu_s, 2.5) and _approx(var_s, 7.25)
    for t in (-0.4, 0.0, 0.3, 0.8):
        lhs = product_of_normal_mgfs(t, means, variances)
        rhs = normal_mgf(t, mu_s, math.sqrt(var_s))
        assert _approx(lhs, rhs)
    # the recognized sum density integrates to one
    total = _integrate(lambda x: normal_pdf(x, mu_s, math.sqrt(var_s)),
                       mu_s - 14 * math.sqrt(var_s), mu_s + 14 * math.sqrt(var_s), 60000)
    assert _approx(total, 1.0, tol=1e-6)


def test_linear_combination_of_normals():
    # a.X ~ N(sum a_i mu_i, sum a_i^2 sigma_i^2): prod M_i(a_i t) matches
    means, variances, coeffs = [1.0, -0.5, 2.0], [4.0, 2.25, 1.0], [2.0, -1.0, 0.5]
    mu_l, var_l = linear_combination_of_normals(coeffs, means, variances)
    assert _approx(mu_l, 2.0 * 1.0 - 1.0 * (-0.5) + 0.5 * 2.0)      # 3.5
    assert _approx(var_l, 4.0 * 4.0 + 1.0 * 2.25 + 0.25 * 1.0)      # 18.5
    for t in (-0.3, 0.0, 0.5):
        lhs = mgf_of_linear_combination_normals(t, coeffs, means, variances)
        rhs = normal_mgf(t, mu_l, math.sqrt(var_l))
        assert _approx(lhs, rhs)


def test_difference_of_two_normals():
    # X1 - X2 ~ N(mu1 - mu2, sigma1^2 + sigma2^2): variances ADD even for a difference
    mu_d, var_d = linear_combination_of_normals([1.0, -1.0], [5.0, 3.0], [4.0, 9.0])
    assert _approx(mu_d, 2.0)
    assert _approx(var_d, 13.0)   # 4 + 9, NOT 4 - 9


def test_gammas_add_shapes():
    # common scale => shapes add; prod of gamma mgfs == single gamma mgf
    alphas, theta = [1.5, 2.0, 3.5], 2.0
    a_sum, th = sum_of_gammas_via_mgf(alphas, theta)
    assert _approx(a_sum, 7.0) and _approx(th, 2.0)
    for t in (-0.5, 0.0, 0.2, 0.45):   # t < 1/theta = 0.5
        lhs = product_of_gamma_mgfs(t, alphas, theta)
        rhs = gamma_mgf(t, a_sum, theta)
        assert _approx(lhs, rhs)


def test_chisquares_add_df():
    # chi^2 d.f. add; prod of chi^2 mgfs == single chi^2 mgf
    dfs = [3, 5, 2]
    r_sum = sum_of_chisquares(dfs)
    assert _approx(r_sum, 10.0)
    for t in (-0.5, 0.0, 0.2, 0.45):   # t < 1/2
        lhs = product_of_chi2_mgfs(t, dfs)
        rhs = chi2_mgf(t, r_sum)
        assert _approx(lhs, rhs)
    # chi^2 mgf is the gamma mgf with theta = 2
    assert _approx(chi2_mgf(0.3, 8), gamma_mgf(0.3, 4.0, 2.0))


def test_square_of_standard_normal_is_chi2_1():
    # Z^2 ~ chi^2_1: phi(sqrt x)/sqrt x == chi2_pdf(x, 1)  (the seed of sampling theory)
    for x in (0.2, 1.0, 2.5, 4.0):
        assert _approx(square_of_standard_normal_pdf(x), chi2_pdf(x, 1), tol=1e-9)
    # chi^2_2 = sum of two Z^2 is exactly Exponential of mean 2:  (1/2) e^{-x/2}
    for x in (0.5, 2.0, 5.0):
        assert _approx(chi2_pdf(x, 2), 0.5 * math.exp(-x / 2.0), tol=1e-12)
    # chi^2_4 (a sum of four squared normals, no x^{-1/2} spike) integrates to one
    total = _integrate(lambda x: chi2_pdf(x, 4), 0.0, 80.0, 80000)
    assert _approx(total, 1.0, tol=1e-4)


# === (B) sampling distributions ==============================================

def test_sampling_dist_of_mean():
    # Xbar ~ N(mu, sigma^2/n); variance shrinks like 1/n
    mu, sigma2, n = 10.0, 8.0, 16
    m, v = sampling_dist_of_mean(mu, sigma2, n)
    assert _approx(m, 10.0) and _approx(v, 0.5)
    # doubling n halves the variance
    _, v2 = sampling_dist_of_mean(mu, sigma2, 32)
    assert _approx(v2, v / 2.0)


def test_standardized_mean_is_standard_normal():
    # mgf of (Xbar - mu)/(sigma/sqrt n) is exp(t^2/2) for every mu, sigma2, n
    for (mu, sigma2, n) in ((10.0, 8.0, 16), (-3.0, 5.0, 9), (0.0, 1.0, 100)):
        for t in (-0.6, 0.0, 0.7, 1.2):
            assert _approx(standardized_mean_mgf(t, mu, sigma2, n),
                           math.exp(0.5 * t * t))


def test_sample_variance_df():
    # (n-1) S^2 / sigma^2 ~ chi^2_{n-1}: one d.f. lost estimating the mean
    assert sample_variance_chi2_df(16) == 15
    assert sample_variance_chi2_df(2) == 1


def test_students_t_density_normalizes_and_moments():
    r = 6.0
    # normalizes to one
    total = _integrate(lambda t: students_t_pdf(t, r), -40.0, 40.0, 200000)
    assert _approx(total, 1.0, tol=1e-4)
    # mean 0 by symmetry, and the closed-form variance r/(r-2)
    mean = _integrate(lambda t: t * students_t_pdf(t, r), -40.0, 40.0, 200000)
    var = _integrate(lambda t: t * t * students_t_pdf(t, r), -40.0, 40.0, 200000)
    assert _approx(mean, 0.0, tol=1e-6)
    assert _approx(students_t_mean(r), 0.0)
    assert _approx(var, r / (r - 2.0), tol=1e-3)
    assert _approx(students_t_var(r), r / (r - 2.0))
    # the Beta form of the constant: f(0) = 1/(sqrt(r) B(1/2, r/2))
    assert _approx(students_t_pdf(0.0, r), 1.0 / (math.sqrt(r) * beta_function(0.5, r / 2.0)))


def test_students_t_var_tails_and_limit():
    # heavier than normal but -> 1; var infinite for r <= 2
    assert students_t_var(2) == float("inf")
    assert students_t_var(10) > 1.0
    assert students_t_var(1000) < students_t_var(10)   # approaches 1 from above
    # t_r -> N(0,1) pointwise as r -> inf
    err_small = abs(students_t_pdf(1.0, 5) - standard_normal_pdf(1.0))
    err_large = abs(students_t_pdf(1.0, 5000) - standard_normal_pdf(1.0))
    assert err_large < err_small
    assert err_large < 1e-3


def test_f_density_normalizes_and_mean():
    r1, r2 = 5.0, 10.0
    total = _integrate(lambda x: f_pdf(x, r1, r2), 1e-9, 400.0, 400000)
    assert _approx(total, 1.0, tol=2e-3)
    mean = _integrate(lambda x: x * f_pdf(x, r1, r2), 1e-9, 400.0, 400000)
    assert _approx(mean, f_mean(r2), tol=3e-3)
    assert _approx(f_mean(r2), r2 / (r2 - 2.0))      # 1.25
    # variance closed form is finite only for r2 > 4
    assert f_var(5, 4) == float("inf")
    assert f_var(5, 10) > 0.0


def test_t_squared_is_F_1_r():
    # T ~ t_r  =>  T^2 ~ F_{1,r}: the densities agree
    r = 7.0
    for w in (0.1, 0.5, 1.0, 2.0, 5.0):
        assert _approx(t_squared_pdf(w, r), f_pdf(w, 1.0, r), tol=1e-9)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
