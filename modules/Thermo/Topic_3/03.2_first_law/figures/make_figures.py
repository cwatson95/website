"""Module 3.2 figures — the first law as a plane over (Q, W), and the cycle
identity W_cycle = Q_cycle that it forces.

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
from first_law import (                           # noqa: E402
    delta_E, cycle_net_work, power_cycle_work, first_law_holds,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — E2 - E1 = Q - W is a plane over the (Q, W) plane.  Its contours are
    # parallel 45-degree lines of constant energy change; the zero contour is the
    # locus of cyclic (or otherwise energy-neutral) processes.
    Q = np.linspace(-100.0, 100.0, 220)
    W = np.linspace(-100.0, 100.0, 220)
    QQ, WW = np.meshgrid(Q, W)
    dE = delta_E(QQ, WW)

    # sequential magnitude -> one hue, light to dark (never a rainbow)
    fig, ax = plt.subplots(figsize=(6.2, 3.9))
    cs = ax.contourf(QQ, WW, dE, levels=14, cmap="Purples", alpha=0.62)
    line = ax.contour(QQ, WW, dE, levels=[0.0], colors=[FLOW], linewidths=2.4)
    ax.clabel(line, fmt={0.0: r"$\Delta E=0$"}, fontsize=9.5)
    cb = fig.colorbar(cs, ax=ax, pad=0.02)
    cb.set_label(r"$\Delta E=Q-W$ (kJ)", fontsize=9.5)
    ax.axhline(0, color="0.65", lw=0.8)
    ax.axvline(0, color="0.65", lw=0.8)
    ax.set_xlabel(r"heat added to the system $Q$ (kJ)")
    ax.set_ylabel(r"work done by the system $W$ (kJ)")
    ax.set_title(r"First law: $E_2-E_1=Q-W$")
    _save(fig, "fig1_first_law_plane.svg")
    caps["fig1_first_law_plane.svg"] = (
        r"The closed-system first law $E_2-E_1=Q-W$ (delta_E) drawn over the "
        r"whole $(Q,W)$ plane. Because it is linear, its contours are parallel "
        r"lines at 45$^\circ$: any heat input can be matched by an equal work "
        r"output with no change in stored energy. The highlighted $\Delta E=0$ "
        r"contour is exactly the condition a cycle must satisfy, since a cycle "
        r"returns the system to its initial state. Everything above that line "
        r"drains the system's energy; everything below charges it.")

    # Fig 2 — on the zero contour the first law becomes W_cycle = Q_cycle.  For a
    # power cycle taking Q_in and rejecting Q_out, the net work is the difference
    # (power_cycle_work); the dashed limit W = Q_in is the unreachable Q_out = 0
    # case the SECOND law will later forbid.
    # over a cycle dE = 0, so the net work IS the net heat; check the identity
    assert first_law_holds(600.0, cycle_net_work(600.0), 0.0)
    Q_in = np.linspace(0.0, 1000.0, 200)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for Q_out, c, ls in ((200.0, INK, "-"), (400.0, FLOW, "--"), (600.0, ALT, ":")):
        Wnet = np.array([max(power_cycle_work(q, Q_out), 0.0) for q in Q_in])
        ax.plot(Q_in, Wnet, color=c, lw=2.1, ls=ls,
                label=r"$Q_{out}=%d$ kJ" % Q_out)
    ax.plot(Q_in, Q_in, color="0.6", lw=1.4, ls="-.",
            label=r"$Q_{out}=0$: forbidden by the 2nd law")
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1000)
    ax.set_xlabel(r"heat supplied per cycle $Q_{in}$ (kJ)")
    ax.set_ylabel(r"net work per cycle $W_{cycle}$ (kJ)")
    ax.set_title(r"Over a cycle the first law gives $W_{cycle}=Q_{cycle}$")
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_power_cycle.svg")
    caps["fig2_power_cycle.svg"] = (
        r"A cycle stores no energy, so the first law collapses to "
        r"$W_{cycle}=Q_{cycle}$ (cycle_net_work) and a power cycle's net work is "
        r"simply what it takes in minus what it throws away, "
        r"$W=Q_{in}-Q_{out}$ (power_cycle_work). Supplying 1000 kJ while "
        r"rejecting 400 kJ yields "
        + "%.0f" % power_cycle_work(1000.0, 400.0) + r" kJ of work, and "
        r"first_law_holds confirms the books balance. Nothing in the first law "
        r"forbids the grey line $Q_{out}=0$ — a cycle converting heat entirely "
        r"into work. Ruling it out takes the second law (module 3.3).")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
