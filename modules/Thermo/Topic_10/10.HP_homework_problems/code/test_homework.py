"""
test_homework.py — checks for Module 10.HP.  Run: python3 test_homework.py

Worked answers + balance/consistency closures (Q_C + W = Q_H; eta = W/Q_in;
mep from Eq. 9.1), plus CROSS-CHECKS against the concept modules 10.1
(carnot_engine) and 10.2 (stirling_engine): the Stirling problems must land
on the same ceiling those modules compute.
"""
import math
import os
import sys

from homework import p1, p2, p3, p4, p5, p6, p7, p8

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "10.1_carnot_engine", "code"))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "10.2_stirling_engine", "code"))
import carnot_engine as m_carnot      # noqa: E402
import stirling_engine as m_stirling  # noqa: E402

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# P1 -- CU #24 verdict + impossible inventor upgrade
r = p1()
chk("1 eta_a", r["eta_a"], 0.50)
chk("1 eta_max", r["eta_max"], 0.60)
assert r["verdict_a"] == "irreversible", r["verdict_a"]; _n += 1
chk("1 eta_b", r["eta_b"], 0.70)
assert r["verdict_b"] == "impossible", r["verdict_b"]; _n += 1
# P2 -- Carnot efficiency at Fig. 5.12 point b (CU #23)
r = p2()
chk("2 eta_max ~80%", r["eta_max"], 0.801, 1e-3)
chk("2 matches 10.1", r["eta_max"], m_carnot.carnot_efficiency(298.0, r["T_H"]))
# P3 -- isothermal ideal-gas leg of the Carnot cycle (CU #17)
chk("3 v4", p3()["v4"], 12.6, 1e-9)
# P4 -- maximum work / minimum rejection between 745 K and 298 K
r = p4()
chk("4 eta_max", r["eta_max"], 0.60)
chk("4 W_max", r["W_max"], 600.0)
chk("4 Q_C_min", r["Q_C_min"], 400.0)
chk("4 balance closes", r["Q_C_min"] + r["W_max"], 1000.0)       # Q_C + W = Q_H
chk("4 Q_C_min = Q_H*T_C/T_H", r["Q_C_min"],
    m_carnot.carnot_heat_rejected(1000.0, 298.0, 745.0))         # Eq. 5.7 route agrees
# P5 -- minimum refrigerator power + inventor claim (Ex 5.2 QQ)
r = p5()
chk("5 beta_max", r["beta_max"], 9.926, 1e-3)
chk("5 Wdot_min", r["Wdot_min_kJ_h"], 806.0, 0.05)
chk("5 Wdot_min kW", r["Wdot_min_kW"], 0.2239, 1e-4)
chk("5 claimed beta", r["beta_claim"], 10.0)
assert not r["claim_valid"], "800 kJ/h claim must fail the second law"; _n += 1
chk("5 matches 10.1", r["beta_max"], m_carnot.carnot_cop_refrigerator(268.0, 295.0))
# P6 -- Problem 9.102: air Stirling cycle, r = 6
r = p6()
chk("6 T_C", r["T_C"], 290.36, 0.01)
chk("6 Q_34", r["Q_34"], 18.51, 0.005)
chk("6 Q_12", r["Q_12"], 5.375, 0.005)
chk("6 W_net", r["W_net"], 13.14, 0.005)
chk("6 eta", r["eta"], 0.710, 5e-4)
chk("6 mep", r["mep_bar"], 5.25, 0.005)
chk("6 eta = W/Q_34 closes", r["eta"], r["eta_from_heats"], 1e-12)
chk("6 balance closes", r["Q_12"] + r["W_net"], r["Q_34"], 1e-12)   # Q_C + W = Q_H
chk("6 matches 10.2", r["eta"], m_stirling.stirling_efficiency(r["T_C"], 1000.0), 1e-12)
chk("6 W matches 10.2 (per kg x m)", r["W_net"],
    0.036 * m_stirling.stirling_net_work(0.287, 1000.0, r["T_C"], 6.0), 1e-9)
# P7 -- the regenerator's worth (9.102 continued)
r = p7()
chk("7 Q_regen", r["Q_regen"], 18.34, 0.005)
chk("7 eta ideal", r["eta_full"], 0.710, 5e-4)
chk("7 eta 80%", r["eta_80"], 0.592, 5e-4)
chk("7 eta none", r["eta_none"], 0.356, 5e-4)
assert r["eta_none"] < r["eta_80"] < r["eta_full"], "regeneration must help monotonically"; _n += 1
chk("7 matches 10.2 no-regen (per-mass)", r["eta_none"],
    m_stirling.stirling_efficiency_no_regen(0.287, 0.718, 1000.0, p6()["T_C"], 6.0), 1e-12)
# P8 -- Problem 9.103: helium Stirling cycle + Stirling-vs-Carnot
r = p8()
chk("8 R helium", r["R"], 0.4961, 1e-4)
chk("8 W_12", r["W_12"], -639.4, 0.1)
chk("8 W_34", r["W_34"], 2238.7, 0.1)
chk("8 Q_23 (regen)", r["Q_23"], 1041.9, 0.1)
chk("8 regen legs cancel", r["Q_23"] + r["Q_41"], 0.0, 1e-12)
chk("8 W_net", r["W_net"], 1599.3, 0.1)
chk("8 eta", r["eta"], 0.7144, 1e-4)
chk("8 Stirling = Carnot (10.1)", r["eta"],
    m_carnot.carnot_efficiency(r["T_C"], r["T_H"]), 1e-12)
chk("8 Stirling = Carnot (10.2)", r["eta"],
    m_stirling.stirling_efficiency(r["T_C"], r["T_H"]), 1e-12)
chk("8 isothermal legs match 10.2", r["W_34"],
    m_stirling.isothermal_heat(r["R"], r["T_H"], 10.0), 1e-9)

print(f"All {_n} tests passed.")
