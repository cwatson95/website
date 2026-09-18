"""test_homework.py — checks for Module 6.HP.  Run: python3 test_homework.py"""
import math
from homework import p4_34, p4_42, p6_17, p6_24, p6_37, p6_40, p6_43, p6_53

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# 4.34 -- air nozzle
r = p4_34()
chk("4.34 v1", r["v1"], 0.369, 1e-3)
chk("4.34 A1", r["A1"], 0.283, 1e-3)
chk("4.34 dke", r["dke"], 105.8, 0.05)
chk("4.34 Q", r["Q"], -105.5, 0.1)
assert r["Q"] < 0.0;   _n += 1                       # heat out of the cooling stream

# 4.42 -- insulated steam turbine
r = p4_42()
chk("4.42 dke", r["dke"], -4.0, 1e-6)
chk("4.42 W", r["W"], 6927.0, 1.0)
assert r["W"] > 0.0;   _n += 1                       # turbine develops power

# 6.17 -- argon final volume
r = p6_17()
chk("6.17 V2", r["V2"], 0.500, 5e-3)
assert r["V2"] < 1.0;  _n += 1                       # compressed -> smaller volume

# 6.24 -- isothermal internally reversible work
r = p6_24()
chk("6.24 Q", r["Q"], -120.0, 1e-9)
chk("6.24 W", r["W"], -120.0, 1e-9)                  # ideal-gas isothermal: W = Q (dU=0)

# 6.37 -- air paddle, rigid insulated
r = p6_37()
chk("6.37 m", r["m"], 4.757, 1e-2)
chk("6.37 T2", r["T2"], 500.3, 0.5)
chk("6.37 sigma", r["sigma"], 1.83, 0.01)
assert r["sigma"] > 0.0;  _n += 1                    # irreversible stirring

# 6.40 -- air paddle, k=1.4
r = p6_40()
chk("6.40 p2", r["p2"], 8.0, 0.01)
chk("6.40 m", r["m"], 0.890, 1e-3)
chk("6.40 W", r["W"], -200.0, 0.2)                   # work input (negative)
chk("6.40 sigma", r["sigma"], 0.443, 1e-3)

# 6.43 -- adiabatic compression (cold-air standard)
r = p6_43()
chk("6.43 sigma", r["sigma"], 0.0358, 1e-3)
chk("6.43 T2s", r["T2s"], 579.2, 0.2)
chk("6.43 Wmin", r["W_in_min"], 200.5, 0.2)
assert r["W_in_actual"] > r["W_in_min"];  _n += 1    # irreversibility exacts a penalty

# 6.53 -- heat across a finite temperature difference
r = p6_53()
chk("6.53 Q", r["Q"], 342.0, 0.1)
chk("6.53 dS", r["dS"], 0.4919, 1e-3)
chk("6.53 sigma", r["sigma"], 0.112, 1e-3)
assert r["sigma"] > 0.0;  _n += 1                    # finite-dT heat transfer is irreversible

print(f"All {_n} tests passed.")
