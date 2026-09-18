"""QF-01 figures — Klein-Gordon dispersion & the UV-divergent vacuum energy.

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
from field_quantization import (                   # noqa: E402
    kg_dispersion, field_modes, vacuum_energy,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — Klein-Gordon dispersion omega_p = sqrt(p^2 + m^2) from kg_dispersion:
    # the massless field is the light cone omega=|p|; a mass opens a gap omega(0)=m
    # (the rest energy) and every massive branch asymptotes back to the light cone.
    p = np.linspace(0.0, 5.0, 400)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(p, kg_dispersion(p, 0.0), color=FLOW, lw=2.2,
            label=r"$m=0$:  $\omega_p=|p|$  (light cone)")
    for m, col in [(1.0, INK), (2.0, ALT)]:
        ax.plot(p, kg_dispersion(p, m), color=col, lw=2,
                label=fr"$m={m:.0f}$:  $\omega_p=\sqrt{{p^2+{m:.0f}^2}}$")
        ax.plot(0.0, m, marker="o", ms=5, color=col)             # rest energy omega(0)=m
        ax.annotate(fr"$\omega(0)=m={m:.0f}$", xy=(0.0, m), xytext=(0.18, m + 0.18),
                    color=col, fontsize=9)
    ax.set_xlim(0, 5); ax.set_ylim(0, 5.5)
    ax.set_xlabel(r"momentum magnitude $|p|$")
    ax.set_ylabel(r"frequency / energy $\omega_p$")
    ax.set_title(r"Klein-Gordon dispersion: a mass gaps the light cone $\omega_p=|p|$")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    _save(fig, "fig1_kg_dispersion.svg")
    caps["fig1_kg_dispersion.svg"] = (
        r"Klein-Gordon dispersion $\omega_p=\sqrt{p^2+m^2}$ from kg_dispersion for "
        r"$m=0,1,2$ (natural units $\hbar=c=1$). The massless field is the light cone "
        r"$\omega_p=|p|$ (orange); a mass opens a gap, so each massive branch starts at "
        r"the rest energy $\omega(0)=m$ and bends up to meet the light cone at large $|p|$.")

    # Fig 2 — the vacuum (zero-point) energy E_0 = (1/2) sum omega_p over box modes
    # |p| <= cutoff, from vacuum_energy: finite for any finite cutoff but growing like
    # Lambda^4 (the UV divergence). Dots are the module's own sum; dashed line is the
    # Lambda^4 power law pinned at the largest cutoff.
    cutoffs = np.array([2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0])
    E0 = np.array([vacuum_energy(0.0, float(L)) for L in cutoffs])
    nmodes = np.array([len(field_modes(float(L))) for L in cutoffs])
    Lam = np.geomspace(cutoffs[0], cutoffs[-1], 200)
    C = E0[-1] / cutoffs[-1] ** 4                                 # pin power law at last point

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(Lam, C * Lam ** 4, color=ALT, lw=1.8, ls="--",
            label=r"$\propto \Lambda^4$  (UV divergence)")
    ax.plot(cutoffs, E0, ls="none", marker="o", ms=5, color=INK,
            label=r"$E_0=\frac{1}{2}\sum_p \omega_p$  (massless field)")
    grow = E0[cutoffs == 16.0][0] / E0[cutoffs == 8.0][0]
    ax.annotate(fr"$\Lambda:8\to16$ grows $\times{grow:.1f}\approx2^4$",
                xy=(11.0, C * 11.0 ** 4), xytext=(2.4, 3e4),
                color=STEEL, fontsize=9)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel(r"momentum cutoff $\Lambda$")
    ax.set_ylabel(r"vacuum energy $E_0$")
    ax.set_title(r"Zero-point energy diverges in the UV: $E_0\sim\Lambda^4$")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig2_vacuum_energy_uv.svg")
    caps["fig2_vacuum_energy_uv.svg"] = (
        r"Regularized vacuum energy $E_0=\frac{1}{2}\sum_p\omega_p$ from vacuum_energy, "
        r"summing the half-quantum of every box mode $|p|\le\Lambda$ for a massless "
        r"field (dots; $n_{modes}$ grows from %d to %d). It is finite for any finite "
        r"cutoff but follows the power law $E_0\propto\Lambda^4$ (dashed): doubling "
        r"$\Lambda$ multiplies $E_0$ by $\approx2^4=16$ — the UV divergence tamed by "
        r"normal-ordering / renormalization." % (nmodes[0], nmodes[-1]))

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
