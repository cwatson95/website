"""ST-09  The Poisson distribution -- pmf, moments, mgf, law of rare events.

Probability Theory trunk, module ST-09 (modules/list_ST.txt), a replica of
Penn State STAT 414, Lesson 12 "The Poisson Distribution".  Pure numpy + stdlib.

A Poisson random variable counts the number of independent events that occur in
a fixed interval of time or space when those events happen at a constant average
rate.  Its pmf is

    P(X = k) = e^{-lam} lam^k / k!,   k = 0, 1, 2, ...

with the single parameter lam = E[X] = Var(X) > 0.  Two derivations anchor the
distribution: (i) the **law of rare events** -- the n -> infinity, p -> 0,
np -> lam limit of the binomial (~ST-07) -- and (ii) the **Poisson process**,
where independent increments over disjoint intervals force exactly this count
law.  The moment-generating function M(t) = exp(lam(e^t - 1)) makes the moments
and the "sum of independent Poissons is Poisson" reproductive property one-line
corollaries.

All functions are scalar (loop for arrays) and self-contained; nothing imports a
sibling ST module.
"""

import math

import numpy as np

__all__ = [
    "poisson_pmf", "poisson_cdf", "poisson_normalization",
    "poisson_mean", "poisson_var", "poisson_std",
    "poisson_skewness", "poisson_excess_kurtosis", "poisson_mode",
    "poisson_mgf", "poisson_pgf", "poisson_factorial_moment",
    "binomial_pmf", "poisson_limit_of_binomial",
    "sum_of_poissons", "poisson_convolution_pmf",
]


# --- the pmf and cdf  (STAT 414 L12.1) ---------------------------------------

def poisson_pmf(k, lam):
    """Poisson pmf  P(X=k) = e^{-lam} lam^k / k!  (log form for stability)."""
    if k < 0 or k != int(k):
        return 0.0
    k = int(k)
    if lam < 0:
        raise ValueError("lam must be >= 0")
    if lam == 0:
        return 1.0 if k == 0 else 0.0
    # exp(k ln lam - lam - ln k!) avoids overflow of lam**k and k! separately
    return math.exp(k * math.log(lam) - lam - math.lgamma(k + 1))


def poisson_cdf(k, lam):
    """Poisson cdf  F(k) = P(X<=k) = sum_{j=0}^{floor(k)} e^{-lam} lam^j / j!."""
    kf = math.floor(k)
    if kf < 0:
        return 0.0
    return sum(poisson_pmf(j, lam) for j in range(kf + 1))


def poisson_normalization(lam, kmax=200):
    """Tail-truncated probability sum  sum_{k=0}^{kmax} P(X=k)  (-> 1)."""
    return sum(poisson_pmf(k, lam) for k in range(kmax + 1))


# --- moments  (STAT 414 L12.2) -----------------------------------------------

def poisson_mean(lam):
    """Mean of the Poisson distribution:  E[X] = lam."""
    return lam


def poisson_var(lam):
    """Variance of the Poisson distribution:  Var(X) = lam  (= mean)."""
    return lam


def poisson_std(lam):
    """Standard deviation:  sigma = sqrt(lam)."""
    return math.sqrt(lam)


def poisson_skewness(lam):
    """Skewness:  mu_3 / sigma^3 = 1 / sqrt(lam)  (always right-skewed)."""
    return 1.0 / math.sqrt(lam)


def poisson_excess_kurtosis(lam):
    """Excess kurtosis:  mu_4/sigma^4 - 3 = 1 / lam."""
    return 1.0 / lam


def poisson_mode(lam):
    """Mode:  floor(lam)  (and also lam-1 when lam is a positive integer)."""
    return math.floor(lam)


# --- generating functions  (STAT 414 L12.2; ~ST-06) -------------------------

def poisson_mgf(t, lam):
    """Moment-generating function  M(t) = E[e^{tX}] = exp(lam (e^t - 1))."""
    return math.exp(lam * (math.exp(t) - 1.0))


def poisson_pgf(s, lam):
    """Probability-generating function  G(s) = E[s^X] = exp(lam (s - 1))."""
    return math.exp(lam * (s - 1.0))


