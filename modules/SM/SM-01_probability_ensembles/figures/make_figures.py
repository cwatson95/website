"""SM-01 figures — the two-state macrostate distribution sharpening toward a
delta, and the 1/sqrt(N) fractional width that makes thermodynamics deterministic.

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
from probability_ensembles import (               # noqa: E402
    two_state_probability, gaussian_approx_two_state, fractional_width,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — P(N,n) for a fair two-state system (two_state_probability) plotted as
    # a density in the fraction x=n/N for growing N: the peak at x=1/2 narrows
    # toward a delta, and the de Moivre-Laplace Gaussian (gaussian_approx_two_state)
    # tracks it.  Density in x is N * (probability mass in n).
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for N, col in [(16, STEEL), (64, FLOW), (256, INK)]:
        n = np.arange(N + 1)
        x = n / N
        pmf = np.array([two_state_probability(N, int(k)) for k in n])
        gss = np.array([gaussian_approx_two_state(N, int(k)) for k in n])
        ax.plot(x, N * pmf, ls="none", marker="o", ms=3.5, color=col,
                label=fr"$N={N}$  ($\sigma/\langle n\rangle={fractional_width(N):.3f}$)")
        ax.plot(x, N * gss, color=col, lw=1.5, alpha=0.9)
    ax.axvline(0.5, color="#aaaaaa", lw=0.8, ls=":")
    ax.set_xlim(0.0, 1.0)
    ax.set_xlabel(r"fraction up  $x=n/N$")
    ax.set_ylabel(r"probability density in $x$")
    ax.set_title(r"Two-state macrostate peak sharpens at $x=\frac{1}{2}$ as $N$ grows")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_macrostate_distribution.svg")
    caps["fig1_macrostate_distribution.svg"] = (
        r"Macrostate distribution of a fair two-state system from "
        r"two_state_probability$(N,n)=\binom{N}{n}/2^N$, shown as a density in the "
        r"fraction $x=n/N$ for $N=16,64,256$ (dots), with the de Moivre-Laplace "
        r"Gaussian gaussian_approx_two_state (lines) tracking it. As $N$ grows the "
        r"peak at $x=\tfrac12$ grows taller and narrower — collapsing toward a delta "
        r"function — the microscopic root of a sharp thermodynamic limit.")

    # Fig 2 — the fractional width sigma/<n> = 1/sqrt(N) (fractional_width): the
    # relative fluctuation that vanishes in the thermodynamic limit.
    N = np.logspace(1, 24, 200)
    w = np.array([fractional_width(float(n)) for n in N])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(N, w, color=INK, lw=2.2, label=r"$\sigma/\langle n\rangle=1/\sqrt{N}$")
    for n0, col, lab in [(1e2, STEEL, r"$N=10^{2}$"),
                         (1e6, FLOW, r"$N=10^{6}$"),
                         (1e23, ALT, r"$N\sim10^{23}$")]:
        ax.plot([n0], [fractional_width(n0)], "o", ms=7, color=col)
        ax.annotate(lab + fr"  ($={fractional_width(n0):.0e}$)",
                    xy=(n0, fractional_width(n0)),
                    xytext=(n0 * 0.04, fractional_width(n0) * 6),
                    color=col, fontsize=8.5,
                    arrowprops=dict(arrowstyle="->", color=col, lw=1.0))
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel(r"number of elements $N$")
    ax.set_ylabel(r"fractional width $\sigma/\langle n\rangle$")
    ax.set_title(r"Why thermodynamics is deterministic: relative width $\to0$ as $1/\sqrt{N}$")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_fractional_width.svg")
    caps["fig2_fractional_width.svg"] = (
        r"Relative fluctuation of the two-state macrostate from fractional_width: "
        r"$\sigma/\langle n\rangle=1/\sqrt{N}$, a line of slope $-\tfrac12$ on "
        r"log-log axes. It is $10\%$ at $N=10^2$ but only $\sim3\times10^{-12}$ at "
        r"$N\sim10^{23}$ — at macroscopic particle number the macrostate is "
        r"effectively certain, which is exactly why thermodynamics looks "
        r"deterministic.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
