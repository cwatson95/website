"""MA-05 figures — the n-th roots in the complex plane and the principal branch cut.

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
from complex_numbers import (                       # noqa: E402
    roots_of_unity, nth_roots, principal_log, modulus,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _poly(ax, roots, color, marker, label):
    xs = [w.real for w in roots] + [roots[0].real]   # close the polygon
    ys = [w.imag for w in roots] + [roots[0].imag]
    ax.plot(xs, ys, color=color, lw=1.4, alpha=0.7)
    ax.plot([w.real for w in roots], [w.imag for w in roots],
            marker=marker, ls="none", ms=8, color=color, label=label)


def main():
    caps = {}

    # Fig 1 — the n n-th roots sit equally spaced on a circle of radius r^{1/n}.
    n = 5
    unit = roots_of_unity(n)                 # 5th roots of 1  (unit circle)
    z0 = complex(0.0, 32.0)                  # |z0| = 32  ->  radius 32^{1/5} = 2
    gen = nth_roots(z0, n)                   # 5th roots of 32 i  (rotated, radius 2)
    r1, r2 = 1.0, modulus(z0) ** (1.0 / n)

    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(r1 * np.cos(th), r1 * np.sin(th), color="#bbbbbb", lw=0.9)
    ax.plot(r2 * np.cos(th), r2 * np.sin(th), color="#bbbbbb", lw=0.9, ls="--")
    for w in unit:                           # radial spokes e^{2 pi i k / n}
        ax.plot([0, w.real], [0, w.imag], color="#dddddd", lw=0.8, zorder=0)
    _poly(ax, unit, INK, "o", r"5th roots of $1$")
    _poly(ax, gen, FLOW, "s", r"5th roots of $32i$")
    ax.plot(0, 0, "*", ms=12, color="k")
    ax.annotate(r"$\sum$ roots $=0$", (0, 0), textcoords="offset points",
                xytext=(8, 6), fontsize=9)
    ax.axhline(0, color="#888888", lw=0.5); ax.axvline(0, color="#888888", lw=0.5)
    ax.set_aspect("equal"); ax.set_xlim(-2.4, 2.4); ax.set_ylim(-2.4, 2.4)
    ax.set_xlabel(r"$\mathrm{Re}\,z$"); ax.set_ylabel(r"$\mathrm{Im}\,z$")
    ax.set_title(r"$n$-th roots: equally spaced by $2\pi/n$ on a circle of radius $r^{1/n}$")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_roots.svg")
    caps["fig1_roots.svg"] = (
        r"The five 5th-roots of $1$ (blue, from roots_of_unity) lie on the unit circle, "
        r"spaced $72^\circ$ apart and summing to $0$. The five 5th-roots of $32i$ "
        r"(orange, from nth_roots) sit on a circle of radius $32^{1/5}=2$, rotated by "
        r"$\arg(32i)/5$: every nonzero $z$ has exactly $n$ roots, evenly spaced by "
        r"$2\pi/n$ at radius $r^{1/n}$.")

    # Fig 2 — principal argument Im(Log z): the branch cut on the negative real axis.
    g = np.linspace(-2.0, 2.0, 241)
    Arg = np.empty((g.size, g.size))
    for iy, yv in enumerate(g):
        for ix, xv in enumerate(g):
            z = complex(xv, yv)
            Arg[iy, ix] = np.nan if z == 0 else principal_log(z).imag

    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    im = ax.imshow(Arg, extent=[-2, 2, -2, 2], origin="lower",
                   cmap="twilight", vmin=-np.pi, vmax=np.pi)
    ax.plot([-2, 0], [0, 0], color="w", lw=2.2, ls=(0, (4, 3)))
    ax.annotate("branch cut", (-1.0, 0.0), color="w", fontsize=9,
                ha="center", va="bottom")
    ax.set_aspect("equal")
    ax.set_xlabel(r"$\mathrm{Re}\,z$"); ax.set_ylabel(r"$\mathrm{Im}\,z$")
    ax.set_title(r"Principal argument $\mathrm{Im}\,\mathrm{Log}\,z=\arg z\in(-\pi,\pi]$")
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.set_ticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi])
    cb.set_ticklabels([r"$-\pi$", r"$-\pi/2$", "$0$", r"$\pi/2$", r"$\pi$"])
    _save(fig, "fig2_branch_cut.svg")
    caps["fig2_branch_cut.svg"] = (
        r"The imaginary part of the principal logarithm, $\mathrm{Im}\,\mathrm{Log}\,z=\arg z$, "
        r"over the complex plane (computed from principal_log). It is single-valued in "
        r"$(-\pi,\pi]$ but jumps by $2\pi$ across the negative real axis — the branch cut "
        r"(dashed). Crossing it flips $\sqrt z$ in sign and shifts $\mathrm{Log}\,z$ by $2\pi i$.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
