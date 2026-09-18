"""ST-15  The bivariate normal distribution -- joint Gaussian in (mu_X,mu_Y,sx,sy,rho).

Probability theory module ST-15 (Penn State STAT 414, Lesson 21).
Builds on ~ST-14 (covariance, correlation, conditional means) and ~ST-12 (the
univariate normal), with the positive-definite covariance matrix Sigma of ~MA-04.

The bivariate normal density on (X, Y) is the two-dimensional Gaussian

    f(x,y) = 1 / (2 pi sx sy sqrt(1-rho^2))
             * exp( -z / (2 (1-rho^2)) ),
    z = (x-mu_X)^2/sx^2 - 2 rho (x-mu_X)(y-mu_Y)/(sx sy) + (y-mu_Y)^2/sy^2.

Packed into a mean vector mu = (mu_X, mu_Y) and covariance matrix
Sigma = [[sx^2, rho sx sy],[rho sx sy, sy^2]] it is the clean quadratic-form

    f(x) = 1 / (2 pi sqrt(det Sigma)) * exp(-1/2 (x-mu)^T Sigma^{-1} (x-mu)).

Everything that matters about it is here: both marginals are univariate normal,
the conditional Y | X = x is normal with mean mu_Y + rho (sy/sx)(x-mu_X) and
variance sy^2 (1-rho^2), and -- uniquely for the joint Gaussian -- rho = 0 is
equivalent to independence.  numpy + stdlib math only; no scipy.
"""

import math
import numpy as np

__all__ = [
    "normal_pdf",
    "bivariate_normal_pdf",
    "covariance_matrix",
    "bivariate_normal_pdf_cov",
    "mahalanobis_sq",
    "marginal_pdf_x", "marginal_pdf_y",
    "conditional_params",
    "conditional_pdf_y_given_x",
    "correlation",
    "is_positive_definite",
    "mgf",
    "ellipse_axes",
    "ellipse_points",
]


# --- univariate normal: the marginal building block (~ST-12) ------------------

def normal_pdf(x, mu=0.0, sigma=1.0):
    """Univariate normal pdf  N(mu, sigma^2):  exp(-(x-mu)^2/(2 sigma^2)) / (sigma sqrt(2 pi))."""
    z = (x - mu) / sigma
    return math.exp(-0.5 * z * z) / (sigma * math.sqrt(2.0 * math.pi))


# --- the bivariate normal pdf, explicit (mu_X,mu_Y,sx,sy,rho) form ------------

def bivariate_normal_pdf(x, y, mux=0.0, muy=0.0, sx=1.0, sy=1.0, rho=0.0):
    """Bivariate normal pdf, explicit form (STAT 414 L21):
        f = exp(-z/(2(1-rho^2))) / (2 pi sx sy sqrt(1-rho^2)),
        z = u^2 - 2 rho u v + v^2 with u=(x-mux)/sx, v=(y-muy)/sy."""
    u = (x - mux) / sx
    v = (y - muy) / sy
    one_m = 1.0 - rho * rho
    z = u * u - 2.0 * rho * u * v + v * v
    norm = 2.0 * math.pi * sx * sy * math.sqrt(one_m)
    return math.exp(-z / (2.0 * one_m)) / norm


# --- covariance-matrix form (~MA-04 linear algebra) ---------------------------

def covariance_matrix(sx, sy, rho):
    """Covariance matrix  Sigma = [[sx^2, rho sx sy],[rho sx sy, sy^2]]  (~MA-04)."""
    c = rho * sx * sy
    return np.array([[sx * sx, c], [c, sy * sy]], dtype=float)


def bivariate_normal_pdf_cov(x, y, mu, Sigma):
    """Bivariate normal pdf, covariance-matrix form:
        f = exp(-1/2 (w)^T Sigma^{-1} (w)) / (2 pi sqrt(det Sigma)),  w = (x,y) - mu.
    Uses numpy linear algebra; equals bivariate_normal_pdf for matching params."""
    w = np.array([x, y], dtype=float) - np.asarray(mu, dtype=float)
    Sigma = np.asarray(Sigma, dtype=float)
    det = np.linalg.det(Sigma)
    inv = np.linalg.inv(Sigma)
    q = float(w @ inv @ w)
    return math.exp(-0.5 * q) / (2.0 * math.pi * math.sqrt(det))


