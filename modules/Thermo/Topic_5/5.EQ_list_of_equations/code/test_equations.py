"""
test_equations.py  —  checks for Module 5.EQ.

(1) each canonical Topic-5 equation reproduces a known value;
(2) CROSS-CHECK -- the concept modules 5.1/5.2/5.3/5.4/5.5 compute the same things, so the
    property-table and area equations are used consistently across the whole topic.  A
    formula change anywhere fails this test.

Run:  cd code && python3 test_equations.py   ->  "All N tests passed."
"""
import math
import os
import sys

import equations as eq

_HERE = os.path.dirname(os.path.abspath(__file__))
for _s in ("05.1_saturation_tables", "05.2_vapor_tables", "05.3_liquid_tables",
           "05.4_pv_diagram", "05.5_ts_diagram"):
    sys.path.insert(0, os.path.join(_HERE, "..", "..", _s, "code"))
import sat_tables      # noqa: E402  (5.1)
import vapor_tables    # noqa: E402  (5.2)
import liquid_tables   # noqa: E402  (5.3)
import pv_diagram      # noqa: E402  (5.4)
import ts_diagram      # noqa: E402  (5.5)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1


# ---- (1) canonical values --------------------------------------------------
chk("quality", eq.quality(0.295, 0.295), 0.5)
chk("mixture v@100C,x=0.9", eq.mixture(1.0435e-3, 1.673, 0.9), 1.506, 1e-3)   # Moran p.108
chk("mixture x=0 -> yf", eq.mixture(1.0432e-3, 1.694, 0.0), 1.0432e-3)
chk("mixture x=1 -> yg", eq.mixture(1.0432e-3, 1.694, 1.0), 1.694)
chk("quality_from_v round-trip", eq.quality_from_v(eq.mixture(0.001, 1.7, 0.37), 0.001, 1.7), 0.37)
chk("enthalpy_extensive", eq.enthalpy_extensive(1000.0, 100.0, 2.0), 1200.0)
chk("enthalpy h=u+pv", eq.enthalpy(2537.3, 100.0, 1.793), 2716.6, 0.05)        # Moran p.112
chk("linear_interp mid", eq.linear_interp(0.5, 0.0, 1.0, 10.0, 20.0), 15.0)
chk("linear_interp 215C", eq.linear_interp(215.0, 200.0, 240.0, 0.2060, 0.2275), 0.2141, 5e-5)
chk("v_approx is vf", eq.v_approx(1.0435e-3), 1.0435e-3)
chk("u_approx is uf", eq.u_approx(418.94), 418.94)
chk("h_approx 3.13", eq.h_approx(419.04, 1.0435e-3, 1.0e4, 101.4), 429.37, 0.1)
chk("h_approx_simple is hf", eq.h_approx_simple(419.04), 419.04)
chk("s_approx is sf", eq.s_approx(1.3069), 1.3069)
chk("work_isobaric Ex3.4", eq.work_isobaric(1000.0, 0.3066, 0.1944), -112.2, 0.05)
chk("work_pdV rectangle", eq.work_pdV([300.0, 300.0], [0.1, 0.2]), 30.0)
chk("heat_isothermal Ex6.1", eq.heat_isothermal(423.15, 1.8418, 6.8379), 2114.1, 0.1)
chk("heat_TdS rectangle", eq.heat_TdS([400.0, 400.0], [1.0, 2.0]), 400.0)
chk("carnot_efficiency", eq.carnot_efficiency(600.0, 300.0), 0.5)

# ---- (2) cross-checks: concept modules match the registry ------------------
# 5.1 saturation tables
chk("5.1 mixture", sat_tables.mixture(1.0435e-3, 1.673, 0.9), eq.mixture(1.0435e-3, 1.673, 0.9))
chk("5.1 quality_from_v", sat_tables.quality_from_v(0.8475, 1.0528e-3, 1.159),
    eq.quality_from_v(0.8475, 1.0528e-3, 1.159))
chk("5.1 linear_interp", sat_tables.linear_interp(215.0, 200.0, 240.0, 0.206, 0.2275),
    eq.linear_interp(215.0, 200.0, 240.0, 0.206, 0.2275))
# the actual A-2/A-3 mixture used in Moran Ex 3.2 matches the registry mixture
_vf1, _vg1 = sat_tables.sat_p(1.0, "vf"), sat_tables.sat_p(1.0, "vg")
chk("5.1 Ex3.2 v1 via registry", sat_tables.mixture(_vf1, _vg1, 0.5),
    eq.mixture(_vf1, _vg1, 0.5))
# 5.2 superheated vapor
chk("5.2 enthalpy", vapor_tables.enthalpy(2537.3, 100.0, 1.793),
    eq.enthalpy(2537.3, 100.0, 1.793))
chk("5.2 linear_interp", vapor_tables.linear_interp(215.0, 200.0, 240.0, 0.206, 0.2275),
    eq.linear_interp(215.0, 200.0, 240.0, 0.206, 0.2275))
# 5.3 compressed liquid approximations
chk("5.3 v_approx", liquid_tables.v_approx(1.0435e-3), eq.v_approx(1.0435e-3))
chk("5.3 u_approx", liquid_tables.u_approx(418.94), eq.u_approx(418.94))
chk("5.3 h_approx", liquid_tables.h_approx(419.04, 1.0435e-3, 1.0e4, 101.4),
    eq.h_approx(419.04, 1.0435e-3, 1.0e4, 101.4))
chk("5.3 h_approx_simple", liquid_tables.h_approx_simple(419.04), eq.h_approx_simple(419.04))
chk("5.3 linear_interp", liquid_tables.linear_interp(0.5, 0.0, 1.0, 10.0, 20.0),
    eq.linear_interp(0.5, 0.0, 1.0, 10.0, 20.0))
# 5.4 p-v diagram (area = work)
chk("5.4 work_isobaric", pv_diagram.work_isobaric(1000.0, 0.3066, 0.1944),
    eq.work_isobaric(1000.0, 0.3066, 0.1944))
chk("5.4 work_pdV", pv_diagram.work_pdV([300.0, 300.0], [0.1, 0.2]),
    eq.work_pdV([300.0, 300.0], [0.1, 0.2]))
# 5.5 T-s diagram (area = heat)
chk("5.5 heat_isothermal", ts_diagram.heat_isothermal(423.15, 1.8418, 6.8379),
    eq.heat_isothermal(423.15, 1.8418, 6.8379))
chk("5.5 heat_TdS", ts_diagram.heat_TdS([400.0, 400.0], [1.0, 2.0]),
    eq.heat_TdS([400.0, 400.0], [1.0, 2.0]))
chk("5.5 carnot_efficiency", ts_diagram.carnot_efficiency(600.0, 300.0),
    eq.carnot_efficiency(600.0, 300.0))
# 5.4 and 5.5 share the same "area under a path" trapezoid kernel (work vs heat)
chk("5.4 work_pdV == 5.5 heat_TdS kernel", pv_diagram.work_pdV([2.0, 4.0], [0.0, 3.0]),
    ts_diagram.heat_TdS([2.0, 4.0], [0.0, 3.0]))

print(f"All {_n} tests passed.")
