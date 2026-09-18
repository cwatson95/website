"""SM-02 figures — the Carnot limits (engine efficiency & refrigerator/heat-pump
COP) and temperature emerging from entropy via 1/T = dS/dU.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
"""
import json
import math
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
from laws_of_thermodynamics import (              # noqa: E402
    carnot_efficiency, carnot_cop_refrigerator, carnot_cop_heat_pump,
    temperature_from_entropy, K_B,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the Carnot limits between a fixed cold reservoir T_c and a varying
    # hot reservoir T_h: engine efficiency (left axis) climbs toward 1, while the
    # reversible refrigerator / heat-pump COPs (right axis) diverge as T_h -> T_c.
    Tc = 300.0
    Th = np.linspace(Tc + 5.0, 1500.0, 400)
    eta = np.array([carnot_efficiency(Tc, t) for t in Th])
    cop_r = np.array([carnot_cop_refrigerator(Tc, t) for t in Th])
    cop_hp = np.array([carnot_cop_heat_pump(Tc, t) for t in Th])

    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    l1, = ax.plot(Th, eta, color=INK, lw=2.2,
                  label=r"engine $\eta=1-T_c/T_h$")
    ax.set_xlabel(r"hot reservoir $T_h$ (K)   ($T_c=300$ K)")
    ax.set_ylabel(r"Carnot efficiency $\eta$", color=INK)
    ax.set_ylim(0, 1.0)
    ax.tick_params(axis="y", labelcolor=INK)
    ax2 = ax.twinx()
    l2, = ax2.plot(Th, cop_r, color=FLOW, lw=2,
                   label=r"fridge COP $=T_c/(T_h-T_c)$")
    l3, = ax2.plot(Th, cop_hp, color=STEEL, lw=2, ls="--",
                   label=r"heat-pump COP $=T_h/(T_h-T_c)$")
    ax2.set_ylabel(r"coefficient of performance", color=FLOW)
    ax2.set_ylim(0, 16)
    ax2.tick_params(axis="y", labelcolor=FLOW)
    ax.set_title(r"Carnot limits between $T_c$ and $T_h$")
    ax.legend(handles=[l1, l2, l3], loc="center right", frameon=False, fontsize=9)
    _save(fig, "fig1_carnot.svg")
    caps["fig1_carnot.svg"] = (
        r"The reversible Carnot bounds between a cold reservoir $T_c=300$ K and a "
        r"hot one $T_h$. The engine efficiency $\eta=1-T_c/T_h$ (carnot_efficiency, "
        r"left axis) is zero when $T_h=T_c$ and climbs toward $1$ only as "
        r"$T_h\to\infty$; the refrigerator and heat-pump coefficients of performance "
        r"(carnot_cop_refrigerator / carnot_cop_heat_pump, right axis) instead "
        r"diverge as $T_h\to T_c$ — moving heat across a vanishing gap is nearly "
        r"free. No real device beats these limits.")

    # Fig 2 — temperature emerges from entropy.  Feed the ideal-gas entropy
    # S(U)=(3/2)Nk ln U to temperature_from_entropy (a numerical 1/T=dS/dU): the
    # recovered T is linear in U, i.e. U=(3/2)NkT (equipartition).
    N = 1.0
    S_of_U = lambda U: 1.5 * N * K_B * math.log(U)
    U = np.linspace(1.0e-21, 2.0e-20, 200)
    T_num = np.array([temperature_from_entropy(S_of_U, float(u)) for u in U])
    T_exact = U / (1.5 * N * K_B)                  # from U = (3/2) N k T

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(U * 1e21, T_exact, color=INK, lw=2,
            label=r"$U=\frac{3}{2}Nk_BT$ (equipartition)")
    ax.plot((U * 1e21)[::8], T_num[::8], ls="none", marker="o", ms=5, mfc="white",
            mec=FLOW, mew=1.6, label=r"$T$ from $1/T=dS/dU$ (numeric)")
    ax.set_xlim(0, 20)
    ax.set_xlabel(r"internal energy $U$  ($10^{-21}$ J)")
    ax.set_ylabel(r"temperature $T$ (K)")
    ax.set_title(r"Temperature is defined by entropy: $1/T=(\partial S/\partial U)_{V,N}$")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig2_temperature_from_entropy.svg")
    caps["fig2_temperature_from_entropy.svg"] = (
        r"Temperature emerges from entropy. Feeding the ideal-gas entropy "
        r"$S(U)=\tfrac32 Nk_B\ln U$ to temperature_from_entropy — a numerical "
        r"$1/T=(\partial S/\partial U)_{V,N}$ — returns a temperature (circles) that "
        r"is exactly linear in $U$, i.e. $U=\tfrac32 Nk_BT$ (line). The second law's "
        r"definition of $T$ thus reproduces equipartition: each of the three "
        r"translational degrees of freedom carries $\tfrac12 k_BT$.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
