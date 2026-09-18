"""
equations.py  —  Module 8.EQ (Topic 8: canonical equation registry, Components & Devices)

The key equations of Topic 8 in canonical Moran 8e form, one per function:
  * mass flow forms      mdot = A V / v ; ideal-gas A V p/(R T)     (Eq. 4.4b)
  * steady CV balance    one-inlet/one-exit energy rate balance      (Eq. 4.20a)
  * device forms         compressor power, single-stream heat rate,
                         two-stream (heat-exchanger) balance         (Secs. 4.8, 4.9; Eq. 4.18)
  * isentropic compressor efficiency  eta_c = (h2s-h1)/(h2-h1)      (Eq. 6.48)
  * vapor-compression cycle  Qin/mdot, Wc/mdot, Qout/mdot, h4=h3,
                         beta, gamma, Q_H = Q_C + W, Carnot limits   (Eqs. 10.1, 10.3-10.10)

test_equations.py checks each value AND imports the four concept modules 08.1-08.4
(compressor.py, condenser.py, heat_exchanger.py, heat_pump.py), asserting they
reproduce these forms.  Citations: Moran 8e (PDF = printed + 18).

Units: power_cv is STRICT SI (h [J/kg], V [m/s], z [m], Qdot [W] -> Wdot [W]); the
enthalpy-difference forms accept any consistent energy unit (kJ/kg is fine); Carnot
limits need ABSOLUTE temperature (K or degR).
"""


# --- mass flow (Ch.4 Sec. 4.2.1) ---------------------------------------------
def mass_flow_rate(A, V, v):
    """mdot = A V / v  (one-dimensional flow). [Eq. 4.4b, Sec. 4.2.1, p.172]"""
    return A * V / v


def mass_flow_rate_ideal_gas(A, V, p, R, T):
    """mdot = A V p / (R T)  (Eq. 4.4b with ideal-gas v = RT/p; R specific).
    [Eq. 4.4b + ideal gas, Ex. 4.5, p.191]"""
    return A * V * p / (R * T)


# --- steady CV energy balance & device forms (Ch.4 Secs. 4.5, 4.8, 4.9) ------
def power_cv(mdot, h1, h2, Qdot=0.0, V1=0.0, V2=0.0, g=9.81, z1=0.0, z2=0.0):
    """One-inlet/one-exit steady CV energy balance solved for the power:
        Wdot_cv = Qdot_cv + mdot[(h1 - h2) + (V1^2 - V2^2)/2 + g(z1 - z2)].
    STRICT SI (h in J/kg -> Wdot in W).  Negative for a compressor/pump.
    [Eq. 4.20a, Sec. 4.5.1, p.181]"""
    return Qdot + mdot * ((h1 - h2) + (V1 * V1 - V2 * V2) / 2.0 + g * (z1 - z2))


def compressor_power(mdot, h1, h2):
    """Compressor/pump specialization (adiabatic, dKE = dPE = 0):
    Wdot_cv = mdot (h1 - h2)  (< 0; the power INPUT is -Wdot_cv).
    [Sec. 4.8.1 form (b) of Eq. 4.20a, p.190]"""
    return mdot * (h1 - h2)


def single_stream_heat_rate(mdot, h_in, h_out):
    """Condenser / one side of a heat exchanger (Wdot_cv = 0, dKE = dPE = 0):
    Qdot_cv = mdot (h_out - h_in)  (< 0 when the stream rejects heat).
    [from Eq. 4.20a; Ex. 4.7(b), p.198]"""
    return mdot * (h_out - h_in)


def two_stream_balance_residual(mdot_h, h_hi, h_ho, mdot_c, h_ci, h_co):
    """Whole-exchanger steady balance (Qdot_cv = Wdot_cv = 0, dKE = dPE = 0):
        0 = mdot_h (h_hi - h_ho) + mdot_c (h_ci - h_co).
    Returns the residual (~0 at a consistent solution).
    [from Eq. 4.18, Sec. 4.5.1, p.181; applied in Ex. 4.7(a), p.197]"""
    return mdot_h * (h_hi - h_ho) + mdot_c * (h_ci - h_co)


def mass_flow_ratio_cold_to_hot(h_hi, h_ho, h_ci, h_co):
    """Adiabatic two-stream exchanger:  mdot_c/mdot_h = (h_hi - h_ho)/(h_co - h_ci).
    [Eq. 4.18 rearranged; Ex. 4.7(a), p.197]"""
    return (h_hi - h_ho) / (h_co - h_ci)


# --- isentropic compressor efficiency (Ch.6 Sec. 6.12.3) ---------------------
def isentropic_compressor_efficiency(h1, h2, h2s):
    """eta_c = (-Wdot/mdot)_s / (-Wdot/mdot) = (h2s - h1)/(h2 - h1)
    (same inlet state and exit pressure; typically 0.75-0.85).
    [Eq. 6.48, Sec. 6.12.3, p.338]"""
    return (h2s - h1) / (h2 - h1)


# --- vapor-compression cycle relations (Ch.10) -------------------------------
def refrigeration_capacity_per_mass(h1, h4):
    """Evaporator (refrigeration capacity per unit mass)  Qdot_in/mdot = h1 - h4.
    [Eq. 10.3, Sec. 10.2.1, p.612]"""
    return h1 - h4


