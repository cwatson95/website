"""
examples.py  —  Module 3.EP (Topic 3: worked Example problems, Moran Ch.5 second law)

Moran 8e Chapter-5 worked Examples 5.1-5.3 reproduced from their GIVEN data using
the Topic-3 second-law relations (Carnot efficiency Eq. 5.9; COPs Eqs. 5.10/5.11),
so the book's published ANSWERS regenerate and can be checked (test_examples.py).

Full statements (GIVEN / FIND / ANSWER) with page citations in ../examples.md.
Units: 5.1 SI (kJ); 5.2 SI (kJ/h, K); 5.3 English (Btu/day, degR, $).
All temperatures ABSOLUTE (K or degR).
"""


def carnot_efficiency(T_C, T_H):
    """eta_max = 1 - T_C/T_H. [Moran Eq. 5.9, Sec. 5.9.1, p.265]"""
    return 1.0 - T_C / T_H


def cop_ref_max(T_C, T_H):
    """beta_max = T_C/(T_H - T_C). [Moran Eq. 5.10, Sec. 5.9.2, p.267]"""
    return T_C / (T_H - T_C)


def cop_hp_max(T_C, T_H):
    """gamma_max = T_H/(T_H - T_C). [Moran Eq. 5.11, Sec. 5.9.2, p.267]"""
    return T_H / (T_H - T_C)


def ex_5_1():
    """Power cycle, reservoirs T_H=2000 K, T_C=400 K (p.266-267).
    (a) claimed eta=60%; (b) Q_H=1000 kJ, W=850 kJ; (c) Q_H=1000 kJ, Q_C=200 kJ."""
    T_C, T_H = 400.0, 2000.0
    eta_max = carnot_efficiency(T_C, T_H)                 # 0.80
    eta_a = 0.60                                          # (a) given
    eta_b = 850.0 / 1000.0                                # (b) 0.85
    W_c = 1000.0 - 200.0                                  # (c) W = Q_H - Q_C = 800 kJ
    eta_c = W_c / 1000.0                                  # 0.80
    return {"eta_max": eta_max,
            "eta_a": eta_a, "a_possible": eta_a <= eta_max,   # irreversible, allowed
            "eta_b": eta_b, "b_possible": eta_b <= eta_max,   # 0.85 > 0.80 -> impossible
            "W_c": W_c, "eta_c": eta_c}                        # reversible (= eta_max)


def ex_5_2():
    """Refrigerator: freezer at T_C=268 K, ambient T_H=295 K (p.268-269).
    Qc_dot=8000 kJ/h removed, W_dot=3200 kJ/h input."""
    T_C, T_H = 268.0, 295.0
    Qc_dot, W_dot = 8000.0, 3200.0
    beta = Qc_dot / W_dot                                 # 2.5 actual COP
    beta_max = cop_ref_max(T_C, T_H)                      # 9.9
    beta_claim = 8000.0 / 800.0                           # quick-quiz: claim W=800 -> 10
    return {"beta": beta, "beta_max": beta_max,
            "irreversible": beta < beta_max,
            "beta_claim": beta_claim, "claim_valid": beta_claim <= beta_max}


def ex_5_3():
    """Heat pump: building 70 degF (530 degR), surroundings 32 degF (492 degR),
    Q_H = 5e5 Btu/day; electricity $0.13/kWh, 3413 Btu/kWh (p.269-270)."""
    T_C, T_H = 492.0, 530.0
    Q_H = 5.0e5
    gamma_max = cop_hp_max(T_C, T_H)                      # 13.95
    W_min = Q_H / gamma_max                               # 3.58e4 Btu/day
    cost = round(W_min, -2) * (1.0 / 3413.0) * 0.13       # book carries W_min=3.58e4 (3 s.f.) -> $1.36/day
    return {"gamma_max": gamma_max, "W_min_Btu_day": W_min, "cost_per_day": cost}


def _demo():
    print("Module 3.EP -- Moran Ch.5 second-law examples regenerated from GIVEN data\n")
    e1 = ex_5_1()
    print("  Ex 5.1 power cycle (2000/400 K): eta_max=%.2f" % e1["eta_max"])
    print("    (a) eta=0.60 possible? %s (irreversible)   [book yes]" % e1["a_possible"])
    print("    (b) eta=%.2f possible? %s                  [book NO]" % (e1["eta_b"], e1["b_possible"]))
    print("    (c) W=%.0f kJ, eta=%.2f (reversible)        [book 800 kJ, 0.80]" % (e1["W_c"], e1["eta_c"]))
    e2 = ex_5_2()
    print("\n  Ex 5.2 refrigerator (268/295 K): beta=%.1f, beta_max=%.1f  [book 2.5, 9.9]"
          % (e2["beta"], e2["beta_max"]))
    print("    inventor claim beta=%.0f valid? %s          [book invalid]"
          % (e2["beta_claim"], e2["claim_valid"]))
    e3 = ex_5_3()
    print("\n  Ex 5.3 heat pump (530/492 degR): gamma_max=%.2f  [book 13.95]" % e3["gamma_max"])
    print("    W_min=%.3g Btu/day, cost=$%.2f/day            [book 3.58e4, $1.36]"
          % (e3["W_min_Btu_day"], e3["cost_per_day"]))


if __name__ == "__main__":
    _demo()
