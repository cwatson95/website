"""ST-16  Transformations of random variables -- cdf, Jacobian, convolution.

Probability theory trunk, module ST-16 (modules/ST/list_ST.txt).
Source: Penn State STAT 414 OER, Lessons 22-24
  (L22 Functions of One Random Variable; L23 Transformations of Two Random
   Variables; L24 Several Independent Random Variables).
Follows Hogg, Tanis & Zimmerman, *Probability and Statistical Inference*, Ch. 5.

Given a random variable X with a known density f_X and a function Y = g(X), what
is the density f_Y?  Three tools answer this:

  * the **cdf (distribution-function) method** -- compute F_Y(y)=P(g(X)<=y) by
    integrating f_X over the set {x : g(x)<=y}, then differentiate;
  * the **change-of-variables formula** for a one-to-one (monotone) g,
        f_Y(y) = f_X(g^{-1}(y)) |dx/dy| ,
    the differentiated cdf method, with |dx/dy| the local stretch factor;
  * the **2-D Jacobian transformation** for (U,V)=T(X,Y),
        f_{UV}(u,v) = f_{XY}(x(u,v),y(u,v)) |J| ,  J = det d(x,y)/d(u,v)  (~MA-03).

Sums of independent variables are the special transform Z=X+Y, whose density is
the **convolution** f_Z(z)=\\int f_X(t) f_Y(z-t) dt -- the probabilistic mirror of
the Fourier convolution theorem (~MA-09; products of transforms in ~ST-17).  Two
canonical results fall out: the sum of two Uniform(0,1) is **triangular**, and
the sum of n independent Exponential(rate) is **Gamma(n,rate)** (Erlang).  The
**probability integral transform** F_X(X) ~ Uniform(0,1) is the change-of-variable
identity in disguise and underlies inverse-transform random sampling.

Pure numpy + stdlib math (math.gamma, math.erf).  Self-contained.
"""

import math

import numpy as np

__all__ = [
    "uniform_pdf", "exp_pdf", "exp_cdf", "exp_quantile", "linear_pdf",
    "linear_quantile", "gamma_pdf", "triangular_pdf", "normal_pdf", "normal_cdf",
    "cdf_of_Y", "pdf_of_Y_cdf_method", "change_of_variables_1d",
    "jacobian_det_2d", "jacobian_transform_2d", "convolution",
    "sum_two_uniforms_pdf", "sum_n_exponentials_pdf",
    "probability_integral_transform_pdf",
]


# --- numerical helpers -------------------------------------------------------

def _integrate(f, a, b, n=20000):
    """Midpoint-rule estimate of \\int_a^b f(x) dx (f may be vectorized)."""
    x = a + (np.arange(n) + 0.5) * (b - a) / n
    return float(np.sum(np.asarray(f(x), dtype=float)) * (b - a) / n)


def _diff(f, x, h=1e-5):
    """Central-difference estimate of f'(x)."""
    return (f(x + h) - f(x - h)) / (2.0 * h)


# --- elementary densities (closed forms used as targets) ---------------------

def uniform_pdf(x, a=0.0, b=1.0):
    """Uniform(a,b) density f(x)=1/(b-a) on [a,b], else 0  (PSU L10)."""
    x = np.asarray(x, dtype=float)
    return np.where((x >= a) & (x <= b), 1.0 / (b - a), 0.0)


def exp_pdf(x, rate=1.0):
    """Exponential(rate) density f(x)=rate*exp(-rate*x), x>=0  (PSU L15)."""
    x = np.asarray(x, dtype=float)
    xpos = np.where(x >= 0.0, x, 0.0)
    return np.where(x >= 0.0, rate * np.exp(-rate * xpos), 0.0)


def exp_cdf(x, rate=1.0):
    """Exponential(rate) cdf F(x)=1-exp(-rate*x), x>=0  (PSU L15)."""
    x = np.asarray(x, dtype=float)
    xpos = np.where(x >= 0.0, x, 0.0)
    return np.where(x >= 0.0, 1.0 - np.exp(-rate * xpos), 0.0)


def exp_quantile(u, rate=1.0):
    """Exponential(rate) quantile F^{-1}(u)=-ln(1-u)/rate  (inverse transform)."""
    u = np.asarray(u, dtype=float)
    return -np.log(1.0 - u) / rate


def linear_pdf(x):
    """Triangular-on-[0,1] density f(x)=2x, 0<=x<=1, else 0 (test density)."""
    x = np.asarray(x, dtype=float)
    return np.where((x >= 0.0) & (x <= 1.0), 2.0 * x, 0.0)


def linear_quantile(u):
    """Quantile of linear_pdf: F(x)=x^2 so F^{-1}(u)=sqrt(u)."""
    u = np.asarray(u, dtype=float)
    return np.sqrt(u)


