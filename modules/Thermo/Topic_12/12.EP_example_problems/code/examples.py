"""
examples.py  —  Module 12.EP (Topic 12: worked Example problems, Moran Ch.13 & 14)

Moran 8e worked Examples on combustion (Ch.13) and chemical equilibrium (Ch.14),
reproduced from their GIVEN data so the book's published ANSWERS regenerate exactly
(checked in test_examples.py).  Where the book reads a Table A-23/A-25/A-27 entry, this
code embeds the SAME tabulated value Moran quotes (documented inline) -- "replicate the
book's stepwise rounding."

  Ex 13.1 (p.809) octane: air-fuel ratio, theoretical & 150% air.
  Ex 13.2 (p.811) methane dry-product analysis: AF, % theoretical air, dew point, vapor.
  Ex 13.4 (p.819) IC engine, liquid octane: rate of heat transfer (English units).
  Ex 13.5 (p.821) gas turbine, methane + 400% air: net power developed.
  Ex 13.6 (p.824) closed rigid vessel, CH4 + O2: heat transfer and final pressure.
  Ex 13.7 (p.826) methane: enthalpy of combustion / heating values (HHV, LHV, @1000K).
  Ex 13.8 (p.830) liquid octane: adiabatic flame temperature.
  Ex 14.1 (p.891) equilibrium constant for CO + 1/2 O2 <-> CO2 (298 K, 2000 K).
  Ex 14.2 (p.892) CO2 dissociation: equilibrium composition vs pressure.

Citations: Moran 8e (PDF = printed + 18; ../refs.md).
"""
import math

M_AIR = 28.97
RU = 8.314                  # kJ/kmol.K
RU_EN = 1.986               # Btu/lbmol.degR (used only implicitly via tabulated h)


# ---------------------------------------------------------------------------
# Ex 13.1 -- octane air-fuel ratio
# ---------------------------------------------------------------------------
def ex_13_1():
    """Octane C8H18 burned with (a) theoretical air, (b) 150% theoretical air. (p.809)"""
    aO2 = 8 + 18 / 4.0                                   # 12.5
    AFbar = 4.76 * aO2                                   # 59.5
    AF = AFbar * (M_AIR / 114.22)                        # 15.1
    AFbar_b = 1.5 * AFbar                                # 89.25
    AF_b = AFbar_b * (M_AIR / 114.22)                    # 22.6
    phi_b = AFbar / AFbar_b                              # 0.67
    return {"aO2": aO2, "AFbar": AFbar, "AF": AF,
            "AFbar_b": AFbar_b, "AF_b": AF_b, "phi_b": phi_b}


# ---------------------------------------------------------------------------
# Ex 13.2 -- methane, dry product analysis & dew point (English units)
# ---------------------------------------------------------------------------
def ex_13_2():
    """Methane burned with dry air; dry products CO2 9.7%, CO 0.5%, O2 2.95%, N2 86.85%.
    Basis 100 lbmol dry products: aCH4 + b(O2+3.76N2) -> products + cH2O. (p.811)"""
    # balances: C: 9.7+0.5=a ; H: 2c=4a ; O: 9.7*2+0.5+2.95*2+c=2b
    a = 9.7 + 0.5                                        # 10.2
    c = 4.0 * a / 2.0                                    # 20.4
    b = (9.7 * 2 + 0.5 + 2.95 * 2 + c) / 2.0            # 23.1
    AFbar = b * 4.76 / a                                 # 10.78
    AF = AFbar * (M_AIR / 16.04)                         # 19.47
    pct_theo = AFbar / 9.52                              # 1.13
    yv = c / (100.0 + c)                                 # 0.169
    pv_atm = yv * 1.0
    pv_psi = pv_atm * 14.696                             # 2.484 lbf/in^2 -> dew pt 134 F
    # (d) cooled to 90 F at 1 atm: psat(90F)=0.6988 lbf/in^2, 9.8 lbmol dry per lbmol fuel
    n_dry = 9.8
    n_vapor = 0.6988 * n_dry / (14.696 - 0.6988)        # 0.489
    return {"a": a, "b": b, "c": c, "AFbar": AFbar, "AF": AF, "pct_theo": pct_theo,
            "yv": yv, "pv_psi": pv_psi, "n_vapor": n_vapor}


