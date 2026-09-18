"""Module 10.2 figures — the Stirling cycle on p-v, and the regenerator that is the
whole reason it can reach the Carnot efficiency.

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
from stirling_engine import (                     # noqa: E402
    stirling_efficiency, stirling_heat_added, stirling_heat_rejected,
    stirling_net_work, regenerator_heat, stirling_efficiency_no_regen,
    regenerator_effectiveness,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

R_AIR, CV_AIR = 0.287, 0.718                       # kJ/kg.K


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — two isotherms joined by two constant-volume legs.  The two
    # isochoric legs exchange EQUAL and opposite heat, so an ideal regenerator
    # can shuttle it internally and neither transfer needs an external source.
    T_H, T_C, r = 900.0, 300.0, 2.5
    v_min = 0.30
    v_max = r * v_min
    v = np.linspace(v_min, v_max, 200)
    p_hot = R_AIR * T_H / v
    p_cold = R_AIR * T_C / v

    fig, ax = plt.subplots(figsize=(6.2, 3.9))
    ax.plot(v, p_hot, color=FLOW, lw=2.3,
            label=r"3$\rightarrow$4 isothermal expansion at $T_H$")
    ax.plot(v, p_cold, color=INK, lw=2.3,
            label=r"1$\rightarrow$2 isothermal compression at $T_C$")
    ax.plot([v_min, v_min], [R_AIR * T_C / v_min, R_AIR * T_H / v_min],
            color=ALT, lw=2.4, ls="--",
            label=r"2$\rightarrow$3 regenerator heats at const. $v$")
    ax.plot([v_max, v_max], [R_AIR * T_H / v_max, R_AIR * T_C / v_max],
            color=ALT, lw=2.4, ls=(0, (1, 1.6)),
            label=r"4$\rightarrow$1 regenerator cools at const. $v$")
    ax.fill(np.concatenate([v, v[::-1]]),
            np.concatenate([p_hot, p_cold[::-1]]), color=ALT, alpha=0.10, lw=0)
    ax.set_xlim(0.24, 0.83)
    ax.set_ylim(0, 950)
    ax.set_xlabel(r"specific volume $v$ (m$^3$/kg)")
    ax.set_ylabel(r"pressure $p$ (kPa)")
    ax.set_title(r"Stirling cycle: $T_H=900$ K, $T_C=300$ K, $r=2.5$")
    ax.legend(loc="upper right", frameon=False, fontsize=8.5)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_stirling_pv.svg")
    caps["fig1_stirling_pv.svg"] = (
        r"The Stirling cycle: two isotherms joined by two constant-volume legs. "
        r"External heat enters only along the hot isotherm, "
        + "%.0f" % stirling_heat_added(R_AIR, T_H, r) + r" kJ/kg "
        r"(stirling_heat_added), and leaves only along the cold one, "
        + "%.0f" % stirling_heat_rejected(R_AIR, T_C, r) + r" kJ/kg, giving a "
        r"net work of " + "%.0f" % stirling_net_work(R_AIR, T_H, T_C, r) +
        r" kJ/kg — the shaded area. The two vertical legs each move "
        + "%.0f" % regenerator_heat(CV_AIR, T_H, T_C) + r" kJ/kg "
        r"(regenerator_heat), equal in size and opposite in sign, which is the "
        r"cycle's defining trick: a regenerator can store the heat given up on "
        r"one leg and hand it back on the other, so neither has to be paid for "
        r"externally.")

    # Fig 2 — that trick is worth everything.  With perfect regeneration the
    # efficiency equals Carnot at ANY compression ratio; without it, the
    # constant-volume heating must be bought and the efficiency collapses.
    rr = np.linspace(1.2, 8.0, 300)
    eta_regen = np.full_like(rr, stirling_efficiency(T_C, T_H))
    eta_none = np.array([stirling_efficiency_no_regen(R_AIR, CV_AIR, T_H, T_C, x)
                         for x in rr])

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot(rr, eta_regen, color=INK, lw=2.4,
            label=r"ideal regenerator: $\eta=1-T_C/T_H=%.3f$ (= Carnot)"
                  % stirling_efficiency(T_C, T_H))
    ax.plot(rr, eta_none, color=FLOW, lw=2.3, ls="--",
            label=r"no regenerator at all")
    ax.fill_between(rr, eta_none, eta_regen, color=ALT, alpha=0.12, lw=0)
    ax.text(5.2, 0.44, "what the regenerator\nis worth", fontsize=9.5,
            color="0.35", ha="center")
    ax.set_xlim(1.2, 8.0)
    ax.set_ylim(0, 0.78)
    ax.set_xlabel(r"volume ratio $r=v_{max}/v_{min}$")
    ax.set_ylabel(r"thermal efficiency $\eta$")
    ax.set_title(r"The regenerator is what makes Stirling special")
    ax.legend(loc="lower right", frameon=False, fontsize=8.5)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_regenerator_value.svg")
    caps["fig2_regenerator_value.svg"] = (
        r"With perfect regeneration the Stirling engine attains the Carnot "
        r"efficiency $1-T_C/T_H=" + "%.3f" % stirling_efficiency(T_C, T_H) +
        r"$ (stirling_efficiency) — and does so at EVERY volume ratio, because "
        r"the internally shuttled heat never appears in the numerator or the "
        r"denominator. Strip the regenerator out and the constant-volume heating "
        r"must be supplied externally (stirling_efficiency_no_regen): at $r=2.5$ "
        r"the efficiency falls to "
        + "%.3f" % stirling_efficiency_no_regen(R_AIR, CV_AIR, T_H, T_C, 2.5) +
        r", less than half. The shaded gap narrows as $r$ grows, since more of "
        r"the heat then flows through the isothermal legs. Real machines land "
        r"between the curves according to regenerator_effectiveness, and building "
        r"a regenerator that is both effective and low-dead-volume is the central "
        r"engineering difficulty of the Stirling engine.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
