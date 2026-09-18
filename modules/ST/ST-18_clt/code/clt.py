"""ST-18  The central limit theorem & approximations.

Probability Theory trunk, module ST-18 (modules/ST/list_ST.txt), a replica of
Penn State STAT 414, Lesson 27 "The Central Limit Theorem" and Lesson 28
"Approximations for Discrete Distributions".  Pure numpy + stdlib math.

For i.i.d. X_1, X_2, ... with mean mu and finite variance sigma^2, the **central
limit theorem** says the standardized sample mean (equivalently the standardized
sum) converges in distribution to the standard normal:

    (Xbar - mu) / (sigma / sqrt(n))  =  (S_n - n mu) / (sigma sqrt(n))  -->  N(0,1),

where S_n = X_1 + ... + X_n.  Whatever the parent law, the limit shape is the
Gaussian (~ST-12).  The convergence is exhibited here by **convolution**: the pmf
of S_n is the n-fold convolution of the parent pmf, and the maximum gap between
its standardized cdf and Phi shrinks like 1/sqrt(n) (Berry-Esseen).

Two practical corollaries (Lesson 28) are the **normal approximations to the
binomial and the Poisson**, sharpened by the **continuity correction**

    P(X <= k)  ~=  Phi( (k + 0.5 - mu) / sigma ),

valid once np and n(1-p) (resp. lambda) are large.  Self-contained: nothing
imports a sibling ST module.
"""

import math

import numpy as np

__all__ = [
    "SQRT_2PI", "standard_normal_pdf", "standard_normal_cdf",
    "convolve_pmf", "nfold_pmf", "pmf_mean", "pmf_var", "pmf_third_abs_moment",
    "die_pmf", "bernoulli_pmf_array",
    "clt_cdf_max_error", "clt_demo", "kolmogorov_cdf_error", "berry_esseen_bound",
    "binom_pmf", "binom_cdf", "poisson_pmf", "poisson_cdf",
    "normal_approx_binomial", "normal_approx_binomial_interval",
    "de_moivre_laplace_pmf", "normal_approx_poisson",
    "binomial_approx_max_error", "poisson_approx_max_error",
    "binomial_approx_error_table", "normal_approx_applicable",
]

SQRT_2PI = math.sqrt(2.0 * math.pi)         # sqrt(2 pi) = 2.5066... (Gaussian norm)


# --- numerical integrator (midpoint rule, for continuous checks) -------------

def _integrate(f, a, b, n=20000):
    """Midpoint-rule estimate of int_a^b f(x) dx with n panels."""
    dx = (b - a) / n
    return sum(f(a + (i + 0.5) * dx) * dx for i in range(n))


# --- the standard normal limit law (~ST-12) ----------------------------------

def standard_normal_pdf(z):
    """Standard normal density  phi(z) = exp(-z^2/2)/sqrt(2 pi)."""
    z = np.asarray(z, dtype=float)
    return np.exp(-0.5 * z * z) / SQRT_2PI


def standard_normal_cdf(z):
    """Standard normal cdf  Phi(z) = (1/2)[1 + erf(z/sqrt2)] (vectorized)."""
    z = np.asarray(z, dtype=float)
    return 0.5 * (1.0 + np.vectorize(math.erf)(z / math.sqrt(2.0)))


# --- pmf convolution: the distribution of a sum of i.i.d. terms (L27) --------
#     A pmf is a numpy array `probs` with probs[k] = P(X = k), support 0..len-1.

def convolve_pmf(p, q):
    """Pmf of X+Y from independent pmfs p, q:  (p * q)[k] = sum_j p[j] q[k-j]."""
    return np.convolve(np.asarray(p, float), np.asarray(q, float))


def nfold_pmf(probs, n):
    """n-fold convolution: pmf of S_n = X_1 + ... + X_n for i.i.d. X_i ~ probs."""
    probs = np.asarray(probs, float)
    out = np.array([1.0])                    # pmf of the empty sum S_0 = 0
    for _ in range(n):
        out = np.convolve(out, probs)
    return out


