"""
efficiency.py  —  Module 07.1 (Performance Metrics: Efficiency)

ONE structured toolkit for every performance metric in Moran 8e.  The metrics fall
into three families; the second-law CEILINGS (Carnot) bound the first family, and the
ISENTROPIC efficiencies rate single devices against a reversible-adiabatic ideal.

  THERMAL EFFICIENCY -- power cycle (Sec. 2.6.2)
    eta = W_cycle / Q_in = 1 - Q_out/Q_in              (Eqs. 2.42, 2.43)
  COEFFICIENTS OF PERFORMANCE (Sec. 2.6.3)
    refrigerator   beta  = Q_C / W_cycle               (Eq. 2.45)
    heat pump      gamma = Q_H / W_cycle               (Eq. 2.47)    [gamma = beta + 1]
  CARNOT CEILINGS -- two reservoirs (Sec. 5.9) -- best ANY cycle can do
    eta_max   = 1 - T_C/T_H                            (Eq. 5.9)     [cf. module 3.3]
    beta_max  = T_C/(T_H - T_C)                        (Eq. 5.10)
    gamma_max = T_H/(T_H - T_C)                        (Eq. 5.11)    [gamma_max = beta_max + 1]
  ISENTROPIC (device) EFFICIENCIES -- actual vs. reversible-adiabatic (Sec. 6.12)
    turbine      eta_t = (h1 - h2)/(h1 - h2s)          (Eq. 6.46)    [cf. Topic 6 isentropic]
    nozzle       eta_n = (V2^2/2)/(V2^2/2)_s           (Eq. 6.47)
    compressor   eta_c = (h2s - h1)/(h2 - h1)          (Eq. 6.48)    (pump: same form)

CONVENTIONS.  Cycle metrics take Q_in, Q_out, Q_C, Q_H, W_cycle as POSITIVE magnitudes
(Moran's cycle sign convention, Sec. 2.6.1).  Carnot temperatures must be ABSOLUTE
(K or degR) -- ratios of T are meaningless otherwise (module 3.1).  Each isentropic
efficiency compares the actual device with the ideal having the SAME inlet state and
the SAME exit pressure.  Citations: Moran 8e (PDF = printed + 18); see ../refs.md.
"""


# ---- thermal efficiency of a power cycle (Sec. 2.6.2) ----------------------
def thermal_efficiency(W_cycle, Q_in):
    """Thermal efficiency of a power cycle:  eta = W_cycle / Q_in.
    [Moran Eq. 2.42, Sec. 2.6.2, p.74]"""
    return W_cycle / Q_in


def thermal_efficiency_from_heat(Q_in, Q_out):
    """Thermal efficiency from heat magnitudes:  eta = 1 - Q_out/Q_in  (uses Eq. 2.41).
    [Moran Eq. 2.43, Sec. 2.6.2, p.74]"""
    return 1.0 - Q_out / Q_in


# ---- coefficients of performance (Sec. 2.6.3) -----------------------------
def cop_refrigerator(Q_C, W_cycle):
    """COP of a refrigeration cycle:  beta = Q_C / W_cycle  (Q_C = heat from cold body).
    [Moran Eq. 2.45, Sec. 2.6.3, p.75]"""
    return Q_C / W_cycle


def cop_refrigerator_from_heat(Q_C, Q_H):
    """COP refrigerator from heat magnitudes:  beta = Q_C/(Q_H - Q_C)  (uses Eq. 2.44).
    [Moran Eq. 2.46, Sec. 2.6.3, p.75]"""
    return Q_C / (Q_H - Q_C)


def cop_heat_pump(Q_H, W_cycle):
    """COP of a heat-pump cycle:  gamma = Q_H / W_cycle  (Q_H = heat to hot body).
    [Moran Eq. 2.47, Sec. 2.6.3, p.75]"""
    return Q_H / W_cycle


def cop_heat_pump_from_heat(Q_C, Q_H):
    """COP heat pump from heat magnitudes:  gamma = Q_H/(Q_H - Q_C)  (uses Eq. 2.44).
    Note gamma = beta + 1 for the same cycle. [Moran Eq. 2.48, Sec. 2.6.3, p.75]"""
    return Q_H / (Q_H - Q_C)


# ---- Carnot ceilings, two reservoirs (Sec. 5.9) ---------------------------
def carnot_efficiency(T_C, T_H):
    """Carnot (maximum) thermal efficiency between reservoirs T_C < T_H:
    eta_max = 1 - T_C/T_H.  T ABSOLUTE (K or degR). [Moran Eq. 5.9, Sec. 5.9.1, p.265]"""
    return 1.0 - T_C / T_H


def carnot_cop_refrigerator(T_C, T_H):
    """Maximum COP of a refrigeration cycle:  beta_max = T_C/(T_H - T_C).
    [Moran Eq. 5.10, Sec. 5.9.2, p.267]"""
    return T_C / (T_H - T_C)


