"""
examples.py  —  Module 5.EP (Topic 5: worked Example problems, Moran Ch.3 & Ch.6)

Moran 8e worked Examples on property evaluation reproduced from their GIVEN data using the
Topic-5 steam-table tools (concept modules 5.1-5.5), so the book's published ANSWERS
regenerate and can be checked (test_examples.py).  All use WATER and the project SI steam
tables in modules/Thermo/steam_tables/ (A-2..A-5).

  * Example 3.2 (printed p.109-111): Heating Water at Constant Volume -- rigid two-phase
                tank, p1=1 bar x1=0.5 -> p2=1.5 bar.  Quality, mass of vapor, p3.
  * Example 3.4 (printed p.118-119): Analyzing Two Processes in Series -- superheated 10
                bar/400 C, cool isobarically to sat. vapor, then cool at constant v to
                150 C.  Work, quality, internal energy, heat transfer.
  * Example 6.1 (printed p.303-304): Internally reversible vaporization of water at 150 C.
                Work W/m = p(v2-v1) and heat Q/m = T(s2-s1).

Plus two published in-text illustrations (clearly labelled, not numbered Examples):
  * superheated water at 0.10 MPa, u=2537.3 -> T,v,h and the h=u+pv check (printed p.112).
  * Mollier (h-s) isentropic expansion 240 C/0.10 MPa -> 0.01 MPa (printed p.296).

Where Moran reads a coarse table value and rounds an intermediate (Ex 3.4 rounds the
quality to x3=0.494 before forming u3), this code replicates that rounding so the published
answer reproduces exactly.  Citations: Moran 8e (PDF = printed + 18; ../refs.md).
"""
import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
for _s in ("05.1_saturation_tables", "05.2_vapor_tables", "05.3_liquid_tables",
           "05.4_pv_diagram", "05.5_ts_diagram"):
    sys.path.insert(0, os.path.join(_HERE, "..", "..", _s, "code"))
import sat_tables as S      # noqa: E402  (5.1)
import vapor_tables as V    # noqa: E402  (5.2)
import pv_diagram as P      # noqa: E402  (5.4)
import ts_diagram as TS     # noqa: E402  (5.5)


def _p_from_vg(v_target):
    """Interpolate the pressure in Table A-3 at which vg = v_target (Ex 3.2c).
    [Moran Sec. 3.5.1/3.5.2, p.105/107]"""
    rows = sorted(S.load_A3(), key=lambda r: float(r["P_bar"]))
    vg = [float(r["vg_m3kg"]) for r in rows]
    pp = [float(r["P_bar"]) for r in rows]
    for i in range(len(vg) - 1):
        if vg[i] >= v_target >= vg[i + 1]:           # vg decreases with p
            return S.linear_interp(v_target, vg[i], vg[i + 1], pp[i], pp[i + 1])
    raise ValueError("vg=%g out of A-3 range" % v_target)


# --- Example 3.2: Heating Water at Constant Volume (rigid two-phase) ---------
def ex_3_2():
    """Rigid tank V=0.5 m^3, water two-phase at p1=1 bar, x1=0.5; heated to p2=1.5 bar.
    Find T1,T2; total mass; vapor mass at 1 and 2; and p3 when only sat. vapor remains.
    [Moran Ex 3.2, printed p.109-111]"""
    V_tank, x1 = 0.5, 0.5
    vf1, vg1 = S.sat_p(1.0, "vf"), S.sat_p(1.0, "vg")
    v1 = S.mixture(vf1, vg1, x1)                          # 0.8475 m^3/kg
    T1, T2 = S.sat_p(1.0, "T"), S.sat_p(1.5, "T")         # 99.63, 111.4 C
    m = V_tank / v1                                       # 0.59 kg
    mg1 = x1 * m                                          # 0.295 kg
    vf2, vg2 = S.sat_p(1.5, "vf"), S.sat_p(1.5, "vg")
    x2 = S.quality_from_v(v1, vf2, vg2)                   # rigid: v2 = v1 -> 0.731
    mg2 = x2 * m                                          # 0.431 kg
    p3 = _p_from_vg(v1)                                   # 2.11 bar
    return {"v1": v1, "T1": T1, "T2": T2, "m": m, "mg1": mg1,
            "x2": x2, "mg2": mg2, "p3": p3}


# --- Example 3.4: Analyzing Two Processes in Series -------------------------
def ex_3_4():
    """Water at 10 bar, 400 C (state 1). Process 1-2: cool at const p to sat. vapor.
    Process 2-3: cool at const v to 150 C. Find W/m, x3, u3, Q/m. [Moran Ex 3.4, p.118-119]"""
    v1 = V.superheated(10.0, 400.0, "v")                  # 0.3066 m^3/kg
    u1 = V.superheated(10.0, 400.0, "u")                  # 2957.3 kJ/kg
    v2 = S.sat_p(10.0, "vg")                              # 0.1944 (sat vapor at 10 bar)
    Wm = P.work_isobaric(1000.0, v1, v2)                  # p(v2-v1) = -112.2 kJ/kg
    vf3, vg3 = S.sat_T(150.0, "vf"), S.sat_T(150.0, "vg")
    x3 = round(S.quality_from_v(v2, vf3, vg3), 3)         # rigid v3=v2; book rounds -> 0.494
    uf3, ug3 = S.sat_T(150.0, "uf"), S.sat_T(150.0, "ug")
    u3 = S.mixture(uf3, ug3, x3)                          # 1584.0 kJ/kg
    Qm = (u3 - u1) + Wm                                   # -1485.5 kJ/kg
    return {"v1": v1, "u1": u1, "v2": v2, "Wm": Wm, "x3": x3, "u3": u3, "Qm": Qm}


