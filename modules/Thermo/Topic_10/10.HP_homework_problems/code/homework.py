"""
homework.py  —  Module 10.HP (Topic 10: end-of-chapter homework, Moran Ch.5/9)

8 problems on the Carnot and Stirling engines, one per function, each SOLVED
from complete given data.  P1-P3 are Moran 8e Ch.5 "Checking Understanding"
items (p.277) whose answer is fixed by the physics; P6-P8 are built on the
Ch.9 end-of-chapter Stirling problems 9.102-9.103 (p.601).  Moran provides no
worked key, so all are *worked solutions*, reproduced and checked (with
balance/consistency closures) in test_homework.py.

Statements in ../problems.md; citations in ../refs.md.  Temperatures ABSOLUTE:
T(K) = T(degC) + 273.15; T(degR) = T(degF) + 459.67.  Cycle Q, W are positive
magnitudes unless signed per process (P8).
"""
import math

R_AIR, CV_AIR = 0.287, 0.718        # kJ/kg.K
RBAR_ENG = 1.986                     # Btu/(lbmol.degR)
M_HELIUM = 4.003                     # lb/lbmol = kg/kmol (Table A-1, p.926)


def to_kelvin(T_C):
    """Absolute temperature: T(K) = T(degC) + 273.15."""
    return T_C + 273.15


def to_rankine(T_F):
    """Absolute temperature: T(degR) = T(degF) + 459.67."""
    return T_F + 459.67


def _status(eta, eta_max, tol=1e-9):
    """Carnot-corollary verdict (Example 5.1 logic)."""
    if eta > eta_max + tol:
        return "impossible"
    if eta > eta_max - tol:
        return "reversible"
    return "irreversible"


def p1():
    """CU #24 (p.277) + inventor upgrade.  A power cycle receives Q_H = 1000 kJ
    from a reservoir at 1000 K and discharges Q_C = 500 kJ to one at 400 K.
    (a) eta and verdict.  (b) An inventor claims a redesign rejecting only
    Q_C = 300 kJ for the same Q_H and reservoirs: verdict.  Eqs. 5.4, 5.9."""
    T_H, T_C, Q_H = 1000.0, 400.0, 1000.0
    eta_max = 1.0 - T_C / T_H                       # 0.60
    eta_a = 1.0 - 500.0 / Q_H                       # 0.50
    eta_b = 1.0 - 300.0 / Q_H                       # 0.70
    return {"eta_a": eta_a, "eta_max": eta_max,
            "verdict_a": _status(eta_a, eta_max),   # irreversible (possible)
            "eta_b": eta_b,
            "verdict_b": _status(eta_b, eta_max)}   # impossible


def p2():
    """CU #23 (p.277): Carnot efficiency at point b of Fig. 5.12 -- T_C = 298 K
    with T_H = 1225 degC.  eta_max = 1 - T_C/T_H (Eq. 5.9), T absolute."""
    T_H, T_C = to_kelvin(1225.0), 298.0             # 1498.15 K
    return {"T_H": T_H, "eta_max": 1.0 - T_C / T_H}  # 0.801 (~80%)


def p3():
    """CU #17 (p.277): Carnot gas power cycle (Fig. 5.13), ideal gas.  Given
    p1 = 3 atm, v1 = 4.2 ft3/lb, p4 = 1 atm, find v4.  States 4 and 1 sit on
    the same isotherm T_C (Process 4-1), so p v = const: v4 = p1 v1 / p4."""
    p1_, v1, p4_ = 3.0, 4.2, 1.0
    return {"v4": p1_ * v1 / p4_}                   # 12.6 ft3/lb


def p4():
    """Maximum work / minimum rejection.  A power cycle receives Q_H = 1000 kJ
    between reservoirs at 745 K and 298 K (the Sec. 5.9.1 example pair).
    Find eta_max, W_max, and the minimum Q_C.  Eqs. 5.9, 5.7."""
    T_H, T_C, Q_H = 745.0, 298.0, 1000.0
    eta_max = 1.0 - T_C / T_H                       # 0.60
    W_max = eta_max * Q_H                           # 600 kJ
    return {"eta_max": eta_max, "W_max": W_max, "Q_C_min": Q_H - W_max}


def p5():
    """Minimum refrigerator power (Ex 5.2 data + Quick Quiz claim).  A freezer
    at -5 degC (268 K) in surroundings at 22 degC (295 K) must reject
    Qdot_C = 8000 kJ/h.  Find beta_max, the minimum power input, and judge an
    inventor's claim of running it on 800 kJ/h.  Eqs. 5.5, 5.10."""
    T_C, T_H, Qdot_C = 268.0, 295.0, 8000.0
    beta_max = T_C / (T_H - T_C)                    # 9.926
    Wdot_min = Qdot_C / beta_max                    # 806 kJ/h
    beta_claim = Qdot_C / 800.0                     # 10 > beta_max
    return {"beta_max": beta_max, "Wdot_min_kJ_h": Wdot_min,
            "Wdot_min_kW": Wdot_min / 3600.0,
            "beta_claim": beta_claim,
            "claim_valid": beta_claim <= beta_max}  # False


