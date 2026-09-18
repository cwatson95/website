"""SM-04 figures — the three occupation numbers and the Planck blackbody spectrum.

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
from quantum_statistics import (                   # noqa: E402
    bose_einstein, fermi_dirac, maxwell_boltzmann,
    planck_energy_density, rayleigh_jeans, wien_peak_x,
    K_B, HBAR,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — mean occupation <n> vs (eps-mu)/kT for the three statistics.
    # Set mu=0 so the abscissa is x = eps/kT; evaluate the module's own functions.
    T, mu = 300.0, 0.0
    x_be = np.linspace(0.06, 5.0, 500)             # bosons need eps > mu
    x_all = np.linspace(-2.0, 5.0, 500)
    n_be = np.array([bose_einstein(xx * K_B * T, mu, T) for xx in x_be])
    n_fd = np.array([fermi_dirac(xx * K_B * T, mu, T) for xx in x_all])
    n_mb = np.array([maxwell_boltzmann(xx * K_B * T, mu, T) for xx in x_all])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(x_be, n_be, color=FLOW, lw=2, label=r"Bose-Einstein  $1/(e^{x}-1)$")
    ax.plot(x_all, n_fd, color=INK, lw=2, label=r"Fermi-Dirac  $1/(e^{x}+1)$")
    ax.plot(x_all, n_mb, color=STEEL, lw=2, ls="--", label=r"Maxwell-Boltzmann  $e^{-x}$")
    ax.axhline(1.0, color="#aaaaaa", lw=0.8, ls=":")
    ax.plot([0.0], [0.5], marker="o", ms=5, color=INK)
    ax.annotate(r"FD $=\frac{1}{2}$ at $\varepsilon=\mu$", xy=(0.0, 0.5),
                xytext=(0.6, 0.72), color=INK, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
    ax.annotate(r"Pauli ceiling $\langle n\rangle\leq 1$", xy=(3.2, 1.0),
                xytext=(2.0, 1.55), color=ALT, fontsize=9)
    ax.set_xlim(-2.0, 5.0)
    ax.set_ylim(0, 3.0)
    ax.set_xlabel(r"$(\varepsilon-\mu)/kT$")
    ax.set_ylabel(r"mean occupation $\langle n\rangle$")
    ax.set_title("Bose-Einstein, Fermi-Dirac, Maxwell-Boltzmann occupations")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_occupation_numbers.svg")
    caps["fig1_occupation_numbers.svg"] = (
        r"Mean occupation $\langle n\rangle$ vs $(\varepsilon-\mu)/kT$ from "
        r"bose_einstein, fermi_dirac and maxwell_boltzmann. Bosons (orange) diverge as "
        r"$\varepsilon\to\mu^+$; fermions (blue) obey the Pauli ceiling "
        r"$\langle n\rangle\le1$ and pass through $\frac{1}{2}$ at $\varepsilon=\mu$; "
        r"all three merge onto the classical $e^{-x}$ once $\varepsilon-\mu\gg kT$.")

    # Fig 2 — Planck spectrum at two temperatures (Wien shift + Stefan-Boltzmann
    # growth) with the classical Rayleigh-Jeans law diverging: the UV catastrophe.
    w = np.linspace(1e12, 1.1e16, 1200)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    peak5778 = 0.0
    for T, col in [(4000.0, STEEL), (5778.0, INK)]:
        u = np.array([planck_energy_density(float(ww), T) for ww in w])
        ax.plot(w / 1e15, u, color=col, lw=2, label=fr"Planck, $T={T:.0f}$ K")
        wmax = wien_peak_x() * K_B * T / HBAR       # Wien displacement, omega_max
        umax = planck_energy_density(wmax, T)
        ax.plot([wmax / 1e15], [umax], marker="o", ms=5, color=col)
        if T == 5778.0:
            peak5778 = umax
    u_rj = np.array([rayleigh_jeans(float(ww), 5778.0) for ww in w])
    ax.plot(w / 1e15, u_rj, color=FLOW, lw=1.8, ls="--",
            label=r"Rayleigh-Jeans ($T=5778$): $\propto\omega^2$")
    ax.annotate("ultraviolet\ncatastrophe", xy=(3.2, 1.9 * peak5778),
                color=FLOW, fontsize=9, ha="center")
    ax.annotate(r"Wien peak $\hbar\omega_\mathrm{max}=2.82\,kT$", xy=(2.13, peak5778),
                xytext=(4.3, 0.55 * peak5778), color=ALT, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=ALT, lw=1.0))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 1.3 * peak5778)
    ax.set_xlabel(r"angular frequency $\omega$ ($10^{15}$ rad/s)")
    ax.set_ylabel(r"$u(\omega)$ (J s m$^{-3}$)")
    ax.set_title(r"Planck blackbody spectrum vs the Rayleigh-Jeans catastrophe")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_planck_spectrum.svg")
    caps["fig2_planck_spectrum.svg"] = (
        r"Planck spectral energy density $u(\omega)$ from planck_energy_density at "
        r"4000 and 5778 K: hotter means a taller spectrum whose peak shifts up as "
        r"$\hbar\omega_\mathrm{max}=2.82\,kT$ (Wien, dots from wien_peak_x). The "
        r"classical Rayleigh-Jeans law (dashed, rayleigh_jeans) tracks it at low "
        r"$\omega$ but runs off as $\omega^2$ -- the ultraviolet catastrophe the "
        r"quantum $1/(e^{x}-1)$ cuts off.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
