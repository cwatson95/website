"""ST-13 figures — joint distributions: a joint density with its marginals, and
independence vs dependence as a factorization of the joint pmf.

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
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from joint_distributions import (                  # noqa: E402
    marginal_pdf_x, marginal_pdf_y, joint_pdf_is_valid, independent_pdf_check,
    marginal_x, marginal_y, joint_pmf_is_valid, independent_rv_check,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"
CMAP = LinearSegmentedColormap.from_list("ink", ["#ffffff", INK])


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — continuous joint pdf f(x,y)=x+y on the unit square, drawn as a
    # heatmap with the true marginals f_X, f_Y (from the module) on the margins.
    f = lambda x, y: x + y
    ax0, bx0, ay0, by0 = 0.0, 1.0, 0.0, 1.0
    gx = np.linspace(0.0, 1.0, 140)
    gy = np.linspace(0.0, 1.0, 140)
    X, Y = np.meshgrid(gx, gy, indexing="ij")
    Z = f(X, Y)
    fX = np.array([marginal_pdf_x(f, float(x), ay0, by0) for x in gx])   # int f dy
    fY = np.array([marginal_pdf_y(f, float(y), ax0, bx0) for y in gy])   # int f dx
    valid = joint_pdf_is_valid(f, ax0, bx0, ay0, by0)
    indep = independent_pdf_check(f, ax0, bx0, ay0, by0)

    fig = plt.figure(figsize=(6.2, 3.5))
    gs = fig.add_gridspec(2, 2, width_ratios=(4.0, 1.0), height_ratios=(1.0, 4.0),
                          wspace=0.04, hspace=0.04)
    ax_main = fig.add_subplot(gs[1, 0])
    ax_top = fig.add_subplot(gs[0, 0], sharex=ax_main)
    ax_right = fig.add_subplot(gs[1, 1], sharey=ax_main)

    ax_main.contourf(X, Y, Z, levels=12, cmap=CMAP)
    ax_main.set_xlabel("$x$"); ax_main.set_ylabel("$y$")
    ax_main.set_xlim(0, 1); ax_main.set_ylim(0, 1)

    ax_top.plot(gx, fX, color=FLOW, lw=2)
    ax_top.fill_between(gx, fX, color=FLOW, alpha=0.15)
    ax_top.set_ylabel(r"$f_X$")
    ax_top.tick_params(labelbottom=False); ax_top.set_ylim(bottom=0)

    ax_right.plot(fY, gy, color=ALT, lw=2)
    ax_right.fill_betweenx(gy, fY, color=ALT, alpha=0.15)
    ax_right.set_xlabel(r"$f_Y$")
    ax_right.tick_params(labelleft=False); ax_right.set_xlim(left=0)

    ax_top.set_title(r"Joint pdf $f(x,y)=x+y$ with marginals "
                     f"(valid={valid}, independent={indep})", fontsize=10)
    _save(fig, "fig1_joint_pdf_marginals.svg")
    caps["fig1_joint_pdf_marginals.svg"] = (
        "Continuous joint density f(x,y)=x+y on the unit square (heatmap), with the "
        "marginals f_X(x)=x+1/2 (top) and f_Y(y)=y+1/2 (right) computed by integrating "
        "out the other variable. The density is a valid pdf but NOT a product of its "
        "marginals, so X and Y are dependent.")

    # Fig 2 — independence vs dependence as a factorization test on a discrete pmf.
    sup = np.arange(6)
    px = np.array([0.10, 0.20, 0.30, 0.22, 0.12, 0.06]); px /= px.sum()
    py = np.array([0.18, 0.30, 0.26, 0.14, 0.08, 0.04]); py /= py.sum()
    P_ind = np.outer(px, py)                          # independent by construction
    I, J = np.meshgrid(sup, sup, indexing="ij")
    W = np.exp(-0.5 * ((I - J) / 0.9) ** 2)           # mass hugs the diagonal
    P_dep = W / W.sum()                               # dependent

    valid_i = joint_pmf_is_valid(P_ind); indep_i = independent_rv_check(P_ind)
    valid_d = joint_pmf_is_valid(P_dep); indep_d = independent_rv_check(P_dep)

    fig, axes = plt.subplots(1, 2, figsize=(6.2, 3.5))
    vmax = max(P_ind.max(), P_dep.max())
    for ax, P, lab, ind in [
        (axes[0], P_ind, r"$f=f_X f_Y$", indep_i),
        (axes[1], P_dep, "diagonal mass", indep_d),
    ]:
        im = ax.imshow(P.T, origin="lower", cmap=CMAP, vmin=0.0, vmax=vmax,
                       extent=(-0.5, 5.5, -0.5, 5.5))
        ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
        ax.set_title(f"{lab}\nindependent = {ind}", fontsize=10)
        ax.set_xticks(sup); ax.set_yticks(sup)
    fig.colorbar(im, ax=axes, fraction=0.046, pad=0.04, label=r"$f(x,y)$")
    fig.suptitle(r"Independence $\Leftrightarrow$ joint pmf factors  "
                 r"$f(x,y)=f_X(x)\,f_Y(y)$", fontsize=11)
    _save(fig, "fig2_independence_vs_dependence.svg")
    caps["fig2_independence_vs_dependence.svg"] = (
        "Two valid discrete joint pmfs f(x,y). Left: an outer product f=f_X f_Y, so the "
        "factorization test returns independent=True. Right: mass concentrated on the "
        "diagonal does not factor, so independent=False -- X and Y are dependent.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
