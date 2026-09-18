"""
examples.py  —  Module 6.EP (Topic 6: worked Moran Examples, "Processes & Idealizations")

Real Moran 8e worked Examples reproduced from their GIVEN data, regenerating the book's
published ANSWERS (checked in test_examples.py):

  Ch. 4 (control volumes, steady state)
    Ex 4.1  feedwater heater at steady state        -> mdot3=54.15, mdot2=14.15, V2=5.7
    Ex 4.2  barrel filling (transient -> steady)    -> L=3.33 ft
    Ex 4.4  heat transfer from a steam turbine      -> Qcv=-62.3 kW
  Ch. 6 (entropy: reversible, irreversible, isentropic)
    Ex 6.1  internally reversible process of water  -> W/m=186.38, Q/m=2114.1 kJ/kg
    Ex 6.2  irreversible (paddle) process of water  -> W/m=-1927.82, sigma/m=4.9961
    Ex 6.3  minimum theoretical compression work    -> 12.78 Btu/lb
    Ex 6.4  pinpointing irreversibilities (gearbox) -> sigmadot=4.0e-3, 4.1e-3 kW/K
    Ex 6.5  quenching a hot metal bar               -> Tf=535 R, sigma=0.0864 Btu/R
    Ex 6.9  isentropic process of air               -> p2=15.28 atm (pr), 15.26 (k)
    Ex 6.10 air leaking from a tank                 -> m2=1.58 kg, T2=317 K
    Ex 6.11 turbine work from isentropic efficiency -> W/m=271.95 kJ/kg
    Ex 6.12 evaluating isentropic turbine efficiency-> eta_t=0.70

Full statements (GIVEN/FIND/ANSWER) with page citations in ../examples.md.
Property values (h, u, s, v, pr) are book table look-ups quoted as given.
"""
import math


# ---- Ch. 4: control volumes at steady state --------------------------------
def ex_4_1():
    """Feedwater heater, steady, 2 inlets + 1 exit (p.174-175).  (AV)3=0.06 m3/s,
    v3=1.108e-3, mdot1=40 kg/s, v2=1.0078e-3 m3/kg, A2=25 cm2."""
    mdot3 = 0.06 / 1.108e-3                  # = AV3 / v3
    mdot2 = mdot3 - 40.0                     # steady: mdot1 + mdot2 = mdot3
    V2 = mdot2 * 1.0078e-3 / 25e-4           # V = mdot v / A
    return {"mdot3": mdot3, "mdot2": mdot2, "V2": V2}


def ex_4_2():
    """Barrel filling, transient -> steady height where mdot_e = mdot_i (p.175-176).
    mdot_i = 30 lb/s, mdot_e = 9 L (L in ft)."""
    L_steady = 30.0 / 9.0                    # dL/dt = 0 -> 9 L = 30
    return {"L_steady": L_steady}


def ex_4_4():
    """Steam turbine, steady (p.188-189).  mdot=4600 kg/h, Wcv=1000 kW,
    h1=3177.2, h2=2345.4 kJ/kg, V1=10, V2=30 m/s."""
    mdot = 4600.0 / 3600.0
    dke = (30.0 ** 2 - 10.0 ** 2) / 2.0 / 1000.0          # +0.4 kJ/kg
    Qcv = 1000.0 + mdot * ((2345.4 - 3177.2) + dke)
    return {"dke": dke, "Qcv": Qcv}


# ---- Ch. 6: reversible / irreversible / isentropic -------------------------
def ex_6_1():
    """Water, internally reversible, sat-liquid -> sat-vapor at 150 C = 423.15 K (p.303-304).
    p=4.758 bar, v1=1.0905e-3, v2=0.3928, s1=1.8418, s2=6.8379 (Table A-2)."""
    W = 475.8 * (0.3928 - 1.0905e-3)         # p(v2-v1), kPa*m3/kg = kJ/kg
    Q = 423.15 * (6.8379 - 1.8418)           # T(s2-s1) = INT T dS
    return {"W_per_m": W, "Q_per_m": Q}


def ex_6_2():
    """Water, adiabatic & irreversible (paddle wheel), same end states as Ex 6.1 (p.308-309).
    u1=631.68, u2=2559.5, s1=1.8418, s2=6.8379 (Table A-2)."""
    W = -(2559.5 - 631.68)                   # energy balance, Q=0: W = -(u2-u1)
    sigma = 6.8379 - 1.8418                  # entropy balance, transfer=0: sigma/m = s2-s1
    return {"W_per_m": W, "sigma_per_m": sigma}


def ex_6_3():
    """R-134a compressed adiabatically from sat vapor at 10 F to 120 lbf/in^2 (p.309-310).
    u1=94.68 Btu/lb; isentropic end state 2s (s2s=s1=0.2214) gives u2s=107.46 Btu/lb."""
    u1, u2s = 94.68, 107.46
    W_in_min = u2s - u1                       # (-W/m)_min = u2s - u1
    return {"W_in_min": W_in_min}


def ex_6_4():
    """Gearbox at steady state, Q = -1.2 kW (p.311-312).  (a) Tb=300 K, (b) Tf=293 K."""
    return {"sigmadot_a": -(-1.2) / 300.0, "sigmadot_b": -(-1.2) / 293.0}


