"""NE-07  Decay chains, equilibria and radiodating.

Nuclear Science & Engineering trunk, module NE-07 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Sections 5.6-5.9 (printed pp. 117-131).  Pure stdlib; half-lives from
../../data_tables/A4_isotopic_abundances.csv.

~NE-06 handled one nuclide decaying on its own.  Real radioactivity comes in
chains: a parent decays to a daughter that decays in turn, and each member is
simultaneously being created and destroyed.  Adding a source term to the
first-order equation of ~NE-06,

    dN/dt = -lambda N + Q(t)                                    [S&F Eq. 5.51]

covers both production by irradiation (Q constant) and production by a parent's
decay (Q = lambda_1 N_1).  The chain version is the Bateman system, whose
solution for a pure parent at t=0 is a sum of exponentials with coefficients
fixed entirely by the decay constants.

Two limits matter more than the general solution.  When the parent is much
longer-lived than everything below it -- the natural uranium and thorium series,
where the parent's half-life is billions of years and the daughters' are days --
the chain reaches *secular equilibrium* and every member has the SAME activity.
That single fact explains radon in basements, radium in ore, and the whole
business of dating rocks.
"""

import csv
import math
import os

__all__ = [
    "LN2", "SECONDS_PER",
    "decay_with_production", "equilibrium_number", "approach_fraction",
    "bateman_coefficients", "bateman_activity", "bateman_number",
    "two_component_chain", "daughter_maximum_time",
    "secular_equilibrium_activities", "is_secular", "is_transient",
    "activity_ratio", "series_of", "NATURAL_SERIES",
    "age_from_parent_fraction", "age_from_daughter_ratio", "K40_TO_AR40_BRANCH",
    "carbon14_age", "CARBON14_MODERN_DPM_PER_G",
    "parse_half_life", "load_half_lives", "half_life_of", "decay_constant",
]

LN2 = math.log(2.0)

SECONDS_PER = {
    "ys": 1e-24, "zs": 1e-21, "as": 1e-18, "fs": 1e-15, "ps": 1e-12,
    "ns": 1e-9, "us": 1e-6, "µs": 1e-6, "ms": 1e-3, "s": 1.0,
    "min": 60.0, "h": 3600.0, "d": 86400.0, "y": 365.25 * 86400.0,
}
for _p, _m in (("k", 1e3), ("M", 1e6), ("G", 1e9), ("T", 1e12),
               ("P", 1e15), ("E", 1e18), ("Z", 1e21), ("Y", 1e24)):
    SECONDS_PER[_p + "y"] = SECONDS_PER["y"] * _m

# specific activity of 14C in living matter, the radiocarbon reference
CARBON14_MODERN_DPM_PER_G = 13.56          # disintegrations per minute per gram of carbon

# The four decay series, labelled by A mod 4.  Only three occur naturally: the
# 4n+1 (neptunium) series has no member long-lived enough to have survived.
NATURAL_SERIES = {
    0: ("thorium", "232Th", "208Pb", 1.405e10),
    1: ("neptunium", "237Np", "209Bi", 2.144e6),
    2: ("uranium", "238U", "206Pb", 4.468e9),
    3: ("actinium", "235U", "207Pb", 7.038e8),
}

_HALF_LIVES = None


def decay_constant(t_half):
    if t_half <= 0:
        raise ValueError("half-life must be positive")
    return LN2 / t_half


# --- decay with production  [S&F Eqs. (5.51)-(5.53), printed p. 117] -------

def decay_with_production(n0, q0, t, t_half=None, lam=None):
    """N(t) = N0 exp(-lambda t) + (Q0/lambda)[1 - exp(-lambda t)]  [Eq. (5.53)].

    Constant production Q0 against first-order loss.  Whatever N0 is, the
    population is driven toward Q0/lambda -- the activity toward Q0 itself."""
    if lam is None:
        lam = decay_constant(t_half)
    if t < 0:
        raise ValueError("time must be non-negative")
    e = math.exp(-lam * t)
    return n0 * e + (q0 / lam) * (1.0 - e)