def pmf_mean(probs):
    """Mean  mu = sum_k k * P(X=k)  of a pmf on the integers 0..len-1."""
    probs = np.asarray(probs, float)
    k = np.arange(len(probs))
    return float(np.sum(k * probs))


def pmf_var(probs):
    """Variance  sigma^2 = E[X^2] - (E[X])^2  of a pmf on 0..len-1."""
    probs = np.asarray(probs, float)
    k = np.arange(len(probs))
    m = float(np.sum(k * probs))
    return float(np.sum(k * k * probs)) - m * m


def pmf_third_abs_moment(probs):
    """Third absolute central moment  rho = E|X - mu|^3  (Berry-Esseen input)."""
    probs = np.asarray(probs, float)
    k = np.arange(len(probs))
    m = float(np.sum(k * probs))
    return float(np.sum(np.abs(k - m) ** 3 * probs))


def die_pmf():
    """Pmf of a fair six-sided die on support {1,...,6}: probs[1..6] = 1/6."""
    p = np.zeros(7)
    p[1:7] = 1.0 / 6.0
    return p


def bernoulli_pmf_array(p):
    """Pmf array of a Bernoulli(p): [1-p, p] on support {0, 1}."""
    return np.array([1.0 - p, p])


# --- the CLT in action: standardized cdf vs Phi (L27) ------------------------

def clt_cdf_max_error(probs, n):
    """Max |F_{S_n}(k) - Phi((k+0.5-mu_n)/sigma_n)| over the lattice (cont. corr.).

    Convolves n copies of `probs`, standardizes the exact cdf of the sum, and
    returns its largest gap from the standard-normal cdf.  Shrinks ~ 1/sqrt(n):
    the central limit theorem made quantitative."""
    conv = nfold_pmf(probs, n)
    mu_n = pmf_mean(conv)
    sd_n = math.sqrt(pmf_var(conv))
    cdf = np.cumsum(conv)
    k = np.arange(len(conv))
    approx = standard_normal_cdf((k + 0.5 - mu_n) / sd_n)
    return float(np.max(np.abs(cdf - approx)))


def clt_demo(probs, ns=(1, 2, 4, 8, 16, 32, 64)):
    """Table [(n, max cdf error)] showing the CLT gap shrink toward zero."""
    return [(n, clt_cdf_max_error(probs, n)) for n in ns]


def kolmogorov_cdf_error(probs, n):
    """True sup_x |F_{S_n}(x) - Phi((x-mu_n)/sigma_n)| (no continuity correction).

    The Kolmogorov distance bounded by the Berry-Esseen theorem.  For a step
    cdf the sup over each flat segment is attained at a lattice point, so we
    check both one-sided limits F(k^-)=F(k-1) and F(k^+)=F(k) there."""
    conv = nfold_pmf(probs, n)
    mu_n = pmf_mean(conv)
    sd_n = math.sqrt(pmf_var(conv))
    cdf = np.cumsum(conv)
    cdf_left = cdf - conv                      # F(k^-) = F(k-1)
    k = np.arange(len(conv))
    phi = standard_normal_cdf((k - mu_n) / sd_n)
    return float(np.max(np.maximum(np.abs(cdf - phi), np.abs(cdf_left - phi))))


def berry_esseen_bound(probs, n, C=0.7655):
    """Berry-Esseen bound  C * rho / (sigma^3 sqrt(n))  on the Kolmogorov error.

    rho = E|X-mu|^3, sigma = SD of the parent.  C = 0.7655 (van Beek) is a valid
    universal constant; the best known is ~0.469 (Shevtsova)."""
    sigma = math.sqrt(pmf_var(probs))
    rho = pmf_third_abs_moment(probs)
    return C * rho / (sigma ** 3 * math.sqrt(n))


# --- exact binomial and Poisson (the laws we approximate, ~ST-07, ~ST-09) ----

def binom_pmf(k, n, p):
    """Binomial pmf  P(X=k) = C(n,k) p^k (1-p)^{n-k}  (log form, stable)."""
    if k < 0 or k > n or k != int(k):
        return 0.0
    k = int(k)
    if p <= 0.0:
        return 1.0 if k == 0 else 0.0
    if p >= 1.0:
        return 1.0 if k == n else 0.0
    log_pmf = (math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
               + k * math.log(p) + (n - k) * math.log1p(-p))
    return math.exp(log_pmf)


