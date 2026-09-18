"""Module 2.5 figures — kinetic energy is quadratic in speed, so stopping distance
and the speed bought by a fixed work input both behave counter-intuitively.

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
from kinetic_energy import (                      # noqa: E402
    kinetic_energy, delta_KE, speed_after_work,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — KE = 1/2 m V^2 for three masses.  The quadratic is the point:
    # doubling the speed quadruples the energy that has to be dissipated to stop.
    V = np.linspace(0.0, 40.0, 300)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for m, c, ls in ((800.0, INK, "-"), (1500.0, FLOW, "--"), (3000.0, ALT, ":")):
        KE = np.array([kinetic_energy(m, v) for v in V]) / 1000.0      # kJ
        ax.plot(V, KE, color=c, lw=2.1, ls=ls, label=r"$m=%d$ kg" % m)
    ax.set_xlim(0, 40)
    ax.set_xlabel(r"speed $V$ (m/s)")
    ax.set_ylabel(r"kinetic energy $\frac{1}{2}mV^2$ (kJ)")
    ax.set_title(r"Kinetic energy is quadratic in speed")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_ke_vs_speed.svg")
    caps["fig1_ke_vs_speed.svg"] = (
        r"$KE=\tfrac12mV^2$ (kinetic_energy) for three vehicle-scale masses. The "
        r"curvature carries the practical content: a 1500 kg car at 20 m/s holds "
        + "%.0f" % (kinetic_energy(1500.0, 20.0) / 1000.0) + r" kJ, but at "
        r"40 m/s it holds " + "%.0f" % (kinetic_energy(1500.0, 40.0) / 1000.0) +
        r" kJ — four times as much for twice the speed. Braking from 40 to "
        r"20 m/s alone sheds "
        + "%.0f" % (abs(delta_KE(1500.0, 40.0, 20.0)) / 1000.0) +
        r" kJ, all of which the brakes must turn into heat. This term is usually "
        r"negligible next to internal energy, which is why closed-system problems "
        r"drop it, but it dominates in nozzles and in collisions.")

    # Fig 2 — invert it.  Adding a fixed amount of work to a body already moving
    # buys less and less speed, because speed_after_work is a square root.
    W = np.linspace(0.0, 600.0e3, 300)
    m = 1500.0
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for V1, c, ls in ((0.0, INK, "-"), (20.0, FLOW, "--"), (30.0, ALT, ":")):
        V2 = np.array([speed_after_work(m, V1, w) for w in W])
        ax.plot(W / 1000.0, V2, color=c, lw=2.1, ls=ls,
                label=r"starting at $V_1=%d$ m/s" % V1)
    ax.set_xlim(0, 600)
    ax.set_xlabel(r"net work added $W$ (kJ)   to a 1500 kg body")
    ax.set_ylabel(r"resulting speed $V_2$ (m/s)")
    ax.set_title(r"Work-energy theorem: $W_{net}=\Delta KE$")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_speed_after_work.svg")
    caps["fig2_speed_after_work.svg"] = (
        r"The work-energy theorem run backwards: given the net work delivered to "
        r"a 1500 kg body, what speed results (speed_after_work, from "
        r"$\tfrac12mV_2^2=\tfrac12mV_1^2+W$)? Because the answer is a square "
        r"root, the returns diminish sharply — the first 300 kJ takes a body from "
        r"rest to " + "%.1f" % speed_after_work(1500.0, 0.0, 300e3) + r" m/s, "
        r"while the second 300 kJ adds only "
        + "%.1f" % (speed_after_work(1500.0, 0.0, 600e3) - speed_after_work(1500.0, 0.0, 300e3)) +
        r" m/s more. The same work does less for a body that is already fast.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
