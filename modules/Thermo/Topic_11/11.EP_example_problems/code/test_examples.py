"""test_examples.py — checks for Module 11.EP (Moran Ch.12 examples).  Run: python3 test_examples.py"""
import math
from examples import ex_12_7, ex_12_8, ex_12_11, ex_12_12

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# Ex 12.7 -- cooling moist air at constant pressure
e = ex_12_7()
chk("12.7 pv1", e["pv1"], 0.2542, 1e-3)
chk("12.7 omega1", e["omega1"], 0.011, 5e-4)
chk("12.7 omega2", e["omega2"], 0.0052, 5e-4)
chk("12.7 ma", e["ma"], 0.9891, 1e-3)
chk("12.7 mv1", e["mv1"], 0.0109, 3e-4)
chk("12.7 mw", e["mw"], 0.0058, 3e-4)
# Ex 12.8 -- cooling moist air at constant volume
e = ex_12_8()
chk("12.8 pv1", e["pv1"], 0.1985, 1e-4)
chk("12.8 vv1", e["vv1"], 9.145, 5e-3)
chk("12.8 mv1", e["mv1"], 3.827, 5e-3)
chk("12.8 x2", e["x2"], 0.178, 1e-3)
chk("12.8 mv2", e["mv2"], 0.681, 3e-3)
chk("12.8 mw2", e["mw2"], 3.146, 5e-3)
chk("12.8 ma", e["ma"], 40.389, 0.05)
# Ex 12.11 -- dehumidifier
e = ex_12_11()
chk("12.11 ma_dot", e["ma_dot"], 319.35, 0.1)
chk("12.11 omega1", e["omega1"], 0.0133, 5e-4)
chk("12.11 omega2", e["omega2"], 0.0076, 5e-4)
chk("12.11 mw/ma", e["mw_per_ma"], 0.0057, 5e-4)
chk("12.11 tons", e["tons"], 52.5, 0.2)
# Ex 12.12 -- steam-spray humidifier
e = ex_12_12()
chk("12.12 omega2", e["omega2"], 0.0116, 5e-4)
chk("12.12 term2", e["term2"], 25.8, 0.2)
chk("12.12 h2", e["h2"], 53.0, 0.2)

print(f"All {_n} tests passed.")
