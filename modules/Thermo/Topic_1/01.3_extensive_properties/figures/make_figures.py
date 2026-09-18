"""Module 1.3 figures — extensive properties scale with extent (they collapse onto
one straight line through the origin) and they add over subsystems.

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
from extensive import (                           # noqa: E402
    total, scales_with_extent, is_additive, volume, internal_energy,
    kinetic_energy,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — take k identical units and ask what each property does.  V, U and
    # KE have different units and wildly different magnitudes, so plotting them
    # raw would need two axes (never do that); instead each is divided by its
    # own one-unit value.  Every extensive property then collapses onto the SAME
    # line X(k)/X(1) = k -- which is the definition of extensive.
    m1, v1, u1, V_speed = 2.0, 0.5, 300.0, 10.0    # one unit: kg, m^3/kg, kJ/kg, m/s
    k = np.arange(1, 9)
    ratios = {
        r"volume $V=mv$": [scales_with_extent(volume(m1, v1), int(kk)) / volume(m1, v1) for kk in k],
        r"internal energy $U=mu$": [scales_with_extent(internal_energy(m1, u1), int(kk)) / internal_energy(m1, u1) for kk in k],
        r"kinetic energy $\frac{1}{2}mV^2$": [scales_with_extent(kinetic_energy(m1, V_speed), int(kk)) / kinetic_energy(m1, V_speed) for kk in k],
    }

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(k, k, color="0.75", lw=6, solid_capstyle="round", zorder=1,
            label=r"the extensive law  $X(k)/X(1)=k$")
    for (lab, y), c, mk in zip(ratios.items(), (INK, FLOW, ALT), ("o", "s", "^")):
        ax.plot(k, y, ls="none", marker=mk, ms=7, mfc="white", mec=c, mew=1.7,
                label=lab, zorder=3)
    ax.set_xlabel(r"number of identical units  $k$")
    ax.set_ylabel(r"$X(k)\,/\,X(1)$")
    ax.set_title(r"Extensive properties scale with the amount of substance")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_extensive_scaling.svg")
    caps["fig1_extensive_scaling.svg"] = (
        r"What makes a property *extensive*: double the system and you double the "
        r"property. Volume, internal energy and kinetic energy carry different "
        r"units and magnitudes, so each is divided by its own one-unit value "
        r"(scales_with_extent) — and all three then land exactly on the line "
        r"$X(k)/X(1)=k$. The collapse is the content of the definition: an "
        r"extensive property has no meaning without saying how much substance "
        r"there is. Contrast module 1.4, where the same rescaling leaves the "
        r"intensive properties flat at 1.")

    # Fig 2 — additivity.  Three unequal subsystems; the extensive total is just
    # the sum (total / is_additive).  Bars carry a 2px surface gap so adjacent
    # segments read as separate marks.
    masses = [3.0, 5.0, 2.0]
    specific_v = 0.8                                # m^3/kg, same substance
    parts = [volume(m, specific_v) for m in masses]
    whole = total(parts)
    ok = is_additive(parts, whole)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    labels = ["part A\n3 kg", "part B\n5 kg", "part C\n2 kg", "whole\n10 kg"]
    vals = parts + [whole]
    cols = [INK, FLOW, ALT, "0.55"]
    bars = ax.bar(range(4), vals, width=0.62, color=cols, linewidth=2,
                  edgecolor="white")
    for b, val in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, val + 0.15, "%.1f" % val,
                ha="center", fontsize=9.5, color="0.25")
    ax.axvline(2.5, color="0.8", lw=1.0, ls="--")
    ax.set_xticks(range(4))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel(r"volume $V=mv$  (m$^3$)")
    ax.set_ylim(0, 9.6)
    ax.set_title(r"Additivity: $\sum_i V_i = V_{whole}$  (is_additive $\rightarrow$ %s)" % ok)
    ax.grid(alpha=0.25, lw=0.6, axis="y")
    _save(fig, "fig2_additivity.svg")
    caps["fig2_additivity.svg"] = (
        r"The operational test for extensivity (is_additive): cut the system into "
        r"parts, evaluate the property on each, and check that the pieces sum to "
        r"the whole. Three subsystems of the same substance ($v=0.8$ m$^3$/kg) "
        r"holding 3, 5 and 2 kg contribute 2.4, 4.0 and 1.6 m$^3$, summing "
        r"exactly to the 8.0 m$^3$ of the combined 10 kg system. Mass, volume, "
        r"energy and entropy all pass this test; temperature and pressure do not, "
        r"which is precisely why they are classified as intensive instead.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
