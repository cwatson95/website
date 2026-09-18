"""Tests for ST-05 discrete random variables & expectation.

Asserts the headline analytic identities of STAT 414 L7-L8: pmf normalization,
the cdf step function, LOTUS, mu = E[X], the variance computational formula
sigma^2 = E[X^2] - mu^2, vanishing first central moment, linearity of E and the
a^2 scaling of Var, the survival-function and integral representations of the
mean, and the mgf-derivative = mean preview.

Run:  python3 test_discrete_rv_expectation.py    ->  "All N tests passed."
"""

import math

import numpy as np

from discrete_rv_expectation import (
    pmf_is_valid, support, cdf_from_pmf, cdf_table,
    expectation, mean, expectation_of, raw_moment, central_moment,
    variance, std, standardize, skewness, linear_transform,
    survival, mean_via_survival, mgf,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _integrate(f, a, b, n=20000):
    """Midpoint rule for a continuous cross-check (cf. SM-06's _integrate)."""
    dx = (b - a) / n
    return sum(f(a + (i + 0.5) * dx) * dx for i in range(n))


# --- fixtures: a fair die, a Bernoulli, and a skewed signed RV ---------------

DIE_X = np.arange(1, 7)
DIE_P = np.full(6, 1.0 / 6.0)

P_BERN = 0.3
BERN_X = np.array([0.0, 1.0])
BERN_P = np.array([1.0 - P_BERN, P_BERN])

CX = np.array([-1.0, 0.0, 2.0])
CP = np.array([0.2, 0.5, 0.3])


def test_pmf_validity_and_rejection():
    # a genuine pmf is accepted; mass that does not sum to 1, or is negative, is not
    assert pmf_is_valid(DIE_X, DIE_P)
    assert pmf_is_valid(CX, CP)
    assert not pmf_is_valid(CX, np.array([0.2, 0.5, 0.5]))   # sums to 1.2
    assert not pmf_is_valid(CX, np.array([-0.1, 0.6, 0.5]))  # negative mass
    # the support drops zero-probability atoms
    sx = support(np.array([0.0, 1.0, 2.0]), np.array([0.5, 0.0, 0.5]))
    assert sx.tolist() == [0.0, 2.0]


def test_cdf_step_function():
    F = cdf_from_pmf(DIE_X, DIE_P)
    # below the support F = 0, at/above the top F = 1, right-continuous and nondecreasing
    assert _approx(F(0.5), 0.0)
    assert _approx(F(6.0), 1.0)
    assert _approx(F(3.0), 0.5)            # P(X <= 3) = 3/6
    assert F(2.9) <= F(3.0) <= F(3.1)
    # the jump of F at each atom equals the pmf there
    xs, cum = cdf_table(DIE_X, DIE_P)
    jumps = np.diff(np.concatenate(([0.0], cum)))
    assert np.allclose(jumps, DIE_P)
    assert _approx(cum[-1], 1.0)


def test_mean_values():
    assert _approx(expectation(DIE_X, DIE_P), 3.5)          # 7/2
    assert _approx(mean(DIE_X, DIE_P), 3.5)
    assert _approx(expectation(BERN_X, BERN_P), P_BERN)     # E[Bernoulli] = p
    assert _approx(expectation(CX, CP), -0.2 + 0.0 + 0.6)   # = 0.4


def test_lotus_matches_pushforward():
    # E[g(X)] by LOTUS equals E[Y] computed from the law of Y = g(X).
    g = lambda x: x * x
    lhs = expectation_of(g, CX, CP)
    # law of Y = X^2: values {1, 0, 4} with the SAME probabilities (atoms distinct here)
    yx = np.array([1.0, 0.0, 4.0])
    rhs = expectation(yx, CP)
    assert _approx(lhs, rhs)
    # and g(x)=x reproduces the mean
    assert _approx(expectation_of(lambda x: x, CX, CP), expectation(CX, CP))


def test_variance_computational_formula():
    # sigma^2 = E[X^2] - mu^2  equals the second central moment E[(X-mu)^2]
    for x, p in ((DIE_X, DIE_P), (BERN_X, BERN_P), (CX, CP)):
        var = variance(x, p)
        assert _approx(var, central_moment(x, p, 2))
        assert _approx(var, raw_moment(x, p, 2) - expectation(x, p) ** 2)
        assert var >= 0.0
    # closed forms
    assert _approx(variance(DIE_X, DIE_P), 35.0 / 12.0)
    assert _approx(variance(BERN_X, BERN_P), P_BERN * (1.0 - P_BERN))
    assert _approx(std(DIE_X, DIE_P), math.sqrt(35.0 / 12.0))


def test_moment_normalizations():
    # mu'_0 = 1 (normalization), mu'_1 = mu, mu_1 = 0 (mean of deviations)
    for x, p in ((DIE_X, DIE_P), (CX, CP)):
        assert _approx(raw_moment(x, p, 0), 1.0)
        assert _approx(raw_moment(x, p, 1), expectation(x, p))
        assert _approx(central_moment(x, p, 1), 0.0)


def test_standardize_and_skewness():
    # Z = (X-mu)/sigma has mean 0 and variance 1
    zx, zp = standardize(CX, CP)
    assert _approx(expectation(zx, zp), 0.0)
    assert _approx(variance(zx, zp), 1.0)
    # a symmetric distribution has zero skewness; the die is symmetric about 3.5
    assert _approx(skewness(DIE_X, DIE_P), 0.0, tol=1e-9)
    # the skewed custom RV has nonzero skew (mass piled at -1/0 with a long right atom)
    assert abs(skewness(CX, CP)) > 0.1


def test_linearity_of_expectation_and_variance():
    a, b = 3.0, -4.0
    yx, yp = linear_transform(a, b, CX, CP)
    # E[aX+b] = a E[X] + b
    assert _approx(expectation(yx, yp), a * expectation(CX, CP) + b)
    # Var(aX+b) = a^2 Var(X)  -- and is independent of the shift b
    assert _approx(variance(yx, yp), a ** 2 * variance(CX, CP))
    yx2, yp2 = linear_transform(a, b + 100.0, CX, CP)
    assert _approx(variance(yx2, yp2), variance(yx, yp))
    # additivity over a function decomposition: E[2X + 5] = 2E[X] + 5
    assert _approx(expectation_of(lambda x: 2 * x + 5, CX, CP),
                   2 * expectation(CX, CP) + 5)


def test_mean_via_survival_and_integral():
    # tail-sum identity for a non-negative integer RV: E[X] = sum_{k>=0} (1-F(k))
    assert _approx(mean_via_survival(DIE_X, DIE_P), 3.5)
    # continuous cross-check: E[X] = int_0^inf (1-F(x)) dx for a non-negative RV
    S = survival(DIE_X, DIE_P)
    integral = _integrate(lambda t: S(t), 0.0, 6.0, n=60000)
    assert _approx(integral, 3.5, tol=1e-3)
    # two-sided form for a signed RV: E[X] = int_0^inf (1-F) - int_{-inf}^0 F
    F = cdf_from_pmf(CX, CP)
    pos = _integrate(lambda t: 1.0 - F(t), 0.0, 2.0, n=60000)
    neg = _integrate(lambda t: F(t), -1.0, 0.0, n=60000)
    assert _approx(pos - neg, expectation(CX, CP), tol=1e-3)


def test_mgf_derivatives_give_moments():
    # M(0) = 1; M'(0) = mu; M''(0) = E[X^2]  (preview of ~ST-06)
    assert _approx(mgf(CX, CP, 0.0), 1.0)
    h = 1e-5
    m_prime = (mgf(CX, CP, h) - mgf(CX, CP, -h)) / (2 * h)
    m_second = (mgf(CX, CP, h) - 2 * mgf(CX, CP, 0.0) + mgf(CX, CP, -h)) / h ** 2
    assert _approx(m_prime, expectation(CX, CP), tol=1e-6)
    assert _approx(m_second, raw_moment(CX, CP, 2), tol=1e-5)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
