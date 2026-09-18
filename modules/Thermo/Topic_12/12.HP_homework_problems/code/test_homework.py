"""test_homework.py — checks for Module 12.HP (Moran Ch.13/14 problems + ~PK Saha leaf).
Run: python3 test_homework.py.  Moran has no answer key; these are worked solutions with
consistency checks (element balances close, mole fractions sum to 1, K round-trips, dew
points inside their steam-table bracket, Saha == Moran Eq.-14.35 form).  Cross-checks
import the concept modules 12.1 (fuels) and 12.2 (ionization)."""
import math
import os
import sys

from homework import p1, p2, p3, p4, p5, p6, p7, p8, p9, theoretical_O2

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "12.1_fuels", "code"))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "12.2_ionization", "code"))
import fuels as m_fuels      # noqa: E402
import ionization as m_ion   # noqa: E402

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# P1 -- ethane, theoretical air (13.2)
r = p1()
chk("1 a_O2", r["aO2"], 3.5)
chk("1 AF_bar", r["AFbar"], 16.66)
chk("1 AF mass", r["AF"], 16.05, 0.01)
chk("1 == 12.1 theoretical_air", r["AFbar"], m_fuels.theoretical_air_molar(2, 6))
chk("1 == 12.1 afr mass", r["AF"], m_fuels.afr_molar_to_mass(16.66, 30.07))

# P2 -- butane, phi = 0.9 (13.7)
r = p2()
chk("2 O2 supplied", r["O2_supplied"], 7.2222, 1e-4)
chk("2 free O2", r["free_O2"], 0.7222, 1e-4)
chk("2 N2", r["N2"], 27.156, 1e-3)
chk("2 % excess", r["excess"], 1.0 / 9.0, 1e-9)             # 11.1%
chk("2 O balance closes", r["O_balance"], 0.0, 1e-12)
chk("2 phi recovered (12.1)", m_fuels.equivalence_ratio(
    4.76 * r["O2_supplied"], 4.76 * r["aO2"]), 0.9, 1e-12)

# P3 -- hexane dry-product back-out (13.30)
r = p3()
chk("3 a (kmol fuel)", r["a"], 2.2833, 1e-4)
chk("3 c (kmol H2O)", r["c"], 15.983, 1e-3)
chk("3 b (kmol O2)", r["b"], 22.092, 1e-3)
chk("3 C balance", 6.0 * r["a"], 8.5 + 5.2, 1e-12)
chk("3 H balance", 14.0 * r["a"], 2.0 * r["c"], 1e-12)
chk("3 O balance", 2.0 * r["b"], 2 * 8.5 + 5.2 + 2 * 3.0 + r["c"], 1e-12)
assert abs(r["n2_check"] - 83.3) < 0.35;  _n += 1           # reported dry N2 closes to 0.3%
chk("3 % theo air", r["pct_theo"], 1.018, 1e-3)             # ~102%
chk("3 == 12.1 %theo", r["pct_theo"],
    m_fuels.percent_theoretical_air(r["b"] / r["a"], theoretical_O2(6, 14)))
chk("3 y_v", r["yv"], 0.1378, 1e-4)
chk("3 == 12.1 y_v", r["yv"], m_fuels.water_vapor_mole_fraction(r["c"], 100.0))
chk("3 dew point (C)", r["T_dew_C"], 52.4, 0.1)
assert 50.0 <= r["T_dew_C"] <= 55.0;  _n += 1               # inside the A-2 bracket

# P4 -- dodecane, 150% theoretical air (13.17)
r = p4()
chk("4 AF_bar", r["AFbar"], 132.09, 0.01)
chk("4 AF mass", r["AF"], 22.47, 0.01)
chk("4 products total", r["n_prod"], 138.59, 0.01)
chk("4 y sums to 1", (12.0 + 13.0 + 9.25 + 104.34) / r["n_prod"], 1.0, 1e-4)
chk("4 y_v", r["yv"], 0.0938, 1e-4)
chk("4 dew point (C)", r["T_dew_C"], 44.8, 0.1)
chk("4 50% excess (12.1)", m_fuels.percent_excess_air(r["AFbar"], 4.76 * r["aO2"]), 0.5, 1e-12)

