"""MA-19 figures — the Central Limit Theorem and a least-squares line fit.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
"""
import json
import math
import os
import random
import sys

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"      # text as vector paths (portable, no font dep)
matplotlib.rcParams["font.size"] = 11
import matplotlib.pyplot as plt                    # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from probability import (                          # noqa: E402
    sample_uniform_sum, normal_pdf, least_squares_line,
)

INK, RUST, PLUM, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    rng = random.Random(2024)

    # Fig 1 — Central Limit Theorem: the standardized sum of m U(0,1) variables
    # (sample_uniform_sum has mean 0, variance m/12) converges to N(0,1).
    N = 60000
    grid = np.linspace(-4, 4, 400)
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    for m, col in [(1, STEEL), (2, PLUM), (12, RUST)]:
        xs = sample_uniform_sum(m, N, rng)
        sd = math.sqrt(m / 12.0)
        z = [x / sd for x in xs]                    # standardize to unit variance
        ax.hist(z, bins=64, range=(-4, 4), density=True, histtype="step",
                color=col, lw=1.9, label=fr"$m={m}$ uniform(s)")
    ax.plot(grid, [normal_pdf(x) for x in grid], color=INK, lw=2.2, ls="--",
            label=r"$N(0,1)$ limit")
    ax.set_xlim(-4, 4)
    ax.set_xlabel(r"standardized sum $z=(\sum U-m/2)/\sqrt{m/12}$")
    ax.set_ylabel("probability density")
    ax.set_title(r"Central Limit Theorem: flat $\to$ triangular $\to$ Gaussian")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_central_limit.svg")
    caps["fig1_central_limit.svg"] = (
        "Central Limit Theorem via sample_uniform_sum: the sum of $m$ independent "
        "$U(0,1)$ variables, standardized to zero mean and unit variance, against the "
        "$N(0,1)$ density (normal_pdf, dashed). One uniform is flat, two make a triangle, "
        "and by $m=12$ the histogram is already an excellent Gaussian — why errors "
        "built from many small independent effects come out normally distributed.")

    # Fig 2 — least-squares line fit with a 1-sigma confidence band, from the
    # module's least_squares_line (returns slope, intercept, and their sigmas).
    xs = [i * 0.5 for i in range(20)]
    sigma_noise = 0.7
    ys = [2.0 + 3.0 * x + rng.gauss(0.0, sigma_noise) for x in xs]
    b, a, sb, sa = least_squares_line(xs, ys)
    nn = len(xs)
    xbar = sum(xs) / nn
    Sxx = sum((x - xbar) ** 2 for x in xs)
    s2 = sb ** 2 * Sxx                              # residual variance: sigma_b^2 = s^2/Sxx
    xx = np.linspace(min(xs) - 0.4, max(xs) + 0.4, 200)
    yhat = a + b * xx
    band = math.sqrt(s2) * np.sqrt(1.0 / nn + (xx - xbar) ** 2 / Sxx)

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.fill_between(xx, yhat - band, yhat + band, color=RUST, alpha=0.20,
                    label=r"$\pm 1\sigma$ fit band")
    ax.errorbar(xs, ys, yerr=sigma_noise, fmt="o", ms=4, color=INK,
                ecolor="#b0b0b0", capsize=2, lw=1, label="data")
    ax.plot(xx, yhat, color=RUST, lw=2.3,
            label=fr"fit: $b={b:.2f}\pm{sb:.2f}$, $a={a:.2f}\pm{sa:.2f}$")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title(r"Least squares: $y=a+bx$  (true $a=2,\ b=3$)")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig2_least_squares.svg")
    caps["fig2_least_squares.svg"] = (
        "Ordinary least-squares fit from least_squares_line to noisy data $y=2+3x$ "
        "(Gaussian noise $\\sigma=0.7$). The routine returns the slope and intercept "
        "with $1\\sigma$ uncertainties; the shaded region is the $\\pm1\\sigma$ confidence "
        "band $s\\sqrt{1/n+(x-\\bar x)^2/S_{xx}}$ for the fitted line, tightest at the "
        "data's centroid. Recovered slope and intercept match the truth within error.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
