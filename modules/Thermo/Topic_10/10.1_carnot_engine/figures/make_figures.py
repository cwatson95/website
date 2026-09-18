"""Module 10.1 figures — the Carnot corollaries as a verdict on any claimed engine,
and the heat ratio that defines the thermodynamic temperature scale itself.

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
from carnot_engine import (                       # noqa: E402
    carnot_efficiency, thermal_efficiency, efficiency_from_heats,
    kelvin_heat_ratio, carnot_heat_rejected, carnot_work, cycle_status,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — cycle_status turns the Carnot corollaries into a three-way verdict.
    # Plot claimed efficiency against the ceiling for a fixed pair of reservoirs
    # and mark where three example engines land.
    T_C, T_H = 300.0, 900.0
    eta_max = carnot_efficiency(T_C, T_H)
    claims = [("a plausible real engine", 0.45),
              ("a very good engine", 0.64),
              ("an impossible claim", 0.78)]

    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.axhspan(0, eta_max, color=INK, alpha=0.09, lw=0)
    ax.axhspan(eta_max, 1.0, color=FLOW, alpha=0.13, lw=0)
    ax.axhline(eta_max, color=INK, lw=2.4)
    ax.text(0.5, eta_max + 0.012,
            r"reversible: $\eta=\eta_{max}=%.3f$" % eta_max, fontsize=9.5,
            color=INK, ha="center")
    ax.text(0.5, 0.86, "IMPOSSIBLE  (Carnot corollary 1)", fontsize=10,
            color=FLOW, ha="center")
    ax.text(0.5, 0.22, "irreversible: every real engine", fontsize=10,
            color="0.3", ha="center")
    for i, (lab, e) in enumerate(claims):
        x = 0.18 + 0.32 * i
        c = FLOW if e > eta_max else ALT
        ax.plot([x], [e], marker="o", ms=9, mfc="white", mec=c, mew=2.0,
                ls="none", zorder=5)
        ax.annotate("%s\n%s" % (lab, cycle_status(e, T_C, T_H)), xy=(x, e),
                    xytext=(x, e - 0.145), fontsize=8.5, color="0.25",
                    ha="center")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_ylabel(r"thermal efficiency $\eta=W_{cycle}/Q_H$")
    ax.set_title(r"Any cycle between 300 K and 900 K is judged by one line")
    ax.grid(alpha=0.25, lw=0.6, axis="y")
    _save(fig, "fig1_cycle_status.svg")
    caps["fig1_cycle_status.svg"] = (
        r"The two Carnot corollaries, applied. Between reservoirs at 300 K and "
        r"900 K no cycle whatever — Otto, Diesel, Rankine, or something not yet "
        r"invented — may exceed $\eta_{max}=" + "%.3f" % eta_max + r"$ "
        r"(carnot_efficiency), and any cycle that equals it must be reversible. "
        r"cycle_status takes a claimed efficiency (from thermal_efficiency or "
        r"efficiency_from_heats) and returns which of the three verdicts applies, "
        r"so an advertised 0.78 is rejected on thermodynamic grounds alone, "
        r"without knowing anything about the machine's construction. That is "
        r"unusual power for a single inequality.")

    # Fig 2 — the deeper content: for a REVERSIBLE cycle the heat ratio equals
    # the temperature ratio, which is what lets temperature be DEFINED by heat
    # measurements rather than by any particular thermometer fluid.
    T_C_grid = np.linspace(50.0, 900.0, 400)
    T_H0 = 900.0
    ratio = np.array([kelvin_heat_ratio(t, T_H0) for t in T_C_grid])

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(T_C_grid, ratio, color=INK, lw=2.4,
            label=r"$(Q_C/Q_H)_{rev}=T_C/T_H$")
    for t in (300.0, 600.0):
        ax.plot([t], [kelvin_heat_ratio(t, T_H0)], marker="o", ms=7.5,
                mfc="white", mec=FLOW, mew=1.8, ls="none")
        ax.annotate(r"$T_C=%.0f$ K: $Q_C/Q_H=%.3f$" % (t, kelvin_heat_ratio(t, T_H0)),
                    xy=(t, kelvin_heat_ratio(t, T_H0)),
                    xytext=(t + 30, kelvin_heat_ratio(t, T_H0) - 0.11),
                    fontsize=9, color="0.3")
    ax.set_xlim(0, 900)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel(r"cold reservoir $T_C$ (K)    ($T_H=900$ K)")
    ax.set_ylabel(r"$Q_C/Q_H$ for a reversible cycle")
    ax.set_title(r"Heat ratios define the thermodynamic temperature scale")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_kelvin_scale.svg")
    caps["fig2_kelvin_scale.svg"] = (
        r"Why the Kelvin scale is not just another thermometer. Because every "
        r"reversible cycle between the same two reservoirs has the same "
        r"efficiency, the ratio of the heats it exchanges depends on the "
        r"reservoirs alone: $(Q_C/Q_H)_{rev}=T_C/T_H$ (kelvin_heat_ratio). That "
        r"relation DEFINES thermodynamic temperature — measure two heats and you "
        r"have a temperature ratio, with no reference to mercury, ideal gases, or "
        r"any working substance at all. Fixing one point (the triple point of "
        r"water) then fixes the whole scale. carnot_heat_rejected and carnot_work "
        r"split a given $Q_H$ into the parts this ratio dictates: from 1000 kJ at "
        r"900 K rejecting to 300 K, "
        + "%.0f" % carnot_work(1000.0, 300.0, 900.0) + r" kJ of work and "
        + "%.0f" % carnot_heat_rejected(1000.0, 300.0, 900.0) + r" kJ discarded.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
