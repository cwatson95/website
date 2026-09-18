"""test_supersonic.py — checks for Module 13.2.  Run: python3 test_supersonic.py"""
import math
from supersonic import (speed_of_sound_ideal_gas, mach_number, stagnation_pressure_ratio,
                        area_mach_ratio, critical_pressure_ratio, critical_temperature_ratio,
                        is_choked, mach_from_pressure_ratio, mach_from_area_ratio)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

R = 8314.0 / 28.97          # air, J/kg.K

# --- area-Mach relation vs Table 9.2 (k=1.4) ---
chk("A/A* M=0.5", area_mach_ratio(0.5, 1.4), 1.3398, 1e-3)
chk("A/A* M=0.7", area_mach_ratio(0.7, 1.4), 1.09437, 1e-4)
chk("A/A* M=1.0", area_mach_ratio(1.0, 1.4), 1.0, 1e-9)
chk("A/A* M=2.0", area_mach_ratio(2.0, 1.4), 1.6875, 1e-3)
chk("A/A* M=2.4", area_mach_ratio(2.4, 1.4), 2.4031, 1e-3)
# --- critical (sonic) ratios ---
chk("p*/po k=1.4", critical_pressure_ratio(1.4), 0.528282, 1e-5)
chk("T*/To k=1.4", critical_temperature_ratio(1.4), 0.833333, 1e-5)
# --- Example 9.14(a): choked converging nozzle, po=1.0 MPa, To=360 K ---
assert is_choked(500.0e3, 1.0e6, 1.4) is True;  _n += 1     # pB=500 < p*=528 -> choked
assert is_choked(784.0e3, 1.0e6, 1.4) is False; _n += 1     # pB=784 > p*=528 -> subsonic
chk("Ex9.14a p*", critical_pressure_ratio(1.4) * 1.0e6, 528.0e3, 300.0)
T2a = critical_temperature_ratio(1.4) * 360.0
chk("Ex9.14a T2", T2a, 300.0, 0.1)
V2a = speed_of_sound_ideal_gas(1.4, R, T2a)
chk("Ex9.14a V2", V2a, 347.2, 0.2)
chk("Ex9.14a mdot", (critical_pressure_ratio(1.4) * 1.0e6) * 0.001 * V2a / (R * T2a), 2.13, 0.01)
# --- Example 9.15(c): supersonic exit of C-D nozzle, A2/A*=2.4 ---
M2c = mach_from_area_ratio(2.4, 1.4, supersonic=True)
chk("Ex9.15c M2", M2c, 2.4, 0.01)
chk("Ex9.15c p2", (1.0 / stagnation_pressure_ratio(2.4, 1.4)) * 100.0, 6.84, 0.01)
# --- inverse maps recover Table 9.2 Mach numbers ---
chk("M from p/po (M=0.6)", mach_from_pressure_ratio(1.0 / 0.78400, 1.4), 0.6, 1e-3)
chk("M from A/A* subsonic", mach_from_area_ratio(1.3398, 1.4, supersonic=False), 0.5, 1e-3)
chk("M from A/A* supersonic", mach_from_area_ratio(1.6875, 1.4, supersonic=True), 2.0, 1e-3)
# --- Mach number sanity ---
chk("Mach supersonic", mach_number(694.36, 347.18), 2.0, 1e-3)

print(f"All {_n} tests passed.")
