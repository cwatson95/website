"""test_potential_energy.py — checks for Module 2.6.  Run: python3 test_potential_energy.py"""
import math
from potential_energy import potential_energy, delta_PE, work_by_gravity

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

chk("PE", potential_energy(2.0, 10.0), 196.2)
chk("delta_PE", delta_PE(10.0, 0.0, 50.0), 4905.0)
chk("work by gravity (falling)", work_by_gravity(10.0, 50.0, 0.0), 4905.0)   # +ve, gravity does work
chk("work by gravity (rising)", work_by_gravity(10.0, 0.0, 50.0), -4905.0)
# consistency: PE2 - PE1 == delta_PE
chk("PE diff", potential_energy(2.0, 30.0) - potential_energy(2.0, 10.0), delta_PE(2.0, 10.0, 30.0))

# ---- Moran's units example, p.43: 1 kg descends 10 m at g = 9.7 -> -0.10 kJ ----
chk("Moran p.43 dPE (J)", delta_PE(1.0, 0.0, -10.0, 9.7), -97.0)
chk("Moran p.43 dPE (kJ, book rounds to -0.10)",
    delta_PE(1.0, 0.0, -10.0, 9.7) / 1e3, -0.10, tol=5e-3)

# gravity is conservative: W_grav = -dPE for any pair of elevations
for _z1, _z2 in ((0.0, 50.0), (50.0, 0.0), (-12.0, 7.5)):
    chk("W_grav = -dPE (%g->%g)" % (_z1, _z2),
        work_by_gravity(10.0, _z1, _z2), -delta_PE(10.0, _z1, _z2))

# the datum cancels: the SAME 30 m fall scored against three different zeros
_ref = delta_PE(200.0, 40.0, 10.0)
for _datum in (0.0, 10.0, 25.0):
    chk("datum independence (z0=%g)" % _datum,
        delta_PE(200.0, 40.0 - _datum, 10.0 - _datum), _ref)
# ...while the absolute PE emphatically does not cancel
assert potential_energy(200.0, 40.0) != potential_energy(200.0, 40.0 - 25.0);  _n += 1

print(f"All {_n} tests passed.")
