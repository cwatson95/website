"""
test_equations.py  —  checks for Module 12.EQ.

(1) each canonical Topic-12 equation reproduces a known (book-verified) value;
(2) CROSS-CHECKS -- the concept modules 12.1 (fuels.py) and 12.2 (ionization.py) and the
    worked-examples module 12.EP (examples.py) compute the same things, so a formula
    change anywhere in the topic fails this suite.  The Saha rows are the ~PK plasma
    extension (NOT Moran); their anchor is the literature de Broglie wavelength plus
    exact algebraic consistency with Moran's Eq.-14.35 ionization form.

Run:  cd code && python3 test_equations.py   ->  "All N tests passed."
"""
import math
import os
import sys

import equations as eq

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "12.1_fuels", "code"))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "12.2_ionization", "code"))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "12.EP_example_problems", "code"))
import fuels as m_fuels          # noqa: E402  (12.1)
import ionization as m_ion       # noqa: E402  (12.2)
import examples as m_ep          # noqa: E402  (12.EP)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1


# ---- (1) canonical values (book-verified) -----------------------------------
# combustion stoichiometry (Ex 13.1 / Eq. 13.4)
chk("theoretical_O2 octane", eq.theoretical_O2(8, 18), 12.5)                    # Ex 13.1
chk("theoretical_air octane", eq.theoretical_air_molar(8, 18), 59.5)            # Ex 13.1
chk("theoretical_air methane", eq.theoretical_air_molar(1, 4), 9.52)            # Eq. 13.4
chk("Eq13.2 AF mass", eq.air_fuel_mass_from_molar(59.5, 114.22), 15.1, 0.05)    # Ex 13.1
chk("Eq13.2 methane", eq.air_fuel_mass_from_molar(9.52, 16.04), 17.19, 0.01)    # p.808
chk("% theoretical air", eq.percent_theoretical_air(10.78, 9.52), 1.13, 5e-3)   # Ex 13.2
chk("% excess air", eq.percent_excess_air(89.25, 59.5), 0.50)                   # Ex 13.1b
chk("equivalence ratio", eq.equivalence_ratio(89.25, 59.5), 0.67, 5e-3)         # Ex 13.1 QQ
chk("dew point p_v (psi)", eq.dew_point_partial_pressure(0.169, 14.696), 2.484, 0.01)  # Ex 13.2c
# Eq. 13.9 (CO2 at 500 K spot check printed in Sec. 13.3.2, p.829)
chk("Eq13.9 CO2@500K", eq.enthalpy_formation_plus_dh(-393520.0, 17678.0 - 9364.0),
    -3.852e5, 60.0)
# steady-flow energy balance (Ex 13.5)
P_gt = [(1, -393520.0, 28622.0 - 9364.0), (2, -241820.0, 25218.0 - 9904.0),
        (6, 0.0, 22177.0 - 8682.0), (30.08, 0.0, 21529.0 - 8669.0)]
R_gt = [(1, -74850.0, 0.0)]
chk("Ex13.5 hP", eq.stream_enthalpy(P_gt), -359475.0, 1.0)                       # book -359,475
chk("Ex13.5 hP-hR", eq.energy_balance_steady(P_gt, R_gt), -284625.0, 1.0)
# closed-vessel energy balance (Ex 13.6, Eq. 13.17b)
P_cv = [(1, -393520.0, 37405.0 - 9364.0), (2, -241820.0, 31828.0 - 9904.0)]
R_cv = [(1, -74850.0, 0.0), (2, 0.0, 0.0)]
chk("Eq13.17b Ex13.6 Q", eq.energy_balance_closed(P_cv, R_cv, 900.0, 298.0),
    -745436.0, 1.0)                                                             # book -745,436
# enthalpy of combustion & heating values (Ex 13.7)
hhv = eq.enthalpy_of_combustion([(1, -393520.0, 0.0), (2, -285830.0, 0.0)],
                                [(1, -74850.0, 0.0)])
