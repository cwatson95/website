"""ST-07  The binomial distribution -- Bernoulli trials, pmf, mean np, var np(1-p), mgf.

Penn State STAT 414, Lesson 10 "The Binomial Distribution".  Builds on ~ST-02
(counting: the binomial coefficient C(n,k)) and ~ST-05/~ST-06 (expectation,
variance, and the moment-generating function M(t)=E[e^{tX}]).  Self-contained:
pure numpy + stdlib math, no sibling-module imports.

A Bernoulli(p) trial is a single success/failure experiment with P(success)=p.
The number X of successes in n independent, identical Bernoulli(p) trials is the
binomial random variable Bin(n,p), with probability mass function
    P(X=k) = C(n,k) p^k (1-p)^{n-k},   k = 0,1,...,n.
The binomial theorem makes the pmf sum to 1; the mean is np, the variance
np(1-p), and the mgf (q+p e^t)^n with q=1-p.  Two famous limits sit just
downstream: the Poisson limit (n->inf with np=lambda fixed; ~ST-09) and the
normal / de Moivre-Laplace limit (~ST-18), both demonstrated here against
self-contained reference helpers.
"""

import math

import numpy as np

__all__ = [
    "bernoulli_pmf", "bernoulli_mean", "bernoulli_var",
    "binom_pmf", "binom_cdf", "binom_mean", "binom_var", "binom_std",
    "binom_mgf", "binom_pgf", "binom_mode", "binom_skewness",
    "sum_two_binomials_pmf",
]


# --- Bernoulli trial: the n=1 building block (STAT 414, L10) ------------------

def bernoulli_pmf(k, p):
    """Bernoulli(p) pmf  P(X=k) = p^k (1-p)^{1-k},  k in {0,1}  (= Bin(1,p))."""
    if k not in (0, 1):
        return 0.0
    return p ** k * (1.0 - p) ** (1 - k)


def bernoulli_mean(p):
    """Mean of a Bernoulli(p) trial:  E[X] = p."""
    return p


def bernoulli_var(p):
    """Variance of a Bernoulli(p) trial:  Var(X) = p(1-p)."""
    return p * (1.0 - p)


# --- binomial pmf / cdf (STAT 414, L10) --------------------------------------

def binom_pmf(k, n, p):
    """Binomial pmf  P(X=k) = C(n,k) p^k (1-p)^{n-k}  (0 outside 0<=k<=n)."""
    if k < 0 or k > n:
        return 0.0
    q = 1.0 - p
    return math.comb(n, k) * p ** k * q ** (n - k)


def binom_cdf(k, n, p):
    """Binomial cdf  F(k) = P(X<=k) = sum_{j=0}^{k} C(n,j) p^j (1-p)^{n-j}."""
    if k < 0:
        return 0.0
    kk = min(int(math.floor(k)), n)
    return sum(binom_pmf(j, n, p) for j in range(0, kk + 1))


# --- moments in closed form (STAT 414, L10) ----------------------------------

def binom_mean(n, p):
    """Binomial mean  E[X] = n p  (= sum of n Bernoulli means)."""
    return n * p


def binom_var(n, p):
    """Binomial variance  Var(X) = n p (1-p)  (= sum of n Bernoulli variances)."""
    return n * p * (1.0 - p)


def binom_std(n, p):
    """Binomial standard deviation  sigma = sqrt(n p (1-p))."""
    return math.sqrt(binom_var(n, p))


def binom_skewness(n, p):
    """Binomial skewness  (1-2p)/sqrt(n p (1-p))  (0 at p=1/2, the symmetric case)."""
    return (1.0 - 2.0 * p) / math.sqrt(n * p * (1.0 - p))


# --- generating functions (STAT 414, L9-L10) ---------------------------------

def binom_mgf(t, n, p):
    """Binomial mgf  M(t) = E[e^{tX}] = (q + p e^t)^n,  q = 1-p."""
    q = 1.0 - p
    return (q + p * math.exp(t)) ** n


def binom_pgf(s, n, p):
    """Binomial probability generating function  G(s) = E[s^X] = (q + p s)^n."""
    q = 1.0 - p
    return (q + p * s) ** n


# --- mode (STAT 414, L10) ----------------------------------------------------

def binom_mode(n, p):
    """Binomial mode  floor((n+1)p)  (largest of the (up to two) most likely k)."""
    if p >= 1.0:
        return n
    if p <= 0.0:
        return 0
    return min(int(math.floor((n + 1) * p)), n)


# --- additivity: sum of independent binomials with common p (STAT 414, L10) --

def sum_two_binomials_pmf(k, n1, n2, p):
    """pmf of X1+X2 for independent Bin(n1,p), Bin(n2,p): the convolution
    sum_j C(n1,j)C(n2,k-j) p^k q^{n1+n2-k} = Bin(n1+n2,p) (Vandermonde)."""
    return sum(binom_pmf(j, n1, p) * binom_pmf(k - j, n2, p)
               for j in range(0, k + 1))


# --- numerical helpers (for continuous / limit checks) -----------------------

