"""ST-17  The MGF technique & normal sampling distributions.

Probability theory trunk, module ST-17 (Penn State STAT 414, Lessons 25-26;
see modules/ST/list_ST.txt).  Self-contained: pure numpy + Python stdlib (math).
No sibling imports.

Two ideas, one engine.

(A) The **moment-generating-function technique** (L25).  For independent
    X_1, ..., X_n the mgf of the sum is the *product* of the mgfs,
        M_{sum X_i}(t) = prod_i M_{X_i}(t),
    and (uniqueness, ~ST-06) an mgf that exists near 0 names exactly one
    distribution.  So to find the law of a sum, multiply mgfs and recognize the
    answer.  Three closure facts drop out:
      * sum of independent normals is normal:  mu's add, sigma^2's add;
      * sum of independent gammas of common scale theta: shapes alpha add;
      * sum of independent chi-squares: degrees of freedom add
        (and Z^2 ~ chi^2_1, so sum_{i=1}^n Z_i^2 ~ chi^2_n).

(B) **Random functions of a normal sample** (L26).  From X_1,...,X_n iid
    N(mu, sigma^2):
      * the sample mean  Xbar = (1/n) sum X_i ~ N(mu, sigma^2/n);
      * (n-1) S^2 / sigma^2 ~ chi^2_{n-1}, with Xbar and S^2 independent;
      * Student's t:  T = Z / sqrt(V/r),  Z~N(0,1), V~chi^2_r independent
        -- and (Xbar-mu)/(S/sqrt n) ~ t_{n-1};  t_r -> N(0,1) as r -> inf;
      * Snedecor's F:  F = (U/r1)/(V/r2),  U~chi^2_{r1}, V~chi^2_{r2} independent
        -- the ratio of two scaled chi-squares; and T^2 ~ F_{1,r}.

The closed-form t and F densities are built from the gamma / Beta functions.
"""

import math

import numpy as np

__all__ = [
    # mgfs (recognized closed forms)
    "normal_mgf", "gamma_mgf", "chi2_mgf",
    # densities used as targets
    "standard_normal_pdf", "normal_pdf", "gamma_pdf", "chi2_pdf",
    "beta_function",
    # (A) the mgf technique
    "product_of_normal_mgfs", "sum_of_normals_via_mgf",
    "mgf_of_linear_combination_normals", "linear_combination_of_normals",
    "product_of_gamma_mgfs", "sum_of_gammas_via_mgf",
    "product_of_chi2_mgfs", "sum_of_chisquares",
    "square_of_standard_normal_pdf",
    # (B) sampling distributions
    "sampling_dist_of_mean", "standardized_mean_mgf", "sample_variance_chi2_df",
    "students_t_pdf", "students_t_mean", "students_t_var",
    "f_pdf", "f_mean", "f_var", "t_squared_pdf",
]


# --- numerical integrator (midpoint rule) for the continuous checks ----------

def _integrate(f, a, b, n=20000):
    """Midpoint-rule estimate of int_a^b f(x) dx."""
    dx = (b - a) / n
    return sum(f(a + (i + 0.5) * dx) * dx for i in range(n))


# --- recognized closed-form mgfs (~ST-06, ~ST-12, ~ST-11) --------------------

def normal_mgf(t, mu, sigma):
    """Normal mgf M(t) = exp(mu t + sigma^2 t^2 / 2)  (~ST-12)."""
    return math.exp(mu * t + 0.5 * sigma * sigma * t * t)


def gamma_mgf(t, alpha, theta):
    """Gamma mgf M(t) = (1 - theta t)^{-alpha} for t < 1/theta  (~ST-11)."""
    return (1.0 - theta * t) ** (-alpha)


def chi2_mgf(t, r):
    """Chi-square mgf M(t) = (1 - 2t)^{-r/2} for t < 1/2  (gamma with theta=2)."""
    return (1.0 - 2.0 * t) ** (-r / 2.0)


# --- densities used as recognition targets -----------------------------------

