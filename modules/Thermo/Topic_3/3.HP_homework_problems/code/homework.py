"""
homework.py  —  Module 3.HP (Topic 3: end-of-chapter homework, Moran Ch.5 second law)

7 second-law problems from Moran 8e Ch.5 (printed pp.278-286), each SOLVED from its
given data.  Moran provides no answer key, so these are *worked solutions*,
reproduced and checked in test_homework.py (with energy-balance/consistency checks).

Statements in ../problems.md; citations in ../refs.md.  English temperatures use
T(degR) = T(degF) + 459.67, EXCEPT P5.50 which follows the book's rounded +460.
All Carnot-formula temperatures are ABSOLUTE (K or degR).
"""


def carnot_efficiency(T_C, T_H):
    return 1.0 - T_C / T_H


def cop_ref_max(T_C, T_H):
    return T_C / (T_H - T_C)


def p5_2():
    """Proposed cycle receives Q_C=500 kJ from a cold reservoir, rejects Q_H=400 kJ
    to a hot reservoir, and delivers W=100 kJ. Possible? (p.278)"""
    Q_C_from_cold, Q_H_to_hot, W_claim = 500.0, 400.0, 100.0
    W_balance = Q_C_from_cold - Q_H_to_hot          # first law: 100 kJ (consistent)
    # Net heat flows cold->hot AND net work is produced -> violates the 2nd law.
    return {"W_balance": W_balance,
            "energy_ok": abs(W_balance - W_claim) < 1e-9,
            "possible": False}


def p5_21():
    """Reversible power cycle, eta=40%, Q_H=50 kJ at T_H=600 K. Find T_C, Q_C, W. (p.281)"""
    eta, Q_H, T_H = 0.40, 50.0, 600.0
    T_C = T_H * (1.0 - eta)                          # reversible: eta = 1 - T_C/T_H -> 360 K
    W = eta * Q_H                                    # 20 kJ
    Q_C = Q_H - W                                    # 30 kJ
    return {"T_C": T_C, "W": W, "Q_C": Q_C}


def p5_31():
    """Power cycle, Q_H=1000 Btu, T_H=1000 degF, T_C=300 degF; actual eta = 75% of the
    reversible value. Find eta_rev, actual eta, W, Q_C. (p.282)"""
    T_H, T_C = 1000.0 + 459.67, 300.0 + 459.67      # degR
    eta_rev = carnot_efficiency(T_C, T_H)           # ~0.480
    eta = 0.75 * eta_rev                            # ~0.360
    Q_H = 1000.0
    W = eta * Q_H                                   # ~359.7 Btu
    Q_C = Q_H - W                                   # ~640.3 Btu
    return {"eta_rev": eta_rev, "eta": eta, "W": W, "Q_C": Q_C}


def p5_34():
    """Power cycle between 500 K and 310 K, W=0.1 MW. Minimum theoretical rate of energy
    rejected to the cold reservoir, in MW. (p.282)"""
    T_H, T_C, W = 500.0, 310.0, 0.1
    eta_max = carnot_efficiency(T_C, T_H)           # 0.38
    Qh_min = W / eta_max                            # 0.2632 MW (reversible -> min heat in)
    Qc_min = Qh_min - W                             # 0.1632 MW
    return {"eta_max": eta_max, "Qh_min": Qh_min, "Qc_min": Qc_min}


def p5_48():
    """A reversible power cycle has eta=20% between two reservoirs. COP of (a) a
    reversible refrigerator, (b) a reversible heat pump, between the same two. (p.283)"""
    eta = 0.20
    ratio = 1.0 - eta                               # T_C/T_H = 0.8
    beta = ratio / (1.0 - ratio)                    # 4.0
    gamma = 1.0 / (1.0 - ratio)                     # 5.0  (= beta + 1)
    return {"beta": beta, "gamma": gamma}


def p5_50():
    """Refrigerator: freezer at 20 degF, kitchen at 70 degF. Claimed COP (a) 10, (b) 9.6,
    (c) 4 -- evaluate each. Book uses T(degR)=T(degF)+460 -> beta_max=9.6. (p.284)"""
    T_C, T_H = 20.0 + 460.0, 70.0 + 460.0           # 480, 530 degR
    beta_max = cop_ref_max(T_C, T_H)                # 9.6
    claims = {"a": 10.0, "b": 9.6, "c": 4.0}
    verdict = {k: ("impossible" if v > beta_max + 1e-9 else
                   "reversible" if abs(v - beta_max) <= 1e-9 else
                   "possible (irreversible)")
               for k, v in claims.items()}
    return {"beta_max": beta_max, "verdict": verdict}


def p5_76():
    """Carnot power cycle, T_H=600 K, T_C=300 K. (a) thermal efficiency; (b) percent
    change in efficiency if T_H increases by 15% with T_C fixed. (p.286)"""
    T_H, T_C = 600.0, 300.0
    eta = carnot_efficiency(T_C, T_H)               # 0.5
    eta2 = carnot_efficiency(T_C, 1.15 * T_H)       # T_H'=690 K -> 0.5652
    pct = (eta2 - eta) / eta * 100.0                # +13.04 %
    return {"eta": eta, "eta2": eta2, "pct_change": pct}


def _demo():
    print("Module 3.HP -- Topic 3 homework (Moran Ch.5; worked solutions, no book key)\n")
    print("  5.2  W=%.0f kJ by balance, but possible? %s (cold->hot + work: violates 2nd law)"
          % (p5_2()["W_balance"], p5_2()["possible"]))
    r = p5_21(); print("  5.21 T_C=%.0f K, W=%.0f kJ, Q_C=%.0f kJ" % (r["T_C"], r["W"], r["Q_C"]))
    r = p5_31(); print("  5.31 eta_rev=%.3f, eta=%.3f, W=%.1f Btu, Q_C=%.1f Btu"
                       % (r["eta_rev"], r["eta"], r["W"], r["Q_C"]))
    r = p5_34(); print("  5.34 eta_max=%.2f, min Q_C rejected=%.4f MW" % (r["eta_max"], r["Qc_min"]))
    r = p5_48(); print("  5.48 beta_ref=%.0f, gamma_hp=%.0f" % (r["beta"], r["gamma"]))
    r = p5_50(); print("  5.50 beta_max=%.1f -> (a)%s (b)%s (c)%s"
                       % (r["beta_max"], r["verdict"]["a"], r["verdict"]["b"], r["verdict"]["c"]))
    r = p5_76(); print("  5.76 eta=%.2f; +15%% T_H -> eta=%.4f (%.2f%% change)"
                       % (r["eta"], r["eta2"], r["pct_change"]))


if __name__ == "__main__":
    _demo()
