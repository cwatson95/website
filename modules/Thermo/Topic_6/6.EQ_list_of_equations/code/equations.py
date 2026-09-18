"""
equations.py  —  Module 6.EQ (Topic 6: canonical equation registry, "Processes & Idealizations")

The key equations of Topic 6 in canonical Moran 8e form, one per function:
  * 6.1 reversible   -- Q_int rev = INT T dS, dS = dQ/T          (Eqs. 6.23, 6.2b, Sec. 6.6)
  * 6.2 irreversible -- entropy balance, increase principle      (Eqs. 6.24, 6.30, 6.13, Sec. 6.7-6.8)
  * 6.3 adiabatic    -- isentropic ideal-gas relations, eta      (Eqs. 6.43, 6.45, 6.46, 3.47, Sec. 6.11-6.12)
  * 6.4 steady state -- steady-state energy rate balance         (Eq. 4.20a, Sec. 4.5)
  * 6.5 mass         -- mass flow rate, steady mass balance      (Eqs. 4.4b, 4.6, Sec. 4.1-4.2)

`test_equations.py` checks each value AND imports the concept modules 6.1-6.5, asserting
they reproduce these forms (so any formula drift fails the test).

Citations: Moran 8e (printed pages; PDF = printed + 18); full table in ../refs.md.
"""
import math


# --- 6.1 reversible / internally reversible (Sec. 6.6) ----------------------
def heat_int_rev_isothermal(T, s2, s1):
    """Q = INT T dS = T(s2 - s1), isothermal internally reversible. [Eq. 6.23, p.302]"""
    return T * (s2 - s1)


def entropy_change_int_rev(Q, T):
    """dS = (dQ/T)_int rev -> Q/T. [Eq. 6.2b, p.302]"""
    return Q / T


# --- 6.2 irreversible / entropy production (Sec. 6.7-6.8) -------------------
def entropy_production(dS, entropy_transfer):
    """sigma = (S2 - S1) - INT(dQ/T)_b. [Eq. 6.24, p.305]"""
    return dS - entropy_transfer


def sigma_isolated(dS_system, dS_surr):
    """sigma_isol = dS_system + dS_surr (increase of entropy principle). [Eq. 6.30b, p.313]"""
    return dS_system + dS_surr


def entropy_change_incompressible(m, c, T2, T1):
    """DeltaS = m c ln(T2/T1), incompressible, constant c. [Eq. 6.13, p.298]"""
    return m * c * math.log(T2 / T1)


# --- 6.3 adiabatic / isentropic (Sec. 6.11-6.12) ---------------------------
def final_temp_isentropic(T1, p2, p1, k):
    """T2 = T1 (p2/p1)^((k-1)/k), isentropic ideal gas, constant k. [Eq. 6.43, p.328]"""
    return T1 * (p2 / p1) ** ((k - 1.0) / k)


def pressure_ratio_from_volume(v1, v2, k):
    """p2/p1 = (v1/v2)^k  (p v^k = const), isentropic ideal gas. [Eq. 6.45, p.328]"""
    return (v1 / v2) ** k


def isentropic_turbine_eff(h1, h2, h2s):
    """eta_t = (h1 - h2)/(h1 - h2s). [Eq. 6.46, p.333]"""
    return (h1 - h2) / (h1 - h2s)


def cp_from_k(k, R):
    """cp = k R/(k-1). [Eq. 3.47, p.328]"""
    return k * R / (k - 1.0)


def cv_from_k(k, R):
    """cv = R/(k-1). [Eq. 3.47, p.328]"""
    return R / (k - 1.0)


# --- 6.4 steady-state energy rate balance (Sec. 4.5) -----------------------
def heat_rate_steady(Wdot_cv, mdot, h1, h2, V1=0.0, V2=0.0, z1=0.0, z2=0.0, g=9.81):
    """Qdot_cv = Wdot_cv + mdot[(h2-h1) + (V2^2-V1^2)/2 + g(z2-z1)]. [Eq. 4.20a, p.181]"""
    dke = (V2 ** 2 - V1 ** 2) / 2.0 / 1000.0
    dpe = g * (z2 - z1) / 1000.0
    return Wdot_cv + mdot * ((h2 - h1) + dke + dpe)


# --- 6.5 conservation of mass (Sec. 4.1-4.2) -------------------------------
def mass_flow_rate(A, V, v):
    """mdot = A V / v. [Eq. 4.4b, p.172]"""
    return A * V / v


def steady_mass_residual(mdot_in, mdot_out):
    """sum(mdot_i) - sum(mdot_e) (= 0 at steady state). [Eq. 4.6, p.173]"""
    si = sum(mdot_in) if hasattr(mdot_in, "__iter__") else mdot_in
    se = sum(mdot_out) if hasattr(mdot_out, "__iter__") else mdot_out
    return si - se


REGISTRY = [
    ("6.23", "heat_int_rev_isothermal",   "Q = INT T dS = T(s2-s1)",     "6.1", "Sec. 6.6.1, p.302"),
    ("6.2b", "entropy_change_int_rev",     "dS = (dQ/T)_int rev",         "6.1", "Sec. 6.6, p.302"),
    ("6.24", "entropy_production",         "sigma = dS - INT(dQ/T)_b",    "6.2", "Sec. 6.7, p.305"),
    ("6.30", "sigma_isolated",             "sigma_isol = dS_sys + dS_sur","6.2", "Sec. 6.8.1, p.313"),
    ("6.13", "entropy_change_incompr.",    "dS = m c ln(T2/T1)",          "6.2", "Sec. 6.4, p.298"),
    ("6.43", "final_temp_isentropic",      "T2/T1 = (p2/p1)^((k-1)/k)",   "6.3", "Sec. 6.11.2, p.328"),
    ("6.45", "pressure_ratio_from_volume", "p2/p1 = (v1/v2)^k (pv^k=C)",  "6.3", "Sec. 6.11.2, p.328"),
    ("6.46", "isentropic_turbine_eff",     "eta_t = (h1-h2)/(h1-h2s)",    "6.3", "Sec. 6.12.1, p.333"),
    ("3.47", "cp_from_k / cv_from_k",      "cp=kR/(k-1), cv=R/(k-1)",     "6.3", "Sec. 6.11.2, p.328"),
    ("4.20a","heat_rate_steady",           "0=Qdot-Wdot+mdot[dh+dke+dpe]","6.4", "Sec. 4.5.1, p.181"),
    ("4.4b", "mass_flow_rate",             "mdot = A V / v",              "6.5", "Sec. 4.2.1, p.172"),
    ("4.6",  "steady_mass_residual",       "sum(mdot_i) = sum(mdot_e)",   "6.5", "Sec. 4.2.2, p.173"),
]


def _demo():
    print("Module 6.EQ -- Topic 6 (Processes & Idealizations) equation registry\n")
    for eq, fn, form, mod, src in REGISTRY:
        print(f"  [{mod}] Eq {eq:<6} {fn:<26} {form:<30} [Moran {src}]")


if __name__ == "__main__":
    _demo()
