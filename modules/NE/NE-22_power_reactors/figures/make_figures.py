"""NE-22 figures -- the 374 C ceiling and what it costs, PWR against BWR, the
Generation III component count, and the Generation IV escape.

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
from power_reactors import (                       # noqa: E402
    WATER_CRITICAL_C, TYPICAL_CORE_LIMIT_C, PWR, BWR, GEN_III_BWR, GEN_III_PWR,
    GEN_IV_SYSTEMS, SMALL_REACTORS, carnot_efficiency, thermal_efficiency,
    waste_heat, peaking_factor,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- the ceiling.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.2))
    t = np.linspace(200, 1050, 400)
    axL.plot(t, [100 * carnot_efficiency(x, 33.0) for x in t], color=INK, lw=2.4,
             label="Carnot (sink 33 $^\\circ$C)")
    axL.plot(t, [100 * 0.75 * carnot_efficiency(x, 33.0) for x in t], color=FLOW,
             lw=2.0, ls="--", label="75% of Carnot (a real turbine)")
    axL.axvspan(WATER_CRITICAL_C, 1060, color=LEAF, alpha=0.10, lw=0)
    axL.axvline(WATER_CRITICAL_C, color=ALT, lw=2.0, ls=":")
    axL.annotate("water's critical\ntemperature, 374 $^\\circ$C",
                 xy=(WATER_CRITICAL_C, 20), xytext=(430, 14), fontsize=8.5,
                 color=ALT, arrowprops=dict(arrowstyle="->", color=ALT, lw=1.0))
    axL.plot([PWR["steam_temp_C"]], [100 * PWR["efficiency"]], "o", color=INK, ms=9)
    axL.annotate("PWR: 284 $^\\circ$C, 34%", xy=(PWR["steam_temp_C"], 34),
                 xytext=(210, 46), fontsize=9, color=INK,
                 arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
    for k, v in GEN_IV_SYSTEMS.items():
        axL.plot([v["outlet_C"]], [100 * v["efficiency"]], "s", color=LEAF, ms=6)
    axL.annotate("Generation IV", xy=(760, 47), fontsize=9, color=LEAF)
    axL.set_xlabel("turbine inlet temperature ($^\\circ$C)")
    axL.set_ylabel("efficiency (%)")
    axL.set_ylim(0, 80)
    axL.legend(fontsize=8.5, loc="upper left")
    axL.set_title("Everything follows from 374 $^\\circ$C")

    etas = np.linspace(0.28, 0.52, 200)
    axR.plot(100 * etas, [waste_heat(1000.0, e) for e in etas], color=INK, lw=2.4)
    for e, lab, col in ((0.34, "LWR", FLOW), (0.44, "MSR/SCWR", LEAF),
                        (0.50, "VHTR", ALT)):
        axR.plot([100 * e], [waste_heat(1000.0, e)], "o", color=col, ms=8)
        axR.annotate("%s\n%.0f MW" % (lab, waste_heat(1000.0, e)),
                     xy=(100 * e, waste_heat(1000.0, e)),
                     xytext=(100 * e + 1.2, waste_heat(1000.0, e) + 130),
                     fontsize=8.5, color=col)
    axR.axhline(1000.0, color="0.8", ls="--", lw=1.2)
    axR.annotate("the 1000 MW actually sold", xy=(29, 1060), fontsize=8.5, color="0.4")
    axR.set_xlabel("plant efficiency (%)")
    axR.set_ylabel("heat rejected by a 1000 MW(e) plant (MW)")
    axR.set_title("What is thrown away")
    fig.tight_layout()
    _save(fig, "fig1_efficiency_ceiling.svg")
    caps["fig1_efficiency_ceiling.svg"] = (
        "Left: S&F Eq. (11.1) against turbine inlet temperature. Water cannot exist as a liquid "
        "above 374 C at any pressure, and a water-moderated core needs liquid water to moderate "
        "as well as to cool -- so the outlet is capped near 340 C, the steam reaches the turbine "
        "at 284 C barely superheated, and the plant lands at 34%, which is 75% of its Carnot "
        "limit. The Generation IV systems (squares) all sit to the right of that line, which is "
        "what they are for. Right: the consequence that picks the site. A 1000 MW(e) LWR rejects "
        "1940 MW to a river, the sea or a cooling tower -- nearly twice what it sells. A 50% "
        "plant would reject half as much.")

    # Fig 2 -- PWR vs BWR.
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    keys = [("pressure_MPa", "operating pressure\n(MPa)"),
            ("power_density_kW_per_L", "power density\n(kW/L)"),
            ("specific_power_kW_per_kgU", "specific power\n(kW/kg U)"),
            ("equil_enrichment_pct", "equil. enrichment\n(%)"),
            ("burnup_GWd_per_tU", "burnup\n(GWd/tU)"),
            ("vessel_wall_cm", "vessel wall\n(cm)")]
    x = np.arange(len(keys))
    pwr_v = [PWR[k] / max(PWR[k], BWR[k]) for k, _ in keys]
    bwr_v = [BWR[k] / max(PWR[k], BWR[k]) for k, _ in keys]
    ax.bar(x - 0.2, pwr_v, 0.38, color=INK, edgecolor="white", lw=0.8, label="PWR")
    ax.bar(x + 0.2, bwr_v, 0.38, color=FLOW, hatch="///", edgecolor="white",
           lw=0.8, label="BWR")
    for i, (k, _) in enumerate(keys):
        ax.text(i - 0.2, pwr_v[i] + 0.02, "%g" % PWR[k], ha="center", fontsize=8)
        ax.text(i + 0.2, bwr_v[i] + 0.02, "%g" % BWR[k], ha="center", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels([lab for _, lab in keys], fontsize=8.5)
    ax.set_ylabel("normalised to the larger of the pair")
    ax.set_ylim(0, 1.22)
    ax.legend(fontsize=9)
    ax.set_title("Same steam, same 34% -- and a factor of two everywhere else")
    _save(fig, "fig2_pwr_vs_bwr.svg")
    caps["fig2_pwr_vs_bwr.svg"] = (
        "S&F Tables 11.2 and 11.3, normalised pairwise. Both plants deliver ~285 C steam at 34% "
        "efficiency and both are 1000 MW(e)-class machines of the same vintage, yet nearly every "
        "other number differs by about a factor of two -- and every one of those differences "
        "traces to a single decision: a BWR boils in the core and a PWR does not. Boiling lets "
        "the BWR run at half the pressure (and so a thinner vessel wall), but the steam voids "
        "need room, so its power density is 1.8 times lower and its core is nearly twice the "
        "volume for the same output. Direct-cycle steam also lets it run on less enrichment, at "
        "the cost of lower discharge burnup.")

    # Fig 3 -- Generation III: fewer components.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.0))
    names = ["BWR/6", "ABWR", "ESBWR"]
    comps = [("recirculation_pumps", "recirculation pumps", INK),
             ("safety_pumps", "safety-system pumps", FLOW),
             ("diesels", "safety diesel gens", LEAF)]
    xs = np.arange(len(names))
    for i, (key, lab, col) in enumerate(comps):
        axL.bar(xs + (i - 1) * 0.27, [GEN_III_BWR[n][key] for n in names], 0.25,
                color=col, edgecolor="white", lw=0.8, label=lab)
    axL.set_xticks(xs)
    axL.set_xticklabels(names)
    axL.set_ylabel("component count")
    axL.legend(fontsize=8.5)
    axL.annotate("zero", xy=(2, 0.7), fontsize=11, color=ALT, ha="center")
    axL.set_title("Passive safety is not a better pump")

    axR.bar(xs - 0.2, [GEN_III_BWR[n]["electric_MW"] for n in names], 0.38,
            color=INK, edgecolor="white", lw=0.8, label="MW(e)")
    ax2 = axR.twinx()
    ax2.plot(xs, [100 * thermal_efficiency(GEN_III_BWR[n]["electric_MW"],
                                           GEN_III_BWR[n]["thermal_MW"])
                  for n in names], "o-", color=FLOW, lw=2.2, ms=9, label="efficiency")
    ax2.set_ylim(30, 40)
    ax2.set_ylabel("efficiency (%)", color=FLOW)
    axR.set_xticks(xs)
    axR.set_xticklabels(names)
    axR.set_ylabel("electric output MW(e)")
    axR.set_ylim(0, 1800)
    axR.annotate("+14% output,\nunchanged steam cycle", xy=(0.5, 1620),
                 fontsize=9, color=STEEL, ha="center")
    axR.set_title("...and the thermodynamics does not move")
    fig.tight_layout()
    _save(fig, "fig3_generation_iii.svg")
    caps["fig3_generation_iii.svg"] = (
        "S&F Table 11.4. Left: the real content of the Generation II-to-III transition is "
        "subtraction. The ABWR moves the recirculation pumps inside the vessel (2 external "
        "become 10 internal); the ESBWR deletes them entirely, along with every safety pump and "
        "every emergency diesel generator, by growing the vessel 27% taller so natural "
        "circulation drives the core flow. Right: meanwhile the steam cycle does not change at "
        "all -- all three sit between 34% and 35%, because all three are still limited by water. "
        "Generation III improved safety and economics; it did not improve thermodynamics.")

    # Fig 4 -- Gen IV, and the peaking factor context.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.0))
    order = sorted(GEN_IV_SYSTEMS, key=lambda k: GEN_IV_SYSTEMS[k]["outlet_C"])
    outs = [GEN_IV_SYSTEMS[k]["outlet_C"] for k in order]
    effs = [100 * GEN_IV_SYSTEMS[k]["efficiency"] for k in order]
    cols = [LEAF if "fast" in GEN_IV_SYSTEMS[k]["spectrum"] else STEEL for k in order]
    axL.scatter(outs, effs, s=140, c=cols, edgecolors="white", zorder=5)
    for k, o, e in zip(order, outs, effs):
        axL.annotate(k, xy=(o, e), xytext=(o + 12, e - 1.4), fontsize=9)
    tt = np.linspace(300, 1100, 200)
    axL.plot(tt, [100 * 0.75 * carnot_efficiency(x, 33.0) for x in tt],
             color=INK, lw=1.8, ls="--", label="75% of Carnot")
    axL.axhline(34, color=FLOW, lw=1.8, ls=":")
    axL.annotate("today's LWRs, 34%", xy=(330, 35), fontsize=9, color=FLOW)
    axL.axvline(WATER_CRITICAL_C, color=ALT, lw=1.6, ls=":")
    axL.set_xlabel("coolant outlet temperature ($^\\circ$C)")
    axL.set_ylabel("design efficiency (%)")
    axL.set_xlim(300, 1150)
    axL.set_ylim(28, 62)
    axL.legend(fontsize=8.5, loc="lower right")
    axL.set_title("Generation IV (green = fast spectrum)")

    labels = ["bare uniform\ncylinder\n(~NE-21)", "1970s BWR\n(Table 11.3)",
              "1970s PWR\n(Table 11.2)"]
    vals = [3.639, peaking_factor(BWR["heat_flux_max_MW_per_m2"],
                                  BWR["heat_flux_avg_MW_per_m2"]),
            peaking_factor(PWR["heat_flux_max_MW_per_m2"],
                           PWR["heat_flux_avg_MW_per_m2"])]
    bars = axR.barh(range(3), vals, 0.55, color=[ALT, FLOW, INK],
                    edgecolor="white", lw=0.8)
    for i, b in enumerate(bars):
        axR.text(b.get_width() + 0.06, b.get_y() + b.get_height() / 2,
                 "%.2f" % vals[i], va="center", fontsize=10)
    axR.set_yticks(range(3))
    axR.set_yticklabels(labels, fontsize=9)
    axR.set_xlabel("peak / average heat flux")
    axR.set_xlim(0, 4.3)
    axR.annotate("reflectors, fuel zoning\nand burnable poisons\nbuy this gap",
                 xy=(2.9, 1.0), fontsize=8.5, color=STEEL, ha="center")
    axR.set_title("Flattening the core is worth 46%")
    fig.tight_layout()
    _save(fig, "fig4_geniv_and_peaking.svg")
    caps["fig4_geniv_and_peaking.svg"] = (
        "Left: the six Generation IV systems of S&F §11.5, placed by coolant outlet temperature "
        "and design efficiency, against a 75%-of-Carnot line. Every one runs above water's "
        "critical temperature -- that is the point of them -- and every one therefore beats 34%. "
        "Note also that four of the six are fast-spectrum: that is a fuel-cycle argument "
        "(~NE-23), not a thermodynamic one, and the two goals are being pursued together. Right: "
        "the other side of the design problem. ~NE-21 derives 3.64 for a bare uniform cylinder; "
        "the real 1970s cores run 2.2 to 2.5, and since the hottest fuel pin limits the whole "
        "reactor, that flattening is worth 46% more saleable power from the same core.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
