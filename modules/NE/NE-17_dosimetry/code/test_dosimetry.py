"""NE-17 tests -- dosimetry against Shultis & Faw §§9.1-9.4, Examples 9.1-9.5,
Tables 9.1-9.6, and Chapter 9 problems 1-6 (with the authors' solution manual).

Four printed results are contradicted by the book's own numbers and are pinned
here with the evidence that forces the correction; see refs.md.

Run:  python3 test_dosimetry.py
"""

import math

from dosimetry import (
    MEV_TO_J, DOSE_PREFACTOR, EXPOSURE_PREFACTOR, W_AIR_EV,
    ROENTGEN_C_PER_KG, GY_PER_ROENTGEN, BQ_PER_CI, SV_PER_REM, MATERIALS,
    mass_coefficient, linear_coefficient, point_source_fluence,
    kerma, absorbed_dose, exposure, roentgen_to_air_dose, air_dose_to_roentgen,
    photon_kerma_rate, photon_dose_rate, photon_dose_rate_from_lines,
    neutron_recoil_fraction, neutron_kerma, water_neutron_kerma_coefficient,
    quality_factor, dose_equivalent, effective_dose,
    ICRP77_TISSUE_WEIGHTS, ICRP90_TISSUE_WEIGHTS, ICRP07_TISSUE_WEIGHTS,
    INGESTION_DOSE_COEFFICIENTS, committed_effective_dose,
    NATURAL_BACKGROUND_WORLD, NATURAL_BACKGROUND_US, US_MANMADE_BREAKDOWN,
    US_MANMADE_MSV, rule_of_thumb_exposure_rate, exposure_rate_exact,
    rule_of_thumb_valid_range,
    EXAMPLE_9_3_PRINTED_USV, EXAMPLE_9_5_PRINTED_MREM,
    PROBLEM_9_1_PRINTED_MEV, PROBLEM_9_4A_PRINTED_MGY_PER_H,
)

# Appendix D gamma lines (../../data_tables/D1_decay_radiation.csv), used by
# S&F Ch. 9 problems 4 and 5.  Listed literally so the test is self-contained
# about WHAT it is reproducing; `test_appendix_D_lines_match_the_book` checks
# them against the extracted CSV.
N16_GAMMAS = [(6.1292, 0.690), (7.1151, 0.050)]
K43_GAMMAS = [(0.2206, 0.0411), (0.3728, 0.8727), (0.3969, 0.1143),
              (0.5934, 0.1103), (0.6175, 0.8051), (1.0218, 0.0188)]


def _rel(a, b, tol):
    return abs(a / b - 1.0) <= tol


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --- the unit conversions the whole chapter rests on ---------------------

def test_the_two_prefactors_are_derivable_not_magic():
    """Eqs. (9.5)/(9.6) carry 1.602e-10 and Eq. (9.9) carries 1.835e-8.  Neither
    is a physical constant: both are pure unit algebra, and re-deriving them is
    the cheapest possible check that the equations are being used right."""
    # dose: J per MeV, times g per kg
    assert _rel(MEV_TO_J * 1000.0, DOSE_PREFACTOR, 1e-12)
    # exposure: (g/kg)(eV/MeV)(C/ion pair) / [(eV/ion pair)(C/kg per R)]
    derived = 1000.0 * 1e6 * 1.602e-19 / (W_AIR_EV * ROENTGEN_C_PER_KG)
    assert _rel(derived, EXPOSURE_PREFACTOR, 5e-4), "%.4e" % derived


def test_the_roentgen_to_gray_conversion_the_book_never_writes_down():
    """S&F define exposure and dose separately and never connect them, yet the
    connection is forced: a roentgen is 2.58e-4 C/kg and each ion pair costs
    W = 33.85 eV, so 1 R = 8.73 mGy in air.

    Equivalently it is the ratio of the two prefactors -- which is the check,
    because those were derived independently above."""
    assert _rel(GY_PER_ROENTGEN, 8.73e-3, 1e-3), "%.5e" % GY_PER_ROENTGEN
    assert _rel(DOSE_PREFACTOR / EXPOSURE_PREFACTOR, GY_PER_ROENTGEN, 1e-3)
    # round trip
    for x in (0.001, 1.0, 250.0):
        assert _rel(air_dose_to_roentgen(roentgen_to_air_dose(x)), x, 1e-12)
    # and it is the number that converts a survey meter reading: 10 mR/h
    assert _rel(roentgen_to_air_dose(0.010) * 1e6, 87.3, 1e-2)
    for fn in (roentgen_to_air_dose, air_dose_to_roentgen):
        try:
            fn(-1.0)
        except ValueError:
            pass
        else:
            raise AssertionError("%s should reject negatives" % fn.__name__)


