"""QM-09 figures -- the harmonic-oscillator ladder and the correspondence principle.

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
from oscillator import psi, energy                 # noqa: E402  (Hermite-Gaussian eigenfns, E_n=n+1/2)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- the eigenfunctions psi_n(x) drawn on the EQUALLY-SPACED ladder
    # E_n = n + 1/2 inside the parabola V = x^2/2.  psi and energy are the module's
    # own (psi imports H_n from MA-12).
    x = np.linspace(-5.5, 5.5, 1200)
    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    ax.plot(x, 0.5 * x ** 2, color=STEEL, lw=1.6, label=r"$V=\frac{1}{2}x^2$")
    for n, col in zip(range(5), (INK, FLOW, ALT, STEEL, INK)):
        En = energy(n)
        wf = psi(n, x)
        wf = wf / np.max(np.abs(wf))                      # unit amplitude
        ax.axhline(En, color="#dddddd", lw=0.8, ls="--")
        ax.plot(x, 0.42 * wf + En, color=col, lw=1.8)
        ax.text(5.45, En + 0.07, fr"$n={n}$", color=col, fontsize=9, ha="right")
    ax.annotate("", xy=(-4.7, energy(1)), xytext=(-4.7, energy(0)),
                arrowprops=dict(arrowstyle="<->", color="#555555", lw=1.0))
    ax.text(-4.55, 1.0, r"$\hbar\omega=1$", color="#555555", fontsize=9)
    ax.set_xlim(-5.6, 5.6); ax.set_ylim(0, 6.0)
    ax.set_xlabel(r"position $x$")
    ax.set_ylabel(r"energy $E/\hbar\omega$   ($+\,$scaled $\psi_n$)")
    ax.set_title(r"Harmonic ladder: equally spaced $E_n=n+\frac{1}{2}$, zero-point $\frac{1}{2}$")
    ax.legend(loc="upper center", frameon=False, fontsize=9)
    _save(fig, "fig1_oscillator_ladder.svg")
    caps["fig1_oscillator_ladder.svg"] = (
        r"The five lowest eigenfunctions $\psi_n(x)$ (from the module's psi, whose "
        r"$H_n$ comes from MA-12) drawn on their levels $E_n=n+\frac12$ in the well "
        r"$V=\frac12 x^2$ ($\hbar=m=\omega=1$). The ladder is EQUALLY spaced by "
        r"$\hbar\omega$ with a nonzero zero-point energy $E_0=\frac12$; $\psi_n$ has "
        r"$n$ nodes and parity $(-1)^n$. Equal spacing is the oscillator's "
        r"signature -- unlike the $n^2$ box of QM-08.")

    # Fig 2 -- correspondence principle: a high-n |psi_n|^2 oscillates about the
    # classical time-at-position density.  Quantum curve is the module's psi(n,x);
    # the smooth envelope is the closed-form classical distribution for E_n.
    n = 12
    Et = energy(n)
    xt = np.sqrt(2.0 * Et)                                # classical turning point
    x = np.linspace(-1.18 * xt, 1.18 * xt, 2400)
    quantum = psi(n, x) ** 2
    mask = np.abs(x) < 0.985 * xt
    classical = np.zeros_like(x)
    classical[mask] = 1.0 / (np.pi * np.sqrt(xt ** 2 - x[mask] ** 2))

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(x, quantum, color=INK, lw=1.3, label=r"$|\psi_{12}|^2$  (quantum)")
    ax.plot(x, classical, color=FLOW, lw=2.2,
            label=r"$\frac{1}{\pi\sqrt{2E_n-x^2}}$  (classical)")
    for s in (-1, 1):
        ax.axvline(s * xt, color="#aaaaaa", lw=0.8, ls=":")
    ax.set_xlim(-1.18 * xt, 1.18 * xt); ax.set_ylim(0, 0.42)
    ax.set_xlabel(r"position $x$"); ax.set_ylabel(r"probability density")
    ax.set_title(r"Correspondence: $|\psi_n|^2$ averages to the classical density ($n=12$)")
    ax.text(0.0, 0.285, r"turning points $x=\pm\sqrt{2E_n}$", ha="center",
            color="#555555", fontsize=9)
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_correspondence.svg")
    caps["fig2_correspondence.svg"] = (
        r"The $n=12$ probability density $|\psi_n(x)|^2$ from the module's psi "
        r"(blue), against the classical time-at-position density "
        r"$1/(\pi\sqrt{2E_n-x^2})$ (orange). For large $n$ the rapidly oscillating "
        r"quantum density (with its $n$ nodes) tracks the classical curve on "
        r"average, both piling up at the turning points $x=\pm\sqrt{2E_n}$ where the "
        r"particle moves slowest -- Bohr's correspondence principle.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
