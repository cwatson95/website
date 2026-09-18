"""
examples.py  —  Module 13.EP (Topic 13: worked Example problems, Moran Ch.9 compressible flow)

Moran 8e Chapter-9 worked Examples 9.14 and 9.15 reproduced from their GIVEN data using
the Topic-13 compressible-flow relations (isentropic functions Eqs. 9.50-9.52; critical
ratios; normal-shock functions Eqs. 9.53-9.56), so the book's published ANSWERS
regenerate and can be checked (test_examples.py).

  * Example 9.14 (printed p.579-580): converging nozzle, effect of back pressure
                 -> mass flow rate and exit Mach number for pB = 500 and 784 kPa.
  * Example 9.15 (printed p.582-585): converging-DIVERGING nozzle, five cases (a)-(e)
                 incl. choking and a normal shock -> mdot, exit pressure, exit Mach number.

Where Moran reads coarse Table 9.2 / 9.3 entries (e.g. M2 = 0.24, T2/To = 0.988), this
code uses the SAME table-read values the book quotes so the published answers reproduce
exactly ("replicate the book's stepwise rounding"); the A/A*, p*/po and the shock ratios
that the book computes are computed here too.  Each case also exposes the value Moran
computes (e.g. A2/A* = 2.6265) for verification.

Units: 9.14 SI (Pa, K, m, kg/s); 9.15 English (lbf/in.^2, degR, in.^2, lb/s).
English mass flow uses gc = 32.2 lb.ft/(lbf.s^2) and R = 1545/28.97 ft.lbf/(lb.degR).
Citations: Moran 8e (PDF = printed + 18; ../refs.md).
"""
import math

K = 1.4
R_SI = 8314.0 / 28.97               # air, J/kg.K
R_EN = 1545.0 / 28.97               # air, ft.lbf/(lb.degR)
GC = 32.2                           # lb.ft/(lbf.s^2)


# --- shared compressible-flow relations (Topic 13) --------------------------
def _stagT(M, k=K):
    return 1.0 + (k - 1.0) / 2.0 * M * M


def _stagP(M, k=K):
    return _stagT(M, k) ** (k / (k - 1.0))


def _crit_p(k=K):
    """p*/po = (2/(k+1))^(k/(k-1)). [Moran Eq. 9.51 @M=1, p.574]"""
    return (2.0 / (k + 1.0)) ** (k / (k - 1.0))


def _crit_T(k=K):
    """T*/To = 2/(k+1). [Moran Eq. 9.50 @M=1, p.578]"""
    return 2.0 / (k + 1.0)


def _area_mach(M, k=K):
    """A/A* (Moran Eq. 9.52, p.578)."""
    t = (2.0 / (k + 1.0)) * _stagT(M, k)
    return (1.0 / M) * t ** ((k + 1.0) / (2.0 * (k - 1.0)))


def _mach_from_p(po_over_p, k=K):
    """M from po/p (invert Eq. 9.51)."""
    return math.sqrt(2.0 / (k - 1.0) * (po_over_p ** ((k - 1.0) / k) - 1.0))


def _mach_from_area(A_over_Astar, supersonic, k=K):
    lo, hi = (1.0, 50.0) if supersonic else (1e-6, 1.0)
    for _ in range(200):
        m = 0.5 * (lo + hi)
        f = _area_mach(m, k) - A_over_Astar
        if supersonic:
            hi, lo = (m, lo) if f > 0 else (hi, m)
        else:
            lo, hi = (m, hi) if f > 0 else (lo, m)
    return 0.5 * (lo + hi)


def _My(Mx, k=K):
    """Downstream Mach (Moran Eq. 9.55)."""
    return math.sqrt((Mx * Mx + 2.0 / (k - 1.0)) / ((2.0 * k / (k - 1.0)) * Mx * Mx - 1.0))


def _shock_p(Mx, k=K):
    """py/px (Moran Eq. 9.54)."""
    My = _My(Mx, k)
    return (1.0 + k * Mx * Mx) / (1.0 + k * My * My)


def _poy_pox(Mx, k=K):
    """poy/pox (Moran Eq. 9.56)."""
    My = _My(Mx, k)
    E = (k + 1.0) / (2.0 * (k - 1.0))
    return (Mx / My) * (_stagT(My, k) / _stagT(Mx, k)) ** E


