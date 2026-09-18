"""
examples.py  —  Module 9.EP (Topic 9: worked Example problems)

Each Moran 8e worked cycle Example from Ch.8-9 reproduced from its GIVEN data using
the canonical Topic-9 equations (imported from module 9.EQ), so the book's published
ANSWER can be regenerated and checked (test_examples.py).  Air properties (u, h, vr,
pr from Table A-22/A-22E) and steam states (Tables A-3/A-4) are embedded exactly as
the book quotes them, and the book's stepwise rounding is replicated.

Full statements (GIVEN / FIND / ANSWER / METHOD) with page citations are in
../examples.md.  Units follow each book example: Ex 9.1 English (degR, atm, Btu);
the rest SI (K, kPa/MPa, kJ/kg).
"""
import os
import sys

# canonical equations from module 9.EQ
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "9.EQ_list_of_equations", "code"))
import equations as eq   # noqa: E402

R_SI = 8314.0 / 28.97    # J/kg.K  (R/M for air)
R_ENG = 1545.0 / 28.97   # ft.lbf/lb.degR


# ------------------------------------------------------------ Ch.9 examples ---
def ex_9_1():
    """Analyzing the Otto Cycle (p.515). r=8, T1=540 degR, p1=1 atm, V1=0.02 ft^3,
    T3=3600 degR.  Table A-22E: u1=92.04, vr1=144.32; T2=1212, u2=211.3;
    u3=721.44, vr3=0.6449; T4=1878, u4=342.2 (Btu/lb)."""
    T1, p1, V1, T3 = 540.0, 1.0, 0.02, 3600.0
    r = 8.0
    vr2 = 144.32 / r                            # 18.04 -> T2 = 1212 degR (A-22E)
    T2, u1, u2 = 1212.0, 92.04, 211.3
    p2 = p1 * (T2 / T1) * r                     # 17.96 atm
    p3 = p2 * (T3 / T2)                         # 53.3 atm
    vr4 = 0.6449 * r                            # 5.16 -> T4 = 1878 degR
    T4, u3, u4 = 1878.0, 721.44, 342.2
    p4 = p1 * (T4 / T1)                         # 3.48 atm
    eta = eq.otto_efficiency_air_table(u1, u2, u3, u4)          # 0.51
    m = (14.696 * 144.0 * V1) / (R_ENG * T1)    # 1.47e-3 lb
    W = m * ((u3 - u4) - (u2 - u1))             # 0.382 Btu
    mep_psi = eq.mean_effective_pressure(W, V1, V1 / r) * 778.0 / 144.0   # 118 lbf/in^2
    return {
        "vr2": vr2, "T2": T2, "p2_atm": p2, "p3_atm": p3, "vr4": vr4, "T4": T4,
        "p4_atm": p4, "eta": eta, "m_lb": m, "W_Btu": W, "mep_atm": mep_psi / 14.696,
        "Q23_Btu": m * (u3 - u2), "Q41_Btu": m * (u4 - u1),     # quiz: 0.750, 0.368
        # cold air-standard comparison column (k=1.4)
        "T2_cold": eq.otto_temp_after_compression(T1, r),       # 1241 degR
        "T4_cold": eq.otto_temp_after_expansion(T3, r),         # 1567 degR
        "eta_cold": eq.otto_efficiency(r),                      # 0.565
    }


