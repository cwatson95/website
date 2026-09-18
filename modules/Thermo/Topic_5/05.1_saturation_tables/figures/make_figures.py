"""Module 5.1 figures — the saturation dome drawn straight out of Table A-2, and
the two curves (p_sat and h_fg) that close it at the critical point.

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
from sat_tables import (                          # noqa: E402
    load_A2, sat_T, sat_p, mixture, quality_from_v, phase_pT,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the dome itself, from every row of A-2.  The saturated-liquid and
    # saturated-vapour branches are the SAME table read in two columns; they meet
    # at the critical point.  A constant-quality line inside shows how the lever
    # rule (mixture) fills the interior.
    rows = load_A2()
    T = np.array([float(r["T_C"]) for r in rows])
    vf = np.array([sat_T(float(r["T_C"]), "vf") for r in rows])
    vg = np.array([sat_T(float(r["T_C"]), "vg") for r in rows])
    v50 = np.array([mixture(a, b, 0.5) for a, b in zip(vf, vg)])

    fig, ax = plt.subplots(figsize=(6.2, 3.9))
    ax.plot(vf, T, color=INK, lw=2.3, label=r"saturated liquid  $v_f$")
    ax.plot(vg, T, color=FLOW, lw=2.3, ls="--", label=r"saturated vapour  $v_g$")
    ax.plot(v50, T, color=ALT, lw=1.6, ls=":", label=r"$x=0.5$ (lever rule)")
    ax.fill(np.concatenate([vf, vg[::-1]]), np.concatenate([T, T[::-1]]),
            color=STEEL, alpha=0.10, lw=0)
    ax.plot([vf[-1]], [T[-1]], marker="o", ms=8, mfc="white", mec="0.2",
            mew=1.8, ls="none")
    ax.annotate("critical point\n374.14 $^\\circ$C, 220.9 bar",
                xy=(vf[-1], T[-1]), xytext=(0.06, 288), fontsize=9,
                color="0.3", ha="left",
                arrowprops=dict(arrowstyle="->", color="0.5", lw=1.0))
    ax.text(0.9, 120, "two-phase\nregion", fontsize=9.5, color="0.4",
            ha="center")
    ax.set_xscale("log")
    ax.set_xlim(8e-4, 400)
    ax.set_ylim(0, 400)
    ax.set_xlabel(r"specific volume $v$ (m$^3$/kg, log scale)")
    ax.set_ylabel(r"temperature $T$ ($^\circ$C)")
    ax.set_title(r"The saturation dome, read from Table A-2")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6, which="both")
    _save(fig, "fig1_saturation_dome.svg")
    caps["fig1_saturation_dome.svg"] = (
        r"Every row of Table A-2 plotted at once (load_A2, sat_T). The left "
        r"branch is the saturated liquid and the right branch the saturated "
        r"vapour; between them lies the two-phase region, where pressure and "
        r"temperature are no longer independent. The volume axis must be "
        r"logarithmic because the two branches differ by five orders of "
        r"magnitude at low temperature — at 10 $^\circ$C a kilogram of vapour "
        r"occupies " + "%.0f" % (sat_T(10.0, "vg") / sat_T(10.0, "vf")) +
        r" times the volume of a kilogram of liquid. The branches converge at "
        r"the critical point, beyond which the distinction between liquid and "
        r"vapour ceases to exist.")

    # Fig 2 — the two curves that govern the dome, as small multiples (two
    # measures of different scale never share one axis).  p_sat climbs by five
    # decades; h_fg falls to zero at exactly the temperature where it closes.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(6.4, 3.3))
    p = np.array([sat_T(t, "p") for t in T])
    hfg = np.array([sat_T(t, "hfg") for t in T])

    axL.semilogy(T, p, color=INK, lw=2.3)
    axL.axhline(1.01325, color="0.6", lw=1.0, ls=":")
    axL.text(6, 1.35, "1 atm", fontsize=8.5, color="0.4")
    axL.set_xlim(0, 380)
    axL.set_xlabel(r"$T$ ($^\circ$C)")
    axL.set_ylabel(r"saturation pressure (bar)")
    axL.set_title(r"$p_{sat}(T)$", fontsize=11)
    axL.grid(alpha=0.25, lw=0.6, which="both")

    axR.plot(T, hfg, color=FLOW, lw=2.3)
    axR.set_xlim(0, 380)
    axR.set_ylim(0, 2600)
    axR.set_xlabel(r"$T$ ($^\circ$C)")
    axR.set_ylabel(r"latent heat $h_{fg}$ (kJ/kg)")
    axR.set_title(r"$h_{fg}(T)\rightarrow 0$", fontsize=11)
    axR.grid(alpha=0.25, lw=0.6)
    fig.tight_layout()
    _save(fig, "fig2_psat_and_latent_heat.svg")
    caps["fig2_psat_and_latent_heat.svg"] = (
        r"The two saturation curves that control the dome, shown side by side "
        r"because their scales have nothing in common. Saturation pressure "
        r"(left, logarithmic) rises about five decades between the triple point "
        r"and the critical point, crossing 1 atm at 100 $^\circ$C by definition. "
        r"The latent heat (right) moves the opposite way: "
        + "%.0f" % sat_T(10.0, "hfg") + r" kJ/kg at 10 $^\circ$C, "
        + "%.0f" % sat_T(100.0, "hfg") + r" at 100 $^\circ$C, and collapsing to "
        r"zero at the critical temperature — there is no longer any phase change "
        r"to pay for. sat_p indexes the same data by pressure, quality_from_v "
        r"inverts the lever rule, and phase_pT uses the curve to decide whether a "
        r"given $(p,T)$ is liquid, vapour or saturated.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
