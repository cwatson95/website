"""QM-12 figures — hydrogen radial densities and the Bohr term diagram.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.

Atomic units throughout (hbar = m = e = 4 pi eps0 = 1, so a0 = 1, energies in
hartrees; HARTREE_EV converts to eV).
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"      # text as vector paths (portable, no font dep)
matplotlib.rcParams["font.size"] = 11
import matplotlib.pyplot as plt                    # noqa: E402
from matplotlib.lines import Line2D                # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from hydrogen import (                             # noqa: E402
    radial_probability, count_radial_nodes,
    coulomb_energy_eV, radial_solve, HARTREE_EV,
)

INK, FLOW, ALT, EXTRA = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"
_LETTER = {0: "s", 1: "p", 2: "d", 3: "f"}


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — radial probability density P(r) = r^2 |R_nl|^2 for a few orbitals.
    # The 1s/3d are nodeless, 2s has one node, 3s two: # interior zeros = n-l-1.
    r = np.linspace(0.0, 22.0, 2000)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    states = [(1, 0, INK), (2, 0, FLOW), (3, 0, ALT), (3, 2, EXTRA)]
    for n, l, col in states:
        P = radial_probability(n, l, r)
        nodes = count_radial_nodes(n, l)            # the real n-l-1 count
        label = "%d%s : %d node%s" % (n, _LETTER[l], nodes, "" if nodes == 1 else "s")
        ax.plot(r, P, color=col, lw=2, label=label)
    ax.axvline(1.0, color="#aaaaaa", lw=0.8, ls="--")
    ax.text(1.15, ax.get_ylim()[1] * 0.92, r"$a_0$", color="#777777", fontsize=10)
    ax.set_xlim(0, 22)
    ax.set_xlabel(r"radius $r$  ($a_0=1$)")
    ax.set_ylabel(r"$P(r)=r^{2}\,|R_{nl}|^{2}$")
    ax.set_title("Hydrogen radial density: interior zeros count $n-l-1$")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig1_radial_density.svg")
    caps["fig1_radial_density.svg"] = (
        "Radial probability density $P(r)=r^2|R_{nl}|^2$ for the 1s, 2s, 3s and 3d "
        "orbitals of hydrogen (atomic units, $a_0=1$), from radial_probability. The "
        "number of interior zeros is exactly $n-l-1$ (count_radial_nodes): 1s and 3d "
        "are nodeless, 2s has one node, 3s has two. The 1s density peaks at the Bohr "
        "radius $r=a_0=1$ (dashed) — the most-probable electron radius.")

    # Fig 2 — term diagram: closed-form Bohr levels vs the finite-difference solve.
    # Bars at E_n = -13.6/n^2 eV span each allowed l; FD eigenvalues overlay them.
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    n_max, hw = 4, 0.38
    for n in range(1, n_max + 1):                   # faint shell guide lines + n label
        E = coulomb_energy_eV(n)
        ax.plot([-0.5, n_max - 0.5], [E, E], color="#cccccc", lw=0.6, ls=":", zorder=0)
        ax.text(n_max - 0.45, E, "n=%d" % n, color="#888888", fontsize=8, va="center")
    for l in range(n_max):                          # closed-form bars + orbital names
        for n in range(l + 1, n_max + 1):
            E = coulomb_energy_eV(n)
            ax.plot([l - hw, l + hw], [E, E], color=INK, lw=2.4, solid_capstyle="round")
            ax.text(l, E + 0.22, "%d%s" % (n, _LETTER[l]), color=INK,
                    fontsize=7.5, ha="center", va="bottom")
    for l in range(n_max):                          # finite-difference eigenvalues
        E_fd, _, _ = radial_solve(l, n_states=n_max - l)
        ax.plot(np.full(E_fd.size, l), E_fd * HARTREE_EV, "o", color=FLOW,
                ms=5.5, zorder=5)
    ax.axhline(0.0, color="#aaaaaa", lw=0.8, ls="--")
    ax.text(-0.45, 0.25, r"ionization  ($E\to 0$)", color="#777777", fontsize=9)
    ax.set_xlim(-0.5, n_max - 0.05)
    ax.set_ylim(-14.4, 1.2)
    ax.set_xticks(range(n_max))
    ax.set_xticklabels(["$l=%d$\n(%s)" % (l, _LETTER[l]) for l in range(n_max)])
    ax.set_ylabel("energy  $E$  [eV]")
    ax.set_title(r"Bohr spectrum $E_n=-13.6\,\mathrm{eV}/n^{2}$: bars vs FD solve")
    legend = [Line2D([0], [0], color=INK, lw=2.4, label=r"closed form $-13.6/n^2$"),
              Line2D([0], [0], marker="o", color=FLOW, lw=0, ms=5.5,
                     label="finite-difference solve")]
    ax.legend(handles=legend, loc="lower right", frameon=False)
    _save(fig, "fig2_term_diagram.svg")
    caps["fig2_term_diagram.svg"] = (
        "Hydrogen term diagram: the closed-form Bohr levels $E_n=-13.6\\,\\mathrm{eV}/n^2$ "
        "(coulomb_energy_eV, blue bars) drawn against the orbital quantum number $l$, with "
        "the finite-difference radial eigenvalues (radial_solve, orange markers) overlaid. "
        "The two independent solutions agree, and every $l$ in a shell shares one energy — "
        "the $n^2$-fold accidental degeneracy of the $1/r$ potential.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
