"""NE-06 tests -- decay kinetics against Shultis & Faw §5.5 and the half-lives
of Appendix A.4.

Run:  python3 test_decay_kinetics.py
"""

import math

from decay_kinetics import (
    LN2, AVOGADRO, BQ_PER_CI, SECONDS_PER,
    decay_constant, half_life, mean_lifetime,
    number_remaining, fraction_remaining, half_lives_elapsed,
    activity, activity_at_time, specific_activity,
    survival_probability, decay_probability, decay_time_pdf,
    time_to_fraction, time_to_activity,
    total_decay_constant, branching_fractions, partial_half_life,
    parse_half_life, load_half_lives, half_life_of,
    curies, becquerels,
)

YEAR = SECONDS_PER["y"]


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --- the exponential law -----------------------------------------------------

def test_decay_constant_and_half_life_are_inverses():
    for T in (1.0, 12.32 * YEAR, 4.468e9 * YEAR):
        lam = decay_constant(T)
        assert _approx(half_life(lam), T)
        assert _approx(lam * T, LN2)


def test_mean_life_is_1_44_half_lives():
    """T_av = 1/lambda = T/ln2 [Eq. (5.44)] -- the exponential tail pulls the
    mean above the median."""
    T = 10.0
    assert _approx(mean_lifetime(t_half=T), T / LN2)
    assert _approx(mean_lifetime(t_half=T) / T, 1.442695, tol=1e-6)
    assert mean_lifetime(t_half=T) > T


def test_halving_every_half_life():
    """N(T) = N0/2, N(2T) = N0/4, ... [Eqs. (5.34), (5.39)]."""
    T, N0 = 7.0, 1000.0
    for k in range(6):
        assert _approx(number_remaining(N0, k * T, T), N0 / 2 ** k, tol=1e-9)
    assert _approx(fraction_remaining(3 * T, T), 0.125)


def test_half_lives_elapsed_inverts_the_fraction():
    """Eq. (5.38): n = -log2(f)."""
    assert _approx(half_lives_elapsed(0.5), 1.0)
    assert _approx(half_lives_elapsed(0.25), 2.0)
    assert _approx(half_lives_elapsed(1.0), 0.0)
    assert _approx(half_lives_elapsed(0.001), 9.9658, tol=1e-4)
    for f in (0.9, 0.3, 0.01):
        T = 5.0
        assert _approx(fraction_remaining(half_lives_elapsed(f) * T, T), f, tol=1e-9)


def test_decay_is_memoryless():
    """Survival is exp(-lambda t) regardless of prior age -- the defining
    property [Eq. (5.40)], and the reason 'the age of a nucleus' is meaningless."""
    T = 3.0
    for age in (0.0, 1.0, 10.0, 100.0):
        cond = fraction_remaining(age + T, T) / fraction_remaining(age, T)
        assert _approx(cond, 0.5, tol=1e-9)


def test_probability_identities():
    T = 4.0
    for t in (0.5, 2.0, 9.0):
        assert _approx(survival_probability(t, T) + decay_probability(t, T), 1.0)
    # small-time limit P ~ lambda t  [Eq. (5.42)]
    lam = decay_constant(T)
    dt = 1e-6
    assert _approx(decay_probability(dt, T), lam * dt, tol=1e-5)


def test_decay_time_density_normalises_and_has_the_right_mean():
    """p(t) = lambda exp(-lambda t) [Eq. (5.43)]; its integral is 1 and its mean
    is 1/lambda [Eq. (5.44)].  Integrated numerically."""
    T = 2.0
    lam = decay_constant(T)
    n, tmax = 200000, 40.0 / lam
    h = tmax / n
    total = mean = 0.0
    for i in range(n):
        t = (i + 0.5) * h
        p = decay_time_pdf(t, lam=lam)
        total += p * h
        mean += t * p * h
    assert _approx(total, 1.0, tol=1e-4)
    assert _approx(mean, 1.0 / lam, tol=1e-4)
    assert decay_time_pdf(-1.0, T) == 0.0


# --- activity  [Eq. (5.45)] --------------------------------------------------

def test_activity_and_its_decay():
    T, N0 = 5.0, 1e12
    lam = decay_constant(T)
    assert _approx(activity(N0, T), lam * N0)
    assert _approx(activity_at_time(activity(N0, T), T, T), 0.5 * activity(N0, T))
    # activity and population share the same decay constant
    assert _approx(activity(number_remaining(N0, 3 * T, T), T),
                   activity_at_time(activity(N0, T), 3 * T, T))


def test_time_to_activity_inverts():
    T = 30.17 * YEAR
    t = time_to_activity(100.0, 12.5, T)
    assert _approx(t, 3 * T, tol=1e-9)


def test_curie_units():
    assert _approx(becquerels(1.0), 3.7e10)
    assert _approx(curies(3.7e10), 1.0)
    assert _approx(curies(becquerels(5.0)), 5.0)


