"""ST-10 figures — continuous RV: the cdf as a running integral, probability as area.

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
from continuous_rv import (                        # noqa: E402
    cdf_from_pdf, prob_between, expectation_continuous,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def main():
    caps = {}
    a, b = 0.0, 1.0
    f = lambda x: 2.0 * x                  # triangular density on [0,1]; cdf = x^2
    xs = np.linspace(a, b, 120)

    def _save(fig, name):
        fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
        plt.close(fig)

    # Fig 1 — pdf and its cdf side by side: F(x) is the running area under f.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(6.2, 3.5))
    fx = [f(x) for x in xs]
    axL.plot(xs, fx, color=INK, lw=2)
    axL.fill_between(xs, fx, color=INK, alpha=0.12)
    axL.set_title("pdf  $f(x)=2x$"); axL.set_xlabel("$x$"); axL.set_ylabel("$f(x)$")
    Fx = [cdf_from_pdf(f, x, a, 2000) for x in xs]
    axR.plot(xs, Fx, color=FLOW, lw=2)
    axR.set_title(r"cdf  $F(x)=\int_{0}^{x} f$")
    axR.set_xlabel("$x$"); axR.set_ylabel("$F(x)$")
    fig.tight_layout()
    _save(fig, "fig1_pdf_cdf.svg")
    caps["fig1_pdf_cdf.svg"] = (
        "The triangular density f(x)=2x (left) and its cdf F(x) (right), where F "
        "is built point by point with cdf_from_pdf as the running integral of f "
        "from 0 to x. The cdf rises from 0 to 1, steepest where the density is largest.")

    # Fig 2 — probability is area: P(a<X<b) shaded, value from prob_between.
    lo, hi = 0.3, 0.7
    prob = prob_between(f, lo, hi)
    mu = expectation_continuous(f, a, b)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(xs, fx, color=INK, lw=2, label="$f(x)=2x$")
    mask = (xs >= lo) & (xs <= hi)
    ax.fill_between(xs[mask], [f(x) for x in xs[mask]], color=FLOW, alpha=0.4,
                    label=fr"$P({lo}<X<{hi})={prob:.3f}$")
    ax.axvline(mu, color=ALT, lw=1.5, ls="--", label=fr"$E[X]={mu:.3f}$")
    ax.set_xlabel("$x$"); ax.set_ylabel("$f(x)$")
    ax.set_title(r"Probability as area:  $P(a<X<b)=\int_a^b f$")
    ax.legend(frameon=False)
    _save(fig, "fig2_prob_area.svg")
    caps["fig2_prob_area.svg"] = (
        "For the same pdf, P(0.3<X<0.7) is the shaded area under f (orange), "
        "computed by prob_between, and equals F(0.7)-F(0.3). The dashed line marks "
        "the mean E[X]=integral x f(x) dx from expectation_continuous.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
