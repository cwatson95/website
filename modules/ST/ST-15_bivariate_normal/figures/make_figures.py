"""ST-15 figures — the bivariate normal: how the correlation rho tilts and
elongates the contour ellipses, and how those Mahalanobis ellipses coincide with
the level sets of the density.

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
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from bivariate_normal import (                     # noqa: E402
    bivariate_normal_pdf, ellipse_points, ellipse_axes, covariance_matrix,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"
CMAP = LinearSegmentedColormap.from_list("ink", ["#ffffff", INK])


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the c=1 contour ellipse at several rho (equal sigmas, so rho is pure
    # tilt/elongation): rho=0 is a circle, |rho|->1 stretches along a diagonal.
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    cols = [STEEL, INK, ALT, FLOW]
    for rho, col in zip((-0.7, 0.0, 0.5, 0.9), cols):
        x, y = ellipse_points(0.0, 0.0, 1.0, 1.0, rho, c=1.0, n=200)
        ax.plot(x, y, color=col, lw=2, label=fr"$\rho={rho:+.1f}$")
    ax.scatter([0.0], [0.0], color="#666666", s=14, zorder=3)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title(r"Bivariate-normal contour ellipse vs $\rho$ "
                 r"($\sigma_X=\sigma_Y=1$)")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig1_ellipse_vs_rho.svg")
    caps["fig1_ellipse_vs_rho.svg"] = (
        "The constant-Mahalanobis (c=1) contour ellipse of the bivariate normal at four "
        "correlations, with equal standard deviations. At rho=0 it is a circle; as |rho| "
        "grows the ellipse elongates and tilts toward the y=x diagonal (rho>0) or y=-x "
        "(rho<0).")

    # Fig 2 — the density itself for one rho, with the c=1,2,3 Mahalanobis ellipses
    # and the principal axes overlaid: the ellipses ARE the density level sets.
    mux, muy, sx, sy, rho = 0.0, 0.0, 1.0, 1.6, 0.6
    gx = np.linspace(-4.5, 4.5, 160)
    gy = np.linspace(-5.5, 5.5, 160)
    X, Y = np.meshgrid(gx, gy, indexing="ij")
    pdf = np.vectorize(lambda x, y: bivariate_normal_pdf(x, y, mux, muy, sx, sy, rho))
    Z = pdf(X, Y)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.contourf(X, Y, Z, levels=12, cmap=CMAP)
    for c in (1.0, 2.0, 3.0):
        ex, ey = ellipse_points(mux, muy, sx, sy, rho, c=c, n=200)
        ax.plot(ex, ey, color=FLOW, lw=1.6,
                label="Mahalanobis $c=1,2,3$" if c == 1.0 else None)
    # principal axes from the eigen-decomposition of Sigma (semi-axes at c=2)
    a, b, theta = ellipse_axes(covariance_matrix(sx, sy, rho), c=2.0)
    ct, st = math.cos(theta), math.sin(theta)
    ax.plot([mux - a * ct, mux + a * ct], [muy - a * st, muy + a * st],
            color=ALT, lw=1.8, ls="--", label="principal axes")
    ax.plot([mux + b * st, mux - b * st], [muy - b * ct, muy + b * ct],
            color=ALT, lw=1.8, ls="--")
    ax.set_aspect("equal")
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title(fr"Density level sets are the contour ellipses ($\rho={rho}$)")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig2_density_ellipses.svg")
    caps["fig2_density_ellipses.svg"] = (
        "Filled contours of the bivariate-normal density (sigma_X=1, sigma_Y=1.6, "
        "rho=0.6) with the Mahalanobis ellipses at c=1,2,3 drawn on top: the ellipses "
        "trace constant-density level sets. Dashed lines are the principal axes from the "
        "eigen-decomposition of the covariance matrix.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