lhv = eq.enthalpy_of_combustion([(1, -393520.0, 0.0), (2, -241820.0, 0.0)],
                                [(1, -74850.0, 0.0)])
chk("Eq13.18 HHV molar", hhv, -890330.0)                                        # book -890,330
chk("HHV mass", eq.heating_value_mass(hhv, 16.04), 55507.0, 1.0)                # book 55,507
chk("Eq13.18 LHV molar", lhv, -802310.0)                                        # book -802,310
chk("LHV magnitude", eq.heating_value_molar(lhv), 802310.0)
# adiabatic flame temperature (Ex 13.8, Eq. 13.21b)
rhs = eq.adiabatic_flame_rhs([(1, -249910.0)], [(8, -393520.0), (9, -241820.0)])
chk("Eq13.21b RHS", rhs, 5074630.0, 1.0)                                        # book 5,074,630
TP = eq.interpolate_flame_temperature(
    rhs, {2350: 4955163.0, 2400: 5089337.0, 2500: 5358748.0})
chk("Ex13.8 TP", TP, 2395.0, 1.0)                                               # book ~2395 K

# equilibrium constant (Ex 14.1, Eqs. 14.29b/14.31/14.34)
dG298 = eq.gibbs_of_reaction([(1, -393520.0, 213.69)],
                             [(1, -110530.0, 197.54), (0.5, 0.0, 205.03)], 298.0)
chk("Eq14.29b dG0@298", dG298, -257253.0, 60.0)                                 # book -257,253
chk("Eq14.31 lnK@298", eq.lnK_from_gibbs(dG298, 298.0), 103.83, 0.02)           # book 103.83
chk("log10K@298", eq.log10K_from_gibbs(dG298, 298.0), 45.093, 0.02)             # book 45.093
h2000 = {"CO2": -393520.0 + (100804.0 - 9364.0), "CO": -110530.0 + (65408.0 - 8669.0),
         "O2": 0.0 + (67881.0 - 8682.0)}
dG2000 = eq.gibbs_of_reaction([(1, h2000["CO2"], 309.210)],
                              [(1, h2000["CO"], 258.600), (0.5, h2000["O2"], 268.655)],
                              2000.0)
chk("Eq14.29b dG0@2000", dG2000, -110453.0, 60.0)                               # book -110,453
chk("log10K@2000", eq.log10K_from_gibbs(dG2000, 2000.0), 2.885, 0.01)           # book 2.885
chk("Eq14.34 inverse", eq.log10K_inverse(2.885), -2.885)                        # A-27: -2.884
# Eq. 14.17 / 14.26: at the standard state (y p/pref = 1) mu reduces to g0, and the
# reaction-equilibrium residual is dG0; Table A-25 Gibbs-of-formation data reproduce
# Ex 14.1's dG0(298) to table round-off.
mu_CO2 = eq.chemical_potential_ideal_gas(-394380.0, 298.0, 1.0, 1.0)   # g_f0 (A-25)
mu_CO = eq.chemical_potential_ideal_gas(-137150.0, 298.0, 1.0, 1.0)
mu_O2 = eq.chemical_potential_ideal_gas(0.0, 298.0, 1.0, 1.0)
chk("Eq14.17 std state mu=g0", mu_CO2, -394380.0)
chk("Eq14.26 residual = dG0", eq.reaction_equilibrium_residual(
    [(1, mu_CO2)], [(1, mu_CO), (0.5, mu_O2)]), -257230.0, 1.0)         # vs -257,253 (A-25 g_f0)
assert abs(-257230.0 - dG298) < 60.0;  _n += 1
# equilibrium composition forms (Ex 14.2, Eqs. 14.32/14.35)
chk("Eq14.32 Ex14.2 K", eq.equilibrium_constant_composition(
    [(0.121, 1.0), (0.061, 0.5)], [(0.818, 1.0)], 1.0), 0.0363, 5e-4)   # book K = 0.0363
z = 0.129
chk("Eq14.35 Ex14.2 K", eq.equilibrium_constant_moles(
    [(z, 1.0), (z / 2.0, 0.5)], [(1.0 - z, 1.0)], (2.0 + z) / 2.0, 1.0), 0.0363, 5e-4)
