"""test_brayton_cycle.py — checks for Module 09.5.  Run: python3 test_brayton_cycle.py"""
import math
from brayton_cycle import (turbine_work, compressor_work, heat_added, heat_rejected,
                           brayton_efficiency_air_table, back_work_ratio,
                           pr_after_compression, pr_after_expansion,
                           temp_after_isentropic_compression,
                           temp_after_isentropic_expansion,
                           brayton_efficiency, pressure_ratio_max_work,
                           turbine_work_actual, compressor_work_actual,
                           regenerator_effectiveness, regenerator_exit_enthalpy,
                           heat_added_regenerative)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# --- Example 9.4 (ideal Brayton; Table A-22 enthalpies, book-verified) -------
h1, h2, h3, h4 = 300.19, 579.9, 1515.4, 808.5
chk("wt = 706.9", turbine_work(h3, h4), 706.9, 0.05)
chk("wc = 279.7", compressor_work(h1, h2), 279.71, 0.05)
chk("qin = 935.5", heat_added(h2, h3), 935.5, 0.05)
chk("eta air-table = 0.457", brayton_efficiency_air_table(h1, h2, h3, h4), 0.457, 0.001)
chk("bwr = 0.396", back_work_ratio(h1, h2, h3, h4), 0.396, 0.001)
chk("pr2 = 13.86 (isentropic 1-2)", pr_after_compression(1.386, 10.0), 13.86, 1e-9)
chk("pr4 = 45.05 (isentropic 3-4)", pr_after_expansion(450.5, 10.0), 45.05, 1e-9)
# net power at mdot = 5.807 kg/s (book 2481 kW); Quick Quiz Qin = 5432 kW
chk("Wdot = 2481 kW", 5.807 * (turbine_work(h3, h4) - compressor_work(h1, h2)), 2481.0, 1.0)
chk("Qdot_in = 5432 kW", 5.807 * heat_added(h2, h3), 5432.0, 1.0)
# cold air-standard comparison column of Ex 9.4 (k = 1.4)
chk("T2 cold = 579.2 K", temp_after_isentropic_compression(300.0, 10.0), 579.2, 0.05)
chk("T4 cold = 725.1 K", temp_after_isentropic_expansion(1400.0, 10.0), 725.1, 0.05)
chk("eta cold rp=10 = 0.482", brayton_efficiency(10.0), 0.482, 0.001)
T2c = temp_after_isentropic_compression(300.0, 10.0)
T4c = temp_after_isentropic_expansion(1400.0, 10.0)
chk("bwr cold = 0.414", (T2c - 300.0) / (1400.0 - T4c), 0.414, 0.001)

# --- Example 9.6 (eta_t = eta_c = 80%, book-verified) ------------------------
wt = turbine_work_actual(706.9, 0.8)
wc = compressor_work_actual(279.7, 0.8)
chk("wt actual = 565.5", wt, 565.52, 0.05)
chk("wc actual = 349.6", wc, 349.625, 0.05)
h2a = h1 + wc                                   # 649.8 kJ/kg
chk("h2 actual = 649.8", h2a, 649.8, 0.05)
chk("eta = 0.249", (wt - wc) / (h3 - h2a), 0.249, 0.001)
chk("bwr = 0.618", wc / wt, 0.618, 0.001)
chk("Wdot = 1254 kW", 5.807 * (wt - wc), 1254.0, 1.0)
# Quick Quiz: eta_t = 70% (same eta_c) -> eta = 16.8%, bwr = 70.65%
wt70 = turbine_work_actual(706.9, 0.7)
chk("quiz eta (eta_t=0.7) = 0.168", (wt70 - wc) / (h3 - h2a), 0.168, 0.001)
chk("quiz bwr = 0.7065", wc / wt70, 0.7065, 0.001)

# --- Example 9.7 (regenerator, eta_reg = 80%, book-verified) -----------------
hx = regenerator_exit_enthalpy(h2, h4, 0.8)
chk("hx = 762.8", hx, 762.8, 0.05)
chk("Eq. 9.27 round-trip", regenerator_effectiveness(hx, h2, h4), 0.8)
chk("eta with regen = 0.568",
    (turbine_work(h3, h4) - compressor_work(h1, h2)) / heat_added_regenerative(hx, h3),
    0.568, 0.001)
# Quick Quiz: eta_reg = 100% -> hx = h4, eta = 60.4%
chk("quiz eta_reg=1 -> 0.604",
    (turbine_work(h3, h4) - compressor_work(h1, h2)) /
    heat_added_regenerative(regenerator_exit_enthalpy(h2, h4, 1.0), h3), 0.604, 0.001)

# --- Example 9.5 (pressure ratio for maximum net work) -----------------------
chk("rp* (300 K, 1700 K) ~ 21", pressure_ratio_max_work(300.0, 1700.0), 20.8, 0.1)

# --- structure/consistency ----------------------------------------------------
# efficiency rises with pressure ratio (Eq. 9.25 / Fig. 9.12)
assert brayton_efficiency(20.0) > brayton_efficiency(10.0) > brayton_efficiency(6.0);  _n += 1
# cold closed form == air-table form fed cp*T enthalpies on isentropic-consistent states
cp, rp, T1, T3 = 1.005, 10.0, 300.0, 1400.0
T2 = temp_after_isentropic_compression(T1, rp)
T4 = temp_after_isentropic_expansion(T3, rp)
chk("cold form == air-table(cp*T)",
    brayton_efficiency_air_table(cp * T1, cp * T2, cp * T3, cp * T4),
    brayton_efficiency(rp))
# energy balance closes: qin - qout = wt - wc
chk("qin - qout = wnet", heat_added(h2, h3) - heat_rejected(h1, h4),
    turbine_work(h3, h4) - compressor_work(h1, h2))
# below the Carnot ceiling for its temperature extremes (1400/300 K -> 0.786)
assert brayton_efficiency_air_table(h1, h2, h3, h4) < 1.0 - 300.0 / 1400.0;  _n += 1
# gas-turbine bwr is large (40-80% band, Sec. 9.6.1) vs Rankine's ~1%
assert 0.3 < back_work_ratio(h1, h2, h3, h4) < 0.8;  _n += 1

print(f"All {_n} tests passed.")
