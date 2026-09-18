"""Tests for ST-15 the bivariate normal distribution.

Asserts the headline analytic identities: explicit-form == covariance-matrix
form, the joint pdf normalizes, both marginals are normal, the conditional
Y|X=x is normal with the regression mean and the (1-rho^2) variance, the
joint factorizes, rho=0 <=> independence, mgf derivatives give the moments,
det Sigma and positive-definiteness, and the contour-ellipse level set.

Run:  python3 test_bivariate_normal.py     ->  "All N tests passed."
"""
import math
import numpy as np

from bivariate_normal import (
    normal_pdf, bivariate_normal_pdf, covariance_matrix, bivariate_normal_pdf_cov,
    mahalanobis_sq, marginal_pdf_x, marginal_pdf_y, conditional_params,
    conditional_pdf_y_given_x, correlation, is_positive_definite, mgf,
    ellipse_axes, ellipse_points,
)

# a generic, off-diagonal test case
MUX, MUY, SX, SY, RHO = 1.0, 2.0, 1.0, 2.0, 0.6


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _integrate(f, a, b, n=4000):
    """Midpoint rule for a 1-D continuous check."""
    dx = (b - a) / n
    return sum(f(a + (i + 0.5) * dx) * dx for i in range(n))


def _integrate2d(f, ax, bx, ay, by, nx=400, ny=400):
    """Midpoint rule on a rectangle for a 2-D continuous check."""
    dx = (bx - ax) / nx
    dy = (by - ay) / ny
    total = 0.0
    for i in range(nx):
        xi = ax + (i + 0.5) * dx
        col = 0.0
        for j in range(ny):
            yj = ay + (j + 0.5) * dy
            col += f(xi, yj)
        total += col
    return total * dx * dy


def _d1(g, h=1e-4):
    """Central first derivative of t -> g(t) at 0."""
    return (g(h) - g(-h)) / (2.0 * h)


def _d2(g, h=1e-3):
    """Central second derivative of t -> g(t) at 0."""
    return (g(h) - 2.0 * g(0.0) + g(-h)) / (h * h)


# integration window: mean +- 8 sigma in each coordinate
AX, BX = MUX - 8 * SX, MUX + 8 * SX
AY, BY = MUY - 8 * SY, MUY + 8 * SY


def test_explicit_equals_covariance_form():
    Sigma = covariance_matrix(SX, SY, RHO)
    mu = (MUX, MUY)
    for x, y in [(1.5, 3.0), (0.0, 0.0), (-1.0, 5.0), (MUX, MUY)]:
        a = bivariate_normal_pdf(x, y, MUX, MUY, SX, SY, RHO)
        b = bivariate_normal_pdf_cov(x, y, mu, Sigma)
        assert _approx(a, b, tol=1e-9)


def test_quadratic_form_equals_mahalanobis():
    # (w)^T Sigma^{-1} (w) computed two ways agree
    Sigma = covariance_matrix(SX, SY, RHO)
    inv = np.linalg.inv(Sigma)
    for x, y in [(1.5, 3.0), (-2.0, 1.0), (4.0, 0.0)]:
        w = np.array([x - MUX, y - MUY])
        q_mat = float(w @ inv @ w)
        q_exp = mahalanobis_sq(x, y, MUX, MUY, SX, SY, RHO)
        assert _approx(q_mat, q_exp, tol=1e-9)


def test_joint_pdf_normalizes():
    total = _integrate2d(lambda x, y: bivariate_normal_pdf(x, y, MUX, MUY, SX, SY, RHO),
                         AX, BX, AY, BY)
    assert _approx(total, 1.0, tol=1e-3)


def test_marginal_x_is_normal():
    # integrate the joint over y at fixed x -> N(mu_X, sx^2)
    for x in (MUX, MUX + 0.7 * SX, MUX - 1.3 * SX):
        fx = _integrate(lambda y: bivariate_normal_pdf(x, y, MUX, MUY, SX, SY, RHO),
                        AY, BY, n=4000)
        assert _approx(fx, marginal_pdf_x(x, MUX, SX), tol=1e-3)


