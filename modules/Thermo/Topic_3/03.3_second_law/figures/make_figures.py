"""Module 3.3 figures — the Carnot ceiling that divides possible power cycles from
impossible ones, and the work actually extractable from a given heat input.

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
from second_law import (                          # noqa: E402
    carnot_efficiency, max_work_from_heat, efficiency_is_possible,
    kelvin_planck_allows, carnot_cop_refrigerator, carnot_cop_heat_pump,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the ceiling.  Everything above the Carnot curve is forbidden by the
    # second law (efficiency_is_possible -> False); a real engine lives somewhere
    # underneath it.  Kelvin-Planck kills the whole eta = 1 line.
    T_C = 300.0
    T_H = np.linspace(T_C + 1.0, 1500.0, 400)
    eta_max = np.array([carnot_efficiency(T_C, t) for t in T_H])

    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.fill_between(T_H, eta_max, 1.0, color=FLOW, alpha=0.13, lw=0)
    ax.plot(T_H, eta_max, color=INK, lw=2.4,
            label=r"Carnot ceiling $\eta_{max}=1-T_C/T_H$")
    ax.plot(T_H, 0.6 * eta_max, color=ALT, lw=2.0, ls="--",
            label=r"a real engine (60% of Carnot)")
    ax.axhline(1.0, color="0.55", lw=1.3, ls="-.")
    ax.text(760, 0.86, "FORBIDDEN by the second law", color=FLOW, fontsize=10,
            ha="center")
    ax.text(1480, 0.955, r"$\eta=1$ violates Kelvin-Planck", color="0.4",
            fontsize=8.5, ha="right")
    ax.set_xlim(T_C, 1500)
    ax.set_ylim(0, 1.06)
    ax.set_xlabel(r"hot-reservoir temperature $T_H$ (K)    ($T_C=300$ K)")
    ax.set_ylabel(r"thermal efficiency $\eta$")
    ax.set_title(r"No power cycle may cross the Carnot line")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_carnot_ceiling.svg")
    caps["fig1_carnot_ceiling.svg"] = (
        r"The second law drawn as a boundary. Between reservoirs at $T_C=300$ K "
        r"and $T_H$, no power cycle may have an efficiency above "
        r"$\eta_{max}=1-T_C/T_H$ (carnot_efficiency); the shaded region is ruled "
        r"out, and efficiency_is_possible returns False anywhere inside it. Even "
        r"at 1500 K the ceiling is only "
        + "%.0f" % (100 * carnot_efficiency(T_C, 1500.0)) + r"%, and it reaches "
        r"1 only as $T_H\to\infty$ — the Kelvin-Planck statement, that no cycle "
        r"can convert heat from a single reservoir entirely into work "
        r"(kelvin_planck_allows). Real engines run well below the line.")

    # Fig 2 — the same statement in energy rather than ratio: of 1000 kJ supplied
    # at T_H, how much can leave as work?  The rest MUST be dumped to the cold
    # reservoir.  Stacked so the two shares read as one budget.
    Q_H = 1000.0
    W_max = np.array([max_work_from_heat(Q_H, T_C, t) for t in T_H])

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.fill_between(T_H, 0, W_max, color=INK, alpha=0.30, lw=0,
                    label=r"available as work  $\eta_{max}Q_H$")
    ax.fill_between(T_H, W_max, Q_H, color=FLOW, alpha=0.22, lw=0,
                    label=r"must be rejected to $T_C$")
    ax.plot(T_H, W_max, color=INK, lw=2.2)
    ax.set_xlim(T_C, 1500)
    ax.set_ylim(0, Q_H)
    ax.set_xlabel(r"hot-reservoir temperature $T_H$ (K)")
    ax.set_ylabel(r"energy per 1000 kJ supplied (kJ)")
    ax.set_title(r"How much of a heat input can become work")
    ax.legend(loc="center right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_max_work_budget.svg")
    caps["fig2_max_work_budget.svg"] = (
        r"The second law as an energy budget rather than a ratio. Of 1000 kJ "
        r"drawn from a reservoir at $T_H$ and rejected to one at 300 K, the lower "
        r"band is the most that can ever leave as work (max_work_from_heat) and "
        r"the upper band is waste heat that MUST be discarded — not a design "
        r"flaw, a requirement. At 600 K only "
        + "%.0f" % max_work_from_heat(Q_H, T_C, 600.0) + r" kJ is available; "
        r"doubling the source to 1200 K raises it to just "
        + "%.0f" % max_work_from_heat(Q_H, T_C, 1200.0) + r" kJ. Run the same "
        r"cycle backwards and the ratios invert into the refrigerator and "
        r"heat-pump COPs (carnot_cop_refrigerator, carnot_cop_heat_pump), which "
        r"exceed 1 precisely because they move heat rather than make work.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
