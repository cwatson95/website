"""test_liquid_tables.py — checks for Module 5.3.  Run: python3 test_liquid_tables.py"""
import math
from liquid_tables import (load_A5, linear_interp, pressures, compressed, sat_liquid,
                           v_approx, u_approx, h_approx, h_approx_simple)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# table present; 8 pressure blocks (steam_tables/README)
assert len(pressures()) == 8; _n += 1

# exact on-grid A-5 lookups (100 bar block, 100 C)
chk("A-5 v@100bar,100C", compressed(100.0, 100.0, "v"), 1.0385e-3)
chk("A-5 u@100bar,100C", compressed(100.0, 100.0, "u"), 416.12)
chk("A-5 h@100bar,100C", compressed(100.0, 100.0, "h"), 426.50)
# Problem 3.13(b): 40 C, 200 bar
chk("A-5 v@200bar,40C", compressed(200.0, 40.0, "v"), 0.9992e-3)

# saturated-liquid reference values from A-2
sl100 = sat_liquid(100.0)
chk("sat_liq vf@100C", sl100["vf"], 1.0435e-3)
chk("sat_liq uf@100C", sl100["uf"], 418.94)
chk("sat_liq hf@100C", sl100["hf"], 419.04)
chk("sat_liq psat@100C", sl100["psat_bar"], 1.014)

# Eq. 3.11/3.12 approximations vs the A-5 table value (within a few tenths of a percent)
v_tab = compressed(100.0, 100.0, "v")
assert abs(v_approx(sl100["vf"]) - v_tab) / v_tab < 0.01; _n += 1     # < 1 %
u_tab = compressed(100.0, 100.0, "u")
assert abs(u_approx(sl100["uf"]) - u_tab) / u_tab < 0.01; _n += 1
chk("v_approx is vf", v_approx(sl100["vf"]), sl100["vf"])
chk("u_approx is uf", u_approx(sl100["uf"]), sl100["uf"])

# Eq. 3.13: h ~= hf + vf (p - psat)  at 100 bar, 100 C
h13 = h_approx(sl100["hf"], sl100["vf"], 100 * 100.0, sl100["psat_bar"] * 100.0)
chk("h_approx 3.13", h13, 429.37, 0.1)
assert abs(h13 - compressed(100.0, 100.0, "h")) < 3.0; _n += 1        # within 3 kJ/kg of table
chk("h_approx_simple is hf", h_approx_simple(sl100["hf"]), 419.04)
# the pressure correction term is positive and a few kJ/kg
assert h13 > h_approx_simple(sl100["hf"]); _n += 1

# Problem 3.13(c): 40 C, 20 bar -> approximation v ~= vf(40 C)
chk("3.13c v~vf@40C", v_approx(sat_liquid(40.0)["vf"]), 1.0078e-3)

# v varies little with pressure at fixed T (20 -> 200 bar at 40 C): < 1 %
v_lo = compressed(25.0, 40.0, "v"); v_hi = compressed(200.0, 40.0, "v")
assert abs(v_hi - v_lo) / v_lo < 0.01; _n += 1

print(f"All {_n} tests passed.")
