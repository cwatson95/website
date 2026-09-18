"""ST-17 figures — the MGF technique & sampling distributions: the sampling
distribution of the mean sharpening as n grows, and a sum of iid variables
collapsing to a known family (Gamma) by the multiply-the-MGFs rule.

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
from mgf_technique_sampling import (               # noqa: E402
    sampling_dist_of_mean, normal_pdf, sum_of_gammas_via_mgf, gamma_pdf,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — sampling distribution of the mean: X_i iid N(mu, sigma^2) gives
    # Xbar ~ N(mu, sigma^2/n) (module fn), which sharpens as n grows.
    mu, sigma2 = 0.0, 4.0
    xs = np.linspace(-6.0, 6.0, 400)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    cols = [STEEL, ALT, "#7a8a4a", FLOW, INK]
    for n, col in zip((1, 2, 4, 8, 16), cols):
        m, v = sampling_dist_of_mean(mu, sigma2, n)
        sd = math.sqrt(v)
        y = np.array([normal_pdf(float(x), m, sd) for x in xs])
        ax.plot(xs, y, color=col, lw=2,
                label=fr"$n={n}$  ($\sigma^2/n={v:.2f}$)")
    ax.set_xlim(-6, 6); ax.set_xlabel(r"$\bar{X}$"); ax.set_ylabel("density")
    ax.set_title(r"Sampling distribution of the mean: "
                 r"$\bar{X}\sim N(\mu,\sigma^2/n)$")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_sampling_mean.svg")
    caps["fig1_sampling_mean.svg"] = (
        "For X_i iid N(0,4) the sample mean is exactly N(mu, sigma^2/n). As the sample "
        "size n grows the variance sigma^2/n shrinks, so the sampling distribution of "
        "Xbar concentrates and sharpens around the population mean mu=0.")

    # Fig 2 — MGF technique: a sum of n iid Exp(1) = Gamma(1,1) is Gamma(n,1),
    # because multiplying the MGFs adds the shapes (sum_of_gammas_via_mgf).
    xx = np.linspace(0.0, 16.0, 400)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for n, col in zip((1, 2, 3, 5, 8), cols):
        alpha, theta = sum_of_gammas_via_mgf([1.0] * n, 1.0)   # -> (n, 1)
        y = np.array([gamma_pdf(float(x), alpha, theta) for x in xx])
        ax.plot(xx, y, color=col, lw=2,
                label=fr"$n={n}\;\to\;\mathrm{{Gamma}}({alpha:.0f},1)$")
    ax.set_xlim(0, 16); ax.set_xlabel("sum $S_n$"); ax.set_ylabel("density")
    ax.set_title(r"MGF technique: $\sum_{i=1}^{n}\mathrm{Exp}(1)"
                 r"\sim\mathrm{Gamma}(n,1)$")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_sum_to_gamma.svg")
    caps["fig2_sum_to_gamma.svg"] = (
        "The MGF of a sum of independents is the product of their MGFs, so summing n iid "
        "Exp(1)=Gamma(1,1) variables adds the shape parameters to give Gamma(n,1). The "
        "exact summed density is plotted for several n, moving from a decaying "
        "exponential toward a bell shape.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
