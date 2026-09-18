"""
homework.py  —  Module 6.HP (Topic 6: end-of-chapter homework, Moran Ch.4 & Ch.6)

8 problems on Topic-6 processes & idealizations, each SOLVED from its given data.  Moran
provides no answer key, so these are *worked solutions*, reproduced and checked in
test_homework.py (with energy- and entropy-balance consistency checks).

  4.34  air nozzle: inlet area and heat transfer
  4.42  well-insulated steam turbine: power
  6.17  argon, ideal-gas entropy change -> final volume
  6.24  isothermal internally reversible ideal gas -> work
  6.37  air stirred in a rigid insulated tank -> mass, T2, sigma
  6.40  air stirred in a rigid insulated tank (k=1.4) -> p2, W, sigma
  6.43  air compressed adiabatically (cold-air standard) -> sigma, minimum work
  6.53  air heated across a finite Delta-T -> Q, sigma

Statements in ../problems.md; citations in ../refs.md.  Ideal-gas air: R = 0.287 kJ/kg.K
(English cv = 0.171 Btu/lb.R).  Argon R = 0.2081 kJ/kg.K.  Cold-air standard: k=1.4,
cp=1.005, cv=0.718 kJ/kg.K.  All temperatures used in ratios are ABSOLUTE (K or degR).
"""
import math

R_AIR = 0.287          # kJ/kg.K
R_AR = 0.2081          # kJ/kg.K (argon, M = 39.95)


def p4_34():
    """Air nozzle, steady: mdot=2.3 kg/s, T1=450 K, p1=350 kPa, V1=3 m/s; exit T2=300 K,
    V2=460 m/s; cp=1.011, R=0.287.  Find inlet area A1 (m^2) and heat transfer (kW). (p.223)"""
    mdot, T1, p1, V1, T2, V2, cp = 2.3, 450.0, 350.0, 3.0, 300.0, 460.0, 1.011
    v1 = R_AIR * T1 / p1                              # ideal gas: v = RT/p = 0.369 m3/kg
    A1 = mdot * v1 / V1                               # mdot = A V / v  -> A = mdot v / V
    dke = (V2 ** 2 - V1 ** 2) / 2.0 / 1000.0          # 105.8 kJ/kg
    Q = mdot * (cp * (T2 - T1) + dke)                 # Qdot = mdot[cp dT + dKE]
    return {"v1": v1, "A1": A1, "dke": dke, "Q": Q}


def p4_42():
    """Well-insulated steam turbine, steady: h1=3015.4, h2=2431.7 kJ/kg, V1=10, V2=90 m/s,
    mdot=11.95 kg/s.  Find the power (kW). (p.223)"""
    mdot, h1, h2, V1, V2 = 11.95, 3015.4, 2431.7, 10.0, 90.0
    dke = (V1 ** 2 - V2 ** 2) / 2.0 / 1000.0          # -4.0 kJ/kg
    W = mdot * ((h1 - h2) + dke)                      # Q=0 (insulated)
    return {"dke": dke, "W": W}


def p6_17():
    """Argon, ideal gas, k=1.67: T1=300 K, V1=1 m3 -> T2=200 K with s2-s1=-0.27 kJ/kg.K.
    Find the final volume V2 (m3). (p.348)"""
    T1, V1, T2, ds, k = 300.0, 1.0, 200.0, -0.27, 1.67
    cv = R_AR / (k - 1.0)
    # ds = cv ln(T2/T1) + R ln(v2/v1)  ->  solve for v2/v1
    ln_vratio = (ds - cv * math.log(T2 / T1)) / R_AR
    v_ratio = math.exp(ln_vratio)
    V2 = V1 * v_ratio                                 # mass constant -> V2/V1 = v2/v1
    return {"cv": cv, "v_ratio": v_ratio, "V2": V2}


def p6_24():
    """Ideal gas, internally reversible ISOTHERMAL process at T=400 K with dS=-0.3 kJ/K.
    KE/PE negligible.  Find the work (kJ). (p.348)"""
    T, dS = 400.0, -0.3
    Q = T * dS                                        # Q = INT T dS = T dS = -120 kJ
    dU = 0.0                                           # isothermal ideal gas
    W = Q - dU                                         # first law: W = Q - dU
    return {"Q": Q, "W": W}


