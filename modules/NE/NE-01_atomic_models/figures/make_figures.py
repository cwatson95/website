"""NE-01 figures -- hydrogen energy levels with the emission series, and the
scattering evidence that killed the plum-pudding atom.

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
from atomic_models import (                        # noqa: E402
    M_P, bohr_energy, transition_wavelength, series_limit_wavelength,
    series_name, thomson_scattering_probability,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- the level diagram, with the first three series drawn as transitions.
    nmax = 7
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    for n in range(1, nmax + 1):
        E = bohr_energy(n)
        ax.hlines(E, 0.0, 1.0, color="0.35", lw=1.1)
        ax.text(1.02, E, "n=%d" % n, va="center", fontsize=9, color="0.3")
    ax.hlines(0.0, 0.0, 1.0, color="0.15", lw=1.6)
    ax.text(1.02, 0.0, r"$n=\infty$  (ionized)", va="center", fontsize=9)

    series = [(1, INK, 0.16), (2, FLOW, 0.46), (3, ALT, 0.76)]
    for n_lo, col, x in series:
        for k, n_hi in enumerate(range(n_lo + 1, n_lo + 4)):
            xx = x + 0.075 * k
            ax.annotate("", xy=(xx, bohr_energy(n_lo)), xytext=(xx, bohr_energy(n_hi)),
                        arrowprops=dict(arrowstyle="->", color=col, lw=1.3))
        lam = transition_wavelength(n_lo, n_lo + 1, nuclear_mass=M_P) * 1e9
        ax.text(x + 0.075, bohr_energy(n_lo) - 0.9,
                "%s\n%.0f nm" % (series_name(n_lo), lam),
                ha="center", va="top", fontsize=9, color=col)
    ax.set_ylim(-14.6, 1.6)
    ax.set_xlim(0, 1.32)
    ax.set_xticks([])
    ax.set_ylabel("energy (eV)")
    ax.set_title(r"Hydrogen levels $E_n=-13.606/n^2$ eV and the emission series")
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    _save(fig, "fig1_hydrogen_levels.svg")
    caps["fig1_hydrogen_levels.svg"] = (
        "Bohr energy levels of hydrogen, E_n = -13.606/n^2 eV (from bohr_energy), with "
        "the first three transitions of the Lyman, Balmer and Paschen series. Levels "
        "crowd toward the ionization limit at 0 eV, so the n=1 to n=2 jump alone costs "
        "75% of the 13.6 eV ionization energy.")

    # Fig 2 -- where each series sits in wavelength, against the visible band.
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    for i, (n_lo, col, _) in enumerate(series):
        lam = [transition_wavelength(n_lo, n, nuclear_mass=M_P) * 1e9
               for n in range(n_lo + 1, n_lo + 9)]
        ax.plot(lam, [i] * len(lam), "o", color=col, ms=5)
        ax.plot([series_limit_wavelength(n_lo) * 1e9], [i], "|", color=col, ms=16, mew=2)
        ax.text(lam[0] * 1.06, i + 0.16, series_name(n_lo), color=col, fontsize=9)
    ax.axvspan(380, 750, color="0.85", zorder=0)
    ax.text(530, 2.45, "visible", ha="center", fontsize=9, color="0.35")
    ax.set_xscale("log")
    ax.set_xlim(80, 3000)
    ax.set_ylim(-0.5, 2.7)
    ax.set_yticks([])
    ax.set_xlabel("wavelength (nm, log scale)")
    ax.set_title("Only the Balmer series falls in the visible")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    _save(fig, "fig2_series_wavelengths.svg")
    caps["fig2_series_wavelengths.svg"] = (
        "Emission lines of the first three hydrogen series (from transition_wavelength) "
        "on a log wavelength axis; the tick at the left end of each row is the series "
        "limit n->infinity. Lyman is entirely ultraviolet and Paschen entirely infrared, "
        "so only Balmer lines are visible to the eye.")

    # Fig 3 -- the plum-pudding prediction against the Geiger-Marsden measurement.
    phi = np.linspace(0, 180, 400)
    p = np.array([thomson_scattering_probability(a) for a in phi])
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.semilogy(phi, p, color=INK, lw=1.6, label=r"Thomson model  $e^{-\phi/\phi_m}$")
    ax.axhline(1.0 / 8000, color=FLOW, lw=1.4, ls="--",
               label="Geiger-Marsden: 1 alpha in 8000")
    ax.axvline(90, color="0.6", lw=1.0, ls=":")
    ax.annotate(r"$10^{35}$ too small at $90^\circ$",
                xy=(90, thomson_scattering_probability(90.0)), xytext=(96, 1e-25),
                arrowprops=dict(arrowstyle="->", color="0.35"), fontsize=9, color="0.25")
    ax.set_ylim(1e-45, 5)
    ax.set_xlim(0, 180)
    ax.set_xlabel(r"scattering angle $\phi$ (degrees)")
    ax.set_ylabel(r"$P(\geq\phi)$")
    ax.set_title("Why the plum-pudding atom failed")
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    _save(fig, "fig3_thomson_failure.svg")
    caps["fig3_thomson_failure.svg"] = (
        "Thomson-model probability of an alpha scattering by at least phi (from "
        "thomson_scattering_probability, phi_m = 1 degree) against the measured 1-in-8000 "
        "backscatter rate. At 90 degrees the model predicts 8e-40, wrong by 35 orders of "
        "magnitude -- the discrepancy that forced Rutherford's compact nucleus.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
