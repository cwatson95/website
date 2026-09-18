"""QM-17 figures — the fine-structure decomposition and the anomalous Zeeman fan.

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
from fine_structure import (                       # noqa: E402
    relativistic_correction_eV, spin_orbit_correction_eV,
    darwin_correction_eV, fine_structure_correction_eV,
    lande_g_factor, zeeman_weak_field_eV, e, h,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"
UEV = 1e6   # eV -> micro-eV


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # The three n=2 fine-structure states (name, n, l, j).
    states = [(r"$2S_{1/2}$", 2, 0, 0.5),
              (r"$2P_{1/2}$", 2, 1, 0.5),
              (r"$2P_{3/2}$", 2, 1, 1.5)]

    # Fig 1 — relativistic + spin-orbit + Darwin = the (n,j)-only fine structure.
    # Each contribution and the total come straight from the module's functions;
    # the total marker lands on fine_structure_correction_eV (the central identity).
    rel = np.array([relativistic_correction_eV(n, l) for _, n, l, j in states]) * UEV
    so  = np.array([spin_orbit_correction_eV(n, l, j) for _, n, l, j in states]) * UEV
    dar = np.array([darwin_correction_eV(n, l) for _, n, l, j in states]) * UEV
    tot = np.array([fine_structure_correction_eV(n, j) for _, n, l, j in states]) * UEV

    x = np.arange(len(states))
    w = 0.22
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.bar(x - 1.5 * w, rel, width=w, color=INK,   label=r"relativistic $-p^4/8m^3c^2$")
    ax.bar(x - 0.5 * w, so,  width=w, color=FLOW,  label=r"spin-orbit $\propto L\cdot S$")
    ax.bar(x + 0.5 * w, dar, width=w, color=ALT,   label=r"Darwin ($\ell=0$)")
    ax.plot(x + 1.5 * w, tot, ls="none", marker="D", ms=7, color=STEEL,
            label=r"sum $= E_{fs}(n,j)$")
    ax.axhline(0, color="#aaaaaa", lw=0.6)
    # the two j=1/2 states reach the SAME total by different routes (j-degeneracy)
    ax.axhline(tot[0], color=STEEL, lw=0.8, ls=":")
    ax.set_xticks(x)
    ax.set_xticklabels([s for s, *_ in states])
    ax.set_ylabel(r"energy shift  ($\mu$eV)")
    ax.set_title(r"Fine structure of $n=2$: rel. $+$ spin-orbit $+$ Darwin $=E_{fs}(n,j)$")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    _save(fig, "fig1_fine_structure_decomposition.svg")
    caps["fig1_fine_structure_decomposition.svg"] = (
        r"The three first-order corrections to the $n=2$ hydrogen levels, each from "
        r"the module's own function: relativistic $-p^4/8m^3c^2$ (blue), spin-orbit "
        r"$\propto L\cdot S$ (orange, zero for $\ell=0$), and the Darwin contact term "
        r"(purple, only $\ell=0$). Their sum (diamonds) equals "
        r"fine_structure_correction_eV$(n,j)$ to machine precision. Note $2S_{1/2}$ and "
        r"$2P_{1/2}$ reach the SAME total by different routes — fine structure breaks "
        r"the $\ell$-degeneracy but preserves the $j$-degeneracy.")

    # Fig 2 — weak-field (anomalous) Zeeman: each n=2 fine-structure level fans into
    # its 2j+1 m_j sublevels, with spacing set by the Lande g_J.  Energies are taken
    # relative to E_2; the zero-field offsets are the fine-structure shifts of Fig 1.
    B = np.linspace(0.0, 0.4, 200)            # weak field (linear regime), tesla
    cols = {0.5: {0: INK, 1: FLOW}, 1.5: ALT}  # color by level
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    f_split = (fine_structure_correction_eV(2, 1.5) - fine_structure_correction_eV(2, 0.5)) * e / h / 1e9
    for name, n, l, j in states:
        col = INK if (l == 0) else (FLOW if j == 0.5 else ALT)
        base = fine_structure_correction_eV(n, j) * UEV
        gJ = lande_g_factor(j, l)
        mjs = np.arange(-j, j + 0.1, 1.0)
        for k, m_j in enumerate(mjs):
            E = base + np.array([zeeman_weak_field_eV(j, l, m_j, b) for b in B]) * UEV
            lbl = fr"{name},  $g_J={gJ:.3g}$" if k == len(mjs) - 1 else None
            ax.plot(B, E, color=col, lw=1.8, label=lbl)
    ax.axvline(0, color="#cccccc", lw=0.6)
    ax.annotate(fr"$2P_{{3/2}}-2P_{{1/2}}$" "\n" fr"$\approx{f_split:.1f}$ GHz at $B=0$",
                xy=(0.012, -34), fontsize=8.5, color="#555555")
    ax.set_xlim(0, 0.4)
    ax.set_xlabel(r"external field  $B$  (tesla)")
    ax.set_ylabel(r"energy rel. to $E_2$  ($\mu$eV)")
    ax.set_title(r"Anomalous Zeeman: $n=2$ levels fan into $m_j$ sublevels, spacing $\propto g_J$")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig2_zeeman_fan.svg")
    caps["fig2_zeeman_fan.svg"] = (
        r"Weak-field (anomalous) Zeeman splitting of the $n=2$ fine-structure levels "
        r"vs external $B$, each line $E=E_{fs}+\mu_B g_J B\,m_j$ from "
        r"zeeman_weak_field_eV. Every level fans into its $2j+1$ equally spaced $m_j$ "
        r"sublevels with slope set by the Lande $g_J$ (lande_g_factor): $2S_{1/2}$ "
        r"($g_J=2$) splits widely, $2P_{1/2}$ ($g_J=\frac{2}{3}$) narrowly — so the two "
        r"$j=\frac{1}{2}$ levels, degenerate at $B=0$, pull apart in the field.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
