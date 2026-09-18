"""NE-27 tests -- medical applications against Shultis & Faw Chapter 14 and
Tables 14.1-14.7.

Run:  python3 test_medical.py
"""

import csv
import math
import os

from medical import (
    HC_KEV_ANGSTROM, M_E_C2_KEV, ANODE_LINES, ATOMIC_NUMBER, PET_NUCLIDES,
    SPECT_TRACERS, THERAPY_MODALITIES, CANCER_LIFETIME_RISK, CT_NOBEL,
    CANCER_2004, CANCER_2004_TOTALS, pinhole_resolution,
    spect_system_resolution,
    xray_energy, xray_wavelength, moseley_k_alpha, hounsfield_unit,
    mu_from_hounsfield, contrast_ratio, positron_range_mm, beta_mean_fraction,
    coincidence_window_length, activity_after_transport, usable_transport_time,
    annihilation_photon_energy, therapeutic_ratio, brachytherapy_dose_rate,
)


def _rel(a, b, tol):
    return abs(a / b - 1.0) <= tol


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def test_table_14_2_lists_the_same_photons_twice():
    """Every wavelength/energy pair in Table 14.2 reproduces from E = hc/lambda
    to better than 0.02% -- so the two columns are one measurement expressed
    twice, and the table is internally consistent."""
    worst = 0.0
    for el, lines in ANODE_LINES.items():
        for line, (lam, e, kv) in lines.items():
            err = abs(xray_energy(lam) / e - 1.0)
            worst = max(worst, err)
            assert err < 3e-4, "%s %s: %.4f vs %.4f" % (el, line, xray_energy(lam), e)
    assert worst < 3e-4, "%.2e" % worst
    # round trip
    for e in (17.5, 59.3, 140.5):
        assert _rel(xray_energy(xray_wavelength(e)), e, 1e-12)
    # K lines always exceed L lines, and the excitation voltage exceeds the line
    for el, lines in ANODE_LINES.items():
        k = [v[1] for n, v in lines.items() if n.startswith("K")]
        l = [v[1] for n, v in lines.items() if n.startswith("L")]
        assert min(k) > max(l), el
        # the tube voltage must exceed the line it excites, always
        for n, (lam, e, kv) in lines.items():
            assert kv > e, "%s %s: %.3f kV vs %.3f keV" % (el, n, kv, e)
    for fn in (xray_energy, xray_wavelength):
        try:
            fn(0.0)
        except ValueError:
            pass
        else:
            raise AssertionError("%s should reject zero" % fn.__name__)


def test_anode_choice_is_energy_choice():
    """Moseley's law estimates Table 14.2's K-alpha lines to 2% for Mo and Rh
    and 8% for W -- the screening approximation degrades at high Z.

    The consequence is the design point: a characteristic line cannot be tuned,
    only replaced. Mammography needs ~17-20 keV to exploit the photoelectric
    contrast of soft tissue, so it uses a molybdenum anode; general radiography
    needs penetration, so it uses tungsten at 59 keV."""
    for el, tol in (("Mo", 0.03), ("Rh", 0.03), ("W", 0.10)):
        est = moseley_k_alpha(ATOMIC_NUMBER[el])
        true = ANODE_LINES[el]["Ka1"][1]
        assert _rel(est, true, tol), "%s: %.2f vs %.2f" % (el, est, true)
    # and Moseley is monotone in Z, as the physics demands
    zs = sorted(ATOMIC_NUMBER.values())
    assert [moseley_k_alpha(z) for z in zs] == sorted(moseley_k_alpha(z) for z in zs)
    # Mo's K lines bracket the mammographic window S&F name (17.5 and 19.6 keV)
    assert _rel(ANODE_LINES["Mo"]["Ka1"][1], 17.5, 2e-3)
    assert _rel(ANODE_LINES["Mo"]["Kb1"][1], 19.6, 2e-3)
    # tungsten's K-alpha is 3.4x higher: a different machine, not a setting
    assert _rel(ANODE_LINES["W"]["Ka1"][1] / ANODE_LINES["Mo"]["Ka1"][1], 3.39, 1e-2)
    try:
        moseley_k_alpha(1)
    except ValueError:
        pass
    else:
        raise AssertionError("Z = 1 should be refused")