def p6():
    """Problem 9.102 (p.601): 36 g of air execute a Stirling cycle, compression
    ratio r = 6; at the start of the isothermal compression p1 = 1 bar and
    V1 = 0.03 m3; the isothermal expansion is at T_H = 1000 K.  Find (a) the
    net work, (b) eta, (c) the mep.  Ideal gas; Eq. 2.17 form; Eq. 9.1."""
    m, r = 0.036, 6.0
    p1_, V1, T_H = 100.0, 0.03, 1000.0              # kPa, m3, K
    T_C = p1_ * V1 / (m * R_AIR)                    # 290.4 K (ideal gas at state 1)
    Q_34 = m * R_AIR * T_H * math.log(r)            # 18.51 kJ in at T_H
    Q_12 = m * R_AIR * T_C * math.log(r)            # 5.375 kJ out at T_C
    W_net = Q_34 - Q_12                             # 13.14 kJ
    eta = 1.0 - T_C / T_H                           # 0.710
    mep = W_net / (V1 - V1 / r)                     # kPa (Eq. 9.1)
    return {"T_C": T_C, "Q_34": Q_34, "Q_12": Q_12, "W_net": W_net,
            "eta": eta, "eta_from_heats": W_net / Q_34, "mep_bar": mep / 100.0}


def p7():
    """Problem 9.102 continued -- the regenerator's worth.  For the cycle of
    P6, find the constant-volume heat c_v(T_H - T_C) and eta if (a) there is
    NO regenerator (that heat becomes an external input), (b) the regenerator
    is 80% effective (20% of it remains external).  Compare with P6."""
    m = 0.036
    r6 = p6()
    T_C, T_H = r6["T_C"], 1000.0
    Q_regen = m * CV_AIR * (T_H - T_C)              # 18.34 kJ per cycle
    eta_full = r6["eta"]                            # 0.710 (ideal regeneration)
    eta_none = r6["W_net"] / (r6["Q_34"] + Q_regen)             # 0.356
    eta_80 = r6["W_net"] / (r6["Q_34"] + 0.20 * Q_regen)        # 0.592
    return {"Q_regen": Q_regen, "eta_full": eta_full,
            "eta_none": eta_none, "eta_80": eta_80}


def p8():
    """Problem 9.103 (p.601) + Stirling-vs-Carnot.  Helium executes a Stirling
    cycle: isothermal compression from 15 lbf/in2, 100 degF to 150 lbf/in2;
    isothermal expansion at 1500 degF.  Find (a) the work and heat transfer
    for each process, Btu/lb (Moran signs: Q positive INTO the gas, W positive
    BY the gas), and (b) eta; check eta equals the Carnot value.
    R = Rbar/M with M_He = 4.003 (Table A-1, p.926); c_v = (3/2)R (monatomic)."""
    R = RBAR_ENG / M_HELIUM                          # 0.4961 Btu/lb.degR
    c_v = 1.5 * R                                    # 0.7442 Btu/lb.degR
    T_C, T_H = to_rankine(100.0), to_rankine(1500.0)  # 559.67 / 1959.67 degR
    v_ratio = 15.0 / 150.0                           # V2/V1 = p1/p2 isothermally
    W_12 = R * T_C * math.log(v_ratio)               # -639.4 Btu/lb (in, = Q_12)
    W_34 = R * T_H * math.log(1.0 / v_ratio)         # +2238.7 Btu/lb (out, = Q_34)
    Q_23 = c_v * (T_H - T_C)                         # +1041.9 Btu/lb (regenerator in, W=0)
    Q_41 = -Q_23                                     # -1041.9 Btu/lb (regenerator out, W=0)
    W_net = W_34 + W_12                              # 1599.3 Btu/lb
    eta = W_net / W_34                               # 0.714 (external Q_in = Q_34)
    return {"R": R, "c_v": c_v, "T_C": T_C, "T_H": T_H,
            "W_12": W_12, "Q_12": W_12, "W_34": W_34, "Q_34": W_34,
            "Q_23": Q_23, "Q_41": Q_41, "W_net": W_net,
            "eta": eta, "eta_carnot": 1.0 - T_C / T_H}


def _demo():
    print("Module 10.HP -- Topic 10 homework (worked solutions, no book key)\n")
    r = p1(); print("  P1 1000/400 K, 1000->500 kJ: eta = %.2f vs %.2f -> %s; claim Q_C=300 -> %s"
                    % (r["eta_a"], r["eta_max"], r["verdict_a"], r["verdict_b"]))
    r = p2(); print("  P2 Fig 5.12 point b:         eta_max = %.3f (~80%%) at T_H = %.0f K" % (r["eta_max"], r["T_H"]))
    r = p3(); print("  P3 Carnot isotherm 4-1:      v4 = %.1f ft3/lb" % r["v4"])
    r = p4(); print("  P4 745/298 K, Q_H=1000 kJ:   W_max = %.0f kJ, Q_C_min = %.0f kJ" % (r["W_max"], r["Q_C_min"]))
    r = p5(); print("  P5 freezer 268/295 K:        Wdot_min = %.0f kJ/h (%.3f kW); 800 kJ/h claim -> %s"
                    % (r["Wdot_min_kJ_h"], r["Wdot_min_kW"], "valid" if r["claim_valid"] else "invalid"))
    r = p6(); print("  P6 (9.102) air Stirling r=6: W = %.2f kJ, eta = %.3f, mep = %.2f bar"
                    % (r["W_net"], r["eta"], r["mep_bar"]))
    r = p7(); print("  P7 regenerator's worth:      eta = %.3f (ideal) / %.3f (80%%) / %.3f (none)"
                    % (r["eta_full"], r["eta_80"], r["eta_none"]))
    r = p8(); print("  P8 (9.103) He Stirling:      W12 = %.0f, W34 = %.0f, Qregen = %.0f Btu/lb"
                    % (r["W_12"], r["W_34"], r["Q_23"]))
    print("                               eta = %.3f = Carnot %.3f" % (r["eta"], r["eta_carnot"]))


if __name__ == "__main__":
    _demo()
