"""NE-10 tests -- fusion and nucleosynthesis against Shultis & Faw §6.7, its
Example 6.6, and the atomic masses of Appendix B.

Run:  python3 test_fusion.py
"""

import math

from fusion import (
    M_N_U, M_H_U, M_E_U, U_MEV, TWO_ME_MEV, ALPHA_FS,
    K_BOLTZ_MEV_PER_K, AVOGADRO, MEV_PER_J, C_M_PER_S,
    load_atomic_masses, atomic_mass, has_nuclide,
    q_value, q_value_beta_plus,
    FUSION_REACTIONS, PP_CHAIN, PP_MULTIPLICITY, CNO_CYCLE,
    HELIUM_BURNING, ADVANCED_BURNING, TRITIUM_BREEDING, SUN,
    BOOK_Q_ERRATA, SUN_ERRATA,
    temperature_for_energy, thermal_energy, mean_thermal_energy,
    gamow_energy, gamow_peak_energy, gamow_peak_width,
    tunnelling_probability, barrier_temperature,
    reaction_product_energies, pp_chain_energy, energy_per_deuteron,
    mass_to_energy, solar_mass_loss_rate, solar_helium_rate,
    radiant_flux, core_power_density, deuterium_atoms, fusion_energy_of_water,
)

TAB = load_atomic_masses()

# (Z1, A1, Z2, A2) for each reaction in FUSION_REACTIONS
CHARGES = {"D+D->T+p": (1, 2, 1, 2), "D+D->3He+n": (1, 2, 1, 2),
           "D+T->4He+n": (1, 2, 1, 3), "D+3He->4He+p": (1, 2, 2, 3),
           "T+T->4He+2n": (1, 3, 1, 3), "p+6Li->4He+3He": (1, 1, 3, 6),
           "p+11B->3alpha": (1, 1, 5, 11)}


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --- Q-values  [§6.7] -------------------------------------------------------

def test_book_q_values():
    """Every Q-value S&F print for the candidate fusion reactions, recomputed
    from Appendix B.  Six of the seven agree to better than 3 keV; the seventh
    is the p+11B erratum below."""
    for lab, (reac, prod, q_book) in FUSION_REACTIONS.items():
        got = q_value(reac, prod, TAB)
        assert _approx(got, q_book, tol=1e-3), "%s: %.4f vs %.4f" % (lab, got, q_book)
        assert got > 0, lab          # every candidate fuel is exoergic


def test_the_p11B_erratum():
    """S&F print Q = 8.08 MeV for p + 11B -> 3 alpha.  Their own Appendix B
    masses give 8.68 MeV, which is the value quoted throughout the aneutronic
    fusion literature -- a 6/0 transposition."""
    assert set(BOOK_Q_ERRATA) == {"p+11B->3alpha"}
    printed, corrected = BOOK_Q_ERRATA["p+11B->3alpha"]
    assert _approx(printed, 8.08) and _approx(corrected, 8.68)
    got = q_value([(1, 1), (11, 5)], [(4, 2), (4, 2), (4, 2)], TAB)
    assert _approx(got, 8.682, tol=1e-3), "%.4f" % got
    assert abs(got - printed) > 0.5           # the printed value is not recoverable
    assert FUSION_REACTIONS["p+11B->3alpha"][2] == corrected


def test_beta_plus_reactions_need_the_electron_correction():
    """p + p -> D + beta+ + nu comes out at 1.442 MeV from bare neutral-atom
    masses and 0.420 MeV once 2 m_e c^2 is subtracted.  S&F quote 0.42.

    This is the same trap as ~NE-05's beta+ decays, and it matters here because
    stellar hydrogen burning is full of beta+ steps.  Getting it wrong inflates
    the sun's energy budget by 4% and the p-p step itself by 240%."""
    naive = q_value([(1, 1), (1, 1)], [(2, 1)], TAB, n_positrons=0)
    corrected = q_value([(1, 1), (1, 1)], [(2, 1)], TAB, n_positrons=1)
    assert _approx(naive, 1.4422, tol=1e-3)
    assert _approx(corrected, 0.4202, tol=1e-3)
    assert _approx(naive - corrected, TWO_ME_MEV)
    assert _approx(TWO_ME_MEV, 1.022, tol=1e-3)
    assert _approx(q_value_beta_plus([(1, 1), (1, 1)], [(2, 1)], 1, TAB), corrected)
    # a reaction with no positrons is unaffected
    assert _approx(q_value([(2, 1), (3, 1)], [(4, 2), (1, 0)], TAB, 0),
                   q_value([(2, 1), (3, 1)], [(4, 2), (1, 0)], TAB))


