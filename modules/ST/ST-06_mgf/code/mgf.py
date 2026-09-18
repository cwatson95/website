"""ST-06  Moment-generating functions -- M(t)=E[e^{tX}], moments by differentiation.

Probability-theory trunk, module ST-06 (a replica of Penn State STAT 414,
Lesson 9 "Moment Generating Functions").  Self-contained: numpy + stdlib only,
no sibling-module imports.

The moment-generating function (mgf) of a random variable X is

    M(t) = E[e^{tX}]   =  sum_x e^{tx} p(x)        (discrete)
                       =  integral e^{tx} f(x) dx  (continuous),

defined on the open interval of t about 0 where the sum/integral converges.
Two facts make it a workhorse:

  (1) MOMENTS BY DIFFERENTIATION.  Expanding e^{tX} = sum_k (tX)^k/k! gives
      M(t) = sum_k E[X^k] t^k / k!, so M is the exponential generating function
      of the raw moments and  M^{(k)}(0) = E[X^k].  In particular
      mean  mu     = M'(0),
      var   sigma^2= M''(0) - [M'(0)]^2.
  (2) SUMS OF INDEPENDENTS MULTIPLY.  If X,Y are independent,
      M_{X+Y}(t) = M_X(t) M_Y(t)  (the mgf turns convolution into a product).
  And by the UNIQUENESS theorem an mgf (when it exists near 0) determines the
  distribution: equal mgf  <=>  equal distribution.

The log-mgf  K(t) = ln M(t)  is the cumulant generating function:
K'(0)=mean, K''(0)=variance, and cumulants of a sum add.  This is exactly the
statistical-mechanics partition function ln Z(beta) generating energy cumulants
(~SM-03), and the mgf itself is the (two-sided) Laplace transform of the density
read at s=-t (~MA-10).  Direct mean/variance (the ground truth here) is ~ST-05.
"""

import math

import numpy as np

__all__ = [
    "mgf", "cgf", "mean", "variance",
    "mean_from_mgf", "var_from_mgf", "moment_from_mgf", "cumulant_from_mgf",
    "mgf_of_sum", "convolve_dists",
    "mgf_continuous",
    "bernoulli_mgf", "binomial_mgf", "poisson_mgf", "geometric_mgf",
    "exponential_mgf", "gamma_mgf", "normal_mgf",
    "bernoulli_dist", "binomial_dist", "poisson_dist", "geometric_dist",
]


# --- the moment-generating function (STAT 414 L9.1) --------------------------

def mgf(t, values, probs):
    """Discrete mgf  M(t)=E[e^{tX}]=sum_x e^{tx} p(x)."""
    values = np.asarray(values, dtype=float)
    probs = np.asarray(probs, dtype=float)
    return float(np.sum(probs * np.exp(t * values)))


def cgf(t, values, probs):
    """Cumulant generating function  K(t)=ln M(t)."""
    return math.log(mgf(t, values, probs))


# --- direct moments: the ~ST-05 ground truth --------------------------------

def mean(values, probs):
    """Mean  mu = E[X] = sum_x x p(x)  (the ~ST-05 definition)."""
    values = np.asarray(values, dtype=float)
    probs = np.asarray(probs, dtype=float)
    return float(np.sum(values * probs))


def variance(values, probs):
    """Variance  sigma^2 = E[X^2]-(E[X])^2 = sum_x (x-mu)^2 p(x)  (~ST-05)."""
    values = np.asarray(values, dtype=float)
    probs = np.asarray(probs, dtype=float)
    mu = mean(values, probs)
    return float(np.sum((values - mu) ** 2 * probs))


# --- accurate central finite-difference derivatives at 0 --------------------
# Symmetric stencils; orders 1,2 are O(h^4)-accurate, orders 3,4 are O(h^2).
_STENCILS = {
    1: ([-2, -1, 1, 2], [1.0, -8.0, 8.0, -1.0], 12.0),
    2: ([-2, -1, 0, 1, 2], [-1.0, 16.0, -30.0, 16.0, -1.0], 12.0),
    3: ([-2, -1, 1, 2], [-1.0, 2.0, -2.0, 1.0], 2.0),
    4: ([-2, -1, 0, 1, 2], [1.0, -4.0, 6.0, -4.0, 1.0], 1.0),
}