# --- Examples 9.1 and 9.2 ------------------------------------------------

def test_reproduces_example_9_1():
    """S&F Ex. 9.1: 1e8 5-MeV photons/s into infinite water; iron kerma and dose
    1 m away.  Every coefficient comes from the extracted Appendix C.3, so this
    tests the data tables as much as the formulas."""
    mu_w = linear_coefficient("water", 5.0, "total")
    assert _rel(mu_w, 0.03031, 1e-6)                 # book: mu = 0.03031 /cm
    phi = point_source_fluence(1e8, 1.0, 100.0, mu_w)
    assert _rel(phi, 38.41, 1e-3), "%.3f" % phi
    assert _rel(mass_coefficient("iron", 5.0, "tr"), 0.02112, 1e-9)
    assert _rel(mass_coefficient("iron", 5.0, "en"), 0.01983, 1e-9)
    k = photon_kerma_rate("iron", 5.0, phi)
    d = photon_dose_rate("iron", 5.0, phi)
    assert _rel(k, 6.50e-10, 2e-3), "%.4e" % k
    assert _rel(d, 6.10e-10, 2e-3), "%.4e" % d
    assert _rel(k * 3.6e9, 2.34, 3e-3)               # uGy/h
    assert _rel(d * 3.6e9, 2.20, 3e-3)


def test_kerma_exceeds_dose_by_exactly_the_radiative_fraction():
    """K/D = mu_tr/mu_en, and the gap IS the bremsstrahlung leaving the volume.
    It is invisible at 100 keV and 6.5% at 5 MeV in iron -- so the two words are
    interchangeable in a laboratory and are not in a shield."""
    phi = 1e10
    for e, material, floor in ((0.1, "iron", 0.0), (5.0, "iron", 0.05),
                               (5.0, "lead", 0.10)):
        k = kerma(e, mass_coefficient(material, e, "tr"), phi)
        d = absorbed_dose(e, mass_coefficient(material, e, "en"), phi)
        assert k >= d, "kerma must not fall below dose"
        assert k / d - 1.0 >= floor, "%s at %g MeV: %.4f" % (material, e, k / d)
        assert _rel(k / d, mass_coefficient(material, e, "tr")
                    / mass_coefficient(material, e, "en"), 1e-12)
    # at 100 keV in iron the two are equal to better than 1%
    k = kerma(0.1, mass_coefficient("iron", 0.1, "tr"), phi)
    d = absorbed_dose(0.1, mass_coefficient("iron", 0.1, "en"), phi)
    assert k / d - 1.0 < 0.01
    for fn in (kerma, absorbed_dose):
        try:
            fn(-1.0, 0.02, 1.0)
        except ValueError:
            pass
        else:
            raise AssertionError("%s should reject a negative energy" % fn.__name__)


def test_reproduces_example_9_2():
    """S&F Ex. 9.2: kerma rate in water from 0.1-MeV neutrons at 1e10 /cm2/s.

    The physics worth keeping is the weighting: hydrogen is 11% of water by mass
    but takes 97% of the kerma, because f_s = 2A/(A+1)^2 is 0.5 for hydrogen and
    0.11 for oxygen and hydrogen's scattering cross section is 3.7x larger."""
    assert _approx(neutron_recoil_fraction(1), 0.5)
    assert _rel(neutron_recoil_fraction(16), 0.1107, 1e-3)
    c = water_neutron_kerma_coefficient(12.8, 3.5)
    assert _rel(c, 0.4412, 1e-3), "%.5f" % c
    k = neutron_kerma(0.1, c, 1e10)
    assert _rel(k, 0.071, 2e-2), "%.5f" % k
    assert _rel(k * 3600, 254.0, 5e-3)
    # the share carried by hydrogen
    h = 2 * 12.8 * 0.5
    o = 3.5 * neutron_recoil_fraction(16)
    assert _rel(h / (h + o), 0.9706, 1e-3)


