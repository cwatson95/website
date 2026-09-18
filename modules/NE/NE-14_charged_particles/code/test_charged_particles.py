"""NE-14 tests -- charged-particle stopping against Shultis & Faw §7.5, its
Examples 7.6 and 7.7, and Tables 7.2-7.3.

Run:  python3 test_charged_particles.py
"""

import math

from charged_particles import (
    M_E_C2_MEV, M_P_U, M_ALPHA_U,
    RANGE_CONSTANTS_PROTON, RANGE_CONSTANTS_ALPHA, RANGE_CONSTANTS_ELECTRON,
    SUSPECT_RANGE_CONSTANTS, EXAMPLE_7_7_B_DISCREPANCY,
    FISSION_FRAGMENT_C, RANGE_FORMULA_RANGE_MEV,
    csda_mass_range, csda_range, range_energy_valid,
    scaled_heavy_range, equivalent_proton_energy,
    radiative_to_collisional, bremsstrahlung_crossover_energy,
    fission_fragment_range,
    energy_deposition_depth_fraction, DEPOSITION_FRACTIONS,
)


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def _rel(a, b, tol):
    """Strictly RELATIVE comparison.  `_approx` falls back to an absolute
    tolerance for values below 1, which silently makes assertions on quantities
    like 3.8e-3 g/cm2 vacuous -- every candidate passes.  Range checks must use
    this instead."""
    return abs(a / b - 1.0) <= tol


# --- ranges against accepted NIST/PSTAR/ASTAR/ESTAR values ----------------

def test_ranges_match_the_NIST_star_codes():
    """S&F's Tables 7.2-7.3 are fits to the NIST STAR codes, so the formula must
    reproduce them.  These are the accepted CSDA ranges (g/cm2), independent of
    the book -- the strongest available check on the transcription."""
    cases = [
        # (particle, material, E MeV, accepted rho R g/cm2)
        ("proton",   "H2O",      1.0,  2.458e-3),
        ("proton",   "H2O",      2.0,  7.178e-3),
        ("proton",   "H2O",     10.0,  0.1230),
        ("proton",   "Al",       1.0,  4.020e-3),
        ("proton",   "Al",      10.0,  0.1692),
        ("alpha",    "H2O",      1.0,  5.93e-4),
        ("alpha",    "H2O",      5.0,  3.630e-3),
        ("electron", "water",    1.0,  0.4367),
        ("electron", "water",   10.0,  4.975),
        ("electron", "aluminum", 1.0,  0.5546),
        ("electron", "lead",     1.0,  0.8420),
    ]
    worst = 0.0
    for particle, material, e, expect in cases:
        got = csda_mass_range(particle, material, e)
        err = abs(got / expect - 1.0)
        worst = max(worst, err)
        assert _rel(got, expect, 0.08), \
            "%s in %s at %g MeV: %.5g vs accepted %.5g (%.1f%% off)" \
            % (particle, material, e, got, expect, 100 * err)
    # the fits are a 3-parameter quadratic over two decades, so a few percent is
    # the honest expectation -- but nothing should be wildly off
    assert worst < 0.08, "worst deviation %.1f%%" % (100 * worst)
    assert worst > 0.02, "suspiciously perfect -- check the comparison is relative"


def test_the_formula_refuses_to_extrapolate():
    """Eq. (7.47) is a quadratic in log E fitted over 0.1-10 MeV.  Outside that
    it has no physical content, and at low energy it turns over and becomes
    nonsense -- so the default is to raise, with an explicit opt-out."""
    assert range_energy_valid(0.1) and range_energy_valid(10.0)
    assert not range_energy_valid(0.099) and not range_energy_valid(10.1)
    csda_mass_range("proton", "H2O", 0.1)          # at the boundary: fine
    csda_mass_range("proton", "H2O", 10.0)
    for e in (0.01, 0.05, 50.0, 1000.0):
        try:
            csda_mass_range("proton", "H2O", e)
        except ValueError:
            pass
        else:
            raise AssertionError("%g MeV should be refused" % e)
        csda_mass_range("proton", "H2O", e, strict=False)      # opt-out works
    for bad in (0.0, -1.0):
        try:
            csda_mass_range("proton", "H2O", bad, strict=False)
        except ValueError:
            pass
        else:
            raise AssertionError("E = %r should be rejected" % bad)


