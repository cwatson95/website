"""Module 2.7 figures — Archimedes: how deep a floating body sits, and how much
weight the fluid appears to take off a submerged one.

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
from buoyancy import (                            # noqa: E402
    G, buoyant_force, apparent_weight, floats, submerged_fraction,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the submerged fraction of a freely floating body is just the
    # density ratio, up to the point where it stops floating at all.
    rho_w = 1000.0
    ratio = np.linspace(0.0, 1.0, 200)
    frac = np.array([submerged_fraction(r * rho_w, rho_w) for r in ratio])

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(ratio, frac, color=INK, lw=2.3)
    ax.fill_between(ratio, frac, 1.0, color=STEEL, alpha=0.10, lw=0)
    ax.axvline(1.0, color=FLOW, lw=1.6, ls="--")
    assert floats(917.0, rho_w) and not floats(7850.0, rho_w)   # the predicate
    ax.text(1.005, 0.45, "floats $\\rightarrow$ False", rotation=90, color=FLOW,
            fontsize=9, va="center")
    for name, rho_o in (("cork", 240.0), ("oak", 750.0), ("ice", 917.0)):
        r = rho_o / rho_w
        ax.plot([r], [submerged_fraction(rho_o, rho_w)], marker="o", ms=7.5,
                mfc="white", mec=ALT, mew=1.8, ls="none", zorder=4)
        ax.annotate(name, xy=(r, submerged_fraction(rho_o, rho_w)),
                    xytext=(r - 0.02, submerged_fraction(rho_o, rho_w) + 0.09),
                    fontsize=9, color="0.3", ha="center")
    ax.set_xlim(0, 1.12)
    ax.set_ylim(0, 1.14)
    ax.set_xlabel(r"density ratio $\rho_{body}/\rho_{fluid}$")
    ax.set_ylabel(r"fraction of volume submerged")
    ax.set_title(r"A floating body sinks to exactly its density ratio")
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_submerged_fraction.svg")
    caps["fig1_submerged_fraction.svg"] = (
        r"For a freely floating body the buoyant force equals the weight, and the "
        r"submerged fraction reduces to the density ratio "
        r"$\rho_{body}/\rho_{fluid}$ (submerged_fraction). Ice at 917 kg/m$^3$ "
        r"therefore floats with " + "%.0f" % (100 * submerged_fraction(917.0, rho_w)) +
        r"% of its volume under water — the iceberg rule — while cork shows "
        r"three-quarters of itself above the surface. At a ratio of 1 the line "
        r"reaches full submersion and the body is neutrally buoyant; beyond it "
        r"(floats $\rightarrow$ False) there is no equilibrium and it sinks.")

    # Fig 2 — a fixed steel block weighed in fluids of increasing density.  The
    # apparent weight falls linearly, hitting zero when the fluid matches the
    # block's own density.
    V_obj = 0.010                                   # m^3
    rho_steel = 7850.0
    W_true = rho_steel * V_obj * G
    rho_f = np.linspace(0.0, 9000.0, 300)
    W_app = np.array([apparent_weight(W_true, r, V_obj) for r in rho_f])
    Fb_water = buoyant_force(rho_w, V_obj)

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(rho_f, W_app / 1000.0, color=INK, lw=2.3,
            label=r"apparent weight $W-\rho_f gV$")
    ax.axhline(0.0, color="0.7", lw=0.9)
    ax.axvline(rho_steel, color=FLOW, lw=1.5, ls="--",
               label=r"$\rho_f=\rho_{steel}$: neutrally buoyant")
    ax.plot([rho_w], [apparent_weight(W_true, rho_w, V_obj) / 1000.0],
            marker="o", ms=8, mfc="white", mec=ALT, mew=1.8, ls="none",
            label=r"in water: $-%.2f$ kN of relief" % (Fb_water / 1000.0))
    ax.set_xlim(0, 9000)
    ax.set_xlabel(r"fluid density $\rho_{fluid}$ (kg/m$^3$)")
    ax.set_ylabel(r"apparent weight (kN)")
    ax.set_title(r"Weighing a 10 L steel block in ever denser fluids")
    ax.legend(loc="lower left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_apparent_weight.svg")
    caps["fig2_apparent_weight.svg"] = (
        r"A 10 L steel block weighs "
        + "%.2f" % (W_true / 1000.0) + r" kN in vacuum. Immersed, the fluid "
        r"pushes back with $F_b=\rho_f gV$ (buoyant_force) and the scale reads "
        r"the difference (apparent_weight) — a straight line falling with fluid "
        r"density. Water removes only " + "%.2f" % (Fb_water / 1000.0) + r" kN, "
        r"about " + "%.0f" % (100 * Fb_water / W_true) + r"% of the weight; the "
        r"reading reaches zero exactly when the fluid density matches the block's "
        r"own, and a denser fluid than that would float it. This is the fluid-"
        r"statics leaf of the map — the mechanics trunk (CM) develops it further.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
