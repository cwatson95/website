"""SM-03 figures — the Schottky anomaly and the Einstein-solid heat capacity.

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
from classical_statmech import (                   # noqa: E402
    two_level_energy, two_level_heat_capacity,
    einstein_heat_capacity, K_B, HBAR,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — two-level system: the mean energy saturates while the heat capacity
    # makes the Schottky bump, both plotted against the dimensionless kT/eps.
    eps = 1e-21                                     # level gap [J]
    x = np.linspace(0.03, 3.0, 600)                 # x = kT/eps
    T = x * eps / K_B
    E_over_eps = np.array([two_level_energy(eps, float(t)) / eps for t in T])
    C_over_k = np.array([two_level_heat_capacity(eps, float(t)) / K_B for t in T])
    ipk = int(np.argmax(C_over_k))

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(x, C_over_k, color=FLOW, lw=2, label=r"$C/k$  (Schottky anomaly)")
    ax.plot(x, E_over_eps, color=INK, lw=2, label=r"$\langle E\rangle/\varepsilon$")
    ax.axhline(0.5, color="#aaaaaa", lw=0.8, ls=":")
    ax.axvline(x[ipk], color=ALT, lw=1.2, ls="--",
               label=fr"peak at $kT\approx{x[ipk]:.2f}\,\varepsilon$, $C/k={C_over_k[ipk]:.2f}$")
    ax.set_xlim(0, 3.0)
    ax.set_ylim(0, 0.62)
    ax.set_xlabel(r"reduced temperature $kT/\varepsilon$")
    ax.set_ylabel(r"$C/k$   and   $\langle E\rangle/\varepsilon$")
    ax.set_title(r"Two-level system: the Schottky anomaly in $C(T)$")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_schottky_anomaly.svg")
    caps["fig1_schottky_anomaly.svg"] = (
        r"Two-level system $\{0,\varepsilon\}$ vs reduced temperature $kT/\varepsilon$, "
        r"from two_level_energy and two_level_heat_capacity. The mean energy (blue) "
        r"climbs from 0 to $\varepsilon/2$ as the levels equalise; the heat capacity "
        r"(orange) vanishes at both extremes and peaks near $kT\approx0.42\,\varepsilon$ "
        r"-- the Schottky anomaly. Only a partly-excited gap can absorb heat.")

    # Fig 2 — Einstein solid: heat capacity of one quantum oscillator vs T/Theta_E,
    # frozen out at low T, approaching the Dulong-Petit value C/k = 1 when hot.
    omega = 1e13                                    # oscillator frequency [rad/s]
    theta_E = HBAR * omega / K_B                    # Einstein temperature [K]
    t = np.linspace(0.04, 2.5, 600)                 # t = T/Theta_E
    Te = t * theta_E
    C_E = np.array([einstein_heat_capacity(omega, float(tt)) / K_B for tt in Te])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(t, C_E, color=INK, lw=2, label=r"$C/k$ (Einstein oscillator)")
    ax.axhline(1.0, color=FLOW, lw=1.4, ls="--", label="Dulong-Petit  $C/k=1$")
    ax.annotate("frozen out\n$(kT\\ll\\hbar\\omega)$", xy=(0.22, 0.12),
                xytext=(0.5, 0.30), color=STEEL, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=STEEL, lw=1.0))
    ax.set_xlim(0, 2.5)
    ax.set_ylim(0, 1.12)
    ax.set_xlabel(r"reduced temperature $T/\Theta_E$   ($\Theta_E=\hbar\omega/k$)")
    ax.set_ylabel(r"heat capacity $C/k$")
    ax.set_title(r"Einstein solid: $C$ freezes out cold, Dulong-Petit hot")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    _save(fig, "fig2_einstein_heat_capacity.svg")
    caps["fig2_einstein_heat_capacity.svg"] = (
        r"Heat capacity of one quantum (Einstein) oscillator vs $T/\Theta_E$, from "
        r"einstein_heat_capacity. Below the Einstein temperature $\Theta_E=\hbar\omega/k$ "
        r"the gap freezes the mode out and $C\to0$; well above it every quadratic "
        r"degree of freedom is thermally active and $C/k\to1$, the classical "
        r"Dulong-Petit value (dashed).")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
