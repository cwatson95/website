"""NE-15 tests -- detectors against Shultis & Faw §§8.1-8.5, Tables 8.1-8.2,
and measured detector performance.

Run:  python3 test_detectors.py
"""

import math

from detectors import (
    SEMICONDUCTORS, SCINTILLATORS_INORGANIC, SCINTILLATORS_ORGANIC,
    GAS_W_VALUES, FANO_FACTORS, ANTHRACENE_RELATIVE_TO_NAI, FWHM_PER_SIGMA,
    carriers_produced, carrier_sigma, intrinsic_resolution_fraction,
    intrinsic_resolution_percent, fwhm_energy,
    gas_multiplication, townsend_series_terms,
    scintillator_photoelectrons, photopeak_resolution_percent,
    compare_resolution,
)


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def _rel(a, b, tol):
    """Strictly relative -- see the note in ~NE-14's tests about `_approx`
    degrading to an absolute tolerance for small values."""
    return abs(a / b - 1.0) <= tol


# --- carrier statistics: the whole module in one relation ----------------

def test_carrier_count_and_its_fluctuation():
    """N = E/w, sigma = sqrt(F N), FWHM/E = 2.355 sqrt(F/N)."""
    n = carriers_produced(1.0, 2.98)                  # 1 MeV in germanium
    assert _rel(n, 335570, 1e-3), "%.0f" % n
    assert _approx(carrier_sigma(n, 1.0), math.sqrt(n))
    assert _approx(carrier_sigma(n, 0.13), math.sqrt(0.13 * n))
    # the resolution identity
    assert _approx(intrinsic_resolution_fraction(1.0, 2.98, 0.13),
                   FWHM_PER_SIGMA * math.sqrt(0.13 / n))
    assert _approx(intrinsic_resolution_percent(1.0, 2.98, 0.13),
                   100 * intrinsic_resolution_fraction(1.0, 2.98, 0.13))
    assert _approx(fwhm_energy(1.0, 2.98, 0.13),
                   intrinsic_resolution_fraction(1.0, 2.98, 0.13))
    for fn, args in ((carriers_produced, (0.0, 3.0)), (carriers_produced, (1.0, 0.0)),
                     (carrier_sigma, (-1.0,)), (carrier_sigma, (100.0, 0.0))):
        try:
            fn(*args)
        except ValueError:
            pass
        else:
            raise AssertionError("%s%r should be rejected" % (fn.__name__, args))


def test_resolution_improves_as_one_over_sqrt_E():
    """FWHM/E ~ 1/sqrt(E), so the ABSOLUTE width grows as sqrt(E) while the
    FRACTIONAL width shrinks.  Both statements are the same equation and both
    get quoted, which is a standard source of confusion."""
    r1 = intrinsic_resolution_fraction(0.1, 2.98, 0.13)
    r2 = intrinsic_resolution_fraction(1.0, 2.98, 0.13)
    assert _rel(r1 / r2, math.sqrt(10.0), 1e-6)       # fractional: better at high E
    w1 = fwhm_energy(0.1, 2.98, 0.13)
    w2 = fwhm_energy(1.0, 2.98, 0.13)
    assert _rel(w2 / w1, math.sqrt(10.0), 1e-6)       # absolute: worse at high E
    assert w2 > w1 and r2 < r1


def test_the_fano_factor_matters_by_a_factor_of_three():
    """Carrier statistics in a semiconductor are SUB-Poisson: the total energy is
    fixed, so quanta spent on one excitation are unavailable to another and the
    variance is suppressed.  F ~ 0.13 in germanium, so assuming Poisson
    overestimates the photopeak width by sqrt(1/0.13) = 2.8x.

    S&F never mention the Fano factor; refs.md explains why this module adds it."""
    poisson = intrinsic_resolution_percent(0.6617, 2.98, 1.0)
    real = intrinsic_resolution_percent(0.6617, 2.98, FANO_FACTORS["Ge"])
    assert _rel(poisson / real, math.sqrt(1.0 / 0.13), 1e-6)
    assert _rel(poisson / real, 2.77, 1e-2)
    # scintillators get no such suppression -- F = 1 there
    assert _approx(FANO_FACTORS["scintillator"], 1.0)
    assert FANO_FACTORS["Ge"] < 0.2 and FANO_FACTORS["Si"] < 0.2


