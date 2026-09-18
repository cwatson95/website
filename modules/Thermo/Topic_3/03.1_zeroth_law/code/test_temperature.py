"""test_temperature.py — checks for Module 3.1.  Run: python3 test_temperature.py"""
import math
from temperature import (rankine_from_kelvin, kelvin_from_rankine,
                         celsius_from_kelvin, kelvin_from_celsius,
                         fahrenheit_from_rankine, rankine_from_fahrenheit,
                         fahrenheit_from_celsius, celsius_from_fahrenheit,
                         zeroth_law, in_thermal_equilibrium,
                         TRIPLE_POINT_K, STEAM_POINT_K, ABS_ZERO_F)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# absolute <-> absolute
chk("K->R 300", rankine_from_kelvin(300.0), 540.0)
chk("R->K 540", kelvin_from_rankine(540.0), 300.0)
chk("K->R 1200", rankine_from_kelvin(1200.0), 2160.0)
# absolute <-> shifted
chk("K->C 300", celsius_from_kelvin(300.0), 26.85)
chk("C->K 100", kelvin_from_celsius(100.0), 373.15)
chk("K->C 1200", celsius_from_kelvin(1200.0), 926.85)
chk("steam point C", celsius_from_kelvin(STEAM_POINT_K), 100.0)
# Fahrenheit / Celsius
chk("C->F 100", fahrenheit_from_celsius(100.0), 212.0)
chk("F->C 32", celsius_from_fahrenheit(32.0), 0.0)
chk("F->C 212", celsius_from_fahrenheit(212.0), 100.0)
chk("C->F -40 (C==F)", fahrenheit_from_celsius(-40.0), -40.0)
# Rankine / Fahrenheit
chk("R->F 540", fahrenheit_from_rankine(540.0), 80.33)
chk("F->R 80.33", rankine_from_fahrenheit(80.33), 540.0)
# fixed points / constants
chk("abs zero F", ABS_ZERO_F, -459.67)
chk("triple point K", TRIPLE_POINT_K, 273.16)
# zeroth law as a predicate
assert zeroth_law(350.0, 350.0, 350.0) is True;  _n += 1
assert zeroth_law(350.0, 360.0, 350.0) is None;  _n += 1
assert in_thermal_equilibrium(300.0, 300.0) is True;  _n += 1

print(f"All {_n} tests passed.")
