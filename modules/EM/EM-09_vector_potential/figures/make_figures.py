"""EM-09 figures -- a magnetic dipole's vector potential A and its curl B.

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
from vector_potential import (                     # noqa: E402
    magnetic_dipole_moment, dipole_vector_potential, B_from_A,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # a small current loop along z  ==  a magnetic dipole  m = I*area zhat.
    I, R = 3.0, 0.05
    m = magnetic_dipole_moment(I, (0.0, 0.0, math.pi * R ** 2))
    A = dipole_vector_potential(m)
    B = B_from_A(A)                                   # B = curl A  (Eq. 5.59)

    # Fig 1 -- A in the equatorial plane z=0: azimuthal streamlines (m x rhat / r^2)
    # coloured by |A| ~ 1/s^2.
    g = np.linspace(-1.0, 1.0, 26)
    X, Y = np.meshgrid(g, g)
    Ax = np.zeros_like(X); Ay = np.zeros_like(X); Amag = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            ax_, ay_, _ = A(X[i, j], Y[i, j], 0.0)
            Ax[i, j], Ay[i, j] = ax_, ay_
            Amag[i, j] = np.hypot(ax_, ay_)
    core = np.hypot(X, Y) < 0.18
    Ax[core] = np.nan; Ay[core] = np.nan; Amag[core] = np.nan

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.streamplot(g, g, Ax, Ay, color=np.log10(Amag), cmap="viridis",
                  density=1.1, linewidth=1.0, arrowsize=1.0)
    ax.plot(0, 0, "o", color=FLOW, ms=8, label=r"dipole $\mathbf{m}\parallel\hat{z}$")
    ax.set_aspect("equal")
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title(r"Vector potential $\mathbf{A}=\frac{\mu_0}{4\pi}\frac{\mathbf{m}\times\hat{r}}{r^{2}}$  (plane $z=0$)")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig1_dipole_vector_potential.svg")
    caps["fig1_dipole_vector_potential.svg"] = (
        "Vector potential A of a magnetic dipole m along z, in the equatorial plane z=0. "
        "A = (mu0/4pi) m x rhat / r^2 circulates azimuthally around the dipole; colour "
        "(log scale) shows |A| falling as 1/s^2 with distance.")

    # Fig 2 -- the resulting field B = curl A in the meridional plane y=0: the
    # classic dipole field-line pattern, computed by the module's finite-diff curl.
    gx = np.linspace(-1.0, 1.0, 27)
    gz = np.linspace(-0.75, 0.75, 23)
    Xg, Zg = np.meshgrid(gx, gz)
    Bx = np.zeros_like(Xg); Bz = np.zeros_like(Xg); Bmag = np.zeros_like(Xg)
    for i in range(Xg.shape[0]):
        for j in range(Xg.shape[1]):
            bx, _, bz = B(Xg[i, j], 0.0, Zg[i, j])
            Bx[i, j], Bz[i, j] = bx, bz
            Bmag[i, j] = math.hypot(bx, bz)
    core = np.hypot(Xg, Zg) < 0.18
    Bx[core] = np.nan; Bz[core] = np.nan; Bmag[core] = np.nan

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.streamplot(gx, gz, Bx, Bz, color=np.log10(Bmag), cmap="magma",
                  density=1.2, linewidth=1.0, arrowsize=1.0)
    ax.annotate("", xy=(0, 0.28), xytext=(0, -0.28),
                arrowprops=dict(arrowstyle="-|>", color=FLOW, lw=2.4))
    ax.text(0.06, 0.30, r"$\mathbf{m}$", color=FLOW, fontsize=12)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$"); ax.set_ylabel("$z$")
    ax.set_title(r"Resulting field $\mathbf{B}=\nabla\times\mathbf{A}$  (plane $y=0$)")
    _save(fig, "fig2_dipole_B_curl_A.svg")
    caps["fig2_dipole_B_curl_A.svg"] = (
        "The magnetic field B = curl A of the same dipole, in the meridional plane y=0, "
        "obtained from the module's finite-difference curl of the vector potential. It is "
        "the familiar dipole field-line pattern, looping from the north to the south pole.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
