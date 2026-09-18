"""test_quasiequilibrium.py — checks for Module 1.5.  Run: python3 test_quasiequilibrium.py"""
import math
from quasiequilibrium import (pdv_work, constant_pressure_work,
                              constant_volume_work, polytropic_work, path_work)

_n = 0


def chk(name, got, want, tol=1e-2):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: got {got!r}, want {want!r}"
    _n += 1


# constant-pressure and constant-volume legs
chk("const p work", constant_pressure_work(100.0, 2.0, 1.0), -100.0)
chk("const V work", constant_volume_work(2.0), 0.0)

# isothermal n=1 path A->B: W = p1 V1 ln(V2/V1)
chk("isothermal work", polytropic_work(100.0, 2.0, 1.0, 1.0), 100.0 * 2.0 * math.log(0.5))
# numerical ∫p dV along p = 200/V matches the closed form
chk("pdv == closed form", pdv_work(lambda V: 200.0 / V, 2.0, 1.0),
    100.0 * 2.0 * math.log(0.5), tol=1e-3)

# PATH DEPENDENCE: same end states A=(100,2) -> B=(200,1), three paths, three works
W1 = polytropic_work(100.0, 2.0, 1.0, 1.0)                       # isothermal
W2 = path_work([("p", 100.0, 2.0, 1.0), ("V", 1.0)])            # const-p then const-V
W3 = path_work([("V", 2.0), ("p", 200.0, 2.0, 1.0)])            # const-V then const-p
chk("path1 isothermal", W1, -138.63, tol=0.02)
chk("path2", W2, -100.0)
chk("path3", W3, -200.0)
assert not math.isclose(W1, W2) and not math.isclose(W2, W3), "paths should differ — work is path-dependent"
_n += 1

print(f"All {_n} tests passed.")
