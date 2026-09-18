"""test_homework.py — checks for Module 9.HP.  Run: python3 test_homework.py

Worked answers plus consistency closures: energy balance q_in - q_out = w_net for each
cycle, eta below the Carnot ceiling at the same temperature extremes, bwr in the
characteristic band (gas turbine large, vapor plant tiny), mep positive.
"""
import math
from homework import p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# P1 -- Carnot ceiling verdicts
r = p1()
chk("1 eta_max", r["eta_max"], 0.7857, 1e-4)
assert r["verdict_075"] == "irreversible", r; _n += 1
assert r["verdict_080"] == "impossible", r;  _n += 1

# P2 -- Otto cycle, cold air-standard
r = p2()
chk("2 T2", r["T2"], 738.3, 0.1)
chk("2 T4", r["T4"], 812.7, 0.1)
chk("2 eta", r["eta"], 0.5936, 1e-4)
chk("2 w_net", r["w_net"], 537.8, 0.1)
chk("2 mep", r["mep_kPa"], 698.0, 0.5)
chk("2 balance closes", r["q_in"] - r["q_out"], r["w_net"], 1e-9)
chk("2 eta = w/q_in", r["w_net"] / r["q_in"], r["eta"], 1e-12)   # Eq. 9.8 == balance
assert r["eta"] < r["eta_carnot"];  _n += 1                       # 0.594 < 0.85
assert r["mep_kPa"] > 0;            _n += 1

# P3 -- compression ratio for a target efficiency
r = p3()
chk("3 r", r["r"], 9.882, 0.001)
chk("3 round-trip", r["eta_check"], 0.60, 1e-12)

# P4 -- Diesel cycle, cold air-standard
r = p4()
chk("4 T2", r["T2"], 939.7, 0.1)
chk("4 T3", r["T3"], 2349.4, 0.1)
chk("4 T4", r["T4"], 1118.1, 0.1)
chk("4 eta", r["eta"], 0.5905, 1e-4)
chk("4 balance -> eta", r["w_net"] / r["q_in"], r["eta"], 1e-12)  # Eq. 9.13 == balance
assert r["eta"] < r["eta_carnot"];  _n += 1                       # 0.59 < 0.868

# P5 -- cutoff-ratio effect at fixed r
r = p5()
chk("5 eta rc=1.5", r["eta_15"], 0.6565, 1e-4)
chk("5 eta rc=2", r["eta_2"], 0.6316, 1e-4)
chk("5 eta rc=3", r["eta_3"], 0.5891, 1e-4)
assert r["eta_otto"] > r["eta_15"] > r["eta_2"] > r["eta_3"];  _n += 1

# P6 -- dual cycle brackets Diesel and Otto
r = p6()
chk("6 T2", r["T2"], 909.4, 0.1)
chk("6 T5", r["T5"], 688.0, 0.1)
chk("6 eta", r["eta"], 0.6474, 1e-4)
chk("6 balance -> eta", r["w_net"] / r["q_in"], r["eta"], 1e-12)
assert r["eta_diesel"] < r["eta"] < r["eta_otto"];  _n += 1

# P7 -- ideal Brayton, cold air-standard
r = p7()
chk("7 T2", r["T2"], 610.2, 0.1)
chk("7 T4", r["T4"], 688.3, 0.1)
chk("7 eta", r["eta"], 0.5084, 1e-4)
chk("7 w_net", r["w_net"], 403.5, 0.1)
chk("7 bwr", r["bwr"], 0.4359, 1e-4)
chk("7 balance closes", r["q_in"] - r["q_out"], r["w_net"], 1e-9)
assert r["eta"] < r["eta_carnot"];       _n += 1                  # 0.508 < 0.786
assert 0.4 < r["bwr"] < 0.8;             _n += 1                  # gas-turbine band

# P8 -- Brayton with irreversible turbomachines
r = p8()
chk("8 wt", r["wt"], 608.0, 0.1)
chk("8 wc", r["wc"], 366.8, 0.1)
chk("8 eta", r["eta"], 0.3265, 1e-4)
chk("8 bwr", r["bwr"], 0.6033, 1e-4)
assert r["eta"] < p7()["eta"];           _n += 1                  # efficiency collapses
assert r["bwr"] > p7()["bwr"];           _n += 1                  # back work grows
assert r["wt"] - r["wc"] > 0;            _n += 1                  # still nets work out

# P9 -- Brayton with regeneration
r = p9()
chk("9 Tx", r["Tx"], 668.8, 0.1)
chk("9 eta", r["eta"], 0.5491, 1e-4)
assert r["T4_minus_T2"] > 0;             _n += 1                  # regeneration possible
assert r["eta"] > r["eta_no_regen"];     _n += 1                  # eta rises, w unchanged

# P10 -- ideal Rankine 60 bar -> 0.10 bar (states from steam_tables CSVs)
r = p10()
chk("10 x2", r["x2"], 0.6986, 1e-4)
chk("10 h2", r["h2"], 1863.4, 0.1)
chk("10 wp", r["wp"], 6.05, 0.01)
chk("10 eta", r["eta"], 0.3537, 1e-4)
chk("10 bwr", r["bwr"], 0.0066, 1e-4)
chk("10 balance closes", r["q_in"] - r["q_out"], r["wt"] - r["wp"], 1e-9)
assert r["bwr"] < 0.02;                  _n += 1                  # vapor-plant band
assert 0.0 < r["x2"] < 1.0;              _n += 1                  # exit is two-phase

# P11 -- condenser-pressure effect at fixed boiler pressure
r = p11()
chk("11 eta 0.08 bar", r["eta_008"], 0.3708, 1e-4)
chk("11 eta 1.0 bar", r["eta_100"], 0.2902, 1e-4)
assert r["eta_008"] > r["eta_100"];      _n += 1                  # lower p_cond wins
assert r["x2_008"] < r["x2_100"];        _n += 1                  # ...but exits wetter

# P12 -- boiler-pressure effect + Carnot ceiling at Tsat extremes
r = p12()
chk("12 eta 40 bar", r["eta_40"], 0.3429, 1e-4)
chk("12 eta 80 bar", r["eta_80"], 0.3708, 1e-4)
chk("12 carnot 80 bar", r["carnot_80"], 0.4463, 1e-4)
assert r["eta_80"] > r["eta_40"];        _n += 1                  # higher p_boiler wins
assert r["eta_40"] < r["carnot_40"];     _n += 1
assert r["eta_80"] < r["carnot_80"];     _n += 1

print(f"All {_n} tests passed.")