# P5 -- pentane enthalpy of combustion / heating values (13.59)
r = p5()
chk("5 h_RP vapor", r["hRP_vapor"], -3272080.0)
chk("5 LHV mass vs A-25", r["LHV_mass"], 45350.0, 2.0)      # Table A-25: 45,350 kJ/kg
chk("5 h_RP liquid", r["hRP_liquid"], -3536140.0)
chk("5 HHV mass vs A-25", r["HHV_mass"], 49010.0, 2.0)      # Table A-25: 49,010 kJ/kg
chk("5 HHV-LHV = latent term", r["hRP_liquid"] - r["hRP_vapor"],
    6.0 * (-285830.0 + 241820.0), 1e-9)                     # 6 kmol water condensed
chk("5 == 12.1 h_RP", r["hRP_vapor"], m_fuels.enthalpy_of_combustion(
    [(5, -393520.0, 0.0), (6, -241820.0, 0.0)], [(1, -146440.0, 0.0)]))
assert r["HHV_mass"] > r["LHV_mass"];  _n += 1

# P6 -- adiabatic flame temperature, liquid propane (13.51)
r = p6()
chk("6 RHS", r["RHS"], 2028940.0)
assert r["sum_a"][2350] < r["RHS"] < r["sum_a"][2400];  _n += 1   # (a) bracketed
assert r["sum_b"][1140] < r["RHS"] < r["sum_b"][1160];  _n += 1   # (b) bracketed
chk("6a T (theo air)", r["T_a"], 2381.0, 1.0)               # worked: 2380.5 K
chk("6b T (300% air)", r["T_b"], 1152.0, 1.0)               # worked: 1151.7 K
assert r["T_a"] > r["T_b"];  _n += 1                        # excess air dilutes/cools
assert abs(r["T_a"] - 2395.0) < 20.0;  _n += 1              # ~ Ex 13.8 octane value

# P7 -- closed-vessel equilibrium, final pressure (14.32)
r = p7()
chk("7 K (A-27 @2500K)", r["K"], 0.0363, 5e-5)
chk("7 z", r["z"], 0.0741, 2e-4)
chk("7 p2 (atm)", r["p2_atm"], 5.76, 0.01)
chk("7 y sums to 1", sum(r["y"].values()), 1.0, 1e-12)
chk("7 K round trip (Eq. 14.35)",
    (r["z"] / (1 - r["z"])) * math.sqrt(r["z"] / (2 + r["z"])) * math.sqrt(r["p2_atm"]),
    r["K"], 1e-9)
chk("7 ideal gas p2", r["p2_atm"], 1.0 * (r["n2"] / 1.5) * (2500.0 / 300.0), 1e-12)
assert r["z"] < 0.129;  _n += 1                             # self-pressurization suppresses
chk("7 == 12.2 extent at fixed p2", r["z"],
    m_ion.dissociation_extent_CO2(r["K"], r["p2_atm"]), 1e-6)

# P8 -- N ionization-equilibrium constant (14.67)
r = p8()
chk("8 z", r["z"], 0.05)
chk("8 K", r["K"], 0.01504, 1e-5)
chk("8 log10K", r["log10K"], -1.823, 1e-3)
chk("8 z-form identical", r["K"], r["K_zform"], 1e-15)

# P9 -- [~PK, NOT Moran] Saha ionization of hydrogen; no book key
r = p9()
xs = [r["x"][T] for T in (8000.0, 12000.0, 16000.0)]
assert all(0.0 < x < 1.0 for x in xs);  _n += 1
assert xs[0] < xs[1] < xs[2];  _n += 1                      # hotter -> more ionized
chk("9 x @12,000 K (worked)", xs[1], 0.2194, 1e-3)
chk("9 == 12.2 saha fraction", xs[1],
    m_ion.saha_ionization_fraction(12000.0, 1.0e23, 13.6), 1e-12)
chk("9 K_moran (worked)", r["K_moran_12000K"], 0.01008, 1e-4)
chk("9 Saha == Eq.14.35 form", r["x_from_K"], xs[1], 1e-9)  # exact algebraic identity
# denser plasma is less ionized (recombination), via 12.2
assert m_ion.saha_ionization_fraction(12000.0, 1.0e25, 13.6) < xs[1];  _n += 1

print(f"All {_n} tests passed.")
