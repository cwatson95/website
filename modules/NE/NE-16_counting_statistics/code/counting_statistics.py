"""NE-16  Counting statistics: Poisson counting, propagated error, dead time.

Nuclear Science & Engineering trunk, module NE-16 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Sections 8.6-8.7 (printed pp. 259-267).  Pure stdlib.

~NE-15 built the detectors.  This module is about what their output MEANS, and
it rests on one fact that makes radiation measurement unlike most others:

    THE UNCERTAINTY IS KNOWN IN ADVANCE.

Radioactive decay is a Bernoulli process (~NE-06), so a count x carries variance
x -- you do not have to repeat the measurement to learn its precision, you read
it off the single number you already have:

    sigma = sqrt(x),     sigma/x = 1/sqrt(x) .

Everything follows.  1% precision needs 10 000 counts, and no amount of care with
the electronics changes that.  Halving the uncertainty costs four times the
counting time.  And because the relative error falls only as 1/sqrt(x), there is
a sharp practical ceiling on what patience can buy.

Two things then complicate it, and both are here:

  * PROPAGATION.  Real results are differences and ratios of counts (sample minus
    background, one rate over another), and the errors compound.  A weak source
    on a strong background can have an uncertainty far larger than either count's
    own -- and the optimal division of a fixed counting time between sample and
    background is NOT 50/50.
  * DEAD TIME.  A detector busy with one event cannot record the next, so the
    observed rate understates the true one.  The correction diverges, and past
    m*tau ~ 0.5 the measurement stops meaning anything.
"""

import math

__all__ = [
    "SIGMA_TABLE", "CONFIDENCE_TABLE", "FWHM_PER_SIGMA",
    "counting_sigma", "relative_error", "counts_for_relative_error",
    "mean_of_counts", "sigma_of_mean", "sigma_of_sum",
    "confidence_multiplier", "probability_within",
    "propagate_sum", "propagate_difference", "propagate_product_or_ratio",
    "net_rate", "net_rate_sigma", "optimal_time_split",
    "true_rate", "observed_rate", "dead_time_loss_fraction",
    "max_rate_for_loss", "dead_time_from_two_source_method",
    "fwhm_from_sigma", "sigma_from_fwhm",
]

FWHM_PER_SIGMA = 2.355          # Gaussian FWHM = 2.355 sigma  [S&F §8.6.2]

# S&F Table 8.3 (printed p. 261): counts vs percent standard deviation.
SIGMA_TABLE = {100: 10.0, 400: 5.0, 1100: 3.0, 2500: 2.0, 10000: 1.0}

# S&F Table 8.4 (printed p. 261): k-sigma vs enclosed probability.
CONFIDENCE_TABLE = {0.67: 0.500, 1.00: 0.683, 1.65: 0.900,
                    1.96: 0.950, 3.00: 0.997}


# --- the single-measurement result  [S&F Eqs. (8.10), (8.14)] ------------

def counting_sigma(x):
    """sigma = sqrt(x)  [S&F Eq. (8.10)].

    Valid for x greater than about 20, where the underlying binomial is well
    approximated by a Gaussian.  Below that the distribution is visibly skewed
    and a symmetric x +- sqrt(x) interval misrepresents it -- so this raises
    rather than quietly returning a number that looks fine."""
    if x < 0:
        raise ValueError("a count cannot be negative")
    if 0 < x < 20:
        raise ValueError("x = %g is below the ~20 counts at which S&F state the "
                         "Gaussian approximation holds; the Poisson distribution "
                         "is still visibly skewed there" % x)
    return math.sqrt(x)


def relative_error(x):
    """sigma/x = 1/sqrt(x), as a FRACTION.

    The defining scaling of the subject.  Note that it improves only as the
    square root: 1% needs 10 000 counts, 0.1% needs 1 000 000."""
    if x <= 0:
        raise ValueError("count must be positive")
    return counting_sigma(x) / x


def counts_for_relative_error(fraction):
    """Counts needed to reach a target relative error:  N = 1/f^2.

    The inverse of `relative_error`, and the number that actually plans an
    experiment."""
    if not 0 < fraction < 1:
        raise ValueError("relative error must lie in (0, 1)")
    return 1.0 / (fraction * fraction)


