"""test_steady_state.py — checks for Module 6.4.  Run: python3 test_steady_state.py"""
import math
from steady_state import (steady_mass_residual, is_steady, delta_ke,
                          heat_rate_steady, power_rate_steady, turbine_power_adiabatic)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# steady-state mass: in == out
chk("mass residual zero", steady_mass_residual([40.0, 14.15], [54.15]), 0.0, 1e-9)
chk("mass residual nonzero", steady_mass_residual([30.0], [12.0]), 18.0)
assert is_steady(0.0, 0.0) is True;     _n += 1
assert is_steady(1e-12, 0.0) is True;   _n += 1
assert is_steady(0.5, 0.0) is False;    _n += 1

# specific kinetic-energy change (Ex 4.4): (30^2 - 10^2)/2 = 400 J/kg = 0.4 kJ/kg
chk("delta_ke Ex4.4", delta_ke(10.0, 30.0), 0.4, 1e-9)

# Example 4.4 -- steam turbine, steady (p.188-189)
mdot = 4600.0 / 3600.0
Qcv = heat_rate_steady(1000.0, mdot, 3177.2, 2345.4, V1=10.0, V2=30.0)
chk("Ex4.4 Qcv", Qcv, -62.3, 0.1)
# neglecting KE the book gets -62.9 kW
chk("Ex4.4 Qcv no-KE", heat_rate_steady(1000.0, mdot, 3177.2, 2345.4), -62.9, 0.1)
# energy balance is consistent: solving for power recovers the given 1000 kW
chk("Ex4.4 power back-solve", power_rate_steady(Qcv, mdot, 3177.2, 2345.4, V1=10.0, V2=30.0), 1000.0, 1e-6)

# adiabatic turbine special case Wdot = mdot (h1 - h2)
chk("turbine adiabatic", turbine_power_adiabatic(2.0, 3015.4, 2431.7), 2.0 * (3015.4 - 2431.7))
# heat_rate_steady with all KE/PE zero reduces to Wdot + mdot(h2-h1)
chk("heat reduces", heat_rate_steady(100.0, 2.0, 500.0, 450.0), 100.0 + 2.0 * (450.0 - 500.0))
# potential-energy term: 10 m drop, mdot=1 -> g*(z2-z1)/1000 contributes
chk("dpe term", heat_rate_steady(0.0, 1.0, 100.0, 100.0, z1=10.0, z2=0.0), 9.81 * (0.0 - 10.0) / 1000.0)

print(f"All {_n} tests passed.")
