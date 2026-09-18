"""ST-14  Correlation & conditional distributions -- covariance, rho, regression.

Probability-theory trunk, module ST-14 (a replica of Penn State STAT 414,
lessons L18 The Correlation Coefficient and L19 Conditional Distributions).
Builds on ~ST-13 (joint pmf/pdf, marginals, independence) and ~MA-04 (the
covariance matrix and the Cauchy-Schwarz inequality).

Two random variables on a common probability space are tied together by their
*covariance* Cov(X,Y) = E[XY] - E[X]E[Y].  Rescaling it by the two standard
deviations gives the dimensionless *correlation coefficient*
rho = Cov(X,Y) / (sigma_X sigma_Y), which the Cauchy-Schwarz inequality pins to
|rho| <= 1.  Independence forces rho = 0, but the converse is FALSE: rho only
measures the strength of the *linear* association.  Conditioning replaces the
marginal by the slice f(y|x) = f(x,y)/f_X(x); its mean E[Y|X=x] is the
*regression function*, and averaging it back over X recovers E[Y] -- the law of
total expectation E[E[Y|X]] = E[Y].  The best straight-line predictor has slope
rho sigma_Y/sigma_X, and because |rho| <= 1 it pulls predictions toward the mean
(*regression to the mean*).

A discrete joint distribution is carried by the small `Joint` object (support
arrays xs, ys and a matrix P[i,j] = P(X=xs[i], Y=ys[j])); continuous laws are
handled by the f(x,y) callables and the midpoint integrators `_integrate` /
`_integrate2`.  Pure numpy + stdlib math; self-contained.
"""

import math

import numpy as np

__all__ = [
    "Joint", "marginal_x", "marginal_y", "mean_x", "mean_y", "mean_xy",
    "var_x", "var_y", "std_x", "std_y", "covariance", "correlation",
    "covariance_matrix", "conditional_pmf", "conditional_expectation",
    "regression_function", "law_of_total_expectation", "regression_line",
    "best_linear_predictor", "product_joint", "is_independent",
    "uncorrelated_dependent_example", "linear_dependence_example",
    "regression_to_mean_example", "demo_joint",
    "cont_marginal_x", "cont_mean_x", "cont_mean_y", "cont_var_x", "cont_var_y",
    "cont_covariance", "cont_correlation", "cont_conditional_expectation",
    "cont_total_expectation",
]


# --- discrete joint distribution (STAT 414 L17/L18) --------------------------

class Joint:
    """Discrete joint law of (X,Y): support xs, ys and matrix P[i,j]=P(X=xs[i],Y=ys[j])."""

    def __init__(self, xs, ys, P):
        self.xs = np.asarray(xs, dtype=float)
        self.ys = np.asarray(ys, dtype=float)
        self.P = np.asarray(P, dtype=float)
        if self.P.shape != (self.xs.size, self.ys.size):
            raise ValueError("P must have shape (len(xs), len(ys))")
        if np.any(self.P < -1e-12):
            raise ValueError("P has negative entries")
        if abs(self.P.sum() - 1.0) > 1e-9:
            raise ValueError("P must sum to 1")


def _index_of(arr, val):
    """Index of support value `val` in `arr` (exact match within 1e-9)."""
    i = int(np.argmin(np.abs(arr - val)))
    if abs(arr[i] - val) > 1e-9:
        raise ValueError("value %r is not in the support" % (val,))
    return i


def marginal_x(j):
    """Marginal pmf f_X(x_i) = sum_j P(x_i, y_j)  (row sums of P)."""
    return j.P.sum(axis=1)


def marginal_y(j):
    """Marginal pmf f_Y(y_j) = sum_i P(x_i, y_j)  (column sums of P)."""
    return j.P.sum(axis=0)


def mean_x(j):
    """E[X] = sum_i x_i f_X(x_i)."""
    return float(np.dot(j.xs, marginal_x(j)))


def mean_y(j):
    """E[Y] = sum_j y_j f_Y(y_j)."""
    return float(np.dot(j.ys, marginal_y(j)))


def mean_xy(j):
    """E[XY] = sum_{i,j} x_i y_j P(x_i, y_j)  (the cross moment)."""
    return float(j.xs @ j.P @ j.ys)


def var_x(j):
    """Var(X) = E[X^2] - E[X]^2."""
    return float(np.dot(j.xs ** 2, marginal_x(j))) - mean_x(j) ** 2


