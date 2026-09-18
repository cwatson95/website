"""
homework.py  —  Module 1.HP (Topic 1: end-of-chapter homework problems)

Selected quantitative "Problems: Developing Engineering Skills" from Moran 8e
Ch.1-2 (printed pp.29-34, 81-90), each SOLVED here from its given data using the
Topic-1 equations.  Moran provides no answer key, so these are *worked solutions*
— the value of the module is that every solution is encoded and reproducible
(`test_homework.py`), and many carry an independent consistency check.

Statements with given/find are in `../problems.md`; citations in `../refs.md`.
Canonical equations are imported from module 1.EQ; English-unit problems use
gc = 32.174 lb*ft/(lbf*s^2).
"""
import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "1.EQ_list_of_equations", "code"))
import equations as eq   # noqa: E402

GC = 32.174           # lb*ft/(lbf*s^2)
NA = 6.02214e23       # Avogadro number, 1/mol
ATM_PSI = 14.696      # 1 atm in lbf/in^2
FT_LBF_PER_BTU = 778.17


def F_to_C(F):   return (F - 32.0) / 1.8
def F_to_R(F):   return F + 459.67


# ============================ Chapter 1 ====================================
def p1_8():   # weight on Mars vs Earth
    m = 350.0
    return {"W_mars_N": m * 3.73, "W_earth_N": m * 9.81}

def p1_13():  # local g from weight; weight/mass after drifting
    m, W = 120.0, 119.0
    g_a = W * GC / m
    return {"g_a_ft_s2": g_a, "W_b_lbf": m * 32.05 / GC, "m_b_lb": m}

def p1_20():  # ammonia: weight and specific volume
    n, V, M = 0.5, 6.0, 17.03          # kmol, m^3, kg/kmol
    m = n * M
    return {"W_N": m * 9.81, "v_molar": V / n, "v_mass": V / m}

def p1_21():  # specific volume & density (English)
    v = (62.6 / 2.0) / 1728.0          # ft^3/lb  (in^3 -> ft^3)
    return {"v_ft3_lb": v, "rho_lb_ft3": 1.0 / v}

def p1_23():  # volume, moles, molecules of water vapor
    m, v, M = 5.0, 0.2160, 18.02       # kg, m^3/kg, g/mol
    n_mol = m * 1000.0 / M
    return {"V_m3": m * v, "n_gmol": n_mol, "molecules": n_mol * NA}

def p1_33():  # manometer: gas pressure
    p = 101e3 + 13590.0 * 9.81 * 1.0
    return {"p_gas_kPa": p / 1000.0}

def p1_35():  # barometer column height
    L = 100e3 / (13590.0 * 9.81)
    return {"L_mm": L * 1000.0, "L_in": L * 1000.0 / 25.4}

def p1_36():  # venturi pressure difference
    rho = 1.0 / 0.00122
    return {"dp_kPa": rho * 9.81 * 0.12 / 1000.0}

def p1_38():  # submarine absolute pressure (atm)
    p_water_psi = 62.4 * 1000.0 / 144.0
    return {"p_atm": 1.0 + p_water_psi / ATM_PSI}

def p1_40():  # compressor exit absolute pressure
    return {"p_exit_psia": (5.5 + 14.5) * 8.0}

def p1_42():  # piston & added-weight masses
    A = math.pi * 0.25 ** 2
    return {"m_piston_kg": 1200.0 * A / 9.81, "m_added_kg": (2800.0 - 1200.0) * A / 9.81}

def p1_50():  # Toronto temperatures -> F, R
    return {"summer_F": 19.5 * 1.8 + 32, "summer_R": F_to_R(19.5 * 1.8 + 32),
            "winter_F": -4.9 * 1.8 + 32, "winter_R": F_to_R(-4.9 * 1.8 + 32)}

def p1_51():  # F -> C and K
    out = {}
    for F in (86, -22, 50, -40, 32, -459.67):
        C = F_to_C(F)
        out[f"{F}F"] = (C, eq.celsius_to_kelvin(C))
    return out


# ============================ Chapter 2 ====================================
def p2_5():   # elevation gain of a car
    z = 5183.0 + 2.25e4 * FT_LBF_PER_BTU / 2500.0
    return {"z_high_ft": z}

def p2_6():   # change in kinetic energy
    return {"dKE_kJ": eq.delta_KE(1000.0, 100.0, 20.0)}

def p2_7():   # airliner KE and PE change
    V = 620.0 / 3.6
    return {"dKE_kJ": eq.delta_KE(14000.0, 0.0, V),
            "dPE_kJ": 14000.0 * 9.78 * 10000.0 / 1000.0}

