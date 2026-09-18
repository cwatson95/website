"""test_enthalpy.py — checks for Module 4.1.  Run: python3 test_enthalpy.py"""
import math
from enthalpy import (enthalpy, enthalpy_total, enthalpy_molar,
                      internal_energy_from_quality, enthalpy_from_quality,
                      quality_from_enthalpy, const_pressure_heat)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

chk("h water", enthalpy(2537.3, 100.0, 1.793), 2716.6, 0.05)
chk("H total", enthalpy_total(100.0, 200.0, 0.5), 200.0)
chk("h molar", enthalpy_molar(2537.3, 100.0, 1.793), 2716.6, 0.05)
chk("u from x", internal_energy_from_quality(58.77, 230.38, 0.5), 144.575)
chk("h from x", enthalpy_from_quality(59.35, 253.99, 0.5), 156.67, 0.01)
chk("x from h", quality_from_enthalpy(156.67, 59.35, 253.99), 0.5, 1e-4)
chk("x=0 -> hf", enthalpy_from_quality(59.35, 253.99, 0.0), 59.35)
chk("x=1 -> hg", enthalpy_from_quality(59.35, 253.99, 1.0), 253.99)
chk("const-p Q", const_pressure_heat(2939.9, 3531.9, 5.0), 2960.0)

print(f"All {_n} tests passed.")