def test_the_lead_proton_row_is_withheld():
    """Table 7.2's proton/Pb constants do not belong to the same family as any
    other proton row and give a range ~70x the accepted value.  The module
    refuses to use them rather than returning a confident wrong number.

    The evidence: every other proton row gives 0.024-0.062 g/cm2 at 4 MeV; the
    printed Pb row gives 4.59.  Its b also matches the Pb ALPHA row's b to 1e-4,
    which no other material pair does."""
    assert ("proton", "Pb") in SUSPECT_RANGE_CONSTANTS
    assert "Pb" not in RANGE_CONSTANTS_PROTON
    assert "Pb" in RANGE_CONSTANTS_ALPHA          # the alpha row is fine

    try:
        csda_mass_range("proton", "Pb", 4.0)
    except ValueError as exc:
        assert "withheld" in str(exc) or "inconsistent" in str(exc)
    else:
        raise AssertionError("the suspect Pb proton row should be refused")

    # the anomaly, quantified
    a, b, c = SUSPECT_RANGE_CONSTANTS[("proton", "Pb")]
    x = math.log10(4.0)
    printed = 10.0 ** (a + b * x + c * x * x)
    others = [csda_mass_range("proton", m, 4.0) for m in RANGE_CONSTANTS_PROTON]
    assert printed > 50 * max(others), "%.4g vs max %.4g" % (printed, max(others))
    assert max(others) / min(others) < 3.0        # the real rows are a tight family
    # and the tell-tale coincidence with the alpha row's b
    assert _approx(b, RANGE_CONSTANTS_ALPHA["Pb"][1], tol=2e-4)


def test_example_7_7_uses_the_wrong_b():
    """S&F Example 7.7 evaluates the water proton range with b = 1.4501, but
    Table 7.2's H2O row gives 1.4975.  1.4501 is the LiF proton value.

    The TABLE is right: it gives 7.202e-3 g/cm2 at 2 MeV against PSTAR's
    7.178e-3 (0.3% high), while the example's b gives 6.969e-3 (2.9% low)."""
    d = EXAMPLE_7_7_B_DISCREPANCY
    assert _approx(d["printed_in_example"], 1.4501)
    assert _approx(d["table_7_2_H2O"], 1.4975)
    assert _approx(RANGE_CONSTANTS_PROTON["H2O"][1], d["table_7_2_H2O"])
    # the example's b is exactly the LiF row's b
    assert _approx(RANGE_CONSTANTS_PROTON["LiF"][1], d["printed_in_example"])

    a, _, c = RANGE_CONSTANTS_PROTON["H2O"]
    x = math.log10(2.0)
    from_table = 10.0 ** (a + d["table_7_2_H2O"] * x + c * x * x)
    from_example = 10.0 ** (a + d["printed_in_example"] * x + c * x * x)
    assert _approx(from_table, 7.202e-3, tol=1e-3)
    assert _approx(from_example, 6.969e-3, tol=1e-3)
    # PSTAR's accepted value picks the table
    assert abs(from_table / 7.178e-3 - 1) < 0.01
    assert abs(from_example / 7.178e-3 - 1) > 0.02


def test_reproduces_example_7_7_by_scaling():
    """S&F Example 7.7: the range of a 6 MeV triton in water, obtained from the
    proton range at the SAME SPEED via the m/z^2 rule.  The book gets 0.021 cm;
    with the table's b (see above) it is 0.0216 cm."""
    m_t = 3.0160492
    ep = equivalent_proton_energy(6.0, m_t)
    assert _approx(ep, 2.0, tol=5e-3), "%.4f" % ep          # step 1: E/3

    rp = csda_mass_range("proton", "H2O", ep)
    rt = scaled_heavy_range(rp, m_t, 1)
    assert _approx(rt / rp, 3.0, tol=5e-3)                  # step 3: m/z^2 = 3
    assert _approx(rt, 0.0216, tol=2e-2), "%.5f" % rt
    # the book's 0.021 cm, from its 0.00697, is 3% lower -- the b discrepancy
    assert 0.020 < rt < 0.023


# --- the scaling rules  [§7.5.4] ------------------------------------------