def var_y(j):
    """Var(Y) = E[Y^2] - E[Y]^2."""
    return float(np.dot(j.ys ** 2, marginal_y(j))) - mean_y(j) ** 2


def std_x(j):
    """sigma_X = sqrt(Var X)."""
    return math.sqrt(var_x(j))


def std_y(j):
    """sigma_Y = sqrt(Var Y)."""
    return math.sqrt(var_y(j))


# --- covariance and correlation (STAT 414 L18) -------------------------------

def covariance(j):
    """Cov(X,Y) = E[XY] - E[X]E[Y]  (= E[(X-mu_X)(Y-mu_Y)])."""
    return mean_xy(j) - mean_x(j) * mean_y(j)


def correlation(j):
    """Pearson correlation rho = Cov(X,Y)/(sigma_X sigma_Y); |rho|<=1 (Cauchy-Schwarz)."""
    cov = covariance(j)
    rho = cov / (std_x(j) * std_y(j))
    if abs(rho) > 1.0 + 1e-9:
        raise AssertionError("Cauchy-Schwarz violated: |rho| = %r > 1" % (rho,))
    return rho


def covariance_matrix(j):
    """Covariance matrix Sigma = [[Var X, Cov],[Cov, Var Y]]; the ~MA-04 object, PSD."""
    cov = covariance(j)
    return np.array([[var_x(j), cov], [cov, var_y(j)]])


# --- conditional distributions (STAT 414 L19) --------------------------------

def conditional_pmf(j, x):
    """Conditional pmf f(y|x) = f(x,y)/f_X(x); returns (ys, probs) for the slice X=x."""
    i = _index_of(j.xs, x)
    fx = marginal_x(j)[i]
    if fx <= 0.0:
        raise ValueError("cannot condition on x with f_X(x)=0")
    return j.ys.copy(), j.P[i, :] / fx


def conditional_expectation(j, x):
    """E[Y|X=x] = sum_j y_j f(y_j|x); the regression function evaluated at x."""
    ys, p = conditional_pmf(j, x)
    return float(np.dot(ys, p))


def regression_function(j):
    """The regression function x -> E[Y|X=x]; returns (xs, E[Y|X=xs]) over the X-support."""
    g = np.array([conditional_expectation(j, x) for x in j.xs])
    return j.xs.copy(), g


def law_of_total_expectation(j):
    """E[E[Y|X]] = sum_i E[Y|X=x_i] f_X(x_i); equals E[Y] (the tower property)."""
    _, g = regression_function(j)
    return float(np.dot(g, marginal_x(j)))


# --- linear (least-squares) prediction and regression to the mean ------------

def regression_line(j):
    """Least-squares line of Y on X: slope b = Cov/Var(X) = rho sigma_Y/sigma_X,
    intercept a = mu_Y - b mu_X.  Returns (a, b)."""
    b = covariance(j) / var_x(j)
    a = mean_y(j) - b * mean_x(j)
    return a, b


def best_linear_predictor(j, x):
    """Best linear predictor of Y at X=x: mu_Y + rho (sigma_Y/sigma_X)(x - mu_X)."""
    a, b = regression_line(j)
    return a + b * x


# --- independence and the rho=0 / dependence dictionary ----------------------

def product_joint(xs, px, ys, py):
    """Independent joint P(x_i,y_j)=f_X(x_i) f_Y(y_j) (outer product): X and Y independent."""
    P = np.outer(np.asarray(px, float), np.asarray(py, float))
    return Joint(xs, ys, P)


def is_independent(j, tol=1e-9):
    """True iff P(x,y)=f_X(x)f_Y(y) for every cell (the factorization test)."""
    outer = np.outer(marginal_x(j), marginal_y(j))
    return bool(np.all(np.abs(j.P - outer) <= tol))


# --- canonical example joints ------------------------------------------------

def demo_joint():
    """STAT 414 example f(x,y)=(x+y)/32 on x in {1,2}, y in {1,2,3,4}."""
    xs = np.array([1.0, 2.0])
    ys = np.array([1.0, 2.0, 3.0, 4.0])
    P = np.array([[(x + y) / 32.0 for y in ys] for x in xs])
    return Joint(xs, ys, P)


def uncorrelated_dependent_example():
    """X uniform on {-1,0,1}, Y=X^2: Cov=0 (rho=0) yet Y is a function of X (dependent).
    The standing counterexample to 'rho=0 implies independence'."""
    xs = np.array([-1.0, 0.0, 1.0])
    ys = np.array([0.0, 1.0])
    P = np.array([[0.0, 1.0 / 3.0],    # X=-1 -> Y=1
                  [1.0 / 3.0, 0.0],    # X= 0 -> Y=0
                  [0.0, 1.0 / 3.0]])   # X= 1 -> Y=1
    return Joint(xs, ys, P)


