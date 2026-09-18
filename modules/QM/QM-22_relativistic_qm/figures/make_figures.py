"""QM-22 figures -- the relativistic dispersion and its non-relativistic expansion.

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
from relativistic import (                         # noqa: E402
    kg_energy, nonrel_energy, energy_expansion,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def main():
    caps = {}
    m = 1.0

    # Fig 1 -- the relativistic dispersion E = +-sqrt(p^2+m^2): BOTH energy signs
    # solve E^2 = p^2 + m^2 (kg_energy with sign=+-1).  The 2m gap and the negative
    # branch (antiparticles) are the whole reason QM must become field theory.
    p = np.linspace(-3.0, 3.0, 600)
    Ep = np.array([kg_energy([pp, 0.0, 0.0], m, +1) for pp in p])
    Em = np.array([kg_energy([pp, 0.0, 0.0], m, -1) for pp in p])
    Enr = np.array([energy_expansion([pp, 0.0, 0.0], m, 1) for pp in p])  # m + p^2/2m

    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.plot(p, Ep, color=INK, lw=2.2, label=r"$+\sqrt{p^2+m^2}$ (particle)")
    ax.plot(p, Em, color=FLOW, lw=2.2, label=r"$-\sqrt{p^2+m^2}$ (antiparticle)")
    ax.plot(p, Enr, color=STEEL, lw=1.6, ls="--", label=r"$m+\frac{p^2}{2m}$ (non-rel.)")
    ax.plot(p, np.abs(p), color="#bbbbbb", lw=0.9, ls=":")
    ax.plot(p, -np.abs(p), color="#bbbbbb", lw=0.9, ls=":", label=r"$\pm|p|$ (massless)")
    ax.annotate("", xy=(0, m), xytext=(0, -m),
                arrowprops=dict(arrowstyle="<->", color="#555555", lw=1.2))
    ax.text(0.12, 0.0, r"$2mc^2$ gap", color="#555555", fontsize=9, va="center")
    ax.text(-2.9, -2.55, "negative-energy sea", color=FLOW, fontsize=9)
    ax.set_xlim(-3, 3); ax.set_ylim(-3.4, 3.4)
    ax.set_xlabel(r"momentum $p$  (units $mc$)")
    ax.set_ylabel(r"energy $E$  (units $mc^2$)")
    ax.set_title(r"Relativistic dispersion $E=\pm\sqrt{p^2c^2+m^2c^4}$")
    ax.legend(loc="upper center", frameon=False, fontsize=8, ncol=2)
    fig.savefig(os.path.join(HERE, "fig1_dispersion.svg"), format="svg", bbox_inches="tight")
    plt.close(fig)
    caps["fig1_dispersion.svg"] = (
        r"The energy-momentum relation $E=\pm\sqrt{p^2+m^2}$ from the module's "
        r"kg_energy ($\hbar=c=1$): BOTH signs solve $E^2=p^2+m^2$, so a positive "
        r"branch (the particle) and a negative branch (the antiparticle sea) are "
        r"split by a $2mc^2$ gap. Near $p=0$ the positive branch matches the "
        r"non-relativistic $m+p^2/2m$; for $|p|\gg m$ both approach the massless "
        r"cones $\pm|p|$. The unavoidable negative energies are what force QM into "
        r"field theory.")

    # Fig 2 -- the low-momentum expansion E = m + p^2/2m - p^4/8m^3 + ...  Exact
    # kinetic energy (nonrel_energy) vs the truncations from energy_expansion: the
    # Schrodinger p^2/2m and the leading relativistic -p^4/8m^3 (fine-structure seed).
    p = np.linspace(0.0, 1.2, 400)
    Kexact = np.array([nonrel_energy([pp, 0.0, 0.0], m) for pp in p])
    K1 = np.array([energy_expansion([pp, 0.0, 0.0], m, 1) for pp in p]) - m
    K2 = np.array([energy_expansion([pp, 0.0, 0.0], m, 2) for pp in p]) - m

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(p, Kexact, color=INK, lw=2.4, label=r"exact $\sqrt{p^2+m^2}-m$")
    ax.plot(p, K1, color=FLOW, lw=1.8, ls="--", label=r"$\frac{p^2}{2m}$ (Schrodinger)")
    ax.plot(p, K2, color=ALT, lw=1.8, ls="-.",
            label=r"$\frac{p^2}{2m}-\frac{p^4}{8m^3}$")
    ax.set_xlim(0, 1.2); ax.set_ylim(0, 0.62)
    ax.set_xlabel(r"momentum $p$  (units $mc$)")
    ax.set_ylabel(r"kinetic energy $E-m$  (units $mc^2$)")
    ax.set_title(r"Non-relativistic limit and the $-\,p^4/8m^3$ correction")
    ax.annotate(r"$-\frac{p^4}{8m^3}$: leading relativistic correction",
                xy=(0.62, 0.40), color=ALT, fontsize=9)
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    fig.savefig(os.path.join(HERE, "fig2_nonrel_expansion.svg"), format="svg", bbox_inches="tight")
    plt.close(fig)
    caps["fig2_nonrel_expansion.svg"] = (
        r"Kinetic energy $E-m$ vs momentum from the module: the exact "
        r"$\sqrt{p^2+m^2}-m$ (nonrel_energy) against the truncated "
        r"energy_expansion. The order-1 term is the Schrodinger $p^2/2m$, which "
        r"over-predicts as $p\to m$; adding the order-2 term $-p^4/8m^3$ tracks the "
        r"exact curve much further. That $-p^4/8m^3$ is the leading relativistic "
        r"correction that opens hydrogen's fine structure (QM-17).")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
