"""Module 13.3 figures — the property jumps across a normal shock, and the
stagnation-pressure loss that measures its irreversibility.

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
from shock import (                               # noqa: E402
    mach_after_shock, shock_temperature_ratio, shock_pressure_ratio,
    stagnation_pressure_ratio_across_shock, sonic_area_ratio_across_shock,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

K = 1.4


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — everything jumps at once.  A normal shock always takes a
    # supersonic flow to subsonic, and the pressure and temperature ratios grow
    # without bound as the upstream Mach number rises.
    Mx = np.linspace(1.0, 4.0, 400)
    My = np.array([mach_after_shock(m, K) for m in Mx])
    pr = np.array([shock_pressure_ratio(m, K) for m in Mx])
    Tr = np.array([shock_temperature_ratio(m, K) for m in Mx])

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(6.4, 3.4))
    axL.plot(Mx, My, color=INK, lw=2.3)
    axL.axhline(1.0, color="0.6", lw=1.1, ls="-.")
    axL.fill_between(Mx, My, 1.0, color=INK, alpha=0.10, lw=0)
    axL.text(2.5, 0.78, "always subsonic\nafter the shock", fontsize=9,
             color="0.35", ha="center")
    axL.set_xlim(1, 4)
    axL.set_ylim(0.4, 1.15)
    axL.set_xlabel(r"upstream $M_x$")
    axL.set_ylabel(r"downstream $M_y$")
    axL.set_title(r"the flow is decelerated", fontsize=10.5)
    axL.grid(alpha=0.25, lw=0.6)

    axR.plot(Mx, pr, color=FLOW, lw=2.3, label=r"$p_y/p_x$")
    axR.plot(Mx, Tr, color=ALT, lw=2.3, ls="--", label=r"$T_y/T_x$")
    axR.set_xlim(1, 4)
    axR.set_xlabel(r"upstream $M_x$")
    axR.set_ylabel(r"jump across the shock")
    axR.set_title(r"...and violently compressed", fontsize=10.5)
    axR.legend(loc="upper left", frameon=False, fontsize=9)
    axR.grid(alpha=0.25, lw=0.6)
    fig.tight_layout()
    _save(fig, "fig1_shock_jumps.svg")
    caps["fig1_shock_jumps.svg"] = (
        r"A normal shock is a discontinuity a few mean free paths thick across "
        r"which every property jumps at once. The downstream Mach number "
        r"(mach_after_shock) is ALWAYS subsonic — that is a theorem, not a "
        r"coincidence — and it approaches an asymptote of "
        + "%.3f" % mach_after_shock(50.0, K) + r" for very strong shocks. "
        r"Meanwhile the static pressure and temperature ratios "
        r"(shock_pressure_ratio, shock_temperature_ratio) grow without limit: at "
        r"$M_x=3$ the pressure rises by a factor of "
        + "%.1f" % shock_pressure_ratio(3.0, K) + r" and the temperature by "
        + "%.2f" % shock_temperature_ratio(3.0, K) + r". The heating is why "
        r"re-entry vehicles need thermal protection, and why the shock is a "
        r"compression device you cannot simply run backwards.")

    # Fig 2 — the price.  A shock is adiabatic, so stagnation TEMPERATURE is
    # preserved; but it is strongly irreversible, so stagnation PRESSURE is lost,
    # and that loss is the usable-work loss.
    po_ratio = np.array([stagnation_pressure_ratio_across_shock(m, K) for m in Mx])
    A_ratio = np.array([sonic_area_ratio_across_shock(m, K) for m in Mx])

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot(Mx, po_ratio, color=INK, lw=2.4, label=r"$p_{oy}/p_{ox}$ (retained)")
    ax.plot(Mx, 1.0 - po_ratio, color=FLOW, lw=2.2, ls="--",
            label=r"fraction lost")
    ax.axhline(1.0, color="0.7", lw=1.0, ls=":")
    for m in (1.5, 2.5, 3.5):
        ax.plot([m], [stagnation_pressure_ratio_across_shock(m, K)], marker="o",
                ms=6.5, mfc="white", mec=ALT, mew=1.7, ls="none")
        ax.annotate("%.2f" % stagnation_pressure_ratio_across_shock(m, K),
                    xy=(m, stagnation_pressure_ratio_across_shock(m, K)),
                    xytext=(m + 0.06, stagnation_pressure_ratio_across_shock(m, K) + 0.05),
                    fontsize=9, color="0.35")
    ax.set_xlim(1, 4)
    ax.set_ylim(0, 1.1)
    ax.set_xlabel(r"upstream Mach number $M_x$")
    ax.set_ylabel(r"stagnation pressure ratio")
    ax.set_title(r"A shock costs stagnation pressure, not stagnation temperature")
    ax.legend(loc="center right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_stagnation_loss.svg")
    caps["fig2_stagnation_loss.svg"] = (
        r"A shock is adiabatic, so the stagnation TEMPERATURE passes through "
        r"unchanged — no energy is lost. What is lost is stagnation PRESSURE "
        r"(stagnation_pressure_ratio_across_shock), and that is exactly the "
        r"exergy destroyed by the irreversibility. The penalty accelerates "
        r"sharply with shock strength: only "
        + "%.0f" % (100 * (1 - stagnation_pressure_ratio_across_shock(1.5, K))) +
        r"% is lost at $M_x=1.5$ but "
        + "%.0f" % (100 * (1 - stagnation_pressure_ratio_across_shock(3.5, K))) +
        r"% at $M_x=3.5$. This is why supersonic inlets are designed to "
        r"decelerate the flow through several WEAK oblique shocks rather than "
        r"one strong normal shock. Because $A_x^*/A_y^*=p_{oy}/p_{ox}$ "
        r"(sonic_area_ratio_across_shock), the same loss shows up as an "
        r"effective throat that has grown behind the shock.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
