"""
examples.py  —  Module 8.EP (Topic 8: worked Example problems)

Each Moran 8e worked Example for the Topic-8 devices (compressor, condenser, heat
exchanger, heat pump / vapor-compression cycle) reproduced from its GIVEN data using
the canonical Topic-8 equations (imported from module 8.EQ), so the book's published
ANSWER can be regenerated and checked (`test_examples.py`).

Full statements (GIVEN / FIND / ANSWER / METHOD) with page citations are in
`../examples.md`.  Table values quoted by the book (A-2/A-3, A-9, A-10/A-11/A-12,
A-22) are embedded as the book quotes them, and the book's stepwise rounding is
replicated (e.g. Ex 4.5 rounds mdot to 0.72 kg/s before the power step).

Units follow each book example: strict SI (J/kg, W) inside power_cv; kJ/kg elsewhere;
refrigeration capacity uses 1 ton = 211 kJ/min.
"""
import os
import sys

# canonical equations from module 8.EQ
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "8.EQ_list_of_equations", "code"))
import equations as eq   # noqa: E402

R_AIR = 8314.0 / 28.97          # air, J/kg.K  (R-bar/M, as the book evaluates it)
TON_KJ_MIN = 211.0              # 1 ton of refrigeration = 211 kJ/min


# ------------------------------------------------------------- Ch.4 devices ---
def ex_4_5():
    """Calculating Compressor Power (p.190-191).  Air: 1 bar, 290 K, 6 m/s, A1=0.1 m^2
    -> 7 bar, 450 K, 2 m/s; Qdot_cv = -180 kJ/min; h from Table A-22."""
    mdot_raw = eq.mass_flow_rate_ideal_gas(0.1, 6.0, 1.0e5, R_AIR, 290.0)
    mdot = 0.72                                     # book rounds before the power step
    h1, h2 = 290.16e3, 451.80e3                     # J/kg (Table A-22 at 290/450 K)
    W = eq.power_cv(mdot, h1, h2, Qdot=-180.0e3 / 60.0, V1=6.0, V2=2.0, g=0.0)
    W_noKE = eq.power_cv(mdot, h1, h2, Qdot=-180.0e3 / 60.0, g=0.0)   # Quick Quiz
    return {"mdot": mdot_raw, "W_kW": W / 1e3, "W_noKE_kW": W_noKE / 1e3,
            "power_input_kW": -W / 1e3}


def ex_4_7():
    """Evaluating Performance of a Power Plant Condenser (p.197-198).  Steam 0.1 bar,
    x=0.95 -> condensate 45 C; cooling water 20 -> 35 C; hf/hg from Tables A-3/A-2."""
    h1 = 191.83 + 0.95 * (2584.7 - 191.83)          # 2465.1 kJ/kg (Table A-3, 0.1 bar)
    h2 = 188.45                                     # hf(45 C), Table A-2
    dh_cold = 62.7                                  # h4 - h3 = hf(35 C) - hf(20 C)
    ratio = eq.mass_flow_ratio_cold_to_hot(h1, h2, 0.0, dh_cold)      # 36.3
    q_per_kg = eq.single_stream_heat_rate(1.0, h1, h2)                # -2276.7 kJ/kg
    mdot_w = 125.0 * ratio                          # Quick Quiz: 4538 kg/s
    resid = eq.two_stream_balance_residual(1.0, h1, h2, ratio, 0.0, dh_cold)
    return {"h1": h1, "ratio": ratio, "q_per_kg": q_per_kg, "mdot_w": mdot_w,
            "residual": resid}


def ex_4_8():
    """Cooling Computer Components (p.198-199).  Air 20 C, 1 atm, V1 <= 1.3 m/s,
    T2 <= 32 C; electronics 80 W + fan 18 W; find the smallest inlet area (cm^2)."""
    Wdot = -(80.0 + 18.0)                           # W (electric power IN)
    cp = 1005.0                                     # J/kg.K (book: 1.005 kJ/kg.K)
    T1, T2 = 293.0, 305.0                           # K (20 C in, 32 C limit)
    mdot = -Wdot / (cp * (T2 - T1))                 # from 0 = -Wdot + mdot(h1-h2)
    v1 = R_AIR * T1 / 1.01325e5                     # ideal gas, 1 atm
    A1 = mdot * v1 / 1.3                            # m^2 (Eq. 4.4b rearranged)
    # closure: Eq. 4.4b returns the same mdot from this area
    mdot_back = eq.mass_flow_rate(A1, 1.3, v1)
    return {"mdot": mdot, "A1_cm2": A1 * 1.0e4, "mdot_back": mdot_back}


