"""
test_closed_systems.py  —  checks for Module 1.2 (Closed Systems).

Run:  cd code && python3 test_closed_systems.py   ->  "All N tests passed."
Every expected value is hand-derivable (see comments).
"""
import math

from closed_systems import (delta_KE, delta_PE, energy_balance_residual,
                            heat_transfer, work_done, power_balance_residual,
                            polytropic_pressure, polytropic_work,
                            constant_pressure_work, pdv_work_trapz)

_n = 0


def chk(name, got, want, tol=1e-2):
    global _n
    if not math.isclose(got, want, rel_tol=0, abs_tol=tol):
        raise AssertionError(f"{name}: got {got!r}, want {want!r} (tol {tol})")
    _n += 1


# kinetic / potential pieces
chk("delta_KE", delta_KE(2.0, 0.0, 10.0), 0.1)            # 1/2*2*100 = 100 J
chk("delta_PE", delta_PE(2.0, 0.0, 10.0), 0.19620)        # 2*9.81*10 = 196.2 J

# energy balance: (Q - W) = dU + dKE + dPE
chk("balance residual", energy_balance_residual(100.0, 30.0, 70.0), 0.0)
chk("heat_transfer", heat_transfer(W=30.0, dU=70.0), 100.0)
chk("work_done", work_done(Q=100.0, dU=70.0), 30.0)
# with kinetic & potential terms: dU = 100 - 30 - 0.1 - 0.196 = 69.704
chk("Q from full balance", heat_transfer(30.0, 69.704, 0.1, 0.19620), 100.0)
chk("power balance residual", power_balance_residual(50.0, 20.0, 30.0), 0.0)

# polytropic compression  p V^1.3 = const,  100 kPa, 1 m^3 -> 0.5 m^3
chk("polytropic_pressure", polytropic_pressure(100.0, 1.0, 0.5, 1.3), 100.0 * 2 ** 1.3)
W13 = polytropic_work(100.0, 1.0, 0.5, 1.3)               # (p2 V2 - p1 V1)/(1-n)
chk("polytropic_work n=1.3", W13, -77.05, tol=0.02)        # work IN (compression)
chk("pdV trapezoid == closed form",
    pdv_work_trapz(lambda V: 100.0 * (1.0 / V) ** 1.3, 1.0, 0.5), W13, tol=0.05)

# isothermal ideal gas  n = 1:  W = p1 V1 ln(V2/V1)
chk("polytropic_work n=1", polytropic_work(100.0, 1.0, 2.0, 1.0), 100.0 * math.log(2.0))
chk("pdV trapezoid n=1",
    pdv_work_trapz(lambda V: 100.0 / V, 1.0, 2.0), 100.0 * math.log(2.0), tol=1e-3)

# polytropic n = 0  must reduce to constant-pressure work  p (V2 - V1)
chk("constant_pressure_work", constant_pressure_work(200.0, 1.0, 3.0), 400.0)
chk("n=0 == const pressure", polytropic_work(200.0, 1.0, 3.0, 0.0), 400.0)

# adiabatic (Q=0) compression raises internal energy by |W|
chk("adiabatic dU = -W", work_done(Q=0.0, dU=0.0) - W13, -W13)

print(f"All {_n} tests passed.")
