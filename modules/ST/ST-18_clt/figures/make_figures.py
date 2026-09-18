"""ST-18 figures — the central limit theorem: the standardized distribution of a
sum of iid terms converging to the standard normal as n grows (from a clearly
non-normal parent), and the cdf gap to Phi shrinking like 1/sqrt(n).

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
from clt import (                                  # noqa: E402
    die_pmf, nfold_pmf, pmf_mean, pmf_var, standard_normal_pdf,
    clt_cdf_max_error, kolmogorov_cdf_error, berry_esseen_bound,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    die = die_pmf()                                  # parent: flat U{1,...,6}, non-normal

    # Fig 1 — standardized distribution of S_n = X_1+...+X_n (n-fold convolution of
    # the parent), overlaid for several n against the standard-normal density.
    zg = np.linspace(-4.0, 4.0, 400)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(zg, standard_normal_pdf(zg), color=INK, lw=2.4, zorder=5,
            label=r"$N(0,1)$ limit")
    cols = [STEEL, "#7a8a4a", ALT, FLOW]
    for n, col in zip((1, 2, 4, 16), cols):
        conv = nfold_pmf(die, n)                      # exact pmf of the sum
        mu_n = pmf_mean(conv)
        sd_n = math.sqrt(pmf_var(conv))
        k = np.arange(len(conv))
        keep = conv > 1e-5
        z = (k[keep] - mu_n) / sd_n
        dens = conv[keep] * sd_n                      # lattice pmf -> density in z
        ax.plot(z, dens, color=col, lw=1.6, marker="o", ms=3, alpha=0.9,
                label=fr"$n={n}$")
    ax.set_xlim(-4, 4); ax.set_xlabel(r"standardized sum $z$")
    ax.set_ylabel("density")
    ax.set_title(r"CLT: standardized $S_n$ converges to $N(0,1)$ "
                 r"(parent: fair die)")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_clt_convergence.svg")
    caps["fig1_clt_convergence.svg"] = (
        "Starting from a clearly non-normal parent (a flat fair die), the exact "
        "standardized distribution of the sum S_n is obtained by n-fold convolution and "
        "overlaid for n=1,2,4,16. As n grows the lattice distribution converges to the "
        "standard normal density (thick curve).")

    # Fig 2 — the convergence made quantitative: max |cdf - Phi| vs n, on log-log,
    # with the Berry-Esseen bound; everything decays like 1/sqrt(n).
    ns = np.array([1, 2, 4, 8, 16, 32, 64])
    err_kol = np.array([kolmogorov_cdf_error(die, int(n)) for n in ns])
    err_cc = np.array([clt_cdf_max_error(die, int(n)) for n in ns])
    bound = np.array([berry_esseen_bound(die, int(n)) for n in ns])
    ref = err_kol[0] / np.sqrt(ns)                    # 1/sqrt(n) guide

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.loglog(ns, bound, color=ALT, lw=2, ls="--", marker="s", ms=4,
              label="Berry-Esseen bound")
    ax.loglog(ns, err_kol, color=FLOW, lw=2, marker="o", ms=5,
              label="max cdf gap to $\\Phi$")
    ax.loglog(ns, err_cc, color=STEEL, lw=2, marker="^", ms=5,
              label="with continuity correction")
    ax.loglog(ns, ref, color="#999999", lw=1.3, ls=":",
              label=r"$\propto 1/\sqrt{n}$")
    ax.set_xlabel("sample size $n$"); ax.set_ylabel("Kolmogorov error")
    ax.set_title(r"Convergence rate of the CLT: error $\sim 1/\sqrt{n}$")
    ax.legend(loc="lower left", frameon=False, fontsize=9)
    _save(fig, "fig2_convergence_rate.svg")
    caps["fig2_convergence_rate.svg"] = (
        "The largest gap between the standardized cdf of S_n and the normal cdf Phi, "
        "plotted against n on log-log axes for the fair die. The error sits under the "
        "Berry-Esseen bound and decays like 1/sqrt(n); the continuity correction lowers "
        "it further.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