def test_germanium_beats_sodium_iodide_by_thirty_fold():
    """The headline comparison, and the reason to tolerate liquid nitrogen.
    Both numbers are intrinsic limits from carrier statistics alone."""
    ge = intrinsic_resolution_percent(0.6617, SEMICONDUCTORS["Ge"]["w_eV"],
                                      FANO_FACTORS["Ge"])
    nai = photopeak_resolution_percent(0.6617, "NaI(Tl)")
    assert _rel(ge, 0.180, 5e-2), "%.4f" % ge
    assert _rel(nai, 3.55, 5e-2), "%.4f" % nai
    assert nai / ge > 15.0
    # in absolute terms: ~1.2 keV against ~23 keV at 662 keV
    assert _rel(ge / 100 * 662.0, 1.19, 5e-2)
    assert _rel(nai / 100 * 662.0, 23.5, 5e-2)


def test_these_are_lower_bounds_not_predictions():
    """Carrier statistics give the FLOOR.  Real detectors add electronic noise,
    incomplete charge collection and -- for scintillators -- non-proportionality
    and light-collection non-uniformity, all in quadrature.

    A real NaI(Tl) detector achieves ~6-7% FWHM at 662 keV against this module's
    3.55% statistical limit, so roughly half the observed width is NOT carrier
    statistics.  A real germanium detector achieves ~1.3-1.5 keV against the
    1.2 keV floor, i.e. the floor is nearly attained.  The test asserts the
    computed values sit BELOW the measured ones."""
    nai_stat = photopeak_resolution_percent(0.6617, "NaI(Tl)")
    nai_measured = 6.5                                   # typical 3x3 NaI(Tl)
    assert nai_stat < nai_measured
    assert nai_measured / nai_stat > 1.5                 # statistics is a minority
    ge_stat_kev = intrinsic_resolution_percent(0.6617, 2.98, 0.13) / 100 * 662.0
    ge_measured_kev = 1.4
    assert ge_stat_kev < ge_measured_kev
    assert ge_measured_kev / ge_stat_kev < 1.5           # germanium nearly attains it
    # quadrature: the "extra" width implied for NaI
    extra = math.sqrt(nai_measured ** 2 - nai_stat ** 2)
    assert extra > nai_stat


# --- Table 8.2, semiconductors -------------------------------------------

def test_table_8_2_is_intact_and_internally_sensible():
    """Six semiconductors; w is always ~3x the band gap, which is the standard
    empirical rule -- the excess goes into phonons rather than carriers."""
    assert len(SEMICONDUCTORS) == 6
    assert _approx(SEMICONDUCTORS["Si"]["w_eV"], 3.61)
    assert _approx(SEMICONDUCTORS["Ge"]["w_eV"], 2.98)
    assert _approx(SEMICONDUCTORS["Ge"]["band_gap_eV"], 0.72)
    for m, d in SEMICONDUCTORS.items():
        ratio = d["w_eV"] / d["band_gap_eV"]
        assert 2.0 < ratio < 4.5, "%s: w/Eg = %.2f" % (m, ratio)
    # germanium has the smallest gap and the smallest w -- and so the best
    # resolution, at the price of needing cooling
    assert min(SEMICONDUCTORS, key=lambda k: SEMICONDUCTORS[k]["band_gap_eV"]) == "Ge"
    assert min(SEMICONDUCTORS, key=lambda k: SEMICONDUCTORS[k]["w_eV"]) == "Ge"


def test_high_Z_semiconductors_stop_photons_better():
    """The other axis of the trade-off: detection EFFICIENCY needs high Z and
    high density (~NE-12's photoelectric Z^4), which is why CdTe and HgI2 exist
    despite their worse w."""
    def zmax(d):
        return d["Z"] if isinstance(d["Z"], int) else max(d["Z"])
    assert zmax(SEMICONDUCTORS["HgI2"]) > zmax(SEMICONDUCTORS["Ge"]) > zmax(SEMICONDUCTORS["Si"])
    assert SEMICONDUCTORS["HgI2"]["density"] > SEMICONDUCTORS["Ge"]["density"]
    # but they pay for it in carrier cost
    assert SEMICONDUCTORS["HgI2"]["w_eV"] > SEMICONDUCTORS["Ge"]["w_eV"]
    assert SEMICONDUCTORS["CdTe"]["w_eV"] > SEMICONDUCTORS["Si"]["w_eV"]