def _deriv1(f, x, h=1e-5):
    """Central first derivative  f'(x) ~ (f(x+h)-f(x-h))/(2h)."""
    return (f(x + h) - f(x - h)) / (2.0 * h)


def _deriv2(f, x, h=1e-3):
    """Central second derivative, 5-point O(h^4) stencil (accurate enough that
    Var = M''(0) - M'(0)^2 survives the large-mean cancellation):
        f''(x) ~ [-f(x-2h)+16f(x-h)-30f(x)+16f(x+h)-f(x+2h)] / (12 h^2)."""
    return (-f(x - 2 * h) + 16.0 * f(x - h) - 30.0 * f(x)
            + 16.0 * f(x + h) - f(x + 2 * h)) / (12.0 * h * h)


def _integrate(f, a, b, n=20000):
    """Midpoint-rule integral of f on [a,b] (continuous normalization checks)."""
    dx = (b - a) / n
    return sum(f(a + (i + 0.5) * dx) * dx for i in range(n))


def _poisson_pmf(k, lam):
    """Reference Poisson(lambda) pmf  e^{-lam} lam^k / k!  (for the ~ST-09 limit)."""
    return math.exp(-lam) * lam ** k / math.factorial(k)


def _normal_pdf(x, mu, sigma):
    """Reference normal pdf (for the de Moivre-Laplace / ~ST-18 limit check)."""
    return math.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * math.sqrt(2.0 * math.pi))


# --- demo --------------------------------------------------------------------

def _demo():
    print("ST-07  the binomial distribution -- demo")
    print("=" * 52)

    n, p = 10, 0.35
    q = 1.0 - p
    print(f"Bin(n={n}, p={p})   q = 1-p = {q}")
    ks = np.arange(0, n + 1)
    pmf = np.array([binom_pmf(int(k), n, p) for k in ks])
    print("  k    P(X=k)")
    for k, pk in zip(ks, pmf):
        bar = "#" * int(round(60 * pk))
        print(f"  {k:>2}  {pk:.5f}  {bar}")
    print(f"  sum of pmf            = {pmf.sum():.10f}   (binomial theorem -> 1)")
    print(f"  mean  sum k P(k)      = {(ks * pmf).sum():.6f}   np = {binom_mean(n, p)}")
    var_emp = (((ks - binom_mean(n, p)) ** 2) * pmf).sum()
    print(f"  var   sum (k-np)^2 P  = {var_emp:.6f}   np(1-p) = {binom_var(n, p)}")
    print(f"  mode  floor((n+1)p)   = {binom_mode(n, p)}   argmax k = {int(ks[np.argmax(pmf)])}")

    print("\nmgf  M(t) = (q + p e^t)^n  ->  moments by differentiation at t=0:")
    M = lambda t: binom_mgf(t, n, p)
    print(f"  M(0)        = {M(0.0):.6f}   (always 1)")
    print(f"  M'(0)       = {_deriv1(M, 0.0):.6f}   E[X]   = np      = {binom_mean(n, p)}")
    m2 = _deriv2(M, 0.0)
    print(f"  M''(0)      = {m2:.6f}   E[X^2] = npq+(np)^2 = {binom_var(n, p) + binom_mean(n, p) ** 2}")
    print(f"  M''(0)-M'(0)^2 = {m2 - _deriv1(M, 0.0) ** 2:.6f}   Var = np(1-p) = {binom_var(n, p)}")

    print("\nadditivity: Bin(n1,p) + Bin(n2,p) = Bin(n1+n2,p)  (common p):")
    n1, n2 = 4, 6
    pmf1 = np.array([binom_pmf(k, n1, p) for k in range(n1 + 1)])
    pmf2 = np.array([binom_pmf(k, n2, p) for k in range(n2 + 1)])
    conv = np.convolve(pmf1, pmf2)                 # pmf of the sum
    direct = np.array([binom_pmf(k, n1 + n2, p) for k in range(n1 + n2 + 1)])
    print(f"  max |conv - Bin(n1+n2,p)| = {np.max(np.abs(conv - direct)):.2e}")

    print("\nPoisson limit (n->inf, p=lam/n, lam fixed)  -> ~ST-09:")
    lam = 2.5
    for nn in (25, 250, 2500):
        pp = lam / nn
        err = max(abs(binom_pmf(k, nn, pp) - _poisson_pmf(k, lam)) for k in range(11))
        print(f"  n={nn:>5}, p={pp:.4f}:  max_k |Bin - Poisson(2.5)| = {err:.2e}")

    print("\nnormal (de Moivre-Laplace) approximation near the peak  -> ~ST-18:")
    nN, pN = 100, 0.5
    mu, sig = binom_mean(nN, pN), binom_std(nN, pN)
    for k in (45, 50, 55):
        print(f"  k={k}:  Bin = {binom_pmf(k, nN, pN):.5f}   "
              f"N(np, npq) = {_normal_pdf(k, mu, sig):.5f}")


if __name__ == "__main__":
    _demo()