def test_the_m_over_z_squared_rule():
    """Rule 2: at the same SPEED, rho R scales as m/z^2.  So a 4 MeV alpha and a
    1 MeV proton have nearly the same range -- S&F say so explicitly."""
    # same speed: E_alpha/E_proton = m_alpha/m_proton ~ 4
    ep = equivalent_proton_energy(4.0, M_ALPHA_U)
    assert _approx(ep, 1.0, tol=1e-2), "%.4f" % ep
    rp = csda_mass_range("proton", "H2O", ep)
    r_alpha_scaled = scaled_heavy_range(rp, M_ALPHA_U, 2)
    # m/z^2 = 4/4 = 1, so the alpha range equals the 1 MeV proton range
    assert _approx(r_alpha_scaled / rp, 1.0, tol=1e-2)
    # and that is close to what the tabulated alpha fit gives directly
    r_alpha_direct = csda_mass_range("alpha", "H2O", 4.0)
    assert _approx(r_alpha_scaled, r_alpha_direct, tol=0.25), \
        "%.5g vs %.5g" % (r_alpha_scaled, r_alpha_direct)
    for bad in ((1.0, 0.0, 1), (1.0, 1.0, 0)):
        try:
            scaled_heavy_range(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_mass_range_is_density_independent():
    """Rule 1: rho R does not depend on density.  Air and water differ by 800x
    in density and only 1.7x in mass-thickness range for the same particle --
    stopping is about electrons per gram, not per cubic centimetre."""
    r_air = csda_mass_range("proton", "air", 4.0)
    r_h2o = csda_mass_range("proton", "H2O", 4.0)
    assert 1.0 < r_air / r_h2o < 1.4, r_air / r_h2o
    # as a LENGTH they differ enormously, entirely because of density
    len_air = csda_range("proton", "air", 4.0, 1.205e-3)
    len_h2o = csda_range("proton", "H2O", 4.0, 1.0)
    assert len_air / len_h2o > 500
    try:
        csda_range("proton", "H2O", 4.0, 0.0)
    except ValueError:
        pass
    else:
        raise AssertionError("zero density should be rejected")


def test_heavier_and_more_charged_means_shorter_range():
    """The physical content of m/z^2, checked against the tables directly: at the
    same ENERGY an alpha stops far sooner than a proton, because z^2 = 4 beats
    the factor-4 mass advantage and it is moving much more slowly."""
    for e in (1.0, 4.0, 10.0):
        assert (csda_mass_range("alpha", "H2O", e)
                < csda_mass_range("proton", "H2O", e))
    # and both stop far sooner than an electron of the same energy
    assert (csda_mass_range("alpha", "H2O", 1.0)
            < csda_mass_range("proton", "H2O", 1.0)
            < csda_mass_range("electron", "water", 1.0))
    # a 4 MeV alpha travels ~28 microns in water; an electron ~4 mm
    assert _approx(csda_range("alpha", "H2O", 4.0, 1.0) * 1e4, 27.9, tol=5e-2)
    assert _approx(csda_range("electron", "water", 1.0, 1.0) * 10, 4.35, tol=5e-2)


# --- bremsstrahlung  [Eqs. (7.42)-(7.43), Example 7.6] --------------------

def test_reproduces_example_7_6():
    """S&F Example 7.6: in gold (Z = 79) an electron loses as much energy to
    bremsstrahlung as to ionization at E = 700/79 = 8.9 MeV."""
    assert _approx(bremsstrahlung_crossover_energy(79), 8.86, tol=1e-2)
    assert _approx(radiative_to_collisional(8.86, 79), 1.0, tol=1e-2)
    # the crossover falls as 1/Z: carbon needs 117 MeV, lead only 8.5
    assert _approx(bremsstrahlung_crossover_energy(6), 116.7, tol=1e-2)
    assert bremsstrahlung_crossover_energy(6) > 10 * bremsstrahlung_crossover_energy(82)
    for bad in (0, -1):
        try:
            bremsstrahlung_crossover_energy(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("Z = %r should be rejected" % bad)


def test_bremsstrahlung_is_an_electron_only_problem():
    """The (m_e/M)^2 in Eq. (7.43) is decisive: a proton is 1836x heavier, so its
    radiative fraction is 3.4e6 times smaller.  S&F: 'all other charged particles
    are far too massive to produce significant amounts of bremsstrahlung.'"""
    electron = radiative_to_collisional(1.0, 82)
    proton = radiative_to_collisional(1.0, 82, M_E_C2_MEV / (M_P_U * 931.494))
    assert _approx(electron, 0.117, tol=1e-2)
    assert proton < 1e-6
    assert electron / proton > 1e6
    # linear in both E and Z
    assert _approx(radiative_to_collisional(2.0, 82) / electron, 2.0)
    assert _approx(radiative_to_collisional(1.0, 41) / electron, 0.5)


def test_why_beta_shields_are_plastic():
    """A practical consequence of the linear Z: shielding a 2 MeV beta with lead
    converts 23% of the energy into penetrating bremsstrahlung, against 1.7% in
    carbon.  Low-Z first, then lead for the photons that remain."""
    for e in (1.0, 2.0, 3.0):
        assert (radiative_to_collisional(e, 6)
                < radiative_to_collisional(e, 13)
                < radiative_to_collisional(e, 82))
    assert _approx(radiative_to_collisional(2.0, 82), 0.234, tol=1e-2)
    assert _approx(radiative_to_collisional(2.0, 6), 0.0171, tol=1e-2)
    assert radiative_to_collisional(2.0, 82) / radiative_to_collisional(2.0, 6) > 12


# --- fission fragments  [Eq. (7.48)] --------------------------------------

def test_fission_fragment_ranges_are_microscopic():
    """Eq. (7.48): rho R = C E^(2/3), +-10%.  A 99.9 MeV light fragment travels
    4.1 mg/cm2 in aluminium -- 15 microns.  That is why fission's 168 MeV of
    fragment energy is deposited inside the fuel pellet (~NE-09) and heats the
    fuel rather than the coolant."""
    assert _approx(fission_fragment_range(99.9, "air"), 3.01, tol=1e-2)
    assert _approx(fission_fragment_range(99.9, "aluminum"), 4.09, tol=1e-2)
    assert _approx(fission_fragment_range(67.9, "gold"), 8.32, tol=1e-2)
    # the light fragment (more energy, S&F §7.5.4) goes further
    for m in FISSION_FRAGMENT_C:
        assert fission_fragment_range(99.9, m) > fission_fragment_range(67.9, m)
    # E^(2/3): eight times the energy is four times the range
    assert _approx(fission_fragment_range(80.0, "air")
                   / fission_fragment_range(10.0, "air"), 4.0)
    # 15 microns in aluminium (rho = 2.70)
    microns = fission_fragment_range(99.9, "aluminum") * 1e-3 / 2.70 * 1e4
    assert _approx(microns, 15.2, tol=2e-2)
    for bad in (("x", "air"), (99.9, "tungsten")):
        try:
            fission_fragment_range(*bad) if bad[0] != "x" else fission_fragment_range(-1.0, "air")
        except (KeyError, ValueError, TypeError):
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


# --- range is a path length, not a depth  [§7.5.4] ------------------------

def test_range_overstates_penetration_depth():
    """The CSDA range is the length of a TWISTING path, so an electron's
    penetration DEPTH is much less.  90% of a normally incident beam's energy is
    deposited within 70% of the range; everything within 110%.

    Confusing the two overestimates shielding requirements, or -- used the other
    way -- underestimates dose."""
    assert _approx(energy_deposition_depth_fraction(0.90), 0.70)
    assert _approx(energy_deposition_depth_fraction(0.95), 0.80)
    assert _approx(energy_deposition_depth_fraction(1.00), 1.10)
    # a point isotropic source spreads more, so needs a larger fraction
    assert (energy_deposition_depth_fraction(0.90, "point")
            > energy_deposition_depth_fraction(0.90, "beam"))
    # monotone in energy fraction
    beam = DEPOSITION_FRACTIONS["beam"]
    ks = sorted(beam)
    assert all(beam[ks[i]] > beam[ks[i - 1]] for i in range(1, len(ks)))
    try:
        energy_deposition_depth_fraction(0.99)
    except KeyError:
        pass
    else:
        raise AssertionError("an untabulated fraction should raise")


def test_tables_are_complete():
    """Table 7.2 has 11 materials for alphas and 10 usable for protons (Pb
    withheld); Table 7.3 has 14 for electrons."""
    assert len(RANGE_CONSTANTS_ALPHA) == 11
    assert len(RANGE_CONSTANTS_PROTON) == 10
    assert len(RANGE_CONSTANTS_PROTON) + len(SUSPECT_RANGE_CONSTANTS) == 11
    assert len(RANGE_CONSTANTS_ELECTRON) == 14
    assert set(RANGE_CONSTANTS_ALPHA) - {"Pb"} == set(RANGE_CONSTANTS_PROTON)
    # electron 'c' is NEGATIVE for every material and positive for heavy
    # particles -- the range-energy curve bends the other way
    assert all(c < 0 for _, _, c in RANGE_CONSTANTS_ELECTRON.values())
    assert all(c > 0 for _, _, c in RANGE_CONSTANTS_ALPHA.values())
    assert all(c > 0 for _, _, c in RANGE_CONSTANTS_PROTON.values())
    for m in ("tissue", "bone", "water", "air"):
        assert m in RANGE_CONSTANTS_ELECTRON


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
