"""Module 1.5 figures — three quasiequilibrium paths between the SAME end states
enclose different areas (work is path-dependent), and the trapezoid rule used by
pdv_work converges on the closed form at second order.

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
from quasiequilibrium import (                    # noqa: E402
    pdv_work, polytropic_work, path_work,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the module's whole point, drawn.  A=(100 kPa, 2 m^3) compressed to
    # B=(200 kPa, 1 m^3) along three different quasiequilibrium paths.  Same end
    # states, three different enclosed areas, three different works.
    pA, VA, pB, VB = 100.0, 2.0, 200.0, 1.0
    W1 = polytropic_work(pA, VA, VB, 1.0)                       # isothermal pV=200
    W2 = path_work([("p", pA, VA, VB), ("V", VB)])              # const-p then const-V
    W3 = path_work([("V", VA), ("p", pB, VA, VB)])              # const-V then const-p

    Vg = np.linspace(VB, VA, 300)
    fig, ax = plt.subplots(figsize=(6.2, 3.9))
    ax.plot(Vg, 200.0 / Vg, color=INK, lw=2.2,
            label=r"1  isothermal $pV=$const:  $W=%.1f$ kJ" % W1)
    ax.plot([VA, VB, VB], [pA, pA, pB], color=FLOW, lw=2.0, ls="--",
            label=r"2  const-$p$ then const-$V$:  $W=%.1f$ kJ" % W2)
    ax.plot([VA, VA, VB], [pA, pB, pB], color=ALT, lw=2.0, ls=":",
            label=r"3  const-$V$ then const-$p$:  $W=%.1f$ kJ" % W3)
    ax.plot([VA, VB], [pA, pB], ls="none", marker="o", ms=8, mfc="white",
            mec="0.25", mew=1.8, zorder=5)
    ax.annotate("A", xy=(VA, pA), xytext=(VA - 0.07, pA - 18), fontsize=11,
                color="0.25")
    ax.annotate("B", xy=(VB, pB), xytext=(VB + 0.03, pB + 8), fontsize=11,
                color="0.25")
    ax.set_xlim(0.85, 2.22)
    ax.set_ylim(30, 225)
    ax.set_xlabel(r"volume $V$ (m$^3$)")
    ax.set_ylabel(r"pressure $p$ (kPa)")
    ax.set_title(r"Same end states, different paths, different work")
    ax.legend(loc="lower left", frameon=False, fontsize=8.5)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_path_dependence.svg")
    caps["fig1_path_dependence.svg"] = (
        r"Work is a path function, not a property. The same compression from "
        r"A $=(100$ kPa, 2 m$^3)$ to B $=(200$ kPa, 1 m$^3)$ is carried out along "
        r"three quasiequilibrium paths, and the area under each differs: "
        + "%.1f, %.1f and %.1f" % (W1, W2, W3) +
        r" kJ (polytropic_work and path_work; negative because work is done ON "
        r"the gas). Only because each path is quasiequilibrium — slow enough that "
        r"a single pressure exists at every instant — can it be drawn as a curve "
        r"at all. $\Delta U$ between A and B is the same for all three; $W$ and "
        r"$Q$ are not.")

    # Fig 2 — numerics.  pdv_work integrates p(V) by the trapezoid rule; compare
    # against the exact polytropic closed form.  Log-log slope -2 is the
    # signature of a second-order rule, and a reference line confirms it.
    p1, V1, V2, n = 300.0, 0.1, 0.2, 1.4
    exact = polytropic_work(p1, V1, V2, n)
    p_of_V = lambda V: p1 * (V1 / V) ** n
    steps = np.array([2, 4, 8, 16, 32, 64, 128, 256, 512, 1024])
    err = np.array([abs(pdv_work(p_of_V, V1, V2, int(N)) - exact) for N in steps])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.loglog(steps, err, color=INK, lw=2.0, marker="o", ms=6, mfc="white",
              mew=1.6, label=r"|trapezoid $-$ closed form|")
    ax.loglog(steps, err[0] * (steps / steps[0]) ** -2.0, color=FLOW, lw=1.6,
              ls="--", label=r"second order, $\propto N^{-2}$")
    ax.set_xlabel(r"number of trapezoid steps $N$")
    ax.set_ylabel(r"absolute error in $W$ (kJ)")
    ax.set_title(r"pdv_work converges on $\int p\,dV$ at second order")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6, which="both")
    _save(fig, "fig2_trapezoid_convergence.svg")
    caps["fig2_trapezoid_convergence.svg"] = (
        r"The numerical method behind pdv_work, checked against a case with a "
        r"closed-form answer. Integrating $p=p_1(V_1/V)^{1.4}$ from 0.1 to "
        r"0.2 m$^3$ by the trapezoid rule and differencing against "
        r"polytropic_work gives an error that falls as $N^{-2}$ — the reference "
        r"line has slope $-2$ — so each doubling of the step count cuts the error "
        r"fourfold. The module's default of 20000 steps therefore sits far below "
        r"any tolerance that matters here, and the routine can be trusted on "
        r"paths $p(V)$ that have no closed form at all.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
