"""Module 2.6 figures — gravitational potential energy is linear in height, and the
choice of datum cancels out of every physically meaningful answer.

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
from potential_energy import (                    # noqa: E402
    G, potential_energy, delta_PE, work_by_gravity,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — PE = mgz is a straight line through the datum; the slope is mg.
    z = np.linspace(0.0, 50.0, 200)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for m, c, ls in ((50.0, INK, "-"), (200.0, FLOW, "--"), (1000.0, ALT, ":")):
        PE = np.array([potential_energy(m, zi) for zi in z]) / 1000.0   # kJ
        ax.plot(z, PE, color=c, lw=2.1, ls=ls, label=r"$m=%d$ kg" % m)
    ax.set_xlim(0, 50)
    ax.set_xlabel(r"elevation above the datum $z$ (m)")
    ax.set_ylabel(r"potential energy $mgz$ (kJ)")
    ax.set_title(r"Potential energy is linear in height; the slope is $mg$")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_pe_vs_height.svg")
    caps["fig1_pe_vs_height.svg"] = (
        r"$PE=mgz$ (potential_energy, $g=" + "%.2f" % G + r"$ m/s$^2$) for three "
        r"masses. Each is a straight line whose slope is the weight $mg$, so "
        r"lifting a 1000 kg mass 50 m stores "
        + "%.0f" % (potential_energy(1000.0, 50.0) / 1000.0) + r" kJ. Compared "
        r"with the internal energy of the same mass of working fluid this is "
        r"tiny, which is why $\Delta$PE is dropped from most closed-system "
        r"balances — but it is the entire operating principle of a "
        r"pumped-storage power station.")

    # Fig 2 — the datum is arbitrary.  Three different choices of z = 0 shift the
    # whole PE line up or down, yet the physically meaningful quantity, the
    # CHANGE over a given drop, is identical for all three.
    m = 200.0
    z_abs = np.linspace(0.0, 50.0, 200)
    z_a, z_b = 40.0, 10.0                          # the body falls 40 m -> 10 m
    dPE = delta_PE(m, z_a, z_b)
    W_grav = work_by_gravity(m, z_a, z_b)

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    for datum, c, ls in ((0.0, INK, "-"), (10.0, FLOW, "--"), (25.0, ALT, ":")):
        PE = np.array([potential_energy(m, zi - datum) for zi in z_abs]) / 1000.0
        ax.plot(z_abs, PE, color=c, lw=2.0, ls=ls,
                label=r"datum at $z=%d$ m" % datum)
    for zz in (z_a, z_b):
        ax.axvline(zz, color="0.75", lw=0.9, ls=":")
    ax.annotate("", xy=(z_b, -30), xytext=(z_a, -30),
                arrowprops=dict(arrowstyle="->", color="0.3", lw=1.4))
    ax.text(0.5 * (z_a + z_b), -27, r"a 30 m fall", ha="center", fontsize=9,
            color="0.3")
    ax.text(0.5 * (z_a + z_b), -45,
            r"$\Delta PE=%.1f$ kJ for every datum" % (dPE / 1000.0),
            ha="center", fontsize=9.5, color="0.2")
    ax.set_xlim(0, 50)
    ax.set_xlabel(r"height above ground $z$ (m)")
    ax.set_ylabel(r"potential energy (kJ)")
    ax.set_title(r"The datum is a bookkeeping choice; $\Delta PE$ is not")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_datum_independence.svg")
    caps["fig2_datum_independence.svg"] = (
        r"Potential energy has no absolute value — only differences are physical. "
        r"Moving the datum shifts the entire $mgz$ line vertically, so the three "
        r"choices disagree completely about how much potential energy a 200 kg "
        r"body 'has'. They agree exactly about what matters: a 30 m fall changes "
        r"it by " + "%.1f" % (dPE / 1000.0) + r" kJ (delta_PE) whatever the "
        r"datum, and gravity does " + "%.1f" % (W_grav / 1000.0) + r" kJ of work "
        r"on the body (work_by_gravity $=-\Delta PE$). Pick any datum; just keep "
        r"it fixed for the whole problem.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