def test_tritium_breeding_reactions():
    """D-T fusion consumes tritium, which has a 12.3 y half-life and does not
    occur naturally -- so a D-T reactor must breed its own from lithium
    [S&F p. 164].  6Li gives it exoergically; 7Li costs 2.5 MeV but RETURNS the
    neutron, so it can breed more than one triton per incident neutron."""
    q6 = q_value(*TRITIUM_BREEDING["n+6Li->4He+T"][:2], table=TAB)
    q7 = q_value(*TRITIUM_BREEDING["n+7Li->4He+T+n"][:2], table=TAB)
    assert _approx(q6, 4.783, tol=1e-3)
    assert _approx(q7, -2.467, tol=1e-2)
    assert q6 > 0 > q7
    # the 7Li route is a NEUTRON MULTIPLIER: one neutron in, one out plus a triton
    assert len(TRITIUM_BREEDING["n+7Li->4He+T+n"][1]) == 3
    assert (1, 0) in TRITIUM_BREEDING["n+7Li->4He+T+n"][1]
    # and the 14.05 MeV D-T neutron has ample energy for its 2.5 MeV threshold
    q_dt = q_value([(2, 1), (3, 1)], [(4, 2), (1, 0)], TAB)
    _, e_n = reaction_product_energies(q_dt, atomic_mass(4, 2, TAB), M_N_U)
    assert e_n > abs(q7) * (1 + M_N_U / 7.016)


# --- temperatures, barriers and the Gamow peak ------------------------------

