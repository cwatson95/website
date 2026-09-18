"""test_sat_tables.py — checks for Module 5.1.  Run: python3 test_sat_tables.py"""
import math
from sat_tables import (load_A2, load_A3, linear_interp, sat_T, sat_p,
                        mixture, quality_from_v, phase_pT)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

def chk_eq(name, got, want):
    global _n
    assert got == want, f"{name}: {got!r} != {want!r}"
    _n += 1

# tables load with expected row counts (steam_tables/README: A-2 70, A-3 50)
chk_eq("A-2 rows", len(load_A2()), 70)
chk_eq("A-3 rows", len(load_A3()), 50)

# exact on-grid lookups (A-2 @150 C; A-3 @1 bar)
chk("A-2 vg@150C", sat_T(150.0, "vg"), 0.3928)
chk("A-2 vf@150C", sat_T(150.0, "vf"), 1.0905e-3)
chk("A-2 sf@150C", sat_T(150.0, "sf"), 1.8418)
chk("A-2 sg@150C", sat_T(150.0, "sg"), 6.8379)
chk("A-2 p@150C", sat_T(150.0, "p"), 4.758)
chk("A-3 vf@1bar", sat_p(1.0, "vf"), 1.0432e-3)
chk("A-3 vg@1bar", sat_p(1.0, "vg"), 1.694)
chk("A-3 T@1bar", sat_p(1.0, "T"), 99.63)
chk("A-3 T@1.5bar", sat_p(1.5, "T"), 111.4)

# linear interpolation helper
chk("interp mid", linear_interp(0.5, 0.0, 1.0, 10.0, 20.0), 15.0)
# off-grid interpolation in A-2 (T=145 C, between 140 and 150)
v_chk = linear_interp(145.0, 140.0, 150.0, 0.5089, 0.3928)
chk("A-2 vg@145C interp", sat_T(145.0, "vg"), v_chk)

# Eq. 3.2 mixture + quality inversion
chk("mixture x=0", mixture(1.0432e-3, 1.694, 0.0), 1.0432e-3)
chk("mixture x=1", mixture(1.0432e-3, 1.694, 1.0), 1.694)
chk("mixture@100C,x=0.9", mixture(1.0435e-3, 1.673, 0.9), 1.506, 1e-3)   # Moran p.108
chk("quality round-trip", quality_from_v(mixture(0.001, 1.7, 0.37), 0.001, 1.7), 0.37)

# Moran Example 3.2 (water, rigid 1 bar x=0.5 -> 1.5 bar)
v1 = mixture(sat_p(1.0, "vf"), sat_p(1.0, "vg"), 0.5)
chk("Ex3.2 v1", v1, 0.8475, 1e-3)
chk("Ex3.2 m", 0.5 / v1, 0.59, 0.01)
x2 = quality_from_v(v1, sat_p(1.5, "vf"), sat_p(1.5, "vg"))
chk("Ex3.2 x2", x2, 0.731, 2e-3)
chk("Ex3.2 mg2", x2 * (0.5 / v1), 0.431, 5e-3)

# Moran Example 3.4 state 3: rigid v=0.1944, 150 C -> two-phase quality
x3 = quality_from_v(0.1944, sat_T(150.0, "vf"), sat_T(150.0, "vg"))
chk("Ex3.4 x3", x3, 0.494, 1e-3)
u3 = mixture(sat_T(150.0, "uf"), sat_T(150.0, "ug"), x3)
chk("Ex3.4 u3", u3, 1584.0, 1.0)

# Problem 3.15(a): 4 kg water in 1 m^3 at 100 C -> two-phase, quality
x_315 = quality_from_v(1.0 / 4.0, sat_T(100.0, "vf"), sat_T(100.0, "vg"))
chk("P3.15a x", x_315, 0.149, 1e-3)

# Phase determination (Problem 3.6 a-e)
chk_eq("3.6a 10bar/179.9C", phase_pT(10.0, 179.9), "two-phase")
chk_eq("3.6b 10bar/150C", phase_pT(10.0, 150.0), "compressed liquid")
chk_eq("3.6c 0.5bar/100C", phase_pT(0.5, 100.0), "superheated vapor")
chk_eq("3.6d 50bar/20C", phase_pT(50.0, 20.0), "compressed liquid")
chk_eq("3.6e 1bar/-6C", phase_pT(1.0, -6.0), "solid")

print(f"All {_n} tests passed.")
