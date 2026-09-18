"""
fuels.py  —  Module 12.1 (Fuels & Combustion of Reacting Mixtures)

The Moran 8e Chapter-13 toolkit for combustion of hydrocarbon fuels with air:

  * balancing complete combustion  CaHbOc + a_O2 (O2 + 3.76 N2) -> b CO2 + (c/2) H2O + ...
        theoretical O2 per mole fuel:  a_O2 = C + H/4 + S - O/2          (Sec. 13.1.2)
        air model: 1 mol O2 carried by 3.76 mol N2  (4.76 mol air / mol O2)
  * air-fuel ratio, mass <-> molar     AF = AF_bar (M_air / M_fuel)       (Eq. 13.2)
  * % theoretical air, % excess air, equivalence ratio                    (Sec. 13.1.2)
  * products composition & dew point   p_v = y_v p                        (Sec. 13.1.3)
  * enthalpy of formation / combustion h = h_f0 + dh,  h_RP = SUM_P n h - SUM_R n h
                                                       (Eqs. 13.9, 13.18)
  * heating values HHV/LHV = |h_RP| (liquid / vapor water in products)    (Sec. 13.2.3)
  * steady-flow energy balance         Qcv/nF - Wcv/nF = hP - hR          (Eqs. 13.12b/13.15b)

Standard reference state: Tref = 298.15 K (25 C), pref = 1 atm.  Enthalpy of the stable
elements (C, H2, O2, N2, ...) is zero there.  M_air = 28.97 kg/kmol.

Units: enthalpies kJ/kmol (molar) or kJ/kg (mass); M kg/kmol; pressures share any unit.
Citations: Moran 8e (PDF = printed + 18; refs.md).
"""
import math

M_AIR = 28.97               # kg/kmol, combustion-air model (Moran Sec. 13.1.2, p.808)
N2_PER_O2 = 3.76            # mol N2 per mol O2 in air (0.79/0.21)
AIR_PER_O2 = 4.76           # 1 + 3.76 mol air per mol O2
RU = 8.314                  # kJ/kmol.K


# --- stoichiometry: theoretical (minimum) air --------------------------------
def theoretical_O2(nC, nH, nO=0.0, nS=0.0):
    """Theoretical (stoichiometric) moles of O2 to completely burn a fuel CcHhOoSs:
    a_O2 = C + H/4 + S - O/2.  [Moran Sec. 13.1.2, p.808]"""
    return nC + nH / 4.0 + nS - nO / 2.0


def theoretical_air_molar(nC, nH, nO=0.0, nS=0.0):
    """Theoretical air per mole of fuel (molar AF) = 4.76 * a_O2.
    [Moran Sec. 13.1.2, Eq. 13.4 (octane Ex. 13.1), p.808]"""
    return AIR_PER_O2 * theoretical_O2(nC, nH, nO, nS)


# --- air-fuel and fuel-air ratios --------------------------------------------
def afr_molar_to_mass(afr_molar, M_fuel, M_air=M_AIR):
    """Air-fuel ratio mass basis from molar basis  AF = AF_bar (M_air/M_fuel).
    [Moran Eq. 13.2, Sec. 13.1.2, p.808]"""
    return afr_molar * (M_air / M_fuel)


def afr_mass_to_molar(afr_mass, M_fuel, M_air=M_AIR):
    """Air-fuel ratio molar basis from mass basis (inverse of Eq. 13.2).
    [Moran Eq. 13.2, Sec. 13.1.2, p.808]"""
    return afr_mass * (M_fuel / M_air)


def fuel_air_ratio(afr):
    """Fuel-air ratio = reciprocal of the air-fuel ratio.  [Moran Sec. 13.1.2, p.807]"""
    return 1.0 / afr


# --- amount of air supplied relative to theoretical --------------------------
def percent_theoretical_air(afr_actual, afr_theoretical):
    """Fraction of theoretical air = AF / AF_theo (1.50 = 150% theoretical air).
    [Moran Sec. 13.1.2, Ex. 13.2(b), p.812]"""
    return afr_actual / afr_theoretical


def percent_excess_air(afr_actual, afr_theoretical):
    """Fractional excess air = (AF - AF_theo)/AF_theo (0.50 = 50% excess = 150% theo).
    [Moran Sec. 13.1.2, p.808]"""
    return (afr_actual - afr_theoretical) / afr_theoretical


def equivalence_ratio(afr_actual, afr_theoretical):
    """Equivalence ratio phi = (F/A)_actual/(F/A)_theo = AF_theo/AF_actual.
    phi < 1 lean, phi > 1 rich.  [Moran Sec. 13.1.2, p.809]"""
    return afr_theoretical / afr_actual


def O2_supplied(O2_theoretical, percent_theoretical):
    """Moles O2 actually supplied = (% theoretical air) * theoretical O2.
    [Moran Sec. 13.1.2, Eq. 13.5, p.809]"""
    return percent_theoretical * O2_theoretical


# --- products composition & dew point ----------------------------------------
def mole_fraction(n_i, n_total):
    """Mole fraction y_i = n_i / n_total of a product species.  [Moran Sec. 13.1.3]"""
    return n_i / n_total


def water_vapor_mole_fraction(n_water, n_dry):
    """Mole fraction of water vapor in products = n_H2O/(n_H2O + n_dry).
    [Moran Sec. 13.1.3, Ex. 13.2(c), p.812]"""
    return n_water / (n_water + n_dry)


