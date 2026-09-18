"""
examples.py  —  Module 7.EP (Topic 7: worked Examples, Moran Ch.5/6)

Seven Moran 8e worked Examples spanning the performance metrics, reproduced from their
GIVEN data so the book's published ANSWERS regenerate and can be checked (test_examples.py):
  5.1 power cycle reversible/irreversible/impossible  (thermal efficiency + Carnot)
  5.2 evaluating refrigerator performance             (COP beta + Carnot ceiling)
  5.3 evaluating heat pump performance                (COP gamma_max, min work, cost)
  6.11 turbine work from the isentropic efficiency    (steam, Eq. 6.46)
  6.12 isentropic turbine efficiency from the work    (air,   Eq. 6.46)
  6.13 isentropic nozzle efficiency                   (steam, Eq. 6.47)
  6.14 isentropic compressor efficiency               (R-22,  Eq. 6.48)

Full statements with page citations in ../examples.md.  Units per example (SI or English);
T(degR) = T(degF) + 459.67.
"""


def _classify(eta, eta_max, tol=1e-9):
    """Second-law verdict for a power cycle vs. its Carnot ceiling (Ex 5.1)."""
    if eta > eta_max + tol:
        return "impossible"
    if abs(eta - eta_max) <= 1e-6:
        return "reversible"
    return "irreversible"


def ex_5_1():
    """Evaluating Power Cycle Performance (p.266-267). Power cycle between TH=2000 K,
    TC=400 K. (a) QH=1000 kJ, eta=60%. (b) QH=1000 kJ, Wcycle=850 kJ. (c) QH=1000 kJ,
    QC=200 kJ.  Classify each: reversible / irreversible / impossible."""
    TH, TC = 2000.0, 400.0
    eta_max = 1.0 - TC / TH
    eta_a = 0.60
    eta_b = 850.0 / 1000.0
    eta_c = (1000.0 - 200.0) / 1000.0
    return {"eta_max": eta_max,
            "eta_a": eta_a, "class_a": _classify(eta_a, eta_max),
            "eta_b": eta_b, "class_b": _classify(eta_b, eta_max),
            "eta_c": eta_c, "class_c": _classify(eta_c, eta_max)}


def ex_5_2():
    """Evaluating Refrigerator Performance (p.268-269). Freezer at -5 C (268 K) in 22 C
    (295 K) air; QC=8000 kJ/h removed, Wcycle=3200 kJ/h input.  FIND beta, beta_max."""
    TC, TH = 268.0, 295.0
    beta = 8000.0 / 3200.0
    beta_max = TC / (TH - TC)
    return {"beta": beta, "beta_max": beta_max}


def ex_5_3():
    """Evaluating Heat Pump Performance (p.269-270). Building at 70 F (530 degR) needs
    QH=5e5 Btu/day; outside 32 F (492 degR); electricity 0.13 $/kWh.
    FIND gamma_max, minimum work input, minimum cost.  (1 kWh = 3413 Btu.)"""
    TH, TC, QH = 530.0, 492.0, 5.0e5
    gamma_max = TH / (TH - TC)
    W_min = QH / gamma_max                      # ~3.58e4 Btu/day
    # book carries the rounded 3.58e4 Btu/day into the cost calculation
    cost = (3.58e4 / 3413.0) * 0.13             # $/day
    return {"gamma_max": gamma_max, "W_min": W_min, "cost": cost}


def ex_6_11():
    """Determining Turbine Work Using the Isentropic Efficiency (p.333-334). Steam,
    p1=5 bar, T1=320 C -> p2=1 bar, eta_t=75%.  h1=3105.6, h2s=2743.0 kJ/kg (Table A-4).
    FIND work per unit mass."""
    h1, h2s, eta_t = 3105.6, 2743.0, 0.75
    return {"W_m": eta_t * (h1 - h2s)}