def binom_cdf(k, n, p):
    """Binomial cdf  F(k) = sum_{j=0}^{floor(k)} C(n,j) p^j (1-p)^{n-j}."""
    kf = math.floor(k)
    if kf < 0:
        return 0.0
    if kf >= n:
        return 1.0
    return sum(binom_pmf(j, n, p) for j in range(kf + 1))


def poisson_pmf(k, lam):
    """Poisson pmf  P(X=k) = e^{-lam} lam^k / k!  (log form, stable)."""
    if k < 0 or k != int(k):
        return 0.0
    k = int(k)
    if lam == 0:
        return 1.0 if k == 0 else 0.0
    return math.exp(k * math.log(lam) - lam - math.lgamma(k + 1))


def poisson_cdf(k, lam):
    """Poisson cdf  F(k) = sum_{j=0}^{floor(k)} e^{-lam} lam^j / j!."""
    kf = math.floor(k)
    if kf < 0:
        return 0.0
    return sum(poisson_pmf(j, lam) for j in range(kf + 1))


# --- normal approximation to the binomial (L28) ------------------------------

def normal_approx_binomial(k, n, p, continuity=True):
    """Normal approx to P(X<=k) for X~Bin(n,p):  Phi((k+0.5c-np)/sqrt(npq)).

    c = 1 with the continuity correction (default), c = 0 without."""
    mu = n * p
    sigma = math.sqrt(n * p * (1.0 - p))
    c = 0.5 if continuity else 0.0
    return float(standard_normal_cdf((k + c - mu) / sigma))


def normal_approx_binomial_interval(a, b, n, p, continuity=True):
    """Normal approx to P(a<=X<=b) for X~Bin(n,p) with continuity correction:
        Phi((b+0.5-mu)/sigma) - Phi((a-0.5-mu)/sigma),  mu=np, sigma=sqrt(npq)."""
    mu = n * p
    sigma = math.sqrt(n * p * (1.0 - p))
    c = 0.5 if continuity else 0.0
    hi = standard_normal_cdf((b + c - mu) / sigma)
    lo = standard_normal_cdf((a - c - mu) / sigma)
    return float(hi - lo)


def de_moivre_laplace_pmf(k, n, p):
    """de Moivre-Laplace local limit:  P(X=k) ~= (1/sigma) phi((k-np)/sigma)."""
    mu = n * p
    sigma = math.sqrt(n * p * (1.0 - p))
    return float(standard_normal_pdf((k - mu) / sigma)) / sigma


# --- normal approximation to the Poisson (L28) -------------------------------

def normal_approx_poisson(k, lam, continuity=True):
    """Normal approx to P(X<=k) for X~Poisson(lam):  Phi((k+0.5c-lam)/sqrt(lam))."""
    sigma = math.sqrt(lam)
    c = 0.5 if continuity else 0.0
    return float(standard_normal_cdf((k + c - lam) / sigma))


# --- tabulating the approximation error (L28) --------------------------------

def binomial_approx_max_error(n, p, continuity=True):
    """Max_k |Binom cdf F(k) - normal approx| over k=0..n (Kolmogorov gap)."""
    mu = n * p
    sigma = math.sqrt(n * p * (1.0 - p))
    c = 0.5 if continuity else 0.0
    worst = 0.0
    F = 0.0
    for k in range(n + 1):
        F += binom_pmf(k, n, p)
        approx = float(standard_normal_cdf((k + c - mu) / sigma))
        worst = max(worst, abs(F - approx))
    return worst


def poisson_approx_max_error(lam, continuity=True, kmax=None):
    """Max_k |Poisson cdf F(k) - normal approx| over k=0..kmax (Kolmogorov gap)."""
    if kmax is None:
        kmax = int(lam + 12.0 * math.sqrt(lam) + 10)
    sigma = math.sqrt(lam)
    c = 0.5 if continuity else 0.0
    worst = 0.0
    F = 0.0
    for k in range(kmax + 1):
        F += poisson_pmf(k, lam)
        approx = float(standard_normal_cdf((k + c - lam) / sigma))
        worst = max(worst, abs(F - approx))
    return worst