def standard_normal_pdf(z):
    """Standard normal density phi(z) = exp(-z^2/2)/sqrt(2 pi)."""
    return math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)


def normal_pdf(x, mu, sigma):
    """Normal(mu, sigma^2) density (~ST-12)."""
    return math.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * math.sqrt(2.0 * math.pi))


def gamma_pdf(x, alpha, theta):
    """Gamma(shape alpha, scale theta) density x^{a-1}e^{-x/theta}/(Gamma(a)theta^a) (~ST-11)."""
    if x <= 0.0:
        return 0.0
    return (x ** (alpha - 1.0) * math.exp(-x / theta)
            / (math.gamma(alpha) * theta ** alpha))


def chi2_pdf(x, r):
    """Chi-square density with r d.f. = gamma_pdf(x, r/2, 2)  (~ST-11)."""
    return gamma_pdf(x, r / 2.0, 2.0)


def beta_function(a, b):
    """Beta function B(a,b) = Gamma(a)Gamma(b)/Gamma(a+b) (via lgamma)  (~MA-12)."""
    return math.exp(math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b))


# === (A) The MGF technique (STAT 414 L25) ====================================
# Independent => the mgf of the sum is the PRODUCT of the mgfs; uniqueness then
# names the distribution.

def product_of_normal_mgfs(t, means, variances):
    """prod_i M_{X_i}(t) for independent normals -- the mgf of their sum (L25)."""
    out = 1.0
    for mu, var in zip(means, variances):
        out *= normal_mgf(t, mu, math.sqrt(var))
    return out


def sum_of_normals_via_mgf(means, variances):
    """Sum of independent normals is normal: returns (sum mu_i, sum sigma_i^2),
    because prod exp(mu_i t + sigma_i^2 t^2/2) = exp((sum mu)t + (sum var)t^2/2)."""
    return float(sum(means)), float(sum(variances))


def mgf_of_linear_combination_normals(t, coeffs, means, variances):
    """mgf of sum_i a_i X_i for independent normals: prod_i M_{X_i}(a_i t) (L25)."""
    out = 1.0
    for a, mu, var in zip(coeffs, means, variances):
        out *= normal_mgf(a * t, mu, math.sqrt(var))
    return out


def linear_combination_of_normals(coeffs, means, variances):
    """sum_i a_i X_i ~ N(sum a_i mu_i, sum a_i^2 sigma_i^2): returns those params."""
    mu = sum(a * m for a, m in zip(coeffs, means))
    var = sum(a * a * v for a, v in zip(coeffs, variances))
    return float(mu), float(var)


def product_of_gamma_mgfs(t, alphas, theta):
    """prod_i (1 - theta t)^{-alpha_i} -- the mgf of a sum of common-scale gammas."""
    out = 1.0
    for a in alphas:
        out *= gamma_mgf(t, a, theta)
    return out


def sum_of_gammas_via_mgf(alphas, theta):
    """Sum of independent Gamma(alpha_i, theta) (common scale) is
    Gamma(sum alpha_i, theta): returns (sum alpha_i, theta).  Shapes add."""
    return float(sum(alphas)), float(theta)


def product_of_chi2_mgfs(t, dfs):
    """prod_i (1 - 2t)^{-r_i/2} -- the mgf of a sum of independent chi-squares."""
    out = 1.0
    for r in dfs:
        out *= chi2_mgf(t, r)
    return out


def sum_of_chisquares(dfs):
    """Sum of independent chi^2_{r_i} is chi^2_{sum r_i}: returns sum r_i.
    Degrees of freedom add (chi^2 is gamma with theta=2, so this is the gamma rule)."""
    return float(sum(dfs))


def square_of_standard_normal_pdf(x):
    """Density of W = Z^2 for Z ~ N(0,1):  phi(sqrt x)/sqrt x  ==  chi2_pdf(x, 1).
    The seed of sampling theory: sum of n squared standard normals is chi^2_n."""
    if x <= 0.0:
        return 0.0
    return standard_normal_pdf(math.sqrt(x)) / math.sqrt(x)


# === (B) Random functions of a normal sample (STAT 414 L26) ==================

