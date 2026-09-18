"""NE-07 tests -- chains, equilibria and dating against Shultis & Faw §§5.6-5.9.

Run:  python3 test_decay_chains.py
"""

import math

from decay_chains import (
    LN2, SECONDS_PER, decay_constant,
    decay_with_production, equilibrium_number, approach_fraction,
    bateman_coefficients, bateman_activity, bateman_number,
    two_component_chain, daughter_maximum_time,
    secular_equilibrium_activities, is_secular, is_transient,
    activity_ratio, series_of, NATURAL_SERIES,
    age_from_parent_fraction, age_from_daughter_ratio, K40_TO_AR40_BRANCH,
    carbon14_age, CARBON14_MODERN_DPM_PER_G,
    load_half_lives, half_life_of,
)

YEAR = SECONDS_PER["y"]
HL = load_half_lives()


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --- decay with production  [Eqs. (5.51)-(5.53)] ---------------------------

def test_saturation_at_q_over_lambda():
    """N -> Q0/lambda as t -> infinity, so the activity approaches Q0 itself."""
    T, Q0 = 10.0, 500.0
    lam = decay_constant(T)
    assert _approx(equilibrium_number(Q0, T), Q0 / lam)
    late = decay_with_production(0.0, Q0, 40 * T, T)
    assert _approx(late, Q0 / lam, tol=1e-6)
    # activity at saturation equals the production rate
    assert _approx(lam * (Q0 / lam), Q0)


def test_saturation_fractions():
    """50% after one half-life, 75% after two, 96.9% after five."""
    T = 3.0
    assert _approx(approach_fraction(T, T), 0.5)
    assert _approx(approach_fraction(2 * T, T), 0.75)
    assert _approx(approach_fraction(5 * T, T), 0.96875)
    assert approach_fraction(10 * T, T) > 0.999


def test_production_solution_satisfies_the_ode():
    """dN/dt = -lambda N + Q0, checked by central differences [Eq. (5.51)]."""
    T, Q0, N0 = 7.0, 20.0, 100.0
    lam = decay_constant(T)
    for t in (1.0, 5.0, 20.0):
        h = 1e-5
        dN = (decay_with_production(N0, Q0, t + h, T)
              - decay_with_production(N0, Q0, t - h, T)) / (2 * h)
        rhs = -lam * decay_with_production(N0, Q0, t, T) + Q0
        assert _approx(dN, rhs, tol=1e-6)


def test_starting_above_equilibrium_decays_down_to_it():
    T, Q0 = 5.0, 10.0
    lam = decay_constant(T)
    Ne = Q0 / lam
    assert decay_with_production(3 * Ne, Q0, T, T) < 3 * Ne
    assert decay_with_production(3 * Ne, Q0, 30 * T, T) > Ne * 0.999
    assert _approx(decay_with_production(Ne, Q0, 12.3, T), Ne, tol=1e-9)


# --- the Bateman solution  [Eqs. (5.68)-(5.70)] ---------------------------

def test_bateman_reduces_to_simple_decay_for_one_member():
    lam = 0.3
    assert _approx(bateman_coefficients([lam], 1)[0], lam)
    for t in (0.0, 1.0, 5.0):
        assert _approx(bateman_activity([lam], 1000.0, t, 1),
                       lam * 1000.0 * math.exp(-lam * t))


def test_bateman_two_member_matches_the_closed_form():
    """The j=2 Bateman coefficients must reproduce
    N2 = N1(0) lam1/(lam2-lam1)[exp(-lam1 t) - exp(-lam2 t)]."""
    lam1, lam2, N0 = 0.2, 0.9, 1000.0
    for t in (0.5, 2.0, 8.0):
        n1, n2 = two_component_chain(lam1, lam2, N0, t)
        assert _approx(bateman_number([lam1, lam2], N0, t, 1), n1, tol=1e-9)
        assert _approx(bateman_number([lam1, lam2], N0, t, 2), n2, tol=1e-9)


