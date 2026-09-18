"""
homework.py  —  Module 7.HP (Topic 7: end-of-chapter homework, Moran Ch.2/5/6)

8 problems on performance metrics, one per function, each SOLVED from complete given
data.  Several (p2-p5) are Moran 8e "Checking Understanding" items (p.277) whose answer
is fixed by the physics; Moran provides no worked key, so these are *worked solutions*,
reproduced and checked in test_homework.py.

Statements in ../problems.md; citations in ../refs.md.  English problems use
T(degR)=T(degF)+459.67; Celsius uses T(K)=T(degC)+273.15.
"""


def to_rankine(T_F):
    """Absolute temperature: T(degR) = T(degF) + 459.67."""
    return T_F + 459.67


def to_kelvin(T_C):
    """Absolute temperature: T(K) = T(degC) + 273.15."""
    return T_C + 273.15


def p1():
    """Power cycle: Q_in=1000 kJ in, W_cycle=400 kJ out. Find eta and Q_out.
    eta = W/Q_in (Eq. 2.42); Q_out = Q_in - W (Eq. 2.41)."""
    Q_in, W = 1000.0, 400.0
    return {"eta": W / Q_in, "Q_out": Q_in - W}


def p2():
    """CU #6 (p.277): power cycle between 2000 F and 1000 F claims eta=45%.
    Reversible, irreversible, or impossible?  Compare with Carnot (Eq. 5.9)."""
    T_H, T_C = to_rankine(2000.0), to_rankine(1000.0)
    eta_max = 1.0 - T_C / T_H
    eta_claim = 0.45
    verdict = "impossible" if eta_claim > eta_max else "irreversible"
    return {"eta_max": eta_max, "verdict": verdict}


def p3():
    """CU #15 (p.277): maximum thermal efficiency of any power cycle between
    1000 C and 500 C.  eta_max = 1 - T_C/T_H (Eq. 5.9), T absolute."""
    T_H, T_C = to_kelvin(1000.0), to_kelvin(500.0)
    return {"eta_max": 1.0 - T_C / T_H}


def p4():
    """CU #16 (p.277): power cycle between 500 K and 300 K receives Q_H=1000 kJ.
    Find the minimum Q_C the cycle must reject.  Q_C,min = Q_H(1 - eta_max) (Eq. 5.9)."""
    T_H, T_C, Q_H = 500.0, 300.0, 1000.0
    eta_max = 1.0 - T_C / T_H
    W_max = eta_max * Q_H
    return {"eta_max": eta_max, "W_max": W_max, "Q_C_min": Q_H - W_max}


def p5():
    """CU #11 (p.277): maximum COP of any heat pump between 40 F and 80 F.
    gamma_max = T_H/(T_H - T_C) (Eq. 5.11), T absolute."""
    T_C, T_H = to_rankine(40.0), to_rankine(80.0)
    return {"gamma_max": T_H / (T_H - T_C)}


def p6():
    """Refrigerator removes Q_C=2000 kJ using W=500 kJ between T_C=250 K and T_H=300 K.
    Find beta (Eq. 2.45) and the reversible ceiling beta_max (Eq. 5.10)."""
    Q_C, W, T_C, T_H = 2000.0, 500.0, 250.0, 300.0
    return {"beta": Q_C / W, "beta_max": T_C / (T_H - T_C)}


def p7():
    """Steam turbine: h1=3000.0, actual exit h2=2680.0, isentropic exit h2s=2600.0 kJ/kg.
    Find eta_t (Eq. 6.46), the actual work, and the isentropic (ideal) work."""
    h1, h2, h2s = 3000.0, 2680.0, 2600.0
    return {"eta_t": (h1 - h2) / (h1 - h2s), "w_actual": h1 - h2, "w_ideal": h1 - h2s}


def p8():
    """Pump: h1=200.0, actual exit h2=212.5, isentropic exit h2s=210.0 kJ/kg.
    Find eta_p (Eq. 6.48, pump form) and the actual work input."""
    h1, h2, h2s = 200.0, 212.5, 210.0
    return {"eta_p": (h2s - h1) / (h2 - h1), "w_actual": h2 - h1}


def _demo():
    print("Module 7.HP -- Topic 7 homework (worked solutions, no book key)\n")
    r = p1(); print("  P1 power cycle:        eta = %.2f, Q_out = %.0f kJ" % (r["eta"], r["Q_out"]))
    r = p2(); print("  P2 2000/1000 F, 45%%:   eta_max = %.3f -> %s" % (r["eta_max"], r["verdict"]))
    r = p3(); print("  P3 1000/500 C max:     eta_max = %.3f (%.1f%%)" % (r["eta_max"], 100 * r["eta_max"]))
    r = p4(); print("  P4 500/300 K, Q_H=1000: Q_C,min = %.0f kJ (eta_max=%.2f)" % (r["Q_C_min"], r["eta_max"]))
    r = p5(); print("  P5 40/80 F heat pump:  gamma_max = %.2f" % r["gamma_max"])
    r = p6(); print("  P6 refrigerator:       beta = %.1f, beta_max = %.1f" % (r["beta"], r["beta_max"]))
    r = p7(); print("  P7 steam turbine:      eta_t = %.2f, w = %.0f kJ/kg (ideal %.0f)" % (r["eta_t"], r["w_actual"], r["w_ideal"]))
    r = p8(); print("  P8 pump:               eta_p = %.2f, w_in = %.1f kJ/kg" % (r["eta_p"], r["w_actual"]))


if __name__ == "__main__":
    _demo()
