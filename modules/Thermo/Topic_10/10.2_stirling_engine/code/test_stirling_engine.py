"""test_stirling_engine.py — checks for Module 10.2.  Run: python3 test_stirling_engine.py"""
import math
from stirling_engine import (stirling_efficiency, isothermal_heat, stirling_heat_added,
                             stirling_heat_rejected, stirling_net_work, regenerator_heat,
                             stirling_efficiency_no_regen, regenerator_effectiveness)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

R, cv = 0.287, 0.718          # air, kJ/kg.K
ln2 = math.log(2.0)

# ideal Stirling (100% regeneration) == Carnot value (Eq. 5.9)
chk("eta 1000/300 = 0.70", stirling_efficiency(300.0, 1000.0), 0.70)
chk("eta 745/298 = 0.60", stirling_efficiency(298.0, 745.0), 0.60)        # = Carnot
chk("eta 2000/400 = 0.80", stirling_efficiency(400.0, 2000.0), 0.80)      # = Carnot Ex 5.1
# per-process isothermal heats (Q = R T ln r), r = 2
chk("isothermal_heat", isothermal_heat(R, 1000.0, 2.0), R * 1000.0 * ln2)
chk("Q_34 added @T_H", stirling_heat_added(R, 1000.0, 2.0), 198.933, 0.01)
chk("Q_12 rejected @T_C", stirling_heat_rejected(R, 300.0, 2.0), 59.680, 0.01)
chk("W_net = Q_34 - Q_12", stirling_net_work(R, 1000.0, 300.0, 2.0), 139.253, 0.01)
# efficiency from heats reproduces the Carnot value (R and ln r cancel)
chk("eta = W/Q_34 = 0.70",
    stirling_net_work(R, 1000.0, 300.0, 2.0) / stirling_heat_added(R, 1000.0, 2.0), 0.70)
# regenerator-shuttled (constant-volume) heat
chk("Q_regen = cv(T_H-T_C)", regenerator_heat(cv, 1000.0, 300.0), 502.6, 0.01)
# without regeneration: efficiency collapses well below Carnot
chk("eta no-regen", stirling_efficiency_no_regen(R, cv, 1000.0, 300.0, 2.0), 0.19850, 1e-4)
# regenerator effectiveness (Eq. 9.27): actual 80%, ideal 100%
chk("eta_reg actual", regenerator_effectiveness(700.0, 300.0, 800.0), 0.80)
chk("eta_reg ideal", regenerator_effectiveness(800.0, 300.0, 800.0), 1.0)

# inequalities: ideal regeneration recovers Carnot; no regeneration falls short
assert stirling_efficiency_no_regen(R, cv, 1000.0, 300.0, 2.0) < stirling_efficiency(300.0, 1000.0)
_n += 1
assert math.isclose(stirling_efficiency(300.0, 1000.0), 1.0 - 300.0 / 1000.0); _n += 1

print(f"All {_n} tests passed.")