def linear_dependence_example(a=2.0, b=1.0):
    """Y = a X + b deterministically: rho = sign(a), |rho|=1 (Cauchy-Schwarz equality)."""
    xs = np.array([0.0, 1.0, 2.0, 3.0])
    px = np.full(4, 0.25)
    yvals = a * xs + b
    ys = np.unique(yvals)
    P = np.zeros((xs.size, ys.size))
    for i, xv in enumerate(xs):
        jcol = int(np.argmin(np.abs(ys - (a * xv + b))))
        P[i, jcol] = px[i]
    return Joint(xs, ys, P)


def regression_to_mean_example():
    """Symmetric law on {-1,1}^2 with rho=0.6: equal means/sds, |rho|<1 -> predictions
    are pulled toward the mean (regression to the mean)."""
    xs = np.array([-1.0, 1.0])
    ys = np.array([-1.0, 1.0])
    P = np.array([[0.4, 0.1],
                  [0.1, 0.4]])
    return Joint(xs, ys, P)


# --- continuous laws: midpoint integrators (cf. SM-06 _integrate) ------------

def _integrate(f, a, b, n=4000):
    """Midpoint rule for a 1-D integral int_a^b f(t) dt (f numpy-vectorized)."""
    t = a + (np.arange(n) + 0.5) * (b - a) / n
    return float(np.sum(f(t)) * (b - a) / n)


def _integrate2(f, ax, bx, ay, by, nx=400, ny=400):
    """Midpoint rule for int int f(x,y) dy dx over [ax,bx]x[ay,by] (f vectorized)."""
    x = ax + (np.arange(nx) + 0.5) * (bx - ax) / nx
    y = ay + (np.arange(ny) + 0.5) * (by - ay) / ny
    X, Y = np.meshgrid(x, y, indexing="ij")
    return float(np.sum(f(X, Y)) * (bx - ax) / nx * (by - ay) / ny)


def cont_marginal_x(f, x, bounds, n=4000):
    """Continuous marginal f_X(x) = int f(x,y) dy."""
    _, _, ay, by = bounds
    return _integrate(lambda y: f(x, y), ay, by, n)


def cont_mean_x(f, bounds, **kw):
    """E[X] = int int x f(x,y) dy dx."""
    return _integrate2(lambda x, y: x * f(x, y), *bounds, **kw)


def cont_mean_y(f, bounds, **kw):
    """E[Y] = int int y f(x,y) dy dx."""
    return _integrate2(lambda x, y: y * f(x, y), *bounds, **kw)


def cont_var_x(f, bounds, **kw):
    """Var(X) = E[X^2] - E[X]^2 (continuous)."""
    ex2 = _integrate2(lambda x, y: x * x * f(x, y), *bounds, **kw)
    return ex2 - cont_mean_x(f, bounds, **kw) ** 2


def cont_var_y(f, bounds, **kw):
    """Var(Y) = E[Y^2] - E[Y]^2 (continuous)."""
    ey2 = _integrate2(lambda x, y: y * y * f(x, y), *bounds, **kw)
    return ey2 - cont_mean_y(f, bounds, **kw) ** 2


def cont_covariance(f, bounds, **kw):
    """Cov(X,Y) = E[XY] - E[X]E[Y] (continuous)."""
    exy = _integrate2(lambda x, y: x * y * f(x, y), *bounds, **kw)
    return exy - cont_mean_x(f, bounds, **kw) * cont_mean_y(f, bounds, **kw)


def cont_correlation(f, bounds, **kw):
    """rho = Cov/(sigma_X sigma_Y) (continuous); |rho|<=1."""
    cov = cont_covariance(f, bounds, **kw)
    return cov / math.sqrt(cont_var_x(f, bounds, **kw) * cont_var_y(f, bounds, **kw))


def cont_conditional_expectation(f, x, bounds, n=4000):
    """E[Y|X=x] = int y f(x,y) dy / f_X(x); the continuous regression function."""
    _, _, ay, by = bounds
    num = _integrate(lambda y: y * f(x, y), ay, by, n)
    return num / cont_marginal_x(f, x, bounds, n)


