"""test_examples.py — checks for Module 12.EP (Moran Ch.13 & 14 worked Examples).
Run: python3 test_examples.py.  Each value checked against Moran's published answer."""
import math
from examples import (ex_13_1, ex_13_2, ex_13_4, ex_13_5, ex_13_6, ex_13_7, ex_13_8,
                     ex_14_1, ex_14_2)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# ===== Ex 13.1 octane AFR =====
e = ex_13_1()
chk("13.1 a_O2", e["aO2"], 12.5)
chk("13.1 AF_bar theo", e["AFbar"], 59.5)
chk("13.1 AF theo", e["AF"], 15.1, 0.05)
chk("13.1 AF_bar 150%", e["AFbar_b"], 89.25)
chk("13.1 AF 150%", e["AF_b"], 22.6, 0.05)
chk("13.1 phi 150%", e["phi_b"], 0.67, 5e-3)

# ===== Ex 13.2 methane dry analysis & dew point =====
e = ex_13_2()
chk("13.2 a", e["a"], 10.2)
chk("13.2 b", e["b"], 23.1)
chk("13.2 c", e["c"], 20.4)
chk("13.2 AF_bar", e["AFbar"], 10.78, 0.005)
chk("13.2 AF mass", e["AF"], 19.47, 0.01)
chk("13.2 %theo", e["pct_theo"], 1.13, 5e-3)
chk("13.2 y_v", e["yv"], 0.169, 5e-4)
chk("13.2 p_v psi", e["pv_psi"], 2.484, 0.01)
chk("13.2 vapor @90F", e["n_vapor"], 0.489, 5e-4)

# ===== Ex 13.4 IC engine heat transfer =====
e = ex_13_4()
chk("13.4 hR", e["hR"], -107530.0)
chk("13.4 hP", e["hP"], -1752251.0, 2.0)                # book -1,752,251 Btu/lbmol
chk("13.4 nF", e["nF"], 3.5e-5, 1e-7)
chk("13.4 Qcv", e["Qcv"], -22.22, 0.02)                # book -22.22 Btu/s
assert e["Qcv"] < 0.0;  _n += 1                         # heat rejected from engine

# ===== Ex 13.5 gas turbine net power =====
e = ex_13_5()
chk("13.5 hP", e["hP"], -359475.0, 1.0)                # book -359,475 kJ/kmol
chk("13.5 Wnet (MW)", e["Wcv_MW"], 5.74, 0.01)         # book 5.74 MW
assert e["Wcv_MW"] > 0.0;  _n += 1                      # power out of the plant

# ===== Ex 13.6 closed vessel =====
e = ex_13_6()
chk("13.6 Q", e["Q"], -745436.0, 60.0)                 # book -745,436 kJ
chk("13.6 p2", e["p2"], 3.02, 0.005)                   # book 3.02 atm

# ===== Ex 13.7 enthalpy of combustion / heating values =====
e = ex_13_7()
chk("13.7a HHV molar", e["hRP_a"], -890330.0)          # book -890,330 kJ/kmol
chk("13.7a HHV /kg", e["hRP_a_kg"], -55507.0, 1.0)     # book -55,507 kJ/kg
chk("13.7b LHV molar", e["hRP_b"], -802310.0)          # book -802,310 kJ/kmol
chk("13.7b LHV /kg", e["hRP_b_kg"], -50019.0, 1.0)     # book -50,019 kJ/kg
chk("13.7c @1000K molar", e["hRP_c"], -800552.0)       # book -800,552 kJ/kmol
chk("13.7c @1000K /kg", e["hRP_c_kg"], -49910.0, 1.0)  # book -49,910 kJ/kg

# ===== Ex 13.8 adiabatic flame temperature =====
e = ex_13_8()
chk("13.8 RHS", e["RHS"], 5074630.0, 1.0)              # book 5,074,630 kJ/kmol fuel
chk("13.8a TP (theo air)", e["TP_a"], 2395.0, 1.0)     # book ~2395 K (IT 2394)
chk("13.8b TP (400% air)", e["TP_b"], 962.0)           # book 962 K
assert e["TP_a"] > e["TP_b"];  _n += 1                  # excess air dilutes/cools products

# ===== Ex 14.1 equilibrium constant =====
e = ex_14_1()
chk("14.1 dG 298K", e["dG298"], -257253.0, 60.0)       # book -257,253 kJ/kmol
chk("14.1 lnK 298K", e["lnK298"], 103.83, 0.02)        # book 103.83
chk("14.1 log10K 298K", e["log10K298"], 45.093, 0.02)  # book 45.093
chk("14.1 dG 2000K", e["dG2000"], -110453.0, 60.0)     # book -110,453 kJ/kmol
chk("14.1 lnK 2000K", e["lnK2000"], 6.643, 0.01)       # book 6.643
chk("14.1 log10K 2000K", e["log10K2000"], 2.885, 0.01) # book 2.885

# ===== Ex 14.2 CO2 dissociation composition =====
e = ex_14_2()
chk("14.2 K", e["K"], 0.0363, 5e-4)                    # 10^-1.44
chk("14.2a z (1 atm)", e["a"]["z"], 0.129, 1e-3)       # book 0.129
chk("14.2a yCO", e["a"]["yCO"], 0.121, 2e-3)           # book 0.121
chk("14.2a yO2", e["a"]["yO2"], 0.061, 2e-3)           # book 0.061
chk("14.2a yCO2", e["a"]["yCO2"], 0.818, 2e-3)         # book 0.818
chk("14.2b z (10 atm)", e["b"]["z"], 0.062, 2e-3)      # book 0.062
chk("14.2b yCO2", e["b"]["yCO2"], 0.91, 5e-3)          # book 0.91
assert e["b"]["z"] < e["a"]["z"];  _n += 1             # higher p suppresses dissociation

print(f"All {_n} tests passed.")
