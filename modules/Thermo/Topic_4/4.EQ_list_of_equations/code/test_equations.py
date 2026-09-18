"""
test_equations.py  —  checks for Module 4.EQ.

(1) each canonical Topic-4 equation reproduces a known value;
(2) CROSS-CHECK -- the concept modules 4.1/4.2/4.3/4.4/4.5 compute the same things.

Run:  cd code && python3 test_equations.py   ->  "All N tests passed."
"""
import math
import os
import sys

import equations as eq

_HERE = os.path.dirname(os.path.abspath(__file__))
for _s in ("04.1_enthalpy", "04.2_entropy", "04.3_exergy",
           "04.4_phase_change", "04.5_gibbs_phase_rule"):
    sys.path.insert(0, os.path.join(_HERE, "..", "..", _s, "code"))
import enthalpy as m_enth        # noqa: E402
import entropy as m_entr         # noqa: E402
import exergy as m_exrg          # noqa: E402
import phase_change as m_phase   # noqa: E402
import gibbs_phase_rule as m_gpr # noqa: E402

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1


# ---- (1) canonical values --------------------------------------------------
chk("enthalpy", eq.enthalpy(2537.3, 100.0, 1.793), 2716.6, 0.05)
chk("enthalpy_total", eq.enthalpy_total(100.0, 200.0, 0.5), 200.0)
chk("quality", eq.quality(55.6, 79.44), 0.7, 0.01)
chk("mixture_property", eq.mixture_property(1.0435e-3, 1.673, 0.9), 1.506, 1e-3)
chk("Ds incompressible", eq.entropy_change_incompressible(4.2, 295.0, 300.0), 4.2 * math.log(300.0 / 295.0))
chk("Ds ideal gas cp", eq.entropy_change_ideal_gas_cp(1.005, 0.287, 300.0, 600.0, 100.0, 100.0), 1.005 * math.log(2.0))
chk("sigma closed", eq.entropy_production_closed(6.8379, 1.8418, 0.0), 4.9961, 1e-4)
chk("specific_exergy dead", eq.specific_exergy(10.0, 1.0, 2.0, 10.0, 1.0, 2.0, 300.0, 100.0), 0.0)
chk("exergy_transfer_heat", eq.exergy_transfer_heat(2114.1, 293.15, 423.15), 649.49, 0.1)
chk("exergy_destruction", eq.exergy_destruction(537.0, 0.15959), 85.70, 0.1)
chk("gibbs_phase_rule", eq.gibbs_phase_rule(1, 2), 1)

# ---- (2) cross-checks: concept modules match the registry ------------------
chk("4.1 enthalpy", m_enth.enthalpy(2537.3, 100.0, 1.793), eq.enthalpy(2537.3, 100.0, 1.793))
chk("4.4 quality", m_phase.quality(55.6, 79.44), eq.quality(55.6, 79.44))
chk("4.4 mixture", m_phase.mixture_property(1.0435e-3, 1.673, 0.9), eq.mixture_property(1.0435e-3, 1.673, 0.9))
chk("4.2 Ds incompressible", m_entr.entropy_change_incompressible(4.2, 295.0, 300.0), eq.entropy_change_incompressible(4.2, 295.0, 300.0))
chk("4.2 Ds cp", m_entr.entropy_change_ideal_gas_cp(1.005, 0.287, 300.0, 600.0, 100.0, 100.0), eq.entropy_change_ideal_gas_cp(1.005, 0.287, 300.0, 600.0, 100.0, 100.0))
chk("4.2 sigma", m_entr.entropy_production_closed(6.8379, 1.8418, 0.0), eq.entropy_production_closed(6.8379, 1.8418, 0.0))
chk("4.3 exergy heat", m_exrg.exergy_transfer_heat(2114.1, 293.15, 423.15), eq.exergy_transfer_heat(2114.1, 293.15, 423.15))
chk("4.3 exergy destruction", m_exrg.exergy_destruction(537.0, 0.15959), eq.exergy_destruction(537.0, 0.15959))
chk("4.5 phase rule", m_gpr.gibbs_phase_rule(2, 1), eq.gibbs_phase_rule(2, 1))

print(f"All {_n} tests passed.")
