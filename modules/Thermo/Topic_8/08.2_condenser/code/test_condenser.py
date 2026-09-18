"""test_condenser.py — checks for Module 08.2.  Run: python3 test_condenser.py
Values reproduce Moran 8e Example 4.7 (power-plant condenser) and Example 10.4
(heat-pump condenser)."""
import math
from condenser import (heat_transfer_rate, heat_rejected, condenser_heat_per_mass,
                       enthalpy_two_phase, quality_from_h)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# --- two-phase enthalpy / quality (Table A-3 @0.1 bar: hf=191.83, hg=2584.7) ---
chk("h two-phase x=0.95", enthalpy_two_phase(191.83, 2584.7, 0.95), 2465.06, 0.05)  # book 2465.1
chk("x=1 -> hg", enthalpy_two_phase(191.83, 2584.7, 1.0), 2584.7)
chk("x=0 -> hf", enthalpy_two_phase(191.83, 2584.7, 0.0), 191.83)
chk("quality round-trip", quality_from_h(2465.06, 191.83, 2584.7), 0.95, 1e-4)

# --- Example 4.7: power-plant condenser, steam side ---
h1 = enthalpy_two_phase(191.83, 2584.7, 0.95)            # 2465.1 kJ/kg
h2 = 188.45                                               # hf(45 C), Table A-2
chk("Ex4.7 Qcv/m", heat_transfer_rate(1.0, h1, h2), -2276.7, 0.1)   # book -2276.7 kJ/kg
chk("Ex4.7 |q| rejected", heat_rejected(1.0, h1, h2), 2276.7, 0.1)
assert heat_transfer_rate(1.0, h1, h2) < 0.0; _n += 1    # condenser rejects heat
# Quick Quiz: with mdot_steam = 125 kg/s the steam-side heat rate is large & negative
chk("Ex4.7 Qcv at 125 kg/s (MW)", heat_transfer_rate(125.0, h1, h2) / 1e3, -284.6, 0.1)

# --- Example 10.4: heat-pump condenser, h2=280.19, h3=105.29, mdot=0.2 kg/s ---
chk("Ex10.4 Qout (kW)", heat_rejected(0.2, 280.19, 105.29), 34.98, 0.005)   # book 34.98 kW
chk("Ex10.4 per-mass h2-h3", condenser_heat_per_mass(280.19, 105.29), 174.90, 1e-2)
# heat rejected = mdot * (per-mass condenser heat)
chk("Ex10.4 consistency", heat_rejected(0.2, 280.19, 105.29),
    0.2 * condenser_heat_per_mass(280.19, 105.29), 1e-9)

print(f"All {_n} tests passed.")
