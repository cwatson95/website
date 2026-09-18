"""
liquid_tables.py  —  Module 5.3 (Compressed liquid table A-5 + saturated-liquid approximation)

For a compressed (subcooled) liquid the state is fixed by p and T (single phase), and
Table A-5 lists v, u, h, s versus (p, T) just like the superheated table -- but A-5
exists only for water and only on a coarse grid (Moran 8e Sec. 3.5.1, p.105).

Because v and u of a liquid change very little with pressure at fixed temperature,
Moran gives the SATURATED-LIQUID APPROXIMATIONS (Sec. 3.10.1, p.123):
      v(T, p) ~= vf(T)                                 (Eq. 3.11)
      u(T, p) ~= uf(T)                                 (Eq. 3.12)
      h(T, p) ~= hf(T) + vf(T) [ p - psat(T) ]         (Eq. 3.13)
      h(T, p) ~= hf(T)        (when the p-term is small)(Eq. 3.14)
i.e. evaluate liquid properties at the saturated-liquid state for the given T.

This module READS  modules/Thermo/steam_tables/  : A-5 for the compressed-liquid
table and A-2 for the saturated-liquid (f) reference values -- it does NOT duplicate
the data.  A-5 v and A-2 vf are tabulated x10^3 (divide by 1000 for m^3/kg).
Citations: Moran 8e (PDF page = printed + 18).
"""
import csv
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_STEAM = os.path.normpath(os.path.join(_HERE, "..", "..", "..", "steam_tables"))
_CACHE = {}
# A-5 columns; v is x10^3
_A5COL = {"v": ("v_x1e3_m3kg", 1e-3), "u": ("u_kJkg", 1.0),
          "h": ("h_kJkg", 1.0), "s": ("s_kJkgK", 1.0)}


def _load(name):
    if name not in _CACHE:
        with open(os.path.join(_STEAM, name), newline="") as f:
            _CACHE[name] = list(csv.DictReader(f))
    return _CACHE[name]


def load_A5():
    """Table A-5: compressed (subcooled) liquid water, v/u/h/s vs (p, T).
    [Moran Sec. 3.5.1, p.105]"""
    return _load("A5_compressed_liquid_water.csv")


def linear_interp(x, x1, x2, y1, y2):
    """Linear interpolation y(x) between (x1,y1) and (x2,y2). [Moran Sec. 3.5.1, p.105]"""
    return y1 + (x - x1) / (x2 - x1) * (y2 - y1)


def pressures():
    """Sorted list of pressure blocks (bar) present in Table A-5."""
    return sorted({float(r["P_bar"]) for r in load_A5()})


def _block(P_bar):
    rows = [r for r in load_A5() if float(r["P_bar"]) == P_bar]
    if not rows:
        raise ValueError("no A-5 block at p=%g bar (have %s)" % (P_bar, pressures()))
    return sorted(rows, key=lambda r: float(r["T_C"]))


def _interp_T(P_bar, T_C, prop):
    col, scale = _A5COL[prop]
    rows = _block(P_bar)
    Ts = [float(r["T_C"]) for r in rows]
    if T_C < Ts[0] or T_C > Ts[-1]:
        raise ValueError("T=%g C out of A-5 block [%g, %g] at %g bar"
                         % (T_C, Ts[0], Ts[-1], P_bar))
    for i in range(len(Ts) - 1):
        if Ts[i] <= T_C <= Ts[i + 1]:
            return linear_interp(T_C, Ts[i], Ts[i + 1],
                                 float(rows[i][col]) * scale, float(rows[i + 1][col]) * scale)
    return float(rows[-1][col]) * scale


