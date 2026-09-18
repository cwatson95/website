"""test_examples.py — checks for Module 5.EP (Moran Ch.3/Ch.6 property examples).
Run: python3 test_examples.py.  Each value is checked against Moran's published answer."""
import math
from examples import ex_3_2, ex_3_4, ex_6_1, ex_superheat_uh, ex_mollier

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# ===== Example 3.2 -- Heating Water at Constant Volume =====
e = ex_3_2()
chk("3.2 v1", e["v1"], 0.8475, 5e-4)        # book 0.8475 m^3/kg
chk("3.2 T1", e["T1"], 99.63, 0.01)
chk("3.2 T2", e["T2"], 111.4, 0.05)
chk("3.2 m", e["m"], 0.59, 5e-3)
chk("3.2 mg1", e["mg1"], 0.295, 5e-3)
chk("3.2 x2", e["x2"], 0.731, 2e-3)
chk("3.2 mg2", e["mg2"], 0.431, 5e-3)
chk("3.2 p3", e["p3"], 2.11, 0.02)          # book 2.11 bar (interp at vg=0.8475)
# consistency: vapor mass grows as the mixture is heated toward all-vapor
assert e["mg2"] > e["mg1"]; _n += 1

# ===== Example 3.4 -- Analyzing Two Processes in Series =====
e = ex_3_4()
chk("3.4 v1", e["v1"], 0.3066, 1e-4)        # A-4 @10 bar, 400 C
chk("3.4 u1", e["u1"], 2957.3, 0.1)
chk("3.4 v2", e["v2"], 0.1944, 1e-4)        # sat vapor @10 bar
chk("3.4 W/m", e["Wm"], -112.2, 0.05)       # book -112.2 kJ/kg
chk("3.4 x3", e["x3"], 0.494, 1e-9)         # book quality (rounded)
chk("3.4 u3", e["u3"], 1584.0, 0.1)         # book 1584.0 kJ/kg
chk("3.4 Q/m", e["Qm"], -1485.5, 0.1)       # book -1485.5 kJ/kg
# consistency: both work and heat are out of the system (negative)
assert e["Wm"] < 0 and e["Qm"] < 0; _n += 1

# ===== Example 6.1 -- reversible vaporization of water at 150 C =====
e = ex_6_1()
chk("6.1 p_kPa", e["p_kPa"], 475.8, 0.05)   # psat(150 C) = 4.758 bar
chk("6.1 W/m", e["Wm"], 186.38, 0.05)       # book 186.38 kJ/kg
chk("6.1 Q/m", e["Qm"], 2114.1, 0.1)        # book 2114.1 kJ/kg
# consistency: Q = W + (u2-u1) = W + (h2-h1) - (p)(v2-v1)... here Q>W>0 (heat in, work out)
assert e["Qm"] > e["Wm"] > 0; _n += 1

# ===== in-text illustration p.112: superheated water from u =====
e = ex_superheat_uh()
chk("p112 v", e["v"], 1.793, 1e-3)
chk("p112 u", e["u"], 2537.3, 0.05)
chk("p112 h_tab", e["h_tab"], 2716.6, 0.05)
chk("p112 h=u+pv", e["h_calc"], 2716.6, 0.05)   # h = u + pv reproduces the table h
chk("p112 h_calc == h_tab", e["h_calc"], e["h_tab"], 0.05)

# ===== in-text illustration p.296: Mollier isentropic expansion =====
e = ex_mollier()
chk("p296 x2", e["x2"], 0.98, 5e-3)             # Moran's stated chart value ~0.98
chk("p296 h2", e["h2"], 2537.0, 3.0)            # ~2537 kJ/kg (chart-reading accuracy)
assert 0.0 < e["x2"] < 1.0; _n += 1             # state 2 is inside the dome

print(f"All {_n} tests passed.")
