"""Module 5.3 figures — how nearly a compressed liquid behaves like saturated
liquid at the same temperature, and where that shortcut starts to cost you.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"      # text as vector paths (portable, no font dep)
matplotlib.rcParams["font.size"] = 11
import matplotlib.pyplot as plt                    # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from liquid_tables import (                       # noqa: E402
    load_A5, compressed, sat_liquid, v_approx, u_approx, h_approx,
    h_approx_simple,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    rows = load_A5()

    # Fig 1 — the shortcut v(T,p) ~ vf(T).  Plot the true tabulated specific
    # volume at three pressures against the saturated-liquid value at the same
    # temperature: the curves nearly coincide, which is the whole justification
    # for the approximation.  Liquid water is very nearly incompressible.
    T_grid = [40.0, 80.0, 120.0, 160.0, 200.0]
    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    T_ref = np.linspace(20.0, 220.0, 200)
    vf_ref = np.array([sat_liquid(t)["vf"] for t in T_ref])
    ax.plot(T_ref, vf_ref * 1e3, color="0.5", lw=1.8, ls="-.",
            label=r"saturated liquid $v_f(T)$  (the approximation)")
    for p, c, mk in ((50.0, INK, "o"), (150.0, FLOW, "s"), (300.0, ALT, "^")):
        v = [compressed(p, t, "v") for t in T_grid]
        ax.plot(T_grid, np.array(v) * 1e3, color=c, lw=1.8, marker=mk, ms=6.5,
                mfc="white", mew=1.6, label=r"$p=%g$ bar (Table A-5)" % p)
    ax.set_xlim(20, 220)
    ax.set_xlabel(r"temperature $T$ ($^\circ$C)")
    ax.set_ylabel(r"specific volume $v$ ($\times10^{-3}$ m$^3$/kg)")
    ax.set_title(r"A compressed liquid barely notices the pressure")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_compressed_vs_saturated.svg")
    caps["fig1_compressed_vs_saturated.svg"] = (
        r"Specific volume of liquid water from Table A-5 (compressed) at three "
        r"pressures, against the saturated-liquid value at the same temperature "
        r"(sat_liquid). Squeezing water from 50 to 300 bar at 100 $^\circ$C "
        r"changes its specific volume by only about "
        + "%.1f" % (100 * abs(compressed(300.0, 120.0, "v") / compressed(50.0, 120.0, "v") - 1)) +
        r"%, so all four curves lie almost on top of each other. That is the "
        r"licence for the standard shortcut $v(T,p)\approx v_f(T)$ (v_approx, "
        r"and u_approx for internal energy): where no compressed-liquid table "
        r"exists, read the saturated-liquid column at the right TEMPERATURE and "
        r"ignore the pressure entirely.")

    # Fig 2 — where the shortcut breaks.  Enthalpy is the property that does NOT
    # tolerate dropping the pressure term, because h carries pv.  Compare the two
    # approximations against the tabulated truth.
    p_grid = [25.0, 50.0, 100.0, 150.0, 200.0, 250.0, 300.0]
    T_fix = 100.0
    sl = sat_liquid(T_fix)
    err_simple, err_full = [], []
    for p in p_grid:
        h_true = compressed(p, T_fix, "h")
        err_simple.append(h_approx_simple(sl["hf"]) - h_true)
        err_full.append(h_approx(sl["hf"], sl["vf"], p * 100.0,
                                 sl["psat_bar"] * 100.0) - h_true)

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(p_grid, err_simple, color=FLOW, lw=2.1, marker="s", ms=6.5,
            mfc="white", mew=1.6, label=r"$h\approx h_f(T)$  (drops $v\,\Delta p$)")
    ax.plot(p_grid, err_full, color=INK, lw=2.1, marker="o", ms=6.5,
            mfc="white", mew=1.6,
            label=r"$h\approx h_f+v_f\,(p-p_{sat})$")
    ax.axhline(0.0, color="0.6", lw=1.0)
    ax.set_xlim(0, 310)
    ax.set_xlabel(r"pressure $p$ (bar)    (water at $100\,^\circ$C)")
    ax.set_ylabel(r"error against Table A-5 (kJ/kg)")
    ax.set_title(r"Enthalpy is where the pressure term earns its keep")
    ax.legend(loc="lower left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_enthalpy_approximation_error.svg")
    caps["fig2_enthalpy_approximation_error.svg"] = (
        r"The one place the saturated-liquid shortcut fails. For liquid water at "
        r"100 $^\circ$C, simply taking $h\approx h_f(T)$ (h_approx_simple) drifts "
        r"steadily off the tabulated value as pressure rises — about "
        + "%.0f" % abs(err_simple[-1]) + r" kJ/kg low at 300 bar — because "
        r"enthalpy contains $pv$ and the pressure has moved a long way from "
        r"saturation. Restoring the correction term, "
        r"$h\approx h_f+v_f(p-p_{sat})$ (h_approx), pulls the error back to "
        r"within " + "%.1f" % max(abs(e) for e in err_full) + r" kJ/kg across the "
        r"whole range. Volume and internal energy need no such correction; "
        r"enthalpy does.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
