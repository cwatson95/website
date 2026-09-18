"""test_heat_exchanger.py — checks for Module 08.3.  Run: python3 test_heat_exchanger.py
Values reproduce Moran 8e Example 4.7 (power-plant condenser as a two-stream exchanger)."""
import math
from heat_exchanger import (energy_balance_residual, mass_flow_ratio_cold_to_hot,
                            mass_flow_other, heat_duty, sensible_enthalpy_change,
                            enthalpy_two_phase)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# --- Example 4.7: condensing steam (hot) vs cooling water (cold) ---
h_hi = enthalpy_two_phase(191.83, 2584.7, 0.95)          # 2465.1 (0.1 bar, x=0.95)
h_ho = 188.45                                             # hf(45 C)
dcold = 62.7                                              # h_co - h_ci (water 20->35 C)
ratio = mass_flow_ratio_cold_to_hot(h_hi, h_ho, 0.0, dcold)
chk("Ex4.7 mdot_c/mdot_h", ratio, 36.3, 0.05)            # book 36.3
# whole-exchanger energy balance closes when Qcv = Wcv = 0
chk("Ex4.7 balance residual", energy_balance_residual(1.0, h_hi, h_ho, ratio, 0.0, dcold), 0.0,
    1e-9)
# Quick Quiz: mdot_steam = 125 kg/s -> cooling water
chk("Ex4.7 cooling water @125", mass_flow_other(125.0, h_hi - h_ho, dcold), 4538.0, 1.0)
# hot stream gives up exactly what the cold stream takes up
chk("hot duty = -cold duty", heat_duty(1.0, h_hi, h_ho), -heat_duty(ratio, 0.0, dcold), 1e-9)
assert heat_duty(1.0, h_hi, h_ho) < 0.0; _n += 1         # hot stream loses energy
assert heat_duty(ratio, 0.0, dcold) > 0.0; _n += 1       # cold stream gains energy

# --- sensible (constant-cp) ratio: air cools oil, energy balance in T terms ---
# oil c=2 kJ/kg.K, 450->350 K, mdot=10; water c=4.18, 20->? ; just exercise the helpers
dh_oil = sensible_enthalpy_change(2.0, 450.0, 350.0)     # -200 kJ/kg (hot, loses)
chk("oil dh", dh_oil, -200.0)
dh_water = sensible_enthalpy_change(4.18, 20.0, 60.0)    # +167.2 kJ/kg
chk("water dh", dh_water, 167.2)
# mdot_water that absorbs the oil's 10 kg/s * 200 kJ/kg = 2000 kW
mdot_w = mass_flow_other(10.0, 200.0, 167.2)
chk("mdot_water", mdot_w, 2000.0 / 167.2, 1e-9)
chk("balance closes (cp form)",
    energy_balance_residual(10.0, 2.0 * 450.0, 2.0 * 350.0, mdot_w, 4.18 * 20.0, 4.18 * 60.0),
    0.0, 1e-9)

print(f"All {_n} tests passed.")
