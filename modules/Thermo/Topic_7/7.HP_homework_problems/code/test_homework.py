"""test_homework.py — checks for Module 7.HP.  Run: python3 test_homework.py"""
import math
from homework import p1, p2, p3, p4, p5, p6, p7, p8

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# P1 -- power cycle thermal efficiency
r = p1()
chk("1 eta", r["eta"], 0.40)
chk("1 Q_out", r["Q_out"], 600.0)
# P2 -- Carnot ceiling spots an impossible claim (CU #6)
r = p2()
chk("2 eta_max", r["eta_max"], 0.4066, 1e-3)
assert r["verdict"] == "impossible", r["verdict"]; _n += 1     # 45% > 40.66%
# P3 -- max thermal efficiency (CU #15)
chk("3 eta_max", p3()["eta_max"], 0.3927, 1e-3)
# P4 -- minimum heat rejection (CU #16)
r = p4()
chk("4 eta_max", r["eta_max"], 0.40)
chk("4 W_max", r["W_max"], 400.0)
chk("4 Q_C_min", r["Q_C_min"], 600.0)
chk("4 balance closes", r["Q_C_min"] + r["W_max"], 1000.0)     # Q_C + W = Q_H
# P5 -- max heat-pump COP (CU #11)
chk("5 gamma_max", p5()["gamma_max"], 13.49, 0.01)
# P6 -- refrigerator COP vs ceiling
r = p6()
chk("6 beta", r["beta"], 4.0)
chk("6 beta_max", r["beta_max"], 5.0)
# P7 -- isentropic turbine
r = p7()
chk("7 eta_t", r["eta_t"], 0.80)
chk("7 w_actual", r["w_actual"], 320.0)
chk("7 w_ideal", r["w_ideal"], 400.0)
chk("7 consistency", r["eta_t"] * r["w_ideal"], r["w_actual"])  # w = eta_t * w_ideal
# P8 -- isentropic pump
r = p8()
chk("8 eta_p", r["eta_p"], 0.80)
chk("8 w_actual", r["w_actual"], 12.5)

print(f"All {_n} tests passed.")