def ex_6_5():
    """Quench 0.8-lb metal bar (1900 R) in 20 lb water (530 R) (p.313-315).
    cw=1.0, cm=0.1 Btu/lb.R, tank adiabatic & isolated."""
    mw, cw, Twi = 20.0, 1.0, 530.0
    mm, cm, Tmi = 0.8, 0.1, 1900.0
    Tf = (mw * cw * Twi + mm * cm * Tmi) / (mw * cw + mm * cm)
    Tf_r = round(Tf)                          # book carries Tf = 535 R
    sigma = mw * cw * math.log(Tf_r / Twi) + mm * cm * math.log(Tf_r / Tmi)
    return {"Tf": Tf_r, "sigma": sigma}


def ex_6_9():
    """Air, isentropic, p1=1 atm, T1=540 R -> T2=1160 R (p.329-330).
    (a) pr1=1.3860, pr2=21.18 (Table A-22E); (c) k=1.39 at 850 R."""
    p2_pr = 1.0 * 21.18 / 1.3860              # p2 = p1 pr2/pr1
    p2_k = 1.0 * (1160.0 / 540.0) ** (1.39 / 0.39)   # p2 = p1 (T2/T1)^(k/(k-1))
    return {"p2_pr": p2_pr, "p2_k": p2_k}


def ex_6_10():
    """Air leaking from a rigid insulated tank, 5 kg at 5 bar/500 K -> 1 bar (p.330-331).
    Remaining mass undergoes an isentropic process.  pr1=8.411 @ 500 K -> T2=317 K."""
    pr2 = 8.411 * (1.0 / 5.0)                 # pr2 = (p2/p1) pr1 = 1.6822 -> T2=317 K
    T2 = 317.0
    m2 = (1.0 / 5.0) * (500.0 / T2) * 5.0     # m2 = (p2/p1)(T1/T2) m1
    return {"pr2": pr2, "T2": T2, "m2": m2}


def ex_6_11():
    """Steam turbine, p1=5 bar/320 C -> 1 bar, eta_t=0.75 (p.333-334).
    h1=3105.6, s1=7.5308; h2s=2743.0 kJ/kg (s2s=s1, 1 bar)."""
    W = 0.75 * (3105.6 - 2743.0)             # W/m = eta_t (h1 - h2s)
    return {"W_per_m": W}


def ex_6_12():
    """Air turbine, p1=3 bar/390 K -> 1 bar, measured W/m=74 kJ/kg (p.334-335).
    h1=390.88, pr1=3.481; pr(T2s)=(1/3)(3.481)=1.1603 -> h2s=285.27 kJ/kg."""
    h1, W = 390.88, 74.0
    h2 = h1 - W
    h2s = 285.27
    eta_t = (h1 - h2) / (h1 - h2s)
    return {"Ws": h1 - h2s, "eta_t": eta_t}


def _demo():
    print("Module 6.EP -- Moran Ch.4/6 worked Examples regenerated from GIVEN data\n")
    e = ex_4_1(); print("  Ex 4.1  mdot3=%.2f, mdot2=%.2f kg/s, V2=%.1f m/s   [book 54.15, 14.15, 5.7]"
                        % (e["mdot3"], e["mdot2"], e["V2"]))
    e = ex_4_2(); print("  Ex 4.2  L_steady=%.2f ft                          [book 3.33]" % e["L_steady"])
    e = ex_4_4(); print("  Ex 4.4  dKE=%.1f kJ/kg, Qcv=%.1f kW               [book +0.4, -62.3]"
                        % (e["dke"], e["Qcv"]))
    e = ex_6_1(); print("  Ex 6.1  W/m=%.2f, Q/m=%.1f kJ/kg                  [book 186.38, 2114.1]"
                        % (e["W_per_m"], e["Q_per_m"]))
    e = ex_6_2(); print("  Ex 6.2  W/m=%.2f kJ/kg, sigma/m=%.4f kJ/kg.K      [book -1927.82, 4.9961]"
                        % (e["W_per_m"], e["sigma_per_m"]))
    e = ex_6_3(); print("  Ex 6.3  (-W/m)_min=%.2f Btu/lb                    [book 12.78]" % e["W_in_min"])
    e = ex_6_4(); print("  Ex 6.4  sigmadot_a=%.1e, sigmadot_b=%.1e kW/K     [book 4.0e-3, 4.1e-3]"
                        % (e["sigmadot_a"], e["sigmadot_b"]))
    e = ex_6_5(); print("  Ex 6.5  Tf=%d R, sigma=%.4f Btu/R                 [book 535, 0.0864]"
                        % (e["Tf"], e["sigma"]))
    e = ex_6_9(); print("  Ex 6.9  p2=%.2f atm (pr), %.2f atm (k)            [book 15.28, 15.26]"
                        % (e["p2_pr"], e["p2_k"]))
    e = ex_6_10(); print("  Ex 6.10 pr2=%.4f, T2=%.0f K, m2=%.2f kg          [book 1.6822, 317, 1.58]"
                         % (e["pr2"], e["T2"], e["m2"]))
    e = ex_6_11(); print("  Ex 6.11 W/m=%.2f kJ/kg                            [book 271.95]" % e["W_per_m"])
    e = ex_6_12(); print("  Ex 6.12 (W/m)s=%.1f kJ/kg, eta_t=%.2f            [book 105.6, 0.70]"
                         % (e["Ws"], e["eta_t"]))


if __name__ == "__main__":
    _demo()