def gamma_pdf(x, k, rate=1.0):
    """Gamma(shape k, rate) density rate^k/Gamma(k) * x^{k-1} e^{-rate x} (PSU L15)."""
    x = np.asarray(x, dtype=float)
    coef = rate ** k / math.gamma(k)
    xpos = np.where(x > 0.0, x, 1.0)          # avoid 0**(k-1) for k<1
    return np.where(x > 0.0, coef * np.power(xpos, k - 1.0) * np.exp(-rate * x), 0.0)


def triangular_pdf(z):
    """Triangular(0,1,2) density: z on [0,1], 2-z on [1,2] (sum of two U(0,1))."""
    z = np.asarray(z, dtype=float)
    return np.where((z >= 0.0) & (z <= 1.0), z,
                    np.where((z > 1.0) & (z <= 2.0), 2.0 - z, 0.0))


def normal_pdf(x, mu=0.0, sigma=1.0):
    """Normal(mu,sigma^2) density (PSU L16)."""
    x = np.asarray(x, dtype=float)
    return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * math.sqrt(2.0 * math.pi))


def normal_cdf(x, mu=0.0, sigma=1.0):
    """Normal(mu,sigma^2) cdf Phi = (1+erf((x-mu)/(sigma*sqrt2)))/2 (scalar)."""
    return 0.5 * (1.0 + math.erf((x - mu) / (sigma * math.sqrt(2.0))))


# --- the cdf (distribution-function) method (PSU L22) ------------------------

def cdf_of_Y(fX, g, y, x_lo, x_hi, n=200000):
    """cdf method: F_Y(y)=P(g(X)<=y)=\\int_{g(x)<=y} f_X(x) dx  (PSU L22)."""
    x = x_lo + (np.arange(n) + 0.5) * (x_hi - x_lo) / n
    dx = (x_hi - x_lo) / n
    fx = np.asarray(fX(x), dtype=float)
    inside = np.asarray(g(x)) <= y
    return float(np.sum(np.where(inside, fx, 0.0)) * dx)


def pdf_of_Y_cdf_method(fX, g, y, x_lo, x_hi, h=1e-2, n=200000):
    """f_Y(y) = d/dy F_Y(y) from the cdf method, by central difference (PSU L22)."""
    fwd = cdf_of_Y(fX, g, y + h, x_lo, x_hi, n)
    bwd = cdf_of_Y(fX, g, y - h, x_lo, x_hi, n)
    return (fwd - bwd) / (2.0 * h)


# --- change of variables for monotone g (PSU L22) ---------------------------

def change_of_variables_1d(fX, ginv, dxdy, y):
    """Monotone transform: f_Y(y)=f_X(g^{-1}(y)) |dx/dy|  (PSU L22).

    ginv(y)=g^{-1}(y) (the back-substitution) and dxdy(y)=d g^{-1}/dy (signed)."""
    return float(np.asarray(fX(ginv(y)), dtype=float)) * abs(dxdy(y))


# --- 2-D Jacobian transformation (PSU L23; ~MA-03) ---------------------------

def jacobian_det_2d(inv_map, u, v, h=1e-5):
    """Jacobian determinant J = x_u y_v - x_v y_u of (u,v) -> (x,y)=inv_map (~MA-03)."""
    x_up, y_up = inv_map(u + h, v)
    x_um, y_um = inv_map(u - h, v)
    x_vp, y_vp = inv_map(u, v + h)
    x_vm, y_vm = inv_map(u, v - h)
    x_u = (x_up - x_um) / (2.0 * h)
    y_u = (y_up - y_um) / (2.0 * h)
    x_v = (x_vp - x_vm) / (2.0 * h)
    y_v = (y_vp - y_vm) / (2.0 * h)
    return x_u * y_v - x_v * y_u


def jacobian_transform_2d(fXY, inv_map, u, v, jacobian=None, h=1e-5):
    """2-D change of variables: f_{UV}(u,v)=f_{XY}(x,y) |J|  (PSU L23).

    inv_map(u,v)=(x,y); jacobian(u,v)=det d(x,y)/d(u,v) (numeric if None)."""
    x, y = inv_map(u, v)
    J = jacobian(u, v) if jacobian is not None else jacobian_det_2d(inv_map, u, v, h)
    return float(np.asarray(fXY(x, y), dtype=float)) * abs(J)


# --- sums of independent variables = convolution (PSU L23-L24; ~MA-09) -------

def convolution(fX, fY, z, t_lo, t_hi, n=4000):
    """Sum of independents: f_{X+Y}(z)=\\int f_X(t) f_Y(z-t) dt  (PSU L23; ~MA-09)."""
    t = t_lo + (np.arange(n) + 0.5) * (t_hi - t_lo) / n
    dt = (t_hi - t_lo) / n
    return float(np.sum(np.asarray(fX(t), dtype=float)
                        * np.asarray(fY(z - t), dtype=float)) * dt)


