"""RE-04 figures — gamma(beta) diverging at c (with the reciprocal length factor),
and a moving-clock / moving-rod comparison: dilated ticks, contracted rods.

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
from sr_effects import (                           # noqa: E402
    gamma, time_dilation, length_contraction,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — one gamma stretches time (gamma -> inf) and shrinks length (1/gamma
    # -> 0); both from the module, diverging / vanishing at beta = 1.
    beta = np.linspace(0.0, 0.995, 400)
    g = np.array([gamma(b) for b in beta])
    inv_g = np.array([length_contraction(1.0, b) for b in beta])     # = 1/gamma
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(beta, g, color=INK, lw=2, label=r"time dilation  $\gamma=\Delta t/\Delta\tau$")
    ax.plot(beta, inv_g, color=FLOW, lw=2,
            label=r"length contraction  $1/\gamma=L/L_{0}$")
    ax.axvline(1.0, color=ALT, lw=1.2, ls="--", label="speed of light $\\beta=1$")
    ax.axhline(1.0, color="#cccccc", lw=0.6)
    ax.set_xlim(0, 1.02); ax.set_ylim(0, 8)
    ax.set_xlabel(r"speed $\beta=v/c$"); ax.set_ylabel("factor")
    ax.set_title(r"One $\gamma$: time stretches, length shrinks, diverging at $c$")
    ax.legend(loc="upper left", frameon=False)
    _save(fig, "fig1_gamma_vs_beta.svg")
    caps["fig1_gamma_vs_beta.svg"] = (
        "The Lorentz factor gamma(beta) (blue) climbs from 1 and diverges as beta -> 1, "
        "while the length factor 1/gamma = L/L0 (orange) falls to zero — the same gamma "
        "that dilates a moving clock's ticks contracts a moving rod. Both effects are "
        "negligible until beta is an appreciable fraction of c.")

    # Fig 2 — concrete comparison at several speeds: a rest-length-1 rod contracts,
    # a proper-1 clock interval dilates, via length_contraction / time_dilation.
    betas = [0.0, 0.5, 0.8, 0.95]
    rods = [length_contraction(1.0, b) for b in betas]
    ticks = [time_dilation(1.0, b) for b in betas]
    y = np.arange(len(betas))
    fig, (axR, axC) = plt.subplots(1, 2, figsize=(6.2, 3.5), sharey=True)
    axR.barh(y, [1.0] * len(betas), color="#e7e7ef", height=0.6)   # rest length ref
    axR.barh(y, rods, color=FLOW, height=0.6)
    for yi, L in zip(y, rods):
        axR.text(L + 0.03, yi, "%.2f" % L, va="center", fontsize=9, color=INK)
    axR.set_title(r"rod  $L=L_{0}/\gamma$  ($L_{0}=1$)")
    axR.set_xlabel("length"); axR.set_xlim(0, 1.15)
    axC.barh(y, ticks, color=INK, height=0.6)
    for yi, T in zip(y, ticks):
        axC.text(T + 0.08, yi, "%.2f" % T, va="center", fontsize=9, color=INK)
    axC.set_title(r"clock  $\Delta t=\gamma\,\Delta\tau$  ($\Delta\tau=1$)")
    axC.set_xlabel("time"); axC.set_xlim(0, 3.6)
    axR.set_yticks(y); axR.set_yticklabels([r"$\beta=%.2f$" % b for b in betas])
    fig.suptitle("Moving rods shorten, moving clocks slow — by the same $\\gamma$")
    _save(fig, "fig2_rod_clock_comparison.svg")
    caps["fig2_rod_clock_comparison.svg"] = (
        "At beta = 0, 0.5, 0.8, 0.95: a rod of rest length 1 (orange, left) contracts to "
        "L0/gamma against its full-length reference, while a clock interval of proper time "
        "1 (blue, right) dilates to gamma. As beta -> c the rod collapses toward 0 and the "
        "tick stretches without bound, both governed by the single factor gamma.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
