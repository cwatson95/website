"""
test_equations.py  —  checks for Module 8.EQ.

(1) each canonical Topic-8 equation reproduces a known (book-verified) value;
(2) CROSS-CHECK -- the four concept modules 08.1/08.2/08.3/08.4 (compressor.py,
    condenser.py, heat_exchanger.py, heat_pump.py) compute the same things, so the
    device equations are used consistently across the whole topic.  A formula change
    anywhere fails this test.

Book anchors: Ex 4.5 (air compressor), Ex 4.7 (power-plant condenser), Ex 6.14
(R-22 compressor), Ex 10.1 (ideal R-134a refrigerator), Ex 10.4 (R-134a heat pump).

Run:  cd code && python3 test_equations.py   ->  "All N tests passed."
"""
import math
import os
import sys

import equations as eq

_HERE = os.path.dirname(os.path.abspath(__file__))
for _s in ("08.1_compressor", "08.2_condenser", "08.3_heat_exchanger", "08.4_heat_pump"):
    sys.path.insert(0, os.path.join(_HERE, "..", "..", _s, "code"))
import compressor       # noqa: E402  (08.1)
import condenser        # noqa: E402  (08.2)
import heat_exchanger   # noqa: E402  (08.3)
import heat_pump        # noqa: E402  (08.4)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1


R_AIR = 8314.0 / 28.97      # J/kg.K

# ---- (1) canonical values (book-verified) ----------------------------------
# mass flow, Ex 4.5 inlet: A=0.1 m^2, V=6 m/s, p=1 bar, T=290 K -> 0.72 kg/s
chk("mass_flow_rate", eq.mass_flow_rate(0.1, 6.0, R_AIR * 290.0 / 1.0e5), 0.72, 0.005)
chk("mass_flow_rate_ideal_gas", eq.mass_flow_rate_ideal_gas(0.1, 6.0, 1.0e5, R_AIR, 290.0), 0.72, 0.005)
# Ex 4.5 power (book's stepwise mdot = 0.72): Wdot_cv = -119.4 kW
W45 = eq.power_cv(0.72, 290.16e3, 451.80e3, Qdot=-180.0e3 / 60.0, V1=6.0, V2=2.0, g=0.0)
chk("power_cv Ex4.5 (kW)", W45 / 1e3, -119.4, 0.05)
# Ex 6.14: R-22, mdot=0.07 kg/s, h1=249.75, h2=294.17 kJ/kg -> -3.11 kW
chk("compressor_power Ex6.14 (kW)", eq.compressor_power(0.07, 249.75, 294.17), -3.11, 0.005)
# Ex 4.7(b) steam side: h_in=2465.1, h_out=188.45 -> -2276.7 kJ per kg of steam
chk("single_stream_heat_rate Ex4.7", eq.single_stream_heat_rate(1.0, 2465.1, 188.45), -2276.7, 0.1)
# Ex 4.7(a): mdot_c/mdot_h = (2465.1-188.45)/62.7 = 36.3, and the balance closes
ratio = eq.mass_flow_ratio_cold_to_hot(2465.1, 188.45, 0.0, 62.7)
chk("mass_flow_ratio Ex4.7", ratio, 36.3, 0.05)
chk("two_stream_balance closes", eq.two_stream_balance_residual(1.0, 2465.1, 188.45, ratio, 0.0, 62.7), 0.0, 1e-9)
# Eq. 6.48, Ex 6.14: eta_c = (285.58-249.75)/(294.17-249.75) = 0.81
chk("isentropic_compressor_efficiency", eq.isentropic_compressor_efficiency(249.75, 294.17, 285.58), 0.81, 0.005)
# Ex 10.1 (ideal R-134a): h1=247.23, h2s=264.7, h3=h4=85.75 kJ/kg, mdot=0.08 kg/s
h4 = eq.throttling_exit_enthalpy(85.75)
chk("throttling h4 = h3", h4, 85.75)
chk("Wc Ex10.1 (kW)", 0.08 * eq.vc_compressor_work_per_mass(247.23, 264.7), 1.4, 0.005)
chk("capacity Ex10.1 (ton)", 0.08 * eq.refrigeration_capacity_per_mass(247.23, h4) * 60.0 / 211.0, 3.67, 0.01)
chk("beta Ex10.1", eq.cop_refrigeration_vc(247.23, 264.7, h4), 9.24, 0.01)
chk("beta_max Ex10.1", eq.carnot_cop_refrigeration(299.0, 273.0), 10.5, 0.005)
# Ex 10.4 (R-134a heat pump): h1=242.54, h2=280.19, h3=105.29 kJ/kg, mdot=0.2 kg/s
chk("Qout Ex10.4 (kW)", 0.2 * eq.vc_condenser_heat_per_mass(280.19, 105.29), 34.98, 0.005)
chk("gamma Ex10.4", eq.cop_heat_pump_vc(242.54, 280.19, 105.29), 4.65, 0.01)
chk("first law Ex10.4 (kW)", eq.heat_pump_first_law(27.45, 7.53), 34.98, 1e-9)
# Carnot identity gamma_max = beta_max + 1
chk("carnot_cop_heat_pump", eq.carnot_cop_heat_pump(299.0, 273.0), 11.5, 0.005)
chk("Carnot identity", eq.carnot_cop_heat_pump(299.0, 273.0),
    eq.carnot_cop_refrigeration(299.0, 273.0) + 1.0, 1e-9)

