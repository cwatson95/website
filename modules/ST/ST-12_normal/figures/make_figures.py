"""ST-12 figures — the normal pdf with the 68-95-99.7 rule, and standardization.

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
from normal import (                               # noqa: E402
    normal_pdf, standard_normal_pdf, standardize, empirical_rule,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — standard normal with nested 68-95-99.7 bands from empirical_rule.
    z = np.linspace(-4.0, 4.0, 800)
    phi = standard_normal_pdf(z)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(z, phi, color=INK, lw=2)
    for k, col in [(3, "#cdd6df"), (2, "#9bb0c2"), (1, STEEL)]:   # widest band first
        m = (z >= -k) & (z <= k)
        pct = 100.0 * empirical_rule(k)
        ax.fill_between(z[m], phi[m], color=col, label=fr"$|z|\leq{k}$:  {pct:.1f}%")
    ax.set_xlabel(r"$z=(x-\mu)/\sigma$"); ax.set_ylabel(r"$\phi(z)$")
    ax.set_title(r"Standard normal and the 68--95--99.7 rule")
    ax.legend(frameon=False, loc="upper right")
    _save(fig, "fig1_empirical_rule.svg")
    caps["fig1_empirical_rule.svg"] = (
        "The standard normal density phi(z) with the central bands |z|<=1, 2, 3 "
        "shaded. Their areas, from empirical_rule, are about 68.3%, 95.4%, and "
        "99.7% -- the fraction of a normal population within k standard deviations.")

    # Fig 2 — standardization: different N(mu,sigma^2) collapse onto phi(z).
    params = [(0.0, 1.0, INK), (2.0, 1.5, FLOW), (-1.0, 0.7, ALT)]
    xx = np.linspace(-6.0, 8.0, 800)
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(6.2, 3.5))
    for mu, sig, col in params:
        axL.plot(xx, normal_pdf(xx, mu, sig), color=col, lw=2,
                 label=fr"$\mu={mu:.0f},\ \sigma={sig}$")
    axL.set_title("Different normals"); axL.set_xlabel("$x$"); axL.set_ylabel("$f(x)$")
    axL.legend(frameon=False, fontsize=8)
    zz = np.linspace(-4.0, 4.0, 400)
    axR.plot(zz, standard_normal_pdf(zz), color="k", lw=4, alpha=0.25,
             label=r"$\phi(z)$")
    for mu, sig, col in params:
        zc = standardize(xx, mu, sig)
        axR.plot(zc, sig * normal_pdf(xx, mu, sig), color=col, lw=1.5, ls="--")
    axR.set_xlim(-4.0, 4.0)
    axR.set_title(r"Standardized  $Z=\frac{X-\mu}{\sigma}$")
    axR.set_xlabel("$z$"); axR.set_ylabel(r"$\phi(z)$")
    axR.legend(frameon=False)
    fig.tight_layout()
    _save(fig, "fig2_standardization.svg")
    caps["fig2_standardization.svg"] = (
        "Left: three normals with different mu and sigma (from normal_pdf). Right: "
        "after the z-score z=(x-mu)/sigma from standardize, each density (scaled by "
        "sigma) lands exactly on the single standard normal phi(z) shown in grey.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
