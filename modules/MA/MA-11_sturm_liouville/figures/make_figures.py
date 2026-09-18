"""MA-11 figures — Sturm-Liouville eigenfunctions and eigenfunction completeness.

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
from sturm_liouville import (                       # noqa: E402
    sl_eigenpairs, expand, reconstruct,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"
L = math.pi


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — lowest eigenfunctions of  -y'' = lambda y  on [0, pi], Dirichlet
    # (p = w = 1, q = 0) from sl_eigenpairs: the canonical SL problem whose
    # eigenpairs are (n^2, sin n x) — i.e. the Fourier sine basis.
    lams, ys, xs, wv, h = sl_eigenpairs(1.0, 0.0, 1.0, 0.0, L, 200, 4)
    cols = [INK, FLOW, ALT, STEEL]
    xf = np.array([0.0] + list(xs) + [L])           # impose the Dirichlet ends
    xfine = np.linspace(0.0, L, 400)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for nidx, (lam, y, col) in enumerate(zip(lams, ys, cols)):
        n = nidx + 1
        yv = np.array(y); yv = yv / np.max(np.abs(yv))          # scale to amplitude 1
        ax.plot(xf, np.concatenate(([0.0], yv, [0.0])), color=col, lw=2,
                label=fr"$y_{n}$:  $\lambda={lam:.3f}$  ($n^2={n*n}$)")
        ax.plot(xfine, np.sin(n * xfine), color=col, lw=1.0, ls=":", alpha=0.6)
    ax.axhline(0, color="#cccccc", lw=0.6)
    ax.set_xlim(0, L); ax.set_ylim(-1.2, 1.7)
    ax.set_xticks([0, math.pi / 2, math.pi]); ax.set_xticklabels(["0", r"$\pi/2$", r"$\pi$"])
    ax.set_xlabel("$x$"); ax.set_ylabel("eigenfunction (normalized)")
    ax.set_title(r"Sturm-Liouville eigenfunctions of $-y''=\lambda y$ on $[0,\pi]$")
    ax.legend(loc="upper center", frameon=False, fontsize=8.5, ncol=2)
    _save(fig, "fig1_eigenfunctions.svg")
    caps["fig1_eigenfunctions.svg"] = (
        "The four lowest eigenfunctions of $\\mathcal{L}y=-y''=\\lambda w y$ on "
        "$[0,\\pi]$ (Dirichlet, $p=w=1$) from sl_eigenpairs. The finite-difference "
        "eigenvalues $\\lambda_n$ track the exact $n^2$ and the eigenfunctions match "
        "$\\sin nx$ (dotted) — Fourier analysis is the simplest Sturm-Liouville "
        "problem, with $w$-orthogonal modes.")

    # Fig 2 — completeness: a symmetric tent f(x) = min(x, pi - x) expanded in the
    # SL eigenbasis via expand, partial sums rebuilt with reconstruct.
    lamA, ysA, xsA, wvA, hA = sl_eigenpairs(1.0, 0.0, 1.0, 0.0, L, 120, 12)
    xA = np.array(xsA)
    f = [min(x, L - x) for x in xsA]                # tent, peak pi/2, zero at the ends
    c = expand(f, ysA, wvA, hA)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(xA, f, color="#999999", lw=2.4, alpha=0.5, label="tent  $f(x)$")
    for M, col in [(1, STEEL), (3, ALT), (9, FLOW)]:
        rec = reconstruct(c[:M], ysA[:M])
        ax.plot(xA, rec, color=col, lw=1.7, label=fr"{M}-term sum")
    ax.axhline(0, color="#cccccc", lw=0.6)
    ax.set_xlim(0, L)
    ax.set_xticks([0, math.pi / 2, math.pi]); ax.set_xticklabels(["0", r"$\pi/2$", r"$\pi$"])
    ax.set_xlabel("$x$"); ax.set_ylabel("$f(x)$  and partial sums")
    ax.set_title(r"Completeness: a tent rebuilt from SL eigenfunctions")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_completeness.svg")
    caps["fig2_completeness.svg"] = (
        "Eigenfunction completeness: the tent $f(x)=\\min(x,\\pi-x)$ expanded in the "
        "SL eigenbasis with expand ($c_n=\\langle f,y_n\\rangle_w/\\langle "
        "y_n,y_n\\rangle_w$) and rebuilt by reconstruct. Only odd modes contribute "
        "(symmetry); the partial sums sharpen toward the peak as terms are added, "
        "converging in the mean (Parseval) — any nice $f$ expands in the eigenbasis.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
