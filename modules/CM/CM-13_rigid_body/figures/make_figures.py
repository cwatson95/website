"""CM-13 figures — moment-of-inertia geometry: the directional moment of inertia
and its principal axes, and the L = I omega misalignment off a principal axis.

Imports the module's own rigid-body code in ../code and renders two SVGs plus a
captions.json (the convention every module shares: matplotlib -> SVG with text as
portable vector outlines, saved next to a captions.json the browser shows under
each figure).  Run:  python3 make_figures.py
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
from rigid_body import (                           # noqa: E402
    inertia_tensor, principal_axes, moment_about_axis, angular_momentum,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _triaxial_body():
    """Six point masses on three orthogonal directions, the in-plane pair tilted
    30 deg in the x-y plane, giving a triaxial inertia tensor whose principal axes
    sit at 30 deg, 120 deg, and the z-axis."""
    phi = math.radians(30.0)
    u = (math.cos(phi), math.sin(phi), 0.0)        # in-plane principal direction 1
    v = (-math.sin(phi), math.cos(phi), 0.0)       # in-plane principal direction 2
    e3 = (0.0, 0.0, 1.0)
    pts, masses = [], []
    for direction, s in ((u, 1.0), (v, 1.6), (e3, 2.2)):
        pts.append(tuple(+s * d for d in direction))
        pts.append(tuple(-s * d for d in direction))
        masses += [1.0, 1.0]
    return inertia_tensor(masses, pts)


def main():
    caps = {}
    I = _triaxial_body()
    moments, axes = principal_axes(I)               # ascending eigenvalues + eigenvectors

    # Fig 1 — directional moment of inertia I_n for the spin axis swept in the x-y plane.
    th = np.linspace(0.0, 2 * np.pi, 721)
    In = np.array([moment_about_axis(I, (math.cos(t), math.sin(t), 0.0)) for t in th])
    fig, ax = plt.subplots(figsize=(6.2, 3.5), subplot_kw={"projection": "polar"})
    ax.plot(th, In, color=INK, lw=2)
    rmax = float(In.max()) * 1.05
    first = True
    for vec in axes:                                # mark the two in-plane principal axes
        if abs(vec[2]) < 0.5:
            ang = math.atan2(vec[1], vec[0])
            lab = "principal axes" if first else None
            ax.plot([ang, ang + math.pi], [rmax, rmax], color=FLOW, lw=1.6, label=lab)
            first = False
    ax.set_rlabel_position(100)
    ax.set_title(r"Directional moment of inertia $I_n=\hat{n}\cdot I\,\hat{n}$"
                 "  (principal axes = extrema)", pad=16)
    ax.legend(loc="lower left", bbox_to_anchor=(-0.05, -0.05), frameon=False)
    _save(fig, "fig1_inertia_rosette.svg")
    caps["fig1_inertia_rosette.svg"] = (
        "Directional moment of inertia I_n = n.I.n (blue) for a triaxial body as the unit "
        "spin axis n sweeps the x-y plane. The orange lines are the in-plane principal axes "
        "returned by principal_axes; they fall exactly on the maximum and minimum of I_n.")

    # Fig 2 — L = I omega aligns with omega only along a principal axis.
    psi = np.linspace(0.0, np.pi, 361)
    mis = []
    for t in psi:
        w = (math.cos(t), math.sin(t), 0.0)
        L = angular_momentum(I, w)
        Ln = math.sqrt(sum(c * c for c in L))
        c = sum(L[i] * w[i] for i in range(3)) / Ln          # |w| = 1
        mis.append(math.degrees(math.acos(max(-1.0, min(1.0, c)))))
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(np.degrees(psi), mis, color=FLOW, lw=2, label=r"$\angle(\vec{L},\vec{\omega})$")
    first = True
    for vec in axes:
        if abs(vec[2]) < 0.5:
            ang = math.degrees(math.atan2(vec[1], vec[0])) % 180.0
            ax.axvline(ang, color=STEEL, lw=1.2, ls="--",
                       label=("principal axis" if first else None))
            first = False
    ax.axhline(0, color="#aaaaaa", lw=0.6)
    ax.set_xlim(0, 180)
    ax.set_xlabel(r"spin-axis angle $\psi$ in the $xy$-plane (deg)")
    ax.set_ylabel(r"angle between $\vec{L}$ and $\vec{\omega}$ (deg)")
    ax.set_title(r"$\vec{L}=I\,\vec{\omega}$ is parallel to $\vec{\omega}$ only on a principal axis")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig2_L_omega_misalignment.svg")
    caps["fig2_L_omega_misalignment.svg"] = (
        "Angle between angular momentum L = I omega and the spin axis omega as omega is "
        "tilted in the x-y plane (orange). It vanishes exactly at the dashed principal-axis "
        "directions; everywhere else L is not parallel to omega, so a freely spun body wobbles.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
