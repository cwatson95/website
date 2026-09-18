"""
sat_tables.py  —  Module 5.1 (Saturation tables: Tables A-2 and A-3)

In the two-phase liquid-vapor region pressure and temperature are NOT independent
(Moran 8e Sec. 3.5.2): for each saturation temperature there is one saturation
pressure.  The saturation tables therefore index the f / fg / g property values by a
single variable:
  * Table A-2  indexes by TEMPERATURE   [Moran Sec. 3.5.2, p.107]
  * Table A-3  indexes by PRESSURE      [Moran Sec. 3.5.2, p.107]
Both give, at each entry, the saturated-liquid (f) and saturated-vapor (g) values of
v, u, h, s plus the evaporation difference (fg = g - f) for h.

A two-phase mixture of quality x has any specific property y between yf and yg:
      y = yf + x (yg - yf)              (Moran Eq. 3.2, Sec. 3.5.2, p.108)
the same x-weighting for v, u, h, s.

States not on the table grid are reached by LINEAR INTERPOLATION between adjacent
entries (Moran Sec. 3.5.1, p.105).

This module READS the project water tables in  modules/Thermo/steam_tables/  (CSV,
programmatically extracted from the same Moran 8e appendix; see that folder's
README) -- it does NOT duplicate the data.  vf is stored x10^3, i.e. divide by 1000
for m^3/kg.  Citations: Moran 8e (PDF page = printed + 18).
"""
import csv
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_STEAM = os.path.normpath(os.path.join(_HERE, "..", "..", "..", "steam_tables"))
_CACHE = {}

# human name -> (CSV column, scale)  [vf is tabulated x10^3]
_COL = {"p": ("P_bar", 1.0), "T": ("T_C", 1.0),
        "vf": ("vf_x1e3_m3kg", 1e-3), "vg": ("vg_m3kg", 1.0),
        "uf": ("uf_kJkg", 1.0), "ug": ("ug_kJkg", 1.0),
        "hf": ("hf_kJkg", 1.0), "hfg": ("hfg_kJkg", 1.0), "hg": ("hg_kJkg", 1.0),
        "sf": ("sf_kJkgK", 1.0), "sg": ("sg_kJkgK", 1.0)}


def _load(name):
    if name not in _CACHE:
        with open(os.path.join(_STEAM, name), newline="") as f:
            _CACHE[name] = list(csv.DictReader(f))
    return _CACHE[name]


def load_A2():
    """Table A-2: saturated water indexed by temperature. [Moran Sec. 3.5.2, p.107]"""
    return _load("A2_sat_water_temperature.csv")


def load_A3():
    """Table A-3: saturated water indexed by pressure. [Moran Sec. 3.5.2, p.107]"""
    return _load("A3_sat_water_pressure.csv")


def linear_interp(x, x1, x2, y1, y2):
    """Linear interpolation y(x) between (x1,y1) and (x2,y2). [Moran Sec. 3.5.1, p.105]"""
    return y1 + (x - x1) / (x2 - x1) * (y2 - y1)


def _lookup(rows, index_key, x, col):
    """Interpolate property `col` against the index column `index_key` at value x."""
    icol = _COL[index_key][0]
    ccol, scale = _COL[col]
    xs = [float(r[icol]) for r in rows]
    if x < xs[0] or x > xs[-1]:
        raise ValueError("%s=%g out of table range [%g, %g]" % (index_key, x, xs[0], xs[-1]))
    for i in range(len(xs) - 1):
        if xs[i] <= x <= xs[i + 1]:
            y1 = float(rows[i][ccol]) * scale
            y2 = float(rows[i + 1][ccol]) * scale
            return linear_interp(x, xs[i], xs[i + 1], y1, y2)
    return float(rows[-1][ccol]) * scale


def sat_T(T_C, col):
    """Saturated property `col` ('p','vf','vg','uf','ug','hf','hfg','hg','sf','sg')
    at temperature T_C, interpolated in Table A-2. [Moran Sec. 3.5.2, p.107]"""
    return _lookup(load_A2(), "T", T_C, col)


def sat_p(P_bar, col):
    """Saturated property `col` at pressure P_bar, interpolated in Table A-3.
    [Moran Sec. 3.5.2, p.107]"""
    return _lookup(load_A3(), "p", P_bar, col)


def mixture(yf, yg, x):
    """Two-phase property  y = yf + x (yg - yf)  (v, u, h, or s).
    [Moran Eq. 3.2, Sec. 3.5.2, p.108]"""
    return yf + x * (yg - yf)


def quality_from_v(v, vf, vg):
    """Invert Eq. 3.2 for quality:  x = (v - vf)/(vg - vf). [Moran Eq. 3.2, p.108]"""
    return (v - vf) / (vg - vf)


def phase_pT(P_bar, T_C, tol=0.5):
    """Classify a water state from (p, T) using the saturation tables -- the
    'Finding States in the Steam Tables' decision tree [Moran p.109]:
      T < 0.01 C            -> 'solid'                 (below the triple point)
      T > Tsat(p)           -> 'superheated vapor'
      T < Tsat(p)           -> 'compressed liquid'
      T = Tsat(p)           -> 'two-phase'
    Only the liquid-vapor dome (plus a triple-point floor) is modelled."""
    if T_C < 0.01 - tol:
        return "solid"
    Tsat = sat_p(P_bar, "T")
    if T_C > Tsat + tol:
        return "superheated vapor"
    if T_C < Tsat - tol:
        return "compressed liquid"
    return "two-phase"


def _demo():
    print("Module 5.1 -- Saturation tables A-2 (by T) and A-3 (by p)\n")
    # Reproduce Moran Example 3.2 (water, rigid, p1=1 bar, x1=0.5 -> p2=1.5 bar)
    vf1, vg1 = sat_p(1.0, "vf"), sat_p(1.0, "vg")
    v1 = mixture(vf1, vg1, 0.5)
    print("  Ex 3.2: @1 bar  vf=%.4e  vg=%.4f  ->  v1=vf+0.5*vfg=%.4f m3/kg  [book 0.8475]"
          % (vf1, vg1, v1))
    m = 0.5 / v1
    print("          T1=Tsat(1bar)=%.2f C, T2=Tsat(1.5bar)=%.1f C, m=%.2f kg [book 99.63, 111.4, 0.59]"
          % (sat_p(1.0, "T"), sat_p(1.5, "T"), m))
    vf2, vg2 = sat_p(1.5, "vf"), sat_p(1.5, "vg")
    x2 = quality_from_v(v1, vf2, vg2)            # rigid: v2 = v1
    print("          x2=(v1-vf2)/(vg2-vf2)=%.3f, mg2=x2*m=%.3f kg   [book 0.731, 0.431]"
          % (x2, x2 * m))
    # Phase determination (Problem 3.6 a-e)
    cases = [(10.0, 179.9), (10.0, 150.0), (0.5, 100.0), (50.0, 20.0), (1.0, -6.0)]
    print("\n  Phase of H2O (Problem 3.6):")
    for p, T in cases:
        print("    p=%-5g bar, T=%-6g C -> %s" % (p, T, phase_pT(p, T)))


if __name__ == "__main__":
    _demo()