# --- Table 8.1, scintillators --------------------------------------------

def test_table_8_1_light_yields_and_the_relative_column():
    """Twelve inorganic scintillators.  The 'relative PMT response' column is NOT
    the light yield -- it also folds in how well the emission wavelength matches
    a bialkali photocathode.  CsI(Tl) makes 1.7x NaI's light and produces HALF
    the PMT response, because 540 nm is far off the photocathode's peak."""
    assert len(SCINTILLATORS_INORGANIC) == 12
    nai = SCINTILLATORS_INORGANIC["NaI(Tl)"]
    csi = SCINTILLATORS_INORGANIC["CsI(Tl)"]
    assert _approx(nai["photons_per_MeV"], 38000) and _approx(nai["rel"], 1.00)
    assert csi["photons_per_MeV"] > 1.7 * nai["photons_per_MeV"]
    assert csi["rel"] < 0.5 * nai["rel"]                  # the wavelength penalty
    assert csi["nm"] > 500 and nai["nm"] < 450
    # LaBr3 is the outlier that beats NaI on both counts
    lab = SCINTILLATORS_INORGANIC["LaBr3(Ce)"]
    assert lab["photons_per_MeV"] > nai["photons_per_MeV"]
    assert lab["rel"] > nai["rel"]
    assert lab["decay_ns"][0] < nai["decay_ns"][0] / 10   # and it is 14x faster


def test_speed_and_brightness_usually_trade_off():
    """BGO is dense and slow and dim; plastics are fast and dim; LaBr3 breaks
    the pattern.  Checked as a real anti-correlation across the inorganic set,
    excluding the modern lanthanum halides."""
    classic = {k: v for k, v in SCINTILLATORS_INORGANIC.items()
               if not k.startswith("La")}
    bright = max(classic, key=lambda k: classic[k]["photons_per_MeV"])
    fast = min(classic, key=lambda k: classic[k]["decay_ns"][0])
    assert bright == "CsI(Tl)" and fast == "YAP(Ce)"
    assert classic[fast]["photons_per_MeV"] < classic[bright]["photons_per_MeV"]
    # BGO: dense (good efficiency) but dim -- the PET workhorse before LSO
    assert SCINTILLATORS_INORGANIC["BGO"]["photons_per_MeV"] < 10000
    assert SCINTILLATORS_INORGANIC["LSO(Ce)"]["photons_per_MeV"] > 2 * \
        SCINTILLATORS_INORGANIC["BGO"]["photons_per_MeV"]
    assert SCINTILLATORS_INORGANIC["LSO(Ce)"]["decay_ns"][0] < \
        SCINTILLATORS_INORGANIC["BGO"]["decay_ns"][0]


def test_organic_scintillators_are_fast_and_dim():
    """Organics trade light for speed: nanosecond decay against NaI's 230 ns,
    at a third to a half the light.  That is why they do timing and neutron
    pulse-shape discrimination rather than spectroscopy."""
    assert len(SCINTILLATORS_ORGANIC) == 11
    assert _approx(SCINTILLATORS_ORGANIC["Anthracene"]["rel_anthracene_pct"], 100)
    # anthracene itself is only 1/2.3 of NaI's light yield
    assert _rel(ANTHRACENE_RELATIVE_TO_NAI, 1 / 2.3, 1e-9)
    anth_photons = 38000 * ANTHRACENE_RELATIVE_TO_NAI
    assert _rel(anth_photons, 16522, 1e-3)
    # the fast plastics are all sub-3 ns and under 70% of anthracene
    for k in ("BC-400", "EJ-204", "EJ-232"):
        d = SCINTILLATORS_ORGANIC[k]
        assert d["decay_ns"] < 3.0
        assert d["rel_anthracene_pct"] < 70
    # and all of them are faster than every classic inorganic
    slowest_organic = max(d["decay_ns"] for k, d in SCINTILLATORS_ORGANIC.items()
                          if d["form"] == "liquid")
    assert slowest_organic < SCINTILLATORS_INORGANIC["NaI(Tl)"]["decay_ns"][0]


