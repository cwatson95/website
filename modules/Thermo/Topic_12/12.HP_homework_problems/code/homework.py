"""
homework.py  —  Module 12.HP (Topic 12: end-of-chapter homework, Moran Ch.13 & 14)

9 combustion / equilibrium problems, one per function, each SOLVED from complete given
data.  P1-P8 are Moran 8e end-of-chapter problems (printed pp.867-871, 919, 921); Moran
provides NO answer key, so these are *worked solutions*, reproduced and checked in
test_homework.py (with consistency checks: element balances close, mole fractions sum
to 1, K round-trips, dew points inside their steam-table bracket).

P9 is the ~PK plasma extension:  *** [~PK, NOT Moran] ***  the Saha equation supplies
the ionization-equilibrium constant that Moran Sec. 14.4.3 cites to statistical
thermodynamics but does not give.  P9 has no book key; it is checked for physical
consistency and for exact agreement with Moran's Eq.-14.35 ionization form.

Data embedded from the book (all page-verified): Table A-25 h_f0 (kJ/kmol), Table A-23
ideal-gas h_bar(T) (kJ/kmol), Table A-2 saturation pressures (bar), Table A-27
log10 K.  Air model: 1 mol O2 + 3.76 mol N2 (M_air = 28.97).

Statements in ../problems.md; citations in ../refs.md.
"""
import math

M_AIR = 28.97
AIR_PER_O2 = 4.76
N2_PER_O2 = 3.76
R_BAR = 8.314                    # kJ/kmol.K
ATM_BAR = 1.01325                # 1 atm in bar
# Saha part (~PK): CODATA SI constants, as in module 12.2
M_E = 9.1093837015e-31
K_B = 1.380649e-23
H_PLANCK = 6.62607015e-34
EV = 1.602176634e-19

# Table A-25 enthalpies of formation, kJ/kmol (p.970)
HF = {"CO2": -393520.0, "H2O_g": -241820.0, "H2O_l": -285830.0, "CH4": -74850.0,
      "C5H12": -146440.0, "C3H8_l": -118900.0}      # C3H8(l): given in Prob. 13.51
# Table A-23 ideal-gas molar enthalpies h_bar(T), kJ/kmol (p.966-968)
H23 = {
    "CO2": {298: 9364.0, 1140: 50484.0, 1160: 51602.0, 2350: 122091.0, 2400: 125152.0},
    "H2O": {298: 9904.0, 1140: 41780.0, 1160: 42642.0, 2350: 100846.0, 2400: 103508.0},
    "O2":  {298: 8682.0, 1140: 36314.0, 1160: 37023.0},
    "N2":  {298: 8669.0, 1140: 34760.0, 1160: 35430.0, 2350: 77496.0, 2400: 79320.0},
}
# Table A-2 saturation pressure of water, bar (p.927-928)
PSAT = {40: 0.07384, 45: 0.09593, 50: 0.1235, 55: 0.1576}


def theoretical_O2(nC, nH, nO=0.0, nS=0.0):
    """a_O2 = C + H/4 + S - O/2. [Moran Sec. 13.1.2, p.808]"""
    return nC + nH / 4.0 + nS - nO / 2.0


def dew_point_C(y_vapor, p_atm=1.0):
    """Dew point (deg C) = Tsat(p_v = y_v p), interpolating the Table A-2 rows embedded
    above. [Moran Sec. 13.1.3, p.812]  Returns (p_v bar, T_dew C, bracket)."""
    pv = y_vapor * p_atm * ATM_BAR
    Ts = sorted(PSAT)
    for Tlo, Thi in zip(Ts, Ts[1:]):
        if PSAT[Tlo] <= pv <= PSAT[Thi]:
            T = Tlo + (Thi - Tlo) * (pv - PSAT[Tlo]) / (PSAT[Thi] - PSAT[Tlo])
            return {"p_v_bar": pv, "T_dew_C": T, "bracket": (Tlo, Thi)}
    raise ValueError("p_v outside the embedded Table A-2 rows")


def p1():
    """Prob. 13.2 (p.867): ethane C2H6 burns completely with theoretical air.
    Find AF on (a) molar, (b) mass basis.  [Eq. 13.2; Sec. 13.1.2]"""
    aO2 = theoretical_O2(2, 6)                              # 3.5
    AFbar = AIR_PER_O2 * aO2                                # 16.66
    AF = AFbar * (M_AIR / 30.07)                            # 16.05 (M from A-1)
    return {"aO2": aO2, "AFbar": AFbar, "AF": AF}


