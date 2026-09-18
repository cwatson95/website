"""
steam_lookup.py  —  tiny read-only accessor for the shared steam_tables/*.csv

Just enough water-property lookup to drive the open-systems worked examples and
tests.  A full, properly-interpolated steam-table interface belongs to the §5
"Property tables & diagrams" module; this is deliberately minimal:

    sat_pressure(P_bar)      -> dict of saturated props at P  (A-3, linear interp in P)
    h_two_phase(P_bar, x)    -> hf + x*hfg                    [kJ/kg]
    h_superheated(P_bar, T_C)-> h from A-4 (exact P block, linear interp in T)

Pressures/temperatures that fall on tabulated grid points return the exact book
values; off-grid points are linearly interpolated.
"""
import csv
import os

def _find_steam_tables(start):
    """Walk up from `start` until a directory containing steam_tables/ is found,
    so this works regardless of how deep the module sits (Topic_N/<mod>/code/...)."""
    d = start
    for _ in range(8):
        cand = os.path.join(d, "steam_tables")
        if os.path.isdir(cand):
            return cand
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    raise FileNotFoundError(f"could not locate steam_tables/ above {start}")


_HERE = os.path.dirname(os.path.abspath(__file__))
_TBL = _find_steam_tables(_HERE)


def _load(name):
    with open(os.path.join(_TBL, name)) as f:
        return list(csv.DictReader(f))


_A3 = _load("A3_sat_water_pressure.csv")   # saturated water, pressure index
_A4 = _load("A4_superheated_water.csv")     # superheated vapor


def _interp(x, x0, x1, y0, y1):
    if x1 == x0:
        return y0
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def sat_pressure(P_bar):
    """Saturated-water properties at pressure P_bar (bar), interpolated from A-3.

    Returns a dict with float values: T_C, vf, vg, uf, ug, hf, hfg, hg, sf, sg
    (vf is the raw table value x1e3; see steam_tables/README.md).
    """
    rows = sorted(_A3, key=lambda r: float(r["P_bar"]))
    Ps = [float(r["P_bar"]) for r in rows]
    if P_bar < Ps[0] or P_bar > Ps[-1]:
        raise ValueError(f"P={P_bar} bar outside A-3 range [{Ps[0]}, {Ps[-1]}]")
    # locate bracketing rows
    i = max(j for j in range(len(Ps)) if Ps[j] <= P_bar)
    j = min(i + 1, len(Ps) - 1)
    lo, hi = rows[i], rows[j]
    keys = {"T_C": "T_C", "vf": "vf_x1e3_m3kg", "vg": "vg_m3kg",
            "uf": "uf_kJkg", "ug": "ug_kJkg", "hf": "hf_kJkg",
            "hfg": "hfg_kJkg", "hg": "hg_kJkg", "sf": "sf_kJkgK", "sg": "sg_kJkgK"}
    out = {}
    for name, col in keys.items():
        out[name] = _interp(P_bar, Ps[i], Ps[j], float(lo[col]), float(hi[col]))
    return out


def h_two_phase(P_bar, x):
    """Specific enthalpy of a liquid-vapor mixture, h = hf + x*hfg  [kJ/kg]."""
    if not 0.0 <= x <= 1.0:
        raise ValueError("quality x must be in [0, 1]")
    s = sat_pressure(P_bar)
    return s["hf"] + x * s["hfg"]


def h_superheated(P_bar, T_C):
    """Superheated-vapor enthalpy h(P, T) from A-4  [kJ/kg].

    Requires P to match a tabulated pressure block exactly; interpolates linearly
    in temperature within that block.
    """
    block = sorted((r for r in _A4 if float(r["P_bar"]) == P_bar and r["sat"] == "0"),
                   key=lambda r: float(r["T_C"]))
    if not block:
        avail = sorted({float(r["P_bar"]) for r in _A4})
        raise ValueError(f"no A-4 block at P={P_bar} bar; tabulated: {avail}")
    Ts = [float(r["T_C"]) for r in block]
    if T_C < Ts[0] or T_C > Ts[-1]:
        raise ValueError(f"T={T_C} C outside {P_bar}-bar block [{Ts[0]}, {Ts[-1]}]")
    i = max(j for j in range(len(Ts)) if Ts[j] <= T_C)
    j = min(i + 1, len(Ts) - 1)
    return _interp(T_C, Ts[i], Ts[j], float(block[i]["h_kJkg"]), float(block[j]["h_kJkg"]))