def ex_9_2():
    """Analyzing the Diesel Cycle (p.520). r=18, rc=2, T1=300 K, p1=0.1 MPa.
    Table A-22: u1=214.07, vr1=621.2; T2=898.3, h2=930.98; h3=1999.1, vr3=3.97;
    T4=887.7, u4=664.3 (kJ/kg)."""
    T1, p1, r, rc = 300.0, 0.1, 18.0, 2.0
    vr2 = 621.2 / r                             # 34.51 -> T2 = 898.3 K (A-22)
    T2, u1, h2 = 898.3, 214.07, 930.98
    p2 = p1 * (T2 / T1) * r                     # 5.39 MPa
    T3 = rc * T2                                # 1796.6 K
    h3, vr3 = 1999.1, 3.97
    vr4 = (r / rc) * vr3                        # 35.73 -> T4 = 887.7, u4 = 664.3
    T4, u4 = 887.7, 664.3
    p4 = p1 * (T4 / T1)                         # 0.3 MPa
    eta = eq.diesel_efficiency_air_table(u1, u4, h2, h3)        # 0.578
    w = (h3 - h2) - (u4 - u1)                   # 617.9 kJ/kg (net = qin - qout)
    v1 = R_SI * T1 / (p1 * 1e6)                 # 0.861 m^3/kg
    mep = eq.mean_effective_pressure(w, v1, v1 / r)             # kPa -> 0.76 MPa
    return {"T2": T2, "p2_MPa": p2, "T3": T3, "T4": T4, "p4_MPa": p4, "eta": eta,
            "w_kJkg": w, "v1": v1, "mep_MPa": mep / 1e3,
            "displacement_L": 0.0123 * v1 * (1.0 - 1.0 / r) * 1e3,   # quiz: 10 L
            "eta_cold": eq.diesel_efficiency(r, rc)}                 # 0.632 (note 1)


def ex_9_3():
    """Analyzing the Dual Cycle (p.523). r=18, rp=1.5, rc=1.2, T1=300 K, p1=0.1 MPa.
    States 1-2 from Ex 9.2 (u1=214.07, T2=898.3, u2=673.2); Table A-22: h3=1452.6,
    u3=1065.8; h4=1778.3, vr4=5.609; u5=475.96 (kJ/kg)."""
    r, rp, rc = 18.0, 1.5, 1.2
    T2, u1, u2 = 898.3, 214.07, 673.2
    T3 = rp * T2                                # 1347.5 K
    h3, u3 = 1452.6, 1065.8
    T4 = rc * 1347.5                            # 1617 K (book's rounded T3)
    h4, vr4 = 1778.3, 5.609
    vr5 = vr4 * (r / rc)                        # 5.609*15 = 84.135 -> u5 = 475.96
    u5 = 475.96
    eta = eq.dual_efficiency_air_table(u1, u2, u3, h3, h4, u5)  # 0.635
    q_in = (u3 - u2) + (h4 - h3)                # 718.3 kJ/kg
    w = q_in - (u5 - u1)                        # 456 kJ/kg
    mep = eq.mean_effective_pressure(w, 0.861, 0.861 / r)       # kPa -> 0.56 MPa
    return {"T3": T3, "T4": T4, "vr5": vr5, "eta": eta, "Qin_kJkg": q_in,
            "w_kJkg": w, "mep_MPa": mep / 1e3,
            "eta_cold": eq.dual_efficiency(r, rp, rc)}          # 0.680 (overpredicts)


def ex_9_4():
    """Analyzing the Ideal Brayton Cycle (p.529). 100 kPa, 300 K, (AV)=5 m^3/s,
    rp=10, T3=1400 K.  Table A-22: h1=300.19, pr1=1.386; h2=579.9; h3=1515.4,
    pr3=450.5; h4=808.5 (kJ/kg)."""
    T1, p1, AV, rp, T3 = 300.0, 100.0e3, 5.0, 10.0, 1400.0
    h1, pr1 = 300.19, 1.386
    pr2 = pr1 * rp                              # 13.86 -> h2 = 579.9 (A-22)
    h2 = 579.9
    h3, pr3 = 1515.4, 450.5
    pr4 = pr3 / rp                              # 45.05 -> h4 = 808.5
    h4 = 808.5
    eta = eq.brayton_efficiency_air_table(h1, h2, h3, h4)       # 0.457
    bwr = eq.brayton_back_work_ratio(h1, h2, h3, h4)            # 0.396
    mdot = AV * p1 / (R_SI * T1)                # 5.807 kg/s
    W = mdot * (eq.brayton_turbine_work(h3, h4) - eq.brayton_compressor_work(h1, h2))
    T2c = eq.brayton_temp_after_compression(T1, rp)             # 579.2 K
    T4c = eq.brayton_temp_after_expansion(T3, rp)               # 725.1 K
    return {"pr2": pr2, "pr4": pr4, "eta": eta, "bwr": bwr, "mdot": mdot,
            "W_kW": W, "Qin_kW": mdot * eq.brayton_heat_added(h2, h3),  # quiz: 5432
            # cold air-standard comparison column (k=1.4, cp=1.005)
            "T2_cold": T2c, "T4_cold": T4c,
            "eta_cold": eq.brayton_efficiency(rp),                      # 0.482
            "bwr_cold": (T2c - T1) / (T3 - T4c),                        # 0.414
            "W_cold_kW": mdot * 1.005 * ((T3 - T4c) - (T2c - T1))}      # 2308


