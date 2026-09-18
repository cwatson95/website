"""NE-10 figures -- the Gamow peak, the fuel ranking, the stellar burning
ladder to iron, and fusion against fission per nucleon.

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
from fusion import (                               # noqa: E402
    FUSION_REACTIONS, HELIUM_BURNING, ADVANCED_BURNING, SUN,
    load_atomic_masses, q_value, gamow_energy, gamow_peak_energy,
    thermal_energy, temperature_for_energy, tunnelling_probability,
    reaction_product_energies, atomic_mass, M_N_U,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"

CHARGES = {"D+D->T+p": (1, 2, 1, 2), "D+D->3He+n": (1, 2, 1, 2),
           "D+T->4He+n": (1, 2, 1, 3), "D+3He->4He+p": (1, 2, 2, 3),
           "T+T->4He+2n": (1, 3, 1, 3), "p+6Li->4He+3He": (1, 1, 3, 6),
           "p+11B->3alpha": (1, 1, 5, 11)}


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    t = load_atomic_masses()

    # Fig 1 -- the Gamow peak: Maxwellian x tunnelling.
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    T = temperature_for_energy(0.010)              # 10 keV plasma
    kt = thermal_energy(T)
    e = np.linspace(0.001, 0.20, 900)              # MeV
    maxw = np.exp(-e / kt)
    tunn = np.array([tunnelling_probability(x, 1, 2, 1, 3) for x in e])
    prod = maxw * tunn
    ax.plot(e * 1e3, maxw / maxw.max(), color=STEEL, lw=1.9,
            label="Maxwellian  $e^{-E/kT}$")
    ax.plot(e * 1e3, tunn / tunn.max(), color=FLOW, lw=1.9,
            label="tunnelling  $e^{-\\sqrt{E_G/E}}$")
    ax.plot(e * 1e3, prod / prod.max(), color=INK, lw=2.4, label="product (Gamow peak)")
    e0 = gamow_peak_energy(T, 1, 2, 1, 3)
    ax.axvline(e0 * 1e3, color=INK, ls=":", lw=1.3)
    ax.axvline(kt * 1e3, color=STEEL, ls=":", lw=1.3)
    ax.annotate("$kT$ = 10 keV", xy=(kt * 1e3, 0.62), xytext=(24, 0.78),
                fontsize=9, color=STEEL,
                arrowprops=dict(arrowstyle="->", color=STEEL, lw=1.0))
    ax.annotate("$E_0$ = %.0f keV" % (e0 * 1e3), xy=(e0 * 1e3, 1.0),
                xytext=(58, 0.95), fontsize=9, color=INK,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
    ax.set_xlabel("centre-of-mass energy (keV)")
    ax.set_ylabel("relative rate (each curve normalised)")
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 1.12)
    ax.legend(fontsize=9)
    ax.set_title("D-T at 10 keV: fusion happens in a narrow window")
    _save(fig, "fig1_gamow_peak.svg")
    caps["fig1_gamow_peak.svg"] = (
        "Why fusion works far below the Coulomb barrier. Almost no particles have the "
        "~400 keV needed to climb it, and almost none of the abundant low-energy ones can "
        "tunnel; the reaction rate is the product of a falling Maxwellian and a rising "
        "Gamow factor (gamow_peak_energy), peaking at E_0 = 31 keV -- three times kT but "
        "a tenth of the barrier. Everything a star or a tokamak does happens in this "
        "narrow window.")

    # Fig 2 -- ranking the fuels: Q against difficulty.
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    labels = {"D+D->T+p": "D-D (p)", "D+D->3He+n": "D-D (n)", "D+T->4He+n": "D-T",
              "D+3He->4He+p": "D-$^3$He", "T+T->4He+2n": "T-T",
              "p+6Li->4He+3He": "p-$^6$Li", "p+11B->3alpha": "p-$^{11}$B"}
    for lab, (reac, prod_, qb) in FUSION_REACTIONS.items():
        eg = gamow_energy(*CHARGES[lab])
        q = q_value(reac, prod_, t)
        col = FLOW if lab == "D+T->4He+n" else (ALT if "11B" in lab else STEEL)
        mk = "*" if lab == "D+T->4He+n" else ("D" if "11B" in lab else "o")
        ax.plot([eg], [q], mk, color=col, ms=12 if mk == "*" else 8)
        ax.annotate(labels[lab], xy=(eg, q), xytext=(eg * 1.12, q + 0.7),
                    fontsize=9, color=col)
    ax.set_xscale("log")
    ax.set_xlabel("Gamow energy $E_G$ (MeV) -- how hard  $\\longrightarrow$")
    ax.set_ylabel("$Q$ (MeV) -- how much")
    ax.set_xlim(0.7, 60)
    ax.set_ylim(0, 22)
    ax.set_title("Why every experiment runs D-T")
    _save(fig, "fig2_fuel_ranking.svg")
    caps["fig2_fuel_ranking.svg"] = (
        "Energy release against difficulty for the candidate fusion fuels (q_value and "
        "gamow_energy). D-T (orange) sits in the top-left corner: nearly the largest Q "
        "with the smallest Gamow energy, which is why every experiment on earth uses it "
        "despite needing to breed its own tritium. D-3He releases more but is 4x harder; "
        "p-11B (purple) is aneutronic and therefore tempting, but its E_G of 22 MeV makes "
        "it 1e16 times less likely to tunnel at the same energy.")

    # Fig 3 -- the burning ladder up to iron.
    fig, ax = plt.subplots(figsize=(6.8, 3.9))
    chain = [(12, 6), (16, 8), (20, 10), (24, 12), (28, 14), (32, 16), (36, 18),
             (40, 20), (44, 22), (48, 24), (52, 26), (56, 28), (60, 30), (64, 32)]
    xs, ys, cols = [], [], []
    for i in range(len(chain) - 1):
        (A, Z), (A2, Z2) = chain[i], chain[i + 1]
        q = q_value([(4, 2), (A, Z)], [(A2, Z2)], t)
        xs.append(A2)
        ys.append(q)
        cols.append(LEAF if A2 <= 56 else STEEL)
    ax.bar(xs, ys, width=2.6, color=cols)
    ax.axvline(58, color=FLOW, ls="--", lw=1.6)
    ax.text(59, 8.6, "the iron peak\n($^{62}$Ni is the most bound)",
            fontsize=9, color=FLOW)
    ax.annotate("yield collapses by 3x\nat exactly the peak", xy=(60, 2.7),
                xytext=(30, 4.2), fontsize=9, color=STEEL,
                arrowprops=dict(arrowstyle="->", color=STEEL, lw=1.1))
    ax.set_xlabel("mass number of the product")
    ax.set_ylabel("$Q$ per $\\alpha$ capture (MeV)")
    ax.set_ylim(0, 11)
    ax.set_title("Alpha-capture burning: not forbidden past iron, just futile")
    _save(fig, "fig3_burning_ladder.svg")
    caps["fig3_burning_ladder.svg"] = (
        "Energy released by each alpha capture up the stellar burning ladder (q_value). "
        "The common statement that fusion 'stops being exoergic at iron' is not quite "
        "right -- 56Ni + alpha still releases 2.7 MeV. What happens is that the yield "
        "collapses by a factor of three exactly at the peak, so a star gains almost "
        "nothing per gram burned, while symmetric fusion (56Fe + 56Fe) does go endoergic "
        "and photodisintegration at 1e10 K starts running the whole ladder backwards.")

    # Fig 4 -- fusion vs fission per nucleon, and the D-T energy split.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 3.7))
    names = ["D-T\nfusion", "$^{235}$U\nfission", "chemical\n(C + O$_2$)"]
    per_nucleon = [q_value([(2, 1), (3, 1)], [(4, 2), (1, 0)], t) / 5.0,
                   200.0 / 236.0, 4.1e-6 / 1.0]
    axL.bar(range(3), per_nucleon, color=[FLOW, STEEL, LEAF], width=0.55)
    axL.set_yscale("log")
    axL.set_xticks(range(3))
    axL.set_xticklabels(names, fontsize=9)
    axL.set_ylabel("MeV per nucleon (log scale)")
    for i, v in enumerate(per_nucleon):
        axL.text(i, v * 1.6, "%.3g" % v, ha="center", fontsize=9, color="0.25")
    axL.set_ylim(1e-6, 40)
    axL.set_title("Energy density")

    q_dt = q_value([(2, 1), (3, 1)], [(4, 2), (1, 0)], t)
    ea, en = reaction_product_energies(q_dt, atomic_mass(4, 2, t), M_N_U)
    axR.barh([1], [ea], color=FLOW, height=0.5, label="$\\alpha$, 3.5 MeV: stays in the plasma")
    axR.barh([0], [en], color=STEEL, height=0.5, label="neutron, 14.1 MeV: leaves")
    axR.set_yticks([0, 1])
    axR.set_yticklabels(["$^1$n", "$^4$He"])
    axR.set_xlabel("kinetic energy (MeV)")
    axR.set_xlim(0, 16)
    axR.legend(fontsize=8.5, loc="lower right")
    axR.set_title("D-T: only 20% heats the plasma")
    fig.tight_layout()
    _save(fig, "fig4_energy_density.svg")
    caps["fig4_energy_density.svg"] = (
        "Left: energy per nucleon for D-T fusion, 235U fission and a chemical bond. "
        "Fusion beats fission by a factor of four and chemistry by a factor of a million. "
        "Right: the D-T products (reaction_product_energies) split inverse to their "
        "masses, so the alpha keeps only 3.5 of the 17.6 MeV. Since only the charged alpha "
        "stays confined, ignition requires that 20% alone to balance every loss channel -- "
        "the central difficulty of magnetic fusion.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