def test_neutron_recoil_fraction_shape():
    """f_s = 2A/(A+1)^2 peaks at hydrogen and dies as 2/A -- the same algebra
    that makes light nuclei good moderators in ~NE-13, read as a dose statement
    instead of a slowing-down one."""
    assert max((neutron_recoil_fraction(a), a) for a in range(1, 250))[1] == 1
    for a in (100, 238):
        assert _rel(neutron_recoil_fraction(a), 2.0 / a, 0.05)
    # equivalently (1-alpha)/2 with alpha = ((A-1)/(A+1))^2  [Eq. (6.28)]
    for a in (1, 2, 12, 16, 56, 238):
        alpha = ((a - 1.0) / (a + 1.0)) ** 2
        assert _rel(neutron_recoil_fraction(a), 0.5 * (1 - alpha), 1e-12)
    try:
        neutron_recoil_fraction(0)
    except ValueError:
        pass
    else:
        raise AssertionError("A = 0 should be rejected")


# --- the two errata in the worked examples -------------------------------

def test_example_9_3_is_wrong_by_a_factor_of_one_hundred():
    """S&F Ex. 9.3 states its own inputs and then reports an answer 100x larger
    than they give.  The printed line is

        H = (1)(1.602e-10)(1)(0.03103)(2.122e4) = 10.5 uSv

    and that product is 1.055e-7 Sv = 0.105 uSv.  Nothing about the inputs is in
    doubt: 0.03103 is Appendix C.3's mu_en/rho for water at 1 MeV, and 2.122e4 is
    what the example's own fluence line computes.

    There is a SECOND, independent slip in the same example: the text says the
    source ran for "5 minutes" while the fluence line uses 600 s."""
    phi = point_source_fluence(1e9, 600.0, 1500.0)
    assert _rel(phi, 2.122e4, 1e-3), "%.4e" % phi          # the book's own value
    assert _rel(mass_coefficient("water", 1.0, "en"), 0.03103, 1e-9)
    h = dose_equivalent(absorbed_dose(1.0, 0.03103, 2.122e4),
                        quality_factor("gamma"))
    assert _rel(h * 1e6, 0.1055, 1e-3), "%.4f uSv" % (h * 1e6)
    assert _rel(EXAMPLE_9_3_PRINTED_USV / (h * 1e6), 100.0, 5e-3)
    # 5 minutes would halve it again
    phi5 = point_source_fluence(1e9, 300.0, 1500.0)
    assert _rel(phi5, 1.061e4, 1e-3)
    # and 10.5 uSv is the answer for r = 1.5 m, not 15 m -- a lost factor of 10
    # in the distance, squared
    phi_1p5 = point_source_fluence(1e9, 600.0, 150.0)
    h15 = absorbed_dose(1.0, 0.03103, phi_1p5)
    assert _rel(h15 * 1e6, EXAMPLE_9_3_PRINTED_USV, 5e-3)


def test_example_9_5_number_is_right_and_the_unit_is_not():
    """S&F Ex. 9.5: ingesting 1 mCi 59Fe and 50 uCi 60Co.  Table 9.4 gives
    6.6e3 and 1.0e4 rem/Ci, so

        (1e-3 Ci)(6.6e3) + (5e-5 Ci)(1.0e4) = 6.6 + 0.5 = 7.1 REM,

    and the example prints "7.1 mrem".  Three things went wrong in one line: the
    59Fe coefficient is printed as 6.6 rather than 6.6e3 rem/Ci, the 60Co intake
    as 1e-6 rather than 5e-5 Ci, and the answer's prefix as milli.  The printed
    intermediates do not even reproduce the printed answer -- they give 16.6
    mrem -- which is what makes this unambiguous rather than a matter of taste.

    It matters: 7.1 rem is 71 mSv, thirty times a year's natural background and
    a reportable overexposure.  7.1 mrem is a bus ride."""
    fe = INGESTION_DOSE_COEFFICIENTS["59Fe"]
    co = INGESTION_DOSE_COEFFICIENTS["60Co"]
    assert (fe[2], co[2]) == (6.6e3, 1.0e4)
    rem = 1e-3 * fe[2] + 50e-6 * co[2]
    assert _rel(rem, 7.1, 1e-9), "%.4f rem" % rem
    assert _rel(rem * 10.0, 71.0, 1e-9)                    # mSv
    # the printed intermediates give something else again
    printed = (1e-3 * 6.6 + 1e-6 * 1.0e4) * 1000.0
    assert _rel(printed, 16.6, 1e-9)
    assert not _rel(printed, EXAMPLE_9_5_PRINTED_MREM, 0.5)
    # the Sv/Bq column agrees to 1%, which is all two-figure rounding allows
    sv = committed_effective_dose({"59Fe": 1e-3 * BQ_PER_CI,
                                   "60Co": 50e-6 * BQ_PER_CI})
    assert _rel(sv / SV_PER_REM, rem, 0.02), "%.4f vs %.4f rem" % (sv / SV_PER_REM, rem)
    assert sv > 0.05                                       # tens of mSv, not tens of uSv


