"""
test_equations.py  —  checks for Module 2.EQ.

(1) each canonical work/energy equation reproduces a known value;
(2) CROSS-CHECK — the Topic-2 concept modules (2.1/2.2/2.3/2.4/2.5/2.6) compute
    the same thing, so the topic's equations are used consistently.

Run:  cd code && python3 test_equations.py   ->  "All N tests passed."
"""
import math
import os
import sys

import equations as eq

_HERE = os.path.dirname(os.path.abspath(__file__))
for _s in ("02.1_work", "02.2_expansion_work", "02.3_compression_work",
           "02.4_power", "02.5_kinetic_energy", "02.6_potential_energy"):
    sys.path.insert(0, os.path.join(_HERE, "..", "..", _s, "code"))
import work                # noqa: E402
import power               # noqa: E402
import kinetic_energy      # noqa: E402
import potential_energy    # noqa: E402
import expansion_work      # noqa: E402
import compression_work    # noqa: E402

_n = 0


def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1


# ---- (1) canonical values --------------------------------------------------
chk("general_work", eq.general_work(lambda s: 50.0, 0.0, 3.0), 150.0, 1e-3)
chk("boundary_work", eq.boundary_work(lambda V: 200.0, 1.0, 1.5), 100.0, 1e-3)
chk("shaft_work", eq.shaft_work(18.0, 100.0, 1.0), 1800.0)
chk("shaft_power", eq.shaft_power(18.0, 100.0), 1800.0)
chk("electric_work", eq.electric_work(110.0, 10.0, 1.0), 1100.0)
chk("electric_power", eq.electric_power(110.0, 10.0), 1100.0)
chk("spring_work", eq.spring_work(200.0, 0.0, 0.1), 1.0)
chk("power_force_velocity", eq.power_force_velocity(500.0, 4.0), 2000.0)
chk("kinetic_energy", eq.kinetic_energy(2.0, 10.0), 100.0)
chk("delta_KE", eq.delta_KE(1000.0, 100.0, 20.0), -4.8e6)
chk("potential_energy", eq.potential_energy(2.0, 10.0), 196.2)
chk("delta_PE", eq.delta_PE(10.0, 0.0, 50.0), 4905.0)
chk("total_energy", eq.total_energy(100.0, 5.0, 2.0), 107.0)

# ---- (2) cross-checks: Topic-2 modules match the registry ------------------
chk("2.1 general", work.work_force_displacement(lambda s: 50.0, 0.0, 3.0), eq.general_work(lambda s: 50.0, 0.0, 3.0), 1e-3)
chk("2.1 boundary", work.boundary_work(lambda V: 200.0, 1.0, 1.5), eq.boundary_work(lambda V: 200.0, 1.0, 1.5), 1e-3)
chk("2.1 shaft_work", work.shaft_work(18.0, 100.0, 1.0), eq.shaft_work(18.0, 100.0, 1.0))
chk("2.1 electric_work", work.electric_work(110.0, 10.0, 1.0), eq.electric_work(110.0, 10.0, 1.0))
chk("2.1 spring_work", work.spring_work(200.0, 0.0, 0.1), eq.spring_work(200.0, 0.0, 0.1))
chk("2.4 shaft_power", power.shaft_power(18.0, 100.0), eq.shaft_power(18.0, 100.0))
chk("2.4 electric_power", power.electric_power(110.0, 10.0), eq.electric_power(110.0, 10.0))
chk("2.4 force*velocity", power.power_force_velocity(500.0, 4.0), eq.power_force_velocity(500.0, 4.0))
chk("2.5 kinetic_energy", kinetic_energy.kinetic_energy(2.0, 10.0), eq.kinetic_energy(2.0, 10.0))
chk("2.5 delta_KE", kinetic_energy.delta_KE(1000.0, 100.0, 20.0), eq.delta_KE(1000.0, 100.0, 20.0))
chk("2.6 potential_energy", potential_energy.potential_energy(2.0, 10.0), eq.potential_energy(2.0, 10.0))
chk("2.6 delta_PE", potential_energy.delta_PE(10.0, 0.0, 50.0), eq.delta_PE(10.0, 0.0, 50.0))
chk("2.2 expansion==boundary", expansion_work.expansion_work(lambda V: 200.0, 1.0, 1.5), eq.boundary_work(lambda V: 200.0, 1.0, 1.5), 1e-3)
chk("2.3 compression==boundary", compression_work.compression_work(lambda V: 150.0, 1.0, 0.6), eq.boundary_work(lambda V: 150.0, 1.0, 0.6), 1e-3)

print(f"All {_n} tests passed.")
