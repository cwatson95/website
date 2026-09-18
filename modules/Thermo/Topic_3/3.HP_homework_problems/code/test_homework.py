"""test_homework.py — checks for Module 3.HP.  Run: python3 test_homework.py"""
import math
from homework import p5_2, p5_21, p5_31, p5_34, p5_48, p5_50, p5_76

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# 5.2 -- impossible cycle (energy balance still closes)
chk("5.2 W_balance", p5_2()["W_balance"], 100.0)
assert p5_2()["energy_ok"] is True;   _n += 1
assert p5_2()["possible"] is False;   _n += 1

# 5.21 -- reversible power cycle
r = p5_21()
chk("5.21 T_C", r["T_C"], 360.0)
chk("5.21 W", r["W"], 20.0)
chk("5.21 Q_C", r["Q_C"], 30.0)

# 5.31 -- actual cycle = 75% of reversible
r = p5_31()
chk("5.31 eta_rev", r["eta_rev"], 0.4796, 1e-3)
chk("5.31 eta", r["eta"], 0.3597, 1e-3)
chk("5.31 W", r["W"], 359.67, 0.1)
chk("5.31 Q_C", r["Q_C"], 640.33, 0.1)
chk("5.31 balance", r["W"] + r["Q_C"], 1000.0, 1e-6)        # W + Q_C = Q_H

# 5.34 -- minimum heat rejection rate
r = p5_34()
chk("5.34 eta_max", r["eta_max"], 0.38)
chk("5.34 Qh_min", r["Qh_min"], 0.1 / 0.38, 1e-9)
chk("5.34 Qc_min", r["Qc_min"], 0.1 / 0.38 - 0.1, 1e-9)

# 5.48 -- COP from efficiency
r = p5_48()
chk("5.48 beta", r["beta"], 4.0)
chk("5.48 gamma", r["gamma"], 5.0)

# 5.50 -- evaluate the three COP claims
r = p5_50()
chk("5.50 beta_max", r["beta_max"], 9.6)
assert r["verdict"]["a"] == "impossible";              _n += 1   # 10 > 9.6
assert r["verdict"]["b"] == "reversible";              _n += 1   # 9.6 = max
assert r["verdict"]["c"].startswith("possible");       _n += 1   # 4 < 9.6

# 5.76 -- Carnot efficiency and its sensitivity
r = p5_76()
chk("5.76 eta", r["eta"], 0.5)
chk("5.76 eta2", r["eta2"], 0.56522, 1e-4)
chk("5.76 pct", r["pct_change"], 13.043, 1e-2)

print(f"All {_n} tests passed.")
