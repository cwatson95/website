"""
homework.py  —  Module 9.HP (Topic 9: end-of-chapter homework, Moran Ch.8-9 + Ch.5)

12 problems across the six Topic-9 cycles, one per function, each SOLVED from complete
given data.  Moran provides no worked key for its end-of-chapter problems, so these are
*worked solutions* in the style of the Ch.8-9 problem sets, reproduced and checked
(with consistency closures: energy balance, Carnot ceiling, bwr range, mep > 0) in
test_homework.py.

Statements in ../problems.md; citations in ../refs.md.  Cold air-standard k = 1.4,
cv = 0.718 kJ/kg.K, cp = k cv (Table A-20); R/M = 8.314/28.97 kJ/kg.K.  The Rankine
problems take their saturation states from the project water tables
(modules/Thermo/steam_tables/, Table A-3), read at runtime.
"""
import csv
import os

K = 1.4
CV = 0.718                 # kJ/kg.K
CP = K * CV                # so the cold-air energy balance closes exactly
R_AIR = 8.314 / 28.97      # kJ/kg.K

_STEAM = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       "..", "..", "..", "steam_tables"))


def sat_p(p_bar):
    """Saturation row from Table A-3 (project CSV) at pressure p_bar."""
    with open(os.path.join(_STEAM, "A3_sat_water_pressure.csv"), newline="") as f:
        for r in csv.DictReader(f):
            if abs(float(r["P_bar"]) - p_bar) < 1e-9 * max(1.0, p_bar):
                return {k: float(v) for k, v in r.items()}
    raise KeyError(p_bar)


# --- Carnot (09.1) -------------------------------------------------------------
def p1():
    """A power cycle between reservoirs at 1400 K and 300 K claims eta = 0.75; a
    second inventor claims 0.80.  Judge both against the Carnot ceiling (Eq. 5.9)."""
    eta_max = 1.0 - 300.0 / 1400.0                    # 0.7857
    return {"eta_max": eta_max,
            "verdict_075": "irreversible" if 0.75 < eta_max else "impossible",
            "verdict_080": "impossible" if 0.80 > eta_max else "irreversible"}


# --- Otto (09.2) ---------------------------------------------------------------
def p2():
    """Cold air-standard Otto cycle: r = 9.5, T1 = 300 K, p1 = 100 kPa, T3 = 2000 K.
    Find T2, T4, eta, w_net, and mep (Eqs. 9.6-9.8, 9.1)."""
    r, T1, p1_, T3 = 9.5, 300.0, 100.0, 2000.0
    T2 = T1 * r ** (K - 1.0)                          # 738.3 K
    T4 = T3 / r ** (K - 1.0)                          # 812.7 K
    eta = 1.0 - 1.0 / r ** (K - 1.0)                  # 0.5936
    q_in = CV * (T3 - T2)                             # 905.9 kJ/kg
    q_out = CV * (T4 - T1)                            # 368.1 kJ/kg
    w_net = q_in - q_out                              # 537.8 kJ/kg
    v1 = R_AIR * T1 / p1_                             # 0.861 m^3/kg
    mep = w_net / (v1 * (1.0 - 1.0 / r))              # 698 kPa
    return {"T2": T2, "T4": T4, "eta": eta, "q_in": q_in, "q_out": q_out,
            "w_net": w_net, "mep_kPa": mep, "eta_carnot": 1.0 - T1 / T3}


def p3():
    """What compression ratio does a cold air-standard Otto cycle need for
    eta = 0.60 (k = 1.4)?  Invert Eq. 9.8: r = (1 - eta)^(-1/(k-1))."""
    eta = 0.60
    r = (1.0 - eta) ** (-1.0 / (K - 1.0))             # 9.88
    return {"r": r, "eta_check": 1.0 - 1.0 / r ** (K - 1.0)}


# --- Diesel (09.3) ---------------------------------------------------------------
def p4():
    """Cold air-standard Diesel cycle: r = 16, rc = 2.5, T1 = 310 K.
    Find T2, T3, T4 and eta (Eq. 9.13); close the energy balance."""
    r, rc, T1 = 16.0, 2.5, 310.0
    T2 = T1 * r ** (K - 1.0)                          # 939.7 K
    T3 = rc * T2                                      # 2349.4 K
    T4 = T3 * (rc / r) ** (K - 1.0)                   # 1118.1 K
    eta = 1.0 - (1.0 / r ** (K - 1.0)) * (rc ** K - 1.0) / (K * (rc - 1.0))   # 0.5905
    q_in = CP * (T3 - T2)                             # constant-p heat addition
    q_out = CV * (T4 - T1)
    return {"T2": T2, "T3": T3, "T4": T4, "eta": eta,
            "q_in": q_in, "q_out": q_out, "w_net": q_in - q_out,
            "eta_carnot": 1.0 - T1 / T3}


