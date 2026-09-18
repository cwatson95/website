"""test_compression_work.py — checks for Module 2.3.  Run: python3 test_compression_work.py"""
import math
from compression_work import compression_work, work_input, polytropic_compression

_n = 0
def chk(name, got, want, tol=1e-2):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

chk("polytropic n=1.3", polytropic_compression(100.0, 1.0, 0.5, 1.3), -77.05, 0.02)
chk("isothermal compression", polytropic_compression(100.0, 2.0, 1.0, 1.0), 100.0 * 2.0 * math.log(0.5), 1e-6)
chk("compression is negative", polytropic_compression(100.0, 1.0, 0.5, 1.3) < 0, True)
chk("work_input = -W > 0", work_input(lambda V: 150.0, 1.0, 0.6), 60.0)   # -(150*(0.6-1))
chk("compression ∫p dV", compression_work(lambda V: 150.0, 1.0, 0.6), -60.0)

# expanding through the compression API must raise
try:
    compression_work(lambda V: 200.0, 1.0, 1.5)
    raise AssertionError("should have rejected V2 > V1")
except ValueError:
    _n += 1

# ---- the table in notes.md §3: 1 bar, 1.0 -> 0.5 m^3 along four exponents ----
_P1, _V1, _V2 = 100.0, 1.0, 0.5
_TABLE = {1.0: (200.0, 69.31), 1.2: (229.7, 74.35),
          1.3: (246.2, 77.05), 1.4: (263.9, 79.88)}
for _n_exp, (_p2, _win) in _TABLE.items():
    chk("p2 at n=%.1f" % _n_exp, _P1 * (_V1 / _V2) ** _n_exp, _p2, tol=0.06)
    chk("work input at n=%.1f" % _n_exp,
        -polytropic_compression(_P1, _V1, _V2, _n_exp), _win, tol=6e-3)
# the bill rises monotonically with n
_costs = [-polytropic_compression(_P1, _V1, _V2, x) for x in (1.0, 1.2, 1.3, 1.4)]
assert _costs == sorted(_costs) and _costs[0] < _costs[-1];  _n += 1
# closed form == numerical quadrature
chk("quadrature agrees, n=1.3",
    work_input(lambda V: _P1 * _V1 ** 1.3 / V ** 1.3, _V1, _V2),
    -polytropic_compression(_P1, _V1, _V2, 1.3), tol=1e-3)

# Retracing one isotherm in both directions must cancel exactly.  On pV = const
# through (300 kPa, 0.2 m^3) the product is 60 kPa.m^3, so the pressure at
# V = 0.1 m^3 is 60/0.1 = 600 kPa -- NOT 300*(0.2/0.1)^-1.
_W_compress = polytropic_compression(300.0, 0.2, 0.1, 1.0)   # 0.2 -> 0.1, negative
_W_expand = polytropic_compression(600.0, 0.1, 0.2, 1.0)     # 0.1 -> 0.2, positive
chk("same isotherm, opposite directions", _W_expand, -_W_compress, tol=1e-9)
assert _W_compress < 0 < _W_expand;  _n += 1

print(f"All {_n} tests passed.")
