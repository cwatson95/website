"""
examples.py  —  Module 11.EP (Topic 11: worked Examples, Moran Ch.12 psychrometrics)

Four Moran 8e worked Examples spanning Topic 11, reproduced from their GIVEN data so
the book's published ANSWERS regenerate and can be checked (test_examples.py):
  12.7  cooling moist air at constant pressure   (omega, dew point, condensate)
  12.8  cooling moist air at constant volume      (dew point, onset T', condensate)
  12.11 dehumidifier performance                  (omega via Eq. 12.43, sat. exit)
  12.12 steam-spray humidifier                    (omega via water balance; chart)

Full statements with page citations in ../examples.md.  Table data (pg, hf, hg, ha)
are Moran's own (Tables A-2, A-2E, A-22).  Citations: Moran 8e (PDF = printed + 18).
"""

EPS = 0.622
R_BAR = 8314.0     # J/kmol.K
MV, MA = 18.0, 28.97


def ex_12_7():
    """Cooling Moist Air at Constant Pressure (p.758-759). 1 lb moist air @70 F,
    14.7 lbf/in^2, phi=70%, cooled to 40 F.  FIND omega1, dew point, condensate."""
    p, phi = 14.7, 0.70
    pg70, pg40 = 0.3632, 0.1217                 # Table A-2E
    pv1 = phi * pg70                            # = 0.2542
    w1 = EPS * pv1 / (p - pv1)                  # = 0.011
    ma = 1.0 / (1.0 + w1)                       # 1-lb sample = ma + mv1
    mv1 = w1 * ma
    w2 = EPS * pg40 / (p - pg40)               # 40 F: vapor saturated, pv2 = pg40
    mv2 = w2 * ma
    mw = mv1 - mv2
    return {"pv1": pv1, "omega1": w1, "dew_point_F": 60.0, "omega2": w2,
            "ma": ma, "mv1": mv1, "mv2": mv2, "mw": mw}


def ex_12_8():
    """Cooling Moist Air at Constant Volume (p.759-761). 35 m^3 rigid, 1.5 bar, 120 C,
    phi=10%, cooled to 22 C.  FIND dew point, onset T', condensate."""
    V, p1, T1, phi = 35.0, 1.5, 393.0, 0.10
    pg120 = 1.985                               # Table A-2 @120 C, bar
    pv1 = phi * pg120                           # 0.1985 bar
    vv1 = (R_BAR / MV) * T1 / (pv1 * 1e5)       # ideal gas, m^3/kg  (= 9.145)
    mv1 = V / vv1                               # 3.827 kg
    vf2, vg2 = 1.0022e-3, 51.447               # Table A-2 @22 C
    x2 = (vv1 - vf2) / (vg2 - vf2)             # rigid: vv2 = vv1
    mv2 = x2 * mv1
    mw2 = mv1 - mv2
    pa1 = (p1 - pv1) * 1e5
    ma = pa1 * V / ((R_BAR / MA) * T1)
    return {"pv1": pv1, "dew_point_C": 60.0, "vv1": vv1, "mv1": mv1,
            "T_onset_C": 56.0, "x2": x2, "mv2": mv2, "mw2": mw2, "ma": ma}


def ex_12_11():
    """Dehumidifier Performance (p.773-775). Moist air @30 C, 50% RH, 280 m^3/min;
    condensate + saturated air exit @10 C, p=1.013 bar.  FIND ma_dot, mw/ma, tons."""
    AV1, T1, phi1, p = 280.0, 303.0, 0.50, 1.013
    pg30, pg10 = 0.04246, 0.01228               # Table A-2, bar
    pv1 = phi1 * pg30                            # 0.02123 bar
    pa1 = (p - pv1) * 1e5
    ma_dot = AV1 * pa1 / ((R_BAR / MA) * T1)     # kg/min
    w1 = EPS * pv1 / (p - pv1)                   # 0.0133
    w2 = EPS * pg10 / (p - pg10)                 # 0.0076 (saturated exit)
    mw_per_ma = w1 - w2                          # 0.0057
    # (c) heat transfer: ha @303/283 K (A-22); hg @30/10 C, hf @10 C (A-2)
    ha1, ha2, hg1, hg2, hf2 = 303.2, 283.1, 2556.3, 2519.8, 42.0
    Qcv = ma_dot * ((ha2 - ha1) - w1 * hg1 + w2 * hg2 + mw_per_ma * hf2)
    tons = -Qcv / 211.0                          # 211 kJ/min per ton (Sec. 10.2.1)
    return {"pv1": pv1, "pa1_bar": pa1 / 1e5, "ma_dot": ma_dot,
            "omega1": w1, "omega2": w2, "mw_per_ma": mw_per_ma, "Qcv": Qcv, "tons": tons}


def ex_12_12():
    """Steam-Spray Humidifier (p.776-777). Moist air @22 C, Twb=9 C, ma=90 kg/min;
    sat. vapor @110 C injected at 52 kg/h, p=1 bar.  FIND exit omega2 and T2 (chart)."""
    w1 = 0.002                                   # chart read at (22 C, Twb=9 C)
    mst, ma_dot = 52.0 / 60.0, 90.0              # kg/min
    w2 = w1 + mst / ma_dot                        # water mass balance
    h1_chart = 27.2                               # (ha+omega*hg)1 from chart
    hg3 = 2691.5                                  # sat. vapor @110 C, Table A-2
    term2 = (w2 - w1) * hg3
    h2 = h1_chart + term2                          # (ha+omega*hg)2
    return {"omega1": w1, "omega2": w2, "h1_chart": h1_chart,
            "term2": term2, "h2": h2, "T2_C": 23.5}


def _demo():
    print("Module 11.EP -- Topic 11 worked examples regenerated from GIVEN data\n")
    e = ex_12_7(); print("  Ex 12.7  pv1=%.4f, omega1=%.4f, dewpt=%.0f F, condensate mw=%.4f lb"
                         "  [book 0.2542, 0.011, 60, 0.0058]" % (e["pv1"], e["omega1"], e["dew_point_F"], e["mw"]))
    e = ex_12_8(); print("  Ex 12.8  dewpt=%.0f C, vv1=%.3f, mv1=%.3f, onset=%.0f C, x2=%.3f, mw2=%.3f kg"
                         "  [book 60, 9.145, 3.827, 56, 0.178, 3.146]"
                         % (e["dew_point_C"], e["vv1"], e["mv1"], e["T_onset_C"], e["x2"], e["mw2"]))
    e = ex_12_11(); print("  Ex 12.11 ma_dot=%.1f kg/min, omega1=%.4f, omega2=%.4f, mw/ma=%.4f, %.1f tons"
                          "  [book 319.35, 0.0133, 0.0076, 0.0057, 52.5]"
                          % (e["ma_dot"], e["omega1"], e["omega2"], e["mw_per_ma"], e["tons"]))
    e = ex_12_12(); print("  Ex 12.12 omega2=%.4f, h2=%.1f kJ/kg(da), T2=%.1f C"
                          "  [book 0.0116, 53, 23.5]" % (e["omega2"], e["h2"], e["T2_C"]))


if __name__ == "__main__":
    _demo()