# --- Example 6.1: internally reversible vaporization of water at 150 C ------
def ex_6_1():
    """Water, sat. liquid -> sat. vapor at 150 C (423.15 K), internally reversible at
    constant p and T. Find W/m = p(v2-v1) and Q/m = T(s2-s1). [Moran Ex 6.1, p.303-304]"""
    vf, vg = S.sat_T(150.0, "vf"), S.sat_T(150.0, "vg")
    sf, sg = S.sat_T(150.0, "sf"), S.sat_T(150.0, "sg")
    p_kPa = S.sat_T(150.0, "p") * 100.0                   # 4.758 bar -> 475.8 kPa
    T = 423.15
    Wm = P.work_isobaric(p_kPa, vf, vg)                   # 186.38 kJ/kg
    Qm = TS.heat_isothermal(T, sf, sg)                    # 2114.1 kJ/kg
    return {"p_kPa": p_kPa, "Wm": Wm, "Qm": Qm}


# --- in-text illustration (printed p.112): superheated water from u --------
def ex_superheat_uh():
    """Water at 0.10 MPa (1 bar) with u=2537.3 kJ/kg lies in the superheat region:
    by inspection of A-4, T=120 C, v=1.793 m^3/kg, h=2716.6 kJ/kg; verify h=u+pv.
    [Moran in-text, printed p.112]"""
    v = V.superheated(1.0, 120.0, "v")                    # 1.793
    u = V.superheated(1.0, 120.0, "u")                    # 2537.3
    h_tab = V.superheated(1.0, 120.0, "h")               # 2716.6
    h_calc = V.enthalpy(u, 100.0, v)                      # u + p v (p=100 kPa)
    return {"T": 120.0, "v": v, "u": u, "h_tab": h_tab, "h_calc": h_calc}


# --- in-text illustration (printed p.296): Mollier isentropic expansion ----
def ex_mollier():
    """Water at state 1 (T1=240 C, p1=0.10 MPa) expands isentropically (s2=s1) to
    p2=0.01 MPa. From the Mollier chart / Tables A-3,A-4: x2~0.98, h2~2537 kJ/kg.
    [Moran in-text, printed p.296]"""
    s1 = V.superheated(1.0, 240.0, "s")                  # at 0.10 MPa, 240 C
    sf2, sg2 = S.sat_p(0.1, "sf"), S.sat_p(0.1, "sg")    # at 0.01 MPa
    x2 = (s1 - sf2) / (sg2 - sf2)                         # ~0.979
    hf2, hg2 = S.sat_p(0.1, "hf"), S.sat_p(0.1, "hg")
    h2 = S.mixture(hf2, hg2, x2)                          # ~2535 kJ/kg
    return {"s1": s1, "x2": x2, "h2": h2}


def _demo():
    print("Module 5.EP -- Moran Ch.3/Ch.6 property examples regenerated from GIVEN data\n")
    e = ex_3_2()
    print("  Ex 3.2 rigid two-phase water (1 bar, x=0.5 -> 1.5 bar):")
    print("    v1=%.4f m3/kg [0.8475], T1=%.2f C [99.63], T2=%.1f C [111.4]"
          % (e["v1"], e["T1"], e["T2"]))
    print("    m=%.2f kg [0.59], mg1=%.3f [0.295], x2=%.3f [0.731], mg2=%.3f [0.431], p3=%.2f bar [2.11]"
          % (e["m"], e["mg1"], e["x2"], e["mg2"], e["p3"]))
    e = ex_3_4()
    print("  Ex 3.4 two processes in series (10 bar/400 C -> sat vap -> 150 C):")
    print("    v1=%.4f [0.3066], u1=%.1f [2957.3], v2=%.4f [0.1944]" % (e["v1"], e["u1"], e["v2"]))
    print("    W/m=%.1f kJ/kg [-112.2], x3=%.3f [0.494], u3=%.1f [1584.0], Q/m=%.1f [-1485.5]"
          % (e["Wm"], e["x3"], e["u3"], e["Qm"]))
    e = ex_6_1()
    print("  Ex 6.1 reversible vaporization at 150 C:")
    print("    W/m=p(v2-v1)=%.2f kJ/kg [186.38], Q/m=T(s2-s1)=%.1f kJ/kg [2114.1]"
          % (e["Wm"], e["Qm"]))
    e = ex_superheat_uh()
    print("  in-text p.112: 0.10 MPa, u=2537.3 -> v=%.3f [1.793], h_tab=%.1f [2716.6], h=u+pv=%.1f"
          % (e["v"], e["h_tab"], e["h_calc"]))
    e = ex_mollier()
    print("  in-text p.296 (Mollier): 240 C/0.1 MPa -> 0.01 MPa: x2=%.3f [~0.98], h2=%.0f [~2537]"
          % (e["x2"], e["h2"]))


if __name__ == "__main__":
    _demo()
