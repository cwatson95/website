"""
test_equations.py  —  checks for Module 9.EQ.

(1) each canonical Topic-9 equation reproduces a known (book-verified) value;
(2) CROSS-CHECK -- ALL SIX concept modules (09.1 carnot, 09.2 otto, 09.3 diesel,
    09.4 dual, 09.5 brayton, 09.6 rankine) compute the same things, so the cycle
    equations are used consistently across the whole topic.  A formula change
    anywhere fails this test.

Run:  cd code && python3 test_equations.py   ->  "All N tests passed."
"""
import math
import os
import sys

import equations as eq

_HERE = os.path.dirname(os.path.abspath(__file__))
for _s in ("09.1_carnot_cycle", "09.2_otto_cycle", "09.3_diesel_cycle",
           "09.4_dual_cycle", "09.5_brayton_cycle", "09.6_rankine_cycle"):
    sys.path.insert(0, os.path.join(_HERE, "..", "..", _s, "code"))
import carnot_cycle    # noqa: E402  (09.1)
import otto_cycle      # noqa: E402  (09.2)
import diesel_cycle    # noqa: E402  (09.3)
import dual_cycle      # noqa: E402  (09.4)
import brayton_cycle   # noqa: E402  (09.5)
import rankine_cycle   # noqa: E402  (09.6)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1


# ---- (1) canonical values (book-verified) -----------------------------------
chk("carnot 2000/400 K", eq.carnot_efficiency(400.0, 2000.0), 0.80)             # Ex 5.1
chk("mep Ex 9.1", eq.mean_effective_pressure(0.382, 0.02, 0.0025), 21.83, 0.01) # Btu/ft^3 -> 8.03 atm
chk("otto air-table Ex 9.1", eq.otto_efficiency_air_table(92.04, 211.3, 721.44, 342.2), 0.51, 0.002)
chk("otto T2 Ex 9.1 cold", eq.otto_temp_after_compression(540.0, 8.0), 1241.0, 0.6)
chk("otto T4 Ex 9.1 cold", eq.otto_temp_after_expansion(3600.0, 8.0), 1567.0, 0.6)
chk("otto eta r=8", eq.otto_efficiency(8.0), 0.565, 0.001)                      # Ex 9.1 table
chk("diesel air-table Ex 9.2", eq.diesel_efficiency_air_table(214.07, 664.3, 930.98, 1999.1), 0.578, 0.001)
chk("diesel eta r=18,rc=2", eq.diesel_efficiency(18.0, 2.0), 0.632, 0.001)      # Ex 9.2 note
chk("dual air-table Ex 9.3", eq.dual_efficiency_air_table(214.07, 673.2, 1065.8, 1452.6, 1778.3, 475.96), 0.635, 0.001)
chk("dual eta r=18,rp=1.5,rc=1.2", eq.dual_efficiency(18.0, 1.5, 1.2), 0.6798, 0.001)
chk("brayton wt Ex 9.4", eq.brayton_turbine_work(1515.4, 808.5), 706.9, 0.01)
chk("brayton wc Ex 9.4", eq.brayton_compressor_work(300.19, 579.9), 279.71, 0.01)
chk("brayton qin Ex 9.4", eq.brayton_heat_added(579.9, 1515.4), 935.5, 0.01)
chk("brayton qout Ex 9.4", eq.brayton_heat_rejected(300.19, 808.5), 508.31, 0.01)
chk("brayton eta Ex 9.4", eq.brayton_efficiency_air_table(300.19, 579.9, 1515.4, 808.5), 0.457, 0.001)
chk("brayton bwr Ex 9.4", eq.brayton_back_work_ratio(300.19, 579.9, 1515.4, 808.5), 0.396, 0.001)
chk("brayton T2 cold Ex 9.4", eq.brayton_temp_after_compression(300.0, 10.0), 579.2, 0.05)
chk("brayton T4 cold Ex 9.4", eq.brayton_temp_after_expansion(1400.0, 10.0), 725.1, 0.05)
chk("brayton eta rp=10", eq.brayton_efficiency(10.0), 0.482, 0.001)             # Ex 9.4 table
chk("regenerator Ex 9.7", eq.regenerator_effectiveness(762.8, 579.9, 808.5), 0.80, 0.001)
chk("rankine wt Ex 8.1", eq.rankine_turbine_work(2758.0, 1794.8), 963.2, 0.01)
chk("rankine qout Ex 8.1", eq.rankine_condenser_heat(1794.8, 173.88), 1620.92, 0.01)
chk("rankine wp Ex 8.1", eq.rankine_pump_work(173.88, 181.94), 8.06, 0.001)
chk("rankine qin Ex 8.1", eq.rankine_boiler_heat(181.94, 2758.0), 2576.06, 0.01)
chk("rankine eta Ex 8.1", eq.rankine_efficiency(2758.0, 1794.8, 173.88, 181.94), 0.371, 0.001)
chk("rankine bwr Ex 8.1", eq.rankine_back_work_ratio(2758.0, 1794.8, 173.88, 181.94), 8.37e-3, 0.01e-3)
chk("rankine wp approx Ex 8.1", eq.rankine_pump_work_approx(1.0084e-3, 8.0, 8000.0), 8.06, 0.01)

