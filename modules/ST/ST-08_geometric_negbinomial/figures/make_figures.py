"""ST-08 figures — geometric & negative binomial: waiting times and memorylessness.

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
from geometric_negbinomial import (                # noqa: E402
    negbinom_pmf, geometric_sf, memoryless_check,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    p = 0.3

    # Fig 1 — negative binomial pmf for r=1,2,3: waiting time to the r-th success.
    xs = np.arange(1, 26)
    params = [(1, INK), (2, FLOW), (3, ALT)]
    width = 0.27
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for i, (r, col) in enumerate(params):
        pmf = [negbinom_pmf(int(x), r, p) for x in xs]
        lbl = fr"$r={r}$" + ("  (geometric)" if r == 1 else f"  ($\\mu=r/p={r/p:.1f}$)")
        ax.bar(xs + (i - 1) * width, pmf, width=width, color=col, label=lbl)
    ax.set_xlabel("trials $x$ to the $r$-th success"); ax.set_ylabel("$P(X=x)$")
    ax.set_title(fr"Negative binomial pmf ($p={p}$): the $r=1$ case is geometric")
    ax.legend(frameon=False)
    _save(fig, "fig1_negbinom_pmf.svg")
    caps["fig1_negbinom_pmf.svg"] = (
        "Negative binomial pmf P(X=x)=C(x-1,r-1)(1-p)^{x-r} p^r for p=0.3 and "
        "r=1,2,3 (bars, from negbinom_pmf). X counts the trials to the r-th "
        "success; r=1 is the geometric law, and the mean r/p moves right with r.")

    # Fig 2 — memoryless geometric tail: the conditional tail equals the original.
    ns = np.arange(0, 15)
    marg = [geometric_sf(int(nn), p) for nn in ns]
    m = 5
    cond = [memoryless_check(m, int(nn), p)[0] for nn in ns]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.bar(ns, marg, width=0.7, color=STEEL, alpha=0.7,
           label=r"$P(X>n)=(1-p)^{n}$")
    ax.plot(ns, cond, "o", color=FLOW, ms=6,
            label=rf"$P(X>{m}+n \mid X>{m})$")
    ax.set_xlabel("$n$"); ax.set_ylabel("survival probability")
    ax.set_title("Memoryless geometric tail: the shifted tail matches the original")
    ax.legend(frameon=False)
    _save(fig, "fig2_memoryless_tail.svg")
    caps["fig2_memoryless_tail.svg"] = (
        "Geometric survival P(X>n)=(1-p)^n (bars, from geometric_sf) and the "
        "conditional tail P(X>5+n | X>5) (orange dots, from memoryless_check) for "
        "p=0.3. They coincide: having waited 5 trials does not change the future.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
