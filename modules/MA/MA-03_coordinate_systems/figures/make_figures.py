"""MA-03 figures -- the plane polar grid and its area element, and the spherical
moving frame.

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
from coordinates import (                           # noqa: E402
    cyl_to_cart, cyl_jacobian, sph_to_cart, sph_basis,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _cell_polygon(rho0, rho1, phi0, phi1, n=24):
    """Boundary of a polar grid cell (xy), built from cyl_to_cart."""
    ph = np.linspace(phi0, phi1, n)
    outer = [cyl_to_cart(rho1, p, 0.0)[:2] for p in ph]
    inner = [cyl_to_cart(rho0, p, 0.0)[:2] for p in ph[::-1]]
    return np.array(outer + inner)


def main():
    caps = {}

    # Fig 1 -- polar / cylindrical grid + the area element dA = rho drho dphi.
    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    rhos = np.arange(0.5, 3.01, 0.5)
    phis = np.arange(0.0, 2 * math.pi, math.pi / 6)
    th = np.linspace(0, 2 * math.pi, 240)
    for rho in rhos:                                   # circles rho = const
        xy = np.array([cyl_to_cart(rho, p, 0.0)[:2] for p in th])
        ax.plot(xy[:, 0], xy[:, 1], color=STEEL, lw=0.8, alpha=0.7)
    for phi in phis:                                   # rays phi = const
        x0, y0, _ = cyl_to_cart(0.0, phi, 0.0)
        x1, y1, _ = cyl_to_cart(3.0, phi, 0.0)
        ax.plot([x0, x1], [y0, y1], color=STEEL, lw=0.8, alpha=0.7)

    dphi = math.pi / 6
    # one small-rho cell (blue) and one large-rho cell (orange); equal drho, dphi
    areas = {}
    for (rho0, col, lab) in ((0.5, INK, "inner"), (2.5, FLOW, "outer")):
        poly = _cell_polygon(rho0, rho0 + 0.5, math.pi / 6, math.pi / 6 + dphi)
        ax.fill(poly[:, 0], poly[:, 1], color=col, alpha=0.55, zorder=3)
        rho_mid = rho0 + 0.25
        dA = cyl_jacobian(rho_mid) * 0.5 * dphi        # rho * drho * dphi
        areas[lab] = dA
        cx, cy, _ = cyl_to_cart(rho_mid, math.pi / 6 + dphi / 2, 0.0)
        ax.annotate(f"{lab}\n$dA\\approx${dA:.2f}", (cx, cy),
                    xytext=(cx + 0.15, cy + 0.35), fontsize=9, color=col,
                    arrowprops=dict(arrowstyle="->", color=col, lw=1.1))
    ratio = areas["outer"] / areas["inner"]            # ~ rho_outer / rho_inner

    ax.set_aspect("equal")
    ax.set_xlim(-3.3, 3.3); ax.set_ylim(-3.3, 3.3)
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title(r"Polar grid: area element $dA=\rho\,d\rho\,d\phi$ grows with $\rho$")
    _save(fig, "fig1_polar_grid_area.svg")
    caps["fig1_polar_grid_area.svg"] = (
        r"The plane polar / cylindrical grid from `cyl_to_cart`: circles "
        r"$\rho=$const and rays $\phi=$const. The area element is "
        r"$dA=\rho\,d\rho\,d\phi$ (the Jacobian `cyl_jacobian`$=\rho$), so for equal "
        r"$\Delta\rho,\Delta\phi$ the outer cell (orange, $\rho\approx2.75$) has "
        r"about " + f"{ratio:.1f}" + r" times the area of the inner one "
        r"(blue, $\rho\approx0.75$) -- the area grows in proportion to $\rho$.")

    # Fig 2 -- spherical moving frame (e_r, e_theta, e_phi) tangent to the curves.
    theta0, phi0 = math.radians(55), math.radians(40)
    P = sph_to_cart(1.0, theta0, phi0)
    e_r, e_th, e_ph = sph_basis(theta0, phi0)

    fig = plt.figure(figsize=(6.2, 4.0))
    ax = fig.add_subplot(111, projection="3d")

    # light sphere wireframe, generated through sph_to_cart
    tt = np.linspace(0, math.pi, 13)
    pp = np.linspace(0, 2 * math.pi, 25)
    for t in tt:                                        # parallels
        pts = np.array([sph_to_cart(1.0, t, p) for p in pp])
        ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color="0.8", lw=0.5)
    for p in pp[::2]:                                   # meridians
        pts = np.array([sph_to_cart(1.0, t, p) for t in np.linspace(0, math.pi, 25)])
        ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color="0.85", lw=0.5)

    # coordinate curves through P: meridian (phi fixed) and parallel (theta fixed)
    mer = np.array([sph_to_cart(1.0, t, phi0) for t in np.linspace(0, math.pi, 60)])
    par = np.array([sph_to_cart(1.0, theta0, p) for p in np.linspace(0, 2 * math.pi, 80)])
    ax.plot(mer[:, 0], mer[:, 1], mer[:, 2], color=FLOW, lw=1.6,
            label=r"meridian ($\phi$ fixed)")
    ax.plot(par[:, 0], par[:, 1], par[:, 2], color=ALT, lw=1.6,
            label=r"parallel ($\theta$ fixed)")
    ax.plot([0, P[0]], [0, P[1]], [0, P[2]], color="0.5", lw=1.0, ls=":")

    L = 0.55
    for vec, col, lab in ((e_r, INK, r"$\hat e_r$"),
                          (e_th, FLOW, r"$\hat e_\theta$"),
                          (e_ph, ALT, r"$\hat e_\phi$")):
        ax.quiver(P[0], P[1], P[2], L * vec[0], L * vec[1], L * vec[2],
                  color=col, lw=2.3, arrow_length_ratio=0.22)
        tip = [P[i] + L * 1.25 * vec[i] for i in range(3)]
        ax.text(tip[0], tip[1], tip[2], lab, color=col, fontsize=13)

    ax.set_box_aspect((1, 1, 1))
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
    ax.view_init(elev=22, azim=35)
    ax.set_title(r"Spherical moving frame $(\hat e_r,\hat e_\theta,\hat e_\phi)$"
                 + "\n" + r"at $\theta=55^\circ,\ \phi=40^\circ$")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig2_spherical_frame.svg")
    caps["fig2_spherical_frame.svg"] = (
        r"The spherical moving frame from `sph_basis`. At a point $P(r,\theta,\phi)$ "
        r"the orthonormal right-handed triad $(\hat e_r,\hat e_\theta,\hat e_\phi)$ "
        r"is tangent to the coordinate curves: $\hat e_r$ along the radius, "
        r"$\hat e_\theta$ along the meridian ($\phi$ fixed, orange), $\hat e_\phi$ "
        r"along the parallel ($\theta$ fixed, purple). Unlike fixed Cartesian axes, "
        r"the basis depends on position.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
