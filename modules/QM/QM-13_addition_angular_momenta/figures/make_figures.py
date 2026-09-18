"""QM-13 figures — Clebsch-Gordan change of basis (coupled <-> uncoupled).

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
"""
import json
import os
import sys
from fractions import Fraction

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"      # text as vector paths (portable, no font dep)
matplotlib.rcParams["font.size"] = 11
import matplotlib.pyplot as plt                    # noqa: E402
import numpy as np                                 # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from addition import (                             # noqa: E402
    coupled_basis, cg_table, decomposition, multiplet_content,
)

INK, FLOW, ALT, EXTRA = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"
# on-palette diverging map: INK (negative) -> white (zero) -> FLOW (positive)
CG_CMAP = LinearSegmentedColormap.from_list("cg", [INK, "#ffffff", FLOW])


def _mt(x):
    """mathtext for a (possibly half-integer) quantum number: 0.5 -> \\frac{1}{2}."""
    f = Fraction(x).limit_denominator(2)
    if f.denominator == 1:
        return str(f.numerator)
    sign = "-" if f.numerator < 0 else ""
    return sign + r"\frac{%d}{%d}" % (abs(f.numerator), f.denominator)


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the Clebsch-Gordan matrix for 1 (x) 1/2 (Griffiths Table 4.8):
    # the unitary change of basis |j1 m1; j2 m2> -> |J,M>, built by ../code.
    j1, j2 = 1.0, 0.5
    U, coupled, uncoupled = coupled_basis(j1, j2)
    M = U.real
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    im = ax.imshow(M, cmap=CG_CMAP, vmin=-1, vmax=1, aspect="auto",
                   rasterized=True)
    # annotate every nonzero CG coefficient
    for r in range(M.shape[0]):
        for c in range(M.shape[1]):
            v = M[r, c]
            if abs(v) > 1e-9:
                ax.text(c, r, "%+.2f" % v, ha="center", va="center",
                        fontsize=8.5,
                        color="white" if abs(v) > 0.55 else "#222222")
    ax.set_xticks(range(len(coupled)))
    ax.set_xticklabels([r"$|%s,%s\rangle$" % (_mt(J), _mt(Mz))
                        for (J, Mz) in coupled], fontsize=9)
    ax.set_yticks(range(len(uncoupled)))
    ax.set_yticklabels([r"$|%s,%s\rangle$" % (_mt(m1), _mt(m2))
                        for (m1, m2) in uncoupled], fontsize=9)
    ax.set_xlabel(r"coupled  $|J,M\rangle$")
    ax.set_ylabel(r"uncoupled  $|m_1,m_2\rangle$")
    ax.set_title(r"Clebsch-Gordan change of basis:  $1\otimes\frac{1}{2}=\frac{3}{2}\oplus\frac{1}{2}$")
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cb.set_label(r"$\langle m_1 m_2 | J M\rangle$", fontsize=9)
    cb.outline.set_linewidth(0.5)
    _save(fig, "fig1_cg_matrix.svg")
    caps["fig1_cg_matrix.svg"] = (
        "The Clebsch-Gordan matrix for $1\\otimes\\tfrac12=\\tfrac32\\oplus\\tfrac12$ "
        "(Griffiths Table 4.8), built from scratch by the highest-weight + ladder "
        "recursion in ../code. Each column is a coupled state $|J,M\\rangle$ expanded "
        "in the uncoupled product basis $|m_1,m_2\\rangle$; entries are nonzero only "
        "when $m_1+m_2=M$, and every row and column has unit norm (the unitary, "
        "orthonormal change of basis).")

    # Fig 2 — the archetype: two spin-1/2 -> symmetric triplet (J=1) +
    # antisymmetric singlet (J=0).  Amplitudes are the CG coefficients themselves.
    Uh, ch, uh = coupled_basis(0.5, 0.5)
    Uh = Uh.real
    col = {lbl: i for i, lbl in enumerate(ch)}
    order = [(1.0, 1.0), (1.0, 0.0), (1.0, -1.0), (0.0, 0.0)]   # triplet..singlet
    unc_arrow = [r"$|\uparrow\uparrow\rangle$", r"$|\uparrow\downarrow\rangle$",
                 r"$|\downarrow\uparrow\rangle$", r"$|\downarrow\downarrow\rangle$"]
    unc_cols = [INK, FLOW, ALT, EXTRA]

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    width = 0.19
    x = np.arange(len(order))
    for k in range(4):                                  # 4 uncoupled basis states
        amps = [Uh[k, col[lbl]] for lbl in order]
        ax.bar(x + (k - 1.5) * width, amps, width, color=unc_cols[k],
               label=unc_arrow[k])
    ax.axhline(0, color="#888888", lw=0.6)
    ax.axvspan(-0.5, 2.5, color=INK, alpha=0.05)        # triplet region
    ax.axvspan(2.5, 3.5, color=FLOW, alpha=0.06)        # singlet region
    ax.text(1.0, 1.06, "triplet  $J=1$ (symmetric)", ha="center", fontsize=9,
            color=INK)
    ax.text(3.0, 1.06, "singlet  $J=0$\n(antisymmetric)", ha="center",
            fontsize=9, color=FLOW)
    ax.set_xticks(x)
    ax.set_xticklabels([r"$|%s,%s\rangle$" % (_mt(J), _mt(Mz)) for (J, Mz) in order])
    ax.set_ylim(-0.95, 1.32)
    ax.set_xlabel(r"coupled state  $|J,M\rangle$")
    ax.set_ylabel(r"amplitude  $\langle m_1 m_2|J M\rangle$")
    ax.set_title(r"Two spin-$\frac{1}{2}$:  $\frac{1}{2}\otimes\frac{1}{2}=1\oplus 0$")
    ax.legend(loc="lower left", frameon=False, fontsize=9, ncol=2)
    _save(fig, "fig2_singlet_triplet.svg")
    caps["fig2_singlet_triplet.svg"] = (
        "Coupling two spin-$\\tfrac12$'s, $\\tfrac12\\otimes\\tfrac12=1\\oplus0$: each "
        "coupled state is decomposed into the uncoupled basis "
        "$|\\!\\uparrow\\uparrow\\rangle,|\\!\\uparrow\\downarrow\\rangle,"
        "|\\!\\downarrow\\uparrow\\rangle,|\\!\\downarrow\\downarrow\\rangle$, with "
        "bar heights the Clebsch-Gordan amplitudes from ../code. The $M=0$ states "
        "split the doubled $|\\!\\uparrow\\downarrow\\rangle,|\\!\\downarrow\\uparrow"
        "\\rangle$ sector: the triplet $|1,0\\rangle=(|\\!\\uparrow\\downarrow\\rangle"
        "+|\\!\\downarrow\\uparrow\\rangle)/\\sqrt2$ is symmetric, the singlet "
        "$|0,0\\rangle=(|\\!\\uparrow\\downarrow\\rangle-|\\!\\downarrow\\uparrow"
        "\\rangle)/\\sqrt2$ antisymmetric (the QM-21 Bell state).")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)
    print("  decomposition(1, 1/2):", decomposition(1.0, 0.5))
    print("  multiplet_content(1/2,1/2):", multiplet_content(0.5, 0.5))


if __name__ == "__main__":
    main()
