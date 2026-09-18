"""ST-10  Continuous random variables -- pdf/cdf, expectation, quantiles, uniform.

Probability theory trunk, module ST-10 (modules/ST/list_ST.txt).
Source: Penn State STAT 414 OER, Lesson 13 (Exploring Continuous Data) and
Lesson 14 (Continuous Random Variables).  Continuous analogue of the discrete
machinery in ~ST-05; the point-mass / Dirac-delta limit ties to ~MA-15.

A continuous random variable X is described by a probability *density* f(x):
    f(x) >= 0   and   integral over R of f = 1,
with the cumulative distribution function (cdf)
    F(x) = P(X <= x) = integral_{-inf}^{x} f(t) dt,   so   f(x) = F'(x).
Because probability is an *area* under f, the probability of any single point is
zero, P(X = x) = 0, and
    P(a < X < b) = F(b) - F(a) = integral_a^b f.
Expectation and variance are integrals (the sums of ~ST-05 become integrals),
    E[X]   = integral x f(x) dx,
    Var[X] = E[X^2] - (E[X])^2 = integral x^2 f - (integral x f)^2,
percentiles invert the cdf, F(x_p) = p, and the simplest continuous law is the
uniform U(a,b): f = 1/(b-a), F = (x-a)/(b-a), mean (a+b)/2, variance (b-a)^2/12.
"""

import math

__all__ = [
    "_integrate", "pdf_is_normalized", "cdf_from_pdf", "prob_between",
    "expectation_continuous", "expectation_of", "moment_continuous",
    "variance_continuous", "quantile", "median_continuous",
    "uniform_pdf", "uniform_cdf", "uniform_mean", "uniform_var",
    "uniform_quantile", "point_mass_pdf",
]


# --- numerical integrator (continuous-check helper, cf. SM-06 _integrate) -----

def _integrate(f, a, b, n=20000):
    """Composite midpoint-rule integral of f over [a,b] (continuous-check helper)."""
    if b <= a:
        return 0.0
    h = (b - a) / n
    return sum(f(a + (i + 0.5) * h) * h for i in range(n))


# --- pdf / cdf axioms (STAT 414 Lesson 14.1-14.2) ----------------------------

def pdf_is_normalized(f, a, b, tol=1e-6, n=20000):
    """Total-probability axiom: True iff integral_a^b f(x) dx == 1 (to tol)."""
    return abs(_integrate(f, a, b, n) - 1.0) <= tol


def cdf_from_pdf(f, x, a, n=20000):
    """cdf as the area under the pdf: F(x) = integral_{a}^{x} f(t) dt (support >= a)."""
    return _integrate(f, a, x, n)


def prob_between(f, lo, hi, n=20000):
    """Interval probability P(lo < X < hi) = integral_{lo}^{hi} f = F(hi) - F(lo).
    Note P(X = c) = prob_between(f, c, c) = 0 -- single points carry no area."""
    return _integrate(f, lo, hi, n)


# --- expectation and variance as integrals (STAT 414 Lesson 14.3) ------------

def expectation_continuous(f, a, b, n=20000):
    """Mean of a continuous RV: E[X] = integral_a^b x f(x) dx."""
    return _integrate(lambda x: x * f(x), a, b, n)


def expectation_of(g, f, a, b, n=20000):
    """Law of the unconscious statistician: E[g(X)] = integral_a^b g(x) f(x) dx."""
    return _integrate(lambda x: g(x) * f(x), a, b, n)


def moment_continuous(f, a, b, k, n=20000):
    """k-th raw moment: E[X^k] = integral_a^b x^k f(x) dx."""
    return _integrate(lambda x: (x ** k) * f(x), a, b, n)


def variance_continuous(f, a, b, n=20000):
    """Variance: Var[X] = E[X^2] - (E[X])^2 (shortcut form of E[(X-mu)^2])."""
    m1 = expectation_continuous(f, a, b, n)
    m2 = moment_continuous(f, a, b, 2, n)
    return m2 - m1 * m1


# --- percentiles / quantiles by inverting the cdf (STAT 414 Lesson 14.4) -----