def test_hounsfield_units_are_calibrated_attenuation():
    """HU = 1000(mu - mu_w)/mu_w. Water is 0 and air is -1000 by construction,
    which is what makes a CT number comparable between machines -- it is ~NE-11's
    mu, calibrated at two points."""
    assert _approx(hounsfield_unit(0.206), 0.0)
    assert _approx(hounsfield_unit(0.0), -1000.0)
    assert _rel(hounsfield_unit(0.500), 1427.2, 1e-3)
    for hu in (-1000.0, -100.0, 0.0, 1000.0):
        assert _rel(hounsfield_unit(mu_from_hounsfield(hu)) + 1001,
                    hu + 1001, 1e-9)
    # bone, fat and lung land where radiologists expect them
    assert hounsfield_unit(0.052) < -700          # lung
    assert -150 < hounsfield_unit(0.185) < -50    # fat
    assert hounsfield_unit(0.500) > 1000          # bone
    # below air is unphysical
    try:
        mu_from_hounsfield(-1200.0)
    except ValueError as exc:
        assert "negative" in str(exc)
    else:
        raise AssertionError("HU below -1000 should be refused")
    try:
        hounsfield_unit(-0.1)
    except ValueError:
        pass
    else:
        raise AssertionError("a negative mu should be refused")


def test_contrast_comes_from_the_photoelectric_effect():
    """~NE-12's Z^4/E^3 is why radiography works at all. At 20 keV the
    photoelectric effect dominates and bone stands out enormously against soft
    tissue; by 100 keV Compton dominates, mu tracks electron density alone, and
    the contrast largely collapses.

    That is the tension every imaging protocol resolves: low energy for contrast,
    high energy for penetration and dose."""
    c20 = contrast_ratio(3.0, 0.80, 5.0)
    c60 = contrast_ratio(0.60, 0.21, 5.0)
    c100 = contrast_ratio(0.35, 0.17, 5.0)
    assert c20 > c60 > c100
    assert c20 > 0.99
    assert c100 < 0.7
    assert _rel(c20 / c100, 1.69, 1e-2)
    # zero thickness gives zero contrast, identical tissues give none either
    assert _approx(contrast_ratio(3.0, 0.8, 0.0), 0.0)
    assert _approx(contrast_ratio(0.5, 0.5, 5.0), 0.0)
    # and contrast is symmetric in which tissue is which
    assert _rel(contrast_ratio(0.6, 0.21, 5.0), contrast_ratio(0.21, 0.6, 5.0), 1e-12)
    try:
        contrast_ratio(0.6, 0.2, -1.0)
    except ValueError:
        pass
    else:
        raise AssertionError("a negative thickness should be refused")


def test_the_pet_nuclides_all_show_the_beta_plus_signature():
    """All four of Table 14.3's positron emitters have Eav/Emax between 0.39 and
    0.43, against the ~0.33 typical of beta-MINUS emitters.

    The difference is Coulomb: the nucleus repels the emerging positron, pushing
    the spectrum to higher energies. Four independent entries agreeing on 0.40
    is a check that the table is measured data rather than assembled from rules
    of thumb."""
    fracs = [beta_mean_fraction(n) for n in PET_NUCLIDES]
    assert len(fracs) == 4
    for f in fracs:
        assert 0.39 < f < 0.43, "%.4f" % f
    assert max(fracs) - min(fracs) < 0.04
    assert all(f > 0.36 for f in fracs)          # clear of the beta-minus 0.33
    # branching to positrons is essentially 100% for all four
    for n, v in PET_NUCLIDES.items():
        assert v[2] > 0.99, n
    # and every one is made by a (p,x) reaction -- proton-rich, hence cyclotrons
    for n, v in PET_NUCLIDES.items():
        assert "(p," in v[4], n
    try:
        beta_mean_fraction("99mTc")
    except KeyError:
        pass
    else:
        raise AssertionError("a non-PET nuclide should be refused")


def test_only_fluorine_18_survives_a_journey():
    """S&F: "only 18F [has] a sufficiently long life to permit transport of
    radiopharmaceuticals to sites a few hours from the point of preparation."

    18F lasts 6.1 hours to 10% of its activity; 15O lasts 6.6 MINUTES. Three of
    the four therefore require the cyclotron to be in the building, which is why
    a PET centre is a far larger commitment than a SPECT one."""
    t18 = usable_transport_time("18F")
    assert _rel(t18, 6.09, 1e-2), "%.2f h" % t18
    assert t18 > 3.0
    for n in ("11C", "13N", "15O"):
        assert usable_transport_time(n) < 1.2, n
    assert usable_transport_time("15O") * 60 < 8.0     # minutes
    assert _rel(t18 / usable_transport_time("15O"), 54.1, 1e-2)
    # decay over a two-hour delivery
    assert _rel(activity_after_transport("18F", 2.0), 0.469, 1e-2)
    assert activity_after_transport("15O", 2.0) < 1e-17
    assert _approx(activity_after_transport("18F", 0.0), 1.0)
    # 18F's half-life is exactly two hours' worth of usefulness
    assert _rel(PET_NUCLIDES["18F"][3], 110.0, 1e-9)
    for bad in (0.0, 1.0):
        try:
            usable_transport_time("18F", bad)
        except ValueError:
            pass
        else:
            raise AssertionError("fraction %r should be refused" % bad)