def p2():
    """Prob. 13.7 (p.868): butane C4H10 burns completely with air, equivalence ratio
    phi = 0.9.  Find (a) the balanced reaction equation, (b) % excess air.
    C4H10 + (6.5/0.9)(O2 + 3.76N2) -> 4CO2 + 5H2O + eO2 + dN2.  [Sec. 13.1.2]"""
    aO2 = theoretical_O2(4, 10)                             # 6.5
    O2_supplied = aO2 / 0.9                                 # phi = AF_theo/AF_act
    e = O2_supplied - aO2                                   # free O2 in products
    d = N2_PER_O2 * O2_supplied
    excess = O2_supplied / aO2 - 1.0                        # 11.1%
    return {"aO2": aO2, "O2_supplied": O2_supplied, "free_O2": e, "N2": d,
            "excess": excess,
            "O_balance": 2 * O2_supplied - (2 * 4 + 5 + 2 * e)}   # must close to 0


def p3():
    """Prob. 13.30 (p.869): hexane C6H14 burns with dry air; dry molar analysis
    CO2 8.5%, CO 5.2%, O2 3%, N2 83.3%.  Find (a) balanced reaction equation,
    (b) % theoretical air, (c) dew point at 1 atm.  Basis: 100 kmol dry products;
    aC6H14 + b(O2+3.76N2) -> 8.5CO2 + 5.2CO + 3O2 + 83.3N2 + cH2O.  [Ex. 13.2 method]"""
    a = (8.5 + 5.2) / 6.0                                   # C balance: 2.2833
    c = 14.0 * a / 2.0                                      # H balance: 15.983
    b = (2 * 8.5 + 5.2 + 2 * 3.0 + c) / 2.0                # O balance: 22.092
    n2_check = N2_PER_O2 * b                                # 83.06 vs 83.3 reported
    pct_theo = (b / a) / theoretical_O2(6, 14)              # O2 supplied / O2 theo
    yv = c / (100.0 + c)                                    # 0.1378
    dew = dew_point_C(yv)
    return {"a": a, "b": b, "c": c, "n2_check": n2_check, "pct_theo": pct_theo,
            "yv": yv, "p_v_bar": dew["p_v_bar"], "T_dew_C": dew["T_dew_C"]}


def p4():
    """Prob. 13.17 (p.868): dodecane C12H26 burns completely with 150% theoretical air.
    Find (a) AF on molar and mass bases, (b) dew point of the products at 1 atm.
    C12H26 + 1.5(18.5)(O2+3.76N2) -> 12CO2 + 13H2O + 9.25O2 + 104.34N2."""
    aO2 = theoretical_O2(12, 26)                            # 18.5
    AFbar = 1.5 * AIR_PER_O2 * aO2                          # 132.09
    M_fuel = 12 * 12.01 + 26 * 1.008                        # 170.33 (atomic weights)
    AF = AFbar * (M_AIR / M_fuel)                           # 22.47
    n_prod = 12.0 + 13.0 + 0.5 * aO2 + 1.5 * aO2 * N2_PER_O2
    yv = 13.0 / n_prod                                      # 0.0938
    dew = dew_point_C(yv)
    return {"aO2": aO2, "AFbar": AFbar, "M_fuel": M_fuel, "AF": AF, "n_prod": n_prod,
            "yv": yv, "T_dew_C": dew["T_dew_C"]}


def p5():
    """Prob. 13.59 (p.871): enthalpy of combustion of gaseous pentane C5H12 at 25 C
    with water VAPOR in the products (the LHV), kJ/kmol; plus the liquid-water variant
    (the HHV).  C5H12 + 8O2 -> 5CO2 + 6H2O.  [Eq. 13.18; Table A-25]
    Consistency: |h_RP|/M must reproduce Table A-25's heating values (45,350 / 49,010
    kJ/kg for pentane)."""
    M = 72.15
    hRP_v = 5 * HF["CO2"] + 6 * HF["H2O_g"] - HF["C5H12"]   # -3,272,080
    hRP_l = 5 * HF["CO2"] + 6 * HF["H2O_l"] - HF["C5H12"]   # -3,536,140
    return {"hRP_vapor": hRP_v, "LHV_mass": -hRP_v / M,
            "hRP_liquid": hRP_l, "HHV_mass": -hRP_l / M}


