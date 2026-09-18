"""test_compressor.py — checks for Module 08.1.  Run: python3 test_compressor.py
Values reproduce Moran 8e Examples 4.5 (air compressor) and 6.14 (R-22 compressor)."""
import math
from compressor import (mass_flow_rate, mass_flow_rate_ideal_gas, power_cv, power_input,
                        actual_compressor_work, isentropic_compressor_work,
                        isentropic_efficiency, exit_enthalpy_from_efficiency)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

R = 8314.0 / 28.97          # air, J/kg.K

# --- mass flow rate mdot = A V / v ---
chk("mdot = A V / v", mass_flow_rate(0.1, 6.0, 0.8323), 0.1 * 6.0 / 0.8323)
# --- Example 4.5: air compressor (STRICT SI: h in J/kg, Qdot in W, result in W) ---
mdot = mass_flow_rate_ideal_gas(0.1, 6.0, 1.0e5, R, 290.0)
chk("Ex4.5 mdot", mdot, 0.72, 0.005)                                    # book 0.72 kg/s
h1, h2 = 290.16e3, 451.80e3                                             # Table A-22, J/kg
W = power_cv(mdot, h1, h2, Qdot=-180.0e3 / 60.0, V1=6.0, V2=2.0, g=0.0)
chk("Ex4.5 Wdot_cv (kW)", W / 1e3, -119.4, 0.2)                         # book -119.4 kW
chk("Ex4.5 power input (kW)",
    power_input(mdot, h1, h2, Qdot=-180.0e3 / 60.0, V1=6.0, V2=2.0, g=0.0) / 1e3, 119.4, 0.2)
# kinetic-energy term is tiny (Quick Quiz: neglecting it -> still -119.4 kW)
W_noKE = power_cv(mdot, h1, h2, Qdot=-180.0e3 / 60.0, g=0.0)
chk("Ex4.5 W no KE (kW)", W_noKE / 1e3, -119.4, 0.2)
assert abs(W - W_noKE) < 50.0; _n += 1                                  # dKE contributes < 0.05 kW

# --- Example 6.14: R-22 compressor, isentropic efficiency (enthalpy diffs: kJ/kg ok) ---
h1, h2, h2s = 249.75, 294.17, 285.58
chk("Ex6.14 actual work", actual_compressor_work(h1, h2), 44.42, 1e-9)  # h2-h1
chk("Ex6.14 isentropic work", isentropic_compressor_work(h1, h2s), 35.83, 1e-9)
chk("Ex6.14 Wdot_cv (kW)", power_cv(0.07, h1 * 1e3, h2 * 1e3) / 1e3, -3.11, 0.005)  # book -3.11
chk("Ex6.14 eta_c", isentropic_efficiency(h1, h2, h2s), 0.81, 0.005)    # book 0.81
# round-trip: rebuild h2 from eta_c
eta = isentropic_efficiency(h1, h2, h2s)
chk("Ex6.14 h2 from eta", exit_enthalpy_from_efficiency(h1, h2s, eta), h2, 1e-9)
# isentropic work is the minimum (h2s <= h2 for the same exit pressure)
assert isentropic_compressor_work(h1, h2s) < actual_compressor_work(h1, h2); _n += 1
assert 0.0 < eta <= 1.0; _n += 1

print(f"All {_n} tests passed.")
