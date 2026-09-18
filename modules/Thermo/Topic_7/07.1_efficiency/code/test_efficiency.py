"""test_efficiency.py — checks for Module 07.1.  Run: python3 test_efficiency.py"""
import math
from efficiency import (thermal_efficiency, thermal_efficiency_from_heat,
                        cop_refrigerator, cop_refrigerator_from_heat,
                        cop_heat_pump, cop_heat_pump_from_heat,
                        carnot_efficiency, carnot_cop_refrigerator,
                        carnot_cop_heat_pump, isentropic_turbine_efficiency,
                        turbine_work_actual, isentropic_nozzle_efficiency,
                        nozzle_exit_ke, isentropic_compressor_efficiency,
                        isentropic_pump_efficiency, compressor_work_actual,
                        efficiency_is_possible)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# --- thermal efficiency (Eqs 2.42/2.43) ---
chk("eta W/Q_in", thermal_efficiency(800.0, 1000.0), 0.80)            # Ex 5.1c
chk("eta 1-Qout/Qin", thermal_efficiency_from_heat(1000.0, 200.0), 0.80)
chk("eta forms agree", thermal_efficiency(800.0, 1000.0),
    thermal_efficiency_from_heat(1000.0, 200.0))
# --- COP refrigerator / heat pump (Eqs 2.45-2.48) ---
chk("beta = Q_C/W", cop_refrigerator(8000.0, 3200.0), 2.5)            # Ex 5.2
chk("beta from heat", cop_refrigerator_from_heat(8000.0, 11200.0), 2.5)  # Q_H=Q_C+W
chk("gamma = Q_H/W", cop_heat_pump(11200.0, 3200.0), 3.5)
chk("gamma from heat", cop_heat_pump_from_heat(8000.0, 11200.0), 3.5)
chk("gamma = beta + 1", cop_heat_pump(11200.0, 3200.0),
    cop_refrigerator(8000.0, 3200.0) + 1.0)
# --- Carnot ceilings (Eqs 5.9-5.11) ---
chk("eta_max 400/2000", carnot_efficiency(400.0, 2000.0), 0.80)      # Ex 5.1
chk("beta_max 268/295", carnot_cop_refrigerator(268.0, 295.0), 9.926, 1e-3)  # Ex 5.2 ->9.9
chk("gamma_max 492/530", carnot_cop_heat_pump(492.0, 530.0), 13.947, 1e-3)   # Ex 5.3 ->13.95
chk("gamma_max=beta_max+1", carnot_cop_heat_pump(268.0, 295.0),
    carnot_cop_refrigerator(268.0, 295.0) + 1.0)
# --- isentropic turbine (Eq 6.46) ---
chk("turbine work Ex6.11", turbine_work_actual(0.75, 3105.6, 2743.0), 271.95, 0.01)
chk("turbine eta Ex6.12", isentropic_turbine_efficiency(390.88, 316.88, 285.27), 0.70, 0.005)
# (h2 = h1 - 74 = 316.88, since actual work 74 = h1 - h2)
chk("turbine eta defn", isentropic_turbine_efficiency(3105.6, 2833.65, 2743.0), 0.75, 1e-3)
# --- isentropic nozzle (Eq 6.47) ---
chk("nozzle ke2 Ex6.13", nozzle_exit_ke(1326.4, 1211.8, 0.2), 114.8, 0.01)
chk("nozzle ke2s Ex6.13", nozzle_exit_ke(1326.4, 1202.3, 0.2), 124.3, 0.01)
chk("nozzle eta Ex6.13", isentropic_nozzle_efficiency(114.8, 124.3), 0.924, 1e-3)
# --- isentropic compressor / pump (Eq 6.48) ---
chk("compressor eta Ex6.14", isentropic_compressor_efficiency(249.75, 294.17, 285.58), 0.81, 0.005)
chk("compressor work", compressor_work_actual(0.81, 249.75, 285.58), 44.23, 0.05)
chk("pump = compressor form", isentropic_pump_efficiency(249.75, 294.17, 285.58),
    isentropic_compressor_efficiency(249.75, 294.17, 285.58))
# --- second-law ceiling on cycle efficiency (Carnot corollary) ---
assert efficiency_is_possible(0.60, 400.0, 2000.0) is True;   _n += 1   # below 0.80
assert efficiency_is_possible(0.80, 400.0, 2000.0) is True;   _n += 1   # reversible limit
assert efficiency_is_possible(0.85, 400.0, 2000.0) is False;  _n += 1   # impossible (Ex 5.1b)

print(f"All {_n} tests passed.")
