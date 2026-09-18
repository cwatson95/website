"""
equations.py  —  Module 9.EQ (Topic 9: canonical equation registry, Power & Refrigeration Cycles)

The key equations of Topic 9 in canonical Moran 8e form, one per function:
  * Carnot ceiling        eta_max = 1 - T_C/T_H                       (Eq. 5.9)
  * engine terminology    mep = W_cycle/(V1 - V2)                     (Eq. 9.1)
  * Otto cycle            eta air-table / T2, T4 / eta(r)             (Eqs. 9.3, 9.6-9.8)
  * Diesel cycle          eta air-table / eta(r, rc)                  (Eqs. 9.11, 9.13)
  * dual cycle            eta air-table / eta(r, rp, rc)              (Eq. 9.14 + closed form)
  * Brayton cycle         component works & heats / eta / bwr /
                          cold-air T's / eta(rp) / regenerator        (Eqs. 9.15-9.20, 9.23-9.25, 9.27)
  * Rankine cycle         component balances / eta / bwr / pump work  (Eqs. 8.1-8.6, 8.7b)

test_equations.py checks each against a book-verified value AND imports ALL SIX concept
modules (09.1 carnot, 09.2 otto, 09.3 diesel, 09.4 dual, 09.5 brayton, 09.6 rankine),
asserting they compute identical results -- a formula change anywhere in Topic 9 fails
the hub.  Citations: Moran 8e (PDF = printed + 18); see ../refs.md.
"""

K_AIR = 1.4  # cp/cv for air, cold air-standard (Moran Table A-20)


# --- Carnot ceiling (Ch.5) ---------------------------------------------------
def carnot_efficiency(T_C, T_H):
    """eta_max = 1 - T_C/T_H  (T absolute). [Eq. 5.9, p.265]"""
    return 1.0 - T_C / T_H


# --- engine terminology (Sec. 9.1) -------------------------------------------
def mean_effective_pressure(W_cycle, V1, V2):
    """mep = (net work for one cycle)/(displacement volume) = W_cycle/(V1 - V2).
    [Eq. 9.1, p.511]"""
    return W_cycle / (V1 - V2)


# --- Otto cycle (Sec. 9.2) ----------------------------------------------------
def otto_efficiency_air_table(u1, u2, u3, u4):
    """eta = 1 - (u4 - u1)/(u3 - u2)  (Table A-22 u's). [Eq. 9.3, p.514]"""
    return 1.0 - (u4 - u1) / (u3 - u2)


def otto_temp_after_compression(T1, r, k=K_AIR):
    """T2 = T1 r^(k-1)  (cold air-standard). [Eq. 9.6, p.514]"""
    return T1 * r ** (k - 1.0)


def otto_temp_after_expansion(T3, r, k=K_AIR):
    """T4 = T3 / r^(k-1)  (cold air-standard). [Eq. 9.7, p.514]"""
    return T3 / r ** (k - 1.0)


def otto_efficiency(r, k=K_AIR):
    """eta = 1 - 1/r^(k-1)  (cold air-standard), r = V1/V2. [Eq. 9.8, p.515]"""
    return 1.0 - 1.0 / r ** (k - 1.0)


# --- Diesel cycle (Sec. 9.3) ---------------------------------------------------
def diesel_efficiency_air_table(u1, u4, h2, h3):
    """eta = 1 - (u4 - u1)/(h3 - h2)  (constant-p heat addition). [Eq. 9.11, p.519]"""
    return 1.0 - (u4 - u1) / (h3 - h2)


def diesel_efficiency(r, rc, k=K_AIR):
    """eta = 1 - (1/r^(k-1)) (rc^k - 1)/(k(rc - 1))  (cold air-standard),
    rc = V3/V2 cutoff ratio. [Eq. 9.13, p.519]"""
    return 1.0 - (1.0 / r ** (k - 1.0)) * (rc ** k - 1.0) / (k * (rc - 1.0))


# --- dual cycle (Sec. 9.4) -----------------------------------------------------
def dual_efficiency_air_table(u1, u2, u3, h3, h4, u5):
    """eta = 1 - (u5 - u1)/[(u3 - u2) + (h4 - h3)]  (constant-V then constant-p).
    [Eq. 9.14, p.523]"""
    return 1.0 - (u5 - u1) / ((u3 - u2) + (h4 - h3))


