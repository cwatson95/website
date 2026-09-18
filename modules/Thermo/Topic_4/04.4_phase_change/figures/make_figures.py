"""Module 4.4 figures — the lever rule that makes every two-phase property linear
in quality, and the reason a half-evaporated tank still looks almost empty.

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
from phase_change import (                        # noqa: E402
    quality, mixture_property, quality_from_property, latent_heat,
    liquid_volume_fraction,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

# Saturated water at p = 10 bar  [Moran 8e, Table A-3].
VF, VG = 1.1273e-3, 0.19444                        # m^3/kg
HF, HG = 762.81, 2778.1                            # kJ/kg
SF, SG = 2.1387, 6.5865                            # kJ/kg.K


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the lever rule.  Every specific property of a two-phase mixture is
    # the same straight line in x once it is scaled to its own f-to-g span, so
    # v, h and s all collapse onto the diagonal.  That collapse is what lets one
    # measured property fix the quality (quality_from_property).
    x = np.linspace(0.0, 1.0, 200)
    curves = (
        (r"specific volume $v$", VF, VG, INK, "-", "o"),
        (r"enthalpy $h$", HF, HG, FLOW, "--", "s"),
        (r"entropy $s$", SF, SG, ALT, ":", "^"),
    )

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(x, x, color="0.78", lw=6, solid_capstyle="round", zorder=1,
            label=r"the lever rule  $(y-y_f)/y_{fg}=x$")
    for lab, yf, yg, c, ls, mk in curves:
        y = np.array([mixture_property(yf, yg, xi) for xi in x])
        ax.plot(x[::14], ((y - yf) / (yg - yf))[::14], ls="none", marker=mk,
                ms=7, mfc="white", mec=c, mew=1.7, label=lab, zorder=3)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel(r"quality $x=m_{vapour}/m_{total}$")
    ax.set_ylabel(r"position across the dome")
    ax.set_title(r"Every two-phase property is linear in quality")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_lever_rule.svg")
    caps["fig1_lever_rule.svg"] = (
        r"Inside the dome the mixture is just a mass-weighted blend of saturated "
        r"liquid and saturated vapour, so $y=y_f+x\,y_{fg}$ for EVERY specific "
        r"property (mixture_property). Scaling each by its own $f\!-\!g$ span, "
        r"the specific volume, enthalpy and entropy of water at 10 bar all land "
        r"on the same diagonal. This is the lever rule, and it is what makes the "
        r"tables usable: measure any one property, invert the line "
        r"(quality_from_property), and every other property follows. The latent "
        r"heat here is " + "%.0f" % latent_heat(HF, HG) + r" kJ/kg.")

    # Fig 2 — the counter-intuitive one.  Mass and volume are wildly different
    # book-keepings, because a kilogram of vapour occupies ~173x a kilogram of
    # liquid.  A tank half evaporated BY MASS is still ~99.4% liquid by volume.
    x2 = np.linspace(1e-4, 1.0, 500)
    liq = np.array([liquid_volume_fraction(xi, VF, VG) for xi in x2])

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot(x2, 100 * liq, color=INK, lw=2.4, label=r"liquid share of the VOLUME")
    ax.plot(x2, 100 * (1 - x2), color=FLOW, lw=2.0, ls="--",
            label=r"liquid share of the MASS  ($1-x$)")
    ax.plot([0.5], [100 * liquid_volume_fraction(0.5, VF, VG)], marker="o",
            ms=8, mfc="white", mec=ALT, mew=1.8, ls="none")
    ax.annotate(r"half the mass boiled off," "\n"
                r"still %.1f%% liquid by volume"
                % (100 * liquid_volume_fraction(0.5, VF, VG)),
                xy=(0.5, 100 * liquid_volume_fraction(0.5, VF, VG)),
                xytext=(0.20, 24), fontsize=9, color="0.3",
                arrowprops=dict(arrowstyle="->", color="0.5", lw=1.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 100)
    ax.set_xlabel(r"quality $x$  (vapour fraction BY MASS)")
    ax.set_ylabel(r"liquid fraction (%)")
    ax.set_title(r"Mass and volume tell completely different stories")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_liquid_volume_fraction.svg")
    caps["fig2_liquid_volume_fraction.svg"] = (
        r"Quality is a MASS fraction, and at 10 bar a kilogram of steam occupies "
        + "%.0f" % (VG / VF) + r" times the volume of a kilogram of water. The "
        r"consequence (liquid_volume_fraction) is that the two book-keepings "
        r"diverge violently: a vessel that is half evaporated by mass is still "
        + "%.1f" % (100 * liquid_volume_fraction(0.5, VF, VG)) + r"% liquid by "
        r"volume, and the sight-glass barely moves until the quality is close "
        r"to 1. Reading a level gauge as if it showed quality is a classic error; "
        r"the module's quality() takes masses precisely to keep the distinction "
        r"explicit.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
