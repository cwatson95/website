"""
equations.py  —  Module 7.EQ (Topic 7: canonical equation registry, Performance Metrics)

The key equations of Topic 7 in canonical Moran 8e form, one per function:
  * thermal efficiency   eta = W/Q_in = 1 - Q_out/Q_in      (Eqs. 2.42, 2.43)
  * COP refrig./heat pump beta = Q_C/W ; gamma = Q_H/W      (Eqs. 2.45, 2.47)
  * Carnot ceilings      eta_max, beta_max, gamma_max        (Eqs. 5.9, 5.10, 5.11)
  * isentropic device    turbine / nozzle / compressor       (Eqs. 6.46, 6.47, 6.48)

test_equations.py checks each value AND imports the concept module 07.1 (efficiency.py),
asserting it reproduces these forms.  Citations: Moran 8e (PDF = printed + 18).
"""


# --- cycle metrics (Ch.2 Sec. 2.6) ------------------------------------------
def thermal_efficiency(W_cycle, Q_in):
    """eta = W_cycle / Q_in. [Eq. 2.42, p.74]"""
    return W_cycle / Q_in


def thermal_efficiency_alt(Q_in, Q_out):
    """eta = 1 - Q_out/Q_in. [Eq. 2.43, p.74]"""
    return 1.0 - Q_out / Q_in


def cop_refrigerator(Q_C, W_cycle):
    """beta = Q_C / W_cycle. [Eq. 2.45, p.75]"""
    return Q_C / W_cycle


def cop_heat_pump(Q_H, W_cycle):
    """gamma = Q_H / W_cycle  (gamma = beta + 1). [Eq. 2.47, p.75]"""
    return Q_H / W_cycle


# --- Carnot ceilings (Ch.5 Sec. 5.9) ----------------------------------------
def carnot_efficiency(T_C, T_H):
    """eta_max = 1 - T_C/T_H. [Eq. 5.9, p.265]"""
    return 1.0 - T_C / T_H


def carnot_cop_refrigerator(T_C, T_H):
    """beta_max = T_C/(T_H - T_C). [Eq. 5.10, p.267]"""
    return T_C / (T_H - T_C)


def carnot_cop_heat_pump(T_C, T_H):
    """gamma_max = T_H/(T_H - T_C). [Eq. 5.11, p.267]"""
    return T_H / (T_H - T_C)


# --- isentropic device efficiencies (Ch.6 Sec. 6.12) ------------------------
def isentropic_turbine_efficiency(h1, h2, h2s):
    """eta_t = (h1 - h2)/(h1 - h2s). [Eq. 6.46, p.333]"""
    return (h1 - h2) / (h1 - h2s)


def isentropic_nozzle_efficiency(ke2, ke2s):
    """eta_n = (V2^2/2)/(V2^2/2)_s. [Eq. 6.47, p.335]"""
    return ke2 / ke2s


def isentropic_compressor_efficiency(h1, h2, h2s):
    """eta_c = (h2s - h1)/(h2 - h1)  (pump: same form). [Eq. 6.48, p.338]"""
    return (h2s - h1) / (h2 - h1)


REGISTRY = [
    ("2.42", "thermal_efficiency",              "eta = W/Q_in",            "07.1", "Sec. 2.6.2, p.74"),
    ("2.43", "thermal_efficiency_alt",          "eta = 1 - Q_out/Q_in",    "07.1", "Sec. 2.6.2, p.74"),
    ("2.45", "cop_refrigerator",                "beta = Q_C/W",            "07.1", "Sec. 2.6.3, p.75"),
    ("2.47", "cop_heat_pump",                   "gamma = Q_H/W",           "07.1", "Sec. 2.6.3, p.75"),
    ("5.9",  "carnot_efficiency",               "eta_max = 1 - T_C/T_H",   "07.1", "Sec. 5.9.1, p.265"),
    ("5.10", "carnot_cop_refrigerator",         "beta_max = T_C/(T_H-T_C)","07.1", "Sec. 5.9.2, p.267"),
    ("5.11", "carnot_cop_heat_pump",            "gamma_max= T_H/(T_H-T_C)","07.1", "Sec. 5.9.2, p.267"),
    ("6.46", "isentropic_turbine_efficiency",   "eta_t=(h1-h2)/(h1-h2s)",  "07.1", "Sec. 6.12.1, p.333"),
    ("6.47", "isentropic_nozzle_efficiency",    "eta_n=ke2/ke2s",          "07.1", "Sec. 6.12.2, p.335"),
    ("6.48", "isentropic_compressor_efficiency","eta_c=(h2s-h1)/(h2-h1)",  "07.1", "Sec. 6.12.3, p.338"),
]


def _demo():
    print("Module 7.EQ -- Topic 7 (Performance Metrics) equation registry\n")
    for eq, fn, form, mod, src in REGISTRY:
        print("  Eq %-5s %-32s %-26s [%s | Moran %s]" % (eq, fn, form, mod, src))


if __name__ == "__main__":
    _demo()
