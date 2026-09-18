"""NE-06  Decay kinetics -- the decay constant, half-life, mean life, activity.

Nuclear Science & Engineering trunk, module NE-06 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Section 5.5 (printed pp. 111-117).  Pure stdlib; half-lives are read from
../../data_tables/A4_isotopic_abundances.csv (Appendix A.4).

Radioactive decay is the archetypal memoryless process.  A nucleus has a
constant probability per unit time of decaying, lambda, independent of how long
it has already existed, so

    dN/dt = -lambda N   =>   N(t) = N0 exp(-lambda t)

and everything else follows: the half-life T = ln2/lambda, the mean life
1/lambda, the exponential waiting-time density lambda exp(-lambda t), and the
activity A = lambda N.  The same structure appears as the exponential
distribution in ~ST-11 and as Beer's law for photon attenuation in ~NE-11 -- one
differential equation, three different physical readings.

What is measured is never N but the *activity* A = lambda N, in becquerels (one
decay per second) or curies (3.7e10 Bq).  Note the inversion this forces: at
fixed sample mass, a *short* half-life means a *high* activity, so the most
intensely radioactive nuclides are the ones that disappear fastest.  That single
fact organises most of radiological protection (~NE-18) and waste management
(~NE-23).
"""

import csv
import math
import os
import re

__all__ = [
    "LN2", "AVOGADRO", "BQ_PER_CI", "SECONDS_PER",
    "decay_constant", "half_life", "mean_lifetime",
    "number_remaining", "fraction_remaining", "half_lives_elapsed",
    "activity", "activity_at_time", "specific_activity",
    "survival_probability", "decay_probability", "decay_time_pdf",
    "time_to_fraction", "time_to_activity",
    "total_decay_constant", "branching_fractions", "partial_half_life",
    "parse_half_life", "load_half_lives", "half_life_of",
    "curies", "becquerels",
]

LN2 = math.log(2.0)
AVOGADRO = 6.0221415e23          # Table A.1
BQ_PER_CI = 3.7e10               # 1 Ci = 3.7e10 decays/s, by definition

# time units as printed in Appendix A.4, in seconds
SECONDS_PER = {
    "ys": 1e-24, "zs": 1e-21, "as": 1e-18, "fs": 1e-15, "ps": 1e-12,
    "ns": 1e-9, "us": 1e-6, "µs": 1e-6, "ms": 1e-3, "s": 1.0,
    "min": 60.0, "h": 3600.0, "d": 86400.0,
    "y": 365.25 * 86400.0,
}
for _p, _m in (("k", 1e3), ("M", 1e6), ("G", 1e9), ("T", 1e12),
               ("P", 1e15), ("E", 1e18), ("Z", 1e21), ("Y", 1e24)):
    SECONDS_PER[_p + "y"] = SECONDS_PER["y"] * _m

_HALF_LIVES = None


# --- the exponential law  [S&F Eqs. (5.32)-(5.36)] --------------------------

def decay_constant(t_half):
    """lambda = ln2 / T_1/2  [Eq. (5.36)].  Units are the inverse of t_half's."""
    if t_half <= 0:
        raise ValueError("half-life must be positive")
    return LN2 / t_half


def half_life(lam):
    """T_1/2 = ln2 / lambda  [Eq. (5.36)]."""
    if lam <= 0:
        raise ValueError("decay constant must be positive")
    return LN2 / lam


def mean_lifetime(t_half=None, lam=None):
    """Mean life T_av = 1/lambda = T_1/2 / ln2  [Eq. (5.44)].

    The average of t over the exponential waiting-time density, and therefore
    about 1.44 times the half-life -- the long tail pulls the mean above the
    median."""
    if lam is None:
        lam = decay_constant(t_half)
    return 1.0 / lam


def number_remaining(n0, t, t_half=None, lam=None):
    """N(t) = N0 exp(-lambda t)  [Eq. (5.34)], equivalently N0 (1/2)^(t/T)
    [Eq. (5.39)]."""
    if lam is None:
        lam = decay_constant(t_half)
    if t < 0:
        raise ValueError("time must be non-negative")
    return n0 * math.exp(-lam * t)


def fraction_remaining(t, t_half=None, lam=None):
    """N(t)/N0 = exp(-lambda t)."""
    return number_remaining(1.0, t, t_half, lam)


