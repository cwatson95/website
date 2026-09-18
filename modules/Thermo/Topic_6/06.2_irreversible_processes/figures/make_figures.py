"""Module 6.2 figures — the sign of sigma as a three-way verdict on a process, and
the entropy a steady heat leak pours out per second.

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
from irreversible import (                        # noqa: E402
    IRREVERSIBILITIES, entropy_production, sigma_isolated,
    entropy_production_rate, is_possible, classify_process,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the entropy balance as a verdict.  Sweep the entropy transfer
    # against a fixed system entropy change; sigma is the shortfall, and its sign
    # sorts every conceivable process into three bins (classify_process).
    dS = 1.0
    transfer = np.linspace(-0.6, 1.6, 400)
    sigma = np.array([entropy_production(dS, t) for t in transfer])

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.axhspan(-1.0, 0.0, color=FLOW, alpha=0.12, lw=0)
    ax.plot(transfer, sigma, color=INK, lw=2.4,
            label=r"$\sigma=\Delta S-\int\delta Q/T_b$")
    ax.axhline(0.0, color="0.5", lw=1.2, ls="-.")
    ax.plot([dS], [0.0], marker="o", ms=8.5, mfc="white", mec=ALT, mew=1.9,
            ls="none", label=r"internally reversible ($\sigma=0$)")
    ax.text(-0.5, -0.34, r"$\sigma<0$: IMPOSSIBLE" "\n"
                         r"(is_possible $\rightarrow$ False)",
            fontsize=9.5, color=FLOW)
    ax.text(-0.5, 0.72, r"$\sigma>0$: irreversible — every real process",
            fontsize=9.5, color="0.3")
    ax.set_xlim(-0.6, 1.6)
    ax.set_ylim(-0.65, 1.65)
    ax.set_xlabel(r"entropy transferred in with heat  $\int\delta Q/T_b$ (kJ/K)")
    ax.set_ylabel(r"entropy produced $\sigma$ (kJ/K)")
    ax.set_title(r"The entropy balance sorts processes into three bins")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_sigma_verdict.svg")
    caps["fig1_sigma_verdict.svg"] = (
        r"The closed-system entropy balance solved for the production term "
        r"(entropy_production): whatever entropy change is not accounted for by "
        r"transfer with heat must have been generated inside. Its sign is a "
        r"verdict rather than a quantity to be minimised away — negative is "
        r"IMPOSSIBLE (is_possible returns False, the shaded band), zero is the "
        r"internally reversible idealization, and positive covers every process "
        r"that actually happens. classify_process returns these three labels "
        r"directly. The module lists "
        + "%d" % len(IRREVERSIBILITIES) + r" named mechanisms — friction, "
        r"unrestrained expansion, heat transfer across a finite temperature "
        r"difference, mixing — that push a real process off the $\sigma=0$ line.")

    # Fig 2 — a steady heat leak.  A component holding steady state while losing
    # heat through a boundary at Tb produces entropy at Qdot/Tb; the colder the
    # boundary it dumps across, the more entropy per joule.
    Tb = np.linspace(280.0, 900.0, 400)
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    for Qdot, c, ls in ((-1.0, INK, "-"), (-3.0, FLOW, "--"), (-6.0, ALT, ":")):
        rate = np.array([entropy_production_rate(Qdot, t) for t in Tb])
        ax.plot(Tb, rate, color=c, lw=2.1, ls=ls,
                label=r"$\dot{Q}=%.0f$ kW lost" % Qdot)
    ax.set_xlim(280, 900)
    ax.set_xlabel(r"boundary temperature $T_b$ (K)")
    ax.set_ylabel(r"entropy production rate $\dot{\sigma}$ (kW/K)")
    ax.set_title(r"A steady heat leak is an entropy source")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_steady_entropy_rate.svg")
    caps["fig2_steady_entropy_rate.svg"] = (
        r"A component at steady state stores no entropy, so whatever it produces "
        r"must leave with the heat: $\dot\sigma=-\dot Q/T_b$ "
        r"(entropy_production_rate). Losing 3 kW across a 300 K surface "
        r"generates " + "%.4f" % entropy_production_rate(-3.0, 300.0) + r" kW/K, "
        r"but the same 3 kW leaving a 900 K surface generates only "
        + "%.4f" % entropy_production_rate(-3.0, 900.0) + r" kW/K — a third as "
        r"much, because entropy is heat divided by the temperature it crosses "
        r"at. sigma_isolated applies the same accounting to a composite isolated "
        r"system, where the total can only grow.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