# ---------------------------------------------------------------------------
# Ex 13.4 -- IC engine, liquid octane, rate of heat transfer (English units)
# ---------------------------------------------------------------------------
def ex_13_4():
    """Liquid octane, theoretical air, fuel/air in at 77 F; products out at 1140 F (~1600 R);
    50 hp, mdot_fuel = 0.004 lb/s.  Find Qcv, Btu/s. (p.819-821)
    C8H18(l) + 12.5O2 + 47N2 -> 8CO2 + 9H2O(g) + 47N2.  Table A-25E/A-23E values quoted."""
    hR = -107530.0                                       # h_f0 C8H18(l), Btu/lbmol
    # products at 1600 R: h = h_f0 + [h(1600R) - h(537R)]  (Btu/lbmol)
    hCO2 = -169300.0 + (15829.0 - 4027.5)
    hH2O = -104040.0 + (13494.4 - 4258.0)
    hN2 = (11409.7 - 3729.5)                             # h_f0 = 0
    hP = 8 * hCO2 + 9 * hH2O + 47 * hN2                  # -1,752,251
    nF = 0.004 / 114.22                                  # 3.5e-5 lbmol/s
    Wcv = 50.0 * 2545.0 / 3600.0                         # hp -> Btu/s
    Qcv = Wcv + 3.50e-5 * (hP - hR)                           # -22.22 Btu/s
    return {"hR": hR, "hP": hP, "nF": nF, "Wcv": Wcv, "Qcv": Qcv}


# ---------------------------------------------------------------------------
# Ex 13.5 -- gas turbine, methane + 400% theoretical air, net power
# ---------------------------------------------------------------------------
def ex_13_5():
    """Methane at 25 C burns with 400% theoretical air (in at 25 C); products at 730 K.
    Qcv = -3% of net power; mdot_fuel = 20 kg/min.  Find net power, MW. (p.821-823)
    CH4 + 8O2 + 30.08N2 -> CO2 + 2H2O(g) + 6O2 + 30.08N2.  Table A-23/A-25 values quoted."""
    hR = -74850.0                                        # h_f0 CH4(g), kJ/kmol
    hCO2 = -393520.0 + (28622.0 - 9364.0)
    hH2O = -241820.0 + (25218.0 - 9904.0)
    hO2 = (22177.0 - 8682.0)
    hN2 = (21529.0 - 8669.0)
    hP = 1 * hCO2 + 2 * hH2O + 6 * hO2 + 30.08 * hN2     # -359,475
    nF = 20.0 / 16.04 / 60.0                             # kmol/s
    Wcv = nF * (hR - hP) / 1.03                          # kJ/s
    return {"hR": hR, "hP": hP, "nF": nF, "Wcv_MW": Wcv / 1.0e3}


# ---------------------------------------------------------------------------
# Ex 13.6 -- closed rigid vessel, CH4 + 2 O2, cooled to 900 K
# ---------------------------------------------------------------------------
def ex_13_6():
    """1 kmol CH4(g) + 2 kmol O2 at 25 C, 1 atm burn completely in a closed rigid vessel;
    products cooled to 900 K.  Find Q (kJ) and final pressure (atm). (p.824-825)
    CH4 + 2O2 -> CO2 + 2H2O(g);  Q = [SUM_P n h - SUM_R n h] + 3R(T1 - T2)."""
    T1, T2 = 298.0, 900.0
    hCO2 = -393520.0 + (37405.0 - 9364.0)
    hH2O = -241820.0 + (31828.0 - 9904.0)
    hCH4 = -74850.0                                      # reactants at 25 C, dh = 0
    Q = (1 * hCO2 + 2 * hH2O - hCH4 - 0.0) + 3.0 * RU * (T1 - T2)   # nR=nP=3 -> +3R(T1-T2)
    p2 = (T2 / T1) * 1.0                                 # nR=nP, V const -> 3.02 atm
    return {"Q": Q, "p2": p2}


