"""Module 7.1 figures — the three cycle performance metrics against their common
Carnot ceiling, and the isentropic efficiencies that grade real components.

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
from efficiency import (                          # noqa: E402
    thermal_efficiency, thermal_efficiency_from_heat, cop_refrigerator,
    cop_heat_pump, carnot_efficiency, carnot_cop_refrigerator,
    carnot_cop_heat_pump, isentropic_turbine_efficiency, turbine_work_actual,
    isentropic_compressor_efficiency, compressor_work_actual,
    efficiency_is_possible,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the same two reservoirs, three different questions.  eta is bounded
    # by 1; the two COPs are not bounded at all, so they get their own panel
    # rather than a second y-axis.
    T_C = 300.0
    T_H = np.linspace(310.0, 900.0, 400)
    eta = np.array([carnot_efficiency(T_C, t) for t in T_H])
    beta = np.array([carnot_cop_refrigerator(T_C, t) for t in T_H])
    gamma = np.array([carnot_cop_heat_pump(T_C, t) for t in T_H])

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(6.4, 3.4))
    axL.plot(T_H, eta, color=INK, lw=2.3)
    axL.fill_between(T_H, eta, 1.0, color=FLOW, alpha=0.11, lw=0)
    axL.text(600, 0.82, "impossible", fontsize=9, color=FLOW, ha="center")
    axL.set_ylim(0, 1)
    axL.set_xlabel(r"$T_H$ (K)")
    axL.set_ylabel(r"thermal efficiency $\eta$")
    axL.set_title(r"power cycle", fontsize=11)
    axL.grid(alpha=0.25, lw=0.6)

    axR.plot(T_H, gamma, color=INK, lw=2.3, label=r"heat pump $\gamma$")
    axR.plot(T_H, beta, color=FLOW, lw=2.1, ls="--", label=r"refrigerator $\beta$")
    axR.set_ylim(0, 22)
    axR.set_xlabel(r"$T_H$ (K)")
    axR.set_ylabel(r"coefficient of performance")
    axR.set_title(r"reversed cycle", fontsize=11)
    axR.legend(loc="upper right", frameon=False, fontsize=9)
    axR.grid(alpha=0.25, lw=0.6)
    fig.tight_layout()
    _save(fig, "fig1_metrics_and_ceilings.svg")
    caps["fig1_metrics_and_ceilings.svg"] = (
        r"Three ways to score the same pair of reservoirs, kept on separate axes "
        r"because their ranges have nothing in common. A power cycle is graded by "
        r"$\eta=W/Q_{in}$, capped by the Carnot value (carnot_efficiency) with "
        r"everything above it forbidden — efficiency_is_possible enforces the "
        r"line. Run the cycle backwards and the figure of merit becomes a "
        r"coefficient of performance, which is NOT capped by 1 and diverges as "
        r"the two reservoirs approach each other: at $T_H=310$ K the ideal heat "
        r"pump delivers " + "%.0f" % carnot_cop_heat_pump(T_C, 310.0) + r" units "
        r"of heat per unit of work. $\gamma=\beta+1$ always, because the heat "
        r"pump also gets to keep the work.")

    # Fig 2 — component grading.  A turbine's actual work is eta times the ideal;
    # a compressor's actual input is the ideal DIVIDED by eta.  The asymmetry is
    # the point: inefficiency subtracts from output but adds to input.
    eta_c = np.linspace(0.55, 1.0, 300)
    # a steam expansion and an air compression, as (h1, h2s) pairs
    ht1, ht2s = 3230.0, 2480.0                      # turbine:    w_s = 750 kJ/kg
    hc1, hc2s = 293.5, 573.5                        # compressor: w_s = 280 kJ/kg
    wt_s = ht1 - ht2s
    wc_s = hc2s - hc1
    wt = np.array([turbine_work_actual(e, ht1, ht2s) for e in eta_c])
    wc = np.array([compressor_work_actual(e, hc1, hc2s) for e in eta_c])

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(eta_c, wt / wt_s, color=INK, lw=2.3,
            label=r"turbine: $w=\eta_t\,w_s$  (output falls)")
    ax.plot(eta_c, wc / wc_s, color=FLOW, lw=2.3, ls="--",
            label=r"compressor: $w=w_s/\eta_c$  (input rises)")
    ax.axhline(1.0, color="0.6", lw=1.1, ls="-.")
    ax.set_xlim(0.55, 1.0)
    ax.set_xlabel(r"isentropic efficiency $\eta$")
    ax.set_ylabel(r"actual work / isentropic work")
    ax.set_title(r"Irreversibility hurts twice in a cycle")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_isentropic_component_grading.svg")
    caps["fig2_isentropic_component_grading.svg"] = (
        r"Why component losses compound in a cycle. The isentropic efficiency "
        r"multiplies a turbine's output (isentropic_turbine_efficiency, "
        r"turbine_work_actual) but DIVIDES into a compressor's input "
        r"(isentropic_compressor_efficiency, compressor_work_actual), so the two "
        r"curves bend in opposite directions away from the ideal. At $\eta=0.8$ "
        r"the turbine returns 80% of its ideal work while the compressor demands "
        + "%.0f" % (100 * compressor_work_actual(0.8, hc1, hc2s) / wc_s) + r"% of "
        r"its ideal input. Since the net work of a gas-turbine cycle is the "
        r"difference of two large numbers, both errors eat the same margin — the "
        r"back work ratio problem that Topic 9 returns to.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
