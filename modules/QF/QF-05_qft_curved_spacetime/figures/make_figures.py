"""QF-05 figures — the Unruh spectrum is Planckian, and the Hawking temperature
runs as 1/M (tiny holes blazing hot, solar holes colder than the CMB).

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
from curved_spacetime import (                     # noqa: E402
    unruh_occupation, bose_occupation, fermi_occupation,
    unruh_temperature, hawking_temperature,
    HBAR, K_B, M_SUN,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the Unruh occupation built purely from the Bogoliubov ratio
    # (unruh_occupation) IS the Planck/Bose-Einstein law (bose_occupation) at the
    # Unruh temperature.  Plot vs the dimensionless x = hbar omega / k_B T_U.
    a = 1.0e20                                     # proper acceleration [m/s^2]
    T_U = unruh_temperature(a)
    x = np.linspace(0.08, 6.0, 220)
    omega = x * K_B * T_U / HBAR                   # so x = hbar omega / k_B T_U
    n_unruh = np.array([unruh_occupation(w, a) for w in omega])   # from Bogoliubov beta^2
    n_bose = bose_occupation(omega, T_U)
    n_fermi = fermi_occupation(omega, T_U)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(x, n_bose, color=INK, lw=2,
            label=r"Bose $1/(e^{x}-1)$ at $T_U$")
    ax.plot(x[::6], n_unruh[::6], ls="none", marker="o", ms=5, mfc="white",
            mec=FLOW, mew=1.6, label=r"Unruh $|\beta_\omega|^2$ (Bogoliubov)")
    ax.plot(x, n_fermi, color=ALT, lw=1.8, ls="--",
            label=r"Fermi $1/(e^{x}+1)$ (contrast)")
    ax.set_yscale("log")
    ax.set_xlim(0, 6)
    ax.set_xlabel(r"$\hbar\omega/k_B T_U$")
    ax.set_ylabel(r"mode occupation $\langle n_\omega\rangle$")
    ax.set_title(r"Acceleration is temperature: the Unruh $|\beta_\omega|^2$ IS Planck ($T_U=%.3f$ K)" % T_U)
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_unruh_planck.svg")
    caps["fig1_unruh_planck.svg"] = (
        r"A uniformly accelerated observer sees the inertial vacuum as a thermal "
        r"bath. The Rindler-mode occupation $|\beta_\omega|^2$ built only from the "
        r"Bogoliubov ratio $e^{-2\pi c\omega/a}$ (unruh_occupation, open circles) "
        r"lands exactly on the Planck/Bose-Einstein law $1/(e^{\hbar\omega/k_BT_U}-1)$ "
        r"(bose_occupation, solid) at the Unruh temperature $T_U=\hbar a/2\pi c k_B$ "
        r"— the Fermi law (dashed) shown for contrast. Mode mixing $\Rightarrow$ a "
        r"genuinely thermal spectrum.")

    # Fig 2 — Hawking temperature vs black-hole mass: T_H ~ 1/M, crossing the
    # 2.725 K CMB.  Solar-mass holes are colder than the CMB; a 1 kg hole blazes.
    M = np.logspace(0, 33, 400)                    # 1 kg ... ~1e33 kg
    T_H = np.array([hawking_temperature(m) for m in M])
    T_CMB = 2.725

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(M, T_H, color=INK, lw=2.2, label=r"$T_H=\hbar c^3/8\pi GMk_B\ \propto 1/M$")
    ax.axhline(T_CMB, color=FLOW, lw=1.6, ls="--", label=r"CMB $T=2.725$ K")
    # mark the solar-mass and 1 kg holes via the module's own hawking_temperature
    ax.plot([M_SUN], [hawking_temperature(M_SUN)], "o", ms=7, color=STEEL)
    ax.annotate(r"$M_\odot$: $T_H\approx6\times10^{-8}$ K (colder than CMB)",
                xy=(M_SUN, hawking_temperature(M_SUN)), xytext=(2e21, 1e-3),
                color=STEEL, fontsize=8.5,
                arrowprops=dict(arrowstyle="->", color=STEEL, lw=1.0))
    ax.plot([1.0], [hawking_temperature(1.0)], "o", ms=7, color=ALT)
    ax.annotate(r"$1$ kg: $T_H\sim10^{23}$ K", xy=(1.0, hawking_temperature(1.0)),
                xytext=(5e2, 1e16), color=ALT, fontsize=8.5,
                arrowprops=dict(arrowstyle="->", color=ALT, lw=1.0))
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel(r"black-hole mass $M$ (kg)")
    ax.set_ylabel(r"Hawking temperature $T_H$ (K)")
    ax.set_title(r"Black holes are hot: $T_H\propto1/M$")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_hawking_temperature.svg")
    caps["fig2_hawking_temperature.svg"] = (
        r"Hawking temperature versus mass from hawking_temperature(): "
        r"$T_H=\hbar c^3/8\pi GMk_B$ falls as $1/M$ (a straight line of slope $-1$ "
        r"on log-log axes). A solar-mass hole sits at $\sim6\times10^{-8}$ K, far "
        r"below the $2.725$ K CMB (dashed) so it absorbs more than it radiates, "
        r"while a $1$ kg hole would glow at $\sim10^{23}$ K. With the horizon "
        r"($r_s=2GM/c^2$) shrinking too, the hole radiates ever faster as it "
        r"evaporates.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
