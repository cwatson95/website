"""
heat_pump.py  —  Module 08.4 (Heat pump / refrigerator: the device & COP view)

A HEAT PUMP runs a refrigeration cycle "in reverse purpose": a net work input W_net drives
heat Q_C out of a cold region and delivers heat Q_H to a warm region.  At steady state the
first law for the cycle is

    Q_H = Q_C + W_net                                                  (Moran Eq. 10.8)

Performance is measured by a COEFFICIENT OF PERFORMANCE (COP) -- the wanted effect over
the net work needed to get it:

    refrigerator:  beta  = Q_C / W_net                                (Moran Eq. 10.7 form)
    heat pump:     gamma = Q_H / W_net                                (Moran Eq. 10.10 form)

Because Q_H = Q_C + W_net, the two are linked by the identity  gamma = beta + 1, so a heat
pump's COP can NEVER be less than 1.

CARNOT (reversible) limits, between reservoirs at T_C and T_H (absolute temperatures):

    beta_max  = T_C / (T_H - T_C)                                     (Moran Eq. 10.1)
    gamma_max = T_H / (T_H - T_C)                                     (Moran Eq. 10.9)

For an actual VAPOR-COMPRESSION cycle (states 1=compressor in, 2=compressor out,
3=condenser out, 4=valve out, with the throttling valve h4=h3), the net work is the
compressor work and the COPs become enthalpy ratios:

    beta  = (h1 - h4) / (h2 - h1)                                     (Moran Eq. 10.7)
    gamma = (h2 - h3) / (h2 - h1)                                     (Moran Eq. 10.10)

Worked anchors: Example 10.1 (ideal R-134a refrigerator, beta = 9.24; Carnot 10.5) and
Example 10.4 (R-134a heat pump, gamma = 4.65).

Units: Q, W any consistent energy/power unit (ratios are dimensionless); T in KELVIN for
the Carnot limits.  Citations: Moran 8e (PDF = printed + 18; refs.md).
"""


def heat_rejected(Q_C, W_net):
    """Heat delivered to the warm region  Q_H = Q_C + W_net  (cycle first law).
    [Moran Eq. 10.8, Sec. 10.6.1, p.629]"""
    return Q_C + W_net


def cop_refrigeration(Q_C, W_net):
    """Refrigerator COP  beta = Q_C / W_net  (refrigeration effect / net work in).
    [Moran Eq. 10.7 form, Sec. 10.2.1, p.613]"""
    return Q_C / W_net


def cop_heat_pump(Q_H, W_net):
    """Heat-pump COP  gamma = Q_H / W_net  (heating effect / net work in); always >= 1.
    [Moran Eq. 10.10 form, Sec. 10.6.2, p.630]"""
    return Q_H / W_net


def carnot_cop_refrigeration(T_H, T_C):
    """Maximum (Carnot) refrigerator COP  beta_max = T_C/(T_H - T_C)  (T in kelvin).
    [Moran Eq. 10.1, Sec. 10.1.1, p.611]"""
    return T_C / (T_H - T_C)


def carnot_cop_heat_pump(T_H, T_C):
    """Maximum (Carnot) heat-pump COP  gamma_max = T_H/(T_H - T_C)  (T in kelvin).
    [Moran Eq. 10.9, Sec. 10.6.1, p.629]"""
    return T_H / (T_H - T_C)


def cop_ref_from_enthalpies(h1, h2, h4):
    """Vapor-compression refrigerator COP  beta = (h1 - h4)/(h2 - h1).
    [Moran Eq. 10.7, Sec. 10.2.1, p.613]"""
    return (h1 - h4) / (h2 - h1)


def cop_hp_from_enthalpies(h1, h2, h3):
    """Vapor-compression heat-pump COP  gamma = (h2 - h3)/(h2 - h1).
    [Moran Eq. 10.10, Sec. 10.6.2, p.630]"""
    return (h2 - h3) / (h2 - h1)


def _demo():
    print("Module 08.4 -- Heat pump / refrigerator (device & COP view)\n")
    # Example 10.1: ideal R-134a refrigerator. h1=247.23, h2s=264.7, h3=h4=85.75 kJ/kg.
    h1, h2, h3 = 247.23, 264.7, 85.75
    beta = cop_ref_from_enthalpies(h1, h2, h3)            # h4 = h3
    beta_carnot = carnot_cop_refrigeration(299.0, 273.0)
    print("  Ex 10.1 ideal refrigerator: beta = %.2f  [book 9.24];  Carnot beta_max = %.1f  [book 10.5]"
          % (beta, beta_carnot))
    # Example 10.4: R-134a heat pump. h1=242.54, h2=280.19, h3=h4=105.29 kJ/kg.
    h1, h2, h3 = 242.54, 280.19, 105.29
    gamma = cop_hp_from_enthalpies(h1, h2, h3)
    print("  Ex 10.4 heat pump:          gamma = %.2f [book 4.65]" % gamma)
    # the gamma = beta + 1 identity (same cycle as Ex 10.4)
    beta_same = cop_ref_from_enthalpies(h1, h2, h3)       # refrigeration effect of same cycle
    print("  identity gamma = beta + 1:  %.3f = %.3f + 1  (%s)"
          % (gamma, beta_same, "OK" if abs(gamma - (beta_same + 1.0)) < 1e-9 else "FAIL"))
    # Q_H = Q_C + W_net check with Ex 10.4 rates (Q_C=Q_in, W=Wc, Q_H=Q_out)
    print("  Ex 10.4 first law Q_H = Q_C + W_net: %.2f = %.2f + %.2f kW"
          % (heat_rejected(27.45, 7.53), 27.45, 7.53))


if __name__ == "__main__":
    _demo()
