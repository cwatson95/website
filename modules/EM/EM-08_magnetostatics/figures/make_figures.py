"""EM-08 figures -- straight-wire field lines and the current-loop axial field.

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
from magnetostatics import (                       # noqa: E402
    infinite_wire_field, circular_loop_field, loop_axis_field_closed,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- field of an infinite straight wire (current along z): azimuthal B
    # lines circling the wire, with |B| ~ 1/s. Streamlines coloured by log|B|.
    I = 10.0
    B = infinite_wire_field(I, axis="z")
    g = np.linspace(-0.05, 0.05, 26)
    X, Y = np.meshgrid(g, g)
    Bx = np.zeros_like(X); By = np.zeros_like(X); Bmag = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            bx, by, _ = B(X[i, j], Y[i, j], 0.0)
            Bx[i, j], By[i, j] = bx, by
            Bmag[i, j] = np.hypot(bx, by)
    mask = np.hypot(X, Y) < 0.008                  # blank the singular core near the wire
    Bx[mask] = np.nan; By[mask] = np.nan; Bmag[mask] = np.nan

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.streamplot(g * 100, g * 100, Bx, By, color=np.log10(Bmag),
                  cmap="viridis", density=1.1, linewidth=1.0, arrowsize=1.0)
    ax.plot(0, 0, "o", color=FLOW, ms=9, label=r"wire, $I=10$ A ($+z$)")
    ax.set_aspect("equal")
    ax.set_xlabel("$x$ (cm)"); ax.set_ylabel("$y$ (cm)")
    ax.set_title(r"Straight wire: $\mathbf{B}=\frac{\mu_0 I}{2\pi s}\,\hat{\boldsymbol{\phi}}$")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig1_wire_field_lines.svg")
    caps["fig1_wire_field_lines.svg"] = (
        "Magnetic field of an infinite straight wire carrying 10 A out of the page, in a "
        "plane across the wire. The field lines are azimuthal circles (right-hand rule) and "
        "the colour (log scale) shows |B| ~ mu0 I / (2 pi s) growing toward the wire.")

    # Fig 2 -- circular current loop on its axis: Biot-Savart integral from the
    # module vs the closed-form B_z = mu0 I R^2 / 2(R^2+z^2)^(3/2).
    I, R = 5.0, 0.10
    Bloop = circular_loop_field(I, R, n=600)
    z = np.linspace(-0.30, 0.30, 41)
    Bz_bs = np.array([Bloop(0.0, 0.0, zz)[2] for zz in z])
    Bz_cf = np.array([loop_axis_field_closed(I, R, zz) for zz in z])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(z * 100, Bz_cf * 1e6, color=INK, lw=2.4,
            label=r"closed form $\frac{\mu_0 I R^{2}}{2(R^{2}+z^{2})^{3/2}}$")
    ax.plot(z[::2] * 100, Bz_bs[::2] * 1e6, "o", color=FLOW, ms=4.5,
            label="Biot-Savart (module)")
    ax.axvline(-R * 100, color="#cccccc", lw=0.8, ls="--")
    ax.axvline(R * 100, color="#cccccc", lw=0.8, ls="--")
    ax.set_xlabel("axial position  $z$  (cm)")
    ax.set_ylabel(r"$B_z$  ($\mu$T)")
    ax.set_title(r"Current loop on axis ($I=5$ A, $R=10$ cm): Biot-Savart vs closed form")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig2_loop_axial_field.svg")
    caps["fig2_loop_axial_field.svg"] = (
        "On-axis field of a circular current loop (I=5 A, R=10 cm). The module's "
        "Biot-Savart line integral (dots) reproduces the closed form "
        "B_z = mu0 I R^2 / 2(R^2+z^2)^{3/2} (curve); the field peaks at the loop centre.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
