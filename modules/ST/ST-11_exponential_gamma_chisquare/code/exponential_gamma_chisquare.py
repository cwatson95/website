"""ST-11  Exponential, gamma & chi-square distributions -- the gamma function.

Probability theory trunk, module ST-11 (Penn State STAT 414, Lesson 15).
Self-contained: pure numpy + Python stdlib (math) only.  No sibling imports.

The gamma function  Gamma(a) = int_0^inf t^{a-1} e^{-t} dt  (a > 0) interpolates the
factorial, Gamma(n) = (n-1)!, and obeys the recursion Gamma(a+1) = a Gamma(a).  It
normalizes the **gamma family**:

    exponential(lam):  f(x) = lam e^{-lam x},          mean 1/lam, var 1/lam^2
    gamma(a, theta):   f(x) = x^{a-1} e^{-x/theta}
                              / (Gamma(a) theta^a),     mean a theta, var a theta^2
    chi-square(r):     gamma(a = r/2, theta = 2),       mean r,      var 2r

The exponential is gamma with shape a = 1; a sum of a iid exponentials of common
rate is gamma (the Erlang waiting time); chi-square_r is gamma(r/2, 2).  The
exponential alone is **memoryless**: P(X > s+t | X > s) = P(X > t).  These three
laws are the continuous waiting-time / sum-of-squares distributions used everywhere
downstream (sampling theory ~ST-17, molecular speeds & energies ~SM-06).
"""

import math

import numpy as np

__all__ = [
    "gamma_function", "gamma_lanczos",
    "exponential_pdf", "exponential_cdf", "exponential_survival",
    "exponential_mean", "exponential_var", "exponential_mgf",
    "exp_memoryless_check",
    "gamma_pdf", "gamma_cdf", "gamma_mean", "gamma_var", "gamma_mgf",
    "chi2_pdf", "chi2_cdf", "chi2_mean", "chi2_var", "chi2_mgf",
    "convolve_two_exponentials_pdf", "simulate_sum_of_exponentials",
    "lower_incomplete_gamma_regularized",
]


# --- numerical integrator (midpoint rule) for the continuous checks ----------

def _integrate(f, a, b, n=20000):
    """Midpoint-rule estimate of int_a^b f(x) dx (avoids the x=0 endpoint)."""
    dx = (b - a) / n
    return sum(f(a + (i + 0.5) * dx) * dx for i in range(n))


# --- the gamma function  Gamma(a) = int_0^inf t^{a-1} e^{-t} dt  (STAT 414 L15.1)

def gamma_function(alpha):
    """Gamma function Gamma(a) = int_0^inf t^{a-1} e^{-t} dt (math.gamma); the
    factorial interpolant Gamma(n) = (n-1)! obeying Gamma(a+1) = a Gamma(a)."""
    return math.gamma(alpha)


# Lanczos g=7, n=9 coefficients -- an independent approximation of Gamma(z).
_LANCZOS_G = 7
_LANCZOS_C = (
    0.99999999999980993,
    676.5203681218851,
    -1259.1392167224028,
    771.32342877765313,
    -176.61502916214059,
    12.507343278686905,
    -0.13857109526572012,
    9.9843695780195716e-6,
    1.5056327351493116e-7,
)


def gamma_lanczos(z):
    """Lanczos approximation of Gamma(z) -- an independent cross-check of
    gamma_function (reflection formula handles z < 1/2)."""
    if z < 0.5:
        return math.pi / (math.sin(math.pi * z) * gamma_lanczos(1.0 - z))
    z -= 1.0
    x = _LANCZOS_C[0]
    for i in range(1, _LANCZOS_G + 2):
        x += _LANCZOS_C[i] / (z + i)
    t = z + _LANCZOS_G + 0.5
    return math.sqrt(2.0 * math.pi) * t ** (z + 0.5) * math.exp(-t) * x


# --- regularized lower incomplete gamma  P(a,x) = gamma(a,x)/Gamma(a) ---------
# (Numerical Recipes: series for x < a+1, continued fraction otherwise.)

def _gser(a, x, itmax=1000, eps=1e-15):
    """Series expansion of P(a,x) for x < a+1."""
    if x <= 0.0:
        return 0.0
    ap = a
    total = 1.0 / a
    delta = total
    for _ in range(itmax):
        ap += 1.0
        delta *= x / ap
        total += delta
        if abs(delta) < abs(total) * eps:
            break
    return total * math.exp(-x + a * math.log(x) - math.lgamma(a))


