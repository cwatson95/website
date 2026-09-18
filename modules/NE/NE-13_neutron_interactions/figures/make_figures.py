"""NE-13 figures -- the 1/v law, the erratic isotope-to-isotope scatter,
resonance character by mass, and activation saturation.

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
from neutron_interactions import (                 # noqa: E402
    E_THERMAL_EV, V_THERMAL_CM_S,
    load_thermal_cross_sections, load_activation_data,
    absorption_cross_section, scattering_cross_section, fission_cross_section,
    one_over_v_cross_section, neutron_speed,
    activation_activity, saturation_activity, capture_to_fission_ratio,
    eta_neutrons_per_absorption,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    xs = load_thermal_cross_sections()

    # Fig 1 -- the 1/v law across eight decades.
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    e = np.logspace(-4, 3, 400)
    for nuc, col, ls in [("1H", FLOW, "-"), ("10B", LEAF, "--"), ("6Li", INK, "-.")]:
        s0 = absorption_cross_section(nuc, xs)
        ax.loglog(e, [one_over_v_cross_section(s0, x) for x in e],
                  color=col, lw=1.9, ls=ls, label="%s ($\\sigma_a$ = %.3g b)" % (nuc, s0))
    ax.axvline(E_THERMAL_EV, color=STEEL, ls=":", lw=1.4)
    ax.annotate("thermal\n0.0253 eV\n2200 m/s", xy=(E_THERMAL_EV, 2e2),
                xytext=(2e-3, 4e3), fontsize=8.5, color=STEEL,
                arrowprops=dict(arrowstyle="->", color=STEEL, lw=1.0))
    ax.set_xlabel("neutron energy (eV)")
    ax.set_ylabel("absorption cross section (b)")
    ax.set_xlim(1e-4, 1e3)
    ax.legend(fontsize=8.5, loc="upper right")
    ax.set_title("The 1/v law: slow neutrons are captured far more readily")
    _save(fig, "fig1_one_over_v.svg")
    caps["fig1_one_over_v.svg"] = (
        "Absorption cross section under the 1/v law (one_over_v_cross_section), anchored at "
        "the 0.0253 eV thermal point where Appendix C.1 is quoted. A neutron lingers near a "
        "nucleus in proportion to 1/v, so capture scales the same way: slowing a neutron from "
        "1 keV to thermal multiplies its capture probability by 199. This single fact is why "
        "moderation (NE-08) is worth 115 collisions in graphite.")

    # Fig 2 -- neutron cross sections are erratic; photon ones are not.
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    items = sorted(((v["A"], k, absorption_cross_section(k, xs)) for k, v in xs.items()),
                   key=lambda t: t[0])
    As = [a for a, _, _ in items]
    Ss = [max(s, 1e-6) for _, _, s in items]
    ax.semilogy(As, Ss, "o", color=STEEL, ms=6)
    for lab, dy, col in [("1H", 1.8, INK), ("2H", 0.25, INK), ("10B", 1.8, FLOW),
                         ("11B", 0.22, FLOW), ("12C", 0.25, LEAF), ("235U", 1.9, ALT),
                         ("238U", 0.3, ALT)]:
        A = xs[lab]["A"]
        s = max(absorption_cross_section(lab, xs), 1e-6)
        ax.annotate(lab, xy=(A, s), xytext=(A + 2, s * dy), fontsize=9, color=col)
        ax.plot([A], [s], "o", color=col, ms=7)
    for a, b, col in [("1H", "2H", INK), ("10B", "11B", FLOW), ("235U", "238U", ALT)]:
        ax.plot([xs[a]["A"], xs[b]["A"]],
                [max(absorption_cross_section(a, xs), 1e-6),
                 max(absorption_cross_section(b, xs), 1e-6)],
                color=col, lw=1.0, ls=":", alpha=0.7)
    ax.set_xlabel("mass number $A$")
    ax.set_ylabel("thermal absorption cross section (b)")
    ax.set_ylim(1e-6, 1e5)
    ax.set_title("Neighbouring isotopes differ by up to $10^6$")
    _save(fig, "fig2_erratic.svg")
    caps["fig2_erratic.svg"] = (
        "Thermal absorption cross section against mass number for all 27 nuclides of "
        "Appendix C.1 (absorption_cross_section). Compare NE-12, where photon coefficients "
        "follow smooth Z^4, Z and Z^2 laws. Here there is no trend at all: dotted lines join "
        "isotope pairs of the SAME element, and 1H/2H differ by 658x while 10B/11B differ by "
        "700000x. S&F are blunt that no predictive theory exists and all data are empirical -- "
        "which is why this module tabulates rather than models.")

    # Fig 3 -- resonance character shifts with mass.
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    bands = [("light\n$A<25$", 3e3, 2e7, LEAF, "keV-MeV wide,\nsparse; H and D none"),
             ("intermediate\n$25<A<150$", 1e2, 1e4, FLOW, "100 eV - keV"),
             ("heavy\n$A>150$", 1e0, 1e2, ALT, "eV region, <1 eV wide;\nunresolved above ~keV")]
    for i, (lab, lo, hi, col, note) in enumerate(bands):
        ax.barh([i], [hi - lo], left=[lo], color=col, height=0.5, alpha=0.75)
        ax.text(math.sqrt(lo * hi), i + 0.34, note, fontsize=8, color="0.25", ha="center")
    ax.axvline(E_THERMAL_EV, color=STEEL, ls=":", lw=1.4)
    ax.text(E_THERMAL_EV * 1.4, 2.42, "thermal", fontsize=8.5, color=STEEL, rotation=90)
    ax.axvline(2e6, color=INK, ls="--", lw=1.2)
    ax.text(2e6 * 1.3, 2.42, "fission mean", fontsize=8.5, color=INK, rotation=90)
    ax.set_xscale("log")
    ax.set_yticks(range(len(bands)))
    ax.set_yticklabels([b[0] for b in bands], fontsize=9)
    ax.set_xlabel("neutron energy (eV)")
    ax.set_xlim(1e-3, 2e7)
    ax.set_ylim(-0.6, 2.8)
    ax.set_title("Where the resonances live, by nuclide mass")
    _save(fig, "fig3_resonance_bands.svg")
    caps["fig3_resonance_bands.svg"] = (
        "Resonance energy ranges by nuclide class (resonance_character, S&F §7.4.1). Heavier "
        "nuclei have denser level schemes, so their resonances sit lower, closer together and "
        "narrower -- below 1 eV wide for A > 150, and unresolvable above a few keV. Note where "
        "the two vertical markers fall: a fission neutron is born at 2 MeV, above almost every "
        "resonance, and must be slowed through the heavy-nuclide resonance forest to reach "
        "thermal. Surviving that passage is the resonance-escape probability of NE-19.")

    # Fig 4 -- activation saturation, and where Example 7.5 sits on it.
    fig, ax = plt.subplots(figsize=(6.6, 3.8))
    act = load_activation_data()
    sigma = act["56Mn"]["sigma_b"]
    t_half = 2.579 * 3600.0
    sat = saturation_activity(2.0, 55.0, sigma, 1e13)
    t = np.linspace(0, 6 * t_half, 500)
    a = [activation_activity(2.0, 55.0, sigma, 1e13, x, t_half) / sat for x in t]
    ax.plot(t / t_half, a, color=INK, lw=2.1)
    ax.axhline(1.0, color="0.55", ls="--", lw=1.2)
    ax.text(3.4, 1.03, "saturation: activity = production rate", fontsize=9, color="0.35")
    for k, lab in [(1, "50%"), (2, "75%"), (5, "96.9%")]:
        ax.plot([k], [1 - 2.0 ** -k], "o", color=FLOW, ms=6)
        ax.annotate(lab, xy=(k, 1 - 2.0 ** -k), xytext=(k + 0.12, 1 - 2.0 ** -k - 0.09),
                    fontsize=9, color=FLOW)
    # Example 7.5 sits almost at the origin -- that is why its linear form works
    ax.plot([120.0 / t_half], [activation_activity(2.0, 55.0, sigma, 1e13, 120.0, t_half) / sat],
            "D", color=LEAF, ms=8)
    ax.annotate("S&F Example 7.5\n2 min = 0.9% of saturation\n(so $A\\simeq\\lambda R t$ is safe)",
                xy=(120.0 / t_half, 0.009), xytext=(0.55, 0.30), fontsize=8.5, color=LEAF,
                arrowprops=dict(arrowstyle="->", color=LEAF, lw=1.0))
    ax.set_xlabel("irradiation time (half-lives of the product)")
    ax.set_ylabel("activity / saturation activity")
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1.14)
    ax.set_title("Activation saturates; Example 7.5 barely starts")
    _save(fig, "fig4_activation.svg")
    caps["fig4_activation.svg"] = (
        "Buildup of induced activity toward saturation (activation_activity). The curve is "
        "NE-07's decay-with-production law: activity can never exceed the production rate, and "
        "five half-lives reaches 97% of it. The diamond marks S&F Example 7.5, which irradiates "
        "for 2 minutes against a 2.579 h half-life -- 0.9% of the way up. That is precisely why "
        "the book's linear approximation A = lambda R t is safe there, and why it overstates "
        "the exact answer by only lambda*t/2 = 0.45%.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
