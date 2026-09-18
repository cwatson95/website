"""MA-13 figures — the brachistochrone extremal and the numerical recovery of a geodesic.

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
from variational import (                          # noqa: E402
    cycloid_brachistochrone, minimize_path, functional,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the brachistochrone: the cycloid that minimizes descent time.
    # The extremal x=a(t-sin t), y=a(1-cos t) comes from cycloid_brachistochrone;
    # the descent time T=int sqrt((1+y'^2)/(2 g y)) dx is the module's own
    # `functional` of the brachistochrone Lagrangian, evaluated on the cycloid and
    # on the straight chord to the same endpoint -> the cycloid is faster.
    g = 9.81
    a = 0.6
    thetas = [k * math.pi / 400 for k in range(401)]        # uniform parameter, 0..pi
    xs_c, ys_c = cycloid_brachistochrone(a, thetas)
    xB, yB = xs_c[-1], ys_c[-1]                              # endpoint = cycloid's low point
    xs_l = [xB * i / 600 for i in range(601)]               # straight chord, densely sampled
    ys_l = [(yB / xB) * x for x in xs_l]

    Lb = lambda x, y, p: math.sqrt((1.0 + p * p) / (2.0 * g * y)) if y > 1e-12 else 0.0
    T_cyc = functional(Lb, xs_c, ys_c)
    T_line = functional(Lb, xs_l, ys_l)

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot(xs_l, ys_l, color=STEEL, lw=2, ls="--",
            label=fr"straight chord   $T={T_line:.4f}\,$s")
    ax.plot(xs_c, ys_c, color=FLOW, lw=2.4,
            label=fr"brachistochrone (cycloid)   $T={T_cyc:.4f}\,$s")
    ax.plot([0.0, xB], [0.0, yB], "o", color=INK, ms=6)
    ax.annotate("A", (0.0, 0.0), textcoords="offset points", xytext=(-2, 8),
                color=INK, fontsize=11)
    ax.annotate("B", (xB, yB), textcoords="offset points", xytext=(6, -2),
                color=INK, fontsize=11)
    ax.invert_yaxis()                                       # y is depth: gravity points down
    ax.set_xlabel("horizontal distance $x$")
    ax.set_ylabel("depth $y$  (descent)")
    ax.set_title(r"Brachistochrone: the cycloid beats the chord, $L=\sqrt{(1+y'^2)/(2gy)}$")
    ax.legend(loc="lower left", frameon=False, fontsize=9)
    _save(fig, "fig1_brachistochrone.svg")
    caps["fig1_brachistochrone.svg"] = (
        r"The brachistochrone (fastest-descent) curve from A to B is a cycloid "
        r"$x=a(t-\sin t),\,y=a(1-\cos t)$ (cycloid_brachistochrone, orange), not the "
        r"straight chord (dashed). Descent times, computed with the module's own "
        r"`functional` of $L=\sqrt{(1+y'^2)/2gy}$, show the cycloid is faster despite "
        r"the longer path — it trades length for early steepness.")

    # Fig 2 — recovering the geodesic numerically: minimize_path drives a bent path
    # to the straight line by coordinate-Newton sweeps. Snapshots at increasing
    # sweep counts (sweeps=0 returns the bent start) show J[y] -> sqrt(2).
    arclen = lambda x, y, p: math.sqrt(1.0 + p * p)
    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    for sweeps, col in [(0, ALT), (2, FLOW), (8, STEEL), (400, INK)]:
        xs, ys = minimize_path(arclen, 0.0, 0.0, 1.0, 1.0, N=15, sweeps=sweeps)
        J = functional(arclen, xs, ys)
        lbl = (fr"start (bent), $J={J:.4f}$" if sweeps == 0
               else fr"{sweeps} sweeps, $J={J:.4f}$")
        ax.plot(xs, ys, color=col, lw=2, marker="o", ms=3, label=lbl)
    ax.plot([0.0, 1.0], [0.0, 1.0], color="#999999", lw=1.0, ls=":",
            label=r"exact geodesic $y=x$,  $J=\sqrt{2}=1.4142$")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y(x)$")
    ax.set_title(r"Euler–Lagrange in action: a bent path relaxes to the straight geodesic")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig2_geodesic_recovery.svg")
    caps["fig2_geodesic_recovery.svg"] = (
        r"Recovering the shortest path for $L=\sqrt{1+y'^2}$ with minimize_path: a "
        r"deliberately bent initial guess (0 sweeps) is driven to the straight line "
        r"$y=x$ by coordinate-Newton sweeps that null the Euler–Lagrange residual. The "
        r"length $J[y]$ (the module's `functional`) falls monotonically to "
        r"$\sqrt{2}\approx1.4142$, the geodesic minimum.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