def sum_two_uniforms_pdf(z):
    """Closed form: U(0,1)+U(0,1) ~ Triangular(0,1,2) = triangular_pdf(z) (PSU L23)."""
    return triangular_pdf(z)


def sum_n_exponentials_pdf(z, n, rate=1.0):
    """Closed form: sum of n iid Exponential(rate) ~ Gamma(n,rate) (Erlang) (PSU L24)."""
    return gamma_pdf(z, float(n), rate)


# --- probability integral transform (PSU L22) --------------------------------

def probability_integral_transform_pdf(fX, Finv, u, h=1e-6):
    """Density of U=F_X(X): f_U(u)=f_X(F^{-1}(u)) |dF^{-1}/du| == 1 on (0,1) (PSU L22).

    Finv(u)=F_X^{-1}(u) is the quantile function; the result must be 1."""
    x = Finv(u)
    dFinv = (Finv(u + h) - Finv(u - h)) / (2.0 * h)
    return float(np.asarray(fX(x), dtype=float)) * abs(dFinv)


# --- demo --------------------------------------------------------------------

def _demo():
    print("ST-16  Transformations of random variables -- demo")
    print("=" * 58)

    print("\n[1] cdf method:  X ~ U(0,1),  Y = X^2")
    for y in (0.25, 0.5, 0.81):
        Fnum = cdf_of_Y(uniform_pdf, lambda x: x * x, y, 0.0, 1.0)
        print(f"   F_Y({y}) = {Fnum:.5f}   (exact sqrt(y) = {math.sqrt(y):.5f})")
    y = 0.25
    fnum = pdf_of_Y_cdf_method(uniform_pdf, lambda x: x * x, y, 0.0, 1.0)
    print(f"   f_Y({y}) = {fnum:.5f}   (exact 1/(2 sqrt y) = {1/(2*math.sqrt(y)):.5f})")

    print("\n[2] change of variables:  X ~ U(0,1),  Y = -ln(X)/rate  ->  Exp(rate)")
    rate = 1.5
    for y in (0.2, 1.0, 2.5):
        fY = change_of_variables_1d(uniform_pdf,
                                    lambda yy: math.exp(-rate * yy),
                                    lambda yy: -rate * math.exp(-rate * yy), y)
        print(f"   f_Y({y}) = {fY:.5f}   (Exp(rate) = {float(exp_pdf(y, rate)):.5f})")

    print("\n[3] sum of two Uniform(0,1) is triangular:")
    for z in (0.5, 1.0, 1.5):
        c = convolution(uniform_pdf, uniform_pdf, z, 0.0, 1.0)
        print(f"   f_Z({z}) = {c:.5f}   (triangular = {float(triangular_pdf(z)):.5f})")

    print("\n[4] sum of exponentials is gamma (Erlang):  rate = 1")
    g2 = lambda zz: gamma_pdf(zz, 2.0, 1.0)
    for z in (1.0, 2.0, 3.0):
        two = convolution(exp_pdf, exp_pdf, z, 0.0, z)
        three = convolution(g2, exp_pdf, z, 0.0, z)
        print(f"   z={z}:  Exp*Exp={two:.5f} (Gamma2={float(gamma_pdf(z,2,1)):.5f}),  "
              f"+Exp={three:.5f} (Gamma3={float(gamma_pdf(z,3,1)):.5f})")

    print("\n[5] 2-D Jacobian:  X,Y ~ Exp(1) iid;  U=X+Y, V=X/(X+Y)")
    print("    inverse map x=uv, y=u(1-v), |J|=u  ->  f_UV(u,v)=u e^{-u} (Gamma2 x U(0,1))")
    fXY = lambda x, y: float(exp_pdf(x, 1.0)) * float(exp_pdf(y, 1.0))
    inv = lambda u, v: (u * v, u * (1.0 - v))
    for (u, v) in ((1.5, 0.3), (2.0, 0.7)):
        f = jacobian_transform_2d(fXY, inv, u, v)
        print(f"   f_UV({u},{v}) = {f:.5f}   (u e^-u = {u*math.exp(-u):.5f},  |J|~{jacobian_det_2d(inv,u,v):+.4f})")

    print("\n[6] probability integral transform:  F_X(X) ~ Uniform(0,1)")
    for u in (0.2, 0.5, 0.8):
        d_exp = probability_integral_transform_pdf(lambda x: exp_pdf(x, 2.0),
                                                   lambda uu: exp_quantile(uu, 2.0), u)
        d_lin = probability_integral_transform_pdf(linear_pdf, linear_quantile, u)
        print(f"   u={u}:  density(Exp)={d_exp:.5f},  density(f=2x)={d_lin:.5f}  (both = 1)")


if __name__ == "__main__":
    _demo()
