"""
shock.py  —  Module 13.3 (Normal Shock)

When a supersonic flow in the diverging section of a converging-diverging nozzle meets
too high a back pressure, an abrupt, irreversible transition called a NORMAL SHOCK can
stand across a plane normal to the flow.  Across it the flow jumps from supersonic
(Mx > 1) to subsonic (My < 1); pressure and temperature rise sharply, entropy increases
(sy > sx), and the stagnation pressure DROPS, while the stagnation TEMPERATURE is
unchanged (Tox = Toy) (Moran Sec. 9.13.3 / 9.14.2).

Closed-form NORMAL-SHOCK FUNCTIONS for an ideal gas with constant k (Moran Sec. 9.14.2):
  * downstream Mach   My^2 = (Mx^2 + 2/(k-1)) / ( (2k/(k-1)) Mx^2 - 1 )            (9.55)
  * temperature jump  Ty/Tx = (1 + (k-1)/2 Mx^2) / (1 + (k-1)/2 My^2)             (9.53)
  * pressure jump     py/px = (1 + k Mx^2) / (1 + k My^2)                          (9.54)
  * stagnation-p loss poy/pox = (Mx/My)[ (1+(k-1)/2 My^2)/(1+(k-1)/2 Mx^2) ]^E    (9.56)
                       with E = (k+1)/(2(k-1));  and A*x/A*y = poy/pox            (9.57)

Worked anchors: the Table-9.3 row at Mx = 2.0 (My = 0.5774, py/px = 4.5, Ty/Tx = 1.6875,
poy/pox = 0.7209) and Example 9.15(d,e) (shock at Mx = 2.4 and Mx = 2.2).

All ratios are dimensionless; T [K] or [degR], p any consistent unit.  k = cp/cv.
Citations: Moran 8e (PDF = printed + 18; refs.md).
"""
import math


def stagnation_temperature_ratio(M, k):
    """To/T = 1 + (k-1)/2 M^2 (used inside the shock functions). [Eq. 9.50, p.578]"""
    return 1.0 + (k - 1.0) / 2.0 * M * M


def mach_after_shock(Mx, k):
    """Downstream Mach number  My = sqrt( (Mx^2 + 2/(k-1)) / ((2k/(k-1)) Mx^2 - 1) ).
    Requires Mx >= 1 (a shock forms only in supersonic flow).
    [Moran Eq. 9.55, Sec. 9.14.2, p.581]"""
    if Mx < 1.0:
        raise ValueError("normal shock requires Mx >= 1")
    num = Mx * Mx + 2.0 / (k - 1.0)
    den = (2.0 * k / (k - 1.0)) * Mx * Mx - 1.0
    return math.sqrt(num / den)


def shock_temperature_ratio(Mx, k):
    """Static-temperature ratio across the shock  Ty/Tx (Eq. 9.53), with My from Eq. 9.55.
    [Moran Eq. 9.53, Sec. 9.14.2, p.581]"""
    My = mach_after_shock(Mx, k)
    return stagnation_temperature_ratio(Mx, k) / stagnation_temperature_ratio(My, k)


def shock_pressure_ratio(Mx, k):
    """Static-pressure ratio across the shock  py/px = (1+k Mx^2)/(1+k My^2) (Eq. 9.54).
    [Moran Eq. 9.54, Sec. 9.14.2, p.581]"""
    My = mach_after_shock(Mx, k)
    return (1.0 + k * Mx * Mx) / (1.0 + k * My * My)


def stagnation_pressure_ratio_across_shock(Mx, k):
    """Stagnation-pressure ratio  poy/pox = (Mx/My)[ (1+(k-1)/2 My^2)/(1+(k-1)/2 Mx^2) ]^E,
    E = (k+1)/(2(k-1)).  Always <= 1 (irreversible loss).  [Moran Eq. 9.56, Sec. 9.14.2, p.581]"""
    My = mach_after_shock(Mx, k)
    E = (k + 1.0) / (2.0 * (k - 1.0))
    base = stagnation_temperature_ratio(My, k) / stagnation_temperature_ratio(Mx, k)
    return (Mx / My) * base ** E


def sonic_area_ratio_across_shock(Mx, k):
    """Ratio of sonic (throat) areas before/after a shock  A*x/A*y = poy/pox (Eq. 9.57).
    [Moran Eq. 9.57, Sec. 9.14.2, p.582]"""
    return stagnation_pressure_ratio_across_shock(Mx, k)


def _demo():
    print("Module 13.3 -- Normal shock (Mx>1 -> My<1; p,T rise; po drops; To fixed)\n")
    k = 1.4
    Mx = 2.0
    print("  Table 9.3 row at Mx = 2.0 (k=1.4):")
    print("     My      = %.5f   [book 0.57735]" % mach_after_shock(Mx, k))
    print("     py/px   = %.4f   [book 4.5000]"  % shock_pressure_ratio(Mx, k))
    print("     Ty/Tx   = %.4f   [book 1.6875]"  % shock_temperature_ratio(Mx, k))
    print("     poy/pox = %.5f   [book 0.72088]" % stagnation_pressure_ratio_across_shock(Mx, k))
    # Example 9.15(d): shock at exit, Mx=2.4, px=6.84 lbf/in^2
    My = mach_after_shock(2.4, k); pr = shock_pressure_ratio(2.4, k)
    print("\n  Ex 9.15(d) shock at exit: Mx=2.4 -> My=%.3f, py/px=%.4f, py=%.2f lbf/in^2"
          % (My, pr, 6.84 * pr))
    print("     [book My=0.52, py/px=6.5533, py=44.82]")
    # Example 9.15(e): shock in diverging section at Mx=2.2
    print("  Ex 9.15(e) shock in diverging duct: Mx=2.2 -> poy/pox=%.5f  [book 0.62812]"
          % stagnation_pressure_ratio_across_shock(2.2, k))


if __name__ == "__main__":
    _demo()
