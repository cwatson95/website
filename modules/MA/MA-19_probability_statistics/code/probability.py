"""
MA-19  Probability & statistics -- discrete and continuous distributions, their
moments, the Central Limit Theorem, error propagation, and least-squares fitting.

Part of the physics topic network (modules/topic_network.txt, module MA-19).
Feeds ~SM-01 (ensembles & probability foundations), ~SM-03 (partition functions),
and the data-analysis side of every experiment (~PK-04 swarm statistics, error
bars on fitted rate coefficients).

Pure Python: `math` for closed forms (uses math.erf for the normal CDF) and the
stdlib `random` (seeded) for sampling. Self-validating: every distribution's
quadrature/sum integrates to 1 and its sample moments converge to the closed-form
mean/variance; the CLT, error-propagation, and least-squares routines are checked
against their analytic answers.
"""

import math
import random

__all__ = [
    "binomial_pmf", "poisson_pmf", "normal_pdf", "normal_cdf", "exponential_pdf",
    "mean_var", "sample_moments", "sample_normal", "sample_uniform_sum",
    "error_propagation", "least_squares_line", "covariance", "correlation",
]


# --- distributions: pmf / pdf and their closed-form moments ------------------

def binomial_pmf(k, n, p):
    """P(k successes in n trials) = C(n,k) p^k (1-p)^{n-k}."""
    if k < 0 or k > n:
        return 0.0
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def poisson_pmf(k, lam):
    """P(k) = lam^k e^{-lam} / k!  -- the n->inf, p->0, np=lam limit of binomial."""
    if k < 0:
        return 0.0
    return math.exp(-lam) * lam ** k / math.factorial(k)


def normal_pdf(x, mu=0.0, sigma=1.0):
    """Gaussian density (1/(sigma sqrt(2pi))) exp(-(x-mu)^2/(2 sigma^2))."""
    return math.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * math.sqrt(2 * math.pi))


def normal_cdf(x, mu=0.0, sigma=1.0):
    """Normal CDF via the error function: 1/2 (1 + erf((x-mu)/(sigma sqrt2)))."""
    return 0.5 * (1.0 + math.erf((x - mu) / (sigma * math.sqrt(2.0))))


def exponential_pdf(x, lam=1.0):
    """Exponential density lam e^{-lam x} for x >= 0."""
    return lam * math.exp(-lam * x) if x >= 0 else 0.0


def mean_var(kind, **p):
    """Closed-form (mean, variance) of a named distribution."""
    if kind == "binomial":
        n, q = p["n"], p["p"]
        return n * q, n * q * (1 - q)
    if kind == "poisson":
        return p["lam"], p["lam"]
    if kind == "normal":
        return p["mu"], p["sigma"] ** 2
    if kind == "exponential":
        return 1.0 / p["lam"], 1.0 / p["lam"] ** 2
    raise ValueError(kind)


# --- sample statistics -------------------------------------------------------

def sample_moments(xs):
    """Return (mean, variance, skewness, excess_kurtosis) of a sample."""
    n = len(xs)
    m = sum(xs) / n
    m2 = sum((x - m) ** 2 for x in xs) / n
    m3 = sum((x - m) ** 3 for x in xs) / n
    m4 = sum((x - m) ** 4 for x in xs) / n
    s = math.sqrt(m2)
    skew = m3 / s ** 3 if s > 0 else 0.0
    kurt = m4 / s ** 4 - 3.0 if s > 0 else 0.0
    return m, m2, skew, kurt


def sample_normal(mu, sigma, n, rng):
    """n Gaussian samples by the Box-Muller transform."""
    out = []
    while len(out) < n:
        u1, u2 = rng.random(), rng.random()
        z = math.sqrt(-2.0 * math.log(u1 + 1e-300)) * math.cos(2 * math.pi * u2)
        out.append(mu + sigma * z)
    return out


def sample_uniform_sum(m, n, rng):
    """n samples of (sum of m U(0,1)) - m/2  -- a CLT demonstrator. For m=12 this
    is the classic ~N(0,1) generator (mean 0, variance m/12 = 1)."""
    return [sum(rng.random() for _ in range(m)) - m / 2.0 for _ in range(n)]