# --- Example 9.14: converging nozzle, effect of back pressure ---------------
def ex_9_14():
    """Converging nozzle, A2 = 0.001 m^2, air po = 1.0 MPa, To = 360 K, k = 1.4.
    mdot and exit Mach for back pressures (a) 500 kPa and (b) 784 kPa. (printed p.579-580)"""
    po, To, A2 = 1.0e6, 360.0, 0.001
    p_star = _crit_p() * po                                  # 528 kPa -> choking test
    # (a) pB = 500 kPa < p* -> CHOKED: M2 = 1, p2 = p* = 528 kPa
    M2a = 1.0
    p2a = p_star
    T2a = _crit_T() * To                                     # 300 K
    V2a = M2a * math.sqrt(K * R_SI * T2a)                    # 347.2 m/s
    mdot_a = p2a * A2 * V2a / (R_SI * T2a)                   # 2.13 kg/s
    # (b) pB = 784 kPa > p* -> SUBSONIC: p2 = pB
    p2b = 7.84e5
    M2b = _mach_from_p(po / p2b)                             # 0.6
    T2b = To / _stagT(M2b)                                   # 336 K
    V2b = M2b * math.sqrt(K * R_SI * T2b)                    # 220.5 m/s
    mdot_b = p2b * A2 * V2b / (R_SI * T2b)                   # 1.79 kg/s
    return {"p_star_kPa": p_star / 1e3, "choked_a": 500e3 <= p_star,
            "M2a": M2a, "p2a_kPa": p2a / 1e3, "T2a": T2a, "V2a": V2a, "mdot_a": mdot_a,
            "M2b": M2b, "T2b": T2b, "V2b": V2b, "mdot_b": mdot_b}


# --- Example 9.15: converging-diverging nozzle, five cases ------------------
def ex_9_15():
    """C-D nozzle, throat At = 1.0 in^2, exit A2 = 2.4 in^2, air po = 100 lbf/in^2,
    To = 500 degR, k = 1.4.  Five cases (printed p.582-585).  Table-read Mach numbers and
    isentropic ratios are the values Moran quotes from Table 9.2/9.3."""
    po, To, At, A2 = 100.0, 500.0, 1.0, 2.4

    def mdot(p2, A_in2, V_fts, T2):                          # lb/s; p2 lbf/in^2, A in^2
        rho = p2 * 144.0 / (R_EN * T2)                       # lb/ft^3
        return rho * (A_in2 / 144.0) * V_fts

    out = {}

    # (a) isentropic, Mt = 0.7 at throat
    At_Astar = _area_mach(0.7)                               # 1.09437 (Table 9.2)
    A2_Astar_a = (A2 / At) * At_Astar                        # 2.6265
    M2a = 0.24                                               # subsonic table read
    T2a = 0.988 * To                                         # T2/To = 0.988 -> 494 degR
    p2a = 0.959 * po                                         # p2/po = 0.959 -> 95.9
    V2a = M2a * math.sqrt(K * R_EN * T2a * GC)               # 262 ft/s
    out.update(At_Astar=At_Astar, A2_Astar_a=A2_Astar_a,
               M2a=M2a, T2a=T2a, p2a=p2a, V2a=V2a, mdot_a=mdot(p2a, A2, V2a, T2a))

    # (b) Mt = 1 -> At = A*, A2/A* = 2.4; subsonic root (diverging = diffuser)
    A2_Astar_b = A2 / At                                     # 2.4
    M2b = 0.26                                               # subsonic table read
    T2b = 0.986 * To                                         # 493 degR
    p2b = 0.953 * po                                         # 95.3
    V2b = M2b * math.sqrt(K * R_EN * T2b * GC)               # 283 ft/s
    mdot_b = mdot(p2b, A2, V2b, T2b)                         # 2.46 lb/s (choked, max)
    out.update(A2_Astar_b=A2_Astar_b, M2b=M2b, T2b=T2b, p2b=p2b, V2b=V2b, mdot_b=mdot_b)

    # (c) Mt = 1, diverging = supersonic nozzle: supersonic root M2 = 2.4
    M2c = 2.4
    p2c = po / _stagP(M2c)                                   # p2/po = 0.0684 -> 6.84
    out.update(M2c=M2c, p2c=p2c, mdot_c=mdot_b)              # choked: same mdot

    # (d) normal shock at exit: upstream = case (c) values Mx = 2.4, px = 6.84
    Mx_d, px_d = 2.4, p2c
    My_d = _My(Mx_d)                                         # 0.52
    py_d = _shock_p(Mx_d) * px_d                             # 6.5533 * 6.84 = 44.82
    out.update(Mx_d=Mx_d, My_d=My_d, py_px_d=_shock_p(Mx_d), py_d=py_d, mdot_d=mdot_b)

    # (e) shock in diverging section at Ax = 2.0 in^2 (A*x = At = 1.0)
    Mx_e = _mach_from_area(2.0 / At, supersonic=True)        # ~2.2 (Table 9.2)
    poy_pox_e = _poy_pox(2.2)                                # 0.62812 (use book table Mx=2.2)
    A2_Asy_e = (A2 / At) * poy_pox_e                         # 1.51
    M2e = 0.43                                               # subsonic table read after shock
    p2_poy = 1.0 / _stagP(M2e)                               # p2/poy = 0.88
    p2e = p2_poy * poy_pox_e * po                            # 55.3 lbf/in^2
    out.update(Mx_e=Mx_e, poy_pox_e=poy_pox_e, A2_Asy_e=A2_Asy_e,
               M2e=M2e, p2e=p2e, mdot_e=mdot_b)
    return out