def dew_point_partial_pressure(y_vapor, p_mixture):
    """Partial pressure of product water vapor  p_v = y_v p; its saturation
    temperature is the dew point (onset of condensation on cooling at constant p).
    [Moran Sec. 13.1.3, Ex. 13.2(c), p.812]"""
    return y_vapor * p_mixture


def vapor_remaining_on_cooling(p_sat, p_mixture, n_dry):
    """Moles of water vapor still present when products are cooled below the dew point:
    from p_sat = (n/(n+n_dry)) p  ->  n = p_sat n_dry/(p_mixture - p_sat).  The remaining
    water has condensed to liquid.  [Moran Sec. 13.1.3, Ex. 13.2(d), p.812]"""
    return p_sat * n_dry / (p_mixture - p_sat)


# --- enthalpy of reacting systems --------------------------------------------
def enthalpy(h_f0, dh=0.0):
    """Specific enthalpy of a compound  h = h_f0 + [h(T) - h(Tref)] = h_f0 + dh.
    [Moran Eq. 13.9, Sec. 13.2.1, p.817]"""
    return h_f0 + dh


def stream_enthalpy(terms):
    """Total enthalpy per mole of fuel of a reactant or product stream:
    SUM_i n_i (h_f0 + dh)_i, with terms = list of (n, h_f0, dh) tuples.
    [Moran Eq. 13.15b, Sec. 13.2.2, p.819]"""
    return sum(n * enthalpy(h_f0, dh) for (n, h_f0, dh) in terms)


def enthalpy_of_combustion(products, reactants):
    """Enthalpy of combustion  h_RP = SUM_P n_e h_e - SUM_R n_i h_i  (complete combustion,
    reactants & products at same T, p).  products/reactants = lists of (n, h_f0, dh).
    [Moran Eq. 13.18, Sec. 13.2.3, p.825]"""
    return stream_enthalpy(products) - stream_enthalpy(reactants)


def heating_value_molar(h_RP):
    """Heating value (molar) = magnitude of the enthalpy of combustion |h_RP|.
    HHV if products have liquid water, LHV if vapor.  [Moran Sec. 13.2.3, p.825]"""
    return abs(h_RP)


def heating_value_mass(h_RP, M_fuel):
    """Heating value per unit mass of fuel = |h_RP| / M_fuel.  [Moran Sec. 13.2.3, p.826]"""
    return abs(h_RP) / M_fuel


# --- steady-flow energy balance ----------------------------------------------
def energy_balance_per_mole_fuel(products, reactants):
    """Steady-flow reactor:  (Qcv - Wcv)/nF = hP - hR  per mole of fuel.
    products/reactants = lists of (n, h_f0, dh).  [Moran Eqs. 13.12b/13.15b, p.818-819]"""
    return stream_enthalpy(products) - stream_enthalpy(reactants)


def _demo():
    print("Module 12.1 -- Fuels & combustion of reacting mixtures (Moran Ch.13)\n")
    # Example 13.1: octane C8H18, theoretical air
    aO2 = theoretical_O2(8, 18)
    afm = theoretical_air_molar(8, 18)
    print("  Ex 13.1 octane, theoretical air:  a_O2 = %.1f, AF_bar = %.1f [book 12.5, 59.5]"
          % (aO2, afm))
    print("    AF (mass) = %.1f kg air/kg fuel                       [book 15.1]"
          % afr_molar_to_mass(afm, 114.22))
    afm15 = 1.5 * afm
    print("  Ex 13.1(b) 150%% theoretical air: AF_bar = %.2f, AF = %.1f, phi = %.2f"
          " [book 89.25, 22.6, 0.67]"
          % (afm15, afr_molar_to_mass(afm15, 114.22), equivalence_ratio(afm15, afm)))
    # Example 13.2: dry product analysis of methane combustion
    yv = water_vapor_mole_fraction(20.4, 100.0)
    pv = dew_point_partial_pressure(yv, 1.0)      # atm
    print("\n  Ex 13.2 methane (dry products): y_v = %.3f, p_v = %.3f atm (dew pt 134 F)"
          " [book 0.169, 0.169]" % (yv, pv))
    print("    %% theoretical air = %.2f                              [book 1.13 (113%%)]"
          % percent_theoretical_air(10.78, 9.52))
    n = vapor_remaining_on_cooling(0.6988, 14.696, 9.8)
    print("    water vapor left at 90 F = %.3f lbmol/lbmol fuel      [book 0.489]" % n)
    # Example 13.7: enthalpy of combustion / heating values of methane
    P_liq = [(1, -393520, 0.0), (2, -285830, 0.0)]      # CO2, H2O(l)
    P_vap = [(1, -393520, 0.0), (2, -241820, 0.0)]      # CO2, H2O(g)
    R = [(1, -74850, 0.0)]                                # CH4(g) (+ 2 O2, h_f0=0)
    hhv = enthalpy_of_combustion(P_liq, R)
    lhv = enthalpy_of_combustion(P_vap, R)
    print("\n  Ex 13.7 methane h_RP: HHV = %.0f kJ/kmol (%.0f kJ/kg), LHV = %.0f (%.0f kJ/kg)"
          % (hhv, heating_value_mass(hhv, 16.04), lhv, heating_value_mass(lhv, 16.04)))
    print("    [book HHV 890,330 / 55,507 ; LHV 802,310 / 50,019]")


if __name__ == "__main__":
    _demo()
