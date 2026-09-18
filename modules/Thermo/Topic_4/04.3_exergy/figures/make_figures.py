"""Module 4.3 figures — the Carnot factor that grades heat by its temperature, and
the exergy irreversibility destroys.

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
from exergy import (                              # noqa: E402
    exergy_transfer_heat, exergy_destruction, exergy_change_incompressible,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

T0 = 300.0                                         # dead-state temperature [K]


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — a joule of heat is not a joule of usefulness.  The Carnot factor
    # 1 - T0/Tb weights heat by the temperature it is delivered at: worthless at
    # the dead state, and NEGATIVE below it (cooling carries exergy the other
    # way).
    Tb = np.linspace(200.0, 1200.0, 400)
    frac = np.array([exergy_transfer_heat(1.0, T0, t) for t in Tb])

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot(Tb, frac, color=INK, lw=2.4, label=r"$E_q/Q=1-T_0/T_b$")
    ax.axhline(0.0, color="0.6", lw=1.0)
    ax.axvline(T0, color=FLOW, lw=1.5, ls="--",
               label=r"dead state $T_0=300$ K: heat is worthless")
    ax.fill_between(Tb, frac, 0, where=(Tb < T0), color=FLOW, alpha=0.13, lw=0)
    ax.text(215, -0.55, "below $T_0$: exergy\nflows the other way", fontsize=9,
            color="0.35")
    for t in (400.0, 800.0, 1200.0):
        ax.plot([t], [exergy_transfer_heat(1.0, T0, t)], marker="o", ms=7,
                mfc="white", mec=ALT, mew=1.7, ls="none")
        ax.text(t, exergy_transfer_heat(1.0, T0, t) + 0.07,
                "%.0f%%" % (100 * exergy_transfer_heat(1.0, T0, t)),
                ha="center", fontsize=9, color="0.3")
    ax.set_xlim(200, 1200)
    ax.set_xlabel(r"boundary temperature $T_b$ (K)")
    ax.set_ylabel(r"useful fraction of the heat")
    ax.set_title(r"Exergy grades heat by the temperature it arrives at")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_carnot_factor.svg")
    caps["fig1_carnot_factor.svg"] = (
        r"Energy is conserved; exergy is not, and it is what actually gets sold. "
        r"Heat crossing a boundary at $T_b$ carries useful work potential only in "
        r"the proportion $1-T_0/T_b$ (exergy_transfer_heat) — the Carnot factor. "
        r"At 400 K just "
        + "%.0f" % (100 * exergy_transfer_heat(1.0, T0, 400.0)) + r"% of the heat "
        r"is convertible; at 1200 K, "
        + "%.0f" % (100 * exergy_transfer_heat(1.0, T0, 1200.0)) + r"%. At the "
        r"dead state itself the factor is zero: a large reservoir of 300 K heat "
        r"in a 300 K environment is thermodynamically worthless. Below $T_0$ the "
        r"factor goes negative, which is the statement that removing heat from a "
        r"cold body takes work.")

    # Fig 2 — Gouy-Stodola.  Whatever entropy a process produces is paid for in
    # destroyed exergy at the flat rate T0, so the loss line's slope is the dead
    # state temperature itself.
    sigma = np.linspace(0.0, 2.0, 200)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for T0v, c, ls in ((250.0, INK, "-"), (300.0, FLOW, "--"), (350.0, ALT, ":")):
        Ed = np.array([exergy_destruction(T0v, s) for s in sigma])
        ax.plot(sigma, Ed, color=c, lw=2.1, ls=ls, label=r"$T_0=%d$ K" % T0v)
    ax.set_xlim(0, 2)
    ax.set_xlabel(r"entropy produced $\sigma$ (kJ/K)")
    ax.set_ylabel(r"exergy destroyed $E_d=T_0\sigma$ (kJ)")
    ax.set_title(r"Gouy-Stodola: irreversibility has a price")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_exergy_destruction.svg")
    caps["fig2_exergy_destruction.svg"] = (
        r"The Gouy-Stodola relation $E_d=T_0\sigma$ (exergy_destruction) converts "
        r"the abstract entropy production of module 4.2 into lost kilojoules of "
        r"work potential. The relation is exactly linear and its slope is the "
        r"dead-state temperature, so the SAME irreversibility costs more in a "
        r"warm environment than a cold one: one kJ/K of entropy production "
        r"destroys " + "%.0f" % exergy_destruction(250.0, 1.0) + r" kJ at 250 K "
        r"but " + "%.0f" % exergy_destruction(350.0, 1.0) + r" kJ at 350 K. "
        r"exergy_change_incompressible applies the same accounting to a heated "
        r"solid, whose exergy is positive whether it is hotter OR colder than the "
        r"surroundings.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
