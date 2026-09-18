"""QM-08 figures -- tunnelling/resonances through a barrier, and well quantization.

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
from one_dim import (                              # noqa: E402
    transmission_barrier, scatter_piecewise,
    bound_states, infinite_well_energy,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- rectangular barrier transmission T(E): the two signature regimes.
    # Line: the analytic transmission_barrier; dots: the INDEPENDENT transfer-matrix
    # scatter_piecewise on the same potential [0,V0,0] -- they must coincide.
    V0, a = 10.0, 1.0
    E = np.linspace(0.05, 35.0, 1600)
    T = np.array([transmission_barrier(float(e), V0, a) for e in E])
    Ed = np.linspace(1.0, 35.0, 30)
    Td = np.array([scatter_piecewise(float(e), [0.0, V0, 0.0], [0.0, a])[0] for e in Ed])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.axvspan(0.0, V0, color=FLOW, alpha=0.06)
    ax.plot(E, T, color=INK, lw=2, label=r"$T(E)$  (analytic)")
    ax.plot(Ed, Td, ls="none", marker="o", ms=4, color=FLOW,
            label="transfer matrix")
    ax.axhline(1.0, color="#888888", lw=0.8, ls="--")
    ax.axvline(V0, color="#888888", lw=1.0, ls="--", label=r"barrier top $V_0$")
    for n in (1, 2):                                      # over-barrier resonances
        Eres = V0 + (n * np.pi) ** 2 / (2.0 * a ** 2)
        ax.axvline(Eres, color=ALT, lw=0.9, ls=":")
    ax.set_yscale("log")
    ax.set_ylim(1e-6, 2.0); ax.set_xlim(0, 35)
    ax.set_xlabel(r"incident energy $E$"); ax.set_ylabel(r"transmission $T$")
    ax.set_title(r"Barrier ($V_0=10,\ a=1$): tunnelling for $E<V_0$, resonances above")
    ax.annotate("tunnelling\n$E<V_0$, $T>0$", xy=(2.2, 3e-3), color=FLOW, fontsize=9)
    ax.annotate(r"$T=1$ at $k_2 a=n\pi$", xy=(15.6, 1.15), color=ALT, fontsize=9)
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    _save(fig, "fig1_barrier_transmission.svg")
    caps["fig1_barrier_transmission.svg"] = (
        r"Transmission through a rectangular barrier ($V_0=10$, width $a=1$, "
        r"$\hbar=m=1$): the line is transmission_barrier, the dots the module's "
        r"independent transfer-matrix scatter_piecewise. For $E<V_0$ (shaded) "
        r"$T>0$ but exponentially small -- quantum tunnelling; for $E>V_0$ $T$ "
        r"oscillates and hits perfect transmission $T=1$ at the resonances "
        r"$k_2 a=n\pi$, where the barrier is an integer number of half-waves wide.")

    # Fig 2 -- infinite square well: confinement quantizes E into the n^2 ladder.
    # bound_states (finite-difference TISE) on V=0 with Dirichlet walls; each level
    # carries the FD energy, checked against the closed form infinite_well_energy.
    L = 1.0
    x = np.linspace(0.0, L, 1201)
    Efd, psi = bound_states(np.zeros_like(x), x, n_states=4)
    scale = 5.0

    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    ax.axvline(0.0, color="#555555", lw=3); ax.axvline(L, color="#555555", lw=3)
    for k, col in zip(range(4), (INK, FLOW, ALT, STEEL)):
        n = k + 1
        wf = psi[k] / np.max(np.abs(psi[k]))             # unit amplitude
        wf *= np.sign(wf[np.argmax(np.abs(wf))])         # largest antinode positive
        ax.axhline(Efd[k], color="#cccccc", lw=0.8, ls="--")
        ax.plot(x, wf * scale + Efd[k], color=col, lw=2)
        ax.text(0.50, Efd[k] + scale + 1.2,
                fr"$n={n}$:  $E={Efd[k]:.2f}$  (exact ${infinite_well_energy(n, L):.2f}$)",
                ha="center", color=col, fontsize=9)
    ax.set_xlim(-0.04, L + 0.04); ax.set_ylim(0, Efd[3] + scale + 10)
    ax.set_xlabel(r"position $x/L$")
    ax.set_ylabel(r"energy $E$   ($+\,$scaled $\psi_n$)")
    ax.set_title(r"Infinite square well: confinement quantizes $E_n=\frac{n^2\pi^2}{2L^2}$")
    _save(fig, "fig2_infinite_well_levels.svg")
    caps["fig2_infinite_well_levels.svg"] = (
        r"The lowest four infinite-well states from bound_states (a finite-"
        r"difference TISE solve with $\psi=0$ at the walls), each $\psi_n$ drawn on "
        r"its energy level. Confinement alone forces a DISCRETE ladder "
        r"$E_n\propto n^2$ (the FD energies match the closed form "
        r"infinite_well_energy), $\psi_n$ has $n-1$ nodes and alternates parity. "
        r"Contrast the harmonic well (QM-09), whose levels are equally spaced.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