def equilibrium_number(q0, t_half=None, lam=None):
    """N_e = Q0/lambda, the saturation population  [S&F p. 118].

    At equilibrium the activity lambda*N_e equals the production rate Q0
    exactly: you cannot make a source more active than you are creating it."""
    if lam is None:
        lam = decay_constant(t_half)
    return q0 / lam


def approach_fraction(t, t_half=None, lam=None):
    """Fraction of the equilibrium value reached after time t, 1 - exp(-lambda t).

    Saturation is 50% after one half-life, 75% after two, 97% after five --
    the rule of thumb for irradiation times in ~NE-26."""
    if lam is None:
        lam = decay_constant(t_half)
    return 1.0 - math.exp(-lam * t)


# --- the Bateman chain  [S&F Eqs. (5.68)-(5.70), printed pp. 122-123] -----

def bateman_coefficients(lambdas, j=None):
    """Coefficients C_m of the Bateman solution  [Eq. (5.70)]:

        C_m = (prod_{i=1..j} lambda_i) / (prod_{i=1..j, i!=m} (lambda_i - lambda_m))

    for the j-th chain member.  Requires distinct decay constants; equal ones
    make the denominator vanish and need a separate (degenerate) treatment."""
    lams = list(lambdas)
    if j is None:
        j = len(lams)
    if not 1 <= j <= len(lams):
        raise ValueError("j must index a chain member")
    lams = lams[:j]
    if any(l <= 0 for l in lams):
        raise ValueError("decay constants must be positive")
    num = 1.0
    for l in lams:
        num *= l
    out = []
    for m, lm in enumerate(lams):
        den = 1.0
        for i, li in enumerate(lams):
            if i == m:
                continue
            d = li - lm
            if d == 0.0:
                raise ValueError("Bateman solution requires distinct decay constants")
            den *= d
        out.append(num / den)
    return out


def bateman_activity(lambdas, n1_0, t, j=None):
    """Activity of chain member j at time t, for a pure parent at t=0
    [Eq. (5.69)]:  A_j(t) = N1(0) sum_m C_m exp(-lambda_m t)."""
    lams = list(lambdas)
    if j is None:
        j = len(lams)
    C = bateman_coefficients(lams, j)
    return n1_0 * sum(c * math.exp(-l * t) for c, l in zip(C, lams[:j]))


def bateman_number(lambdas, n1_0, t, j=None):
    """Population of chain member j: N_j = A_j / lambda_j."""
    lams = list(lambdas)
    if j is None:
        j = len(lams)
    return bateman_activity(lams, n1_0, t, j) / lams[j - 1]


def two_component_chain(lam1, lam2, n1_0, t):
    """(N1, N2) for parent -> daughter -> stable, the case worth knowing by heart:

        N1 = N1(0) exp(-lam1 t)
        N2 = N1(0) lam1/(lam2-lam1) [exp(-lam1 t) - exp(-lam2 t)] .
    """
    if lam1 == lam2:
        raise ValueError("equal decay constants need the degenerate solution")
    n1 = n1_0 * math.exp(-lam1 * t)
    n2 = n1_0 * lam1 / (lam2 - lam1) * (math.exp(-lam1 * t) - math.exp(-lam2 * t))
    return n1, n2


def daughter_maximum_time(lam1, lam2):
    """Time at which the daughter population peaks:

        t_max = ln(lam2/lam1) / (lam2 - lam1) .

    Before this the daughter is building up, after it the parent's supply is
    failing faster than the daughter decays.  This is what sets the optimum
    'milking' interval for a radionuclide generator (~NE-27)."""
    if lam1 <= 0 or lam2 <= 0:
        raise ValueError("decay constants must be positive")
    if lam1 == lam2:
        raise ValueError("equal decay constants need the degenerate solution")
    return math.log(lam2 / lam1) / (lam2 - lam1)


# --- equilibria  [S&F §5.7.4, Eqs. (5.71)-(5.72), printed p. 125] ---------

def secular_equilibrium_activities(a_parent, n_members):
    """Under secular equilibrium every chain member has the parent's activity
    [Eq. (5.72)]:  A0 = A1 = ... = A_{n-1}."""
    if n_members < 1:
        raise ValueError("need at least one member")
    return [a_parent] * n_members


