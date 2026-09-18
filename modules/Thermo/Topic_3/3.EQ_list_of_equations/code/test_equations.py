"""
test_equations.py  —  checks for Module 3.EQ.

(1) each canonical Topic-3 equation reproduces a known value;
(2) CROSS-CHECK -- the concept modules 3.1/3.2/3.3/3.4 compute the same things, so
    the laws' equations are used consistently across the topic.

Run:  cd code && python3 test_equations.py   ->  "All N tests passed."
"""
import math
import os
import sys

import equations as eq

_HERE = os.path.dirname(os.path.abspath(__file__))
for _s in ("03.1_zeroth_law", "03.2_first_law", "03.3_second_law", "03.4_third_law"):
    sys.path.insert(0, os.path.join(_HERE, "..", "..", _s, "code"))
import temperature   # noqa: E402
import first_law     # noqa: E402
import second_law    # noqa: E402
import third_law     # noqa: E402

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1


# ---- (1) canonical values --------------------------------------------------
chk("rankine_from_kelvin", eq.rankine_from_kelvin(300.0), 540.0)
chk("celsius_from_kelvin", eq.celsius_from_kelvin(300.0), 26.85)
chk("fahrenheit_from_celsius", eq.fahrenheit_from_celsius(100.0), 212.0)
chk("delta_E", eq.delta_E(100.0, 30.0), 70.0)
chk("power_cycle_work", eq.power_cycle_work(1000.0, 600.0), 400.0)
chk("efficiency_from_heat", eq.efficiency_from_heat(298.0, 745.0), 0.60)
chk("kelvin_ratio", eq.kelvin_ratio(298.0, 745.0), 0.40)
chk("carnot_efficiency", eq.carnot_efficiency(400.0, 2000.0), 0.80)
chk("carnot_cop_refrigerator", eq.carnot_cop_refrigerator(250.0, 300.0), 5.0)
chk("carnot_cop_heat_pump", eq.carnot_cop_heat_pump(250.0, 300.0), 6.0)
chk("absolute_entropy_debye", eq.absolute_entropy_debye(10.0, 1e-3), 1.0 / 3.0)
assert eq.standard_entropy_at_zero(True) == 0.0;        _n += 1
assert eq.standard_entropy_at_zero(False) is None;      _n += 1

# ---- (2) cross-checks: concept modules match the registry ------------------
chk("3.1 rankine", temperature.rankine_from_kelvin(300.0), eq.rankine_from_kelvin(300.0))
chk("3.1 celsius", temperature.celsius_from_kelvin(300.0), eq.celsius_from_kelvin(300.0))
chk("3.1 fahrenheit", temperature.fahrenheit_from_celsius(100.0), eq.fahrenheit_from_celsius(100.0))
chk("3.2 delta_E", first_law.delta_E(100.0, 30.0), eq.delta_E(100.0, 30.0))
chk("3.2 power_cycle", first_law.power_cycle_work(1000.0, 600.0), eq.power_cycle_work(1000.0, 600.0))
chk("3.3 carnot_eff", second_law.carnot_efficiency(400.0, 2000.0), eq.carnot_efficiency(400.0, 2000.0))
chk("3.3 eff_from_heat", second_law.efficiency_from_heat(298.0, 745.0), eq.efficiency_from_heat(298.0, 745.0))
chk("3.3 kelvin_ratio", second_law.kelvin_ratio(298.0, 745.0), eq.kelvin_ratio(298.0, 745.0))
chk("3.3 cop_ref", second_law.carnot_cop_refrigerator(250.0, 300.0), eq.carnot_cop_refrigerator(250.0, 300.0))
chk("3.3 cop_hp", second_law.carnot_cop_heat_pump(250.0, 300.0), eq.carnot_cop_heat_pump(250.0, 300.0))
chk("3.4 abs_entropy", third_law.absolute_entropy_debye(10.0, 1e-3), eq.absolute_entropy_debye(10.0, 1e-3))
assert third_law.standard_entropy_at_zero(True) == eq.standard_entropy_at_zero(True);  _n += 1

print(f"All {_n} tests passed.")
