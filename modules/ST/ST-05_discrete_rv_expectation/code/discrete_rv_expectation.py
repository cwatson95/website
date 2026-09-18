"""ST-05  Discrete random variables & expectation -- pmf/cdf, E[X], variance, moments.

Probability-theory trunk, module ST-05 (a module-by-module replica of Penn State
STAT 414; lessons L7 "Discrete Random Variables" and L8 "Mathematical Expectation").

A discrete random variable X takes values in a countable support S_X with a
**probability mass function** f(x) = P(X = x).  A valid pmf satisfies f(x) >= 0 and
sum_x f(x) = 1.  Its **cdf** F(x) = P(X <= x) is a right-continuous step function
that jumps by f(x) at each support point.  The **expectation** of any function
g(X) is the LOTUS sum E[g(X)] = sum_x g(x) f(x); taking g(x)=x gives the mean
mu = E[X], and g(x)=(x-mu)^2 gives the variance sigma^2 = E[X^2] - mu^2.
Expectation is **linear**: E[aX+b] = a E[X] + b and Var(aX+b) = a^2 Var(X).

This is the same averaging rule as the quantum expectation value
<A> = sum_a a |c_a|^2 (~QM-06) and the statistical-mechanics ensemble average
<.> = sum_i (.) P_i (~SM-01): a random variable's law f(x) is a probability
weight, and E[.] is its weighted sum.

Pure numpy + stdlib math.  No scipy / matplotlib / pandas.  Self-contained.
"""

import math

import numpy as np

__all__ = [
    "pmf_is_valid", "support", "cdf_from_pmf", "cdf_table",
    "expectation", "mean", "expectation_of", "lotus",
    "raw_moment", "central_moment", "variance", "std",
    "standardize", "skewness", "excess_kurtosis",
    "linear_transform", "survival", "mean_via_survival", "mgf",
]


# --- the probability mass function (STAT 414 L7) -----------------------------

def _arrays(values, probs):
    """Coerce (values, probs) to float numpy arrays of equal length."""
    x = np.asarray(values, dtype=float)
    p = np.asarray(probs, dtype=float)
    if x.shape != p.shape:
        raise ValueError("values and probs must have the same shape")
    return x, p


def pmf_is_valid(values, probs, tol=1e-9):
    """Validity of a pmf: f(x) >= 0 for all x and sum_x f(x) = 1  (STAT 414 L7)."""
    x, p = _arrays(values, probs)
    nonneg = bool(np.all(p >= -tol))
    sums_to_one = abs(float(np.sum(p)) - 1.0) <= tol
    distinct = len(set(np.round(x, 12))) == len(x)
    return nonneg and sums_to_one and distinct


def support(values, probs, tol=1e-15):
    """Support S_X = { x : f(x) > 0 }: the values carrying positive mass."""
    x, p = _arrays(values, probs)
    return x[p > tol]


# --- the cdf as a step function (STAT 414 L7) --------------------------------

def cdf_from_pmf(values, probs):
    """Cumulative distribution F(x) = P(X <= x) = sum_{x_i <= x} f(x_i) as a
    right-continuous step function; returns a callable F (STAT 414 L7)."""
    x, p = _arrays(values, probs)

    def F(t):
        return float(np.sum(p[x <= t]))

    return F


def cdf_table(values, probs):
    """Step-function table of the cdf: sorted support values and the cumulative
    probabilities F(x_i) reached just after each jump (STAT 414 L7)."""
    x, p = _arrays(values, probs)
    order = np.argsort(x)
    xs = x[order]
    cum = np.cumsum(p[order])
    return xs, cum


# --- expectation and the law of the unconscious statistician (STAT 414 L8) ---

def expectation(values, probs):
    """Mean mu = E[X] = sum_x x f(x): the probability-weighted average value
    (STAT 414 L8).  Equals <A> = sum_a a |c_a|^2 of ~QM-06."""
    x, p = _arrays(values, probs)
    return float(np.sum(x * p))


