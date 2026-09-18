"""test_examples.py — checks for Module 3.EP (Moran Ch.5 examples).  Run: python3 test_examples.py"""
import math
from examples import ex_5_1, ex_5_2, ex_5_3

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# Example 5.1 -- power cycle
e1 = ex_5_1()
chk("5.1 eta_max", e1["eta_max"], 0.80)
chk("5.1 eta_b", e1["eta_b"], 0.85)
chk("5.1 W_c", e1["W_c"], 800.0)
chk("5.1 eta_c", e1["eta_c"], 0.80)
assert e1["a_possible"] is True;   _n += 1     # eta 0.60 < 0.80: irreversible, allowed
assert e1["b_possible"] is False;  _n += 1     # eta 0.85 > 0.80: impossible

# Example 5.2 -- refrigerator
e2 = ex_5_2()
chk("5.2 beta", e2["beta"], 2.5)
chk("5.2 beta_max", e2["beta_max"], 9.9, 0.05)            # book 9.9
chk("5.2 beta_claim", e2["beta_claim"], 10.0)
assert e2["irreversible"] is True;  _n += 1
assert e2["claim_valid"] is False;  _n += 1               # 10 > 9.93 -> claim invalid

# Example 5.3 -- heat pump
e3 = ex_5_3()
chk("5.3 gamma_max", e3["gamma_max"], 13.95, 0.01)
chk("5.3 W_min", e3["W_min_Btu_day"], 3.58e4, 100.0)      # 3.58e4 Btu/day
chk("5.3 cost", e3["cost_per_day"], 1.36, 0.01)           # $1.36/day

print(f"All {_n} tests passed.")
