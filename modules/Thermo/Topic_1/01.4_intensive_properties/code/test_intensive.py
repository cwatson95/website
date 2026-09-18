"""test_intensive.py — checks for Module 1.4.  Run: python3 test_intensive.py"""
from intensive import (specific, molar, density, specific_volume,
                       mass_average, is_size_independent)

_n = 0


def chk(name, got, want, tol=1e-9):
    global _n
    assert abs(got - want) <= tol, f"{name}: got {got!r}, want {want!r}"
    _n += 1


chk("specific", specific(150.0, 3.0), 50.0)               # u = U/m
chk("molar", molar(100.0, 4.0), 25.0)
chk("specific_volume", specific_volume(1.5, 3.0), 0.5)
chk("density = 1/v", density(3.0, 1.5), 2.0)
chk("v * rho == 1", specific_volume(1.5, 3.0) * density(3.0, 1.5), 1.0)
# intensive property unchanged when the system is scaled up
chk("size-independent", is_size_independent(0.5, specific_volume(3.0, 6.0)), True)
# intensive v MASS-AVERAGES over subsystems (does not add)
chk("mass_average", mass_average([0.5, 2.0], [3.0, 1.0]), 0.875)
# cross-check with module 1.3: extensive V adds to 3.5, so v_mix = 3.5/4 = 0.875
chk("mix == V_total/m_total", mass_average([0.5, 2.0], [3.0, 1.0]), (3 * 0.5 + 1 * 2.0) / 4)

print(f"All {_n} tests passed.")
