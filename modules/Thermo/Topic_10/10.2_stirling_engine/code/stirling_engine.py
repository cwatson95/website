"""
stirling_engine.py  —  Module 10.2 (Stirling Engine)

The Stirling cycle is a reversible power cycle of FOUR internally reversible
processes in series, employing a REGENERATOR (Moran 8e Sec. 9.8.4):

  Process 1-2: isothermal compression at T_C          (rejects Q_12 to surroundings)
  Process 2-3: constant-volume heating  T_C -> T_H     (heat from the regenerator)
  Process 3-4: isothermal expansion at T_H            (receives Q_34 from the source)
  Process 4-1: constant-volume cooling  T_H -> T_C     (heat to the regenerator)

i.e. two isothermals alternated with two constant-volume regenerative processes.

THE REGENERATOR.  With effectiveness 100%, the heat rejected during the
constant-volume cooling 4-1 is stored and returned as the heat input for the
constant-volume heating 2-3.  These two equal-and-opposite internal transfers
(Q = c_v (T_H - T_C)) then cancel, so ALL external heat addition occurs in the
isothermal expansion at T_H and ALL external heat rejection in the isothermal
compression at T_C.  The cycle is then equivalent to two reservoirs and reaches
the CARNOT efficiency (Moran p.552-553):

  eta = 1 - T_C/T_H            (same expression as Carnot, Eq. 5.9)

Without the regenerator the constant-volume heating must be supplied externally
too, so eta drops well below the Carnot value.  This module quantifies both
limits, the per-process heats (isothermal Q = m R T ln(V2/V1)), the regenerator
heat it shuttles, and the regenerator effectiveness (Eq. 9.27).

ALL temperatures ABSOLUTE (K or degR).  Citations: Moran 8e (PDF = printed + 18);
see ../refs.md.
"""
import math


def stirling_efficiency(T_C, T_H):
    """Ideal Stirling thermal efficiency (100% regeneration) -- equals the Carnot
    value: eta = 1 - T_C/T_H.  T absolute.
    [Moran Sec. 9.8.4, p.552-553; Eq. 5.9, p.265]"""
    return 1.0 - T_C / T_H


def isothermal_heat(R, T, V_ratio):
    """Heat transfer in an internally reversible ISOTHERMAL process of an ideal gas,
    per unit mass: Q = W = R T ln(V_ratio), with V_ratio = V_out/V_in (du = 0).
    [Moran Eq. 2.17 with ideal-gas law; cf. Example 2.1(b), p.49 / 51]"""
    return R * T * math.log(V_ratio)


def stirling_heat_added(R, T_H, r):
    """External heat added per unit mass -- the isothermal expansion 3-4 at T_H:
    Q_34 = R T_H ln(r), where r = V_max/V_min is the volume (compression) ratio.
    [Moran Sec. 9.8.4, p.552; Eq. 2.17, p.49]"""
    return isothermal_heat(R, T_H, r)


def stirling_heat_rejected(R, T_C, r):
    """Heat rejected per unit mass -- the isothermal compression 1-2 at T_C
    (magnitude): Q_12 = R T_C ln(r).  [Moran Sec. 9.8.4, p.552; Eq. 2.17, p.49]"""
    return isothermal_heat(R, T_C, r)


def stirling_net_work(R, T_H, T_C, r):
    """Net work per unit mass: W = Q_34 - Q_12 = R (T_H - T_C) ln(r).
    (A regenerator does not change the net work.)  [Moran Sec. 9.8.4, p.552]"""
    return stirling_heat_added(R, T_H, r) - stirling_heat_rejected(R, T_C, r)


def regenerator_heat(c_v, T_H, T_C):
    """Heat per unit mass shuttled internally by an ideal regenerator -- the
    constant-volume processes 4-1 (out) and 2-3 (in): Q = c_v (T_H - T_C).
    [Moran Sec. 9.8.4, p.552; constant-volume ideal gas Eq. 3.50, p.140]"""
    return c_v * (T_H - T_C)


def stirling_efficiency_no_regen(R, c_v, T_H, T_C, r):
    """Stirling efficiency with NO regenerator: the constant-volume heating 2-3 must
    also be supplied externally, so eta = W / (Q_34 + c_v(T_H - T_C)) < Carnot.
    [Moran Sec. 9.8.4, p.552 (role of the regenerator)]"""
    W = stirling_net_work(R, T_H, T_C, r)
    Q_in = stirling_heat_added(R, T_H, r) + regenerator_heat(c_v, T_H, T_C)
    return W / Q_in


def regenerator_effectiveness(h_x, h_2, h_4):
    """Regenerator effectiveness: ratio of actual to maximum enthalpy increase,
    eta_reg = (h_x - h_2)/(h_4 - h_2).  Ideal regeneration -> h_x = h_4 -> 1 (100%).
    [Moran Eq. 9.27, Sec. 9.7, p.539]"""
    return (h_x - h_2) / (h_4 - h_2)


def _demo():
    R, cv = 0.287, 0.718                 # air, kJ/kg.K
    T_H, T_C, r = 1000.0, 300.0, 2.0
    print("Module 10.2 -- Stirling Engine  (2 isothermals + 2 constant-volume, regenerated)\n")
    print("  Ideal Stirling (100%% regeneration), T_H=1000 K, T_C=300 K:")
    print("    eta = 1 - T_C/T_H = %.2f   == Carnot ceiling" % stirling_efficiency(T_C, T_H))
    print("\n  Air, r = V_max/V_min = 2 (per unit mass, kJ/kg):")
    print("    Q_34 added at T_H   = %.1f" % stirling_heat_added(R, T_H, r))
    print("    Q_12 rejected at T_C= %.1f" % stirling_heat_rejected(R, T_C, r))
    print("    W_net               = %.1f" % stirling_net_work(R, T_H, T_C, r))
    print("    eta = W/Q_34        = %.2f" %
          (stirling_net_work(R, T_H, T_C, r) / stirling_heat_added(R, T_H, r)))
    print("\n  The regenerator shuttles Q = c_v(T_H-T_C) = %.1f kJ/kg internally."
          % regenerator_heat(cv, T_H, T_C))
    print("    WITHOUT a regenerator that heat is external -> eta = %.3f  (<< 0.70!)"
          % stirling_efficiency_no_regen(R, cv, T_H, T_C, r))
    print("\n  Regenerator effectiveness (h2=300,h4=800): actual h_x=700 -> %.2f ; ideal h_x=h4 -> %.2f"
          % (regenerator_effectiveness(700.0, 300.0, 800.0),
             regenerator_effectiveness(800.0, 300.0, 800.0)))


if __name__ == "__main__":
    _demo()
