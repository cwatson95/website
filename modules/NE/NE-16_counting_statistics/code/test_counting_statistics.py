"""NE-16 tests -- counting statistics against Shultis & Faw §§8.6-8.7,
Tables 8.3-8.4, and Chapter 8 problems 2 and 7.

Run:  python3 test_counting_statistics.py
"""

import math
import random
import statistics

from counting_statistics import (
    SIGMA_TABLE, CONFIDENCE_TABLE, FWHM_PER_SIGMA,
    counting_sigma, relative_error, counts_for_relative_error,
    mean_of_counts, sigma_of_mean, sigma_of_sum,
    confidence_multiplier, probability_within,
    propagate_sum, propagate_difference, propagate_product_or_ratio,
    net_rate, net_rate_sigma, optimal_time_split,
    true_rate, observed_rate, dead_time_loss_fraction,
    max_rate_for_loss, dead_time_from_two_source_method,
    fwhm_from_sigma, sigma_from_fwhm,
)


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def _rel(a, b, tol):
    return abs(a / b - 1.0) <= tol


# --- the single measurement  [Eqs. (8.10), (8.14); Table 8.3] ------------

def test_reproduces_table_8_3():
    """S&F Table 8.3: counts against percent standard deviation.  Every entry is
    just 100/sqrt(N), and the table exists to make the 1/sqrt(N) scaling
    concrete."""
    for counts, pct in SIGMA_TABLE.items():
        got = 100 * relative_error(counts)
        assert _rel(got, pct, 0.02), "%d counts: %.3f%% vs table %.0f%%" % (counts, got, pct)
    # the inverse: 1% needs 10 000 counts exactly
    assert _approx(counts_for_relative_error(0.01), 10000.0)
    assert _approx(counts_for_relative_error(0.001), 1e6)
    # halving the error costs 4x the counts
    assert _approx(counts_for_relative_error(0.005) / counts_for_relative_error(0.01), 4.0)
    for bad in (0.0, 1.0, -0.1, 1.5):
        try:
            counts_for_relative_error(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("relative error %r should be rejected" % bad)


def test_sigma_equals_sqrt_x_and_refuses_small_counts():
    """sigma = sqrt(x) holds for x above about 20 [S&F Eq. (8.10)].  Below that
    the Poisson distribution is visibly skewed and a symmetric interval
    misrepresents it, so the function raises rather than returning a
    plausible-looking number."""
    for x in (25, 100, 10000):
        assert _approx(counting_sigma(x), math.sqrt(x))
    counting_sigma(20)                      # the stated boundary is allowed
    counting_sigma(0)                       # and zero is a legitimate count
    for x in (1, 5, 19.9):
        try:
            counting_sigma(x)
        except ValueError as exc:
            assert "20" in str(exc)
        else:
            raise AssertionError("x = %r should be refused" % x)
    try:
        counting_sigma(-1)
    except ValueError:
        pass
    else:
        raise AssertionError("negative counts should be rejected")


def test_poisson_variance_really_is_the_mean():
    """The claim underlying the whole module, checked by simulation rather than
    assumed: for a Poisson process the variance equals the mean.

    The events are generated from EXPONENTIAL INTER-ARRIVAL TIMES, which is the
    actual physical model (~NE-06's memoryless decay), not from a binomial.
    A binomial with n trials of probability p has variance np(1-p), which only
    approaches np when p is small -- simulating with a convenient p ~ 0.2 gives
    a variance 20% below the mean and would make this test fail for a correct
    module."""
    rng = random.Random(20260801)
    lam = 400.0
    draws = []
    for _ in range(3000):
        t, k = 0.0, 0
        while True:
            t += rng.expovariate(lam)          # memoryless waiting time
            if t > 1.0:
                break
            k += 1
        draws.append(k)
    m = statistics.mean(draws)
    v = statistics.variance(draws)
    assert _rel(m, lam, 0.02), "mean %.1f" % m
    assert _rel(v, m, 0.06), "variance %.1f vs mean %.1f" % (v, m)
    # and the predicted sigma matches the observed scatter
    assert _rel(statistics.stdev(draws), counting_sigma(m), 0.04)
    # the contrast that motivates the docstring: a binomial at p = 0.2 does NOT
    # satisfy variance = mean, so the distribution genuinely matters
    binom = [sum(1 for _ in range(2000) if rng.random() < 0.2) for _ in range(500)]
    assert statistics.variance(binom) < 0.9 * statistics.mean(binom)


def test_averaging_N_measurements():
    """Eqs. (8.11)-(8.14).  sigma of the mean is sqrt(xbar/N), NOT the sample
    standard deviation -- it is derived from counting statistics, and the two
    agreeing is a check that the source was stable."""
    vals = [1255, 1286, 1234, 1301, 1221]
    xbar = mean_of_counts(vals)
    assert _rel(xbar, 1259.4, 1e-6)
    assert _rel(sigma_of_sum(vals), math.sqrt(sum(vals)), 1e-12)
    assert _rel(sigma_of_mean(vals), math.sqrt(xbar / 5), 1e-12)
    # Eq. (8.13) reduces to Eq. (8.10) for N = 1
    assert _approx(sigma_of_mean([400]), counting_sigma(400))
    # averaging N measurements improves the error by sqrt(N)
    assert _rel(sigma_of_mean([400]) / sigma_of_mean([400] * 9), 3.0, 1e-9)
    for bad in ([], [0]):
        try:
            sigma_of_mean(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % bad)


def test_reproduces_chapter_8_problem_7():
    """S&F Ch. 8 Prob. 7: five one-minute counts, 1255/1286/1234/1301/1221.
    Find the standard deviation of the average, and the factor a sixth
    measurement would change it by."""
    vals = [1255, 1286, 1234, 1301, 1221]
    s = sigma_of_mean(vals)
    assert _rel(s, 15.87, 1e-3), "%.4f" % s
    assert _rel(mean_of_counts(vals), 1259.4, 1e-4)
    # a sixth measurement: sqrt(5/6) = 0.913
    factor = math.sqrt(5.0 / 6.0)
    assert _rel(factor, 0.9129, 1e-3)
    six = sigma_of_mean(vals + [1259])
    assert _rel(six / s, factor, 5e-3)
    # the observed scatter is consistent with counting statistics, which is the
    # evidence that the source did not drift over the series
    assert _rel(statistics.stdev(vals), math.sqrt(mean_of_counts(vals)), 0.15)


# --- confidence intervals  [Table 8.4] -----------------------------------

def test_reproduces_table_8_4():
    """S&F Table 8.4, with the book's rounding made explicit: it lists k = 0.67
    for 50% (exact 0.6745) and 1.65 for 90% (exact 1.6449)."""
    for k, p in CONFIDENCE_TABLE.items():
        assert _rel(probability_within(k), p, 8e-3), \
            "k = %.2f: %.4f vs table %.3f" % (k, probability_within(k), p)
    # the exact multipliers
    assert _rel(confidence_multiplier(0.500), 0.6745, 1e-3)
    assert _rel(confidence_multiplier(0.683), 1.0006, 1e-3)
    assert _rel(confidence_multiplier(0.900), 1.6449, 1e-3)
    assert _rel(confidence_multiplier(0.950), 1.9600, 1e-3)
    # round trip
    for p in (0.5, 0.68, 0.9, 0.95, 0.99):
        assert _rel(probability_within(confidence_multiplier(p)), p, 1e-9)
    for bad in (0.0, 1.0, -0.5, 2.0):
        try:
            confidence_multiplier(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("p = %r should be rejected" % bad)


# --- propagation ---------------------------------------------------------

def test_errors_add_in_quadrature_for_both_sum_and_difference():
    """The single most-misused result in the subject: subtracting does NOT
    subtract the uncertainty.  x - y and x + y have identical error."""
    assert _approx(propagate_sum(3.0, 4.0), 5.0)
    assert propagate_difference is propagate_sum
    assert _approx(propagate_difference(3.0, 4.0), 5.0)
    # the error of a difference always EXCEEDS either input's
    for a, b in ((3.0, 4.0), (10.0, 1.0), (1.0, 1.0)):
        assert propagate_difference(a, b) > max(a, b)
    # products and ratios: relative errors combine
    val = 10.0 / 2.0
    s = propagate_product_or_ratio(val, [(10.0, 1.0), (2.0, 0.1)])
    assert _rel(s / val, math.sqrt(0.1 ** 2 + 0.05 ** 2), 1e-12)
    try:
        propagate_product_or_ratio(1.0, [(0.0, 1.0)])
    except ValueError:
        pass
    else:
        raise AssertionError("a zero denominator should be rejected")


def test_background_subtraction_always_costs_precision():
    """A net rate is a difference, so the background contributes its own full
    uncertainty.  A source barely above background is far worse determined than
    either raw count suggests -- which is what a detection limit is about."""
    # a strong source: background barely matters
    r1 = net_rate(10000, 60.0, 100, 60.0)
    s1 = net_rate_sigma(10000, 60.0, 100, 60.0)
    assert _rel(100 * s1 / r1, 1.02, 5e-2)

    # a weak source: 20 net counts on 500 of background
    r2 = net_rate(520, 60.0, 500, 60.0)
    s2 = net_rate_sigma(520, 60.0, 500, 60.0)
    assert _rel(100 * s2 / r2, 160.0, 5e-2), "%.1f%%" % (100 * s2 / r2)
    assert s2 > r2, "the uncertainty exceeds the signal -- no detection"

    # yet each raw count on its own is known to better than 5%
    assert 100 * relative_error(520) < 5.0
    assert 100 * relative_error(500) < 5.0

    # the net sigma always exceeds the gross count's own sigma
    assert s2 > counting_sigma(520) / 60.0
    for bad in ((100, 0.0, 50, 60.0), (100, 60.0, -1, 60.0)):
        try:
            net_rate_sigma(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_optimal_time_split_beats_fifty_fifty():
    """t_g/t_b = sqrt(r_g/r_b) minimises the net-rate variance for a fixed total
    time.  Beyond S&F; verified here by direct numerical minimisation rather
    than by trusting the formula."""
    for rg, rb in ((100.0, 1.0), (100.0, 10.0), (10.0, 5.0), (3.0, 2.0)):
        f_formula = optimal_time_split(rg, rb)

        def variance(f, total=100.0):
            tg, tb = f * total, (1 - f) * total
            return rg / tg + rb / tb          # sigma^2 of the net rate

        best = min((variance(f), f) for f in [i / 20000.0 for i in range(1, 20000)])
        assert _rel(f_formula, best[1], 2e-3), \
            "rg=%g rb=%g: formula %.4f vs numerical %.4f" % (rg, rb, f_formula, best[1])
        # and it is genuinely better than an even split
        assert variance(f_formula) <= variance(0.5) + 1e-12
        assert f_formula > 0.5                # more time on the stronger sample

    # the size of the win: for a 10:1 source, an even split wastes ~10% of the
    # attainable precision
    rg, rb = 100.0, 10.0
    f = optimal_time_split(rg, rb)
    v_opt = rg / (f * 100) + rb / ((1 - f) * 100)
    v_even = rg / 50.0 + rb / 50.0
    assert 1.05 < math.sqrt(v_even / v_opt) < 1.20
    for bad in ((0.0, 1.0), (1.0, 0.0), (-1.0, 1.0)):
        try:
            optimal_time_split(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


# --- dead time  [Eq. (8.15)] ---------------------------------------------

def test_reproduces_chapter_8_problem_2():
    """S&F Ch. 8 Prob. 2: a GM tube with tau = 0.25 ms reads 900 counts/s.
    What is the true rate?"""
    m, tau = 900.0, 0.25e-3
    assert _rel(dead_time_loss_fraction(m, tau), 0.225, 1e-9)
    n = true_rate(m, tau)
    assert _rel(n, 1161.3, 1e-3), "%.1f" % n
    # a 22.5% dead fraction means a 29% upward correction
    assert _rel(n / m - 1, 0.2903, 1e-3)
    # and the forward map inverts it
    assert _rel(observed_rate(n, tau), m, 1e-12)


def test_the_five_percent_rule_and_the_GM_ceiling():
    """S&F §8.6.3 advises keeping m*tau below 0.05.  For a GM tube with
    tau = 100 us that caps the usable rate at 500 counts/s -- the number the book
    quotes, and a severe limit."""
    assert _rel(max_rate_for_loss(100e-6, 0.05), 500.0, 1e-12)
    assert _rel(dead_time_loss_fraction(500.0, 100e-6), 0.05, 1e-12)
    # a fast scintillator with tau = 1 us tolerates 100x more
    assert _rel(max_rate_for_loss(1e-6, 0.05), 50000.0, 1e-12)
    for bad in ((0.0, 0.05), (-1e-6, 0.05), (1e-6, 0.0), (1e-6, 1.0)):
        try:
            max_rate_for_loss(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_the_correction_is_refused_once_it_dominates():
    """Eq. (8.15) diverges at m*tau = 1, but it stops being trustworthy long
    before: past m*tau = 0.5 the correction exceeds the measurement itself, so
    the answer is set by the assumed model rather than by the data.

    The non-paralysable model used here is one of two standard choices; the
    paralysable model gives a materially different answer in exactly that
    regime, which is why the module refuses rather than picking one."""
    true_rate(4000.0, 100e-6)                      # m*tau = 0.40, allowed
    true_rate(5000.0, 100e-6)                      # m*tau = 0.50, the boundary
    for m in (6000.0, 9000.0, 10000.0, 20000.0):
        try:
            true_rate(m, 100e-6)
        except ValueError as exc:
            assert "0.5" in str(exc) or "diverges" in str(exc)
        else:
            raise AssertionError("m*tau = %.2f should be refused" % (m * 1e-4))


def test_the_observed_rate_saturates_which_is_the_dangerous_failure():
    """m = n/(1 + n tau) never diverges -- it saturates at 1/tau.  So a detector
    at saturation reports the SAME reading for any input above it, and a
    catastrophically intense field can read as a merely moderate one.

    This is the physical reason dead time is a safety issue and not just a
    precision one."""
    tau = 100e-6
    ceiling = 1.0 / tau
    prev = 0.0
    for n in (1e4, 1e5, 1e6, 1e9, 1e12):
        m = observed_rate(n, tau)
        assert m < ceiling
        assert m > prev
        prev = m
    assert _rel(observed_rate(1e12, tau), ceiling, 1e-6)
    # a 10^5 range of true rates compresses into less than a factor of 2 observed
    assert observed_rate(1e9, tau) / observed_rate(1e5, tau) < 1.15
    # forward and reverse are consistent where the reverse is allowed
    for n in (100.0, 1000.0, 4000.0):
        assert _rel(true_rate(observed_rate(n, tau), tau), n, 1e-9)


def test_dead_time_from_the_two_source_method():
    """Losses are non-linear, so m12 < m1 + m2 and the shortfall measures tau.
    Beyond S&F, which states Eq. (8.15) without saying where tau comes from.

    Checked self-consistently: generate observed rates from a known tau via the
    forward map, then recover it."""
    tau = 120e-6

    def recover(n1, n2):
        m1, m2 = observed_rate(n1, tau), observed_rate(n2, tau)
        m12 = observed_rate(n1 + n2, tau)
        assert m12 < m1 + m2                      # the whole basis of the method
        return dead_time_from_two_source_method(m1, m2, m12)

    # In the low-loss regime the leading-order formula is good to a few percent
    assert _rel(recover(300.0, 400.0), tau, 0.05)

    # It is only leading-order, and it degrades MONOTONICALLY with the loss --
    # always underestimating, because it drops the second-order term. Asserting
    # that pattern is a stronger check than picking one lucky operating point.
    errs = [abs(recover(a, b) / tau - 1.0)
            for a, b in ((300.0, 400.0), (1000.0, 1500.0), (3000.0, 4000.0))]
    assert errs[0] < errs[1] < errs[2], errs
    assert _rel(errs[0], 0.039, 0.10) and _rel(errs[2], 0.228, 0.10)
    for a, b in ((300.0, 400.0), (3000.0, 4000.0)):
        assert recover(a, b) < tau                # always low, never high
    # and it must refuse data showing no loss at all
    try:
        dead_time_from_two_source_method(100.0, 100.0, 200.0)
    except ValueError:
        pass
    else:
        raise AssertionError("no detectable loss should be refused")
    try:
        dead_time_from_two_source_method(10.0, 100.0, 100.0, m_bkg=50.0)
    except ValueError:
        pass
    else:
        raise AssertionError("a source below background should be rejected")


# --- peak widths ---------------------------------------------------------

def test_fwhm_and_sigma_round_trip():
    """FWHM = 2.355 sigma [S&F §8.6.2], used throughout ~NE-15."""
    assert _approx(fwhm_from_sigma(1.0), 2.355)
    assert _approx(sigma_from_fwhm(2.355), 1.0)
    for s in (0.5, 22.5, 100.0):
        assert _rel(sigma_from_fwhm(fwhm_from_sigma(s)), s, 1e-12)
    # the exact Gaussian factor is 2 sqrt(2 ln 2) = 2.3548
    assert _rel(FWHM_PER_SIGMA, 2.0 * math.sqrt(2.0 * math.log(2.0)), 1e-3)
    for fn in (fwhm_from_sigma, sigma_from_fwhm):
        try:
            fn(-1.0)
        except ValueError:
            pass
        else:
            raise AssertionError("%s should reject negatives" % fn.__name__)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
