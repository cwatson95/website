"""EM-15 figures -- transverse E/B/k structure and polarization states.

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
from em_waves import (                             # noqa: E402
    transverse_B, scalar_plane_wave, is_transverse, classify_polarization,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- E, B, k are mutually orthogonal (natural units v=1 so |B|=|E|).
    E0 = (1.0, 0.0, 0.0)                            # E along x
    khat = (0.0, 0.0, 1.0)                          # propagation +z
    B0 = transverse_B(E0, khat, v=1.0)             # = (0, 1, 0), |B|=|E|/v
    f = scalar_plane_wave(1.0, 1.0)                # cos(kz - wt), k=w=1
    zs = np.linspace(0.0, 2.0 * np.pi, 13)

    fig = plt.figure(figsize=(6.2, 3.7))
    ax = fig.add_subplot(projection="3d")
    for i, zz in enumerate(zs):
        a = f(0.0, 0.0, zz, 0.0)                    # cos(kz) modulation
        lblE = r"$\mathbf{E}\parallel\hat{x}$" if i == 0 else None
        lblB = r"$\mathbf{B}\parallel\hat{y}$" if i == 0 else None
        ax.quiver(zz, 0, 0, 0, 0, E0[0] * a, color=INK, lw=1.6, label=lblE)
        ax.quiver(zz, 0, 0, 0, B0[1] * a, 0, color=FLOW, lw=1.6, label=lblB)
    ax.quiver(0, 0, 0, 2.0 * np.pi, 0, 0, color=ALT, lw=2.2, arrow_length_ratio=0.06,
              label=r"$\mathbf{k}\parallel\hat{z}$")
    ax.plot(zs, 0 * zs, 0 * zs, color="#bbbbbb", lw=0.8)
    ax.set_xlabel(r"$z$ (along $k$)"); ax.set_ylabel(r"$y$ (B)"); ax.set_zlabel(r"$x$ (E)")
    ax.set_title(r"Transverse wave: $\mathbf{E}\perp\mathbf{B}\perp\mathbf{k}$")
    ax.view_init(elev=18, azim=-66)
    ax.legend(loc="upper left", frameon=False)
    _save(fig, "fig1_transverse_ebk.svg")
    ok = is_transverse(E0, khat) and is_transverse(B0, khat)
    caps["fig1_transverse_ebk.svg"] = (
        "A +z plane wave with E along x; transverse_B returns B along y with |B|=|E|/v. "
        "E (blue) and B (orange) oscillate in step, each perpendicular to the other "
        "and to the propagation direction k (purple). is_transverse confirms "
        "E.k = B.k = 0: %s." % ("orthogonal" if ok else "check"))

    # Fig 2 -- polarization: the E-vector tip traces a line, circle, or ellipse.
    t = np.linspace(0.0, 2.0 * np.pi, 400)
    cases = [
        (1.0, 1.0, 0.0,            INK),
        (1.0, 1.0, math.pi / 2.0,  FLOW),
        (2.0, 1.0, math.pi / 2.0,  STEEL),
    ]
    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    for Ax, Ay, delta, col in cases:
        Ex = Ax * np.cos(t)
        Ey = Ay * np.cos(t + delta)
        kind = classify_polarization(Ax, Ay, delta)
        ax.plot(Ex, Ey, color=col, lw=2.0,
                label=r"$A_x{=}%g,\ A_y{=}%g,\ \delta{=}%.2f$: %s"
                      % (Ax, Ay, delta, kind))
    ax.axhline(0, color="#cccccc", lw=0.6); ax.axvline(0, color="#cccccc", lw=0.6)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(r"$E_x$"); ax.set_ylabel(r"$E_y$")
    ax.set_title("Polarization: trace of the E-vector over one period")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), frameon=False, fontsize=9)
    _save(fig, "fig2_polarization.svg")
    caps["fig2_polarization.svg"] = (
        "The path swept by the E-vector tip over one period, labelled by "
        "classify_polarization. Equal amplitudes in phase (delta=0) give a line "
        "(linear); equal amplitudes a quarter-period apart (delta=pi/2) give a circle "
        "(circular); unequal amplitudes give an ellipse (elliptical).")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