# ---- (2) cross-checks: concept modules match the registry ------------------
# 08.1 compressor
chk("08.1 mdot = AV/v", compressor.mass_flow_rate(0.1, 6.0, 0.8323),
    eq.mass_flow_rate(0.1, 6.0, 0.8323))
chk("08.1 mdot ideal gas", compressor.mass_flow_rate_ideal_gas(0.1, 6.0, 1.0e5, R_AIR, 290.0),
    eq.mass_flow_rate_ideal_gas(0.1, 6.0, 1.0e5, R_AIR, 290.0))
chk("08.1 power_cv (Ex4.5)", compressor.power_cv(0.72, 290.16e3, 451.80e3,
    Qdot=-180.0e3 / 60.0, V1=6.0, V2=2.0, g=0.0), W45)
chk("08.1 adiabatic power", compressor.power_cv(0.07, 249.75, 294.17),
    eq.compressor_power(0.07, 249.75, 294.17))
chk("08.1 eta_c", compressor.isentropic_efficiency(249.75, 294.17, 285.58),
    eq.isentropic_compressor_efficiency(249.75, 294.17, 285.58))
chk("08.1 w = h2-h1 (Eq.10.4)", compressor.actual_compressor_work(242.54, 280.19),
    eq.vc_compressor_work_per_mass(242.54, 280.19))
# eta_c round-trip through the 08.1 inverse (Ex 10.3 state 2: 241.35 -> 280.15)
h2 = compressor.exit_enthalpy_from_efficiency(241.35, 272.39, 0.80)
chk("08.1 h2 from eta_c", eq.isentropic_compressor_efficiency(241.35, h2, 272.39), 0.80, 1e-12)
# 08.2 condenser
chk("08.2 Qdot_cv", condenser.heat_transfer_rate(1.0, 2465.1, 188.45),
    eq.single_stream_heat_rate(1.0, 2465.1, 188.45))
chk("08.2 heat rejected = -Qdot_cv", condenser.heat_rejected(0.2, 280.19, 105.29),
    -eq.single_stream_heat_rate(0.2, 280.19, 105.29))
chk("08.2 Qout/mdot (Eq.10.5)", condenser.condenser_heat_per_mass(280.19, 105.29),
    eq.vc_condenser_heat_per_mass(280.19, 105.29))
# 08.3 heat exchanger
chk("08.3 balance residual", heat_exchanger.energy_balance_residual(1.0, 2465.1, 188.45, ratio, 0.0, 62.7),
    eq.two_stream_balance_residual(1.0, 2465.1, 188.45, ratio, 0.0, 62.7))
chk("08.3 mc/mh", heat_exchanger.mass_flow_ratio_cold_to_hot(2465.1, 188.45, 0.0, 62.7),
    eq.mass_flow_ratio_cold_to_hot(2465.1, 188.45, 0.0, 62.7))
chk("08.3 solve other flow", heat_exchanger.mass_flow_other(125.0, 2465.1 - 188.45, 62.7),
    125.0 * eq.mass_flow_ratio_cold_to_hot(2465.1, 188.45, 0.0, 62.7), 1e-9)
# 08.4 heat pump
chk("08.4 beta (Eq.10.7)", heat_pump.cop_ref_from_enthalpies(247.23, 264.7, 85.75),
    eq.cop_refrigeration_vc(247.23, 264.7, 85.75))
chk("08.4 gamma (Eq.10.10)", heat_pump.cop_hp_from_enthalpies(242.54, 280.19, 105.29),
    eq.cop_heat_pump_vc(242.54, 280.19, 105.29))
chk("08.4 Q_H = Q_C + W (Eq.10.8)", heat_pump.heat_rejected(27.45, 7.53),
    eq.heat_pump_first_law(27.45, 7.53))
chk("08.4 beta_max (Eq.10.1)", heat_pump.carnot_cop_refrigeration(299.0, 273.0),
    eq.carnot_cop_refrigeration(299.0, 273.0))
chk("08.4 gamma_max (Eq.10.9)", heat_pump.carnot_cop_heat_pump(299.0, 273.0),
    eq.carnot_cop_heat_pump(299.0, 273.0))

print(f"All {_n} tests passed.")