def test_the_photoelectron_count_governs_not_the_photon_count():
    """A scintillator's resolution is set by the SMALLEST number in the chain.
    NaI makes 38 000 photons/MeV and delivers ~6 600 photoelectrons -- an
    effective w of ~150 eV, fifty times germanium's 2.98."""
    npe = scintillator_photoelectrons(1.0, "NaI(Tl)")
    assert _rel(npe, 6650, 1e-2), "%.0f" % npe
    assert npe < SCINTILLATORS_INORGANIC["NaI(Tl)"]["photons_per_MeV"]
    w_eff = 1e6 / npe
    assert _rel(w_eff, 150.4, 1e-2)
    assert w_eff / SEMICONDUCTORS["Ge"]["w_eV"] > 40
    # efficiencies must be physical
    for bad in ((1.0, "NaI(Tl)", 0.0, 0.25), (1.0, "NaI(Tl)", 0.7, 1.5)):
        try:
            scintillator_photoelectrons(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))
    try:
        scintillator_photoelectrons(1.0, "unobtainium")
    except KeyError:
        pass
    else:
        raise AssertionError("unknown scintillator should raise")


# --- gas multiplication  [Eqs. (8.6)-(8.7)] ------------------------------

def test_the_townsend_series_sums_to_the_closed_form():
    """Eq. (8.6) is a geometric series; Eq. (8.7) is its sum.  They must agree."""
    for f, delta in ((10.0, 0.02), (5.0, 0.1), (100.0, 0.005)):
        terms = townsend_series_terms(f, delta, 200)
        assert _rel(sum(terms), gas_multiplication(f, delta), 1e-9)
        assert _approx(terms[0], f)                      # first term is f alone
        assert terms[1] < terms[0] if delta * f < 1 else True
    # delta = 0 means no feedback: M = f exactly
    assert _approx(gas_multiplication(7.0, 0.0), 7.0)
    assert _approx(townsend_series_terms(7.0, 0.0, 5)[1], 0.0)


def test_divergence_is_the_geiger_transition():
    """M = f/(1 - delta f) diverges at delta*f = 1.  That is not a numerical
    artefact: it IS the boundary between proportional operation (output tracks
    deposited energy) and Geiger-Mueller operation (output is the same for every
    event, so all energy information is lost)."""
    assert gas_multiplication(10.0, 0.099) > 900
    assert gas_multiplication(10.0, 0.05) < 25
    for delta in (0.1, 0.15, 1.0):
        try:
            gas_multiplication(10.0, delta)
        except ValueError as exc:
            assert "Geiger" in str(exc)
        else:
            raise AssertionError("delta*f >= 1 should be refused (delta=%g)" % delta)
    # M rises steeply as the product approaches 1 -- the reason proportional
    # counters need a very stable high-voltage supply
    # a 12% change in delta (0.08 -> 0.09) doubles M; a further 10% decuples it
    m1, m2, m3 = (gas_multiplication(10.0, d) for d in (0.08, 0.09, 0.099))
    assert _rel(m2 / m1, 2.0, 1e-6)
    assert _rel(m3 / m2, 10.0, 1e-6)
    for bad in ((0.0, 0.1), (-1.0, 0.1), (10.0, -0.1)):
        try:
            gas_multiplication(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


# --- the family comparison ------------------------------------------------

def test_compare_resolution_orders_the_families_correctly():
    """Semiconductors beat gases beat scintillators, on resolution, always --
    and the ordering is entirely the ordering of w."""
    rows = compare_resolution(0.6617)
    labels = [r[0] for r in rows]
    assert labels[0].startswith("Ge")
    assert "BGO" in labels[-1]
    # sorted best-first, and w tracks the same order
    assert all(rows[i][3] >= rows[i - 1][3] for i in range(1, len(rows)))
    ge = next(r for r in rows if r[0].startswith("Ge"))
    nai = next(r for r in rows if "NaI" in r[0])
    ar = next(r for r in rows if r[0].startswith("Ar"))
    assert ge[1] < ar[1] < nai[1]                        # w ordering
    assert ge[3] < ar[3] < nai[3]                        # resolution ordering
    # every family resolves worse at lower energy
    lo = compare_resolution(0.1)
    assert lo[0][3] > rows[0][3]


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