def _gcf(a, x, itmax=1000, eps=1e-15):
    """Continued-fraction expansion of Q(a,x) = 1 - P(a,x) for x >= a+1 (Lentz)."""
    tiny = 1e-300
    b = x + 1.0 - a
    c = 1.0 / tiny
    d = 1.0 / b
    h = d
    for i in range(1, itmax + 1):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h


def lower_incomplete_gamma_regularized(a, x):
    """Regularized lower incomplete gamma P(a,x) = (1/Gamma(a)) int_0^x t^{a-1}
    e^{-t} dt -- the building block of the gamma / chi-square cdf."""
    if x < 0.0 or a <= 0.0:
        raise ValueError("require a > 0 and x >= 0")
    if x == 0.0:
        return 0.0
    if x < a + 1.0:
        return _gser(a, x)
    return 1.0 - _gcf(a, x)


# --- exponential distribution  f(x) = lam e^{-lam x}  (STAT 414 L15.2) --------

def exponential_pdf(x, lam):
    """Exponential pdf f(x) = lam e^{-lam x} for x >= 0 (rate lam, scale 1/lam)."""
    if x < 0.0:
        return 0.0
    return lam * math.exp(-lam * x)


def exponential_cdf(x, lam):
    """Exponential cdf F(x) = 1 - e^{-lam x} for x >= 0."""
    if x < 0.0:
        return 0.0
    return 1.0 - math.exp(-lam * x)


def exponential_survival(x, lam):
    """Exponential survival function S(x) = P(X > x) = e^{-lam x}."""
    if x < 0.0:
        return 1.0
    return math.exp(-lam * x)


def exponential_mean(lam):
    """Exponential mean E[X] = 1/lam (= theta, the scale)."""
    return 1.0 / lam


def exponential_var(lam):
    """Exponential variance Var(X) = 1/lam^2."""
    return 1.0 / (lam * lam)


def exponential_mgf(t, lam):
    """Exponential mgf M(t) = lam/(lam - t) = 1/(1 - theta t) for t < lam."""
    return lam / (lam - t)


def exp_memoryless_check(s, t, lam):
    """Memorylessness: returns (P(X > s+t | X > s), P(X > t)); the two are equal
    because P(X>s+t)/P(X>s) = e^{-lam(s+t)}/e^{-lam s} = e^{-lam t}."""
    conditional = exponential_survival(s + t, lam) / exponential_survival(s, lam)
    marginal = exponential_survival(t, lam)
    return conditional, marginal


# --- gamma distribution  f(x) = x^{a-1} e^{-x/theta} / (Gamma(a) theta^a) -----

def gamma_pdf(x, alpha, theta):
    """Gamma pdf f(x) = x^{a-1} e^{-x/theta} / (Gamma(a) theta^a), shape a > 0,
    scale theta > 0, x > 0."""
    if x < 0.0:
        return 0.0
    if x == 0.0:
        if alpha < 1.0:
            return math.inf
        if alpha == 1.0:
            return 1.0 / theta
        return 0.0
    return (x ** (alpha - 1.0) * math.exp(-x / theta)
            / (math.gamma(alpha) * theta ** alpha))


def gamma_cdf(x, alpha, theta):
    """Gamma cdf F(x) = P(a, x/theta), the regularized lower incomplete gamma."""
    if x <= 0.0:
        return 0.0
    return lower_incomplete_gamma_regularized(alpha, x / theta)


def gamma_mean(alpha, theta):
    """Gamma mean E[X] = a theta."""
    return alpha * theta


def gamma_var(alpha, theta):
    """Gamma variance Var(X) = a theta^2."""
    return alpha * theta * theta


def gamma_mgf(t, alpha, theta):
    """Gamma mgf M(t) = (1 - theta t)^{-a} for t < 1/theta."""
    return (1.0 - theta * t) ** (-alpha)


# --- chi-square distribution  chi^2_r = gamma(a = r/2, theta = 2) -------------

def chi2_pdf(x, r):
    """Chi-square pdf with r degrees of freedom = gamma_pdf(x, r/2, 2)."""
    return gamma_pdf(x, r / 2.0, 2.0)


