"""test_heat_pump.py — checks for Module 08.4.  Run: python3 test_heat_pump.py
Values reproduce Moran 8e Example 10.1 (ideal R-134a refrigerator) and Example 10.4
(R-134a vapor-compression heat pump)."""
import math
from heat_pump import (heat_rejected, cop_refrigeration, cop_heat_pump,
                       carnot_cop_refrigeration, carnot_cop_heat_pump,
                       cop_ref_from_enthalpies, cop_hp_from_enthalpies)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# --- cycle first law and COP definitions ---
chk("Q_H = Q_C + W", heat_rejected(27.45, 7.53), 34.98, 1e-9)
chk("beta = Q_C/W", cop_refrigeration(12.92, 1.40), 12.92 / 1.40)
chk("gamma = Q_H/W", cop_heat_pump(34.98, 7.53), 34.98 / 7.53)
# gamma = beta + 1 from the rate definitions (same W, Q_H=Q_C+W)
chk("gamma = beta + 1 (rates)", cop_heat_pump(34.98, 7.53),
    cop_refrigeration(27.45, 7.53) + 1.0, 1e-9)

# --- Example 10.1: ideal R-134a refrigerator ---
h1, h2s, h3 = 247.23, 264.7, 85.75                       # h4 = h3
beta = cop_ref_from_enthalpies(h1, h2s, h3)
chk("Ex10.1 beta", beta, 9.24, 0.01)                     # book 9.24
chk("Ex10.1 Carnot beta_max", carnot_cop_refrigeration(299.0, 273.0), 10.5, 0.05)   # book 10.5
assert beta < carnot_cop_refrigeration(299.0, 273.0); _n += 1   # real < Carnot
# compressor work & capacity reproduce: Wc=mdot(h2s-h1), Qin=mdot(h1-h4)
mdot = 0.08
chk("Ex10.1 Wc (kW)", mdot * (h2s - h1), 1.40, 0.01)     # book 1.4 kW
chk("Ex10.1 capacity (ton)", mdot * (h1 - h3) * 60.0 / 211.0, 3.67, 0.01)   # book 3.67 ton

# --- Example 10.4: R-134a vapor-compression heat pump ---
h1, h2, h3 = 242.54, 280.19, 105.29                      # h4 = h3
gamma = cop_hp_from_enthalpies(h1, h2, h3)
chk("Ex10.4 gamma", gamma, 4.65, 0.01)                   # book 4.65
chk("Ex10.4 Wc (kW)", 0.2 * (h2 - h1), 7.53, 0.005)      # book 7.53 kW
chk("Ex10.4 Qout (kW)", 0.2 * (h2 - h3), 34.98, 0.005)   # book 34.98 kW
chk("Ex10.4 gamma from rates", cop_heat_pump(0.2 * (h2 - h3), 0.2 * (h2 - h1)), gamma, 1e-9)
# gamma = beta + 1 identity for the SAME cycle (h4 = h3)
beta_same = cop_ref_from_enthalpies(h1, h2, h3)
chk("Ex10.4 gamma = beta + 1", gamma, beta_same + 1.0, 1e-9)
assert gamma > 1.0; _n += 1                              # heat-pump COP always > 1

# --- Carnot identity gamma_max = beta_max + 1 ---
chk("Carnot identity", carnot_cop_heat_pump(299.0, 273.0),
    carnot_cop_refrigeration(299.0, 273.0) + 1.0, 1e-9)

print(f"All {_n} tests passed.")
