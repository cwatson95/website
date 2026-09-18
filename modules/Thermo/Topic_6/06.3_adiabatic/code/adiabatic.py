"""
adiabatic.py  —  Module 6.3 (Adiabatic & Isentropic Processes)

An ADIABATIC process has no heat transfer, Q = 0.  An adiabatic process that is also
INTERNALLY REVERSIBLE has constant entropy -- it is ISENTROPIC (Moran 8e Sec. 6.6).  This
module collects the isentropic relations for an ideal gas (Sec. 6.11) plus the ideal-gas
entropy-change relations they specialize (Sec. 6.5), and the isentropic-efficiency
definitions that bridge to real (adiabatic but irreversible) devices (Sec. 6.12).

Ideal-gas entropy change (Sec. 6.5):
    s2 - s1 = s0(T2) - s0(T1) - R ln(p2/p1)                 (Eq. 6.20a, tables)
    s2 - s1 = cp ln(T2/T1)    - R ln(p2/p1)                 (Eq. 6.22, constant cp)

Setting s2 = s1 gives the ISENTROPIC relations of an ideal gas (Sec. 6.11):
    air tables:  p2/p1 = pr(T2)/pr(T1)                      (Eq. 6.41)
                 v2/v1 = vr(T2)/vr(T1)                      (Eq. 6.42)
    constant k:  T2/T1 = (p2/p1)^((k-1)/k)                  (Eq. 6.43)
                 T2/T1 = (v1/v2)^(k-1)                      (Eq. 6.44)
                 p2/p1 = (v1/v2)^k   <=>  p v^k = constant  (Eq. 6.45)
with cp = kR/(k-1),  cv = R/(k-1)  (Eq. 3.47), k = cp/cv the specific heat ratio.  The
p v^k = const "cold-air-standard" model is the constant-k isentropic of an ideal gas.

Isentropic efficiency (Sec. 6.12) compares an actual ADIABATIC device to an isentropic one
between the same inlet state and the same exit pressure:
    turbine:  eta_t = (h1 - h2)/(h1 - h2s)                  (Eq. 6.46)
    nozzle:   eta_n = (V2^2/2)/(V2^2/2)_s                   (Eq. 6.47)

Units: T [K or degR]; p [any consistent]; v [m^3/kg]; R, cp, cv, s [kJ/kg.K]; h [kJ/kg].
Citations: Moran 8e (PDF = printed + 18).  Worked Examples 6.9 (isentropic air,
p2=15.28 atm), 6.10 (air leaking from a tank), 6.11/6.12 (isentropic efficiency).
"""
import math


def is_adiabatic(Q, tol=1e-9):
    """Adiabatic test: True iff there is no heat transfer (Q ~ 0).
    [Moran Sec. 6.6, p.302]"""
    return abs(Q) <= tol


# --- ideal-gas entropy change (Sec. 6.5) ------------------------------------
def delta_s_ideal_gas_so(so2, so1, R, p2, p1):
    """Ideal-gas specific entropy change using s0(T) tables:
    s2 - s1 = s0(T2) - s0(T1) - R ln(p2/p1).  [Moran Eq. 6.20a, Sec. 6.5.1, p.300]"""
    return (so2 - so1) - R * math.log(p2 / p1)


def delta_s_ideal_gas_cp(cp, T2, T1, R, p2, p1):
    """Ideal-gas specific entropy change, constant cp:
    s2 - s1 = cp ln(T2/T1) - R ln(p2/p1).  T absolute.  [Moran Eq. 6.22, Sec. 6.5.2, p.301]"""
    return cp * math.log(T2 / T1) - R * math.log(p2 / p1)


# --- specific heats from k (Eq. 3.47) ---------------------------------------
def cp_from_k(k, R):
    """cp = k R/(k-1).  [Moran Eq. 3.47, Sec. 6.11.2, p.328]"""
    return k * R / (k - 1.0)


def cv_from_k(k, R):
    """cv = R/(k-1).  [Moran Eq. 3.47, Sec. 6.11.2, p.328]"""
    return R / (k - 1.0)


# --- isentropic, constant specific heat ratio k (Sec. 6.11.2) ---------------
def temp_ratio_from_pressure(p2, p1, k):
    """Isentropic ideal gas, constant k:  T2/T1 = (p2/p1)^((k-1)/k).
    [Moran Eq. 6.43, Sec. 6.11.2, p.328]"""
    return (p2 / p1) ** ((k - 1.0) / k)


def final_temp_isentropic(T1, p2, p1, k):
    """Final temperature of an isentropic ideal-gas process (constant k):
    T2 = T1 (p2/p1)^((k-1)/k).  [Moran Eq. 6.43, Sec. 6.11.2, p.328]"""
    return T1 * temp_ratio_from_pressure(p2, p1, k)