def cont_total_expectation(f, bounds, n=400):
    """E[E[Y|X]] = int E[Y|X=x] f_X(x) dx; equals E[Y] (continuous tower)."""
    ax, bx, _, _ = bounds
    g = lambda x: cont_conditional_expectation(f, float(x), bounds, n) \
        * cont_marginal_x(f, float(x), bounds, n)
    # 1-D outer integral done with an explicit (non-vectorized) midpoint sum
    h = (bx - ax) / n
    return sum(g(ax + (k + 0.5) * h) for k in range(n)) * h


# --- demo --------------------------------------------------------------------

def _demo():
    print("ST-14  correlation & conditional distributions -- demo")
    print("=" * 58)

    j = demo_joint()
    print("Joint f(x,y)=(x+y)/32, x in {1,2}, y in {1,2,3,4}:")
    print("  E[X]=%.6g  E[Y]=%.6g  E[XY]=%.6g" % (mean_x(j), mean_y(j), mean_xy(j)))
    print("  Cov(X,Y)=%.6g  (= -5/256=%.6g)" % (covariance(j), -5 / 256))
    print("  Var X=%.6g  Var Y=%.6g" % (var_x(j), var_y(j)))
    print("  rho=%.6f   |rho|<=1: %s" % (correlation(j), abs(correlation(j)) <= 1))
    a, b = regression_line(j)
    print("  regression line  E[Y]~ %.5f %+.5f x   (slope=Cov/VarX=-5/63=%.6g)"
          % (a, b, -5 / 63))
    print("  E[Y|X=1]=%.6f (=20/7)  E[Y|X=2]=%.6f (=25/9)"
          % (conditional_expectation(j, 1), conditional_expectation(j, 2)))
    print("  law of total expectation: E[E[Y|X]]=%.6f  =  E[Y]=%.6f"
          % (law_of_total_expectation(j), mean_y(j)))
    Sig = covariance_matrix(j)
    print("  cov matrix det = VarX*VarY - Cov^2 = %.6g >= 0  (<=>|rho|<=1)"
          % np.linalg.det(Sig))

    print("\nIndependence => rho=0  (but NOT conversely):")
    ind = product_joint([0, 1], [0.3, 0.7], [2, 5], [0.5, 0.5])
    print("  product law: Cov=%.2e  rho=%.2e  independent=%s"
          % (covariance(ind), correlation(ind), is_independent(ind)))
    u = uncorrelated_dependent_example()
    print("  X~U{-1,0,1}, Y=X^2: rho=%.2e  independent=%s  but E[Y|X=-1]=%.0f, "
          "E[Y|X=0]=%.0f, E[Y|X=1]=%.0f"
          % (correlation(u), is_independent(u),
             conditional_expectation(u, -1), conditional_expectation(u, 0),
             conditional_expectation(u, 1)))

    print("\nPerfect linear dependence Y=2X+1: rho=%.3f (Cauchy-Schwarz equality)"
          % correlation(linear_dependence_example(2.0, 1.0)))
    print("Y=-3X+5: rho=%.3f" % correlation(linear_dependence_example(-3.0, 5.0)))

    print("\nRegression to the mean (symmetric law, rho=0.6):")
    r = regression_to_mean_example()
    print("  mu_X=mu_Y=%.1f  sigma_X=sigma_Y=%.1f  rho=%.2f"
          % (mean_x(r), std_x(r), correlation(r)))
    print("  X=+1 (z=+1) predicts E[Y|lin]=%.2f  -> pulled toward the mean (|0.6|<|1|)"
          % best_linear_predictor(r, 1.0))

    print("\nContinuous law f(x,y)=x+y on the unit square:")
    f = lambda x, y: x + y
    bd = (0.0, 1.0, 0.0, 1.0)
    print("  normalization int int f = %.6f" % _integrate2(f, *bd))
    print("  E[X]=%.6f (=7/12=%.6f)  Cov=%.6f (=-1/144=%.6f)"
          % (cont_mean_x(f, bd), 7 / 12, cont_covariance(f, bd), -1 / 144))
    print("  rho=%.6f (=-1/11=%.6f)" % (cont_correlation(f, bd), -1 / 11))
    print("  regression fn E[Y|X=0]=%.6f (=2/3)  E[Y|X=1]=%.6f (=5/9)"
          % (cont_conditional_expectation(f, 0.0, bd),
             cont_conditional_expectation(f, 1.0, bd)))
    print("  tower: E[E[Y|X]]=%.6f  =  E[Y]=%.6f"
          % (cont_total_expectation(f, bd), cont_mean_y(f, bd)))


if __name__ == "__main__":
    _demo()