def half_lives_elapsed(fraction):
    """Number of half-lives needed to reach the given surviving fraction
    [Eq. (5.38)]:  n = -log2(f) = -1.4427 ln f."""
    if not 0 < fraction <= 1:
        raise ValueError("fraction must lie in (0, 1]")
    return -math.log(fraction) / LN2


# --- probability readings  [S&F Eqs. (5.40)-(5.44)] ------------------------

def survival_probability(t, t_half=None, lam=None):
    """P(a given nucleus is still intact at t) = exp(-lambda t)  [Eq. (5.40)].

    Memoryless: this does not depend on how long the nucleus has already
    survived, which is what makes 'the age of a nucleus' a meaningless idea."""
    return fraction_remaining(t, t_half, lam)


def decay_probability(t, t_half=None, lam=None):
    """P(decays within t) = 1 - exp(-lambda t)  [Eq. (5.41)].

    For lambda t << 1 this is ~ lambda t  [Eq. (5.42)] -- the approximation
    behind every 'reactions per second' estimate in ~NE-11."""
    return 1.0 - survival_probability(t, t_half, lam)


def decay_time_pdf(t, t_half=None, lam=None):
    """Probability density of the decay time, p(t) = lambda exp(-lambda t)
    [Eq. (5.43)] -- the exponential distribution of ~ST-11."""
    if lam is None:
        lam = decay_constant(t_half)
    if t < 0:
        return 0.0
    return lam * math.exp(-lam * t)


def time_to_fraction(fraction, t_half=None, lam=None):
    """Time for the population to fall to the given fraction of its initial value."""
    if lam is None:
        lam = decay_constant(t_half)
    if not 0 < fraction <= 1:
        raise ValueError("fraction must lie in (0, 1]")
    return -math.log(fraction) / lam


# --- activity  [S&F Eq. (5.45)] ---------------------------------------------

def activity(n, t_half=None, lam=None):
    """A = lambda N  [Eq. (5.45)], in decays per unit time.

    This -- not N -- is what a detector measures."""
    if lam is None:
        lam = decay_constant(t_half)
    return lam * n


def activity_at_time(a0, t, t_half=None, lam=None):
    """A(t) = A0 exp(-lambda t): activity decays with the same constant as N."""
    return number_remaining(a0, t, t_half, lam)


def time_to_activity(a0, a, t_half=None, lam=None):
    """Time for an activity to fall from a0 to a."""
    if a <= 0 or a0 <= 0:
        raise ValueError("activities must be positive")
    return time_to_fraction(a / a0, t_half, lam)


def specific_activity(t_half_s, mass_number):
    """Activity per gram of pure nuclide, in Bq/g:

        SA = lambda N = (ln2 / T) * (N_A / A) .

    Inversely proportional to half-life, which is why a gram of a short-lived
    nuclide is fiercely radioactive and a gram of 238U barely is."""
    if t_half_s <= 0 or mass_number <= 0:
        raise ValueError("half-life and mass number must be positive")
    return decay_constant(t_half_s) * AVOGADRO / mass_number


# --- competing decay modes  [S&F Eqs. (5.47)-(5.49)] -----------------------

def total_decay_constant(lambdas):
    """lambda = sum_i lambda_i  [Eq. (5.48)].

    Independent channels add their *rates*, not their half-lives."""
    lams = list(lambdas)
    if not lams or any(l < 0 for l in lams):
        raise ValueError("decay constants must be non-negative")
    return sum(lams)


def branching_fractions(lambdas):
    """f_i = lambda_i / lambda  [Eq. (5.49)] -- the fraction of decays going by
    each channel.  Sums to one."""
    lams = list(lambdas)
    tot = total_decay_constant(lams)
    if tot == 0:
        raise ValueError("at least one channel must be open")
    return [l / tot for l in lams]


def partial_half_life(t_half_total, branch_fraction):
    """Half-life the nuclide *would* have if only this channel existed:
    T_i = T / f_i.  Always longer than the observed half-life."""
    if not 0 < branch_fraction <= 1:
        raise ValueError("branching fraction must lie in (0, 1]")
    return t_half_total / branch_fraction


# --- unit conversions --------------------------------------------------------

def curies(bq):
    """Becquerel -> curie."""
    return bq / BQ_PER_CI


def becquerels(ci):
    """Curie -> becquerel."""
    return ci * BQ_PER_CI


# --- half-lives from the extracted Appendix A.4 -----------------------------

_HL = re.compile(r"^\s*([<>~≃]?)\s*([0-9]*\.?[0-9]+)\s*([A-Za-zµ]+)\s*$")