def test_one_gram_of_radium_is_about_one_curie():
    """The curie was originally defined as the activity of 1 g of 226Ra.  With
    the modern fixed definition (1 Ci = 3.7e10 Bq exactly) and the currently
    accepted radium half-life, a gram comes out at 0.989 Ci -- the 1% gap is the
    later revision of the half-life, not an arithmetic error."""
    T = half_life_of("226Ra")
    sa = specific_activity(T, 226)
    assert _approx(curies(sa), 0.9886, tol=1e-3)
    assert 0.97 < curies(sa) < 1.01


def test_specific_activity_is_inverse_in_half_life():
    """Short-lived means intensely radioactive.  Checked against standard values."""
    hl = load_half_lives()
    for nuc, A, expect_ci_per_g in [("3H", 3, 9672.0), ("60Co", 60, 1130.3),
                                    ("90Sr", 90, 137.97), ("137Cs", 137, 86.50)]:
        sa = curies(specific_activity(hl[nuc], A))
        assert _approx(sa, expect_ci_per_g, tol=2e-3), "%s: %.2f Ci/g" % (nuc, sa)
    # 238U, with a 4.5 Gy half-life, is a billion times weaker per gram than 3H
    sa_u = specific_activity(hl["238U"], 238)
    sa_h = specific_activity(hl["3H"], 3)
    assert sa_h / sa_u > 1e10


# --- competing channels  [Eqs. (5.47)-(5.49)] ------------------------------

def test_channels_add_rates_not_half_lives():
    lams = [0.7, 0.3]
    assert _approx(total_decay_constant(lams), 1.0)
    assert _approx(half_life(1.0), LN2)
    # the combined half-life is SHORTER than either channel's alone
    assert half_life(total_decay_constant(lams)) < half_life(0.7)
    assert half_life(total_decay_constant(lams)) < half_life(0.3)


def test_branching_fractions_sum_to_one():
    for lams in ([0.7, 0.3], [1.0, 2.0, 3.0], [5.0]):
        f = branching_fractions(lams)
        assert _approx(sum(f), 1.0)
        assert all(0 <= x <= 1 for x in f)
    assert _approx(branching_fractions([0.7, 0.3])[0], 0.7)


def test_partial_half_life_exceeds_the_observed_one():
    """A channel taking only a fraction f of decays would, alone, give a
    half-life T/f -- always longer than what is observed."""
    T = 1.28e9 * YEAR
    for f in (0.8928, 0.1072):          # the 40K branching ratios
        assert partial_half_life(T, f) > T
        assert _approx(partial_half_life(T, f) * f, T)


# --- half-life parsing from Appendix A.4 ------------------------------------

def test_parse_half_life_units():
    assert _approx(parse_half_life("1 s"), 1.0)
    assert _approx(parse_half_life("1 min"), 60.0)
    assert _approx(parse_half_life("1 h"), 3600.0)
    assert _approx(parse_half_life("1 d"), 86400.0)
    assert _approx(parse_half_life("1 y"), YEAR)
    assert _approx(parse_half_life("1 ky"), 1e3 * YEAR)
    assert _approx(parse_half_life("1 My"), 1e6 * YEAR)
    assert _approx(parse_half_life("1 Gy"), 1e9 * YEAR)
    assert _approx(parse_half_life("1 Ey"), 1e18 * YEAR)
    assert parse_half_life("stable") == math.inf
    assert _approx(parse_half_life(">600 Ty"), 600e12 * YEAR)   # 123Te
    for bad in ("12.3 fortnights", "soon"):
        try:
            parse_half_life(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should not parse" % bad)


def test_known_half_lives_from_appendix_a4():
    """Spot-check against values every nuclear engineer knows."""
    hl = load_half_lives()
    assert len(hl) > 800
    checks = [("3H", 12.32 * YEAR), ("14C", 5700 * YEAR), ("60Co", 5.2714 * YEAR),
              ("90Sr", 28.79 * YEAR), ("137Cs", 30.17 * YEAR),
              ("131I", 8.0233 * 86400.0), ("226Ra", 1600 * YEAR),
              ("235U", 704e6 * YEAR), ("238U", 4.468e9 * YEAR),
              ("239Pu", 24110 * YEAR)]
    for nuc, expect in checks:
        assert nuc in hl, nuc
        assert _approx(hl[nuc], expect, tol=5e-3), \
            "%s: %.4g s vs expected %.4g s" % (nuc, hl[nuc], expect)
    # stable nuclides are infinite
    assert hl["12C"] == math.inf
    assert hl["56Fe"] == math.inf


def test_half_life_of_raises_for_unknown():
    try:
        half_life_of("999Zz")
    except KeyError:
        pass
    else:
        raise AssertionError("unknown nuclide should raise")


def test_invalid_inputs_raise():
    for fn, args in [(decay_constant, (0,)), (decay_constant, (-1,)),
                     (half_life, (0,)), (half_lives_elapsed, (0,)),
                     (half_lives_elapsed, (1.5,)), (specific_activity, (0, 12))]:
        try:
            fn(*args)
        except ValueError:
            pass
        else:
            raise AssertionError("%s%r should be rejected" % (fn.__name__, args))


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
