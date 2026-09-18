"""MA-02 figures -- divergence vs curl of a planar field, and Stokes' theorem
checked numerically.

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
from vector_calculus import (                       # noqa: E402
    divergence, curl, line_integral,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    F = lambda x, y, z: (-y, x, 0.0)     # rigid rotation: curl = 2 z_hat, div = 0
    G = lambda x, y, z: (x, y, 0.0)      # radial source:  div = 2,        curl = 0

    # values from the module's own finite-difference operators
    curlF_z = curl(F)(0.3, -0.2, 0.0)[2]
    divF = divergence(F)(0.3, -0.2, 0.0)
    divG = divergence(G)(0.3, -0.2, 0.0)
    curlG_z = curl(G)(0.3, -0.2, 0.0)[2]

    # Fig 1 -- side-by-side: curl without divergence, vs divergence without curl.
    g = np.linspace(-2.0, 2.0, 11)
    X, Y = np.meshgrid(g, g)
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.4))
    for ax, fld, name, comps, txt in (
        (axes[0], F, r"$F=(-y,\,x,\,0)$",
         (-Y, X), f"curl$_z$ = {curlF_z:.2f}\ndiv = {divF:.2f}"),
        (axes[1], G, r"$G=(x,\,y,\,0)$",
         (X, Y), f"div = {divG:.2f}\ncurl$_z$ = {curlG_z:.2f}"),
    ):
        U, Vv = comps
        mag = np.hypot(U, Vv)
        ax.quiver(X, Y, U, Vv, mag, cmap="viridis", scale=28, width=0.007,
                  pivot="mid")
        th = np.linspace(0, 2 * math.pi, 200)
        ax.plot(np.cos(th), np.sin(th), color=ALT, lw=1.4, ls="--")
        ax.set_aspect("equal"); ax.set_xlim(-2.3, 2.3); ax.set_ylim(-2.3, 2.3)
        ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_title(name)
        ax.text(0.03, 0.97, txt, transform=ax.transAxes, va="top", ha="left",
                fontsize=9.5, bbox=dict(boxstyle="round", fc="white", ec="0.7",
                                        alpha=0.85))
    fig.suptitle("Divergence without curl, and curl without divergence", y=1.02)
    _save(fig, "fig1_div_curl_fields.svg")
    caps["fig1_div_curl_fields.svg"] = (
        r"A planar rotation field $F=(-y,x,0)$ (left) has curl $\nabla\times F="
        + f"{curlF_z:.0f}" + r"\,\hat z$ but zero divergence; a radial source "
        r"$G=(x,y,0)$ (right) has $\nabla\cdot G=" + f"{divG:.0f}" + r"$ but zero "
        r"curl. Both diagnostics are computed by the module's `curl` and "
        r"`divergence` (central differences); the dashed circle is the unit loop "
        r"used for the Stokes check.")

    # Fig 2 -- Stokes' theorem numerically: circulation = (curl_z) * area.
    radii = np.linspace(0.25, 2.0, 12)
    circ = []
    for R in radii:
        path = lambda t, R=R: (R * math.cos(t), R * math.sin(t), 0.0)
        circ.append(line_integral(F, path, 0.0, 2 * math.pi))
    pred = curlF_z * math.pi * radii ** 2     # (curl F)_z * pi R^2

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(radii, pred, color=INK, lw=2,
            label=r"$(\nabla\times F)_z\,\pi R^2 = 2\pi R^2$")
    ax.plot(radii, circ, "o", color=FLOW, ms=6, mfc="white", mew=1.6,
            label=r"circulation $\oint_C F\cdot dl$  (`line_integral`)")
    ax.set_xlabel("loop radius $R$")
    ax.set_ylabel("circulation")
    ax.set_title(r"Stokes' theorem: circulation $=(\nabla\times F)_z\times$ area")
    ax.legend(loc="upper left", frameon=False)
    _save(fig, "fig2_stokes_check.svg")
    caps["fig2_stokes_check.svg"] = (
        r"Stokes' theorem, checked numerically. The circulation "
        r"$\oint_C F\cdot d\mathbf l$ of $F=(-y,x,0)$ around a circle of radius $R$ "
        r"(markers, from `line_integral`) matches the curl flux "
        r"$(\nabla\times F)_z\,\pi R^2=2\pi R^2$ (line, with $(\nabla\times F)_z$ "
        r"from `curl`) across every radius -- the integral theorem made "
        r"quantitative.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