def sampling_dist_of_mean(mu, sigma2, n):
    """Xbar = (1/n) sum X_i for X_i iid N(mu, sigma2): Xbar ~ N(mu, sigma2/n).
    Returns (mean, variance) = (mu, sigma2/n).  Linear combination, a_i = 1/n."""
    return float(mu), float(sigma2) / n


def standardized_mean_mgf(t, mu, sigma2, n):
    """mgf of Z = (Xbar - mu)/(sigma/sqrt n).  Equals exp(t^2/2) (standard normal)
    for every mu, sigma2, n -- the standardized sample mean is exactly N(0,1)."""
    mean, var = sampling_dist_of_mean(mu, sigma2, n)
    sigma_xbar = math.sqrt(var)
    a = 1.0 / sigma_xbar          # Z = a*Xbar + b
    b = -mu / sigma_xbar
    return math.exp(b * t) * normal_mgf(a * t, mean, sigma_xbar)


def sample_variance_chi2_df(n):
    """Degrees of freedom of (n-1)S^2/sigma^2 ~ chi^2_{n-1}: returns n-1.
    One d.f. is lost estimating mu by Xbar; Xbar and S^2 are independent."""
    return n - 1


# --- Student's t  (Z over sqrt(V/r)) -----------------------------------------

def students_t_pdf(t, r):
    """Student's t density with r d.f.:
        f(t) = Gamma((r+1)/2) / (sqrt(r pi) Gamma(r/2)) * (1 + t^2/r)^{-(r+1)/2}
             = 1 / (sqrt(r) B(1/2, r/2)) * (1 + t^2/r)^{-(r+1)/2}."""
    log_c = math.lgamma((r + 1.0) / 2.0) - math.lgamma(r / 2.0) \
        - 0.5 * math.log(r * math.pi)
    return math.exp(log_c) * (1.0 + t * t / r) ** (-(r + 1.0) / 2.0)


def students_t_mean(r):
    """Mean of t_r: 0 for r > 1 (symmetry), undefined otherwise."""
    return 0.0 if r > 1 else float("nan")


def students_t_var(r):
    """Variance of t_r: r/(r-2) for r > 2; infinite for 1 < r <= 2.
    Heavier-tailed than the normal, but -> 1 as r -> inf."""
    if r > 2:
        return r / (r - 2.0)
    return float("inf")


# --- Snedecor's F  ((U/r1) over (V/r2)) --------------------------------------

def f_pdf(x, r1, r2):
    """Snedecor's F density with (r1, r2) d.f., via the Beta/gamma function:
        f(x) = (r1/r2)^{r1/2} / B(r1/2, r2/2)
               * x^{r1/2 - 1} * (1 + (r1/r2) x)^{-(r1+r2)/2},   x > 0."""
    if x <= 0.0:
        return 0.0
    log_c = (r1 / 2.0) * math.log(r1 / r2) \
        - (math.lgamma(r1 / 2.0) + math.lgamma(r2 / 2.0) - math.lgamma((r1 + r2) / 2.0))
    return (math.exp(log_c) * x ** (r1 / 2.0 - 1.0)
            * (1.0 + (r1 / r2) * x) ** (-(r1 + r2) / 2.0))


def f_mean(r2):
    """Mean of F_{r1,r2}: r2/(r2-2) for r2 > 2 (independent of r1)."""
    if r2 > 2:
        return r2 / (r2 - 2.0)
    return float("inf")


def f_var(r1, r2):
    """Variance of F_{r1,r2}: 2 r2^2 (r1+r2-2) / (r1 (r2-2)^2 (r2-4)) for r2 > 4."""
    if r2 > 4:
        return (2.0 * r2 * r2 * (r1 + r2 - 2.0)
                / (r1 * (r2 - 2.0) ** 2 * (r2 - 4.0)))
    return float("inf")


