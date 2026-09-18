"""
vapor_tables.py  —  Module 5.2 (Superheated vapor table: Table A-4)

In the single-phase superheated-vapor region pressure and temperature ARE
independent, so two independent properties fix the state (Moran 8e Sec. 3.5.1,
p.105).  Table A-4 is therefore a two-way table: for each pressure block it lists
v, u, h, s versus temperature, beginning with the saturated-vapor (Sat.) row.

A state off the grid needs interpolation (Moran Sec. 3.5.1, p.105):
  * one independent variable off-grid  -> single linear interpolation
        (Moran's illustration: water vapor at 10 bar, 215 C -> v = 0.2141 m^3/kg)
  * BOTH off-grid                      -> DOUBLE interpolation: interpolate in T
        inside each bracketing pressure block, then interpolate those two results
        in pressure.

This module READS  modules/Thermo/steam_tables/A4_superheated_water.csv  (extracted
from the same Moran 8e appendix; see that folder) -- it does NOT duplicate the data.
A-4 specific volume is direct m^3/kg (unlike the saturation tables' vf x10^3).
Citations: Moran 8e (PDF page = printed + 18).
"""
import csv
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_STEAM = os.path.normpath(os.path.join(_HERE, "..", "..", "..", "steam_tables"))
_CACHE = {}
_COL = {"v": "v_m3kg", "u": "u_kJkg", "h": "h_kJkg", "s": "s_kJkgK"}


def load_A4():
    """Table A-4: superheated water vapor, v/u/h/s vs (p, T). [Moran Sec. 3.5.1, p.105]"""
    if "A4" not in _CACHE:
        with open(os.path.join(_STEAM, "A4_superheated_water.csv"), newline="") as f:
            _CACHE["A4"] = list(csv.DictReader(f))
    return _CACHE["A4"]


def linear_interp(x, x1, x2, y1, y2):
    """Linear interpolation y(x) between (x1,y1) and (x2,y2). [Moran Sec. 3.5.1, p.105]"""
    return y1 + (x - x1) / (x2 - x1) * (y2 - y1)


def pressures():
    """Sorted list of pressure blocks (bar) present in Table A-4."""
    return sorted({float(r["P_bar"]) for r in load_A4()})


def _block(P_bar):
    """Rows of one pressure block, sorted by temperature (Sat. row first)."""
    rows = [r for r in load_A4() if float(r["P_bar"]) == P_bar]
    if not rows:
        raise ValueError("no A-4 block at p=%g bar (have %s)" % (P_bar, pressures()))
    return sorted(rows, key=lambda r: float(r["T_C"]))


def _interp_T(P_bar, T_C, prop):
    """Interpolate `prop` versus temperature within the on-grid pressure block P_bar."""
    col = _COL[prop]
    rows = _block(P_bar)
    Ts = [float(r["T_C"]) for r in rows]
    if T_C < Ts[0] or T_C > Ts[-1]:
        raise ValueError("T=%g C out of block range [%g, %g] at %g bar"
                         % (T_C, Ts[0], Ts[-1], P_bar))
    for i in range(len(Ts) - 1):
        if Ts[i] <= T_C <= Ts[i + 1]:
            return linear_interp(T_C, Ts[i], Ts[i + 1],
                                 float(rows[i][col]), float(rows[i + 1][col]))
    return float(rows[-1][col])


def superheated(P_bar, T_C, prop):
    """Superheated-vapor property `prop` ('v','u','h','s') at (P_bar, T_C) by DOUBLE
    interpolation in Table A-4: interpolate in T inside each bracketing pressure
    block, then interpolate in p. [Moran Sec. 3.5.1, p.105]"""
    ps = pressures()
    if P_bar in ps:
        return _interp_T(P_bar, T_C, prop)
    if P_bar < ps[0] or P_bar > ps[-1]:
        raise ValueError("p=%g bar out of A-4 range [%g, %g]" % (P_bar, ps[0], ps[-1]))
    for i in range(len(ps) - 1):
        if ps[i] <= P_bar <= ps[i + 1]:
            y1 = _interp_T(ps[i], T_C, prop)
            y2 = _interp_T(ps[i + 1], T_C, prop)
            return linear_interp(P_bar, ps[i], ps[i + 1], y1, y2)


def enthalpy(u, p_kPa, v):
    """Definition  h = u + p v  (p in kPa, v in m^3/kg -> kJ/kg). [Moran Eq. 3.4, p.111]
    Used to cross-check A-4: tabulated h should equal u + p v."""
    return u + p_kPa * v


def _demo():
    print("Module 5.2 -- Superheated vapor table A-4 (two independent properties)\n")
    # Moran's single-interpolation illustration: water vapor, 10 bar, 215 C
    v215 = superheated(10.0, 215.0, "v")
    print("  10 bar, 215 C: v = %.4f m3/kg   [Moran p.105 -> 0.2141]" % v215)
    # Double interpolation -- Problem 3.7(c): 220 C, 14 bar (1.4 MPa)
    v_dbl = superheated(14.0, 220.0, "v")
    print("  14 bar, 220 C: v = %.4f m3/kg (double interp)   [Problem 3.7c -> 0.1557]" % v_dbl)
    # Problem 3.7(a)(b)
    print("  Problem 3.7a  12.5 bar, 240 C: v = %.4f  [0.1879]" % superheated(12.5, 240.0, "v"))
    # h = u + p v consistency at 1 bar, 120 C (A-4: u=2537.3, v=1.793, h=2716.6)
    h = enthalpy(superheated(1.0, 120.0, "u"), 100.0, superheated(1.0, 120.0, "v"))
    print("  1 bar, 120 C: h=u+pv = %.1f kJ/kg   [table h = 2716.6]" % h)


if __name__ == "__main__":
    _demo()
