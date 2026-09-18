"""test_second_law.py — checks for Module 3.3.  Run: python3 test_second_law.py"""
import math
from second_law import (carnot_efficiency, efficiency_from_heat, kelvin_ratio,
                        carnot_cop_refrigerator, carnot_cop_heat_pump,
                        max_work_from_heat, kelvin_planck_allows,
                        efficiency_is_possible)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# Carnot efficiency -- two book-verified values
chk("eta 745/298 = 0.60", carnot_efficiency(298.0, 745.0), 0.60)      # Moran p.266
chk("eta 2000/400 = 0.80", carnot_efficiency(400.0, 2000.0), 0.80)    # Moran p.266
# Eq 5.4 reduces to Carnot for a reversible cycle (Q_C/Q_H = T_C/T_H)
chk("eta_from_heat 298/745", efficiency_from_heat(298.0, 745.0), 0.60)
chk("kelvin ratio", kelvin_ratio(298.0, 745.0), 0.4)
# COPs and the gamma = beta + 1 identity
chk("COP_ref 250/300", carnot_cop_refrigerator(250.0, 300.0), 5.0)
chk("COP_hp 250/300", carnot_cop_heat_pump(250.0, 300.0), 6.0)
chk("gamma = beta + 1", carnot_cop_heat_pump(250.0, 300.0),
    carnot_cop_refrigerator(250.0, 300.0) + 1.0)
# maximum work from heat
chk("W_max", max_work_from_heat(1000.0, 298.0, 745.0), 600.0)
# Kelvin-Planck predicate (single reservoir: W_cycle <= 0)
assert kelvin_planck_allows(-50.0) is True;        _n += 1
assert kelvin_planck_allows(0.0) is True;          _n += 1
assert kelvin_planck_allows(+50.0) is False;       _n += 1
assert kelvin_planck_allows(+50.0, single_reservoir=False) is True;  _n += 1
# Carnot corollary: eta cannot exceed the Carnot ceiling
assert efficiency_is_possible(0.50, 298.0, 745.0) is True;   _n += 1   # below 0.60
assert efficiency_is_possible(0.60, 298.0, 745.0) is True;   _n += 1   # reversible limit
assert efficiency_is_possible(0.65, 298.0, 745.0) is False;  _n += 1   # impossible

print(f"All {_n} tests passed.")
