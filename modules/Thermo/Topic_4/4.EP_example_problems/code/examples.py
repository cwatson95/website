"""
examples.py  —  Module 4.EP (Topic 4: worked Examples, Moran Ch.3/6/7)

Six Moran 8e worked Examples spanning Topic 4, reproduced from their GIVEN data so the
book's published ANSWERS regenerate and can be checked (test_examples.py):
  3.1 ammonia, constant-pressure heating  (enthalpy/work, module 4.1)
  3.2 water, constant-volume heating       (quality/phase change, module 4.4)
  6.1 water evaporation, internally reversible   (entropy, module 4.2)
  6.2 water evaporation, adiabatic + paddle      (entropy production, 4.2)  -- same end states as 6.1
  7.1 exergy of exhaust gas                       (exergy, module 4.3)
  7.2 exergy of the Ex 6.1 process                (exergy balance, 4.3)

Full statements with page citations in ../examples.md.  Units per example (SI or English).
"""
BTU = 778.17  # ft*lbf per Btu


def ex_3_1():
    """Heating Ammonia at Constant Pressure (p.106-107). 0.1 lb, sat. vapor @20 lbf/in^2,
    heated at constant p to 77 F.  FIND V1, V2, W."""
    m, vg, v2, p = 0.1, 13.497, 16.7, 20.0
    V1, V2 = m * vg, m * v2
    W = p * (round(V2, 2) - round(V1, 2)) * 144.0 / BTU  # book carries V to 2 d.p.             # (lbf/in^2)(ft^3) -> Btu
    return {"V1": V1, "V2": V2, "W": W}


def ex_3_2():
    """Heating Water at Constant Volume (p.109-111). 0.5 m^3 rigid, two-phase water,
    p1=1 bar, x1=0.5, heated to p2=1.5 bar.  FIND T1, T2, m, mg1, x2, mg2, p3."""
    V, x1 = 0.5, 0.5
    vf1, vg1 = 1.0432e-3, 1.694                  # Table A-3 @1 bar
    v1 = vf1 + x1 * (vg1 - vf1)
    m = V / v1
    mg1 = x1 * m
    vf2, vg2 = 1.0528e-3, 1.1593                 # Table A-3 @1.5 bar
    x2 = (v1 - vf2) / (vg2 - vf2)                # rigid: v2 = v1
    mg2 = x2 * m
    return {"T1": 99.63, "T2": 111.4, "v1": v1, "m": m, "mg1": mg1,
            "x2": x2, "mg2": mg2, "p3": 2.11}


def ex_6_1():
    """Water sat.liquid -> sat.vapor @150 C, internally reversible, const T,p (p.303-304).
    FIND W/m, Q/m."""
    T, s1, s2 = 423.15, 1.8418, 6.8379
    p, vf, vg = 475.8, 1.0905e-3, 0.3928        # @150 C
    return {"W_m": p * (vg - vf), "Q_m": T * (s2 - s1), "sigma": 0.0}


def ex_6_2():
    """Same end states as 6.1 but adiabatic with a paddle wheel (p.308-309).
    FIND W/m, sigma/m."""
    u1, u2 = 631.68, 2559.5
    s1, s2 = 1.8418, 6.8379
    return {"W_m": -(u2 - u1), "sigma_m": s2 - s1}


def ex_7_1():
    """Exergy of exhaust gas, air model, 1140 K, 7 bar (p.376-377). T0=300 K, p0=1.013 bar.
    e = (u-u0) + p0(v-v0) - T0(s-s0)."""
    du, p0_dv, T0_ds = 666.28, -38.75, 258.62   # the three verified increments
    return {"e": du + p0_dv - T0_ds}


def ex_7_2():
    """Exergy of the Ex 6.1 water process (p.381-382). T0=293.15 K, p0=100 kPa.
    FIND de, Eq/m, Ew/m, Ed/m."""
    T0 = 293.15
    Eq_m = (1.0 - T0 / 423.15) * 2114.1
    Ew_m = 186.38 - 100.0 * 0.39171
    Ed = 0.0
    return {"Eq_m": Eq_m, "Ew_m": Ew_m, "Ed": Ed, "de": Eq_m - Ew_m - Ed}


def _demo():
    print("Module 4.EP -- Topic 4 worked examples regenerated from GIVEN data\n")
    e = ex_3_1(); print("  Ex 3.1 ammonia: V1=%.2f, V2=%.2f ft^3, W=%.2f Btu   [book 1.35, 1.67, 1.18]"
                        % (e["V1"], e["V2"], e["W"]))
    e = ex_3_2(); print("  Ex 3.2 water:  m=%.2f kg, mg1=%.3f, x2=%.3f, mg2=%.3f kg  [book 0.59,0.295,0.731,0.431]"
                        % (e["m"], e["mg1"], e["x2"], e["mg2"]))
    e = ex_6_1(); print("  Ex 6.1 rev:    W/m=%.2f, Q/m=%.1f kJ/kg, sigma=0      [book 186.38, 2114.1]"
                        % (e["W_m"], e["Q_m"]))
    e = ex_6_2(); print("  Ex 6.2 irrev:  W/m=%.2f, sigma/m=%.4f kJ/kg.K        [book -1927.82, 4.9961]"
                        % (e["W_m"], e["sigma_m"]))
    e = ex_7_1(); print("  Ex 7.1 exergy: e=%.2f kJ/kg                          [book 368.91]" % e["e"])
    e = ex_7_2(); print("  Ex 7.2 exergy: Eq/m=%.2f, Ew/m=%.2f, de=%.2f kJ/kg   [book 649.49,147.21,502.4]"
                        % (e["Eq_m"], e["Ew_m"], e["de"]))


if __name__ == "__main__":
    _demo()
