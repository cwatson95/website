"""Module 1.2 figures — the polytropic p-V family whose area is the boundary work,
and the closed-system energy balance as a straight line Q = dU + W.

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
from closed_systems import (                      # noqa: E402
    polytropic_pressure, polytropic_work, heat_transfer,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the same expansion 0.1 -> 0.2 m^3 from 3 bar, along three
    # polytropic paths.  The shaded area under each curve IS the work
    # (polytropic_work); a steeper n means the pressure falls off faster, so
    # less area, so less work delivered.
    p1, V1, V2 = 300.0, 0.1, 0.2                   # kPa, m^3
    Vg = np.linspace(V1, V2, 300)

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    for n, c, ls in ((0.0, INK, "-"), (1.0, FLOW, "--"), (1.4, ALT, ":")):
        p = np.array([polytropic_pressure(p1, V1, v, n) for v in Vg])
        W = polytropic_work(p1, V1, V2, n)
        ax.plot(Vg, p, color=c, lw=2.0, ls=ls,
                label=r"$n=%.1f$:  $W=%.1f$ kJ" % (n, W))
        ax.fill_between(Vg, 0, p, color=c, alpha=0.09, lw=0)
    ax.set_xlim(V1, V2)
    ax.set_ylim(0, 330)
    ax.set_xlabel(r"volume $V$ (m$^3$)")
    ax.set_ylabel(r"pressure $p$ (kPa)")
    ax.set_title(r"Boundary work is the area under the path:  $W=\int_{V_1}^{V_2}p\,dV$")
    ax.legend(loc="lower left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_polytropic_pv.svg")
    caps["fig1_polytropic_pv.svg"] = (
        r"The same expansion of a gas from $V_1=0.1$ to $V_2=0.2$ m$^3$ starting "
        r"at 3 bar, along three quasiequilibrium paths $pV^n=$ const "
        r"(polytropic_pressure). The shaded area under each is the boundary work "
        r"$W=\int p\,dV$ (polytropic_work): 30.0 kJ at constant pressure "
        r"($n=0$), 20.8 kJ isothermal ($n=1$), and 18.2 kJ for $n=1.4$. The "
        r"larger $n$ is, the faster the pressure collapses as the gas expands, "
        r"and the less work the same volume change delivers — the work depends "
        r"on the PATH, not just on the end states.")

    # Fig 2 — the closed-system energy balance Q = dU + W (KE, PE dropped) is a
    # family of parallel straight lines, one per dU: read off the heat that a
    # given work output demands.  heat_transfer() evaluates the line.
    W = np.linspace(-40.0, 60.0, 200)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for dU, c, ls in ((-30.0, INK, "-"), (0.0, FLOW, "--"), (30.0, ALT, ":")):
        Q = [heat_transfer(w, dU) for w in W]
        ax.plot(W, Q, color=c, lw=2.0, ls=ls, label=r"$\Delta U=%+d$ kJ" % dU)
    ax.axhline(0, color="0.7", lw=0.8)
    ax.axvline(0, color="0.7", lw=0.8)
    ax.set_xlabel(r"work done BY the system  $W$ (kJ)")
    ax.set_ylabel(r"heat added  $Q$ (kJ)")
    ax.set_title(r"Closed-system energy balance:  $Q=\Delta U+W$")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_energy_balance.svg")
    caps["fig2_energy_balance.svg"] = (
        r"The closed-system first law $\Delta U=Q-W$, solved for the heat "
        r"(heat_transfer) with $\Delta$KE and $\Delta$PE dropped. For a fixed "
        r"internal-energy change each line has unit slope: every extra kilojoule "
        r"of work the system delivers must be paid for by another kilojoule of "
        r"heat in. The intercept is $\Delta U$ — an adiabatic process ($Q=0$) "
        r"crosses the axis exactly where the work equals $-\Delta U$, i.e. the "
        r"system does work only by spending its own internal energy.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
