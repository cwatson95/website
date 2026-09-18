"""MA-17 figures — Theorema Egregium (curvature from the metric) and a sphere geodesic.

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
from mpl_toolkits.mplot3d import Axes3D            # noqa: E402,F401  (enables 3-D axes)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from diffgeo import (                              # noqa: E402
    gaussian_curvature_2d, sphere_metric, plane_polar_metric, christoffel,
)

INK, RUST, PLUM, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _geodesic_on_sphere(state0, ds, nsteps, a=1.0):
    """Integrate the geodesic equation  x''^k = -Gamma^k_ij x'^i x'^j  on the round
    2-sphere, with the Christoffel symbols supplied by the module's `christoffel`
    (RK4 in arc length). state = [theta, phi, theta', phi']."""
    g = sphere_metric(a)

    def rhs(s):
        th, ph, vth, vph = s
        Gam = christoffel(g, [th, ph])              # connection from the metric alone
        v = (vth, vph)
        ath = -sum(Gam[0][i][j] * v[i] * v[j] for i in range(2) for j in range(2))
        aph = -sum(Gam[1][i][j] * v[i] * v[j] for i in range(2) for j in range(2))
        return [vth, vph, ath, aph]

    s = list(state0)
    out = [tuple(s)]
    for _ in range(nsteps):
        k1 = rhs(s)
        k2 = rhs([s[i] + 0.5 * ds * k1[i] for i in range(4)])
        k3 = rhs([s[i] + 0.5 * ds * k2[i] for i in range(4)])
        k4 = rhs([s[i] + ds * k3[i] for i in range(4)])
        s = [s[i] + ds / 6.0 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(4)]
        out.append(tuple(s))
    return out


def main():
    caps = {}

    # Fig 1 — Theorema Egregium: Gaussian curvature computed FROM THE METRIC ALONE
    # is constant across the surface and equals 1/a^2 (sphere) or 0 (flat plane).
    thetas = np.linspace(0.35, math.pi - 0.35, 22)
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    for a, col in [(0.5, INK), (1.0, RUST), (2.0, PLUM)]:
        g = sphere_metric(a)
        K = [gaussian_curvature_2d(g, [float(th), 0.3]) for th in thetas]
        ax.plot(thetas, K, "o", ms=4, color=col,
                label=fr"sphere $a={a}$:  $K=1/a^2={1/a**2:.2f}$")
        ax.axhline(1.0 / a**2, color=col, lw=1.0, ls="--")
    gp = plane_polar_metric()
    Kp = [gaussian_curvature_2d(gp, [float(t), 0.0]) for t in thetas]
    ax.plot(thetas, Kp, "s", ms=4, color=STEEL, label=r"flat plane (polar):  $K=0$")
    ax.axhline(0.0, color=STEEL, lw=1.0, ls="--")
    ax.set_xlabel(r"first metric coordinate ($\theta$ sphere, $r$ plane)")
    ax.set_ylabel(r"Gaussian curvature $K=R/2$")
    ax.set_title(r"Theorema Egregium: $K$ from the metric alone is constant")
    ax.legend(loc="center right", frameon=False, fontsize=9)
    ax.set_ylim(-0.45, 4.5)
    _save(fig, "fig1_theorema_egregium.svg")
    caps["fig1_theorema_egregium.svg"] = (
        "Gaussian curvature $K=R/2$ computed by gaussian_curvature_2d from the metric "
        "alone (dots), for round spheres of radius $a=0.5,1,2$ and the flat plane in "
        "polar coordinates. Each is constant across the coordinate and lands on the "
        "exact value $1/a^2$ (dashed); the plane gives $K=0$ even though its metric "
        "$\\mathrm{diag}(1,r^2)$ depends on $r$ — Gauss's remarkable theorem: "
        "curvature is intrinsic, not an artifact of curvy coordinates.")

    # Fig 2 — a geodesic (great circle) on the unit sphere, integrated from the
    # geodesic equation using the module's Christoffel symbols.
    geo = _geodesic_on_sphere([math.pi / 2, 0.0, 0.6, 0.8],
                              ds=2 * math.pi / 400, nsteps=400, a=1.0)
    th = np.array([s[0] for s in geo]); ph = np.array([s[1] for s in geo])
    gx, gy, gz = np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)

    fig = plt.figure(figsize=(5.8, 5.2))
    ax = fig.add_subplot(111, projection="3d")
    u = np.linspace(0, 2 * math.pi, 49); v = np.linspace(0, math.pi, 25)
    sx = np.outer(np.cos(u), np.sin(v))
    sy = np.outer(np.sin(u), np.sin(v))
    sz = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_wireframe(sx, sy, sz, color="#d2d2e0", lw=0.5, rstride=2, cstride=2)
    ax.plot(gx, gy, gz, color=RUST, lw=2.8, label="geodesic (great circle)")
    ax.scatter([gx[0]], [gy[0]], [gz[0]], color=INK, s=45, label="start")
    ax.set_box_aspect([1, 1, 1])
    ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1]); ax.set_zticks([-1, 0, 1])
    ax.view_init(elev=22, azim=35)
    ax.set_title(r"Geodesic on the sphere: $\ddot{x}^k+\Gamma^k_{ij}\dot{x}^i\dot{x}^j=0$")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig2_sphere_geodesic.svg")
    caps["fig2_sphere_geodesic.svg"] = (
        "A geodesic on the unit sphere, integrated from the geodesic equation "
        "$\\ddot{x}^k+\\Gamma^k_{ij}\\dot{x}^i\\dot{x}^j=0$ with Christoffel symbols from "
        "the module's christoffel() (RK4 in arc length, started on the equator). The "
        "straightest possible path closes into a great circle — the sphere's analogue "
        "of a straight line, fixed entirely by the Levi-Civita connection of the metric.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
