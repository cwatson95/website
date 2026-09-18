"""ST-11 figures — the gamma family by shape, and sums of exponentials become gamma.

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
from exponential_gamma_chisquare import (          # noqa: E402
    exponential_pdf, gamma_pdf, convolve_two_exponentials_pdf,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    xs = np.linspace(0.0, 16.0, 400)

    # Fig 1 — the gamma family at fixed scale: shape a sets the bend.
    theta = 1.0
    params = [(1.0, INK), (2.0, FLOW), (3.0, ALT), (5.0, STEEL)]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for alpha, col in params:
        y = [gamma_pdf(x, alpha, theta) for x in xs]
        lbl = fr"$\alpha={alpha:.0f}$" + ("  (exponential)" if alpha == 1.0 else "")
        ax.plot(xs, y, color=col, lw=2, label=lbl)
    ax.set_xlabel("$x$"); ax.set_ylabel("$f(x)$")
    ax.set_title(r"Gamma family, scale $\theta=1$: shape $\alpha$ controls the shape")
    ax.legend(frameon=False)
    _save(fig, "fig1_gamma_family.svg")
    caps["fig1_gamma_family.svg"] = (
        "Gamma pdfs f(x)=x^{a-1} e^{-x/theta} / (Gamma(a) theta^a) at scale theta=1 "
        "for shape a=1,2,3,5 (from gamma_pdf). a=1 is the exponential's pure decay; "
        "larger a pushes the peak right. Chi-square with r d.o.f. is gamma(r/2, 2).")

    # Fig 2 — a sum of a iid exponentials is gamma (Erlang waiting time).
    lam = 1.0
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(xs, [exponential_pdf(x, lam) for x in xs], color=INK, lw=2,
            label=r"Exp  (sum of 1, $\alpha=1$)")
    ax.plot(xs, [convolve_two_exponentials_pdf(x, lam) for x in xs], color=FLOW, lw=2,
            label=r"Exp$\,*\,$Exp  (sum of 2)")
    ax.plot(xs, [gamma_pdf(x, 2.0, 1.0 / lam) for x in xs], color="k", lw=0,
            marker="o", ms=4, markevery=14, label=r"gamma$(\alpha=2)$")
    ax.plot(xs, [gamma_pdf(x, 3.0, 1.0 / lam) for x in xs], color=ALT, lw=2,
            label=r"gamma$(\alpha=3)$  (sum of 3)")
    ax.set_xlabel("$x$"); ax.set_ylabel("$f(x)$")
    ax.set_title(r"Sum of $\alpha$ iid exponentials is gamma (Erlang)")
    ax.legend(frameon=False)
    _save(fig, "fig2_sum_exponentials.svg")
    caps["fig2_sum_exponentials.svg"] = (
        "Adding iid exponentials (rate 1) builds the gamma family: one exponential "
        "(a=1), the convolution of two from convolve_two_exponentials_pdf (a=2), and "
        "three (a=3). The black dots are gamma_pdf(a=2), confirming the sum-of-two equals gamma.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
