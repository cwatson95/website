"""MA-16 figures — the metric as a length ellipse, and a rank-2 tensor as a
rotation-invariant quadric.

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
from tensors import (                               # noqa: E402
    metric_from_map, inner, det_levi_civita, matvec,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _quadric(T, phis):
    """The unit set {v : v^T T v = 1} as (x,y): along direction (cos,sin) the
    radius is 1/sqrt(d^T T d), evaluated with the module's `inner`."""
    xs, ys = [], []
    for ph in phis:
        d = [math.cos(ph), math.sin(ph)]
        rad = 1.0 / math.sqrt(inner(T, d, d))
        xs.append(rad * d[0])
        ys.append(rad * d[1])
    return xs, ys


def main():
    caps = {}
    phis = np.linspace(0.0, 2.0 * math.pi, 400)

    # Fig 1 — the metric as a ruler. For polar coordinates the induced metric
    # metric_from_map(polar, [r, th]) = diag(1, r^2); the unit-length set
    # g_ij v^i v^j = 1 is an ellipse that flattens along v^theta as r grows,
    # because a unit step in the theta-component spans arclength r.
    polar = lambda q: [q[0] * math.cos(q[1]), q[0] * math.sin(q[1])]

    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    for r, col in [(1.0, INK), (2.0, FLOW), (3.0, STEEL)]:
        g = metric_from_map(polar, [r, 0.7])               # diag(1, r^2)
        xs, ys = _quadric(g, phis)
        ax.plot(xs, ys, color=col, lw=2,
                label=fr"$r={r:.0f}$:  $g=\mathrm{{diag}}(1,{r**2:.0f})$")
    ax.axhline(0, color="#cccccc", lw=0.6)
    ax.axvline(0, color="#cccccc", lw=0.6)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$v^{r}$ component")
    ax.set_ylabel(r"$v^{\theta}$ component")
    ax.set_title(r"Polar metric $g=\mathrm{diag}(1,r^2)$: the unit-length set $g_{ij}v^iv^j=1$")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_metric_ellipse.svg")
    caps["fig1_metric_ellipse.svg"] = (
        r"The metric $g_{ij}$ is the ruler that turns components into length. For polar "
        r"coordinates metric_from_map gives $g=\mathrm{diag}(1,r^2)$; the unit-length "
        r"locus $g_{ij}v^iv^j=1$ (drawn with the module's `inner`) is a circle at $r=1$ "
        r"but flattens along $v^\theta$ as $r$ grows — a unit step in the $\theta$ "
        r"component spans arclength $r$, so it 'costs' more length.")

    # Fig 2 — a rank-2 tensor is a geometric object. The quadric v^T T v = 1 is one
    # ellipse; rotating the coordinate frame changes the component matrix
    # (T' = R^T T R) but not the ellipse, nor the scalars det T (via det_levi_civita)
    # and tr T. Principal axes are the eigen-directions.
    T = [[2.0, 0.8], [0.8, 1.0]]
    xs, ys = _quadric(T, phis)

    A, B, C = T[0][0], T[0][1], T[1][1]
    tr = A + C
    disc = math.hypot(A - C, 2.0 * B)
    lam1, lam2 = (tr + disc) / 2.0, (tr - disc) / 2.0       # eigenvalues
    def _evec(lam):
        vx, vy = B, lam - A
        n = math.hypot(vx, vy)
        return (vx / n, vy / n)
    v1, v2 = _evec(lam1), _evec(lam2)                       # principal directions

    alpha = math.radians(35.0)                              # rotate the coordinate frame
    R = [[math.cos(alpha), -math.sin(alpha)],
         [math.sin(alpha), math.cos(alpha)]]
    e1p, e2p = matvec(R, [1.0, 0.0]), matvec(R, [0.0, 1.0])  # rotated basis vectors
    Rt = [[R[j][i] for j in range(2)] for i in range(2)]
    TR = [[sum(T[i][k] * R[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    Tp = [[sum(Rt[i][k] * TR[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    ax.plot(xs, ys, color=INK, lw=2.4, label=r"quadric $v^{\mathrm{T}}Tv=1$")
    # principal (eigen) axes — the invariant axes of the tensor
    for v, lam in ((v1, lam1), (v2, lam2)):
        L = 1.0 / math.sqrt(lam)
        ax.plot([-L * v[0], L * v[0]], [-L * v[1], L * v[1]],
                color=ALT, lw=1.4, ls="--")
    ax.plot([], [], color=ALT, lw=1.4, ls="--", label="principal axes (eigenvectors)")
    # the two coordinate frames
    Lax = 1.55
    for vec, col, lab, dxy in [([1, 0], "#999999", r"$e_1$", (0.04, -0.16)),
                               ([0, 1], "#999999", r"$e_2$", (-0.18, 0.04))]:
        ax.annotate("", xy=(Lax * vec[0], Lax * vec[1]), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color=col, lw=1.3))
        ax.text(Lax * vec[0] + dxy[0], Lax * vec[1] + dxy[1], lab, color=col, fontsize=10)
    for vec, lab, dxy in [(e1p, r"$e_1'$", (0.05, 0.02)), (e2p, r"$e_2'$", (-0.2, 0.0))]:
        ax.annotate("", xy=(Lax * vec[0], Lax * vec[1]), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color=STEEL, lw=1.3, ls="--"))
        ax.text(Lax * vec[0] + dxy[0], Lax * vec[1] + dxy[1], lab, color=STEEL, fontsize=10)

    box = (f"lab frame:   T = [[{T[0][0]:.2f}, {T[0][1]:.2f}], [{T[1][0]:.2f}, {T[1][1]:.2f}]]\n"
           f"rotated 35: T' = [[{Tp[0][0]:.2f}, {Tp[0][1]:.2f}], [{Tp[1][0]:.2f}, {Tp[1][1]:.2f}]]\n"
           f"det = {det_levi_civita(T):.3f} = {det_levi_civita(Tp):.3f}    "
           f"tr = {tr:.2f} = {Tp[0][0]+Tp[1][1]:.2f}")
    ax.text(0.5, -0.155, box, transform=ax.transAxes, ha="center", va="top",
            fontsize=8.0, family="monospace",
            bbox=dict(boxstyle="round", fc="#f4f4f8", ec="#bbbbbb", lw=0.7))

    ax.set_aspect("equal")
    ax.set_xlim(-1.7, 1.7)
    ax.set_ylim(-1.7, 1.7)
    ax.set_xlabel("")
    ax.set_title(r"A rank-2 tensor as a quadric: components rotate, the ellipse does not")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig2_tensor_quadric.svg")
    caps["fig2_tensor_quadric.svg"] = (
        r"A symmetric rank-2 tensor $T$ is the geometric ellipse $v^{\mathsf T}Tv=1$ "
        r"(drawn with `inner`), with principal axes along its eigenvectors. Rotating the "
        r"coordinate frame ($e_i\to e_i'$) changes the component matrix to $T'=R^{\mathsf "
        r"T}TR$ (see box), but the ellipse is unmoved and the scalars $\det T$ "
        r"(det_levi_civita) and $\mathrm{tr}\,T$ are invariant — that is what makes $T$ a "
        r"tensor, not just a matrix.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
