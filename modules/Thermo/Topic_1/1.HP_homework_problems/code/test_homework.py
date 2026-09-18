"""
test_homework.py  —  checks for Module 1.HP.

These are *worked solutions* (Moran gives no answer key), so the tests pin the
computed answers for reproducibility and add independent consistency checks where
a governing balance lets one be made.

Run:  cd code && python3 test_homework.py   ->  "All N tests passed."
"""
import math
import homework as h

_n = 0


def chk(name, got, want, tol):
    global _n
    assert abs(got - want) <= tol, f"{name}: got {got!r}, want {want!r} (tol {tol})"
    _n += 1


# ---- Chapter 1 -------------------------------------------------------------
chk("1.8 Mars", h.p1_8()["W_mars_N"], 1305.5, 0.1)
chk("1.8 Earth", h.p1_8()["W_earth_N"], 3433.5, 0.1)
chk("1.13 g", h.p1_13()["g_a_ft_s2"], 31.91, 0.02)
chk("1.20 W", h.p1_20()["W_N"], 83.53, 0.05)
chk("1.20 v_mass", h.p1_20()["v_mass"], 0.7046, 1e-3)
chk("1.21 rho", h.p1_21()["rho_lb_ft3"], 55.21, 0.05)
chk("1.23 V", h.p1_23()["V_m3"], 1.08, 1e-6)
chk("1.23 molecules(e26)", h.p1_23()["molecules"] / 1e26, 1.671, 1e-3)
chk("1.33 p_gas", h.p1_33()["p_gas_kPa"], 234.3, 0.1)
chk("1.35 L_mm", h.p1_35()["L_mm"], 750.1, 0.1)
chk("1.36 dp", h.p1_36()["dp_kPa"], 0.965, 0.005)
chk("1.38 p", h.p1_38()["p_atm"], 30.49, 0.02)
chk("1.40 p_exit", h.p1_40()["p_exit_psia"], 160.0, 1e-6)
chk("1.42 piston", h.p1_42()["m_piston_kg"], 24.02, 0.02)
chk("1.42 added", h.p1_42()["m_added_kg"], 32.02, 0.02)
chk("1.50 summer_F", h.p1_50()["summer_F"], 67.1, 0.05)
chk("1.51 86F->C", h.p1_51()["86F"][0], 30.0, 1e-9)
chk("1.51 -459.67F->K", h.p1_51()["-459.67F"][1], 0.0, 1e-9)   # absolute zero

# ---- Chapter 2 -------------------------------------------------------------
chk("2.5 z", h.p2_5()["z_high_ft"], 12186.5, 0.5)
chk("2.6 dKE", h.p2_6()["dKE_kJ"], -4800.0, 1e-6)
chk("2.7 dKE", h.p2_7()["dKE_kJ"], 207623.0, 1.0)
chk("2.7 dPE", h.p2_7()["dPE_kJ"], 1369200.0, 1.0)
chk("2.26 V2", h.p2_26()["V2_m3"], 0.03333, 1e-4)
chk("2.26 W", h.p2_26()["W_kJ"], -20.0, 1e-6)
chk("2.28 n=0 W", h.p2_28()["n0.0"]["W_kJ"], -12.0, 1e-6)
chk("2.28 n=1 W", h.p2_28()["n1.0"]["W_kJ"], -7.33, 0.01)
chk("2.28 n=1.3 W", h.p2_28()["n1.3"]["W_kJ"], -6.41, 0.01)
chk("2.31 n", h.p2_31()["n"], 1.370, 0.001)
chk("2.31 W", h.p2_31()["W_Btu"], 724.4, 0.5)
chk("2.39 cost", h.p2_39()["cost_usd"], 2.534, 0.005)
chk("2.58 Q", h.p2_58()["Q_kJ"], -50.0, 0.02)
chk("2.59 Q", h.p2_59()["Q_gas_kJ"], 4.25, 1e-6)
chk("2.62 P_shaft", h.p2_62()["P_shaft_kW"], 1.016, 0.002)
chk("2.62 Ts", h.p2_62()["Ts_C"], 42.6, 0.1)
chk("2.71 du", h.p2_71()["du_kJ_kg"], -310.6, 0.1)
chk("2.90 COP", h.p2_90()["COP"], 3.0, 1e-9)

# ---- independent consistency checks ---------------------------------------
# 2.59: energy balance must close, Q = dU + W
chk("2.59 balance", h.p2_59()["Q_gas_kJ"] - (0.25 + h.p2_59()["W_gas_kJ"]), 0.0, 1e-9)
# 2.90: refrigerator overall energy balance, Q_out = Q_in + W
chk("2.90 balance", (h.p2_90()["Qdot_in_kW"] + 0.15) - 0.6, 0.0, 1e-9)
# 1.13: recomputing weight from m_b and g_b must match
chk("1.13 W_b consistency", h.p1_13()["W_b_lbf"], 120.0 * 32.05 / 32.174, 1e-6)

print(f"All {_n} tests passed.")
