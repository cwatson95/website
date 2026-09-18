"""RE-09 figures — tensor calculus on manifolds: the connection that twists the
coordinate basis, and parallel transport / holonomy on the 2-sphere.

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
from covariant_derivative import (                 # noqa: E402
    christoffel, parallel_transport, metric_compatibility,
)
import diffgeo                                      # noqa: E402  (MA-17, put on path by the module)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    sphere = diffgeo.sphere_metric(1.0)            # g = diag(1, sin^2 theta)

    # Fig 1 — the Christoffel symbols on the unit 2-sphere vs colatitude theta.
    thetas = np.linspace(0.25, math.pi - 0.25, 200)
    g_tpp, g_ptp = [], []                           # Gamma^theta_phiphi, Gamma^phi_thetaphi
    for th in thetas:
        Gam = christoffel(sphere, [float(th), 0.3])
        g_tpp.append(Gam[0][1][1])
        g_ptp.append(Gam[1][0][1])
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(np.degrees(thetas), g_tpp, color=INK, lw=2,
            label=r"$\Gamma^{\theta}_{\ \phi\phi}=-\sin\theta\cos\theta$")
    ax.plot(np.degrees(thetas), g_ptp, color=FLOW, lw=2,
            label=r"$\Gamma^{\phi}_{\ \theta\phi}=\cot\theta$")
    ax.plot(np.degrees(thetas), [-math.sin(t) * math.cos(t) for t in thetas],
            color="#999999", lw=1.0, ls="--", zorder=0)
    ax.plot(np.degrees(thetas), [math.cos(t) / math.sin(t) for t in thetas],
            color="#999999", lw=1.0, ls="--", zorder=0, label="exact")
    ax.axhline(0, color="#bbbbbb", lw=0.6)
    ax.set_ylim(-3.0, 3.0)
    ax.set_xlabel(r"colatitude  $\theta$  (deg)")
    ax.set_ylabel("connection coefficient")
    ax.set_title(r"Levi-Civita connection on the 2-sphere: the basis twists with $\theta$")
    ax.legend(loc="upper center", frameon=False, ncol=1, fontsize=9)
    _save(fig, "fig1_christoffel_sphere.svg")
    caps["fig1_christoffel_sphere.svg"] = (
        "Christoffel symbols of the unit 2-sphere computed by the module's `christoffel`, "
        "versus colatitude theta. The nonzero coefficients Gamma^theta_{phi phi} = "
        "-sin theta cos theta and Gamma^phi_{theta phi} = cot theta (dashed: exact) measure "
        "how the coordinate basis vectors rotate and stretch from point to point on the curved surface.")

    # Fig 2 — parallel transport round a closed loop: holonomy (the vector rotates).
    th0, dth, dphi = 1.0, 0.55, 0.7
    corners = [[th0, 0.0], [th0, dphi], [th0 + dth, dphi], [th0 + dth, 0.0], [th0, 0.0]]
    loop = []                                       # densify the loop for smooth transport
    for a, b in zip(corners[:-1], corners[1:]):
        for s in np.linspace(0.0, 1.0, 16, endpoint=False):
            loop.append([a[0] + (b[0] - a[0]) * s, a[1] + (b[1] - a[1]) * s])
    loop.append(corners[-1])
    V0 = [1.0, 0.0]                                 # initial tangent vector (along e_theta)
    # transported vector at each waypoint = transport along the path prefix
    vecs = [parallel_transport(sphere, V0, loop[:k + 1], steps=1) for k in range(len(loop))]
    ph = np.array([p[1] for p in loop])
    th = np.array([p[0] for p in loop])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(ph, th, color=INK, lw=1.6, zorder=1)
    sc = 0.16
    idx = list(range(0, len(loop), 6))
    for k in idx:
        st = math.sin(loop[k][0])                   # orthonormal comps: (V^th, V^ph * sin th)
        ax.arrow(ph[k], th[k], sc * vecs[k][0], sc * vecs[k][1] * st,
                 head_width=0.025, head_length=0.03, color=ALT, lw=1.2,
                 length_includes_head=True, zorder=2)
    # start (blue) and end (orange) vectors at the same corner show the holonomy gap
    ax.arrow(ph[0], th[0], sc * vecs[0][0], sc * vecs[0][1] * math.sin(loop[0][0]),
             head_width=0.03, head_length=0.035, color=INK, lw=2.2,
             length_includes_head=True, zorder=4)
    ax.arrow(ph[-1], th[-1], sc * vecs[-1][0], sc * vecs[-1][1] * math.sin(loop[-1][0]),
             head_width=0.03, head_length=0.035, color=FLOW, lw=2.2,
             length_includes_head=True, zorder=4)
    area = (math.cos(th0) - math.cos(th0 + dth)) * dphi
    ax.text(0.04, th0 - 0.16, f"enclosed area = {area:.3f}\n(= holonomy angle)",
            color=INK, fontsize=9)
    ax.set_xlabel(r"longitude  $\phi$"); ax.set_ylabel(r"colatitude  $\theta$")
    ax.set_title("Parallel transport round a loop: the vector returns rotated (holonomy)")
    start = plt.Line2D([], [], color=INK, lw=2.2, label="start vector")
    end = plt.Line2D([], [], color=FLOW, lw=2.2, label="after the loop")
    ax.legend(handles=[start, end], loc="upper right", frameon=False, fontsize=9)
    ax.invert_yaxis()
    _save(fig, "fig2_parallel_transport_holonomy.svg")
    comp = metric_compatibility(sphere, [th0, 0.0])
    caps["fig2_parallel_transport_holonomy.svg"] = (
        "A tangent vector parallel-transported by the module's `parallel_transport` around a "
        "closed latitude-longitude loop on the unit sphere. It comes back rotated (blue start "
        "vs orange finish): the holonomy angle equals the enclosed area (int K dA, K=1). "
        f"Transport stays metric-compatible, max|nabla g| = {comp:.1e}, so the vector's length is preserved.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
