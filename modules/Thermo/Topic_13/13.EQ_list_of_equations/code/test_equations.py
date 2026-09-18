"""
test_equations.py  —  checks for Module 13.EQ.

(1) each canonical Topic-13 equation reproduces a known value;
(2) CROSS-CHECK -- the concept modules 13.1/13.2/13.3/13.4/13.5 compute the same things,
    so the compressible-flow (and cross-trunk pipe-flow) equations are used consistently
    across the whole topic.  A formula change anywhere fails this test.

Run:  cd code && python3 test_equations.py   ->  "All N tests passed."
"""
import math
import os
import sys

import equations as eq

_HERE = os.path.dirname(os.path.abspath(__file__))
for _s in ("13.1_subsonic", "13.2_supersonic", "13.3_shock",
           "13.4_laminar_flow", "13.5_turbulent_flow"):
    sys.path.insert(0, os.path.join(_HERE, "..", "..", _s, "code"))
import subsonic         # noqa: E402  (13.1)
import supersonic       # noqa: E402  (13.2)
import shock            # noqa: E402  (13.3)
import laminar_flow     # noqa: E402  (13.4)
import turbulent_flow   # noqa: E402  (13.5)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1


# ---- (1) canonical values --------------------------------------------------
chk("speed_of_sound air 300K", eq.speed_of_sound_ideal_gas(1.4, 287.0, 300.0), 347.189, 1e-2)
chk("mach_number", eq.mach_number(347.189, 347.189), 1.0)
chk("stagnation_enthalpy", eq.stagnation_enthalpy(3.0e5, 200.0), 3.2e5)
chk("area_change_ratio", eq.area_change_ratio(0.01, 0.5), -0.0075)
chk("stag T ratio M=2", eq.stagnation_temperature_ratio(2.0, 1.4), 1.8)
chk("stag p ratio M=2", eq.stagnation_pressure_ratio(2.0, 1.4), 1.8 ** 3.5)
chk("area_mach M=2", eq.area_mach_ratio(2.0, 1.4), 1.6875, 1e-4)         # Table 9.2
chk("critical p* ratio", eq.critical_pressure_ratio(1.4), 0.52828, 1e-5)  # Table 9.2 @M=1
chk("critical T* ratio", eq.critical_temperature_ratio(1.4), 0.83333, 1e-5)
chk("My after shock Mx=2", eq.mach_after_shock(2.0, 1.4), 0.57735, 1e-5)   # Table 9.3
chk("py/px shock Mx=2", eq.shock_pressure_ratio(2.0, 1.4), 4.5000, 1e-4)
chk("Ty/Tx shock Mx=2", eq.shock_temperature_ratio(2.0, 1.4), 1.6875, 1e-4)
chk("poy/pox shock Mx=2", eq.stagnation_pressure_ratio_across_shock(2.0, 1.4), 0.72088, 1e-5)
chk("reynolds_number", eq.reynolds_number(1000.0, 2.0, 0.05, 1.0e-3), 1.0e5)
chk("friction laminar f=64/Re", eq.friction_factor_laminar(64.0), 1.0)
chk("friction Blasius @1e4", eq.friction_factor_blasius(1.0e4), 0.0316, 1e-4)

# ---- (2) cross-checks: concept modules match the registry ------------------
# 13.1 subsonic
chk("13.1 c", subsonic.speed_of_sound_ideal_gas(1.4, 287.0, 300.0),
    eq.speed_of_sound_ideal_gas(1.4, 287.0, 300.0))
chk("13.1 M", subsonic.mach_number(420.0, 347.0), eq.mach_number(420.0, 347.0))
chk("13.1 To/T", subsonic.stagnation_temperature_ratio(0.6, 1.4),
    eq.stagnation_temperature_ratio(0.6, 1.4))
chk("13.1 po/p", subsonic.stagnation_pressure_ratio(0.6, 1.4),
    eq.stagnation_pressure_ratio(0.6, 1.4))
chk("13.1 dA/A", subsonic.area_change_ratio(0.01, 0.5), eq.area_change_ratio(0.01, 0.5))
# 13.2 supersonic
chk("13.2 A/A*", supersonic.area_mach_ratio(2.4, 1.4), eq.area_mach_ratio(2.4, 1.4))
chk("13.2 p*/po", supersonic.critical_pressure_ratio(1.4), eq.critical_pressure_ratio(1.4))
chk("13.2 T*/To", supersonic.critical_temperature_ratio(1.4), eq.critical_temperature_ratio(1.4))
# 13.3 shock
chk("13.3 My", shock.mach_after_shock(2.0, 1.4), eq.mach_after_shock(2.0, 1.4))
chk("13.3 py/px", shock.shock_pressure_ratio(2.0, 1.4), eq.shock_pressure_ratio(2.0, 1.4))
chk("13.3 Ty/Tx", shock.shock_temperature_ratio(2.0, 1.4), eq.shock_temperature_ratio(2.0, 1.4))
chk("13.3 poy/pox", shock.stagnation_pressure_ratio_across_shock(2.0, 1.4),
    eq.stagnation_pressure_ratio_across_shock(2.0, 1.4))
# 13.4 laminar (~CM)
chk("13.4 Re", laminar_flow.reynolds_number(1000.0, 2.0, 0.05, 1.0e-3),
    eq.reynolds_number(1000.0, 2.0, 0.05, 1.0e-3))
chk("13.4 f=64/Re", laminar_flow.friction_factor_laminar(225.0),
    eq.friction_factor_laminar(225.0))
# 13.5 turbulent (~CM)
chk("13.5 Re", turbulent_flow.reynolds_number(1000.0, 2.0, 0.05, 1.0e-3),
    eq.reynolds_number(1000.0, 2.0, 0.05, 1.0e-3))
chk("13.5 Blasius", turbulent_flow.friction_factor_blasius(1.0e4),
    eq.friction_factor_blasius(1.0e4))
# 13.4 and 13.5 agree on Re (same group, the bridge between the two regimes)
chk("13.4 Re == 13.5 Re", laminar_flow.reynolds_number(900.0, 2.0, 0.05, 0.4),
    turbulent_flow.reynolds_number(900.0, 2.0, 0.05, 0.4))

print(f"All {_n} tests passed.")
