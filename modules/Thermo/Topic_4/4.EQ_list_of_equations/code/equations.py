"""
equations.py  —  Module 4.EQ (Topic 4: canonical equation registry, Properties & State Functions)

The key equations of Topic 4 in canonical Moran 8e form, one per function:
  * enthalpy            h = u + p v                 (Eq. 3.4)
  * quality / mixtures  x; y = yf + x(yg - yf)      (Eqs. 3.1, 3.2/3.6/3.7/6.4)
  * entropy             Ds(incompressible, ideal gas); entropy balance (Eqs. 6.13, 6.22, 6.24)
  * exergy              e; Eq; Ed = T0 sigma         (Eqs. 7.2, 7.5, 7.7)
  * Gibbs phase rule    F = 2 + N - P                (Eq. 14.68)

test_equations.py checks each value AND imports the concept modules 4.1-4.5,
asserting they reproduce these forms.  Citations: Moran 8e (PDF = printed + 18).
"""
import math


# --- enthalpy (Sec. 3.6) ----------------------------------------------------
def enthalpy(u, p, v):
    """h = u + p v. [Eq. 3.4, p.111]"""
    return u + p * v


def enthalpy_total(U, p, V):
    """H = U + p V. [Eq. 3.3, p.111]"""
    return U + p * V


# --- quality & mixtures (Sec. 3.3-3.6) --------------------------------------
def quality(m_vapor, m_total):
    """x = m_vapor / m_total. [Eq. 3.1, p.102]"""
    return m_vapor / m_total


def mixture_property(yf, yg, x):
    """y = yf + x (yg - yf)  (v, u, h, s). [Eqs. 3.2/3.6/3.7/6.4]"""
    return yf + x * (yg - yf)


# --- entropy (Ch.6) ---------------------------------------------------------
def entropy_change_incompressible(c, T1, T2):
    """Ds = c ln(T2/T1). [Eq. 6.13, p.298]"""
    return c * math.log(T2 / T1)


def entropy_change_ideal_gas_cp(cp, R, T1, T2, p1, p2):
    """Ds = cp ln(T2/T1) - R ln(p2/p1). [Eq. 6.22, p.301]"""
    return cp * math.log(T2 / T1) - R * math.log(p2 / p1)


def entropy_production_closed(S2, S1, Q_over_Tb=0.0):
    """sigma = (S2 - S1) - integral(dQ/Tb). [Eq. 6.24, p.305]"""
    return (S2 - S1) - Q_over_Tb


# --- exergy (Ch.7) ----------------------------------------------------------
def specific_exergy(u, v, s, u0, v0, s0, T0, p0):
    """e = (u-u0) + p0(v-v0) - T0(s-s0). [Eq. 7.2, p.376]"""
    return (u - u0) + p0 * (v - v0) - T0 * (s - s0)


def exergy_transfer_heat(Q, T0, Tb):
    """Eq = (1 - T0/Tb) Q. [Eq. 7.5, p.380]"""
    return (1.0 - T0 / Tb) * Q


def exergy_destruction(T0, sigma):
    """Ed = T0 sigma. [Eq. 7.7, p.380]"""
    return T0 * sigma


# --- Gibbs phase rule (Ch.14) -----------------------------------------------
def gibbs_phase_rule(N, P):
    """F = 2 + N - P. [Eq. 14.68, p.913]"""
    return 2 + N - P


REGISTRY = [
    ("3.4",   "enthalpy",                    "h = u + p v",            "4.1", "Sec. 3.6.1, p.111"),
    ("3.3",   "enthalpy_total",              "H = U + p V",            "4.1", "Sec. 3.6.1, p.111"),
    ("3.1",   "quality",                     "x = m_vap/m_tot",        "4.4", "Sec. 3.3, p.102"),
    ("3.2",   "mixture_property",            "y = yf + x*yfg",         "4.4", "Sec. 3.5.2, p.108"),
    ("6.13",  "entropy_change_incompressible","Ds = c ln(T2/T1)",      "4.2", "Sec. 6.4, p.298"),
    ("6.22",  "entropy_change_ideal_gas_cp", "Ds = cp lnT - R lnp",    "4.2", "Sec. 6.5.2, p.301"),
    ("6.24",  "entropy_production_closed",   "sigma = dS - QdQ/Tb",    "4.2", "Sec. 6.7, p.305"),
    ("7.2",   "specific_exergy",             "e=(u-u0)+p0(v-v0)-T0(s-s0)","4.3","Sec. 7.3.2, p.376"),
    ("7.5",   "exergy_transfer_heat",        "Eq = (1-T0/Tb) Q",       "4.3", "Sec. 7.4.1, p.380"),
    ("7.7",   "exergy_destruction",          "Ed = T0 sigma",          "4.3", "Sec. 7.4.1, p.380"),
    ("14.68", "gibbs_phase_rule",            "F = 2 + N - P",          "4.5", "Sec. 14.6.2, p.913"),
]


def _demo():
    print("Module 4.EQ -- Topic 4 (Properties & State Functions) equation registry\n")
    for eq, fn, form, mod, src in REGISTRY:
        print("  Eq %-6s %-30s %-28s [%s | Moran %s]" % (eq, fn, form, mod, src))


if __name__ == "__main__":
    _demo()
