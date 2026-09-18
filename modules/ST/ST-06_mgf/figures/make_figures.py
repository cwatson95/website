"""ST-06 figures -- moment-generating functions.

Two SVG figures (+ captions.json) built from the module's own code in ../code:
  fig1 -- two MGFs with the SAME mean: equal slope at 0, different curvature;
  fig2 -- moments by differentiation: M'(0)=E[X], M''(0)=E[X^2] (tangent + Taylor).
Run:  python3 make_figures.py
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"
matplotlib.rcParams["font.size"] = 11
import matplotlib.pyplot as plt                    # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from mgf import (                                  # noqa: E402
    poisson_mgf, binomial_mgf, mgf, binomial_dist,
    mean_from_mgf, moment_from_mgf, var_from_mgf,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- two MGFs sharing a mean (Poisson(2) and Binomial(8, 0.25)).
    t = np.linspace(-1.0, 0.6, 220)
    Mp = np.array([poisson_mgf(ti, 2.0) for ti in t])
    Mb = np.array([binomial_mgf(ti, 8, 0.25) for ti in t])
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(t, Mp, color=FLOW, lw=2, label=r"Poisson$(2)$,  var $=2$")
    ax.plot(t, Mb, color=INK, lw=2, label=r"Binomial$(8,0.25)$,  var $=1.5$")
    ax.plot(t, 1.0 + 2.0 * t, color=ALT, lw=1.3, ls="--",
            label=r"shared tangent $1+\mu t$")
    ax.plot([0], [1], "o", color="#444444", zorder=4)
    ax.set_xlabel(r"$t$"); ax.set_ylabel(r"$M(t)=E[e^{tX}]$")
    ax.set_ylim(0, 6)
    ax.set_title(r"Same mean $\mu=2$ (slope at $0$), different variance (curvature)")
    ax.legend(loc="upper left", frameon=False)
    _save(fig, "fig1_two_mgfs.svg")
    caps["fig1_two_mgfs.svg"] = (
        "Two distributions with the same mean mu=2 have mgfs M(t)=E[e^{tX}] that share "
        "the value M(0)=1 and the same slope at 0 (the dashed tangent 1+mu*t). They "
        "diverge because their variances differ (Poisson 2 vs Binomial 1.5): the second "
        "derivative M''(0)=E[X^2] sets the curvature.")

    # Fig 2 -- moments from derivatives of the mgf (Binomial(10, 0.3)).
    vals, probs = binomial_dist(10, 0.3)
    t = np.linspace(-0.7, 0.4, 220)
    M = np.array([mgf(ti, vals, probs) for ti in t])
    m1 = mean_from_mgf(vals, probs)            # M'(0)  = E[X]   = 3.0
    m2 = moment_from_mgf(2, vals, probs)       # M''(0) = E[X^2]
    v = var_from_mgf(vals, probs)              # M''(0) - M'(0)^2
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(t, M, color=INK, lw=2, label=r"$M(t)=E[e^{tX}]$")
    ax.plot(t, 1.0 + m1 * t, color=FLOW, lw=1.5, ls="--",
            label=fr"tangent $1+\mu t$,  $\mu={m1:.2f}$")
    ax.plot(t, 1.0 + m1 * t + 0.5 * m2 * t ** 2, color=ALT, lw=1.5, ls=":",
            label=r"$1+\mu t+\frac{1}{2}E[X^{2}]t^{2}$")
    ax.plot([0], [1], "o", color="#444444", zorder=4)
    ax.set_xlabel(r"$t$"); ax.set_ylabel(r"$M(t)$"); ax.set_ylim(0, 4.5)
    ax.set_title(r"$M'(0)=E[X]$,  $M''(0)=E[X^{2}]$: moments from slope & curvature")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.text(0.97, 0.06, fr"$E[X^{{2}}]={m2:.2f}$,   Var $={v:.2f}$",
            transform=ax.transAxes, ha="right", fontsize=9, color=INK)
    _save(fig, "fig2_moments_from_mgf.svg")
    caps["fig2_moments_from_mgf.svg"] = (
        "For Binomial(10, 0.3) the mgf's derivatives at 0 are the moments: the slope "
        "M'(0)=E[X]=3.00 gives the dashed tangent, and adding the curvature term with "
        "M''(0)=E[X^2]=11.10 gives the dotted quadratic that hugs M(t) near t=0. Hence "
        "the variance is M''(0)-M'(0)^2 = 2.10.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
