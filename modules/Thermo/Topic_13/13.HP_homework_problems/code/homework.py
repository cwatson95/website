"""
homework.py  —  Module 13.HP (Topic 13: end-of-chapter homework, Moran Ch.9 compressible flow)

7 compressible-flow problems from Moran 8e Ch.9 (printed pp.601-602), each SOLVED from its
given data.  Moran provides no answer key for end-of-chapter problems, so these are
*worked solutions*, reproduced and checked in test_homework.py (with consistency checks).

Relations are the Topic-13 set (Eqs. 9.37, 9.50-9.52, critical ratios, 9.53-9.56).
Gas constants use R = R_univ / M (SI: 8314/M J/kg.K; English: 1545/M ft.lbf/(lb.degR));
English mass flows carry gc = 32.2 lb.ft/(lbf.s^2).  Specific-heat ratios k are the
ideal-gas (Table A-20, room-temperature) values stated in each function.

Statements in ../problems.md; citations in ../refs.md.
"""
import math

GC = 32.2                       # lb.ft/(lbf.s^2)


def _stagT(M, k):
    return 1.0 + (k - 1.0) / 2.0 * M * M


def _stagP(M, k):
    return _stagT(M, k) ** (k / (k - 1.0))


def _crit_p(k):
    """p*/po = (2/(k+1))^(k/(k-1)). [Moran Eq. 9.51 @M=1, p.574]"""
    return (2.0 / (k + 1.0)) ** (k / (k - 1.0))


def _crit_T(k):
    """T*/To = 2/(k+1). [Moran Eq. 9.50 @M=1, p.578]"""
    return 2.0 / (k + 1.0)


def _mach_from_p(po_over_p, k):
    """M from po/p (invert Eq. 9.51, p.580)."""
    return math.sqrt(2.0 / (k - 1.0) * (po_over_p ** ((k - 1.0) / k) - 1.0))


def _My(Mx, k):
    """Downstream Mach across a normal shock (Eq. 9.55)."""
    return math.sqrt((Mx * Mx + 2.0 / (k - 1.0)) / ((2.0 * k / (k - 1.0)) * Mx * Mx - 1.0))


def _shock_p(Mx, k):
    """py/px (Eq. 9.54)."""
    My = _My(Mx, k)
    return (1.0 + k * Mx * Mx) / (1.0 + k * My * My)


def _shock_T(Mx, k):
    """Ty/Tx (Eq. 9.53)."""
    My = _My(Mx, k)
    return _stagT(Mx, k) / _stagT(My, k)


def speed_of_sound(k, R, T):
    """c = sqrt(k R T). SI: R [J/kg.K] -> c [m/s]. [Moran Eq. 9.37, p.570]"""
    return math.sqrt(k * R * T)


# --- 9.113  sonic velocity of three gases -----------------------------------
def p9_113():
    """Sonic velocity (ideal gas) of (a) air at 1000 K, (b) CO2 at 500 K, (c) He at 300 K.
    k and M from Table A-20 (room-temperature ideal-gas values). (p.601)"""
    Ru = 8314.0
    a = speed_of_sound(1.4, Ru / 28.97, 1000.0)         # air
    b = speed_of_sound(1.289, Ru / 44.01, 500.0)        # CO2
    c = speed_of_sound(1.667, Ru / 4.003, 300.0)        # helium
    return {"air": a, "CO2": b, "He": c}


# --- 9.121  derive critical ratios; evaluate for Example 9.14 ---------------
def p9_121():
    """(a) Show T*/To = 2/(k+1) and p*/po = (2/(k+1))^(k/(k-1)).  (b) Evaluate T* and p*
    for Example 9.14 (To=360 K, po=1.0 MPa, k=1.4). (p.601)"""
    k, To, po = 1.4, 360.0, 1.0e6
    return {"T_star_ratio": _crit_T(k), "p_star_ratio": _crit_p(k),
            "T_star_K": _crit_T(k) * To, "p_star_kPa": _crit_p(k) * po / 1e3}


# --- 9.123  converging nozzle, ideal gas mixture (choked) -------------------
def p9_123():
    """Ideal-gas mixture k=1.31, M=23, supplied at po=5 bar, To=700 K, discharging to
    1 bar; exit area 30 cm^2.  Find (a) exit T, (b) exit V, (c) mdot. (p.602)"""
    k, M_w, po, To, A2, pb = 1.31, 23.0, 5.0e5, 700.0, 30.0e-4, 1.0e5
    R = 8314.0 / M_w
    p_star = _crit_p(k) * po
    choked = pb <= p_star                                # 2.72 bar > 1 bar -> choked
    T2 = _crit_T(k) * To                                 # exit = sonic state
    p2 = p_star
    V2 = speed_of_sound(k, R, T2)
    rho2 = p2 / (R * T2)
    mdot = rho2 * A2 * V2
    return {"p_star_bar": p_star / 1e5, "choked": choked,
            "T2": T2, "V2": V2, "mdot": mdot}


# --- 9.124  converging nozzle, three gases (choked vs subsonic) -------------
def p9_124():
    """Tank at 120 lbf/in^2, 600 degR, discharging to 60 lbf/in^2; exit area 1 in^2.
    Find mdot for (a) air k=1.4, (b) CO2 k=1.26, (c) argon k=1.667. (p.602)"""
    po, To, pb, A2_in2 = 120.0, 600.0, 60.0, 1.0
    out = {}
    for tag, k, Mw in (("air", 1.4, 28.97), ("CO2", 1.26, 44.01), ("argon", 1.667, 39.94)):
        R = 1545.0 / Mw                                  # ft.lbf/(lb.degR)
        p_star = _crit_p(k) * po
        if pb <= p_star:                                 # choked
            M2, p2, T2 = 1.0, p_star, _crit_T(k) * To
        else:                                            # subsonic, exit = back pressure
            p2 = pb
            M2 = _mach_from_p(po / pb, k)
            T2 = To / _stagT(M2, k)
        V2 = M2 * speed_of_sound(k, R, T2 * GC)          # ft/s (gc inside sqrt: kR(T*gc))
        rho2 = p2 * 144.0 / (R * T2)                     # lb/ft^3
        mdot = rho2 * (A2_in2 / 144.0) * V2              # lb/s
        out[tag] = {"choked": pb <= p_star, "M2": M2, "p2": p2, "T2": T2, "mdot": mdot}
    return out


