"""test_homework.py — checks for Module 4.HP.  Run: python3 test_homework.py"""
import math
from homework import p3_46, p3_63, p3_70, p6_11, p6_37, p6_59, p7_21, p7_36

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# 3.46 -- rigid heating (Q/m = du)
r = p3_46()
chk("3.46 u2", r["u2"], 2961.2, 0.2)
chk("3.46 Q/m", r["Q_m"], 407.6, 0.3)
# 3.63 -- rigid cooling
r = p3_63()
chk("3.63 m", r["m"], 6.255, 0.01)
chk("3.63 x2", r["x2"], 0.171, 1e-3)
chk("3.63 Q", r["Q"], -8283.0, 5.0)
# 3.70 -- constant-pressure heating
r = p3_70()
chk("3.70 h2", r["h2"], 3531.9, 0.05)
chk("3.70 T2", r["T2"], 522.0, 0.5)
chk("3.70 W", r["W"], 667.0, 1.0)
# 6.11 -- ideal-gas entropy change (a property)
chk("6.11 ds", p6_11()["ds"], -0.0197, 1e-3)
# 6.37 -- rigid insulated air + paddle
r = p6_37()
chk("6.37 m", r["m"], 4.757, 0.005)
chk("6.37 T2", r["T2"], 500.3, 0.1)
chk("6.37 sigma", r["sigma"], 1.83, 0.01)
# 6.59 -- thermal mixing
r = p6_59()
chk("6.59 Tf", r["Tf"], 295.93, 0.01)
chk("6.59 sigma", r["sigma"], 0.673, 0.005)
# 7.21 -- warmed slab exergy
r = p7_21()
chk("7.21 dE", r["dE"], 218.6, 1.0)
chk("7.21 z", r["z"], 22.3, 0.1)
# 7.36 -- exergy destroyed by quenching
r = p7_36()
chk("7.36 Tf", r["Tf"], 505.98, 0.05)
chk("7.36 Ed", r["Ed"], 85.7, 0.1)

print(f"All {_n} tests passed.")