def _demo():
    print("Module 13.EP -- Moran Ch.9 compressible-flow examples regenerated from GIVEN data\n")
    e = ex_9_14()
    print("  Ex 9.14 converging nozzle (po=1 MPa, To=360 K, A2=10^-3 m^2):")
    print("    p* = %.0f kPa (choking test)                       [book 528]" % e["p_star_kPa"])
    print("    (a) pB=500: CHOKED, M2=%.1f, p2=%.0f kPa, T2=%.0f K, V2=%.1f m/s, mdot=%.2f kg/s"
          % (e["M2a"], e["p2a_kPa"], e["T2a"], e["V2a"], e["mdot_a"]))
    print("        [book M2=1.0, p2=528, T2=300, V2=347.2, mdot=2.13]")
    print("    (b) pB=784: SUBSONIC, M2=%.2f, T2=%.0f K, V2=%.1f m/s, mdot=%.2f kg/s"
          % (e["M2b"], e["T2b"], e["V2b"], e["mdot_b"]))
    print("        [book M2=0.6, T2=336, V2=220.5, mdot=1.79]")
    g = ex_9_15()
    print("\n  Ex 9.15 C-D nozzle (po=100 lbf/in^2, To=500 R, At=1.0, A2=2.4 in^2):")
    print("    (a) Mt=0.7: A2/A*=%.4f, M2=%.2f, T2=%.0f R, p2=%.1f, V2=%.0f, mdot=%.2f lb/s"
          % (g["A2_Astar_a"], g["M2a"], g["T2a"], g["p2a"], g["V2a"], g["mdot_a"]))
    print("        [book A2/A*=2.6265, M2=0.24, T2=494, p2=95.9, V2=262, mdot=2.29]")
    print("    (b) Mt=1 (diffuser): M2=%.2f, T2=%.0f, p2=%.1f, V2=%.0f, mdot=%.2f lb/s (choked)"
          % (g["M2b"], g["T2b"], g["p2b"], g["V2b"], g["mdot_b"]))
    print("        [book M2=0.26, T2=493, p2=95.3, V2=283, mdot=2.46]")
    print("    (c) Mt=1 (nozzle): M2=%.1f, p2=%.2f lbf/in^2          [book 2.4, 6.84]"
          % (g["M2c"], g["p2c"]))
    print("    (d) shock at exit: Mx=2.4 -> My=%.2f, py/px=%.4f, py=%.2f  [book 0.52, 6.5533, 44.82]"
          % (g["My_d"], g["py_px_d"], g["py_d"]))
    print("    (e) shock at Ax=2.0: Mx=%.2f, poy/pox=%.5f, A2/A*y=%.2f, p2=%.1f  [book 2.2, 0.62812, 1.51, 55.3]"
          % (g["Mx_e"], g["poy_pox_e"], g["A2_Asy_e"], g["p2e"]))


if __name__ == "__main__":
    _demo()