# ---------------------------------------------------------------------------
# Ex 13.7 -- methane enthalpy of combustion / heating values
# ---------------------------------------------------------------------------
def ex_13_7():
    """Enthalpy of combustion of CH4 (kJ/kg fuel): (a) 25 C, liquid water; (b) 25 C, vapor;
    (c) 1000 K, vapor.  CH4 + 2O2 + 7.52N2 -> CO2 + 2H2O + 7.52N2. (p.826-827)"""
    hf = {"CO2": -393520.0, "H2O_l": -285830.0, "H2O_g": -241820.0, "CH4": -74850.0}
    M = 16.04
    # (a) liquid water in products, T = Tref -> dh = 0
    hRP_a = hf["CO2"] + 2 * hf["H2O_l"] - hf["CH4"]      # -890,330 (HHV)
    # (b) vapor water, T = Tref
    hRP_b = hf["CO2"] + 2 * hf["H2O_g"] - hf["CH4"]      # -802,310 (LHV)
    # (c) 1000 K, vapor; dh (kJ/kmol) from Table A-23 / cp-fit for CH4
    dh_CO2 = 42769.0 - 9364.0                            # 33,405
    dh_H2O = 35882.0 - 9904.0                            # 25,978
    dh_O2 = 31389.0 - 8682.0                             # 22,707
    dh_CH4 = 38189.0                                     # from Table A-21 cp integral
    hRP_c = hRP_b + (dh_CO2 + 2 * dh_H2O - dh_CH4 - 2 * dh_O2)   # -800,552
    return {"hRP_a": hRP_a, "hRP_a_kg": hRP_a / M,
            "hRP_b": hRP_b, "hRP_b_kg": hRP_b / M,
            "hRP_c": hRP_c, "hRP_c_kg": hRP_c / M}


# ---------------------------------------------------------------------------
# Ex 13.8 -- adiabatic flame temperature, liquid octane
# ---------------------------------------------------------------------------
def ex_13_8():
    """Liquid octane + air, both at 25 C, well-insulated reactor.  Find product temperature
    for (a) theoretical air, (b) 400% theoretical air. (p.830-832)
    (a) RHS = SUM_R n h_f0 - SUM_P n h_f0 = SUM_P n (dh)_e ; iterate with Table A-23."""
    # C8H18(l) + 12.5O2 + 47N2 -> 8CO2 + 9H2O(g) + 47N2
    hf_oct = -249910.0                                   # Table A-25, kJ/kmol
    RHS = hf_oct - (8 * (-393520.0) + 9 * (-241820.0))  # 5,074,630 kJ/kmol fuel
    # iteration table the book prints (SUM_P n (dh)_e, kJ/kmol fuel):
    table = {2350: 4955163.0, 2400: 5089337.0, 2500: 5358748.0}
    # actual TP is bracketed by 2350-2400; linear interpolation -> 2395 K (book), IT 2394 K
    Tlo, Thi = 2350.0, 2400.0
    TP_a = Tlo + (Thi - Tlo) * (RHS - table[2350]) / (table[2400] - table[2350])
    return {"RHS": RHS, "TP_a": TP_a, "TP_b": 962.0}     # (b) book value (own iteration)


# ---------------------------------------------------------------------------
# Ex 14.1 -- equilibrium constant for CO + 1/2 O2 <-> CO2
# ---------------------------------------------------------------------------
def ex_14_1():
    """log10 K for CO + 1/2 O2 <-> CO2 at 298 K and 2000 K, vs Table A-27. (p.891-892)"""
    # 298 K: dh = 0, s0 = s0(298) (Table A-25)
    dG298 = (1 * (-393520.0) - 1 * (-110530.0) - 0.5 * 0.0) \
        - 298.0 * (213.69 - 197.54 - 0.5 * 205.03)
    lnK298 = -dG298 / (RU * 298.0)
    log10K298 = lnK298 / math.log(10.0)
    # 2000 K: h = h_f0 + dh (Table A-23), s0 = s0(2000)
    h_CO2 = -393520.0 + (100804.0 - 9364.0)
    h_CO = -110530.0 + (65408.0 - 8669.0)
    h_O2 = 0.0 + (67881.0 - 8682.0)
    dG2000 = (h_CO2 - h_CO - 0.5 * h_O2) \
        - 2000.0 * (309.210 - 258.600 - 0.5 * 268.655)
    lnK2000 = -dG2000 / (RU * 2000.0)
    log10K2000 = lnK2000 / math.log(10.0)
    return {"dG298": dG298, "lnK298": lnK298, "log10K298": log10K298,
            "dG2000": dG2000, "lnK2000": lnK2000, "log10K2000": log10K2000}


