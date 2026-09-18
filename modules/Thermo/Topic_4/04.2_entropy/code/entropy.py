"""
entropy.py  —  Module 4.2 (Entropy)

Because the cyclic integral of (dQ/T) is path-independent for internally reversible
processes (Clausius inequality), it defines a property: **entropy** S, with
dS = (dQ/T)_int,rev (Moran 8e Eq. 6.2, Sec. 6.1).  This module is the toolkit that
turns entropy into numbers:

  * the two T dS equations            T ds = du + p dv   (Eq. 6.10a)
                                      T ds = dh - v dp   (Eq. 6.10b)
  * closed-form entropy change for an incompressible substance (Eq. 6.13) and an
    ideal gas (gas-table form Eq. 6.20a; constant-cv Eq. 6.21; constant-cp Eq. 6.22)
  * the two-phase mixture form        s = sf + x sfg     (Eq. 6.4)
  * heat as an area under T-S          Q_int,rev = ∫ T dS (Eq. 6.23)
  * the closed-system ENTROPY BALANCE  S2 - S1 = ∫(dQ/Tb) + sigma,  sigma >= 0 (Eq. 6.24)

sigma is the entropy PRODUCED by irreversibilities -- it is NOT a property (two
processes with the same end states can have different sigma; see Ex 6.1 vs 6.2).
Units: s [kJ/kg.K], T [K], R/cp/cv [kJ/kg.K].  Citations: Moran 8e (PDF = printed + 18).
"""
import math


def entropy_mixture(sf, sg, x):
    """Two-phase entropy  s = sf + x (sg - sf) = sf + x sfg. [Moran Eq. 6.4, Sec. 6.2.2, p.294]"""
    return sf + x * (sg - sf)


def du_from_tds(T, ds, p, dv):
    """1st T dS equation, solved for du:  du = T ds - p dv. [Moran Eq. 6.10a, Sec. 6.3, p.297]"""
    return T * ds - p * dv


def dh_from_tds(T, ds, v, dp):
    """2nd T dS equation, solved for dh:  dh = T ds + v dp. [Moran Eq. 6.10b, Sec. 6.3, p.297]"""
    return T * ds + v * dp


def entropy_change_incompressible(c, T1, T2):
    """Incompressible substance:  s2 - s1 = c ln(T2/T1)  [kJ/kg.K].
    [Moran Eq. 6.13, Sec. 6.4, p.298]"""
    return c * math.log(T2 / T1)


def entropy_change_ideal_gas_tables(s0_T1, s0_T2, R, p1, p2):
    """Ideal gas via gas tables:  s2 - s1 = s0(T2) - s0(T1) - R ln(p2/p1).
    [Moran Eq. 6.20a, Sec. 6.5.1, p.300]"""
    return s0_T2 - s0_T1 - R * math.log(p2 / p1)


def entropy_change_ideal_gas_cp(cp, R, T1, T2, p1, p2):
    """Ideal gas, constant cp:  s2 - s1 = cp ln(T2/T1) - R ln(p2/p1).
    [Moran Eq. 6.22, Sec. 6.5.2, p.301]"""
    return cp * math.log(T2 / T1) - R * math.log(p2 / p1)


def entropy_change_ideal_gas_cv(cv, R, T1, T2, v1, v2):
    """Ideal gas, constant cv:  s2 - s1 = cv ln(T2/T1) + R ln(v2/v1).
    [Moran Eq. 6.21, Sec. 6.5.2, p.301]"""
    return cv * math.log(T2 / T1) + R * math.log(v2 / v1)


def heat_isothermal_rev(T, dS):
    """Internally reversible ISOTHERMAL heat transfer  Q = T (S2 - S1) = ∫ T dS.
    [Moran Eq. 6.23, Sec. 6.6.1, p.302]"""
    return T * dS


def entropy_production_closed(S2, S1, Q_over_Tb=0.0):
    """Entropy produced (closed system):  sigma = (S2 - S1) - ∫(dQ/Tb).
    For an ADIABATIC process the transfer term is 0, so sigma = S2 - S1.
    [Moran Eq. 6.24, Sec. 6.7, p.305]"""
    return (S2 - S1) - Q_over_Tb


def process_allowed(sigma, tol=1e-9):
    """2nd law: a real process must have sigma >= 0 (= 0 only if internally reversible).
    Returns True if allowed. [Moran Sec. 6.7, p.305; sign rule Eq. 6.27, p.307]"""
    return sigma >= -tol


def _demo():
    print("Module 4.2 -- Entropy  (sigma >= 0; sigma is NOT a property)\n")
    # The Ex 6.1 / 6.2 pair: SAME end states (sat liq -> sat vap, water @150 C, 423.15 K)
    T = 423.15; s1, s2 = 1.8418, 6.8379
    print("  Water sat.liquid -> sat.vapor @150 C:  ds = s2 - s1 = %.4f kJ/kg.K (a PROPERTY)" % (s2 - s1))
    print("  Ex 6.1 internally reversible: Q/m = T ds = %.1f kJ/kg, W/m = +186.38 kJ/kg, sigma = 0"
          % heat_isothermal_rev(T, s2 - s1))
    sig = entropy_production_closed(s2, s1, 0.0)   # Ex 6.2 adiabatic: sigma = ds
    print("  Ex 6.2 adiabatic + paddle:    W/m = -1927.82 kJ/kg, sigma/m = ds = %.4f kJ/kg.K (> 0)" % sig)
    print("  -> same ds, but sigma = 0 vs %.3f: entropy production depends on the PATH.\n" % sig)
    # Ideal-gas entropy change (HW 6.11): air 300 K/100 kPa -> 500 K/650 kPa
    ds = entropy_change_ideal_gas_tables(1.70203, 2.21952, 0.287, 100.0, 650.0)
    print("  HW 6.11 air (table form): ds = %.4f kJ/kg.K  [book -0.0197]  (same whether rev or irrev)" % ds)


if __name__ == "__main__":
    _demo()
