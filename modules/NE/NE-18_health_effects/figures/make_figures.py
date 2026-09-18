"""NE-18 figures -- deterministic thresholds against the lethality curve, the
five dose-effect models and where they stop being distinguishable, cancer risk
against age at exposure, and where radon's potential alpha energy actually sits.

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
from health_effects import (                       # noqa: E402
    DETERMINISTIC_EFFECTS, LETHAL_DOSES, lethality_fraction,
    cancer_risk_at_age, NCRP_1987_LIMITS, RADON_RISK_BY_POPULATION,
    RN222_CHAIN, PO214_ALPHA_MEV, PO218_ALPHA_MEV,
    potential_alpha_energy_per_bq, lnt, linear_with_threshold, quadratic,
    linear_quadratic, hormetic,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- deterministic thresholds and the lethality curve.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.4),
                                   gridspec_kw={"width_ratios": [1.35, 1.0]})
    labels = ["%s: %s" % (o, e) for o, e, _, _, _, _ in DETERMINISTIC_EFFECTS]
    order = sorted(range(len(DETERMINISTIC_EFFECTS)),
                   key=lambda i: DETERMINISTIC_EFFECTS[i][4])
    y = np.arange(len(order))
    for row, i in enumerate(order):
        _, _, d50, d50u, dth, dthu = DETERMINISTIC_EFFECTS[i]
        axL.plot([dth, d50], [row, row], color="0.75", lw=1.6, zorder=1)
        axL.errorbar([dth], [row], xerr=[[dthu], [dthu]], fmt="o", color=FLOW,
                     ms=6, capsize=2.5, lw=1.2, zorder=3)
        axL.errorbar([d50], [row], xerr=[[d50u], [d50u]], fmt="s", color=INK,
                     ms=6, capsize=2.5, lw=1.2, zorder=3)
    axL.set_yticks(y)
    axL.set_yticklabels([labels[i] for i in order], fontsize=8)
    axL.set_xscale("log")
    axL.set_xlabel("absorbed dose (Gy)")
    axL.set_xlim(0.1, 200)
    axL.plot([], [], "o", color=FLOW, label="threshold $D_{th}$")
    axL.plot([], [], "s", color=INK, label="median $D_{50}$")
    axL.axvline(NCRP_1987_LIMITS["occupational stochastic"] / 1000.0,
                color=LEAF, ls="--", lw=1.4)
    axL.annotate("annual occupational\nlimit, 50 mSv", xy=(0.05, 6.5),
                 fontsize=8, color=LEAF, ha="center")
    axL.legend(fontsize=8, loc="lower right")
    axL.set_title("Deterministic effects: nothing below the threshold")

    d = np.linspace(0, 7, 400)
    axR.plot(d, [100 * lethality_fraction(x) for x in d], color=INK, lw=2.4)
    for name, (lo, hi) in sorted(LETHAL_DOSES.items(),
                                 key=lambda kv: kv[1][0]):
        axR.axvspan(lo, hi, color=FLOW, alpha=0.10, lw=0)
        axR.plot([0.5 * (lo + hi)], [float(name.split("LD")[1].split("/")[0])],
                 "o", color=FLOW, ms=6)
    axR.annotate("LD50/60\n3.0-3.5 Gy", xy=(3.25, 50), xytext=(4.4, 38),
                 fontsize=9, color=FLOW,
                 arrowprops=dict(arrowstyle="->", color=FLOW, lw=1.0))
    axR.set_xlabel("mid-line absorbed dose (Gy)")
    axR.set_ylabel("60-day lethality (%)")
    axR.set_xlim(0, 7)
    axR.set_ylim(-3, 103)
    axR.set_title("From 5% to 99% in a factor\nof 2.2 in dose")
    fig.tight_layout()
    _save(fig, "fig1_deterministic.svg")
    caps["fig1_deterministic.svg"] = (
        "Left: S&F Table 9.7, sorted by threshold. A deterministic effect does not occur below "
        "its threshold in ANYONE -- the bar is a real edge, not a small probability -- and above "
        "it severity grows with dose. The testes are the most radiosensitive endpoint in the "
        "table at 0.3 Gy, six times below the marrow-death threshold. Every one of these sits "
        "far above the 50 mSv annual occupational limit, which is set by stochastic risk "
        "instead. Right: 60-day lethality without treatment (lethality_fraction, Table 9.8). "
        "The span from 'almost everyone lives' to 'almost everyone dies' is only a factor of "
        "2.2 in dose, which is why accident dosimetry has to be good to tens of percent.")

    # Fig 2 -- the five dose-effect models.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.2, 4.0))
    dose = np.linspace(0, 2.0, 400)
    models = (("(a) linear no-threshold", lambda x: lnt(x, 0.5), INK, "-"),
              ("(b) linear with threshold", lambda x: linear_with_threshold(x, 0.6, 0.35), FLOW, "--"),
              ("(c) quadratic", lambda x: quadratic(x, 0.25), LEAF, "-."),
              ("(d) linear-quadratic", lambda x: linear_quadratic(x, 0.3, 0.1), STEEL, ":"),
              ("(e) hormetic", lambda x: hormetic(x, 0.5, 0.35), ALT, (0, (3, 1, 1, 1, 1, 1))))
    for name, fn, col, ls in models:
        axL.plot(dose, [fn(x) for x in dose], color=col, lw=2.0, ls=ls, label=name)
    axL.axhline(0.0, color="0.85", lw=0.9, zorder=0)
    axL.set_xlabel("dose (Gy)")
    axL.set_ylabel("effect (arbitrary)")
    axL.legend(fontsize=8, loc="upper left")
    axL.set_title("S&F Fig. 9.3: five candidate shapes")

    dose2 = np.logspace(-4, 0.3, 400)
    for name, fn, col, ls in models:
        axR.plot(dose2, [abs(fn(x)) for x in dose2], color=col, lw=2.0, ls=ls)
    axR.set_xscale("log")
    axR.set_yscale("log")
    axR.axvspan(1e-4, 0.2, color=FLOW, alpha=0.10, lw=0)
    axR.annotate("no excess has ever been\nobserved in this band", xy=(3e-3, 3e-4),
                 fontsize=8.5, color=FLOW, ha="center")
    axR.axvline(0.05, color=LEAF, ls="--", lw=1.4)
    axR.annotate("annual\noccupational\nlimit", xy=(0.052, 2e-6), fontsize=8,
                 color=LEAF)
    axR.set_xlabel("dose (Gy)")
    axR.set_ylabel("|effect|")
    axR.set_ylim(1e-7, 3)
    axR.set_title("...and where they cannot be told apart")
    fig.tight_layout()
    _save(fig, "fig2_dose_effect_models.svg")
    caps["fig2_dose_effect_models.svg"] = (
        "The five dose-effect models of S&F Fig. 9.3. Left: at doses of order 1 Gy they are "
        "plainly different curves. Right: the same five on log axes, with the shaded band "
        "marking where S&F say excess cancer risk 'cannot be observed' -- below about 0.2 Gy. "
        "Every dose limit in Table 9.17 lies inside that band, four to two hundred times below "
        "its upper edge. The regulatory choice of the linear no-threshold model is not a "
        "measurement; it is the most conservative shape available where measurement stops, "
        "which is exactly the argument S&F §9.10 lays out and does not settle.")

    # Fig 3 -- cancer risk against age at exposure.
    fig, ax = plt.subplots(figsize=(6.9, 4.2))
    ages = np.linspace(0, 80, 200)
    for sex, col, ls in (("female", FLOW, "-"), ("male", INK, "--")):
        ax.plot(ages, [cancer_risk_at_age(sex, a) for a in ages], color=col,
                lw=2.3, ls=ls, label="%s, solid cancer" % sex)
        ax.plot(ages, [cancer_risk_at_age(sex, a, endpoint="leukemia") for a in ages],
                color=col, lw=1.5, ls=":", alpha=0.85,
                label="%s, leukemia" % sex)
    ax.set_yscale("log")
    ax.set_xlabel("age at exposure (years)")
    ax.set_ylabel("excess deaths per $10^5$ per 0.1 Gy")
    ax.set_xlim(0, 80)
    ax.legend(fontsize=8.5)
    ax.annotate("solid cancers need decades of\nlatency an older person may not have",
                xy=(55, 300), xytext=(24, 90), fontsize=8.5, color=STEEL,
                arrowprops=dict(arrowstyle="->", color=STEEL, lw=1.0))
    ax.annotate("leukemia appears within a few years,\nso age barely matters",
                xy=(60, 60), xytext=(20, 25), fontsize=8.5, color=LEAF,
                arrowprops=dict(arrowstyle="->", color=LEAF, lw=1.0))
    ax.set_title("Radiogenic cancer mortality risk (S&F Table 9.13)")
    _save(fig, "fig3_cancer_risk_vs_age.svg")
    caps["fig3_cancer_risk_vs_age.svg"] = (
        "Excess lifetime cancer mortality per 100 000 people exposed to 0.1 Gy, against age at "
        "exposure (cancer_risk_at_age, S&F Table 9.13). Solid-cancer risk falls elevenfold from "
        "infancy to age 80 while leukemia risk is nearly flat -- and the reason is latency, not "
        "biology of the exposure: solid cancers seldom appear before 10 years and keep appearing "
        "for 30 or more, so an 80-year-old may not live to express one, whereas leukemia appears "
        "within a few years and largely disappears within 30. Women carry roughly 1.5x the "
        "solid-cancer risk of men, which is the same asymmetry as the beta = 0.57 vs 0.33 in "
        "the BEIR-VII model of Eq. (9.16).")

    # Fig 4 -- radon: where the potential alpha energy lives, and who it hurts.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.2, 4.0))
    lam = [math.log(2.0) / t for _, t, _ in RN222_CHAIN]
    terms = [(PO218_ALPHA_MEV + PO214_ALPHA_MEV) / lam[0],
             PO214_ALPHA_MEV / lam[1], PO214_ALPHA_MEV / lam[2],
             PO214_ALPHA_MEV / lam[3]]
    names = ["$^{218}$Po\n3.05 min\nalpha 6.00", "$^{214}$Pb\n26.8 min\nno alpha",
             "$^{214}$Bi\n19.9 min\nno alpha", "$^{214}$Po\n164 $\\mu$s\nalpha 7.69"]
    total = potential_alpha_energy_per_bq()
    cols = [FLOW, INK, INK, LEAF]
    bars = axL.bar(range(4), [100 * t / total for t in terms], 0.6, color=cols,
                   edgecolor="white", lw=0.8)
    for i, b in enumerate(bars):
        axL.text(b.get_x() + b.get_width() / 2, b.get_height() + 1.2,
                 "%.1f%%" % (100 * terms[i] / total), ha="center", fontsize=9)
    axL.set_xticks(range(4))
    axL.set_xticklabels(names, fontsize=7.5)
    axL.set_ylabel("share of potential alpha energy (%)")
    axL.set_ylim(0, 62)
    axL.set_title("The two daughters that emit no alphas\ncarry 90% of the hazard")

    pops = ["nonsmoking female", "nonsmoking male", "female", "mixed", "male",
            "smoking female", "smoking male"]
    vals = [RADON_RISK_BY_POPULATION[p][1] for p in pops]
    cols2 = [LEAF if "nonsmok" in p else (FLOW if "smoking" in p else INK)
             for p in pops]
    axR.barh(range(len(pops)), vals, 0.62, color=cols2, edgecolor="white", lw=0.8)
    axR.set_yticks(range(len(pops)))
    axR.set_yticklabels(pops, fontsize=8.5)
    axR.set_xlabel("lifetime lung-cancer mortality\nper MBq h m$^{-3}$ annual EEC")
    axR.annotate("10x", xy=(0.09, 6), xytext=(0.10, 4.2), fontsize=11, color=FLOW,
                 arrowprops=dict(arrowstyle="<->", color=FLOW, lw=1.3))
    axR.set_title("Radon and tobacco multiply")
    fig.tight_layout()
    _save(fig, "fig4_radon.svg")
    caps["fig4_radon.svg"] = (
        "Left: how S&F Eq. (9.19)'s potential alpha energy divides among the four short-lived "
        "222Rn daughters (potential_alpha_energy_per_bq). 214Pb and 214Bi emit no alpha "
        "particles at all and yet carry 90% of the hazard, because each is worth 214Po's 7.69 "
        "MeV held in escrow and each lives hundreds of times longer than 218Po; 214Po's own "
        "term is negligible because it lives 164 microseconds. That is why the dose depends on "
        "the daughter mixture and not on the radon itself. Right: S&F Table 9.15. A smoker's "
        "radiogenic risk is ten times a non-smoker's for the same exposure -- the two hazards "
        "multiply rather than add, so radon remediation is worth ten times as much to a smoker.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
