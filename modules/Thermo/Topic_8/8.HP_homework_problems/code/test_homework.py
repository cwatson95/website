"""test_homework.py — checks for Module 8.HP.  Run: python3 test_homework.py
Worked answers + consistency conditions (balances close, w_s is the minimum,
COPs below the Carnot ceiling)."""
import math
from homework import p1, p2, p3, p4, p5, p6, p7, p8

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# P1 -- mass flow, two forms
r = p1()
chk("1 v", r["v"], 0.832, 1e-3)
chk("1 mdot", r["mdot_ig"], 0.72, 0.005)
chk("1 forms agree", r["mdot_v"], r["mdot_ig"], 1e-12)          # AV/v == AVp/RT
# P2 -- compressor power with heat loss (Ex 4.5 data)
r = p2()
chk("2 W", r["W_kW"], -119.4, 0.05)
chk("2 input", r["input_kW"], 119.4, 0.05)
assert abs(r["KE_kW"]) < 0.05; _n += 1                          # KE term negligible
chk("2 no-KE still -119.4", r["W_noKE_kW"], -119.4, 0.05)
# P3 -- adiabatic compressor + isentropic efficiency (Ex 6.14 data)
r = p3()
chk("3 W", r["W_kW"], -3.11, 0.005)
chk("3 eta_c", r["eta_c"], 0.81, 0.005)
assert r["w_min"] <= r["w_actual"]; _n += 1                     # isentropic = minimum
assert 0.0 < r["eta_c"] <= 1.0; _n += 1
# P4 -- exit state from eta_c (Ex 10.3 compressor)
r = p4()
chk("4 h2", r["h2"], 280.15, 0.005)
chk("4 w_actual", r["w_actual"], 38.80, 0.005)
chk("4 eta round-trip", r["eta_back"], 0.80, 1e-12)             # Eq. 6.48 inverts cleanly
# P5 -- condenser steam side (Ex 4.7 data)
r = p5()
chk("5 h_in", r["h_in"], 2465.1, 0.05)
chk("5 q", r["q"], -2276.7, 0.1)
chk("5 Q (MW)", r["Q_MW"], -284.6, 0.05)
assert r["hf"] <= r["h_in"] <= r["hg"]; _n += 1                 # two-phase inlet in the dome
assert r["q"] < 0.0; _n += 1                                    # heat leaves the steam
# P6 -- heat-exchanger mass-flow ratio (Ex 4.7 two-stream view)
r = p6()
chk("6 ratio", r["ratio"], 36.3, 0.05)
chk("6 water flow", r["mdot_c"], 4538.0, 1.0)
chk("6 balance closes", r["residual"], 0.0, 1e-9)               # Eq. 4.18 residual ~ 0
# P7 -- heat-exchanger exit state (constant cp)
r = p7()
chk("7 duty", r["duty_kW"], 804.0, 1e-9)
chk("7 T_out", r["T_co"], 44.04, 0.005)
chk("7 balance closes", r["residual"], 0.0, 1e-9)
assert r["T_co"] < 500.0 - 273.15; _n += 1                      # water exit (44 C) < hot inlet (227 C)
# P8 -- heat-pump COP + Carnot ceiling (Ex 10.4 cycle)
r = p8()
chk("8 W", r["W_kW"], 7.53, 0.005)
chk("8 Q_out", r["Q_out_kW"], 34.98, 0.005)
chk("8 gamma", r["gamma"], 4.65, 0.01)
chk("8 gamma_max", r["gamma_max"], 17.35, 0.01)
chk("8 first law closes", r["Q_in_kW"] + r["W_kW"], r["Q_out_kW"], 1e-9)   # Q_C + W = Q_H
chk("8 gamma = beta + 1", r["gamma"], r["beta"] + 1.0, 1e-12)
assert r["gamma"] < r["gamma_max"]; _n += 1                     # below the Carnot ceiling
assert r["gamma"] > 1.0; _n += 1                                # heat-pump COP >= 1

print(f"All {_n} tests passed.")