# --- 9.125  air converging nozzle; effect of raising po --------------------
def p9_125():
    """Air po=1.4 bar, To=280 K, converging nozzle to atmosphere 1 bar; exit area
    0.0013 m^2, k=1.4.  (a) mdot.  (b) mdot if po raised to 2 bar. (p.602)"""
    k, To, A2, pb = 1.4, 280.0, 0.0013, 1.0e5
    R = 8314.0 / 28.97
    res = {}
    for label, po in (("a", 1.4e5), ("b", 2.0e5)):
        p_star = _crit_p(k) * po
        if pb <= p_star:                                 # choked
            M2, p2, T2 = 1.0, p_star, _crit_T(k) * To
        else:                                            # subsonic
            p2 = pb
            M2 = _mach_from_p(po / pb, k)
            T2 = To / _stagT(M2, k)
        V2 = M2 * speed_of_sound(k, R, T2)
        mdot = (p2 / (R * T2)) * A2 * V2
        res[label] = {"choked": pb <= p_star, "M2": M2, "T2": T2, "mdot": mdot}
    return res


# --- 9.136  normal shock ----------------------------------------------------
def p9_136():
    """Air (k=1.4) normal shock: px=0.5 bar, Tx=280 K, Mx=1.8.  Find (a) py, (b) pox. (p.602)"""
    k, px, Tx, Mx = 1.4, 0.5, 280.0, 1.8
    My = _My(Mx, k)
    py = _shock_p(Mx, k) * px
    pox = _stagP(Mx, k) * px                             # stagnation upstream of shock
    return {"My": My, "py_bar": py, "pox_bar": pox}


# --- 9.137  C-D nozzle, shock at exit plane (English) ----------------------
def p9_137():
    """C-D nozzle (air, k=1.4) discharging to atmosphere 14.7 lbf/in^2, 520 degR; a normal
    shock stands at the exit plane with Mx=1.5; exit area 1.8 in^2; upstream isentropic.
    Find (a) pox, (b) Tox, (c) mdot. (p.603)"""
    k, py, Ty, Mx, A2_in2 = 1.4, 14.7, 520.0, 1.5, 1.8
    R = 1545.0 / 28.97
    My = _My(Mx, k)
    px = py / _shock_p(Mx, k)                            # upstream of shock
    Tx = Ty / _shock_T(Mx, k)
    pox = _stagP(Mx, k) * px                             # (a)
    Tox = _stagT(Mx, k) * Tx                             # (b) = Toy (To unchanged by shock)
    Vx = Mx * speed_of_sound(k, R, Tx * GC)             # ft/s
    rho_x = px * 144.0 / (R * Tx)                        # lb/ft^3
    mdot = rho_x * (A2_in2 / 144.0) * Vx                 # (c) lb/s
    return {"px": px, "Tx": Tx, "My": My, "pox": pox, "Tox": Tox, "mdot": mdot}


def _demo():
    print("Module 13.HP -- Topic 13 homework (Moran Ch.9; worked solutions, no book key)\n")
    r = p9_113()
    print("  9.113 sonic velocity: air@1000K=%.1f, CO2@500K=%.1f, He@300K=%.0f m/s"
          % (r["air"], r["CO2"], r["He"]))
    r = p9_121()
    print("  9.121 T*/To=2/(k+1)=%.4f, p*/po=%.4f; Ex9.14: T*=%.0f K, p*=%.0f kPa"
          % (r["T_star_ratio"], r["p_star_ratio"], r["T_star_K"], r["p_star_kPa"]))
    r = p9_123()
    print("  9.123 mixture k=1.31: p*=%.2f bar (choked %s) -> T2=%.0f K, V2=%.0f m/s, mdot=%.2f kg/s"
          % (r["p_star_bar"], r["choked"], r["T2"], r["V2"], r["mdot"]))
    r = p9_124()
    for g in ("air", "CO2", "argon"):
        d = r[g]
        print("  9.124 %-5s choked=%-5s M2=%.3f p2=%.1f T2=%.0f mdot=%.3f lb/s"
              % (g, d["choked"], d["M2"], d["p2"], d["T2"], d["mdot"]))
    r = p9_125()
    print("  9.125 (a) po=1.4bar: choked=%s M2=%.3f mdot=%.4f kg/s"
          % (r["a"]["choked"], r["a"]["M2"], r["a"]["mdot"]))
    print("        (b) po=2.0bar: choked=%s M2=%.1f mdot=%.4f kg/s"
          % (r["b"]["choked"], r["b"]["M2"], r["b"]["mdot"]))
    r = p9_136()
    print("  9.136 shock Mx=1.8: My=%.4f, py=%.4f bar, pox=%.4f bar"
          % (r["My"], r["py_bar"], r["pox_bar"]))
    r = p9_137()
    print("  9.137 shock@exit Mx=1.5: pox=%.2f lbf/in^2, Tox=%.1f degR, mdot=%.4f lb/s"
          % (r["pox"], r["Tox"], r["mdot"]))


if __name__ == "__main__":
    _demo()