def carnot_cop_heat_pump(T_C, T_H):
    """Maximum COP of a heat-pump cycle:  gamma_max = T_H/(T_H - T_C).
    Note gamma_max = beta_max + 1. [Moran Eq. 5.11, Sec. 5.9.2, p.267]"""
    return T_H / (T_H - T_C)


# ---- isentropic (device) efficiencies (Sec. 6.12) -------------------------
def isentropic_turbine_efficiency(h1, h2, h2s):
    """Isentropic turbine efficiency:  eta_t = (h1 - h2)/(h1 - h2s)  (actual / ideal
    work, same inlet state & exit pressure).  Typically 0.7-0.9.
    [Moran Eq. 6.46, Sec. 6.12.1, p.333]"""
    return (h1 - h2) / (h1 - h2s)


def turbine_work_actual(eta_t, h1, h2s):
    """Actual turbine work per unit mass from the isentropic efficiency:
    w = eta_t (h1 - h2s).  Rearrangement of Eq. 6.46. [Moran Sec. 6.12.1, p.334]"""
    return eta_t * (h1 - h2s)


def isentropic_nozzle_efficiency(ke2, ke2s):
    """Isentropic nozzle efficiency:  eta_n = (V2^2/2)/(V2^2/2)_s  (actual / ideal exit
    kinetic energy, same inlet state & exit pressure).  Often >= 0.95.
    [Moran Eq. 6.47, Sec. 6.12.2, p.335]"""
    return ke2 / ke2s


def nozzle_exit_ke(h1, h2, ke1=0.0):
    """Adiabatic-nozzle exit kinetic energy from the energy balance (Eq. 4.21):
    V2^2/2 = (h1 - h2) + V1^2/2.  Use with isentropic_nozzle_efficiency.
    [Moran Sec. 6.12.2, p.336]"""
    return (h1 - h2) + ke1


def isentropic_compressor_efficiency(h1, h2, h2s):
    """Isentropic compressor efficiency:  eta_c = (h2s - h1)/(h2 - h1)  (ideal / actual
    work input, same inlet state & exit pressure).  Typically 0.75-0.85.
    [Moran Eq. 6.48, Sec. 6.12.3, p.338]"""
    return (h2s - h1) / (h2 - h1)


def isentropic_pump_efficiency(h1, h2, h2s):
    """Isentropic pump efficiency -- same form as the compressor (Eq. 6.48):
    eta_p = (h2s - h1)/(h2 - h1). [Moran Sec. 6.12.3, p.338]"""
    return (h2s - h1) / (h2 - h1)


def compressor_work_actual(eta_c, h1, h2s):
    """Actual compressor work input per unit mass from the isentropic efficiency:
    w_in = (h2s - h1)/eta_c.  Rearrangement of Eq. 6.48. [Moran Sec. 6.12.3, p.338]"""
    return (h2s - h1) / eta_c


# ---- second-law check (Carnot is the ceiling) -----------------------------
def efficiency_is_possible(eta, T_C, T_H, tol=1e-9):
    """A power cycle between T_C, T_H must have eta <= eta_carnot (equality only if
    reversible).  Returns True if the claimed eta is allowed. [Moran Sec. 5.9.1, p.265]"""
    return eta <= carnot_efficiency(T_C, T_H) + tol


def _demo():
    print("Module 07.1 -- Efficiency  (all performance metrics; Carnot bounds the cycles)\n")
    print("  Thermal efficiency (power cycle):")
    print("    Q_in=1000, Q_out=200 kJ -> eta = %.2f          [Ex 5.1c]"
          % thermal_efficiency_from_heat(1000.0, 200.0))
    print("    Carnot ceiling at T_H=2000 K, T_C=400 K -> eta_max = %.2f  [Ex 5.1, 80%%]"
          % carnot_efficiency(400.0, 2000.0))
    print("\n  Coefficients of performance:")
    print("    Refrigerator  beta  = 8000/3200 = %.1f ; beta_max(268,295 K) = %.1f  [Ex 5.2]"
          % (cop_refrigerator(8000.0, 3200.0), carnot_cop_refrigerator(268.0, 295.0)))
    print("    Heat pump     gamma_max(492,530 degR) = %.2f                     [Ex 5.3]"
          % carnot_cop_heat_pump(492.0, 530.0))
    print("\n  Isentropic (device) efficiencies:")
    print("    Turbine  work = eta_t(h1-h2s) = 0.75(3105.6-2743.0) = %.2f kJ/kg [Ex 6.11]"
          % turbine_work_actual(0.75, 3105.6, 2743.0))
    print("    Compressor eta_c(249.75,294.17,285.58) = %.2f                  [Ex 6.14, 81%%]"
          % isentropic_compressor_efficiency(249.75, 294.17, 285.58))
    print("\n  Second law: claimed power-cycle eta=0.85 between 2000/400 K possible?",
          efficiency_is_possible(0.85, 400.0, 2000.0), "(ceiling 0.80)")


if __name__ == "__main__":
    _demo()
