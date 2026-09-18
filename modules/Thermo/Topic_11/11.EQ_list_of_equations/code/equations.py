"""
equations.py  —  Module 11.EQ (Topic 11: canonical equation registry, Psychrometrics)

The key equations of Topic 11 (moist air) in canonical Moran 8e Ch.12 form, one per
function:
  * composition: humidity ratio (12.42/12.43), relative humidity (12.44)
  * energy: mixture enthalpy total / per dry air (12.45/12.46), low-p vapor (12.47)
  * wet-bulb / adiabatic saturation: omega from Tas (12.48), omega' (12.49),
        energy-balance residual (12.50), chart dry-air enthalpy datum (12.51)
  * air-conditioning water mass balance (12.52)

`test_equations.py` checks each value AND imports the concept modules 11.1 (dry_bulb) and
11.2 (wet_bulb), asserting they reproduce these forms (so any formula drift fails it).

Citations: Moran 8e (printed pages; PDF = printed + 18).  Full table in ../refs.md.
"""

# Mv/Ma (water vapor over dry air molecular weights); chart dry-air specific heat
EPS = 0.622          # Moran Eq. 12.43, p.755
CPA = 1.005          # kJ/kg.K, chart datum (Moran Eq. 12.51, p.767)


# --- composition (Moran Sec. 12.5.2) ----------------------------------------
def humidity_ratio(m_vapor, m_dry_air):
    """omega = m_v / m_a  [kg(vap)/kg(dry air)]. [Moran Eq. 12.42, Sec. 12.5.2, p.754]"""
    return m_vapor / m_dry_air


def humidity_ratio_from_pressures(p_v, p):
    """omega = 0.622 pv/(p - pv). [Moran Eq. 12.43, Sec. 12.5.2, p.755]"""
    return EPS * p_v / (p - p_v)


def relative_humidity(p_v, p_g):
    """phi = pv / pg(T)  |_{T,p}. [Moran Eq. 12.44, Sec. 12.5.2, p.755]"""
    return p_v / p_g


def vapor_pressure_from_phi(phi, p_g):
    """Invert Eq. 12.44:  pv = phi * pg(T). [Moran Eq. 12.44, Sec. 12.5.2, p.755]"""
    return phi * p_g


def vapor_pressure_from_ratio(omega, p):
    """Invert Eq. 12.43:  pv = omega p / (0.622 + omega).  Also the dew-point pv.
    [Moran Eq. 12.43, Sec. 12.5.2/12.5.4, p.755/757]"""
    return omega * p / (EPS + omega)


# --- energy (Moran Sec. 12.5.2) ---------------------------------------------
def mixture_enthalpy_total(m_dry_air, h_a, m_vapor, h_v):
    """H = ma*ha + mv*hv  (extensive). [Moran Eq. 12.45, Sec. 12.5.2, p.755]"""
    return m_dry_air * h_a + m_vapor * h_v


def mixture_enthalpy_per_dry_air(h_a, omega, h_v):
    """h = H/ma = ha + omega*hv  (per unit dry air). [Moran Eq. 12.46, Sec. 12.5.2, p.755]"""
    return h_a + omega * h_v


def vapor_enthalpy_approx(h_g_T):
    """hv ~ hg(T)  (low-pressure vapor). [Moran Eq. 12.47, Sec. 12.5.2, p.755]"""
    return h_g_T


# --- wet-bulb / adiabatic saturation (Moran Sec. 12.5.5) --------------------
def humidity_ratio_from_wet_bulb(omega_prime, ha_T, ha_Tas, hf_Tas, hg_Tas, hg_T):
    """omega = [ha(Tas)-ha(T) + omega'(hg(Tas)-hf(Tas))] / [hg(T)-hf(Tas)].
    [Moran Eq. 12.48, Sec. 12.5.5, p.763]"""
    return (ha_Tas - ha_T + omega_prime * (hg_Tas - hf_Tas)) / (hg_T - hf_Tas)


def humidity_ratio_at_saturation(p_g_Tas, p):
    """omega' = 0.622 pg(Tas)/(p - pg(Tas))  (saturated exit). [Moran Eq. 12.49, p.763]"""
    return EPS * p_g_Tas / (p - p_g_Tas)


def adiabatic_saturator_residual(omega, omega_prime, ha_T, ha_Tas, hg_T, hg_Tas, hf_Tas):
    """Residual of the adiabatic-saturator energy balance per unit dry air (Eq. 12.50):
    (ha+omega*hg)_T + (omega'-omega)hf(Tas) - (ha+omega'*hg)_Tas.  Zero at the solution.
    [Moran Eq. 12.50, Sec. 12.5.5, p.764]"""
    lhs = (ha_T + omega * hg_T) + (omega_prime - omega) * hf_Tas
    rhs = ha_Tas + omega_prime * hg_Tas
    return lhs - rhs


def dry_air_enthalpy(T_C, cpa=CPA):
    """Chart dry-air enthalpy (0 at 0 C):  ha = cpa * T(C). [Moran Eq. 12.51, Sec. 12.7, p.767]"""
    return cpa * T_C


# --- air-conditioning water mass balance (Moran Sec. 12.8.1) ----------------
def water_mass_balance(m_dry_air, omega1, omega2):
    """Steady-flow water added (or removed, if < 0):  mw = ma (omega2 - omega1).
    [Moran Eq. 12.52, Sec. 12.8.1, p.768]"""
    return m_dry_air * (omega2 - omega1)


REGISTRY = [
    ("12.42", "humidity_ratio",                "omega = mv/ma",                       "Sec. 12.5.2, p.754"),
    ("12.43", "humidity_ratio_from_pressures", "omega = 0.622 pv/(p-pv)",             "Sec. 12.5.2, p.755"),
    ("12.44", "relative_humidity",             "phi = pv/pg(T)",                      "Sec. 12.5.2, p.755"),
    ("12.43i","vapor_pressure_from_ratio",     "pv = omega p/(0.622+omega)",          "Sec. 12.5.2, p.755"),
    ("12.44i","vapor_pressure_from_phi",       "pv = phi pg",                         "Sec. 12.5.2, p.755"),
    ("12.45", "mixture_enthalpy_total",        "H = ma ha + mv hv",                   "Sec. 12.5.2, p.755"),
    ("12.46", "mixture_enthalpy_per_dry_air",  "h = ha + omega hv",                   "Sec. 12.5.2, p.755"),
    ("12.47", "vapor_enthalpy_approx",         "hv ~ hg(T)",                          "Sec. 12.5.2, p.755"),
    ("12.48", "humidity_ratio_from_wet_bulb",  "omega from Tas (~Twb)",               "Sec. 12.5.5, p.763"),
    ("12.49", "humidity_ratio_at_saturation",  "omega' = 0.622 pg(Tas)/(p-pg(Tas))",  "Sec. 12.5.5, p.763"),
    ("12.50", "adiabatic_saturator_residual",  "energy balance residual = 0",         "Sec. 12.5.5, p.764"),
    ("12.51", "dry_air_enthalpy",              "ha = cpa T(C)",                       "Sec. 12.7, p.767"),
    ("12.52", "water_mass_balance",            "mw = ma(omega2-omega1)",              "Sec. 12.8.1, p.768"),
]


def _demo():
    print("Module 11.EQ -- Topic 11 (Psychrometrics) equation registry\n")
    for eq, fn, form, src in REGISTRY:
        print(f"  Eq {eq:<7} {fn:<30} {form:<36} [Moran {src}]")


if __name__ == "__main__":
    _demo()