def mahalanobis_sq(x, y, mux=0.0, muy=0.0, sx=1.0, sy=1.0, rho=0.0):
    """Quadratic form (x-mu)^T Sigma^{-1} (x-mu) = z/(1-rho^2): the squared
    statistical distance whose level sets are the contour ellipses."""
    u = (x - mux) / sx
    v = (y - muy) / sy
    one_m = 1.0 - rho * rho
    z = u * u - 2.0 * rho * u * v + v * v
    return z / one_m


# --- both marginals are normal (STAT 414 L21) --------------------------------

def marginal_pdf_x(x, mux=0.0, sx=1.0):
    """Marginal of X: integrating out Y gives X ~ N(mu_X, sx^2)."""
    return normal_pdf(x, mux, sx)


def marginal_pdf_y(y, muy=0.0, sy=1.0):
    """Marginal of Y: integrating out X gives Y ~ N(mu_Y, sy^2)."""
    return normal_pdf(y, muy, sy)


# --- the conditional Y | X = x is normal (STAT 414 L21) -----------------------

def conditional_params(x, mux=0.0, muy=0.0, sx=1.0, sy=1.0, rho=0.0):
    """Parameters of Y | X = x ~ N(mean, var):
        mean = mu_Y + rho (sy/sx)(x - mu_X)   (the linear regression line),
        var  = sy^2 (1 - rho^2)               (independent of x: homoscedastic)."""
    mean = muy + rho * (sy / sx) * (x - mux)
    var = sy * sy * (1.0 - rho * rho)
    return mean, var


def conditional_pdf_y_given_x(y, x, mux=0.0, muy=0.0, sx=1.0, sy=1.0, rho=0.0):
    """Conditional density f(y | x): a normal with the conditional_params mean/var."""
    mean, var = conditional_params(x, mux, muy, sx, sy, rho)
    return normal_pdf(y, mean, math.sqrt(var))


# --- correlation and positive-definiteness (~MA-04) ---------------------------

def correlation(Sigma):
    """Pearson correlation read off a covariance matrix:  rho = Sigma_xy/(sx sy)."""
    Sigma = np.asarray(Sigma, dtype=float)
    return float(Sigma[0, 1] / math.sqrt(Sigma[0, 0] * Sigma[1, 1]))


def is_positive_definite(Sigma):
    """True iff Sigma is positive-definite (Sylvester: every leading minor > 0).
    For the bivariate Sigma this is sx,sy>0 and |rho|<1, i.e. det Sigma>0 (~MA-04)."""
    Sigma = np.asarray(Sigma, dtype=float)
    m1 = Sigma[0, 0]
    m2 = np.linalg.det(Sigma)
    return bool(m1 > 0.0 and m2 > 0.0)


# --- moment-generating function (ties Sigma to the moments, ~ST-06) -----------

def mgf(t1, t2, mux=0.0, muy=0.0, sx=1.0, sy=1.0, rho=0.0):
    """Joint mgf  M(t1,t2) = E[exp(t1 X + t2 Y)]
        = exp(mu^T t + 1/2 t^T Sigma t)
        = exp(mux t1 + muy t2 + 1/2(sx^2 t1^2 + 2 rho sx sy t1 t2 + sy^2 t2^2)).
    Its derivatives at 0 deliver the means, variances and covariance."""
    quad = sx * sx * t1 * t1 + 2.0 * rho * sx * sy * t1 * t2 + sy * sy * t2 * t2
    return math.exp(mux * t1 + muy * t2 + 0.5 * quad)


# --- contour ellipses (constant-density level sets) ---------------------------

def ellipse_axes(Sigma, c=1.0):
    """Semi-axes and tilt of the contour ellipse {w: w^T Sigma^{-1} w = c^2}.
    Eigen-decompose Sigma = V diag(lam) V^T (~MA-04): semi-axis i = c sqrt(lam_i)
    along eigenvector i.  Returns (a, b, theta) with a>=b and theta the angle of
    the major axis (radians)."""
    Sigma = np.asarray(Sigma, dtype=float)
    lam, V = np.linalg.eigh(Sigma)          # ascending eigenvalues, orthonormal V
    semi = c * np.sqrt(lam)
    j = int(np.argmax(semi))                # major axis = largest eigenvalue
    a = float(semi[j])
    b = float(semi[1 - j])
    theta = float(math.atan2(V[1, j], V[0, j]))
    return a, b, theta