def test_bateman_satisfies_the_chain_odes():
    """dN2/dt = lam1 N1 - lam2 N2, checked numerically for a three-member chain."""
    lams = [0.15, 0.6, 1.3]
    N0 = 1000.0
    h = 1e-6
    for t in (0.7, 3.0):
        for j in (2, 3):
            dN = (bateman_number(lams, N0, t + h, j)
                  - bateman_number(lams, N0, t - h, j)) / (2 * h)
            rhs = (lams[j - 2] * bateman_number(lams, N0, t, j - 1)
                   - lams[j - 1] * bateman_number(lams, N0, t, j))
            assert _approx(dN, rhs, tol=1e-4), (t, j)


def test_daughters_start_at_zero_and_the_parent_at_n0():
    lams = [0.2, 0.7, 1.1]
    N0 = 500.0
    assert _approx(bateman_number(lams, N0, 0.0, 1), N0)
    for j in (2, 3):
        assert abs(bateman_number(lams, N0, 0.0, j)) < 1e-9


def test_bateman_rejects_degenerate_constants():
    try:
        bateman_coefficients([0.5, 0.5])
    except ValueError:
        pass
    else:
        raise AssertionError("equal decay constants should be rejected")


def test_daughter_peaks_where_its_derivative_vanishes():
    """t_max = ln(lam2/lam1)/(lam2-lam1): at that instant production equals loss,
    so lam1 N1 = lam2 N2."""
    lam1, lam2, N0 = 0.05, 0.4, 1000.0
    tmax = daughter_maximum_time(lam1, lam2)
    n1, n2 = two_component_chain(lam1, lam2, N0, tmax)
    assert _approx(lam1 * n1, lam2 * n2, tol=1e-9)
    # and it really is a maximum
    _, before = two_component_chain(lam1, lam2, N0, tmax - 0.1)
    _, after = two_component_chain(lam1, lam2, N0, tmax + 0.1)
    assert n2 > before and n2 > after


def test_technetium_generator_milking_interval():
    """99Mo (66 h) -> 99mTc (6.01 h): the daughter peaks near 23 h, which is why
    a technetium generator is eluted about once a day (~NE-27)."""
    l1 = decay_constant(66.0 * 3600)
    l2 = decay_constant(6.01 * 3600)
    tmax = daughter_maximum_time(l1, l2) / 3600.0
    assert 22.0 < tmax < 24.0
    assert is_transient(66.0, 6.01)
    assert not is_secular(66.0, 6.01)
    assert _approx(activity_ratio(l1, l2), 1.1002, tol=1e-3)


# --- equilibria  [Eqs. (5.71)-(5.72)] --------------------------------------

def test_secular_equilibrium_gives_equal_activities():
    """A0 = A1 = ... = A_{n-1} [Eq. (5.72)] -- the defining property."""
    assert secular_equilibrium_activities(37.0, 4) == [37.0] * 4
    # numerically: a long-lived parent with a short-lived daughter equalises
    lam1 = decay_constant(1e6)
    lam2 = decay_constant(1.0)
    N0 = 1e12
    t = 20.0                       # many daughter half-lives, no parent decay
    n1, n2 = two_component_chain(lam1, lam2, N0, t)
    assert _approx(lam1 * n1, lam2 * n2, tol=1e-4)


def test_uranium_series_members_are_secular_with_the_parent():
    """238U outlives every daughter by orders of magnitude, so an undisturbed
    ore sample holds equal activities all the way down the chain."""
    parent = HL["238U"]
    for nuc in ("234U", "230Th", "226Ra", "222Rn", "210Pb", "210Po"):
        assert math.isfinite(HL[nuc])
        assert is_secular(parent, HL[nuc]), nuc
    # the equal-activity claim is what makes radon a problem: 222Rn has the
    # same activity as the 238U in the rock beneath a house
    assert HL["222Rn"] < HL["238U"] / 1e10


def test_activity_ratio_tends_to_one_in_the_secular_limit():
    for ratio in (10.0, 1e3, 1e6):
        lam1, lam2 = 1.0 / ratio, 1.0
        r = activity_ratio(lam1, lam2)
        assert r > 1.0
        if ratio >= 1e3:
            assert _approx(r, 1.0, tol=2e-3)
    try:
        activity_ratio(1.0, 0.5)        # daughter longer-lived: no equilibrium
    except ValueError:
        pass
    else:
        raise AssertionError("should refuse when the daughter outlives the parent")


