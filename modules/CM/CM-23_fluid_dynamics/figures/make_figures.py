"""CM-23 figures — potential flow past a cylinder, and vorticity of rotation vs
a free vortex.

Generates SVG figures into this `figures/` directory (plus captions.json) by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path'), saved
next to a captions.json mapping each filename to a short caption.
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
from fluid_dynamics import (                       # noqa: E402
    vorticity, is_incompressible, is_irrotational,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # ---- Fig 1: ideal (potential) flow past a cylinder ----------------------
    U0, a = 1.0, 1.0
    # velocity field as the module consumes it: V(x,y,z) -> (vx,vy,vz)
    def cyl(x, y, z):
        r2 = x * x + y * y
        u = U0 * (1.0 - a * a * (x * x - y * y) / (r2 * r2))
        w = -U0 * a * a * 2.0 * x * y / (r2 * r2)
        return (u, w, 0.0)

    irrot = is_irrotational(cyl, (2.0, 1.3, 0.0))
    incomp = is_incompressible(cyl, (2.0, 1.3, 0.0))

    xx = np.linspace(-3.0, 3.0, 240)
    yy = np.linspace(-2.0, 2.0, 200)
    X, Y = np.meshgrid(xx, yy)
    R2 = X * X + Y * Y
    Ucomp = U0 * (1.0 - a * a * (X * X - Y * Y) / R2 ** 2)
    Vcomp = -U0 * a * a * 2.0 * X * Y / R2 ** 2
    mask = R2 < a * a
    Ucomp = np.where(mask, np.nan, Ucomp)
    Vcomp = np.where(mask, np.nan, Vcomp)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.streamplot(xx, yy, Ucomp, Vcomp, color=STEEL, density=1.3,
                  linewidth=0.8, arrowsize=0.8)
    ax.add_patch(plt.Circle((0, 0), a, color=INK, zorder=4))
    ax.text(0.02, 0.04,
            f"irrotational: {irrot}    incompressible: {incomp}",
            transform=ax.transAxes, fontsize=8.5, color=INK)
    ax.set_aspect("equal"); ax.set_xlim(-3, 3); ax.set_ylim(-2, 2)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title("Potential flow past a cylinder")
    _save(fig, "fig1_cylinder_flow.svg")
    caps["fig1_cylinder_flow.svg"] = (
        "Ideal flow past a cylinder of radius a: streamlines of the uniform-stream-"
        "plus-doublet velocity field, symmetric fore and aft. At a test point the "
        "module confirms the flow is irrotational (curl v = 0) and incompressible "
        "(div v = 0), so both a velocity potential and a stream function exist.")

    # ---- Fig 2: vorticity of rigid rotation vs a free vortex ----------------
    Omega, kappa = 1.5, 1.0
    rigid = lambda x, y, z: (-Omega * y, Omega * x, 0.0)
    free = lambda x, y, z: (-kappa * y / (x * x + y * y),
                            kappa * x / (x * x + y * y), 0.0)
    wz_rigid = vorticity(rigid)(0.6, 0.4, 0.0)[2]            # = 2 Omega
    wz_free = vorticity(free)(0.6, 0.4, 0.0)[2]             # ~ 0

    xx = np.linspace(-2.0, 2.0, 200)
    yy = np.linspace(-2.0, 2.0, 200)
    X, Y = np.meshgrid(xx, yy)
    panels = [
        ("rigid rotation", -Omega * Y, Omega * X, f"$\\omega_z={wz_rigid:.1f}=2\\Omega$"),
        ("free vortex", -kappa * Y / (X * X + Y * Y),
         kappa * X / (X * X + Y * Y), f"$\\omega_z\\approx{wz_free:.1f}$"),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(6.2, 3.5))
    for ax, (name, U, V, lab) in zip(axes, panels):
        spd = np.hypot(U, V)
        if name == "free vortex":
            small = (X * X + Y * Y) < 0.09
            U = np.where(small, np.nan, U); V = np.where(small, np.nan, V)
        ax.streamplot(xx, yy, U, V, color=spd, cmap="viridis",
                      density=0.9, linewidth=0.8, arrowsize=0.8)
        ax.set_title(name, fontsize=9)
        ax.text(0.5, -0.02, lab, transform=ax.transAxes, ha="center",
                va="top", fontsize=9, color=INK)
        ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("Same circular streamlines, opposite vorticity", y=1.0)
    _save(fig, "fig2_vorticity.svg")
    caps["fig2_vorticity.svg"] = (
        "Two flows with identical circular streamlines but opposite vorticity, "
        "from the module's vorticity = curl v. Rigid rotation has uniform "
        "omega_z = 2 Omega (every parcel spins); the free vortex v ~ 1/r is "
        "irrotational (omega_z = 0) everywhere except its singular core. Colour "
        "encodes speed: it rises with radius for rotation, falls as 1/r for the "
        "vortex.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