def test_table_9_4_two_columns_are_consistent():
    """Table 9.4 lists each coefficient twice, in Sv/Bq and rem/Ci.  The two are
    related by 3.7e12 exactly (3.7e10 Bq/Ci times 100 rem/Sv), so the table
    checks itself -- and every one of its 68 rows passes to within the rounding
    of the two-figure Sv/Bq column."""
    worst, worst_row = 0.0, None
    for nuclide, (f1, sv_bq, rem_ci) in INGESTION_DOSE_COEFFICIENTS.items():
        implied = sv_bq * BQ_PER_CI * 100.0
        err = abs(implied / rem_ci - 1.0)
        if err > worst:
            worst, worst_row = err, nuclide
        assert err < 0.10, "%s: %.4g vs %.4g" % (nuclide, implied, rem_ci)
        assert 0 < f1 <= 1.0
    # the worst row is a one-in-the-last-place rounding, not an error
    assert worst < 0.06, "%s is %.1f%% out" % (worst_row, 100 * worst)
    assert len(INGESTION_DOSE_COEFFICIENTS) == 68
    # 90Sr is the most radiotoxic ingested nuclide in the table, by 2.5x
    ranked = sorted(INGESTION_DOSE_COEFFICIENTS.items(), key=lambda kv: -kv[1][1])
    assert ranked[0][0] == "90Sr"
    assert ranked[0][1][1] / ranked[1][1][1] > 1.7


# --- effective dose ------------------------------------------------------

def test_every_tissue_weighting_set_sums_to_one():
    """The defining property: a uniform whole-body equivalent dose must come back
    as itself.  If the weights did not sum to 1, effective dose would not be
    comparable with whole-body dose and the entire risk framework would leak."""
    for name, w in (("ICRP 1977", ICRP77_TISSUE_WEIGHTS),
                    ("ICRP 1991", ICRP90_TISSUE_WEIGHTS),
                    ("ICRP 2007", ICRP07_TISSUE_WEIGHTS)):
        assert _rel(sum(w.values()), 1.0, 1e-12), "%s sums to %.4f" % (name, sum(w.values()))
        uniform = dict((t, 5.0) for t in w)
        assert _rel(effective_dose(uniform, w), 5.0, 1e-12)
    # the historical drift: gonads down 3x, breast up 2.4x
    assert ICRP77_TISSUE_WEIGHTS["gonads"] == 0.25
    assert ICRP90_TISSUE_WEIGHTS["gonads"] == 0.20
    assert ICRP07_TISSUE_WEIGHTS["gonads"] == 0.08
    assert (ICRP07_TISSUE_WEIGHTS["breast"] / ICRP90_TISSUE_WEIGHTS["breast"]) > 2.0


def test_reproduces_example_9_4():
    """S&F Ex. 9.4: annual internal dose from natural radionuclides, weighted by
    Table 9.2.  36 mrem to lung, 110 to bone surfaces, 50 to red marrow, 36 to
    all other soft tissue."""
    organs = {"lung": 36.0, "bone surface": 110.0, "red marrow": 50.0,
              "gonads": 36.0, "breast": 36.0, "thyroid": 36.0, "remainder": 36.0}
    he = effective_dose(organs, ICRP77_TISSUE_WEIGHTS)
    assert _rel(he, 39.90, 1e-4), "%.3f mrem/y" % he
    # each term, as the book tabulates them
    for organ, contribution in (("lung", 4.32), ("bone surface", 3.30),
                                ("red marrow", 6.00), ("gonads", 9.00),
                                ("breast", 5.40), ("thyroid", 1.08),
                                ("remainder", 10.80)):
        assert _rel(ICRP77_TISSUE_WEIGHTS[organ] * organs[organ], contribution, 1e-9)
    # the same organ doses under the 1991 weights: bone surface is demoted, so
    # the answer barely moves, but the reason is different
    assert _rel(effective_dose(organs, ICRP77_TISSUE_WEIGHTS) / 39.90, 1.0, 1e-4)


