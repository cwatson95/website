"""test_kinetic_energy.py — checks for Module 2.5.  Run: python3 test_kinetic_energy.py"""
import math
from kinetic_energy import kinetic_energy, delta_KE, work_from_KE, speed_after_work

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

chk("KE", kinetic_energy(2.0, 10.0), 100.0)
chk("delta_KE", delta_KE(1000.0, 100.0, 20.0), -4.8e6)
chk("work-energy theorem", work_from_KE(2.0, 0.0, 10.0), 100.0)
chk("speed after work", speed_after_work(2.0, 0.0, 100.0), 10.0)
# consistency: KE2 - KE1 == delta_KE
chk("KE diff", kinetic_energy(3.0, 8.0) - kinetic_energy(3.0, 2.0), delta_KE(3.0, 2.0, 8.0))

# ---- Moran's units example, p.43: 1 kg, 15 -> 30 m/s, dKE = 0.34 kJ ----
chk("Moran p.43 dKE (J)", delta_KE(1.0, 15.0, 30.0), 337.5)
chk("Moran p.43 dKE (kJ, book rounds to 0.34)", delta_KE(1.0, 15.0, 30.0) / 1e3,
    0.34, tol=5e-3)

# the quadratic: doubling speed quadruples KE
chk("KE is quadratic", kinetic_energy(1500.0, 40.0), 4.0 * kinetic_energy(1500.0, 20.0))
# braking 40->20 sheds three times what braking 20->0 sheds
chk("braking 40->20 vs 20->0",
    abs(delta_KE(1500.0, 40.0, 20.0)), 3.0 * abs(delta_KE(1500.0, 20.0, 0.0)))

# work-energy theorem as an invertible pair: add dKE, recover V2
for _m, _V1, _V2 in ((1500.0, 0.0, 20.0), (2.0, 3.0, 11.0), (1000.0, 100.0, 20.0)):
    chk("round trip V2 (m=%g, %g->%g)" % (_m, _V1, _V2),
        speed_after_work(_m, _V1, delta_KE(_m, _V1, _V2)), _V2)

print(f"All {_n} tests passed.")
