"""QM-04 figures — probability density & current for a moving wavepacket.

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
from probability_current import (                  # noqa: E402
    prob_density, prob_current, gaussian_packet, free_step,
)

INK, FLOW, ALT = "#3b3b6d", "#b5651d", "#9a5a8a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    x = np.linspace(-30, 30, 1500, endpoint=False)
    dx = x[1] - x[0]
    caps = {}

    # Fig 1 — density and current of a right-moving Gaussian packet: j = rho v.
    psi = gaussian_packet(x, x0=-8.0, k0=2.0, sigma=2.0)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(x, prob_density(psi), color=INK, lw=2, label=r"$\rho=|\Psi|^2$")
    ax.plot(x, prob_current(psi, dx), color=FLOW, lw=2,
            label=r"$j=\frac{\hbar}{m}\,\mathrm{Im}(\Psi^*\partial_x\Psi)$")
    ax.axhline(0, color="#aaaaaa", lw=0.6)
    ax.set_xlim(-20, 20); ax.set_xlabel("position $x$"); ax.set_ylabel("density / current")
    ax.set_title(r"Probability current tracks the density: $j=\rho\,v$  ($v=k_0=2$)")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig1_density_current.svg")
    caps["fig1_density_current.svg"] = (
        "Density rho=|Psi|^2 (blue) and current j (orange) for a Gaussian packet with "
        "mean wavenumber k0=2 (hbar=m=1). The current follows the density and is "
        "positive where probability flows right: j = rho v with v = hbar k0/m.")

    # Fig 2 — free evolution: the packet drifts at v=k0 and spreads; norm conserved.
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    psi_t = gaussian_packet(x, x0=-8.0, k0=2.0, sigma=2.0)
    dt, step = 2e-3, 0
    for target, col in [(0, INK), (1000, "#5a7d9a"), (2000, ALT)]:
        while step < target:
            psi_t = free_step(psi_t, dx, dt); step += 1
        area = float(np.trapezoid(prob_density(psi_t), dx=dx))
        ax.plot(x, prob_density(psi_t), color=col, lw=2,
                label=fr"$t={step*dt:.0f}$  ($\int|\Psi|^2={area:.3f}$)")
    ax.set_xlim(-20, 20); ax.set_xlabel("position $x$"); ax.set_ylabel(r"$|\Psi|^2$")
    ax.set_title("Free evolution: drift at the group velocity, with spreading")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig2_free_evolution.svg")
    caps["fig2_free_evolution.svg"] = (
        "Free Schrodinger evolution of the same packet at t=0,2,4 (hbar=m=1). The centre "
        "drifts at the group velocity v=k0=2 while the packet broadens, yet the total "
        "probability integral|Psi|^2 dx stays 1 — local continuity, global conservation.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
