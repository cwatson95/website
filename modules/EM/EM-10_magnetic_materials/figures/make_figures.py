"""EM-10 figures -- ferromagnetic hysteresis: the loop, remanence and coercivity.

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
from magnetic_materials import (                   # noqa: E402
    hysteresis_branches, remanence, coercivity,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- a single ferromagnet's M-H loop. The ascending branch (field swept
    # up) is shifted to +Hc, the descending branch to -Hc, so the loop is open:
    # M is history-dependent. Mark remanence M_r and coercivity Hc.
    Ms, Hc, w = 8e5, 5e3, 2e3
    M_up, M_down = hysteresis_branches(Ms, Hc, w)
    M_r = remanence(Ms, Hc, w)
    H_c = coercivity(Ms, Hc, w)
    H = np.linspace(-2.0e4, 2.0e4, 400)
    up = np.array([M_up(h) for h in H]) / 1e5         # field increasing
    dn = np.array([M_down(h) for h in H]) / 1e5       # field decreasing

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(H / 1e3, up, color=INK, lw=2, label=r"increasing $H$ (to $+H_c$)")
    ax.plot(H / 1e3, dn, color=FLOW, lw=2, label=r"decreasing $H$ (to $-H_c$)")
    ax.axhline(0, color="#bbbbbb", lw=0.6); ax.axvline(0, color="#bbbbbb", lw=0.6)
    ax.plot([0, 0], [M_r / 1e5, -M_r / 1e5], "o", color=ALT, ms=6)
    ax.plot([H_c / 1e3, -H_c / 1e3], [0, 0], "s", color=STEEL, ms=6)
    ax.annotate(r"$\pm M_r$ (remanence)", xy=(0, M_r / 1e5),
                xytext=(2.2, M_r / 1e5 - 1.0), color=ALT, fontsize=9.5)
    ax.annotate(r"$\pm H_c$ (coercivity)", xy=(H_c / 1e3, 0),
                xytext=(H_c / 1e3 - 1.0, -3.4), color=STEEL, fontsize=9.5)
    ax.set_xlabel(r"applied field  $H$  (kA/m)")
    ax.set_ylabel(r"magnetization  $M$  ($10^{5}$ A/m)")
    ax.set_title("Ferromagnetic hysteresis loop  ($M$ vs $H$)")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    _save(fig, "fig1_hysteresis_loop.svg")
    caps["fig1_hysteresis_loop.svg"] = (
        "Toy two-branch (tanh) hysteresis loop for a ferromagnet, Ms = 8e5 A/m. The "
        "increasing- and decreasing-field branches differ, so M depends on history; the "
        "curve leaves a remanence Mr at H=0 and is driven back to M=0 only at the "
        "coercive field Hc.")

    # Fig 2 -- soft vs hard ferromagnet: same Ms, different coercivity. A small Hc
    # gives a thin, easily-reset loop (transformer cores); a large Hc gives a fat,
    # retentive loop (permanent magnets).
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for (Hc_i, w_i, col, name) in [(2.0e3, 1.2e3, STEEL, "soft"),
                                   (1.2e4, 3.0e3, FLOW, "hard")]:
        up_i, dn_i = hysteresis_branches(Ms, Hc_i, w_i)
        Hc_lab = coercivity(Ms, Hc_i, w_i) / 1e3
        ax.plot(H / 1e3, np.array([up_i(h) for h in H]) / 1e5, color=col, lw=2,
                label=fr"{name}: $H_c={Hc_lab:.0f}$ kA/m")
        ax.plot(H / 1e3, np.array([dn_i(h) for h in H]) / 1e5, color=col, lw=2)
    ax.axhline(0, color="#bbbbbb", lw=0.6); ax.axvline(0, color="#bbbbbb", lw=0.6)
    ax.set_xlabel(r"applied field  $H$  (kA/m)")
    ax.set_ylabel(r"magnetization  $M$  ($10^{5}$ A/m)")
    ax.set_title("Soft vs hard ferromagnet: loop width = coercivity")
    ax.legend(loc="lower right", frameon=False)
    _save(fig, "fig2_soft_vs_hard.svg")
    caps["fig2_soft_vs_hard.svg"] = (
        "Two hysteresis loops with the same saturation but different coercivity. The soft "
        "material (narrow loop, small Hc) is easily reset and dissipates little per cycle; "
        "the hard material (wide loop, large Hc) retains its magnetization, the basis of a "
        "permanent magnet.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
