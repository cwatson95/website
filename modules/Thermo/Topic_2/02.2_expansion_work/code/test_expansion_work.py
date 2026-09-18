"""test_expansion_work.py — checks for Module 2.2.  Run: python3 test_expansion_work.py"""
import math
from expansion_work import expansion_work, constant_pressure_expansion, isothermal_expansion

_n = 0
def chk(name, got, want, tol=1e-3):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

chk("const-p expansion", constant_pressure_expansion(200.0, 1.0, 1.5), 100.0)
chk("isothermal expansion", isothermal_expansion(100.0, 1.0, 2.0), 100.0 * math.log(2.0))
chk("∫p dV const-p", expansion_work(lambda V: 200.0, 1.0, 1.5), 100.0)
chk("expansion is positive", constant_pressure_expansion(200.0, 1.0, 1.5) > 0, True)

# compressing through the expansion API must raise
try:
    expansion_work(lambda V: 200.0, 1.5, 1.0)
    raise AssertionError("should have rejected V2 < V1")
except ValueError:
    _n += 1

# ---- Moran Example 2.1 (pp.50-52): pV^n = const, p1 = 3 bar, 0.1 -> 0.2 m^3 ----
_P1, _V1, _V2 = 300.0, 0.1, 0.2                    # kPa, m^3
# (a) n = 1.5 -> p2 = 1.06 bar, W = +17.6 kJ
chk("Ex 2.1 p2 (n=1.5)", _P1 * (_V1 / _V2) ** 1.5 / 100.0, 1.06, tol=5e-3)
chk("Ex 2.1(a) W, n=1.5",
    expansion_work(lambda V: _P1 * _V1 ** 1.5 / V ** 1.5, _V1, _V2), 17.6, tol=0.05)
# (b) n = 1.0 -> W = +20.79 kJ, closed form and quadrature must agree
chk("Ex 2.1(b) W, n=1.0", isothermal_expansion(_P1, _V1, _V2), 20.79, tol=5e-3)
chk("Ex 2.1(b) quadrature", expansion_work(lambda V: _P1 * _V1 / V, _V1, _V2),
    isothermal_expansion(_P1, _V1, _V2), tol=1e-6)
# (c) n = 0 -> W = +30 kJ
chk("Ex 2.1(c) W, n=0", constant_pressure_expansion(_P1, _V1, _V2), 30.0)
# work falls as n rises, for the same end volumes
assert (constant_pressure_expansion(_P1, _V1, _V2)
        > isothermal_expansion(_P1, _V1, _V2)
        > expansion_work(lambda V: _P1 * _V1 ** 1.5 / V ** 1.5, _V1, _V2));  _n += 1

# Quick Quiz (p.52): isothermal 0.1 -> 0.15, then constant p to 0.2.  Ans 22.16 kJ.
_leg1 = isothermal_expansion(_P1, _V1, 0.15)
_pmid = _P1 * _V1 / 0.15                           # pressure on the isotherm at 0.15
chk("Ex 2.1 Quick Quiz two-step", _leg1 + constant_pressure_expansion(_pmid, 0.15, _V2),
    22.16, tol=5e-3)

print(f"All {_n} tests passed.")
