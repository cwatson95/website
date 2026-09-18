"""NE-23 tests -- the nuclear fuel cycle against Shultis & Faw §§11.7-11.8 and
Tables 11.7-11.8.

Run:  python3 test_fuel_cycle.py
"""

import math

from fuel_cycle import (
    U235_ATOM_PERCENT, U235_WEIGHT_FRACTION, M_U235, M_U238,
    ANNUAL_FLOWS, CAPACITY_FACTOR, TAILS_ASSAY,
    NEW_FUEL_ATOM_PERCENT, SPENT_FUEL_ATOM_PERCENT,
    WASTE_CLASSES, LONG_LIVED_FISSION_PRODUCTS, ENRICHMENT_TECHNOLOGIES,
    atom_to_weight_fraction, weight_to_atom_fraction,
    value_function, separative_work, feed_per_product, tails_per_product,
    swu_per_product, optimal_tails_assay, cascade_balance,
    burnup_from_fissioned_fraction, fission_energy_from_mass,
    plutonium_fission_fraction, fission_product_activity_fraction,
    years_to_ore_activity, natural_uranium_per_year, lifetime_uranium,
)


def _rel(a, b, tol):
    return abs(a / b - 1.0) <= tol


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --- the atom/weight trap -------------------------------------------------

def test_natural_uranium_is_0_7204_atom_percent_and_0_711_weight_percent():
    """The single most common arithmetic error in fuel-cycle work. S&F print
    0.7204 a% (§11.7) and every enrichment calculation uses weight fractions.

    Substituting the atom percent into a cascade balance changes the feed
    requirement by 1.8% -- on a 150 t/y reactor that is 2.6 t of natural uranium
    a year, and it is invisible because both numbers look like 0.72%."""
    w = atom_to_weight_fraction(U235_ATOM_PERCENT / 100.0)
    assert _rel(w, 0.007114, 1e-3), "%.6f" % w
    assert _rel(U235_WEIGHT_FRACTION, w, 1e-12)
    assert w < U235_ATOM_PERCENT / 100.0        # 235U is the lighter isotope
    # round trip
    for a in (0.007204, 0.03, 0.5, 0.93):
        assert _rel(weight_to_atom_fraction(atom_to_weight_fraction(a)), a, 1e-12)
    # what the mistake costs
    good = feed_per_product(U235_WEIGHT_FRACTION, 0.03, 0.002)
    bad = feed_per_product(U235_ATOM_PERCENT / 100.0, 0.03, 0.002)
    assert _rel(good / bad, 1.018, 2e-3)
    assert _rel((good - bad) * 28070 / 1e3, 2.67, 0.02)     # tonnes per year
    # the difference shrinks at high enrichment, where the two agree better
    assert (atom_to_weight_fraction(0.93) / 0.93) > (w / (U235_ATOM_PERCENT / 100))
    for bad_in in (-0.1, 1.5):
        try:
            atom_to_weight_fraction(bad_in)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % bad_in)


# --- Table 11.7 -----------------------------------------------------------

