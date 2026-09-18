"""
test_equations.py  —  checks for Module 11.EQ.

(1) each canonical Topic-11 (psychrometric) equation reproduces a known value;
(2) CROSS-CHECK -- the concept modules 11.1 (dry_bulb) and 11.2 (wet_bulb) compute the
    same things, so the moist-air equations are used consistently across the whole topic.
    A formula change in either concept module fails this test.

Run:  cd code && python3 test_equations.py   ->  "All N tests passed."
"""
import math
import os
import sys

import equations as eq

_HERE = os.path.dirname(os.path.abspath(__file__))
for _s in ("11.1_dry_bulb_temperature", "11.2_wet_bulb_temperature"):
    sys.path.insert(0, os.path.join(_HERE, "..", "..", _s, "code"))
import dry_bulb        # noqa: E402  (11.1)
import wet_bulb        # noqa: E402  (11.2)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1


# ---- (1) canonical values --------------------------------------------------
chk("12.42 omega def", eq.humidity_ratio(0.0109, 0.9891), 0.011, 5e-4)
chk("12.43 omega(pv)", eq.humidity_ratio_from_pressures(0.2542, 14.7), 0.011, 5e-4)
chk("12.44 phi", eq.relative_humidity(0.2542, 0.3632), 0.70, 1e-3)
chk("12.44i pv=phi*pg", eq.vapor_pressure_from_phi(0.70, 0.3632), 0.25424, 1e-4)
# round trip: pv -> omega -> pv (Eq. 12.43 and its inverse)
_w = eq.humidity_ratio_from_pressures(0.2542, 14.7)
chk("12.43 round trip", eq.vapor_pressure_from_ratio(_w, 14.7), 0.2542, 1e-4)
chk("12.46 h per dry air", eq.mixture_enthalpy_per_dry_air(22.11, 0.002, 2541.7), 27.193, 1e-3)
chk("12.45 H == ma*h", eq.mixture_enthalpy_total(0.9891, 22.11, 0.9891 * 0.002, 2541.7),
    0.9891 * eq.mixture_enthalpy_per_dry_air(22.11, 0.002, 2541.7), 1e-9)
chk("12.47 hv~hg", eq.vapor_enthalpy_approx(2541.7), 2541.7)
chk("12.49 omega'(25C)", eq.humidity_ratio_at_saturation(3.169, 101.325), 0.020082, 1e-5)
_wp = eq.humidity_ratio_at_saturation(3.169, 101.325)
_omega = eq.humidity_ratio_from_wet_bulb(_wp, eq.dry_air_enthalpy(40), eq.dry_air_enthalpy(25),
                                         104.89, 2547.2, 2574.3)
chk("12.48 omega(40C/25C)", _omega, 0.013757, 1e-4)
chk("12.50 residual=0", eq.adiabatic_saturator_residual(
    _omega, _wp, eq.dry_air_enthalpy(40), eq.dry_air_enthalpy(25), 2574.3, 2547.2, 104.89), 0.0, 1e-9)
chk("12.51 ha=cpa*T", eq.dry_air_enthalpy(22.0), 22.11, 1e-9)
chk("12.51 ha(0C)=0", eq.dry_air_enthalpy(0.0), 0.0)
# Eq. 12.52 water mass balance: Ex 12.12 steam rate = ma(omega2-omega1)
chk("12.52 mw", eq.water_mass_balance(90.0, 0.002, 0.0116), 0.864, 1e-9)

# ---- (2) cross-checks: concept modules match the registry ------------------
# 11.1 dry_bulb
chk("11.1 omega def", dry_bulb.humidity_ratio(0.0109, 0.9891), eq.humidity_ratio(0.0109, 0.9891))
chk("11.1 omega(pv)", dry_bulb.humidity_ratio_from_pressures(0.2542, 14.7),
    eq.humidity_ratio_from_pressures(0.2542, 14.7))
chk("11.1 phi", dry_bulb.relative_humidity(0.2542, 0.3632), eq.relative_humidity(0.2542, 0.3632))
chk("11.1 pv=phi*pg", dry_bulb.vapor_pressure_from_phi(0.70, 0.3632),
    eq.vapor_pressure_from_phi(0.70, 0.3632))
chk("11.1 pv(omega)", dry_bulb.vapor_pressure_from_ratio(0.011, 14.7),
    eq.vapor_pressure_from_ratio(0.011, 14.7))
chk("11.1 H total", dry_bulb.mixture_enthalpy_total(0.9891, 22.11, 0.00198, 2541.7),
    eq.mixture_enthalpy_total(0.9891, 22.11, 0.00198, 2541.7))
chk("11.1 h per dry air", dry_bulb.mixture_enthalpy_per_dry_air(22.11, 0.002, 2541.7),
    eq.mixture_enthalpy_per_dry_air(22.11, 0.002, 2541.7))
chk("11.1 hv~hg", dry_bulb.vapor_enthalpy_approx(2541.7), eq.vapor_enthalpy_approx(2541.7))
# 11.2 wet_bulb
chk("11.2 omega'", wet_bulb.humidity_ratio_at_saturation(3.169, 101.325),
    eq.humidity_ratio_at_saturation(3.169, 101.325))
chk("11.2 omega(Tas)", wet_bulb.humidity_ratio_from_wet_bulb(_wp, eq.dry_air_enthalpy(40),
    eq.dry_air_enthalpy(25), 104.89, 2547.2, 2574.3),
    eq.humidity_ratio_from_wet_bulb(_wp, eq.dry_air_enthalpy(40), eq.dry_air_enthalpy(25),
    104.89, 2547.2, 2574.3))
chk("11.2 residual", wet_bulb.adiabatic_saturator_residual(_omega, _wp, eq.dry_air_enthalpy(40),
    eq.dry_air_enthalpy(25), 2574.3, 2547.2, 104.89),
    eq.adiabatic_saturator_residual(_omega, _wp, eq.dry_air_enthalpy(40), eq.dry_air_enthalpy(25),
    2574.3, 2547.2, 104.89))
chk("11.2 ha=cpa*T", wet_bulb.dry_air_enthalpy(22.0), eq.dry_air_enthalpy(22.0))
# 11.2 state_enthalpy is the Eq. 12.46 form (ha + omega*hg)
chk("11.2 state_enthalpy == 12.46", wet_bulb.state_enthalpy(22.11, 0.002, 2541.7),
    eq.mixture_enthalpy_per_dry_air(22.11, 0.002, 2541.7))
# 11.2 dew-point pv is the Eq. 12.43 inverse (same as 11.1 vapor_pressure_from_ratio)
chk("11.2 dew pv == 12.43i", wet_bulb.dew_point_pressure(0.010947, 14.7),
    eq.vapor_pressure_from_ratio(0.010947, 14.7))
# 11.1 and 11.2 agree on the shared pv<->omega inversion (the bridge between the modules)
chk("11.1 pv == 11.2 dew pv", dry_bulb.vapor_pressure_from_ratio(0.0116, 100.0),
    wet_bulb.dew_point_pressure(0.0116, 100.0))
# 11.2 exit_humidity_ratio inverts Eq. 12.52: adding mw to ma gives omega2; balance returns mw
_w2 = wet_bulb.exit_humidity_ratio(0.002, 0.864, 90.0)
chk("11.2 exit omega2", _w2, 0.0116, 1e-9)
chk("12.52 inverts exit", eq.water_mass_balance(90.0, 0.002, _w2), 0.864, 1e-9)

print(f"All {_n} tests passed.")
