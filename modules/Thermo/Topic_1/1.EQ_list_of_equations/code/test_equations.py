"""
test_equations.py  —  checks for Module 1.EQ.

Two layers:
  (1) each canonical equation reproduces a known numerical value;
  (2) CROSS-CHECK — the sibling concept modules (1.1/1.2/1.4/1.5) compute the same
      thing, so Topic 1's equations are used consistently everywhere.

Run:  cd code && python3 test_equations.py   ->  "All N tests passed."
"""
import math
import os
import sys

import equations as eq

# make the sibling modules importable
_HERE = os.path.dirname(os.path.abspath(__file__))
for _s in ("01.1_open_systems", "01.2_closed_systems",
           "01.4_intensive_properties", "01.5_quasiequilibrium"):
    sys.path.insert(0, os.path.join(_HERE, "..", "..", _s, "code"))
import open_systems          # noqa: E402
import closed_systems        # noqa: E402
import intensive             # noqa: E402
import quasiequilibrium      # noqa: E402

_n = 0


def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1


# ---- (1) numerical correctness of the canonical forms ----------------------
chk("specific_volume", eq.specific_volume(1.5, 3.0), 0.5)
chk("density", eq.density(3.0, 1.5), 2.0)
chk("celsius_to_kelvin", eq.celsius_to_kelvin(25.0), 298.15)
chk("kelvin_to_rankine", eq.kelvin_to_rankine(300.0), 540.0)
chk("gauge_to_absolute", eq.gauge_to_absolute(100.0, 101.325), 201.325)
chk("enthalpy", eq.enthalpy(2000.0, 100.0, 1.5), 2150.0)
chk("mass_flow_rate", eq.mass_flow_rate(0.1, 20.0, 0.2), 10.0)
chk("mass_rate_residual", eq.mass_rate_residual(10.0, 10.0), 0.0)
chk("flow_energy", eq.flow_energy(2700.0, 100.0), 2705.0)
chk("delta_KE", eq.delta_KE(2.0, 0.0, 10.0), 0.1)
chk("delta_PE", eq.delta_PE(2.0, 0.0, 10.0), 0.19620)
chk("closed_system_heat", eq.closed_system_heat(30.0, 70.0), 100.0)
chk("boundary_work", eq.boundary_work(lambda V: 200.0 / V, 2.0, 1.0), 200.0 * math.log(0.5), tol=1e-3)
chk("polytropic_pressure", eq.polytropic_pressure(100.0, 1.0, 0.5, 1.3), 100.0 * 2 ** 1.3)
chk("polytropic_work n!=1", eq.polytropic_work(100.0, 1.0, 0.5, 1.3), -77.05, tol=0.02)
chk("polytropic_work n=1", eq.polytropic_work(100.0, 1.0, 2.0, 1.0), 100.0 * math.log(2.0))

# ---- (2) cross-checks: siblings must match the canonical registry ----------
chk("1.1 mass_flow_rate", open_systems.mass_flow_rate(0.1, 20.0, 0.2), eq.mass_flow_rate(0.1, 20.0, 0.2))
chk("1.1 flow_energy", open_systems.flow_energy(2700.0, 100.0, 10.0), eq.flow_energy(2700.0, 100.0, 10.0))
chk("1.2 delta_KE", closed_systems.delta_KE(2.0, 0.0, 10.0), eq.delta_KE(2.0, 0.0, 10.0))
chk("1.2 delta_PE", closed_systems.delta_PE(2.0, 0.0, 10.0), eq.delta_PE(2.0, 0.0, 10.0))
chk("1.2 polytropic_work", closed_systems.polytropic_work(100.0, 1.0, 0.5, 1.3), eq.polytropic_work(100.0, 1.0, 0.5, 1.3))
chk("1.2 polytropic_pressure", closed_systems.polytropic_pressure(100.0, 1.0, 0.5, 1.3), eq.polytropic_pressure(100.0, 1.0, 0.5, 1.3))
chk("1.5 polytropic_work", quasiequilibrium.polytropic_work(100.0, 1.0, 0.5, 1.3), eq.polytropic_work(100.0, 1.0, 0.5, 1.3))
chk("1.4 specific_volume", intensive.specific_volume(1.5, 3.0), eq.specific_volume(1.5, 3.0))
chk("1.4 density", intensive.density(3.0, 1.5), eq.density(3.0, 1.5))
# closed-system heat solver agrees with 1.2's heat_transfer
chk("1.2 closed_system_heat", closed_systems.heat_transfer(30.0, 70.0), eq.closed_system_heat(30.0, 70.0))

print(f"All {_n} tests passed.")
