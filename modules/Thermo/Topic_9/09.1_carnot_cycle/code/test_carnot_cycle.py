"""test_carnot_cycle.py — checks for Module 09.1.  Run: python3 test_carnot_cycle.py"""
import math
from carnot_cycle import (carnot_efficiency, carnot_efficiency_from_heat,
                          carnot_cop_refrigerator, carnot_cop_heat_pump,
                          max_work_from_heat, min_work_heat_pump,
                          efficiency_is_possible)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# Carnot efficiency -- book-verified Examples 5.1 (80%) and the 3.3 value (60%)
chk("eta 2000/400 = 0.80", carnot_efficiency(400.0, 2000.0), 0.80)        # Moran Ex 5.1
chk("eta 745/298 = 0.60", carnot_efficiency(298.0, 745.0), 0.60)          # module 3.3
chk("eta_from_heat (rev) 400/2000", carnot_efficiency_from_heat(400.0, 2000.0), 0.80)
# Carnot COPs -- Examples 5.2 and 5.3
chk("beta_max 268/295 = 9.93", carnot_cop_refrigerator(268.0, 295.0), 268.0/27.0)   # Ex 5.2 -> 9.9
chk("gamma_max 492/530 = 13.95", carnot_cop_heat_pump(492.0, 530.0), 530.0/38.0)    # Ex 5.3
chk("gamma = beta + 1", carnot_cop_heat_pump(250.0, 300.0),
    carnot_cop_refrigerator(250.0, 300.0) + 1.0)
# work bounds
chk("W_max", max_work_from_heat(1000.0, 400.0, 2000.0), 800.0)
chk("W_min heat pump", min_work_heat_pump(5.0e5, 492.0, 530.0), 5.0e5/(530.0/38.0))  # Ex 5.3 -> 3.58e4
# Carnot is the CEILING for every Topic-9 cycle (second-law corollary)
assert efficiency_is_possible(0.565, 400.0, 2000.0) is True;   _n += 1   # real Otto, below 0.80
assert efficiency_is_possible(0.80, 400.0, 2000.0) is True;    _n += 1   # reversible limit
assert efficiency_is_possible(0.85, 400.0, 2000.0) is False;   _n += 1   # impossible
# monotonicity: efficiency rises as T_H rises / T_C falls
assert carnot_efficiency(400.0, 2200.0) > carnot_efficiency(400.0, 2000.0);  _n += 1
assert carnot_efficiency(350.0, 2000.0) > carnot_efficiency(400.0, 2000.0);  _n += 1

print(f"All {_n} tests passed.")