def p6():
    """Prob. 13.51 (p.871): LIQUID propane (h_f0 = -118,900 kJ/kmol, given) at 25 C,
    1 atm burns completely in a well-insulated steady reactor with air at 25 C, 1 atm.
    Find the adiabatic flame temperature for (a) theoretical air, (b) 300% theoretical
    air.  [Eqs. 13.21a/b; Table A-23 iteration as in Ex. 13.8]
    (a) C3H8(l) + 5O2 + 18.8N2  -> 3CO2 + 4H2O(g) + 18.8N2
    (b) C3H8(l) + 15O2 + 56.4N2 -> 3CO2 + 4H2O(g) + 10O2 + 56.4N2"""
    RHS = HF["C3H8_l"] - (3 * HF["CO2"] + 4 * HF["H2O_g"])  # 2,028,940 kJ/kmol fuel

    def dh(sp, T):
        return H23[sp][T] - H23[sp][298]

    def product_sum(T, coeffs):
        return sum(n * dh(sp, T) for sp, n in coeffs.items())

    # (a) theoretical air: bracket 2350-2400 K (as in Ex 13.8's table)
    ca = {"CO2": 3.0, "H2O": 4.0, "N2": 18.8}
    sa = {T: product_sum(T, ca) for T in (2350, 2400)}
    Ta = 2350 + 50 * (RHS - sa[2350]) / (sa[2400] - sa[2350])
    # (b) 300% theoretical air: bracket 1140-1160 K
    cb = {"CO2": 3.0, "H2O": 4.0, "O2": 10.0, "N2": 56.4}
    sb = {T: product_sum(T, cb) for T in (1140, 1160)}
    Tb = 1140 + 20 * (RHS - sb[1140]) / (sb[1160] - sb[1140])
    return {"RHS": RHS, "sum_a": sa, "T_a": Ta, "sum_b": sb, "T_b": Tb}


def p7():
    """Prob. 14.32 (p.919): a closed vessel initially holds 1 kmol CO + 0.5 kmol O2 at
    1 atm, 300 K; the mixture reacts and reaches equilibrium (CO2, CO, O2) at 2500 K.
    Find the final pressure.  [Eq. 14.35 with Table A-27 K(2500 K) = 10^-1.44 = 0.0363,
    coupled to the rigid-vessel ideal-gas relation p2 = p1 (n2/n1)(T2/T1)]
    1CO + 0.5O2 -> zCO + (z/2)O2 + (1-z)CO2 ; n2 = (2+z)/2, n1 = 1.5."""
    K = 10.0 ** (-1.44)
    p1_atm, T1, T2, n1 = 1.0, 300.0, 2500.0, 1.5

    def p2_of(z):
        return p1_atm * ((2.0 + z) / 2.0 / n1) * (T2 / T1)

    def f(z):
        return (z / (1.0 - z)) * math.sqrt(z / (2.0 + z)) * math.sqrt(p2_of(z)) - K

    lo, hi = 1e-12, 1.0 - 1e-12
    while hi - lo > 1e-13:
        mid = 0.5 * (lo + hi)
        if f(mid) > 0.0:
            hi = mid
        else:
            lo = mid
    z = 0.5 * (lo + hi)
    n2 = (2.0 + z) / 2.0
    p2 = p2_of(z)
    return {"K": K, "z": z, "n2": n2, "p2_atm": p2,
            "y": {"CO": z / n2, "O2": (z / 2.0) / n2, "CO2": (1.0 - z) / n2}}


def p8():
    """Prob. 14.67 (p.921): at 12,000 K and 6 atm, 1 kmol of N ionizes to an
    equilibrium mixture of N, N+, e- with 0.95 kmol N present.  Find the
    ionization-equilibrium constant for N <-> N+ + e-.  [Sec. 14.4.3, Ex. 14.8 method]
    N -> (1-z)N + zN+ + ze-, z = 0.05, n = 1 + z; Eq. 14.35:
    K = [z.z/(1-z)] [(p/pref)/(1+z)] = [z^2/(1-z^2)](p/pref)."""
    z = 1.0 - 0.95
    p_over_pref = 6.0
    K = (z * z / (1.0 - z)) * (p_over_pref / (1.0 + z))
    return {"z": z, "K": K, "log10K": math.log10(K),
            "K_zform": (z * z / (1.0 - z * z)) * p_over_pref}     # identical algebra