def ex_9_5():
    """Determining Compressor Pressure Ratio for Maximum Net Work (p.533).
    Cold air-standard; fixed T1 and T3.  Result: rp = (T3/T1)^(k/(2(k-1))) (Eq. (a));
    quiz evaluates it for T1=300 K, T3=1700 K, k=1.4 -> ~21 (Fig. 9.12)."""
    k = 1.4
    rp_star = (1700.0 / 300.0) ** (k / (2.0 * (k - 1.0)))       # 20.8 -> ~21
    return {"rp_star": rp_star}


def ex_9_6():
    """Evaluating Performance of a Brayton Cycle with Irreversibilities (p.535).
    Ex 9.4 cycle with eta_t = eta_c = 80%; isentropic works from Ex 9.4."""
    h1, h3 = 300.19, 1515.4
    wt = 0.8 * 706.9                            # 565.5 kJ/kg  (Wt = eta_t (Wt)_s)
    wc = 279.7 / 0.8                            # 349.6 kJ/kg  (Wc = (Wc)_s/eta_c)
    h2 = h1 + wc                                # 649.8 kJ/kg
    q_in = h3 - h2                              # 865.6 kJ/kg
    eta = (wt - wc) / q_in                      # 0.249
    bwr = wc / wt                               # 0.618
    W = 5.807 * (wt - wc)                       # 1254 kW (mdot from Ex 9.4)
    wt70 = 0.7 * 706.9                          # quiz: eta_t = 70%
    return {"wt": wt, "wc": wc, "h2": h2, "qin": q_in, "eta": eta, "bwr": bwr,
            "W_kW": W, "eta_70": (wt70 - wc) / q_in, "bwr_70": wc / wt70}


def ex_9_7():
    """Evaluating Thermal Efficiency of a Brayton Cycle with Regeneration (p.539).
    Regenerator (eta_reg = 80%) on the Ex 9.4 cycle; h's from Ex 9.4."""
    h1, h2, h3, h4 = 300.19, 579.9, 1515.4, 808.5
    hx = 0.8 * (h4 - h2) + h2                   # 762.8 kJ/kg (Eq. 9.27 solved for hx)
    eta = ((h3 - h4) - (h2 - h1)) / (h3 - hx)   # 0.568
    eta100 = ((h3 - h4) - (h2 - h1)) / (h3 - h4)   # quiz: eta_reg = 100% -> hx = h4
    return {"hx": hx, "eta_reg_check": eq.regenerator_effectiveness(hx, h2, h4),
            "eta": eta, "eta_100": eta100}