# ionization equilibrium (Ex 14.8, Sec. 14.4.3)
chk("Ex14.8 p @95%", 15.63 * (1.0 - 0.95 ** 2) / 0.95 ** 2, 1.69, 0.005)        # book 1.69 atm
chk("Ex14.8 K round trip", eq.ionization_K_from_extent(0.95, 1.6885), 15.63, 0.01)
chk("Ex14.8 QQ z(K=0.78,1atm)", eq.ionization_extent_from_K(0.78, 1.0), 0.662, 5e-4)  # book 66.2%
chk("ionization inverse pair", eq.ionization_extent_from_K(
    eq.ionization_K_from_extent(0.4, 2.5), 2.5), 0.4, 1e-12)
# Saha extension [~PK, NOT Moran]: literature anchor + behavior
lam = (1.0 / eq.quantum_concentration(300.0)) ** (1.0 / 3.0)
chk("~PK e- de Broglie @300K", lam * 1e9, 4.30, 0.02)                            # lit ~4.30 nm
assert eq.saha_rhs(12000.0, 13.6) > eq.saha_rhs(6000.0, 13.6) > 0.0;  _n += 1
assert eq.saha_ionization_K(20000.0, 13.6) > eq.saha_ionization_K(10000.0, 13.6);  _n += 1

# ---- (2) cross-checks: concept modules match the registry -------------------
# 12.1 (fuels)
chk("12.1 theoretical_O2", m_fuels.theoretical_O2(8, 18), eq.theoretical_O2(8, 18))
chk("12.1 theoretical_air", m_fuels.theoretical_air_molar(8, 18),
    eq.theoretical_air_molar(8, 18))
chk("12.1 AF mass", m_fuels.afr_molar_to_mass(59.5, 114.22),
    eq.air_fuel_mass_from_molar(59.5, 114.22))
chk("12.1 %theo", m_fuels.percent_theoretical_air(10.78, 9.52),
    eq.percent_theoretical_air(10.78, 9.52))
chk("12.1 %excess", m_fuels.percent_excess_air(89.25, 59.5),
    eq.percent_excess_air(89.25, 59.5))
chk("12.1 phi", m_fuels.equivalence_ratio(89.25, 59.5),
    eq.equivalence_ratio(89.25, 59.5))
chk("12.1 dew point", m_fuels.dew_point_partial_pressure(0.169, 14.696),
    eq.dew_point_partial_pressure(0.169, 14.696))
chk("12.1 Eq13.9", m_fuels.enthalpy(-393520.0, 33405.0),
    eq.enthalpy_formation_plus_dh(-393520.0, 33405.0))
chk("12.1 stream_enthalpy", m_fuels.stream_enthalpy(P_gt), eq.stream_enthalpy(P_gt))
chk("12.1 steady balance", m_fuels.energy_balance_per_mole_fuel(P_gt, R_gt),
    eq.energy_balance_steady(P_gt, R_gt))
chk("12.1 h_RP", m_fuels.enthalpy_of_combustion(
    [(1, -393520.0, 0.0), (2, -285830.0, 0.0)], [(1, -74850.0, 0.0)]), hhv)
chk("12.1 HV molar", m_fuels.heating_value_molar(lhv), eq.heating_value_molar(lhv))
chk("12.1 HV mass", m_fuels.heating_value_mass(hhv, 16.04),
    eq.heating_value_mass(hhv, 16.04))
# 12.2 (ionization) -- Moran trunk
chk("12.2 gibbs_of_reaction", m_ion.gibbs_of_reaction(
    [(1, -393520.0, 213.69)], [(1, -110530.0, 197.54), (0.5, 0.0, 205.03)], 298.0),
    dG298)
chk("12.2 lnK", m_ion.lnK_from_gibbs(dG298, 298.0), eq.lnK_from_gibbs(dG298, 298.0))
chk("12.2 log10K", m_ion.log10K_from_gibbs(dG298, 298.0),
    eq.log10K_from_gibbs(dG298, 298.0))
