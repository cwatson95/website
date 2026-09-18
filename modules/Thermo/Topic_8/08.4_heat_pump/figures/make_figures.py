"""Module 8.4 figures — why a heat pump beats a resistance heater, and how the
vapour-compression COP is read off four enthalpies.

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
from heat_pump import (                           # noqa: E402
    heat_rejected, cop_refrigeration, cop_heat_pump,
    carnot_cop_refrigeration, carnot_cop_heat_pump,
    cop_ref_from_enthalpies, cop_hp_from_enthalpies,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — a heat pump heating a 293 K house from outdoor air.  The ideal COP
    # collapses as the outside gets colder, but even a real machine at 45% of
    # Carnot stays well above the resistance heater's COP of exactly 1.
    T_house = 293.0
    T_out = np.linspace(253.0, 288.0, 300)
    gamma_max = np.array([carnot_cop_heat_pump(T_house, t) for t in T_out])
    gamma_real = 0.45 * gamma_max

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot(T_out - 273.15, gamma_max, color=INK, lw=2.3,
            label=r"Carnot ceiling $\gamma_{max}=T_H/(T_H-T_C)$")
    ax.plot(T_out - 273.15, gamma_real, color=FLOW, lw=2.2, ls="--",
            label=r"a real unit (45% of Carnot)")
    ax.axhline(1.0, color="0.5", lw=1.5, ls="-.",
               label=r"resistance heater ($\gamma=1$)")
    ax.fill_between(T_out - 273.15, 1.0, gamma_real, color=ALT, alpha=0.12,
                    lw=0)
    ax.set_xlim(-20, 15)
    ax.set_ylim(0, 26)
    ax.set_xlabel(r"outdoor temperature ($^\circ$C)    (house held at 20 $^\circ$C)")
    ax.set_ylabel(r"heat delivered per unit of work")
    ax.set_title(r"A heat pump moves heat instead of making it")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_heat_pump_vs_heater.svg")
    caps["fig1_heat_pump_vs_heater.svg"] = (
        r"An electric resistance heater turns one joule of work into exactly one "
        r"joule of heat. A heat pump instead MOVES heat, so its coefficient of "
        r"performance $\gamma=Q_H/W$ (cop_heat_pump) can be many times larger — "
        r"bounded by $T_H/(T_H-T_C)$ (carnot_cop_heat_pump). Holding a house at "
        r"20 $^\circ$C, the ideal COP is "
        + "%.1f" % carnot_cop_heat_pump(T_house, 283.0) + r" when it is "
        r"10 $^\circ$C outside but only "
        + "%.1f" % carnot_cop_heat_pump(T_house, 253.0) + r" at $-20\,^\circ$C, "
        r"because the heat must be lifted further. The shaded band is the "
        r"margin a real unit keeps over resistance heating; it narrows in exactly "
        r"the weather when heat is needed most.")

    # Fig 2 — where those numbers come from in a vapour-compression cycle: four
    # enthalpies around the loop.  Sweep the compressor exit enthalpy (a proxy
    # for how hard the compressor works) and watch both COPs fall together.
    h1, h3 = 241.0, 91.5                            # kJ/kg: evaporator exit, condenser exit
    h4 = h3                                         # throttle is isenthalpic
    h2 = np.linspace(268.0, 300.0, 300)
    beta = np.array([cop_ref_from_enthalpies(h1, x, h4) for x in h2])
    gamma = np.array([cop_hp_from_enthalpies(h1, x, h3) for x in h2])

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(h2, gamma, color=INK, lw=2.3, label=r"heat pump $\gamma=(h_2-h_3)/(h_2-h_1)$")
    ax.plot(h2, beta, color=FLOW, lw=2.2, ls="--",
            label=r"refrigerator $\beta=(h_1-h_4)/(h_2-h_1)$")
    ax.plot(h2, gamma - beta, color="0.55", lw=1.5, ls=":",
            label=r"difference $=1$ exactly")
    ax.set_xlim(268, 300)
    ax.set_ylim(0, 8)
    ax.set_xlabel(r"compressor exit enthalpy $h_2$ (kJ/kg)")
    ax.set_ylabel(r"coefficient of performance")
    ax.set_title(r"Vapour-compression COPs from four enthalpies")
    ax.legend(loc="upper right", frameon=False, fontsize=8.5)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_vapour_compression_cop.svg")
    caps["fig2_vapour_compression_cop.svg"] = (
        r"The same machine scored as a refrigerator and as a heat pump. Around a "
        r"vapour-compression loop the refrigeration effect is $h_1-h_4$, the "
        r"heating effect is $h_2-h_3$, and the compressor work is $h_2-h_1$, so "
        r"both figures of merit (cop_ref_from_enthalpies, "
        r"cop_hp_from_enthalpies) come from four table look-ups. As the "
        r"compressor is asked to do more work both COPs fall, but their "
        r"difference stays pinned at exactly 1 — the first law again, since the "
        r"heat delivered upstairs is the heat absorbed downstairs PLUS the work "
        r"(heat_rejected). Whether you call the device a fridge or a heat pump "
        r"is a question about which side of it you care about.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