# ------------------------------------------------------------ Ch.8 examples ---
def ex_8_1():
    """Analyzing an Ideal Rankine Cycle (p.450). Sat vapor 8.0 MPa -> condenser
    0.008 MPa, Wcycle=100 MW, cooling water 15->35 C.  Table A-3: h1=2758.0,
    s1=5.7432; at 0.008 MPa sf=0.5926, sg=8.2287, hf=173.88, hfg=2403.1,
    vf=1.0084e-3; Table A-2: hf(35 C)=146.68, hf(15 C)=62.99."""
    h1, s1 = 2758.0, 5.7432
    x2 = (s1 - 0.5926) / (8.2287 - 0.5926)      # 0.6745
    h2 = 173.88 + x2 * 2403.1                   # 1794.8 kJ/kg
    h3 = 173.88
    wp = eq.rankine_pump_work_approx(1.0084e-3, 8.0, 8000.0)    # 8.06 kJ/kg
    h4 = h3 + wp                                # 181.94 kJ/kg
    eta = eq.rankine_efficiency(h1, h2, h3, h4)                 # 0.371
    bwr = eq.rankine_back_work_ratio(h1, h2, h3, h4)            # 8.37e-3
    mdot = 100e3 * 3600.0 / ((h1 - h2) - (h4 - h3))             # 3.77e5 kg/h
    # book carries its rounded mdot = 3.77e5 kg/h into (d)-(f):
    Qin = 3.77e5 * eq.rankine_boiler_heat(h4, h1) / 3600.0 / 1e3      # 269.77 MW
    Qout = 3.77e5 * eq.rankine_condenser_heat(h2, h3) / 3600.0 / 1e3  # 169.75 MW
    mcw = 169.75e3 * 3600.0 / (146.68 - 62.99)                  # 7.3e6 kg/h
    return {"x2": x2, "h2": h2, "wp": wp, "h4": h4, "eta": eta, "bwr": bwr,
            "mdot_kgh": mdot, "Qin_MW": Qin, "Qout_MW": Qout, "mcw_kgh": mcw,
            "W_150kgs_MW": 150.0 * ((h1 - h2) - (h4 - h3)) / 1e3}   # quiz: 143.2


def ex_8_2():
    """Analyzing a Rankine Cycle with Irreversibilities (p.456). Ex 8.1 cycle with
    eta_t = eta_p = 85%; h2s = 1794.8 from Ex 8.1."""
    h1, h2s, h3 = 2758.0, 1794.8, 173.88
    h2 = h1 - 0.85 * (h1 - h2s)                 # 1939.3 kJ/kg (Eq. 8.9)
    wp = 8.06 / 0.85                            # 9.48 kJ/kg (Eq. 8.10b)
    h4 = h3 + wp                                # 183.36 kJ/kg
    eta = eq.rankine_efficiency(h1, h2, h3, h4)                 # 0.314
    mdot = 100e3 * 3600.0 / ((h1 - h2) - (h4 - h3))             # 4.449e5 kg/h
    Qin = 4.449e5 * eq.rankine_boiler_heat(h4, h1) / 3600.0 / 1e3     # 318.2 MW
    Qout = 4.449e5 * eq.rankine_condenser_heat(h2, h3) / 3600.0 / 1e3 # 218.2 MW
    mcw = 218.2e3 * 3600.0 / (146.68 - 62.99)                   # 9.39e6 kg/h
    return {"h2": h2, "wp": wp, "h4": h4, "eta": eta, "mdot_kgh": mdot,
            "Qin_MW": Qin, "Qout_MW": Qout, "mcw_kgh": mcw,
            "Wp_150kgs_kW": 150.0 * wp,                         # quiz: 1422 kW
            "bwr": eq.rankine_back_work_ratio(h1, h2, h3, h4)}  # quiz: 0.0116


def ex_8_3():
    """Evaluating Performance of an Ideal Reheat Cycle (p.461). 8.0 MPa, 480 C ->
    0.7 MPa; reheat to 440 C; condenser 0.008 MPa; 100 MW.  Table A-4: h1=3348.4,
    s1=6.6586; h3=3353.3, s3=7.7571.  Table A-3 @ 0.7 MPa: sf=1.9922, sg=6.708,
    hf=697.22, hfg=2066.3; @ 0.008 MPa as Ex 8.1; h6=181.94 from Ex 8.1."""
    h1, s1 = 3348.4, 6.6586
    x2 = (s1 - 1.9922) / (6.708 - 1.9922)       # 0.9895
    h2 = 697.22 + x2 * 2066.3                   # 2741.8 kJ/kg
    h3, s3 = 3353.3, 7.7571
    x4 = (s3 - 0.5926) / (8.2287 - 0.5926)      # 0.9382
    h4 = 173.88 + x4 * 2403.1                   # 2428.5 kJ/kg
    h5, h6 = 173.88, 181.94
    w_net = (h1 - h2) + (h3 - h4) - (h6 - h5)   # 1523.3 kJ/kg
    q_in = (h1 - h6) + (h3 - h2)                # 3778 kJ/kg
    eta = w_net / q_in                          # 0.403
    mdot = 100e3 * 3600.0 / w_net               # 2.363e5 kg/h
    Qout = 2.363e5 * (h4 - h5) / 3600.0 / 1e3   # 148 MW (book's rounded mdot)
    Qreheat = 2.363e5 * (h3 - h2) / 3600.0 / 1e3   # quiz: 40.1 MW
    return {"x2": x2, "h2": h2, "x4": x4, "h4": h4, "eta": eta, "mdot_kgh": mdot,
            "Qout_MW": Qout, "Qreheat_MW": Qreheat,
            "reheat_frac": (h3 - h2) / q_in}    # quiz: 16.2%