def parse_half_life(text):
    """'12.32 y' -> 3.888e8 s.  'stable' -> math.inf.  Handles the SI-prefixed
    year units Appendix A.4 uses (ky, My, Gy, Ty, Py, Ey) and the relational
    prefixes on limits ('>600 Ty')."""
    s = str(text).strip()
    if not s or s.lower() == "stable":
        return math.inf
    m = _HL.match(s)
    if not m:
        raise ValueError("cannot parse half-life %r" % (text,))
    _rel, value, unit = m.groups()
    if unit not in SECONDS_PER:
        raise ValueError("unknown time unit %r in %r" % (unit, text))
    return float(value) * SECONDS_PER[unit]


def load_half_lives(path=None):
    """{nuclide: half_life_seconds} from the extracted Appendix A.4.  Cached.
    Stable nuclides map to math.inf."""
    global _HALF_LIVES
    if _HALF_LIVES is not None and path is None:
        return _HALF_LIVES
    here = os.path.dirname(os.path.abspath(__file__))
    p = path or os.path.normpath(os.path.join(
        here, os.pardir, os.pardir, "data_tables", "A4_isotopic_abundances.csv"))
    out = {}
    with open(p, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                out[row["nuclide"]] = parse_half_life(row["half_life"])
            except ValueError:
                continue
    if path is None:
        _HALF_LIVES = out
    return out


def half_life_of(nuclide):
    """Half-life in seconds for a nuclide named as in Appendix A.4, e.g. '137Cs'."""
    t = load_half_lives()
    if nuclide not in t:
        raise KeyError("no half-life tabulated for %r" % (nuclide,))
    return t[nuclide]


# --- demo --------------------------------------------------------------------

_YEAR = SECONDS_PER["y"]


def _demo():
    print("NE-06  decay kinetics\n")
    hl = load_half_lives()
    print("  half-lives parsed from Appendix A.4 (%d nuclides)" % len(hl))
    print("   nuclide   T_1/2            lambda (1/s)     mean life")
    for n, A in [("3H", 3), ("14C", 14), ("60Co", 60), ("90Sr", 90),
                 ("137Cs", 137), ("131I", 131), ("235U", 235), ("238U", 238)]:
        if n not in hl:
            continue
        T = hl[n]
        print("   %-8s %11.4g s   %12.4e   %11.4g s"
              % (n, T, decay_constant(T), mean_lifetime(lam=decay_constant(T))))

    print("\n  the mean life is 1.44 half-lives, not one")
    print("   T_av / T_1/2 = 1/ln2 = %.6f" % (1.0 / LN2))

    print("\n  specific activity: short-lived means intensely radioactive")
    print("   nuclide   T_1/2            Bq/g         Ci/g")
    for n, A in [("3H", 3), ("60Co", 60), ("90Sr", 90), ("137Cs", 137),
                 ("226Ra", 226), ("235U", 235), ("238U", 238)]:
        if n not in hl or not math.isfinite(hl[n]):
            continue
        sa = specific_activity(hl[n], A)
        print("   %-8s %11.4g s   %10.4e   %10.4e" % (n, hl[n], sa, curies(sa)))

    print("\n  the curie was defined as the activity of one gram of 226Ra")
    sa_ra = specific_activity(hl["226Ra"], 226)
    print("   computed: %.4e Bq/g = %.4f Ci/g   (definition: 1 Ci = 3.7e10 Bq)"
          % (sa_ra, curies(sa_ra)))

    print("\n  decay of a 1 Ci 60Co source")
    T = hl["60Co"]
    print("     years    activity (Ci)   fraction left")
    for yr in (0, 1, 5.27, 10, 30):
        f = fraction_remaining(yr * _YEAR, T)
        print("   %7.2f   %13.4f   %12.5f" % (yr, f, f))

    print("\n  competing channels add rates, not half-lives")
    lam_a, lam_b = 0.7, 0.3
    print("   two channels with lambda = %.1f and %.1f /s" % (lam_a, lam_b))
    print("   total lambda = %.1f /s, T_1/2 = %.4f s"
          % (total_decay_constant([lam_a, lam_b]),
             half_life(total_decay_constant([lam_a, lam_b]))))
    print("   branching fractions: %s" % ["%.2f" % f for f in branching_fractions([lam_a, lam_b])])
    print("   partial half-life of the 70%% channel: %.4f s (vs %.4f s observed)"
          % (partial_half_life(half_life(1.0), 0.7), half_life(1.0)))


if __name__ == "__main__":
    _demo()
