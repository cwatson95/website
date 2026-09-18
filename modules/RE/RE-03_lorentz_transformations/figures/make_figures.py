"""RE-03 figures — the Lorentz boost: the (x', ct') axes scissoring toward the
light line, and the full S' coordinate grid with a transformed event.

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
from lorentz import (                              # noqa: E402
    boost, inverse, apply, rapidity,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _axis_dir(beta, basis):
    """S' basis vector (basis=[1,0,0,0] for ct', [0,1,0,0] for x') expressed in S
    via the real boost: columns of inverse(boost) carry S' bases back to S."""
    v = apply(inverse(boost(beta)), basis)         # -> [ct, x, y, z] in S
    return v[1], v[0]                              # return (x, ct) for plotting


def main():
    caps = {}

    # Fig 1 — the boosted axes scissor symmetrically toward the light line ct=x as
    # beta grows; both ct'- and x'-axes are images of the S axes under the boost.
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    lim = 2.4
    ax.plot([-lim, lim], [-lim, lim], color="#bbbbbb", lw=1.2, ls="--",
            label="light line $ct=x$")
    ax.axhline(0, color=INK, lw=1.5)              # S x-axis
    ax.axvline(0, color=INK, lw=1.5)              # S ct-axis
    for beta, col in [(0.4, STEEL), (0.7, FLOW)]:
        cx, ct = _axis_dir(beta, [1.0, 0.0, 0.0, 0.0])    # ct'-axis direction (x,ct)
        sx, st = _axis_dir(beta, [0.0, 1.0, 0.0, 0.0])    # x'-axis direction (x,ct)
        s = lim / ct                              # scale so the axis spans the box
        ax.plot([-s * cx, s * cx], [-s * ct, s * ct], color=col, lw=2,
                label=r"$\beta=%.1f$  ($\phi=%.2f$)" % (beta, rapidity(beta)))
        ax.plot([-s * sx, s * sx], [-s * st, s * st], color=col, lw=2)
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xlabel("space $x$"); ax.set_ylabel("time $ct$")
    ax.set_title(r"Boosted $(x',ct')$ axes scissor toward the light line")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    _save(fig, "fig1_scissoring_axes.svg")
    caps["fig1_scissoring_axes.svg"] = (
        "The Lorentz boost carries the orthogonal S axes (dark) into the S' axes for "
        "beta=0.4 and beta=0.7, computed as inverse(boost) applied to the basis vectors. "
        "The ct'-axis (slope 1/beta) and x'-axis (slope beta) close like scissors toward "
        "the 45-degree light line as beta grows, each tilted by the rapidity phi.")

    # Fig 2 — the S' coordinate grid drawn in S (a skewed mesh), with one event
    # carried between frames by the real boost.
    beta = 0.5
    L = inverse(boost(beta))                       # S' bases -> S coordinates
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    grid = np.arange(-2, 2.01, 1.0)
    span = np.linspace(-2.5, 2.5, 2)
    for k in grid:                                 # lines of constant ct' (vary x')
        pts = [apply(L, [k, xp, 0, 0]) for xp in span]
        ax.plot([p[1] for p in pts], [p[0] for p in pts], color=STEEL, lw=0.9)
    for k in grid:                                 # lines of constant x' (vary ct')
        pts = [apply(L, [tp, k, 0, 0]) for tp in span]
        ax.plot([p[1] for p in pts], [p[0] for p in pts], color=ALT, lw=0.9)
    ax.axhline(0, color="#cccccc", lw=0.6); ax.axvline(0, color="#cccccc", lw=0.6)
    # one event, shown with its S and S' coordinates (boost maps S -> S')
    ev_S = [1.5, 0.5, 0.0, 0.0]                    # (ct, x) in S
    ev_Sp = apply(boost(beta), ev_S)               # (ct', x') in S'
    ax.scatter([ev_S[1]], [ev_S[0]], color=FLOW, zorder=5, s=55)
    ax.annotate(r"$S:(ct,x)=(%.1f,%.1f)$" % (ev_S[0], ev_S[1]),
                (ev_S[1], ev_S[0]), textcoords="offset points", xytext=(8, 6),
                color=FLOW, fontsize=9)
    ax.annotate(r"$S':(ct',x')=(%.2f,%.2f)$" % (ev_Sp[0], ev_Sp[1]),
                (ev_S[1], ev_S[0]), textcoords="offset points", xytext=(8, -14),
                color=FLOW, fontsize=9)
    ax.set_xlim(-2.6, 2.6); ax.set_ylim(-2.6, 2.6); ax.set_aspect("equal")
    ax.set_xlabel("space $x$"); ax.set_ylabel("time $ct$")
    ax.set_title(r"$S'$ coordinate grid in $S$ ($\beta=0.5$), and one boosted event")
    ax.plot([], [], color=STEEL, lw=0.9, label=r"$ct'=$ const")
    ax.plot([], [], color=ALT, lw=0.9, label=r"$x'=$ const")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig2_boosted_grid.svg")
    caps["fig2_boosted_grid.svg"] = (
        "The S' coordinate mesh drawn in the S diagram for beta=0.5: lines of constant "
        "ct' (blue-grey) and constant x' (mauve) are obtained by applying inverse(boost) "
        "to a regular grid, producing the characteristic skewed lattice. One event is "
        "marked with both its S coordinates and its S' coordinates from boost(beta).")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