# ------------------------------------------------- Ch.6 compressor efficiency ---
def ex_6_14():
    """Evaluating Isentropic Compressor Efficiency (p.338-339).  R-22, mdot=0.07 kg/s;
    h1=249.75 (-5 C, 3.5 bar), h2=294.17 (75 C, 14 bar), h2s=285.58 kJ/kg (Table A-9)."""
    h1, h2, h2s = 249.75, 294.17, 285.58
    W = eq.compressor_power(0.07, h1, h2)                             # -3.11 kW
    eta_c = eq.isentropic_compressor_efficiency(h1, h2, h2s)          # 0.81
    w_min = eq.vc_compressor_work_per_mass(h1, h2s)                   # Quick Quiz: 35.83
    return {"W_kW": W, "eta_c": eta_c, "w_min": w_min}


# --------------------------------------------- Ch.10 vapor-compression cycles ---
def ex_10_1():
    """Analyzing an Ideal Vapor-Compression Refrigeration Cycle (p.614-615).  R-134a,
    cold 0 C / warm 26 C; h1=247.23 (sat vap 0 C), h2s=264.7, h3=85.75 (sat liq 26 C);
    mdot=0.08 kg/s."""
    h1, h2s, h3 = 247.23, 264.7, 85.75              # kJ/kg (Tables A-10/A-12)
    h4 = eq.throttling_exit_enthalpy(h3)
    Wc = 0.08 * eq.vc_compressor_work_per_mass(h1, h2s)               # 1.4 kW
    cap_ton = 0.08 * eq.refrigeration_capacity_per_mass(h1, h4) * 60.0 / TON_KJ_MIN
    beta = eq.cop_refrigeration_vc(h1, h2s, h4)                       # 9.24
    beta_max = eq.carnot_cop_refrigeration(299.0, 273.0)              # 10.5
    mdot_10ton = 10.0 * TON_KJ_MIN / 60.0 / eq.refrigeration_capacity_per_mass(h1, h4)
    return {"Wc_kW": Wc, "cap_ton": cap_ton, "beta": beta, "beta_max": beta_max,
            "mdot_10ton": mdot_10ton}                                 # QQ: 0.218 kg/s


def ex_10_2():
    """Considering the Effect of Irreversible Heat Transfer on Performance (p.616-617).
    Ex 10.1 modified: sat vapor at -10 C into the compressor (h1=241.35), condenser at
    9 bar (h2s=272.39, h3=99.56); mdot=0.08 kg/s."""
    h1, h2s, h3 = 241.35, 272.39, 99.56             # kJ/kg (Tables A-10/A-12/A-11)
    h4 = eq.throttling_exit_enthalpy(h3)
    Wc = 0.08 * eq.vc_compressor_work_per_mass(h1, h2s)               # 2.48 kW
    cap_ton = 0.08 * eq.refrigeration_capacity_per_mass(h1, h4) * 60.0 / TON_KJ_MIN
    beta = eq.cop_refrigeration_vc(h1, h2s, h4)                       # 4.57
    Qout = 0.08 * eq.vc_condenser_heat_per_mass(h2s, h3)              # QQ: 13.83 kW
    return {"Wc_kW": Wc, "cap_ton": cap_ton, "beta": beta, "Qout_kW": Qout}


def ex_10_3():
    """Analyzing an Actual Vapor-Compression Refrigeration Cycle (p.618-619).
    Ex 10.2 with eta_c = 80% and liquid at 30 C leaving the condenser (h3=91.49);
    exergy destruction rates for T0 = 299 K from the book's entropy data."""
    h1, h2s, eta_c = 241.35, 272.39, 0.80
    h2 = h1 + (h2s - h1) / eta_c                    # 280.15 kJ/kg (Eq. 6.48 inverted)
    h3 = 91.49                                      # hf(30 C), Table A-11 via Eq. 3.14
    h4 = eq.throttling_exit_enthalpy(h3)
    Wc = 0.08 * eq.vc_compressor_work_per_mass(h1, h2)                # 3.1 kW
    cap_ton = 0.08 * eq.refrigeration_capacity_per_mass(h1, h4) * 60.0 / TON_KJ_MIN
    beta = eq.cop_refrigeration_vc(h1, h2, h4)                        # 3.86
    # exergy destruction Ed = mdot T0 (s_out - s_in); book's s values (kJ/kg.K):
    s1, s2, s3, s4 = 0.9253, 0.9497, 0.3396, 0.3557
    Ed_c = 0.08 * 299.0 * (s2 - s1)                                   # 0.58 kW
    Ed_valve = 0.08 * 299.0 * (s4 - s3)                               # 0.39 kW
    x4 = (h4 - 36.97) / 204.39                      # quality at 4 (book: 0.2667)
    return {"h2": h2, "Wc_kW": Wc, "cap_ton": cap_ton, "beta": beta,
            "Ed_c_kW": Ed_c, "Ed_valve_kW": Ed_valve, "x4": x4}