def is_secular(t_half_parent, t_half_daughter, ratio=1e3):
    """True when the parent outlives the daughter by at least `ratio`.

    In that limit the parent's activity is effectively constant over the
    daughter's lifetime, and the chain settles to equal activities."""
    return t_half_parent / t_half_daughter >= ratio


def is_transient(t_half_parent, t_half_daughter):
    """True when the parent merely outlives the daughter (transient equilibrium).

    Here the daughter's activity settles to a *fixed multiple* of the parent's,
    A2/A1 = lam2/(lam2-lam1) > 1, and the pair then decays with the parent's
    half-life -- the regime of the 99Mo/99mTc generator (~NE-27)."""
    return 1.0 < t_half_parent / t_half_daughter < 1e3


def activity_ratio(lam1, lam2):
    """Asymptotic daughter-to-parent activity ratio, lam2/(lam2 - lam1).

    Tends to 1 for secular equilibrium (lam1 << lam2) and exceeds 1 in transient
    equilibrium.  Undefined when the daughter is the longer-lived of the two --
    no equilibrium is reached at all."""
    if lam2 <= lam1:
        raise ValueError("no equilibrium: the daughter must be shorter-lived")
    return lam2 / (lam2 - lam1)


def series_of(A):
    """Which natural decay series a mass number belongs to: 4n, 4n+1, 4n+2, 4n+3.

    Alpha decay changes A by 4 and beta decay not at all, so A mod 4 is
    conserved along a chain -- which is why there are exactly four series."""
    if A != int(A) or A < 1:
        raise ValueError("mass number must be a positive integer")
    return NATURAL_SERIES[int(A) % 4]


# --- radiodating  [S&F §5.8, printed pp. 128-131] --------------------------

def age_from_parent_fraction(fraction, t_half=None, lam=None):
    """Age from the surviving parent fraction  [S&F §5.8.1]:

        t = (1/lambda) ln(N0/N) .

    Needs a known initial amount, which is the hard part -- radiocarbon gets it
    from the atmosphere, and that assumption is the method's weak point."""
    if lam is None:
        lam = decay_constant(t_half)
    if not 0 < fraction <= 1:
        raise ValueError("fraction must lie in (0, 1]")
    return -math.log(fraction) / lam


def age_from_daughter_ratio(daughter_over_parent, t_half=None, lam=None,
                            branch_fraction=1.0):
    """Age from the accumulated *stable* daughter  [S&F §5.8.2]:

        N_D = N_P(e^{lambda t} - 1)  =>  t = (1/lambda) ln(1 + N_D/N_P) .

    Needs no initial-amount assumption -- only that no daughter was present at
    t=0 and none has escaped since.  This is the basis of U/Pb and K/Ar dating,
    and why it reaches back billions of years while radiocarbon stops at ~50 ky.

    `branch_fraction` is the share of decays that actually produce the daughter
    being counted.  It is 1.0 for 238U -> 206Pb, but only 0.1072 for
    40K -> 40Ar, because 89% of 40K decays go to 40Ca instead.  Omitting it
    makes a K/Ar rock look far younger than it is."""
    if lam is None:
        lam = decay_constant(t_half)
    if daughter_over_parent < 0:
        raise ValueError("ratio must be non-negative")
    if not 0 < branch_fraction <= 1:
        raise ValueError("branch fraction must lie in (0, 1]")
    return math.log(1.0 + daughter_over_parent / branch_fraction) / lam


# branching ratio of 40K to 40Ar (electron capture); the rest goes to 40Ca
K40_TO_AR40_BRANCH = 0.1072


def carbon14_age(measured_dpm_per_g, modern=CARBON14_MODERN_DPM_PER_G,
                 t_half=None):
    """Radiocarbon age in years from the specific activity of the sample.

    Uses the Libby convention's reference activity for living matter; the
    half-life defaults to the Appendix A.4 value for 14C."""
    if t_half is None:
        t_half = half_life_of("14C")
    if measured_dpm_per_g <= 0:
        raise ValueError("activity must be positive")
    return age_from_parent_fraction(measured_dpm_per_g / modern,
                                    t_half=t_half) / SECONDS_PER["y"]


# --- half-lives from the extracted Appendix A.4 -----------------------------