chk("12.2 log10K inverse", m_ion.log10K_inverse(2.885), eq.log10K_inverse(2.885))
chk("12.2 K composition form", m_ion.equilibrium_constant_from_composition(
    [(0.121, 1.0), (0.061, 0.5)], [(0.818, 1.0)], 1.0),
    eq.equilibrium_constant_composition([(0.121, 1.0), (0.061, 0.5)], [(0.818, 1.0)], 1.0))
r298 = m_ion.equilibrium_constant_CO_oxidation(298)
chk("12.2 Ex14.1 dG0 == EQ", r298["dG0"], dG298)
r2000 = m_ion.equilibrium_constant_CO_oxidation(2000)
chk("12.2 Ex14.1 @2000 == EQ", r2000["dG0"], dG2000)
# 12.2 dissociation extent solves Eq. 14.35: the returned z reproduces K
z22 = m_ion.dissociation_extent_CO2(0.0363, 1.0)
chk("12.2 z -> Eq14.35 K", eq.equilibrium_constant_moles(
    [(z22, 1.0), (z22 / 2.0, 0.5)], [(1.0 - z22, 1.0)], (2.0 + z22) / 2.0, 1.0),
    0.0363, 1e-9)
z22n = m_ion.dissociation_extent_CO2(0.0363, 1.0, n_inert=1.88)          # Ex 14.4
chk("12.2 z(inert) -> Eq14.35 K", eq.equilibrium_constant_moles(
    [(z22n, 1.0), (z22n / 2.0, 0.5)], [(1.0 - z22n, 1.0)],
    (2.0 + 2.0 * 1.88 + z22n) / 2.0, 1.0), 0.0363, 1e-9)
# 12.2 (ionization) -- Saha extension [~PK, NOT Moran]
chk("12.2 n_Q", m_ion.quantum_concentration(300.0), eq.quantum_concentration(300.0),
    1e12)
chk("12.2 saha_rhs", m_ion.saha_rhs(10000.0, 13.6), eq.saha_rhs(10000.0, 13.6), 1e6)
# bridge: Saha x at (T, n) == Moran Eq.-14.35 extent from K = S kB T/pref at the
# plasma's own pressure p = n(1+x) kB T  (exact algebra, so tolerance is float-level)
T_s, n_s = 10000.0, 1.0e23
x12 = m_ion.saha_ionization_fraction(T_s, n_s, 13.6)
K_saha = eq.saha_ionization_K(T_s, 13.6)
p_hat = n_s * (1.0 + x12) * 1.380649e-23 * T_s / 101325.0
chk("~PK Saha == Eq14.35 form", eq.ionization_extent_from_K(K_saha, p_hat), x12, 1e-9)
# 12.EP (worked examples)
e136 = m_ep.ex_13_6()
chk("12.EP Ex13.6 Q == Eq13.17b", e136["Q"],
    eq.energy_balance_closed(P_cv, R_cv, 900.0, 298.0), 1e-6)
e138 = m_ep.ex_13_8()
chk("12.EP Ex13.8 RHS == Eq13.21b", e138["RHS"], rhs, 1e-6)
chk("12.EP Ex13.8 TP == interp", e138["TP_a"],
    eq.interpolate_flame_temperature(rhs, {2350: 4955163.0, 2400: 5089337.0}), 1e-6)
e135 = m_ep.ex_13_5()
chk("12.EP Ex13.5 hP == stream", e135["hP"], eq.stream_enthalpy(P_gt), 1e-6)
e142 = m_ep.ex_14_2()
za = e142["a"]["z"]
chk("12.EP Ex14.2 z -> Eq14.35 K", eq.equilibrium_constant_moles(
    [(za, 1.0), (za / 2.0, 0.5)], [(1.0 - za, 1.0)], (2.0 + za) / 2.0, 1.0),
    e142["K"], 1e-9)

print(f"All {_n} tests passed.")
