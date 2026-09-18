"""NE-12 tests -- photon interactions against Shultis & Faw §7.3 and the
extracted Appendix C.3.

Run:  python3 test_photon_interactions.py
"""

import math

from photon_interactions import (
    M_E_C2_MEV, TWO_ME_C2_MEV, R_E_CM, AVOGADRO, BARN_CM2,
    K_EDGE_KEV, FLUORESCENT_YIELD, MATERIALS, Z_OVER_A_NIST_ORDINARY_CONCRETE,
    load_photon_coefficients, mass_coefficient, linear_coefficient,
    photoelectron_energy, photoelectric_scaling,
    compton_scattered_energy, compton_electron_energy,
    compton_edge, backscatter_energy, compton_wavelength_shift_A,
    klein_nishina_per_electron, klein_nishina_per_atom,
    klein_nishina_mass_coefficient,
    pair_production_threshold, triplet_production_threshold,
    pair_kinetic_energy_shared, annihilation_photon_energy,
    dominant_process, crossover_energies, energy_transfer_fraction,
)


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --- the strongest check: Klein-Nishina vs the tabulated coefficients -----

def test_klein_nishina_reproduces_the_tables_where_electrons_are_free():
    """S&F Eq. (7.34) is an analytic formula; Appendix C.3's 'c' column is
    tabulated data from an independent source.  Computing
    mu_c/rho = (N_a Z/A) sigma_KN must reproduce it -- and above ~0.5 MeV it does,
    to better than 1% in all five materials.

    That single check exercises the Klein-Nishina formula, r_e, the Z/A values
    and the table extraction simultaneously."""
    for m in ("air", "water", "concrete", "iron", "lead"):
        zoa = MATERIALS[m]["z_over_a"]
        for e in (0.5, 1.0, 3.0, 10.0, 20.0):
            calc = klein_nishina_mass_coefficient(e, zoa)
            tab = mass_coefficient(m, e, "c")
            assert _approx(calc, tab, tol=0.012), \
                "%s at %.2f MeV: computed %.5f vs tabulated %.5f" % (m, e, calc, tab)


def test_the_free_electron_approximation_fails_exactly_where_S_and_F_say():
    """S&F §7.3.2: Eqs. (7.33)-(7.34) 'break down when the kinetic energy of the
    recoil electron is comparable to its binding energy in the atom'.  The
    tabulated column is the BOUND-electron (incoherent) cross section, which is
    smaller, so free-electron Klein-Nishina must OVER-predict -- more so as the
    energy falls and as Z rises.

    Both trends hold quantitatively, and the onset tracks the K edge: lead
    (K = 88 keV) is already 19% high at 100 keV and 236% high at 10 keV, while
    water (oxygen K = 0.54 keV) is within 1.3% at 100 keV.  This is physics, not
    a discrepancy to be tuned away."""
    def over(m, e):
        return (klein_nishina_mass_coefficient(e, MATERIALS[m]["z_over_a"])
                / mass_coefficient(m, e, "c"))

    # never under-predicts, anywhere
    for m in ("water", "iron", "lead"):
        for e in (0.01, 0.05, 0.1, 0.5, 1.0):
            assert over(m, e) > 0.99, (m, e, over(m, e))

    # worsens as energy falls, in every material
    for m in ("water", "iron", "lead"):
        assert over(m, 0.01) > over(m, 0.05) > over(m, 0.2) > over(m, 1.0)

    # worsens with Z at fixed energy
    for e in (0.01, 0.05, 0.1):
        assert over("water", e) < over("iron", e) < over("lead", e), e

    # the specific numbers, tied to the K edges
    assert _approx(over("lead", 0.1), 1.187, tol=0.02)     # K edge 88 keV: 19% high
    assert _approx(over("water", 0.1), 1.013, tol=0.02)    # O K edge 0.54 keV: 1% high
    assert over("lead", 0.01) > 3.0                        # far below the K edge
    # and by 0.5 MeV, five times lead's K edge, binding is negligible again
    assert over("lead", 0.5) < 1.03


