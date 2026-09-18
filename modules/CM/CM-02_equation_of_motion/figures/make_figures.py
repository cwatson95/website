"""CM-02 figures — solutions of Newton's equation of motion for a damped oscillator.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
"""
import json
import math
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
from equation_of_motion import (                   # noqa: E402
    trajectory, spring_force, linear_drag, sum_forces,
)

INK, FLOW, ALT, FOUR = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    m, k = 1.0, 16.0                       # natural frequency omega_0 = 4
    r0, v0 = (1.0, 0.0, 0.0), (0.0, 0.0, 0.0)
    t0, t1, n = 0.0, 6.0, 3000
    bc = 2.0 * math.sqrt(k * m)            # critical-damping coefficient

    # Fig 1 — x(t) integrated by the module for four damping regimes.
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for b, lab, col in [(0.0, "undamped", FOUR),
                        (0.4 * bc, "underdamped", INK),
                        (bc, "critical", FLOW),
                        (2.0 * bc, "overdamped", ALT)]:
        force = sum_forces(spring_force(k), linear_drag(b))
        ts, rs, vs = trajectory(force, m, r0, v0, t0, t1, n)
        ax.plot(ts, [p[0] for p in rs], color=col, lw=2, label=lab)
    ax.axhline(0, color="#aaaaaa", lw=0.6)
    ax.set_xlabel("time $t$ (s)"); ax.set_ylabel("displacement $x$ (m)")
    ax.set_title(r"Newton EOM $m\ddot{x}+b\dot{x}+kx=0$  ($\omega_0=4$)")
    ax.legend(loc="upper right", frameon=False, ncol=2)
    _save(fig, "fig1_damping_regimes.svg")
    caps["fig1_damping_regimes.svg"] = (
        "Displacement x(t) obtained by integrating the module's Newton RHS (spring + "
        "linear drag) from x=1 at rest, for four damping levels. The undamped case "
        "oscillates forever; adding drag gives decaying oscillation (underdamped), the "
        "fastest non-oscillating return (critical), and a slow crawl (overdamped).")

    # Fig 2 — phase portrait x vs v for the same EOM: drag spirals into the attractor.
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for b, col, lab in [(0.0, FOUR, "b=0 (closed orbit)"),
                        (0.6, INK, "b=0.6 (spiral in)"),
                        (1.6, ALT, "b=1.6 (fast decay)")]:
        force = sum_forces(spring_force(k), linear_drag(b))
        ts, rs, vs = trajectory(force, m, r0, v0, t0, t1, n)
        ax.plot([p[0] for p in rs], [u[0] for u in vs], color=col, lw=1.6, label=lab)
    ax.plot(0, 0, "o", color="#333333", ms=5)
    ax.axhline(0, color="#cccccc", lw=0.6); ax.axvline(0, color="#cccccc", lw=0.6)
    ax.set_xlabel("displacement $x$ (m)"); ax.set_ylabel(r"velocity $\dot{x}$ (m/s)")
    ax.set_title("Phase portrait: damping spirals the orbit to rest")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig2_phase_portrait.svg")
    caps["fig2_phase_portrait.svg"] = (
        "Phase-space (x, x-dot) tracks of the same equation of motion. Without drag the "
        "orbit is a closed ellipse (energy conserved); with drag it spirals inward to the "
        "stable fixed point at the origin, faster for larger damping b.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
