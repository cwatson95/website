"""
homework.py  —  Module 2.HP (Topic 2: end-of-chapter homework, work & energy)

17 quantitative work/energy problems from Moran 8e Ch.2 (printed pp.82-90), none
overlapping Topic_1/1.HP, each SOLVED here from its given data. No answer key
exists, so these are *worked solutions* — reproduced and checked in
test_homework.py, with consistency checks where a balance allows.

Statements in ../problems.md; citations in ../refs.md. English-unit work uses
gc = 32.174 lb*ft/(lbf*s^2) and 1 Btu = 778.17 ft*lbf.
"""
import math

GC = 32.174
BTU = 778.17          # ft*lbf per Btu


def polytropic_work_kJ(p1, V1, V2, n):
    """∫p dV for pVⁿ=const, p in kPa & V in m³ → kJ."""
    if math.isclose(n, 1.0):
        return p1 * V1 * math.log(V2 / V1)
    p2 = p1 * (V1 / V2) ** n
    return (p2 * V2 - p1 * V1) / (1.0 - n)


# ---- kinetic / potential energy -------------------------------------------
def p2_10():   # initial velocity from energy balance (English)
    m, W_on, dz, V2 = 300.0, 140.0, 100.0, 200.0
    dPE = m * dz / BTU                                  # g/gc = 1 -> m*dz/778.17 [Btu]
    dKE = W_on - dPE                                    # ΔKE+ΔPE = work on body
    V1 = math.sqrt(V2 ** 2 - dKE * 2 * GC * BTU / m)
    return {"V1_ft_s": V1}

def p2_14():   # free fall final velocity
    V1, dz, g = 50.0, 600.0, 31.5
    return {"V2_ft_s": math.sqrt(V1 ** 2 + 2 * g * dz)}

def p2_16():   # frictionless ramp
    g, L, ang = 9.81, 10.0, math.radians(40.0)
    return {"V2_m_s": math.sqrt(2 * g * L * math.sin(ang))}

# ---- work from a resultant force ------------------------------------------
def p2_19():   # constant acceleration
    m, a, t = 10.0, 4.0, 20.0
    d = 0.5 * a * t ** 2
    return {"W_kJ": m * a * d / 1000.0}                 # = ΔKE

# ---- power / rate ----------------------------------------------------------
def p2_22():   # rolling resistance power
    w, f, v = 322.5e3, 0.0069, 110.0 / 3.6
    return {"P_kW": f * w * v / 1000.0}

# ---- expansion / compression (∫p dV) work ---------------------------------
def p2_27():   # linear p(V): p = 23.75 - 7.5 V  (psi, ft³) -> Btu
    # W = ∫_{2.5}^{0.5} (23.75 - 7.5 V) dV = [23.75 V - 3.75 V²]
    F = lambda V: 23.75 * V - 3.75 * V ** 2
    W_psi_ft3 = F(0.5) - F(2.5)
    return {"p1_psi": 23.75 - 7.5 * 2.5, "p2_psi": 23.75 - 7.5 * 0.5,
            "W_Btu": W_psi_ft3 * 144.0 / BTU}

def p2_29():   # N2 polytropic n=1.35 (bar, m³) -> kJ  [expansion, see flag]
    p1, V1, V2, n = 20.0 * 100.0, 0.5, 2.75, 1.35       # bar->kPa
    return {"p2_bar": (p1 * (V1 / V2) ** n) / 100.0, "W_kJ": polytropic_work_kJ(p1, V1, V2, n)}

def p2_30():   # p = A/V + B (bar, m³) -> kJ
    A, B = 0.06, 3.0                                    # bar·m³, bar
    V1, V2 = 0.01, 0.03
    p1, p2 = A / V1 + B, A / V2 + B
    W_bar_m3 = A * math.log(V2 / V1) + B * (V2 - V1)
    return {"p1_bar": p1, "p2_bar": p2, "W_kJ": W_bar_m3 * 100.0}

def p2_35():   # three-process cycle (psi, ft³) -> Btu
    p1, V1, p2 = 10.0, 4.0, 50.0
    V2 = p1 * V1 / p2                                   # 1-2 pV=const
    W12 = p1 * V1 * math.log(V2 / V1) * 144.0 / BTU     # Btu
    W23 = 0.0                                           # 2-3 const V
    W31 = p1 * (V1 - V2) * 144.0 / BTU                  # 3-1 const p=10
    return {"V2_ft3": V2, "W12_Btu": W12, "W23_Btu": W23, "W31_Btu": W31}