def dual_efficiency(r, rp, rc, k=K_AIR):
    """eta = 1 - (1/r^(k-1)) (rp rc^k - 1)/[(rp - 1) + k rp (rc - 1)]  (cold
    air-standard closed form; -> Otto as rc->1, Diesel as rp->1). [Sec. 9.4, p.523]"""
    return 1.0 - (1.0 / r ** (k - 1.0)) * (rp * rc ** k - 1.0) / ((rp - 1.0) + k * rp * (rc - 1.0))


# --- Brayton cycle (Secs. 9.6-9.7) ---------------------------------------------
def brayton_turbine_work(h3, h4):
    """Wt/m = h3 - h4. [Eq. 9.15, p.527]"""
    return h3 - h4


def brayton_compressor_work(h1, h2):
    """Wc/m = h2 - h1. [Eq. 9.16, p.527]"""
    return h2 - h1


def brayton_heat_added(h2, h3):
    """Qin/m = h3 - h2. [Eq. 9.17, p.527]"""
    return h3 - h2


def brayton_heat_rejected(h1, h4):
    """Qout/m = h4 - h1. [Eq. 9.18, p.528]"""
    return h4 - h1


def brayton_efficiency_air_table(h1, h2, h3, h4):
    """eta = [(h3 - h4) - (h2 - h1)]/(h3 - h2). [Eq. 9.19, p.528]"""
    return ((h3 - h4) - (h2 - h1)) / (h3 - h2)


def brayton_back_work_ratio(h1, h2, h3, h4):
    """bwr = (h2 - h1)/(h3 - h4)  (40-80% for gas turbines). [Eq. 9.20, p.528]"""
    return (h2 - h1) / (h3 - h4)


def brayton_temp_after_compression(T1, rp, k=K_AIR):
    """T2 = T1 rp^((k-1)/k)  (cold air-standard). [Eq. 9.23, p.529]"""
    return T1 * rp ** ((k - 1.0) / k)


def brayton_temp_after_expansion(T3, rp, k=K_AIR):
    """T4 = T3 (1/rp)^((k-1)/k)  (cold air-standard). [Eq. 9.24, p.529]"""
    return T3 * (1.0 / rp) ** ((k - 1.0) / k)


def brayton_efficiency(rp, k=K_AIR):
    """eta = 1 - 1/rp^((k-1)/k)  (cold air-standard), rp = p2/p1. [Eq. 9.25, p.532]"""
    return 1.0 - 1.0 / rp ** ((k - 1.0) / k)


def regenerator_effectiveness(hx, h2, h4):
    """eta_reg = (hx - h2)/(h4 - h2)  (regenerative gas turbine). [Eq. 9.27, p.539]"""
    return (hx - h2) / (h4 - h2)


# --- Rankine cycle (Secs. 8.2) --------------------------------------------------
def rankine_turbine_work(h1, h2):
    """Wt/m = h1 - h2. [Eq. 8.1, p.446]"""
    return h1 - h2


def rankine_condenser_heat(h2, h3):
    """Qout/m = h2 - h3. [Eq. 8.2, p.447]"""
    return h2 - h3


def rankine_pump_work(h3, h4):
    """Wp/m = h4 - h3. [Eq. 8.3, p.447]"""
    return h4 - h3


def rankine_boiler_heat(h4, h1):
    """Qin/m = h1 - h4. [Eq. 8.4, p.447]"""
    return h1 - h4


def rankine_efficiency(h1, h2, h3, h4):
    """eta = [(h1 - h2) - (h4 - h3)]/(h1 - h4). [Eq. 8.5a, p.447]"""
    return ((h1 - h2) - (h4 - h3)) / (h1 - h4)


def rankine_back_work_ratio(h1, h2, h3, h4):
    """bwr = (h4 - h3)/(h1 - h2)  (~1-2% for vapor plants). [Eq. 8.6, p.447]"""
    return (h4 - h3) / (h1 - h2)


def rankine_pump_work_approx(v3, p3, p4):
    """(Wp/m)_s ~ v3 (p4 - p3)  (incompressible liquid). [Eq. 8.7b, p.449]"""
    return v3 * (p4 - p3)


