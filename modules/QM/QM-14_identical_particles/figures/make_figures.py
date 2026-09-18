"""QM-14 figures — exchange symmetry: bunching, the Fermi hole, exchange forces.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.

The two-particle wavefunction Psi(x1,x2) is built *directly* from the module's
own symmetrize / antisymmetrize / tensor: kron of two grid-sampled orbitals is a
flat length-N^2 vector that, reshaped to (N, N), is Psi on the (x1, x2) grid.
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"      # text as vector paths (portable, no font dep)
matplotlib.rcParams["font.size"] = 11
import matplotlib.pyplot as plt                    # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from identical import (                            # noqa: E402
    tensor, symmetrize, antisymmetrize, well_state, ho_state, exchange_dx2,
)

INK, FLOW, ALT, AUX = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"
# on-palette sequential map (white -> ink) for the probability heatmaps
CMAP = LinearSegmentedColormap.from_list("ink", ["#ffffff", "#bcbcd6", INK])


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _density(builder, x):
    """|Psi(x1,x2)|^2 on the grid, from a two-particle builder in ../code.
    kron(psi_a, psi_b) reshaped to (N,N) is Psi(x1,x2); square it and
    normalize to unit max so the three panels share a colour scale."""
    psi = builder(well_state(1, x), well_state(2, x)).reshape(len(x), len(x))
    rho = np.abs(psi) ** 2
    return rho / rho.max()


def main():
    caps = {}

    # Fig 1 — two-particle density |Psi(x1,x2)|^2: distinguishable vs boson vs
    # fermion, infinite-well orbitals n=1,2. Bosons pile on the diagonal x1=x2,
    # fermions are forbidden there (the Fermi hole) — pure exchange symmetry.
    N = 260
    x = np.linspace(0.0, 1.0, N)
    panels = [
        ("distinguishable  $\\psi_1(x_1)\\,\\psi_2(x_2)$", tensor),
        ("boson  (symmetric)",                              symmetrize),
        ("fermion  (antisymmetric)",                        antisymmetrize),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(6.2, 3.5), sharey=True)
    for ax, (title, builder) in zip(axes, panels):
        rho = _density(builder, x)
        ax.pcolormesh(x, x, rho.T, cmap=CMAP, vmin=0.0, vmax=1.0,
                      shading="auto", rasterized=True)
        ax.plot([0, 1], [0, 1], color=FLOW, lw=1.0, ls="--")  # the x1=x2 line
        ax.set_title(title, fontsize=9.5)
        ax.set_xlabel("$x_1$")
        ax.set_aspect("equal")
        ax.set_xticks([0, 0.5, 1])
        ax.set_yticks([0, 0.5, 1])
    axes[0].set_ylabel("$x_2$")
    fig.suptitle(r"Exchange symmetry on the $(x_1,x_2)$ plane:  $|\Psi|^2$"
                 r" for two particles in well states $n=1,2$", fontsize=10.5)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    _save(fig, "fig1_two_particle_density.svg")
    caps["fig1_two_particle_density.svg"] = (
        "Two-particle probability density $|\\Psi(x_1,x_2)|^2$ for two particles "
        "in infinite-well orbitals $n=1,2$, built from the module's "
        "tensor/symmetrize/antisymmetrize. Left: distinguishable product state. "
        "Middle (boson, symmetric): density is enhanced along the diagonal "
        "$x_1=x_2$ (dashed) — particles bunch. Right (fermion, antisymmetric): "
        "$|\\Psi|^2=0$ all along $x_1=x_2$ — the Fermi/exchange hole that "
        "enforces Pauli exclusion. No interaction is present; the difference is "
        "pure exchange symmetry.")

    # Fig 2 — the exchange force: <(x1-x2)^2> for boson < distinguishable <
    # fermion, in two different potentials (infinite well n=1,2 and harmonic
    # oscillator n=0,1), normalized to the distinguishable value so the
    # universal ordering shows on one axis. Computed by exchange_dx2.
    xw = np.linspace(0.0, 1.0, 4001)
    rw = exchange_dx2(well_state(1, xw), well_state(2, xw), xw)
    xh = np.linspace(-9.0, 9.0, 6001)
    rh = exchange_dx2(ho_state(0, xh), ho_state(1, xh), xh)

    systems = [("infinite well\n$n=1,2$", rw), ("harmonic osc.\n$n=0,1$", rh)]
    kinds = [("boson", "boson", ALT), ("distinguishable", "distinguishable", AUX),
             ("fermion", "fermion", FLOW)]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    width = 0.26
    centres = np.arange(len(systems))
    for i, (label, key, col) in enumerate(kinds):
        vals = [r[key] / r["distinguishable"] for _, r in systems]
        raw = [r[key] for _, r in systems]
        bars = ax.bar(centres + (i - 1) * width, vals, width, color=col,
                      label=label, edgecolor="white", linewidth=0.6)
        for b, rv in zip(bars, raw):
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.015,
                    f"{rv:.3f}", ha="center", va="bottom", fontsize=8, color=col)
    ax.axhline(1.0, color="#aaaaaa", lw=0.8, ls=":")
    ax.set_xticks(centres)
    ax.set_xticklabels([s for s, _ in systems])
    ax.set_ylabel(r"$\langle(x_1-x_2)^2\rangle\ /\ \langle\cdot\rangle_{\mathrm{dist}}$")
    ax.set_ylim(0, 1.75)
    ax.set_title(r"Exchange force: bosons bunch ($-$), fermions avoid ($+$),"
                 "\n" r"$\langle(\Delta x)^2\rangle_\pm=\langle(\Delta x)^2"
                 r"\rangle_{\mathrm{dist}}\mp 2\,|\langle x\rangle_{ab}|^2$",
                 fontsize=10.5)
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig2_exchange_force.svg")
    caps["fig2_exchange_force.svg"] = (
        "The exchange 'force', from exchange_dx2 in two potentials. Bars give the "
        "mean-square separation $\\langle(x_1-x_2)^2\\rangle$ for the symmetric "
        "(boson), distinguishable, and antisymmetric (fermion) states, each "
        "normalized to the distinguishable value (dotted line); annotations are "
        "the raw values. In both the infinite well ($n=1,2$) and the harmonic "
        "oscillator ($n=0,1$) the ordering is universal: "
        "$\\langle(\\Delta x)^2\\rangle_{\\mathrm{boson}}<\\langle\\cdot\\rangle_"
        "{\\mathrm{dist}}<\\langle\\cdot\\rangle_{\\mathrm{fermion}}$. The split "
        "is the single exchange term $\\mp2|\\langle x\\rangle_{ab}|^2$ — bosons "
        "closer, fermions farther — with no real interaction.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
