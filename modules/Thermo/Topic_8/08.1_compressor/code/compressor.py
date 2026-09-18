"""
compressor.py  —  Module 08.1 (Compressor: work-input device raising gas pressure)

A COMPRESSOR does work on a gas (vapor) to raise its pressure.  For a control volume
enclosing a compressor at steady state, the one-inlet/one-exit energy rate balance is

    0 = Qdot_cv - Wdot_cv + mdot[ (h1 - h2) + (V1^2 - V2^2)/2 + g(z1 - z2) ]   (Eq. 4.20a)

For compressors the potential-energy change is negligible and (often) so is the kinetic
energy term, leaving 0 = Qdot_cv - Wdot_cv + mdot(h1 - h2), and when heat transfer is a
secondary effect, Wdot_cv = mdot(h1 - h2)  (Eq. 4.20b/Sec. 4.8.1).  NOTE the sign: for a
compressor Wdot_cv is NEGATIVE because power is supplied TO the substance; the power
INPUT magnitude is -Wdot_cv.

Best performance (least work for a given pressure rise) is the adiabatic, internally
reversible -> ISENTROPIC compression to the same exit pressure.  The isentropic
compressor efficiency compares the minimum (isentropic) work to the actual work
(Moran Eq. 6.48, Sec. 6.12.3):

    eta_c = (-Wdot_cv/mdot)_s / (-Wdot_cv/mdot) = (h2s - h1) / (h2 - h1)

Worked anchors: Example 4.5 (air compressor, power = -119.4 kW) and Example 6.14
(R-22 compressor, eta_c = 0.81).

Units: the energy-balance functions (power_cv/power_input) use STRICT SI base units so
that h and V^2/2 are consistent -- h [J/kg], V [m/s], z [m], g [m/s^2], mdot [kg/s],
Qdot/Wdot [W].  The work/efficiency helpers take enthalpy DIFFERENCES, so any consistent
energy unit (J/kg or kJ/kg) works there.  Citations: Moran 8e (PDF = printed + 18; refs.md).
"""


def mass_flow_rate(A, V, v):
    """Mass flow rate  mdot = A V / v  (one-dimensional flow).  A [m^2], V [m/s],
    v specific volume [m^3/kg] -> mdot [kg/s].  [Moran Eq. 4.4b, Sec. 4.2.1, p.172]"""
    return A * V / v


def mass_flow_rate_ideal_gas(A, V, p, R, T):
    """mdot = A V p / (R T)  (ideal-gas v = RT/p).  R the specific gas constant [J/kg.K].
    [Moran Eq. 4.4b + ideal gas, Ex. 4.5, p.191]"""
    return A * V * p / (R * T)


def power_cv(mdot, h1, h2, Qdot=0.0, V1=0.0, V2=0.0, g=9.81, z1=0.0, z2=0.0):
    """Signed control-volume power Wdot_cv [W] from the steady CV energy balance (Eq. 4.20a):
        Wdot_cv = Qdot_cv + mdot[(h1 - h2) + (V1^2 - V2^2)/2 + g(z1 - z2)].
    STRICT SI: h [J/kg], V [m/s], z [m], Qdot [W].  For a compressor this comes out
    NEGATIVE (power supplied to the gas).  [Moran Eq. 4.20a, Sec. 4.8.1, p.190]"""
    return Qdot + mdot * ((h1 - h2) + (V1 * V1 - V2 * V2) / 2.0 + g * (z1 - z2))


def power_input(mdot, h1, h2, Qdot=0.0, V1=0.0, V2=0.0, g=9.81, z1=0.0, z2=0.0):
    """Magnitude of the power INPUT required = -Wdot_cv [W] (positive for a compressor).
    STRICT SI (see power_cv).  [Moran Eq. 4.20a, Sec. 4.8.1, p.190]"""
    return -power_cv(mdot, h1, h2, Qdot, V1, V2, g, z1, z2)


def actual_compressor_work(h1, h2):
    """Actual specific work input  (-Wdot/mdot) = h2 - h1  (adiabatic, dKE,dPE = 0).
    [Moran Sec. 6.12.3, p.337]"""
    return h2 - h1


def isentropic_compressor_work(h1, h2s):
    """Minimum (isentropic) specific work input  (-Wdot/mdot)_s = h2s - h1, where h2s is
    the exit enthalpy of an isentropic compression to the SAME exit pressure.
    [Moran Sec. 6.12.3, p.337]"""
    return h2s - h1


def isentropic_efficiency(h1, h2, h2s):
    """Isentropic compressor efficiency  eta_c = (h2s - h1)/(h2 - h1)  (0 < eta_c <= 1;
    typically 0.75-0.85).  [Moran Eq. 6.48, Sec. 6.12.3, p.338]"""
    return (h2s - h1) / (h2 - h1)


def exit_enthalpy_from_efficiency(h1, h2s, eta_c):
    """Actual exit enthalpy from eta_c:  h2 = h1 + (h2s - h1)/eta_c.
    [Moran Eq. 6.48 rearranged, Sec. 6.12.3, p.338]"""
    return h1 + (h2s - h1) / eta_c


def _demo():
    print("Module 08.1 -- Compressor (steady-state control-volume energy balance)\n")
    # Example 4.5: air compressor, p1=1 bar, T1=290 K, V1=6 m/s, A1=0.1 m^2;
    #              p2=7 bar, T2=450 K, V2=2 m/s; Qcv = -180 kJ/min.  h: Table A-22.
    R = 8314.0 / 28.97                                   # air, J/kg.K
    mdot = mass_flow_rate_ideal_gas(0.1, 6.0, 1.0e5, R, 290.0)        # 0.72 kg/s
    h1, h2 = 290.16e3, 451.80e3                          # J/kg, Table A-22
    Qdot = -180.0e3 / 60.0                               # W  (-180 kJ/min)
    W = power_cv(mdot, h1, h2, Qdot=Qdot, V1=6.0, V2=2.0, g=0.0)      # W (PE neglected)
    print("  Ex 4.5 air compressor: mdot = %.2f kg/s   [book 0.72]" % mdot)
    print("    Wdot_cv = %.1f kW  (power input %.1f kW)   [book -119.4 kW]"
          % (W / 1e3, -W / 1e3))
    # Example 6.14: R-22 compressor, h1=249.75, h2=294.17, h2s=285.58 kJ/kg, mdot=0.07 kg/s
    h1, h2, h2s = 249.75e3, 294.17e3, 285.58e3          # J/kg
    Wc = power_cv(0.07, h1, h2)                          # -3.11 kW
    eta = isentropic_efficiency(h1, h2, h2s)
    print("  Ex 6.14 R-22 compressor: Wdot_cv = %.2f kW [book -3.11], eta_c = %.2f [book 0.81]"
          % (Wc / 1e3, eta))


if __name__ == "__main__":
    _demo()
