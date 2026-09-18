"""
test_equations.py  —  checks for Module 7.EQ.

(1) each canonical Topic-7 equation reproduces a known (book-verified) value;
(2) CROSS-CHECK -- the concept module 07.1 (efficiency.py) computes the same things.

Run:  cd code && python3 test_equations.py   ->  "All N tests passed."
"""
import math
import os
import sys

import equations as eq

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "07.1_efficiency", "code"))
import efficiency as m_eff   # noqa: E402

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1


# ---- (1) canonical values (book-verified) ----------------------------------
chk("thermal_efficiency", eq.thermal_efficiency(800.0, 1000.0), 0.80)            # Ex 5.1c
chk("thermal_efficiency_alt", eq.thermal_efficiency_alt(1000.0, 200.0), 0.80)
chk("cop_refrigerator", eq.cop_refrigerator(8000.0, 3200.0), 2.5)                # Ex 5.2
chk("cop_heat_pump", eq.cop_heat_pump(11200.0, 3200.0), 3.5)
chk("carnot_efficiency", eq.carnot_efficiency(400.0, 2000.0), 0.80)             # Ex 5.1
chk("carnot_cop_refrigerator", eq.carnot_cop_refrigerator(268.0, 295.0), 9.926, 1e-3)  # Ex 5.2
chk("carnot_cop_heat_pump", eq.carnot_cop_heat_pump(492.0, 530.0), 13.947, 1e-3)       # Ex 5.3
chk("isentropic_turbine", eq.isentropic_turbine_efficiency(3105.6, 2833.65, 2743.0), 0.75, 1e-3)  # Ex 6.11
chk("isentropic_nozzle", eq.isentropic_nozzle_efficiency(114.8, 124.3), 0.924, 1e-3)   # Ex 6.13
chk("isentropic_compressor", eq.isentropic_compressor_efficiency(249.75, 294.17, 285.58), 0.81, 0.005)  # Ex 6.14

# ---- (2) cross-checks: concept module 07.1 matches the registry ------------
chk("07.1 thermal", m_eff.thermal_efficiency(800.0, 1000.0), eq.thermal_efficiency(800.0, 1000.0))
chk("07.1 thermal_alt", m_eff.thermal_efficiency_from_heat(1000.0, 200.0), eq.thermal_efficiency_alt(1000.0, 200.0))
chk("07.1 cop_ref", m_eff.cop_refrigerator(8000.0, 3200.0), eq.cop_refrigerator(8000.0, 3200.0))
chk("07.1 cop_hp", m_eff.cop_heat_pump(11200.0, 3200.0), eq.cop_heat_pump(11200.0, 3200.0))
chk("07.1 carnot_eta", m_eff.carnot_efficiency(400.0, 2000.0), eq.carnot_efficiency(400.0, 2000.0))
chk("07.1 carnot_beta", m_eff.carnot_cop_refrigerator(268.0, 295.0), eq.carnot_cop_refrigerator(268.0, 295.0))
chk("07.1 carnot_gamma", m_eff.carnot_cop_heat_pump(492.0, 530.0), eq.carnot_cop_heat_pump(492.0, 530.0))
chk("07.1 turbine", m_eff.isentropic_turbine_efficiency(3105.6, 2833.65, 2743.0), eq.isentropic_turbine_efficiency(3105.6, 2833.65, 2743.0))
chk("07.1 nozzle", m_eff.isentropic_nozzle_efficiency(114.8, 124.3), eq.isentropic_nozzle_efficiency(114.8, 124.3))
chk("07.1 compressor", m_eff.isentropic_compressor_efficiency(249.75, 294.17, 285.58), eq.isentropic_compressor_efficiency(249.75, 294.17, 285.58))

print(f"All {_n} tests passed.")
