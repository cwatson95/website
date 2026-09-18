"""test_mass_conservation.py — checks for Module 6.5.  Run: python3 test_mass_conservation.py"""
import math
from mass_conservation import (mass_flow_rate, mass_flow_rate_rho, mdot_from_volumetric,
                               velocity_from_mdot, dmcv_dt, steady_mass_residual,
                               is_steady_mass)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# mass flow rate: rho A V  ==  A V / v   (v = 1/rho)
chk("mdot AV/v", mass_flow_rate(0.0025, 30.0, 0.2392), 0.0025 * 30.0 / 0.2392)
chk("mdot rhoAV vs AV/v", mass_flow_rate_rho(1.0 / 0.2392, 0.0025, 30.0),
    mass_flow_rate(0.0025, 30.0, 0.2392))
chk("mdot from volumetric", mdot_from_volumetric(0.06, 1.108e-3), 54.1516, 1e-3)
# velocity inversion is consistent with mass_flow_rate
chk("V from mdot", velocity_from_mdot(mass_flow_rate(0.0025, 30.0, 0.2392), 0.2392, 0.0025), 30.0)

# Example 4.1 -- feedwater heater, steady (p.174-175)
mdot3 = mdot_from_volumetric(0.06, 1.108e-3)
mdot2 = mdot3 - 40.0
V2 = velocity_from_mdot(mdot2, 1.0078e-3, 25e-4)
chk("Ex4.1 mdot3", mdot3, 54.15, 0.01)
chk("Ex4.1 mdot2", mdot2, 14.15, 0.01)
chk("Ex4.1 V2", V2, 5.7, 0.05)
# mass rate balance is satisfied at steady state: in == out
chk("Ex4.1 balance", dmcv_dt([40.0, mdot2], [mdot3]), 0.0, 1e-9)
assert is_steady_mass([40.0, mdot2], [mdot3]) is True;  _n += 1

# mass rate balance, general (transient): dmcv/dt = sum in - sum out
chk("dmcv/dt transient", dmcv_dt([30.0], [12.0]), 18.0)
chk("steady residual nonzero", steady_mass_residual([30.0], [12.0]), 18.0)
assert is_steady_mass([30.0], [12.0]) is False;  _n += 1

# Example 4.2 -- barrel steady height: mdot_e = mdot_i  ->  9 L = 30  ->  L = 3.33 ft (p.176)
L_ss = 30.0 / 9.0
chk("Ex4.2 L_steady", L_ss, 3.333, 1e-3)

print(f"All {_n} tests passed.")
