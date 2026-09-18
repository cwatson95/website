"""test_homework.py — checks for Module 13.HP (Moran Ch.9 compressible-flow problems).
Run: python3 test_homework.py.  Moran has no answer key; these are worked solutions, with
physical-consistency cross-checks (choking test, stagnation-T conserved across a shock)."""
import math
from homework import (p9_113, p9_121, p9_123, p9_124, p9_125, p9_136, p9_137,
                      _stagT, _My)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# 9.113 -- sonic velocities
r = p9_113()
chk("9.113 air@1000K", r["air"], 633.9, 0.5)
chk("9.113 CO2@500K", r["CO2"], 348.9, 0.5)
chk("9.113 He@300K", r["He"], 1019.0, 1.0)
assert r["He"] > r["air"] > r["CO2"];  _n += 1          # light gas -> fast sound

# 9.121 -- critical ratios, evaluated for Example 9.14 (must match Ex 9.14's p*, T*)
r = p9_121()
chk("9.121 T*/To", r["T_star_ratio"], 0.83333, 1e-5)
chk("9.121 p*/po", r["p_star_ratio"], 0.52828, 1e-5)
chk("9.121 T* (Ex9.14)", r["T_star_K"], 300.0, 0.5)    # = Ex 9.14
chk("9.121 p* (Ex9.14)", r["p_star_kPa"], 528.0, 0.5)

# 9.123 -- choked converging nozzle, ideal-gas mixture
r = p9_123()
chk("9.123 p* (bar)", r["p_star_bar"], 2.72, 0.01)
assert r["choked"] is True;  _n += 1                    # 2.72 bar > 1 bar back pressure
chk("9.123 T2", r["T2"], 606.0, 1.0)
chk("9.123 V2", r["V2"], 535.7, 0.5)
chk("9.123 mdot", r["mdot"], 2.00, 0.01)

# 9.124 -- three gases, choked (a,b) vs subsonic (c)
r = p9_124()
assert r["air"]["choked"] is True;    _n += 1
assert r["CO2"]["choked"] is True;    _n += 1
assert r["argon"]["choked"] is False; _n += 1           # k=1.667 -> p*=58.5 < 60
chk("9.124 air mdot", r["air"]["mdot"], 2.607, 0.005)
chk("9.124 CO2 mdot", r["CO2"]["mdot"], 3.096, 0.005)
chk("9.124 argon M2", r["argon"]["M2"], 0.979, 0.002)
chk("9.124 argon mdot", r["argon"]["mdot"], 3.245, 0.005)
# heavier gas -> larger mdot at the same po, To, A, pressures
assert r["CO2"]["mdot"] > r["air"]["mdot"];  _n += 1

# 9.125 -- air converging nozzle; raising po chokes it
r = p9_125()
assert r["a"]["choked"] is False;  _n += 1              # p*=0.74 bar < 1 bar
chk("9.125a M2", r["a"]["M2"], 0.710, 0.002)
chk("9.125a mdot", r["a"]["mdot"], 0.4044, 0.001)
assert r["b"]["choked"] is True;   _n += 1              # p*=1.056 bar > 1 bar
chk("9.125b M2", r["b"]["M2"], 1.0)
chk("9.125b mdot", r["b"]["mdot"], 0.6280, 0.001)
assert r["b"]["mdot"] > r["a"]["mdot"];  _n += 1        # higher po -> more mass flow

# 9.136 -- normal shock
r = p9_136()
chk("9.136 My", r["My"], 0.61650, 1e-4)                 # Table 9.3 @Mx=1.8
chk("9.136 py", r["py_bar"], 1.8067, 1e-3)             # 0.5 * 3.6133
chk("9.136 pox", r["pox_bar"], 2.8729, 1e-3)
assert r["py_bar"] > 0.5;  _n += 1                      # pressure rises across shock

# 9.137 -- C-D nozzle, shock at exit plane (English)
r = p9_137()
chk("9.137 px (upstream)", r["px"], 5.980, 0.01)
chk("9.137 pox", r["pox"], 21.95, 0.02)
chk("9.137 Tox", r["Tox"], 571.1, 0.2)
chk("9.137 mdot", r["mdot"], 0.7479, 0.001)
# stagnation temperature is unchanged across the shock: Tox == Toy = Ty*(To/T)_My
chk("9.137 Tox = Toy", r["Tox"], 520.0 * _stagT(_My(1.5, 1.4), 1.4), 0.1)

print(f"All {_n} tests passed.")
