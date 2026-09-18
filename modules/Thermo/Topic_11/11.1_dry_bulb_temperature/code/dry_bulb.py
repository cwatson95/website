"""
dry_bulb.py  —  Module 11.1 (Dry-bulb temperature & the moist-air model)

The dry-bulb temperature is simply the temperature an ordinary thermometer reads
when placed in the air (Moran 8e Sec. 12.6); it is the ABSCISSA of the psychrometric
chart (Sec. 12.7).  To turn that reading into a moist-air state we model the air as a
binary ideal-gas mixture of dry air (a) and water vapor (v), p = pa + pv (Dalton).

Composition is fixed by the **humidity ratio** (a.k.a. specific humidity)
    omega = m_v / m_a                                   (Eq. 12.42)
which, using pa = p - pv and Mv/Ma ~ 0.622, becomes
    omega = 0.622 pv / (p - pv)                         (Eq. 12.43)
and by the **relative humidity**
    phi = pv / pg(T)   |_{T,p}                          (Eq. 12.44)
where pg(T) is the saturation pressure at the mixture (dry-bulb) temperature -- the
link back to module 4.4 (phase change / pg) and 4.1 (enthalpy).

Energy is additive over the components:
    H = Ha + Hv = ma*ha + mv*hv                         (Eq. 12.45)
    h = H/ma = ha + omega*hv      (per unit dry air)    (Eq. 12.46)
    hv ~ hg(T)   (low-pressure vapor)                   (Eq. 12.47)

Units: pressures consistent (kPa or lbf/in^2); h in kJ/kg(dry air) [or Btu/lb].
Citations: Moran 8e (printed pages; PDF = printed + 18, VERIFIED); see ../refs.md.
"""

# Mv/Ma, water vapor over dry air molecular weights (Moran Eq. 12.43, p.754)
EPS = 0.622


def humidity_ratio(m_vapor, m_dry_air):
    """Humidity ratio (specific humidity)  omega = m_v / m_a  [kg(vap)/kg(dry air)].
    [Moran Eq. 12.42, Sec. 12.5.2, p.754]"""
    return m_vapor / m_dry_air


def humidity_ratio_from_pressures(p_v, p):
    """omega = 0.622 pv / (p - pv)  (pv = vapor partial pressure, p = mixture pressure).
    [Moran Eq. 12.43, Sec. 12.5.2, p.755]"""
    return EPS * p_v / (p - p_v)


def relative_humidity(p_v, p_g):
    """Relative humidity  phi = pv / pg(T)  at fixed T, p  (dimensionless, 0..1).
    [Moran Eq. 12.44, Sec. 12.5.2, p.755]"""
    return p_v / p_g


def vapor_pressure_from_phi(phi, p_g):
    """Invert Eq. 12.44 for the vapor partial pressure:  pv = phi * pg(T).
    [Moran Eq. 12.44, Sec. 12.5.2, p.755]"""
    return phi * p_g


def vapor_pressure_from_ratio(omega, p):
    """Invert Eq. 12.43 for the vapor partial pressure:  pv = omega*p / (0.622 + omega).
    [Moran Eq. 12.43, Sec. 12.5.2, p.755]"""
    return omega * p / (EPS + omega)


def mixture_enthalpy_total(m_dry_air, h_a, m_vapor, h_v):
    """Extensive moist-air enthalpy  H = Ha + Hv = ma*ha + mv*hv.
    [Moran Eq. 12.45, Sec. 12.5.2, p.755]"""
    return m_dry_air * h_a + m_vapor * h_v


def mixture_enthalpy_per_dry_air(h_a, omega, h_v):
    """Mixture enthalpy per unit mass of DRY AIR  h = ha + omega*hv.
    [Moran Eq. 12.46, Sec. 12.5.2, p.755]"""
    return h_a + omega * h_v


def vapor_enthalpy_approx(h_g_T):
    """Low-pressure approximation  hv ~ hg(T)  (sat-vapor value at the dry-bulb T).
    [Moran Eq. 12.47, Sec. 12.5.2, p.755]"""
    return h_g_T


def dry_air_mass(m_total, omega):
    """Dry-air mass from total moist-air mass and omega:  ma = m_total/(1+omega).
    (From m_total = ma + mv = ma(1+omega).)  [Moran Sec. 12.5.2, p.754]"""
    return m_total / (1.0 + omega)


def vapor_mass(m_total, omega):
    """Vapor mass from total moist-air mass and omega:  mv = omega*m_total/(1+omega).
    [Moran Sec. 12.5.2, p.754]"""
    return omega * m_total / (1.0 + omega)


def _demo():
    print("Module 11.1 -- Dry-bulb temperature & the moist-air model\n")
    # Moran Example 12.7 (p.758): moist air @70 F, 14.7 psi, phi = 0.70
    pg70 = 0.3632                       # pg(70 F), Table A-2E
    pv1 = vapor_pressure_from_phi(0.70, pg70)
    w1 = humidity_ratio_from_pressures(pv1, 14.7)
    print("  Ex 12.7  phi=0.70, pg(70F)=0.3632 -> pv1 = phi*pg = %.4f lbf/in^2  [book 0.2542]" % pv1)
    print("           omega1 = 0.622 pv/(p-pv) = %.4f lb(vap)/lb(dry air)      [book 0.011]" % w1)
    print("           dew point = Tsat(pv1) ~ 60 F   (saturation T at pv1)")
    # mass split of the 1-lb sample
    ma = dry_air_mass(1.0, w1); mv1 = vapor_mass(1.0, w1)
    print("           1 lb sample: ma = %.4f lb, mv1 = %.4f lb            [book 0.9891, 0.0109]" % (ma, mv1))
    # mixture enthalpy per dry air at the inlet of Ex 12.12 (chart datum ha=cpa*T)
    h = mixture_enthalpy_per_dry_air(1.005 * 22.0, 0.002, 2541.7)
    print("\n  h = ha + omega*hv (Ex 12.12 inlet 22 C, omega=0.002): %.2f kJ/kg(dry air)  [chart 27.2]" % h)


if __name__ == "__main__":
    _demo()