def p6_37():
    """Air, rigid insulated tank + paddle wheel: V1=2 m3, T1=293 K, p1=200 kPa, paddle work
    in = 710 kJ, cv=0.72.  Find mass (kg), T2 (K), sigma (kJ/K). (p.350)"""
    V1, T1, p1, W_in, cv = 2.0, 293.0, 200.0, 710.0, 0.72
    m = p1 * V1 / (R_AIR * T1)                        # ideal gas
    dU = W_in                                         # Q=0, W=-W_in -> dU = -W = +W_in
    T2 = T1 + dU / (m * cv)
    sigma = m * cv * math.log(T2 / T1)               # rigid (v const) & adiabatic: sigma = dS
    return {"m": m, "T2": T2, "sigma": sigma}


def p6_40():
    """Air, rigid insulated tank + paddle wheel, k=1.4: p1=4 bar, T1=40 C, V1=0.2 m3, stirred
    to T2=353 C.  Find p2 (bar), W (kJ), sigma (kJ/K). (p.350)"""
    p1, T1, V1, T2, k = 4.0, 313.15, 0.2, 626.15, 1.4
    cv = R_AIR / (k - 1.0)                            # 0.7175
    p2 = p1 * (T2 / T1)                               # rigid: p2/p1 = T2/T1
    m = (p1 * 100.0) * V1 / (R_AIR * T1)             # p1 bar -> kPa
    W = -(m * cv * (T2 - T1))                         # Q=0: W = -dU
    sigma = m * cv * math.log(T2 / T1)               # rigid & adiabatic
    return {"cv": cv, "p2": p2, "m": m, "W": W, "sigma": sigma}


def p6_43():
    """Air compressed adiabatically 1 bar/300 K -> 10 bar/600 K.  Cold-air standard
    (k=1.4, cp=1.005, cv=0.718).  Find sigma/m (kJ/kg.K) and the minimum work input for an
    adiabatic compression to 10 bar (kJ/kg). (p.350)"""
    p1, T1, p2, T2 = 1.0, 300.0, 10.0, 600.0
    k, cp, cv = 1.4, 1.005, 0.718
    sigma = cp * math.log(T2 / T1) - R_AIR * math.log(p2 / p1)        # entropy balance, Q=0
    T2s = T1 * (p2 / p1) ** ((k - 1.0) / k)                            # isentropic end state
    W_in_min = cv * (T2s - T1)                                         # (-W/m)_min = u2s - u1
    W_in_actual = cv * (T2 - T1)                                       # actual (-W/m)
    return {"sigma": sigma, "T2s": T2s, "W_in_min": W_in_min, "W_in_actual": W_in_actual}


def p6_53():
    """10 lb air in a rigid tank, 1 atm/600 R, heated by a reservoir at 900 R until 800 R;
    boundary where heat crosses is at 900 R.  cv=0.171 Btu/lb.R.  Find Q (Btu) and
    sigma (Btu/R). (p.351)"""
    m, T1, T2, Tb, cv = 10.0, 600.0, 800.0, 900.0, 0.171
    Q = m * cv * (T2 - T1)                            # rigid: Q = dU
    dS = m * cv * math.log(T2 / T1)                  # rigid: dS = m cv ln(T2/T1)
    sigma = dS - Q / Tb                               # entropy balance
    return {"Q": Q, "dS": dS, "sigma": sigma}


def _demo():
    print("Module 6.HP -- Topic 6 homework (Moran Ch.4 & 6; worked solutions, no book key)\n")
    r = p4_34(); print("  4.34 A1=%.3f m2, Q=%.1f kW            [nozzle; heat out]" % (r["A1"], r["Q"]))
    r = p4_42(); print("  4.42 W=%.0f kW                        [insulated turbine]" % r["W"])
    r = p6_17(); print("  6.17 V2=%.3f m3                       [argon, ds=-0.27]" % r["V2"])
    r = p6_24(); print("  6.24 Q=%.0f kJ, W=%.0f kJ             [isothermal int. rev.]" % (r["Q"], r["W"]))
    r = p6_37(); print("  6.37 m=%.2f kg, T2=%.0f K, sigma=%.2f kJ/K" % (r["m"], r["T2"], r["sigma"]))
    r = p6_40(); print("  6.40 p2=%.1f bar, W=%.0f kJ, sigma=%.3f kJ/K" % (r["p2"], r["W"], r["sigma"]))
    r = p6_43(); print("  6.43 sigma/m=%.4f kJ/kg.K, min work=%.1f kJ/kg (actual %.1f)"
                       % (r["sigma"], r["W_in_min"], r["W_in_actual"]))
    r = p6_53(); print("  6.53 Q=%.0f Btu, sigma=%.3f Btu/R     [heat across finite dT]"
                       % (r["Q"], r["sigma"]))


if __name__ == "__main__":
    _demo()
