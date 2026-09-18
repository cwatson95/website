"""test_vapor_tables.py — checks for Module 5.2.  Run: python3 test_vapor_tables.py"""
import math
from vapor_tables import (load_A4, linear_interp, pressures, superheated, enthalpy)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# table present; 24 pressure blocks (steam_tables/README)
assert len(load_A4()) > 250; _n += 1
assert len(pressures()) == 24; _n += 1

# exact on-grid lookups (10 bar block)
chk("A-4 v@10bar,200C", superheated(10.0, 200.0, "v"), 0.2060)
chk("A-4 v@10bar,240C", superheated(10.0, 240.0, "v"), 0.2275)
chk("A-4 u@10bar,400C", superheated(10.0, 400.0, "u"), 2957.3)
chk("A-4 v@10bar,400C", superheated(10.0, 400.0, "v"), 0.3066)
chk("A-4 h@1bar,120C", superheated(1.0, 120.0, "h"), 2716.6)

# Moran single-interpolation illustration (p.105): 10 bar, 215 C -> 0.2141 m3/kg
chk("interp 10bar,215C", superheated(10.0, 215.0, "v"), 0.2141, 5e-5)

# Problem 3.7 -- single & double interpolation (book data = A-4 @10,15 bar)
chk("3.7a 12.5bar,240C", superheated(12.5, 240.0, "v"), 0.1879, 1e-4)   # interp in p
# 3.7b: invert -> at 15 bar, v=0.1555 -> T (between 240->0.1483 and 280->0.1627)
chk("3.7b T@15bar,v=0.1555", linear_interp(0.1555, 0.1483, 0.1627, 240.0, 280.0), 260.0, 0.1)
chk("3.7c 14bar,220C double", superheated(14.0, 220.0, "v"), 0.1557, 1e-4)

# Example 3.3 (English) interpolation analogue is checked in 5.EP; here verify the
# DOUBLE-interpolation reduces to single interpolation on a grid pressure:
chk("double==single on grid", superheated(15.0, 220.0, "v"),
    linear_interp(220.0, 200.0, 240.0, 0.1325, 0.1483))

# h = u + p v consistency from the table itself (10 bar = 1000 kPa, 240 C)
u = superheated(10.0, 240.0, "u"); v = superheated(10.0, 240.0, "v")
chk("h=u+pv @10bar,240C", enthalpy(u, 1000.0, v), superheated(10.0, 240.0, "h"), 0.5)

# monotonic: v increases with T at fixed p
assert superheated(10.0, 240.0, "v") > superheated(10.0, 200.0, "v"); _n += 1
# v decreases with p at fixed T (220 C: 10 bar > 15 bar)
assert superheated(10.0, 220.0, "v") > superheated(15.0, 220.0, "v"); _n += 1

print(f"All {_n} tests passed.")