def mean_of_counts(values):
    """Sample mean  [S&F Eq. (8.11)]."""
    if not values:
        raise ValueError("need at least one measurement")
    return sum(values) / float(len(values))


def sigma_of_sum(values):
    """sigma of the TOTAL of N counts  [S&F Eq. (8.12)]: sqrt(sum x_i).

    Because each x_i has variance x_i, variances add and the total behaves like
    one long measurement -- which it is."""
    if not values:
        raise ValueError("need at least one measurement")
    if any(v < 0 for v in values):
        raise ValueError("counts cannot be negative")
    return math.sqrt(sum(values))


def sigma_of_mean(values):
    """sigma of the MEAN of N counts  [S&F Eq. (8.13)]:  sqrt(xbar/N).

    Note what this is NOT: it is not the sample standard deviation of the
    values.  S&F derive it from counting statistics, assuming the source
    activity is constant over the series.  If the measured scatter greatly
    exceeds this, that is evidence the assumption is false -- a drifting source,
    a drifting detector -- not a reason to use the sample sigma instead."""
    xbar = mean_of_counts(values)
    if xbar <= 0:
        raise ValueError("mean count must be positive")
    return math.sqrt(xbar / len(values))


# --- confidence intervals  [S&F Table 8.4] -------------------------------

def probability_within(k):
    """Probability a Gaussian variate falls within +-k sigma: erf(k/sqrt2)."""
    if k < 0:
        raise ValueError("k must be non-negative")
    return math.erf(k / math.sqrt(2.0))


def confidence_multiplier(probability, tol=1e-12):
    """The k for a wanted two-sided probability -- the inverse of
    `probability_within`, by bisection.

    S&F's Table 8.4 rounds: it lists 0.67 for 50% (exact 0.6745) and 1.65 for
    90% (exact 1.6449).  This returns the exact values."""
    if not 0 < probability < 1:
        raise ValueError("probability must lie in (0, 1)")
    lo, hi = 0.0, 40.0
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if probability_within(mid) < probability:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# --- error propagation ---------------------------------------------------

def propagate_sum(*sigmas):
    """Quadrature sum -- for x + y or x - y alike.

    Subtraction does NOT subtract the errors; it adds them in quadrature, which
    is why a small difference between two large counts is so badly determined."""
    for s in sigmas:
        if s < 0:
            raise ValueError("sigmas cannot be negative")
    return math.sqrt(sum(s * s for s in sigmas))


propagate_difference = propagate_sum


def propagate_product_or_ratio(value, pairs):
    """sigma of a product or quotient: relative errors add in quadrature.

    `pairs` is [(v_i, sigma_i), ...].  Returns the ABSOLUTE sigma of `value`."""
    if any(v == 0 for v, _ in pairs):
        raise ValueError("cannot take a relative error about zero")
    rel = math.sqrt(sum((s / v) ** 2 for v, s in pairs))
    return abs(value) * rel


def net_rate(gross_counts, gross_time, bkg_counts, bkg_time):
    """Net (source) count rate:  r = C_g/t_g - C_b/t_b."""
    if gross_time <= 0 or bkg_time <= 0:
        raise ValueError("counting times must be positive")
    return gross_counts / gross_time - bkg_counts / bkg_time


def net_rate_sigma(gross_counts, gross_time, bkg_counts, bkg_time):
    """sigma of the net rate:  sqrt(C_g/t_g^2 + C_b/t_b^2).

    The background contributes its OWN full uncertainty, so subtracting a
    background never reduces the error -- it always increases it.  A source
    barely above background can have a net rate whose uncertainty exceeds the
    rate itself, which is the whole content of a detection limit."""
    if gross_time <= 0 or bkg_time <= 0:
        raise ValueError("counting times must be positive")
    if gross_counts < 0 or bkg_counts < 0:
        raise ValueError("counts cannot be negative")
    return math.sqrt(gross_counts / gross_time ** 2 + bkg_counts / bkg_time ** 2)


