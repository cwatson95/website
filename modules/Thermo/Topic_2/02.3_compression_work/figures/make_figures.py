"""Module 2.3 figures — the work that must be SUPPLIED to compress a gas, and how
the polytropic exponent sets the bill.

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
from compression_work import (                    # noqa: E402
    compression_work, work_input, polytropic_compression,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — compressing 0.2 -> 0.1 m^3 from 1 bar along three polytropic paths.
    # The isothermal path (n=1) stays lowest and is the cheapest; an adiabatic
    # compression (n=1.4) heats the gas, raising p at every volume, so the area
    # that must be paid for is larger.
    p1, V1, V2 = 100.0, 0.20, 0.10
    Vg = np.linspace(V2, V1, 300)

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    for n, c, ls in ((1.0, INK, "-"), (1.2, FLOW, "--"), (1.4, ALT, ":")):
        p = p1 * (V1 / Vg) ** n
        Win = -polytropic_compression(p1, V1, V2, n)
        ax.plot(Vg, p, color=c, lw=2.1, ls=ls,
                label=r"$n=%.1f$:  input $%.1f$ kJ" % (n, Win))
        ax.fill_between(Vg, 0, p, color=c, alpha=0.08, lw=0)
    ax.set_xlim(V2, V1)
    ax.set_ylim(0, 290)
    ax.set_xlabel(r"volume $V$ (m$^3$)   (compression runs right $\rightarrow$ left)")
    ax.set_ylabel(r"pressure $p$ (kPa)")
    ax.set_title(r"Compression: the area you have to pay for")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_compression_pv.svg")
    caps["fig1_compression_pv.svg"] = (
        r"Halving the volume of a gas from 0.2 to 0.1 m$^3$ starting at 1 bar, "
        r"along three polytropic paths $pV^n=$ const. The work is negative by the "
        r"sign convention (energy flows INTO the system), so the labels give its "
        r"magnitude — the input required. Isothermal compression is cheapest "
        r"because the gas is cooled as it is squeezed and its pressure stays low; "
        r"the adiabatic path $n=1.4$ traps the heat of compression, lifting the "
        r"pressure at every volume and enlarging the area. This is why real "
        r"compressors are intercooled.")

    # Fig 2 — the price as a continuous function of n.  work_input evaluates the
    # same integral numerically, and lands on the closed-form curve.
    ns = np.linspace(1.0, 1.6, 200)
    Win = np.array([-polytropic_compression(p1, V1, V2, n) for n in ns])
    check_n = [1.0, 1.2, 1.4, 1.6]
    check_W = [work_input(lambda V, n=n: p1 * (V1 / V) ** n, V1, V2) for n in check_n]

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(ns, Win, color=INK, lw=2.2, label=r"closed form  $-(p_2V_2-p_1V_1)/(1-n)$")
    ax.plot(check_n, check_W, ls="none", marker="o", ms=7, mfc="white", mec=FLOW,
            mew=1.8, label=r"work_input (numerical $\int p\,dV$)")
    ax.set_xlim(1.0, 1.6)
    ax.set_xlabel(r"polytropic exponent $n$")
    ax.set_ylabel(r"work input required (kJ)")
    ax.set_title(r"A stiffer path costs more to compress")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_work_input_vs_n.svg")
    caps["fig2_work_input_vs_n.svg"] = (
        r"The compression bill as a continuous function of the polytropic "
        r"exponent, for the same 2:1 volume reduction. It climbs from "
        + "%.1f" % Win[0] + r" kJ at $n=1$ (isothermal, fully intercooled) to "
        + "%.1f" % Win[-1] + r" kJ at $n=1.6$ — about "
        + "%.0f" % (100 * (Win[-1] / Win[0] - 1)) + r"% more for the same volume "
        r"change. The open circles are the module's numerical quadrature "
        r"work_input evaluated at four exponents; they sit on the closed-form "
        r"curve, confirming the two routes agree.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
