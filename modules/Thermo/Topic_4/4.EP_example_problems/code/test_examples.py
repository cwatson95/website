"""test_examples.py — checks for Module 4.EP (Moran Ch.3/6/7 examples).  Run: python3 test_examples.py"""
import math
from examples import ex_3_1, ex_3_2, ex_6_1, ex_6_2, ex_7_1, ex_7_2

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# Ex 3.1 -- ammonia, constant pressure
e = ex_3_1()
chk("3.1 V1", e["V1"], 1.35, 0.005)
chk("3.1 V2", e["V2"], 1.67, 0.005)
chk("3.1 W", e["W"], 1.18, 0.01)
# Ex 3.2 -- water, constant volume
e = ex_3_2()
chk("3.2 v1", e["v1"], 0.8475, 1e-3)
chk("3.2 m", e["m"], 0.59, 0.01)
chk("3.2 mg1", e["mg1"], 0.295, 0.005)
chk("3.2 x2", e["x2"], 0.731, 1e-3)
chk("3.2 mg2", e["mg2"], 0.431, 0.005)
# Ex 6.1 -- reversible
e = ex_6_1()
chk("6.1 W/m", e["W_m"], 186.38, 0.05)
chk("6.1 Q/m", e["Q_m"], 2114.1, 0.1)
# Ex 6.2 -- adiabatic (same end states, sigma > 0)
e = ex_6_2()
chk("6.2 W/m", e["W_m"], -1927.82, 0.01)
chk("6.2 sigma/m", e["sigma_m"], 4.9961, 1e-4)
# Ex 7.1 -- exergy of exhaust gas
chk("7.1 e", ex_7_1()["e"], 368.91, 0.05)
# Ex 7.2 -- exergy balance (reversible -> Ed=0)
e = ex_7_2()
chk("7.2 Eq/m", e["Eq_m"], 649.49, 0.1)
chk("7.2 Ew/m", e["Ew_m"], 147.21, 0.1)
chk("7.2 de", e["de"], 502.4, 0.2)

print(f"All {_n} tests passed.")