def poisson_factorial_moment(r, lam):
    """r-th factorial moment  E[X(X-1)...(X-r+1)] = lam^r  (from the pgf)."""
    return lam ** r


# --- law of rare events: the binomial limit  (STAT 414 L12.1; ~ST-07) -------

def binomial_pmf(k, n, p):
    """Binomial pmf  P(Y=k) = C(n,k) p^k (1-p)^{n-k}."""
    if k < 0 or k > n or k != int(k):
        return 0.0
    k = int(k)
    return math.comb(n, k) * (p ** k) * ((1.0 - p) ** (n - k))


def poisson_limit_of_binomial(n, p, kmax=None):
    """Max |Binomial(n,p) - Poisson(np)| over k -- the law-of-rare-events gap.

    Holding lam = n*p fixed while n -> infinity (so p = lam/n -> 0) drives this
    gap to zero: the binomial converges to the Poisson(lam) distribution.
    """
    lam = n * p
    if kmax is None:
        kmax = n
    return max(abs(binomial_pmf(k, n, p) - poisson_pmf(k, lam))
               for k in range(kmax + 1))


# --- reproductive (additivity) property  (STAT 414 L12.2; ~ST-06) -----------

def sum_of_poissons(lams):
    """Parameter of a sum of independent Poissons:  lam_total = sum_i lam_i.

    If X_i ~ Poisson(lam_i) independently then sum_i X_i ~ Poisson(sum_i lam_i).
    """
    return float(sum(lams))


def poisson_convolution_pmf(k, lam1, lam2):
    """Convolution pmf  sum_{j=0}^{k} P(X1=j) P(X2=k-j)  for X1+X2.

    Equals poisson_pmf(k, lam1 + lam2) -- the closure of the Poisson family.
    """
    return sum(poisson_pmf(j, lam1) * poisson_pmf(k - j, lam2)
               for j in range(int(k) + 1))


# --- demo --------------------------------------------------------------------

def _demo():
    print("ST-09  the Poisson distribution -- demo")
    print("=" * 52)

    lam = 3.0
    print(f"\nPoisson(lam={lam}) pmf P(X=k):")
    for k in range(8):
        bar = "#" * int(round(60 * poisson_pmf(k, lam)))
        print(f"  k={k}: {poisson_pmf(k, lam):.5f}  {bar}")
    print(f"  sum_{{k=0}}^200 P(X=k) = {poisson_normalization(lam):.10f}  (-> 1)")

    print("\nmean = variance = lam   (the Poisson signature):")
    for lam in (0.5, 3.0, 10.0):
        print(f"  lam={lam:>4}:  E[X]={poisson_mean(lam):.3f}  "
              f"Var(X)={poisson_var(lam):.3f}  sigma={poisson_std(lam):.4f}  "
              f"skew={poisson_skewness(lam):.4f}")

    print("\nmgf M(t)=exp(lam(e^t-1)); moments by differentiation at t=0:")
    lam, h = 4.0, 1e-5
    m1 = (poisson_mgf(h, lam) - poisson_mgf(-h, lam)) / (2 * h)
    m2 = (poisson_mgf(h, lam) - 2 * poisson_mgf(0, lam) + poisson_mgf(-h, lam)) / h ** 2
    print(f"  lam={lam}:  M'(0)={m1:.5f}=E[X]   M''(0)-M'(0)^2={m2 - m1 ** 2:.5f}=Var(X)")

    print("\nlaw of rare events: Binomial(n, lam/n) -> Poisson(lam), lam=2:")
    for n in (5, 20, 100, 1000):
        print(f"  n={n:>5}: max|Binom - Poisson| = {poisson_limit_of_binomial(n, 2.0 / n):.3e}")

    print("\nsum of independent Poissons is Poisson (lam1=2, lam2=5):")
    for k in (3, 7):
        conv = poisson_convolution_pmf(k, 2.0, 5.0)
        direct = poisson_pmf(k, sum_of_poissons([2.0, 5.0]))
        print(f"  k={k}: convolution={conv:.6f}  Poisson(7)={direct:.6f}")


if __name__ == "__main__":
    _demo()
