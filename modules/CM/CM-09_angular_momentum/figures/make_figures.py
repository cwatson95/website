"""CM-09 figures -- angular momentum: conservation under a central force, and the
rotational Newton law dL/dt = N under an applied torque.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
"""
import json
import math
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
from angular_momentum import angular_momentum_of, torque_rate   # noqa: E402

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    m = 1.5
    R = 2.0

    # Two planar trajectories at fixed radius R (so motion is purely angular):
    #   central : uniform circular motion -> L_z constant, no torque.
    #   spin-up : constant angular acceleration -> L_z rises linearly (applied torque).
    w0, alpha = 1.0, 0.6

    def central(t):
        return (R * math.cos(w0 * t), R * math.sin(w0 * t), 0.0)

    def spinup(t):
        phi = w0 * t + 0.5 * alpha * t * t
        return (R * math.cos(phi), R * math.sin(phi), 0.0)

    t = np.linspace(0.0, 5.0, 400)
    Lc = angular_momentum_of(m, central)           # real module function -> L(t)
    Ls = angular_momentum_of(m, spinup)
    Lz_c = np.array([Lc(ti)[2] for ti in t])
    Lz_s = np.array([Ls(ti)[2] for ti in t])

    # Fig 1 -- L_z(t): conserved (central force) vs growing (applied torque).
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(t, Lz_c, color=INK, lw=2, label=r"central force: $L_z$ conserved")
    ax.plot(t, Lz_s, color=FLOW, lw=2, label=r"applied torque: $L_z=L_0+N t$")
    ax.set_xlabel("time $t$"); ax.set_ylabel(r"$L_z = m\,(\mathbf{r}\times\mathbf{v})_z$")
    ax.set_title(r"Angular momentum: $\frac{dL}{dt}=N$  (zero torque $\Rightarrow$ $L$ conserved)")
    ax.legend(loc="upper left", frameon=False)
    _save(fig, "fig1_L_conservation.svg")
    caps["fig1_L_conservation.svg"] = (
        "Out-of-plane angular momentum L_z(t) for a mass at fixed radius, from the module's "
        "angular_momentum_of. Under a central force (uniform rotation) L_z is constant -- angular "
        "momentum is conserved. With a tangential force giving constant angular acceleration, L_z "
        "rises linearly: L grows at the rate set by the torque.")

    # Fig 2 -- verify dL/dt = N for an oscillating-angle trajectory: the module's
    # torque_rate (N = r x m a) must equal the time-derivative of L from
    # angular_momentum_of. Both come from real code; their overlap is the law.
    A, Om = 0.9, 2.0

    def torsional(t):
        phi = A * math.sin(Om * t)                 # angle oscillates -> torque oscillates
        return (R * math.cos(phi), R * math.sin(phi), 0.0)

    t2 = np.linspace(0.2, 4.8, 300)
    Lt = angular_momentum_of(m, torsional)
    Nt = torque_rate(m, torsional)                 # real module function -> N(t) = r x (m a)
    Nz = np.array([Nt(ti)[2] for ti in t2])
    hL = 1e-3                                       # centered d/dt of the real L(t) function
    dLz = np.array([(Lt(ti + hL)[2] - Lt(ti - hL)[2]) / (2.0 * hL) for ti in t2])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(t2, Nz, color=ALT, lw=2.4, label=r"torque $N_z=(\mathbf{r}\times m\mathbf{a})_z$")
    ax.plot(t2, dLz, color=INK, lw=1.4, ls="--", label=r"$dL_z/dt$ (from $L(t)$)")
    ax.axhline(0, color="#aaaaaa", lw=0.7)
    ax.set_xlabel("time $t$"); ax.set_ylabel(r"$N_z$, $dL_z/dt$")
    ax.set_title(r"Rotational Newton law: $N_z=\frac{dL_z}{dt}$ (oscillating drive)")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig2_torque_equals_dLdt.svg")
    caps["fig2_torque_equals_dLdt.svg"] = (
        "For a particle whose angular position oscillates, the torque N_z = (r x m a)_z from the "
        "module's torque_rate (solid) lies exactly on top of the time-derivative dL_z/dt of the "
        "angular momentum from angular_momentum_of (dashed). This is the rotational analogue of "
        "Newton's second law, dL/dt = N.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
