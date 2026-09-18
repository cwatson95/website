"""QM-18 figures — the hard-sphere "factor of 4" and Born/Yukawa -> Rutherford.

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
from scattering import (                           # noqa: E402
    phase_shifts_hard_sphere, total_cross_section,
    hard_sphere_phase_shift, partial_cross_section,
    born_amplitude_yukawa, rutherford_cross_section,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the hard-sphere "factor of 4": total cross-section vs ka.
    # sigma/(pi a^2) from total_cross_section(phase_shifts_hard_sphere(...)) runs
    # from 4 (long-wavelength wave diffracts off the WHOLE surface) at ka->0 down
    # toward 2 at high energy; the s-wave (partial_cross_section, l=0) carries it
    # all at low energy then dies off as higher l switch on.
    a = 1.0
    ka = np.linspace(0.05, 8.0, 240)
    lmax = 30                                       # plenty across the whole range
    sig = np.empty_like(ka)
    s0 = np.empty_like(ka)
    for i, x in enumerate(ka):
        k = x / a
        ds = phase_shifts_hard_sphere(k, a, lmax)
        sig[i] = total_cross_section(k, ds) / (math.pi * a ** 2)
        s0[i] = partial_cross_section(0, k, hard_sphere_phase_shift(0, k, a)) / (math.pi * a ** 2)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(ka, sig, color=INK, lw=2.2, label=r"$\sigma$ (all $\ell$)")
    ax.plot(ka, s0, color=FLOW, lw=2, ls="--", label=r"$s$-wave only ($\ell=0$)")
    ax.axhline(4.0, color="#888888", lw=1.0, ls=":")
    ax.axhline(2.0, color="#888888", lw=1.0, ls=":")
    ax.axhline(1.0, color="#cccccc", lw=0.8)
    ax.annotate(r"$4\pi a^2$  (wave, $ka\to0$)", xy=(2.2, 4.06), color=INK, fontsize=9)
    ax.annotate(r"$2\pi a^2$  (high energy)", xy=(4.6, 2.07), color="#555555", fontsize=9)
    ax.annotate(r"$\pi a^2$  (classical shadow)", xy=(4.6, 1.07), color="#777777", fontsize=9)
    ax.set_xlim(0, 8); ax.set_ylim(0, 4.4)
    ax.set_xlabel(r"$ka$  (size / wavelength)")
    ax.set_ylabel(r"$\sigma\,/\,\pi a^2$")
    ax.set_title(r"Hard sphere: $\sigma\to4\pi a^2$ at low energy (the factor of 4)")
    ax.legend(loc="center right", frameon=False)
    _save(fig, "fig1_hard_sphere_factor4.svg")
    caps["fig1_hard_sphere_factor4.svg"] = (
        r"Hard-sphere total cross-section (in units of the geometric disc $\pi a^2$) "
        r"vs $ka$, from total_cross_section of phase_shifts_hard_sphere. As $ka\to0$ "
        r"it tends to $4\pi a^2$ — FOUR times the classical shadow $\pi a^2$: a "
        r"long-wavelength wave diffracts off the whole surface, and the $s$-wave "
        r"($\ell=0$, dashed) carries all of it. At high energy ever more partial "
        r"waves switch on and $\sigma$ settles toward $2\pi a^2$.")

    # Fig 2 — Born approximation: Yukawa differential cross-section dsigma/dOmega
    # = |born_amplitude_yukawa|^2 for shrinking screening mu, approaching the
    # Rutherford limit rutherford_cross_section (mu->0).  Forward-peaked; screening
    # keeps the forward value finite, while bare Coulomb (Rutherford) diverges.
    k, beta = 2.0, 1.0
    th = np.radians(np.linspace(1.0, 180.0, 500))
    th_deg = np.degrees(th)
    mus = [(1.5, ALT), (0.7, FLOW), (0.3, INK)]

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(th_deg, rutherford_cross_section(th, k, beta), color=STEEL, lw=2.4,
            ls="--", label=r"Rutherford ($\mu\to0$): $\propto\sin^{-4}\frac{\theta}{2}$")
    for mu, col in mus:
        f = np.array([born_amplitude_yukawa(t, k, beta, mu) for t in th])
        ax.plot(th_deg, np.abs(f) ** 2, color=col, lw=2,
                label=fr"Yukawa $\mu={mu}$")
    ax.set_yscale("log")
    ax.set_xlim(0, 180)
    ax.set_xticks([0, 45, 90, 135, 180])
    ax.set_xlabel(r"scattering angle $\theta$ (deg)")
    ax.set_ylabel(r"$d\sigma/d\Omega=|f(\theta)|^2$")
    ax.set_title(r"Born/Yukawa $\to$ Rutherford as screening $\mu\to0$  ($k=2$)")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_born_yukawa_rutherford.svg")
    caps["fig2_born_yukawa_rutherford.svg"] = (
        r"First-Born differential cross-section $|f(\theta)|^2$ for the Yukawa "
        r"potential $V=\beta e^{-\mu r}/r$ at $k=2$, from born_amplitude_yukawa, as "
        r"the screening $\mu$ shrinks. Each curve is strongly forward-peaked; the "
        r"finite screening length $1/\mu$ keeps the forward ($\theta\to0$) value "
        r"finite. As $\mu\to0$ the curves climb toward the bare-Coulomb "
        r"rutherford_cross_section $\propto\sin^{-4}(\theta/2)$ (dashed), which "
        r"diverges forward — the same $d\sigma/d\Omega$ classical mechanics gives.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