def p5():
    """Effect of cutoff ratio: cold air-standard Diesel at r = 18 with
    rc = 1.5, 2, 3 (Eq. 9.13); compare with the Otto cycle at the same r (Eq. 9.8)."""
    r = 18.0
    def eta(rc):
        return 1.0 - (1.0 / r ** (K - 1.0)) * (rc ** K - 1.0) / (K * (rc - 1.0))
    return {"eta_15": eta(1.5), "eta_2": eta(2.0), "eta_3": eta(3.0),
            "eta_otto": 1.0 - 1.0 / r ** (K - 1.0)}


# --- dual (09.4) -----------------------------------------------------------------
def p6():
    """Cold air-standard dual cycle: r = 16, rp = 1.3, rc = 1.5, T1 = 300 K.
    Find T2..T5 and eta (Sec. 9.4 closed form); verify Diesel < dual < Otto and
    close the two-stage energy balance."""
    r, rp, rc, T1 = 16.0, 1.3, 1.5, 300.0
    T2 = T1 * r ** (K - 1.0)                          # 909.4 K
    T3 = rp * T2                                      # 1182.3 K
    T4 = rc * T3                                      # 1773.4 K
    T5 = T4 * (rc / r) ** (K - 1.0)                   # 688.0 K
    eta = 1.0 - (1.0 / r ** (K - 1.0)) * (rp * rc ** K - 1.0) / \
        ((rp - 1.0) + K * rp * (rc - 1.0))            # 0.6474
    q_in = CV * (T3 - T2) + CP * (T4 - T3)
    q_out = CV * (T5 - T1)
    eta_diesel = 1.0 - (1.0 / r ** (K - 1.0)) * (rc ** K - 1.0) / (K * (rc - 1.0))
    eta_otto = 1.0 - 1.0 / r ** (K - 1.0)
    return {"T2": T2, "T3": T3, "T4": T4, "T5": T5, "eta": eta,
            "q_in": q_in, "q_out": q_out, "w_net": q_in - q_out,
            "eta_diesel": eta_diesel, "eta_otto": eta_otto}


# --- Brayton (09.5) ----------------------------------------------------------------
def p7():
    """Cold air-standard ideal Brayton cycle: rp = 12, T1 = 300 K, T3 = 1400 K.
    Find T2, T4, eta (Eq. 9.25), w_net, and bwr (Eq. 9.20)."""
    rp, T1, T3 = 12.0, 300.0, 1400.0
    T2 = T1 * rp ** ((K - 1.0) / K)                   # 610.2 K
    T4 = T3 * (1.0 / rp) ** ((K - 1.0) / K)          # 688.3 K
    eta = 1.0 - 1.0 / rp ** ((K - 1.0) / K)          # 0.508
    w_net = CP * ((T3 - T4) - (T2 - T1))              # 403.5 kJ/kg (cp = k cv)
    q_in = CP * (T3 - T2)
    return {"T2": T2, "T4": T4, "eta": eta, "w_net": w_net, "q_in": q_in,
            "q_out": CP * (T4 - T1), "bwr": (T2 - T1) / (T3 - T4),
            "eta_carnot": 1.0 - T1 / T3}


def p8():
    """The p7 cycle with eta_t = eta_c = 0.85 (Sec. 9.6.3).  Find the actual works,
    T2, eta, and bwr; show the efficiency collapse."""
    rp, T1, T3 = 12.0, 300.0, 1400.0
    T2s = T1 * rp ** ((K - 1.0) / K)
    T4s = T3 * (1.0 / rp) ** ((K - 1.0) / K)
    wt = 0.85 * CP * (T3 - T4s)                       # 608.0 kJ/kg
    wc = CP * (T2s - T1) / 0.85                       # 366.8 kJ/kg
    T2 = T1 + wc / CP                                 # 664.9 K
    q_in = CP * (T3 - T2)                             # 738.7 kJ/kg
    return {"wt": wt, "wc": wc, "T2": T2, "q_in": q_in,
            "eta": (wt - wc) / q_in, "bwr": wc / wt}  # 0.327, 0.603


def p9():
    """The p7 cycle with a regenerator of effectiveness 0.75 (Eq. 9.27 in cold-air
    temperature form: Tx = T2 + eta_reg (T4 - T2)).  Find Tx and the new eta."""
    e = p7()
    T2, T4, T3 = e["T2"], e["T4"], 1400.0
    Tx = T2 + 0.75 * (T4 - T2)                        # 668.8 K
    q_in = CP * (T3 - Tx)                             # 734.9 kJ/kg
    return {"Tx": Tx, "q_in": q_in, "eta": e["w_net"] / q_in,   # 0.549
            "eta_no_regen": e["eta"], "T4_minus_T2": T4 - T2}   # regen needs T4 > T2