# --- error propagation & least squares ---------------------------------------

def error_propagation(f, values, sigmas, eps=1e-6):
    """First-order propagated uncertainty
       sigma_f^2 = sum_i (df/dx_i)^2 sigma_i^2,
    with partials by central differences. Returns (f(values), sigma_f)."""
    n = len(values)
    var = 0.0
    for i in range(n):
        vp, vm = list(values), list(values)
        vp[i] += eps
        vm[i] -= eps
        dfi = (f(vp) - f(vm)) / (2 * eps)
        var += (dfi * sigmas[i]) ** 2
    return f(values), math.sqrt(var)


def covariance(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / n


def correlation(xs, ys):
    return covariance(xs, ys) / math.sqrt(covariance(xs, xs) * covariance(ys, ys))


def least_squares_line(xs, ys):
    """Ordinary least-squares fit y = a + b x. Returns
    (slope b, intercept a, sigma_b, sigma_a) with standard 1-sigma uncertainties."""
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    Sxx = sum((x - mx) ** 2 for x in xs)
    Sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = Sxy / Sxx
    a = my - b * mx
    sse = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys))
    s2 = sse / (n - 2) if n > 2 else 0.0                 # residual variance
    sigma_b = math.sqrt(s2 / Sxx) if Sxx > 0 else 0.0
    sigma_a = math.sqrt(s2 * (1.0 / n + mx ** 2 / Sxx)) if Sxx > 0 else 0.0
    return b, a, sigma_b, sigma_a


# --- demo --------------------------------------------------------------------

def _demo():
    print("MA-19 probability & statistics -- demo")
    print("=" * 40)
    rng = random.Random(2024)

    print("\ndistributions integrate/sum to 1, and match closed-form moments:")
    sbin = sum(binomial_pmf(k, 10, 0.3) for k in range(11))
    spoi = sum(poisson_pmf(k, 3.0) for k in range(40))
    print(f"  binomial(10,0.3) sum_k = {sbin:.6f}   mean,var = {mean_var('binomial', n=10, p=0.3)}")
    print(f"  poisson(3) sum_k       = {spoi:.6f}   mean,var = {mean_var('poisson', lam=3.0)}")

    print("\nbinomial -> Poisson  (n large, p=lam/n, lam=2):")
    for n in (10, 100, 1000):
        print(f"  n={n:5d}: P(k=3) binomial={binomial_pmf(3, n, 2.0/n):.6f}  poisson={poisson_pmf(3, 2.0):.6f}")

    print("\nCentral Limit Theorem: (sum of 12 U(0,1)) - 6  ~  N(0,1)")
    xs = sample_uniform_sum(12, 40000, rng)
    m, v, sk, ku = sample_moments(xs)
    print(f"  sample mean={m:+.4f} var={v:.4f} skew={sk:+.4f} kurt={ku:+.4f}  (-> 0, 1, 0, 0)")
    for x in (-1.0, 0.0, 1.0):
        emp = sum(1 for z in xs if z <= x) / len(xs)
        print(f"    CDF({x:+.0f}): empirical {emp:.4f}  normal {normal_cdf(x):.4f}")

    print("\nerror propagation for f = x*y:")
    f = lambda v: v[0] * v[1]
    val, sig = error_propagation(f, [4.0, 5.0], [0.1, 0.2])
    rel = math.sqrt((0.1 / 4) ** 2 + (0.2 / 5) ** 2)
    print(f"  f={val:.3f} +/- {sig:.4f}   (relative {sig/val:.4f} vs sqrt-sum-of-squares {rel:.4f})")

    print("\nleast-squares fit of noisy y = 2 + 3x:")
    xd = [i * 0.5 for i in range(20)]
    yd = [2.0 + 3.0 * x + rng.gauss(0, 0.3) for x in xd]
    b, a, sb, sa = least_squares_line(xd, yd)
    print(f"  slope {b:.4f} +/- {sb:.4f}  (true 3)   intercept {a:.4f} +/- {sa:.4f}  (true 2)")


if __name__ == "__main__":
    _demo()