def test_marginal_y_is_normal():
    # integrate the joint over x at fixed y -> N(mu_Y, sy^2)
    for y in (MUY, MUY + 0.9 * SY):
        fy = _integrate(lambda x: bivariate_normal_pdf(x, y, MUX, MUY, SX, SY, RHO),
                        AX, BX, n=4000)
        assert _approx(fy, marginal_pdf_y(y, MUY, SY), tol=1e-3)


def test_conditional_params_formulas():
    # mean = mu_Y + rho (sy/sx)(x-mu_X); var = sy^2 (1-rho^2), independent of x
    for x in (0.0, 1.0, 3.5):
        mean, var = conditional_params(x, MUX, MUY, SX, SY, RHO)
        assert _approx(mean, MUY + RHO * (SY / SX) * (x - MUX))
        assert _approx(var, SY * SY * (1.0 - RHO * RHO))
    # var does not depend on x (homoscedastic)
    _, v0 = conditional_params(0.0, MUX, MUY, SX, SY, RHO)
    _, v1 = conditional_params(10.0, MUX, MUY, SX, SY, RHO)
    assert _approx(v0, v1)


def test_conditional_pdf_normalizes_and_factorizes():
    x = MUX + 0.5 * SX
    # f(y|x) is itself a normalized density in y
    norm = _integrate(lambda y: conditional_pdf_y_given_x(y, x, MUX, MUY, SX, SY, RHO),
                      AY, BY, n=4000)
    assert _approx(norm, 1.0, tol=1e-4)
    # f(x,y) = f_X(x) * f(y|x) pointwise (always true, not only at rho=0)
    for y in (1.0, 2.5, 4.0):
        joint = bivariate_normal_pdf(x, y, MUX, MUY, SX, SY, RHO)
        prod = marginal_pdf_x(x, MUX, SX) * conditional_pdf_y_given_x(y, x, MUX, MUY, SX, SY, RHO)
        assert _approx(joint, prod, tol=1e-9)


def test_conditional_mean_and_var_by_integration():
    # E[Y|X=x] and Var(Y|X=x) by integrating the conditional density
    x = MUX + 1.0 * SX
    mean, var = conditional_params(x, MUX, MUY, SX, SY, RHO)
    f = lambda y: conditional_pdf_y_given_x(y, x, MUX, MUY, SX, SY, RHO)
    m_int = _integrate(lambda y: y * f(y), AY, BY, n=8000)
    v_int = _integrate(lambda y: (y - mean) ** 2 * f(y), AY, BY, n=8000)
    assert _approx(m_int, mean, tol=1e-3)
    assert _approx(v_int, var, tol=1e-3)


def test_rho_zero_is_independence():
    # rho = 0  =>  f(x,y) = f_X(x) f_Y(y) exactly
    for x, y in [(0.5, 3.0), (-1.0, 1.0), (2.0, 2.0)]:
        joint = bivariate_normal_pdf(x, y, MUX, MUY, SX, SY, 0.0)
        prod = marginal_pdf_x(x, MUX, SX) * marginal_pdf_y(y, MUY, SY)
        assert _approx(joint, prod, tol=1e-12)
    # and for rho != 0 it is NOT a product (dependence)
    x, y = 2.5, 4.5
    joint = bivariate_normal_pdf(x, y, MUX, MUY, SX, SY, RHO)
    prod = marginal_pdf_x(x, MUX, SX) * marginal_pdf_y(y, MUY, SY)
    assert not _approx(joint, prod, tol=1e-6)


def test_covariance_matrix_det_and_correlation():
    Sigma = covariance_matrix(SX, SY, RHO)
    det = float(np.linalg.det(Sigma))
    assert _approx(det, SX * SX * SY * SY * (1.0 - RHO * RHO))
    assert _approx(correlation(Sigma), RHO)
    assert _approx(Sigma[0, 1], RHO * SX * SY)


