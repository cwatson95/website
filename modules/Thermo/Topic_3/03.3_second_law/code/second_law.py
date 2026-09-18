"""
second_law.py  —  Module 3.3 (Second Law)

The first law says energy is conserved; the **second law** says energy transfers
have a DIRECTION and that converting heat fully into work is impossible.  Two
classical statements (Moran 8e Sec. 5.2):

  Clausius:        no cycle can have, as its SOLE result, heat flowing from a
                   cooler to a hotter body.                          (p.245)
  Kelvin-Planck:   no cycle exchanging heat with a SINGLE reservoir can deliver
                   net work; analytically  W_cycle <= 0.    (Eq. 5.1/5.3, p.246/254)

Consequences (this module's toolkit):
  * Carnot efficiency  eta_max = 1 - T_C/T_H            (Eq. 5.9)  -- the ceiling
    on any power cycle between two reservoirs;
  * max COPs for refrigerators/heat pumps              (Eqs. 5.10, 5.11);
  * the Kelvin scale itself, fixed by (Q_C/Q_H)_rev = T_C/T_H  (Eq. 5.7).

ALL temperatures here must be ABSOLUTE (K or degR) -- ratios of T are meaningless
otherwise (module 3.1).  Citations: Moran 8e (PDF = printed + 18); see ../refs.md.
"""


def carnot_efficiency(T_C, T_H):
    """Carnot (maximum) thermal efficiency of a power cycle between reservoirs
    T_C < T_H:  eta_max = 1 - T_C/T_H.  T in K or degR. [Moran Eq. 5.9, Sec. 5.9.1, p.265]"""
    return 1.0 - T_C / T_H


def efficiency_from_heat(Q_C, Q_H):
    """Thermal efficiency from heat magnitudes:  eta = 1 - Q_C/Q_H.
    [Moran Eq. 5.4, Sec. 5.4, p.256]  (Equals the Carnot value iff the cycle is reversible.)"""
    return 1.0 - Q_C / Q_H


def kelvin_ratio(T_C, T_H):
    """Reversible cycle between two reservoirs:  (Q_C/Q_H)_rev = T_C/T_H.
    This relation DEFINES the Kelvin scale. [Moran Eq. 5.7, Sec. 5.7, p.262]"""
    return T_C / T_H


def carnot_cop_refrigerator(T_C, T_H):
    """Maximum COP of a refrigeration cycle:  beta_max = T_C/(T_H - T_C).
    [Moran Eq. 5.10, Sec. 5.9.2, p.267]"""
    return T_C / (T_H - T_C)


def carnot_cop_heat_pump(T_C, T_H):
    """Maximum COP of a heat-pump cycle:  gamma_max = T_H/(T_H - T_C).
    Note gamma_max = beta_max + 1. [Moran Eq. 5.11, Sec. 5.9.2, p.267]"""
    return T_H / (T_H - T_C)


def max_work_from_heat(Q_H, T_C, T_H):
    """Most work obtainable from heat Q_H supplied at T_H, rejecting to T_C:
    W_max = eta_carnot * Q_H. [Moran Eqs. 5.9 with 2.42]"""
    return carnot_efficiency(T_C, T_H) * Q_H


def kelvin_planck_allows(W_cycle, single_reservoir=True, tol=1e-12):
    """Kelvin-Planck test: a cycle exchanging heat with a SINGLE reservoir cannot
    produce net positive work, so W_cycle <= 0.  Returns True if allowed.
    [Moran Eq. 5.1 / 5.3, Sec. 5.3.2 / 5.4, p.246 / 254]"""
    if single_reservoir:
        return W_cycle <= tol
    return True  # two or more reservoirs: not constrained by the single-reservoir form


def efficiency_is_possible(eta, T_C, T_H, tol=1e-9):
    """Second-law (Carnot corollary 1) check: any power cycle between T_C,T_H must
    have eta <= eta_carnot (equality only for a reversible cycle).  Returns True if
    the claimed eta is allowed. [Moran Sec. 5.5, p.257]"""
    return eta <= carnot_efficiency(T_C, T_H) + tol


def _demo():
    print("Module 3.3 -- Second Law  (T must be ABSOLUTE; Carnot bounds)\n")
    print("  Carnot efficiency:")
    print("    T_H=745 K, T_C=298 K -> eta_max = %.2f   [book 60%%]"
          % carnot_efficiency(298.0, 745.0))
    print("    T_H=2000 K, T_C=400 K -> eta_max = %.2f  [book 80%%]"
          % carnot_efficiency(400.0, 2000.0))
    print("\n  Max COP (T_C=250 K, T_H=300 K):")
    print("    refrigerator beta_max = %.1f ;  heat pump gamma_max = %.1f  (gamma = beta + 1)"
          % (carnot_cop_refrigerator(250.0, 300.0), carnot_cop_heat_pump(250.0, 300.0)))
    print("\n  Kelvin-Planck (single reservoir):")
    print("    W_cycle = -50 allowed?", kelvin_planck_allows(-50.0))
    print("    W_cycle = +50 allowed?", kelvin_planck_allows(+50.0), " (would violate 2nd law)")
    print("\n  Claimed power cycle eta=0.65 between 745/298 K possible?",
          efficiency_is_possible(0.65, 298.0, 745.0), "(Carnot ceiling is 0.60)")


if __name__ == "__main__":
    _demo()
