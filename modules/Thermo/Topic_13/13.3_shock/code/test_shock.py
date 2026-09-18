"""test_shock.py — checks for Module 13.3.  Run: python3 test_shock.py"""
import math
from shock import (mach_after_shock, shock_temperature_ratio, shock_pressure_ratio,
                   stagnation_pressure_ratio_across_shock, sonic_area_ratio_across_shock)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

k = 1.4

# --- Table 9.3 row at Mx = 1.0 (no shock: all ratios unity) ---
chk("My @Mx=1", mach_after_shock(1.0, k), 1.0, 1e-9)
chk("py/px @Mx=1", shock_pressure_ratio(1.0, k), 1.0, 1e-9)
chk("Ty/Tx @Mx=1", shock_temperature_ratio(1.0, k), 1.0, 1e-9)
chk("poy/pox @Mx=1", stagnation_pressure_ratio_across_shock(1.0, k), 1.0, 1e-9)
# --- Table 9.3 row at Mx = 1.5 (k=1.4) ---
chk("My @Mx=1.5", mach_after_shock(1.5, k), 0.70109, 1e-4)
chk("py/px @Mx=1.5", shock_pressure_ratio(1.5, k), 2.4583, 1e-3)
chk("Ty/Tx @Mx=1.5", shock_temperature_ratio(1.5, k), 1.3202, 1e-3)
chk("poy/pox @Mx=1.5", stagnation_pressure_ratio_across_shock(1.5, k), 0.92978, 1e-4)
# --- Table 9.3 row at Mx = 2.0 (k=1.4) ---
chk("My @Mx=2.0", mach_after_shock(2.0, k), 0.57735, 1e-4)
chk("py/px @Mx=2.0", shock_pressure_ratio(2.0, k), 4.5000, 1e-3)
chk("Ty/Tx @Mx=2.0", shock_temperature_ratio(2.0, k), 1.6875, 1e-3)
chk("poy/pox @Mx=2.0", stagnation_pressure_ratio_across_shock(2.0, k), 0.72088, 1e-4)
# --- across a shock entropy rises -> stagnation pressure must drop (<1) ---
assert stagnation_pressure_ratio_across_shock(2.0, k) < 1.0;  _n += 1
assert mach_after_shock(2.0, k) < 1.0;                        _n += 1     # supersonic -> subsonic
# --- Eq. 9.57: A*x/A*y = poy/pox ---
chk("A*x/A*y = poy/pox", sonic_area_ratio_across_shock(2.0, k),
    stagnation_pressure_ratio_across_shock(2.0, k), 1e-12)
# --- Example 9.15(d): shock at exit, Mx=2.4, px=6.84 lbf/in^2 ---
My_d = mach_after_shock(2.4, k)
chk("Ex9.15d My", My_d, 0.52312, 1e-4)
chk("Ex9.15d py/px", shock_pressure_ratio(2.4, k), 6.5533, 1e-3)
chk("Ex9.15d py", 6.84 * shock_pressure_ratio(2.4, k), 44.82, 0.02)
# --- Example 9.15(e): shock in diverging section, Mx=2.2 ---
chk("Ex9.15e poy/pox", stagnation_pressure_ratio_across_shock(2.2, k), 0.62812, 1e-4)
chk("Ex9.15e My", mach_after_shock(2.2, k), 0.54706, 1e-4)

print(f"All {_n} tests passed.")
