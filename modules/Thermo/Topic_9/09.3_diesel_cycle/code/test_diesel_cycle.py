"""test_diesel_cycle.py — checks for Module 09.3.  Run: python3 test_diesel_cycle.py"""
import math
from diesel_cycle import (diesel_efficiency, diesel_efficiency_air_table,
                          cutoff_ratio, temp_after_isentropic_compression,
                          temp_after_constant_pressure_heat,
                          temp_after_isentropic_expansion)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# Air-table efficiency -- Example 9.2 (book 0.578)
chk("eta air-table = 0.578",
    diesel_efficiency_air_table(214.07, 664.3, 930.98, 1999.1), 0.578, 0.001)
# Cold air-standard closed form for the same r, rc (Eq. 9.13)
chk("eta cold (r=18, rc=2)", diesel_efficiency(18.0, 2.0), 0.6316, 0.001)
# the cold closed form overpredicts the air-table value (constant cp)
assert diesel_efficiency(18.0, 2.0) > diesel_efficiency_air_table(214.07, 664.3, 930.98, 1999.1);  _n += 1
# Example 9.2 state temperatures (cold air-standard helpers)
T2 = temp_after_isentropic_compression(300.0, 18.0)
chk("T3 = rc*T2", temp_after_constant_pressure_heat(T2, 2.0), 2.0 * T2)
chk("cutoff ratio", cutoff_ratio(0.1220, 0.0610), 2.0)
chk("T4 = T3 (rc/r)^(k-1)", temp_after_isentropic_expansion(1800.0, 18.0, 2.0, 1.4),
    1800.0 * (2.0/18.0) ** 0.4)
# limit: as rc -> 1 the Diesel cycle reduces to the Otto cycle (Eq. 9.8)
chk("rc->1 reduces to Otto", diesel_efficiency(18.0, 1.0 + 1e-9), 1.0 - 1.0/18.0**0.4, 1e-4)
# for the SAME r, Diesel (rc>1) is LESS efficient than Otto (Moran p.520)
assert diesel_efficiency(18.0, 2.0) < (1.0 - 1.0/18.0**0.4);  _n += 1
# efficiency rises with r, falls with cutoff ratio
assert diesel_efficiency(21.0, 2.0) > diesel_efficiency(15.0, 2.0);  _n += 1
assert diesel_efficiency(18.0, 3.0) < diesel_efficiency(18.0, 2.0);  _n += 1

print(f"All {_n} tests passed.")
