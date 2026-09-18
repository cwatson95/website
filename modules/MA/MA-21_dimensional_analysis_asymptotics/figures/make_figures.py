"""MA-21 figures — Buckingham-Pi data collapse & optimal truncation of a divergent series.

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
from asymptotics import (                          # noqa: E402
    buckingham_pi, is_dimensionless, optimal_truncation,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — Buckingham Pi: the one dimensionless group collapses all the data.
    # Pendulum {period T, length L, gravity g, mass m} over base dims (M, L, T).
    # buckingham_pi returns the single null vector of the dimension matrix; rescaled
    # so the period exponent is 2 it is (T,L,g,m) = (2,-1,1,0), i.e. Pi = g T^2 / L.
    # The small-angle law the notes derive, T = 2*pi*sqrt(L/g), then forces this
    # group to the SAME constant 4*pi^2 on every planet — the data collapse.
    D = [[0, 0, 0, 1],          # Mass
         [0, 1, 1, 0],          # Length
         [1, 0, -2, 0]]         # Time   (cols: T_period, L, g, m)
    p = buckingham_pi(D)[0]
    p = [e * (2.0 / p[0]) for e in p]               # normalize period exponent -> 2
    assert is_dimensionless(D, p)                   # net dimension is zero
    eT, eL, eg, em = p                              # exponents of (T, L, g, m): (2,-1,1,0)

    L = np.linspace(0.2, 3.0, 220)
    worlds = [("Moon  $g=1.62$",   1.62,  STEEL),
              ("Earth  $g=9.81$",  9.81,  INK),
              ("Jupiter  $g=24.8$", 24.79, FLOW)]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.2, 4.8), sharex=True)
    for i, (name, g, c) in enumerate(worlds):
        T = 2.0 * np.pi * np.sqrt(L / g)            # small-angle pendulum period
        ax1.plot(L, T, color=c, lw=2, label=name)
        Pi = (T ** eT) * (L ** eL) * (g ** eg)      # the Buckingham group (m^0 drops out)
        ax2.plot(L, Pi, color=c, lw=1.6, marker="o", ms=4, markevery=(i * 14, 42))
    ax1.set_ylabel(r"period  $T$  (s)")
    ax1.set_title(r"Buckingham $\Pi$: one group collapses the pendulum data")
    ax1.legend(loc="upper left", frameon=False, fontsize=9)
    ax2.axhline(4.0 * np.pi ** 2, color="#888888", lw=0.9, ls=":")
    ax2.text(2.55, 4.0 * np.pi ** 2 + 3.0, r"$4\pi^2$", color="#555555", fontsize=11)
    ax2.set_ylim(0, 60)
    ax2.set_xlim(0.2, 3.0)
    ax2.set_xlabel(r"length  $L$  (m)")
    ax2.set_ylabel(r"$\Pi = g\,T^2/L$")
    _save(fig, "fig1_buckingham_collapse.svg")
    caps["fig1_buckingham_collapse.svg"] = (
        r"Buckingham $\Pi$ theorem in action. buckingham_pi returns the lone null "
        r"vector of the pendulum's dimension matrix, $(T,L,g,m)=(2,-1,1,0)$, so the "
        r"only dimensionless group is $\Pi=gT^2/L$. Top: the small-angle period "
        r"$T=2\pi\sqrt{L/g}$ gives wildly different curves on the Moon, Earth and "
        r"Jupiter. Bottom: forming $\Pi$ collapses all three onto the single constant "
        r"$4\pi^2$ — the period law $T\propto\sqrt{L/g}$ with no equation of motion solved.")

    # Fig 2 — optimal truncation of the DIVERGENT asymptotic series for g(x)=x e^x E_1(x):
    # g(x) ~ sum (-1)^k k!/x^k. optimal_truncation(x) returns the error |S_N(x)-g(x)|
    # at every order N; it bottoms out near N ~ x at ~the smallest term, then diverges.
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    for x, c in [(5.0, STEEL), (8.0, ALT), (12.0, FLOW)]:
        bN, bErr, errs = optimal_truncation(x, Nmax=40)
        N = np.arange(len(errs))
        ax.semilogy(N, errs, color=c, lw=1.8,
                    label=fr"$x={x:.0f}$:  best $N={bN}$, err $={bErr:.1e}$")
        ax.semilogy(bN, bErr, "o", ms=7, color=c, mec="white", mew=0.8)
        ax.axvline(x, color=c, lw=0.7, ls=":", alpha=0.7)
    ax.set_xlim(0, 40)
    ax.set_ylim(1e-6, 1e6)
    ax.set_xlabel(r"truncation order $N$")
    ax.set_ylabel(r"error  $|S_N(x)-g(x)|$")
    ax.set_title(r"Optimal truncation: error bottoms out near $N\approx x$, then diverges")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    _save(fig, "fig2_optimal_truncation.svg")
    caps["fig2_optimal_truncation.svg"] = (
        r"The divergent asymptotic series $g(x)=xe^xE_1(x)\sim\sum_k(-1)^k k!/x^k$ "
        r"evaluated by optimal_truncation. For each $x$ the error $|S_N-g|$ falls to a "
        r"minimum near $N\approx x$ (dots, dotted lines) — of order the smallest term "
        r"$\sim\sqrt{2\pi x}\,e^{-x}$ — then blows up as the $k!$ terms overwhelm $x^{-k}$. "
        r"Adding more terms makes it worse: the hallmark of an asymptotic (non-convergent) "
        r"series, and exactly how WKB and high-order perturbation theory behave.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
