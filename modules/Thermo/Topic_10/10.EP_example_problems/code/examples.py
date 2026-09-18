"""
examples.py  —  Module 10.EP (Topic 10: worked Example problems)

The Moran 8e worked Examples for Topic 10 (Engines) — Ch.5 Examples 5.1, 5.2,
5.3 — regenerated from their GIVEN data using the concept-module functions
(10.1 carnot_engine, 10.2 stirling_engine), so each published ANSWER can be
reproduced and checked (`test_examples.py`).

Moran has NO worked Stirling Example (Sec. 9.8.4, p.552-553, is descriptive
only — verified by reading the section), so ex_s_1() is a module-authored
analysis "worked in the style of the book": an ideal Stirling engine between
stated temperatures with regeneration, per-process heats, and eta = Carnot.

Full statements (GIVEN / FIND / ANSWER / METHOD) with page citations are in
`../examples.md`.  Units follow each book example: 5.1/5.2 SI (kJ, K),
5.3 English (Btu, degR, $); S.1 SI per unit mass (kJ/kg).  Where the book
rounds an intermediate result before reusing it (Ex 5.3), the same stepwise
rounding is replicated.
"""
import os
import sys

# concept modules 10.1 and 10.2
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "10.1_carnot_engine", "code"))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "10.2_stirling_engine", "code"))
import carnot_engine as ce      # noqa: E402
import stirling_engine as se    # noqa: E402

KWH_PER_BTU = 1.0 / 3413.0      # book's conversion: 1 kW.h = 3413 Btu (Ex 5.3)


def ex_5_1():
    """Evaluating Power Cycle Performance (p.266-267).
    Power cycle between T_H = 2000 K and T_C = 400 K with Q_H = 1000 kJ.
    Classify: (a) eta = 60%; (b) W_cycle = 850 kJ; (c) Q_C = 200 kJ.
    Quick Quiz: Q_C = 300 kJ with W_cycle = 2700 kJ."""
    T_C, T_H, Q_H = 400.0, 2000.0, 1000.0
    eta_max = ce.carnot_efficiency(T_C, T_H)                    # 0.80  (Eq. 5.9)
    eta_a = 0.60
    eta_b = ce.thermal_efficiency(850.0, Q_H)                   # 0.85  (Eq. 2.42 form)
    W_c = Q_H - 200.0                                           # energy balance, 800 kJ
    eta_c = ce.efficiency_from_heats(200.0, Q_H)                # 0.80  (Eq. 5.4)
    # Quick Quiz: Q_C = 300 kJ, W = 2700 kJ -> Q_H = 3000 kJ, eta = 0.90
    eta_qq = ce.thermal_efficiency(2700.0, 2700.0 + 300.0)
    return {
        "eta_max": eta_max,
        "verdict_a": ce.cycle_status(eta_a, T_C, T_H),          # irreversible
        "eta_b": eta_b,
        "verdict_b": ce.cycle_status(eta_b, T_C, T_H),          # impossible
        "W_c": W_c,
        "eta_c": eta_c,
        "verdict_c": ce.cycle_status(eta_c, T_C, T_H),          # reversible
        "eta_qq": eta_qq,
        "verdict_qq": ce.cycle_status(eta_qq, T_C, T_H),        # impossible
    }


def ex_5_2():
    """Evaluating Refrigerator Performance (p.268-269).
    Refrigerator holds a freezer at -5 C (268 K) in surroundings at 22 C (295 K);
    Qdot_C = 8000 kJ/h removed, Wdot_cycle = 3200 kJ/h input.  Find beta and
    compare with the reversible ceiling.  Quick Quiz: claim of 800 kJ/h input."""
    T_C, T_H = 268.0, 295.0
    Qdot_C, Wdot = 8000.0, 3200.0
    beta = Qdot_C / Wdot                                        # 2.5  (Eq. 5.5, rate basis)
    beta_max = ce.carnot_cop_refrigerator(T_C, T_H)             # 9.9  (Eq. 5.10)
    # Quick Quiz: same duty with 800 kJ/h claimed -> beta = 10 > beta_max
    beta_claim = Qdot_C / 800.0
    return {
        "beta": beta,
        "beta_max": beta_max,
        "irreversible": beta < beta_max,                        # True: irreversibilities present
        "beta_claim": beta_claim,
        "claim_valid": beta_claim <= beta_max,                  # False: claim invalid
    }


