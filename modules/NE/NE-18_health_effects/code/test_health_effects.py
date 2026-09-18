"""NE-18 tests -- radiation health effects against Shultis & Faw §§9.5-9.10,
Tables 9.7-9.17, Examples 9.6-9.7, and Chapter 9 problems 7-20 with the authors'
solution manual.

Five printed results are contradicted by the book's own numbers and are pinned
here with the evidence that forces each correction; see refs.md.

Run:  python3 test_health_effects.py
"""

import math

from health_effects import (
    DETERMINISTIC_EFFECTS, LETHAL_DOSES, SUBLETHAL_EFFECTS, ARS_STAGES,
    deterministic_effects_at, lethality_fraction, midline_from_free_field,
    GENETIC_RISKS, GENETIC_BASELINE_TOTAL, doubling_dose, hereditary_risk,
    MOUSE_INDUCED_RATE_PER_GY, HUMAN_SPONTANEOUS_RATE,
    CANCER_BASELINE, CANCER_BASELINE_TOTAL, LIFETIME_CANCER_RISK,
    EXPOSURE_SCENARIOS, DDREF, cancer_risk_at_age, scaled_cancer_risk,
    cancer_risk_per_gy, radiogenic_cancer_deaths, excess_relative_risk,
    probability_of_causation, TRIVIAL_DOSE_SV,
    RN222_CHAIN, potential_alpha_energy_per_bq,
    equilibrium_equivalent_concentration, annual_radon_exposure,
    RADON_RISK_BY_POPULATION, RADON_RISK_BY_AGE_DURATION,
    radon_lung_cancer_risk, WL_MEV_PER_LITRE, WLM_HOURS,
    wlm_to_bq_h_per_m3, bq_h_per_m3_to_wlm,
    NCRP_1987_LIMITS, occupational_limit_sv, public_limit_sv,
    cumulative_dose_guidance_sv, FATAL_CANCER_RISK_PER_SV,
    lnt, linear_with_threshold, quadratic, linear_quadratic, hormetic,
    TABLE_9_11_TOTAL_ERRATA, EXAMPLE_9_7_DEATHS_ERRATA,
    EXAMPLE_9_7_RESPIRATORY_ERRATA,
)


def _rel(a, b, tol):
    return abs(a / b - 1.0) <= tol


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --- deterministic effects ----------------------------------------------

def test_a_threshold_means_nobody_not_a_few():
    """The defining property of a deterministic effect [S&F §9.5.2]: below the
    threshold the effect does not occur at all, and above it severity rises with
    dose.  This is the opposite of the stochastic case, where dose changes the
    probability and never the severity."""
    assert deterministic_effects_at(0.2) == []
    assert deterministic_effects_at(0.0) == []
    # the lowest threshold in Table 9.7 is the testes at 0.3 Gy -- the most
    # radiosensitive endpoint in the table by a factor of two
    lowest = min(e[4] for e in DETERMINISTIC_EFFECTS)
    assert _approx(lowest, 0.3)
    assert [e[0] for e in DETERMINISTIC_EFFECTS if e[4] == lowest] == ["testes"]
    assert len(deterministic_effects_at(0.31)) == 1
    # every threshold is below its own D50, which is what "threshold" must mean
    for organ, endpoint, d50, _, dth, _ in DETERMINISTIC_EFFECTS:
        assert dth < d50, "%s %s: Dth %.2f >= D50 %.2f" % (organ, endpoint, dth, d50)
    # and the ordering is monotone in dose
    counts = [len(deterministic_effects_at(d)) for d in (0.2, 0.5, 1.0, 4.0, 50.0)]
    assert counts == sorted(counts) and counts[0] == 0 and counts[-1] == len(DETERMINISTIC_EFFECTS)
    try:
        deterministic_effects_at(-1.0)
    except ValueError:
        pass
    else:
        raise AssertionError("a negative dose should be rejected")