def mean(values, probs):
    """Alias for expectation: mu = E[X] = sum_x x f(x)  (STAT 414 L8)."""
    return expectation(values, probs)


def expectation_of(g, values, probs):
    """Law of the unconscious statistician: E[g(X)] = sum_x g(x) f(x), the
    expectation of g(X) without finding the law of Y = g(X)  (STAT 414 L8)."""
    x, p = _arrays(values, probs)
    gx = np.array([g(float(xi)) for xi in x], dtype=float)
    return float(np.sum(gx * p))


def lotus(g, values, probs):
    """Alias for expectation_of: E[g(X)] = sum_x g(x) f(x)  (STAT 414 L8)."""
    return expectation_of(g, values, probs)


# --- moments (STAT 414 L8) ----------------------------------------------------

def raw_moment(values, probs, k):
    """k-th raw (about 0) moment  mu'_k = E[X^k] = sum_x x^k f(x)  (STAT 414 L8).
    mu'_0 = 1 (normalization), mu'_1 = mu (the mean)."""
    return expectation_of(lambda x: x ** k, values, probs)


def central_moment(values, probs, k):
    """k-th central moment  mu_k = E[(X-mu)^k] = sum_x (x-mu)^k f(x) (STAT 414 L8).
    mu_1 = 0, mu_2 = sigma^2 (the variance)."""
    mu = expectation(values, probs)
    return expectation_of(lambda x: (x - mu) ** k, values, probs)


def variance(values, probs):
    """Variance sigma^2 = E[(X-mu)^2] = E[X^2] - mu^2 (computational formula),
    the mean squared spread about mu  (STAT 414 L8).  Mirrors ~QM-06's
    sigma_A^2 = <A^2> - <A>^2."""
    mu = expectation(values, probs)
    return raw_moment(values, probs, 2) - mu ** 2


def std(values, probs):
    """Standard deviation sigma = sqrt(Var(X)), in the units of X  (STAT 414 L8)."""
    return math.sqrt(variance(values, probs))


def standardize(values, probs):
    """Standardized variable Z = (X - mu)/sigma; returns (z_values, probs) with
    E[Z] = 0 and Var(Z) = 1  (STAT 414 L8)."""
    x, p = _arrays(values, probs)
    mu = expectation(values, probs)
    sd = std(values, probs)
    return (x - mu) / sd, p


def skewness(values, probs):
    """Skewness gamma_1 = E[Z^3] = mu_3 / sigma^3, the standardized third central
    moment; 0 for any distribution symmetric about its mean  (STAT 414 L8)."""
    sd = std(values, probs)
    return central_moment(values, probs, 3) / sd ** 3


def excess_kurtosis(values, probs):
    """Excess kurtosis gamma_2 = mu_4 / sigma^4 - 3, tail heaviness relative to a
    normal distribution  (STAT 414 L8)."""
    var = variance(values, probs)
    return central_moment(values, probs, 4) / var ** 2 - 3.0


# --- linearity and affine transformations (STAT 414 L8) ----------------------

def linear_transform(a, b, values, probs):
    """The affine image Y = aX + b: returns (a*values + b, probs).  Then
    E[Y] = a E[X] + b and Var(Y) = a^2 Var(X)  (STAT 414 L8)."""
    x, p = _arrays(values, probs)
    return a * x + b, p


# --- the mean from the cdf / survival function (STAT 414 L8) ------------------

def survival(values, probs):
    """Survival (tail) function S(x) = P(X > x) = 1 - F(x); returns a callable."""
    F = cdf_from_pmf(values, probs)
    return lambda t: 1.0 - F(t)


def mean_via_survival(values, probs):
    """Mean of a non-negative integer-valued X by the tail-sum identity
    E[X] = sum_{k>=0} P(X > k) = sum_{k>=0} (1 - F(k))  (STAT 414 L8)."""
    x, _ = _arrays(values, probs)
    if np.any(x < -1e-12) or np.any(np.abs(x - np.round(x)) > 1e-9):
        raise ValueError("mean_via_survival requires non-negative integer support")
    S = survival(values, probs)
    kmax = int(round(float(np.max(x))))
    return float(sum(S(k) for k in range(0, kmax)))


