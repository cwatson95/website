"""Tests for ST-09 the Poisson distribution.

Run:  python3 test_poisson.py     ->  "All N tests passed."

Each test asserts a headline analytic identity of Poisson(lam): normalization,
mean = variance = lam, the mgf moment derivatives, the factorial moments from
the pgf, the law of rare events (binomial limit), the additivity property, and
the Poisson-process gamma-integral relation -- not tautologies.
"""
import math

from poisson import (
    poisson_pmf, poisson_cdf, poisson_normalization,
    poisson_mean, poisson_var, poisson_std,
    poisson_skewness, poisson_excess_kurtosis, poisson_mode,
    poisson_mgf, poisson_pgf, poisson_factorial_moment,
    binomial_pmf, poisson_limit_of_binomial,
    sum_of_poissons, poisson_convolution_pmf,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _integrate(f, a, b, n=200000):
    """Midpoint rule -- the continuous check (cf. SM-06 _integrate)."""
    dx = (b - a) / n
    return sum(f(a + (i + 0.5) * dx) * dx for i in range(n))


# --- the pmf -----------------------------------------------------------------

def test_pmf_normalization():
    # sum over all k of e^{-lam} lam^k/k! = e^{-lam} e^{lam} = 1
    for lam in (0.25, 1.0, 4.0, 12.0):
        assert _approx(poisson_normalization(lam, kmax=400), 1.0, tol=1e-12)
    # the degenerate lam = 0 limit: all mass at k = 0
    assert _approx(poisson_pmf(0, 0.0), 1.0)
    assert _approx(poisson_pmf(3, 0.0), 0.0)


def test_pmf_known_values_and_recurrence():
    lam = 2.5
    assert _approx(poisson_pmf(0, lam), math.exp(-lam))      # P(0) = e^{-lam}
    assert _approx(poisson_pmf(1, lam), lam * math.exp(-lam))  # P(1) = lam e^{-lam}
    # the defining recurrence P(k+1) = P(k) * lam/(k+1)
    for k in range(0, 12):
        assert _approx(poisson_pmf(k + 1, lam),
                       poisson_pmf(k, lam) * lam / (k + 1))
    # pmf is a genuine probability: 0 <= P <= 1
    for k in range(0, 20):
        assert 0.0 <= poisson_pmf(k, lam) <= 1.0


def test_mean_equals_lambda():
    for lam in (0.7, 3.0, 9.0):
        m = sum(k * poisson_pmf(k, lam) for k in range(400))
        assert _approx(m, lam, tol=1e-9)
        assert _approx(poisson_mean(lam), lam)


def test_variance_equals_lambda_and_equals_mean():
    for lam in (0.7, 3.0, 9.0):
        m = sum(k * poisson_pmf(k, lam) for k in range(400))
        v = sum((k - m) ** 2 * poisson_pmf(k, lam) for k in range(400))
        assert _approx(v, lam, tol=1e-8)
        assert _approx(poisson_var(lam), poisson_mean(lam))   # the signature
        assert _approx(poisson_std(lam), math.sqrt(lam))


def test_mgf_value_and_moment_derivatives():
    lam, t = 4.0, 0.3
    assert _approx(poisson_mgf(t, lam), math.exp(lam * (math.exp(t) - 1.0)))
    assert _approx(poisson_mgf(0.0, lam), 1.0)               # M(0) = 1 always
    # M'(0) = E[X] = lam ; M''(0) - M'(0)^2 = Var(X) = lam   (central differences)
    h = 1e-5
    m1 = (poisson_mgf(h, lam) - poisson_mgf(-h, lam)) / (2 * h)
    m2 = (poisson_mgf(h, lam) - 2 * poisson_mgf(0.0, lam) + poisson_mgf(-h, lam)) / h ** 2
    assert _approx(m1, lam, tol=1e-5)
    assert _approx(m2 - m1 ** 2, lam, tol=1e-4)


def test_pgf_factorial_moments():
    lam = 3.0
    assert _approx(poisson_pgf(1.0, lam), 1.0)               # G(1) = 1
    assert _approx(poisson_pgf(0.0, lam), math.exp(-lam))    # G(0) = P(X=0)
    # G'(1) = lam = E[X];  G''(1) = lam^2 = E[X(X-1)]   (central differences at s=1)
    h = 1e-5
    g1 = (poisson_pgf(1 + h, lam) - poisson_pgf(1 - h, lam)) / (2 * h)
    g2 = (poisson_pgf(1 + h, lam) - 2 * poisson_pgf(1.0, lam) + poisson_pgf(1 - h, lam)) / h ** 2
    assert _approx(g1, poisson_factorial_moment(1, lam), tol=1e-5)
    assert _approx(g2, poisson_factorial_moment(2, lam), tol=1e-4)


def test_factorial_moment_identity():
    # E[X(X-1)] = lam^2 directly from the pmf, matching poisson_factorial_moment
    for lam in (2.0, 5.0):
        s = sum(k * (k - 1) * poisson_pmf(k, lam) for k in range(400))
        assert _approx(s, poisson_factorial_moment(2, lam), tol=1e-8)
        # hence Var = E[X(X-1)] + E[X] - E[X]^2 = lam^2 + lam - lam^2 = lam
        assert _approx(s + lam - lam ** 2, lam, tol=1e-8)


def test_limit_of_binomial_law_of_rare_events():
    # holding lam = n*p fixed, the gap to Poisson(lam) shrinks as n grows
    lam = 2.0
    gaps = [poisson_limit_of_binomial(n, lam / n) for n in (5, 20, 100, 1000)]
    for a, b in zip(gaps, gaps[1:]):
        assert b < a                                          # monotone decrease
    assert gaps[-1] < 1e-3                                     # converged
    # pointwise: Binomial(1000, lam/1000) ~ Poisson(lam) at each k
    n = 1000
    for k in range(8):
        assert _approx(binomial_pmf(k, n, lam / n), poisson_pmf(k, lam), tol=2e-3)


def test_sum_of_independent_poissons():
    lam1, lam2 = 2.0, 5.0
    assert _approx(sum_of_poissons([lam1, lam2]), lam1 + lam2)
    # convolution of the two pmfs equals Poisson(lam1+lam2): the closure property
    for k in range(15):
        assert _approx(poisson_convolution_pmf(k, lam1, lam2),
                       poisson_pmf(k, lam1 + lam2), tol=1e-12)


def test_cdf_monotone_and_total():
    lam = 4.0
    prev = -1.0
    for k in range(40):
        c = poisson_cdf(k, lam)
        assert c >= prev                                      # nondecreasing
        prev = c
    assert _approx(poisson_cdf(400, lam), 1.0, tol=1e-12)     # F(inf) = 1
    # complement / increment: F(k) - F(k-1) = P(X=k)
    for k in range(1, 20):
        assert _approx(poisson_cdf(k, lam) - poisson_cdf(k - 1, lam),
                       poisson_pmf(k, lam))


def test_poisson_process_gamma_integral():
    # Poisson-process identity (links ~ST-11): for X ~ Poisson(lam),
    #   P(X <= k-1) = integral_lam^inf t^{k-1} e^{-t} / (k-1)!  dt
    # because the k-th arrival time of a unit-rate process is Gamma(k,1).
    lam, k = 3.0, 4
    lhs = poisson_cdf(k - 1, lam)
    rhs = _integrate(lambda t: t ** (k - 1) * math.exp(-t) / math.factorial(k - 1),
                     lam, lam + 60.0)
    assert _approx(lhs, rhs, tol=1e-4)


def test_skewness_and_excess_kurtosis():
    lam = 4.0
    m = sum(k * poisson_pmf(k, lam) for k in range(400))
    mu2 = sum((k - m) ** 2 * poisson_pmf(k, lam) for k in range(400))
    mu3 = sum((k - m) ** 3 * poisson_pmf(k, lam) for k in range(400))
    mu4 = sum((k - m) ** 4 * poisson_pmf(k, lam) for k in range(400))
    assert _approx(mu3 / mu2 ** 1.5, poisson_skewness(lam), tol=1e-7)
    assert _approx(mu4 / mu2 ** 2 - 3.0, poisson_excess_kurtosis(lam), tol=1e-7)


def test_mode_is_argmax_of_pmf():
    for lam in (2.3, 4.0, 7.8):
        mode = poisson_mode(lam)
        pm = poisson_pmf(mode, lam)
        assert pm >= poisson_pmf(mode - 1, lam)
        assert pm >= poisson_pmf(mode + 1, lam)
        assert mode == math.floor(lam)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
