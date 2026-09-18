"""RE-05 figures — Minkowski geometry: invariant hyperbolae of constant interval
with the light cone, and how the unit hyperbola calibrates the boosted time axis.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
"""
import json
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
from minkowski import (                            # noqa: E402
    interval2, classify, four_velocity,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — invariant hyperbolae interval2 = +/- a^2, coloured by classify(),
    # asymptoting to the null light cone ct = +/- x.
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    u = np.linspace(-1.9, 1.9, 400)
    for a in (0.6, 1.1, 1.6):
        # timelike: ct^2 - x^2 = a^2  (interval2 = -a^2), both branches
        ct = np.sqrt(u * u + a * a)
        ax.plot(u, ct, color=INK, lw=1.8)
        ax.plot(u, -ct, color=INK, lw=1.8)
        # spacelike: x^2 - ct^2 = a^2  (interval2 = +a^2), both branches
        x = np.sqrt(u * u + a * a)
        ax.plot(x, u, color=FLOW, lw=1.8)
        ax.plot(-x, u, color=FLOW, lw=1.8)
    # verify the labels with the real interval2/classify on a representative point
    s2_t = interval2([np.sqrt(1.0 + 1.1 ** 2), 1.0, 0.0, 0.0])    # ~ -1.21 timelike
    s2_s = interval2([1.0, np.sqrt(1.0 + 1.1 ** 2), 0.0, 0.0])    # ~ +1.21 spacelike
    cone = np.array([-2.2, 2.2])
    ax.plot(cone, cone, color=STEEL, lw=1.2, ls="--")
    ax.plot(cone, -cone, color=STEEL, lw=1.2, ls="--")
    ax.plot([], [], color=INK, lw=1.8,
            label=r"timelike  $s^{2}<0$  (%s)" % classify([1.5, 0.3, 0, 0]))
    ax.plot([], [], color=FLOW, lw=1.8,
            label=r"spacelike  $s^{2}>0$  (%s)" % classify([0.3, 1.5, 0, 0]))
    ax.plot([], [], color=STEEL, lw=1.2, ls="--", label=r"null  $ct=\pm x$")
    ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.2, 2.2); ax.set_aspect("equal")
    ax.set_xlabel("space $x$"); ax.set_ylabel("time $ct$")
    ax.set_title(r"Invariant hyperbolae  $x^{2}-(ct)^{2}=$ const")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    _save(fig, "fig1_invariant_hyperbolae.svg")
    caps["fig1_invariant_hyperbolae.svg"] = (
        "Curves of constant Minkowski interval, verified with interval2/classify: timelike "
        "hyperbolae s^2 < 0 (blue, opening in time) and spacelike s^2 > 0 (orange, opening "
        "in space), both asymptotic to the null light cone ct = +/- x (dashed). Every "
        "Lorentz boost slides points along these curves, so the interval is frame-invariant. "
        "(checks: s2_t=%.2f, s2_s=%.2f)" % (s2_t, s2_s))

    # Fig 2 — the unit timelike hyperbola interval2 = -1 calibrates the moving time
    # axis: four_velocity(beta) lands ON it, marking '1 tick' of proper time.
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    x = np.linspace(-1.8, 1.8, 400)
    ct = np.sqrt(1.0 + x * x)                       # ct^2 - x^2 = 1 (upper branch)
    ax.plot(x, ct, color=ALT, lw=2, label=r"unit hyperbola  $s^{2}=-1$")
    cone = np.array([0.0, 2.2])
    ax.plot(cone, cone, color=STEEL, lw=1.2, ls="--")
    ax.plot(-cone, cone, color=STEEL, lw=1.2, ls="--", label=r"light cone")
    for beta, col in [(0.0, INK), (0.4, STEEL), (0.7, FLOW), (0.85, INK)]:
        U = four_velocity([beta, 0.0, 0.0])        # = [gamma, gamma*beta, 0, 0]
        ax.plot([0, U[1]], [0, U[0]], color=col, lw=1.4, alpha=0.7)
        ax.scatter([U[1]], [U[0]], color=col, zorder=5, s=40)
        ax.annotate(r"$\beta=%.2f$" % beta, (U[1], U[0]),
                    textcoords="offset points", xytext=(5, -2), fontsize=8, color=col)
    ax.set_xlim(-0.4, 1.9); ax.set_ylim(0.8, 2.1); ax.set_aspect("equal")
    ax.set_xlabel("space $x$"); ax.set_ylabel("time $ct$")
    ax.set_title(r"Unit hyperbola calibrates each boosted time axis")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig2_hyperbola_calibration.svg")
    caps["fig2_hyperbola_calibration.svg"] = (
        "The four-velocity U = gamma(1, beta) of a moving observer (computed by "
        "four_velocity) always lands exactly on the unit timelike hyperbola s^2 = -1, "
        "because U.U = -1. So that hyperbola marks 'one tick' of proper time on every "
        "boosted ct'-axis (rays from the origin) — the geometric calibration of moving "
        "clocks, reaching higher in coordinate time as beta grows.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
