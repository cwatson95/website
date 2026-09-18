"""
carnot_cycle.py  —  Module 09.1 (Carnot Cycle)

The Carnot cycle is the REVERSIBLE BENCHMARK against which every cycle in Topic 9
is measured.  It consists of four internally reversible processes -- two adiabatic
processes alternated with two isothermal processes (Moran 8e Sec. 5.10):

  Power cycle (Fig. 5.13/5.14):
    1-2  adiabatic compression  (T_C -> T_H)
    2-3  isothermal expansion at T_H   (receives Q_H from the hot reservoir)
    3-4  adiabatic expansion    (T_H -> T_C)
    4-1  isothermal compression at T_C (rejects Q_C to the cold reservoir)

Its thermal efficiency is given by Eq. 5.9 (Sec. 5.10.1):

  eta_max = 1 - T_C/T_H                                (Eq. 5.9)

the MAXIMUM efficiency any power cycle can have between two reservoirs.  Reversed,
the same cycle is a refrigerator/heat pump with the best possible COPs (Sec. 5.10.2):

  beta_max  = T_C/(T_H - T_C)                          (Eq. 5.10)   refrigerator
  gamma_max = T_H/(T_H - T_C)                          (Eq. 5.11)   heat pump   [= beta_max + 1]

ALL temperatures here must be ABSOLUTE (K or degR) -- ratios of T are meaningless
otherwise (module 3.1).  Same carnot_* functions as modules 3.3 and 07.1; here they
serve as the ceiling for the Otto/Diesel/dual/Brayton/Rankine cycles (09.2-09.6).
Citations: Moran 8e (PDF = printed + 18); see ../refs.md.
"""


def carnot_efficiency(T_C, T_H):
    """Carnot (maximum) thermal efficiency of a power cycle between reservoirs
    T_C < T_H:  eta_max = 1 - T_C/T_H.  T in K or degR. [Moran Eq. 5.9, Sec. 5.10.1, p.271]"""
    return 1.0 - T_C / T_H


def carnot_efficiency_from_heat(Q_C, Q_H):
    """Carnot efficiency from the reversible heat magnitudes:  eta = 1 - Q_C/Q_H,
    where (Q_C/Q_H)_rev = T_C/T_H (Eq. 5.7). [Moran Eq. 5.4 with 5.7, Sec. 5.9.1, p.265]"""
    return 1.0 - Q_C / Q_H


def carnot_cop_refrigerator(T_C, T_H):
    """Maximum COP of a (Carnot) refrigeration cycle:  beta_max = T_C/(T_H - T_C).
    [Moran Eq. 5.10, Sec. 5.9.2 / 5.10.2, p.267]"""
    return T_C / (T_H - T_C)


def carnot_cop_heat_pump(T_C, T_H):
    """Maximum COP of a (Carnot) heat-pump cycle:  gamma_max = T_H/(T_H - T_C).
    Note gamma_max = beta_max + 1. [Moran Eq. 5.11, Sec. 5.9.2 / 5.10.2, p.267]"""
    return T_H / (T_H - T_C)


def max_work_from_heat(Q_H, T_C, T_H):
    """Most work obtainable from heat Q_H supplied at T_H, rejecting to T_C:
    W_max = eta_carnot * Q_H. [Moran Eq. 5.9, Sec. 5.10.1, p.271]"""
    return carnot_efficiency(T_C, T_H) * Q_H


def min_work_heat_pump(Q_H, T_C, T_H):
    """Least work input to deliver Q_H with a heat pump between T_C, T_H:
    W_min = Q_H/gamma_max. [Moran Eq. 5.11, Sec. 5.10.2, p.270]"""
    return Q_H / carnot_cop_heat_pump(T_C, T_H)


def efficiency_is_possible(eta, T_C, T_H, tol=1e-9):
    """Second-law (Carnot corollary) check: ANY power cycle between T_C, T_H -- Otto,
    Diesel, Brayton, Rankine, ... -- must have eta <= eta_carnot (equality only for a
    reversible cycle).  Returns True if the claimed eta is allowed.
    [Moran Sec. 5.10.3, p.273]"""
    return eta <= carnot_efficiency(T_C, T_H) + tol


def _demo():
    print("Module 09.1 -- Carnot Cycle  (the reversible ceiling for all of Topic 9)\n")
    print("  Carnot power-cycle efficiency  eta_max = 1 - T_C/T_H:")
    print("    T_H=2000 K, T_C=400 K -> eta_max = %.2f   [Ex 5.1, book 80%%]"
          % carnot_efficiency(400.0, 2000.0))
    print("    T_H=745 K,  T_C=298 K -> eta_max = %.2f   [module 3.3, book 60%%]"
          % carnot_efficiency(298.0, 745.0))
    print("\n  Carnot COPs (reverse the cycle):")
    print("    refrigerator beta_max(T_C=268 K, T_H=295 K) = %.1f   [Ex 5.2, book 9.9]"
          % carnot_cop_refrigerator(268.0, 295.0))
    print("    heat pump  gamma_max(T_C=492 degR, T_H=530 degR) = %.2f  [Ex 5.3, book 13.95]"
          % carnot_cop_heat_pump(492.0, 530.0))
    print("\n  As the ceiling: a real Otto cycle at r=8 has eta=0.565 (module 09.2);")
    print("    is 0.565 possible between 2000/400 K?  ",
          efficiency_is_possible(0.565, 400.0, 2000.0), "(ceiling 0.80)")
    print("    is a claimed 0.85 possible?            ",
          efficiency_is_possible(0.85, 400.0, 2000.0), "(exceeds 0.80 -> impossible)")


if __name__ == "__main__":
    _demo()
