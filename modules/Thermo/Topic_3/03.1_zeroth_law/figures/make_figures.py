"""Module 3.1 figures — the four temperature scales as one straight line seen in
different units, and the zeroth law as the transitivity that lets a thermometer
work at all.

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
from temperature import (                         # noqa: E402
    TRIPLE_POINT_K, ICE_POINT_K, STEAM_POINT_K, ABS_ZERO_C,
    celsius_from_kelvin, rankine_from_kelvin, fahrenheit_from_rankine,
    in_thermal_equilibrium, zeroth_law,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the same physical temperature read on four scales.  Kelvin and
    # Rankine are absolute (through the origin); Celsius and Fahrenheit are the
    # same lines shifted by their offsets.  Fixed points marked.
    T_K = np.linspace(0.0, 700.0, 300)
    T_C = np.array([celsius_from_kelvin(t) for t in T_K])
    T_R = np.array([rankine_from_kelvin(t) for t in T_K])
    T_F = np.array([fahrenheit_from_rankine(r) for r in T_R])

    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.plot(T_K, T_R, color=INK, lw=2.2, label=r"Rankine $^\circ$R $=1.8\,T$(K)")
    ax.plot(T_K, T_F, color=FLOW, lw=2.0, ls="--",
            label=r"Fahrenheit $^\circ$F $=\,^\circ$R $-459.67$")
    ax.plot(T_K, T_K, color=ALT, lw=2.2, ls="-", label=r"Kelvin (absolute)")
    ax.plot(T_K, T_C, color=ALT, lw=1.4, ls=":",
            label=r"Celsius $^\circ$C $=T$(K)$-273.15$")
    ax.axhline(0.0, color="0.7", lw=0.9)
    for T, lab in ((ICE_POINT_K, "ice point"), (STEAM_POINT_K, "steam point")):
        ax.axvline(T, color="0.8", lw=0.9, ls=":")
        ax.text(T + 6, -180, lab, rotation=90, fontsize=8.5, color="0.4")
    ax.set_xlim(0, 700)
    ax.set_xlabel(r"thermodynamic temperature $T$ (K)")
    ax.set_ylabel(r"reading on each scale (degrees)")
    ax.set_title(r"One temperature, four scales")
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_temperature_scales.svg")
    caps["fig1_temperature_scales.svg"] = (
        r"The four scales are one straight line re-labelled. Kelvin and Rankine "
        r"pass through the origin — they are absolute, differing only by the "
        r"factor 1.8 (rankine_from_kelvin) — while Celsius and Fahrenheit are the "
        r"same two lines slid down by 273.15 and 459.67 (celsius_from_kelvin, "
        r"fahrenheit_from_rankine). Absolute zero sits at "
        + "%.2f" % ABS_ZERO_C + r" $^\circ$C, and the triple point of water, the "
        r"single fixed point that defines the kelvin, is at "
        + "%.2f" % TRIPLE_POINT_K + r" K. Only the absolute scales may be used in "
        r"ratios such as the Carnot efficiency.")

    # Fig 2 — the zeroth law is what makes a thermometer meaningful: if a
    # thermometer C reads the same against A and against B, then A and B are in
    # equilibrium with each other, without ever touching.  Drawn as three
    # pairings; the predicate labels each one.
    T_A, T_B, T_C_body, T_D = 350.0, 350.0, 350.0, 320.0
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    def block(x, y, w, h, label, T, color):
        ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=color, alpha=0.16,
                                   edgecolor=color, lw=1.8))
        ax.text(x + w / 2, y + h / 2 + 0.28, label, ha="center", fontsize=11,
                color="0.2")
        ax.text(x + w / 2, y + h / 2 - 0.42, r"$%d$ K" % T, ha="center",
                fontsize=9.5, color="0.35")

    pairs = [
        (0.2, "A", T_A, "C", T_C_body, INK, in_thermal_equilibrium(T_A, T_C_body)),
        (4.4, "B", T_B, "C", T_C_body, FLOW, in_thermal_equilibrium(T_B, T_C_body)),
        (8.6, "A", T_A, "B", T_B, ALT, in_thermal_equilibrium(T_A, T_B)),
    ]
    for x0, l1, t1, l2, t2, col, eq in pairs:
        block(x0, 2.4, 1.3, 1.5, l1, t1, col)
        block(x0 + 2.0, 2.4, 1.3, 1.5, l2, t2, col)
        ax.text(x0 + 1.65, 3.1, r"$\longleftrightarrow$", ha="center",
                va="center", fontsize=13, color="0.45")
        ax.text(x0 + 1.65, 2.0, "equilibrium" if eq else "not equilibrium",
                ha="center", fontsize=8.5, color="0.35")
    ax.text(4.0, 3.1, "and", ha="center", va="center", fontsize=10, color="0.4")
    ax.text(8.2, 3.1, r"$\Rightarrow$", ha="center", va="center", fontsize=16,
            color="0.25")
    ax.text(6.0, 4.6, r"Zeroth law: A$\sim$C and B$\sim$C  $\Rightarrow$  A$\sim$B"
                      r"    (zeroth_law $\rightarrow$ %s)"
            % zeroth_law(T_A, T_B, T_C_body), ha="center", fontsize=11,
            color="0.15")
    ax.text(6.0, 0.75, r"C is the thermometer: it never touches A and B together,"
                       r" yet certifies they would not exchange heat.",
            ha="center", fontsize=9, color="0.4")
    ax.text(6.0, 0.25, r"A body at %d K instead (in_thermal_equilibrium "
                       r"$\rightarrow$ %s) would break the chain."
            % (T_D, in_thermal_equilibrium(T_A, T_D)), ha="center", fontsize=9,
            color="0.4")
    _save(fig, "fig2_zeroth_law.svg")
    caps["fig2_zeroth_law.svg"] = (
        r"The zeroth law is the licence to use a thermometer. If body A and body "
        r"B each separately reach equilibrium with a third body C, then A and B "
        r"are in equilibrium with each other (zeroth_law) — even though they were "
        r"never brought into contact. That transitivity is what allows one number "
        r"to be attached to a state and called its temperature: 'thermal "
        r"equilibrium' is an equivalence relation, and temperature is the label "
        r"on its classes. The law is numbered zeroth because it was recognised as "
        r"a prerequisite only after the first and second laws were established.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
