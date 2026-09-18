"""
equations.py  —  Module 3.EQ (Topic 3: canonical equation registry for "The Laws")

The key equations of Topic 3 in canonical Moran 8e form, one per function:
  * zeroth law  -- temperature scales        (Eqs. 1.16-1.19, Sec. 1.7)
  * first law   -- energy balance & cycles   (Eqs. 2.35, 2.41, Sec. 2.5-2.6)
  * second law  -- Carnot efficiency & COPs  (Eqs. 5.4, 5.7, 5.9-5.11, Sec. 5.4-5.9)
  * third law   -- absolute-entropy datum    (Sec. 13.5)

`test_equations.py` checks each value AND imports the concept modules 3.1-3.4,
asserting they reproduce these forms (so any formula drift fails the test).

Citations: Moran 8e (printed pages; PDF = printed + 18); full table in ../refs.md.
"""


# --- zeroth law: temperature scales (Sec. 1.7) ------------------------------
def rankine_from_kelvin(T_K):
    """T_R = 1.8 T_K. [Eq. 1.16, p.21]"""
    return 1.8 * T_K


def celsius_from_kelvin(T_K):
    """T_C = T_K - 273.15. [Eq. 1.17, p.22]"""
    return T_K - 273.15


def fahrenheit_from_celsius(T_C):
    """T_F = 1.8 T_C + 32. [Eq. 1.19, p.22]"""
    return 1.8 * T_C + 32.0


# --- first law: energy balance & cycles (Sec. 2.5-2.6) ----------------------
def delta_E(Q, W):
    """E2 - E1 = Q - W. [Eq. 2.35a, p.61]"""
    return Q - W


def power_cycle_work(Q_in, Q_out):
    """W_cycle = Q_in - Q_out. [Eq. 2.41, p.73]"""
    return Q_in - Q_out


# --- second law: Carnot efficiency & COPs (Sec. 5.4-5.9) --------------------
def efficiency_from_heat(Q_C, Q_H):
    """eta = 1 - Q_C/Q_H. [Eq. 5.4, p.256]"""
    return 1.0 - Q_C / Q_H


def kelvin_ratio(T_C, T_H):
    """(Q_C/Q_H)_rev = T_C/T_H. [Eq. 5.7, p.262]"""
    return T_C / T_H


def carnot_efficiency(T_C, T_H):
    """eta_max = 1 - T_C/T_H. [Eq. 5.9, p.265]"""
    return 1.0 - T_C / T_H


def carnot_cop_refrigerator(T_C, T_H):
    """beta_max = T_C/(T_H - T_C). [Eq. 5.10, p.267]"""
    return T_C / (T_H - T_C)


def carnot_cop_heat_pump(T_C, T_H):
    """gamma_max = T_H/(T_H - T_C). [Eq. 5.11, p.267]"""
    return T_H / (T_H - T_C)


# --- third law: absolute-entropy datum (Sec. 13.5) --------------------------
def standard_entropy_at_zero(pure_crystalline=True):
    """S(0 K) = 0 for a pure crystal; None otherwise. [Sec. 13.5.1, p.837]"""
    return 0.0 if pure_crystalline else None


def absolute_entropy_debye(T, a):
    """S(T) = a T^3 / 3 for c_p = a T^3. [Sec. 13.5; Debye low-T limit]"""
    return a * T ** 3 / 3.0


REGISTRY = [
    ("1.16", "rankine_from_kelvin",      "T_R = 1.8 T_K",          "0th", "Sec. 1.7.2, p.21"),
    ("1.17", "celsius_from_kelvin",      "T_C = T_K - 273.15",     "0th", "Sec. 1.7.3, p.22"),
    ("1.19", "fahrenheit_from_celsius",  "T_F = 1.8 T_C + 32",     "0th", "Sec. 1.7.3, p.22"),
    ("2.35a","delta_E",                  "E2-E1 = Q - W",          "1st", "Sec. 2.5, p.61"),
    ("2.41", "power_cycle_work",         "W_cyc = Q_in - Q_out",   "1st", "Sec. 2.6, p.73"),
    ("5.4",  "efficiency_from_heat",     "eta = 1 - Q_C/Q_H",      "2nd", "Sec. 5.4, p.256"),
    ("5.7",  "kelvin_ratio",             "(Q_C/Q_H)rev = T_C/T_H", "2nd", "Sec. 5.7, p.262"),
    ("5.9",  "carnot_efficiency",        "eta_max = 1 - T_C/T_H",  "2nd", "Sec. 5.9.1, p.265"),
    ("5.10", "carnot_cop_refrigerator",  "beta = T_C/(T_H-T_C)",   "2nd", "Sec. 5.9.2, p.267"),
    ("5.11", "carnot_cop_heat_pump",     "gamma = T_H/(T_H-T_C)",  "2nd", "Sec. 5.9.2, p.267"),
    ("13.5", "standard_entropy_at_zero", "S(0) = 0 (pure crystal)","3rd", "Sec. 13.5.1, p.837"),
    ("13.5", "absolute_entropy_debye",   "S = a T^3 / 3",          "3rd", "Sec. 13.5, p.837"),
]


def _demo():
    print("Module 3.EQ -- Topic 3 (The Laws) equation registry\n")
    for eq, fn, form, law, src in REGISTRY:
        print(f"  [{law}] Eq {eq:<6} {fn:<26} {form:<26} [Moran {src}]")


if __name__ == "__main__":
    _demo()
