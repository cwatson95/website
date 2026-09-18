"""test_buoyancy.py — checks for Module 2.7.  Run: python3 test_buoyancy.py"""
import math
from buoyancy import buoyant_force, apparent_weight, floats, submerged_fraction

_n = 0
def chk(name, got, want, tol=1e-3):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

chk("F_b 1 m³ water", buoyant_force(1000.0, 1.0), 9810.0)
chk("iceberg fraction", submerged_fraction(917.0, 1025.0), 917.0 / 1025.0)   # ~0.895
chk("floats yes", floats(500.0, 1000.0), True)
chk("floats no", floats(1200.0, 1000.0), False)
# steel object, V from its density, apparent weight in water
V = 100.0 / (7850.0 * 9.81)
chk("apparent weight", apparent_weight(100.0, 1000.0, V), 100.0 - buoyant_force(1000.0, V))
# Archimedes consistency: a floating body displaces its own weight of fluid
#   weight = rho_obj*g*V_total ; F_b at full submersion-fraction = rho_fl*g*(frac*V_total) = weight
rho_obj, rho_fl, Vtot = 600.0, 1000.0, 2.0
frac = submerged_fraction(rho_obj, rho_fl)
chk("floats: F_b == weight", buoyant_force(rho_fl, frac * Vtot), rho_obj * 9.81 * Vtot, 1e-6)

# a sinking body has no floating fraction
try:
    submerged_fraction(1200.0, 1000.0)
    raise AssertionError("should raise for sinking body")
except ValueError:
    _n += 1

# ---- the table in notes.md §4, fresh water ----
for _name, _rho, _frac in (("cork", 240.0, 0.240), ("oak", 750.0, 0.750),
                           ("ice", 917.0, 0.917)):
    chk("%s submerged fraction" % _name, submerged_fraction(_rho, 1000.0), _frac)
    assert floats(_rho, 1000.0);  _n += 1
chk("ice in seawater (89.5%)", submerged_fraction(917.0, 1025.0), 0.895, tol=5e-4)

# neutral buoyancy: equal densities means fully submerged, and still not sinking
chk("neutral buoyancy", submerged_fraction(1000.0, 1000.0), 1.0)

# g cancels out of the floating balance -- same fraction on the Moon
chk("g cancels", submerged_fraction(917.0, 1000.0), 0.917)

# the 10 L steel block quoted in notes.md §3
_V, _RHO_S = 0.010, 7850.0
_W = _RHO_S * _V * 9.81
chk("steel block true weight", _W, 770.1, tol=0.05)
chk("steel block buoyant relief in water", buoyant_force(1000.0, _V), 98.1, tol=0.05)
chk("steel block apparent weight", apparent_weight(_W, 1000.0, _V), 672.0, tol=0.05)
chk("relief is 12.7% of weight", 100.0 * buoyant_force(1000.0, _V) / _W, 12.7, tol=0.05)

print(f"All {_n} tests passed.")