def test_what_pet_buys_and_what_it_cannot():
    """Coincidence detection gives a line of response with no physical
    collimator -- "electronic collimation" -- which is why PET beats SPECT on
    both resolution and sensitivity.

    But a 10 ns timing window corresponds to 150 cm along that line, far larger
    than a patient, so conventional PET localises by reconstruction and not by
    timing. And the positron range is a floor no detector can beat: 18F blurs
    0.5 mm before it annihilates, 15O blurs 2.5 mm."""
    assert _rel(annihilation_photon_energy(), 511.0, 1e-3)
    assert _rel(annihilation_photon_energy(), M_E_C2_KEV, 1e-9)
    d10 = coincidence_window_length(10.0)
    assert _rel(d10, 150.0, 1e-2), "%.1f cm" % d10
    assert d10 > 50.0                            # bigger than a patient
    # time-of-flight PET at 400 ps does help
    assert _rel(coincidence_window_length(0.4), 6.0, 1e-2)
    # positron range: 18F is the workhorse for a physical reason
    r18 = positron_range_mm(PET_NUCLIDES["18F"][1])
    r15 = positron_range_mm(PET_NUCLIDES["15O"][1])
    assert r18 < 1.0 and r15 > 2.0
    assert _rel(r15 / r18, 5.0, 0.05)
    assert _rel(positron_range_mm(1.0), 4.0, 1e-9)   # S&F's anchor
    assert _approx(positron_range_mm(0.0), 0.0)
    for fn, bad in ((coincidence_window_length, 0.0), (positron_range_mm, -1.0)):
        try:
            fn(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%s should reject %r" % (fn.__name__, bad))


def test_spect_tracers_and_the_99mtc_dominance():
    """99mTc dominates SPECT -- S&F §14.1.7: "The most commonly used radionuclide
    is 99mTc" -- because it is a near-ideal combination: a 140 keV gamma
    (penetrating enough to escape a body, soft enough to collimate), a 6-hour
    half-life (long enough to image, short enough to clear), essentially no
    particle emission, and a generator (~NE-26) that ships it anywhere.

    Note what the chapter does NOT supply: Table 14.5 lists process -> tracer and
    gives no energies or half-lives at all. These come from the repo's shared
    nuclear data, and the next test re-reads that CSV rather than trusting the
    dict."""
    tc = SPECT_TRACERS["99mTc"]
    assert _rel(tc["gamma_kev"], 140.5, 1e-3)
    assert _rel(tc["half_life_h"], 6.015, 1e-3)
    assert len(tc["uses"]) >= 4                  # the most versatile by far
    # its gamma sits in the sweet spot: above 201Tl's 71 keV, below 111In's 171
    energies = sorted(v["gamma_kev"] for v in SPECT_TRACERS.values())
    assert energies[0] < tc["gamma_kev"] < energies[-1]
    # and it is by far the shortest-lived, which is the point of a generator
    assert tc["half_life_h"] == min(v["half_life_h"] for v in SPECT_TRACERS.values())
    assert min(v["half_life_h"] for v in SPECT_TRACERS.values() if v is not tc) > 10
    # every SPECT gamma is well under PET's 511 keV -- which is exactly why SPECT
    # can use an absorbing collimator at all and PET cannot
    assert max(energies) < 0.5 * annihilation_photon_energy()


def test_the_pet_table_reproduces_from_the_repo_nuclear_data():
    """Table 14.3's four nuclides are re-read from the shared decay table
    (modules/NE/data_tables/D1_decay_radiation.csv) and agree to better than
    0.5% on Emax, Eav and half-life alike.

    The check that matters more is the annihilation yield: D1 gives the 511 keV
    frequency as almost exactly TWICE the positron branch for all four -- 199.5%
    against 99.76% for 11C, and so on. Two photons per positron, which is the
    whole basis of coincidence detection."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "..", "..", "data_tables", "D1_decay_radiation.csv")
    assert os.path.exists(path), path
    pos, ann = {}, {}
    with open(path, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            n = row["nuclide"]
            if n not in PET_NUCLIDES:
                continue
            if row["group"] == "positron":
                pos[n] = (float(row["E_max_keV"]), float(row["E_avg_keV"]),
                          float(row["freq_pct"]))
            elif row["group"] == "gamma_xray" and row["E_keV"].strip() == "511":
                ann[n] = float(row["freq_pct"])
    assert set(pos) == set(PET_NUCLIDES), sorted(pos)
    for n, (emax, eav, branch, _t, _r) in PET_NUCLIDES.items():
        d_max, d_av, d_br = pos[n]
        assert _rel(emax * 1000.0, d_max, 5e-3), "%s Emax" % n
        assert _rel(eav * 1000.0, d_av, 5e-3), "%s Eav" % n
        assert _rel(branch * 100.0, d_br, 5e-3), "%s branch" % n
        # two 511 keV photons per positron, to a fraction of a percent
        assert _rel(ann[n], 2.0 * d_br, 1e-3), "%s annihilation yield" % n
    # and the Eav/Emax signature survives the independent numbers
    for n in PET_NUCLIDES:
        assert 0.39 < pos[n][1] / pos[n][0] < 0.43, n


def test_the_pinhole_caption_cannot_be_right_as_printed():
    """S&F Fig. 14.16's caption (printed p. 528) gives the pinhole point-spread
    as "R_ph/(f + b) = d/b or R_ph = (d/b)/(f + b)".

    The written division is impossible on dimensions alone -- (d/b)/(f+b) has
    units of 1/length -- and the caption's own first equality says it should be
    the PRODUCT d(f+b)/b. That product is the spot size in the IMAGE plane; the
    body text's R_ph = (d/f)(f+b) is the same blur referred back to the OBJECT
    plane, smaller by the magnification M = f/b. Eq. (14.19) closes only with the
    object-referred form, because its other term R_I/M is object-referred too."""
    d, f, b = 0.4, 20.0, 10.0
    M = f / b
    obj = pinhole_resolution(d, f, b)             # (d/f)(f+b), the body text
    img = (d / b) * (f + b)                       # the caption's intended product
    assert _rel(obj, 0.6, 1e-9)
    assert _rel(img, 1.2, 1e-9)
    assert _rel(img / obj, M, 1e-12)              # they differ by exactly M
    # the printed division is off by a factor of (f+b)^2 -- not a small slip
    printed = (d / b) / (f + b)
    assert _rel(img / printed, (f + b) ** 2, 1e-12)
    # Eq. (14.19): quadrature, so whichever blur is larger dominates. Improving
    # the crystal from R_I = 4.5 to 2.5 mm (§14.1.7's stated range) is worth
    # almost the full 2 mm when the pinhole is fine, and almost nothing when the
    # collimator is coarse -- which is why SPECT resolution is a collimator
    # problem in practice, not a detector one.
    for r_ph, kept in ((obj, 0.47), (3.0, 0.25)):
        coarse = spect_system_resolution(r_ph, 4.5, M)
        fine = spect_system_resolution(r_ph, 2.5, M)
        assert coarse > fine > r_ph
        assert _rel((coarse - fine) / 2.0, kept, 0.02), "%.3f" % ((coarse - fine) / 2.0)
    assert _rel(spect_system_resolution(3.0, 4.0, 1.0), 5.0, 1e-12)
    assert _rel(spect_system_resolution(obj, 0.0, M), obj, 1e-12)
    # magnifying (larger f) shrinks the object-referred pinhole blur
    assert pinhole_resolution(d, 40.0, b) < obj
    for bad in ((0.0, 20.0, 10.0), (0.4, 0.0, 10.0), (0.4, 20.0, -1.0)):
        try:
            pinhole_resolution(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be refused" % (bad,))


def test_therapy_is_the_same_quantity_optimised_the_other_way():
    """Diagnosis minimises dose for a given image; therapy maximises the ratio
    of tumour dose to normal-tissue dose. Every technique in §14.5 is an attempt
    to raise that ratio, and they divide by HOW they sharpen it: geometrically
    (conformal, stereotactic), physically (Bragg peak, finite electron range),
    or biochemically (radionuclide therapy)."""
    assert _rel(therapeutic_ratio(70.0, 35.0), 2.0, 1e-9)
    for bad in ((60.0, 60.0), (30.0, 60.0)):
        try:
            therapeutic_ratio(*bad)
        except ValueError as exc:
            assert "therapy" in str(exc)
        else:
            raise AssertionError("%r should be refused" % (bad,))
    try:
        therapeutic_ratio(70.0, 0.0)
    except ValueError:
        pass
    else:
        raise AssertionError("zero normal-tissue dose should be refused")
    assert len(THERAPY_MODALITIES) == 9
    # the Bragg peak is the proton beam's entire argument (~NE-14)
    assert "Bragg" in THERAPY_MODALITIES["proton beam"]["sharpening"]
    # brachytherapy's 1/r^2 is worth a factor of 400 over 0.5 to 10 cm
    near = brachytherapy_dose_rate(1.0, 0.5)
    far = brachytherapy_dose_rate(1.0, 10.0)
    assert _rel(near / far, 400.0, 1e-9)
    assert _rel(brachytherapy_dose_rate(1.0, 1.0), 1.109, 1e-9)
    try:
        brachytherapy_dose_rate(1.0, 0.0)
    except ValueError:
        pass
    else:
        raise AssertionError("r = 0 should be refused")


def test_the_cancer_statistics_therapy_addresses():
    """Tables 14.6 and 14.7 (printed p. 541), and the three claims S&F make from
    them -- all of which check out.

    Table 14.6 closes exactly in all four columns, which is a real check on a
    hand-typeset table. Its totals give the "1.37 million new cases and 564
    thousand deaths" of the text. Table 14.7 gives "nearly half ... may expect to
    experience cancer" (46.6% of men) and "only about half of those persons
    ... survive" (49% of men and 48% of women die of it). This is the denominator
    every radiogenic-risk number in ~NE-18 has to be compared against."""
    for i, printed in enumerate(CANCER_2004_TOTALS):
        got = sum(v[i] for v in CANCER_2004.values())
        assert got == printed, "column %d: %d vs printed %d" % (i, got, printed)
    new_cases = CANCER_2004_TOTALS[0] + CANCER_2004_TOTALS[1]
    deaths = CANCER_2004_TOTALS[2] + CANCER_2004_TOTALS[3]
    assert _rel(new_cases, 1.37e6, 2e-3), "%d" % new_cases      # "1.37 million"
    assert _rel(deaths, 564e3, 2e-3), "%d" % deaths             # "564 thousand"
    # breast cancer is the one site that is essentially sex-specific
    assert CANCER_2004["breast"][1] / CANCER_2004["breast"][0] > 100
    # and respiratory cancer is the one that kills nearly everyone it strikes
    resp = CANCER_2004["respiratory"]
    assert resp[2] / resp[0] > 0.9

    tot = [sum(v[i] for v in CANCER_LIFETIME_RISK.values()) for i in range(4)]
    inc_m, inc_f, mor_m, mor_f = [x / 1e5 for x in tot]
    assert _rel(inc_m, 0.4656, 1e-3), "%.4f" % inc_m            # "nearly half"
    assert 0.44 < inc_m < 0.50
    assert _rel(inc_f, 0.3804, 1e-3), "%.4f" % inc_f
    # "only about half of those persons encountering cancer survive"
    assert _rel(mor_m / inc_m, 0.491, 1e-2), "%.3f" % (mor_m / inc_m)
    assert _rel(mor_f / inc_f, 0.476, 1e-2), "%.3f" % (mor_f / inc_f)
    # solid cancers dominate both columns; leukemia is rare but far more lethal
    for i in range(4):
        assert CANCER_LIFETIME_RISK["solid cancer"][i] > 0.9 * tot[i]
    leuk = CANCER_LIFETIME_RISK["leukemia"]
    solid = CANCER_LIFETIME_RISK["solid cancer"]
    assert leuk[2] / leuk[0] > 0.8                  # ~86% of male leukemias kill
    assert solid[2] / solid[0] < 0.5                # under half of solid cancers
    # thyroid cancer is the mirror image -- common-ish and rarely fatal, which is
    # why ~NE-18 treats thyroid dose separately from whole-body dose
    thy = CANCER_LIFETIME_RISK["thyroid"]
    assert thy[2] / thy[0] < 0.2


def test_the_ct_nobel_year_is_wrong_in_the_book():
    """ERRATUM, S&F §14.1.5 (printed p. 521): "Hounsfield and Cormack ... shared
    the Nobel prize in 1972."

    The prize was 1979 -- Physiology or Medicine, "for the development of
    computer assisted tomography". 1972 is a real date in the story: Hounsfield's
    first published CT images and EMI's first clinical scanner. The book has
    collapsed the demonstration into the prize, seven years early.

    Pinned here so a later reader does not quietly re-absorb the printed year."""
    assert CT_NOBEL["actual_year"] == 1979
    assert CT_NOBEL["printed_year"] == 1972
    assert CT_NOBEL["actual_year"] - CT_NOBEL["printed_year"] == 7
    assert set(CT_NOBEL["laureates"]) == {"Allan M. Cormack", "Godfrey N. Hounsfield"}
    # and the prize follows the scanner, never the other way round
    assert CT_NOBEL["actual_year"] > CT_NOBEL["printed_year"]


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
