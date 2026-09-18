"""test_wet_bulb.py — checks for Module 11.2.  Run: python3 test_wet_bulb.py"""
import math
from wet_bulb import (humidity_ratio_at_saturation, humidity_ratio_from_wet_bulb,
                      adiabatic_saturator_residual, dry_air_enthalpy, state_enthalpy,
                      dew_point_pressure, exit_humidity_ratio)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# Eq. 12.49 omega' (saturated exit): pg(10 C)=1.228 kPa, p=101.325 kPa
wprime = humidity_ratio_at_saturation(1.228, 101.325)
chk("omega' (10C)", wprime, 0.007631, 1e-5)
# at saturation pv = pg, so Eq. 12.49 == Eq. 12.43 with pv=pg
chk("omega' == 0.622 pg/(p-pg)", wprime, 0.622 * 1.228 / (101.325 - 1.228), 1e-9)

# Eq. 12.48 self-consistency: T = Tas (incoming air already saturated) -> omega = omega'
w_sc = humidity_ratio_from_wet_bulb(0.02, 30.0, 30.0, 100.0, 2550.0, 2550.0)
chk("Eq12.48 T=Tas", w_sc, 0.02)

# Eq. 12.48 worked: T=40 C, Tas=25 C with table data (ha = cpa*T datum)
ha_T, ha_Tas = dry_air_enthalpy(40), dry_air_enthalpy(25)
hf25, hg25, hg40 = 104.89, 2547.2, 2574.3
wp = humidity_ratio_at_saturation(3.169, 101.325)        # pg(25 C)=3.169 kPa
chk("omega'(25C)", wp, 0.020082, 1e-5)
omega = humidity_ratio_from_wet_bulb(wp, ha_T, ha_Tas, hf25, hg25, hg40)
chk("omega (40C/25C)", omega, 0.013757, 1e-4)
# Eq. 12.50 residual is zero at the Eq. 12.48 solution
chk("Eq12.50 residual=0", adiabatic_saturator_residual(omega, wp, ha_T, ha_Tas, hg40, hg25, hf25), 0.0, 1e-9)

# chart enthalpy datum (Eq. 12.51)
chk("ha = cpa*T", dry_air_enthalpy(22.0), 22.11, 1e-9)
chk("ha(0C)=0", dry_air_enthalpy(0.0), 0.0)
# Ex 12.12 inlet chart enthalpy (ha+omega*hg) = 27.2 kJ/kg(dry air)
chk("Ex12.12 inlet h ~ 27.2", state_enthalpy(dry_air_enthalpy(22), 0.002, 2541.7), 27.2, 0.05)

# dew point pv: Example 12.7 (omega=0.010947, p=14.7) -> pv1 = 0.2542 (Tsat ~ 60 F)
chk("dew pt pv (Ex12.7)", dew_point_pressure(0.010947, 14.7), 0.2542, 1e-3)

# Example 12.12 mass balance: omega2 = omega1 + mst/ma = 0.002 + (52/60)/90 = 0.0116
chk("Ex12.12 omega2", exit_humidity_ratio(0.002, 52.0 / 60.0, 90.0), 0.0116, 5e-4)

print(f"All {_n} tests passed.")
