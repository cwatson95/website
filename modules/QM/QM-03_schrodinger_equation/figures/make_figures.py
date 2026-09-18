"""QM-03 figures — the infinite-well TISE spectrum, and stationary vs beating
dynamics under the time-dependent Schrodinger equation.

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
from schrodinger import (                          # noqa: E402
    make_grid, solve, infinite_well_energy, evolve, expectation_position,
    superposition_period, measure_period,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    L, N = 1.0, 400
    x = make_grid(0.0, L, N)
    E, psi = solve(x, V=0.0)                        # TISE: H psi = E psi

    # Fig 1 — the time-INDEPENDENT Schrodinger equation solved on a grid: the
    # finite-difference Hamiltonian is diagonalised (solve) and its lowest four
    # eigenfunctions psi_n are drawn offset by their eigen-energies E_n, each
    # compared to the closed form infinite_well_energy E_n = n^2 pi^2 /(2 L^2).
    xf = np.concatenate(([0.0], x, [L]))           # add the Dirichlet walls for the plot
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    amp = 6.0
    cols = [INK, FLOW, ALT, STEEL]
    for n in range(4):
        vec = psi[:, n].real
        vec = vec / np.max(np.abs(vec))
        if vec[0] < 0.0:                            # fix sign so the first lobe rises
            vec = -vec
        vf = np.concatenate(([0.0], vec, [0.0]))
        ax.axhline(E[n], color="#cccccc", lw=0.8, ls="--")
        ax.plot(xf, E[n] + amp * vf, color=cols[n], lw=2,
                label=fr"$n={n+1}$:  $E={E[n]:.2f}$  (exact {infinite_well_energy(n+1, L):.2f})")
    ax.axvline(0.0, color="#555555", lw=1.6)
    ax.axvline(L, color="#555555", lw=1.6)
    ax.set_xlim(-0.05, L + 0.05)
    ax.set_xlabel("position $x$  (infinite well, width $L=1$)")
    ax.set_ylabel(r"energy $E_n$  (with $\psi_n$ offset)")
    ax.set_title(r"Infinite-well TISE $\hat H\psi_n=E_n\psi_n$:  $E_n=n^2\pi^2\hbar^2/2mL^2$")
    ax.legend(loc="upper center", frameon=False, fontsize=8, ncol=2)
    _save(fig, "fig1_infinite_well_levels.svg")
    caps["fig1_infinite_well_levels.svg"] = (
        "The time-independent Schrodinger equation solved on a grid (solve): the "
        "finite-difference Hamiltonian is diagonalised and its lowest four "
        "eigenfunctions psi_n are drawn offset by their eigen-energies E_n. The "
        "numeric levels match the closed form infinite_well_energy "
        "E_n=n^2 pi^2/(2 L^2) (hbar=m=1) to <0.02%; psi_n has n antinodes and n-1 "
        "interior nodes, and the levels fan out as n^2.")

    # Fig 2 — the time-DEPENDENT equation: a single eigenstate is stationary
    # (|Psi|^2 frozen, so <x>(t) is flat), while a two-level superposition beats
    # at the Bohr frequency omega=(E2-E1)/hbar.  evolve attaches the phases
    # exp(-i E_n t/hbar) and sums; measure_period reads the period off <x>(t).
    K = psi.shape[1]
    c_stat = np.zeros(K); c_stat[0] = 1.0
    c_sup = np.zeros(K); c_sup[0] = c_sup[1] = 1.0 / np.sqrt(2.0)
    T = superposition_period(E[1], E[0])
    ts = np.linspace(0.0, 2.5 * T, 700)
    x_stat = np.array([expectation_position(evolve(E, psi, c_stat, t), x) for t in ts])
    x_sup = np.array([expectation_position(evolve(E, psi, c_sup, t), x) for t in ts])
    T_meas = measure_period(ts, x_sup)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(ts, x_sup, color=FLOW, lw=2,
            label=r"superposition $(\psi_1+\psi_2)/\sqrt{2}$")
    ax.plot(ts, x_stat, color=INK, lw=2, label=r"stationary state $\psi_1$")
    ax.axhline(L / 2.0, color="#aaaaaa", lw=0.7, ls=":")
    for k in (1, 2):
        ax.axvline(k * T_meas, color="#bbbbbb", lw=0.8, ls=":")
    ax.annotate(fr"$T={T_meas:.4f}=\frac{{2\pi\hbar}}{{E_2-E_1}}$",
                xy=(T_meas, x_sup.max()), xytext=(1.18 * T_meas, x_sup.max() + 0.015),
                color="#555555", fontsize=9)
    ax.set_xlim(0, ts[-1])
    ax.set_xlabel(r"time $t$")
    ax.set_ylabel(r"$\langle x\rangle(t)$")
    ax.set_title(r"A superposition moves: $\langle x\rangle(t)$ beats at $\omega=(E_2-E_1)/\hbar$")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    _save(fig, "fig2_stationary_vs_beat.svg")
    caps["fig2_stationary_vs_beat.svg"] = (
        "Stationary vs non-stationary dynamics (evolve). A single eigenstate psi_1 "
        "is a STATIONARY state: |Psi|^2, hence <x>(t) (blue), is frozen at L/2 even "
        "as its phase rotates. The equal superposition (psi_1+psi_2)/sqrt2 (orange) "
        "instead oscillates -- the interference cross-term beats at the Bohr "
        f"frequency omega=(E2-E1)/hbar. measure_period recovers T={T_meas:.4f}, "
        "equal to 2 pi hbar/(E2-E1) from superposition_period.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
