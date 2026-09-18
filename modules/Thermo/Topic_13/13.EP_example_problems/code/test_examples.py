"""test_examples.py — checks for Module 13.EP (Moran Ch.9 Examples 9.14, 9.15).
Run: python3 test_examples.py.  Each value is checked against Moran's published answer."""
import math
from examples import ex_9_14, ex_9_15

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# ===== Example 9.14 -- converging nozzle, back-pressure effect =====
e = ex_9_14()
chk("9.14 p* (kPa)", e["p_star_kPa"], 528.0, 0.5)            # book 528 kPa
assert e["choked_a"] is True;  _n += 1                       # 500 < 528 -> choked
# (a) choked
chk("9.14a M2", e["M2a"], 1.0)
chk("9.14a p2 (kPa)", e["p2a_kPa"], 528.0, 0.5)
chk("9.14a T2", e["T2a"], 300.0, 0.5)
chk("9.14a V2", e["V2a"], 347.2, 0.1)
chk("9.14a mdot", e["mdot_a"], 2.13, 0.01)
# (b) subsonic
chk("9.14b M2", e["M2b"], 0.6, 1e-3)
chk("9.14b T2", e["T2b"], 336.0, 0.5)
chk("9.14b V2", e["V2b"], 220.5, 0.5)
chk("9.14b mdot", e["mdot_b"], 1.79, 0.01)

# ===== Example 9.15 -- converging-diverging nozzle, five cases =====
g = ex_9_15()
# (a)
chk("9.15 At/A* (Mt=0.7)", g["At_Astar"], 1.09437, 1e-4)    # Table 9.2
chk("9.15a A2/A*", g["A2_Astar_a"], 2.6265, 1e-3)           # book 2.6265
chk("9.15a M2", g["M2a"], 0.24)
chk("9.15a T2", g["T2a"], 494.0, 0.5)
chk("9.15a p2", g["p2a"], 95.9, 0.05)
chk("9.15a V2", g["V2a"], 262.0, 1.0)
chk("9.15a mdot", g["mdot_a"], 2.29, 0.01)
# (b)
chk("9.15b A2/A*", g["A2_Astar_b"], 2.4)
chk("9.15b M2", g["M2b"], 0.26)
chk("9.15b T2", g["T2b"], 493.0, 0.5)
chk("9.15b p2", g["p2b"], 95.3, 0.05)
chk("9.15b V2", g["V2b"], 283.0, 1.0)
chk("9.15b mdot", g["mdot_b"], 2.46, 0.01)
# (c)
chk("9.15c M2", g["M2c"], 2.4)
chk("9.15c p2", g["p2c"], 6.84, 0.01)
chk("9.15c mdot (= choked)", g["mdot_c"], g["mdot_b"], 1e-9)
# (d) normal shock at exit
chk("9.15d My", g["My_d"], 0.52312, 1e-4)                    # Table 9.3 @Mx=2.4
chk("9.15d py/px", g["py_px_d"], 6.5533, 1e-3)
chk("9.15d py", g["py_d"], 44.82, 0.02)
# (e) shock in diverging section
chk("9.15e Mx (from A/A*=2.0)", g["Mx_e"], 2.2, 0.01)       # Table 9.2
chk("9.15e poy/pox", g["poy_pox_e"], 0.62812, 1e-4)         # Table 9.3 @Mx=2.2
chk("9.15e A2/A*y", g["A2_Asy_e"], 1.51, 0.005)
chk("9.15e M2", g["M2e"], 0.43)
chk("9.15e p2", g["p2e"], 55.3, 0.1)
# all five C-D cases share the choked mass flow rate
for c in ("mdot_b", "mdot_c", "mdot_d", "mdot_e"):
    chk("9.15 choked mdot " + c, g[c], 2.46, 0.01)

print(f"All {_n} tests passed.")
