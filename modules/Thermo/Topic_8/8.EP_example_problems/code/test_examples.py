"""
test_examples.py  —  checks for Module 8.EP.

Each assertion regenerates a Moran 8e worked Example from its GIVEN data and
matches the book's published ANSWER (tolerances absorb the book's rounding).

Run:  cd code && python3 test_examples.py   ->  "All N tests passed."
"""
import examples as ex

_n = 0


def chk(name, got, want, tol):
    global _n
    assert abs(got - want) <= tol, f"{name}: got {got!r}, want book {want!r} (tol {tol})"
    _n += 1


# Example 4.5 — air compressor power
e = ex.ex_4_5()
chk("4.5 mdot", e["mdot"], 0.72, tol=0.005)
chk("4.5 Wcv (kW)", e["W_kW"], -119.4, tol=0.05)
chk("4.5 power input (kW)", e["power_input_kW"], 119.4, tol=0.05)
chk("4.5 QQ no-KE (kW)", e["W_noKE_kW"], -119.4, tol=0.05)     # KE term negligible

# Example 4.7 — power-plant condenser (two-stream and steam-side views)
e = ex.ex_4_7()
chk("4.7 h1", e["h1"], 2465.1, tol=0.05)
chk("4.7 ratio", e["ratio"], 36.3, tol=0.05)
chk("4.7 q per kg", e["q_per_kg"], -2276.7, tol=0.1)
chk("4.7 QQ water flow", e["mdot_w"], 4538.0, tol=1.0)
chk("4.7 balance residual", e["residual"], 0.0, tol=1e-9)

# Example 4.8 — computer cooling, smallest fan inlet area
e = ex.ex_4_8()
chk("4.8 A1 (cm^2)", e["A1_cm2"], 52.0, tol=0.3)
chk("4.8 mdot closure", e["mdot_back"], e["mdot"], tol=1e-12)

# Example 6.14 — isentropic compressor efficiency (R-22)
e = ex.ex_6_14()
chk("6.14 Wcv (kW)", e["W_kW"], -3.11, tol=0.005)
chk("6.14 eta_c", e["eta_c"], 0.81, tol=0.005)
chk("6.14 QQ min work", e["w_min"], 35.83, tol=1e-9)

# Example 10.1 — ideal vapor-compression refrigeration cycle
e = ex.ex_10_1()
chk("10.1 Wc (kW)", e["Wc_kW"], 1.4, tol=0.005)
chk("10.1 capacity (ton)", e["cap_ton"], 3.67, tol=0.01)
chk("10.1 beta", e["beta"], 9.24, tol=0.01)
chk("10.1 beta_max", e["beta_max"], 10.5, tol=0.005)
chk("10.1 QQ mdot 10 ton", e["mdot_10ton"], 0.218, tol=0.001)
assert e["beta"] < e["beta_max"]; _n += 1                      # ideal cycle < Carnot

# Example 10.2 — irreversible heat transfer (evaporator -10 C, condenser 9 bar)
e = ex.ex_10_2()
chk("10.2 Wc (kW)", e["Wc_kW"], 2.48, tol=0.005)
chk("10.2 capacity (ton)", e["cap_ton"], 3.23, tol=0.01)
chk("10.2 beta", e["beta"], 4.57, tol=0.01)
chk("10.2 QQ condenser (kW)", e["Qout_kW"], 13.83, tol=0.005)

# Example 10.3 — actual cycle: eta_c = 80%, subcooled condenser exit
e = ex.ex_10_3()
chk("10.3 h2", e["h2"], 280.15, tol=0.005)
chk("10.3 Wc (kW)", e["Wc_kW"], 3.1, tol=0.005)
chk("10.3 capacity (ton)", e["cap_ton"], 3.41, tol=0.005)
chk("10.3 beta", e["beta"], 3.86, tol=0.005)
chk("10.3 Ed compressor (kW)", e["Ed_c_kW"], 0.58, tol=0.005)
chk("10.3 Ed valve (kW)", e["Ed_valve_kW"], 0.39, tol=0.01)
chk("10.3 x4", e["x4"], 0.2667, tol=0.0005)

# Example 10.4 — actual vapor-compression heat pump
e = ex.ex_10_4()
chk("10.4 Wc (kW)", e["Wc_kW"], 7.53, tol=0.005)
chk("10.4 eta_c", e["eta_c"], 0.84, tol=0.005)
chk("10.4 Qout (kW)", e["Qout_kW"], 34.98, tol=0.005)
chk("10.4 gamma", e["gamma"], 4.65, tol=0.01)
chk("10.4 cost ($)", e["cost_usd"], 90.36, tol=0.01)
chk("10.4 QQ cost ($)", e["cost_qq_usd"], 60.24, tol=0.01)
chk("10.4 first law Qout = Qin + Wc", e["first_law"], e["Qout_kW"], 1e-9)
chk("10.4 Qin (kW)", e["Qin_kW"], 27.45, tol=0.005)

print(f"All {_n} tests passed.")
