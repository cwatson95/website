"""
supersonic.py  —  Module 13.2 (Supersonic Compressible Flow, M > 1)

A flow is SUPERSONIC when M = V/c > 1.  The area-velocity relation (Moran Eq. 9.45)

    dA/A = -(dV/V)(1 - M^2)

flips sign once M passes 1:  for M > 1 the factor (1 - M^2) < 0, so area and velocity
change in the SAME direction.  A supersonic flow therefore ACCELERATES in a DIVERGING
duct (supersonic nozzle, case 2) and DECELERATES in a CONVERGING duct (supersonic
diffuser, case 3).  Because M = 1 can occur only at a minimum area (the THROAT), going
from subsonic to supersonic requires a CONVERGING-DIVERGING nozzle (Moran Sec. 9.13.1).

Closed-form tools for an ideal gas with constant k (Moran Sec. 9.14.1):
  * area-Mach relation     A/A* = (1/M)[ (2/(k+1))(1 + (k-1)/2 M^2) ]^((k+1)/(2(k-1)))  (9.52)
  * critical (M=1) ratios  p*/po = (2/(k+1))^(k/(k-1)),  T*/To = 2/(k+1)        (Eq. 9.51, 9.50 @M=1)
  * choking test           a converging nozzle is CHOKED when pB <= p*           (Sec. 9.13.2)
  * inverse maps           M from p/po (Eq. 9.51) and M from A/A* (Eq. 9.52, by bisection)

Worked anchors: Example 9.14(a) (choked converging nozzle, p* = 0.528 po, exit M=1) and
Example 9.15(c) (supersonic exit of a converging-diverging nozzle, M = 2.4).

Units: c,V [m/s], T [K], R [J/kg.K], k dimensionless.  Citations: Moran 8e (PDF=printed+18).
"""
import math


def speed_of_sound_ideal_gas(k, R, T):
    """c = sqrt(k R T) [m/s]. [Moran Eq. 9.37, Sec. 9.12.2, p.570]"""
    return math.sqrt(k * R * T)


def mach_number(V, c):
    """M = V / c. [Moran Eq. 9.38, Sec. 9.12.2, p.570]"""
    return V / c


def stagnation_temperature_ratio(M, k):
    """To/T = 1 + (k-1)/2 M^2. [Moran Eq. 9.50, Sec. 9.14.1, p.578]"""
    return 1.0 + (k - 1.0) / 2.0 * M * M


def stagnation_pressure_ratio(M, k):
    """po/p = (1 + (k-1)/2 M^2)^(k/(k-1)). [Moran Eq. 9.51, Sec. 9.14.1, p.578]"""
    return stagnation_temperature_ratio(M, k) ** (k / (k - 1.0))


def area_mach_ratio(M, k):
    """Isentropic area ratio  A/A* = (1/M)[ (2/(k+1))(1 + (k-1)/2 M^2) ]^((k+1)/(2(k-1))).
    [Moran Eq. 9.52, Sec. 9.14.1, p.578]"""
    t = (2.0 / (k + 1.0)) * stagnation_temperature_ratio(M, k)
    return (1.0 / M) * t ** ((k + 1.0) / (2.0 * (k - 1.0)))


def critical_pressure_ratio(k):
    """Critical (sonic, M=1) pressure ratio  p*/po = (2/(k+1))^(k/(k-1)).
    For k=1.4 this is 0.528. [Moran Eq. 9.51 at M=1, Sec. 9.13.2/9.14.1, p.574/578]"""
    return (2.0 / (k + 1.0)) ** (k / (k - 1.0))


def critical_temperature_ratio(k):
    """Critical (sonic, M=1) temperature ratio  T*/To = 2/(k+1).
    [Moran Eq. 9.50 at M=1, Sec. 9.14.1, p.578]"""
    return 2.0 / (k + 1.0)


def is_choked(p_back, p0, k):
    """Converging nozzle: choked (exit M=1, max mass flow) when pB <= p* = (p*/po) p0.
    [Moran Sec. 9.13.2, p.574-575]"""
    return p_back <= critical_pressure_ratio(k) * p0


def mach_from_pressure_ratio(p0_over_p, k):
    """Invert Eq. 9.51:  M = sqrt( 2/(k-1) [ (po/p)^((k-1)/k) - 1 ] ).
    [Moran Eq. 9.51 solved for M, Sec. 9.14.1, p.580]"""
    return math.sqrt(2.0 / (k - 1.0) * (p0_over_p ** ((k - 1.0) / k) - 1.0))


def mach_from_area_ratio(A_over_Astar, k, supersonic=True):
    """Invert the area-Mach relation (Eq. 9.52) by bisection.  A/A* >= 1 has two roots;
    supersonic=True returns M>1, else the subsonic M<1.  [Moran Eq. 9.52, p.578]"""
    if A_over_Astar < 1.0:
        raise ValueError("A/A* must be >= 1")
    lo, hi = (1.0, 50.0) if supersonic else (1e-6, 1.0)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        f = area_mach_ratio(mid, k) - A_over_Astar
        # A/A* decreases with M on the subsonic branch, increases on the supersonic branch
        if supersonic:
            if f > 0.0:
                hi = mid
            else:
                lo = mid
        else:
            if f > 0.0:
                lo = mid
            else:
                hi = mid
    return 0.5 * (lo + hi)


def _demo():
    print("Module 13.2 -- Supersonic compressible flow (M > 1), choking, area-Mach\n")
    R = 8314.0 / 28.97
    # Example 9.14(a): converging nozzle, po=1.0 MPa, To=360 K, back pressure 500 kPa
    pstar_ratio = critical_pressure_ratio(1.4)
    print("  Ex 9.14(a) choking:  p*/po = %.3f -> p* = %.0f kPa  [book 0.528, 528]"
          % (pstar_ratio, pstar_ratio * 1000.0))
    print("     pB=500 kPa choked?  %s (500 < 528)" % is_choked(500.0e3, 1.0e6, 1.4))
    T2 = critical_temperature_ratio(1.4) * 360.0
    V2 = speed_of_sound_ideal_gas(1.4, R, T2)
    mdot = (pstar_ratio * 1.0e6) * 0.001 * V2 / (R * T2)
    print("     exit M=1: T2 = %.0f K, V2 = %.1f m/s, mdot = %.2f kg/s  [book 300, 347.2, 2.13]"
          % (T2, V2, mdot))
    # Example 9.15(c): converging-diverging nozzle, supersonic exit, A2/A* = 2.4
    M2 = mach_from_area_ratio(2.4, 1.4, supersonic=True)
    p_ratio = 1.0 / stagnation_pressure_ratio(2.4, 1.4)
    print("  Ex 9.15(c) supersonic exit:  A/A*=2.4 -> M=%.2f, p/po=%.4f -> p2=%.2f lbf/in^2"
          % (M2, p_ratio, p_ratio * 100.0))
    print("     [book M=2.4, p2=6.84 lbf/in^2]   area_mach_ratio(2.4)=%.4f [Table 9.2: 2.4031]"
          % area_mach_ratio(2.4, 1.4))


if __name__ == "__main__":
    _demo()