def ex_8_4():
    """Evaluating Performance of a Reheat Cycle with Turbine Irreversibility (p.463).
    Ex 8.3 cycle with eta_t = 85% per stage; h2s=2741.8, h4s=2428.5 from Ex 8.3."""
    h1, h2s, h3, h4s, h5, h6 = 3348.4, 2741.8, 3353.3, 2428.5, 173.88, 181.94
    h2 = h1 - 0.85 * (h1 - h2s)                 # 2832.8 kJ/kg
    h4 = h3 - 0.85 * (h3 - h4s)                 # 2567.2 kJ/kg
    eta = ((h1 - h2) + (h3 - h4) - (h6 - h5)) / ((h1 - h6) + (h3 - h2))   # 0.351
    return {"h2": h2, "h4": h4, "eta": eta}


def _demo():
    print("Module 9.EP — Topic 9 worked examples regenerated from GIVEN data\n")
    r = ex_9_1()
    print(f"  Ex 9.1 Otto:    eta = {r['eta']:.2f}, T2/T4 = {r['T2']:.0f}/{r['T4']:.0f} degR, "
          f"mep = {r['mep_atm']:.2f} atm   [book 0.51, 1212/1878, 8.03]")
    r = ex_9_2()
    print(f"  Ex 9.2 Diesel:  eta = {r['eta']:.3f}, T2 = {r['T2']:.1f} K, "
          f"mep = {r['mep_MPa']:.2f} MPa   [book 0.578, 898.3, 0.76]")
    r = ex_9_3()
    print(f"  Ex 9.3 dual:    eta = {r['eta']:.3f}, w = {r['w_kJkg']:.0f} kJ/kg, "
          f"mep = {r['mep_MPa']:.2f} MPa   [book 0.635, 456, 0.56]")
    r = ex_9_4()
    print(f"  Ex 9.4 Brayton: eta = {r['eta']:.3f}, bwr = {r['bwr']:.3f}, "
          f"W = {r['W_kW']:.0f} kW   [book 0.457, 0.396, 2481]")
    r = ex_9_5()
    print(f"  Ex 9.5 rp* :    (1700/300)^1.75 = {r['rp_star']:.1f}   [book ~21]")
    r = ex_9_6()
    print(f"  Ex 9.6 Brayton+irr: eta = {r['eta']:.3f}, bwr = {r['bwr']:.3f}, "
          f"W = {r['W_kW']:.0f} kW   [book 0.249, 0.618, 1254]")
    r = ex_9_7()
    print(f"  Ex 9.7 Brayton+regen: hx = {r['hx']:.1f}, eta = {r['eta']:.3f}   [book 762.8, 0.568]")
    r = ex_8_1()
    print(f"  Ex 8.1 Rankine: eta = {r['eta']:.3f}, bwr = {r['bwr']:.2e}, "
          f"mdot = {r['mdot_kgh']:.3g} kg/h   [book 0.371, 8.37e-3, 3.77e5]")
    r = ex_8_2()
    print(f"  Ex 8.2 Rankine+irr: eta = {r['eta']:.3f}, Qin = {r['Qin_MW']:.1f} MW   [book 0.314, 318.2]")
    r = ex_8_3()
    print(f"  Ex 8.3 reheat:  eta = {r['eta']:.3f}, x4 = {r['x4']:.4f}, "
          f"Qout = {r['Qout_MW']:.0f} MW   [book 0.403, 0.9382, 148]")
    r = ex_8_4()
    print(f"  Ex 8.4 reheat+irr: eta = {r['eta']:.3f}   [book 0.351]")


if __name__ == "__main__":
    _demo()
