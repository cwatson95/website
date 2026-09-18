"""NE-25 figures -- specific power against half-life, the ZT penalty, the
Richardson exponential, and the flight record.

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
from direct_conversion import (                    # noqa: E402
    RADIONUCLIDE_SOURCES, SPACE_REACTORS, CONVERTER_TYPES, CI_TO_BQ,
    power_after, fuel_mass_for_power, carnot_efficiency,
    thermoelectric_efficiency, richardson_current, betavoltaic_power,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- specific power vs half-life, and decay.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.2))
    for nuc, v in RADIONUCLIDE_SOURCES.items():
        col = LEAF if v[5] == "alpha" else FLOW
        axL.loglog([v[0]], [v[3]], "o" if v[5] == "alpha" else "s",
                   color=col, ms=9)
        axL.annotate(nuc, xy=(v[0], v[3]), xytext=(v[0] * 1.15, v[3] * 1.15),
                     fontsize=8.5)
    axL.plot([], [], "o", color=LEAF, label="alpha emitter")
    axL.plot([], [], "s", color=FLOW, label="beta emitter")
    axL.axvspan(10, 200, color=ALT, alpha=0.12, lw=0)
    axL.annotate("useful for a\ndecades-long mission", xy=(45, 0.03),
                 fontsize=8.5, color=ALT, ha="center")
    axL.set_xlabel("half-life (years)")
    axL.set_ylabel("specific power (W/g)")
    axL.set_xlim(0.2, 400)
    axL.set_ylim(0.05, 400)
    axL.legend(fontsize=8.5, loc="upper right")
    axL.set_title("The trade that picks the isotope")

    years = np.linspace(0, 50, 300)
    for nuc, col, ls in (("210Po", ALT, ":"), ("242Cm", STEEL, "-."),
                         ("244Cm", FLOW, "--"), ("238Pu", INK, "-")):
        t12 = RADIONUCLIDE_SOURCES[nuc][0]
        axR.plot(years, [power_after(y, t12) for y in years], color=col, lw=2.2,
                 ls=ls, label="%s (%.1f y)" % (nuc, t12))
    axR.axvline(47, color=LEAF, ls=":", lw=1.6)
    axR.annotate("Voyager 1,\nlaunched 1977", xy=(47, 0.72), xytext=(28, 0.85),
                 fontsize=8.5, color=LEAF,
                 arrowprops=dict(arrowstyle="->", color=LEAF, lw=1.0))
    axR.set_xlabel("years after fuelling")
    axR.set_ylabel("fraction of initial thermal power")
    axR.set_ylim(0, 1.02)
    axR.legend(fontsize=8.5)
    axR.set_title("...and why it is 238Pu")
    fig.tight_layout()
    _save(fig, "fig1_isotope_choice.svg")
    caps["fig1_isotope_choice.svg"] = (
        "Left: S&F Table 12.2's nine practical thermal sources. Specific power spans a factor "
        "of 1500, and it is almost the wrong axis to read: 210Po's 144 W/g is unbeatable for a "
        "90-day mission and useless for anything longer, because specific power and half-life "
        "are inversely related by construction (both come from the same decay constant). Right: "
        "the consequence. After 47 years -- Voyager 1's age -- a 238Pu source retains 69% of its "
        "power while 210Po retains 1e-37 of it. By mass the curiums would beat 238Pu even on a "
        "30-year mission, but both are strong spontaneous-fission neutron emitters that lead "
        "cannot shield, which is why every outer-planet mission has flown plutonium.")

    # Fig 2 -- the ZT penalty.
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    zts = np.logspace(-1, 2, 300)
    for th, tc, col, ls in ((1300.0, 500.0, INK, "-"), (900.0, 400.0, FLOW, "--"),
                            (600.0, 350.0, LEAF, "-.")):
        etac = carnot_efficiency(th, tc)
        ax.semilogx(zts, [100 * thermoelectric_efficiency(z, th, tc) for z in zts],
                    color=col, lw=2.2, ls=ls,
                    label="%.0f K $\\to$ %.0f K (Carnot %.0f%%)" % (th, tc, 100 * etac))
        ax.axhline(100 * etac, color=col, lw=0.9, ls=":", alpha=0.6)
    ax.axvspan(0.8, 1.2, color=ALT, alpha=0.14, lw=0)
    ax.annotate("$ZT\\approx1$: what the best\nmaterials managed for decades",
                xy=(1.0, 42), fontsize=8.5, color=ALT, ha="center")
    ax.axhspan(5, 7, color=STEEL, alpha=0.16, lw=0)
    ax.annotate("a real RTG: 5-7%", xy=(12, 3.0), fontsize=9, color=STEEL)
    ax.set_xlabel("figure of merit $ZT$")
    ax.set_ylabel("thermoelectric efficiency (%)")
    ax.set_ylim(0, 65)
    ax.legend(fontsize=8.5, loc="upper left")
    ax.set_title("$\\eta = \\eta_C\\,\\frac{\\sqrt{1+ZT}-1}{\\sqrt{1+ZT}+T_c/T_h}$")
    _save(fig, "fig2_zt_penalty.svg")
    caps["fig2_zt_penalty.svg"] = (
        "The thermoelectric efficiency relation, which S&F quote results from (5-10%) but never "
        "write down. The dotted lines are the Carnot limits for each temperature pair; the "
        "curves approach them only as ZT goes to infinity. At ZT = 1 -- the plateau the best "
        "materials sat on for decades -- the penalty factor is 0.23, so a 61%-Carnot temperature "
        "difference yields a 14% device, and a real RTG with worse temperatures and parasitic "
        "heat leaks lands at 5-7%. That factor of five is the entire reason direct conversion is "
        "a niche technology rather than a replacement for the turbine.")

    # Fig 3 -- the Richardson exponential, and the converter landscape.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.0))
    temps = np.linspace(600, 2400, 300)
    for phi, col, ls in ((1.8, LEAF, "-."), (2.5, INK, "-"), (3.2, FLOW, "--")):
        axL.semilogy(temps, [richardson_current(t, phi) for t in temps],
                     color=col, lw=2.2, ls=ls, label="$\\phi$ = %.1f eV" % phi)
    axL.axvline(1400, color=ALT, ls=":", lw=1.8)
    axL.annotate("S&F: 'in excess\nof 1400 K'", xy=(1430, 1e-6), fontsize=8.5,
                 color=ALT)
    axL.axhline(1.0, color="0.75", lw=1.0)
    axL.annotate("1 A/cm$^2$", xy=(650, 1.6), fontsize=8.5, color="0.4")
    axL.set_xlabel("emitter temperature (K)")
    axL.set_ylabel("$J = AT^2e^{-\\phi/kT}$  (A/cm$^2$)")
    axL.set_ylim(1e-12, 1e5)
    axL.legend(fontsize=8.5, loc="lower right")
    axL.set_title("Ten decades for a factor of 2 in $T$")

    names = list(CONVERTER_TYPES)
    lows = [100 * CONVERTER_TYPES[k]["efficiency"][0] for k in names]
    highs = [100 * CONVERTER_TYPES[k]["efficiency"][1] for k in names]
    ys = np.arange(len(names))
    cols = [LEAF if CONVERTER_TYPES[k]["heat_engine"] else ALT for k in names]
    for i, k in enumerate(names):
        axR.barh([i], [highs[i] - lows[i]], 0.55, left=[lows[i]], color=cols[i],
                 edgecolor="white", lw=0.8,
                 hatch="///" if CONVERTER_TYPES[k]["moving_parts"] else "")
        axR.text(highs[i] + 0.8, i, "%.0f-%.0f%%" % (lows[i], highs[i]),
                 va="center", fontsize=8.5)
    axR.axvline(34, color=INK, ls="--", lw=1.8)
    axR.annotate("an LWR turbine\n(~NE-22)", xy=(34.6, 1.4), fontsize=8.5, color=INK)
    axR.set_yticks(ys)
    axR.set_yticklabels(names, fontsize=9)
    axR.set_xlabel("conversion efficiency (%)")
    axR.set_xlim(0, 44)
    axR.set_title("Green = heat engine; hatched = moving parts")
    fig.tight_layout()
    _save(fig, "fig3_converters.svg")
    caps["fig3_converters.svg"] = (
        "Left: the Richardson law, which S&F's §12.6.1 rests on without stating. It is why "
        "'emitter temperatures typically in excess of 1400 K' is a requirement and not a "
        "preference: the emission current rises ten orders of magnitude between 800 K and 1800 K, "
        "so there is no such thing as a low-temperature thermionic converter. It is also why "
        "caesium coatings matter -- dropping the work function from 2.5 to 1.8 eV buys a factor "
        "of 200. Right: the conversion landscape. Four of the five are still heat engines bound "
        "by Carnot; only the betavoltaic escapes, and it pays in microwatts. Every one is well "
        "below the turbine an LWR uses, and that is the price of having no moving parts.")

    # Fig 4 -- the flight record.
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    for k, v in SPACE_REACTORS.items():
        eta = 100 * v["kwe"] / v["kwt"]
        sm = v["mass_kg"] / v["kwe"]
        col = LEAF if v["flights"] > 0 else FLOW
        size = 60 + 22 * math.sqrt(v["flights"])
        ax.scatter([eta], [sm], s=size, c=col, edgecolors="white", zorder=5)
        ax.annotate("%s\n(%d flights)" % (k, v["flights"]), xy=(eta, sm),
                    xytext=(eta + 0.12, sm * 1.18), fontsize=8.5)
    ax.set_yscale("log")
    ax.set_xlabel("conversion efficiency (%)")
    ax.set_ylabel("specific mass (kg per kW(e))")
    ax.set_xlim(0.8, 6.2)
    ax.set_ylim(30, 1400)
    ax.plot([], [], "o", color=LEAF, label="flew")
    ax.plot([], [], "o", color=FLOW, label="never flew")
    ax.legend(fontsize=9)
    ax.set_title("S&F Table 12.3: the space reactor record")
    _save(fig, "fig4_space_reactors.svg")
    caps["fig4_space_reactors.svg"] = (
        "S&F Table 12.3, plotted by the two figures of merit that matter for a launch: how "
        "efficiently the reactor's heat becomes electricity, and how many kilograms each "
        "kilowatt costs. Marker area scales with flights flown. The shape of the programme is "
        "visible in one glance -- BUK flew 31 times at 3% efficiency and 310 kg/kW(e), while "
        "SP-100, the best design on both axes by a wide margin (5%, 54 kg/kW(e), 100 kW(e)), "
        "never flew at all. Every system here converts at 1-5%, an order of magnitude below the "
        "LWR turbine of ~NE-22, which is what having no moving parts costs.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
