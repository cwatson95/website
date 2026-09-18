"""test_third_law.py — checks for Module 3.4.  Run: python3 test_third_law.py"""
import math
from third_law import (standard_entropy_at_zero, debye_cp, absolute_entropy,
                       absolute_entropy_debye, carnot_cop_refrigerator)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# third-law datum
chk("S0 pure crystal", standard_entropy_at_zero(True), 0.0)
# Debye c_p
chk("debye_cp 10", debye_cp(10.0, 1e-3), 1.0)
chk("debye_cp 20", debye_cp(20.0, 1e-3), 8.0)
# absolute entropy: numeric integral matches analytic aT^3/3
chk("S_debye analytic 10", absolute_entropy_debye(10.0, 1e-3), 1.0 / 3.0)
chk("S_debye analytic 20", absolute_entropy_debye(20.0, 1e-3), 8.0 / 3.0)
chk("S numeric 10", absolute_entropy(10.0, lambda T: debye_cp(T, 1e-3)), 1.0 / 3.0, 1e-3)
chk("S numeric 20", absolute_entropy(20.0, lambda T: debye_cp(T, 1e-3)), 8.0 / 3.0, 1e-2)
# unattainability: COP_ref -> 0 as T_C -> 0
chk("COP_ref 250/300", carnot_cop_refrigerator(250.0, 300.0), 5.0)
chk("COP_ref 1/300", carnot_cop_refrigerator(1.0, 300.0), 1.0 / 299.0)
# predicates
assert standard_entropy_at_zero(False) is None;  _n += 1
assert carnot_cop_refrigerator(1.0, 300.0) < carnot_cop_refrigerator(250.0, 300.0);  _n += 1

print(f"All {_n} tests passed.")
