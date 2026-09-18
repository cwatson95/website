"""test_homework.py — checks for Module 5.HP (Moran Ch.3 property-data problems).
Run: python3 test_homework.py.  Moran has no answer key; these are worked solutions, with
physical-consistency checks (phase classification, interpolation, rigid-process trends)."""
import math
from homework import p3_6, p3_7, p3_13, p3_14, p3_15a, p3_23

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

def chk_eq(name, got, want):
    global _n
    assert got == want, f"{name}: {got!r} != {want!r}"
    _n += 1

# 3.6 -- phase determination
r = p3_6()
chk_eq("3.6a", r["a"], "two-phase")          # Tsat(10 bar)=179.9 C
chk_eq("3.6b", r["b"], "compressed liquid")
chk_eq("3.6c", r["c"], "superheated vapor")  # Tsat(0.5 bar)=81.3 C < 100
chk_eq("3.6d", r["d"], "compressed liquid")
chk_eq("3.6e", r["e"], "solid")              # below triple point

# 3.7 -- superheated interpolation
r = p3_7()
chk("3.7a v", r["v_a"], 0.1879, 1e-4)
chk("3.7b T", r["T_b"], 260.0, 0.1)
chk("3.7c v", r["v_c"], 0.1557, 1e-4)
# consistency: (c) double-interp value lies between the 1.0 and 1.5 MPa block values @220 C
assert 0.1404 < r["v_c"] < 0.2168; _n += 1

# 3.13 -- specific volume of water at three states
r = p3_13()
chk("3.13b v (A-5)", r["v_b"], 0.9992e-3, 1e-7)
chk("3.13c v~vf(40C)", r["v_c"], 1.0078e-3, 1e-7)
# (a) superheated 200 bar/400 C: order-of-magnitude sanity (much larger than liquid v)
assert 5e-3 < r["v_a"] < 2e-2; _n += 1
# liquid v barely changes with pressure: (b) 200 bar vs (c) ~sat are within 1.5 %
assert abs(r["v_b"] - r["v_c"]) / r["v_c"] < 0.015; _n += 1

# 3.14 -- locate states
r = p3_14()
chk("3.14 psat(120C)", r["psat120_bar"], 1.985, 0.01)
chk_eq("3.14a 5bar", r["a"], "compressed liquid")    # p=5 > psat=1.985
chk_eq("3.14b v=0.6", r["b"], "two-phase")           # vf<0.6<vg at 120 C
chk_eq("3.14c 1bar", r["c"], "superheated vapor")    # p=1 < psat=1.985

# 3.15(a) -- two-phase quality
r = p3_15a()
chk("3.15a v", r["v"], 0.25, 1e-9)
chk_eq("3.15a phase", r["phase"], "two-phase")
chk("3.15a x", r["x"], 0.149, 1e-3)

# 3.23 -- rigid tank, sat vapor cooled
r = p3_23()
chk("3.23 p1", r["p1_bar"], 15.54, 0.02)             # psat(200 C)
chk_eq("3.23 phase2", r["phase2"], "two-phase")
chk("3.23 p2", r["p2_bar"], 1.014, 0.005)            # psat(100 C)
chk("3.23 x2", r["x2"], 0.0756, 5e-4)
# consistency: cooling a rigid sat-vapor drops the pressure and the quality (partial condensation)
assert r["p2_bar"] < r["p1_bar"]; _n += 1
assert 0.0 < r["x2"] < 1.0; _n += 1

print(f"All {_n} tests passed.")
