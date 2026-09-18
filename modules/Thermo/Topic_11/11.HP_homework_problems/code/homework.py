"""
homework.py  —  Module 11.HP (Topic 11: end-of-chapter homework, Moran Ch.12 psychrometrics)

7 psychrometric problems from Moran 8e Ch.12 (printed pp.795-799), each SOLVED from its
given data.  Moran provides no answer key for end-of-chapter problems, so these are
*worked solutions*, reproduced and checked in test_homework.py (with physical-consistency
checks: dew point < dry bulb, omega ordering, mass-balance closure, etc.).

Relations are the Topic-11 set (Eqs. 12.43, 12.44, 12.46, 12.48-12.52).  Saturation
pressures and h_f/h_g are Table A-2 (SI, PDF 945) and Table A-2E (English, PDF 993) reads,
stated in each function.  Dry-air enthalpy uses ha = cpa*T (cpa = 1.005 kJ/kg.K or
0.24 Btu/lb.degR).  Following Moran's worked examples, T(K) = T(C) + 273.

Statements in ../problems.md; citations in ../refs.md.
"""

EPS = 0.622                       # Mv/Ma (Eq. 12.43)
CPA_SI = 1.005                    # kJ/kg.K, dry-air cp (chart datum, Eq. 12.51)
CPA_EN = 0.24                     # Btu/lb.degR, dry-air cp (English chart datum)
RA = 8314.0 / 28.97              # dry-air gas constant, J/kg.K
P_ATM_BAR = 1.01325              # 1 atm in bar
P_ATM_PSI = 14.696               # 1 atm in lbf/in.^2


def _omega(p_v, p):
    """omega = 0.622 pv/(p-pv). [Moran Eq. 12.43]"""
    return EPS * p_v / (p - p_v)


def _pv_from_omega(omega, p):
    """pv = omega p/(0.622+omega). [invert Eq. 12.43]"""
    return omega * p / (EPS + omega)


def _tsat_interp(p, p_lo, T_lo, p_hi, T_hi):
    """Linear interpolation of saturation temperature from two bracketing table rows."""
    return T_lo + (p - p_lo) / (p_hi - p_lo) * (T_hi - T_lo)


# --- 12.51  cooling moist air at constant pressure (SI) ---------------------
def p12_51():
    """Moist air at 30 C, 2 bar, 50% RH, 600 kg/h, cooled at constant pressure to 20 C.
    Find the rate of heat transfer.  Table A-2: pg(30)=0.04246, pg(20)=0.02339 bar;
    hg(30)=2556.3, hg(20)=2538.1 kJ/kg. (p.795, Prob. 12.51)"""
    p, phi1, mdot = 2.0, 0.50, 600.0
    pg30, pg20 = 0.04246, 0.02339
    pv1 = phi1 * pg30                                   # 0.02123 bar
    w1 = _omega(pv1, p)                                 # 0.006674
    dew_C = _tsat_interp(pv1, 0.02064, 18.0, 0.02198, 19.0)   # ~18.4 C (Table A-2)
    cond = dew_C > 20.0                                 # dew point below 20 C -> no condensate
    w2 = w1                                             # no condensation: omega constant
    ma = mdot / (1.0 + w1)                              # dry-air flow, kg/h
    Q = ma * (CPA_SI * (20.0 - 30.0) + w1 * (2538.1 - 2556.3))   # kJ/h
    return {"omega1": w1, "dew_point_C": dew_C, "condensation": cond,
            "ma": ma, "omega2": w2, "Q_kJ_per_h": Q}


# --- 12.52  isothermal compression -> condensation (English) ----------------
def p12_52():
    """2 lb moist air at 100 F, 1 atm, 40% RH, compressed isothermally to 4 atm.  If
    condensation occurs find the amount condensed.  Table A-2E: pg(100 F)=0.9503 lbf/in^2.
    (p.795, Prob. 12.52)"""
    m_tot, T_F, phi1 = 2.0, 100.0, 0.40
    pg100 = 0.9503
    p1, p2 = P_ATM_PSI, 4.0 * P_ATM_PSI
    pv1 = phi1 * pg100                                  # 0.38012
    w1 = _omega(pv1, p1)                                # 0.016516
    pv2_would_be = pv1 * (p2 / p1)                      # 1.5205 > pg100 -> condensation
    cond = pv2_would_be > pg100
    pv2 = pg100 if cond else pv2_would_be               # saturated at 100 F
    w2 = _omega(pv2, p2)                                # 0.010221
    ma = m_tot / (1.0 + w1)
    mw = ma * (w1 - w2)                                 # condensate, lb
    return {"omega1": w1, "condensation": cond, "omega2": w2, "ma": ma, "mw_condensed": mw}