def test_z_over_a_is_recoverable_from_the_tables():
    """Above a few MeV the free-electron formula is exact, so the tabulated
    Compton column can be SOLVED for Z/A -- an independent check on both the
    extraction and the assumed compositions.

    Four materials return the standard NIST values to 0.3%.  Concrete does not,
    and that is expected: S&F's table is ANSI/ANS-6.4.3 standard concrete, not
    NIST 'ordinary concrete', so this module takes concrete's Z/A from the book's
    own data rather than from NIST."""
    for m in ("air", "water", "iron", "lead"):
        implied = (mass_coefficient(m, 10.0, "c")
                   / (AVOGADRO * klein_nishina_per_electron(10.0)))
        assert _approx(implied, MATERIALS[m]["z_over_a"], tol=5e-3), \
            "%s: implied %.5f vs assumed %.5f" % (m, implied, MATERIALS[m]["z_over_a"])

    implied_concrete = (mass_coefficient("concrete", 10.0, "c")
                        / (AVOGADRO * klein_nishina_per_electron(10.0)))
    assert _approx(implied_concrete, MATERIALS["concrete"]["z_over_a"], tol=8e-3)
    # and it is genuinely NOT the NIST ordinary-concrete value
    assert not _approx(implied_concrete, Z_OVER_A_NIST_ORDINARY_CONCRETE, tol=5e-3)
    assert Z_OVER_A_NIST_ORDINARY_CONCRETE > MATERIALS["concrete"]["z_over_a"]


