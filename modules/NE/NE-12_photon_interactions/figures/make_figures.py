"""NE-12 figures -- the three processes and their domains, the lead K edge,
Compton kinematics, and interaction vs deposition.

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
from photon_interactions import (                  # noqa: E402
    M_E_C2_MEV, TWO_ME_C2_MEV, MATERIALS, K_EDGE_KEV,
    load_photon_coefficients, mass_coefficient,
    compton_scattered_energy, compton_electron_energy,
    compton_edge, backscatter_energy,
    klein_nishina_mass_coefficient, crossover_energies,
    energy_transfer_fraction,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _curve(material, comp):
    """(E, mu/rho) with edge duplicates split so the discontinuity draws sharply."""
    rows = load_photon_coefficients(material)
    xs, ys = [], []
    for i, (e, d) in enumerate(rows):
        ee = e
        if i and rows[i - 1][0] == e:            # upper branch of an edge
            ee = e * (1 + 1e-9)
        xs.append(ee)
        ys.append(d[comp])
    return xs, ys


def main():
    caps = {}

    # Fig 1 -- the three processes in lead, with their domains shaded.
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    for comp, col, lab in [("ph", FLOW, "photoelectric  ($\\sim Z^4/E^3$)"),
                           ("c", STEEL, "Compton  ($\\sim Z/E$)"),
                           ("pp", LEAF, "pair production  ($\\sim Z^2$)")]:
        xs, ys = _curve("lead", comp)
        pts = [(x, y) for x, y in zip(xs, ys) if y > 0]
        ax.loglog([p[0] for p in pts], [p[1] for p in pts], color=col, lw=2.0, label=lab)
    xs, ys = _curve("lead", "total")
    ax.loglog(xs, ys, color=INK, lw=1.3, ls="--", label="total")
    lo, hi = crossover_energies("lead")
    ax.axvspan(1e-3, lo, color=FLOW, alpha=0.07)
    ax.axvspan(lo, hi, color=STEEL, alpha=0.07)
    ax.axvspan(hi, 20, color=LEAF, alpha=0.07)
    ax.axvline(TWO_ME_C2_MEV, color="0.5", lw=1.0, ls=":")
    ax.text(1.05, 2.5e-3, "1.022 MeV\nthreshold", fontsize=8, color="0.4")
    ax.annotate("K edge, 88 keV", xy=(0.088, 7.32), xytext=(0.012, 0.6),
                fontsize=9, color=FLOW,
                arrowprops=dict(arrowstyle="->", color=FLOW, lw=1.1))
    ax.set_xlabel("photon energy (MeV)")
    ax.set_ylabel("$\\mu/\\rho$  (cm$^2$/g)")
    ax.set_xlim(1e-3, 20)
    ax.set_ylim(1e-3, 5e3)
    ax.legend(fontsize=8.5, loc="upper right")
    ax.set_title("Lead: three processes, three domains")
    _save(fig, "fig1_three_processes.svg")
    caps["fig1_three_processes.svg"] = (
        "The three photon interaction processes in lead (mass_coefficient), each dominating "
        "its own band. The photoelectric effect falls as roughly E^-3 and carries the sawtooth "
        "absorption edges; Compton scattering is broad and flat; pair production is identically "
        "zero below 1.022 MeV and rises thereafter. The dashed total is what NE-11's "
        "exponential attenuation actually uses -- this figure is what is inside it.")

    # Fig 2 -- the K edge, and why contrast agents work.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.8, 3.8))
    xs, ys = _curve("lead", "ph")
    axL.loglog(xs, ys, color=FLOW, lw=2.0)
    for e, lab in [(0.088, "K"), (0.01586, "L1"), (0.01520, "L2"), (0.01304, "L3")]:
        axL.axvline(e, color="0.75", lw=0.9, ls=":")
    axL.annotate("K", xy=(0.088, 7.32), xytext=(0.11, 20), fontsize=10, color=INK)
    axL.annotate("L$_{1,2,3}$", xy=(0.0152, 145), xytext=(0.020, 400), fontsize=10, color=INK)
    axL.annotate("M$_{1..5}$", xy=(0.003, 2000), xytext=(0.0012, 300), fontsize=10, color=INK)
    axL.set_xlabel("photon energy (MeV)")
    axL.set_ylabel("$\\mu_{ph}/\\rho$  (cm$^2$/g)")
    axL.set_xlim(1e-3, 1.0)
    axL.set_title("Lead photoelectric: nine edges")

    pair = [r for r in load_photon_coefficients("lead") if abs(r[0] - 0.088) < 1e-6]
    below, above = sorted(pair, key=lambda r: r[1]["total"])
    labels = ["$\\mu$\n(interactions)", "$\\mu_{en}$\n(energy deposited)"]
    x = np.arange(2)
    axR.bar(x - 0.2, [below[1]["total"], below[1]["en"]], 0.4,
            color=STEEL, label="just below (87.9 keV)")
    axR.bar(x + 0.2, [above[1]["total"], above[1]["en"]], 0.4,
            color=FLOW, label="just above (88.1 keV)")
    for i, (b, a) in enumerate([(below[1]["total"], above[1]["total"]),
                                (below[1]["en"], above[1]["en"])]):
        axR.text(i - 0.2, b + 0.15, "%.2f" % b, ha="center", fontsize=8.5, color="0.3")
        axR.text(i + 0.2, a + 0.15, "%.2f" % a, ha="center", fontsize=8.5, color="0.3")
    axR.set_xticks(x)
    axR.set_xticklabels(labels, fontsize=9)
    axR.set_ylabel("cm$^2$/g")
    axR.legend(fontsize=8.5)
    axR.set_title("Across the K edge: $f$ falls 0.90 $\\to$ 0.29")
    fig.tight_layout()
    _save(fig, "fig2_k_edge.svg")
    caps["fig2_k_edge.svg"] = (
        "Left: lead's photoelectric coefficient showing all nine absorption edges (K, L1-L3, "
        "M1-M5) recovered from Appendix C.3. Right: what happens across the K edge. The total "
        "coefficient jumps 4.5x because two more electrons become available, but the energy "
        "ABSORPTION coefficient rises only 1.5x -- so the deposited fraction collapses from "
        "0.90 to 0.29. The K vacancy emits a 75-85 keV fluorescence x-ray that escapes with "
        "the energy: more interactions, less deposition, and the origin of detector escape "
        "peaks.")

    # Fig 3 -- Compton kinematics.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.8, 3.8))
    deg = np.linspace(0, 180, 361)
    th = np.radians(deg)
    for e, lab, col, ls in [(0.14051, "$^{99m}$Tc, 140 keV", LEAF, "-"),
                           (0.6617, "$^{137}$Cs, 662 keV", FLOW, "--"),
                           (1.3325, "$^{60}$Co, 1.33 MeV", STEEL, "-."),
                           (6.129, "$^{16}$N, 6.13 MeV", ALT, ":")]:
        axL.plot(deg, [compton_scattered_energy(e, t) / e for t in th], color=col,
                 lw=1.9, ls=ls, label=lab)
    axL.set_xlabel("scattering angle (degrees)")
    axL.set_ylabel("$E'/E$")
    axL.set_xlim(0, 180)
    axL.set_ylim(0, 1.02)
    axL.set_xticks([0, 45, 90, 135, 180])
    axL.legend(fontsize=8)
    axL.set_title("Harder photons lose relatively more")

    e = 0.6617
    axR.plot(deg, [compton_electron_energy(e, t) * 1e3 for t in th], color=INK, lw=2.1)
    axR.axhline(compton_edge(e) * 1e3, color=FLOW, ls="--", lw=1.4)
    axR.axhline(backscatter_energy(e) * 1e3, color=STEEL, ls=":", lw=1.4)
    axR.annotate("Compton edge, %.0f keV" % (compton_edge(e) * 1e3),
                 xy=(150, compton_edge(e) * 1e3), xytext=(38, 400),
                 fontsize=9, color=FLOW,
                 arrowprops=dict(arrowstyle="->", color=FLOW, lw=1.0))
    axR.annotate("backscatter photon, %.0f keV" % (backscatter_energy(e) * 1e3),
                 xy=(150, backscatter_energy(e) * 1e3), xytext=(20, 240),
                 fontsize=9, color=STEEL,
                 arrowprops=dict(arrowstyle="->", color=STEEL, lw=1.0))
    axR.set_xlabel("scattering angle (degrees)")
    axR.set_ylabel("electron kinetic energy (keV)")
    axR.set_xlim(0, 180)
    axR.set_ylim(0, 700)
    axR.set_xticks([0, 45, 90, 135, 180])
    axR.set_title("$^{137}$Cs: what the detector sees")
    fig.tight_layout()
    _save(fig, "fig3_compton.svg")
    caps["fig3_compton.svg"] = (
        "Left: the fraction of its energy a photon keeps on Compton scattering "
        "(compton_scattered_energy). The curves depend on energy and angle only -- never on "
        "the material -- because the target is a free electron. Right: the recoil-electron "
        "energy for 137Cs, whose maximum at 180 degrees is the 477 keV Compton edge seen in "
        "every gamma spectrum. The 184 keV backscatter photon is the complement, and the two "
        "sum to 662 keV.")

    # Fig 4 -- interaction is not deposition.
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    for m, col, ls in [("water", STEEL, "-"), ("iron", ALT, "--"), ("lead", FLOW, "-.")]:
        rows = load_photon_coefficients(m)
        es = sorted({e for e, _ in rows if 0.01 <= e <= 20})
        fs = []
        keep = []
        for e in es:
            try:
                fs.append(energy_transfer_fraction(m, e))
                keep.append(e)
            except ValueError:
                pass
        ax.semilogx(keep, fs, color=col, lw=2.0, ls=ls, label=m)
    ax.axhline(1.0, color="0.6", lw=1.0, ls="--")
    ax.annotate("K-edge fluorescence\nescapes with the energy", xy=(0.09, 0.30),
                xytext=(0.14, 0.10), fontsize=8.5, color=FLOW,
                arrowprops=dict(arrowstyle="->", color=FLOW, lw=1.0))
    ax.set_xlabel("photon energy (MeV)")
    ax.set_ylabel("$f = \\mu_{en}/\\mu$")
    ax.set_xlim(0.01, 20)
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=9, loc="lower right")
    ax.set_title("Interacting is not depositing")
    _save(fig, "fig4_transfer_fraction.svg")
    caps["fig4_transfer_fraction.svg"] = (
        "The fraction of an interacting photon's energy actually left behind "
        "(energy_transfer_fraction). It is far below 1 through the Compton region, because "
        "the scattered photon leaves carrying most of the energy -- the gap that buildup "
        "factors (NE-11) and dose conversion (NE-17) exist to handle. Lead's sharp dip just "
        "above 88 keV is K-fluorescence escape. Only at low energy in high-Z material, where "
        "the photoelectric effect absorbs outright, does f approach 1.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