def test_table_11_7_mass_balance_closes_exactly():
    """The enrichment stage of S&F's annual flowsheet:

        product (821 + 27 249) + tails (121 227) = 149 297 = feed

    to the kilogram. That exactness is what makes the rest of the table
    trustworthy, and it is also how one can tell the table used WEIGHT
    fractions: the 235U balance closes to 0.13% with 0.7114 wt-% and to 1.4%
    with 0.7204 a%."""
    f = ANNUAL_FLOWS["U in UF6 (conversion)"]
    p = (ANNUAL_FLOWS["235U (enrichment product)"]
         + ANNUAL_FLOWS["238U (enrichment product)"])
    t = ANNUAL_FLOWS["U tails at 0.2%"]
    assert _approx(p + t, f, 1e-12), "%.1f vs %.1f" % (p + t, f)
    assert _rel(p, 28070.0, 1e-9)
    # product assay
    x_p = ANNUAL_FLOWS["235U (enrichment product)"] / p
    assert _rel(x_p, 0.029249, 1e-4), "%.5f" % x_p
    assert 0.029 < x_p < 0.030                       # "about 3%"
    # the 235U balance, with weight fractions
    lhs = f * U235_WEIGHT_FRACTION
    rhs = ANNUAL_FLOWS["235U (enrichment product)"] + t * TAILS_ASSAY
    assert _rel(lhs, rhs, 2e-3), "%.1f vs %.1f kg" % (lhs, rhs)
    # ...and how much worse it is with atom percent
    lhs_atom = f * U235_ATOM_PERCENT / 100.0
    assert abs(lhs_atom / rhs - 1) > 5 * abs(lhs / rhs - 1)
    # F/P from the balance equations reproduces the table
    assert _rel(f / p, feed_per_product(U235_WEIGHT_FRACTION, x_p, TAILS_ASSAY),
                3e-3)
    # conversion loses 0.5% of the uranium, as it should
    assert _rel(f / ANNUAL_FLOWS["U in U3O8 (mining/milling)"], 0.995, 1e-3)


def test_the_fission_product_mass_matches_the_energy_produced():
    """Table 11.7 reports 873 kg of fission products a year. That mass, at
    200 MeV per fission, is 830 000 MWd(t) = 277 full-power days at 3000 MW(t)
    -- against the 274 days its own stated 75% capacity factor implies.

    A 1% agreement between a mass flow and an energy output, computed by
    completely different routes, is the strongest single check available on this
    table."""
    mwd = fission_energy_from_mass(ANNUAL_FLOWS["fission products"])
    assert _rel(mwd, 829595.0, 1e-3), "%.0f MWd" % mwd
    days = mwd / 3000.0
    assert _rel(days, 277.0, 5e-3), "%.1f d" % days
    implied = 365.25 * CAPACITY_FACTOR
    assert _rel(days, implied, 0.02), "%.1f vs %.1f" % (days, implied)
    # the reactor mass balance closes to 96%, the gap being fabrication losses
    loaded = 28070.0
    out = (ANNUAL_FLOWS["U + Pu discharged"] + ANNUAL_FLOWS["fission products"])
    assert 0.95 < out / loaded < 0.97, "%.4f" % (out / loaded)
    # 73% of the 235U loaded is gone
    assert _rel(1 - ANNUAL_FLOWS["235U discharged"]
                / ANNUAL_FLOWS["235U (enrichment product)"], 0.732, 1e-2)
    # and the discharged fissile plutonium is 81% of the total plutonium
    assert _rel(ANNUAL_FLOWS["fissile Pu discharged"]
                / ANNUAL_FLOWS["total Pu discharged"], 0.724, 1e-2)
    # the discharged fissile inventory rivals the 235U that is left
    assert ANNUAL_FLOWS["fissile Pu discharged"] < ANNUAL_FLOWS["235U discharged"]
    assert _rel((ANNUAL_FLOWS["235U discharged"]
                 + ANNUAL_FLOWS["fissile Pu discharged"]) / 28070.0, 0.0142, 1e-2)


def test_annual_and_lifetime_uranium():
    """S&F §11.7.1: about 150 t of natural uranium a year, 4500 t over a 30-year
    life, for a 1000 MW(e) LWR on the once-through cycle."""
    annual = natural_uranium_per_year()
    assert _rel(annual / 1e3, 153.7, 0.02), "%.1f t/y" % (annual / 1e3)
    assert _rel(annual, ANNUAL_FLOWS["U in UF6 (conversion)"], 0.04)
    assert _rel(lifetime_uranium(annual, 30.0), 4611.0, 0.03)
    assert _rel(lifetime_uranium(150e3, 30.0), 4500.0, 1e-9)
    # recycling roughly halves it, as §11.7.1 says (150 -> 80 t/y)
    assert _rel(80.0 / 150.0, 0.533, 1e-2)
    # a fast breeder needs 40 kg over its whole life -- five orders of magnitude
    assert _rel(4500e3 / 40.0, 1.1e5, 0.05)