def test_positive_definiteness():
    # |rho| < 1 -> positive-definite; |rho| = 1 -> degenerate (det 0)
    assert is_positive_definite(covariance_matrix(SX, SY, 0.0))
    assert is_positive_definite(covariance_matrix(SX, SY, 0.99))
    assert not is_positive_definite(covariance_matrix(SX, SY, 1.0))
    assert not is_positive_definite(covariance_matrix(SX, SY, -1.0))
    # eigenvalues of a pd Sigma are strictly positive
    lam = np.linalg.eigvalsh(covariance_matrix(SX, SY, RHO))
    assert lam[0] > 0.0 and lam[1] > 0.0


def test_covariance_by_integration():
    # Cov(X,Y) = E[(X-muX)(Y-muY)] = rho sx sy by direct 2-D integration
    cov = _integrate2d(
        lambda x, y: (x - MUX) * (y - MUY) * bivariate_normal_pdf(x, y, MUX, MUY, SX, SY, RHO),
        AX, BX, AY, BY)
    assert _approx(cov, RHO * SX * SY, tol=1e-2)
    # variances of X and Y likewise
    vx = _integrate2d(
        lambda x, y: (x - MUX) ** 2 * bivariate_normal_pdf(x, y, MUX, MUY, SX, SY, RHO),
        AX, BX, AY, BY)
    assert _approx(vx, SX * SX, tol=1e-2)


def test_mgf_derivatives_give_moments():
    # M(t1,t2) = exp(mu.t + 1/2 t.Sigma.t); its derivatives at 0 are the moments
    assert _approx(mgf(0.0, 0.0, MUX, MUY, SX, SY, RHO), 1.0)
    # dM/dt1 |0 = E[X] = mu_X ; dM/dt2 |0 = E[Y] = mu_Y
    EX = _d1(lambda t: mgf(t, 0.0, MUX, MUY, SX, SY, RHO))
    EY = _d1(lambda t: mgf(0.0, t, MUX, MUY, SX, SY, RHO))
    assert _approx(EX, MUX, tol=1e-5)
    assert _approx(EY, MUY, tol=1e-5)
    # d2M/dt1^2 |0 = E[X^2] = mu_X^2 + sx^2  ->  Var(X) = sx^2
    EX2 = _d2(lambda t: mgf(t, 0.0, MUX, MUY, SX, SY, RHO))
    assert _approx(EX2 - MUX * MUX, SX * SX, tol=1e-4)


def test_mgf_mixed_partial_is_covariance():
    # d2M/dt1 dt2 |0 = E[XY] = muX muY + rho sx sy  ->  Cov = rho sx sy
    h = 1e-3
    f = lambda a, b: mgf(a, b, MUX, MUY, SX, SY, RHO)
    mixed = (f(h, h) - f(h, -h) - f(-h, h) + f(-h, -h)) / (4.0 * h * h)
    cov = mixed - MUX * MUY
    assert _approx(cov, RHO * SX * SY, tol=1e-4)


def test_contour_ellipse_level_set():
    # every point returned by ellipse_points(c) has Mahalanobis^2 = c^2
    for c in (1.0, 2.0):
        xs, ys = ellipse_points(MUX, MUY, SX, SY, RHO, c=c, n=40)
        for xi, yi in zip(xs, ys):
            assert _approx(mahalanobis_sq(xi, yi, MUX, MUY, SX, SY, RHO), c * c, tol=1e-9)
    # semi-axes^2 are the eigenvalues of Sigma (times c^2); product = det Sigma
    Sigma = covariance_matrix(SX, SY, RHO)
    a, b, _ = ellipse_axes(Sigma, c=1.0)
    assert _approx(a * a * b * b, float(np.linalg.det(Sigma)), tol=1e-9)
    assert a >= b


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