# --- 12.56  dew point of an N2/water-vapor mixture (English) ----------------
def p12_56():
    """N2 + water-vapor mixture at 200 F, 1 atm, molar 80% N2 / 20% water vapor, cooled at
    constant pressure.  Find the temperature at which water vapor begins to condense.
    Table A-2E: psat=2.892 (140 F), 3.722 lbf/in^2 (150 F). (p.795, Prob. 12.56)"""
    yv, p = 0.20, P_ATM_PSI
    pv = yv * p                                         # 2.9392 lbf/in^2 = dew-point pv
    dew_F = _tsat_interp(pv, 2.892, 140.0, 3.722, 150.0)   # ~140.6 F
    return {"pv": pv, "dew_point_F": dew_F}


# --- 12.60  dehumidifier with refrigerant (SI) -----------------------------
def p12_60():
    """Air at 30 C, 1.05 bar, 80% RH enters a dehumidifier; saturated moist air exits at
    15 C, 1 bar, 95% RH; condensate exits at 15 C.  Refrigerant gains 100 kJ/kg.  Find the
    refrigerant flow per kg dry air.  Table A-2: pg(30)=0.04246, pg(15)=0.01705 bar;
    hg(30)=2556.3, hg(15)=2528.9, hf(15)=62.99. (p.796, Prob. 12.60)"""
    p1, T1, phi1 = 1.05, 30.0, 0.80
    p2, phi2 = 1.0, 0.95
    pg30, pg15 = 0.04246, 0.01705
    hg30, hg15, hf15 = 2556.3, 2528.9, 62.99
    pv1 = phi1 * pg30                                   # 0.033968
    w1 = _omega(pv1, p1)                                # 0.020795
    pv2 = phi2 * pg15                                   # 0.0161975
    w2 = _omega(pv2, p2)                                # 0.010241
    mw_per_ma = w1 - w2                                 # 0.010554
    dh_ref = 100.0                                      # he - hi, kJ/kg refrigerant
    num = CPA_SI * (T1 - 15.0) + w1 * hg30 - w2 * hg15 - mw_per_ma * hf15
    mr_per_ma = num / dh_ref
    return {"omega1": w1, "omega2": w2, "mw_per_ma": mw_per_ma, "mr_per_ma": mr_per_ma}


# --- 12.77  wet-bulb / dry-bulb, then cooling (English) ---------------------
def p12_77():
    """Air at 1 atm, dry-bulb 82 F, wet-bulb 68 F, 10 lb/min, cooled at constant pressure
    to 62 F.  Find (a) inlet relative humidity, (b) the rate of heat transfer.
    Table A-2E: pg(68)=0.3391, pg(82)=0.5414; hf(68)=36.09, hg(68)=1091.2, hg(82)=1097.3,
    hg(62)=1088.6. omega from the adiabatic-saturation (~wet-bulb) Eqs. 12.48-12.49.
    (p.797, Prob. 12.77)"""
    p, Tdb, Twb, mdot = P_ATM_PSI, 82.0, 68.0, 10.0
    pg68, pg82 = 0.3391, 0.5414
    hf68, hg68, hg82, hg62 = 36.09, 1091.2, 1097.3, 1088.6
    wprime = _omega(pg68, p)                            # omega' at Twb (Eq. 12.49)
    w1 = (CPA_EN * (Twb - Tdb) + wprime * (hg68 - hf68)) / (hg82 - hf68)   # Eq. 12.48
    pv1 = _pv_from_omega(w1, p)
    phi1 = pv1 / pg82                                   # relative humidity at inlet
    dew_F = _tsat_interp(pv1, 0.2563, 60.0, 0.2751, 62.0)   # ~61 F (Table A-2E)
    cond = dew_F > 62.0                                 # dew point below 62 F -> no condensate
    ma = mdot / (1.0 + w1)
    Q = ma * (CPA_EN * (62.0 - Tdb) + w1 * (hg62 - hg82))   # Btu/min
    return {"omega_prime": wprime, "omega1": w1, "phi1": phi1, "dew_point_F": dew_F,
            "condensation": cond, "ma": ma, "Q_Btu_per_min": Q}


