"""
examples.py  —  Module 1.EP (Topic 1: worked Example problems)

Each Moran 8e worked Example from Ch.1–2 reproduced from its GIVEN data using the
canonical Topic-1 equations (imported from module 1.EQ), so the book's published
ANSWER can be regenerated and checked (`test_examples.py`). This is the "ensure
the example problems are correct" half of the plan.

Full statements (GIVEN / FIND / ANSWER / METHOD) with page citations are in
`../examples.md`. Example 1.1 is conceptual (no numbers) and is discussed there.

Units follow each book example: 2.1/2.2 SI (kPa, m³, kJ); 2.3 English (Btu — the
energy balance is unit-agnostic addition); 2.4–2.6 SI (kW, K).
"""
import os
import sys

# canonical equations from module 1.EQ
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "1.EQ_list_of_equations", "code"))
import equations as eq   # noqa: E402

G_SI = 9.81           # m/s^2
GC_ENG = 32.2         # lb·ft/(lbf·s^2)


# extra rate-balance helpers used by the steady/transient examples
def newton_cooling(h, A, Tb, Tf):
    """Heat-transfer rate by convection  Q̇ = −h A (T_b − T_f).
    [Moran Eq. 2.34; used in Examples 2.4, 2.5, pp.68–69]"""
    return -h * A * (Tb - Tf)


def shaft_power(torque, omega):
    """Rotating-shaft power  Ẇ_shaft = τ ω  [W] (τ in N·m, ω in rad/s).
    [Moran Eq. 2.20; used in Example 2.6, p.71]"""
    return torque * omega


# ----------------------------------------------------------- Ch.2 examples ---
def ex_2_1():
    """Evaluating Expansion Work (p.50). Gas, pVⁿ=const, p1=3 bar, V1=0.1, V2=0.2 m³."""
    p1, V1, V2 = 300.0, 0.1, 0.2          # 3 bar = 300 kPa
    return {
        "p2_a_kPa": eq.polytropic_pressure(p1, V1, V2, 1.5),   # 106.1 kPa = 1.06 bar
        "W_a_n1.5": eq.polytropic_work(p1, V1, V2, 1.5),       # +17.6 kJ
        "W_b_n1":   eq.polytropic_work(p1, V1, V2, 1.0),       # +20.79 kJ
        "W_c_n0":   eq.polytropic_work(p1, V1, V2, 0.0),       # +30 kJ
    }


def ex_2_2():
    """Cooling a Gas in a Piston–Cylinder (p.64). m=0.4 kg, W from 2.1(a), Δu=−55 kJ/kg."""
    W = ex_2_1()["W_a_n1.5"]
    dU = 0.4 * (-55.0)                      # m (u2 - u1) = -22 kJ
    return {"W": W, "dU": dU, "Q": eq.closed_system_heat(W=W, dU=dU)}   # Q = -4.4 kJ


def ex_2_3():
    """Considering Alternative Systems (p.65). Air+piston, English units (Btu).
    Energy-balance assembly is unit-agnostic; piston pressure shown with conversions."""
    m_air, du_air = 0.6, 18.0              # lb, Btu/lb -> m_air*du = 10.8 Btu
    dU = m_air * du_air
    # piston force balance: p = m_piston*g/(gc*A) + p_atm  (lbf/in^2)
    p = 100.0 * 32.0 / (GC_ENG * 1.0) / 144.0 + 14.7        # ~15.4 lbf/in^2
    return {
        "p_lbf_in2": p,
        "Q_a": eq.closed_system_heat(W=4.56, dU=dU),               # 15.36 Btu (air alone)
        "Q_b": eq.closed_system_heat(W=4.35, dU=dU, dPE=0.2),      # 15.35 Btu (air+piston)
    }


def ex_2_4():
    """Gearbox at Steady State (p.68). Ẇ1=−60 kW in; Q̇=−hA(Tb−Tf), h=0.171, A=1, Tb=300, Tf=293 K."""
    Qdot = newton_cooling(0.171, 1.0, 300.0, 293.0)        # -1.2 kW
    W1 = -60.0                                              # input shaft (in)
    # steady state: Ẇ = Q̇ and Ẇ = W1 + W2  ->  W2 = Q̇ - W1
    W2 = Qdot - W1                                          # +58.8 kW
    return {"Qdot": Qdot, "W2": W2}


def ex_2_5():
    """Silicon Chip at Steady State (p.69). Ẇ=−0.225 W, h=150 W/m²K, A=25e−6 m², Tf=293 K."""
    Wdot, h, A, Tf = -0.225, 150.0, 25e-6, 293.0
    Tb_K = -Wdot / (h * A) + Tf                            # 353 K
    return {"Tb_K": Tb_K, "Tb_C": Tb_K - 273.15}           # 79.85 C (book rounds to 80)


def ex_2_6():
    """Transient Operation of a Motor (p.71). τ=18 N·m, ω=100 rad/s, Ẇ_elec=−2.0 kW."""
    Wshaft_kW = shaft_power(18.0, 100.0) / 1000.0          # +1.8 kW
    W_total = -2.0 + Wshaft_kW                             # -0.2 kW
    dE_limit = 4.0                                         # kJ, ΔE -> 4[1-e^(-0.05t)] -> 4
    return {"Wshaft_kW": Wshaft_kW, "W_total": W_total, "dE_limit": dE_limit}


def _demo():
    print("Module 1.EP — Topic 1 worked examples regenerated from GIVEN data\n")
    print(f"  Ex 2.1  W = {ex_2_1()['W_a_n1.5']:.1f} / {ex_2_1()['W_b_n1']:.2f} / "
          f"{ex_2_1()['W_c_n0']:.0f} kJ  (n=1.5/1/0)   [book 17.6 / 20.79 / 30]")
    print(f"  Ex 2.2  Q = {ex_2_2()['Q']:.1f} kJ                        [book -4.4]")
    print(f"  Ex 2.3  p={ex_2_3()['p_lbf_in2']:.1f} lbf/in², Q={ex_2_3()['Q_b']:.2f} Btu  [book 15.4, 15.35]")
    print(f"  Ex 2.4  Q̇ = {ex_2_4()['Qdot']:.1f} kW, Ẇ2 = {ex_2_4()['W2']:.1f} kW  [book -1.2, 58.8]")
    print(f"  Ex 2.5  Tb = {ex_2_5()['Tb_K']:.0f} K = {ex_2_5()['Tb_C']:.1f} °C    [book 353 K, 80 °C]")
    print(f"  Ex 2.6  Ẇ = {ex_2_6()['W_total']:.1f} kW, ΔE→{ex_2_6()['dE_limit']:.0f} kJ  [book -0.2, 4]")


if __name__ == "__main__":
    _demo()
