"""CM-04 figures — the work integral, the work-energy theorem, and work as area under F.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"
matplotlib.rcParams["font.size"] = 11
import matplotlib.pyplot as plt                    # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from work_energy import kinetic_energy, work       # noqa: E402

INK, FLOW, ALT, FOUR = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — work-energy theorem: accumulated work == kinetic energy gained.
    m, F0 = 2.0, 3.0
    a = F0 / m
    force_field = lambda x, y, z: (F0, 0.0, 0.0)
    path = lambda s: (0.5 * a * s * s, 0.0, 0.0)    # x(s) under constant force, from rest
    Tt = np.linspace(0.05, 2.5, 60)
    disp = [0.5 * a * float(t) ** 2 for t in Tt]
    W = [work(force_field, path, 0.0, float(t)) for t in Tt]
    dT = [kinetic_energy(m, (a * float(t), 0.0, 0.0)) for t in Tt]   # T(t) starting from rest
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(disp, W, color=FLOW, lw=2.4, label=r"work $\int \mathbf{F}\cdot d\mathbf{l}$")
    ax.plot(disp, dT, color=INK, lw=2, ls="--", label=r"$\Delta T=\frac{1}{2}mv^2$")
    ax.set_xlabel("displacement $x$ (m)"); ax.set_ylabel("energy (J)")
    ax.set_title(r"Work-energy theorem: $W=\Delta T$ (constant force, from rest)")
    ax.legend(loc="upper left", frameon=False)
    _save(fig, "fig1_work_energy_theorem.svg")
    caps["fig1_work_energy_theorem.svg"] = (
        "For a mass pushed from rest by a constant force, the work computed by the "
        "module's line-integral work() (orange) matches the kinetic energy from "
        "kinetic_energy() (dashed) at every displacement: W = Delta T, the work-energy theorem.")

    # Fig 2 — work as the area under F vs distance, for two force laws.
    Xs = np.linspace(0.0, 3.0, 60)
    Fconst = lambda x, y, z: (2.0, 0.0, 0.0)        # constant force
    Flin = lambda x, y, z: (2.0 * x, 0.0, 0.0)      # position-dependent (spring-like) force
    straight = lambda s: (s, 0.0, 0.0)              # straight push, parameter s = distance
    Wc = [work(Fconst, straight, 0.0, float(X)) for X in Xs]
    Wl = [work(Flin, straight, 0.0, float(X)) for X in Xs]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(Xs, Wc, color=INK, lw=2, label=r"constant $F=2$:  $W=2x$")
    ax.plot(Xs, Wl, color=ALT, lw=2, label=r"linear $F=2x$:  $W=x^2$")
    ax.set_xlabel("displacement $x$ (m)"); ax.set_ylabel(r"work $W$ (J)")
    ax.set_title(r"Work is the integral of force over distance")
    ax.legend(loc="upper left", frameon=False)
    _save(fig, "fig2_work_force_law.svg")
    caps["fig2_work_force_law.svg"] = (
        "Work accumulated by work() along a straight push for two force laws. A constant "
        "force gives work growing linearly with distance (W=2x); a force that grows with "
        "position (F=2x) gives quadratic work (W=x^2) -- work is the area under F vs x.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
