"""test_entropy.py — checks for Module 4.2.  Run: python3 test_entropy.py"""
import math
from entropy import (entropy_mixture, du_from_tds, dh_from_tds,
                     entropy_change_incompressible, entropy_change_ideal_gas_tables,
                     entropy_change_ideal_gas_cp, entropy_change_ideal_gas_cv,
                     heat_isothermal_rev, entropy_production_closed, process_allowed)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# mixture entropy
chk("s mixture", entropy_mixture(1.8418, 6.8379, 0.5), 4.33985)
chk("s x=0", entropy_mixture(1.8418, 6.8379, 0.0), 1.8418)
# T dS equations: dh - du = d(pv) = p dv + v dp
du = du_from_tds(400.0, 0.5, 200.0, 0.01)
dh = dh_from_tds(400.0, 0.5, 0.8, 5.0)
chk("TdS consistency dh-du", dh - du, 200.0 * 0.01 + 0.8 * 5.0)
# incompressible
chk("ds incompressible", entropy_change_incompressible(4.2, 295.0, 300.0), 4.2 * math.log(300.0 / 295.0))
# ideal gas -- HW 6.11 (table form), and the const-cp/const-cv special cases
chk("ds gas tables (6.11)", entropy_change_ideal_gas_tables(1.70203, 2.21952, 0.287, 100.0, 650.0), -0.0197, 1e-3)
chk("ds gas const-p", entropy_change_ideal_gas_cp(1.005, 0.287, 300.0, 600.0, 100.0, 100.0), 1.005 * math.log(2.0))
chk("ds gas const-v", entropy_change_ideal_gas_cv(0.718, 0.287, 300.0, 600.0, 1.0, 1.0), 0.718 * math.log(2.0))
# Example 6.1 -- internally reversible isothermal heat
chk("Ex6.1 Q/m", heat_isothermal_rev(423.15, 6.8379 - 1.8418), 2114.1, 0.1)
# Example 6.2 -- adiabatic: sigma = ds (same end states, but now sigma > 0)
chk("Ex6.2 sigma", entropy_production_closed(6.8379, 1.8418, 0.0), 4.9961, 1e-4)
# HW 6.37 -- rigid insulated air + paddle: sigma = m cv ln(T2/T1)
T2_637 = 293.0 + 710.0 / (4.757 * 0.72)
sig_637 = 4.757 * entropy_change_ideal_gas_cv(0.72, 0.287, 293.0, T2_637, 1.0, 1.0)
chk("HW6.37 T2", T2_637, 500.3, 0.1)
chk("HW6.37 sigma", sig_637, 1.83, 0.01)
# HW 6.59 -- thermal mixing of two incompressible bodies
Tf = (1.0 * 0.5 * 1075.0 + 100.0 * 4.2 * 295.0) / (1.0 * 0.5 + 100.0 * 4.2)
sig_659 = 1.0 * entropy_change_incompressible(0.5, 1075.0, Tf) + 100.0 * entropy_change_incompressible(4.2, 295.0, Tf)
chk("HW6.59 Tf", Tf, 295.93, 0.01)
chk("HW6.59 sigma", sig_659, 0.673, 0.01)
# 2nd-law sign check
assert process_allowed(4.9961) is True;    _n += 1
assert process_allowed(0.0) is True;        _n += 1
assert process_allowed(-0.1) is False;      _n += 1

print(f"All {_n} tests passed.")
