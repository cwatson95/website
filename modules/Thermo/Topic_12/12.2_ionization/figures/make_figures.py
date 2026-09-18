"""Module 12.2 figures — the Saha ionization curve and how sharply it depends on
density, plus the equilibrium constant that governs CO2 dissociation.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
"""
import json
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
from ionization import (                          # noqa: E402
    EV, saha_ionization_fraction, saha_electron_density,
    thermal_debroglie_wavelength, quantum_concentration,
    equilibrium_constant_CO_oxidation, log10K_from_gibbs,
    gibbs_of_reaction, dissociation_extent_CO2,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — Saha for caesium-like (3.9 eV) and argon-like (15.76 eV) species.
    # The transition from neutral to ionized is very sharp in temperature, and
    # it moves with the ionization potential: this is the boundary between a hot
    # gas and a plasma.
    T = np.linspace(2000.0, 30000.0, 500)
    n_tot = 1e22                                    # m^-3

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    for chi, lab, c, ls in ((3.89, r"caesium, $\chi=3.89$ eV", INK, "-"),
                            (7.90, r"iron, $\chi=7.90$ eV", FLOW, "--"),
                            (15.76, r"argon, $\chi=15.76$ eV", ALT, ":")):
        x = np.array([saha_ionization_fraction(t, n_tot, chi) for t in T])
        ax.plot(T / 1000.0, x, color=c, lw=2.2, ls=ls, label=lab)
    ax.axhline(0.5, color="0.65", lw=1.0, ls="-.")
    ax.text(28.5, 0.53, "half ionized", fontsize=8.5, color="0.45", ha="right")
    ax.set_xlim(2, 30)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel(r"temperature (kK)    ($n_{tot}=10^{22}$ m$^{-3}$)")
    ax.set_ylabel(r"ionization fraction $x=n_e/n_{tot}$")
    ax.set_title(r"The Saha equation: where a gas becomes a plasma")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_saha_ionization.svg")
    caps["fig1_saha_ionization.svg"] = (
        r"The Saha equation gives the equilibrium ionization fraction of a gas in "
        r"local thermodynamic equilibrium (saha_ionization_fraction), and the "
        r"transition it predicts is startlingly sharp — a few thousand kelvin "
        r"takes a species from essentially neutral to essentially fully ionized. "
        r"The threshold tracks the ionization potential: at $10^{22}$ m$^{-3}$ "
        r"caesium is half ionized near "
        + "%.1f" % (T[int(np.argmin(abs(np.array([saha_ionization_fraction(t, n_tot, 3.89) for t in T]) - 0.5)))] / 1000.0) +
        r" kK while argon needs about "
        + "%.1f" % (T[int(np.argmin(abs(np.array([saha_ionization_fraction(t, n_tot, 15.76) for t in T]) - 0.5)))] / 1000.0) +
        r" kK. This is the same statistical-mechanical machinery as chemical "
        r"equilibrium, with the electron playing the part of a reaction product; "
        r"the link to the plasma-kinetics trunk (PK) runs through here.")

    # Fig 2 — the density dependence people find counter-intuitive: at FIXED
    # temperature a rarer gas is MORE ionized, because recombination needs two
    # particles to meet while ionization needs only one photon-equivalent.
    n_grid = np.logspace(18.0, 25.0, 300)

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    for Tv, c, ls in ((6000.0, INK, "-"), (8000.0, FLOW, "--"),
                      (10000.0, ALT, ":")):
        x = np.array([saha_ionization_fraction(Tv, n, 3.89) for n in n_grid])
        ax.semilogx(n_grid, x, color=c, lw=2.2, ls=ls,
                    label=r"$T=%.0f$ K" % Tv)
    ax.set_xlim(1e18, 1e25)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel(r"total number density $n_{tot}$ (m$^{-3}$)")
    ax.set_ylabel(r"ionization fraction $x$")
    ax.set_title(r"Thinner gas ionizes more readily (caesium, $\chi=3.89$ eV)")
    ax.legend(loc="lower left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6, which="both")
    _save(fig, "fig2_saha_density.svg")
    caps["fig2_saha_density.svg"] = (
        r"At fixed temperature a DILUTE gas is more ionized than a dense one — "
        r"the opposite of most people's intuition. The reason is in the "
        r"structure of the Saha right-hand side (saha_rhs): "
        r"$n_{i+1}n_e/n_i$ is a function of temperature only, so spreading the "
        r"same species thinner forces the ratio to be met with a larger "
        r"IONIZED fraction. Recombination requires an ion and an electron to "
        r"find each other, which becomes rare as density falls, while ionization "
        r"does not. The scale is set by the quantum concentration "
        r"$n_Q=(2\pi mk_BT/h^2)^{3/2}$ (quantum_concentration, "
        r"thermal_debroglie_wavelength) — "
        + "%.2e" % quantum_concentration(8000.0) + r" m$^{-3}$ at 8000 K. "
        r"The same reasoning drives dissociation equilibria: "
        r"equilibrium_constant_CO_oxidation and dissociation_extent_CO2 apply it "
        r"to CO$_2$ breaking up at flame temperatures, via "
        r"gibbs_of_reaction and log10K_from_gibbs.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