# ---- (2) cross-checks: concept modules match the registry -------------------
# 09.1 Carnot
chk("09.1 carnot", carnot_cycle.carnot_efficiency(400.0, 2000.0),
    eq.carnot_efficiency(400.0, 2000.0))
# 09.2 Otto (+ shared mep, Eq. 9.1)
chk("09.2 mep", otto_cycle.mean_effective_pressure(0.382, 0.02, 0.0025),
    eq.mean_effective_pressure(0.382, 0.02, 0.0025))
chk("09.2 eta air-table", otto_cycle.otto_efficiency_air_table(92.04, 211.3, 721.44, 342.2),
    eq.otto_efficiency_air_table(92.04, 211.3, 721.44, 342.2))
chk("09.2 T2", otto_cycle.temp_after_isentropic_compression(540.0, 8.0),
    eq.otto_temp_after_compression(540.0, 8.0))
chk("09.2 T4", otto_cycle.temp_after_isentropic_expansion(3600.0, 8.0),
    eq.otto_temp_after_expansion(3600.0, 8.0))
chk("09.2 eta(r)", otto_cycle.otto_efficiency(8.0), eq.otto_efficiency(8.0))
# 09.3 Diesel
chk("09.3 eta air-table", diesel_cycle.diesel_efficiency_air_table(214.07, 664.3, 930.98, 1999.1),
    eq.diesel_efficiency_air_table(214.07, 664.3, 930.98, 1999.1))
chk("09.3 eta(r,rc)", diesel_cycle.diesel_efficiency(18.0, 2.0), eq.diesel_efficiency(18.0, 2.0))
# 09.4 dual (mep in the per-unit-mass form: V1-V2 = v1(1-1/r) per kg)
chk("09.4 eta air-table", dual_cycle.dual_efficiency_air_table(214.07, 673.2, 1065.8, 1452.6, 1778.3, 475.96),
    eq.dual_efficiency_air_table(214.07, 673.2, 1065.8, 1452.6, 1778.3, 475.96))
chk("09.4 eta(r,rp,rc)", dual_cycle.dual_efficiency(18.0, 1.5, 1.2), eq.dual_efficiency(18.0, 1.5, 1.2))
chk("09.4 mep", dual_cycle.mean_effective_pressure(456.4, 0.861, 18.0),
    eq.mean_effective_pressure(456.4, 0.861, 0.861 / 18.0))
# the dual closed form brackets Otto (rc->1) and Diesel (rp->1) across modules
chk("09.4->09.2 limit", dual_cycle.dual_efficiency(18.0, 1.5, 1.0 + 1e-9),
    eq.otto_efficiency(18.0), 1e-4)
