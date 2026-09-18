"""
reversible.py  —  Module 6.1 (Reversible & Internally Reversible Processes)

A process is REVERSIBLE if the system and ALL parts of its surroundings can be exactly
restored to their initial states (Moran 8e Sec. 5.3.3).  It is INTERNALLY REVERSIBLE if
there are no irreversibilities WITHIN the system (Sec. 5.3.4); irreversibilities may
still reside in the surroundings.  An internally reversible process is a quasi-equilibrium
process -- a series of equilibrium states -- and is the limiting ideal of an actual
process as friction, finite-DeltaT heat transfer, etc. are reduced toward zero.

For a closed system undergoing an INTERNALLY REVERSIBLE process the entropy change is
linked to heat transfer by (Sec. 6.6):

    dS = (dQ/T)_int rev                       (Eq. 6.2b)
    Q_int rev = integral_1^2 T dS             (Eq. 6.23)

so the heat transfer is the AREA UNDER the path on a temperature-entropy (T-s) diagram
(T in kelvin or rankine).  For an internally reversible process NO entropy is produced
within the system: sigma = 0.  An adiabatic (Q = 0) internally reversible process is
therefore a constant-entropy = ISENTROPIC process.

Units: T [K or degR]; S, s [kJ/K, kJ/kg.K]; Q [kJ]; for work_const_pressure use p [kPa]
and v [m^3/kg] -> W [kJ/kg]  (kPa.m^3 = kJ).
Citations: Moran 8e (PDF = printed + 18).  Worked Example 6.1 (internally reversible
process of water): W/m = 186.38 kJ/kg, Q/m = 2114.1 kJ/kg.
"""


def entropy_change_int_rev(Q, T):
    """Entropy change accompanying heat transfer in an isothermal internally reversible
    process:  dS = (dQ/T)_int rev  ->  Q/T.  [Moran Eq. 6.2b, Sec. 6.6, p.302]"""
    return Q / T


def heat_int_rev_isothermal(T, s2, s1):
    """Heat transfer of an ISOTHERMAL internally reversible process (T constant):
    Q = integral T dS = T (s2 - s1).  [Moran Eq. 6.23, Sec. 6.6.1, p.302]"""
    return T * (s2 - s1)


def heat_int_rev_area(T_pts, s_pts):
    """Heat transfer of an internally reversible process as the AREA under the path on a
    T-s diagram:  Q = integral T dS, evaluated by the trapezoidal rule over the supplied
    (s, T) points.  T must be absolute (K or degR).  [Moran Eq. 6.23, Sec. 6.6.1, p.302]"""
    Q = 0.0
    for i in range(len(s_pts) - 1):
        Q += 0.5 * (T_pts[i] + T_pts[i + 1]) * (s_pts[i + 1] - s_pts[i])
    return Q


def work_const_pressure(p, v2, v1):
    """Work of a constant-pressure (internally reversible) process:
    W = integral p dV = p (v2 - v1).  With p [kPa], v [m^3/kg] -> W [kJ/kg].
    [Moran Sec. 6.6.3, Ex. 6.1, p.304]"""
    return p * (v2 - v1)


def sigma_internally_reversible():
    """Entropy produced within an internally reversible process is zero: sigma = 0.
    [Moran Eq. 6.26 (equality case), Sec. 6.7, p.307]"""
    return 0.0


def is_isentropic(Q, internally_reversible, tol=1e-9):
    """An ADIABATIC (Q = 0) internally reversible process is ISENTROPIC (constant
    entropy).  Returns True iff Q ~ 0 and the process is internally reversible.
    [Moran Sec. 6.6, p.302]"""
    return abs(Q) <= tol and bool(internally_reversible)


def carnot_eff_ts(T_hot, T_cold):
    """Thermal efficiency of a Carnot cycle obtained from the T-s area argument:
    eta = (T_H - T_C)(S3-S2) / [T_H (S3-S2)] = 1 - T_C/T_H.  Absolute temperatures.
    [Moran Sec. 6.6.2, p.303; agrees with Eq. 5.9]"""
    return 1.0 - T_cold / T_hot


def _demo():
    print("Module 6.1 -- Reversible & Internally Reversible Processes  (Q_int rev = INT T dS)\n")
    # Example 6.1: water, sat liquid -> sat vapor at 150 C (423.15 K), internally reversible,
    # constant p, T.  Table A-2 at 150 C: p=4.758 bar=475.8 kPa, v1=1.0905e-3, v2=0.3928,
    # s1=1.8418, s2=6.8379 kJ/kg.K.
    p_kPa, v1, v2 = 475.8, 1.0905e-3, 0.3928
    T, s1, s2 = 423.15, 1.8418, 6.8379
    W = work_const_pressure(p_kPa, v2, v1)
    Q = heat_int_rev_isothermal(T, s2, s1)
    print("  Ex 6.1 water (int rev, 150 C): W/m = %.2f kJ/kg   [book 186.38]" % W)
    print("                                  Q/m = %.1f kJ/kg   [book 2114.1]" % Q)
    # Heat as area under T-s for the (isothermal) path -- same number:
    Q_area = heat_int_rev_area([T, T], [s1, s2])
    print("  area under T-s = %.1f kJ/kg (== T dS)            [book 2114.1]" % Q_area)
    print("  internally reversible => sigma = %.1f ; adiabatic int rev is isentropic? %s"
          % (sigma_internally_reversible(), is_isentropic(0.0, True)))
    print("  Carnot eff from T-s area (1400/350 K) = %.3f      [= 1 - T_C/T_H]"
          % carnot_eff_ts(1400.0, 350.0))


if __name__ == "__main__":
    _demo()
