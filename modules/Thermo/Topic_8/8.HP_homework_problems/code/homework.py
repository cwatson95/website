"""
homework.py  —  Module 8.HP (Topic 8: homework problems, Moran Ch.4/6/10 devices)

8 problems spanning the four Topic-8 devices (compressor, condenser, heat exchanger,
heat pump), one per function, each SOLVED from complete given data.  Moran provides
no worked key, so these are *worked solutions*: test_homework.py checks each answer
AND the physical consistency conditions (energy balances close, isentropic work is
the minimum, COPs sit below the Carnot ceiling).

Property values are the book-verified ones from the Topic-8 worked Examples (see
../refs.md); P7 uses constant specific heats.  Statements in ../problems.md.

Units: h [kJ/kg] and Qdot/Wdot [kW] unless noted; power_cv-style calls use strict SI
(J/kg, W); Carnot temperatures are ABSOLUTE (K).
"""

R_AIR = 8314.0 / 28.97       # J/kg.K


def p1():
    """Air enters a compressor inlet (A=0.1 m^2) at 1 bar, 290 K, 6 m/s.  Find the
    specific volume and mdot two ways: mdot = AV/v (Eq. 4.4b) and the ideal-gas form
    AVp/(RT).  Both must agree."""
    A, V, p, T = 0.1, 6.0, 1.0e5, 290.0
    v = R_AIR * T / p                          # 0.832 m^3/kg
    mdot_v = A * V / v
    mdot_ig = A * V * p / (R_AIR * T)          # 0.72 kg/s
    return {"v": v, "mdot_v": mdot_v, "mdot_ig": mdot_ig}


def p2():
    """Compressor power WITH heat loss (Ex 4.5 data): mdot=0.72 kg/s, h1=290.16,
    h2=451.80 kJ/kg (Table A-22), V1=6, V2=2 m/s, Qdot=-3 kW.  Find the power input
    and the size of the KE contribution.  Eq. 4.20a."""
    mdot, h1, h2 = 0.72, 290.16e3, 451.80e3    # strict SI
    Qdot = -3.0e3                              # W (-180 kJ/min)
    dKE = (6.0 ** 2 - 2.0 ** 2) / 2.0          # +16 J/kg
    W = Qdot + mdot * ((h1 - h2) + dKE)        # -119.4 kW
    W_noKE = Qdot + mdot * (h1 - h2)
    return {"W_kW": W / 1e3, "input_kW": -W / 1e3, "KE_kW": mdot * dKE / 1e3,
            "W_noKE_kW": W_noKE / 1e3}


def p3():
    """Adiabatic compressor WITHOUT heat loss + isentropic efficiency (Ex 6.14 data):
    R-22, mdot=0.07 kg/s, h1=249.75, h2=294.17, h2s=285.58 kJ/kg.  Find Wdot_cv,
    eta_c, and the minimum (isentropic) work.  Eqs. 4.20a, 6.48."""
    mdot, h1, h2, h2s = 0.07, 249.75, 294.17, 285.58
    W = mdot * (h1 - h2)                       # -3.11 kW
    w_actual = h2 - h1                         # 44.42 kJ/kg
    w_min = h2s - h1                           # 35.83 kJ/kg
    eta_c = w_min / w_actual                   # 0.81
    return {"W_kW": W, "w_actual": w_actual, "w_min": w_min, "eta_c": eta_c}


def p4():
    """Real exit state from eta_c (Ex 10.3 compressor): h1=241.35, h2s=272.39 kJ/kg,
    eta_c=0.80.  Find h2 and the actual work; verify the efficiency round-trips.
    Eq. 6.48 rearranged."""
    h1, h2s, eta_c = 241.35, 272.39, 0.80
    h2 = h1 + (h2s - h1) / eta_c               # 280.15 kJ/kg
    return {"h2": h2, "w_actual": h2 - h1, "w_ideal": h2s - h1,
            "eta_back": (h2s - h1) / (h2 - h1)}


def p5():
    """Condenser, steam side (Ex 4.7 data): steam in at 0.1 bar, x=0.95 (hf=191.83,
    hg=2584.7), condensate out at 45 C (h_out=hf=188.45 kJ/kg); mdot=125 kg/s.
    Find h_in, the heat transfer per kg of steam, and the total rate (MW)."""
    hf, hg, x = 191.83, 2584.7, 0.95
    h_in = hf + x * (hg - hf)                  # 2465.1 kJ/kg
    h_out = 188.45
    q = h_out - h_in                           # -2276.7 kJ/kg
    Q_MW = 125.0 * q / 1e3                     # -284.6 MW
    return {"h_in": h_in, "hf": hf, "hg": hg, "q": q, "Q_MW": Q_MW}