def p2_26():  # pV^2 = const
    V2 = 0.1 * math.sqrt(1.0 / 9.0)
    return {"V2_m3": V2, "W_kJ": eq.polytropic_work(100.0, 0.1, V2, 2.0)}

def p2_28():  # pV^n compression, three n
    V1, V2, p2 = 0.1, 0.04, 200.0
    out = {}
    for n in (0.0, 1.0, 1.3):
        p1 = p2 * (V2 / V1) ** n
        out[f"n{n}"] = {"p1_kPa": p1, "W_kJ": eq.polytropic_work(p1, V1, V2, n)}
    return out

def p2_31():  # polytropic work, English units
    p1, v1, p2, v2, m = 80.0, 4.0, 20.0, 11.0, 14.5
    n = math.log(p1 / p2) / math.log(v2 / v1)
    w_per_m = (p2 * v2 - p1 * v1) / (1.0 - n)            # psi*ft^3/lb
    W = m * w_per_m * 144.0 / FT_LBF_PER_BTU             # -> Btu
    return {"n": n, "W_Btu": W}

def p2_39():  # electric heater
    P = 220.0 * 6.0 / 1000.0
    E = P * 24.0
    return {"P_kW": P, "E_kWh": E, "cost_usd": E * 0.08}

def p2_58():  # closed system, all terms
    dU = 10.0 * (-5.0)
    dKE = eq.delta_KE(10.0, 15.0, 30.0)
    dPE = 10.0 * 9.7 * (-50.0) / 1000.0
    W = 10.0 * 0.147
    return {"Q_kJ": dU + dKE + dPE + W}

def p2_59():  # constant-pressure expansion (gas as system)
    W = 200.0 * (0.12 - 0.10)
    return {"W_gas_kJ": W, "Q_gas_kJ": 0.25 + W}

def p2_62():  # motor: electric/shaft power, surface temp
    P_elec = 110.0 * 10.0 / 1000.0
    P_shaft = 9.7 * (1000.0 * 2 * math.pi / 60.0) / 1000.0
    Wnet = -P_elec + P_shaft                            # kW (out positive)
    Qdot = Wnet                                         # steady state
    Ts = 21.0 - Qdot * 1000.0 / 3.9                     # Qdot = hA(Tf - Ts)
    return {"P_elec_kW": P_elec, "P_shaft_kW": P_shaft, "Ts_C": Ts}

def p2_71():  # piston-cylinder, change in specific internal energy
    p_gas = 100e3 + 25.0 * 9.8 / 0.005
    W = p_gas * (0.001 - 0.0025)                        # J
    dU = -1000.0 - W                                    # Q - W, J
    return {"p_gas_kPa": p_gas / 1000.0, "du_kJ_kg": dU / 0.0025 / 1000.0}

def p2_90():  # refrigerator COP
    Qin = 0.6 - 0.15
    return {"Qdot_in_kW": Qin, "COP": Qin / 0.15}


def _demo():
    print("Module 1.HP — Topic 1 homework, worked solutions (no book answer key)\n")
    print(f"  1.8  W: Mars {p1_8()['W_mars_N']:.0f} N, Earth {p1_8()['W_earth_N']:.0f} N")
    print(f"  1.20 NH3: W {p1_20()['W_N']:.1f} N, v {p1_20()['v_mass']:.4f} m3/kg")
    print(f"  1.33 manometer gas p = {p1_33()['p_gas_kPa']:.1f} kPa")
    print(f"  1.42 piston {p1_42()['m_piston_kg']:.1f} kg, added {p1_42()['m_added_kg']:.1f} kg")
    print(f"  2.6  dKE = {p2_6()['dKE_kJ']:.0f} kJ")
    print(f"  2.26 V2 {p2_26()['V2_m3']:.4f} m3, W {p2_26()['W_kJ']:.1f} kJ")
    print(f"  2.31 n {p2_31()['n']:.4f}, W {p2_31()['W_Btu']:.0f} Btu")
    print(f"  2.58 Q = {p2_58()['Q_kJ']:.1f} kJ")
    print(f"  2.62 P_elec {p2_62()['P_elec_kW']:.2f}, P_shaft {p2_62()['P_shaft_kW']:.3f} kW, Ts {p2_62()['Ts_C']:.1f} C")
    print(f"  2.90 COP = {p2_90()['COP']:.1f}")


if __name__ == "__main__":
    _demo()
