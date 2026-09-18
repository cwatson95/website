"""test_dry_bulb.py — checks for Module 11.1.  Run: python3 test_dry_bulb.py"""
import math
from dry_bulb import (humidity_ratio, humidity_ratio_from_pressures, relative_humidity,
                      vapor_pressure_from_phi, vapor_pressure_from_ratio,
                      mixture_enthalpy_total, mixture_enthalpy_per_dry_air,
                      vapor_enthalpy_approx, dry_air_mass, vapor_mass)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# humidity ratio definition (Eq. 12.42)
chk("omega def", humidity_ratio(0.0109, 0.9891), 0.011, 5e-4)
# Eq. 12.43 and Example 12.7(a): pv1 = phi*pg = 0.2542, omega1 = 0.011
chk("pv from phi", vapor_pressure_from_phi(0.70, 0.3632), 0.25424, 1e-4)
chk("omega from pv", humidity_ratio_from_pressures(0.25424, 14.7), 0.011, 5e-4)
# the two omega routes agree (round trip pv -> omega -> pv)
chk("pv round trip", vapor_pressure_from_ratio(humidity_ratio_from_pressures(0.25424, 14.7), 14.7), 0.25424, 1e-4)
# relative humidity (Eq. 12.44) and its inverse
chk("phi def", relative_humidity(0.25424, 0.3632), 0.70, 1e-3)
chk("phi=1 saturated", relative_humidity(0.3632, 0.3632), 1.0)
# Example 12.7 second state: omega2 at 40 F (pg=0.1217)
chk("omega2", humidity_ratio_from_pressures(0.1217, 14.7), 0.0052, 5e-4)
# 1-lb sample mass split (Example 12.7)
chk("ma split", dry_air_mass(1.0, 0.011), 0.98912, 5e-4)
chk("mv split", vapor_mass(1.0, 0.011), 0.010880, 5e-4)
chk("masses sum to total", dry_air_mass(1.0, 0.011) + vapor_mass(1.0, 0.011), 1.0)
# mixture enthalpy (Eqs. 12.45/12.46): H/ma == h
chk("h per dry air", mixture_enthalpy_per_dry_air(22.11, 0.002, 2541.7), 27.193, 1e-3)
chk("H total == ma*h", mixture_enthalpy_total(0.9891, 22.11, 0.9891 * 0.002, 2541.7),
    0.9891 * mixture_enthalpy_per_dry_air(22.11, 0.002, 2541.7), 1e-6)
# Ex 12.12 inlet chart enthalpy 27.2 kJ/kg(dry air) using ha = cpa*T (datum Eq. 12.51)
chk("Ex12.12 inlet h ~ 27.2", mixture_enthalpy_per_dry_air(1.005 * 22.0, 0.002, 2541.7), 27.2, 0.05)
# Eq. 12.47 approximation is the identity hv = hg(T)
chk("hv ~ hg", vapor_enthalpy_approx(2541.7), 2541.7)

print(f"All {_n} tests passed.")