def binomial_approx_error_table(p, ns=(10, 20, 40, 80, 160), continuity=True):
    """Table [(n, max binomial-cdf approx error)] at fixed p: error -> 0 as n^-1/2."""
    return [(n, binomial_approx_max_error(n, p, continuity)) for n in ns]


def normal_approx_applicable(n, p, thresh=5.0):
    """Rule of thumb: the normal approx is good when np >= thresh AND n(1-p) >= thresh."""
    return (n * p >= thresh) and (n * (1.0 - p) >= thresh)


# --- demo --------------------------------------------------------------------

def _demo():
    print("ST-18  The central limit theorem & approximations -- demo")
    print("=" * 60)

    print("\nStandard normal cdf Phi via erf (the limit law):")
    for z in (-2.0, -1.0, 0.0, 1.0, 1.96):
        print(f"  Phi({z:+.2f}) = {float(standard_normal_cdf(z)):.6f}")
    integ = _integrate(lambda t: float(standard_normal_pdf(t)), -40.0, 1.0, 80000)
    print(f"  int_-inf^1 phi = {integ:.6f}  (== Phi(1) = {float(standard_normal_cdf(1.0)):.6f})")

    print("\nCLT by convolution -- fair die S_n = X_1+...+X_n,")
    print("max |standardized cdf - Phi| shrinks ~ 1/sqrt(n):")
    die = die_pmf()
    for n, err in clt_demo(die):
        print(f"  n={n:>3}:  max cdf error = {err:.5f}   error*sqrt(n) = {err*math.sqrt(n):.4f}")

    print("\nBerry-Esseen: Kolmogorov error <= C rho/(sigma^3 sqrt n) (die):")
    for n in (1, 2, 4, 8):
        print(f"  n={n}: actual {kolmogorov_cdf_error(die, n):.4f} <= bound "
              f"{berry_esseen_bound(die, n):.4f}")

    print("\nNormal approximation to Bin(n=20, p=0.5), P(X<=k):")
    print("   k   exact      no-corr.   cont.corr.")
    for k in (7, 10, 13):
        ex = binom_cdf(k, 20, 0.5)
        nc = normal_approx_binomial(k, 20, 0.5, continuity=False)
        cc = normal_approx_binomial(k, 20, 0.5, continuity=True)
        print(f"  {k:>2}  {ex:.6f}   {nc:.6f}   {cc:.6f}")

    print("\n  P(8 <= X <= 12) for Bin(20,0.5):")
    ex = binom_cdf(12, 20, 0.5) - binom_cdf(7, 20, 0.5)
    print(f"    exact = {ex:.6f},  cont.corr. = "
          f"{normal_approx_binomial_interval(8, 12, 20, 0.5):.6f}")

    print("\nNormal approx to the binomial: max cdf error vs n (p=0.5):")
    for n, err in binomial_approx_error_table(0.5):
        print(f"  n={n:>3}: cont.corr. error = {err:.5f}   "
              f"(no corr. = {binomial_approx_max_error(n, 0.5, False):.5f})")

    print("\nNormal approximation to Poisson(lam), P(X<=k), continuity-corrected:")
    for lam in (4.0, 16.0, 64.0):
        err = poisson_approx_max_error(lam, True)
        print(f"  lam={lam:>5}: max cdf error = {err:.5f}  (sigma=sqrt(lam)={math.sqrt(lam):.3f})")

    print("\nRule of thumb (np>=5 and n(1-p)>=5):")
    for n, p in ((20, 0.5), (40, 0.1), (8, 0.5)):
        print(f"  Bin({n},{p}): np={n*p:.1f}, n(1-p)={n*(1-p):.1f}  -> "
              f"applicable = {normal_approx_applicable(n, p)}")


if __name__ == "__main__":
    _demo()