# --- the four series ---------------------------------------------------------

def test_four_series_by_A_mod_4():
    """Alpha decay changes A by 4 and beta not at all, so A mod 4 is a chain
    invariant -- hence exactly four series."""
    assert series_of(238)[1] == "238U"
    assert series_of(235)[1] == "235U"
    assert series_of(232)[1] == "232Th"
    assert series_of(237)[1] == "237Np"
    # members of a chain stay in their series
    for A in (238, 234, 230, 226, 222, 218, 214, 210, 206):
        assert series_of(A)[0] == "uranium"
    for A in (232, 228, 224, 220, 216, 212, 208):
        assert series_of(A)[0] == "thorium"


def test_neptunium_series_is_extinct():
    """Its parent's 2.14 My half-life is far too short to have survived the
    4.5 Gy age of the Earth -- which is why only three series occur naturally."""
    _name, _parent, _end, t_y = NATURAL_SERIES[1]
    assert t_y < 1e7
    earth_age = 4.5e9
    surviving = math.exp(-LN2 * earth_age / t_y)
    assert surviving < 1e-600 or surviving == 0.0
    for r in (0, 2, 3):
        assert NATURAL_SERIES[r][3] > 1e8


# --- radiodating  [§5.8] ----------------------------------------------------

def test_age_from_parent_fraction():
    T = 5700 * YEAR
    assert _approx(age_from_parent_fraction(0.5, T), T)
    assert _approx(age_from_parent_fraction(0.25, T), 2 * T)
    assert _approx(age_from_parent_fraction(1.0, T), 0.0)


def test_carbon14_dating():
    """Half the modern activity is exactly one half-life old."""
    assert _approx(carbon14_age(CARBON14_MODERN_DPM_PER_G), 0.0, tol=1e-9)
    assert _approx(carbon14_age(CARBON14_MODERN_DPM_PER_G / 2), 5700.0, tol=1e-3)
    assert _approx(carbon14_age(CARBON14_MODERN_DPM_PER_G / 4), 11400.0, tol=1e-3)
    # older samples give lower activity; 0.1 dpm/g is already ~40 ky
    assert _approx(carbon14_age(0.1), 40375.0, tol=1e-3)
    # the method runs out around ten half-lives, where a gram of carbon yields
    # about one count per hour -- hopeless against detector background (~NE-16)
    ten_half_lives = CARBON14_MODERN_DPM_PER_G / 1024.0
    assert _approx(carbon14_age(ten_half_lives), 57000.0, tol=1e-3)
    assert ten_half_lives < 0.02
    try:
        carbon14_age(0.0)
    except ValueError:
        pass
    else:
        raise AssertionError("zero activity should be rejected")


def test_daughter_ratio_dating_needs_no_initial_amount():
    """t = (1/lambda) ln(1 + N_D/N_P).  A ratio of 1 means exactly one half-life."""
    T = HL["238U"]
    assert _approx(age_from_daughter_ratio(1.0, T), T)
    assert _approx(age_from_daughter_ratio(0.0, T), 0.0)
    # a 10% lead-to-uranium ratio dates a rock at 615 My
    assert _approx(age_from_daughter_ratio(0.1, T) / YEAR, 6.144e8, tol=1e-3)


def test_potassium_argon_needs_the_branching_correction():
    """Only 10.72% of 40K decays give 40Ar; the rest give 40Ca.  Ignoring that
    makes a rock look far younger than it is."""
    T = HL["40K"]
    naive = age_from_daughter_ratio(1.0, T) / YEAR
    corrected = age_from_daughter_ratio(1.0, T, branch_fraction=K40_TO_AR40_BRANCH) / YEAR
    assert corrected > naive
    assert _approx(corrected / naive, 3.37, tol=1e-2)
    assert _approx(naive, T / YEAR, tol=1e-9)      # ratio 1 -> one half-life
    try:
        age_from_daughter_ratio(1.0, T, branch_fraction=0.0)
    except ValueError:
        pass
    else:
        raise AssertionError("zero branch fraction should be rejected")


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