def optimal_time_split(gross_rate, bkg_rate):
    """Fraction of a fixed total counting time to spend on the SAMPLE, to
    minimise the uncertainty in the net rate:

        t_g/t_b = sqrt(r_g/r_b)   =>   f_g = sqrt(r_g)/(sqrt(r_g)+sqrt(r_b)) .

    Beyond S&F, which does not treat time allocation; the result is standard and
    the derivation is a one-line Lagrange multiplier.  Worth having because the
    naive 50/50 split is wrong whenever the rates differ, and the loss is real:
    for a source ten times background, 50/50 wastes about 15% of the available
    precision."""
    if gross_rate <= 0 or bkg_rate <= 0:
        raise ValueError("rates must be positive")
    rg, rb = math.sqrt(gross_rate), math.sqrt(bkg_rate)
    return rg / (rg + rb)


# --- dead time  [S&F Eq. (8.15)] -----------------------------------------

def true_rate(m, tau):
    """n = m/(1 - m tau)  [S&F Eq. (8.15)]: correcting an observed rate for
    dead-time losses, in the NON-PARALYSABLE model.

    Diverges at m*tau = 1.  Long before that the correction dominates the
    measurement: S&F advise keeping m*tau below 0.05, and this raises above 0.5,
    where the correction exceeds the measurement itself and the result depends
    entirely on the assumed model rather than on the data."""
    if m < 0 or tau < 0:
        raise ValueError("rate and dead time must be non-negative")
    loss = m * tau
    if loss >= 1.0:
        raise ValueError("m*tau = %.3f >= 1: Eq. (8.15) diverges -- the detector "
                         "is saturated and no true rate can be inferred" % loss)
    if loss > 0.5:
        raise ValueError("m*tau = %.3f > 0.5: the dead-time correction would "
                         "exceed the measurement, so the answer is dominated by "
                         "the assumed model rather than the data. S&F advise "
                         "keeping m*tau < 0.05." % loss)
    return m / (1.0 - loss)


def observed_rate(n, tau):
    """The forward direction: m = n/(1 + n tau).

    Unlike Eq. (8.15) this never diverges -- as n grows, m saturates at 1/tau.
    That ceiling is the detector's maximum possible reading, and a detector at
    saturation reports the SAME number for any input rate above it, which is the
    dangerous failure mode: a hugely intense field can read as a moderate one."""
    if n < 0 or tau < 0:
        raise ValueError("rate and dead time must be non-negative")
    return n / (1.0 + n * tau)


def dead_time_loss_fraction(m, tau):
    """m*tau -- the fraction of the time the detector is unable to respond."""
    if m < 0 or tau < 0:
        raise ValueError("rate and dead time must be non-negative")
    return m * tau


def max_rate_for_loss(tau, max_loss=0.05):
    """Highest observed rate keeping losses below `max_loss`  [S&F §8.6.3].

    For a GM tube with tau = 100 us, that is 500 counts/s -- the number S&F
    quote, and a severe limit that is the main reason GM counters are survey
    instruments rather than spectrometers."""
    if tau <= 0:
        raise ValueError("dead time must be positive")
    if not 0 < max_loss < 1:
        raise ValueError("max_loss must lie in (0, 1)")
    return max_loss / tau


def dead_time_from_two_source_method(m1, m2, m12, m_bkg=0.0):
    """Dead time from the two-source method: count each source alone and both
    together.  Because losses are non-linear, m12 < m1 + m2, and the shortfall
    measures tau.

    With backgrounds subtracted and to leading order,

        tau ~ (m1 + m2 - m12) / (2 m1 m2) .

    Beyond S&F, which states Eq. (8.15) without saying how tau is obtained.  The
    exact solution needs a quadratic; this is the standard first-order form and
    is documented as such."""
    a, b, ab = m1 - m_bkg, m2 - m_bkg, m12 - m_bkg
    if a <= 0 or b <= 0:
        raise ValueError("source rates must exceed the background")
    if ab >= a + b:
        raise ValueError("m12 = %.4g is not less than m1 + m2 = %.4g: no "
                         "dead-time loss is detectable in these data" % (ab, a + b))
    return (a + b - ab) / (2.0 * a * b)


# --- peak widths  [S&F §8.6.2] -------------------------------------------

