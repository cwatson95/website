"""NE-26 figures -- activation saturation and the 99Mo cow, the gauge optimum,
NAA's seven decades, and the process-dose ladder.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.

Palette note: ALT and STEEL are indistinguishable under deuteranopia, so any
panel using both also varies linestyle or marker (modules/CHANGELOG.md Known-bad).
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
from applications import (                        # noqa: E402
    NAA_SENSITIVITY, PROCESS_DOSES, RADIOGRAPHY_SOURCES,
    saturation_fraction, generator_daughter_activity, optimal_milking_time,
    gauge_precision, optimal_gauge_thickness, transmission,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- saturation and the generator.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.0))
    n = np.linspace(0, 8, 300)
    axL.plot(n, [saturation_fraction(x, 1.0) for x in n], color=INK, lw=2.4)
    for h, lab in ((1, "1 T$_{1/2}$: 50%"), (3, "3: 87.5%"), (7, "7: 99.2%")):
        axL.plot([h], [saturation_fraction(h, 1.0)], "o", color=FLOW, ms=8)
        axL.annotate(lab, xy=(h, saturation_fraction(h, 1.0)),
                     xytext=(h + 0.25, saturation_fraction(h, 1.0) - 0.11),
                     fontsize=9, color=FLOW)
    axL.axhline(1.0, color="0.8", ls="--", lw=1.2)
    axL.set_xlabel("irradiation time (half-lives)")
    axL.set_ylabel("fraction of saturation activity")
    axL.set_ylim(0, 1.08)
    axL.set_title("Activation saturates and never arrives")

    hours = np.linspace(0, 168, 400)
    axR.plot(hours, [generator_daughter_activity(h) for h in hours], color=INK,
             lw=2.4, label="$^{99m}$Tc after elution")
    t_opt = optimal_milking_time()
    axR.plot([t_opt], [generator_daughter_activity(t_opt)], "o", color=ALT, ms=9)
    axR.annotate("peak at %.1f h\n(2.0 days)" % t_opt,
                 xy=(t_opt, generator_daughter_activity(t_opt)),
                 xytext=(70, 0.80), fontsize=9, color=ALT,
                 arrowprops=dict(arrowstyle="->", color=ALT, lw=1.0))
    for d in range(1, 7):
        axR.axvline(24 * d, color=LEAF, ls=":", lw=1.0, alpha=0.7)
    axR.annotate("daily elution", xy=(96, 0.18), fontsize=8.5, color=LEAF)
    axR.set_xlabel("hours after the previous elution")
    axR.set_ylabel("$^{99m}$Tc activity (per unit $^{99}$Mo)")
    axR.legend(fontsize=9)
    axR.set_title("The $^{99}$Mo cow")
    fig.tight_layout()
    _save(fig, "fig1_production.svg")
    caps["fig1_production.svg"] = (
        "Left: activation in a reactor approaches its saturation activity exponentially -- three "
        "half-lives buys 87.5% and the remaining seven buy twelve percentage points, which is "
        "why production schedules are quoted in half-lives. Right: the 99Mo/99mTc generator, "
        "which S&F call the source of 'the most widely used radioisotope in medical diagnoses' "
        "without giving the transient equilibrium that operates it. Ingrowth peaks 48.5 hours "
        "after elution, and the activity is already at 95% of that after 24 hours -- which is "
        "exactly why hospital generators are delivered weekly and eluted daily. The generator is "
        "a way to ship a 6-hour isotope by shipping a 66-day one.")

    # Fig 2 -- the gauge optimum.
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    mut = np.linspace(0.1, 10, 400)
    p2 = gauge_precision(2.0, 1.0, 1e6)
    ax.plot(mut, [gauge_precision(m, 1.0, 1e6) / p2 for m in mut], color=INK, lw=2.4)
    ax.axvline(2.0, color=ALT, ls="--", lw=1.8)
    ax.plot([2.0], [1.0], "o", color=ALT, ms=10, zorder=5)
    ax.annotate("$\\mu t = 2$ exactly", xy=(2.0, 1.0), xytext=(3.0, 1.15),
                fontsize=10, color=ALT,
                arrowprops=dict(arrowstyle="->", color=ALT, lw=1.0))
    ax.axhspan(1.0, 1.25, color=LEAF, alpha=0.13, lw=0)
    ax.annotate("within 25% of optimal\nover $\\mu t$ = 0.9 to 3.6",
                xy=(6.2, 1.12), fontsize=8.5, color=LEAF)
    for x, lab in ((0.5, "1.9x"), (6.0, "2.5x")):
        y = gauge_precision(x, 1.0, 1e6) / p2
        ax.plot([x], [y], "s", color=FLOW, ms=7)
        ax.annotate(lab, xy=(x, y), xytext=(x + 0.2, y + 0.12), fontsize=9,
                    color=FLOW)
    ax.set_xlabel("$\\mu t$  (mean free paths of attenuation)")
    ax.set_ylabel("thickness precision, relative to the optimum")
    ax.set_ylim(0.9, 3.2)
    ax.set_title("The design rule Chapter 13 does not contain")
    _save(fig, "fig2_gauge_optimum.svg")
    caps["fig2_gauge_optimum.svg"] = (
        "S&F §13.4.2 describes transmission thickness gauging without ever asking what "
        "attenuation the gauge should be designed for. Counting statistics answer it in three "
        "lines: the fractional precision is exp(mu t/2)/(mu t sqrt(N0)), and minimising it gives "
        "mu*t = 2 EXACTLY -- two mean free paths. More attenuation gives more signal per unit "
        "thickness and fewer counts, and the optimum is where they balance. It is also "
        "forgiving: anything from 0.9 to 3.6 mean free paths is within 25% of the best "
        "achievable, which is why the rule is useful in practice rather than merely true.")

    # Fig 3 -- NAA's seven decades.
    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    ranked = sorted(NAA_SENSITIVITY.items(), key=lambda kv: kv[1])
    names = [k for k, _ in ranked]
    vals = [v for _, v in ranked]
    cols = [LEAF if v < 1e-3 else (INK if v < 1e-1 else FLOW) for v in vals]
    ax.barh(range(len(names)), vals, 0.72, color=cols, edgecolor="white", lw=0.5)
    ax.set_xscale("log")
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=7.5)
    ax.set_xlabel("minimum detectable mass ($\\mu$g), 1 h at $10^{13}$ cm$^{-2}$s$^{-1}$")
    ax.set_xlim(3e-7, 40)
    ax.annotate("Eu: 0.9 picograms\n($4\\times10^{9}$ atoms)", xy=(9e-7, 0.5),
                xytext=(4e-6, 4.5), fontsize=8.5, color=LEAF,
                arrowprops=dict(arrowstyle="->", color=LEAF, lw=1.0))
    ax.annotate("Fe: 10 $\\mu$g", xy=(10, len(names) - 1.2), fontsize=8.5, color=FLOW)
    ax.set_title("NAA is exquisite for some elements and blind to others")
    _save(fig, "fig3_naa.svg")
    caps["fig3_naa.svg"] = (
        "S&F Table 13.3, sorted. Neutron activation analysis detects europium at 0.9 picograms "
        "-- about four billion atoms -- and iron only at 10 micrograms, seven orders of "
        "magnitude worse. The spread is set by two things the method cannot control: the "
        "activation cross section, and whether the product emits a gamma distinguishable from "
        "everything else in the sample. So NAA is not a general assay; it is exquisite for a few "
        "dozen elements and useless for the rest, which is why §13.4.7 lists what it is used for "
        "(forensic trace signatures, geological samples, pesticide residues) rather than "
        "claiming it is universal.")

    # Fig 4 -- the dose ladder.
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    items = sorted(PROCESS_DOSES.items(), key=lambda kv: kv[1][0])
    for i, (k, (lo, hi)) in enumerate(items):
        ax.barh([i], [max(hi - lo, lo * 0.05)], 0.5, left=[lo], color=INK,
                edgecolor="white", lw=0.8)
        ax.text(hi * 1.35, i, "%g-%g Gy" % (lo, hi) if hi != lo else "%g Gy" % lo,
                va="center", fontsize=8.5)
    ax.axvline(3.5, color=ALT, lw=2.0, ls="--")
    ax.annotate("LD50/60 for a human\n(~NE-18): 3.5 Gy", xy=(3.5, 3.6),
                xytext=(4.5, 3.3), fontsize=8.5, color=ALT,
                arrowprops=dict(arrowstyle="->", color=ALT, lw=1.0))
    ax.set_xscale("log")
    ax.set_yticks(range(len(items)))
    ax.set_yticklabels([k for k, _ in items], fontsize=8.5)
    ax.set_xlabel("absorbed dose (Gy)")
    ax.set_xlim(1, 3e5)
    ax.set_title("'Irradiation' spans a factor of 400")
    _save(fig, "fig4_process_doses.svg")
    caps["fig4_process_doses.svg"] = (
        "S&F §13.5's process doses on a log scale, with ~NE-18's human LD50/60 marked for "
        "scale. Stopping a potato sprouting takes 60 Gy; sterilising a syringe takes 25 000 -- a "
        "factor of 400, and the same word describes both. Note where the ladder starts: the very "
        "lowest process dose is already seventeen times the dose that kills half of exposed "
        "people, which is a useful corrective to the intuition that food irradiation and "
        "radiation exposure are the same phenomenon at different scales. They are not on the "
        "same scale at all.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
