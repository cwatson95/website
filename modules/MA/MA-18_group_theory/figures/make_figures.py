"""MA-18 figures — Cayley tables (abelian vs non-abelian) and a cyclic representation orbit.

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
from groups import (                               # noqa: E402
    cyclic_group, symmetric_group, cyclic_rep, matmul,
)

INK, RUST, PLUM, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _cayley(G):
    """Cayley table as an integer matrix: M[i][j] = index of (e_i . e_j) in G."""
    el = G.elements
    idx = {e: i for i, e in enumerate(el)}
    n = len(el)
    return np.array([[idx[G.op(el[i], el[j])] for j in range(n)] for i in range(n)])


def main():
    caps = {}

    # Fig 1 — Cayley (multiplication) tables: Z_6 (abelian -> symmetric about the
    # diagonal) vs S_3 (non-abelian -> not symmetric). Both order 6.
    M1, M2 = _cayley(cyclic_group(6)), _cayley(symmetric_group(3))
    n = 6
    cmap = plt.get_cmap("Set3", n)
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.6))
    panels = [(axes[0], M1, r"$Z_6$ (abelian: symmetric)"),
              (axes[1], M2, r"$S_3$ (non-abelian: not symmetric)")]
    for ax, M, ttl in panels:
        ax.imshow(M, cmap=cmap, vmin=-0.5, vmax=n - 0.5)
        for i in range(n):
            for j in range(n):
                ax.text(j, i, str(int(M[i, j])), ha="center", va="center",
                        fontsize=8, color="#222222")
        ax.set_xticks(range(n)); ax.set_yticks(range(n))
        ax.set_xlabel(r"right factor $b$")
        ax.set_title(ttl, fontsize=10)
    axes[0].set_ylabel(r"left factor $a$")
    fig.suptitle(r"Cayley tables: cell $(a,b)$ = index of the product $a\cdot b$", y=1.01)
    _save(fig, "fig1_cayley_tables.svg")
    caps["fig1_cayley_tables.svg"] = (
        "Cayley (multiplication) tables built from FiniteGroup.op: each cell $(a,b)$ is "
        "colored and numbered by the index of the product $a\\cdot b$. $Z_6$ (cyclic) is "
        "symmetric across the diagonal — it is abelian, $ab=ba$ — while $S_3$, the "
        "smallest non-abelian group (the 6 permutations of 3 objects), is visibly NOT "
        "symmetric: $ab\\neq ba$. Every row and column is a permutation of all elements, "
        "the Latin-square property every group's table must have.")

    # Fig 2 — representation Z_n -> SO(2): R(k) = rotation by 2 pi k / n (cyclic_rep);
    # the orbit of (1,0) is a regular n-gon, and R(a)R(b) = R(a+b) is the homomorphism.
    n = 6
    reps = cyclic_rep(n)
    col = [[1.0], [0.0]]                            # the vector (1,0) as a column
    pts = [matmul(R, col) for R in reps]
    xs = [p[0][0] for p in pts]; ys = [p[1][0] for p in pts]

    fig, ax = plt.subplots(figsize=(5.4, 5.2))
    tt = np.linspace(0, 2 * math.pi, 240)
    ax.plot(np.cos(tt), np.sin(tt), color="#cccccc", lw=1.0)          # unit circle
    ax.plot(xs + [xs[0]], ys + [ys[0]], color=STEEL, lw=1.6, zorder=1)  # hexagon edges
    for k, (x, y) in enumerate(zip(xs, ys)):
        ax.plot([0, x], [0, y], color="#dddddd", lw=0.8, zorder=0)    # radial spoke
        ax.plot([x], [y], "o", ms=10, color=INK, zorder=2)
        ax.annotate(fr"$R({k})$", (x, y), textcoords="offset points",
                    xytext=(12 * x, 12 * y), ha="center", va="center", fontsize=9)
    ax.axhline(0, color="#eeeeee", lw=0.6); ax.axvline(0, color="#eeeeee", lw=0.6)
    ax.set_aspect("equal")
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title(r"$Z_6\to SO(2)$: orbit of $(1,0)$ is a regular hexagon")
    _save(fig, "fig2_cyclic_representation.svg")
    caps["fig2_cyclic_representation.svg"] = (
        "The representation $\\rho:Z_6\\to SO(2)$, $\\rho(k)=$ rotation by $2\\pi k/6$ "
        "(cyclic_rep), applied to the vector $(1,0)$. The six images $R(k)(1,0)$ "
        "(computed with matmul) are the vertices of a regular hexagon — the symmetry "
        "orbit. Because $R(a)R(b)=R(a+b)$, the rotations multiply exactly as $Z_6$ adds: "
        "a faithful homomorphism that turns the abstract group into matrices.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