def ellipse_points(mux, muy, sx, sy, rho, c=1.0, n=64):
    """Points (x_arr, y_arr) tracing the contour ellipse mahalanobis_sq = c^2.
    Built by rotating the principal-axis parametrization back to (x,y)."""
    Sigma = covariance_matrix(sx, sy, rho)
    a, b, theta = ellipse_axes(Sigma, c)
    t = np.linspace(0.0, 2.0 * math.pi, n)
    ct, st = math.cos(theta), math.sin(theta)
    px = a * np.cos(t)
    py = b * np.sin(t)
    x = mux + ct * px - st * py
    y = muy + st * px + ct * py
    return x, y


# --- demo ---------------------------------------------------------------------

def _demo():
    print("ST-15  the bivariate normal distribution -- demo")
    print("=" * 52)
    mux, muy, sx, sy, rho = 1.0, 2.0, 1.0, 2.0, 0.6
    mu = (mux, muy)
    Sigma = covariance_matrix(sx, sy, rho)
    print(f"params: mu_X={mux}, mu_Y={muy}, sx={sx}, sy={sy}, rho={rho}")
    print(f"Sigma =\n{Sigma}")
    print(f"det Sigma = {np.linalg.det(Sigma):.6f}  (= sx^2 sy^2 (1-rho^2) = "
          f"{sx*sx*sy*sy*(1-rho*rho):.6f})")
    print(f"positive-definite? {is_positive_definite(Sigma)};  "
          f"rho recovered from Sigma = {correlation(Sigma):.4f}")

    x0, y0 = 1.5, 3.0
    f_explicit = bivariate_normal_pdf(x0, y0, mux, muy, sx, sy, rho)
    f_matrix = bivariate_normal_pdf_cov(x0, y0, mu, Sigma)
    print(f"\nf({x0},{y0}):  explicit = {f_explicit:.8f},  "
          f"matrix form = {f_matrix:.8f}  (equal)")
    print(f"Mahalanobis^2 at that point = {mahalanobis_sq(x0,y0,mux,muy,sx,sy,rho):.6f}")

    mean, var = conditional_params(x0, mux, muy, sx, sy, rho)
    print(f"\nY | X={x0}  ~  N(mean={mean:.4f}, var={var:.4f})")
    print(f"  regression slope rho sy/sx = {rho*sy/sx:.4f};  "
          f"conditional var sy^2(1-rho^2) = {sy*sy*(1-rho*rho):.4f}")

    print("\nfactorization check  f(x,y) = f_X(x) * f(y|x):")
    lhs = bivariate_normal_pdf(x0, y0, mux, muy, sx, sy, rho)
    rhs = marginal_pdf_x(x0, mux, sx) * conditional_pdf_y_given_x(y0, x0, mux, muy, sx, sy, rho)
    print(f"  {lhs:.8f}  vs  {rhs:.8f}")

    print("\nrho=0  =>  independence  f(x,y) = f_X(x) f_Y(y):")
    j0 = bivariate_normal_pdf(x0, y0, mux, muy, sx, sy, 0.0)
    p0 = marginal_pdf_x(x0, mux, sx) * marginal_pdf_y(y0, muy, sy)
    print(f"  {j0:.8f}  vs  {p0:.8f}")

    a, b, th = ellipse_axes(Sigma, c=1.0)
    print(f"\none-sigma contour ellipse: semi-axes a={a:.4f}, b={b:.4f}, "
          f"tilt={math.degrees(th):.2f} deg")
    xs, ys = ellipse_points(mux, muy, sx, sy, rho, c=1.0, n=5)
    q = [float(mahalanobis_sq(xi, yi, mux, muy, sx, sy, rho)) for xi, yi in zip(xs, ys)]
    print(f"  Mahalanobis^2 on the c=1 ellipse: {[round(v, 4) for v in q]} (all 1)")


if __name__ == "__main__":
    _demo()