def test_effective_dose_refuses_an_organ_it_cannot_weight():
    """The dangerous failure is silent omission: an unweighted organ contributes
    zero, so the answer still looks like an effective dose and is too LOW.  It
    always errs toward declaring an exposure safe, so it must raise."""
    try:
        effective_dose({"lung": 1.0, "pancreas": 50.0}, ICRP90_TISSUE_WEIGHTS)
    except ValueError as exc:
        assert "pancreas" in str(exc)
    else:
        raise AssertionError("an unweighted organ should be refused")
    # 'red marrow' is the 1977 spelling and 'bone marrow' the 1991 one, so
    # passing the wrong set is caught rather than silently dropping 12%
    try:
        effective_dose({"red marrow": 1.0}, ICRP90_TISSUE_WEIGHTS)
    except ValueError:
        pass
    else:
        raise AssertionError("the 1977 organ name should not pass 1991 weights")


def test_quality_factor_refuses_to_guess():
    """Table 9.1.  QF spans a factor of 20, so a default of 1 is not a
    conservative fallback -- it is a twenty-fold understatement for fast neutrons
    and alphas.  `quality_factor` raises instead."""
    assert quality_factor("gamma") == 1.0
    assert quality_factor("beta") == 1.0
    assert quality_factor("alpha") == 20.0
    for e, qf in ((0.001, 5.0), (0.05, 10.0), (0.5, 20.0), (1.0, 20.0),
                  (5.0, 10.0), (50.0, 5.0)):
        assert quality_factor("neutron", e) == qf, "%g MeV" % e
    # the peak is at fission-spectrum energies, which is not an accident
    assert quality_factor("neutron", 1.0) == 20.0
    # the two standards bodies disagree about protons, so the caller must choose
    assert quality_factor("proton") == 5.0
    assert quality_factor("proton", authority="NCRP") == 2.0
    for bad in (("cosmic ray", None), ("muon", None)):
        try:
            quality_factor(*bad)
        except ValueError as exc:
            assert "Refusing" in str(exc) or "no Table 9.1" in str(exc)
        else:
            raise AssertionError("%r should be refused" % (bad,))
    try:
        quality_factor("neutron")
    except ValueError:
        pass
    else:
        raise AssertionError("a neutron without an energy should be refused")


