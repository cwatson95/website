"""test_dual_cycle.py — checks for Module 09.4.  Run: python3 test_dual_cycle.py"""
import math
from dual_cycle import (dual_efficiency, dual_efficiency_air_table,
                        pressure_ratio, cutoff_ratio,
                        temp_after_isentropic_compression,
                        temp_after_constant_volume_heat,
                        temp_after_constant_pressure_heat,
                        temp_after_isentropic_expansion,
                        mean_effective_pressure)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# Air-table efficiency -- Example 9.3 (book 0.635)
chk("eta air-table = 0.635",
    dual_efficiency_air_table(214.07, 673.2, 1065.8, 1452.6, 1778.3, 475.96), 0.635, 0.001)
# Example 9.3 net work and mep (book 456 kJ/kg, 0.56 MPa)
w_net = (1065.8 - 673.2) + (1778.3 - 1452.6) - (475.96 - 214.07)
chk("net work = 456 kJ/kg", w_net, 456.0, 0.5)
chk("mep = 0.56 MPa", mean_effective_pressure(w_net, 0.861, 18.0) / 1e3, 0.56, 0.005)
# State temperatures of Example 9.3 (book air-table T3=1347.5, T4=1617; ratios exact)
chk("rp = p3/p2", pressure_ratio(1.5, 1.0), 1.5)
chk("rc = V4/V3", cutoff_ratio(1.2, 1.0), 1.2)
chk("T3 = rp*T2 (book)", temp_after_constant_volume_heat(898.3, 1.5), 1347.45, 0.1)
chk("T4 = rc*T3 (book)", temp_after_constant_pressure_heat(1347.5, 1.2), 1617.0, 0.1)
# cold air-standard closed form for the same r, rp, rc
chk("eta cold (r=18,rp=1.5,rc=1.2)", dual_efficiency(18.0, 1.5, 1.2), 0.6798, 0.001)
# the cold closed form overpredicts the air-table value (constant cp/cv)
assert dual_efficiency(18.0, 1.5, 1.2) > 0.635;  _n += 1

# --- the dual cycle brackets Otto and Diesel ---
# rc -> 1 reduces to the Otto cycle (Eq. 9.8)
chk("rc->1 reduces to Otto", dual_efficiency(18.0, 1.5, 1.0 + 1e-9),
    1.0 - 1.0 / 18.0 ** 0.4, 1e-4)
# rp -> 1 reduces to the Diesel cycle (Eq. 9.13)
diesel = 1.0 - (1.0 / 18.0 ** 0.4) * (2.0 ** 1.4 - 1.0) / (1.4 * (2.0 - 1.0))
chk("rp->1 reduces to Diesel", dual_efficiency(18.0, 1.0 + 1e-9, 2.0), diesel, 1e-4)
# with BOTH ratios > 1 the dual efficiency lies between Diesel and Otto at the same r
otto = 1.0 - 1.0 / 18.0 ** 0.4
assert diesel < dual_efficiency(18.0, 1.5, 2.0) < otto;  _n += 1
# cold air-standard state temperatures self-consistency (T1=300, r=18)
T2 = temp_after_isentropic_compression(300.0, 18.0)
T3 = temp_after_constant_volume_heat(T2, 1.5)
T4 = temp_after_constant_pressure_heat(T3, 1.2)
chk("T5 = T4 (rc/r)^(k-1)", temp_after_isentropic_expansion(T4, 18.0, 1.2),
    T4 * (1.2 / 18.0) ** 0.4)
# efficiency rises with r
assert dual_efficiency(21.0, 1.5, 1.2) > dual_efficiency(15.0, 1.5, 1.2);  _n += 1
# the Otto limit is evaluable AT the point, not only as a limit: rp=rc=1 sends
# both numerator and denominator to zero, and the removable singularity is Otto.
chk("rp=rc=1 exactly -> Otto (no ZeroDivisionError)",
    dual_efficiency(18.0, 1.0, 1.0), otto)
chk("approach agrees with the point", dual_efficiency(18.0, 1.0 + 1e-9, 1.0 + 1e-9),
    dual_efficiency(18.0, 1.0, 1.0), 1e-6)

print(f"All {_n} tests passed.")