# --- separative work ------------------------------------------------------

def test_the_value_function_and_its_shape():
    """V(x) = (2x-1) ln[x/(1-x)] is symmetric about x = 1/2, vanishes there, and
    diverges at both ends -- the statement that a pure stream is expensive
    whichever end of the mixture it sits at."""
    assert _approx(value_function(0.5), 0.0)
    for x in (0.01, 0.1, 0.3):
        assert _rel(value_function(x), value_function(1 - x), 1e-12)
        assert value_function(x) > 0
    assert value_function(0.001) > value_function(0.01) > value_function(0.1)
    assert _rel(value_function(0.00711), 4.869, 1e-3)
    assert _rel(value_function(0.03), 3.268, 1e-3)
    assert _rel(value_function(0.002), 6.188, 1e-3)
    for bad in (0.0, 1.0, -0.1, 1.5):
        try:
            value_function(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("assay %r should be rejected" % bad)


def test_separative_work_for_table_11_7s_reactor():
    """S&F describe five enrichment technologies and never write down the unit
    they are all measured in. Table 11.7's own numbers give 116 tSWU/y, squarely
    in the industry range for a 1000 MW(e) PWR."""
    p = 28070.0
    x_p = 821.0 / p
    swu = separative_work(p, U235_WEIGHT_FRACTION, x_p, TAILS_ASSAY)
    assert _rel(swu / 1e3, 116.2, 5e-3), "%.1f tSWU/y" % (swu / 1e3)
    assert 100e3 < swu < 130e3
    assert _rel(swu / p, 4.140, 5e-3)
    # SWU scales linearly with product, as it must
    assert _rel(separative_work(2 * p, U235_WEIGHT_FRACTION, x_p, TAILS_ASSAY),
                2 * swu, 1e-12)
    # weapons-grade material costs far more per kilogram
    assert (swu_per_product(U235_WEIGHT_FRACTION, 0.90, 0.003)
            > 10 * swu_per_product(U235_WEIGHT_FRACTION, 0.045, 0.003))
    # The proliferation-relevant statement, done correctly: track the SAME
    # material. One kg of 90% HEU needs 4.553 kg of 20% material, and making
    # that 20% material is 90% of the total separative work. So a stock of
    # 20%-enriched uranium is nine tenths of the way to weapons grade, which is
    # why 20% is the regulatory line between low- and high-enriched uranium.
    b = swu_per_product(U235_WEIGHT_FRACTION, 0.20, 0.003)
    c = swu_per_product(U235_WEIGHT_FRACTION, 0.90, 0.003)
    m20 = (0.90 - 0.003) / (0.20 - 0.003)
    assert _rel(m20, 4.553, 1e-3)
    assert _rel(m20 * b / c, 0.904, 1e-2), "%.3f" % (m20 * b / c)
    assert 0.85 < m20 * b / c < 0.95


def test_a_cascade_that_cannot_exist_is_refused():
    """The two balance equations have no positive solution unless
    x_t < x_f < x_p. Anything else is not a hard cascade, it is an impossible
    one -- and the formula would happily return a negative feed ratio."""
    for bad in ((0.00711, 0.03, 0.03), (0.00711, 0.005, 0.002),
                (0.00711, 0.03, 0.01), (0.00711, 0.03, 0.0)):
        try:
            feed_per_product(*bad)
        except ValueError as exc:
            assert "cascade" in str(exc) or "x_t" in str(exc)
        else:
            raise AssertionError("%r should be refused" % (bad,))
    # the balance itself
    p, t = cascade_balance(149297.0, U235_WEIGHT_FRACTION, 0.029249, 0.002)
    assert _rel(p, 28070.0, 5e-3)
    assert _approx(p + t, 149297.0, 1e-9)
    assert _rel(tails_per_product(U235_WEIGHT_FRACTION, 0.03, 0.002)
                + 1.0, feed_per_product(U235_WEIGHT_FRACTION, 0.03, 0.002), 1e-12)


def test_the_tails_assay_is_an_economic_choice():
    """Beyond S&F entirely. Leaner tails need less uranium and more separative
    work; the optimum depends on the two prices, and the 0.2% of Table 11.7 is a
    convention of its era rather than a physical constant.

    The direction is the useful part: expensive uranium buys leaner tails."""
    cheap_u, _ = optimal_tails_assay(U235_WEIGHT_FRACTION, 0.045, 50.0, 100.0)
    dear_u, _ = optimal_tails_assay(U235_WEIGHT_FRACTION, 0.045, 250.0, 100.0)
    assert dear_u < cheap_u, "%.5f vs %.5f" % (dear_u, cheap_u)
    assert _rel(cheap_u, 0.00303, 0.02) and _rel(dear_u, 0.00139, 0.02)
    # and expensive enrichment buys richer tails
    dear_swu, _ = optimal_tails_assay(U235_WEIGHT_FRACTION, 0.045, 100.0, 200.0)
    cheap_swu, _ = optimal_tails_assay(U235_WEIGHT_FRACTION, 0.045, 100.0, 50.0)
    assert dear_swu > cheap_swu
    # the historical 0.2-0.25% band corresponds to roughly equal prices
    mid, _ = optimal_tails_assay(U235_WEIGHT_FRACTION, 0.045, 100.0, 100.0)
    assert 0.0018 < mid < 0.0028, "%.5f" % mid
    # leaner tails always cost more SWU and less feed
    assert (swu_per_product(U235_WEIGHT_FRACTION, 0.045, 0.001)
            > swu_per_product(U235_WEIGHT_FRACTION, 0.045, 0.003))
    assert (feed_per_product(U235_WEIGHT_FRACTION, 0.045, 0.001)
            < feed_per_product(U235_WEIGHT_FRACTION, 0.045, 0.003))
    for bad in ((0.0, 100.0), (100.0, 0.0)):
        try:
            optimal_tails_assay(U235_WEIGHT_FRACTION, 0.045, *bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


# --- Table 11.8 -----------------------------------------------------------

def test_table_11_8_closes_exactly_as_a_heavy_atom_balance():
    """Both columns sum to 100.00, and the transmutation accounting closes to
    two decimals with no adjustment:

        235U consumed 2.49 = 0.51 captured to 236U + 1.98 fissioned
        238U consumed 2.40 = 0.88 Pu remaining + 1.52 Pu fissioned
        total fissions      = 1.98 + 1.52 = 3.50 = the printed FP entry

    So 43% of the energy came from plutonium that was not in the fuel when it was
    loaded -- which is what §11.1 means by "almost half the power" at end of
    life, and why a reactor's reactivity does not simply decay away."""
    assert _approx(sum(NEW_FUEL_ATOM_PERCENT.values()), 100.0, 1e-12)
    assert _approx(sum(SPENT_FUEL_ATOM_PERCENT.values()), 100.0, 1e-12)
    u5_burned = NEW_FUEL_ATOM_PERCENT["235U"] - SPENT_FUEL_ATOM_PERCENT["235U"]
    u5_fissioned = u5_burned - SPENT_FUEL_ATOM_PERCENT["236U"]
    pu_left = sum(v for k, v in SPENT_FUEL_ATOM_PERCENT.items() if k.endswith("Pu"))
    u8_burned = NEW_FUEL_ATOM_PERCENT["238U"] - SPENT_FUEL_ATOM_PERCENT["238U"]
    pu_fissioned = u8_burned - pu_left
    assert _rel(u5_burned, 2.49, 1e-9)
    assert _rel(u5_fissioned, 1.98, 1e-9)
    assert _rel(pu_left, 0.88, 1e-9)
    assert _rel(pu_fissioned, 1.52, 1e-9)
    assert _approx(u5_fissioned + pu_fissioned,
                   SPENT_FUEL_ATOM_PERCENT["fission products"], 1e-9)
    assert _rel(plutonium_fission_fraction(), 0.434, 1e-2)
    assert 0.40 < plutonium_fission_fraction() < 0.50      # "almost half"


def test_burnup_from_table_11_8_matches_table_11_2():
    """3.5% of the heavy atoms fissioned gives 33.3 GWd/tU. S&F's Table 11.2,
    six chapters earlier and from a different source, prints a discharge burnup
    of 33 GWd/tU.

    Two independent tables agreeing to 1% is the kind of check that makes a
    number usable."""
    b = burnup_from_fissioned_fraction(SPENT_FUEL_ATOM_PERCENT["fission products"])
    assert _rel(b, 33.3, 1e-2), "%.2f GWd/tU" % b
    assert _rel(b, 33.0, 2e-2)
    # linear in the fissioned fraction, as it must be
    assert _rel(burnup_from_fissioned_fraction(7.0), 2 * b, 1e-12)
    # a modern 50 GWd/tU fuel fissions 5.3% of its heavy atoms
    lo, hi = 0.0, 100.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if burnup_from_fissioned_fraction(mid) < 50.0:
            lo = mid
        else:
            hi = mid
    assert _rel(0.5 * (lo + hi), 5.26, 1e-2)
    for bad in (-1.0, 101.0):
        try:
            burnup_from_fissioned_fraction(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % bad)


# --- waste ----------------------------------------------------------------

def test_two_waste_problems_on_two_timescales():
    """S&F §11.7.4. Of the seven fission products with half-lives over 25 years,
    five have MILLION-year half-lives -- which makes them effectively stable and
    therefore of low activity. The long-term activity is set entirely by 137Cs
    and 90Sr at ~30 years, and falls by 1e-10 in a thousand years.

    The actinides are a different problem: 239Pu's 24 000-year half-life needs
    isolation for several hundred thousand years, a factor of a few hundred
    longer. That gap is the entire technical case for reprocessing."""
    assert len(LONG_LIVED_FISSION_PRODUCTS) == 7
    short = [k for k, v in LONG_LIVED_FISSION_PRODUCTS.items() if v < 100]
    assert sorted(short) == ["137Cs", "90Sr"]
    assert all(LONG_LIVED_FISSION_PRODUCTS[k] > 1e5
               for k in LONG_LIVED_FISSION_PRODUCTS if k not in short)
    # the book's own 1000-year estimate
    assert _rel(fission_product_activity_fraction(1000.0), 1e-10, 0.10)
    assert _rel(years_to_ore_activity(1e-10), 997.0, 1e-2)
    # monotone decay
    prev = 1.0
    for y in (0, 30, 100, 300, 1000):
        v = fission_product_activity_fraction(y)
        assert v <= prev
        prev = v
    assert _approx(fission_product_activity_fraction(30.0), 0.5, 1e-2)
    # the actinide timescale is a few hundred times longer
    assert _rel(years_to_ore_activity(1e-10, 24000.0) / 997.0, 800.0, 0.02)
    for bad in ((-1.0,), (1.0, 0.0)):
        try:
            fission_product_activity_fraction(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_the_waste_classes_and_the_technologies():
    """§§11.7.2-11.7.3, as bookkeeping. The 100 nCi/g actinide line is what
    separates LLW from TRU, and it is the only quantitative boundary in the
    classification."""
    assert set(WASTE_CLASSES) == {"HLW", "TRU", "mill tailings", "LLW", "ILW"}
    assert "100 nCi/g" in WASTE_CLASSES["TRU"]
    assert "100 nCi/g" in WASTE_CLASSES["LLW"]
    assert "spent fuel" in WASTE_CLASSES["HLW"]
    assert "radon" in WASTE_CLASSES["mill tailings"]
    assert len(ENRICHMENT_TECHNOLOGIES) == 5
    # the centrifuge won on energy, which is the whole story of the transition
    assert "dominant" in ENRICHMENT_TECHNOLOGIES["gas centrifuge"]["status"]
    assert "retired" in ENRICHMENT_TECHNOLOGIES["gaseous diffusion"]["status"]
    assert ENRICHMENT_TECHNOLOGIES["electromagnetic"]["stages"] == "one"


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
