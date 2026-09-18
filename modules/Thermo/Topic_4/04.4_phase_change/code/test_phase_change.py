"""test_phase_change.py — checks for Module 4.4.  Run: python3 test_phase_change.py"""
import math
from phase_change import (quality, mixture_property, quality_from_property,
                          latent_heat, mass_from_volume, liquid_volume_fraction)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# quality definition
chk("x def", quality(55.6, 79.44), 0.7, 0.01)
chk("x=0 sat liq", quality(0.0, 50.0), 0.0)
chk("x=1 sat vap", quality(50.0, 50.0), 1.0)
# mixture relation and its inverse (water @100 C, x=0.9)
chk("v mixture", mixture_property(1.0435e-3, 1.673, 0.9), 1.506, 1e-3)
chk("x from v", quality_from_property(1.506, 1.0435e-3, 1.673), 0.9, 1e-3)
chk("yf at x=0", mixture_property(1.0435e-3, 1.673, 0.0), 1.0435e-3)
chk("yg at x=1", mixture_property(1.0435e-3, 1.673, 1.0), 1.673)
# latent heat
chk("hfg water 100C", latent_heat(419.04, 2676.1), 2257.06, 0.05)
# HW 3.16 -- CO2 tank
vf, vg, x = 0.9827e-3, 1.756e-2, 0.7
chk("CO2 v", mixture_property(vf, vg, x), 0.012588, 1e-5)
chk("CO2 mass", mass_from_volume(1.0, mixture_property(vf, vg, x)), 79.44, 0.1)
chk("CO2 liquid vol frac", liquid_volume_fraction(x, vf, vg), 0.02342, 1e-4)

print(f"All {_n} tests passed.")
