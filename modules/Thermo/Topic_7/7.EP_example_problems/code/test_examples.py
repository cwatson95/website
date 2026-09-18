"""test_examples.py — checks for Module 7.EP (Moran Ch.5/6 examples).  Run: python3 test_examples.py"""
import math
from examples import ex_5_1, ex_5_2, ex_5_3, ex_6_11, ex_6_12, ex_6_13, ex_6_14

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# Ex 5.1 -- power cycle classification (TH=2000 K, TC=400 K)
e = ex_5_1()
chk("5.1 eta_max", e["eta_max"], 0.80)
chk("5.1 eta_b", e["eta_b"], 0.85)
assert e["class_a"] == "irreversible", e["class_a"]; _n += 1     # (a) eta=0.60 < 0.80
assert e["class_b"] == "impossible",   e["class_b"]; _n += 1     # (b) eta=0.85 > 0.80
assert e["class_c"] == "reversible",   e["class_c"]; _n += 1     # (c) eta=0.80 = 0.80
# Ex 5.2 -- refrigerator COP
e = ex_5_2()
chk("5.2 beta", e["beta"], 2.5)
chk("5.2 beta_max", e["beta_max"], 9.926, 1e-3)                  # book 9.9
# Ex 5.3 -- heat pump COP, min work, cost
e = ex_5_3()
chk("5.3 gamma_max", e["gamma_max"], 13.947, 1e-3)              # book 13.95
chk("5.3 W_min", e["W_min"], 3.58e4, 100.0)                     # book 3.58e4 Btu/day
chk("5.3 cost", e["cost"], 1.36, 0.01)                          # book $1.36/day
# Ex 6.11 -- steam turbine work from eta_t
chk("6.11 W/m", ex_6_11()["W_m"], 271.95, 0.01)
# Ex 6.12 -- air turbine eta_t from work
e = ex_6_12()
chk("6.12 w_s", e["w_s"], 105.6, 0.05)
chk("6.12 eta_t", e["eta_t"], 0.70, 0.005)
# Ex 6.13 -- steam nozzle efficiency
e = ex_6_13()
chk("6.13 ke2", e["ke2"], 114.8, 0.01)
chk("6.13 ke2s", e["ke2s"], 124.3, 0.01)
chk("6.13 eta_n", e["eta_n"], 0.924, 1e-3)
# Ex 6.14 -- R-22 compressor power and efficiency
e = ex_6_14()
chk("6.14 W_cv", e["W_cv"], -3.11, 0.01)
chk("6.14 eta_c", e["eta_c"], 0.81, 0.005)

print(f"All {_n} tests passed.")