def _central_derivative(f, k, x0=0.0, h=1e-2):
    """f^{(k)}(x0) by a symmetric finite-difference stencil (k = 1..4)."""
    offsets, coeffs, denom = _STENCILS[k]
    s = sum(c * f(x0 + o * h) for o, c in zip(offsets, coeffs))
    return s / (denom * h ** k)


# --- moments and cumulants by differentiation of the mgf (STAT 414 L9.2) ----

def moment_from_mgf(k, values, probs, h=1e-2):
    """k-th raw moment  E[X^k] = M^{(k)}(0)  by differentiating the mgf."""
    return _central_derivative(lambda t: mgf(t, values, probs), k, 0.0, h)


def mean_from_mgf(values, probs, h=1e-2):
    """Mean from the mgf:  mu = M'(0)."""
    return moment_from_mgf(1, values, probs, h)


def var_from_mgf(values, probs, h=1e-2):
    """Variance from the mgf:  sigma^2 = M''(0) - [M'(0)]^2."""
    m1 = moment_from_mgf(1, values, probs, h)
    m2 = moment_from_mgf(2, values, probs, h)
    return m2 - m1 * m1


def cumulant_from_mgf(k, values, probs, h=1e-2):
    """k-th cumulant  kappa_k = K^{(k)}(0),  K(t)=ln M(t).
    kappa_1=mean, kappa_2=variance; cumulants of a sum of independents add."""
    return _central_derivative(lambda t: cgf(t, values, probs), k, 0.0, h)


# --- sums of independent variables: mgf of a sum is a product (L9.x) --------

def mgf_of_sum(t, dists):
    """M_{X1+...+Xn}(t) = prod_i M_{Xi}(t)  for independent X_i.
    `dists` is a list of (values, probs) pairs."""
    prod = 1.0
    for values, probs in dists:
        prod *= mgf(t, values, probs)
    return prod


def convolve_dists(d1, d2):
    """Distribution of X+Y for independent X,Y given as (values,probs) pairs.
    Returns (values, probs); the mgf of this equals the product of the mgfs."""
    v1, p1 = np.asarray(d1[0], float), np.asarray(d1[1], float)
    v2, p2 = np.asarray(d2[0], float), np.asarray(d2[1], float)
    acc = {}
    for a, pa in zip(v1, p1):
        for b, pb in zip(v2, p2):
            key = round(float(a + b), 9)
            acc[key] = acc.get(key, 0.0) + float(pa * pb)
    vals = sorted(acc)
    return np.array(vals), np.array([acc[v] for v in vals])


# --- continuous mgf by quadrature (the Laplace-transform view, ~MA-10) ------

def _integrate(f, a, b, n=20000):
    """Midpoint-rule integral of f on [a,b]  (the SM-06 quadrature idiom)."""
    dx = (b - a) / n
    return sum(f(a + (i + 0.5) * dx) * dx for i in range(n))


def mgf_continuous(t, pdf, a, b, n=20000):
    """Continuous mgf  M(t)=integral_a^b e^{tx} f(x) dx  by midpoint quadrature.
    For nonnegative X this is the Laplace transform of f read at s=-t (~MA-10)."""
    return _integrate(lambda x: math.exp(t * x) * pdf(x), a, b, n)


# --- closed-form mgfs of the named distributions (STAT 414 L9, L10-L16) -----

def bernoulli_mgf(t, p):
    """Bernoulli(p):  M(t) = (1-p) + p e^t."""
    return (1.0 - p) + p * math.exp(t)


def binomial_mgf(t, n, p):
    """Binomial(n,p):  M(t) = ((1-p) + p e^t)^n  = [bernoulli mgf]^n."""
    return ((1.0 - p) + p * math.exp(t)) ** n


def poisson_mgf(t, lam):
    """Poisson(lambda):  M(t) = exp(lambda (e^t - 1))."""
    return math.exp(lam * (math.exp(t) - 1.0))


def geometric_mgf(t, p):
    """Geometric(p), support {1,2,...}:  M(t) = p e^t / (1-(1-p)e^t),
    valid for t < -ln(1-p)."""
    q = 1.0 - p
    return p * math.exp(t) / (1.0 - q * math.exp(t))


def exponential_mgf(t, lam):
    """Exponential(lambda):  M(t) = lambda/(lambda - t),  t < lambda."""
    return lam / (lam - t)


def gamma_mgf(t, alpha, lam):
    """Gamma(alpha, lambda):  M(t) = (lambda/(lambda - t))^alpha,  t < lambda.
    alpha=1 is the exponential; sum of alpha independent Exp(lambda)."""
    return (lam / (lam - t)) ** alpha


