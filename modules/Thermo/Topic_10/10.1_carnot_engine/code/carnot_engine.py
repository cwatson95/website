"""
carnot_engine.py  —  Module 10.1 (Carnot Engine)

The Carnot cycle is the reversible power cycle operating between two thermal
reservoirs.  It consists of FOUR internally reversible processes (Moran 8e
Sec. 5.10):

  Process 1-2: adiabatic (isentropic) compression  T_C -> T_H
  Process 2-3: isothermal expansion at T_H, receiving Q_H from the hot reservoir
  Process 3-4: adiabatic (isentropic) expansion    T_H -> T_C
  Process 4-1: isothermal compression at T_C, discharging Q_C to the cold reservoir

i.e. two isothermals alternated with two isentropics.  Run in reverse it is the
Carnot refrigeration / heat pump cycle (Sec. 5.10.2).

Because it is reversible, its thermal efficiency is the CEILING for any power
cycle between the same two reservoirs (Carnot corollaries, Topic 3 module 3.3):

  eta_max = 1 - T_C/T_H            (Eq. 5.9)  -- the Carnot efficiency.

This module gives the engine's numerics: Carnot efficiency, the reversible
heat-ratio (Eq. 5.7), net work, the reversible refrigerator/heat-pump COPs
(Eqs. 5.10, 5.11), and the corollary test that classifies a claimed cycle as
reversible / irreversible / impossible (Example 5.1).

ALL temperatures must be ABSOLUTE (K or degR) -- T ratios are otherwise
meaningless.  Citations: Moran 8e (PDF = printed + 18); see ../refs.md.
"""


def carnot_efficiency(T_C, T_H):
    """Carnot (maximum) thermal efficiency of a power cycle between reservoirs
    T_C < T_H:  eta_max = 1 - T_C/T_H.  T in K or degR.
    [Moran Eq. 5.9, Sec. 5.9.1, p.265]"""
    return 1.0 - T_C / T_H


def thermal_efficiency(W_cycle, Q_H):
    """Thermal efficiency of any power cycle: eta = W_cycle / Q_H.
    [Moran Eq. 2.42, Sec. 2.6, p.74]"""
    return W_cycle / Q_H


def efficiency_from_heats(Q_C, Q_H):
    """Thermal efficiency from heat magnitudes: eta = 1 - Q_C/Q_H
    (since W_cycle = Q_H - Q_C).  Equals the Carnot value iff reversible.
    [Moran Eq. 5.4, Sec. 5.4, p.256]"""
    return 1.0 - Q_C / Q_H


def kelvin_heat_ratio(T_C, T_H):
    """Reversible cycle between two reservoirs: (Q_C/Q_H)_rev = T_C/T_H.
    This relation defines the Kelvin scale and fixes the Carnot heats.
    [Moran Eq. 5.7, Sec. 5.7, p.262]"""
    return T_C / T_H


def carnot_heat_rejected(Q_H, T_C, T_H):
    """Heat the reversible (Carnot) cycle must reject for heat input Q_H:
    Q_C = Q_H * (T_C/T_H).  [Moran Eq. 5.7, Sec. 5.7, p.262]"""
    return Q_H * kelvin_heat_ratio(T_C, T_H)


def carnot_work(Q_H, T_C, T_H):
    """Net work of a Carnot power cycle: W = Q_H - Q_C = eta_max * Q_H.
    [Moran Eqs. 5.9 with 2.42, p.265 / 74]"""
    return carnot_efficiency(T_C, T_H) * Q_H


def cycle_status(eta, T_C, T_H, tol=1e-9):
    """Classify a power cycle by the Carnot corollaries (Example 5.1, p.266):
    'impossible' if eta > eta_max, 'reversible' if eta == eta_max, else
    'irreversible'.  [Moran Sec. 5.9.1, p.265-266]"""
    eta_max = carnot_efficiency(T_C, T_H)
    if eta > eta_max + tol:
        return "impossible"
    if eta > eta_max - tol:
        return "reversible"
    return "irreversible"


def carnot_cop_refrigerator(T_C, T_H):
    """Carnot refrigeration-cycle COP (Carnot cycle run in reverse):
    beta_max = T_C/(T_H - T_C).  [Moran Eq. 5.10, Sec. 5.9.2 / 5.10.2, p.267 / 272]"""
    return T_C / (T_H - T_C)


def carnot_cop_heat_pump(T_C, T_H):
    """Carnot heat-pump-cycle COP: gamma_max = T_H/(T_H - T_C).
    Note gamma_max = beta_max + 1.  [Moran Eq. 5.11, Sec. 5.9.2 / 5.10.2, p.267 / 272]"""
    return T_H / (T_H - T_C)


def _demo():
    print("Module 10.1 -- Carnot Engine  (reversible cycle: 2 isothermals + 2 isentropics)\n")
    print("  Carnot efficiency (Eq. 5.9):")
    print("    T_H=2000 K, T_C=400 K -> eta_max = %.2f   [Ex 5.1: 80%%]"
          % carnot_efficiency(400.0, 2000.0))
    print("    T_H=745 K,  T_C=298 K -> eta_max = %.2f   [book: 60%%]"
          % carnot_efficiency(298.0, 745.0))
    print("\n  Example 5.1 (Q_H=1000 kJ, T_H=2000 K, T_C=400 K; eta_max=0.80):")
    print("    (a) eta=0.60 ->", cycle_status(0.60, 400.0, 2000.0))
    print("    (b) W=850 kJ -> eta=%.2f ->" % thermal_efficiency(850.0, 1000.0),
          cycle_status(thermal_efficiency(850.0, 1000.0), 400.0, 2000.0))
    print("    (c) Q_C=200 kJ -> eta=%.2f ->" % efficiency_from_heats(200.0, 1000.0),
          cycle_status(efficiency_from_heats(200.0, 1000.0), 400.0, 2000.0))
    print("\n  Carnot cycle heats/work (Q_H=1000 kJ): Q_C=%.0f kJ, W=%.0f kJ"
          % (carnot_heat_rejected(1000.0, 400.0, 2000.0), carnot_work(1000.0, 400.0, 2000.0)))
    print("\n  Reversed Carnot cycle COPs (T_C=268 K, T_H=295 K):")
    print("    refrigerator beta_max = %.1f ;  heat pump gamma_max = %.1f"
          % (carnot_cop_refrigerator(268.0, 295.0), carnot_cop_heat_pump(268.0, 295.0)))


if __name__ == "__main__":
    _demo()
