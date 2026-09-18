"""Module 9.1 figures — the Carnot efficiency over the whole reservoir plane, and
the symmetric work bounds it puts on engines and heat pumps.

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
from carnot_cycle import (                        # noqa: E402
    carnot_efficiency, carnot_efficiency_from_heat, max_work_from_heat,
    min_work_heat_pump, efficiency_is_possible,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the ceiling over the whole plane of reservoir pairs.  Contours of
    # constant efficiency are straight lines through the origin, because eta
    # depends only on the RATIO T_C/T_H.
    T_C = np.linspace(250.0, 700.0, 240)
    T_H = np.linspace(300.0, 1600.0, 240)
    TC, TH = np.meshgrid(T_C, T_H)
    eta = np.where(TH > TC, 1.0 - TC / TH, np.nan)

    fig, ax = plt.subplots(figsize=(6.2, 3.9))
    cs = ax.contourf(TC, TH, eta, levels=np.linspace(0, 0.8, 17), cmap="Purples")
    lines = ax.contour(TC, TH, eta, levels=[0.2, 0.4, 0.6], colors=[INK],
                       linewidths=1.4)
    ax.clabel(lines, fmt="%.1f", fontsize=9)
    cb = fig.colorbar(cs, ax=ax, pad=0.02)
    cb.set_label(r"$\eta_{max}=1-T_C/T_H$", fontsize=9.5)
    ax.plot([288.0], [823.0], marker="o", ms=8, mfc="white", mec=FLOW, mew=1.9,
            ls="none")
    ax.annotate(r"a steam plant: $\eta_{max}=%.2f$" % carnot_efficiency(288.0, 823.0),
                xy=(288.0, 823.0), xytext=(340, 1150), fontsize=9, color="0.25",
                arrowprops=dict(arrowstyle="->", color="0.45", lw=1.0))
    ax.set_xlabel(r"cold reservoir $T_C$ (K)")
    ax.set_ylabel(r"hot reservoir $T_H$ (K)")
    ax.set_title(r"The Carnot ceiling over every reservoir pair")
    _save(fig, "fig1_carnot_efficiency_map.svg")
    caps["fig1_carnot_efficiency_map.svg"] = (
        r"The maximum efficiency of ANY cycle operating between two reservoirs "
        r"(carnot_efficiency), mapped over the whole plane. The contours are "
        r"straight lines through the origin because $\eta$ depends only on the "
        r"ratio $T_C/T_H$, not on either temperature alone — the reason efficiency "
        r"is improved far more cheaply by raising the source than by chilling the "
        r"sink. A steam plant boiling at 550 $^\circ$C and condensing against a "
        r"15 $^\circ$C river is capped at "
        + "%.2f" % carnot_efficiency(288.0, 823.0) + r", and real plants reach "
        r"about three-quarters of that. efficiency_is_possible tests a claimed "
        r"efficiency against this surface; carnot_efficiency_from_heat recovers "
        r"the same number from measured heat quantities.")

    # Fig 2 — the two bounds are mirror images.  Getting work OUT of heat is
    # capped; putting heat IN with a heat pump has a floor.  Both are set by the
    # same Carnot factor, and both are per 1000 kJ of heat at T_H.
    Q = 1000.0
    T_C0 = 300.0
    T_H = np.linspace(320.0, 1200.0, 400)
    W_out = np.array([max_work_from_heat(Q, T_C0, t) for t in T_H])
    W_in = np.array([min_work_heat_pump(Q, T_C0, t) for t in T_H])

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(T_H, W_out, color=INK, lw=2.4,
            label=r"engine: MOST work obtainable from $Q_H$")
    ax.plot(T_H, W_in, color=FLOW, lw=2.4, ls="--",
            label=r"heat pump: LEAST work to deliver $Q_H$")
    ax.set_xlim(320, 1200)
    ax.set_ylim(0, 800)
    ax.set_xlabel(r"hot reservoir $T_H$ (K)    ($T_C=300$ K, $Q_H=1000$ kJ)")
    ax.set_ylabel(r"work (kJ)")
    ax.set_title(r"The same factor bounds both directions")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_work_bounds.svg")
    caps["fig2_work_bounds.svg"] = (
        r"Run a reversible cycle forwards and it delivers the most work any "
        r"engine could from $Q_H$ (max_work_from_heat); run it backwards and it "
        r"consumes the least work any heat pump could to deliver the same $Q_H$ "
        r"(min_work_heat_pump). Both curves are $\eta_{max}Q_H$ — they coincide, "
        r"which is precisely the statement that a reversible cycle can be "
        r"reversed at no cost. The gap between them is zero only for the "
        r"reversible machine; any real pair of devices leaves a shortfall, and "
        r"that shortfall is the exergy destroyed in module 4.3. Delivering "
        r"1000 kJ at 400 K from a 300 K source takes at least "
        + "%.0f" % min_work_heat_pump(Q, T_C0, 400.0) + r" kJ of work.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