def ex_5_3():
    """Evaluating Heat Pump Performance (p.269-270).
    Heat pump supplies Q_H = 5e5 Btu/day to a building at 70 F (530 R) from
    surroundings at 32 F (492 R); electricity at 13 cents/kW.h.
    (a) minimum theoretical work input, Btu/day; (b) minimum cost, $/day.
    Quick Quiz: cost with an actual COP of 3.0, and with resistance heating."""
    T_C, T_H = 492.0, 530.0
    Q_H_day = 5.0e5                                             # Btu/day
    gamma_max = ce.carnot_cop_heat_pump(T_C, T_H)               # 13.95  (Eq. 5.11)
    W_min = Q_H_day / gamma_max                                 # 3.58e4 Btu/day (W >= Q_H/gamma_max)
    W_min_book = float("%.3g" % W_min)                          # book rounds to 3.58e4 ...
    cost_min = W_min_book * KWH_PER_BTU * 0.13                  # ... then prices it: $1.36/day
    # Quick Quiz: (a) actual gamma = 3.0; (b) electric-resistance (W = Q_H)
    cost_cop3 = (Q_H_day / 3.0) * KWH_PER_BTU * 0.13            # $6.35/day
    cost_resistance = Q_H_day * KWH_PER_BTU * 0.13              # $19.04/day
    return {
        "gamma_max": gamma_max,
        "W_min": W_min,
        "W_min_book": W_min_book,
        "cost_min": cost_min,
        "cost_cop3": cost_cop3,
        "cost_resistance": cost_resistance,
    }


def ex_s_1():
    """MODULE-AUTHORED (not a Moran Example) — worked in the style of the book.
    Ideal Stirling engine (100% regeneration): air, T_H = 1000 K, T_C = 300 K,
    volume ratio r = V_max/V_min = 2.  Per unit mass find each process heat, the
    net work, the regenerator duty, and eta; verify eta equals the Carnot value.
    Data: R = 0.287, c_v = 0.718 kJ/kg.K.  [method: Sec. 9.8.4 + Eq. 2.17 form]"""
    R, c_v = 0.287, 0.718
    T_H, T_C, r = 1000.0, 300.0, 2.0
    Q_34 = se.stirling_heat_added(R, T_H, r)                    # 198.9 kJ/kg in at T_H
    Q_12 = se.stirling_heat_rejected(R, T_C, r)                 # 59.7 kJ/kg out at T_C
    W_net = se.stirling_net_work(R, T_H, T_C, r)                # 139.3 kJ/kg
    Q_regen = se.regenerator_heat(c_v, T_H, T_C)                # 502.6 kJ/kg internal
    eta = W_net / Q_34                                          # 0.70
    return {
        "Q_34": Q_34,
        "Q_12": Q_12,
        "W_net": W_net,
        "Q_regen": Q_regen,
        "eta": eta,
        "eta_ideal": se.stirling_efficiency(T_C, T_H),          # 0.70
        "eta_carnot": ce.carnot_efficiency(T_C, T_H),           # 0.70 -- same ceiling
        "eta_no_regen": se.stirling_efficiency_no_regen(R, c_v, T_H, T_C, r),  # 0.199
    }


def _demo():
    print("Module 10.EP — Topic 10 worked examples regenerated from GIVEN data\n")
    e = ex_5_1()
    print(f"  Ex 5.1  eta_max = {e['eta_max']:.2f}; (a) {e['verdict_a']}, "
          f"(b) eta={e['eta_b']:.2f} {e['verdict_b']}, (c) eta={e['eta_c']:.2f} {e['verdict_c']}"
          f"   [book: 0.80; irreversible / impossible / reversible]")
    print(f"          Quick Quiz: eta={e['eta_qq']:.2f} -> {e['verdict_qq']}   [book: impossible]")
    e = ex_5_2()
    print(f"  Ex 5.2  beta = {e['beta']:.1f}, beta_max = {e['beta_max']:.1f}"
          f"   [book: 2.5, 9.9]")
    print(f"          Quick Quiz: claimed beta = {e['beta_claim']:.0f} -> claim "
          f"{'valid' if e['claim_valid'] else 'invalid'}   [book: 10, invalid]")
    e = ex_5_3()
    print(f"  Ex 5.3  gamma_max = {e['gamma_max']:.2f}, W_min = {e['W_min']:.3g} Btu/day, "
          f"cost = ${e['cost_min']:.2f}/day   [book: 13.95, 3.58e4, 1.36]")
    print(f"          Quick Quiz: ${e['cost_cop3']:.2f}/day (COP 3), "
          f"${e['cost_resistance']:.2f}/day (resistance)   [book: 6.35, 19.04]")
    e = ex_s_1()
    print(f"  Ex S.1  (module-authored Stirling)  Q_34 = {e['Q_34']:.1f}, Q_12 = {e['Q_12']:.1f}, "
          f"W = {e['W_net']:.1f} kJ/kg")
    print(f"          Q_regen = {e['Q_regen']:.1f} kJ/kg, eta = {e['eta']:.2f} = Carnot "
          f"{e['eta_carnot']:.2f}  (no regen: {e['eta_no_regen']:.3f})")


if __name__ == "__main__":
    _demo()
