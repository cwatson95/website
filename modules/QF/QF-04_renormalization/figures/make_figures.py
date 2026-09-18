"""QF-04 figures — the running couplings (screening vs asymptotic freedom) and a
toy RG beta function with its fixed points.

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
from renormalization import (                      # noqa: E402
    qed_running_alpha, qed_alpha_sm, qcd_running_alpha,
    beta_toy, fixed_point, M_Z,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — running couplings.  QED alpha(Q) GROWS toward the UV (charge
    # screening); QCD alpha_s(Q) SHRINKS (asymptotic freedom).  Opposite-sign
    # beta functions, both from the module's closed-form runners.
    Q_qed = np.logspace(-3, 4, 400)               # GeV
    a_e = np.array([qed_running_alpha(Q) for Q in Q_qed])      # electron loop only
    a_sm = np.array([qed_alpha_sm(Q) for Q in Q_qed])          # full SM threshold sum
    Q_qcd = np.logspace(np.log10(1.5), 4, 400)
    a_s = np.array([qcd_running_alpha(Q) for Q in Q_qcd])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(Q_qed, a_e, color=STEEL, lw=2,
            label=r"QED $\alpha(Q)$, electron loop")
    ax.plot(Q_qed, a_sm, color=INK, lw=2,
            label=r"QED $\alpha(Q)$, all SM fermions")
    ax.plot(Q_qcd, a_s, color=FLOW, lw=2,
            label=r"QCD $\alpha_s(Q)$ (asymptotic freedom)")
    ax.axvline(M_Z, color="#888888", lw=0.8, ls=":")
    ax.annotate(r"$M_Z$", xy=(M_Z, 0.011), color="#666666", fontsize=9, ha="center")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel(r"energy scale $Q$ (GeV)")
    ax.set_ylabel(r"coupling $\alpha$")
    ax.set_title(r"Running couplings: QED grows ($\beta>0$), QCD shrinks ($\beta<0$)")
    ax.legend(loc="center left", frameon=False, fontsize=9)
    _save(fig, "fig1_running_couplings.svg")
    caps["fig1_running_couplings.svg"] = (
        r"Running couplings from the module's closed forms. The QED fine-structure "
        r"constant $\alpha(Q)$ (qed_running_alpha / qed_alpha_sm) GROWS toward high "
        r"energy — vacuum-polarization screening, $\beta>0$ — climbing from "
        r"$\alpha\simeq1/137$ at low $Q$ to $\simeq1/128$ at $M_Z$ once all charged "
        r"Standard-Model fermions are summed. The QCD coupling $\alpha_s(Q)$ "
        r"(qcd_running_alpha) instead SHRINKS with energy: asymptotic freedom, the "
        r"opposite-sign $\beta<0$.")

    # Fig 2 — a toy beta function beta(g)=a g^2 - b g^3 (beta_toy) with its two
    # fixed points: g=0 (UV-repulsive) and g*=a/b (UV-attractive), the slope
    # beta'(g*) the linearized RG eigenvalue that bridges to critical exponents.
    a, b = 2.0, 4.0
    fp = fixed_point(a, b)
    g_star = fp["g_star"]
    g = np.linspace(-0.05, 0.75, 400)
    beta = beta_toy(g, a, b)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(g, beta, color=INK, lw=2.2, label=r"$\beta(g)=a\,g^2-b\,g^3$")
    ax.axhline(0, color="#aaaaaa", lw=0.8)
    ax.plot([0.0], [0.0], "o", ms=8, mfc="white", mec=FLOW, mew=2)
    ax.plot([g_star], [0.0], "o", ms=8, color=ALT)
    ax.annotate("Gaussian fixed point\n$g=0$ (UV-repulsive)", xy=(0.0, 0.0),
                xytext=(0.07, -0.085), color=FLOW, fontsize=8.5,
                arrowprops=dict(arrowstyle="->", color=FLOW, lw=1.0))
    ax.annotate(r"$g_*=a/b=%.2f$" % g_star + "\n(UV-attractive)", xy=(g_star, 0.0),
                xytext=(g_star - 0.02, 0.05), color=ALT, fontsize=8.5,
                arrowprops=dict(arrowstyle="->", color=ALT, lw=1.0))
    # RG flow arrows on the g-axis: dg/dln(mu)=beta, so flow points toward g*.
    for g0 in (0.18, 0.36, 0.62):
        d = np.sign(beta_toy(g0, a, b))
        ax.annotate("", xy=(g0 + 0.05 * d, 0.0), xytext=(g0, 0.0),
                    arrowprops=dict(arrowstyle="-|>", color=STEEL, lw=1.6))
    ax.set_xlim(-0.05, 0.75)
    ax.set_xlabel(r"coupling $g$")
    ax.set_ylabel(r"$\beta(g)=\mu\,dg/d\mu$")
    ax.set_title(r"RG flow of a toy $\beta$: couplings run into $g_*$ ($\beta'(g_*)=-a^2/b<0$)")
    ax.legend(loc="lower left", frameon=False, fontsize=9)
    _save(fig, "fig2_fixed_point.svg")
    caps["fig2_fixed_point.svg"] = (
        r"Toy renormalization-group flow from beta_toy$(g)=a g^2-b g^3$ "
        r"($a=2,b=4$). The beta function vanishes at two fixed points (fixed_point): "
        r"the Gaussian one $g=0$ (open, UV-repulsive) and $g_*=a/b=0.5$ (filled, "
        r"UV-attractive). Because $dg/d\ln\mu=\beta$, the flow arrows point toward "
        r"$g_*$ from both sides; the slope there, $\beta'(g_*)=-a^2/b<0$, is the "
        r"linearized RG eigenvalue — the same object that fixes the critical "
        r"exponents of statistical mechanics.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