def compressed(P_bar, T_C, prop):
    """Compressed-liquid property `prop` ('v','u','h','s') at (P_bar, T_C) from Table
    A-5 (double interpolation in T then p). [Moran Sec. 3.5.1, p.105]"""
    ps = pressures()
    if P_bar in ps:
        return _interp_T(P_bar, T_C, prop)
    if P_bar < ps[0] or P_bar > ps[-1]:
        raise ValueError("p=%g bar out of A-5 range [%g, %g]" % (P_bar, ps[0], ps[-1]))
    for i in range(len(ps) - 1):
        if ps[i] <= P_bar <= ps[i + 1]:
            return linear_interp(P_bar, ps[i], ps[i + 1],
                                 _interp_T(ps[i], T_C, prop), _interp_T(ps[i + 1], T_C, prop))


def sat_liquid(T_C):
    """Saturated-liquid reference values at temperature T_C, from Table A-2:
    returns dict {psat_bar, vf, uf, hf} (vf in m^3/kg). [Moran Sec. 3.5.2, p.107]"""
    rows = _load("A2_sat_water_temperature.csv")
    Ts = [float(r["T_C"]) for r in rows]
    def col(c, sc=1.0):
        for i in range(len(Ts) - 1):
            if Ts[i] <= T_C <= Ts[i + 1]:
                return linear_interp(T_C, Ts[i], Ts[i + 1],
                                     float(rows[i][c]) * sc, float(rows[i + 1][c]) * sc)
        raise ValueError("T out of A-2 range")
    return {"psat_bar": col("P_bar"), "vf": col("vf_x1e3_m3kg", 1e-3),
            "uf": col("uf_kJkg"), "hf": col("hf_kJkg")}


def v_approx(vf_T):
    """v(T, p) ~= vf(T). [Moran Eq. 3.11, Sec. 3.10.1, p.123]"""
    return vf_T


def u_approx(uf_T):
    """u(T, p) ~= uf(T). [Moran Eq. 3.12, Sec. 3.10.1, p.123]"""
    return uf_T


def h_approx(hf_T, vf_T, p_kPa, psat_kPa):
    """h(T, p) ~= hf(T) + vf(T)[p - psat(T)]  (p in kPa, vf in m^3/kg -> kJ/kg).
    [Moran Eq. 3.13, Sec. 3.10.1, p.123]"""
    return hf_T + vf_T * (p_kPa - psat_kPa)


def h_approx_simple(hf_T):
    """h(T, p) ~= hf(T)  (pressure term negligible). [Moran Eq. 3.14, Sec. 3.10.1, p.123]"""
    return hf_T


def _demo():
    print("Module 5.3 -- Compressed liquid table A-5 + saturated-liquid approximation\n")
    # Moran inline illustration (p.105): water at 100 bar (10 MPa), 100 C
    v_tab = compressed(100.0, 100.0, "v")
    print("  A-5  100 bar, 100 C:  v=%.4e  u=%.2f  h=%.2f  [book v=1.0385e-3]"
          % (v_tab, compressed(100.0, 100.0, "u"), compressed(100.0, 100.0, "h")))
    sl = sat_liquid(100.0)
    print("  approx  v~vf=%.4e (%.2f%% off table)" % (sl["vf"], 100 * (sl["vf"] - v_tab) / v_tab))
    h13 = h_approx(sl["hf"], sl["vf"], 100 * 100.0, sl["psat_bar"] * 100.0)   # bar->kPa
    print("  approx  h~hf+vf(p-psat)=%.2f kJ/kg ; h~hf=%.2f   [table h=%.2f]"
          % (h13, sl["hf"], compressed(100.0, 100.0, "h")))
    # Problem 3.13: specific volume of water at 3 states
    print("\n  Problem 3.13 specific volume of H2O:")
    print("    (a) 400 C, 200 bar (superheated -> elsewhere) : see module 5.2")
    print("    (b) 40 C, 200 bar  (A-5)            v = %.4e m3/kg  [0.9992e-3]"
          % compressed(200.0, 40.0, "v"))
    print("    (c) 40 C, 20 bar   (approx v~vf)    v = %.4e m3/kg  [1.0078e-3]"
          % v_approx(sat_liquid(40.0)["vf"]))


if __name__ == "__main__":
    _demo()