# --- Rankine (09.6) -------------------------------------------------------------------
def _ideal_rankine(p_boiler_bar, p_cond_bar):
    """Ideal Rankine cycle between two Table A-3 saturation rows (sat vapor at the
    turbine inlet, sat liquid at the condenser exit; Eqs. 8.1-8.7b)."""
    b, c = sat_p(p_boiler_bar), sat_p(p_cond_bar)
    h1, s1 = b["hg_kJkg"], b["sg_kJkgK"]
    x2 = (s1 - c["sf_kJkgK"]) / (c["sg_kJkgK"] - c["sf_kJkgK"])
    h2 = c["hf_kJkg"] + x2 * c["hfg_kJkg"]
    h3 = c["hf_kJkg"]
    wp = c["vf_x1e3_m3kg"] * 1e-3 * (p_boiler_bar - p_cond_bar) * 100.0   # bar->kPa
    h4 = h3 + wp
    return {"h1": h1, "x2": x2, "h2": h2, "h3": h3, "wp": wp, "h4": h4,
            "wt": h1 - h2, "q_in": h1 - h4, "q_out": h2 - h3,
            "eta": ((h1 - h2) - wp) / (h1 - h4), "bwr": wp / (h1 - h2),
            "Tsat_boiler_C": b["T_C"], "Tsat_cond_C": c["T_C"]}


def p10():
    """Ideal Rankine cycle: sat vapor at 60 bar, condenser at 0.10 bar (Table A-3
    via the project CSVs).  Find x2, h2, wp, eta, and bwr."""
    return _ideal_rankine(60.0, 0.10)                 # eta = 0.354, bwr = 0.0066


def p11():
    """Condenser-pressure effect (Sec. 8.2.3): boiler fixed at 80 bar (sat vapor);
    condenser at 0.08 bar vs 1.0 bar.  Lowering condenser pressure raises eta."""
    lo, hi = _ideal_rankine(80.0, 0.08), _ideal_rankine(80.0, 1.00)
    return {"eta_008": lo["eta"], "eta_100": hi["eta"],       # 0.371 vs 0.290
            "x2_008": lo["x2"], "x2_100": hi["x2"],
            "gain": lo["eta"] - hi["eta"]}


def p12():
    """Boiler-pressure effect + Carnot comparison (Sec. 8.2.3): condenser fixed at
    0.08 bar; boiler 40 bar vs 80 bar.  Raising boiler pressure raises eta, and each
    eta sits below the Carnot ceiling for its saturation-temperature extremes."""
    lo, hi = _ideal_rankine(40.0, 0.08), _ideal_rankine(80.0, 0.08)
    def carnot(cycle):
        return 1.0 - (cycle["Tsat_cond_C"] + 273.15) / (cycle["Tsat_boiler_C"] + 273.15)
    return {"eta_40": lo["eta"], "eta_80": hi["eta"],         # 0.343 vs 0.371
            "carnot_40": carnot(lo), "carnot_80": carnot(hi)} # 0.399, 0.446


def _demo():
    print("Module 9.HP -- Topic 9 homework (worked solutions, no book key)\n")
    r = p1();  print("  P1  Carnot 1400/300 K:   eta_max = %.4f; 0.75 -> %s, 0.80 -> %s"
                     % (r["eta_max"], r["verdict_075"], r["verdict_080"]))
    r = p2();  print("  P2  Otto r=9.5:          eta = %.4f, w = %.1f kJ/kg, mep = %.0f kPa"
                     % (r["eta"], r["w_net"], r["mep_kPa"]))
    r = p3();  print("  P3  Otto for eta=0.60:   r = %.2f" % r["r"])
    r = p4();  print("  P4  Diesel r=16,rc=2.5:  eta = %.4f, T3 = %.1f K, w = %.1f kJ/kg"
                     % (r["eta"], r["T3"], r["w_net"]))
    r = p5();  print("  P5  Diesel rc effect:    eta(1.5/2/3) = %.4f / %.4f / %.4f  (Otto %.4f)"
                     % (r["eta_15"], r["eta_2"], r["eta_3"], r["eta_otto"]))
    r = p6();  print("  P6  dual r=16:           eta = %.4f  (Diesel %.4f < dual < Otto %.4f)"
                     % (r["eta"], r["eta_diesel"], r["eta_otto"]))
    r = p7();  print("  P7  Brayton rp=12:       eta = %.4f, w = %.1f kJ/kg, bwr = %.3f"
                     % (r["eta"], r["w_net"], r["bwr"]))
    r = p8();  print("  P8  Brayton eta_tc=0.85: eta = %.4f, bwr = %.3f" % (r["eta"], r["bwr"]))
    r = p9();  print("  P9  Brayton regen 0.75:  Tx = %.1f K, eta = %.4f (from %.4f)"
                     % (r["Tx"], r["eta"], r["eta_no_regen"]))
    r = p10(); print("  P10 Rankine 60/0.10 bar: x2 = %.4f, eta = %.4f, bwr = %.4f"
                     % (r["x2"], r["eta"], r["bwr"]))
    r = p11(); print("  P11 condenser effect:    eta(0.08 bar) = %.4f > eta(1.0 bar) = %.4f"
                     % (r["eta_008"], r["eta_100"]))
    r = p12(); print("  P12 boiler effect:       eta(40 bar) = %.4f < eta(80 bar) = %.4f "
                     "(Carnot %.3f/%.3f)" % (r["eta_40"], r["eta_80"], r["carnot_40"], r["carnot_80"]))


if __name__ == "__main__":
    _demo()