def test_dose_equivalent_is_where_the_factor_of_twenty_lives():
    """The same 1 Gy is 1 Sv of gammas and 20 Sv of alphas.  A dose quoted
    without its radiation type is not a statement about hazard."""
    d = 1.0
    assert _approx(dose_equivalent(d, quality_factor("gamma")), 1.0)
    assert _approx(dose_equivalent(d, quality_factor("alpha")), 20.0)
    assert _approx(dose_equivalent(d, quality_factor("neutron", 1.0)), 20.0)
    assert _approx(dose_equivalent(d, quality_factor("neutron", 30.0)), 5.0)
    for bad in ((-1.0, 1.0), (1.0, 0.0), (1.0, -2.0)):
        try:
            dose_equivalent(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


# --- the chapter's problems ---------------------------------------------

def test_problem_9_1_tritium_average_beta_energy_is_keV_not_MeV():
    """S&F Ch. 9 Prob. 1 gives tritium's average beta energy as "5.37 MeV".  A
    tritium beta cannot exceed 18.6 keV -- that is the entire decay energy -- and
    the book's own Appendix D lists 5.67 keV/decay.  The authors' solution manual
    restates the problem with "keV" and then substitutes MeV anyway, and finally
    reports 2.196e-7 Gy/h as "22.0 uGy/h", which is 0.2196 uGy/h.

    The physically correct answer, from Appendix D, is 0.232 nGy/h."""
    conc_ci_per_l = 2.3e-12
    decays_per_h_per_l = conc_ci_per_l * BQ_PER_CI * 3600.0
    assert _rel(decays_per_h_per_l, 306.36, 1e-4)
    rho_kg_per_l = 0.0012

    def kerma_rate(e_mev):
        return decays_per_h_per_l * e_mev * MEV_TO_J / rho_kg_per_l

    # with the printed MeV, which is what the solution manual actually computed
    with_mev = kerma_rate(PROBLEM_9_1_PRINTED_MEV)
    assert _rel(with_mev, 2.196e-7, 1e-3), "%.4e" % with_mev
    assert _rel(with_mev * 1e6, 0.2196, 1e-3)          # NOT the printed 22.0 uGy/h
    # with the book's own Appendix D value
    correct = kerma_rate(5.67e-3)
    assert _rel(correct * 1e9, 0.232, 1e-2), "%.4f nGy/h" % (correct * 1e9)
    assert _rel(with_mev / correct, 1000.0 * 5.37 / 5.67, 1e-9)
    # sanity: a whole year of it is far below any natural background component
    assert correct * 24 * 365 * 1e3 < 1e-2             # mGy/y


def test_reproduces_the_solution_manual_problems_2_and_3():
    """The authors' worked solutions for a 137Cs point source, air and water.
    Every interpolated coefficient in them is reproduced exactly from the
    extracted Appendix C.3 by LINEAR interpolation, which is the method their
    text names.

    Their Prob. 2 solves 900 uCi at 2.5 m; the textbook states 700 uCi at 2 m.
    Part (a) of the solution carries a stale flux, 43.54, from the textbook's
    version -- and 43.54 is exactly the flux for 700 uCi at 2 m, which is how we
    know it is stale rather than wrong."""
    e = 0.662
    mu_en_air = mass_coefficient("air", e, "en", interpolation="linear")
    mu_tr_air = mass_coefficient("air", e, "tr", interpolation="linear")
    mu_en_w = mass_coefficient("water", e, "en", interpolation="linear")
    assert _rel(mu_en_air, 0.02931, 5e-4)      # all three printed to 4 decimals
    assert _rel(mu_tr_air, 0.02937, 5e-4)
    assert _rel(mu_en_w, 0.03260, 5e-4)

    # --- Problem 2, the solution manual's version: 900 uCi, 0.845/decay, 2.5 m
    s = 900e-6 * BQ_PER_CI * 0.845
    phi = point_source_fluence(s, 1.0, 250.0)
    assert _rel(phi, 35.83, 1e-3), "%.3f" % phi
    x = exposure(e, mu_en_air, phi)
    assert _rel(x * 3600 * 1e6, 45.9, 3e-3), "%.2f uR/h" % (x * 3600 * 1e6)
    k = kerma(e, mu_tr_air, phi)
    assert _rel(k * 3.6e9, 0.402, 3e-3)
    h = absorbed_dose(e, mu_en_w, phi)
    assert _rel(h * 3.6e9, 0.446, 3e-3)

    # the stale 43.54 is the textbook's own geometry, which identifies it
    stale = point_source_fluence(700e-6 * BQ_PER_CI * 0.845, 1.0, 200.0)
    assert _rel(stale, 43.54, 1e-3), "%.3f" % stale

    # --- Problem 3: the same source in water, 0.4 m (the solution's geometry)
    mu_w = linear_coefficient("water", e, "total", interpolation="linear")
    assert _rel(mu_w, 0.08604, 1e-4)
    phi3 = point_source_fluence(s, 1.0, 40.0, mu_w)
    assert _rel(phi3, 44.80, 3e-3), "%.3f" % phi3
    assert _rel(exposure(e, mu_en_air, phi3) * 3600 * 1e6, 57.4, 5e-3)
    assert _rel(kerma(e, mu_tr_air, phi3) * 3.6e9, 0.502, 5e-3)
    assert _rel(absorbed_dose(e, mu_en_w, phi3) * 3.6e9, 0.558, 5e-3)


def test_reproduces_problems_4_and_5_and_finds_the_typo_between_them():
    """Problems 4 and 5 are the same 16N and 43K sources, in air and then in
    iron.  Problem 5 is reproduced exactly.  Problem 4(a) is not -- and Problem 5
    is what proves Problem 4 wrong.

    The solution's 16N table for Prob. 4 lists f E (mu_en/rho) = 0.08931 for the
    6.129 MeV line, but 0.690 x 6.129 x 0.01639 = 0.06931.  The SAME product
    appears in Prob. 5 multiplied by exp(-2.403), where it is printed as
    0.006269 -- and 0.006269/exp(-2.403) = 0.06931.  So 0.08931 is a transcribed
    6 read as an 8, and Prob. 4(a)'s answer is 1.27 mGy/h, not 1.611."""
    s = 1e-3 * BQ_PER_CI            # 1 mCi = 3.7e7 Bq
    # Problem 5: dose in air inside iron, reproduced exactly
    d5_n16 = photon_dose_rate_from_lines(N16_GAMMAS, s, 10.0, "air", "iron")
    d5_k43 = photon_dose_rate_from_lines(K43_GAMMAS, s, 10.0, "air", "iron")
    assert _rel(d5_n16 * 1e3, 0.1153, 5e-3), "%.5f mGy/h" % (d5_n16 * 1e3)

    # Problem 4: dose in air, no attenuation
    d4_n16 = photon_dose_rate_from_lines(N16_GAMMAS, s, 10.0, "air")
    assert _rel(d4_n16 * 1e3, 1.2725, 5e-3), "%.4f mGy/h" % (d4_n16 * 1e3)
    assert _rel(PROBLEM_9_4A_PRINTED_MGY_PER_H / (d4_n16 * 1e3), 1.2660, 5e-3)

    # the arithmetic that identifies the typo
    assert _rel(0.690 * 6.129 * 0.01639, 0.06931, 1e-3)
    assert _rel(0.006269 / math.exp(-0.2403 * 10.0), 0.06931, 3e-3)
    assert _rel(0.08931 - 0.06931, 0.02, 1e-9)      # a single mis-set digit

    # 43K in air: 1.2% high against the book, entirely from ONE coefficient --
    # the solution reads the 0.8 MeV row for the 0.6175 MeV line.
    d4_k43 = photon_dose_rate_from_lines(K43_GAMMAS, s, 10.0, "air")
    assert _rel(d4_k43 * 1e3, 0.4793, 5e-3), "%.4f mGy/h" % (d4_k43 * 1e3)
    assert _rel(mass_coefficient("air", 0.6175, "en", interpolation="linear"),
                0.02947, 1e-3)
    assert _rel(mass_coefficient("air", 0.80, "en"), 0.02882, 1e-9)   # what they used
    # in iron the same slip is amplified by the exponential to a factor of 1.73
    assert _rel(1.654e-3 / (d5_k43 * 1e3), 1.73, 2e-2), "%.5f" % (d5_k43 * 1e3)
    assert _rel(d5_k43 * 1e6, 0.954, 5e-3)


def test_appendix_D_lines_match_the_book():
    """The gamma lines used above are the extracted Appendix D, not retyped from
    the solution manual: all eight energies and frequencies agree."""
    import csv
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.normpath(os.path.join(here, "..", "..", "data_tables",
                                         "D1_decay_radiation.csv"))
    got = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["nuclide"] in ("16N", "43K") and r["group"] == "gamma_xray":
                got.setdefault(r["nuclide"], []).append(
                    (float(r["E_keV"]) / 1000.0, float(r["freq_pct"]) / 100.0))
    for nuclide, expected in (("16N", N16_GAMMAS), ("43K", K43_GAMMAS)):
        assert len(got[nuclide]) == len(expected)
        for (e0, f0), (e1, f1) in zip(sorted(got[nuclide]), sorted(expected)):
            assert _rel(e0, e1, 1e-9) and _rel(f0, f1, 1e-9)


def test_the_rule_of_thumb_and_where_it_stops_working():
    """Prob. 9.6's 6CEN/r^2 (C in Ci, r in feet) is exact where
    (mu_en/rho)_air = 0.02866 cm2/g, and air's coefficient is within 20% of that
    over more than a decade of energy -- which is why the rule survives.

    It fails in both directions and for different reasons: below ~0.1 MeV the
    photoelectric effect drives mu_en up, and above ~2 MeV Compton scattering
    drives it down.  Above 5 MeV the rule is 65% high, which is not conservative
    in the direction that matters for shielding design."""
    # the SI restatement asked for in part (a)
    si = 6.0 * 0.3048 ** 2 / BQ_PER_CI
    assert _rel(si, 1.507e-11, 1e-3), "%.4e" % si
    for c_ci, e, n, r_ft in ((1.0, 1.0, 1.0, 3.0), (0.1, 0.662, 0.85, 10.0)):
        a = rule_of_thumb_exposure_rate(c_ci, e, n, r_ft)
        b = 1.5065e-11 * (c_ci * BQ_PER_CI) * e * n / (r_ft * 0.3048) ** 2
        assert _rel(a, b, 1e-3)
    # exactness condition
    exact_coeff = 6.0 / (EXPOSURE_PREFACTOR * 3600.0 * BQ_PER_CI
                         / (4 * math.pi * 30.48 ** 2))
    assert _rel(exact_coeff, 0.02866, 5e-3), "%.5f" % exact_coeff
    lo, hi = rule_of_thumb_valid_range(0.20)
    assert _rel(lo, 0.119, 0.05) and _rel(hi, 1.89, 0.05), "%.3f-%.3f" % (lo, hi)
    lo5, hi5 = rule_of_thumb_valid_range(0.05)
    assert lo5 > lo and hi5 < hi
    assert _rel(lo5, 0.229, 0.05) and _rel(hi5, 1.12, 0.05), "%.3f-%.3f" % (lo5, hi5)
    # it is 65% HIGH at 5 MeV -- conservative for a dose estimate, wasteful for a
    # shield, and simply wrong either way
    ratio = (rule_of_thumb_exposure_rate(1.0, 5.0, 1.0, 1.0)
             / exposure_rate_exact(1.0, 5.0, 1.0, 1.0))
    assert _rel(ratio, 1.647, 1e-2)
    try:
        rule_of_thumb_valid_range(0.0)
    except ValueError:
        pass
    else:
        raise AssertionError("a zero tolerance should be rejected")


# --- background, and the interpolation choice ----------------------------

def test_natural_background_tables_add_up():
    """Tables 9.5 and 9.6.  The world average is 2.4 mSv/y, half of it radon.
    The U.S. total is 3.0 mSv/y, and two thirds of THAT is radon -- which is the
    single most useful fact in the chapter, because it is the yardstick every
    other exposure gets compared against."""
    world = sum(NATURAL_BACKGROUND_WORLD.values())
    assert _rel(world, 2.4, 1e-9), "%.3f mSv/y" % world
    assert _rel(NATURAL_BACKGROUND_WORLD["inhalation"] / world, 0.50, 0.02)
    external = (NATURAL_BACKGROUND_WORLD["cosmic high-LET"]
                + NATURAL_BACKGROUND_WORLD["cosmic low-LET"]
                + NATURAL_BACKGROUND_WORLD["terrestrial gamma"])
    assert _rel(external, 0.9, 1e-9)
    us = sum(NATURAL_BACKGROUND_US.values())
    assert _rel(us, 2.95, 1e-9) and round(us, 1) == 3.0
    assert _rel(NATURAL_BACKGROUND_US["inhaled"] / us, 0.678, 1e-2)
    # the man-made share the book quotes as 18%
    assert _rel(sum(US_MANMADE_BREAKDOWN.values()), 1.0, 1e-9)
    assert _rel(US_MANMADE_MSV / (us + US_MANMADE_MSV), 0.18, 0.02)
    # medical is 79% of the man-made part
    assert _rel(US_MANMADE_BREAKDOWN["medical x rays"]
                + US_MANMADE_BREAKDOWN["nuclear medicine"], 0.79, 1e-9)


def test_linear_vs_loglog_interpolation():
    """S&F's solutions interpolate the Appendix C.3 grid LINEARLY; ~NE-11 and
    ~NE-12 use log-log, which is right because the coefficients are close to
    power laws between grid points.  The difference is negligible for mu_en, and
    it is not negligible for the total mu inside an exponential."""
    e = 0.662
    lin_en = mass_coefficient("water", e, "en", interpolation="linear")
    log_en = mass_coefficient("water", e, "en", interpolation="loglog")
    assert abs(lin_en / log_en - 1.0) < 1.5e-3        # dose: 0.08%, irrelevant
    lin_mu = mass_coefficient("water", e, "total", interpolation="linear")
    log_mu = mass_coefficient("water", e, "total", interpolation="loglog")
    assert 3e-3 < abs(lin_mu / log_mu - 1.0) < 1e-2   # attenuation: 0.6%
    # amplified through 40 cm of water
    r = 40.0
    ratio = math.exp(-(lin_mu - log_mu) * MATERIALS["water"] * r)
    assert 0.97 < ratio < 0.99, "%.4f" % ratio
    # both agree exactly on tabulated grid points
    for e0 in (0.6, 0.8, 1.0):
        assert _approx(mass_coefficient("air", e0, "en", interpolation="linear"),
                       mass_coefficient("air", e0, "en", interpolation="loglog"))
    try:
        mass_coefficient("water", 0.662, "en", interpolation="cubic")
    except ValueError:
        pass
    else:
        raise AssertionError("an unknown interpolation should be refused")
    try:
        mass_coefficient("water", 1e4, "en")
    except ValueError:
        pass
    else:
        raise AssertionError("an out-of-range energy should be refused")


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
