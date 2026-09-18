"""ST-14 figures — correlation & conditional distributions: the conditional mean
E[Y|X] (regression function) over a joint law, and how the correlation rho changes
its sign and slope.

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
from correlation_conditional import (              # noqa: E402
    Joint, correlation, regression_function, regression_line,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def make_bvn_joint(rho, k=8, s=2.2):
    """A discrete bivariate-normal-like Joint on a centred integer grid, built so
    correlation(j) ~ rho.  Returns the module's Joint object."""
    vals = np.arange(k + 1) - k / 2.0
    X, Y = np.meshgrid(vals, vals, indexing="ij")
    q = (X * X - 2.0 * rho * X * Y + Y * Y) / (2.0 * (1.0 - rho * rho) * s * s)
    P = np.exp(-q)
    P /= P.sum()
    return Joint(vals, vals, P)


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _bubble(ax, j, color=INK):
    """Probability 'scatter': each support point sized by its joint probability."""
    X, Y = np.meshgrid(j.xs, j.ys, indexing="ij")
    s = 900.0 * j.P / j.P.max()
    ax.scatter(X.ravel(), Y.ravel(), s=s.ravel(), color=color, alpha=0.30,
               edgecolors="none", zorder=1)


def main():
    caps = {}

    # Fig 1 — one positively-correlated joint: bubble scatter + the conditional
    # mean E[Y|X=x] (regression function) and the least-squares line.
    j = make_bvn_joint(0.7)
    rho = correlation(j)
    xr, g = regression_function(j)                 # x -> E[Y|X=x]
    a, b = regression_line(j)                       # least-squares slope/intercept

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    _bubble(ax, j, INK)
    ax.plot(xr, g, color=FLOW, lw=2.2, marker="o", ms=5,
            label=r"$E[Y\,|\,X=x]$ (regression fn)")
    ax.plot(xr, a + b * xr, color=ALT, lw=2, ls="--",
            label=fr"least-squares line, slope $={b:+.2f}$")
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title(fr"Conditional mean over a joint law  ($\rho={rho:+.2f}$)")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig1_conditional_mean.svg")
    caps["fig1_conditional_mean.svg"] = (
        "A positively correlated discrete joint law (bubble area = joint probability). "
        "The orange curve is the conditional mean E[Y|X=x], the regression function; the "
        "dashed line is the least-squares predictor with slope rho*sigma_Y/sigma_X. Here "
        "the measured correlation is about +0.7.")

    # Fig 2 — same construction at three correlations: positive, zero, negative.
    fig, axes = plt.subplots(1, 3, figsize=(6.2, 3.5), sharex=True, sharey=True)
    for ax, rho_set, col in zip(axes, (0.8, 0.0, -0.8), (FLOW, STEEL, ALT)):
        jj = make_bvn_joint(rho_set)
        r = correlation(jj)
        xr, g = regression_function(jj)
        _bubble(ax, jj, INK)
        ax.plot(xr, g, color=col, lw=2.2, marker="o", ms=3)
        ax.axhline(0.0, color="#bbbbbb", lw=0.6, zorder=0)
        ax.set_title(fr"$\rho={r:+.2f}$", fontsize=10)
        ax.set_xlabel("$x$")
    axes[0].set_ylabel("$y$")
    fig.suptitle(r"Correlation sets the tilt of $E[Y\,|\,X]$: "
                 r"positive, zero, negative", fontsize=11)
    fig.tight_layout()
    _save(fig, "fig2_correlation_signs.svg")
    caps["fig2_correlation_signs.svg"] = (
        "The same bivariate-normal-like joint at three correlations. With rho>0 the "
        "conditional mean E[Y|X] rises, with rho=0 it is flat (Y unrelated to X on "
        "average), and with rho<0 it falls. Correlation measures the sign and strength "
        "of the linear association.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
