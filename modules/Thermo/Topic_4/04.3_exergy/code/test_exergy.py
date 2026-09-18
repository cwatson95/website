"""test_exergy.py — checks for Module 4.3.  Run: python3 test_exergy.py"""
import math
from exergy import (specific_exergy, exergy_change, exergy_transfer_heat,
                    exergy_transfer_work, exergy_destruction, exergy_change_incompressible)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# exergy vanishes at the dead state
chk("dead state e=0", specific_exergy(100.0, 0.5, 2.0, 100.0, 0.5, 2.0, 300.0, 101.3), 0.0)
# Example 7.1 -- assemble e from its three verified increments (u-u0, p0(v-v0), T0(s-s0))
chk("Ex7.1 e", specific_exergy(666.28, -0.38253, 0.862073, 0.0, 0.0, 0.0, 300.0, 101.3), 368.91, 0.1)
# Example 7.2 -- reworks Ex 6.1 (water, internally reversible); T0=293.15 K, p0=100 kPa
chk("Ex7.2 Eq/m", exergy_transfer_heat(2114.1, 293.15, 423.15), 649.49, 0.1)
chk("Ex7.2 Ew/m", exergy_transfer_work(186.38, 100.0, 0.39171), 147.21, 0.1)
chk("Ex7.2 Ed/m", exergy_destruction(293.15, 0.0), 0.0)
chk("Ex7.2 de balance", exergy_transfer_heat(2114.1, 293.15, 423.15)
    - exergy_transfer_work(186.38, 100.0, 0.39171), 502.38, 0.2)   # = de (Ed=0)
# Example 7.3 -- oven wall exergy destruction
chk("Ex7.3 Eq1/A", exergy_transfer_heat(0.2, 293.0, 575.0), 0.0981, 1e-3)
chk("Ex7.3 Ed/A", exergy_transfer_heat(0.2, 293.0, 575.0) - exergy_transfer_heat(0.2, 293.0, 310.0), 0.087, 2e-3)
# HW 7.36 -- metal sphere quench: Ed = T0 sigma
chk("HW7.36 Ed", exergy_destruction(537.0, 0.15959), 85.70, 0.1)
# HW 7.32 -- rigid insulated air + paddle (Btu, degR)
sig = 0.5 * 0.171 * math.log(600.0 / 520.0)
chk("HW7.32 Ed", exergy_destruction(537.0, sig), 6.57, 0.02)
chk("HW7.32 Ew", exergy_transfer_work(-6.84, 14.7, 0.0), -6.84)
chk("HW7.32 dE", exergy_change(6.84, 0.0, sig, 537.0, 14.7), 0.27, 0.02)
# HW 7.21 -- warmed concrete slab, then equivalent lifted height
dE = exergy_change_incompressible(16560.0, 0.88, 298.0, 301.0, 298.0)
chk("HW7.21 dE", dE, 218.6, 1.0)
chk("HW7.21 z", dE * 1000.0 / (1000.0 * 9.81), 22.3, 0.1)   # dE [kJ] -> J, /(m g)

print(f"All {_n} tests passed.")