def test_thermal_energy_conversions():
    """kT = 8.617e-11 MeV/K; 10 keV plasma is 1.16e8 K."""
    assert _approx(thermal_energy(1.0), K_BOLTZ_MEV_PER_K)
    assert _approx(mean_thermal_energy(1.0), 1.5 * K_BOLTZ_MEV_PER_K)
    assert _approx(temperature_for_energy(0.010), 1.1605e8, tol=1e-3)
    assert _approx(thermal_energy(temperature_for_energy(0.010)), 0.010)
    # the sun's core, 15 MK, is only 1.3 keV
    assert _approx(thermal_energy(SUN["core_temperature_k"]) * 1e3, 1.293, tol=1e-3)
    # S&F's stated thermonuclear range, 10-300 MK
    assert 0.8e-3 < thermal_energy(1e7) < 1.0e-3
    assert 0.025 < thermal_energy(3e8) < 0.027
    for bad in (-1.0,):
        try:
            thermal_energy(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("negative temperature should be rejected")


def test_the_classical_barrier_is_hopeless():
    """Requiring 3kT/2 to equal the Coulomb barrier gives 3e9 K for D-T -- two
    hundred times the sun's core temperature and thirty times what any tokamak
    reaches.  If fusion needed that, nothing would burn anywhere."""
    tb = barrier_temperature(1, 2, 1, 3)
    assert 2e9 < tb < 5e9, tb
    assert tb > 100 * SUN["core_temperature_k"]
    assert tb > 20 * temperature_for_energy(0.010)
    # and it scales with charge, so p+11B is worse still
    assert barrier_temperature(1, 1, 5, 11) > 3 * tb


def test_gamow_energy_scales_as_charge_squared():
    """E_G = 2 mu c^2 (pi alpha Z1 Z2)^2.  The (Z1 Z2)^2 sits inside a square
    root inside an exponential, so charge is punished ferociously: D-T's
    1.18 MeV against p-11B's 22.4 MeV, a factor of 19 for a charge product of 5."""
    eg_dt = gamow_energy(1, 2, 1, 3)
    assert _approx(eg_dt, 1.175, tol=1e-3), "%.4f" % eg_dt
    assert _approx(gamow_energy(1, 1, 5, 11), 22.438, tol=1e-3)
    assert _approx(gamow_energy(1, 1, 1, 1), 0.4896, tol=1e-3)
    # explicit formula check
    for Z1, A1, Z2, A2 in [(1, 2, 1, 3), (1, 1, 5, 11), (2, 4, 6, 12)]:
        mu = A1 * A2 / float(A1 + A2)
        assert _approx(gamow_energy(Z1, A1, Z2, A2),
                       2 * mu * U_MEV * (math.pi * ALPHA_FS * Z1 * Z2) ** 2)
    # quadrupling the charge product multiplies E_G by 16 at fixed reduced mass
    assert _approx(gamow_energy(2, 4, 2, 4) / gamow_energy(1, 4, 1, 4), 16.0)
    for bad in [(0, 1, 1, 1), (1, 0, 1, 1)]:
        try:
            gamow_energy(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_the_gamow_peak_sits_between_kT_and_the_barrier():
    """The whole point: E_0 is well ABOVE kT (only the Maxwellian tail tunnels)
    and well BELOW the Coulomb barrier (nothing has to climb it).  For D-T at
    10 keV, E_0 = 31 keV against a ~400 keV barrier."""
    T = temperature_for_energy(0.010)          # a 10 keV plasma
    kt = thermal_energy(T)
    e0 = gamow_peak_energy(T, 1, 2, 1, 3)
    assert _approx(e0, 0.03085, tol=1e-3), "%.5f" % e0
    assert e0 > 3 * kt
    barrier = 1.43996 * 1 * 1 / (1.2 * (2 ** (1 / 3.0) + 3 ** (1 / 3.0)))
    assert e0 < barrier / 5.0
    # explicit formula, E_0 = [E_G (kT)^2/4]^(1/3)
    assert _approx(e0, (gamow_energy(1, 2, 1, 3) * kt * kt / 4.0) ** (1 / 3.0))
    # the peak is broad -- the width is comparable to E_0 itself
    w = gamow_peak_width(T, 1, 2, 1, 3)
    assert 0.8 < w / e0 < 2.0


def test_the_gamow_peak_ranks_the_fuels():
    """At a fixed plasma temperature, E_0 orders the candidate fuels by how hard
    they are: D-D and D-T lowest, then D-3He, then p-11B.  That ordering, not the
    Q-value, is why every experiment on earth runs D-T -- which has neither the
    largest Q (D-3He does) nor the cleanest products."""
    T = temperature_for_energy(0.010)
    e0 = {lab: gamow_peak_energy(T, *CHARGES[lab]) for lab in FUSION_REACTIONS}
    assert e0["D+D->T+p"] < e0["D+T->4He+n"] < e0["D+3He->4He+p"] < e0["p+11B->3alpha"]
    # D-T is the easiest reaction with a large Q; D-3He has a larger Q but needs
    # 1.6x the Gamow energy, and p-11B is 4x harder still
    assert FUSION_REACTIONS["D+3He->4He+p"][2] > FUSION_REACTIONS["D+T->4He+n"][2]
    assert e0["D+3He->4He+p"] > e0["D+T->4He+n"]
    assert e0["p+11B->3alpha"] / e0["D+T->4He+n"] > 2.5


def test_tunnelling_probability_is_ferociously_energy_dependent():
    """P ~ exp(-sqrt(E_G/E)).  Doubling the energy from 10 to 20 keV raises the
    D-T tunnelling probability by a factor of 25 -- which is why fusion power
    scales so violently with temperature and why ignition is a threshold rather
    than a gradient (~NE-24)."""
    p10 = tunnelling_probability(0.010, 1, 2, 1, 3)
    p20 = tunnelling_probability(0.020, 1, 2, 1, 3)
    assert _approx(p20 / p10, 23.9, tol=1e-2), "%.2f" % (p20 / p10)
    assert 0 < p10 < 1 and p10 < p20
    assert _approx(p10, 1.961e-5, tol=1e-3)
    # p-11B at the same energy is 1e-16 times less likely than D-T
    assert _approx(tunnelling_probability(0.010, 1, 1, 5, 11) / p10, 1.37e-16, tol=1e-2)
    try:
        tunnelling_probability(0.0, 1, 2, 1, 3)
    except ValueError:
        pass
    else:
        raise AssertionError("zero energy should be rejected")


# --- D-T and the product split  [Eq. (6.46)] -------------------------------

def test_dt_gives_3_54_and_14_05_mev():
    """S&F Eq. (6.46): D + T -> 4He (3.54 MeV) + n (14.05 MeV).  The split is
    inverse-mass, exactly as for fission fragments.

    The 20/80 split is the central engineering fact of magnetic fusion: only the
    alpha's 3.5 MeV stays in the plasma to sustain the temperature, so ignition
    requires the alpha heating alone to balance all losses (~NE-24)."""
    q = q_value([(2, 1), (3, 1)], [(4, 2), (1, 0)], TAB)
    assert _approx(q, 17.589, tol=1e-3)
    e_alpha, e_n = reaction_product_energies(q, atomic_mass(4, 2, TAB), M_N_U)
    assert _approx(e_alpha, 3.54, tol=2e-3), "%.4f" % e_alpha
    assert _approx(e_n, 14.05, tol=2e-3), "%.4f" % e_n
    assert _approx(e_alpha + e_n, q)
    assert _approx(e_alpha / q, 0.2013, tol=1e-3)      # the alpha gets only 20%


def test_fusion_beats_fission_per_unit_mass():
    """D-T releases 17.6 MeV from 5 nucleons, fission ~200 MeV from 236.  Per
    nucleon that is 3.5 MeV against 0.85 -- a factor of four, and the reason
    fusion is worth the difficulty."""
    q_dt = q_value([(2, 1), (3, 1)], [(4, 2), (1, 0)], TAB)
    per_nucleon_fusion = q_dt / 5.0
    per_nucleon_fission = 200.0 / 236.0
    assert _approx(per_nucleon_fusion, 3.518, tol=1e-3)
    assert 4.0 < per_nucleon_fusion / per_nucleon_fission < 4.3


# --- stellar burning  [§6.7.2] ---------------------------------------------

def test_pp_chain_sums_to_the_book_value():
    """S&F Eq. (6.47): 4(1H) -> 4He + 2 gamma + 2 beta+ + 2 nu, Q = 26.72 MeV.

    The three steps' beta+-corrected Q-values sum to 24.69 MeV of NUCLEAR energy;
    adding the two positron annihilations (4 m_e c^2 = 2.044 MeV) gives 26.73.
    S&F's 26.72 is the second convention -- which is the right one for a star,
    since the positrons annihilate immediately.  The two differ by 8%, so it is
    worth knowing which is being quoted."""
    nuclear = pp_chain_energy(TAB, include_annihilation=False)
    total = pp_chain_energy(TAB, include_annihilation=True)
    assert _approx(nuclear, 24.687, tol=1e-3), "%.4f" % nuclear
    assert _approx(total, 26.731, tol=1e-3), "%.4f" % total
    assert _approx(total - nuclear, 4.0 * M_E_U * U_MEV)
    # each step matches its printed Q
    for (lab, reac, prod, q_book, npos), mult in zip(PP_CHAIN, PP_MULTIPLICITY):
        got = q_value(reac, prod, TAB, npos)
        assert _approx(got, q_book, tol=2e-3), "%s: %.4f vs %.4f" % (lab, got, q_book)
    # and the weighted sum of the printed values reproduces the nuclear total
    printed = sum(m * s[3] for s, m in zip(PP_CHAIN, PP_MULTIPLICITY))
    assert _approx(printed, nuclear, tol=1e-3)
    # a direct neutral-atom 4p -> 4He difference gives the annihilation-inclusive
    # figure with no correction at all -- the two routes must agree
    assert _approx(q_value([(1, 1)] * 4, [(4, 2)], TAB), total)


def test_cno_cycle_is_catalytic_and_equivalent():
    """S&F Eq. (6.48): the CNO cycle nets the same 26.72 MeV as the pp chain,
    because both convert 4 protons into 4He and nothing else.  12C enters the
    first step and leaves the last -- a catalyst, consumed nowhere."""
    total = sum(q_value(r, p, TAB, n) for _, r, p, n in CNO_CYCLE)
    assert _approx(total, 24.687, tol=2e-3), "%.4f" % total
    assert _approx(total + 4 * M_E_U * U_MEV, 26.731, tol=2e-3)
    assert _approx(total, pp_chain_energy(TAB, False), tol=2e-3)
    # 12C in, 12C out
    first_in = CNO_CYCLE[0][1]
    last_out = CNO_CYCLE[-1][2]
    assert (12, 6) in first_in and (12, 6) in last_out
    # four protons consumed, one alpha produced
    protons = sum(step[1].count((1, 1)) for step in CNO_CYCLE)
    alphas = sum(step[2].count((4, 2)) for step in CNO_CYCLE)
    assert protons == 4 and alphas == 1
    # two beta+ decays, as in the pp chain
    assert sum(step[3] for step in CNO_CYCLE) == 2


def test_helium_and_advanced_burning_q_values():
    """Every Q-value S&F print for the triple-alpha process and the subsequent
    alpha, carbon and oxygen burning stages."""
    for table in (HELIUM_BURNING, ADVANCED_BURNING):
        for lab, (reac, prod, q_book) in table.items():
            got = q_value(reac, prod, TAB)
            assert _approx(got, q_book, tol=2e-3), \
                "%s: %.4f vs %.4f" % (lab, got, q_book)
            assert got > 0, lab


def test_the_triple_alpha_bottleneck():
    """Two alphas cannot simply stick: 8Be is UNBOUND, so 4He + 4He is endoergic
    and 8Be falls apart in 7e-17 s.  Only a three-body encounter, catching the
    fleeting 8Be with a third alpha, gets past A = 8 -- and that is why the
    universe's carbon exists at all."""
    q_2alpha = q_value([(4, 2), (4, 2)], [(8, 4)], TAB)
    assert q_2alpha < 0, "8Be must be unbound relative to two alphas"
    assert _approx(q_2alpha, -0.0918, tol=1e-2), "%.4f" % q_2alpha
    # yet the three-body route is comfortably exoergic
    q_3alpha = q_value([(4, 2)] * 3, [(12, 6)], TAB)
    assert _approx(q_3alpha, 7.275, tol=2e-3)
    assert q_3alpha > 0
    # 8Be sits BELOW its neighbours in binding energy per nucleon -- the A = 8 gap
    be8 = q_value([(1, 1)] * 4 + [(1, 0)] * 4, [(8, 4)], TAB) / 8.0
    be4 = q_value([(1, 1)] * 2 + [(1, 0)] * 2, [(4, 2)], TAB) / 4.0
    assert be8 < be4, "B/A must dip at A=8 (%.3f vs %.3f)" % (be8, be4)


def test_binding_energy_peaks_at_nickel_62():
    """The turning point is B/A, and it peaks at 62Ni (8.7945 MeV/nucleon), not
    at 56Fe (8.7902) -- the same result ~NE-03's `most_bound_nuclide` returns.
    56Fe is the most ABUNDANT iron-peak nuclide, for reasons of nucleosynthesis
    (it descends from 56Ni), not the most bound."""
    def b_per_a(A, Z):
        return q_value([(1, 1)] * Z + [(1, 0)] * (A - Z), [(A, Z)], TAB) / A
    peak = max([(52, 24), (56, 26), (58, 26), (60, 28), (62, 28), (64, 30)],
               key=lambda az: b_per_a(*az))
    assert peak == (62, 28), peak
    assert _approx(b_per_a(62, 28), 8.7945, tol=1e-4)
    assert b_per_a(62, 28) > b_per_a(56, 26) > b_per_a(52, 24)


def test_fusion_stops_at_iron_but_not_the_way_one_might_guess():
    """Alpha capture does NOT turn endoergic at iron -- 56Ni + alpha -> 60Zn
    still releases 2.7 MeV, because the alpha's own B/A is only 7.07 and adding
    four nucleons at ~8.7 pays for it.  Two things actually stop the burning.

    (i) The YIELD collapses.  Alpha capture releases ~8 MeV a step all the way up
        to 56Ni and then 2.7 MeV -- a factor of three at exactly the peak.  A
        star gains almost nothing per gram burned and cannot hold off gravity.
    (ii) SYMMETRIC fusion, which is what silicon burning actually does, goes
        endoergic right there: 28Si + 28Si -> 56Ni releases 10.9 MeV, but
        56Fe + 56Fe -> 112Cd COSTS 30.6 MeV."""
    steps = [((48, 24), (52, 26)), ((52, 26), (56, 28)),
             ((56, 28), (60, 30)), ((60, 30), (64, 32))]
    qs = [q_value([(4, 2), a], [b], TAB) for a, b in steps]
    assert all(q > 0 for q in qs), qs                 # all still exoergic
    assert qs[1] > 7.5 and qs[2] < 3.0                # but the yield collapses
    assert qs[1] / qs[2] > 2.5

    assert q_value([(28, 14), (28, 14)], [(56, 28)], TAB) > 0
    q_fe = q_value([(56, 26), (56, 26)], [(112, 48)], TAB)
    assert q_fe < 0, "%.3f" % q_fe
    assert _approx(q_fe, -30.62, tol=1e-3)


def test_photodisintegration_takes_over_at_1e10_k():
    """S&F p. 173: during silicon burning the core reaches ~1e10 K, kT ~ 1 MeV,
    and photons begin to knock nucleons and alphas back out of nuclei.

    The competition is quantitative: S_alpha(56Fe) = 7.6 MeV against kT = 0.86 MeV
    at 1e10 K, so it is the Planck tail at ~9 kT that does the damage -- rare, but
    the photon density is enormous and the reaction is the exact reverse of the
    one making the energy.  Fusion does not merely stall at iron; it starts
    running backwards."""
    kt = thermal_energy(1e10)
    assert _approx(kt, 0.8617, tol=1e-3)
    s_alpha = -q_value([(56, 26)], [(52, 24), (4, 2)], TAB)
    assert _approx(s_alpha, 7.613, tol=1e-3), "%.3f" % s_alpha
    assert s_alpha > 0                     # 56Fe is bound against alpha emission
    assert 5.0 < s_alpha / kt < 12.0       # reachable only in the photon tail
    # and it is exactly the reverse of the last productive burning step
    assert _approx(s_alpha, q_value([(4, 2), (52, 24)], [(56, 26)], TAB))


# --- the sun and the scale of things  [§6.7.1-6.7.2] -----------------------

def test_solar_mass_and_helium_rates():
    """S&F Ch. 6 Prob. 23: at 4e26 W the sun converts 4.4e9 kg/s to energy and
    makes 9.3e37 helium nuclei a second."""
    assert _approx(solar_mass_loss_rate(), 4.45e9, tol=1e-2)
    assert _approx(solar_helium_rate(table=TAB), 9.34e37, tol=1e-2)
    assert _approx(mass_to_energy(1.0), C_M_PER_S ** 2)
    # over 4.6 Gy this is only 0.03% of the sun's mass -- it is not running out
    burned = solar_mass_loss_rate() * 4.6e9 * 3.15576e7
    assert burned / SUN["mass_kg"] < 1e-3


def test_flux_at_the_earth():
    """P/(4 pi r^2) = 1415 W/m2 at 1.5e11 m, within 4% of the measured solar
    constant of 1361 W/m2 -- the gap is S&F's rounding of the solar luminosity to
    4e26 W (the true value is 3.83e26)."""
    f = radiant_flux()
    assert _approx(f, 1414.7, tol=1e-3), "%.1f" % f
    assert abs(f - 1361.0) / 1361.0 < 0.05
    assert _approx(radiant_flux(distance_m=3e11), f / 4.0)      # inverse square
    try:
        radiant_flux(distance_m=0.0)
    except ValueError:
        pass
    else:
        raise AssertionError("zero distance should be rejected")


def test_the_solar_core_radius_erratum():
    """S&F write that the core is 'about 7,000 km in radius or about 0.1% of the
    sun's total volume'.  Those cannot both be true: with R_sun = 696 000 km,
    0.1% of the volume needs r = 69 600 km, and 7 000 km would be 0.0001%.

    The volume fraction is the half that is right, because it yields the familiar
    283 W/m3 core power density; 7 000 km would give 280 kW/m3, a thousand times
    the accepted figure."""
    printed, corrected = SUN_ERRATA["core_radius_km"]
    assert _approx(corrected / printed, 10.0)
    assert _approx(SUN["core_radius_km"], corrected)

    # the corrected radius reproduces the stated volume fraction
    frac = (SUN["core_radius_km"] / SUN["radius_km"]) ** 3
    assert _approx(frac, SUN["core_volume_fraction"], tol=0.03), "%.5f" % frac
    # the printed radius does not, by a factor of 1000
    frac_printed = (printed / SUN["radius_km"]) ** 3
    assert _approx(SUN["core_volume_fraction"] / frac_printed, 1000.0, tol=0.05)

    # and the power density that follows is the familiar one
    assert _approx(core_power_density(), 283.0, tol=5e-3), "%.1f" % core_power_density()


def test_the_sun_is_a_terrible_power_plant():
    """283 W/m3 is less than a compost heap.  The sun is bright because it is
    huge, not because its core is intense -- so gravitational confinement is no
    guide at all to how hard magnetic confinement is (~NE-24)."""
    assert 100.0 < core_power_density() < 500.0
    # a 3 GW-thermal reactor core of ~30 m3 runs at ~1e8 W/m3, a million times more
    assert 1e8 / core_power_density() > 1e5


def test_the_pp_bottleneck_is_absurdly_slow():
    """One proton in 1e18 fuses per second, giving a mean proton lifetime in the
    core of ~3e10 y -- longer than the age of the universe.  The p+p step runs on
    the WEAK force (it must turn a proton into a neutron), and that is what sets
    a star's lifetime."""
    lifetime_s = SUN["proton_density_per_cm3"] / SUN["pp_rate_per_cm3_s"]
    lifetime_y = lifetime_s / 3.15576e7
    assert _approx(lifetime_y, 3.17e10, tol=1e-2), "%.3e" % lifetime_y
    assert lifetime_y > 1.38e10          # longer than the age of the universe
    # the fraction fusing per second
    assert _approx(SUN["pp_rate_per_cm3_s"] / SUN["proton_density_per_cm3"],
                   1e-18, tol=1e-9)


def test_the_fuel_supply_is_effectively_unlimited():
    """S&F Ch. 6 Probs. 22 and 24: an 8 oz glass of water holds 4.5 GJ of d-d
    fusion energy, and the oceans hold 2.7e31 J -- about 50 billion years of
    world energy use."""
    assert _approx(energy_per_deuteron(TAB), 11.923, tol=1e-3)
    assert _approx(energy_per_deuteron(TAB) * 2,
                   q_value([(2, 1), (2, 1)], [(4, 2)], TAB))
    assert _approx(q_value([(2, 1), (2, 1)], [(4, 2)], TAB), 23.84, tol=1e-3)

    glass = fusion_energy_of_water(236.6, table=TAB)
    assert _approx(glass, 4.52e9, tol=1e-2), "%.3e" % glass
    assert 4.0 < glass / 1e4 / 86400.0 < 6.5           # days of a 10 kW house

    oceans = 1.4e43 * energy_per_deuteron(TAB) / MEV_PER_J
    assert _approx(oceans, 2.67e31, tol=1e-2)
    assert _approx(deuterium_atoms(236.6), 2.373e21, tol=1e-2)
    assert _approx(deuterium_atoms(0.0), 0.0)
    try:
        deuterium_atoms(-1.0)
    except ValueError:
        pass
    else:
        raise AssertionError("negative mass should be rejected")


def test_a_type_ia_supernova_outshines_a_stellar_lifetime():
    """S&F Ch. 6 Prob. 24: the sun radiates ~1.3e44 J over 1e10 years; a Type Ia
    supernova releases 1-2e44 J in seconds.  Comparable totals, delivered a
    hundred million times faster -- which is why one is visible across a galaxy."""
    lifetime_j = SUN["power_w"] * SUN["lifetime_y"] * 3.15576e7
    assert _approx(lifetime_j, 1.262e44, tol=1e-2)
    for supernova_j in (1e44, 2e44):
        assert 0.5 < supernova_j / lifetime_j < 2.0


def test_masses_and_constants():
    assert has_nuclide(12, 6) and has_nuclide(4, 2)
    assert _approx(atomic_mass(12, 6, TAB), 12.0, tol=1e-12)
    assert _approx(atomic_mass(1, 0, TAB), M_N_U)      # the neutron passes through
    assert _approx(TWO_ME_MEV, 2 * M_E_U * U_MEV)
    assert _approx(1.0 / ALPHA_FS, 137.036, tol=1e-5)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
