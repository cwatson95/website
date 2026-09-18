"""test_subsonic.py — checks for Module 13.1.  Run: python3 test_subsonic.py"""
import math
from subsonic import (speed_of_sound_ideal_gas, mach_number, stagnation_enthalpy,
                      stagnation_temperature_ratio, stagnation_pressure_ratio,
                      stagnation_density_ratio, static_temperature_from_stagnation,
                      static_pressure_from_stagnation, area_change_ratio, duct_shape)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

R = 8314.0 / 28.97          # air, J/kg.K

# --- speed of sound, in-text examples (Moran p.570) ---
chk("c air 300K", speed_of_sound_ideal_gas(1.4, R, 300.0), 347.0, 1.0)
chk("c air 650K", speed_of_sound_ideal_gas(1.37, R, 650.0), 506.0, 1.0)
chk("c helium 275K", speed_of_sound_ideal_gas(1.67, 8314.0 / 4.003, 275.0), 977.0, 1.0)
# --- Mach number ---
chk("Mach subsonic", mach_number(220.4, 367.3), 0.6, 1e-3)
chk("Mach sonic", mach_number(347.18, 347.18), 1.0)
# --- stagnation enthalpy ho = h + V^2/2 ---
chk("stagnation enthalpy", stagnation_enthalpy(300000.0, 200.0), 300000.0 + 200.0**2 / 2.0)
# --- stagnation ratios at M=0.6 (Table 9.2: T/To=0.93284, p/po=0.78400) ---
chk("To/T M=0.6", stagnation_temperature_ratio(0.6, 1.4), 1.0 / 0.93284, 1e-4)
chk("po/p M=0.6", stagnation_pressure_ratio(0.6, 1.4), 1.0 / 0.78400, 1e-3)
chk("p/po M=0.6", 1.0 / stagnation_pressure_ratio(0.6, 1.4), 0.78400, 1e-4)
chk("rho_o/rho M=0.6", stagnation_density_ratio(0.6, 1.4),
    stagnation_pressure_ratio(0.6, 1.4) / stagnation_temperature_ratio(0.6, 1.4), 1e-9)
chk("ratios at M=0 are unity", stagnation_pressure_ratio(0.0, 1.4), 1.0)
# --- Example 9.14(b): converging nozzle, po=1.0 MPa, To=360 K, pB=784 kPa (subsonic) ---
M2 = math.sqrt(2.0 / 0.4 * ((1.0e6 / 7.84e5) ** (0.4 / 1.4) - 1.0))
chk("Ex9.14b M2", M2, 0.6, 1e-3)
chk("Ex9.14b T2", static_temperature_from_stagnation(360.0, M2, 1.4), 336.0, 0.3)
chk("Ex9.14b V2", M2 * speed_of_sound_ideal_gas(1.4, R, static_temperature_from_stagnation(360.0, M2, 1.4)),
    220.5, 0.2)
chk("Ex9.14b p2 from po", static_pressure_from_stagnation(1.0e6, 0.6, 1.4), 7.84e5, 500.0)
# --- area-velocity relation, Eq. 9.45, subsonic M<1 (1-M^2>0) ---
chk("dA/A sign subsonic accel", area_change_ratio(+0.01, 0.6), -0.01 * (1.0 - 0.36))
assert duct_shape(+0.01, 0.6) == "converging"; _n += 1      # subsonic nozzle (case 1)
assert duct_shape(-0.01, 0.6) == "diverging";  _n += 1      # subsonic diffuser (case 4)

print(f"All {_n} tests passed.")