REGISTRY = [
    ("5.9",  "carnot_efficiency",           "eta_max = 1 - T_C/T_H",                  "09.1", "Sec. 5.9.1, p.265"),
    ("9.1",  "mean_effective_pressure",     "mep = W_cycle/(V1-V2)",                  "09.2/09.4", "Sec. 9.1, p.511"),
    ("9.3",  "otto_efficiency_air_table",   "eta = 1-(u4-u1)/(u3-u2)",                "09.2", "Sec. 9.2, p.514"),
    ("9.6",  "otto_temp_after_compression", "T2 = T1 r^(k-1)",                        "09.2", "Sec. 9.2, p.514"),
    ("9.7",  "otto_temp_after_expansion",   "T4 = T3/r^(k-1)",                        "09.2", "Sec. 9.2, p.514"),
    ("9.8",  "otto_efficiency",             "eta = 1 - 1/r^(k-1)",                    "09.2", "Sec. 9.2, p.515"),
    ("9.11", "diesel_efficiency_air_table", "eta = 1-(u4-u1)/(h3-h2)",                "09.3", "Sec. 9.3, p.519"),
    ("9.13", "diesel_efficiency",           "eta = 1-(1/r^(k-1))(rc^k-1)/(k(rc-1))",  "09.3", "Sec. 9.3, p.519"),
    ("9.14", "dual_efficiency_air_table",   "eta = 1-(u5-u1)/[(u3-u2)+(h4-h3)]",      "09.4", "Sec. 9.4, p.523"),
    ("—",    "dual_efficiency",             "eta = 1-(1/r^(k-1))(rp rc^k-1)/(...)",   "09.4", "Sec. 9.4, p.523"),
    ("9.15", "brayton_turbine_work",        "Wt/m = h3 - h4",                         "09.5", "Sec. 9.6.1, p.527"),
    ("9.16", "brayton_compressor_work",     "Wc/m = h2 - h1",                         "09.5", "Sec. 9.6.1, p.527"),
    ("9.17", "brayton_heat_added",          "Qin/m = h3 - h2",                        "09.5", "Sec. 9.6.1, p.527"),
    ("9.18", "brayton_heat_rejected",       "Qout/m = h4 - h1",                       "09.5", "Sec. 9.6.1, p.528"),
    ("9.19", "brayton_efficiency_air_table","eta = [(h3-h4)-(h2-h1)]/(h3-h2)",        "09.5", "Sec. 9.6.1, p.528"),
    ("9.20", "brayton_back_work_ratio",     "bwr = (h2-h1)/(h3-h4)",                  "09.5", "Sec. 9.6.1, p.528"),
    ("9.23", "brayton_temp_after_compression", "T2 = T1 rp^((k-1)/k)",                "09.5", "Sec. 9.6.2, p.529"),
    ("9.24", "brayton_temp_after_expansion","T4 = T3 (1/rp)^((k-1)/k)",               "09.5", "Sec. 9.6.2, p.529"),
    ("9.25", "brayton_efficiency",          "eta = 1 - 1/rp^((k-1)/k)",               "09.5", "Sec. 9.6.2, p.532"),
    ("9.27", "regenerator_effectiveness",   "eta_reg = (hx-h2)/(h4-h2)",              "09.5", "Sec. 9.7, p.539"),
    ("8.1",  "rankine_turbine_work",        "Wt/m = h1 - h2",                         "09.6", "Sec. 8.2.1, p.446"),
    ("8.2",  "rankine_condenser_heat",      "Qout/m = h2 - h3",                       "09.6", "Sec. 8.2.1, p.447"),
    ("8.3",  "rankine_pump_work",           "Wp/m = h4 - h3",                         "09.6", "Sec. 8.2.1, p.447"),
    ("8.4",  "rankine_boiler_heat",         "Qin/m = h1 - h4",                        "09.6", "Sec. 8.2.1, p.447"),
    ("8.5a", "rankine_efficiency",          "eta = [(h1-h2)-(h4-h3)]/(h1-h4)",        "09.6", "Sec. 8.2.1, p.447"),
    ("8.6",  "rankine_back_work_ratio",     "bwr = (h4-h3)/(h1-h2)",                  "09.6", "Sec. 8.2.1, p.447"),
    ("8.7b", "rankine_pump_work_approx",    "(Wp/m)_s ~ v3(p4-p3)",                   "09.6", "Sec. 8.2.2, p.449"),
]


def _demo():
    print("Module 9.EQ -- Topic 9 (Power & Refrigeration Cycles) equation registry\n")
    for eq, fn, form, mod, src in REGISTRY:
        print("  Eq %-5s %-31s %-40s [%s | Moran %s]" % (eq, fn, form, mod, src))


if __name__ == "__main__":
    _demo()
