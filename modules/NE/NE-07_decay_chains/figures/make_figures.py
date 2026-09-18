"""NE-07 figures -- saturation under constant production, the parent/daughter
chain and its maximum, secular vs transient equilibrium, and the dating curve.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
"""
import json
import math
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
from decay_chains import (                         # noqa: E402
    SECONDS_PER, decay_constant, approach_fraction, two_component_chain,
    daughter_maximum_time, activity_ratio, carbon14_age,
    CARBON14_MODERN_DPM_PER_G, load_half_lives, bateman_number,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"
YEAR = SECONDS_PER["y"]


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    hl = load_half_lives()

    # Fig 1 -- saturation under constant production.
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    n = np.linspace(0, 8, 300)
    ax.plot(n, 1 - 2.0 ** (-n), color=INK, lw=1.9)
    ax.axhline(1.0, color="0.5", ls="--", lw=1.1)
    ax.text(5.6, 1.03, "saturation $N_e=Q_0/\\lambda$", fontsize=9, color="0.35")
    for k, lab in [(1, "50%"), (2, "75%"), (5, "96.9%")]:
        v = 1 - 2.0 ** -k
        ax.plot([k], [v], "o", color=FLOW, ms=6)
        ax.annotate(lab, xy=(k, v), xytext=(k + 0.25, v - 0.09), fontsize=9, color=FLOW)
    ax.set_xlabel("irradiation time (half-lives of the product)")
    ax.set_ylabel("$N/N_e$")
    ax.set_ylim(0, 1.12)
    ax.set_title("Activation saturates: irradiating longer buys nothing")
    _save(fig, "fig1_saturation.svg")
    caps["fig1_saturation.svg"] = (
        "Buildup toward saturation under constant production (approach_fraction). The "
        "activity can never exceed the production rate Q0, and five half-lives already "
        "reaches 97% of it -- the rule of thumb that sets irradiation times in activation "
        "analysis and isotope production.")

    # Fig 2 -- the two-component chain and its maximum (99Mo -> 99mTc).
    fig, ax = plt.subplots(figsize=(6.4, 3.7))
    l1 = decay_constant(66.0)
    l2 = decay_constant(6.01)
    t = np.linspace(0, 120, 500)
    n1 = np.array([two_component_chain(l1, l2, 1.0, x)[0] for x in t])
    n2 = np.array([two_component_chain(l1, l2, 1.0, x)[1] for x in t])
    ax.plot(t, l1 * n1, color=INK, lw=1.9, label=r"$^{99}$Mo activity (parent)")
    ax.plot(t, l2 * n2, color=FLOW, lw=1.9, label=r"$^{99{\rm m}}$Tc activity (daughter)")
    tmax = daughter_maximum_time(l1, l2)
    ax.axvline(tmax, color="0.55", ls=":", lw=1.2)
    ax.annotate("daughter peaks\nat %.1f h" % tmax, xy=(tmax, l2 * two_component_chain(l1, l2, 1.0, tmax)[1]),
                xytext=(tmax + 8, 0.062), fontsize=9, color="0.3",
                arrowprops=dict(arrowstyle="->", color="0.4"))
    ax.set_xlabel("time (hours)")
    ax.set_ylabel("activity (arbitrary units)")
    ax.set_title(r"Transient equilibrium: $^{99}$Mo $\to$ $^{99{\rm m}}$Tc")
    ax.legend(frameon=False, fontsize=9)
    _save(fig, "fig2_parent_daughter.svg")
    caps["fig2_parent_daughter.svg"] = (
        "Parent and daughter activities in the 99Mo/99mTc chain (two_component_chain). The "
        "daughter grows from zero, peaks at 22.9 h where production equals loss "
        "(daughter_maximum_time), and thereafter tracks the parent at 1.10 times its "
        "activity -- which is why a technetium generator is eluted about once a day.")

    # Fig 3 -- secular vs transient vs no equilibrium.
    fig, axes = plt.subplots(1, 3, figsize=(8.4, 2.9), sharey=True)
    cases = [(1000.0, 1.0, "secular\n$T_1/T_2=1000$", LEAF),
             (11.0, 1.0, "transient\n$T_1/T_2=11$", FLOW),
             (0.2, 1.0, "no equilibrium\n$T_1/T_2=0.2$", ALT)]
    for ax, (T1, T2, lab, col) in zip(axes, cases):
        l1, l2 = decay_constant(T1), decay_constant(T2)
        t = np.linspace(1e-3, 8, 400)
        n1 = np.array([two_component_chain(l1, l2, 1.0, x)[0] for x in t])
        n2 = np.array([two_component_chain(l1, l2, 1.0, x)[1] for x in t])
        ax.semilogy(t, l1 * n1, color=INK, lw=1.6, label="parent")
        ax.semilogy(t, l2 * n2, color=col, lw=1.8, label="daughter")
        ax.set_title(lab, fontsize=9.5)
        ax.set_xlabel("time / $T_2$")
        ax.set_ylim(1e-3, 3)
    axes[0].set_ylabel("activity")
    axes[0].legend(frameon=False, fontsize=8.5, loc="lower left")
    fig.suptitle("What happens depends only on the half-life ratio", y=1.04)
    _save(fig, "fig3_equilibrium_regimes.svg")
    caps["fig3_equilibrium_regimes.svg"] = (
        "Parent and daughter activities for three half-life ratios. With a very long-lived "
        "parent the two activities become equal (secular equilibrium); with a moderately "
        "long-lived parent the daughter settles at a fixed multiple above it (transient); "
        "with a short-lived parent no equilibrium is reached at all and the daughter simply "
        "outlives its supply.")

    # Fig 4 -- the radiocarbon dating curve.
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ages = np.linspace(0, 60000, 400)
    T14 = hl["14C"] / YEAR
    act = CARBON14_MODERN_DPM_PER_G * 2.0 ** (-ages / T14)
    ax.semilogy(ages, act, color=INK, lw=1.9)
    for a, lab in [(5700, "1 half-life"), (16606, "the P6 charcoal"),
                   (57000, "10 half-lives")]:
        v = CARBON14_MODERN_DPM_PER_G * 2.0 ** (-a / T14)
        ax.plot([a], [v], "o", color=FLOW, ms=6)
        ax.annotate("%s\n%.2f dpm/g" % (lab, v), xy=(a, v), xytext=(a - 2000, v * 0.25),
                    fontsize=8.5, color=FLOW, ha="center")
    ax.axhspan(1e-3, 0.05, color="0.88", zorder=0)
    ax.text(30000, 0.012, "lost in background", fontsize=9, color="0.35")
    ax.set_xlabel("age (years)")
    ax.set_ylabel("$^{14}$C activity (dpm per gram carbon)")
    ax.set_ylim(3e-3, 30)
    ax.set_title("Radiocarbon: why the method stops near 50 000 years")
    _save(fig, "fig4_radiocarbon.svg")
    caps["fig4_radiocarbon.svg"] = (
        "Specific 14C activity against sample age (carbon14_age inverted), starting from "
        "13.56 dpm per gram of carbon in living matter. Ten half-lives leaves about one "
        "count per hour per gram, indistinguishable from detector background -- the hard "
        "limit on radiocarbon dating, and the reason older samples need daughter-ratio "
        "methods instead.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
