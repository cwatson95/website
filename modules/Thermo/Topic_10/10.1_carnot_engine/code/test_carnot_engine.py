"""test_carnot_engine.py — checks for Module 10.1.  Run: python3 test_carnot_engine.py"""
import math
from carnot_engine import (carnot_efficiency, thermal_efficiency, efficiency_from_heats,
                           kelvin_heat_ratio, carnot_heat_rejected, carnot_work,
                           cycle_status, carnot_cop_refrigerator, carnot_cop_heat_pump)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# Carnot efficiency -- book-verified values
chk("eta 2000/400 = 0.80", carnot_efficiency(400.0, 2000.0), 0.80)   # Moran Ex 5.1, p.266
chk("eta 745/298 = 0.60", carnot_efficiency(298.0, 745.0), 0.60)     # Moran p.266
# basic efficiency definitions used in Example 5.1
chk("eta = W/Q_H = 0.85", thermal_efficiency(850.0, 1000.0), 0.85)   # Ex 5.1(b)
chk("eta = W/Q_H = 0.80", thermal_efficiency(800.0, 1000.0), 0.80)   # Ex 5.1(c)
chk("eta = 1 - Q_C/Q_H", efficiency_from_heats(200.0, 1000.0), 0.80) # Ex 5.1(c)
# reversible heat ratio and the resulting Carnot heats/work (Q_H = 1000 kJ)
chk("kelvin ratio 400/2000", kelvin_heat_ratio(400.0, 2000.0), 0.20)
chk("Carnot Q_C", carnot_heat_rejected(1000.0, 400.0, 2000.0), 200.0)  # = Ex 5.1(c) Q_C
chk("Carnot W", carnot_work(1000.0, 400.0, 2000.0), 800.0)            # = Ex 5.1(c) W
# reversed-Carnot COPs (Examples 5.2 and 5.3)
chk("beta_max 268/295", carnot_cop_refrigerator(268.0, 295.0), 268.0 / 27.0)  # Ex 5.2 ~9.9
chk("gamma_max 492/530", carnot_cop_heat_pump(492.0, 530.0), 530.0 / 38.0)    # Ex 5.3 ~13.95
chk("gamma = beta + 1", carnot_cop_heat_pump(268.0, 295.0),
    carnot_cop_refrigerator(268.0, 295.0) + 1.0)

# Carnot corollary classification (Example 5.1, eta_max = 0.80)
assert cycle_status(0.60, 400.0, 2000.0) == "irreversible";  _n += 1   # Ex 5.1(a)
assert cycle_status(0.85, 400.0, 2000.0) == "impossible";    _n += 1   # Ex 5.1(b)
assert cycle_status(0.80, 400.0, 2000.0) == "reversible";    _n += 1   # Ex 5.1(c)
assert cycle_status(0.90, 400.0, 2000.0) == "impossible";    _n += 1   # quick quiz: Q_C=300,W=2700
assert cycle_status(0.50, 400.0, 2000.0) == "irreversible";  _n += 1   # below ceiling

print(f"All {_n} tests passed.")