def t_squared_pdf(w, r):
    """Density of W = T^2 for T ~ t_r:  f_T(sqrt w)/sqrt w  ==  f_pdf(w, 1, r).
    Because T = Z/sqrt(V/r) gives T^2 = (Z^2/1)/(V/r) = F_{1,r}."""
    if w <= 0.0:
        return 0.0
    return students_t_pdf(math.sqrt(w), r) / math.sqrt(w)


# --- demo --------------------------------------------------------------------

def _demo():
    print("ST-17  MGF technique & normal sampling distributions -- demo")
    print("=" * 60)

    print("\n[A1] sum of independent normals is normal (mgfs multiply):")
    means, variances = [1.0, -0.5, 2.0], [4.0, 2.25, 1.0]
    mu_s, var_s = sum_of_normals_via_mgf(means, variances)
    print(f"   N(1,4) + N(-0.5,2.25) + N(2,1)  ->  N({mu_s}, {var_s})")
    t = 0.3
    print(f"   prod M_i(t)      = {product_of_normal_mgfs(t, means, variances):.8f}")
    print(f"   M_sum(t)         = {normal_mgf(t, mu_s, math.sqrt(var_s)):.8f}  (equal)")

    print("\n[A2] linear combination a.X stays normal:")
    coeffs = [2.0, -1.0, 0.5]
    mu_l, var_l = linear_combination_of_normals(coeffs, means, variances)
    print(f"   2X1 - X2 + 0.5X3 ~ N({mu_l}, {var_l})")
    print(f"   prod M_i(a_i t)  = {mgf_of_linear_combination_normals(t, coeffs, means, variances):.8f}")
    print(f"   M(t) of N        = {normal_mgf(t, mu_l, math.sqrt(var_l)):.8f}  (equal)")

    print("\n[A3] gammas (common scale) add shapes;  chi-squares add d.f.:")
    a_sum, th = sum_of_gammas_via_mgf([1.5, 2.0, 3.5], 2.0)
    print(f"   Gamma(1.5,2)+Gamma(2,2)+Gamma(3.5,2) = Gamma({a_sum},{th})")
    print(f"   chi^2_3 + chi^2_5 + chi^2_2 = chi^2_{sum_of_chisquares([3,5,2]):.0f}")
    print(f"   Z^2 density at x=2: {square_of_standard_normal_pdf(2.0):.6f} "
          f"vs chi2_pdf(2,1) = {chi2_pdf(2.0, 1):.6f}  (chi^2_1)")

    print("\n[B1] sampling distribution of the mean  (n=16, N(mu=10, sigma^2=8)):")
    m, v = sampling_dist_of_mean(10.0, 8.0, 16)
    print(f"   Xbar ~ N({m}, {v})   (sigma^2/n = 8/16 = 0.5)")
    print(f"   mgf of standardized mean at t=0.7 = {standardized_mean_mgf(0.7, 10.0, 8.0, 16):.8f} "
          f"= e^(t^2/2) = {math.exp(0.5*0.7**2):.8f}")
    print(f"   (n-1)S^2/sigma^2 ~ chi^2_{sample_variance_chi2_df(16)}")

    print("\n[B2] Student's t:  mean 0, var r/(r-2), and t_r -> N(0,1):")
    for r in (1, 3, 5, 30):
        mv = students_t_var(r)
        print(f"   r={r:>2}: f(0)={students_t_pdf(0.0, r):.5f}, var={mv}")
    print(f"   t_2000 pdf at 1.0 = {students_t_pdf(1.0, 2000):.6f}  vs "
          f"phi(1.0) = {standard_normal_pdf(1.0):.6f}")

    print("\n[B3] Snedecor's F:  mean r2/(r2-2);  and T^2 ~ F_{1,r}:")
    print(f"   F_{{5,10}}: f(1)={f_pdf(1.0, 5, 10):.5f}, mean={f_mean(10):.5f}, "
          f"var={f_var(5, 10):.5f}")
    w, r = 2.0, 6
    print(f"   T^2 density at w={w} (r={r}): {t_squared_pdf(w, r):.6f} "
          f"vs f_pdf({w},1,{r}) = {f_pdf(w, 1, r):.6f}")


if __name__ == "__main__":
    _demo()