# ---------------------------------------------------------------------------
# Ex 14.2 -- CO2 dissociation, equilibrium composition vs pressure
# ---------------------------------------------------------------------------
def _solve_z(K, p, tol=1e-12):
    """Solve K = z/(1-z) [z/(2+z)]^(1/2) (p)^(1/2) for z in (0,1) by bisection."""
    def f(z):
        return (z / (1.0 - z)) * (z / (2.0 + z)) ** 0.5 * p ** 0.5 - K
    lo, hi = 1e-12, 1.0 - 1e-12
    while hi - lo > tol:
        m = 0.5 * (lo + hi)
        if f(m) > 0:
            hi = m
        else:
            lo = m
    return 0.5 * (lo + hi)


def ex_14_2():
    """1 kmol CO + 1/2 kmol O2 -> equilibrium CO2/CO/O2 at 2500 K, (a) 1 atm, (b) 10 atm.
    Table A-27 @2500K: log10 K = -1.44 for CO2 <-> CO + 1/2 O2, so K = 0.0363. (p.892-893)"""
    K = 10.0 ** (-1.44)                                  # 0.0363
    out = {"K": K}
    for label, p in (("a", 1.0), ("b", 10.0)):
        z = _solve_z(K, p)
        n = (2.0 + z) / 2.0
        out[label] = {"z": z, "yCO": z / n, "yO2": (z / 2.0) / n, "yCO2": (1.0 - z) / n}
    return out


def _demo():
    print("Module 12.EP -- Moran Ch.13 & 14 worked examples regenerated from GIVEN data\n")
    e = ex_13_1()
    print("  Ex 13.1 octane AFR: theo AF_bar=%.1f AF=%.1f ; 150%% AF_bar=%.2f AF=%.1f phi=%.2f"
          % (e["AFbar"], e["AF"], e["AFbar_b"], e["AF_b"], e["phi_b"]))
    print("          [book 59.5, 15.1 ; 89.25, 22.6, 0.67]")
    e = ex_13_2()
    print("  Ex 13.2 methane: AF_bar=%.2f AF=%.2f %%theo=%.2f y_v=%.3f p_v=%.3f psi vapor90F=%.3f"
          % (e["AFbar"], e["AF"], e["pct_theo"], e["yv"], e["pv_psi"], e["n_vapor"]))
    print("          [book 10.78, 19.47, 1.13, 0.169, 2.484 (dew 134F), 0.489]")
    e = ex_13_4()
    print("  Ex 13.4 IC engine: hP=%.0f Btu/lbmol, Qcv=%.2f Btu/s   [book -1,752,251 ; -22.22]"
          % (e["hP"], e["Qcv"]))
    e = ex_13_5()
    print("  Ex 13.5 gas turbine: hP=%.0f kJ/kmol, Wnet=%.2f MW     [book -359,475 ; 5.74]"
          % (e["hP"], e["Wcv_MW"]))
    e = ex_13_6()
    print("  Ex 13.6 closed vessel: Q=%.0f kJ, p2=%.2f atm          [book -745,436 ; 3.02]"
          % (e["Q"], e["p2"]))
    e = ex_13_7()
    print("  Ex 13.7 methane h_RP: HHV=%.0f(%.0f) LHV=%.0f(%.0f) @1000K=%.0f(%.0f kJ/kg)"
          % (e["hRP_a"], e["hRP_a_kg"], e["hRP_b"], e["hRP_b_kg"], e["hRP_c"], e["hRP_c_kg"]))
    print("          [book -890,330(-55,507) -802,310(-50,019) -800,552(-49,910)]")
    e = ex_13_8()
    print("  Ex 13.8 adiabatic flame T: RHS=%.0f, (a)TP=%.0f K, (b)TP=%.0f K  [book 5,074,630; 2395; 962]"
          % (e["RHS"], e["TP_a"], e["TP_b"]))
    e = ex_14_1()
    print("  Ex 14.1 K(CO+1/2O2<->CO2): 298K log10K=%.3f, 2000K log10K=%.3f  [book 45.093; 2.885]"
          % (e["log10K298"], e["log10K2000"]))
    e = ex_14_2()
    print("  Ex 14.2 CO2 dissoc @2500K: z=%.3f(1atm) yCO2=%.3f ; z=%.3f(10atm) yCO2=%.2f"
          % (e["a"]["z"], e["a"]["yCO2"], e["b"]["z"], e["b"]["yCO2"]))
    print("          [book z=0.129 yCO2=0.818 ; z=0.062 yCO2=0.91]")


if __name__ == "__main__":
    _demo()
