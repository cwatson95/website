"""
equations.py  —  Module 10.EQ (Topic 10: canonical equation registry, Engines)

The key equations of Topic 10 in canonical Moran 8e form, one per function:
  * Carnot ceilings       eta_max, beta_max, gamma_max      (Eqs. 5.9, 5.10, 5.11)
  * Kelvin-scale ratio    (Q_C/Q_H)_rev = T_C/T_H            (Eq. 5.7)
  * isothermal ideal gas  Q = W = R T ln(V2/V1)              (Eq. 2.17 form)
  * Stirling ideal eta    = Carnot value 1 - T_C/T_H         (Sec. 9.8.4)
  * regenerator duty      Q = c_v (T_H - T_C)                (Eq. 3.50 form)
  * regenerator effectiveness (h_x-h_2)/(h_4-h_2)            (Eq. 9.27)

test_equations.py checks each value AND imports BOTH concept modules — 10.1
(carnot_engine.py) and 10.2 (stirling_engine.py) — asserting they reproduce
these forms.  The Carnot ceilings (Eqs. 5.9-5.11) are also registered in 3.EQ
and 7.EQ with the same citations; Topic 10's canonical copies here cross-check
the engine modules.  Citations: Moran 8e (PDF = printed + 18).
"""
import math


# --- Carnot ceilings (Ch.5 Sec. 5.9) ----------------------------------------
def carnot_efficiency(T_C, T_H):
    """eta_max = 1 - T_C/T_H.  T absolute (K or degR). [Eq. 5.9, p.265]"""
    return 1.0 - T_C / T_H


def carnot_cop_refrigerator(T_C, T_H):
    """beta_max = T_C/(T_H - T_C). [Eq. 5.10, p.267]"""
    return T_C / (T_H - T_C)


def carnot_cop_heat_pump(T_C, T_H):
    """gamma_max = T_H/(T_H - T_C)  (gamma_max = beta_max + 1). [Eq. 5.11, p.267]"""
    return T_H / (T_H - T_C)


# --- Kelvin-scale heat ratio (Ch.5 Sec. 5.7) --------------------------------
def kelvin_heat_ratio(T_C, T_H):
    """(Q_C/Q_H)_rev = T_C/T_H for any reversible two-reservoir cycle -- the
    relation that defines the Kelvin scale. [Eq. 5.7, p.262]"""
    return T_C / T_H


# --- isothermal ideal-gas heat/work (Ch.2 Sec. 2.2) -------------------------
def isothermal_heat(R, T, V_ratio):
    """Internally reversible isothermal process of an ideal gas, per unit mass:
    Q = W = R T ln(V_ratio), V_ratio = V_out/V_in (du = 0 at constant T).
    [Eq. 2.17, W = integral p dV, p.48-49, with p V = m R T]"""
    return R * T * math.log(V_ratio)


# --- Stirling cycle & regeneration (Ch.9 Secs. 9.8.4, 9.7) ------------------
def stirling_efficiency(T_C, T_H):
    """Ideal Stirling-cycle thermal efficiency (100% regeneration) -- the SAME
    expression as the Carnot (and Ericsson) value: eta = 1 - T_C/T_H.
    [Sec. 9.8.4, p.552-553; Eq. 5.9, p.265]"""
    return 1.0 - T_C / T_H


def regenerator_heat(c_v, T_H, T_C):
    """Heat per unit mass shuttled internally by an ideal Stirling regenerator
    (constant-volume legs): Q = c_v (T_H - T_C).
    [Sec. 9.8.4, p.552; Eq. 3.50, p.140]"""
    return c_v * (T_H - T_C)


def regenerator_effectiveness(h_x, h_2, h_4):
    """Regenerator effectiveness: actual over maximum enthalpy increase,
    eta_reg = (h_x - h_2)/(h_4 - h_2); -> 1 as h_x -> h_4. [Eq. 9.27, p.539]"""
    return (h_x - h_2) / (h_4 - h_2)


REGISTRY = [
    ("5.9",  "carnot_efficiency",        "eta_max = 1 - T_C/T_H",       "10.1", "Sec. 5.9.1, p.265"),
    ("5.10", "carnot_cop_refrigerator",  "beta_max = T_C/(T_H-T_C)",    "10.1", "Sec. 5.9.2, p.267"),
    ("5.11", "carnot_cop_heat_pump",     "gamma_max= T_H/(T_H-T_C)",    "10.1", "Sec. 5.9.2, p.267"),
    ("5.7",  "kelvin_heat_ratio",        "(Q_C/Q_H)_rev = T_C/T_H",     "10.1", "Sec. 5.7, p.262"),
    ("2.17", "isothermal_heat",          "Q = W = R T ln(V2/V1)",       "10.2", "Sec. 2.2.3, p.48-49"),
    ("--",   "stirling_efficiency",      "eta = 1 - T_C/T_H (=Carnot)", "10.2", "Sec. 9.8.4, p.552-553"),
    ("3.50", "regenerator_heat",         "Q = c_v (T_H - T_C)",         "10.2", "Sec. 9.8.4, p.552 / Sec. 3.14.2, p.140"),
    ("9.27", "regenerator_effectiveness","eta_reg=(h_x-h_2)/(h_4-h_2)", "10.2", "Sec. 9.7, p.539"),
]


def _demo():
    print("Module 10.EQ -- Topic 10 (Engines) equation registry\n")
    for eq, fn, form, mod, src in REGISTRY:
        print("  Eq %-5s %-27s %-30s [%s | Moran %s]" % (eq, fn, form, mod, src))


if __name__ == "__main__":
    _demo()
