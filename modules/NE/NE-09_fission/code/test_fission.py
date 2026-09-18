"""NE-09 tests -- fission against Shultis & Faw §§6.5.3-6.6, its Examples 6.4
and 6.5, its Tables 6.2-6.5, and the atomic masses of Appendix B.

Run:  python3 test_fission.py
"""

import math

from fission import (
    M_N_U, M_H_U, U_MEV, MEV_PER_J, AVOGADRO,
    load_atomic_masses, atomic_mass, has_nuclide,
    SPONTANEOUS_FISSION, NEUTRON_YIELD, WATT_PARAMS, FISSION_ENERGY_MEV,
    TABLE_6_2_ERRATA, BETA_BRANCH_PERCENT,
    FISSILE, FISSIONABLE, FERTILE, BREEDING,
    separation_energy_n, excitation_energy, is_fissile,
    spontaneous_fission_rate, neutrons_per_gram_second,
    fragment_energy_split, prompt_energy_release, delayed_energy_release,
    conserve_fission, partner_fragment,
    total_neutrons, delayed_fraction, delayed_neutrons,
    watt_spectrum, watt_mean_energy, watt_peak_energy, fission_energy,
    decay_heat_gamma, decay_heat_beta, decay_heat_total,
    fissions_per_second, grams_per_mwd, mwd_per_gram, burnup_energy,
)

TAB = load_atomic_masses()


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --- fissile vs fissionable  [§6.5.3] ---------------------------------------

def test_separation_energies_match_accepted_values():
    """S_n of the compound nucleus is the whole story.  These are standard
    values, quoted in every reactor-physics text."""
    for A, Z, expect in [(236, 92, 6.545), (239, 92, 4.806), (234, 92, 6.844),
                         (240, 94, 6.533), (242, 94, 6.309), (241, 94, 5.242),
                         (233, 90, 4.786)]:
        got = separation_energy_n(A, Z, TAB)
        assert _approx(got, expect, tol=1e-3), "S_n(%d,%d) = %.4f" % (A, Z, got)


def test_a_zero_energy_neutron_excites_by_exactly_S_n():
    """E* = S_n + E_n [§6.6].  With E_n = 0 the excitation is pure binding
    energy -- energy the nucleus supplies to itself."""
    assert _approx(excitation_energy(235, 92, 0.0, TAB),
                   separation_energy_n(236, 92, TAB))
    assert _approx(excitation_energy(235, 92, 2.0, TAB),
                   separation_energy_n(236, 92, TAB) + 2.0)


def test_fissile_and_fissionable_split_on_the_pairing_term():
    """Every fissile nuclide has an ODD neutron number; every merely fissionable
    one is even.  Adding a neutron to an odd-N target completes a pair and
    releases ~1.5 MeV more -- the pairing term of ~NE-02 -- and that margin is
    exactly what carries E* over the ~6 MeV barrier."""
    for nuc, A, Z in [("233U", 233, 92), ("235U", 235, 92),
                      ("239Pu", 239, 94), ("241Pu", 241, 94)]:
        assert (A - Z) % 2 == 1, nuc
        assert is_fissile(A, Z, table=TAB), nuc
        assert nuc in FISSILE
    for nuc, A, Z in [("238U", 238, 92), ("240Pu", 240, 94), ("232Th", 232, 90)]:
        assert (A - Z) % 2 == 0, nuc
        assert not is_fissile(A, Z, table=TAB), nuc
        assert nuc in FISSIONABLE
    # the gap between the two groups is real and large
    fissile_min = min(excitation_energy(A, Z, 0.0, TAB)
                      for A, Z in [(233, 92), (235, 92), (239, 94), (241, 94)])
    fissionable_max = max(excitation_energy(A, Z, 0.0, TAB)
                          for A, Z in [(238, 92), (240, 94), (232, 90)])
    assert fissile_min > fissionable_max
    assert fissile_min - fissionable_max > 1.0


def test_how_fast_a_neutron_238U_needs():
    """238U reaches only 4.81 MeV of excitation from binding alone, so a neutron
    must bring ~1.4 MeV of kinetic energy.  The fission spectrum peaks at 0.7 MeV
    and averages 2 MeV, so fast fission of 238U happens but is a minority process
    -- worth a few percent of the power in a PWR (~NE-19)."""
    deficit = 6.2 - excitation_energy(238, 92, 0.0, TAB)
    assert _approx(deficit, 1.394, tol=1e-2)
    assert watt_peak_energy() < deficit < watt_mean_energy()


