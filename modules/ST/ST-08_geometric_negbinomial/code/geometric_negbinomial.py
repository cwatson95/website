"""ST-08  Geometric & negative binomial distributions -- discrete waiting times.

Penn State STAT 414, Lesson 11 (Geometric and Negative Binomial Distributions).
Probability network module ST-08 (modules/ST/list_ST.txt).

Where ~ST-07 fixes the number of Bernoulli(p) trials n and counts the successes,
this module fixes the number of successes and counts the *trials*.  The
**geometric** distribution counts the trials X to the FIRST success, with pmf
(1-p)^{x-1} p on x = 1, 2, 3, ...; its mean is 1/p and variance (1-p)/p^2, and it
is the unique discrete distribution with the **memoryless** property
P(X > m+n | X > m) = P(X > n).  The **negative binomial** counts the trials to the
r-th success, pmf C(x-1, r-1)(1-p)^{x-r} p^r on x = r, r+1, ...; mean r/p, variance
r(1-p)/p^2.  The geometric is the r = 1 case, and a sum of r i.i.d. geometrics is
negative binomial(r, p) -- its mgf is the geometric mgf raised to the r.

Pure stdlib `math` only; numpy appears only in the tests (for the convolution
check of the sum relation).  Conventions follow STAT 414 / Hogg, Tanis & Zimmerman:
X counts TRIALS (support starts at 1 for the geometric, at r for the negative
binomial), not failures.
"""

import math

__all__ = [
    "geometric_pmf", "geometric_cdf", "geometric_sf",
    "geometric_mean", "geometric_var", "geometric_mgf",
    "memoryless_check",
    "negbinom_pmf", "negbinom_mean", "negbinom_var", "negbinom_mgf",
]


# --- geometric distribution (STAT 414 L11; trials to first success) ----------

def geometric_pmf(x, p):
    """Geometric pmf  P(X=x) = (1-p)^{x-1} p  on x = 1,2,3,... (trials to 1st success)."""
    if x != int(x) or x < 1:
        return 0.0
    x = int(x)
    return (1.0 - p) ** (x - 1) * p


def geometric_cdf(x, p):
    """Geometric cdf  P(X<=x) = 1 - (1-p)^{floor(x)}  (0 for x<1)."""
    k = math.floor(x)
    if k < 1:
        return 0.0
    return 1.0 - (1.0 - p) ** k


def geometric_sf(x, p):
    """Geometric survival  P(X>x) = (1-p)^{floor(x)}  (the memoryless tail)."""
    k = math.floor(x)
    if k < 0:
        return 1.0
    return (1.0 - p) ** k


def geometric_mean(p):
    """Geometric mean  E[X] = 1/p."""
    return 1.0 / p


def geometric_var(p):
    """Geometric variance  Var(X) = (1-p)/p^2."""
    return (1.0 - p) / (p * p)


def geometric_mgf(t, p):
    """Geometric mgf  M(t) = p e^t / (1 - (1-p) e^t),  valid for t < -ln(1-p)."""
    q = 1.0 - p
    denom = 1.0 - q * math.exp(t)
    if denom <= 0.0:
        raise ValueError("geometric mgf diverges: need t < -ln(1-p)")
    return p * math.exp(t) / denom


def memoryless_check(m, n, p):
    """Memoryless property: returns (P(X>m+n | X>m), P(X>n)); equal for the geometric."""
    conditional = geometric_sf(m + n, p) / geometric_sf(m, p)
    return conditional, geometric_sf(n, p)


# --- negative binomial distribution (STAT 414 L11; trials to r-th success) ----

def negbinom_pmf(x, r, p):
    """Negative binomial pmf  P(X=x) = C(x-1, r-1)(1-p)^{x-r} p^r  on x = r, r+1, ..."""
    r = int(r)
    if x != int(x) or x < r:
        return 0.0
    x = int(x)
    return math.comb(x - 1, r - 1) * (1.0 - p) ** (x - r) * p ** r


def negbinom_mean(r, p):
    """Negative binomial mean  E[X] = r/p  (= r times the geometric mean)."""
    return r / p


def negbinom_var(r, p):
    """Negative binomial variance  Var(X) = r(1-p)/p^2  (= r times the geometric var)."""
    return r * (1.0 - p) / (p * p)


def negbinom_mgf(t, r, p):
    """Negative binomial mgf  M(t) = (p e^t/(1-(1-p)e^t))^r = geometric mgf raised to r."""
    return geometric_mgf(t, p) ** r


# --- demo --------------------------------------------------------------------

def _demo():
    print("ST-08  geometric & negative binomial distributions -- demo")
    print("=" * 58)

    p = 0.25
    print(f"geometric(p={p})  [trials to first success]")
    print(f"  pmf P(X=1..4) = "
          + ", ".join(f"{geometric_pmf(x, p):.4f}" for x in (1, 2, 3, 4)))
    print(f"  mean 1/p          = {geometric_mean(p):.4f}")
    print(f"  variance (1-p)/p^2 = {geometric_var(p):.4f}")
    print(f"  P(X>5) = (1-p)^5  = {geometric_sf(5, p):.4f}  "
          f"(cdf P(X<=5) = {geometric_cdf(5, p):.4f})")

    print("\nmemoryless  P(X>m+n | X>m) = P(X>n):")
    for (m, n) in [(3, 4), (10, 4), (7, 2)]:
        lhs, rhs = memoryless_check(m, n, p)
        print(f"  m={m:>2}, n={n}:  {lhs:.6f}  =  {rhs:.6f}")

    r = 3
    print(f"\nnegative binomial(r={r}, p={p})  [trials to {r}rd success]")
    print(f"  pmf P(X=3..6) = "
          + ", ".join(f"{negbinom_pmf(x, r, p):.4f}" for x in (3, 4, 5, 6)))
    print(f"  mean r/p          = {negbinom_mean(r, p):.4f}  "
          f"(= r x geometric mean {r * geometric_mean(p):.4f})")
    print(f"  variance r(1-p)/p^2 = {negbinom_var(r, p):.4f}  "
          f"(= r x geometric var  {r * geometric_var(p):.4f})")

    print("\ngeometric = negative binomial with r=1:")
    print("  x:        " + "  ".join(f"{x:>7d}" for x in (1, 2, 3, 4)))
    print("  geo pmf:  " + "  ".join(f"{geometric_pmf(x, p):7.4f}" for x in (1, 2, 3, 4)))
    print("  nb(r=1):  " + "  ".join(f"{negbinom_pmf(x, 1, p):7.4f}" for x in (1, 2, 3, 4)))

    print("\nmgf identity  M_nb(t) = M_geo(t)^r  at t=0.1:")
    t = 0.1
    print(f"  M_geo^r = {geometric_mgf(t, p) ** r:.6f},  "
          f"M_nb = {negbinom_mgf(t, r, p):.6f}")


if __name__ == "__main__":
    _demo()