def test_lethality_and_the_midline_convention():
    """Table 9.8, and the dose definition that goes with it.  LD50/60 is 3.0-3.5
    Gy MID-LINE, which is about two thirds of the free-field exposure -- so a
    'dose' quoted without saying which of the three conventions it uses can be
    50% wrong."""
    assert _approx(lethality_fraction(1.5), 0.0)
    assert _approx(lethality_fraction(2.25), 0.05)
    assert _approx(lethality_fraction(3.25), 0.50)
    assert _approx(lethality_fraction(4.0), 0.90)
    assert _approx(lethality_fraction(5.0), 0.99)
    assert _approx(lethality_fraction(8.0), 1.0)
    # monotone
    prev = -1.0
    for d in [i * 0.25 for i in range(0, 40)]:
        f = lethality_fraction(d)
        assert f >= prev - 1e-12, "not monotone at %.2f Gy" % d
        prev = f
    # the whole LD5-to-LD99 span is a factor of about two in dose: the transition
    # from "almost everyone lives" to "almost everyone dies" is astonishingly sharp
    assert _rel(LETHAL_DOSES["LD99/60"][1] / LETHAL_DOSES["LD5/60"][0], 2.75, 1e-9)
    assert _rel(midline_from_free_field(450.0), 300.0, 1e-9)
    for fn in (lethality_fraction, midline_from_free_field):
        try:
            fn(-1.0)
        except ValueError:
            pass
        else:
            raise AssertionError("%s should reject negatives" % fn.__name__)


def test_a_2_3_gray_accident_is_survivable_and_serious():
    """S&F Ch. 9 Prob. 7 (solution manual Prob. 9): a worker takes 2.3 Gy
    whole-body.  The point of the problem is that the answer is a TIMELINE, not
    a number."""
    eff = dict(((o, e), (d50, dth)) for o, e, d50, dth in deterministic_effects_at(2.3))
    assert ("testes", "sperm count suppressed for 2 y") in eff
    assert ("GI system", "vomiting") in eff
    assert ("bone marrow", "death") in eff          # threshold 1.8 Gy is passed
    assert ("skin", "erythema") not in eff          # threshold 3 Gy is not
    # marrow death is possible but not likely: 2.3 Gy is well below its D50
    assert 2.3 < dict(((o, e), d50) for o, e, d50, _ in
                      deterministic_effects_at(2.3))[("bone marrow", "death")]
    assert 0.0 < lethality_fraction(2.3) < 0.10
    # 2.3 Gy is past the top of Table 9.9 (which stops at 2.0 Gy, "transient
    # disability and clear haematological changes in a majority") and into
    # Table 9.8's LD5/60 band -- i.e. it is exactly the dose at which the
    # sublethal table runs out and the lethal one starts.
    assert [d for (lo, hi), d in SUBLETHAL_EFFECTS if lo <= 2.3 <= hi] == []
    assert max(hi for (lo, hi), _ in SUBLETHAL_EFFECTS) == 2.0
    assert any("transient disability" in d for (lo, hi), d in SUBLETHAL_EFFECTS
               if hi == 2.0)
    lo5, hi5 = LETHAL_DOSES["LD5/60"]
    assert lo5 <= 2.3 <= hi5
    assert len(ARS_STAGES) == 4 and ARS_STAGES[1][0] == "latent"


# --- hereditary ---------------------------------------------------------