def ex_10_4():
    """Analyzing an Actual Vapor-Compression Heat Pump Cycle (p.630-632).  R-134a,
    building 22 C / outside 5 C; h1=242.54 (sat vap -8 C), h2=280.19 (50 C, 10 bar),
    h2s=274.18, h3=105.29 (sat liq 10 bar); mdot=0.2 kg/s; electricity 15 cents/kWh."""
    h1, h2, h2s, h3 = 242.54, 280.19, 274.18, 105.29
    h4 = eq.throttling_exit_enthalpy(h3)
    Wc = 0.2 * eq.vc_compressor_work_per_mass(h1, h2)                 # 7.53 kW
    eta_c = eq.isentropic_compressor_efficiency(h1, h2, h2s)          # 0.84
    Qout = 0.2 * eq.vc_condenser_heat_per_mass(h2, h3)                # 34.98 kW
    gamma = eq.cop_heat_pump_vc(h1, h2, h3)                           # 4.65
    cost = Wc * 80.0 * 0.15                                           # $90.36
    cost_qq = Wc * 80.0 * 0.10                                        # QQ: $60.24
    # first-law closure: Qout = Qin + Wc
    Qin = 0.2 * eq.refrigeration_capacity_per_mass(h1, h4)
    return {"Wc_kW": Wc, "eta_c": eta_c, "Qout_kW": Qout, "gamma": gamma,
            "cost_usd": cost, "cost_qq_usd": cost_qq, "Qin_kW": Qin,
            "first_law": eq.heat_pump_first_law(Qin, Wc)}


def _demo():
    print("Module 8.EP — Topic 8 worked examples regenerated from GIVEN data\n")
    r = ex_4_5()
    print(f"  Ex 4.5   mdot = {r['mdot']:.2f} kg/s, Wcv = {r['W_kW']:.1f} kW"
          f"          [book 0.72, -119.4]")
    r = ex_4_7()
    print(f"  Ex 4.7   ratio = {r['ratio']:.1f}, q = {r['q_per_kg']:.1f} kJ/kg,"
          f" mw = {r['mdot_w']:.0f} kg/s  [book 36.3, -2276.7, 4538]")
    r = ex_4_8()
    print(f"  Ex 4.8   mdot = {r['mdot']*1e3:.2f} g/s, A1 = {r['A1_cm2']:.0f} cm^2"
          f"            [book 52 cm^2]")
    r = ex_6_14()
    print(f"  Ex 6.14  Wcv = {r['W_kW']:.2f} kW, eta_c = {r['eta_c']:.2f},"
          f" w_min = {r['w_min']:.2f} kJ/kg  [book -3.11, 0.81, 35.83]")
    r = ex_10_1()
    print(f"  Ex 10.1  Wc = {r['Wc_kW']:.1f} kW, {r['cap_ton']:.2f} ton,"
          f" beta = {r['beta']:.2f} (max {r['beta_max']:.1f})  [book 1.4, 3.67, 9.24, 10.5]")
    r = ex_10_2()
    print(f"  Ex 10.2  Wc = {r['Wc_kW']:.2f} kW, {r['cap_ton']:.2f} ton,"
          f" beta = {r['beta']:.2f}          [book 2.48, 3.23, 4.57]")
    r = ex_10_3()
    print(f"  Ex 10.3  h2 = {r['h2']:.2f}, Wc = {r['Wc_kW']:.1f} kW, {r['cap_ton']:.2f} ton,"
          f" beta = {r['beta']:.2f}  [book 280.15, 3.1, 3.41, 3.86]")
    print(f"           Ed(comp) = {r['Ed_c_kW']:.2f}, Ed(valve) = {r['Ed_valve_kW']:.2f} kW"
          f"        [book 0.58, 0.39]")
    r = ex_10_4()
    print(f"  Ex 10.4  Wc = {r['Wc_kW']:.2f} kW, eta_c = {r['eta_c']:.2f},"
          f" Qout = {r['Qout_kW']:.2f} kW, gamma = {r['gamma']:.2f}")
    print(f"           cost = ${r['cost_usd']:.2f}                        "
          f"[book 7.53, 0.84, 34.98, 4.65, $90.36]")


if __name__ == "__main__":
    _demo()
