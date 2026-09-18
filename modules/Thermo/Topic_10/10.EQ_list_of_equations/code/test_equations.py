"""
test_equations.py  —  checks for Module 10.EQ.

(1) each canonical Topic-10 equation reproduces a known (book-verified) value;
(2) CROSS-CHECKS -- BOTH concept modules, 10.1 (carnot_engine.py) and 10.2
    (stirling_engine.py), compute the same things.

Run:  cd code && python3 test_equations.py   ->  "All N tests passed."
"""
import math
import os
import sys

import equations as eq

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "10.1_carnot_engine", "code"))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "10.2_stirling_engine", "code"))
import carnot_engine as m_carnot      # noqa: E402
import stirling_engine as m_stirling  # noqa: E402

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1


R_AIR, CV_AIR = 0.287, 0.718      # kJ/kg.K

# ---- (1) canonical values (book-verified) ----------------------------------
chk("carnot_efficiency 2000/400", eq.carnot_efficiency(400.0, 2000.0), 0.80)      # Ex 5.1, p.266
chk("carnot_efficiency 745/298", eq.carnot_efficiency(298.0, 745.0), 0.60)        # Sec. 5.9.1, p.266
chk("carnot_cop_refrigerator", eq.carnot_cop_refrigerator(268.0, 295.0), 9.926, 1e-3)  # Ex 5.2 (book 9.9)
chk("carnot_cop_heat_pump", eq.carnot_cop_heat_pump(492.0, 530.0), 13.947, 1e-3)       # Ex 5.3 (book 13.95)
chk("gamma_max = beta_max + 1", eq.carnot_cop_heat_pump(268.0, 295.0),
    eq.carnot_cop_refrigerator(268.0, 295.0) + 1.0)
chk("kelvin_heat_ratio 400/2000", eq.kelvin_heat_ratio(400.0, 2000.0), 0.20)
chk("Q_C = Q_H*(T_C/T_H) [Ex 5.1c]", 1000.0 * eq.kelvin_heat_ratio(400.0, 2000.0), 200.0)
chk("isothermal_heat expansion", eq.isothermal_heat(R_AIR, 1000.0, 2.0), 198.933, 0.01)
chk("isothermal_heat compression", eq.isothermal_heat(R_AIR, 300.0, 0.5), -59.680, 0.01)
chk("stirling_efficiency 1000/300", eq.stirling_efficiency(300.0, 1000.0), 0.70)
chk("Stirling = Carnot ceiling", eq.stirling_efficiency(400.0, 2000.0),
    eq.carnot_efficiency(400.0, 2000.0))                                          # Sec. 9.8.4, p.553
chk("regenerator_heat", eq.regenerator_heat(CV_AIR, 1000.0, 300.0), 502.6, 0.01)
chk("regenerator_effectiveness 80%", eq.regenerator_effectiveness(700.0, 300.0, 800.0), 0.80)
chk("regenerator_effectiveness ideal", eq.regenerator_effectiveness(800.0, 300.0, 800.0), 1.0)

# ---- (2) cross-checks: concept module 10.1 matches the registry ------------
chk("10.1 carnot_efficiency", m_carnot.carnot_efficiency(400.0, 2000.0),
    eq.carnot_efficiency(400.0, 2000.0))
chk("10.1 kelvin_heat_ratio", m_carnot.kelvin_heat_ratio(400.0, 2000.0),
    eq.kelvin_heat_ratio(400.0, 2000.0))
chk("10.1 carnot_heat_rejected", m_carnot.carnot_heat_rejected(1000.0, 400.0, 2000.0),
    1000.0 * eq.kelvin_heat_ratio(400.0, 2000.0))
chk("10.1 carnot_work", m_carnot.carnot_work(1000.0, 400.0, 2000.0),
    eq.carnot_efficiency(400.0, 2000.0) * 1000.0)
chk("10.1 carnot_cop_refrigerator", m_carnot.carnot_cop_refrigerator(268.0, 295.0),
    eq.carnot_cop_refrigerator(268.0, 295.0))
chk("10.1 carnot_cop_heat_pump", m_carnot.carnot_cop_heat_pump(492.0, 530.0),
    eq.carnot_cop_heat_pump(492.0, 530.0))

# ---- (2) cross-checks: concept module 10.2 matches the registry ------------
chk("10.2 stirling_efficiency", m_stirling.stirling_efficiency(300.0, 1000.0),
    eq.stirling_efficiency(300.0, 1000.0))
chk("10.2 isothermal_heat", m_stirling.isothermal_heat(R_AIR, 1000.0, 2.0),
    eq.isothermal_heat(R_AIR, 1000.0, 2.0))
chk("10.2 stirling_heat_added", m_stirling.stirling_heat_added(R_AIR, 1000.0, 2.0),
    eq.isothermal_heat(R_AIR, 1000.0, 2.0))
chk("10.2 stirling_heat_rejected", m_stirling.stirling_heat_rejected(R_AIR, 300.0, 2.0),
    eq.isothermal_heat(R_AIR, 300.0, 2.0))
chk("10.2 stirling_net_work", m_stirling.stirling_net_work(R_AIR, 1000.0, 300.0, 2.0),
    eq.isothermal_heat(R_AIR, 1000.0, 2.0) - eq.isothermal_heat(R_AIR, 300.0, 2.0))
chk("10.2 regenerator_heat", m_stirling.regenerator_heat(CV_AIR, 1000.0, 300.0),
    eq.regenerator_heat(CV_AIR, 1000.0, 300.0))
chk("10.2 regenerator_effectiveness", m_stirling.regenerator_effectiveness(700.0, 300.0, 800.0),
    eq.regenerator_effectiveness(700.0, 300.0, 800.0))

# the two engines share one ceiling (Carnot corollaries; Sec. 9.8.4, p.553)
chk("10.1 == 10.2 ceiling", m_stirling.stirling_efficiency(300.0, 1000.0),
    m_carnot.carnot_efficiency(300.0, 1000.0))

print(f"All {_n} tests passed.")
