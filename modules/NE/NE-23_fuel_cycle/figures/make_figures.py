"""NE-23 figures -- the annual mass flow, the separative-work value function and
the optimal tails assay, where the energy in spent fuel came from, and the two
waste timescales.

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
from fuel_cycle import (                           # noqa: E402
    U235_WEIGHT_FRACTION, U235_ATOM_PERCENT, ANNUAL_FLOWS,
    NEW_FUEL_ATOM_PERCENT, SPENT_FUEL_ATOM_PERCENT, LONG_LIVED_FISSION_PRODUCTS,
    value_function, feed_per_product, swu_per_product, optimal_tails_assay,
    fission_product_activity_fraction, plutonium_fission_fraction,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- the annual mass flow.
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    stages = ["mined\nU in U$_3$O$_8$", "converted\nU in UF$_6$",
              "enriched\nproduct", "discharged\nU + Pu"]
    vals = [ANNUAL_FLOWS["U in U3O8 (mining/milling)"] / 1e3,
            ANNUAL_FLOWS["U in UF6 (conversion)"] / 1e3,
            28.070, ANNUAL_FLOWS["U + Pu discharged"] / 1e3]
    bars = ax.bar(range(4), vals, 0.55, color=[INK, INK, FLOW, LEAF],
                  edgecolor="white", lw=0.8)
    for i, b in enumerate(bars):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 3,
                "%.1f t" % vals[i], ha="center", fontsize=9)
    ax.bar([2], [ANNUAL_FLOWS["U tails at 0.2%"] / 1e3], 0.55, bottom=[28.070],
           color=ALT, alpha=0.45, edgecolor="white", lw=0.8, label="tails at 0.2%")
    ax.annotate("121.2 t of tails --\n81% of the mined uranium,\nthrown away at 0.2% $^{235}$U",
                xy=(2.3, 90), fontsize=8.5, color=ALT)
    ax.annotate("873 kg of this is\nfission products", xy=(3, 26.1),
                xytext=(3.05, 62), fontsize=8.5, color=LEAF,
                arrowprops=dict(arrowstyle="->", color=LEAF, lw=1.0))
    ax.set_xticks(range(4))
    ax.set_xticklabels(stages, fontsize=8.5)
    ax.set_ylabel("tonnes per year")
    ax.set_ylim(0, 170)
    ax.legend(fontsize=8.5, loc="upper right")
    ax.set_title("A 1000 MW(e) PWR, once through (S&F Table 11.7)")
    _save(fig, "fig1_annual_flows.svg")
    caps["fig1_annual_flows.svg"] = (
        "S&F Table 11.7's annual flowsheet. 150 tonnes of natural uranium are mined to load 28 "
        "tonnes of 2.9%-enriched fuel, because 121 tonnes leave as depleted tails at 0.2% -- "
        "four fifths of the mined uranium is set aside at the enrichment plant, still containing "
        "a quarter of the 235U it arrived with. The table's enrichment balance closes to the "
        "kilogram (product + tails = feed exactly), and its 873 kg of fission products "
        "corresponds to 277 full-power days against the 274 its own 75% capacity factor implies "
        "-- a mass flow and an energy output agreeing to 1% by completely different routes.")

    # Fig 2 -- the value function and the optimal tails.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.0))
    x = np.linspace(0.002, 0.998, 600)
    axL.plot(x, [value_function(v) for v in x], color=INK, lw=2.4)
    for a, lab, col in ((0.002, "tails\n0.2%", ALT),
                        (U235_WEIGHT_FRACTION, "natural\n0.711%", FLOW),
                        (0.03, "LWR fuel\n3%", LEAF),
                        (0.90, "weapons\n90%", STEEL)):
        axL.plot([a], [value_function(a)], "o", color=col, ms=8)
        axL.annotate(lab, xy=(a, value_function(a)), xytext=(a + 0.03,
                     value_function(a) + 0.35), fontsize=8.5, color=col)
    axL.axvline(0.5, color="0.85", lw=1.0, zorder=0)
    axL.annotate("$V(1/2)=0$: a 50:50 mixture\nis the least-separated state",
                 xy=(0.5, 0.15), xytext=(0.30, 1.6), fontsize=8.5, color="0.35",
                 arrowprops=dict(arrowstyle="->", color="0.5", lw=1.0))
    axL.set_xlabel("assay $x$ (weight fraction $^{235}$U)")
    axL.set_ylabel("value function $V(x)$")
    axL.set_ylim(0, 7)
    axL.set_title("$V(x)=(2x-1)\\ln[x/(1-x)]$")

    xt = np.linspace(0.0008, 0.006, 300)
    for u, col, ls in ((50.0, LEAF, "-."), (100.0, INK, "-"), (250.0, FLOW, "--")):
        cost = [feed_per_product(U235_WEIGHT_FRACTION, 0.045, t) * u
                + swu_per_product(U235_WEIGHT_FRACTION, 0.045, t) * 100.0
                for t in xt]
        axR.plot(100 * xt, np.array(cost) / min(cost), color=col, lw=2.2, ls=ls,
                 label="U at \\$%d/kg" % u)
        best, _ = optimal_tails_assay(U235_WEIGHT_FRACTION, 0.045, u, 100.0)
        axR.plot([100 * best], [1.0], "o", color=col, ms=8)
    axR.axvspan(0.20, 0.25, color=ALT, alpha=0.13, lw=0)
    axR.annotate("the historical\n0.20-0.25% band", xy=(0.225, 1.16),
                 fontsize=8.5, color=ALT, ha="center")
    axR.set_xlabel("tails assay (% $^{235}$U)")
    axR.set_ylabel("total cost / its own minimum")
    axR.set_ylim(0.98, 1.25)
    axR.legend(fontsize=8.5)
    axR.set_title("The tails assay is a price, not a constant")
    fig.tight_layout()
    _save(fig, "fig2_separative_work.svg")
    caps["fig2_separative_work.svg"] = (
        "Left: the separative-work value function, which S&F never write down although §11.7.2 "
        "describes five technologies that are all measured in it. V vanishes at x = 1/2 -- the "
        "least-separated state -- and diverges at both ends, so purity is expensive whichever "
        "end of the mixture you want. Table 11.7's reactor needs 116 tSWU a year. Right: the "
        "tails assay is an economic optimum and not a physical constant. Leaner tails need less "
        "uranium and more separative work, so expensive uranium pushes the optimum left. The "
        "0.2% of Table 11.7 corresponds to roughly equal uranium and SWU prices, which is a "
        "convention of its era.")

    # Fig 3 -- where the energy in the fuel came from.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.0))
    labels = ["$^{238}$U", "$^{235}$U", "$^{236}$U", "Pu", "fission\nproducts"]
    new = [NEW_FUEL_ATOM_PERCENT["238U"], NEW_FUEL_ATOM_PERCENT["235U"], 0, 0, 0]
    pu = sum(v for k, v in SPENT_FUEL_ATOM_PERCENT.items() if k.endswith("Pu"))
    spent = [SPENT_FUEL_ATOM_PERCENT["238U"], SPENT_FUEL_ATOM_PERCENT["235U"],
             SPENT_FUEL_ATOM_PERCENT["236U"], pu,
             SPENT_FUEL_ATOM_PERCENT["fission products"]]
    xs = np.arange(5)
    axL.bar(xs - 0.2, new, 0.38, color=INK, edgecolor="white", lw=0.8, label="new fuel")
    axL.bar(xs + 0.2, spent, 0.38, color=FLOW, hatch="///", edgecolor="white",
            lw=0.8, label="spent fuel")
    axL.set_yscale("log")
    axL.set_xticks(xs)
    axL.set_xticklabels(labels, fontsize=9)
    axL.set_ylabel("atom-% of the heavy metal")
    axL.set_ylim(0.02, 300)
    axL.legend(fontsize=8.5)
    axL.set_title("S&F Table 11.8: both columns sum to 100.00")

    frac = plutonium_fission_fraction()
    axR.pie([1 - frac, frac], labels=["$^{235}$U\n%.0f%%" % (100 * (1 - frac)),
                                      "plutonium\n%.0f%%" % (100 * frac)],
            colors=[INK, LEAF], startangle=90, autopct=None,
            wedgeprops=dict(edgecolor="white", lw=2),
            textprops=dict(fontsize=11))
    axR.set_title("Which nucleus actually fissioned\n(from Table 11.8's own balance)")
    fig.tight_layout()
    _save(fig, "fig3_spent_fuel.svg")
    caps["fig3_spent_fuel.svg"] = (
        "Left: S&F Table 11.8. Both columns sum to exactly 100.00 atom-%, and the transmutation "
        "accounting closes to two decimals with no adjustment: 235U loses 2.49, of which 0.51 "
        "captures to 236U and 1.98 fissions; 238U loses 2.40, of which 0.88 remains as plutonium "
        "and 1.52 fissioned. Right: the consequence. 1.52 of the 3.50 total fissions -- 43% of "
        "the energy -- came from plutonium that was not in the fuel when it was loaded. That is "
        "what §11.1 means by 'almost half the power' at end of life, it is why a reactor's "
        "reactivity does not simply decay away (~NE-20 §5), and it is the reason spent fuel is "
        "simultaneously a waste and a fuel.")

    # Fig 4 -- the two waste timescales.
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    years = np.logspace(0, 6.5, 400)
    ax.loglog(years, [fission_product_activity_fraction(y) for y in years],
              color=INK, lw=2.4, label="fission products ($^{137}$Cs, $^{90}$Sr, ~30 y)")
    ax.loglog(years, [fission_product_activity_fraction(y, 24000.0) for y in years],
              color=FLOW, lw=2.2, ls="--", label="$^{239}$Pu (24 000 y)")
    ax.axhline(1e-10, color=LEAF, ls=":", lw=1.8)
    ax.annotate("S&F's 'less than the original ore'", xy=(1.6, 1.4e-10),
                fontsize=8.5, color=LEAF)
    ax.axvline(1000, color=ALT, ls=":", lw=1.6)
    ax.annotate("1 000 y", xy=(1100, 1e-3), fontsize=9, color=ALT)
    ax.axvline(8e5, color=ALT, ls=":", lw=1.6)
    ax.annotate("800 000 y", xy=(2.4e5, 1e-3), fontsize=9, color=ALT, ha="right")
    ax.set_xlabel("years after discharge")
    ax.set_ylabel("fraction of initial activity")
    ax.set_ylim(1e-14, 3)
    ax.legend(fontsize=8.5, loc="lower left")
    ax.set_title("Two waste problems, 800-fold apart in time")
    _save(fig, "fig4_waste_timescales.svg")
    caps["fig4_waste_timescales.svg"] = (
        "S&F §11.7.4's argument, drawn. Of the seven fission products with half-lives above 25 "
        "years, five have MILLION-year half-lives -- which makes them effectively stable and "
        "therefore of negligible activity. The long-term fission-product activity is set "
        "entirely by 137Cs and 90Sr at about 30 years, and falls by a factor of 1e-10 in a "
        "thousand years, below the activity of the ore the uranium came from. The actinides are "
        "a different problem: 239Pu's 24 000-year half-life needs the same reduction over 800 000 "
        "years. That factor of 800 in required isolation time is the entire technical case for "
        "reprocessing -- separate the actinides back into fuel and the repository problem "
        "shortens from geological to merely historical.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
