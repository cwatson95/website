"""Module 2.2 figures — the area an expanding gas sweeps out at constant pressure
versus isothermally, and how the two diverge as the expansion ratio grows.

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
from expansion_work import (                      # noqa: E402
    expansion_work, constant_pressure_expansion, isothermal_expansion,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — same expansion, two idealizations.  Holding p constant keeps the
    # full rectangle; letting the gas cool along pV = const drops the pressure as
    # it expands, so the area under the curve is smaller.
    p1, V1, V2 = 300.0, 0.10, 0.30
    W_iso = isothermal_expansion(p1, V1, V2)
    W_cp = constant_pressure_expansion(p1, V1, V2)
    Vg = np.linspace(V1, V2, 300)
    p_iso = p1 * V1 / Vg

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(Vg, np.full_like(Vg, p1), color=INK, lw=2.2,
            label=r"constant $p$:  $W=%.1f$ kJ" % W_cp)
    ax.fill_between(Vg, 0, p1, color=INK, alpha=0.10, lw=0)
    ax.plot(Vg, p_iso, color=FLOW, lw=2.2, ls="--",
            label=r"isothermal $pV=$const:  $W=%.1f$ kJ" % W_iso)
    ax.fill_between(Vg, 0, p_iso, color=FLOW, alpha=0.16, lw=0)
    ax.set_xlim(V1, V2)
    ax.set_ylim(0, 340)
    ax.set_xlabel(r"volume $V$ (m$^3$)")
    ax.set_ylabel(r"pressure $p$ (kPa)")
    ax.set_title(r"Expansion work is the swept area")
    ax.legend(loc="lower left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_expansion_pv.svg")
    caps["fig1_expansion_pv.svg"] = (
        r"The same gas tripling its volume from 0.1 to 0.3 m$^3$ starting at "
        r"3 bar, under two idealizations. Held at constant pressure it sweeps the "
        r"full rectangle, " + "%.1f" % W_cp + r" kJ (constant_pressure_expansion); "
        r"expanding isothermally along $pV=$ const the pressure falls as the "
        r"volume grows and the area shrinks to " + "%.1f" % W_iso +
        r" kJ (isothermal_expansion). Both are positive because the system does "
        r"work on its surroundings — expansion work is energy leaving the system.")

    # Fig 2 — sweep the expansion ratio.  The constant-pressure work is linear in
    # V2 while the isothermal work is logarithmic, so the gap widens without
    # bound: the further a gas expands, the more the assumption matters.
    ratio = np.linspace(1.0, 8.0, 300)
    V2s = V1 * ratio
    W_cp_s = np.array([constant_pressure_expansion(p1, V1, v) for v in V2s])
    W_iso_s = np.array([isothermal_expansion(p1, V1, v) for v in V2s])
    W_quad = expansion_work(lambda V: p1 * V1 / V, V1, V1 * 8.0)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(ratio, W_cp_s, color=INK, lw=2.2, label=r"constant $p$  (linear in $V_2$)")
    ax.plot(ratio, W_iso_s, color=FLOW, lw=2.2, ls="--",
            label=r"isothermal  ($\propto\ln V_2/V_1$)")
    ax.set_xlim(1, 8)
    ax.set_xlabel(r"expansion ratio $V_2/V_1$")
    ax.set_ylabel(r"work delivered $W$ (kJ)")
    ax.set_title(r"Linear versus logarithmic growth of the work")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_work_vs_ratio.svg")
    caps["fig2_work_vs_ratio.svg"] = (
        r"Why the process idealization cannot be waved away. Sweeping the "
        r"expansion ratio, the constant-pressure work grows linearly in $V_2$ "
        r"while the isothermal work grows only as $\ln(V_2/V_1)$, so the two "
        r"diverge steadily: at an eight-fold expansion they are "
        + "%.1f" % W_cp_s[-1] + r" kJ against " + "%.1f" % W_iso_s[-1] +
        r" kJ, a factor of " + "%.1f" % (W_cp_s[-1] / W_iso_s[-1]) + r". The "
        r"general quadrature expansion_work applied to the isothermal path "
        r"returns " + "%.1f" % W_quad + r" kJ, agreeing with the closed form.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