# ---- spring / shaft / electrical ------------------------------------------
def p2_36():   # belt sander
    Ffric = 0.2 * 15.0                                  # lbf
    v = 1500.0 / 60.0                                   # ft/s
    P = Ffric * v                                       # ft·lbf/s
    return {"P_Btu_s": P / BTU, "P_hp": P / 550.0, "W_1min_Btu": P * 60.0 / BTU}

def p2_37():   # pulley: belt force and shaft speed
    tau, P, r = 200.0, 7000.0, 0.075
    return {"F_kN": tau / r / 1000.0, "rpm": (P / tau) * 60.0 / (2 * math.pi)}

def p2_38():   # battery: resistance and energy
    V, I, t = 10.0, 0.5, 30.0 * 60.0
    return {"R_ohm": V / I, "W_kJ": V * I * t / 1000.0}

def p2_45():   # spring work
    k = 1e4
    x1, x2 = 0.06 - 0.03, 0.10 - 0.03                   # stretch from natural length
    return {"W_J": 0.5 * k * (x2 ** 2 - x1 ** 2)}

# ---- closed-system energy balance -----------------------------------------
def p2_65():   # paddle + rising piston, adiabatic
    p_gas = 14.7 + 100.0 / 40.0                         # psi
    dV_in3 = 40.0 * 12.0                                # in³ (rises 1 ft)
    W_boundary = p_gas * dV_in3 / 12.0 / BTU            # in·lbf->ft·lbf->Btu
    W = W_boundary - 3.0                                # paddle does 3 Btu ON gas
    return {"dU_Btu": 0.0 - W}                          # ΔU = Q - W, Q=0

def p2_66():   # polytropic compression with heat loss
    p1, V1, p2, n, m, Q = 160.0, 1.0, 390.0, 1.2, 0.4, -2.1
    V2 = V1 * (p1 / p2) ** (1.0 / n)
    W = (p2 * V2 - p1 * V1) / (1.0 - n) * 144.0 / BTU   # psi·ft³ -> Btu
    return {"du_Btu_lb": (Q - W) / m}

def p2_70():   # adiabatic polytropic ideal gas, final temperature
    T1, p1, p2, n = 1000.0, 100.0, 50.0, 1.4
    return {"T2_R": T1 * (p2 / p1) ** ((n - 1.0) / n)}

# ---- transient energy-rate balance ----------------------------------------
def p2_64():   # rigid tank, paddle + heat out at rate K·t
    m, u1, u2 = 1.0, 232.92, 276.67
    W = -0.1 * 20.0 * 60.0                              # paddle, kJ (on system)
    dU = m * (u2 - u1)
    Q = dU + W                                          # ΔU = Q - W
    # Q (out) = ∫_0^20 K t dt = K·200 [kW·min] = K·200·60 kJ
    K = -Q / (200.0 * 60.0)
    return {"W_kJ": W, "Q_kJ": Q, "K_kW_min": K}


def _demo():
    print("Module 2.HP — Topic 2 homework (worked solutions, no book key)\n")
    print(f"  2.10 V1 = {p2_10()['V1_ft_s']:.1f} ft/s")
    print(f"  2.16 V2 = {p2_16()['V2_m_s']:.2f} m/s")
    print(f"  2.22 P  = {p2_22()['P_kW']:.1f} kW")
    print(f"  2.27 W  = {p2_27()['W_Btu']:.2f} Btu (p1={p2_27()['p1_psi']:.0f}, p2={p2_27()['p2_psi']:.0f})")
    print(f"  2.29 p2 = {p2_29()['p2_bar']:.2f} bar, W = {p2_29()['W_kJ']:.0f} kJ")
    print(f"  2.37 F  = {p2_37()['F_kN']:.2f} kN, {p2_37()['rpm']:.0f} rpm")
    print(f"  2.45 W  = {p2_45()['W_J']:.0f} J")
    print(f"  2.64 W={p2_64()['W_kJ']:.0f} kJ, Q={p2_64()['Q_kJ']:.2f} kJ, K={p2_64()['K_kW_min']:.5f} kW/min")
    print(f"  2.66 du = {p2_66()['du_Btu_lb']:.1f} Btu/lb")


if __name__ == "__main__":
    _demo()