def test_fertile_nuclides_breed_by_two_beta_decays():
    """232Th -> 233U and 238U -> 239Pu, each via (n,gamma) then two beta- decays
    [S&F p. 152].  Both raise Z by 2 and A by 1 -- turning a fissionable nuclide
    into a fissile one, which is the whole idea of a breeder (~NE-23)."""
    for parent in FERTILE:
        chain = BREEDING[parent]
        assert len(chain) == 5
        product = chain[-1]
        assert product in FISSILE
        assert parent in FISSIONABLE


# --- fragments  [Eqs. (6.34), (6.40)-(6.41), Examples 6.4-6.5] --------------

def test_nucleon_conservation_fixes_the_partner():
    """Eq. (6.34): A_L + A_H + nu_p = A_target + 1 and Z_L + Z_H = Z_target."""
    A_h, Z_h = conserve_fission(235, 92, 95, 38, 2)
    assert (A_h, Z_h) == (139, 54)                     # 139Xe, as in Example 6.4
    assert partner_fragment(235, 95, 2) == 139
    assert conserve_fission(235, 92, 90, 36, 4)[0] == 142    # 142Ba, Prob. 18
    assert conserve_fission(235, 92, 90, 36, 4)[1] == 56
    for bad in [(235, 92, 230, 38, 2), (235, 92, 95, 95, 2)]:
        try:
            conserve_fission(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_the_lighter_fragment_carries_more_energy():
    """Momentum conservation gives E_L/E_H = m_H/m_L [Eq. (6.41)].  Equal
    momenta, unequal masses -- so the light fragment is the faster and the more
    energetic, and the fragment-energy spectrum is bimodal rather than a line."""
    el, eh = fragment_energy_split(171.7, 94.919358, 138.918787)
    assert el > eh
    assert _approx(el + eh, 171.7)
    assert _approx(el / eh, 138.918787 / 94.919358)
    # a symmetric split would share equally
    a, b = fragment_energy_split(100.0, 118.0, 118.0)
    assert _approx(a, 50.0) and _approx(b, 50.0)
    # the measured means, 99.2 (light) and 68.1 (heavy) MeV [S&F Fig. 6.7],
    # bracket what this predicts for the most probable A = 95/139 split
    el, eh = fragment_energy_split(167.3, 95.0, 139.0)
    assert 95.0 < el < 105.0, el
    assert 63.0 < eh < 73.0, eh


def test_reproduces_example_6_4():
    """S&F Example 6.4 (printed p. 158): 235U(n,f) -> 139Xe + 95Sr + 2n + 7 gammas,
    with 5.2 MeV in the neutrons and 6.7 MeV in the gammas.  The book gets
    E_p = 183.6 MeV and E_H = 69.8 MeV."""
    ep = prompt_energy_release(235, 92, [(139, 54), (95, 38)], 2, TAB)
    assert _approx(ep, 183.6, tol=1e-3), "%.2f" % ep

    e_ff = ep - 5.2 - 6.7
    assert _approx(e_ff, 171.7, tol=1e-3), "%.2f" % e_ff

    el, eh = fragment_energy_split(e_ff, atomic_mass(95, 38, TAB),
                                   atomic_mass(139, 54, TAB))
    assert _approx(eh, 69.8, tol=2e-3), "%.2f" % eh
    assert _approx(el, 101.9, tol=2e-3), "%.2f" % el
    # the fragments carry 94% of the prompt release; neutrons and gammas 6%
    assert 0.93 < e_ff / ep < 0.95


def test_reproduces_example_6_5():
    """S&F Example 6.5 (printed p. 160): 139Xe and 95Sr beta-decay through seven
    steps to stable 139La and 95Mo, releasing 24.2 MeV.

    The subtlety the example turns on: seven beta- particles leave, but seven
    ambient electrons are absorbed to keep the atoms neutral, so the electron
    masses cancel and NEUTRAL-ATOM masses give the answer with no correction.
    Contrast beta+ and EC in ~NE-05, where they emphatically do not cancel."""
    ed = delayed_energy_release([(139, 54), (95, 38)], [(139, 57), (95, 42)], TAB)
    assert _approx(ed, 24.2, tol=2e-3), "%.2f" % ed
    # 139Xe -> 139La is 3 beta decays (Z 54->57), 95Sr -> 95Mo is 4 (Z 38->42)
    assert (57 - 54) + (42 - 38) == 7
    # delayed release is an order of magnitude below prompt, but not negligible
    ep = prompt_energy_release(235, 92, [(139, 54), (95, 38)], 2, TAB)
    assert 0.10 < ed / ep < 0.15


def test_the_two_examples_sum_to_the_textbook_200_mev():
    """Example 6.4's prompt 183.6 MeV plus Example 6.5's delayed 24.2 MeV is
    207.8 MeV -- the '~200 MeV per fission' of every introduction, and within
    1 MeV of Table 6.5's 207 MeV average over all fission outcomes."""
    ep = prompt_energy_release(235, 92, [(139, 54), (95, 38)], 2, TAB)
    ed = delayed_energy_release([(139, 54), (95, 38)], [(139, 57), (95, 42)], TAB)
    assert _approx(ep + ed, 207.8, tol=2e-3)
    assert abs((ep + ed) - fission_energy(False)) < 1.0


# --- neutrons  [Table 6.3, Eqs. (6.42)-(6.43)] -----------------------------

def test_reproduces_table_6_3():
    """S&F Table 6.3 (printed p. 158): nu and beta for the important nuclides."""
    expect = {("235U", "fast"): (2.57, 0.0064), ("235U", "thermal"): (2.43, 0.0065),
              ("233U", "thermal"): (2.48, 0.0026), ("239Pu", "thermal"): (2.87, 0.0021),
              ("241Pu", "thermal"): (3.14, 0.0049), ("238U", "fast"): (2.79, 0.0148),
              ("232Th", "fast"): (2.44, 0.0203)}
    for (nuc, spec), (nu, beta) in expect.items():
        assert _approx(total_neutrons(nuc, spec), nu)
        assert _approx(delayed_fraction(nuc, spec), beta)
        assert _approx(delayed_neutrons(nuc, spec), nu * beta)
    # every fissile nuclide gives more than 2 neutrons -- the necessary
    # condition for a chain reaction, with margin for leakage and capture
    for nuc in FISSILE:
        assert total_neutrons(nuc, "thermal") > 2.0
    # fast fission yields more neutrons than thermal: a hotter compound nucleus
    for nuc in ("235U", "233U", "239Pu"):
        assert total_neutrons(nuc, "fast") > total_neutrons(nuc, "thermal")


def test_the_delayed_fraction_is_tiny_and_decisive():
    """beta is under 1% everywhere, yet it is what makes a reactor controllable:
    without delayed neutrons the period between generations would be the ~1e-4 s
    prompt lifetime rather than the ~10 s precursor lifetime (~NE-20)."""
    for nuc in FISSILE:
        assert 0 < delayed_fraction(nuc, "thermal") < 0.01
    # 239Pu has a third of 235U's delayed fraction, which is why a
    # plutonium-heavy core has less reactivity margin before prompt criticality
    assert delayed_fraction("239Pu") < delayed_fraction("235U") / 2.5
    # 238U and 232Th, which fission only fast, have much larger fractions
    assert delayed_fraction("238U", "fast") > 2 * delayed_fraction("235U", "fast")
    assert delayed_fraction("232Th", "fast") > 0.02


def test_watt_spectrum_normalises_and_has_the_right_shape():
    """chi(E) [Eq. (6.42)] integrates to 1, peaks near 0.7 MeV and averages
    about 2 MeV.  Mode and mean differ by a factor of 3 -- the spectrum is very
    right-skewed, and quoting the wrong one is a standard error."""
    for nuc, spec in WATT_PARAMS:
        n, e_max = 40000, 30.0
        h = e_max / n
        total = sum(watt_spectrum((i + 0.5) * h, nuc, spec) for i in range(n)) * h
        assert _approx(total, 1.0, tol=2e-4), "%s %s: %.6f" % (nuc, spec, total)
    assert watt_spectrum(0.0) == 0.0
    assert _approx(watt_peak_energy(), 0.70, tol=2e-2)
    assert _approx(watt_mean_energy(), 1.99, tol=1e-2)
    assert watt_mean_energy() > 2.5 * watt_peak_energy()
    # 56% of fission neutrons clear the 1.4 MeV that fast fission of 238U needs,
    # but only 0.1% reach the 10 MeV that 16O(n,p) needs (~NE-08 P5) -- which is
    # why fast fission of 238U contributes real power while 16N production is a
    # trace process confined to the core
    def _tail(e0, n=40000, h=0.001):
        return sum(watt_spectrum(e0 + i * h) for i in range(n)) * h
    assert _approx(_tail(1.4), 0.556, tol=5e-3), _tail(1.4)
    assert _tail(10.0) < 2e-3, _tail(10.0)


def test_watt_agrees_with_the_compact_form():
    """Eq. (6.43), chi = a exp(-E/b) sinh(sqrt(cE)), is Eq. (6.42) rewritten with
    a = exp(-Ew/Tw)/sqrt(pi Ew Tw), b = Tw, c = 4Ew/Tw^2.  Table 6.4 lists BOTH
    parameter sets for each nuclide, so the two halves of every row must agree --
    an over-determined table, and a chance to check the transcription.

    All six rows agree to 5e-4, the rounding of the printed four-figure Ew and
    Tw; no errata here, unlike Table 6.2."""
    for (nuc, spec), (Ew, Tw, a, b, c) in WATT_PARAMS.items():
        assert _approx(a, math.exp(-Ew / Tw) / math.sqrt(math.pi * Ew * Tw), tol=1e-3)
        assert _approx(b, Tw, tol=1e-3)
        assert _approx(c, 4.0 * Ew / (Tw * Tw), tol=1e-3)
        for e in (0.1, 0.7, 2.0, 6.0):
            compact = a * math.exp(-e / b) * math.sinh(math.sqrt(c * e))
            assert _approx(watt_spectrum(e, nuc, spec), compact, tol=3e-3)


# --- energy budget and macroscopic conversions  [Table 6.5, pp. 162-163] ----

def test_reproduces_table_6_5():
    """S&F Table 6.5 (printed p. 161): 207 MeV produced, 198-204 recoverable."""
    assert _approx(fission_energy(False), 207.0)
    assert 198.0 <= fission_energy(True) <= 204.0
    # the fragments alone are 81% of the total and are deposited within ~1e-3 cm
    assert _approx(FISSION_ENERGY_MEV["fragment_kinetic"][0] / 207.0, 0.812, tol=1e-3)
    # the 12 MeV of neutrino energy is the only component that is 100% lost
    assert FISSION_ENERGY_MEV["neutrinos"][1] == 0.0
    assert _approx(FISSION_ENERGY_MEV["neutrinos"][0] / 207.0, 0.058, tol=1e-2)
    # every other component is fully recoverable, and capture gammas are a bonus
    for k, (p, r) in FISSION_ENERGY_MEV.items():
        if k not in ("neutrinos", "capture_gammas"):
            assert p == r, k
    assert FISSION_ENERGY_MEV["capture_gammas"][1] > FISSION_ENERGY_MEV["capture_gammas"][0]


def test_macroscopic_conversion_factors():
    """S&F pp. 162-163: 1 W = 3.1e10 fissions/s, 1 MWd = 1.05 g of 235U
    fissioned = 1.24 g consumed."""
    assert _approx(fissions_per_second(1.0), 3.1e10, tol=1e-2)
    assert _approx(grams_per_mwd(), 1.05, tol=3e-3)
    assert _approx(grams_per_mwd(fission_fraction=0.85), 1.24, tol=3e-3)
    # consumption exceeds fissioning by exactly 1/0.85
    assert _approx(grams_per_mwd(fission_fraction=0.85) / grams_per_mwd(), 1 / 0.85)
    # inverse consistency
    assert _approx(mwd_per_gram() * grams_per_mwd(), 1.0)
    assert _approx(burnup_energy(1000.0), 1000.0 * mwd_per_gram())


def test_a_gram_of_uranium_against_a_tonne_of_coal():
    """1 g of 235U yields ~0.95 MWd = 82 GJ.  Coal is about 12 GJ per TONNE, so
    the ratio is nearly 7 million -- the entire reason to bother with all of
    this, and the number S&F Ch. 6 Prob. 20 asks for."""
    gj = mwd_per_gram() * 86.4                      # 1 MWd = 86.4 GJ
    assert _approx(gj, 82.1, tol=1e-2), "%.2f GJ" % gj
    coal_gj_per_g = 12.0 / 1e6                      # 12 GJ/tonne
    assert 6e6 < gj / coal_gj_per_g < 8e6


def test_decay_heat_falls_as_a_power_law_not_an_exponential():
    """Eqs. (6.44)-(6.45): F = 1.4 t^-1.2 and 1.26 t^-1.2 MeV/s per fission.

    Power-law, not exponential -- the sum of hundreds of decay chains with
    half-lives spread over ten decades.  It therefore has no characteristic time
    and never really switches off, which is why a shut-down core still needs
    cooling days later (~NE-22)."""
    assert _approx(decay_heat_total(10.0), decay_heat_gamma(10.0) + decay_heat_beta(10.0))
    assert _approx(decay_heat_gamma(1.0), 1.4)
    assert _approx(decay_heat_beta(1.0), 1.26)
    # a decade in time costs a factor 10^1.2 ~ 15.8 in power, every decade
    for t in (10.0, 100.0, 1000.0):
        assert _approx(decay_heat_total(t) / decay_heat_total(10 * t), 10 ** 1.2)
    # an exponential would fall much faster over four decades than this does
    assert decay_heat_total(1e5) / decay_heat_total(10.0) > 1e-6
    for fn in (decay_heat_gamma, decay_heat_beta, decay_heat_total):
        try:
            fn(0.0)
        except ValueError:
            pass
        else:
            raise AssertionError("%s(0) should be rejected" % fn.__name__)


# --- spontaneous fission  [Table 6.2] ---------------------------------------

def test_table_6_2_is_internally_consistent():
    """Table 6.2 is over-determined, and that is what makes it checkable.  Every
    row must satisfy two relations that use different columns:

      (i)  n/(g s) = [ln2/T_half] (N_A/A) (P_fission) nu
      (ii) alphas per fission = P_alpha / P_fission,

    where P_alpha = 1 - P_fission - P_beta, with P_beta from the table's own
    caption for the three nuclides that also beta-decay.  Neither relation is
    printed in the book; both follow from what the columns mean.

    All 26 rows pass, but only after the two corrections recorded in
    TABLE_6_2_ERRATA -- see `test_the_two_table_6_2_typos`."""
    for nuc, (t_half_y, fis_pct, nu, alphas, n_per_gs) in SPONTANEOUS_FISSION.items():
        A = int("".join(ch for ch in nuc if ch.isdigit()))
        lam = math.log(2.0) / (t_half_y * 3.15576e7)
        decays_per_g_s = lam * AVOGADRO / A

        predicted = decays_per_g_s * (fis_pct / 100.0) * nu
        assert 0.7 < predicted / n_per_gs < 1.45, \
            "%s emission rate: predicted %.3g vs tabulated %.3g" \
            % (nuc, predicted, n_per_gs)

        alpha_pct = 100.0 - fis_pct - BETA_BRANCH_PERCENT.get(nuc, 0.0)
        assert alpha_pct > 0, nuc
        assert 0.7 < (alpha_pct / fis_pct) / alphas < 1.45, \
            "%s alphas/fission: predicted %.3g vs tabulated %.3g" \
            % (nuc, alpha_pct / fis_pct, alphas)
    assert len(SPONTANEOUS_FISSION) == 26


def test_the_two_table_6_2_typos():
    """The two corrections are not preferences -- each is forced by the row's
    other columns, and each printed value fails by a clean power of ten.

    237Np: printed fission probability 2.1e-12 %.  Both the alphas-per-fission
    column and the emission rate demand 2.1e-10 %, a factor of 100.
    248Cm: printed emission rate 4.1e12 n/(g s).  Its own half-life and fission
    probability give 4.1e7, a factor of 1e5 -- and 4.1e12 would make a
    339 000-year nuclide outshine 252Cf, whose half-life is 2.6 years."""
    assert set(TABLE_6_2_ERRATA) == {"237Np", "248Cm"}

    # 237Np: the printed value is off by exactly 100, in both cross-checks
    field, printed, used = TABLE_6_2_ERRATA["237Np"]
    assert _approx(used / printed, 100.0, tol=1e-9)
    assert _approx(SPONTANEOUS_FISSION["237Np"][1], used)
    assert _approx((100.0 - used) / used / SPONTANEOUS_FISSION["237Np"][3],
                   1.0, tol=0.05)

    # 248Cm: the printed value is off by exactly 1e5
    field, printed, used = TABLE_6_2_ERRATA["248Cm"]
    assert _approx(printed / used, 1e5, tol=1e-9)
    assert _approx(SPONTANEOUS_FISSION["248Cm"][4], used)
    # and the printed figure is physically impossible: 248Cm would beat 252Cf
    assert printed > neutrons_per_gram_second("252Cf")
    assert used < neutrons_per_gram_second("252Cf")
    assert SPONTANEOUS_FISSION["248Cm"][0] > 1e5 * SPONTANEOUS_FISSION["252Cf"][0]


def test_the_caption_matters_for_three_nuclides():
    """241Pu, 250Cm and 249Bk also beta-decay (99.998%, 14%, 99.999%), so alpha
    emission is not the complement of fission for them.  Ignoring the caption
    makes 249Bk look wrong by a factor of 70 000 -- a good reminder that a table
    footnote is part of the table."""
    assert set(BETA_BRANCH_PERCENT) == {"241Pu", "250Cm", "249Bk"}
    for nuc in BETA_BRANCH_PERCENT:
        fis_pct, alphas = SPONTANEOUS_FISSION[nuc][1], SPONTANEOUS_FISSION[nuc][3]
        naive = (100.0 - fis_pct) / fis_pct               # ignoring beta decay
        correct = (100.0 - fis_pct - BETA_BRANCH_PERCENT[nuc]) / fis_pct
        assert _approx(correct / alphas, 1.0, tol=0.05), nuc
        assert naive > correct
    # 249Bk is the extreme case
    assert (100.0 - SPONTANEOUS_FISSION["249Bk"][1]) / SPONTANEOUS_FISSION["249Bk"][1] \
        / SPONTANEOUS_FISSION["249Bk"][3] > 1e4


def test_the_neutron_sources_that_matter():
    """252Cf is a laboratory neutron source; 240Pu is why reactor-grade plutonium
    cannot be used in a gun-type weapon; 238U is a negligible background."""
    assert _approx(neutrons_per_gram_second("252Cf"), 2.3e12)
    # a 10 microgram 252Cf source gives over ten million neutrons a second
    assert neutrons_per_gram_second("252Cf") * 1e-5 > 1e7
    # 240Pu emits 60000 times more neutrons per gram than 239Pu
    assert neutrons_per_gram_second("240Pu") / neutrons_per_gram_second("239Pu") > 4e4
    # and 15 orders of magnitude more than 238U
    assert neutrons_per_gram_second("252Cf") / neutrons_per_gram_second("238U") > 1e14
    # 254Cf is the one nuclide in the table that mostly fissions rather than alphas
    assert SPONTANEOUS_FISSION["254Cf"][1] > 99.0
    assert all(v[1] < 99.0 for k, v in SPONTANEOUS_FISSION.items() if k != "254Cf")
    # rate = neutrons/(g s) divided by neutrons per fission
    assert _approx(spontaneous_fission_rate("252Cf", 1.0), 2.3e12 / 3.73)
    for bad in ("235U ", "1H"):
        try:
            neutrons_per_gram_second(bad)
        except KeyError:
            pass
        else:
            raise AssertionError("%r should not be in Table 6.2" % bad)


def test_neutrons_per_fission_rise_with_mass():
    """Heavier fissioning nuclides are more neutron-rich, so more neutrons boil
    off: 1.76 for 233U, 3.73 for 252Cf, 4.00 for 254Fm."""
    assert SPONTANEOUS_FISSION["233U"][2] < SPONTANEOUS_FISSION["252Cf"][2]
    assert _approx(SPONTANEOUS_FISSION["254Fm"][2], 4.00)
    assert all(1.5 < v[2] < 4.5 for v in SPONTANEOUS_FISSION.values())


def test_invalid_inputs_raise():
    bad = [(fissions_per_second, (1.0, 0.0)), (fissions_per_second, (-1.0,)),
           (grams_per_mwd, (235, 200.0, 0.0)), (grams_per_mwd, (235, 200.0, 1.5)),
           (fragment_energy_split, (100.0, 0.0, 1.0)),
           (watt_spectrum, (-1.0,))]
    for fn, args in bad:
        try:
            fn(*args)
        except ValueError:
            pass
        else:
            raise AssertionError("%s%r should be rejected" % (fn.__name__, args))
    for fn, args in [(total_neutrons, ("235U", "spontaneous")),
                     (watt_spectrum, (1.0, "241Pu", "thermal"))]:
        try:
            fn(*args)
        except KeyError:
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