def fwhm_from_sigma(sigma):
    """FWHM = 2.355 sigma, for a Gaussian peak."""
    if sigma < 0:
        raise ValueError("sigma cannot be negative")
    return FWHM_PER_SIGMA * sigma


def sigma_from_fwhm(fwhm):
    """The inverse."""
    if fwhm < 0:
        raise ValueError("FWHM cannot be negative")
    return fwhm / FWHM_PER_SIGMA


# --- demo --------------------------------------------------------------------

def _demo():
    print("NE-16  counting statistics\n")

    print("  the uncertainty is known from the single measurement  [Table 8.3]")
    print("   counts     sigma      relative error     S&F Table 8.3")
    for x in sorted(SIGMA_TABLE):
        print("   %8d %9.1f %14.2f%% %14.0f%%"
              % (x, counting_sigma(x), 100 * relative_error(x), SIGMA_TABLE[x]))
    print("   -> 1% needs 10 000 counts; 0.1% needs a million.  1/sqrt(N) is brutal.")

    print("\n  confidence intervals  [Table 8.4]")
    print("   k       S&F     exact      exact k for that probability")
    for k in sorted(CONFIDENCE_TABLE):
        p = CONFIDENCE_TABLE[k]
        print("   %-6.2f %7.3f %9.4f %18.4f"
              % (k, p, probability_within(k), confidence_multiplier(p)))

    print("\n  S&F Ch. 8 Prob. 7: five one-minute counts")
    vals = [1255, 1286, 1234, 1301, 1221]
    xbar = mean_of_counts(vals)
    print("   values %s" % vals)
    print("   mean %.1f, sigma of the mean %.2f  -> %.0f +- %.0f"
          % (xbar, sigma_of_mean(vals), xbar, sigma_of_mean(vals)))
    print("   a sixth measurement changes sigma by sqrt(5/6) = %.4f"
          % math.sqrt(5.0 / 6.0))
    import statistics
    print("   (observed scatter %.1f vs counting prediction %.1f -- consistent,"
          % (statistics.stdev(vals), math.sqrt(xbar)))
    print("    which is itself the check that the source was stable)")

    print("\n  subtracting a background always costs precision")
    print("   gross    bkg    net rate   sigma    relative")
    for cg, cb in ((10000, 100), (1000, 500), (520, 500)):
        r = net_rate(cg, 60.0, cb, 60.0)
        s = net_rate_sigma(cg, 60.0, cb, 60.0)
        print("   %6d %6d %10.3f %8.3f %10s"
              % (cg, cb, r, s, "%.1f%%" % (100 * s / r) if r > 0 else "-"))
    print("   -> the last is a source barely above background: 20 net counts on")
    print("      500 of background gives a 160% uncertainty -- no detection at all,")
    print("      even though each count alone is known to better than 5%.")

    print("\n  how to split a fixed counting time")
    print("   gross rate  bkg rate   optimal sample fraction   (naive is 0.50)")
    for rg, rb in ((100.0, 1.0), (100.0, 10.0), (10.0, 5.0), (2.0, 1.0)):
        print("   %10.1f %9.1f %22.3f" % (rg, rb, optimal_time_split(rg, rb)))

    print("\n  dead time  [Eq. (8.15)]")
    tau = 100e-6
    print("   GM tube, tau = 100 us: max rate for 5%% loss = %.0f counts/s"
          % max_rate_for_loss(tau))
    print("   observed    m*tau     true rate    correction")
    for m in (100.0, 500.0, 1000.0, 4000.0, 5000.0, 6000.0):
        try:
            n = true_rate(m, tau)
            print("   %9.0f %8.3f %12.0f %11.1f%%" % (m, m * tau, n, 100 * (n / m - 1)))
        except ValueError:
            print("   %9.0f %8.3f %12s   refused" % (m, m * tau, "-"))
    print("   the forward map saturates: at any true rate, m never exceeds 1/tau = %.0f/s"
          % (1 / tau))
    for n in (1e4, 1e5, 1e6, 1e9):
        print("     true %10.3g /s  ->  observed %8.1f /s" % (n, observed_rate(n, tau)))


if __name__ == "__main__":
    _demo()
