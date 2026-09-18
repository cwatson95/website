"""Module 9.3 figures — the Diesel cycle on p-v, and the cutoff-ratio penalty that
keeps it below Otto at equal compression ratio.

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
from diesel_cycle import (                        # noqa: E402
    K_AIR, diesel_efficiency, cutoff_ratio,
    temp_after_isentropic_compression, temp_after_constant_pressure_heat,
    temp_after_isentropic_expansion,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

R_AIR = 0.287                                      # kJ/kg.K


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — Diesel differs from Otto in one process: heat is added at constant
    # PRESSURE while the piston is already moving out (2->3 is horizontal), not
    # at constant volume.  That flat top is the whole distinction.
    r, rc, T1, p1 = 18.0, 2.0, 300.0, 100.0
    v1 = R_AIR * T1 / p1
    v2 = v1 / r
    v3 = rc * v2
    T2 = temp_after_isentropic_compression(T1, r)
    T3 = temp_after_constant_pressure_heat(T2, rc)
    T4 = temp_after_isentropic_expansion(T3, r, rc)
    p2 = p1 * r ** K_AIR
    p3 = p2
    p4 = p1 * T4 / T1

    v_12 = np.linspace(v2, v1, 200)
    p_12 = p1 * (v1 / v_12) ** K_AIR
    v_34 = np.linspace(v3, v1, 200)
    p_34 = p3 * (v3 / v_34) ** K_AIR

    fig, ax = plt.subplots(figsize=(6.2, 3.9))
    ax.plot(v_12, p_12, color=INK, lw=2.2, label=r"1$\rightarrow$2 isentropic compression")
    ax.plot([v2, v3], [p2, p3], color=ALT, lw=2.6,
            label=r"2$\rightarrow$3 heat in at const. $p$")
    ax.plot(v_34, p_34, color=FLOW, lw=2.2, label=r"3$\rightarrow$4 isentropic expansion")
    ax.plot([v1, v1], [p4, p1], color="0.55", lw=2.4, ls="--",
            label=r"4$\rightarrow$1 heat out at const. $v$")
    ax.fill(np.concatenate([[v2], v_34, v_12[::-1]]),
            np.concatenate([[p2], p_34, p_12[::-1]]), color=ALT, alpha=0.10, lw=0)
    for v, p, lab, dx, dy in ((v1, p1, "1", 0.012, 260), (v2, p2, "2", -0.016, 180),
                              (v3, p3, "3", 0.012, 180), (v1, p4, "4", 0.012, -420)):
        ax.plot([v], [p], marker="o", ms=6.5, mfc="white", mec="0.2", mew=1.6,
                ls="none", zorder=5)
        ax.text(v + dx, p + dy, lab, fontsize=11, color="0.2")
    ax.set_xlim(0.0, 0.94)
    ax.set_ylim(0, 6600)
    ax.set_xlabel(r"specific volume $v$ (m$^3$/kg)")
    ax.set_ylabel(r"pressure $p$ (kPa)")
    ax.set_title(r"Air-standard Diesel cycle, $r=18$, $r_c=2$")
    ax.legend(loc="upper right", frameon=False, fontsize=8.5)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_diesel_pv.svg")
    caps["fig1_diesel_pv.svg"] = (
        r"The air-standard Diesel cycle. Only one process differs from Otto: heat "
        r"is added along the flat 2$\rightarrow$3 line at constant pressure, "
        r"modelling fuel injected into already-compressed air and burning as the "
        r"piston withdraws, rather than all at once at top dead centre. Because "
        r"nothing is pre-mixed there is no knock limit, so compression ratios of "
        r"18 or more are ordinary — here the charge reaches "
        + "%.0f" % temp_after_isentropic_compression(T1, r) + r" K on "
        r"compression alone, which is what ignites the fuel. The cutoff ratio "
        r"$r_c=v_3/v_2$ (cutoff_ratio) measures how far into the stroke "
        r"injection continues; $\eta=" + "%.3f" % diesel_efficiency(r, rc) + r"$.")

    # Fig 2 — the penalty.  At equal compression ratio Diesel is always WORSE
    # than Otto, by a factor that grows with cutoff; rc -> 1 recovers Otto
    # exactly.  Diesel wins in practice only because r can be so much larger.
    rr = np.linspace(5.0, 24.0, 300)

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot(rr, [diesel_efficiency(x, 1.0001) for x in rr], color="0.55",
            lw=1.8, ls="-.", label=r"$r_c\rightarrow1$: the Otto limit")
    for rc_v, c, ls in ((1.5, INK, "-"), (2.5, FLOW, "--"), (3.5, ALT, ":")):
        ax.plot(rr, [diesel_efficiency(x, rc_v) for x in rr], color=c, lw=2.1,
                ls=ls, label=r"$r_c=%.1f$" % rc_v)
    ax.axvline(11.0, color="0.75", lw=1.2, ls=":")
    ax.text(10.4, 0.30, "gasoline stops here", rotation=90, fontsize=8.5,
            color="0.45", ha="right")
    ax.set_xlim(5, 24)
    ax.set_ylim(0.3, 0.72)
    ax.set_xlabel(r"compression ratio $r$")
    ax.set_ylabel(r"thermal efficiency $\eta$")
    ax.set_title(r"Diesel pays a cutoff penalty but may compress much further")
    ax.legend(loc="lower right", frameon=False, fontsize=8.5)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_diesel_vs_otto.svg")
    caps["fig2_diesel_vs_otto.svg"] = (
        r"Compared at the SAME compression ratio, the Diesel cycle is always "
        r"less efficient than Otto (diesel_efficiency): the bracketed cutoff "
        r"term is greater than one whenever $r_c>1$, and it grows as injection "
        r"is prolonged. Letting $r_c\to1$ collapses the expression onto the Otto "
        r"curve exactly. The reason diesel engines nevertheless win on fuel "
        r"consumption is the x-axis, not the y-axis — with no premixed charge to "
        r"knock they run at $r\approx18$ where gasoline must stop near 11, and "
        + "%.3f" % diesel_efficiency(18.0, 2.5) + r" at $r=18$ beats "
        + "%.3f" % diesel_efficiency(11.0, 1.0001) + r" at $r=11$.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
