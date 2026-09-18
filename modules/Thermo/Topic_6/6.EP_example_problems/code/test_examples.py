"""test_examples.py — checks for Module 6.EP (Moran Ch.4/6 examples).  Run: python3 test_examples.py"""
import math
from examples import (ex_4_1, ex_4_2, ex_4_4, ex_6_1, ex_6_2, ex_6_3, ex_6_4, ex_6_5,
                      ex_6_9, ex_6_10, ex_6_11, ex_6_12)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# Ex 4.1 -- feedwater heater
e = ex_4_1()
chk("4.1 mdot3", e["mdot3"], 54.15, 0.01)
chk("4.1 mdot2", e["mdot2"], 14.15, 0.01)
chk("4.1 V2", e["V2"], 5.7, 0.05)

# Ex 4.2 -- barrel steady height
chk("4.2 L", ex_4_2()["L_steady"], 3.333, 1e-3)

# Ex 4.4 -- steam turbine heat transfer
e = ex_4_4()
chk("4.4 dke", e["dke"], 0.4, 1e-9)
chk("4.4 Qcv", e["Qcv"], -62.3, 0.1)

# Ex 6.1 -- internally reversible water
e = ex_6_1()
chk("6.1 W/m", e["W_per_m"], 186.38, 0.05)
chk("6.1 Q/m", e["Q_per_m"], 2114.1, 0.5)

# Ex 6.2 -- irreversible water
e = ex_6_2()
chk("6.2 W/m", e["W_per_m"], -1927.82, 0.01)
chk("6.2 sigma/m", e["sigma_per_m"], 4.9961, 1e-4)

# Ex 6.3 -- minimum compression work
chk("6.3 Wmin", ex_6_3()["W_in_min"], 12.78, 1e-6)

# Ex 6.4 -- gearbox entropy production rate
e = ex_6_4()
chk("6.4 sigmadot_a", e["sigmadot_a"], 4.0e-3, 1e-5)
chk("6.4 sigmadot_b", e["sigmadot_b"], 4.1e-3, 5e-5)

# Ex 6.5 -- quenching a hot bar
e = ex_6_5()
chk("6.5 Tf", e["Tf"], 535.0, 0.5)
chk("6.5 sigma", e["sigma"], 0.0864, 1e-3)

# Ex 6.9 -- isentropic air
e = ex_6_9()
chk("6.9 p2 pr", e["p2_pr"], 15.28, 0.01)
chk("6.9 p2 k", e["p2_k"], 15.26, 0.05)

# Ex 6.10 -- air leaking from a tank
e = ex_6_10()
chk("6.10 pr2", e["pr2"], 1.6822, 1e-4)
chk("6.10 m2", e["m2"], 1.58, 0.01)

# Ex 6.11 -- turbine work from efficiency
chk("6.11 W/m", ex_6_11()["W_per_m"], 271.95, 0.05)

# Ex 6.12 -- turbine isentropic efficiency
e = ex_6_12()
chk("6.12 Ws", e["Ws"], 105.6, 0.05)
chk("6.12 eta_t", e["eta_t"], 0.70, 0.005)

print(f"All {_n} tests passed.")
