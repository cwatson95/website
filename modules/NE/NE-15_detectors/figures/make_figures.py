"""NE-15 figures -- the six operating regions of a gas detector, resolution
against carrier count, the scintillator trade-off, and a simulated spectrum.

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
from detectors import (                            # noqa: E402
    SEMICONDUCTORS, SCINTILLATORS_INORGANIC, GAS_W_VALUES, FANO_FACTORS,
    carriers_produced, intrinsic_resolution_percent, gas_multiplication,
    scintillator_photoelectrons, photopeak_resolution_percent,
    compare_resolution, FWHM_PER_SIGMA,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- resolution is 1/sqrt(N), and w is the only lever.
    fig, ax = plt.subplots(figsize=(6.8, 4.1))
    n = np.logspace(2, 6.2, 300)
    for F, col, ls, lab in [(1.0, STEEL, "--", "$F = 1$ (Poisson: gases, scintillators)"),
                            (0.13, FLOW, "-", "$F = 0.13$ (semiconductors)")]:
        ax.loglog(n, 100 * FWHM_PER_SIGMA * np.sqrt(F / n), color=col, lw=2.0,
                  ls=ls, label=lab)
    pts = [("Ge", carriers_produced(0.6617, 2.98), 0.13, FLOW, "o"),
           ("Si", carriers_produced(0.6617, 3.61), 0.115, FLOW, "s"),
           ("Ar gas", carriers_produced(0.6617, 26.4), 0.20, LEAF, "^"),
           ("NaI(Tl)", scintillator_photoelectrons(0.6617, "NaI(Tl)"), 1.0, ALT, "D"),
           ("BGO", scintillator_photoelectrons(0.6617, "BGO"), 1.0, ALT, "v")]
    for lab, nn, F, col, mk in pts:
        r = 100 * FWHM_PER_SIGMA * math.sqrt(F / nn)
        ax.plot([nn], [r], mk, color=col, ms=9)
        ax.annotate(lab, xy=(nn, r), xytext=(nn * 1.35, r * 1.18), fontsize=9, color=col)
    ax.set_xlabel("information carriers per 662 keV event")
    ax.set_ylabel("intrinsic FWHM (%)")
    ax.set_xlim(3e2, 2e6)
    ax.set_ylim(0.1, 20)
    ax.legend(fontsize=8.5, loc="upper right")
    ax.set_title("Everything is $1/\\sqrt{N}$")
    _save(fig, "fig1_resolution_vs_carriers.svg")
    caps["fig1_resolution_vs_carriers.svg"] = (
        "Intrinsic energy resolution against the number of information carriers "
        "(intrinsic_resolution_percent). Every detector sits on one of these two lines; the "
        "only thing that moves it is w, the energy cost per carrier. Germanium's 2.98 eV "
        "gives 220 000 carriers at 662 keV and 0.18% resolution; NaI(Tl) delivers ~4400 "
        "photoelectrons and 3.6%. The lower line is the Fano-suppressed semiconductor case, "
        "which S&F do not discuss -- see refs.md.")

    # Fig 2 -- gas multiplication and the six operating regions.
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    df = np.linspace(0, 0.985, 400)
    ax.semilogy(df, 1.0 / (1.0 - df), color=INK, lw=2.2)
    regions = [(0.0, 0.02, "ion\nchamber", STEEL),
               (0.02, 0.75, "proportional\ncounter", LEAF),
               (0.75, 0.96, "limited\nproportional", FLOW),
               (0.96, 1.0, "Geiger-\nMueller", ALT)]
    for lo, hi, lab, col in regions:
        ax.axvspan(lo, hi, color=col, alpha=0.10)
        ax.text((lo + hi) / 2, 2.5, lab, ha="center", fontsize=8.5, color=col)
    ax.axvline(1.0, color=INK, ls="--", lw=1.4)
    ax.annotate("$\\delta f = 1$: the avalanche\nself-sustains and all energy\ninformation is lost",
                xy=(0.985, 60), xytext=(0.42, 200), fontsize=9, color=INK,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.1))
    ax.set_xlabel("$\\delta f$  (feedback per avalanche)")
    ax.set_ylabel("gas multiplication $M/f$")
    ax.set_xlim(0, 1.05)
    ax.set_ylim(1, 1e3)
    ax.set_title("Gas detectors: one equation, four instruments")
    _save(fig, "fig2_gas_multiplication.svg")
    caps["fig2_gas_multiplication.svg"] = (
        "S&F Eq. (8.7), M = f/(1 - delta f), with the classical operating regions shaded. "
        "An ion chamber collects the primary ionization with no gain; a proportional counter "
        "multiplies it while keeping output proportional to deposited energy; past delta f = 1 "
        "the avalanche is self-sustaining and every pulse is identical, which is the "
        "Geiger-Mueller regime. The same gas and the same geometry give four different "
        "instruments depending only on the applied voltage -- and gas_multiplication() raises "
        "rather than returning a negative number past the divergence.")

    # Fig 3 -- the scintillator trade-off.
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    for name, d in SCINTILLATORS_INORGANIC.items():
        t = d["decay_ns"][0]
        y = d["photons_per_MeV"]
        modern = name.startswith("La") or name in ("LSO(Ce)", "YAP(Ce)", "YAG(Ce)")
        col = FLOW if modern else STEEL
        mk = "D" if modern else "o"
        ax.plot([t], [y], mk, color=col, ms=9)
        ax.annotate(name, xy=(t, y), xytext=(t * 1.12, y * 1.03), fontsize=8, color=col)
    ax.set_xscale("log")
    ax.set_xlabel("decay time (ns)  -- faster $\\longleftarrow$")
    ax.set_ylabel("light yield (photons/MeV)")
    ax.set_xlim(10, 2000)
    ax.set_ylim(0, 72000)
    ax.set_title("Scintillators: bright or fast, and occasionally both")
    _save(fig, "fig3_scintillator_tradeoff.svg")
    caps["fig3_scintillator_tradeoff.svg"] = (
        "S&F Table 8.1's twelve inorganic scintillators, light yield against decay time. The "
        "classical materials (circles) trade one for the other: CsI(Tl) is the brightest and "
        "among the slowest, BGO is dense but dim. The modern cerium-doped materials (diamonds) "
        "break the pattern -- LaBr3(Ce) is brighter than NaI AND fourteen times faster, which "
        "is why it displaced NaI wherever cost allows. Speed matters for coincidence timing "
        "in PET (NE-27) and for high count rates.")

    # Fig 4 -- what the resolution difference actually looks like.
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    lines = [(1.173, 1.0), (1.332, 1.0)]         # 60Co doublet
    e = np.linspace(1.05, 1.45, 2000)
    for lab, res_pct, col, ls, off in [("Ge (0.16%)", 0.16, FLOW, "-", 0.0),
                                       ("NaI(Tl) (6.5%)", 6.5, STEEL, "--", 0.0)]:
        y = np.zeros_like(e)
        for e0, amp in lines:
            sigma = (res_pct / 100.0) * e0 / FWHM_PER_SIGMA
            y += amp * np.exp(-0.5 * ((e - e0) / sigma) ** 2)
        ax.plot(e, y / y.max(), color=col, lw=2.0, ls=ls, label=lab)
    for e0 in (1.173, 1.332):
        ax.axvline(e0, color="0.85", lw=0.9, zorder=0)
    ax.set_xlabel("energy (MeV)")
    ax.set_ylabel("counts (normalised)")
    ax.set_xlim(1.05, 1.45)
    ax.set_ylim(0, 1.1)
    ax.legend(fontsize=9)
    ax.set_title("The $^{60}$Co doublet: resolved, or one bump")
    _save(fig, "fig4_spectrum_comparison.svg")
    caps["fig4_spectrum_comparison.svg"] = (
        "The practical meaning of the resolution numbers. 60Co emits two gammas 159 keV apart "
        "(NE-05). A germanium detector at 0.16% FWHM separates them completely; a NaI(Tl) "
        "detector at a realistic 6.5% merges them into a single feature from which neither "
        "energy can be read. Peak shapes are Gaussian because the carrier count is (S&F "
        "§8.6.2), with widths taken from this module's calculations. This is what a factor of "
        "forty in w buys, and why germanium spectrometers are worth their cryogenics.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