def p9():
    """*** [~PK, NOT Moran] ***  Saha ionization of hydrogen (chi = 13.6 eV,
    g+/g0 = 1/2) at total nucleus density n = 1e23 m^-3.  Find the ionization fraction
    x = n_e/n at T = 8000, 12,000, 16,000 K, and show the Saha result IS Moran's
    Sec.-14.4.3 equilibrium: the Moran-form constant K = S kB T/pref reproduces x via
    z = sqrt(K/(K + p/pref)) at the plasma's own pressure p = n(1+x) kB T.
    No book key (beyond Moran); physical-consistency checks only.
    [Saha 1920; Chen; Rybicki & Lightman 9.5; Carroll & Ostlie 8.1]"""
    chi_eV, g_ratio, n = 13.6, 0.5, 1.0e23

    def S(T):
        nQ = (2.0 * math.pi * M_E * K_B * T / H_PLANCK ** 2) ** 1.5
        return 2.0 * g_ratio * nQ * math.exp(-chi_eV * EV / (K_B * T))

    def x_of(T):
        r = S(T) / n
        return (-r + math.sqrt(r * r + 4.0 * r)) / 2.0

    out = {"x": {T: x_of(T) for T in (8000.0, 12000.0, 16000.0)}}
    T = 12000.0
    x = out["x"][T]
    K_moran = S(T) * K_B * T / 101325.0                     # dimensionless, pref = 1 atm
    p_over_pref = n * (1.0 + x) * K_B * T / 101325.0
    out["K_moran_12000K"] = K_moran
    out["p_over_pref"] = p_over_pref
    out["x_from_K"] = math.sqrt(K_moran / (K_moran + p_over_pref))
    return out


def _demo():
    print("Module 12.HP -- Topic 12 homework (worked solutions, no book key)\n")
    r = p1(); print("  P1  13.2 ethane theo air:     AF_bar = %.2f, AF = %.2f" % (r["AFbar"], r["AF"]))
    r = p2(); print("  P2  13.7 butane phi=0.9:      O2 supplied = %.3f, free O2 = %.3f, excess = %.1f%%"
                    % (r["O2_supplied"], r["free_O2"], 100 * r["excess"]))
    r = p3(); print("  P3  13.30 hexane dry analysis: %.1f%% theo air, y_v = %.4f, dew pt = %.1f C"
                    % (100 * r["pct_theo"], r["yv"], r["T_dew_C"]))
    r = p4(); print("  P4  13.17 dodecane 150%% air:  AF_bar = %.2f, AF = %.2f, dew pt = %.1f C"
                    % (r["AFbar"], r["AF"], r["T_dew_C"]))
    r = p5(); print("  P5  13.59 pentane h_RP:       LHV %.0f kJ/kmol (%.0f kJ/kg), HHV %.0f (%.0f)"
                    % (r["hRP_vapor"], r["LHV_mass"], r["hRP_liquid"], r["HHV_mass"]))
    print("        [Table A-25 heating values: 45,350 / 49,010 kJ/kg]")
    r = p6(); print("  P6  13.51 liquid propane AFT: (a) theo air T = %.0f K, (b) 300%% air T = %.0f K"
                    % (r["T_a"], r["T_b"]))
    print("        [cf. Ex 13.8 octane: 2395 K theo air]")
    r = p7(); print("  P7  14.32 closed vessel:      z = %.4f, p2 = %.2f atm, yCO2 = %.3f"
                    % (r["z"], r["p2_atm"], r["y"]["CO2"]))
    r = p8(); print("  P8  14.67 N ionization:       K = %.4f (log10K = %.2f) at 12,000 K, 6 atm"
                    % (r["K"], r["log10K"]))
    r = p9(); print("  P9  [~PK] Saha H ionization:  x = %.4g / %.4g / %.4g at 8/12/16 kK (n = 1e23)"
                    % tuple(r["x"][T] for T in (8000.0, 12000.0, 16000.0)))
    print("        Moran-form K(12,000 K) = %.4g; x via Eq.-14.35 form = %.4g (identical)"
          % (r["K_moran_12000K"], r["x_from_K"]))


if __name__ == "__main__":
    _demo()