def parse_half_life(text):
    """'12.32 y' -> seconds; 'stable' -> math.inf."""
    import re
    s = str(text).strip()
    if not s or s.lower() == "stable":
        return math.inf
    m = re.match(r"^\s*([<>~≃]?)\s*([0-9]*\.?[0-9]+)\s*([A-Za-zµ]+)\s*$", s)
    if not m:
        raise ValueError("cannot parse half-life %r" % (text,))
    _rel, value, unit = m.groups()
    if unit not in SECONDS_PER:
        raise ValueError("unknown time unit %r in %r" % (unit, text))
    return float(value) * SECONDS_PER[unit]


def load_half_lives(path=None):
    """{nuclide: half_life_seconds} from the extracted Appendix A.4.  Cached."""
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
    t = load_half_lives()
    if nuclide not in t:
        raise KeyError("no half-life tabulated for %r" % (nuclide,))
    return t[nuclide]


# --- demo --------------------------------------------------------------------

_Y = SECONDS_PER["y"]


def _demo():
    hl = load_half_lives()
    print("NE-07  decay chains, equilibria and dating\n")

    print("  decay with constant production: saturation at Q0/lambda")
    T = 14.96 * 3600            # 24Na
    print("   half-lives   fraction of saturation")
    for k in (0.5, 1, 2, 3, 5, 10):
        print("   %8.1f   %20.4f" % (k, approach_fraction(k * T, T)))

    print("\n  two-component chain, 99Mo (66 h) -> 99mTc (6.01 h)")
    l1, l2 = decay_constant(66.0 * 3600), decay_constant(6.01 * 3600)
    tmax = daughter_maximum_time(l1, l2) / 3600
    print("   daughter peaks at t = %.2f h; asymptotic A2/A1 = %.4f"
          % (tmax, activity_ratio(l1, l2)))
    print("   transient equilibrium? %s   secular? %s"
          % (is_transient(66.0, 6.01), is_secular(66.0, 6.01)))

    print("\n  the four decay series (A mod 4 is conserved along a chain)")
    for r in (0, 1, 2, 3):
        name, parent, end, t_y = NATURAL_SERIES[r]
        natural = "yes" if t_y > 1e8 else "no (extinct)"
        print("   4n+%d  %-10s %-7s -> %-7s  T=%9.3e y   still present: %s"
              % (r, name, parent, end, t_y, natural))

    print("\n  secular equilibrium in the uranium series")
    print("   every member has the same activity as 238U, so a sealed ore sample")
    print("   holds equal activities of 238U, 234U, 230Th, 226Ra, 222Rn, 210Pb, ...")
    for nuc in ("238U", "234U", "230Th", "226Ra", "222Rn", "210Pb", "210Po"):
        if nuc in hl and math.isfinite(hl[nuc]):
            print("     %-7s T_1/2 = %11.4g y   secular vs 238U: %s"
                  % (nuc, hl[nuc] / _Y, is_secular(hl["238U"], hl[nuc])))

    print("\n  radiodating")
    T14 = hl["14C"]
    print("   14C half-life %.4g y; modern activity %.2f dpm/g"
          % (T14 / _Y, CARBON14_MODERN_DPM_PER_G))
    for dpm in (13.56, 6.78, 3.39, 1.70, 0.85):
        print("     %6.2f dpm/g  ->  %9.0f years" % (dpm, abs(carbon14_age(dpm))))
    print("   practical limit ~ 10 half-lives = %.0f y before the count rate"
          % (10 * T14 / _Y))
    print("   is lost in background")

    print("\n   U/Pb: a rock with N(206Pb)/N(238U) = 0.1 is")
    print("     %.3e years old" % (age_from_daughter_ratio(0.1, hl["238U"]) / _Y))
    print("   K/Ar: 40Ar/40K = 1.0, ignoring branching, gives %.3e years"
          % (age_from_daughter_ratio(1.0, hl["40K"]) / _Y))
    print("         with the 10.72%% EC branch to 40Ar:      %.3e years"
          % (age_from_daughter_ratio(1.0, hl["40K"],
                                     branch_fraction=K40_TO_AR40_BRANCH) / _Y))


if __name__ == "__main__":
    _demo()
