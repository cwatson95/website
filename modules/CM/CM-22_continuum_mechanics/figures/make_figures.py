"""CM-22 figures — the continuity equation: advected density, and div v as the
local rate of volume change shown by a deforming grid.

Generates SVG figures into this `figures/` directory (plus captions.json) by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path'), saved
next to a captions.json mapping each filename to a short caption.
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
from continuum_mechanics import (                  # noqa: E402
    continuity_residual, material_derivative, divergence_of_velocity,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _draw_grid(ax, fx, fy, color, lw, alpha=1.0, label=None):
    """Draw the image of a unit grid under the node map (x,y)->(fx,fy)."""
    g = np.linspace(-1.0, 1.0, 7)
    lab = label
    for xv in g:                                   # vertical lines x = const
        ys = np.linspace(-1.0, 1.0, 40); xs = np.full_like(ys, xv)
        ax.plot(fx(xs, ys), fy(xs, ys), color=color, lw=lw, alpha=alpha, label=lab)
        lab = None
    for yv in g:                                   # horizontal lines y = const
        xs = np.linspace(-1.0, 1.0, 40); ys = np.full_like(xs, yv)
        ax.plot(fx(xs, ys), fy(xs, ys), color=color, lw=lw, alpha=alpha)


def main():
    caps = {}

    # ---- Fig 1: continuity for an advected density bump ---------------------
    c = 1.2
    rho = lambda x, y, z, t: math.exp(-(x - c * t) ** 2)
    v = lambda x, y, z, t: (c, 0.0, 0.0)

    xx = np.linspace(-6.0, 9.0, 500)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for t, col in [(0.0, INK), (2.5, STEEL), (5.0, ALT)]:
        ax.plot(xx, np.exp(-(xx - c * t) ** 2), color=col, lw=2.0,
                label=fr"$t={t}$")
    # the module says mass is conserved: residual ~ 0 and Drho/Dt ~ 0
    xs_probe = np.linspace(-2.0, 7.0, 25)
    res = max(abs(continuity_residual(rho, v, float(x), 0.0, 0.0, 2.5)) for x in xs_probe)
    Dmax = max(abs(material_derivative(rho, v, float(x), 0.0, 0.0, 2.5)) for x in xs_probe)
    ax.text(0.02, 0.95,
            f"max $|\\partial_t\\rho+\\nabla\\cdot(\\rho v)|$ = {res:.1e}\n"
            f"max $|D\\rho/Dt|$ = {Dmax:.1e}",
            transform=ax.transAxes, va="top", fontsize=8.5, color=INK)
    ax.set_xlabel(r"position $x$"); ax.set_ylabel(r"density $\rho$")
    ax.set_title(r"Mass continuity: a density bump advected at speed $c$")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig1_advected_density.svg")
    caps["fig1_advected_density.svg"] = (
        "A density bump rho = exp(-(x - c t)^2) carried at constant speed c = 1.2, "
        "shown at t = 0, 2.5, 5. The module's continuity_residual and material "
        "derivative are essentially zero across the bump (values quoted), so mass "
        "is conserved locally and each fluid parcel keeps its density: "
        "d rho/dt + div(rho v) = 0.")

    # ---- Fig 2: div v is the rate of volume change (grid deformation) -------
    t = 0.8
    cases = [
        ("shear (incompressible)", 0.7, -0.7, STEEL),     # div v = 0
        ("expansion (compressible)", 0.5, 0.5, FLOW),     # div v = 2a > 0
    ]
    fig, axes = plt.subplots(1, 2, figsize=(6.2, 3.5))
    for ax, (name, a, b, col) in zip(axes, cases):
        vfield = (lambda a_, b_: (lambda x, y, z, tt: (a_ * x, b_ * y, 0.0)))(a, b)
        div = divergence_of_velocity(vfield, 0.31, 0.22, 0.0, 0.0)   # = a + b
        sx, sy = math.exp(a * t), math.exp(b * t)         # exact stretch factors
        _draw_grid(ax, lambda x, y: x, lambda x, y: y, "#c8c8d0", 0.8)
        _draw_grid(ax, lambda x, y: sx * x, lambda x, y: sy * y, col, 1.4)
        ax.set_title(name, fontsize=9)
        ax.text(0.5, -1.95, f"$\\nabla\\cdot v={div:.2f}$\narea x {sx * sy:.2f}",
                ha="center", va="top", fontsize=8.5, color=INK)
        ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.2, 2.2)
        ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle(r"$\nabla\cdot v$ = local fractional rate of volume change", y=1.0)
    _save(fig, "fig2_divergence_deformation.svg")
    caps["fig2_divergence_deformation.svg"] = (
        "A unit grid deformed by the linear flow v = (a x, b y, 0) after a fixed "
        "time. Left: a pure shear with div v = 0 (the module's "
        "divergence_of_velocity) distorts the cells but preserves area. Right: an "
        "isotropic expansion has div v > 0, so every cell grows; the area factor "
        "equals exp(div v * t). The divergence is the local rate of volume change.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