# --- a preview of the moment-generating function (~ST-06) ---------------------

def mgf(values, probs, t):
    """Moment-generating function M(t) = E[e^{tX}] = sum_x e^{tx} f(x), the
    generator whose derivatives at 0 are the raw moments (full story in ~ST-06)."""
    x, p = _arrays(values, probs)
    return float(np.sum(np.exp(t * x) * p))


# --- demo --------------------------------------------------------------------

def _demo():
    print("ST-05  discrete random variables & expectation -- demo")
    print("=" * 56)

    # 1) a fair six-sided die: X uniform on {1,...,6}
    die_x = np.arange(1, 7)
    die_p = np.full(6, 1.0 / 6.0)
    print("fair die  X ~ Uniform{1..6}:")
    print(f"  valid pmf?        {pmf_is_valid(die_x, die_p)}  (sum f = {die_p.sum():.3f})")
    print(f"  mean   mu = E[X]  = {expectation(die_x, die_p):.4f}   (exact 7/2 = 3.5)")
    print(f"  E[X^2]            = {raw_moment(die_x, die_p, 2):.4f}   (exact 91/6)")
    print(f"  var  sigma^2      = {variance(die_x, die_p):.4f}   (exact 35/12)")
    print(f"  std  sigma        = {std(die_x, die_p):.4f}")
    print(f"  skewness          = {skewness(die_x, die_p):.4f}   (symmetric -> 0)")
    xs, cum = cdf_table(die_x, die_p)
    print(f"  cdf jumps F(x)    = {np.round(cum, 3).tolist()}  (reaches 1 at x=6)")
    print(f"  E[X] via survival = {mean_via_survival(die_x, die_p):.4f}")

    # 2) LOTUS: E[(X-3.5)^2] computed two ways
    g = lambda x: (x - 3.5) ** 2
    print("\nLOTUS  E[g(X)] = sum g(x) f(x),  g(x) = (x-3.5)^2:")
    print(f"  expectation_of(g) = {expectation_of(g, die_x, die_p):.4f}  ==  var = "
          f"{variance(die_x, die_p):.4f}")

    # 3) linearity on a skewed custom pmf
    cx = np.array([-1.0, 0.0, 2.0])
    cp = np.array([0.2, 0.5, 0.3])
    a, b = 3.0, -4.0
    yx, yp = linear_transform(a, b, cx, cp)
    print("\ncustom X (support {-1,0,2}, p={.2,.5,.3}), Y = 3X - 4:")
    print(f"  E[X] = {expectation(cx, cp):.4f},  Var(X) = {variance(cx, cp):.4f}")
    print(f"  E[Y]  = {expectation(yx, yp):.4f}  ==  aE[X]+b = {a*expectation(cx,cp)+b:.4f}")
    print(f"  Var(Y)= {variance(yx, yp):.4f}  ==  a^2 Var(X)= {a**2*variance(cx,cp):.4f}")
    print(f"  skewness(X) = {skewness(cx, cp):.4f}  (not symmetric)")

    # 4) mgf preview: M'(0) = mu, M''(0) = E[X^2]
    h = 1e-5
    m_prime = (mgf(cx, cp, h) - mgf(cx, cp, -h)) / (2 * h)
    m_second = (mgf(cx, cp, h) - 2 * mgf(cx, cp, 0.0) + mgf(cx, cp, -h)) / h ** 2
    print("\nmgf preview (~ST-06)  M(t) = E[e^{tX}]:")
    print(f"  M'(0)  ~ {m_prime:.5f}  ==  E[X]   = {expectation(cx, cp):.5f}")
    print(f"  M''(0) ~ {m_second:.5f}  ==  E[X^2] = {raw_moment(cx, cp, 2):.5f}")


if __name__ == "__main__":
    _demo()
