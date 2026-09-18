"""ST-02 figures -- counting: permutations vs combinations, Pascal's triangle.

Two SVG figures (+ captions.json) built from the module's own code in ../code:
  fig1 -- P(n,k) vs C(n,k) over k (permutations grow k! times faster);
  fig2 -- row n of Pascal's triangle as a bar chart, summing to 2^n.
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
from counting import (                             # noqa: E402
    permutations, combinations, pascal_row, binomial_coefficient_sum,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    n = 10

    # Fig 1 -- ordered (permutations) vs unordered (combinations) counts.
    ks = list(range(0, n + 1))
    P = [permutations(n, k) for k in ks]
    C = [combinations(n, k) for k in ks]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(ks, P, "o-", color=FLOW, lw=2,
            label=r"$P(n,k)=\frac{n!}{(n-k)!}$  (ordered)")
    ax.plot(ks, C, "s-", color=INK, lw=2,
            label=r"$C(n,k)=\frac{n!}{k!\,(n-k)!}$  (unordered)")
    ax.set_yscale("log")
    ax.set_xlabel(r"sample size $k$  (drawn from $n=10$)")
    ax.set_ylabel("number of ways"); ax.set_xticks(ks)
    ax.set_title(r"Ordered vs unordered:  $P(n,k)=k!\,C(n,k)$")
    ax.legend(loc="upper left", frameon=False)
    _save(fig, "fig1_perm_vs_comb.svg")
    caps["fig1_perm_vs_comb.svg"] = (
        "Counting k-subsets of n=10 items. Ordered samples P(n,k) (orange) outnumber "
        "unordered samples C(n,k) (blue) by exactly k!, the number of orderings of each "
        "chosen subset; the log axis spans the millionfold gap that order creates.")

    # Fig 2 -- row n of Pascal's triangle; the bars sum to 2^n.
    row = pascal_row(n)
    total = binomial_coefficient_sum(n)
    cols = [FLOW if k == n // 2 else INK for k in range(n + 1)]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.bar(range(n + 1), row, color=cols, width=0.74)
    for k, c in enumerate(row):
        ax.annotate(str(c), (k, c), ha="center", va="bottom",
                    xytext=(0, 2), textcoords="offset points", fontsize=8)
    ax.set_xlabel(r"$k$"); ax.set_ylabel(r"$C(10,k)$"); ax.set_xticks(range(n + 1))
    ax.set_ylim(0, max(row) * 1.18)
    ax.set_title(fr"Pascal row $n=10$:  $\sum_k C(10,k)=2^{{10}}={total}$")
    _save(fig, "fig2_pascal_row.svg")
    caps["fig2_pascal_row.svg"] = (
        "Row n=10 of Pascal's triangle, the binomial coefficients C(10,k). They are "
        "symmetric about the central term C(10,5)=252 (highlighted) and sum to "
        "2^10 = 1024, the total number of subsets of a 10-element set.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