def chi2_cdf(x, r):
    """Chi-square cdf with r degrees of freedom = gamma_cdf(x, r/2, 2)."""
    return gamma_cdf(x, r / 2.0, 2.0)


def chi2_mean(r):
    """Chi-square mean E[X] = r (= a theta with a = r/2, theta = 2)."""
    return float(r)


def chi2_var(r):
    """Chi-square variance Var(X) = 2r (= a theta^2 with a = r/2, theta = 2)."""
    return 2.0 * r


def chi2_mgf(t, r):
    """Chi-square mgf M(t) = (1 - 2t)^{-r/2} for t < 1/2."""
    return (1.0 - 2.0 * t) ** (-r / 2.0)


# --- sum of exponentials is gamma (Erlang waiting time) ----------------------

def convolve_two_exponentials_pdf(x, lam):
    """Density of X1 + X2, X_i ~ exponential(lam) iid, by the convolution
    int_0^x f(y) f(x-y) dy = lam^2 x e^{-lam x} -- exactly gamma(a=2, theta=1/lam)."""
    if x < 0.0:
        return 0.0
    return lam * lam * x * math.exp(-lam * x)


def simulate_sum_of_exponentials(alpha, theta, n=200000, seed=0):
    """Monte-Carlo check that a sum of `alpha` iid exponential(scale theta)
    variables is gamma(alpha, theta): returns (sample_mean, sample_var)."""
    rng = np.random.default_rng(seed)
    samples = rng.exponential(scale=theta, size=(n, int(alpha))).sum(axis=1)
    return float(samples.mean()), float(samples.var())


# --- demo --------------------------------------------------------------------

def _demo():
    print("ST-11 exponential, gamma & chi-square -- demo")
    print("=" * 46)

    print("gamma function  Gamma(a+1) = a Gamma(a),  Gamma(n) = (n-1)!:")
    for a in (1, 2, 3, 4, 5):
        print(f"  Gamma({a}) = {gamma_function(a):8.4f}   (n-1)! = {math.factorial(a - 1)}")
    print(f"  Gamma(1/2) = {gamma_function(0.5):.6f}  vs sqrt(pi) = {math.sqrt(math.pi):.6f}")
    print(f"  Lanczos Gamma(5.7) = {gamma_lanczos(5.7):.8f}  math.gamma = {math.gamma(5.7):.8f}")

    print("\nexponential(lam=0.5)  [mean 1/lam = 2, var 1/lam^2 = 4]:")
    lam = 0.5
    print(f"  mean = {exponential_mean(lam)}, var = {exponential_var(lam)}")
    area = _integrate(lambda x: exponential_pdf(x, lam), 0.0, 200.0)
    print(f"  int f dx = {area:.6f}   M'(0)=mean? M(t)=lam/(lam-t)")
    cond, marg = exp_memoryless_check(3.0, 2.0, lam)
    print(f"  memoryless: P(X>5|X>3) = {cond:.6f} = P(X>2) = {marg:.6f}")

    print("\ngamma(a=3, theta=2)  [mean a*theta = 6, var a*theta^2 = 12]:")
    a, th = 3.0, 2.0
    print(f"  mean = {gamma_mean(a, th)}, var = {gamma_var(a, th)}")
    area = _integrate(lambda x: gamma_pdf(x, a, th), 0.0, 80.0)
    print(f"  int f dx = {area:.6f},  F(6) = {gamma_cdf(6.0, a, th):.6f}")
    sm, sv = simulate_sum_of_exponentials(a, th)
    print(f"  Monte-Carlo sum of 3 Exp(theta=2): mean {sm:.3f} (->6), var {sv:.3f} (->12)")

    print("\nchi-square  chi^2_r = gamma(r/2, 2)  [mean r, var 2r]:")
    for r in (1, 2, 4, 10):
        print(f"  r={r:>2}: mean={chi2_mean(r):4.1f}, var={chi2_var(r):4.1f}, "
              f"F(r) = {chi2_cdf(r, r):.4f}")
    print(f"  chi^2_2 pdf at x=3 = {chi2_pdf(3.0, 2):.6f}  vs Exp(1/2) = "
          f"{exponential_pdf(3.0, 0.5):.6f}  (equal: chi^2_2 is exponential mean 2)")


if __name__ == "__main__":
    _demo()
