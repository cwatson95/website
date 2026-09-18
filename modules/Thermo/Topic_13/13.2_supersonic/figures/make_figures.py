"""Module 13.2 figures — the two branches of the area-Mach relation, and choking:
the point past which lowering the back pressure buys nothing.

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
from supersonic import (                          # noqa: E402
    area_mach_ratio, critical_pressure_ratio, critical_temperature_ratio,
    is_choked, mach_from_pressure_ratio, mach_from_area_ratio,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

K = 1.4


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — A/A* has a minimum of 1 at M = 1, so every area ratio above 1
    # corresponds to TWO Mach numbers: one subsonic, one supersonic.  Which one
    # a real nozzle takes is decided by the back pressure, not the geometry.
    M_sub = np.linspace(0.10, 1.0, 300)
    M_sup = np.linspace(1.0, 3.2, 300)
    A_sub = np.array([area_mach_ratio(m, K) for m in M_sub])
    A_sup = np.array([area_mach_ratio(m, K) for m in M_sup])

    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.plot(A_sub, M_sub, color=INK, lw=2.3, label=r"subsonic branch")
    ax.plot(A_sup, M_sup, color=FLOW, lw=2.3, ls="--", label=r"supersonic branch")
    ax.plot([1.0], [1.0], marker="o", ms=9, mfc="white", mec=ALT, mew=2.0,
            ls="none", label=r"throat: $A/A^*=1$, $M=1$")
    A_pick = 2.0
    for sup, c in ((False, INK), (True, FLOW)):
        m = mach_from_area_ratio(A_pick, K, supersonic=sup)
        ax.plot([A_pick], [m], marker="s", ms=7, mfc="white", mec=c, mew=1.7,
                ls="none")
        ax.annotate(r"$M=%.3f$" % m, xy=(A_pick, m), xytext=(A_pick + 0.16, m),
                    fontsize=9, color=c, va="center")
    ax.axvline(A_pick, color="0.75", lw=1.0, ls=":")
    ax.set_xlim(0.9, 4.0)
    ax.set_ylim(0, 3.3)
    ax.set_xlabel(r"area ratio $A/A^*$")
    ax.set_ylabel(r"Mach number $M$")
    ax.set_title(r"One area ratio, two possible Mach numbers")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_area_mach.svg")
    caps["fig1_area_mach.svg"] = (
        r"The isentropic area relation $A/A^*$ (area_mach_ratio) has a minimum "
        r"value of exactly 1 at $M=1$, so a duct twice the throat area can carry "
        r"either $M=" + "%.3f" % mach_from_area_ratio(2.0, K, supersonic=False) +
        r"$ or $M=" + "%.3f" % mach_from_area_ratio(2.0, K, supersonic=True) +
        r"$ — the two roots mach_from_area_ratio returns depending on its "
        r"`supersonic` flag. Geometry alone does not decide; the back pressure "
        r"does. This double-valuedness is why converging-diverging nozzles have "
        r"several distinct operating regimes, and why a nozzle designed for "
        r"supersonic exit behaves as a plain venturi when it is run at too high "
        r"a back pressure.")

    # Fig 2 — choking.  Lowering the back pressure raises the mass flow until
    # the throat reaches M = 1; below the critical ratio nothing further happens
    # upstream, no matter how hard you pull.
    pb_ratio = np.linspace(0.02, 1.0, 400)          # p_back / p_0
    p_crit = critical_pressure_ratio(K)
    mdot = np.where(pb_ratio > p_crit,
                    np.sqrt(np.maximum(pb_ratio ** (2.0 / K)
                                       - pb_ratio ** ((K + 1.0) / K), 0.0)),
                    np.sqrt(p_crit ** (2.0 / K) - p_crit ** ((K + 1.0) / K)))
    mdot = mdot / mdot.max()            # the choked value IS the maximum

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot(pb_ratio, mdot, color=INK, lw=2.4)
    ax.axvline(p_crit, color=FLOW, lw=1.6, ls="--")
    ax.fill_between(pb_ratio, 0, mdot, where=(pb_ratio <= p_crit), color=ALT,
                    alpha=0.13, lw=0)
    ax.text(p_crit - 0.03, 0.45, r"CHOKED: $M=1$ at the throat," "\n"
                                 r"mass flow will not increase",
            fontsize=9, color="0.3", ha="right")
    ax.text(p_crit + 0.03, 0.22,
            r"$p^*/p_o=%.4f$" % p_crit, fontsize=9.5, color=FLOW)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.08)
    ax.set_xlabel(r"back-pressure ratio $p_B/p_o$")
    ax.set_ylabel(r"mass flow / choked mass flow")
    ax.set_title(r"A converging nozzle chokes and stops responding")
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_choking.svg")
    caps["fig2_choking.svg"] = (
        r"Mass flow through a converging nozzle as the back pressure is lowered. "
        r"It climbs until the throat reaches $M=1$, at the critical ratio "
        r"$p^*/p_o=(2/(k+1))^{k/(k-1)}=" + "%.4f" % p_crit + r"$ "
        r"(critical_pressure_ratio) — and then stops. Below that the flow is "
        r"CHOKED (is_choked): information cannot travel upstream against a sonic "
        r"throat, so the nozzle simply cannot be told that the outside has got "
        r"emptier. The corresponding throat temperature is "
        + "%.4f" % critical_temperature_ratio(K) + r" of the stagnation value. "
        r"Getting more flow then requires a bigger throat or a higher supply "
        r"pressure, never a lower exit pressure. mach_from_pressure_ratio "
        r"recovers $M$ from a measured $p_o/p$ in the unchoked range.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
