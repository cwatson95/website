"""NE-17 figures -- dose per unit fluence and the kerma/dose gap, the exposure
rule of thumb and where it fails, the quality factor's factor of twenty, and
what natural background is actually made of.

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
from dosimetry import (                            # noqa: E402
    DOSE_PREFACTOR, GY_PER_ROENTGEN, mass_coefficient, absorbed_dose,
    quality_factor, rule_of_thumb_exposure_rate, exposure_rate_exact,
    rule_of_thumb_valid_range, NATURAL_BACKGROUND_WORLD, NATURAL_BACKGROUND_US,
    ICRP77_TISSUE_WEIGHTS, ICRP90_TISSUE_WEIGHTS, ICRP07_TISSUE_WEIGHTS,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    energies = np.logspace(math.log10(0.01), math.log10(20.0), 300)

    # Fig 1 -- dose per unit fluence, and the kerma/dose gap.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.0, 3.9))
    for material, col, ls in (("air", INK, "-"), ("water", FLOW, "--"),
                              ("iron", LEAF, "-."), ("lead", STEEL, ":")):
        d = [1e12 * absorbed_dose(e, mass_coefficient(material, e, "en"), 1.0)
             for e in energies]
        axL.loglog(energies, d, color=col, lw=2.0, ls=ls, label=material)
    axL.set_xlabel("photon energy (MeV)")
    axL.set_ylabel("dose per unit fluence (pGy cm$^2$)")
    axL.legend(fontsize=8.5, loc="lower right")
    axL.set_title("Air and tissue track each other;\nlead does not")

    for material, col, ls in (("water", FLOW, "--"), ("iron", LEAF, "-."),
                              ("lead", STEEL, ":")):
        ratio = [100 * (mass_coefficient(material, e, "tr")
                        / mass_coefficient(material, e, "en") - 1.0)
                 for e in energies]
        axR.semilogx(energies, ratio, color=col, lw=2.0, ls=ls, label=material)
    axR.axhline(0.0, color="0.85", lw=0.9, zorder=0)
    axR.annotate("iron at 5 MeV:\nkerma 6.5% high", xy=(5.0, 6.5),
                 xytext=(0.06, 12.0), fontsize=8.5, color=LEAF,
                 arrowprops=dict(arrowstyle="->", color=LEAF, lw=1.0))
    axR.set_xlabel("photon energy (MeV)")
    axR.set_ylabel("kerma above dose,  $\\mu_{tr}/\\mu_{en}-1$  (%)")
    axR.legend(fontsize=8.5, loc="upper left")
    axR.set_title("Where kerma stops being the dose")
    fig.tight_layout()
    _save(fig, "fig1_dose_per_fluence.svg")
    caps["fig1_dose_per_fluence.svg"] = (
        "Left: absorbed dose per unit photon fluence (absorbed_dose with mu_en from Appendix "
        "C.3). Air and water differ by only ~11% across the whole MeV range, which is the "
        "accident that lets exposure -- defined entirely in air -- survive as a proxy for tissue "
        "dose. Lead does not track them at all, so a lead-walled ion chamber does not read "
        "tissue dose. Right: the gap between kerma and absorbed dose, mu_tr/mu_en - 1. It is "
        "the fraction of secondary-electron energy radiated away as bremsstrahlung, negligible "
        "below ~1 MeV and 6.5% for iron at 5 MeV (S&F Example 9.1); it grows with Z and with "
        "energy, which is exactly when the two words stop being interchangeable.")

    # Fig 2 -- the 6CEN/r^2 rule of thumb.
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    e_rule = np.logspace(math.log10(0.03), math.log10(10.0), 400)
    ratio = [rule_of_thumb_exposure_rate(1.0, e, 1.0, 1.0)
             / exposure_rate_exact(1.0, e, 1.0, 1.0) for e in e_rule]
    ax.semilogx(e_rule, ratio, color=INK, lw=2.2)
    ax.axhline(1.0, color="0.8", lw=1.0, zorder=0)
    ax.axhspan(0.8, 1.2, color=LEAF, alpha=0.13, lw=0)
    lo, hi = rule_of_thumb_valid_range(0.20)
    ax.axvline(lo, color=LEAF, ls="--", lw=1.3)
    ax.axvline(hi, color=LEAF, ls="--", lw=1.3)
    ax.annotate("within 20%%\n%.2f - %.1f MeV" % (lo, hi), xy=(0.5, 0.87),
                fontsize=9, color=LEAF, ha="center")
    ax.annotate("photoelectric\nabsorption in air\nlifts $\\mu_{en}$",
                xy=(0.04, 0.72), fontsize=8.5, color=FLOW, ha="center")
    ax.annotate("Compton\nscattering\ndrops it", xy=(6.0, 1.55),
                fontsize=8.5, color=FLOW, ha="center")
    ax.plot([0.1], [rule_of_thumb_exposure_rate(1.0, 0.1, 1.0, 1.0)
                    / exposure_rate_exact(1.0, 0.1, 1.0, 1.0)],
            "o", color=ALT, ms=7)
    ax.annotate("a marginal dip at 0.1 MeV\nsplits the band", xy=(0.1, 1.233),
                xytext=(0.13, 1.45), fontsize=8.5, color=ALT,
                arrowprops=dict(arrowstyle="->", color=ALT, lw=1.0))
    ax.set_xlabel("photon energy (MeV)")
    ax.set_ylabel("rule of thumb / exact exposure rate")
    ax.set_xlim(0.03, 10.0)
    ax.set_ylim(0.5, 1.8)
    ax.set_title("$\\dot X = 6CEN/r^2$  (Ci, MeV, feet)  vs Eq. (9.9)")
    _save(fig, "fig2_rule_of_thumb.svg")
    caps["fig2_rule_of_thumb.svg"] = (
        "The field rule Xdot = 6CEN/r^2 (S&F Ch. 9 Prob. 6) divided by the exact Eq. (9.9). "
        "The rule is really the statement that air's mu_en/rho is constant at 0.02866 cm2/g, "
        "and it holds within 20% from 0.12 to 1.9 MeV -- more than a decade, which is why it "
        "survives on clipboards. It fails in both directions and for different reasons: "
        "photoelectric absorption lifts mu_en below 0.1 MeV, Compton scattering drops it above "
        "2 MeV. Note the failure at high energy is 65% HIGH at 5 MeV, so the rule is "
        "conservative for a dose estimate and wasteful for a shield.")

    # Fig 3 -- the quality factor.
    fig, ax = plt.subplots(figsize=(6.8, 3.9))
    e_n = np.logspace(-4, 2, 600)
    qf = [quality_factor("neutron", e) for e in e_n]
    ax.semilogx(e_n, qf, color=INK, lw=2.4, label="neutrons (Table 9.1)")
    ax.axhline(1.0, color=FLOW, lw=2.0, ls="--", label="x, $\\gamma$, $\\beta$ (any energy)")
    ax.axhline(20.0, color=LEAF, lw=2.0, ls=":", label="alpha particles")
    ax.axvspan(0.1, 2.0, color=ALT, alpha=0.12, lw=0)
    ax.annotate("fission spectrum\nsits in the peak", xy=(0.45, 15.5),
                fontsize=9, color=ALT, ha="center")
    ax.set_xlabel("neutron energy (MeV)")
    ax.set_ylabel("quality factor  QF")
    ax.set_ylim(0, 23)
    ax.legend(fontsize=8.5, loc="upper left")
    ax.set_title("One gray is not one gray")
    _save(fig, "fig3_quality_factor.svg")
    caps["fig3_quality_factor.svg"] = (
        "S&F Table 9.1 quality factors (quality_factor). The same absorbed dose is weighted by "
        "anything from 1 to 20 depending on how densely the energy is laid down along a track, "
        "so a dose in grays without its radiation type says nothing about hazard. The neutron "
        "curve peaks at 0.1-2 MeV -- which is precisely where the fission spectrum lives "
        "(~NE-09), so a reactor's neutron field is weighted at the maximum. This is also why "
        "quality_factor() refuses an unrecognised radiation rather than defaulting to 1: that "
        "default would understate a fast-neutron dose twentyfold.")

    # Fig 4 -- what background is made of, and how the tissue weights moved.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.2, 4.0))
    world_order = ["cosmic low-LET", "cosmic high-LET", "terrestrial gamma",
                   "ingestion low-LET", "ingestion high-LET", "inhalation"]
    us_order = ["cosmic", "cosmogenic", "external terrestrial", "in body", "inhaled"]
    cols = [INK, STEEL, FLOW, LEAF, ALT, "#8a8a8a"]
    bottom = 0.0
    for i, k in enumerate(world_order):
        v = NATURAL_BACKGROUND_WORLD[k]
        axL.bar([0], [v], 0.55, bottom=bottom, color=cols[i], edgecolor="white", lw=0.8)
        if v >= 0.2:
            axL.text(0, bottom + v / 2, "%s\n%.1f" % (k, v), ha="center",
                     va="center", fontsize=7.5, color="white")
        bottom += v
    axL.text(0, bottom + 0.08, "world 2.4 mSv/y", ha="center", fontsize=9, color=INK)
    bottom = 0.0
    for i, k in enumerate(us_order):
        v = NATURAL_BACKGROUND_US[k]
        axL.bar([1], [v], 0.55, bottom=bottom, color=cols[i], edgecolor="white", lw=0.8)
        if v >= 0.2:
            axL.text(1, bottom + v / 2, "%s\n%.2f" % (k, v), ha="center",
                     va="center", fontsize=7.5, color="white")
        bottom += v
    axL.text(1, bottom + 0.08, "U.S. 3.0 mSv/y", ha="center", fontsize=9, color=INK)
    axL.set_xticks([0, 1])
    axL.set_xticklabels(["Table 9.5\n(world)", "Table 9.6\n(U.S.)"])
    axL.set_ylabel("annual effective dose (mSv)")
    axL.set_ylim(0, 3.5)
    axL.set_title("Half the world's background is radon")

    organs = ["gonads", "breast", "lung", "thyroid", "bone surface"]
    x = np.arange(len(organs))
    for i, (name, w, col, hatch) in enumerate((
            ("ICRP 1977", ICRP77_TISSUE_WEIGHTS, INK, ""),
            ("ICRP 1991", ICRP90_TISSUE_WEIGHTS, FLOW, "///"),
            ("ICRP 2007", ICRP07_TISSUE_WEIGHTS, LEAF, "..."))):
        vals = [w.get(o, 0.0) for o in organs]
        axR.bar(x + (i - 1) * 0.27, vals, 0.25, color=col, hatch=hatch,
                edgecolor="white", lw=0.6, label=name)
    axR.set_xticks(x)
    axR.set_xticklabels(organs, fontsize=8.5, rotation=15)
    axR.set_ylabel("tissue weighting factor $w_T$")
    axR.legend(fontsize=8.5)
    axR.set_title("The weights are a risk estimate,\nand risk estimates move")
    fig.tight_layout()
    _save(fig, "fig4_background_and_weights.svg")
    caps["fig4_background_and_weights.svg"] = (
        "Left: S&F Tables 9.5 and 9.6. Natural background is 2.4 mSv/y worldwide and 3.0 mSv/y "
        "in the U.S., and inhaled radon is half of the first and two thirds of the second -- so "
        "the dominant human radiation exposure is a decay product of uranium in soil, not "
        "anything engineered. This is the yardstick every other number in ~NE-18 is measured "
        "against. Right: the Table 9.2 and 9.3 tissue weighting factors, with ICRP Publication "
        "103 (2007, beyond S&F) added. The gonad weight fell 0.25 -> 0.20 -> 0.08 as the "
        "hereditary-risk estimate came down while breast rose to 0.12: these are scientific "
        "judgements encoded as arithmetic, and an effective dose is only ever quoted with "
        "respect to one vintage of them.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