def normal_mgf(t, mu, sigma):
    """Normal(mu, sigma^2):  M(t) = exp(mu t + 1/2 sigma^2 t^2)."""
    return math.exp(mu * t + 0.5 * sigma * sigma * t * t)


# --- distribution builders (values, probs) for the numeric machinery --------

def bernoulli_dist(p):
    """(values, probs) for Bernoulli(p)."""
    return np.array([0.0, 1.0]), np.array([1.0 - p, p])


def binomial_dist(n, p):
    """(values, probs) for Binomial(n, p)."""
    ks = np.arange(n + 1)
    probs = np.array([math.comb(n, int(k)) * p ** int(k) * (1 - p) ** (n - int(k))
                      for k in ks])
    return ks.astype(float), probs


def poisson_dist(lam, kmax=60):
    """(values, probs) for Poisson(lambda), truncated at kmax."""
    ks = np.arange(kmax + 1)
    probs = np.array([math.exp(-lam) * lam ** int(k) / math.factorial(int(k))
                      for k in ks])
    return ks.astype(float), probs


def geometric_dist(p, kmax=2000):
    """(values, probs) for Geometric(p) on {1,...,kmax}."""
    ks = np.arange(1, kmax + 1)
    probs = np.array([(1.0 - p) ** (int(k) - 1) * p for k in ks])
    return ks.astype(float), probs


# --- demo -------------------------------------------------------------------

def _demo():
    print("ST-06 moment-generating functions -- demo")
    print("=" * 52)

    print("M(0) = 1 for every distribution (probabilities sum to 1):")
    for name, d in [("Bernoulli(0.4)", bernoulli_dist(0.4)),
                    ("Binomial(10,0.3)", binomial_dist(10, 0.3)),
                    ("Poisson(2.5)", poisson_dist(2.5))]:
        print(f"  M_{name}(0) = {mgf(0.0, *d):.12f}")

    n, p = 10, 0.3
    d = binomial_dist(n, p)
    print(f"\nBinomial({n},{p}): moments by differentiating the mgf")
    print(f"  mean:  M'(0)            = {mean_from_mgf(*d):.6f}   (np      = {n*p})")
    print(f"  var:   M''(0)-M'(0)^2   = {var_from_mgf(*d):.6f}   (np(1-p) = {n*p*(1-p)})")
    print(f"  direct E[X], Var[X]     = {mean(*d):.6f}, {variance(*d):.6f}  (~ST-05)")

    lam = 2.0
    dp = poisson_dist(lam)
    print(f"\nPoisson({lam}): every cumulant equals lambda")
    print(f"  kappa_1 = {cumulant_from_mgf(1, *dp):.5f},  "
          f"kappa_2 = {cumulant_from_mgf(2, *dp):.5f},  "
          f"kappa_3 = {cumulant_from_mgf(3, *dp):.5f}")
    print(f"  E[X^3]  = M'''(0) = {moment_from_mgf(3, *dp):.4f}  "
          f"(lam^3+3lam^2+lam = {lam**3 + 3*lam**2 + lam})")

    print("\nSum of independents -> product of mgfs (convolution theorem):")
    bern = bernoulli_dist(p)
    conv = convolve_dists(bern, bern)
    t = 0.5
    print(f"  M_X(t)M_Y(t)         = {mgf(t, *bern)*mgf(t, *bern):.8f}")
    print(f"  M_{{X+Y}}(t)           = {mgf(t, *conv):.8f}")
    print(f"  binomial_mgf(t,2,p)  = {binomial_mgf(t, 2, p):.8f}")

    print("\nPoisson additivity in closed form (lambda's add):")
    print(f"  M_2(t) M_3(t) = {poisson_mgf(t,2)*poisson_mgf(t,3):.8f},  "
          f"M_5(t) = {poisson_mgf(t,5):.8f}")

    print("\nContinuous mgf by quadrature (Laplace-transform view, ~MA-10):")
    lam = 1.5
    num = mgf_continuous(0.5, lambda x: lam * math.exp(-lam * x), 0.0, 60.0)
    print(f"  Exp({lam}): integral e^{{0.5 x}} f(x) dx = {num:.6f}   "
          f"(lam/(lam-t) = {exponential_mgf(0.5, lam):.6f})")


if __name__ == "__main__":
    _demo()
