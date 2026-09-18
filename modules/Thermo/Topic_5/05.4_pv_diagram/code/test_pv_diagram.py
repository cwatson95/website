"""test_pv_diagram.py — checks for Module 5.4.  Run: python3 test_pv_diagram.py"""
import math
from pv_diagram import (work_pdV, work_isobaric, p_polytropic, work_polytropic,
                        work_isothermal_ideal_gas, _polytropic_path)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# trapezoid: rectangle area = p*(V2-V1)
chk("trapezoid rectangle", work_pdV([300.0, 300.0], [0.1, 0.2]), 30.0)
# trapezoid: triangle/linear path area
chk("trapezoid linear", work_pdV([200.0, 100.0], [0.0, 2.0]), 300.0)   # 1/2(200+100)(2)
# sign: compression (V decreases) gives negative work
chk("trapezoid compress sign", work_pdV([100.0, 200.0], [2.0, 0.0]), -300.0)

# Moran Example 2.1 -- p1=300 kPa, V1=0.1, V2=0.2 m^3
p1, V1, V2 = 300.0, 0.1, 0.2
p2 = p_polytropic(p1, V1, V2, 1.5)
chk("Ex2.1 p2", p2, 106.07, 0.05)
chk("Ex2.1 (a) n=1.5", work_polytropic(p1, V1, p2, V2, 1.5), 17.6, 0.05)
chk("Ex2.1 (b) n=1.0", work_isothermal_ideal_gas(p1, V1, V2), 20.79, 0.01)
chk("Ex2.1 (c) n=0", work_isobaric(p1, V1, V2), 30.0)

# trapezoid over a finely sampled polytropic curve reproduces the closed form
ps, Vs = _polytropic_path(p1, V1, V2, 1.5)
chk("trapezoid == polytropic closed form", work_pdV(ps, Vs),
    work_polytropic(p1, V1, p2, V2, 1.5), 1e-3)

# n=1 guard
try:
    work_polytropic(p1, V1, p2, V2, 1.0); raise AssertionError("expected ValueError")
except ValueError:
    _n += 1

# Moran Example 3.4 -- water isobaric 10 bar (1000 kPa)
chk("Ex3.4 W/m", work_isobaric(1000.0, 0.3066, 0.1944), -112.2, 0.05)
# Moran Example 6.1 -- water isobaric 4.758 bar (475.8 kPa)
chk("Ex6.1 W/m", work_isobaric(475.8, 1.0905e-3, 0.3928), 186.38, 0.05)

# path dependence: two paths between the same end states give different work
#   path A: expand at high p then drop p ; path B: drop p then expand at low p
A = work_pdV([300.0, 300.0, 100.0], [0.1, 0.2, 0.2])   # 30 + 0
B = work_pdV([300.0, 100.0, 100.0], [0.1, 0.1, 0.2])   # 0 + 10
assert abs(A - B) > 1.0; _n += 1
chk("path A area", A, 30.0)
chk("path B area", B, 10.0)

print(f"All {_n} tests passed.")
