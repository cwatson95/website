"""SM-05 figures — the mean-field order parameter and the Landau double well.

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
from phase_transitions import (                    # noqa: E402
    spontaneous_magnetization, ising_1d_magnetization,
    landau_free_energy, landau_equilibrium_magnetization, K_B,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — order parameter vs T/Tc: mean-field Ising switches on continuously
    # below Tc (the module's bisection solver), while the exact 1-D chain at h=0
    # stays identically zero -- no transition in one dimension.
    Tc = 300.0
    tr = np.linspace(0.02, 1.4, 600)               # reduced temperature T/Tc
    m_mf = np.array([spontaneous_magnetization(float(t) * Tc, Tc) for t in tr])
    J = K_B * Tc
    m_1d = np.array([ising_1d_magnetization(float(t) * Tc, J, 0.0) for t in tr])
    # leading near-Tc behaviour m ~ sqrt(3)(1 - T/Tc)^{1/2}, the exponent beta=1/2
    tg = np.linspace(0.84, 1.0, 120)
    m_guide = np.sqrt(3.0) * np.sqrt(1.0 - tg)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(tr, m_mf, color=INK, lw=2, label="mean-field Ising  (spontaneous $m$)")
    ax.plot(tg, m_guide, color=ALT, lw=1.6, ls="--",
            label=r"near $T_c$: $\sqrt{3}\,(1-T/T_c)^{1/2}$  ($\beta=\frac{1}{2}$)")
    ax.plot(tr, m_1d, color=FLOW, lw=2, label="exact 1-D Ising ($h=0$): no transition")
    ax.axvline(1.0, color="#aaaaaa", lw=0.9, ls=":")
    ax.annotate(r"$T_c$", xy=(1.0, 0.05), xytext=(1.08, 0.16), color="#666666", fontsize=10)
    ax.set_xlim(0, 1.4)
    ax.set_ylim(-0.03, 1.05)
    ax.set_xlabel(r"reduced temperature $T/T_c$")
    ax.set_ylabel(r"magnetization $m$")
    ax.set_title("Spontaneous magnetization: a second-order transition at $T_c$")
    ax.legend(loc="lower left", frameon=False, fontsize=9)
    _save(fig, "fig1_order_parameter.svg")
    caps["fig1_order_parameter.svg"] = (
        r"Order parameter vs $T/T_c$. The mean-field Ising magnetization (blue, from "
        r"spontaneous_magnetization) rises continuously below $T_c$ as "
        r"$\sqrt{3}\,(1-T/T_c)^{1/2}$ (dashed guide, exponent $\beta=\frac{1}{2}$) -- a "
        r"second-order transition. The exact 1-D chain at $h=0$ (orange, "
        r"ising_1d_magnetization) is zero at every $T>0$: fluctuations forbid order in "
        r"one dimension.")

    # Fig 2 — Landau free energy F(m) = a(T-Tc)m^2 + b m^4: a single well above Tc
    # turns into a symmetric double well below it.  Minima from the module.
    Tc = 1.0                                        # Landau units (a=b=1)
    m = np.linspace(-0.95, 0.95, 600)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for T, col in [(1.3, STEEL), (1.0, ALT), (0.7, FLOW), (0.4, INK)]:
        F = np.array([landau_free_energy(float(mm), T, Tc) for mm in m])
        ax.plot(m, F, color=col, lw=2, label=fr"$T={T:.1f}\,T_c$")
        m0 = landau_equilibrium_magnetization(T, Tc)
        for s in ((-1, 1) if m0 > 0 else (0,)):
            ax.plot([s * m0], [landau_free_energy(s * m0, T, Tc)],
                    marker="o", ms=5, color=col)
    ax.axhline(0.0, color="#cccccc", lw=0.6)
    ax.annotate("single well\n$T>T_c$", xy=(0.0, 0.06), xytext=(0.30, 0.17),
                color=STEEL, fontsize=9, ha="center")
    ax.annotate(r"double well $T<T_c$: $\pm m_0$", xy=(-0.55, -0.07),
                xytext=(-0.9, 0.12), color=INK, fontsize=9)
    ax.set_xlim(-0.95, 0.95)
    ax.set_ylim(-0.12, 0.28)
    ax.set_xlabel(r"order parameter $m$")
    ax.set_ylabel(r"Landau free energy $F(m)$")
    ax.set_title(r"Landau theory: single well $\to$ double well below $T_c$")
    ax.legend(loc="upper center", frameon=False, fontsize=9, ncol=2)
    _save(fig, "fig2_landau_free_energy.svg")
    caps["fig2_landau_free_energy.svg"] = (
        r"Landau free energy $F(m)=a(T-T_c)m^2+b\,m^4$ from landau_free_energy (units "
        r"$a=b=1$). Above $T_c$ a single well pins $m=0$; at $T_c$ the curvature "
        r"vanishes; below $T_c$ a symmetric double well appears with minima at "
        r"$\pm m_0=\pm\sqrt{a(T_c-T)/2b}$ (dots, landau_equilibrium_magnetization) -- "
        r"spontaneous symmetry breaking, again with $\beta=\frac{1}{2}$.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
