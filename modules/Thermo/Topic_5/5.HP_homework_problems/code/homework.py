"""
homework.py  —  Module 5.HP (Topic 5: end-of-chapter homework, Moran Ch.3 property data)

6 property-evaluation problems from Moran 8e Ch.3 (printed pp.152), each SOLVED from its
given data using the Topic-5 steam-table tools (concept modules 5.1-5.3).  Moran provides
no answer key for end-of-chapter problems, so these are *worked solutions*, reproduced and
checked in test_homework.py (with physical-consistency checks).

All problems use WATER and the project SI steam tables in modules/Thermo/steam_tables/.
Statements in ../problems.md; citations in ../refs.md.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
for _s in ("05.1_saturation_tables", "05.2_vapor_tables", "05.3_liquid_tables"):
    sys.path.insert(0, os.path.join(_HERE, "..", "..", _s, "code"))
import sat_tables as S      # noqa: E402  (5.1)
import vapor_tables as V    # noqa: E402  (5.2)
import liquid_tables as L   # noqa: E402  (5.3)


def _classify_Tv(T_C, v):
    """Phase of water from (T, v): compare v to vf(T), vg(T) in Table A-2."""
    vf, vg = S.sat_T(T_C, "vf"), S.sat_T(T_C, "vg")
    if v < vf:
        return "compressed liquid"
    if v > vg:
        return "superheated vapor"
    return "two-phase"


# --- 3.6  phase determination from (p, T) -----------------------------------
def p3_6():
    """Determine the phase of H2O at five (p,T) states. [Moran Problem 3.6, p.152]
    (a) 10 bar,179.9 C (b) 10 bar,150 C (c) 0.5 bar,100 C (d) 50 bar,20 C (e) 1 bar,-6 C."""
    cases = {"a": (10.0, 179.9), "b": (10.0, 150.0), "c": (0.5, 100.0),
             "d": (50.0, 20.0), "e": (1.0, -6.0)}
    return {k: S.phase_pT(p, T) for k, (p, T) in cases.items()}


# --- 3.7  superheated-vapor interpolation -----------------------------------
def p3_7():
    """Interpolate water-vapor specific volume / temperature. [Moran Problem 3.7, p.152]
    (a) v at 240 C, 1.25 MPa; (b) T at 1.5 MPa, v=0.1555; (c) v at 220 C, 1.4 MPa."""
    va = V.superheated(12.5, 240.0, "v")                       # 0.1879 m^3/kg (interp in p)
    # (b) inverse interp in T at 1.5 MPa between 240 C (0.1483) and 280 C (0.1627)
    Tb = V.linear_interp(0.1555, 0.1483, 0.1627, 240.0, 280.0)  # 260 C
    vc = V.superheated(14.0, 220.0, "v")                       # 0.1557 (double interp)
    return {"v_a": va, "T_b": Tb, "v_c": vc}


# --- 3.13  specific volume of water at three states -------------------------
def p3_13():
    """Specific volume of H2O. [Moran Problem 3.13, p.152]
    (a) 400 C, 20 MPa (superheated); (b) 40 C, 20 MPa (A-5); (c) 40 C, 2 MPa (approx)."""
    va = V.superheated(200.0, 400.0, "v")                      # superheated, 200 bar
    vb = L.compressed(200.0, 40.0, "v")                        # A-5, 200 bar, 40 C
    vc = L.v_approx(L.sat_liquid(40.0)["vf"])                  # 20 bar below A-5 grid -> v~vf(40)
    return {"v_a": va, "v_b": vb, "v_c": vc}


# --- 3.14  locate three states ----------------------------------------------
def p3_14():
    """Locate H2O states. [Moran Problem 3.14, p.152]
    (a) 120 C, 5 bar; (b) 120 C, v=0.6 m^3/kg; (c) 120 C, 1 bar."""
    psat120 = S.sat_T(120.0, "p")                              # 1.985 bar
    a = S.phase_pT(5.0, 120.0)                                 # p>psat -> compressed liquid
    b = _classify_Tv(120.0, 0.6)                               # vf<0.6<vg -> two-phase
    c = S.phase_pT(1.0, 120.0)                                 # p<psat -> superheated vapor
    return {"psat120_bar": psat120, "a": a, "b": b, "c": c}


# --- 3.15(a)  two-phase quality from container volume -----------------------
def p3_15a():
    """4 kg of water at 100 C fills a closed 1 m^3 container; if two-phase, find the
    quality. [Moran Problem 3.15(a), p.152]"""
    m, Vol, T = 4.0, 1.0, 100.0
    v = Vol / m                                                # 0.25 m^3/kg
    vf, vg = S.sat_T(T, "vf"), S.sat_T(T, "vg")
    phase = _classify_Tv(T, v)
    x = S.quality_from_v(v, vf, vg) if phase == "two-phase" else None
    return {"v": v, "phase": phase, "x": x}


# --- 3.23  rigid tank: saturated vapor cooled --------------------------------
def p3_23():
    """Water in a closed rigid tank, initially saturated vapor at 200 C, cooled to 100 C.
    Find the initial and final pressures. [Moran Problem 3.23, p.153]"""
    p1 = S.sat_T(200.0, "p")                                   # psat(200 C) = 15.54 bar
    v1 = S.sat_T(200.0, "vg")                                  # rigid: v2 = v1 = vg(200)
    phase2 = _classify_Tv(100.0, v1)                           # vf<v1<vg at 100 C -> two-phase
    p2 = S.sat_T(100.0, "p")                                   # two-phase -> psat(100) = 1.014 bar
    x2 = S.quality_from_v(v1, S.sat_T(100.0, "vf"), S.sat_T(100.0, "vg"))
    return {"p1_bar": p1, "v1": v1, "phase2": phase2, "p2_bar": p2, "x2": x2}


def _demo():
    print("Module 5.HP -- Topic 5 homework (Moran Ch.3; worked solutions, no book key)\n")
    r = p3_6()
    print("  3.6 phases: " + ", ".join("%s=%s" % (k, r[k]) for k in "abcde"))
    r = p3_7()
    print("  3.7 (a) v(240C,1.25MPa)=%.4f m3/kg [0.1879]" % r["v_a"])
    print("      (b) T(1.5MPa,v=0.1555)=%.0f C [260]" % r["T_b"])
    print("      (c) v(220C,1.4MPa)=%.4f m3/kg [0.1557]" % r["v_c"])
    r = p3_13()
    print("  3.13 (a) v(400C,20MPa)=%.6f (superheated)" % r["v_a"])
    print("       (b) v(40C,20MPa)=%.4e (A-5) [0.9992e-3]" % r["v_b"])
    print("       (c) v(40C,2MPa)~vf(40C)=%.4e [1.0078e-3]" % r["v_c"])
    r = p3_14()
    print("  3.14 psat(120C)=%.3f bar -> (a)5bar:%s (b)v=0.6:%s (c)1bar:%s"
          % (r["psat120_bar"], r["a"], r["b"], r["c"]))
    r = p3_15a()
    print("  3.15a v=%.3f m3/kg -> %s, x=%.4f" % (r["v"], r["phase"], r["x"]))
    r = p3_23()
    print("  3.23 p1=psat(200C)=%.2f bar; cooled to 100C -> %s, p2=%.3f bar, x2=%.4f"
          % (r["p1_bar"], r["phase2"], r["p2_bar"], r["x2"]))


if __name__ == "__main__":
    _demo()