def vc_compressor_work_per_mass(h1, h2):
    """Cycle compressor work per unit mass  Wdot_c/mdot = h2 - h1  (input, positive).
    [Eq. 10.4, Sec. 10.2.1, p.613]"""
    return h2 - h1


def vc_condenser_heat_per_mass(h2, h3):
    """Cycle condenser heat rejected per unit mass  Qdot_out/mdot = h2 - h3.
    [Eq. 10.5, Sec. 10.2.1, p.613]"""
    return h2 - h3


def throttling_exit_enthalpy(h3):
    """Expansion-valve (throttling) model:  h4 = h3.
    [Eq. 10.6, Sec. 10.2.1, p.613]"""
    return h3


def cop_refrigeration_vc(h1, h2, h4):
    """Vapor-compression refrigerator COP  beta = (h1 - h4)/(h2 - h1).
    [Eq. 10.7, Sec. 10.2.1, p.613]"""
    return (h1 - h4) / (h2 - h1)


def heat_pump_first_law(Q_in, W_net):
    """Cycle first law  Qdot_out = Qdot_in + Wdot_net  (heat delivered to warm region).
    [Eq. 10.8, Sec. 10.6.1, p.629]"""
    return Q_in + W_net


def carnot_cop_refrigeration(T_H, T_C):
    """Maximum (Carnot) refrigerator COP  beta_max = T_C/(T_H - T_C)  (T in kelvin).
    [Eq. 10.1, Sec. 10.1.1, p.611]"""
    return T_C / (T_H - T_C)


def carnot_cop_heat_pump(T_H, T_C):
    """Maximum (Carnot) heat-pump COP  gamma_max = T_H/(T_H - T_C)  (T in kelvin).
    [Eq. 10.9, Sec. 10.6.1, p.629]"""
    return T_H / (T_H - T_C)


def cop_heat_pump_vc(h1, h2, h3):
    """Vapor-compression heat-pump COP  gamma = (h2 - h3)/(h2 - h1)  (never < 1).
    [Eq. 10.10, Sec. 10.6.2, p.630]"""
    return (h2 - h3) / (h2 - h1)


REGISTRY = [
    ("4.4b",  "mass_flow_rate",                  "mdot = A V / v",                "08.1", "Sec. 4.2.1, p.172"),
    ("4.4b",  "mass_flow_rate_ideal_gas",        "mdot = A V p/(R T)",            "08.1", "Ex. 4.5, p.191"),
    ("4.20a", "power_cv",                        "Wdot = Qdot + mdot[dh+dKE+dPE]","08.1", "Sec. 4.5.1, p.181"),
    ("4.20a", "compressor_power",                "Wdot_cv = mdot(h1-h2)",         "08.1", "Sec. 4.8.1, p.190"),
    ("4.20a", "single_stream_heat_rate",         "Qdot_cv = mdot(h_out-h_in)",    "08.2", "Ex. 4.7(b), p.198"),
    ("4.18",  "two_stream_balance_residual",     "0 = mh*dh_h + mc*dh_c",         "08.3", "Sec. 4.5.1, p.181"),
    ("4.18",  "mass_flow_ratio_cold_to_hot",     "mc/mh=(h_hi-h_ho)/(h_co-h_ci)", "08.3", "Ex. 4.7(a), p.197"),
    ("6.48",  "isentropic_compressor_efficiency","eta_c=(h2s-h1)/(h2-h1)",        "08.1", "Sec. 6.12.3, p.338"),
    ("10.3",  "refrigeration_capacity_per_mass", "Qin/mdot = h1-h4",              "08.4", "Sec. 10.2.1, p.612"),
    ("10.4",  "vc_compressor_work_per_mass",     "Wc/mdot = h2-h1",               "08.1", "Sec. 10.2.1, p.613"),
    ("10.5",  "vc_condenser_heat_per_mass",      "Qout/mdot = h2-h3",             "08.2", "Sec. 10.2.1, p.613"),
    ("10.6",  "throttling_exit_enthalpy",        "h4 = h3",                       "08.4", "Sec. 10.2.1, p.613"),
    ("10.7",  "cop_refrigeration_vc",            "beta=(h1-h4)/(h2-h1)",          "08.4", "Sec. 10.2.1, p.613"),
    ("10.8",  "heat_pump_first_law",             "Q_H = Q_C + W_net",             "08.4", "Sec. 10.6.1, p.629"),
    ("10.1",  "carnot_cop_refrigeration",        "beta_max = T_C/(T_H-T_C)",      "08.4", "Sec. 10.1.1, p.611"),
    ("10.9",  "carnot_cop_heat_pump",            "gamma_max= T_H/(T_H-T_C)",      "08.4", "Sec. 10.6.1, p.629"),
    ("10.10", "cop_heat_pump_vc",                "gamma=(h2-h3)/(h2-h1)",         "08.4", "Sec. 10.6.2, p.630"),
]


def _demo():
    print("Module 8.EQ -- Topic 8 (Components & Devices) equation registry\n")
    for eq, fn, form, mod, src in REGISTRY:
        print("  Eq %-6s %-33s %-31s [%s | Moran %s]" % (eq, fn, form, mod, src))


if __name__ == "__main__":
    _demo()