def quantile(F, p, lo, hi, tol=1e-12, maxiter=200):
    """p-th quantile (100p-th percentile): solve F(x_p) = p on [lo,hi] by bisection."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must lie strictly in (0,1)")
    a, b = lo, hi
    fa = F(a) - p
    if fa == 0.0:
        return a
    for _ in range(maxiter):
        m = 0.5 * (a + b)
        fm = F(m) - p
        if abs(fm) < tol or (b - a) < tol:
            return m
        if (fa < 0.0) == (fm < 0.0):
            a, fa = m, fm
        else:
            b = m
    return 0.5 * (a + b)


def median_continuous(F, lo, hi):
    """Median = the 0.5-quantile: the x with F(x) = 1/2."""
    return quantile(F, 0.5, lo, hi)


# --- the continuous uniform distribution U(a,b) (STAT 414 Lesson 14.6) --------

def uniform_pdf(x, a, b):
    """Uniform pdf on [a,b]: f(x) = 1/(b-a) for a <= x <= b, else 0."""
    return 1.0 / (b - a) if a <= x <= b else 0.0


def uniform_cdf(x, a, b):
    """Uniform cdf: 0 below a, (x-a)/(b-a) on [a,b], 1 above b."""
    if x <= a:
        return 0.0
    if x >= b:
        return 1.0
    return (x - a) / (b - a)


def uniform_mean(a, b):
    """Mean of U(a,b): (a+b)/2 (the midpoint of the support)."""
    return 0.5 * (a + b)


def uniform_var(a, b):
    """Variance of U(a,b): (b-a)^2 / 12."""
    return (b - a) ** 2 / 12.0


def uniform_quantile(p, a, b):
    """p-th percentile of U(a,b): a + p(b-a) (closed-form inverse of the cdf)."""
    return a + p * (b - a)


# --- the discrete -> continuous bridge: a point mass as a nascent delta -------

def point_mass_pdf(x, c, eps):
    """Box density of a point mass at c: 1/(2 eps) on [c-eps, c+eps], else 0.
    As eps -> 0 this -> delta(x-c) (~MA-15): mean -> c, variance -> 0 (= eps^2/3).
    A discrete point mass (~ST-05) is the eps -> 0 limit of this continuous pdf."""
    return 1.0 / (2.0 * eps) if (c - eps) <= x <= (c + eps) else 0.0


# --- demo --------------------------------------------------------------------

def _demo():
    print("ST-10 continuous random variables -- demo")
    print("=" * 52)

    a, b = 2.0, 8.0
    f = lambda x: uniform_pdf(x, a, b)
    F = lambda x: uniform_cdf(x, a, b)
    print(f"Uniform U({a:.0f},{b:.0f}):")
    print(f"  normalized?            {pdf_is_normalized(f, a, b)}")
    print(f"  mean (a+b)/2           = {uniform_mean(a, b):.4f}   "
          f"(integral check {expectation_continuous(f, a, b):.4f})")
    print(f"  variance (b-a)^2/12    = {uniform_var(a, b):.4f}   "
          f"(integral check {variance_continuous(f, a, b):.4f})")
    print(f"  P(3 < X < 5)           = {prob_between(f, 3.0, 5.0):.4f}   "
          f"(F(5)-F(3) = {F(5.0) - F(3.0):.4f})")
    print(f"  P(X = 5)               = {prob_between(f, 5.0, 5.0):.4f}")
    print(f"  median / 25th pct      = {median_continuous(F, a, b):.4f} / "
          f"{quantile(F, 0.25, a, b):.4f}   (closed: {uniform_quantile(0.25, a, b):.4f})")

    print("\nGeneric pdf  f(x) = 2x on [0,1]  (cdf F = x^2):")
    g = lambda x: 2.0 * x
    Gc = lambda x: x * x
    print(f"  normalized?            {pdf_is_normalized(g, 0.0, 1.0)}")
    print(f"  mean = 2/3             = {expectation_continuous(g, 0.0, 1.0):.6f}")
    print(f"  var  = 1/18            = {variance_continuous(g, 0.0, 1.0):.6f}")
    print(f"  median  F(x)=1/2       = {quantile(Gc, 0.5, 0.0, 1.0):.6f}  "
          f"(sqrt(1/2) = {math.sqrt(0.5):.6f})")

    print("\nPoint mass at c=4 as a nascent delta (~MA-15), Var = eps^2/3:")
    c = 4.0
    for eps in (0.5, 0.1, 0.01):
        pm = lambda x, e=eps: point_mass_pdf(x, c, e)
        mu = expectation_continuous(pm, c - eps, c + eps)
        var = variance_continuous(pm, c - eps, c + eps)
        print(f"  eps={eps:5.2f}:  mean={mu:.4f}  var={var:.3e}  (eps^2/3={eps ** 2 / 3:.3e})")
    print("  -> eps->0: the continuous density collapses to a discrete point mass.")


if __name__ == "__main__":
    _demo()
