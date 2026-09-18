"""test_otto_cycle.py — checks for Module 09.2.  Run: python3 test_otto_cycle.py"""
import math
from otto_cycle import (otto_efficiency, otto_efficiency_air_table,
                        temp_after_isentropic_compression,
                        temp_after_isentropic_expansion,
                        heat_added_cold, net_work_cold, mean_effective_pressure)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# Cold air-standard efficiency -- book-verified comparison table of Example 9.1
chk("eta cold r=8 = 0.565", otto_efficiency(8.0), 0.565, 0.001)        # Moran Ex 9.1 table
chk("T2 cold (540, r=8) = 1241", temp_after_isentropic_compression(540.0, 8.0), 1241.0, 0.6)
chk("T4 cold (3600, r=8) = 1567", temp_after_isentropic_expansion(3600.0, 8.0), 1567.0, 0.6)
# Air-table efficiency -- Example 9.1(b), book 0.51
chk("eta air-table = 0.51", otto_efficiency_air_table(92.04, 211.3, 721.44, 342.2), 0.51, 0.002)
# the two methods bracket each other (constant cv overpredicts)
assert otto_efficiency(8.0) > otto_efficiency_air_table(92.04, 211.3, 721.44, 342.2);  _n += 1
# efficiency increases with compression ratio (Fig. 9.4)
assert otto_efficiency(10.0) > otto_efficiency(8.0) > otto_efficiency(6.0);  _n += 1
# closed form matches the air-table form when fed isentropic-consistent u's:
# with constant cv, u = cv*T, so air-table form reduces to 1 - 1/r^(k-1)
cv, k, r, T1, T3 = 0.718, 1.4, 8.0, 300.0, 1500.0
T2 = temp_after_isentropic_compression(T1, r, k)
T4 = temp_after_isentropic_expansion(T3, r, k)
chk("cold form == air-table(cv*T)",
    otto_efficiency_air_table(cv*T1, cv*T2, cv*T3, cv*T4), otto_efficiency(r, k))
# heat added and net work, cold air-standard (q23 = cv(T3-T2); w = eta*q23)
chk("q23 cold", heat_added_cold(T2, T3, cv), cv * (T3 - T2))
chk("w_net = eta*q23", net_work_cold(r, T1, T3, k, cv),
    otto_efficiency(r, k) * heat_added_cold(T2, T3, cv))
# mean effective pressure: net work over displacement volume
chk("mep", mean_effective_pressure(0.382, 0.02, 0.0025), 0.382 / (0.02 - 0.0025))

print(f"All {_n} tests passed.")
