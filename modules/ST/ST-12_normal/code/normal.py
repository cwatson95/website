"""ST-12  The normal (Gaussian) distribution -- pdf, standardization, cdf, mgf.

Probability-theory trunk, module ST-12 (modules/ST/list_ST.txt).
Source: Penn State STAT 414, Lesson 16 "Normal Distributions"
(online.stat.psu.edu/stat414/lesson/16).  Follows Hogg, Tanis & Zimmerman,
*Probability and Statistical Inference*, Ch. 5.  Builds on ST-10 (continuous
random variables, pdf/cdf) and ST-06 (moment-generating functions).

A continuous random variable X is **normal** N(mu, sigma^2) when its density is
the Gaussian bell

    f(x) = 1 / (sigma sqrt(2 pi)) * exp( -(x - mu)^2 / (2 sigma^2) ),

normalized by the **Gaussian integral**  int exp(-x^2/2) dx = sqrt(2 pi).
**Standardizing** Z = (X - mu)/sigma sends every normal to the single standard
normal N(0,1), whose cdf is  Phi(z) = (1/2)[1 + erf(z/sqrt2)].  The mean is mu,
the variance sigma^2, the mgf  M(t) = exp(mu t + sigma^2 t^2 / 2); the
**68-95-99.7 rule** is Phi(k) - Phi(-k) at k = 1, 2, 3.  Pure numpy + math only.
"""

import math

import numpy as np

__all__ = [
    "SQRT_2PI", "normal_pdf", "standard_normal_pdf", "standardize",
    "standard_normal_cdf", "normal_cdf", "normal_interval_prob",
    "gaussian_integral_check", "normal_mean_by_integration",
    "normal_variance_by_integration", "normal_mgf", "mgf_moment",
    "probit", "normal_quantile", "empirical_rule",
]

SQRT_2PI = math.sqrt(2.0 * math.pi)        # sqrt(2 pi) = 2.5066... (the Gaussian norm)


# --- numerical integrator (midpoint rule, for continuous checks) -------------

def _integrate(f, a, b, n=20000):
    """Midpoint-rule estimate of int_a^b f(x) dx with n panels."""
    dx = (b - a) / n
    return sum(f(a + (i + 0.5) * dx) * dx for i in range(n))


# --- the Gaussian density (STAT 414 L16.1) -----------------------------------

def normal_pdf(x, mu=0.0, sigma=1.0):
    """Normal N(mu, sigma^2) pdf  f(x) = exp(-(x-mu)^2/2sigma^2)/(sigma sqrt(2pi))."""
    z = (x - mu) / sigma
    return np.exp(-0.5 * z * z) / (sigma * SQRT_2PI)


def standard_normal_pdf(z):
    """Standard normal N(0,1) density  phi(z) = exp(-z^2/2)/sqrt(2pi)."""
    return np.exp(-0.5 * np.asarray(z, dtype=float) ** 2) / SQRT_2PI


# --- standardization Z = (X - mu)/sigma  (STAT 414 L16.2) --------------------

def standardize(x, mu, sigma):
    """Z-score  z = (x - mu)/sigma; maps N(mu,sigma^2) -> N(0,1)."""
    return (x - mu) / sigma


# --- cumulative distribution function via the error function (L16.3) ---------

def standard_normal_cdf(z):
    """Standard normal cdf  Phi(z) = (1/2)[1 + erf(z/sqrt2)] (vectorized)."""
    z = np.asarray(z, dtype=float)
    return 0.5 * (1.0 + np.vectorize(math.erf)(z / math.sqrt(2.0)))


def normal_cdf(x, mu=0.0, sigma=1.0):
    """Normal cdf  F(x) = Phi((x-mu)/sigma) -- standardize, then Phi."""
    return standard_normal_cdf(standardize(x, mu, sigma))


def normal_interval_prob(a, b, mu=0.0, sigma=1.0):
    """P(a < X <= b) = F(b) - F(a) = Phi((b-mu)/sigma) - Phi((a-mu)/sigma)."""
    return normal_cdf(b, mu, sigma) - normal_cdf(a, mu, sigma)


# --- the Gaussian integral  int exp(-x^2/2) dx = sqrt(2 pi)  (L16.1) ---------

def gaussian_integral_check(half_width=40.0, n=200000):
    """Numerically integrate exp(-x^2/2) over [-W, W]; -> sqrt(2 pi) = SQRT_2PI."""
    return _integrate(lambda x: math.exp(-0.5 * x * x), -half_width, half_width, n)


# --- mean and variance by integrating the density (L16.1) --------------------

