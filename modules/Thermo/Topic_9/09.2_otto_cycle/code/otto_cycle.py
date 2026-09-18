"""
otto_cycle.py  —  Module 09.2 (Air-Standard Otto Cycle)

The air-standard Otto cycle models the spark-ignition (gasoline) engine.  It is four
internally reversible processes of air in a piston-cylinder (Moran 8e Sec. 9.2, Fig. 9.3):

  1-2  isentropic compression
  2-3  constant-VOLUME heat addition   (models the rapid spark-ignited combustion)
  3-4  isentropic expansion (power stroke)
  4-1  constant-volume heat rejection

With kinetic/potential energy neglected, the thermal efficiency is (Eq. 9.3)

  eta = 1 - (u4 - u1)/(u3 - u2)                         (air-table form; Table A-22)

Moran's primary method uses the AIR TABLES (Table A-22), which carry the temperature
variation of the specific heats; otto_efficiency_air_table() reproduces that.  On a
COLD AIR-STANDARD basis (constant specific heats, k = cp/cv) the isentropic relations
T2/T1 = r^(k-1) and T4/T3 = 1/r^(k-1) (Eqs. 9.6, 9.7) collapse Eq. 9.3 to the compact

  eta = 1 - 1/r^(k-1)                                   (Eq. 9.8, cold air-standard)

where r = V1/V2 is the COMPRESSION RATIO.  Efficiency rises with r; for air k = 1.4.
Citations: Moran 8e (PDF = printed + 18); see ../refs.md.
"""

K_AIR = 1.4  # cp/cv for air, cold air-standard (Moran Table A-20, ~300 K)


def otto_efficiency(r, k=K_AIR):
    """Cold air-standard Otto thermal efficiency:  eta = 1 - 1/r^(k-1),
    r = compression ratio V1/V2, k = cp/cv. [Moran Eq. 9.8, Sec. 9.2, p.515]"""
    return 1.0 - 1.0 / r ** (k - 1.0)


def otto_efficiency_air_table(u1, u2, u3, u4):
    """Air-standard Otto efficiency from tabulated internal energies (Table A-22):
    eta = 1 - (u4 - u1)/(u3 - u2). [Moran Eq. 9.3, Sec. 9.2, p.514]"""
    return 1.0 - (u4 - u1) / (u3 - u2)


def temp_after_isentropic_compression(T1, r, k=K_AIR):
    """End-of-compression temperature, cold air-standard:  T2 = T1 r^(k-1).
    [Moran Eq. 9.6, Sec. 9.2, p.514]"""
    return T1 * r ** (k - 1.0)


def temp_after_isentropic_expansion(T3, r, k=K_AIR):
    """End-of-expansion temperature, cold air-standard:  T4 = T3 / r^(k-1)
    (since V4/V3 = r). [Moran Eq. 9.7, Sec. 9.2, p.514]"""
    return T3 / r ** (k - 1.0)


def heat_added_cold(T2, T3, cv=0.718):
    """Constant-volume heat addition per unit mass, cold air-standard:
    q23 = cv (T3 - T2). [Moran Eq. 9.2 with ideal-gas cv, Sec. 9.2, p.514]"""
    return cv * (T3 - T2)


def net_work_cold(r, T1, T3, k=K_AIR, cv=0.718):
    """Net work per unit mass, cold air-standard:  w_net = eta * q23, with
    eta = 1 - 1/r^(k-1) and q23 = cv(T3 - T2). [Moran Sec. 9.2, p.515]"""
    T2 = temp_after_isentropic_compression(T1, r, k)
    return otto_efficiency(r, k) * heat_added_cold(T2, T3, cv)


def mean_effective_pressure(W_net, V1, V2):
    """Mean effective pressure:  mep = W_net/(V1 - V2)  (net work / displacement).
    [Moran Sec. 9.1/9.2, p.512, 515]"""
    return W_net / (V1 - V2)


def _demo():
    print("Module 09.2 -- Air-Standard Otto Cycle  (spark ignition; eta rises with r)\n")
    print("  Cold air-standard, k=1.4:")
    for r in (6.0, 8.0, 10.0):
        print("    r=%2d -> eta = 1 - 1/r^0.4 = %.4f" % (int(r), otto_efficiency(r)))
    print("\n  Example 9.1 (r=8, T1=540 degR, T3=3600 degR):")
    print("    cold air-standard: eta = %.3f, T2 = %.0f degR, T4 = %.0f degR   [book 0.565, 1241, 1567]"
          % (otto_efficiency(8.0),
             temp_after_isentropic_compression(540.0, 8.0),
             temp_after_isentropic_expansion(3600.0, 8.0)))
    print("    air-table (u1=92.04,u2=211.3,u3=721.44,u4=342.2): eta = %.3f   [book 0.51]"
          % otto_efficiency_air_table(92.04, 211.3, 721.44, 342.2))
    print("\n  Note: cold-air eta (0.565) > air-table eta (0.51): constant cv overpredicts.")


if __name__ == "__main__":
    _demo()
