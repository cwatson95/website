"""test_irreversible.py — checks for Module 6.2.  Run: python3 test_irreversible.py"""
import math
from irreversible import (IRREVERSIBILITIES, entropy_production, sigma_adiabatic,
                          entropy_production_rate, sigma_isolated,
                          entropy_change_incompressible, is_possible, classify_process)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# the canonical list of irreversibilities (Sec. 5.3.1)
assert len(IRREVERSIBILITIES) == 8;                              _n += 1
assert any("finite temperature" in s for s in IRREVERSIBILITIES); _n += 1
assert any("Friction" in s for s in IRREVERSIBILITIES);          _n += 1

# entropy balance solved for sigma:  sigma = dS - transfer
chk("sigma balance", entropy_production(4.9961, 0.0), 4.9961)
chk("sigma balance2", entropy_production(2.0, 0.5), 1.5)

# Example 6.2 -- adiabatic, irreversible water (p.308-309)
chk("Ex6.2 sigma/m", sigma_adiabatic(6.8379, 1.8418), 4.9961, 1e-4)
# energy balance for the adiabatic process gives W/m = -(u2-u1)
chk("Ex6.2 W/m", -(2559.5 - 631.68), -1927.82, 1e-2)

# Example 6.4 -- gearbox entropy production rate (p.311-312)
chk("Ex6.4 sigmadot Tb", entropy_production_rate(-1.2, 300.0), 4.0e-3, 1e-5)
chk("Ex6.4 sigmadot Tf", entropy_production_rate(-1.2, 293.0), 4.1e-3, 5e-5)

# Example 6.5 -- quench a hot bar (p.313-315); increase-of-entropy principle
dS_water = entropy_change_incompressible(20.0, 1.0, 535.0, 530.0)
dS_metal = entropy_change_incompressible(0.8, 0.1, 535.0, 1900.0)
chk("Ex6.5 dS_water", dS_water, 0.1878, 1e-3)
chk("Ex6.5 dS_metal", dS_metal, -0.1014, 1e-3)
chk("Ex6.5 sigma", sigma_isolated(dS_water, dS_metal), 0.0864, 1e-3)
assert dS_metal < 0.0 and dS_water > 0.0;     _n += 1     # bar cools (S down), water warms (S up)
assert sigma_isolated(dS_water, dS_metal) > 0.0;  _n += 1 # total increases

# feasibility / classification (Eq. 6.26)
assert is_possible(0.0) is True;          _n += 1
assert is_possible(2.0) is True;          _n += 1
assert is_possible(-1e-3) is False;       _n += 1
assert classify_process(-1.0) == "impossible";    _n += 1
assert classify_process(0.0) == "reversible";     _n += 1
assert classify_process(3.5) == "irreversible";   _n += 1

print(f"All {_n} tests passed.")
