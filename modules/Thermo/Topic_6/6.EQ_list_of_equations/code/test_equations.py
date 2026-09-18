"""
test_equations.py  —  checks for Module 6.EQ.

(1) each canonical Topic-6 equation reproduces a known value;
(2) CROSS-CHECK -- the concept modules 6.1/6.2/6.3/6.4/6.5 compute the same things, so the
    equations are used consistently across the whole topic.

Run:  cd code && python3 test_equations.py   ->  "All N tests passed."
"""
import math
import os
import sys

import equations as eq

_HERE = os.path.dirname(os.path.abspath(__file__))
for _s in ("06.1_reversible_processes", "06.2_irreversible_processes", "06.3_adiabatic",
           "06.4_steady_state", "06.5_mass_conservation"):
    sys.path.insert(0, os.path.join(_HERE, "..", "..", _s, "code"))
import reversible          # noqa: E402
import irreversible        # noqa: E402
import adiabatic           # noqa: E402
import steady_state        # noqa: E402
import mass_conservation   # noqa: E402

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1


# ---- (1) canonical values --------------------------------------------------
chk("heat_int_rev_isothermal", eq.heat_int_rev_isothermal(423.15, 6.8379, 1.8418), 2114.1, 0.5)
chk("entropy_change_int_rev", eq.entropy_change_int_rev(2114.1, 423.15), 4.9961, 1e-3)
chk("entropy_production", eq.entropy_production(4.9961, 0.0), 4.9961)
chk("sigma_isolated", eq.sigma_isolated(0.1878, -0.1014), 0.0864, 1e-6)
chk("entropy_change_incompressible", eq.entropy_change_incompressible(20.0, 1.0, 535.0, 530.0), 0.1878, 1e-3)
chk("final_temp_isentropic", eq.final_temp_isentropic(300.0, 8.0, 1.0, 1.4), 300.0 * 8.0 ** (0.4 / 1.4))
chk("pressure_ratio_from_volume", eq.pressure_ratio_from_volume(1.0, 0.5, 1.4), 2.0 ** 1.4)
chk("isentropic_turbine_eff", eq.isentropic_turbine_eff(390.88, 316.88, 285.27), 0.70, 0.005)
chk("cp_from_k", eq.cp_from_k(1.4, 0.287), 1.4 * 0.287 / 0.4)
chk("cv_from_k", eq.cv_from_k(1.4, 0.287), 0.287 / 0.4)
chk("heat_rate_steady", eq.heat_rate_steady(1000.0, 4600.0 / 3600.0, 3177.2, 2345.4, V1=10.0, V2=30.0), -62.3, 0.1)
chk("mass_flow_rate", eq.mass_flow_rate(0.06, 1.0, 1.108e-3), 0.06 / 1.108e-3)
chk("steady_mass_residual", eq.steady_mass_residual([40.0, 14.15], [54.15]), 0.0, 1e-9)

# ---- (2) cross-checks: concept modules match the registry ------------------
chk("6.1 Q_int rev", reversible.heat_int_rev_isothermal(423.15, 6.8379, 1.8418),
    eq.heat_int_rev_isothermal(423.15, 6.8379, 1.8418))
chk("6.1 dS=Q/T", reversible.entropy_change_int_rev(2114.1, 423.15),
    eq.entropy_change_int_rev(2114.1, 423.15))
chk("6.2 entropy_production", irreversible.entropy_production(4.9961, 0.0),
    eq.entropy_production(4.9961, 0.0))
chk("6.2 sigma_isolated", irreversible.sigma_isolated(0.1878, -0.1014),
    eq.sigma_isolated(0.1878, -0.1014))
chk("6.2 incompressible", irreversible.entropy_change_incompressible(20.0, 1.0, 535.0, 530.0),
    eq.entropy_change_incompressible(20.0, 1.0, 535.0, 530.0))
chk("6.3 isentropic T2", adiabatic.final_temp_isentropic(300.0, 8.0, 1.0, 1.4),
    eq.final_temp_isentropic(300.0, 8.0, 1.0, 1.4))
chk("6.3 pv^k", adiabatic.pressure_ratio_from_volume(1.0, 0.5, 1.4),
    eq.pressure_ratio_from_volume(1.0, 0.5, 1.4))
chk("6.3 eta_t", adiabatic.isentropic_turbine_eff(390.88, 316.88, 285.27),
    eq.isentropic_turbine_eff(390.88, 316.88, 285.27))
chk("6.3 cp_from_k", adiabatic.cp_from_k(1.4, 0.287), eq.cp_from_k(1.4, 0.287))
chk("6.3 cv_from_k", adiabatic.cv_from_k(1.4, 0.287), eq.cv_from_k(1.4, 0.287))
chk("6.4 heat_rate_steady",
    steady_state.heat_rate_steady(1000.0, 4600.0 / 3600.0, 3177.2, 2345.4, V1=10.0, V2=30.0),
    eq.heat_rate_steady(1000.0, 4600.0 / 3600.0, 3177.2, 2345.4, V1=10.0, V2=30.0))
chk("6.5 mass_flow_rate", mass_conservation.mass_flow_rate(0.06, 1.0, 1.108e-3),
    eq.mass_flow_rate(0.06, 1.0, 1.108e-3))
chk("6.5 steady_mass_residual", mass_conservation.steady_mass_residual([40.0, 14.15], [54.15]),
    eq.steady_mass_residual([40.0, 14.15], [54.15]))

print(f"All {_n} tests passed.")