def normal_mean_by_integration(mu=0.0, sigma=1.0, n_sigma=12.0, n=40000):
    """E[X] = int x f(x) dx, integrated over mu +/- n_sigma * sigma; -> mu."""
    lo, hi = mu - n_sigma * sigma, mu + n_sigma * sigma
    return _integrate(lambda x: x * float(normal_pdf(x, mu, sigma)), lo, hi, n)


def normal_variance_by_integration(mu=0.0, sigma=1.0, n_sigma=12.0, n=40000):
    """Var[X] = int (x-mu)^2 f(x) dx over mu +/- n_sigma*sigma; -> sigma^2."""
    lo, hi = mu - n_sigma * sigma, mu + n_sigma * sigma
    return _integrate(lambda x: (x - mu) ** 2 * float(normal_pdf(x, mu, sigma)), lo, hi, n)


# --- moment-generating function  M(t) = exp(mu t + sigma^2 t^2 / 2)  (L16.1) -

def normal_mgf(t, mu=0.0, sigma=1.0):
    """Normal mgf  M(t) = E[e^{tX}] = exp(mu t + sigma^2 t^2 / 2)."""
    return np.exp(mu * t + 0.5 * sigma ** 2 * t ** 2)


def mgf_moment(k, mu=0.0, sigma=1.0, h=1e-3):
    """k-th raw moment E[X^k] via k-th central finite difference of M at t=0."""
    # k-th derivative of M(t) at 0 by central differences of order k
    coeffs = [(-1) ** i * math.comb(k, i) for i in range(k + 1)]
    nodes = [k / 2.0 - i for i in range(k + 1)]   # symmetric stencil k/2 .. -k/2
    deriv = sum(c * float(normal_mgf(j * h, mu, sigma)) for c, j in zip(coeffs, nodes))
    return deriv / h ** k


# --- inverse cdf (probit / quantile) by bisection  (L16.3) -------------------

def probit(p, tol=1e-12, lo=-40.0, hi=40.0):
    """Standard-normal quantile  z = Phi^{-1}(p) by bisection on Phi(z) = p."""
    if not 0.0 < p < 1.0:
        raise ValueError("probit: p must lie strictly in (0, 1)")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if float(standard_normal_cdf(mid)) < p:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


def normal_quantile(p, mu=0.0, sigma=1.0):
    """Quantile of N(mu,sigma^2):  x_p = mu + sigma * Phi^{-1}(p)."""
    return mu + sigma * probit(p)


# --- the 68-95-99.7 (empirical) rule  (L16.2) --------------------------------

def empirical_rule(k):
    """P(|Z| <= k) = Phi(k) - Phi(-k) = 2 Phi(k) - 1; k=1,2,3 -> .68,.95,.997."""
    return float(2.0 * standard_normal_cdf(k) - 1.0)


# --- demo --------------------------------------------------------------------

def _demo():
    print("ST-12  The normal distribution -- demo")
    print("=" * 52)

    print("\nGaussian integral  int exp(-x^2/2) dx = sqrt(2 pi):")
    print(f"  numeric  = {gaussian_integral_check():.10f}")
    print(f"  sqrt(2pi)= {SQRT_2PI:.10f}")

    print("\nStandard normal cdf Phi(z) via erf:")
    for z in (-2.0, -1.0, 0.0, 1.0, 1.96, 2.0):
        print(f"  Phi({z:+.2f}) = {float(standard_normal_cdf(z)):.6f}")

    print("\nMean / variance of N(3, 2^2) by integrating the density:")
    print(f"  E[X]   = {normal_mean_by_integration(3.0, 2.0):.6f}   (mu = 3)")
    print(f"  Var[X] = {normal_variance_by_integration(3.0, 2.0):.6f}   (sigma^2 = 4)")

    print("\nMgf M(t)=exp(mu t + sigma^2 t^2/2) generates the moments (mu=3,sigma=2):")
    print(f"  M(0)            = {float(normal_mgf(0.0, 3.0, 2.0)):.6f}  (=1)")
    print(f"  E[X]  = M'(0)   = {mgf_moment(1, 3.0, 2.0):.6f}  (=mu=3)")
    print(f"  E[X^2]= M''(0)  = {mgf_moment(2, 3.0, 2.0):.6f}  (=mu^2+sigma^2=13)")

    print("\n68-95-99.7 (empirical) rule  P(|Z| <= k) = 2 Phi(k) - 1:")
    for k in (1, 2, 3):
        print(f"  k={k}: {100*empirical_rule(k):.3f}%")

    print("\nInverse cdf (probit) by bisection:")
    for p in (0.5, 0.975, 0.95):
        print(f"  Phi^-1({p}) = {probit(p):.6f}")
    print(f"  N(100,15^2) 97.5th percentile = {normal_quantile(0.975, 100.0, 15.0):.4f}")


if __name__ == "__main__":
    _demo()
