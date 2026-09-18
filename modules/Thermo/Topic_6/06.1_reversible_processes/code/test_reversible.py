"""test_reversible.py — checks for Module 6.1.  Run: python3 test_reversible.py"""
import math
from reversible import (entropy_change_int_rev, heat_int_rev_isothermal, heat_int_rev_area,
                        work_const_pressure, sigma_internally_reversible, is_isentropic,
                        carnot_eff_ts)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# dS = dQ/T  (isothermal int rev)
chk("dS = Q/T", entropy_change_int_rev(2114.1, 423.15), 2114.1 / 423.15)

# Example 6.1 -- water, internally reversible at 150 C (p.303-304)
W = work_const_pressure(475.8, 0.3928, 1.0905e-3)
Q = heat_int_rev_isothermal(423.15, 6.8379, 1.8418)
chk("Ex6.1 W/m", W, 186.38, 0.05)
chk("Ex6.1 Q/m", Q, 2114.1, 0.5)

# Q as the area under the T-s curve equals T dS for the isothermal path
chk("Ex6.1 area==TdS", heat_int_rev_area([423.15, 423.15], [1.8418, 6.8379]), Q, 1e-9)
# trapezoidal area for a linearly ramping temperature: (T1+T2)/2 * (s2-s1)
chk("area trapezoid", heat_int_rev_area([300.0, 500.0], [1.0, 2.0]), 0.5 * (300.0 + 500.0) * 1.0)

# internally reversible: no entropy produced
chk("sigma int rev", sigma_internally_reversible(), 0.0, 1e-12)

# adiabatic + internally reversible => isentropic
assert is_isentropic(0.0, True) is True;          _n += 1
assert is_isentropic(0.0, False) is False;        _n += 1     # int. irreversible -> not isentropic
assert is_isentropic(50.0, True) is False;        _n += 1     # heat added -> entropy changes

# Carnot efficiency from the T-s area argument == 1 - T_C/T_H
chk("carnot_eff_ts", carnot_eff_ts(1400.0, 350.0), 0.75)
chk("carnot_eff_ts2", carnot_eff_ts(2000.0, 400.0), 0.80)

print(f"All {_n} tests passed.")
