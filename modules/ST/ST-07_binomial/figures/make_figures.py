"""ST-07 figures — the binomial distribution: pmf shapes and the normal limit.

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
from binomial import (                             # noqa: E402
    binom_pmf, binom_mean, binom_std, _normal_pdf,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — binomial pmf at fixed n=10 for three p: skew flips through p=1/2.
    n = 10
    ks = np.arange(0, n + 1)
    params = [(0.2, INK), (0.5, FLOW), (0.8, ALT)]
    width = 0.27
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for i, (p, col) in enumerate(params):
        pmf = [binom_pmf(int(k), n, p) for k in ks]
        ax.bar(ks + (i - 1) * width, pmf, width=width, color=col,
               label=fr"$p={p}$  ($np={binom_mean(n, p):.0f}$)")
    ax.set_xticks(ks)
    ax.set_xlabel("successes $k$"); ax.set_ylabel("$P(X=k)$")
    ax.set_title(r"Binomial pmf $\mathrm{Bin}(n=10,\,p)$: the role of $p$")
    ax.legend(frameon=False)
    _save(fig, "fig1_binomial_pmf.svg")
    caps["fig1_binomial_pmf.svg"] = (
        "Binomial pmf P(X=k)=C(n,k) p^k (1-p)^{n-k} for n=10 and p=0.2, 0.5, 0.8 "
        "(bars), computed from binom_pmf. The mean sits at np; the shape is "
        "right-skewed for p<0.5, symmetric at p=0.5, and left-skewed for p>0.5.")

    # Fig 2 — de Moivre–Laplace: N(np, np(1-p)) approximates Bin(30, 1/2).
    nN, pN = 30, 0.5
    ksN = np.arange(0, nN + 1)
    pmfN = [binom_pmf(int(k), nN, pN) for k in ksN]
    mu, sigma = binom_mean(nN, pN), binom_std(nN, pN)
    xx = np.linspace(0, nN, 600)
    yy = [_normal_pdf(x, mu, sigma) for x in xx]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.bar(ksN, pmfN, width=0.9, color=STEEL, alpha=0.65,
           label=r"$\mathrm{Bin}(30,\frac{1}{2})$ pmf")
    ax.plot(xx, yy, color=FLOW, lw=2,
            label=fr"$N(np,\,np(1-p))$  ($\mu={mu:.0f},\ \sigma={sigma:.2f}$)")
    ax.set_xlim(5, 25)
    ax.set_xlabel("successes $k$"); ax.set_ylabel("probability / density")
    ax.set_title("de Moivre--Laplace: the normal approximation to the binomial")
    ax.legend(frameon=False)
    _save(fig, "fig2_normal_approx.svg")
    caps["fig2_normal_approx.svg"] = (
        "The Bin(30, 1/2) pmf (bars) with the normal density N(np, np(1-p)) "
        "overlaid (orange), using binom_mean and binom_std for the parameters. "
        "Near the peak the bell tracks the bars: the de Moivre-Laplace limit.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
