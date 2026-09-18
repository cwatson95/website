"""
wet_bulb.py  —  Module 11.2 (Wet-bulb temperature & adiabatic saturation)

The wet-bulb temperature is read from a thermometer whose bulb is wrapped in a
water-soaked wick (Moran 8e Sec. 12.6).  As unsaturated air flows past, water
evaporates and cools the wick to a steady value below the dry-bulb temperature -- an
evaporative-cooling reading.  Paired with the dry-bulb thermometer in a psychrometer,
the two temperatures FIX the moist-air state and locate it on the psychrometric chart
(Sec. 12.7): dry-bulb on the abscissa, wet-bulb lines running upper-left to lower-right.

Theory: the **adiabatic-saturation temperature** Tas of an adiabatic saturator
(steady, insulated, makeup water at Tas) gives omega from p, T, Tas via the energy
balance per unit dry air (Eq. 12.50):
    (ha + omega*hg)_T + (omega' - omega) hf(Tas) = (ha + omega'*hg)_Tas
solved for omega:
    omega = [ha(Tas)-ha(T) + omega'(hg(Tas)-hf(Tas))] / [hg(T) - hf(Tas)]   (Eq. 12.48)
    omega' = 0.622 pg(Tas) / (p - pg(Tas))                                   (Eq. 12.49)
For normal psychrometric conditions Twb ~ Tas, so the wet-bulb temperature may be used
in place of Tas (Sec. 12.6).

Chart enthalpy datum (ha = 0 at 0 C):  ha = cpa * T(C)  (Eq. 12.51), cpa = 1.005 kJ/kg.K.
Dew point = saturation temperature at pv (Sec. 12.5.4): cool at constant p (constant
omega) until phi = 100%.

Citations: Moran 8e (printed pages; PDF = printed + 18, VERIFIED); see ../refs.md.
"""

EPS = 0.622          # Mv/Ma (Moran Eq. 12.49)
CPA = 1.005          # cp of dry air, kJ/kg.K, chart datum (Moran Eq. 12.51, p.767)


def humidity_ratio_at_saturation(p_g_Tas, p):
    """omega' for the saturated exit stream  omega' = 0.622 pg(Tas)/(p - pg(Tas)).
    [Moran Eq. 12.49, Sec. 12.5.5, p.763]"""
    return EPS * p_g_Tas / (p - p_g_Tas)


def humidity_ratio_from_wet_bulb(omega_prime, ha_T, ha_Tas, hf_Tas, hg_Tas, hg_T):
    """Humidity ratio from the adiabatic-saturation (~ wet-bulb) temperature:
    omega = [ha(Tas)-ha(T) + omega'(hg(Tas)-hf(Tas))] / [hg(T)-hf(Tas)].
    [Moran Eq. 12.48, Sec. 12.5.5, p.763]"""
    return (ha_Tas - ha_T + omega_prime * (hg_Tas - hf_Tas)) / (hg_T - hf_Tas)


def adiabatic_saturator_residual(omega, omega_prime, ha_T, ha_Tas, hg_T, hg_Tas, hf_Tas):
    """Residual of the adiabatic-saturator energy balance per unit dry air (Eq. 12.50):
    (ha+omega*hg)_T + (omega'-omega)hf(Tas) - (ha+omega'*hg)_Tas.  Zero at the solution.
    [Moran Eq. 12.50, Sec. 12.5.5, p.764]"""
    lhs = (ha_T + omega * hg_T) + (omega_prime - omega) * hf_Tas
    rhs = ha_Tas + omega_prime * hg_Tas
    return lhs - rhs


def dry_air_enthalpy(T_C, cpa=CPA):
    """Dry-air enthalpy on the psychrometric-chart datum (0 at 0 C):  ha = cpa * T(C).
    [Moran Eq. 12.51, Sec. 12.7, p.767]"""
    return cpa * T_C


def state_enthalpy(ha, omega, hg):
    """Mixture enthalpy per unit dry air read at a chart point  (ha + omega*hg).
    Constant-wet-bulb lines are ~ constant-enthalpy lines.
    [Moran Eq. 12.46/Sec. 12.7, p.755/766]"""
    return ha + omega * hg


def dew_point_pressure(omega, p):
    """Vapor partial pressure pv from omega (invert Eq. 12.43); the dew point is the
    saturation temperature Tsat(pv).  pv = omega*p/(0.622+omega).
    [Moran Sec. 12.5.4, p.757; Eq. 12.43]"""
    return omega * p / (EPS + omega)


def exit_humidity_ratio(omega_in, mdot_water, mdot_air):
    """Water mass balance for adding moisture to a moist-air stream:
    omega_out = omega_in + mdot_water/mdot_air.  [Moran Sec. 12.8.4, p.776]"""
    return omega_in + mdot_water / mdot_air


def _demo():
    print("Module 11.2 -- Wet-bulb temperature & adiabatic saturation\n")
    # In-text psychrometer reading (Moran p.767): dry-bulb 68 F + wet-bulb 60 F
    print("  Psychrometer (p.767): dry-bulb 68 F, wet-bulb 60 F")
    print("    -> chart read omega = 0.0092 lb/lb, phi = 0.63  (state fixed by the two T's)")
    # Eq. 12.49 omega' at a saturation temperature
    wprime = humidity_ratio_at_saturation(1.228, 101.325)     # pg(10 C)=1.228 kPa
    print("\n  Eq 12.49  omega'(Tas=10C, p=101.325kPa) = %.5f kg/kg" % wprime)
    # Eq. 12.48 self-consistency: T = Tas (already saturated air) -> omega = omega'
    w = humidity_ratio_from_wet_bulb(wprime, dry_air_enthalpy(10), dry_air_enthalpy(10),
                                     42.01, 2519.8, 2519.8)    # hf,hg @10 C
    print("  Eq 12.48  with T = Tas returns omega = omega' = %.5f  (consistency)" % w)
    # chart enthalpy of the Ex 12.12 inlet (dry-bulb 22 C, omega=0.002)
    print("\n  Chart enthalpy (ha+omega*hg) @22C, omega=0.002: %.2f kJ/kg(dry air)  [chart 27.2]"
          % state_enthalpy(dry_air_enthalpy(22), 0.002, 2541.7))
    # dew point pv of Example 12.7 (omega=0.010947, p=14.7)
    print("  Dew-point pv of Ex 12.7 (omega=0.010947, p=14.7) = %.4f lbf/in^2  [book 0.2542 -> 60 F]"
          % dew_point_pressure(0.010947, 14.7))


if __name__ == "__main__":
    _demo()
