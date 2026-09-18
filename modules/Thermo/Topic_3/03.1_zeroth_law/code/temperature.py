"""
temperature.py  —  Module 3.1 (Zeroth Law & Temperature)

The zeroth law of thermodynamics: if two bodies are each in thermal equilibrium
with a third body, they are in thermal equilibrium with each other (Moran 8e
Sec. 1.7).  That transitivity is what makes "temperature" a well-defined property
and what makes a thermometer meaningful -- the third body is the thermometer.

This module is the **temperature-scale toolkit**: convert among the Kelvin,
Rankine, Celsius, and Fahrenheit scales (Moran Eqs. 1.16-1.19), plus the fixed
points (triple/ice/steam points) that define them.  Kelvin and Rankine are
absolute scales (zero at absolute zero); Celsius and Fahrenheit are shifted.

Sign/units: temperatures returned in the named scale's degree.  In every
thermodynamic relation, T must be ABSOLUTE (K or degR) -- see modules 3.3/3.4.

Citations: Moran 8e (printed pages; PDF = printed + 18); full table in ../refs.md.
"""

# Fixed points of water (Moran 8e Sec. 1.7.3, Fig. 1.14)
TRIPLE_POINT_K = 273.16     # K   (defines the Kelvin scale, by agreement)
ICE_POINT_K = 273.15        # K   (0 degC)
STEAM_POINT_K = 373.15      # K   (100 degC, 1 atm)
ABS_ZERO_C = -273.15        # degC
ABS_ZERO_F = -459.67        # degF


def rankine_from_kelvin(T_K):
    """T(degR) = 1.8 T(K). [Moran Eq. 1.16, Sec. 1.7.2, p.21]"""
    return 1.8 * T_K


def kelvin_from_rankine(T_R):
    """T(K) = T(degR) / 1.8. [Moran Sec. 1.7.2, p.21]"""
    return T_R / 1.8


def celsius_from_kelvin(T_K):
    """T(degC) = T(K) - 273.15. [Moran Eq. 1.17, Sec. 1.7.3, p.22]"""
    return T_K - 273.15


def kelvin_from_celsius(T_C):
    """T(K) = T(degC) + 273.15. [Moran Eq. 1.17, Sec. 1.7.3, p.22]"""
    return T_C + 273.15


def fahrenheit_from_rankine(T_R):
    """T(degF) = T(degR) - 459.67. [Moran Eq. 1.18, Sec. 1.7.3, p.22]"""
    return T_R - 459.67


def rankine_from_fahrenheit(T_F):
    """T(degR) = T(degF) + 459.67. [Moran Eq. 1.18, Sec. 1.7.3, p.22]"""
    return T_F + 459.67


def fahrenheit_from_celsius(T_C):
    """T(degF) = 1.8 T(degC) + 32. [Moran Eq. 1.19, Sec. 1.7.3, p.22]"""
    return 1.8 * T_C + 32.0


def celsius_from_fahrenheit(T_F):
    """T(degC) = (T(degF) - 32) / 1.8. [Moran Eq. 1.19, Sec. 1.7.3, p.22]"""
    return (T_F - 32.0) / 1.8


def in_thermal_equilibrium(Ta, Tb, tol=1e-9):
    """Two bodies are in thermal equilibrium iff they share one temperature."""
    return abs(Ta - Tb) <= tol


def zeroth_law(Ta, Tb, Tc, tol=1e-9):
    """Zeroth law as a predicate (Moran 8e Sec. 1.7).

    If A~C and B~C (each in equilibrium with the third body C, the thermometer),
    return whether A~B -- which the zeroth law guarantees is True.  Returns None
    when the premise (both in equilibrium with C) does not hold.
    """
    if in_thermal_equilibrium(Ta, Tc, tol) and in_thermal_equilibrium(Tb, Tc, tol):
        return in_thermal_equilibrium(Ta, Tb, tol)
    return None


def _demo():
    print("Module 3.1 -- Zeroth Law & Temperature scales\n")
    print("  Fixed points (Moran Fig. 1.14):")
    print("    triple point of water = %s K = %.2f degC"
          % (TRIPLE_POINT_K, celsius_from_kelvin(TRIPLE_POINT_K)))
    print("    steam point           = %s K = %.0f degC = %.0f degF"
          % (STEAM_POINT_K, celsius_from_kelvin(STEAM_POINT_K),
             fahrenheit_from_celsius(celsius_from_kelvin(STEAM_POINT_K))))
    print("\n  Scale conversions:")
    print("    300 K  = %.1f degR = %.2f degC = %.2f degF"
          % (rankine_from_kelvin(300.0), celsius_from_kelvin(300.0),
             fahrenheit_from_celsius(celsius_from_kelvin(300.0))))
    print("    absolute zero = 0 K = %s degC = %s degF" % (ABS_ZERO_C, ABS_ZERO_F))
    print("\n  Zeroth law (A~C, B~C => A~B):")
    print("    zeroth_law(350, 350, 350) = %s" % zeroth_law(350.0, 350.0, 350.0))
    print("    zeroth_law(350, 360, 350) = %s  (premise fails -> None)"
          % zeroth_law(350.0, 360.0, 350.0))


if __name__ == "__main__":
    _demo()