def ex_6_12():
    """Evaluating Isentropic Turbine Efficiency (p.334-335). Air, p1=3.0 bar, T1=390 K ->
    p2=1.0 bar; actual work 74 kJ/kg.  h1=390.88, pr1=3.481 (Table A-22).  FIND eta_t."""
    h1, pr1, w_actual = 390.88, 3.481, 74.0
    pr2s = (1.0 / 3.0) * pr1                     # Eq. 6.41 -> pr2s = 1.1603
    h2s = 285.27                                 # interpolation in Table A-22 at pr2s
    w_s = h1 - h2s                               # isentropic work = 105.6 kJ/kg
    return {"pr2s": pr2s, "w_s": w_s, "eta_t": w_actual / w_s}


def ex_6_13():
    """Evaluating Isentropic Nozzle Efficiency (p.336-337). Steam, p1=140 lbf/in^2,
    T1=600 F, V1=100 ft/s -> p2=40 lbf/in^2, T2=350 F.  h1=1326.4, h2=1211.8,
    h2s=1202.3 Btu/lb.  FIND nozzle efficiency."""
    h1, h2, h2s, V1 = 1326.4, 1211.8, 1202.3, 100.0
    ke1 = V1 ** 2 / (2.0 * 32.2 * 778.0)        # Btu/lb (gc=32.2, J=778) -> 0.2
    ke2 = h1 - h2 + ke1                          # actual exit KE     -> 114.8
    ke2s = h1 - h2s + ke1                        # isentropic exit KE -> 124.3
    return {"ke2": ke2, "ke2s": ke2s, "eta_n": ke2 / ke2s}


def ex_6_14():
    """Evaluating Isentropic Compressor Efficiency (p.338-339). R-22 from Ex 6.8:
    mdot=0.07 kg/s, h1=249.75, h2=294.17, h2s=285.58 kJ/kg (Table A-9).
    FIND power, eta_c."""
    mdot, h1, h2, h2s = 0.07, 249.75, 294.17, 285.58
    W_cv = mdot * (h1 - h2)                      # kW (negative: work in)
    eta_c = (h2s - h1) / (h2 - h1)
    return {"W_cv": W_cv, "eta_c": eta_c}


def _demo():
    print("Module 7.EP -- Topic 7 worked examples regenerated from GIVEN data\n")
    e = ex_5_1(); print("  Ex 5.1 power cycle: eta_max=%.2f; (a)%s (b)%s (c)%s  [book irrev/imposs/rev]"
                        % (e["eta_max"], e["class_a"], e["class_b"], e["class_c"]))
    e = ex_5_2(); print("  Ex 5.2 refrigerator: beta=%.1f, beta_max=%.1f                 [book 2.5, 9.9]"
                        % (e["beta"], e["beta_max"]))
    e = ex_5_3(); print("  Ex 5.3 heat pump: gamma_max=%.2f, W_min=%.2e Btu/day, cost=$%.2f [book 13.95, 3.58e4, 1.36]"
                        % (e["gamma_max"], e["W_min"], e["cost"]))
    e = ex_6_11(); print("  Ex 6.11 steam turbine: W/m=%.2f kJ/kg                         [book 271.95]" % e["W_m"])
    e = ex_6_12(); print("  Ex 6.12 air turbine: w_s=%.1f kJ/kg, eta_t=%.2f               [book 105.6, 0.70]"
                        % (e["w_s"], e["eta_t"]))
    e = ex_6_13(); print("  Ex 6.13 steam nozzle: ke2=%.1f, ke2s=%.1f, eta_n=%.3f         [book 114.8,124.3,0.924]"
                        % (e["ke2"], e["ke2s"], e["eta_n"]))
    e = ex_6_14(); print("  Ex 6.14 R-22 compressor: W_cv=%.2f kW, eta_c=%.2f             [book -3.11, 0.81]"
                        % (e["W_cv"], e["eta_c"]))


if __name__ == "__main__":
    _demo()