# --- 12.78  dehumidifier (SI) ----------------------------------------------
def p12_78():
    """Air at 35 C, 1 atm, 50% RH enters a dehumidifier; saturated moist air and condensate
    exit, each at 15 C.  Find (a) heat transfer per kg dry air, (b) water condensed per kg
    dry air.  Table A-2: pg(35)=0.05628, pg(15)=0.01705 bar; hg(35)=2565.3, hg(15)=2528.9,
    hf(15)=62.99. (p.797, Prob. 12.78)"""
    p, T1, phi1 = P_ATM_BAR, 35.0, 0.50
    pg35, pg15 = 0.05628, 0.01705
    hg35, hg15, hf15 = 2565.3, 2528.9, 62.99
    pv1 = phi1 * pg35                                   # 0.02814
    w1 = _omega(pv1, p)                                 # 0.017767
    w2 = _omega(pg15, p)                                # 0.010646 (saturated exit)
    cond_per_ma = w1 - w2                               # 0.007122
    Q_per_ma = (CPA_SI * (15.0 - T1) - w1 * hg35 + w2 * hg15 + cond_per_ma * hf15)
    return {"omega1": w1, "omega2": w2, "condensate_per_ma": cond_per_ma,
            "Q_per_ma": Q_per_ma}


# --- 12.92  evaporative cooler (SI) ----------------------------------------
def p12_92():
    """Air at 35 C, 1 bar, 10% RH, 50 m^3/min enters an evaporative cooler; liquid water at
    20 C fully evaporates; moist air exits at 25 C, 1 bar (adiabatic).  Find (a) liquid
    water rate, (b) exit relative humidity.  Table A-2: pg(35)=0.05628, pg(25)=0.03169 bar;
    hg(35)=2565.3, hg(25)=2547.2, hf(20)=83.96. (p.799, Prob. 12.92)"""
    p, T1, phi1, AV1 = 1.0, 35.0, 0.10, 50.0
    pg35, pg25 = 0.05628, 0.03169
    hg35, hg25, hfw = 2565.3, 2547.2, 83.96            # makeup water at 20 C
    pv1 = phi1 * pg35                                   # 0.005628 bar
    w1 = _omega(pv1, p)                                 # 0.003521
    pa1 = (p - pv1) * 1e5                               # Pa
    va1 = RA * (T1 + 273.0) / pa1                       # m^3/kg dry air
    ma = AV1 / va1                                      # kg/min
    # adiabatic energy balance per unit dry air -> exit humidity ratio
    w2 = (CPA_SI * (T1 - 25.0) + w1 * (hg35 - hfw)) / (hg25 - hfw)
    mw = ma * (w2 - w1)                                 # liquid water rate, kg/min
    pv2 = _pv_from_omega(w2, p)
    phi2 = pv2 / pg25                                   # exit relative humidity
    return {"omega1": w1, "ma": ma, "omega2": w2, "liquid_rate": mw, "phi2": phi2}


def _demo():
    print("Module 11.HP -- Topic 11 psychrometric homework (worked solutions, no book key)\n")
    r = p12_51()
    print("  12.51 cooling @const p: omega1=%.5f, dew=%.1f C (no cond=%s), ma=%.1f kg/h, Q=%.0f kJ/h"
          % (r["omega1"], r["dew_point_C"], not r["condensation"], r["ma"], r["Q_kJ_per_h"]))
    r = p12_52()
    print("  12.52 isothermal compression: omega1=%.5f -> omega2=%.5f (cond=%s), mw=%.5f lb"
          % (r["omega1"], r["omega2"], r["condensation"], r["mw_condensed"]))
    r = p12_56()
    print("  12.56 N2/H2O dew point: pv=%.3f lbf/in^2 -> dew=%.1f F" % (r["pv"], r["dew_point_F"]))
    r = p12_60()
    print("  12.60 dehumidifier+refrig: omega1=%.5f, omega2=%.5f, mw/ma=%.5f, mr/ma=%.3f"
          % (r["omega1"], r["omega2"], r["mw_per_ma"], r["mr_per_ma"]))
    r = p12_77()
    print("  12.77 wet-bulb 82/68 F: omega1=%.5f, phi1=%.1f%%, dew=%.1f F, Q=%.1f Btu/min"
          % (r["omega1"], 100 * r["phi1"], r["dew_point_F"], r["Q_Btu_per_min"]))
    r = p12_78()
    print("  12.78 dehumidifier: omega1=%.5f, omega2=%.5f, cond/ma=%.5f, Q/ma=%.1f kJ/kg(da)"
          % (r["omega1"], r["omega2"], r["condensate_per_ma"], r["Q_per_ma"]))
    r = p12_92()
    print("  12.92 evap cooler: omega1=%.5f -> omega2=%.5f, ma=%.1f kg/min, liquid=%.3f kg/min, phi2=%.1f%%"
          % (r["omega1"], r["omega2"], r["ma"], r["liquid_rate"], 100 * r["phi2"]))


if __name__ == "__main__":
    _demo()
