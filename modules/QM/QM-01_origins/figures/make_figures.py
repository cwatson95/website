"""QM-01 figures — Planck's law vs the UV catastrophe, and the hydrogen spectrum.

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
import matplotlib.ticker as mticker                 # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from origins import (                              # noqa: E402
    planck_u_nu, rayleigh_jeans_u_nu, wien_u_nu,
    rydberg_wavelength, wien_displacement_b, c,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — black-body radiation: Planck's law (finite, peaked) for three
    # temperatures vs the classical Rayleigh-Jeans law that diverges (the UV
    # catastrophe).  All curves from the module's own planck_u_nu / rayleigh_jeans.
    nu = np.linspace(1e12, 1.6e15, 1400)            # frequency [Hz]
    nu14 = nu / 1e14
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    temps = [(4000.0, STEEL), (5800.0, INK), (7000.0, FLOW)]
    peak = 0.0
    for T, col in temps:
        u = np.array([planck_u_nu(v, T) for v in nu])
        peak = max(peak, u.max())
        lam_pk = wien_displacement_b() / T * 1e9    # Wien displacement (peak wavelength)
        ax.plot(nu14, u, color=col, lw=2,
                label=fr"Planck $T={T:.0f}$ K  ($\lambda_{{max}}={lam_pk:.0f}$ nm)")
    rj = np.array([rayleigh_jeans_u_nu(v, 5800.0) for v in nu])
    ax.plot(nu14, rj, color="#999999", lw=1.8, ls="--",
            label="Rayleigh-Jeans (5800 K)")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 1.35 * peak)
    ax.annotate("UV catastrophe\n(classical $\\propto\\nu^2$)", xy=(11.5, 1.18 * peak),
                color="#777777", fontsize=9, ha="center")
    ax.set_xlabel(r"frequency $\nu$  ($10^{14}$ Hz)")
    ax.set_ylabel(r"spectral energy density $u(\nu,T)$")
    ax.set_title(r"Planck's law tames the UV catastrophe: $u=\frac{8\pi h\nu^3/c^3}{e^{h\nu/k_BT}-1}$")
    ax.legend(loc="upper right", frameon=False, fontsize=8.5)
    _save(fig, "fig1_blackbody_uv_catastrophe.svg")
    caps["fig1_blackbody_uv_catastrophe.svg"] = (
        r"Black-body spectral energy density $u(\nu,T)$ from planck_u_nu at "
        r"$T=4000,5800,7000$ K: each curve peaks and rolls over, the peak sliding "
        r"to higher $\nu$ (shorter $\lambda_{max}$, Wien displacement) and the area "
        r"growing as $T^4$ (Stefan-Boltzmann). The classical Rayleigh-Jeans law "
        r"(dashed) instead diverges as $\nu^2$ — the ultraviolet catastrophe that "
        r"Planck's energy quantum $E=h\nu$ removed.")

    # Fig 2 — the hydrogen line spectrum (Bohr / Rydberg): a stick spectrum of the
    # Lyman, Balmer and Paschen series, every wavelength from rydberg_wavelength.
    series = [
        ("Lyman ($n_1{=}1$, UV)",      1, INK),
        ("Balmer ($n_1{=}2$, visible)", 2, FLOW),
        ("Paschen ($n_1{=}3$, IR)",    3, ALT),
    ]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.axvspan(380, 750, color="#f1e8c8", alpha=0.7, lw=0)   # the visible band
    ax.text(np.sqrt(380 * 750), 1.07, "visible", color="#9a8a3a",
            fontsize=9, ha="center")
    for label, n1, col in series:
        lams = [rydberg_wavelength(n1, n2) * 1e9 for n2 in range(n1 + 1, n1 + 7)]
        ax.vlines(lams, 0, 1.0, color=col, lw=1.8, label=label)
        limit = rydberg_wavelength(n1, 100000) * 1e9        # series limit n2 -> inf
        ax.vlines(limit, 0, 0.55, color=col, lw=1.0, ls=":")
    halpha = rydberg_wavelength(2, 3) * 1e9                  # Balmer H-alpha (red)
    ax.annotate(fr"H$\alpha$ {halpha:.0f} nm", xy=(halpha, 1.0), xytext=(halpha, 1.18),
                color=FLOW, fontsize=9, ha="center",
                arrowprops=dict(arrowstyle="-", color=FLOW, lw=0.8))
    ax.set_xscale("log")
    ax.set_xlim(80, 2200)
    ax.set_ylim(0, 1.35)
    ax.set_xticks([100, 200, 400, 700, 1000, 2000])
    ax.get_xaxis().set_major_formatter(mticker.ScalarFormatter())
    ax.set_yticks([])
    ax.set_xlabel(r"wavelength $\lambda$ (nm, log scale)")
    ax.set_title(r"Hydrogen spectrum (Rydberg): $1/\lambda=R(1/n_1^2-1/n_2^2)$")
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    _save(fig, "fig2_hydrogen_spectrum.svg")
    caps["fig2_hydrogen_spectrum.svg"] = (
        r"The hydrogen emission spectrum as a stick plot, every line placed by "
        r"rydberg_wavelength$(n_1,n_2)$. The three lowest series — Lyman "
        r"($n_1{=}1$, ultraviolet), Balmer ($n_1{=}2$, straddling the visible band) "
        r"and Paschen ($n_1{=}3$, infrared) — each converge to a series limit "
        r"(dotted) as $n_2\to\infty$. Bohr's quantized levels $E_n\propto-1/n^2$ "
        r"reproduce the observed lines, e.g. the red Balmer H$\alpha$ at 656 nm.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
