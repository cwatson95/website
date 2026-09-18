"""
homework.py  —  Module 4.HP (Topic 4: end-of-chapter homework, Moran Ch.3/6/7)

8 problems from Moran 8e (printed pp.152-419), one per function, each SOLVED from its
given data (steam-table values cited from Tables A-2..A-5).  Moran has no answer key,
so these are *worked solutions*, reproduced and checked in test_homework.py (with
energy/entropy/exergy-balance consistency).

Statements in ../problems.md; citations in ../refs.md.  English problems use
T(degR)=T(degF)+459.67.
"""
import math


def linear_interp(x, x1, x2, y1, y2):
    """Linear interpolation y(x) between (x1,y1) and (x2,y2)."""
    return y1 + (x - x1) / (x2 - x1) * (y2 - y1)


def p3_46():
    """Water, sat. vapor @4 bar, RIGID, heated to 400 C. Find Q/m. (p.155)
    Rigid -> W=0, Q/m = u2 - u1. At 400 C find p where v = v1 (interp A-4 5/7 bar)."""
    u1, v1 = 2553.6, 0.4625                      # ug, vg @4 bar (Table A-3)
    u2 = linear_interp(v1, 0.6173, 0.4397, 2963.2, 2960.9)   # @400 C, 5 bar -> 7 bar
    return {"u2": u2, "Q_m": u2 - u1}


def p3_63():
    """Water, 20 bar, x1=0.8, V=0.5 m^3, RIGID, cooled to 4 bar. Find Q. (p.156)"""
    vf1, vg1, uf1, ug1 = 1.1767e-3, 0.09963, 906.44, 2600.3        # @20 bar (A-3)
    v1 = vf1 + 0.8 * (vg1 - vf1)
    u1 = uf1 + 0.8 * (ug1 - uf1)
    m = 0.5 / v1
    vf2, vg2, uf2, ug2 = 1.0836e-3, 0.4625, 604.31, 2553.6        # @4 bar (A-3)
    x2 = (v1 - vf2) / (vg2 - vf2)                # rigid: v2 = v1
    u2 = uf2 + x2 * (ug2 - uf2)
    return {"m": m, "x2": x2, "Q": m * (u2 - u1)}


def p3_70():
    """Water, 5 kg, 5 bar, 240 C, CONSTANT-PRESSURE, Q=2960 kJ. Find T2, W. (p.157)"""
    m, p, Q = 5.0, 500.0, 2960.0                 # p in kPa
    h1, v1 = 2939.9, 0.4646                       # @5 bar, 240 C (A-4)
    h2 = h1 + Q / m                               # const-p: Q = m dh
    T2 = linear_interp(h2, 3483.9, 3701.7, 500.0, 600.0)          # A-4 @5 bar
    v2 = linear_interp(h2, 3483.9, 3701.7, 0.7109, 0.8041)
    return {"h2": h2, "T2": T2, "W": m * p * (v2 - v1)}


def p6_11():
    """Air (ideal gas) 300 K/100 kPa -> 500 K/650 kPa. Find Ds (rev = irrev). (p.347)"""
    s0_1, s0_2, R = 1.70203, 2.21952, 0.287       # Table A-22
    return {"ds": s0_2 - s0_1 - R * math.log(650.0 / 100.0)}


def p6_37():
    """2 m^3 air, RIGID insulated, paddle work 710 kJ; 293 K, 200 kPa, cv=0.72. Find m, T2, sigma. (p.350)"""
    R, cv = 0.287, 0.72
    m = 200.0 * 2.0 / (R * 293.0)
    T2 = 293.0 + 710.0 / (m * cv)                 # adiabatic rigid: dU = -W = +710
    sigma = m * cv * math.log(T2 / 293.0)         # rigid: Ds = m cv ln(T2/T1)
    return {"m": m, "T2": T2, "sigma": sigma}


def p6_59():
    """1 kg metal @1075 K (c=0.5) quenched in 100 kg water @295 K (c=4.2), isolated.
    Find Tf, sigma. (p.352)"""
    mm, cm, Tm = 1.0, 0.5, 1075.0
    mw, cw, Tw = 100.0, 4.2, 295.0
    Tf = (mm * cm * Tm + mw * cw * Tw) / (mm * cm + mw * cw)
    sigma = mm * cm * math.log(Tf / Tm) + mw * cw * math.log(Tf / Tw)
    return {"Tf": Tf, "sigma": sigma}


def p7_21():
    """Concrete slab 0.3x4x6 m (rho=2300, c=0.88) warmed 298 -> 301 K; T0=298 K.
    Find exergy increase and equivalent lift height of a 1000 kg mass. (p.417)"""
    m = 2300.0 * (0.3 * 4.0 * 6.0)
    c, T1, T2, T0 = 0.88, 298.0, 301.0, 298.0
    dE = m * c * ((T2 - T1) - T0 * math.log(T2 / T1))     # kJ
    z = dE * 1000.0 / (1000.0 * 9.81)                     # kJ->J, /(m_load g)
    return {"dE": dE, "z": z}


def p7_36():
    """1 lb metal @2000 degR (c=0.1) quenched in 25 lb water @500 degR (c=1.0); T0=537 degR.
    Find exergy destroyed. (p.419)"""
    mm, cm, Tm = 1.0, 0.1, 2000.0
    mw, cw, Tw = 25.0, 1.0, 500.0
    Tf = (mm * cm * Tm + mw * cw * Tw) / (mm * cm + mw * cw)
    sigma = mm * cm * math.log(Tf / Tm) + mw * cw * math.log(Tf / Tw)
    return {"Tf": Tf, "sigma": sigma, "Ed": 537.0 * sigma}


def _demo():
    print("Module 4.HP -- Topic 4 homework (worked solutions, no book key)\n")
    print("  3.46 water rigid heated:   Q/m = %.1f kJ/kg" % p3_46()["Q_m"])
    r = p3_63(); print("  3.63 water rigid cooled:   m=%.2f kg, x2=%.3f, Q = %.0f kJ" % (r["m"], r["x2"], r["Q"]))
    r = p3_70(); print("  3.70 water const-p:        h2=%.1f, T2=%.0f C, W = %.0f kJ" % (r["h2"], r["T2"], r["W"]))
    print("  6.11 air Ds (a property):  Ds = %.4f kJ/kg.K" % p6_11()["ds"])
    r = p6_37(); print("  6.37 air rigid+paddle:     m=%.3f kg, T2=%.1f K, sigma=%.2f kJ/K" % (r["m"], r["T2"], r["sigma"]))
    r = p6_59(); print("  6.59 thermal mixing:       Tf=%.2f K, sigma=%.3f kJ/K" % (r["Tf"], r["sigma"]))
    r = p7_21(); print("  7.21 warmed slab:          dE=%.1f kJ, lift z=%.1f m" % (r["dE"], r["z"]))
    r = p7_36(); print("  7.36 quench (exergy):      Ed = %.1f Btu" % r["Ed"])


if __name__ == "__main__":
    _demo()