chk("09.4->09.3 limit", dual_cycle.dual_efficiency(18.0, 1.0 + 1e-9, 2.0),
    eq.diesel_efficiency(18.0, 2.0), 1e-4)
# 09.5 Brayton
chk("09.5 wt", brayton_cycle.turbine_work(1515.4, 808.5), eq.brayton_turbine_work(1515.4, 808.5))
chk("09.5 wc", brayton_cycle.compressor_work(300.19, 579.9), eq.brayton_compressor_work(300.19, 579.9))
chk("09.5 qin", brayton_cycle.heat_added(579.9, 1515.4), eq.brayton_heat_added(579.9, 1515.4))
chk("09.5 qout", brayton_cycle.heat_rejected(300.19, 808.5), eq.brayton_heat_rejected(300.19, 808.5))
chk("09.5 eta air-table", brayton_cycle.brayton_efficiency_air_table(300.19, 579.9, 1515.4, 808.5),
    eq.brayton_efficiency_air_table(300.19, 579.9, 1515.4, 808.5))
chk("09.5 bwr", brayton_cycle.back_work_ratio(300.19, 579.9, 1515.4, 808.5),
    eq.brayton_back_work_ratio(300.19, 579.9, 1515.4, 808.5))
chk("09.5 T2", brayton_cycle.temp_after_isentropic_compression(300.0, 10.0),
    eq.brayton_temp_after_compression(300.0, 10.0))
chk("09.5 T4", brayton_cycle.temp_after_isentropic_expansion(1400.0, 10.0),
    eq.brayton_temp_after_expansion(1400.0, 10.0))
chk("09.5 eta(rp)", brayton_cycle.brayton_efficiency(10.0), eq.brayton_efficiency(10.0))
chk("09.5 regenerator", brayton_cycle.regenerator_effectiveness(762.8, 579.9, 808.5),
    eq.regenerator_effectiveness(762.8, 579.9, 808.5))
# 09.6 Rankine
chk("09.6 wt", rankine_cycle.turbine_work(2758.0, 1794.8), eq.rankine_turbine_work(2758.0, 1794.8))
chk("09.6 qout", rankine_cycle.condenser_heat(1794.8, 173.88), eq.rankine_condenser_heat(1794.8, 173.88))
chk("09.6 wp", rankine_cycle.pump_work(173.88, 181.94), eq.rankine_pump_work(173.88, 181.94))
chk("09.6 qin", rankine_cycle.boiler_heat(181.94, 2758.0), eq.rankine_boiler_heat(181.94, 2758.0))
chk("09.6 eta", rankine_cycle.rankine_efficiency(2758.0, 1794.8, 173.88, 181.94),
    eq.rankine_efficiency(2758.0, 1794.8, 173.88, 181.94))
chk("09.6 bwr", rankine_cycle.back_work_ratio(2758.0, 1794.8, 173.88, 181.94),
    eq.rankine_back_work_ratio(2758.0, 1794.8, 173.88, 181.94))
chk("09.6 wp approx", rankine_cycle.pump_work_approx(1.0084e-3, 8.0, 8000.0),
    eq.rankine_pump_work_approx(1.0084e-3, 8.0, 8000.0))
# every cycle sits below its Carnot ceiling (09.1 caps the topic)
assert eq.otto_efficiency(8.0) < eq.carnot_efficiency(540.0, 3600.0);            _n += 1
assert eq.brayton_efficiency_air_table(300.19, 579.9, 1515.4, 808.5) \
    < eq.carnot_efficiency(300.0, 1400.0);                                       _n += 1
assert eq.rankine_efficiency(2758.0, 1794.8, 173.88, 181.94) \
    < eq.carnot_efficiency(41.51 + 273.15, 295.1 + 273.15);                      _n += 1

print(f"All {_n} tests passed.")