def temp_ratio_from_volume(v1, v2, k):
    """Isentropic ideal gas, constant k:  T2/T1 = (v1/v2)^(k-1).
    [Moran Eq. 6.44, Sec. 6.11.2, p.328]"""
    return (v1 / v2) ** (k - 1.0)


def pressure_ratio_from_volume(v1, v2, k):
    """Isentropic ideal gas, constant k:  p2/p1 = (v1/v2)^k  (i.e. p v^k = constant).
    [Moran Eq. 6.45, Sec. 6.11.2, p.328]"""
    return (v1 / v2) ** k


def final_pressure_isentropic(T1, T2, p1, k):
    """Final pressure of an isentropic ideal-gas process (constant k), from Eq. 6.43:
    p2 = p1 (T2/T1)^(k/(k-1)).  [Moran Eq. 6.43, Sec. 6.11.2, p.330 (Ex. 6.9c)]"""
    return p1 * (T2 / T1) ** (k / (k - 1.0))


# --- isentropic, air ideal-gas tables (Sec. 6.11.2) -------------------------
def p2_from_pr(p1, pr1, pr2):
    """Isentropic air via relative pressure:  p2 = p1 (pr2/pr1).
    [Moran Eq. 6.41, Sec. 6.11.2, p.327]"""
    return p1 * pr2 / pr1


def v2_from_vr(v1, vr1, vr2):
    """Isentropic air via relative volume:  v2 = v1 (vr2/vr1).
    [Moran Eq. 6.42, Sec. 6.11.2, p.328]"""
    return v1 * vr2 / vr1


def pr2_isentropic(pr1, p2, p1):
    """Relative pressure at the isentropic end state:  pr2 = (p2/p1) pr1  (from Eq. 6.41).
    [Moran Eq. 6.41, Sec. 6.11.2, p.331 (Ex. 6.10)]"""
    return pr1 * (p2 / p1)


# --- isentropic efficiencies (Sec. 6.12) ------------------------------------
def isentropic_turbine_eff(h1, h2, h2s):
    """Isentropic turbine efficiency:  eta_t = (h1 - h2)/(h1 - h2s)  (same inlet state,
    same exit pressure).  [Moran Eq. 6.46, Sec. 6.12.1, p.333]"""
    return (h1 - h2) / (h1 - h2s)


def isentropic_nozzle_eff(ke2, ke2s):
    """Isentropic nozzle efficiency:  eta_n = (V2^2/2)/(V2^2/2)_s  (actual vs isentropic
    exit kinetic energy).  [Moran Eq. 6.47, Sec. 6.12.2, p.335]"""
    return ke2 / ke2s


def _demo():
    print("Module 6.3 -- Adiabatic & Isentropic Processes  (Q=0; adiabatic int rev => isentropic)\n")
    # Example 6.9: air isentropic from p1=1 atm, T1=540 R to T2=1160 R.  Find p2.
    p2_pr = p2_from_pr(1.0, 1.3860, 21.18)             # (a) pr data, Table A-22E
    p2_k = final_pressure_isentropic(540.0, 1160.0, 1.0, 1.39)   # (c) constant k=1.39 @ 850 R
    print("  Ex 6.9 air isentropic: p2 = %.2f atm (pr)   [book 15.28]" % p2_pr)
    print("                          p2 = %.2f atm (k=1.39) [book 15.26]" % p2_k)
    # p v^k = const sanity: T2/T1 from p-ratio and from v-ratio agree (Eqs 6.43-6.45)
    k = 1.4
    tr_p = temp_ratio_from_pressure(8.0, 1.0, k)
    print("  cold-air k=1.4: T2/T1=(8)^((k-1)/k)=%.4f ; cp=%.4f, cv=%.4f kJ/kg.K"
          % (tr_p, cp_from_k(k, 0.287), cv_from_k(k, 0.287)))
    # Example 6.10: air leaking from a tank, 5 bar 500 K -> 1 bar (isentropic per remaining mass)
    pr2 = pr2_isentropic(8.411, 1.0, 5.0)              # pr1=8.411 @ 500 K -> pr2=1.6822 -> T2=317 K
    T2 = 317.0
    m2 = (1.0 / 5.0) * (500.0 / T2) * 5.0
    print("  Ex 6.10 air leak: pr2 = %.4f [book 1.6822] -> T2=317 K ; m2 = %.2f kg [book 1.58]"
          % (pr2, m2))
    # Example 6.11/6.12: isentropic efficiency
    print("  Ex 6.11 steam turbine: W/m = 0.75*(3105.6-2743.0) = %.2f kJ/kg [book 271.95]"
          % (0.75 * (3105.6 - 2743.0)))
    print("  Ex 6.12 air turbine: eta_t = 74/(390.88-285.27) = %.2f [book 0.70]"
          % isentropic_turbine_eff(390.88, 390.88 - 74.0, 285.27))


if __name__ == "__main__":
    _demo()
