"""NE-14 figures -- range vs energy for the three particle types, charged vs
neutral attenuation, the Bragg curve, and where bremsstrahlung takes over.

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
from charged_particles import (                    # noqa: E402
    csda_mass_range, csda_range, radiative_to_collisional,
    bremsstrahlung_crossover_energy, fission_fragment_range,
    RANGE_CONSTANTS_ELECTRON, DEPOSITION_FRACTIONS,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    e = np.logspace(-1, 1, 200)

    # Fig 1 -- range vs energy, three particles, in water.
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    for part, mat, lab, col, ls in [("electron", "water", "electron", STEEL, "-"),
                                    ("proton", "H2O", "proton", FLOW, "--"),
                                    ("alpha", "H2O", "alpha", ALT, "-.")]:
        ax.loglog(e, [csda_mass_range(part, mat, x) * 10.0 for x in e],
                  color=col, lw=2.0, ls=ls, label=lab)
    for y, lab in [(1e-3, "1 um"), (1e-2, "10 um"), (1e-1, "0.1 mm"), (1e0, "1 mm"),
                   (1e1, "1 cm")]:
        ax.axhline(y, color="0.88", lw=0.8, zorder=0)
    ax.set_xlabel("kinetic energy (MeV)")
    ax.set_ylabel("CSDA range in water (mm)")
    ax.set_xlim(0.1, 10)
    ax.set_ylim(1e-4, 60)
    ax.legend(fontsize=9, loc="upper left")
    ax.set_title("Range in water: four decades between alphas and electrons")
    _save(fig, "fig1_range_vs_energy.svg")
    caps["fig1_range_vs_energy.svg"] = (
        "CSDA range in water for the three charged particles (csda_mass_range, S&F "
        "Eq. 7.47 with Tables 7.2-7.3), over the 0.1-10 MeV window the fits are valid for. "
        "At the same energy an alpha stops in tens of microns, a proton in hundreds, an "
        "electron in millimetres -- the m/z^2 rule of §7.5.4 made visible. A 5 MeV alpha "
        "does not penetrate the dead layer of skin; the same alpha inhaled deposits all of "
        "that energy in a few cells (NE-18).")

    # Fig 2 -- the defining contrast: range vs exponential attenuation.
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    R = csda_range("alpha", "H2O", 5.0, 1.0) * 1e4          # microns
    s = np.linspace(0, 1.6 * R, 400)
    # idealised transmission for a heavy charged particle: flat, then straggling
    frac = 0.5 * (1.0 - np.tanh((s - R) / (0.035 * R)))
    ax.plot(s, frac, color=FLOW, lw=2.4, label="5 MeV alphas (a definite range)")
    mu_equiv = 1.0 / R                                       # same mean depth
    ax.plot(s, np.exp(-mu_equiv * s), color=STEEL, lw=2.0, ls="--",
            label="neutral particles ($e^{-\\mu x}$, same mean depth)")
    ax.axvline(R, color=INK, ls=":", lw=1.3)
    ax.annotate("range $R$ = %.0f $\\mu$m" % R, xy=(R, 0.5), xytext=(R * 0.42, 0.72),
                fontsize=9, color=INK,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
    ax.set_xlabel("depth into water ($\\mu$m)")
    ax.set_ylabel("fraction still travelling")
    ax.set_xlim(0, 1.6 * R)
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=8.5)
    ax.set_title("The defining difference: a range, not an exponential")
    _save(fig, "fig2_range_vs_exponential.svg")
    caps["fig2_range_vs_exponential.svg"] = (
        "Why charged particles need their own chapter. A beam of alphas is essentially "
        "unattenuated until the end of its range, then falls off abruptly over a few percent "
        "of the distance (straggling) -- S&F Fig. 7.12. A neutral beam with the same mean "
        "penetration follows exp(-mu x) and has no range at all: some fraction always gets "
        "through. Shielding a charged particle is a matter of thickness; shielding a photon "
        "is a matter of how much you are willing to let past (NE-11).")

    # Fig 3 -- the Bragg curve.
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    for e0, col, ls in [(2.5, LEAF, ":"), (5.0, FLOW, "-"), (10.0, INK, "--")]:
        R0 = csda_mass_range("alpha", "H2O", e0)
        depth = np.linspace(1e-4, R0 * 0.9995, 600)
        # invert the range-energy relation numerically to get E(depth), then -dE/ds
        grid_e = np.linspace(0.1, e0, 800)
        grid_r = np.array([R0 - csda_mass_range("alpha", "H2O", x) for x in grid_e])
        E_of_s = np.interp(depth, grid_r, grid_e)
        dEds = -np.gradient(E_of_s, depth)
        ax.plot(depth * 1e4 / 1.0, dEds / 1e4, color=col, lw=2.0, ls=ls,
                label="%.1f MeV" % e0)
    ax.set_xlabel("depth in water ($\\mu$m)")
    ax.set_ylabel("stopping power $-dE/ds$ (MeV/$\\mu$m$\\times 10^{-4}$)")
    ax.set_xlim(0, 130)
    ax.legend(fontsize=9, title="initial alpha energy", title_fontsize=8.5)
    ax.set_title("Bragg curves: the dose maximum is at the END")
    _save(fig, "fig3_bragg_curve.svg")
    caps["fig3_bragg_curve.svg"] = (
        "Stopping power against depth for alphas in water, reconstructed by differentiating "
        "the range-energy relation (csda_mass_range). Energy loss RISES as the particle slows "
        "and peaks just before it stops -- W.H. Bragg's 1904 observation. Everything about "
        "charged-particle dosimetry follows: the dose maximum is deep, it is sharp, and there "
        "is essentially nothing beyond it. That is the entire basis of proton and heavy-ion "
        "therapy (NE-27) and the reason an inhaled alpha emitter is far more damaging than "
        "the same activity outside the body (NE-18).")

    # Fig 4 -- bremsstrahlung crossover, and why beta shields are plastic.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.8, 3.8))
    Z = np.arange(1, 93)
    axL.semilogy(Z, [bremsstrahlung_crossover_energy(int(z)) for z in Z],
                 color=INK, lw=2.1)
    for lab, z, col, mk in [("C", 6, LEAF, "o"), ("Al", 13, FLOW, "s"),
                            ("Fe", 26, STEEL, "^"), ("Pb", 82, ALT, "D")]:
        ec = bremsstrahlung_crossover_energy(z)
        axL.plot([z], [ec], mk, color=col, ms=8)
        axL.annotate("%s  %.0f MeV" % (lab, ec), xy=(z, ec), xytext=(z + 3, ec * 1.25),
                     fontsize=9, color=col)
    axL.set_xlabel("atomic number $Z$ of the medium")
    axL.set_ylabel("crossover energy (MeV)")
    axL.set_xlim(0, 95)
    axL.set_title("Where radiation loss overtakes ionization")

    ee = np.linspace(0.1, 4.0, 200)
    for lab, z, col, ls in [("carbon", 6, LEAF, "-"), ("aluminium", 13, FLOW, "--"),
                            ("lead", 82, ALT, "-.")]:
        axR.plot(ee, [100 * radiative_to_collisional(x, z) for x in ee],
                 color=col, lw=2.0, ls=ls, label=lab)
    axR.set_xlabel("electron energy (MeV)")
    axR.set_ylabel("radiative loss (% of collisional)")
    axR.set_xlim(0, 4)
    axR.legend(fontsize=9)
    axR.set_title("Why a beta shield is plastic, not lead")
    fig.tight_layout()
    _save(fig, "fig4_bremsstrahlung.svg")
    caps["fig4_bremsstrahlung.svg"] = (
        "Left: the energy at which an electron loses as much to bremsstrahlung as to "
        "ionization (bremsstrahlung_crossover_energy, S&F Example 7.6) -- 700/Z MeV, so 117 "
        "MeV in carbon and 8.5 MeV in lead. Right: the radiative fraction below that. "
        "Shielding a 2 MeV beta with lead converts 23% of the energy into penetrating "
        "bremsstrahlung, against 1.7% in carbon -- which is why beta shields are built from "
        "plastic or aluminium first, with lead only behind them to catch the photons that "
        "are made anyway.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