def test_the_doubling_dose_is_a_mouse_measurement():
    """DD = R_human/R_mice = 2.95e-6/3.6e-6 = 0.82 Gy, rounded to 1 Gy
    [S&F §9.6.2].  The numerator is a human spontaneous rate and the denominator
    a mouse induced rate, because no induced human rate exists -- no heritable
    effect has ever been demonstrated in the atomic-bomb survivors."""
    dd = doubling_dose()
    assert _rel(dd, 0.82, 5e-3), "%.4f Gy" % dd
    assert _rel(HUMAN_SPONTANEOUS_RATE / MOUSE_INDUCED_RATE_PER_GY, dd, 1e-12)
    assert round(dd) == 1
    for bad in ((0.0, 1e-6), (1e-6, 0.0), (-1e-6, 1e-6)):
        try:
            doubling_dose(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_reproduces_equation_9_14():
    """Eq. (9.14): risk = P x MC x PRCF / DD.  For dominant and X-linked
    disorders, 16 500 x 0.3 x (0.15-0.30)/1 Gy = 750-1500 per Gy per million."""
    lo = hereditary_risk(16500, 1.0, 0.3, 0.15)
    hi = hereditary_risk(16500, 1.0, 0.3, 0.30)
    assert _rel(lo, 742.5, 1e-9) and _rel(hi, 1485.0, 1e-9)
    assert _rel(lo, 750, 0.02) and _rel(hi, 1500, 0.02)   # the book's rounding
    assert (lo, hi) == tuple(sorted((lo, hi)))
    # chronic multifactorial: 39x the baseline, and a comparable risk, because
    # MC x PRCF is 75x smaller. That product, not the baseline, drives the answer.
    chronic_lo = hereditary_risk(650000, 1.0, 0.02, 0.02)
    chronic_hi = hereditary_risk(650000, 1.0, 0.02, 0.09)
    assert _rel(chronic_lo, 260.0, 1e-9) and _rel(chronic_hi, 1170.0, 1e-9)
    assert _rel(chronic_lo, 250, 0.05) and _rel(chronic_hi, 1200, 0.03)
    assert _rel(650000 / 16500, 39.4, 1e-2)
    for bad in ((100.0, 0.0, 0.3, 0.1), (100.0, 1.0, 1.5, 0.1), (100.0, 1.0, 0.3, -0.1)):
        try:
            hereditary_risk(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_table_9_11_does_not_add_up_to_its_own_total():
    """Table 9.11's second-generation column adds to 3950; its Total row prints
    3930.  The column is unambiguous -- 1300 + 250 + 2400, with the recessive row
    0 and the chromosomal row folded into the others by its own footnote b.

    What is NOT resolvable from the book alone is which half is wrong.  The
    'percent of baseline' row prints 0.53, and 3930/738000 = 0.5325% rounds to
    0.53 while 3950/738000 = 0.5352% rounds to 0.54 -- so the printed percentage
    was computed from the printed total, and the two are consistent with each
    other.  Either the total and the percentage are both wrong, or one of the
    three column entries is 20 lower than printed.

    This test therefore pins the inconsistency, not a resolution.  (The published
    BEIR-VII table gives 3950-6700, which is why the module treats the column as
    correct -- but that is an outside source, so it is stated and not asserted.)"""
    baseline = sum(v[0] for v in GENETIC_RISKS.values())
    assert baseline == GENETIC_BASELINE_TOTAL == 738000
    first = [v[1] for v in GENETIC_RISKS.values() if v[1] is not None]
    second = [v[2] for v in GENETIC_RISKS.values() if v[2] is not None]
    # the FIRST-generation column adds exactly, which is what shows the format
    # is being read correctly
    assert (sum(lo for lo, _ in first), sum(hi for _, hi in first)) == (3000, 4700)
    got = (sum(lo for lo, _ in second), sum(hi for _, hi in second))
    assert got == (3950, 6700), got
    assert TABLE_9_11_TOTAL_ERRATA == (3930, 6700)
    assert got[0] - TABLE_9_11_TOTAL_ERRATA[0] == 20
    assert got[1] == TABLE_9_11_TOTAL_ERRATA[1]        # the upper bound is fine
    # the percentage row follows the printed total, not the column sum
    assert round(100.0 * 3930 / baseline, 2) == 0.53
    assert round(100.0 * 3950 / baseline, 2) == 0.54
    assert round(100.0 * 3000 / baseline, 2) == 0.41
    assert round(100.0 * 4700 / baseline, 2) == 0.64
    assert round(100.0 * 6700 / baseline, 2) == 0.91


# --- cancer -------------------------------------------------------------

def test_table_9_12_and_9_14_are_internally_consistent():
    """Table 9.12's site rows add to its Total row in all four columns, and
    Table 9.14's leukemia + nonleukemia add to its totals in all twelve.  This
    is what establishes that the tables are transcribed correctly -- and hence
    what makes the Example 9.7 discrepancy below a real one."""
    for col in range(4):
        s = sum(v[col] for v in CANCER_BASELINE.values() if v[col] is not None)
        assert _rel(s, CANCER_BASELINE_TOTAL[col], 1e-9), "column %d: %.1f" % (col, s)
    # about 2 people per 1000 die of cancer each year, as §9.7.2 says
    assert _rel(0.5 * (CANCER_BASELINE_TOTAL[2] + CANCER_BASELINE_TOTAL[3]) / 1e5,
                2.0e-3, 0.02)
    for scenario, groups in EXPOSURE_SCENARIOS.items():
        for group, d in groups.items():
            for k in ("cases", "deaths"):
                if k in d:
                    assert len(d[k]) == 2
    single = EXPOSURE_SCENARIOS["single 0.1 Gy"]
    assert single["radiation induced"]["cases"] == (900, 1370)
    assert single["natural"]["deaths"] == (22810, 18030)
    # lifetime cancer mortality ~1 in 4.4 (M) and 1 in 5.5 (F); §9.7.2 rounds
    # these to "one in five" and "one in six"
    assert _rel(1e5 / 22810, 4.38, 1e-2)
    assert _rel(1e5 / 18030, 5.55, 1e-2)


def test_reproduces_example_9_6():
    """S&F Ex. 9.6: a 30-year-old male takes 0.02 Gy.  Table 9.13 gives 64 and
    317 per 1e5 at 0.1 Gy, scaled linearly."""
    leuk = scaled_cancer_risk("male", 30, 0.02, endpoint="leukemia")
    solid = scaled_cancer_risk("male", 30, 0.02, endpoint="solid")
    assert _rel(leuk, 0.000128, 1e-3), "%.6f" % leuk
    assert _rel(solid, 0.000634, 1e-3), "%.6f" % solid
    assert _rel(1 / leuk, 7800, 2e-2) and _rel(1 / solid, 1600, 2e-2)
    assert _approx(cancer_risk_at_age("male", 30, "mortality", "leukemia"), 64.0)
    assert _approx(cancer_risk_at_age("male", 30, "mortality", "solid"), 317.0)
    # for comparison, the natural lifetime cancer-death risk is ~1 in 4.4, i.e.
    # 350x larger -- the honest framing of a 0.02 Gy exposure
    assert _rel((22810 / 1e5) / solid, 360.0, 0.05)


def test_solid_cancer_risk_falls_with_age_and_leukemia_does_not():
    """The dominant structure of Table 9.13.  Solid-cancer risk falls ~11x from
    infancy to age 80 because the cancers need decades of latency the exposed
    person may not have; leukemia risk is nearly flat, because it appears within
    a few years and largely disappears within 30."""
    solid = [cancer_risk_at_age("female", a) for a in (0, 20, 40, 60, 80)]
    assert solid == sorted(solid, reverse=True)
    assert _rel(solid[0] / solid[-1], 11.3, 0.05)
    leuk = [cancer_risk_at_age("female", a, endpoint="leukemia")
            for a in (0, 20, 40, 60, 80)]
    assert max(leuk) / min(leuk) < 1.6
    # interpolation between grid ages: male solid mortality is 444 at 20 and
    # 317 at 30, so 25 is the midpoint
    assert _rel(cancer_risk_at_age("male", 25), 0.5 * (444 + 317), 1e-9)
    assert _approx(cancer_risk_at_age("male", 20), 444.0)
    # incidence exceeds mortality everywhere, as it must
    for a in (0, 30, 60):
        for s in ("male", "female"):
            assert (cancer_risk_at_age(s, a, "incidence")
                    > cancer_risk_at_age(s, a, "mortality"))
    for bad in (("male", -1), ("male", 95)):
        try:
            cancer_risk_at_age(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))
    try:
        cancer_risk_at_age("other", 30)
    except KeyError:
        pass
    else:
        raise AssertionError("an unknown sex should be rejected")


def test_the_environmental_risk_factor():
    """§9.7.3: 0.5(480 + 660)/(0.1 Gy x 1e5) = 0.057/Gy, rounded to 0.05/Gy or
    5e-4 per rem, and used as the general risk factor for environmental
    exposures.  NCRP's independent value in §9.9.2 is 1e-2 per Sv, a factor of
    5.7 lower -- the two coexist in the same chapter and are worth noticing."""
    r = cancer_risk_per_gy()
    assert _rel(r, 0.057, 1e-3), "%.4f" % r
    assert _rel(r / 100.0, 5.7e-4, 1e-3)
    assert _rel(r / FATAL_CANCER_RISK_PER_SV, 5.7, 1e-2)
    assert DDREF == 1.5
    try:
        cancer_risk_per_gy("1 mGy per year for life")
    except ValueError:
        pass
    else:
        raise AssertionError("a lifetime-accumulation scenario has no per-Gy risk")


def test_the_collective_dose_trap_is_refused():
    """LNT makes N x D the only thing that matters, so 1e7 people at 0.01 mSv
    'produce' the same 5.7 deaths as 1000 people at 100 mSv.  S&F state this as a
    property of the model; ICRP-103 says computing deaths that way from trivial
    individual doses is not reasonable and should be avoided.

    The function refuses rather than returning the number, because the number
    itself is the misleading artefact -- the arithmetic is fine and the
    extrapolation underneath it has no support."""
    a = radiogenic_cancer_deaths(1e7, 1e-5, allow_trivial=True)
    b = radiogenic_cancer_deaths(1000, 0.1)
    assert _rel(a, b, 1e-12) and _rel(a, 5.7, 1e-3)
    try:
        radiogenic_cancer_deaths(1e7, 1e-5)
    except ValueError as exc:
        assert "allow_trivial" in str(exc)
    else:
        raise AssertionError("a trivial individual dose should be refused")
    # just above the floor it answers
    radiogenic_cancer_deaths(1e6, TRIVIAL_DOSE_SV)
    for bad in ((-1.0, 0.1), (10.0, -0.1)):
        try:
            radiogenic_cancer_deaths(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_err_model_and_probability_of_causation():
    """Eq. (9.16) for solid-cancer incidence, and Eq. (9.17).

    Both exponents are negative, so the model says the same dose is worse the
    younger you receive it and the sooner the cancer appears -- and females carry
    beta = 0.57 against males' 0.33, a 1.7x difference that Table 9.13 shows
    independently."""
    # females carry the larger coefficient
    assert (excess_relative_risk(1.0, "female", 30, 60)
            / excess_relative_risk(1.0, "male", 30, 60)) > 1.7
    # linear in dose, by construction
    assert _rel(excess_relative_risk(0.2, "male", 30, 60),
                0.2 * excess_relative_risk(1.0, "male", 30, 60), 1e-12)
    # at age at exposure 30+ the e* term switches off, so 30 and 50 agree
    assert _approx(excess_relative_risk(1.0, "male", 30, 60),
                   excess_relative_risk(1.0, "male", 50, 60))
    # below 30 the risk rises: exposure at 10 is exp(0.6) = 1.82x exposure at 30
    assert _rel(excess_relative_risk(1.0, "male", 10, 60)
                / excess_relative_risk(1.0, "male", 30, 60), math.exp(0.6), 1e-12)
    # at attained age 60 the (a/60)^eta factor is exactly 1
    assert _approx(excess_relative_risk(1.0, "male", 40, 60), 0.33)
    # and risk falls with attained age
    assert (excess_relative_risk(1.0, "male", 30, 80)
            < excess_relative_risk(1.0, "male", 30, 60))
    # probability of causation
    assert _approx(probability_of_causation(0.0), 0.0)
    assert _approx(probability_of_causation(1.0), 0.5)
    assert probability_of_causation(1e6) > 0.999
    for err in (0.1, 1.0, 10.0):
        assert 0 < probability_of_causation(err) < 1
    try:
        probability_of_causation(-0.1)
    except ValueError:
        pass
    else:
        raise AssertionError("a negative ERR should be rejected")


# --- radon --------------------------------------------------------------

def test_potential_alpha_energy_reproduces_the_accepted_conversion():
    """Eqs. (9.19)-(9.20), computed from the chain's own half-lives and alpha
    energies, give 34 689 MeV/m3 per Bq/m3 of EEC = 5.56e-9 J/m3 -- the
    internationally accepted value, which S&F never state.

    The structure is worth seeing: 214Pb and 214Bi emit NO alphas and contribute
    90% of the total, because they live hundreds of times longer than 218Po and
    each holds 214Po's 7.687 MeV in escrow.  214Po itself contributes nothing
    measurable: it lives 164 microseconds."""
    e = potential_alpha_energy_per_bq()
    assert _rel(e, 34689.0, 1e-3), "%.1f MeV/m3" % e
    assert _rel(e * 1.602e-13, 5.56e-9, 2e-3)
    lam = [math.log(2.0) / t for _, t, _ in RN222_CHAIN]
    escrow = 7.687 * (1 / lam[1] + 1 / lam[2])
    assert _rel(escrow / e, 0.90, 0.02), "%.3f" % (escrow / e)
    assert (7.687 / lam[3]) / e < 1e-6                # 214Po's own term


def test_the_working_level_month_conversion():
    """S&F's footnote gives 1 WLM = 629 000 Bq h m-3 (EEC) without derivation.

    From the definition -- 1 WL is 1.3e5 MeV/L of potential alpha energy and a
    WLM is 170 h of it -- the chain gives 3748 Bq/m3 and 637 100 Bq h/m3.  The
    1.3% gap is not an error in either: 1.3e5 is itself a rounding of the
    1.2835e5 MeV/L that the conventional 3700 Bq/m3 carries."""
    e = potential_alpha_energy_per_bq()
    eec_per_wl = WL_MEV_PER_LITRE * 1e3 / e
    assert _rel(eec_per_wl, 3748.0, 1e-3), "%.1f Bq/m3" % eec_per_wl
    assert _rel(WLM_HOURS * eec_per_wl, 637100.0, 1e-3)
    assert _rel(WLM_HOURS * eec_per_wl / wlm_to_bq_h_per_m3(1.0), 1.013, 2e-3)
    # the conventional 3700 Bq/m3 carries 1.2835e5 MeV/L, which rounds to 1.3e5
    assert _rel(3700.0 * e / 1e3, 1.2835e5, 1e-3)
    assert _rel(3700.0 * WLM_HOURS, 629000.0, 1e-3)
    for v in (0.0, 1.0, 25.0):
        assert _rel(bq_h_per_m3_to_wlm(wlm_to_bq_h_per_m3(v)) + 1, v + 1, 1e-12)
    for fn in (wlm_to_bq_h_per_m3, bq_h_per_m3_to_wlm):
        try:
            fn(-1.0)
        except ValueError:
            pass
        else:
            raise AssertionError("%s should reject negatives" % fn.__name__)


def test_reproduces_example_9_7_and_its_two_errors():
    """S&F Ex. 9.7: 1e6 people at 20 Bq/m3 of 222Rn, F = 0.5.

    Reproduced: the annual exposure is 0.0876 MBq h m-3, the NCRP estimate is
    1230 deaths and 17 per year, and the NAS estimate is 47 per year.

    NOT reproduced, twice:

    (1) The example prints "3116 radon-induced deaths" where 0.039 x 0.0876 x 1e6
        = 3416.  Its OWN next sentence divides by 73 years and gets 47/y, which
        requires 3416 (3116/73 = 42.7).

    (2) It quotes natural respiratory-cancer mortality "from Table 9.12" as 71.9
        (male) and 25.2 (female) per 1e5.  Table 9.12 says 76.2 and 42.2 -- and
        that table's four columns add correctly to its own Total row, so it is
        the example that is out of step.  Using the table gives 592 deaths per
        year, not 486."""
    eec = equilibrium_equivalent_concentration(20.0, 0.5)
    assert _approx(eec, 10.0)
    exposure = annual_radon_exposure(eec)
    assert _rel(exposure, 0.0876, 1e-3), "%.5f" % exposure

    nas = radon_lung_cancer_risk(exposure, "mixed") * 1e6
    assert _rel(nas, 3416.0, 2e-3), "%.1f" % nas
    assert nas != EXAMPLE_9_7_DEATHS_ERRATA
    life = RADON_RISK_BY_POPULATION["mixed"][0]
    assert _rel(life, 73.1, 1e-9)
    assert _rel(nas / life, 46.7, 1e-2)                    # the printed 47/y
    assert not _rel(EXAMPLE_9_7_DEATHS_ERRATA / life, 47.0, 0.05)   # 42.7, not 47

    ncrp = RADON_RISK_BY_AGE_DURATION[1][4] * exposure * 1e6
    assert _rel(ncrp, 1226.0, 5e-3), "%.1f" % ncrp         # the printed 1230
    assert _rel(ncrp / life, 16.8, 1e-2)                   # the printed 17/y
    assert _rel(ncrp / nas, 0.359, 1e-2)                   # "about one-third"

    # the natural comparison, done with Table 9.12 as printed
    m, f = CANCER_BASELINE["respiratory"][2], CANCER_BASELINE["respiratory"][3]
    assert (m, f) == (76.2, 42.2)
    natural = 0.5 * (m + f) / 1e5 * 1e6
    assert _rel(natural, 592.0, 1e-3), "%.1f" % natural
    printed_m, printed_f = EXAMPLE_9_7_RESPIRATORY_ERRATA
    assert _rel(0.5 * (printed_m + printed_f) / 1e5 * 1e6, 486.0, 2e-3)
    assert not _rel(natural, 486.0, 0.1)


def test_smoking_multiplies_the_radon_risk_tenfold():
    """Table 9.15's central result.  Radon and tobacco are multiplicative, so a
    smoker's radiogenic lung-cancer risk is ten times a non-smoker's for the same
    exposure -- which means radon remediation is worth ten times as much to a
    smoker, and the two hazards cannot be assessed separately."""
    assert _rel(RADON_RISK_BY_POPULATION["smoking male"][1]
                / RADON_RISK_BY_POPULATION["nonsmoking male"][1], 10.0, 1e-9)
    assert _rel(RADON_RISK_BY_POPULATION["smoking female"][1]
                / RADON_RISK_BY_POPULATION["nonsmoking female"][1], 9.2, 1e-2)
    # the mixed-population value is the average of the two sexes
    assert _rel(0.5 * (RADON_RISK_BY_POPULATION["male"][1]
                       + RADON_RISK_BY_POPULATION["female"][1]),
                RADON_RISK_BY_POPULATION["mixed"][1], 2e-2)
    # males carry 2.5x the female risk, consistent across all three pairs
    for a, b in (("male", "female"), ("smoking male", "smoking female"),
                 ("nonsmoking male", "nonsmoking female")):
        assert 1.8 < (RADON_RISK_BY_POPULATION[a][1]
                      / RADON_RISK_BY_POPULATION[b][1]) < 2.6
    # the EPA action level, 150 Bq/m3 at F = 0.5, for a lifetime
    action = annual_radon_exposure(equilibrium_equivalent_concentration(150.0, 0.5))
    assert _rel(radon_lung_cancer_risk(action, "mixed"), 0.0256, 1e-2)
    assert radon_lung_cancer_risk(action, "smoking male") > 0.10
    try:
        equilibrium_equivalent_concentration(100.0, 1.5)
    except ValueError:
        pass
    else:
        raise AssertionError("F > 1 should be refused")
    try:
        radon_lung_cancer_risk(0.1, "cat")
    except KeyError:
        pass
    else:
        raise AssertionError("an unknown population should be refused")


def test_table_9_16_is_monotone_where_it_should_be():
    """Lifetime risk rises with exposure duration at every age -- and the
    LIFETIME column peaks for children, then falls, because a 70-year-old has
    less life left than the lung cancer needs."""
    for age, row in RADON_RISK_BY_AGE_DURATION.items():
        assert list(row) == sorted(row), "age %d not monotone in duration" % age
    lifetimes = [RADON_RISK_BY_AGE_DURATION[a][4] for a in sorted(RADON_RISK_BY_AGE_DURATION)]
    assert lifetimes[0] == max(lifetimes) or lifetimes[1] == max(lifetimes)
    assert lifetimes[-1] == min(lifetimes)
    assert _rel(max(lifetimes) / min(lifetimes), 23.3, 0.05)


# --- standards and the models -------------------------------------------

def test_the_dose_limits_are_a_risk_comparison_not_a_threshold():
    """§9.9.1 derives the limits from accident statistics in industries already
    called safe, run backwards through an assumed linear risk coefficient:

        occupational: (10 x 0.002)/(40 y x 1e-4 /rem) = 5 rem/y = 50 mSv/y
        public:        0.004/(70 y x 1e-4 /rem)      = 5.7 mSv/y

    The occupational number comes out exactly.  The public one does not -- the
    arithmetic gives 5.7 mSv/y and the adopted limit was 5, with today's limit
    1 mSv/y (Table 9.17).  That gap is ALARA, not error."""
    occ = occupational_limit_sv()
    assert _rel(occ, 0.050, 1e-9), "%.4f Sv" % occ
    assert _rel(1000 * occ, NCRP_1987_LIMITS["occupational stochastic"], 1e-9)
    pub = public_limit_sv()
    assert _rel(pub, 5.714e-3, 1e-3), "%.5f Sv" % pub
    assert _rel(1000 * pub / NCRP_1987_LIMITS["public infrequent"], 1.143, 1e-3)
    # today's continuous-exposure limit is 5.7x tighter than the risk argument
    assert _rel(1000 * pub / NCRP_1987_LIMITS["public continuous"], 5.71, 1e-2)
    # the cumulative guidance, and the fact it is looser than 40 x the annual
    assert _rel(cumulative_dose_guidance_sv(40), 0.40, 1e-9)
    assert cumulative_dose_guidance_sv(40) < 40 * NCRP_1987_LIMITS["occupational stochastic"] / 1000
    # non-stochastic organ limits are 10x the stochastic one, because they guard
    # a threshold rather than a probability
    assert _rel(NCRP_1987_LIMITS["occupational other organs"]
                / NCRP_1987_LIMITS["occupational stochastic"], 10.0, 1e-9)
    # public continuous is 1/50 of occupational; the negligible individual risk
    # level is 1/100 of THAT
    assert _rel(NCRP_1987_LIMITS["occupational stochastic"]
                / NCRP_1987_LIMITS["public continuous"], 50.0, 1e-9)
    assert _rel(NCRP_1987_LIMITS["public continuous"]
                / NCRP_1987_LIMITS["negligible individual risk level"], 100.0, 1e-9)
    try:
        cumulative_dose_guidance_sv(-1)
    except ValueError:
        pass
    else:
        raise AssertionError("a negative age should be rejected")


def test_the_five_dose_effect_models_are_distinguishable_only_at_high_dose():
    """Fig. 9.3's five shapes.  Normalised to agree at 1 Gy, they differ by less
    than they are ever measured to at the doses regulation is written about --
    which is the entire content of §9.10 in one assertion."""
    assert _approx(lnt(0.0), 0.0)
    assert _approx(quadratic(0.0), 0.0)
    assert _approx(linear_with_threshold(0.05, threshold=0.1), 0.0)
    assert _approx(linear_with_threshold(0.3, threshold=0.1), 0.2)
    assert _approx(linear_quadratic(1.0, 1.0, 1.0), 2.0)
    # LNT is the most conservative of the no-threshold pair at low dose: for
    # alpha = beta, the quadratic model is 100x smaller at 0.01 Gy
    assert _rel(lnt(0.01) / quadratic(0.01), 100.0, 1e-9)
    # the hormetic curve dips negative and returns to zero at the ZEP
    assert _approx(hormetic(0.0), 0.0)
    assert abs(hormetic(0.2, zep=0.2)) < 1e-12
    assert hormetic(0.1, zep=0.2) < 0.0
    assert hormetic(0.5, zep=0.2) > 0.0
    assert hormetic(5.0, zep=0.2) > 0.0
    # and is asymptotically LNT
    assert _rel(hormetic(50.0, zep=0.2), lnt(50.0), 1e-6)
    for bad in ({"zep": 0.0}, {"zep": 0.2, "scale": -1.0}):
        try:
            hormetic(1.0, **bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % bad)


def test_the_dose_where_the_argument_actually_stops():
    """§9.7: 'Excess cancer risk cannot be observed at doses less than about
    0.2 Gy.'  Every dose limit in Table 9.17 is far below that, so the entire
    regulatory structure sits in a region where the effect it regulates has never
    been measured.  This test states the gap numerically rather than in prose."""
    observable_gy = 0.2
    annual_occupational = NCRP_1987_LIMITS["occupational stochastic"] / 1000.0
    annual_public = NCRP_1987_LIMITS["public continuous"] / 1000.0
    assert _rel(observable_gy / annual_occupational, 4.0, 1e-9)
    assert _rel(observable_gy / annual_public, 200.0, 1e-9)
    # a whole 40-year career at the limit only just reaches the observable dose
    assert _rel(40 * annual_occupational / observable_gy, 10.0, 1e-9)
    # and natural background over a lifetime is a third of it
    assert _rel(75 * 2.4e-3 / observable_gy, 0.9, 0.02)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
