"""
subsonic.py  —  Module 13.1 (Subsonic Compressible Flow, M < 1)

A compressible flow is SUBSONIC when the Mach number M = V/c is less than 1.  This
module collects the Moran 8e Ch.9 tools that govern subsonic nozzle/diffuser flow:

  * speed of sound in an ideal gas      c = sqrt(k R T)            (Eq. 9.37)
  * Mach number                          M = V / c                 (Eq. 9.38)
  * stagnation enthalpy                  ho = h + V^2/2            (Eq. 9.39)
  * stagnation-property ratios (ideal gas, constant k):
        To/T  = 1 + (k-1)/2 M^2                                    (Eq. 9.50)
        po/p  = (1 + (k-1)/2 M^2)^( k/(k-1) )                      (Eq. 9.51)
        rho_o/rho = (1 + (k-1)/2 M^2)^( 1/(k-1) )     (from Eq. 9.51 + p v^k = const)
  * area-velocity relation               dA/A = -(dV/V)(1 - M^2)   (Eq. 9.45)

For M < 1 the factor (1 - M^2) > 0, so Eq. 9.45 gives the *opposite* sign of duct-area
change to velocity change:  to ACCELERATE a subsonic gas (dV>0) the duct must CONVERGE
(dA<0) -- a subsonic nozzle; to DECELERATE it (dV<0) the duct must DIVERGE -- a subsonic
diffuser (Moran Sec. 9.13.1, cases 1 and 4).  Worked anchor: Example 9.14(b), a
converging nozzle with back pressure 784 kPa > p*, runs subsonic to its exit (M2 = 0.6).

Units: c,V [m/s], T [K], R [J/kg.K], h [J/kg], k dimensionless.
Citations: Moran 8e (PDF = printed + 18; refs.md).
"""
import math


def speed_of_sound_ideal_gas(k, R, T):
    """Speed of sound in an ideal gas  c = sqrt(k R T)  [m/s], R in J/kg.K.
    [Moran Eq. 9.37, Sec. 9.12.2, p.570]"""
    return math.sqrt(k * R * T)


def mach_number(V, c):
    """Mach number  M = V / c.  M < 1 subsonic, = 1 sonic, > 1 supersonic.
    [Moran Eq. 9.38, Sec. 9.12.2, p.570]"""
    return V / c


def stagnation_enthalpy(h, V):
    """Stagnation enthalpy  ho = h + V^2/2  (isentropic deceleration to rest).
    [Moran Eq. 9.39, Sec. 9.12.3, p.571]"""
    return h + V * V / 2.0


def stagnation_temperature_ratio(M, k):
    """Stagnation temperature ratio  To/T = 1 + (k-1)/2 M^2  (ideal gas, const k).
    [Moran Eq. 9.50, Sec. 9.14.1, p.578]"""
    return 1.0 + (k - 1.0) / 2.0 * M * M


def stagnation_pressure_ratio(M, k):
    """Stagnation pressure ratio  po/p = (1 + (k-1)/2 M^2)^(k/(k-1))  (ideal gas, const k).
    [Moran Eq. 9.51, Sec. 9.14.1, p.578]"""
    return stagnation_temperature_ratio(M, k) ** (k / (k - 1.0))


def stagnation_density_ratio(M, k):
    """Stagnation density ratio  rho_o/rho = (1 + (k-1)/2 M^2)^(1/(k-1)).
    Follows from Eq. 9.51 and the ideal-gas isentropic relation p v^k = const.
    [Moran Sec. 9.14.1, p.578]"""
    return stagnation_temperature_ratio(M, k) ** (1.0 / (k - 1.0))


def static_temperature_from_stagnation(To, M, k):
    """Static T from stagnation To:  T = To / (1 + (k-1)/2 M^2).
    [Moran Eq. 9.50 rearranged, Sec. 9.14.1, p.578]"""
    return To / stagnation_temperature_ratio(M, k)


def static_pressure_from_stagnation(po, M, k):
    """Static p from stagnation po:  p = po / (1 + (k-1)/2 M^2)^(k/(k-1)).
    [Moran Eq. 9.51 rearranged, Sec. 9.14.1, p.578]"""
    return po / stagnation_pressure_ratio(M, k)


def area_change_ratio(dV_over_V, M):
    """Area-velocity relation  dA/A = -(dV/V)(1 - M^2).
    [Moran Eq. 9.45, Sec. 9.13.1, p.573]"""
    return -dV_over_V * (1.0 - M * M)


def duct_shape(dV_over_V, M):
    """Classify the duct from Eq. 9.45: returns 'converging' if dA<0, 'diverging' if dA>0,
    'constant-area' if dA=0.  For M<1: accelerate (dV>0) -> converging (nozzle);
    decelerate (dV<0) -> diverging (diffuser).  [Moran Sec. 9.13.1, cases 1,4, p.573]"""
    dA = area_change_ratio(dV_over_V, M)
    if dA < 0.0:
        return "converging"
    if dA > 0.0:
        return "diverging"
    return "constant-area"


def _demo():
    print("Module 13.1 -- Subsonic compressible flow (M < 1)\n")
    R = 8314.0 / 28.97                                   # air gas constant, J/kg.K
    c300 = speed_of_sound_ideal_gas(1.4, R, 300.0)
    print("  Speed of sound, air @300 K, k=1.4:  c = %.0f m/s   [Moran p.570: 347]" % c300)
    # Example 9.14(b): converging nozzle, po=1.0 MPa, To=360 K, back pressure 784 kPa
    To, po, p2 = 360.0, 1.0e6, 7.84e5
    M2 = math.sqrt(2.0 / 0.4 * ((po / p2) ** (0.4 / 1.4) - 1.0))   # invert Eq. 9.51
    T2 = static_temperature_from_stagnation(To, M2, 1.4)
    V2 = M2 * speed_of_sound_ideal_gas(1.4, R, T2)
    print("  Ex 9.14(b) subsonic exit:  M2 = %.2f, T2 = %.0f K, V2 = %.1f m/s  [book 0.6, 336, 220.5]"
          % (M2, T2, V2))
    print("  p/po at M=0.6: %.3f (= back-pressure ratio 784/1000)   [Table 9.2: 0.784]"
          % (1.0 / stagnation_pressure_ratio(0.6, 1.4)))
    print("  Area-velocity (M<1): accelerate dV>0 ->", duct_shape(+0.01, 0.6),
          "| decelerate dV<0 ->", duct_shape(-0.01, 0.6))


if __name__ == "__main__":
    _demo()