def test_klein_nishina_limits_and_scaling():
    """sigma_KN -> the Thomson cross section 6.65e-25 cm2 as E -> 0, and falls
    roughly as 1/E at high energy."""
    thomson = 8.0 / 3.0 * math.pi * R_E_CM ** 2
    assert _approx(thomson, 6.652e-25, tol=1e-3)
    assert _approx(klein_nishina_per_electron(1e-5), thomson, tol=1e-3)
    # monotonically decreasing
    prev = float("inf")
    for e in (0.01, 0.1, 1.0, 10.0, 100.0):
        s = klein_nishina_per_electron(e)
        assert s < prev
        prev = s
    # roughly 1/E at high energy: a decade in E costs about a decade in sigma
    ratio = klein_nishina_per_electron(10.0) / klein_nishina_per_electron(100.0)
    assert 5.0 < ratio < 12.0, ratio
    # LINEAR in Z per atom -- Compton sees electrons, not atoms
    assert _approx(klein_nishina_per_atom(1.0, 82),
                   82 * klein_nishina_per_electron(1.0))
    assert _approx(klein_nishina_per_atom(1.0, 82) / klein_nishina_per_atom(1.0, 41),
                   2.0)
    for bad in ((0.0,), (-1.0,)):
        try:
            klein_nishina_per_electron(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_compton_mass_coefficients_are_nearly_material_independent():
    """Because Z/A ~ 0.5 for everything but hydrogen, mu_c/rho barely varies
    across materials -- the quantitative reason MeV-range shielding is a question
    of mass rather than of chemistry (~NE-11 P2)."""
    vals = [mass_coefficient(m, 1.0, "c")
            for m in ("air", "water", "concrete", "iron", "lead")]
    assert max(vals) / min(vals) < 1.5, vals
    # water is the outlier, and hydrogen is why: Z/A = 1 for 1H, 0.5 for the rest
    assert MATERIALS["water"]["z_over_a"] > MATERIALS["iron"]["z_over_a"]
    assert mass_coefficient("water", 1.0, "c") > mass_coefficient("lead", 1.0, "c")


# --- Compton kinematics  [Eq. (7.33)] -------------------------------------

def test_compton_scattering_energy_and_its_limits():
    """E' = E/[1 + (E/m_e c^2)(1 - cos theta)].  Forward scattering costs
    nothing; backscatter costs the most."""
    e = 0.6617
    assert _approx(compton_scattered_energy(e, 0.0), e)
    assert compton_electron_energy(e, 0.0) == 0.0
    for deg in (30, 90, 180):
        th = math.radians(deg)
        assert compton_scattered_energy(e, th) < e
        assert _approx(compton_scattered_energy(e, th)
                       + compton_electron_energy(e, th), e)
    # monotone in angle
    prev = e + 1.0
    for deg in range(0, 181, 10):
        v = compton_scattered_energy(e, math.radians(deg))
        assert v < prev
        prev = v
    # at 90 degrees the shift is exactly one electron rest energy in 1/E
    assert _approx(1.0 / compton_scattered_energy(e, math.pi / 2) - 1.0 / e,
                   1.0 / M_E_C2_MEV)


def test_the_137Cs_compton_edge_and_backscatter():
    """The numbers every gamma spectroscopist knows: 137Cs emits 662 keV, its
    Compton edge sits at 477 keV and its backscatter peak at 184 keV.  The two
    must sum to the full energy, since one photon's loss is the other's gain."""
    e = 0.6617
    assert _approx(compton_edge(e), 0.4774, tol=1e-3), "%.4f" % compton_edge(e)
    assert _approx(backscatter_energy(e), 0.1843, tol=1e-3)
    assert _approx(compton_edge(e) + backscatter_energy(e), e)
    # 60Co's 1.3325 MeV line
    assert _approx(compton_edge(1.3325), 1.1181, tol=1e-3)
    # the edge is always BELOW the photopeak -- a Compton event cannot deposit
    # everything, which is why the full-energy peak needs photoelectric capture
    for src in (0.05954, 0.14051, 0.6617, 1.3325, 6.129):
        assert compton_edge(src) < src


def test_backscatter_saturates_near_a_quarter_MeV():
    """E'(180) -> m_e c^2/2 = 0.2555 MeV as E -> infinity.  So backscatter peaks
    cluster at 200-250 keV whatever the source, which is what makes them
    recognisable in a spectrum (~NE-15)."""
    assert backscatter_energy(1e4) < M_E_C2_MEV / 2.0
    assert _approx(backscatter_energy(1e4), M_E_C2_MEV / 2.0, tol=1e-3)
    for e in (0.5, 1.0, 5.0, 50.0):
        assert backscatter_energy(e) < M_E_C2_MEV / 2.0
    # and it is monotonically increasing towards that ceiling
    assert (backscatter_energy(0.5) < backscatter_energy(1.0)
            < backscatter_energy(5.0) < backscatter_energy(50.0))


def test_the_compton_wavelength_shift_is_a_universal_constant():
    """Delta lambda = (h/m_e c)(1 - cos theta) depends on ANGLE ONLY -- not on
    energy, not on material.  That is what Compton's 1923 experiment showed and
    why it settled the photon-momentum question."""
    assert _approx(compton_wavelength_shift_A(0.0), 0.0)
    assert _approx(compton_wavelength_shift_A(math.pi / 2), 0.024263, tol=1e-4)
    assert _approx(compton_wavelength_shift_A(math.pi), 2 * 0.024263, tol=1e-4)
    # cross-check against the energy form: converting E' back to a wavelength
    # must give the same shift, at any incident energy
    HC_MEV_ANGSTROM = 0.01239841984         # hc = 12.398 keV A
    for e in (0.1, 0.662, 5.0):
        for deg in (30, 90, 150):
            th = math.radians(deg)
            lam0 = HC_MEV_ANGSTROM / e
            lam1 = HC_MEV_ANGSTROM / compton_scattered_energy(e, th)
            assert _approx(lam1 - lam0, compton_wavelength_shift_A(th), tol=1e-3), \
                "E=%.3f deg=%d: %.6f vs %.6f" % (e, deg, lam1 - lam0,
                                                 compton_wavelength_shift_A(th))


# --- photoelectric effect  [§7.3.1] ---------------------------------------

def test_photoelectron_energy_and_the_binding_threshold():
    """E_e = E - E_b, and a photon below the binding energy cannot eject that
    shell's electron at all -- which is what makes absorption edges DISCONTINUOUS
    rather than smooth."""
    assert _approx(photoelectron_energy(0.5, 0.088), 0.412)
    assert _approx(photoelectron_energy(0.088, 0.088), 0.0)
    try:
        photoelectron_energy(0.05, 0.088)
    except ValueError:
        pass
    else:
        raise AssertionError("below-threshold photon should be rejected")


def test_the_lead_K_edge_is_a_real_discontinuity_in_the_tables():
    """S&F quote the lead K edge at 88 keV.  Appendix C.3 lists that energy
    TWICE -- once with the K shell closed and once with it open -- and the
    photoelectric coefficient jumps by 4.7x between the two, because a whole new
    pair of electrons becomes available at once.

    This is the single sharpest feature in the photon tables, and it is why
    contrast agents work: iodine (K = 33 keV) and barium (K = 37 keV) are chosen
    so that their edges sit inside the diagnostic x-ray band (~NE-27)."""
    assert _approx(K_EDGE_KEV["Pb"], 88.0)
    rows = load_photon_coefficients("lead")
    at_edge = [r for r in rows if abs(r[0] - 0.088) < 1e-6]
    assert len(at_edge) == 2, "expected a duplicated K-edge pair, got %d" % len(at_edge)
    below, above = sorted(at_edge, key=lambda r: r[1]["ph"])
    assert _approx(below[1]["ph"], 1.547, tol=1e-3)
    assert _approx(above[1]["ph"], 7.320, tol=1e-3)
    assert _approx(above[1]["ph"] / below[1]["ph"], 4.73, tol=1e-2)
    # the Compton coefficient is untouched across the edge -- Compton scattering
    # does not care about binding at 88 keV in the way the photoelectric does
    assert _approx(below[1]["c"], above[1]["c"])

    assert len([r for r in rows if abs(r[0] - 0.088) < 1e-6]) == 2

    # water, with Z = 1 and 8, has no edge anywhere above 10 keV
    wrows = [r for r in load_photon_coefficients("water") if r[0] > 0.01]
    for i in range(1, len(wrows)):
        assert wrows[i][1]["ph"] <= wrows[i - 1][1]["ph"] * 1.05


def test_edge_energies_return_the_below_edge_branch():
    """The interpolator's documented convention at a duplicated edge energy:
    exactly-at returns the lower branch, just-above returns the upper one.  The
    jump must therefore appear between 0.0880 and 0.0881 MeV, not be smeared."""
    at = mass_coefficient("lead", 0.088, "ph")
    just_above = mass_coefficient("lead", 0.0881, "ph")
    just_below = mass_coefficient("lead", 0.0879, "ph")
    assert _approx(at, 1.547, tol=1e-3)
    assert just_above > 4 * at
    assert _approx(just_below, at, tol=5e-3)      # continuous from below
    # and no interpolation call ever straddles the pair
    for e in (0.0875, 0.088, 0.0885, 0.09, 0.095):
        v = mass_coefficient("lead", e, "ph")
        assert v > 0


def test_the_K_edges_rise_steeply_with_Z():
    """13.6 eV for hydrogen to 116 keV for uranium -- four orders of magnitude.
    Roughly Z^2 (the Bohr scaling of ~NE-01), which is why heavy elements have
    their edges in the diagnostic x-ray band and light ones do not."""
    assert K_EDGE_KEV["H"] < K_EDGE_KEV["C"] < K_EDGE_KEV["O"] < K_EDGE_KEV["Fe"]
    assert K_EDGE_KEV["Fe"] < K_EDGE_KEV["Pb"] < K_EDGE_KEV["U"]
    # Bohr: E_K ~ 13.6 Z^2 eV; good to a factor of ~2 even at lead
    for el, Z in (("C", 6), ("O", 8), ("Fe", 26)):
        bohr_kev = 13.6e-3 * Z * Z
        assert 0.4 < K_EDGE_KEV[el] / bohr_kev < 1.2, el
    # fluorescent yield rises from almost nothing at low Z to near unity at high Z
    assert FLUORESCENT_YIELD[8] < 0.01 < 0.9 < FLUORESCENT_YIELD[90]


def test_photoelectric_Z4_over_E3_scaling():
    """Eq. (7.32), sigma ~ Z^4/E^3, is a crude approximation and the module says
    so -- but it must at least reproduce the sign and rough size of the trends
    the tables show."""
    # Z^4: doubling Z multiplies by 16 at fixed energy
    assert _approx(photoelectric_scaling(82, 0.1) / photoelectric_scaling(41, 0.1), 16.0)
    # E^-3: doubling energy divides by 8 at fixed Z
    assert _approx(photoelectric_scaling(82, 0.2) / photoelectric_scaling(82, 0.1),
                   1.0 / 8.0)
    # against the tables: lead beats water enormously per gram, and the margin
    # is orders of magnitude, as Z^4 demands
    ratio = (mass_coefficient("lead", 0.1, "ph")
             / mass_coefficient("water", 0.1, "ph"))
    assert ratio > 500, ratio
    # and the photoelectric coefficient falls very steeply with energy
    fall = (mass_coefficient("lead", 0.1, "ph")
            / mass_coefficient("lead", 1.0, "ph"))
    assert fall > 100, fall
    for bad in ((0, 1.0), (1, 0.0)):
        try:
            photoelectric_scaling(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


# --- pair production  [§7.3.3] --------------------------------------------

def test_pair_production_thresholds():
    """2 m_e c^2 = 1.022 MeV in a nuclear field, 4 m_e c^2 = 2.044 in an
    electron's -- the light recoil partner must carry real momentum."""
    assert _approx(pair_production_threshold(), 1.022, tol=1e-3)
    assert _approx(triplet_production_threshold(), 2.044, tol=1e-3)
    assert _approx(triplet_production_threshold() / pair_production_threshold(), 2.0)
    assert _approx(pair_kinetic_energy_shared(5.0), 5.0 - TWO_ME_C2_MEV)
    assert _approx(pair_kinetic_energy_shared(TWO_ME_C2_MEV), 0.0)
    try:
        pair_kinetic_energy_shared(1.0)
    except ValueError:
        pass
    else:
        raise AssertionError("below-threshold pair production should be rejected")


def test_the_tables_switch_pair_production_on_at_the_threshold():
    """Not 'small below 1.022 MeV' -- IDENTICALLY ZERO.  A conservation law, not
    a cross-section trend, and the extracted tables show it exactly."""
    for m in ("water", "iron", "lead"):
        rows = load_photon_coefficients(m)
        assert all(d["pp"] == 0.0 for e, d in rows if e < 1.022), m
        assert all(d["pp"] > 0.0 for e, d in rows if e > 1.5), m
    # and it grows with energy once open, eventually dominating in lead
    assert (mass_coefficient("lead", 10.0, "pp")
            > mass_coefficient("lead", 2.0, "pp") > 0)


def test_annihilation_returns_two_511_keV_photons():
    """The positron's fate.  Pair production parks 1.022 MeV and hands it back
    as two penetrating photons -- which is why it does not simply remove energy,
    and why 511 keV is the signature of every positron emitter (~NE-27)."""
    assert _approx(annihilation_photon_energy(), M_E_C2_MEV)
    assert _approx(2 * annihilation_photon_energy(), TWO_ME_C2_MEV)
    assert _approx(annihilation_photon_energy(), 0.511, tol=1e-3)


# --- the three together  [§7.3.4] -----------------------------------------

def test_each_process_dominates_its_own_band():
    """Photoelectric low, Compton middle, pair high -- in every material."""
    for m in ("water", "iron", "lead"):
        assert dominant_process(m, 0.01) == "ph", m
        assert dominant_process(m, 1.0) == "c", m
    # pair production takes over in lead well within the tabulated range
    assert dominant_process("lead", 10.0) == "pp"
    # but not in water, where Compton still leads at 10 MeV
    assert dominant_process("water", 10.0) == "c"


def test_the_compton_window_narrows_with_Z():
    """The practical statement of the Z^4 and Z^2 scalings: photoelectric eats
    into the window from below and pair production from above, both faster in
    heavy elements.  Water's window spans three decades; lead's, one."""
    windows = {}
    for m in ("water", "concrete", "iron", "lead"):
        lo, hi = crossover_energies(m)
        assert lo is not None, m
        windows[m] = (lo, hi if hi else 20.0)
    # lower crossover rises monotonically with Z
    assert (windows["water"][0] < windows["concrete"][0]
            < windows["iron"][0] < windows["lead"][0])
    # lead's window is far narrower than water's
    w_water = windows["water"][1] / windows["water"][0]
    w_lead = windows["lead"][1] / windows["lead"][0]
    assert w_water > 10 * w_lead, (w_water, w_lead)
    assert _approx(windows["lead"][0], 0.556, tol=5e-2)


def test_interacting_is_not_depositing():
    """f = mu_en/mu is well below 1 through the Compton region, because the
    scattered photon leaves with most of the energy.  This gap is exactly where
    buildup factors (~NE-11) and dose conversion (~NE-17) live."""
    for m in ("water", "iron", "lead"):
        for e in (0.1, 0.5, 1.0, 5.0):
            f = energy_transfer_fraction(m, e)
            assert 0.0 < f <= 1.0, (m, e, f)
    # in water at 100 keV only ~15% is deposited, because the Compton-scattered
    # photon carries the rest away; in lead ~37%, higher because photoelectric
    # absorption is available there
    assert _approx(energy_transfer_fraction("water", 0.1), 0.154, tol=2e-2)
    assert _approx(energy_transfer_fraction("lead", 0.1), 0.370, tol=2e-2)
    assert energy_transfer_fraction("lead", 0.1) > 2 * energy_transfer_fraction("water", 0.1)
    # f dips in the Compton region and recovers at high energy in water
    assert (energy_transfer_fraction("water", 0.1)
            < energy_transfer_fraction("water", 5.0))


def test_K_fluorescence_escape_shows_up_at_the_edge():
    """A feature only visible once the K-edge rows are present.  Crossing lead's
    K edge upward, mu JUMPS by 4.5x but mu_en rises only 1.5x, so the deposited
    FRACTION collapses from 0.90 to 0.29.

    The reason is physical and specific: above the edge the photon is absorbed
    photoelectrically, but the resulting K vacancy is filled with the emission of
    a 75-85 keV fluorescence x-ray (S&F §7.3.1 quotes a K fluorescent yield of
    0.965 at Z = 90), and that x-ray escapes carrying most of the energy. More
    interactions, less deposition. This is the origin of the escape peaks seen in
    high-Z detectors (~NE-15)."""
    pair = [r for r in load_photon_coefficients("lead") if abs(r[0] - 0.088) < 1e-6]
    assert len(pair) == 2
    below, above = sorted(pair, key=lambda r: r[1]["total"])
    f_below = below[1]["en"] / below[1]["total"]
    f_above = above[1]["en"] / above[1]["total"]
    assert _approx(f_below, 0.900, tol=1e-2), "%.4f" % f_below
    assert _approx(f_above, 0.291, tol=1e-2), "%.4f" % f_above
    # total attenuation jumps up while energy absorption barely moves
    assert above[1]["total"] / below[1]["total"] > 4.0
    assert above[1]["en"] / below[1]["en"] < 2.0
    assert f_above < f_below / 2.0
    # the fluorescent yield is high enough at high Z for this to matter
    assert FLUORESCENT_YIELD[90] > 0.9


def test_components_sum_to_the_total():
    """mu/rho = mu_ph/rho + mu_c/rho + mu_pp/rho  [Eq. (7.38)].  Coherent
    scattering is deliberately excluded from the total, per §7.3.4."""
    for m in ("water", "iron", "lead"):
        for e, d in load_photon_coefficients(m):
            parts = d["ph"] + d["c"] + d["pp"]
            assert _approx(parts, d["total"], tol=0.02), \
                "%s at %.4g MeV: %.5g vs %.5g" % (m, e, parts, d["total"])


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
