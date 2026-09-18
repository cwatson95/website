"""CM-16 figures — coupled oscillations: the normal-mode shapes and frequencies of
a fixed-fixed mass chain, and the beating that arises when two near-degenerate
normal modes are superposed.

Imports the module's own code in ../code and renders two SVGs plus a captions.json
(matplotlib -> SVG with text as portable vector outlines, saved next to a
captions.json the browser shows under each figure).  Run:  python3 make_figures.py
"""
import json
import math
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
from normal_modes import normal_modes, mode_inner_product   # noqa: E402

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — normal-mode shapes of N equal masses on a fixed-fixed spring chain.
    N, k, m = 5, 1.0, 1.0
    K = [[(2 * k if i == j else (-k if abs(i - j) == 1 else 0.0)) for j in range(N)]
         for i in range(N)]
    M = [m] * N
    freqs, modes = normal_modes(K, M)
    sites = list(range(N + 2))                      # include the two fixed walls (zeros)
    cols = [INK, FLOW, ALT, STEEL, "#7a8b3a"]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    spacing = 1.7
    for n in range(N):
        shape = [0.0] + list(modes[n]) + [0.0]
        amp = max(abs(c) for c in shape) or 1.0
        disp = [s / amp + n * spacing for s in shape]
        off = n * spacing
        ax.axhline(off, color="#dddddd", lw=0.6)
        ax.plot(sites, disp, "-o", color=cols[n % len(cols)], lw=2, ms=4)
        ax.text(N + 1.15, off, r"$\omega=%.3f$" % freqs[n], va="center", color=cols[n % len(cols)])
    ax.set_xlim(-0.4, N + 2.1)
    ax.set_xlabel("mass index along the chain")
    ax.set_ylabel("mode shape (stacked, normalized)")
    ax.set_title("Normal modes of a fixed-fixed chain: shapes and frequencies")
    ax.set_yticks([])
    _save(fig, "fig1_mode_shapes.svg")
    caps["fig1_mode_shapes.svg"] = (
        "Normal-mode shapes of five equal masses on a fixed-fixed spring chain (k = m = 1), "
        "from normal_modes. Stacked low to high frequency, they are the discrete standing "
        "waves: the lowest mode has no internal node and each higher mode adds one.")

    # Fig 2 — beating: two equal masses, weak coupling, energy sloshing between them.
    kc = 0.06                                       # weak coupling spring
    K2 = [[k + kc, -kc], [-kc, k + kc]]
    M2 = [m, m]
    f2, v2 = normal_modes(K2, M2)
    x0 = [1.0, 0.0]                                 # displace mass 1, both at rest
    a = [mode_inner_product(M2, v2[n], x0) for n in range(2)]   # mass-orthonormal projection
    t = np.linspace(0.0, 170.0, 3000)
    x1 = sum(a[n] * v2[n][0] * np.cos(f2[n] * t) for n in range(2))
    x2 = sum(a[n] * v2[n][1] * np.cos(f2[n] * t) for n in range(2))
    env = np.abs(np.cos(0.5 * (f2[1] - f2[0]) * t))
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(t, x1, color=INK,  lw=1.6, label=r"$x_1(t)$")
    ax.plot(t, x2, color=FLOW, lw=1.6, label=r"$x_2(t)$")
    ax.plot(t,  env, color=ALT, lw=1.0, ls="--", label="beat envelope")
    ax.plot(t, -env, color=ALT, lw=1.0, ls="--")
    ax.set_xlabel("time $t$")
    ax.set_ylabel("displacement")
    ax.set_title("Beating: superposing two near-degenerate normal modes")
    ax.legend(loc="upper right", ncol=3, frameon=False)
    _save(fig, "fig2_beating.svg")
    caps["fig2_beating.svg"] = (
        "Two weakly coupled equal masses started with only mass 1 displaced. The state is "
        "decomposed onto the normal modes with mode_inner_product, so x1 and x2 are sums of "
        "cos(omega_n t): energy sloshes fully back and forth at the beat rate "
        "(omega_2 - omega_1)/2 (dashed envelope).")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
