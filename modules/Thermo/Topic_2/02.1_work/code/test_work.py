"""test_work.py — checks for Module 2.1.  Run: python3 test_work.py"""
import math
from work import (work_force_displacement, boundary_work, shaft_work,
                  electric_work, spring_work)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

chk("boundary const-p", boundary_work(lambda V: 200.0, 1.0, 1.5), 100.0, 1e-3)
chk("force*disp", work_force_displacement(lambda s: 50.0, 0.0, 3.0), 150.0, 1e-3)
chk("force*disp linear", work_force_displacement(lambda s: 10.0 * s, 0.0, 2.0), 20.0, 1e-3)  # ∫10s ds=5s²|=20
chk("shaft τω·dt", shaft_work(18.0, 100.0, 1.0), 1800.0)
chk("electric V I dt", electric_work(110.0, 10.0, 1.0), 1100.0)
chk("spring 0->0.1", spring_work(200.0, 0.0, 0.1), 1.0)
chk("spring 0->0.2", spring_work(200.0, 0.0, 0.2), 4.0)            # quadratic in x

# ---- the spring table in notes.md §5 ----
chk("spring 0.1->0.2", spring_work(200.0, 0.1, 0.2), 3.0)
# doubling the stretch quadruples the stored energy...
chk("quadratic scaling", spring_work(200.0, 0.0, 0.2), 4.0 * spring_work(200.0, 0.0, 0.1))
# ...so the second decimetre costs three times the first
chk("second increment costs 3x", spring_work(200.0, 0.1, 0.2),
    3.0 * spring_work(200.0, 0.0, 0.1))
# the general quadrature reproduces the closed form on F = kx
chk("int F ds == 1/2 k (x2^2 - x1^2)",
    work_force_displacement(lambda s: 200.0 * s, 0.0, 0.2),
    spring_work(200.0, 0.0, 0.2), 1e-6)

print(f"All {_n} tests passed.")
