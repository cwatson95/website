"""test_fuels.py — checks for Module 12.1.  Run: python3 test_fuels.py
Anchored to Moran 8e Examples 13.1, 13.2, 13.7 (book numbers)."""
import math
from fuels import (theoretical_O2, theoretical_air_molar, afr_molar_to_mass,
                   afr_mass_to_molar, fuel_air_ratio, percent_theoretical_air,
                   percent_excess_air, equivalence_ratio, O2_supplied, mole_fraction,
                   water_vapor_mole_fraction, dew_point_partial_pressure,
                   vapor_remaining_on_cooling, enthalpy, stream_enthalpy,
                   enthalpy_of_combustion, heating_value_molar, heating_value_mass,
                   energy_balance_per_mole_fuel)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# --- stoichiometry: octane (Ex 13.1) ---
chk("octane a_O2", theoretical_O2(8, 18), 12.5)
chk("octane AF_bar theo", theoretical_air_molar(8, 18), 59.5)
chk("octane AF mass theo", afr_molar_to_mass(59.5, 114.22), 15.1, 0.05)        # book 15.1
chk("methane a_O2", theoretical_O2(1, 4), 2.0)
chk("methane AF_bar theo", theoretical_air_molar(1, 4), 9.52)                    # book 9.52
# 150% theoretical air (Ex 13.1b)
chk("octane AF_bar 150%", 1.5 * 59.5, 89.25)                                     # book 89.25
chk("octane AF mass 150%", afr_molar_to_mass(89.25, 114.22), 22.6, 0.05)        # book 22.6
chk("octane phi 150%", equivalence_ratio(89.25, 59.5), 0.67, 5e-3)              # book 0.67
# round trips & ratios
chk("afr round trip", afr_mass_to_molar(afr_molar_to_mass(59.5, 114.22), 114.22), 59.5)
chk("fuel-air ratio", fuel_air_ratio(15.1), 1.0 / 15.1)
chk("excess air 50%", percent_excess_air(89.25, 59.5), 0.5)
chk("O2 supplied 400%", O2_supplied(2.0, 4.0), 8.0)                              # Ex 13.5: 8 O2

# --- dry product analysis & dew point: methane (Ex 13.2) ---
chk("Ex13.2 %theo air", percent_theoretical_air(10.78, 9.52), 1.13, 5e-3)       # 113%
chk("Ex13.2 AF mass", afr_molar_to_mass(10.78, 16.04), 19.47, 0.01)            # book 19.47
chk("Ex13.2 y_v", water_vapor_mole_fraction(20.4, 100.0), 0.169, 5e-4)         # book 0.169
chk("Ex13.2 p_v (atm)", dew_point_partial_pressure(0.169, 1.0), 0.169, 1e-9)
chk("Ex13.2 vapor at 90F", vapor_remaining_on_cooling(0.6988, 14.696, 9.8), 0.489, 5e-4)  # book 0.489
chk("mole fraction", mole_fraction(20.4, 120.4), 20.4 / 120.4)

# --- enthalpy of combustion / heating values: methane (Ex 13.7) ---
chk("enthalpy h=hf+dh", enthalpy(-393520, 33405), -393520 + 33405)
P_liq = [(1, -393520, 0.0), (2, -285830, 0.0)]
P_vap = [(1, -393520, 0.0), (2, -241820, 0.0)]
R_ch4 = [(1, -74850, 0.0)]                                   # CH4(g); O2 h_f0 = 0 -> omitted
hhv = enthalpy_of_combustion(P_liq, R_ch4)
lhv = enthalpy_of_combustion(P_vap, R_ch4)
chk("Ex13.7 HHV molar", hhv, -890330.0)                      # book -890,330 kJ/kmol
chk("Ex13.7 HHV mass", heating_value_mass(hhv, 16.04), 55507.0, 1.0)         # book 55,507
chk("Ex13.7 LHV molar", lhv, -802310.0)                      # book -802,310 kJ/kmol
chk("Ex13.7 LHV mass", heating_value_mass(lhv, 16.04), 50019.0, 1.0)         # book 50,019
chk("heating value magnitude", heating_value_molar(lhv), 802310.0)
# Ex 13.7(c): h_RP at 1000 K, water vapor in products  (dh from Table A-23 / cp-fit)
P_1000 = [(1, -393520, 33405), (2, -241820, 25978)]          # CO2, H2O(g) at 1000 K
R_1000 = [(1, -74850, 38189), (2, 0.0, 22707)]               # CH4(g), 2 O2 at 1000 K
chk("Ex13.7c h_RP @1000K", enthalpy_of_combustion(P_1000, R_1000), -800552.0, 1.0)  # book -800,552
chk("Ex13.7c h_RP @1000K /kg", heating_value_mass(enthalpy_of_combustion(P_1000, R_1000), 16.04),
    49910.0, 1.0)                                            # book -49,910 kJ/kg

# --- steady-flow energy balance shape (Ex 13.5 gas turbine, methane 400% air) ---
# hP - hR with the exact dh terms Moran quotes -> book hP = -359,475, hR = -74,850
P_gt = [(1, -393520, 28622 - 9364), (2, -241820, 25218 - 9904),
        (6, 0.0, 22177 - 8682), (30.08, 0.0, 21529 - 8669)]
R_gt = [(1, -74850, 0.0)]                                    # 8 O2 + 30.08 N2 enter at 25 C
chk("Ex13.5 hP", stream_enthalpy(P_gt), -359475.0, 1.0)      # book -359,475 kJ/kmol fuel
chk("Ex13.5 hR", stream_enthalpy(R_gt), -74850.0)
chk("Ex13.5 hP-hR", energy_balance_per_mole_fuel(P_gt, R_gt), -359475.0 - (-74850.0), 1.0)

print(f"All {_n} tests passed.")