def p6():
    """Heat-exchanger mass-flow ratio (Ex 4.7 two-stream view): hot stream 2465.1 ->
    188.45 kJ/kg; cold stream rises 62.7 kJ/kg.  Find mdot_c/mdot_h and the cooling-
    water flow when mdot_h=125 kg/s; verify the whole-device balance closes."""
    h_hi, h_ho, dh_c = 2465.1, 188.45, 62.7
    ratio = (h_hi - h_ho) / dh_c               # 36.3
    mdot_c = 125.0 * ratio                     # 4539 kg/s
    residual = 125.0 * (h_hi - h_ho) + mdot_c * (0.0 - dh_c)
    return {"ratio": ratio, "mdot_c": mdot_c, "residual": residual}


def p7():
    """Heat-exchanger exit state (constant cp): hot air mdot_h=4 kg/s, cp=1.005
    kJ/kg.K cools 500 -> 300 K; water mdot_c=8 kg/s, c=4.18 kJ/kg.K enters at 20 C
    (adiabatic exchanger, Wcv=0).  Find the duty and the water exit temperature."""
    mdot_h, cp_h = 4.0, 1.005
    mdot_c, c_c, T_ci = 8.0, 4.18, 20.0
    duty = mdot_h * cp_h * (500.0 - 300.0)     # 804 kW given up by the air
    dT_c = duty / (mdot_c * c_c)               # +24.04 K
    T_co = T_ci + dT_c                         # 44.04 C
    residual = duty - mdot_c * c_c * (T_co - T_ci)
    return {"duty_kW": duty, "T_co": T_co, "residual": residual}


def p8():
    """Heat-pump COP + Carnot ceiling (Ex 10.4 cycle): h1=242.54, h2=280.19,
    h3=h4=105.29 kJ/kg, mdot=0.2 kg/s; building 22 C (295 K), outside 5 C (278 K).
    Find gamma, the rates, the same cycle's beta, and the Carnot gamma_max.
    Eqs. 10.4, 10.5, 10.8-10.10."""
    h1, h2, h3 = 242.54, 280.19, 105.29
    mdot, T_H, T_C = 0.2, 295.0, 278.0
    W = mdot * (h2 - h1)                       # 7.53 kW
    Q_out = mdot * (h2 - h3)                   # 34.98 kW
    Q_in = mdot * (h1 - h3)                    # 27.45 kW (h4 = h3)
    gamma = (h2 - h3) / (h2 - h1)              # 4.65
    beta = (h1 - h3) / (h2 - h1)               # 3.65
    gamma_max = T_H / (T_H - T_C)              # 17.35
    return {"W_kW": W, "Q_out_kW": Q_out, "Q_in_kW": Q_in, "gamma": gamma,
            "beta": beta, "gamma_max": gamma_max}


def _demo():
    print("Module 8.HP -- Topic 8 homework (worked solutions, no book key)\n")
    r = p1(); print("  P1 mass flow:        v = %.3f m^3/kg, mdot = %.2f kg/s (both forms)"
                    % (r["v"], r["mdot_ig"]))
    r = p2(); print("  P2 compressor w/ Q:  input = %.1f kW (KE term %.3f kW)"
                    % (r["input_kW"], r["KE_kW"]))
    r = p3(); print("  P3 adiabatic + eta:  Wcv = %.2f kW, eta_c = %.2f (w %.2f vs min %.2f)"
                    % (r["W_kW"], r["eta_c"], r["w_actual"], r["w_min"]))
    r = p4(); print("  P4 exit from eta_c:  h2 = %.2f kJ/kg, w = %.2f kJ/kg"
                    % (r["h2"], r["w_actual"]))
    r = p5(); print("  P5 condenser:        h_in = %.1f, q = %.1f kJ/kg, Q = %.1f MW"
                    % (r["h_in"], r["q"], r["Q_MW"]))
    r = p6(); print("  P6 HX flow ratio:    mc/mh = %.1f -> %.0f kg/s (residual %.1e)"
                    % (r["ratio"], r["mdot_c"], r["residual"]))
    r = p7(); print("  P7 HX exit state:    duty = %.0f kW, T_water,out = %.1f C"
                    % (r["duty_kW"], r["T_co"]))
    r = p8(); print("  P8 heat pump:        gamma = %.2f (beta %.2f), Carnot max = %.2f"
                    % (r["gamma"], r["beta"], r["gamma_max"]))


if __name__ == "__main__":
    _demo()
