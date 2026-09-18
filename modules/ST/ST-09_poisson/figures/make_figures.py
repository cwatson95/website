"""ST-09 figures — the Poisson distribution: pmf shapes and the law of rare events.

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
from poisson import (                              # noqa: E402
    poisson_pmf, binomial_pmf, poisson_limit_of_binomial,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — Poisson pmf for three rates: the peak and spread grow with lambda.
    ks = np.arange(0, 21)
    params = [(1.0, INK), (4.0, FLOW), (10.0, ALT)]
    width = 0.27
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for i, (lam, col) in enumerate(params):
        pmf = [poisson_pmf(int(k), lam) for k in ks]
        ax.bar(ks + (i - 1) * width, pmf, width=width, color=col,
               label=fr"$\lambda={lam:.0f}$")
    ax.set_xlabel("count $k$"); ax.set_ylabel("$P(X=k)$")
    ax.set_title(r"Poisson pmf $e^{-\lambda}\lambda^{k}/k!$ for several $\lambda$")
    ax.legend(frameon=False)
    _save(fig, "fig1_poisson_pmf.svg")
    caps["fig1_poisson_pmf.svg"] = (
        "Poisson pmf P(X=k)=e^{-lambda} lambda^k / k! for lambda=1, 4, 10 (bars, "
        "from poisson_pmf). The single parameter lambda is both mean and variance, "
        "so the distribution shifts right and broadens as lambda increases.")

    # Fig 2 — law of rare events: Bin(n, lambda/n) -> Poisson(lambda) as n grows.
    lam = 4.0
    ks = np.arange(0, 16)
    pois = [poisson_pmf(int(k), lam) for k in ks]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.bar(ks, pois, width=0.8, color=STEEL, alpha=0.55,
           label=r"Poisson$(\lambda=4)$")
    for mk, col, nb in [("o", INK, 8), ("s", FLOW, 20), ("^", ALT, 80)]:
        pp = lam / nb
        bino = [binomial_pmf(int(k), nb, pp) for k in ks]
        gap = poisson_limit_of_binomial(nb, pp)
        ax.plot(ks, bino, marker=mk, color=col, ms=5, lw=1.0,
                label=fr"Bin$(n={nb},\,\lambda/n)$  gap$={gap:.1e}$")
    ax.set_xlabel("count $k$"); ax.set_ylabel("probability")
    ax.set_title(r"Law of rare events: Bin$(n,\lambda/n)\to$ Poisson$(\lambda)$")
    ax.legend(frameon=False)
    _save(fig, "fig2_poisson_limit.svg")
    caps["fig2_poisson_limit.svg"] = (
        "Binomial pmfs Bin(n, lambda/n) for n=8, 20, 80 (markers) closing on the "
        "Poisson(4) pmf (bars) as n grows with np=lambda=4 fixed. The legend shows "
        "the max gap from poisson_limit_of_binomial shrinking toward zero.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
