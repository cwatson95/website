"""Module 2.1 figures — work as the area under a force-displacement curve (the
linear spring), and the everyday work modes compared on one energy axis.

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
from work import (                                # noqa: E402
    work_force_displacement, spring_work, shaft_work, electric_work,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — W = int F ds for a linear spring F = kx.  The area under the line
    # from x1 to x2 is the work, and because F grows with x the SECOND
    # centimetre of stretch costs three times the first.  The general
    # quadrature work_force_displacement is checked against spring_work.
    k = 500.0                                       # N/m
    x = np.linspace(0.0, 0.10, 300)
    F = k * x
    x1, x2 = 0.04, 0.08
    W_area = spring_work(k, x1, x2)
    W_quad = work_force_displacement(lambda s: k * s, x1, x2)
    W_first = spring_work(k, 0.0, 0.04)

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(x * 100, F, color=INK, lw=2.2)
    band = (x >= x1) & (x <= x2)
    ax.fill_between(x[band] * 100, 0, F[band], color=FLOW, alpha=0.22, lw=0,
                    label=r"$W=\int_{x_1}^{x_2}F\,ds=%.1f$ J" % W_area)
    first = x <= x1
    ax.fill_between(x[first] * 100, 0, F[first], color=INK, alpha=0.10, lw=0,
                    label=r"first 4 cm costs only %.1f J" % W_first)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 52)
    ax.set_xlabel(r"stretch $x$ (cm)")
    ax.set_ylabel(r"spring force $F=kx$ (N)")
    ax.set_title(r"Work is the area under $F(s)$  ($k=500$ N/m)")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_spring_work_area.svg")
    caps["fig1_spring_work_area.svg"] = (
        r"The defining picture of work: $W=\int F\cdot ds$ is the area under the "
        r"force-displacement curve. For a linear spring $F=kx$ the area is a "
        r"trapezoid, $\tfrac12k(x_2^2-x_1^2)$ (spring_work), and stretching from "
        r"4 to 8 cm takes " + "%.1f" % W_area + r" J while the first 4 cm took "
        r"only " + "%.1f" % W_first + r" J — three times cheaper, because the "
        r"force being worked against is smaller there. The general quadrature "
        r"work_force_displacement reproduces the same "
        + "%.1f" % W_quad + r" J, which is the check that the two agree.")

    # Fig 2 — different work MODES, one energy axis.  A shaft at constant torque
    # and an electrical resistor at constant V*I both deliver energy linearly in
    # time; the slope is the power.  Plotted together so the magnitudes compare.
    t = np.linspace(0.0, 60.0, 200)
    W_shaft = np.array([shaft_work(18.0, 100.0, ti) for ti in t]) / 1000.0   # kJ
    W_elec = np.array([electric_work(120.0, 10.0, ti) for ti in t]) / 1000.0  # kJ

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(t, W_shaft, color=INK, lw=2.2,
            label=r"shaft  $\tau\omega\,\Delta t$  (18 N$\cdot$m, 100 rad/s)")
    ax.plot(t, W_elec, color=FLOW, lw=2.0, ls="--",
            label=r"electrical  $\mathcal{E}I\,\Delta t$  (120 V, 10 A)")
    ax.set_xlim(0, 60)
    ax.set_xlabel(r"time $\Delta t$ (s)")
    ax.set_ylabel(r"energy transferred as work (kJ)")
    ax.set_title(r"Work modes accumulate linearly; the slope is the power")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_work_modes.svg")
    caps["fig2_work_modes.svg"] = (
        r"Thermodynamics counts every mode of work in the same currency. A shaft "
        r"turning at constant torque (shaft_work, $\tau\omega\Delta t$) and a "
        r"resistor drawing constant current (electric_work, "
        r"$\mathcal{E}I\Delta t$) both accumulate energy linearly in time, and "
        r"the slope of each line is that mode's power. Over a minute the "
        r"1.8 kW shaft delivers 108 kJ against the 1.2 kW resistor's 72 kJ. "
        r"Nothing in the energy balance distinguishes their origin — only the "
        r"sign convention does, work OUT of the system being positive.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
