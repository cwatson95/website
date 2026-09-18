"""Module 4.2 figures — ideal-gas entropy change under heating and compression, and
the entropy produced when two blocks at different temperatures are joined.

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
from entropy import (                             # noqa: E402
    entropy_change_ideal_gas_cp, entropy_change_incompressible,
    heat_isothermal_rev, process_allowed,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

CP_AIR, R_AIR = 1.005, 0.287                       # kJ/kg.K


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the two competing terms of ds = cp ln(T2/T1) - R ln(p2/p1).
    # Heating raises entropy; compressing lowers it.  Where a curve crosses zero
    # the two exactly balance -- that locus is an isentropic process.
    T2 = np.linspace(300.0, 900.0, 300)
    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    for pr, c, ls in ((1.0, INK, "-"), (5.0, FLOW, "--"), (20.0, ALT, ":")):
        ds = np.array([entropy_change_ideal_gas_cp(CP_AIR, R_AIR, 300.0, t, 1.0, pr)
                       for t in T2])
        ax.plot(T2, ds, color=c, lw=2.1, ls=ls, label=r"$p_2/p_1=%g$" % pr)
    ax.axhline(0.0, color="0.6", lw=1.1, ls="-.")
    ax.text(880, 0.02, "isentropic", ha="right", fontsize=9, color="0.4")
    ax.set_xlim(300, 900)
    ax.set_xlabel(r"final temperature $T_2$ (K)    (from $T_1=300$ K)")
    ax.set_ylabel(r"$s_2-s_1$ (kJ/kg$\cdot$K)")
    ax.set_title(r"Ideal gas: $\Delta s=c_p\ln(T_2/T_1)-R\ln(p_2/p_1)$")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_ideal_gas_entropy.svg")
    caps["fig1_ideal_gas_entropy.svg"] = (
        r"Entropy change of air between two states "
        r"(entropy_change_ideal_gas_cp, constant $c_p$). The temperature term "
        r"$c_p\ln(T_2/T_1)$ pushes entropy up, the pressure term $-R\ln(p_2/p_1)$ "
        r"pulls it down, and a compression can therefore cancel a heating "
        r"exactly. Each curve crosses zero at the temperature that makes the "
        r"process isentropic — for a 20:1 pressure ratio that is about "
        + "%.0f" % (300.0 * (20.0 ** (R_AIR / CP_AIR))) + r" K, which is why "
        r"compressors deliver hot air. Entropy is a property here: the change "
        r"depends only on the end states, not on how the gas got there.")

    # Fig 2 — the irreversibility.  Two identical blocks at Th and Tc are put in
    # contact and settle at the mean; the entropy the hot one loses is smaller
    # than the entropy the cold one gains, so sigma > 0 and grows with the gap.
    m, c_blk = 1.0, 0.45                            # kg, kJ/kg.K (steel)
    T_mean = 400.0
    # the 2nd law only permits sigma >= 0; Q = T dS is its isothermal companion
    assert process_allowed(0.0) and heat_isothermal_rev(400.0, 0.5) == 200.0
    gap = np.linspace(0.0, 300.0, 300)
    sigma = []
    for g in gap:
        Th, Tc = T_mean + g / 2, T_mean - g / 2
        Tf = 0.5 * (Th + Tc)
        s = (m * entropy_change_incompressible(c_blk, Th, Tf)
             + m * entropy_change_incompressible(c_blk, Tc, Tf))
        sigma.append(s)
    sigma = np.array(sigma)

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(gap, sigma, color=INK, lw=2.4,
            label=r"$\sigma=mc\,\ln[\,T_f^2/(T_hT_c)\,]$")
    ax.fill_between(gap, 0, sigma, color=INK, alpha=0.10, lw=0)
    ax.axhline(0.0, color="0.6", lw=1.0)
    ax.plot([0], [0], marker="o", ms=8, mfc="white", mec=FLOW, mew=1.8,
            ls="none", label=r"reversible limit: $\sigma=0$ only at $\Delta T=0$")
    ax.set_xlim(0, 300)
    ax.set_xlabel(r"initial temperature gap $T_h-T_c$ (K)   (mean fixed at 400 K)")
    ax.set_ylabel(r"entropy produced $\sigma$ (kJ/K)")
    ax.set_title(r"Joining two blocks always produces entropy")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_entropy_production.svg")
    caps["fig2_entropy_production.svg"] = (
        r"Two 1 kg steel blocks whose temperatures average 400 K are placed in "
        r"contact and reach a common final temperature. Summing "
        r"entropy_change_incompressible over both, the hot block's entropy loss "
        r"never quite matches the cold block's gain: the surplus $\sigma$ is "
        r"entropy PRODUCED, and it is positive for every non-zero gap — "
        + "%.4f" % sigma[-1] + r" kJ/K for a 300 K difference. It vanishes only "
        r"in the limit of an infinitesimal gap, the reversible idealization. "
        r"process_allowed enforces the sign, and heat_isothermal_rev supplies the "
        r"$Q=T\Delta S$ companion for the isothermal case.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
