"""Module 9.4 figures — the dual cycle, which burns partly at constant volume and
partly at constant pressure, and the family it spans between Otto and Diesel.

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
from dual_cycle import (                          # noqa: E402
    K_AIR, dual_efficiency, pressure_ratio, cutoff_ratio,
    temp_after_isentropic_compression, temp_after_constant_volume_heat,
    temp_after_constant_pressure_heat, temp_after_isentropic_expansion,
    mean_effective_pressure,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

R_AIR = 0.287                                      # kJ/kg.K


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — five states, because combustion is split: a constant-volume jump
    # 2->3 followed by a constant-pressure stretch 3->4.  This is what a real
    # compression-ignition indicator diagram actually looks like.
    r, rp, rc, T1, p1 = 16.0, 1.6, 1.7, 300.0, 100.0
    v1 = R_AIR * T1 / p1
    v2 = v1 / r
    v4 = rc * v2
    T2 = temp_after_isentropic_compression(T1, r)
    T3 = temp_after_constant_volume_heat(T2, rp)
    T4 = temp_after_constant_pressure_heat(T3, rc)
    T5 = temp_after_isentropic_expansion(T4, r, rc)
    p2 = p1 * r ** K_AIR
    p3 = p2 * rp
    p5 = p1 * T5 / T1

    v_12 = np.linspace(v2, v1, 200)
    p_12 = p1 * (v1 / v_12) ** K_AIR
    v_45 = np.linspace(v4, v1, 200)
    p_45 = p3 * (v4 / v_45) ** K_AIR

    fig, ax = plt.subplots(figsize=(6.2, 3.9))
    ax.plot(v_12, p_12, color=INK, lw=2.2, label=r"1$\rightarrow$2 isentropic")
    # both burns share the ALT hue (they are one category, "heat in") and are
    # separated by linestyle -- ALT vs STEEL is the palette's deuteranopia-unsafe
    # pair (OKLab dE 2.6) and must never be the sole distinction between series.
    ax.plot([v2, v2], [p2, p3], color=ALT, lw=2.6,
            label=r"2$\rightarrow$3 const. $v$ burn")
    ax.plot([v2, v4], [p3, p3], color=ALT, lw=2.6, ls=(0, (5, 2)),
            label=r"3$\rightarrow$4 const. $p$ burn")
    ax.plot(v_45, p_45, color=FLOW, lw=2.2, label=r"4$\rightarrow$5 isentropic")
    ax.plot([v1, v1], [p5, p1], color="0.55", lw=2.4, ls="--",
            label=r"5$\rightarrow$1 const. $v$ reject")
    ax.fill(np.concatenate([[v2, v2], v_45, v_12[::-1]]),
            np.concatenate([[p2, p3], p_45, p_12[::-1]]), color=ALT, alpha=0.09,
            lw=0)
    for v, p, lab, dx, dy in ((v1, p1, "1", 0.012, 260), (v2, p2, "2", -0.018, 0),
                              (v2, p3, "3", -0.018, 190), (v4, p3, "4", 0.012, 200),
                              (v1, p5, "5", 0.012, -430)):
        ax.plot([v], [p], marker="o", ms=6.5, mfc="white", mec="0.2", mew=1.6,
                ls="none", zorder=5)
        ax.text(v + dx, p + dy, lab, fontsize=11, color="0.2")
    ax.set_xlim(0.0, 0.94)
    ax.set_ylim(0, 8200)
    ax.set_xlabel(r"specific volume $v$ (m$^3$/kg)")
    ax.set_ylabel(r"pressure $p$ (kPa)")
    ax.set_title(r"Dual cycle: $r=16$, $r_p=1.6$, $r_c=1.7$")
    ax.legend(loc="upper right", frameon=False, fontsize=8.5)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_dual_pv.svg")
    caps["fig1_dual_pv.svg"] = (
        r"The dual (or limited-pressure) cycle splits combustion in two: a "
        r"constant-volume pressure jump 2$\rightarrow$3 set by the pressure "
        r"ratio $r_p$ (pressure_ratio), then a constant-pressure stretch "
        r"3$\rightarrow$4 set by the cutoff ratio $r_c$ (cutoff_ratio). Real "
        r"compression-ignition engines behave this way — some of the injected "
        r"fuel burns almost instantly once it ignites, the rest burns as it "
        r"arrives — so the dual cycle is the better model of the two idealized "
        r"extremes. Here $\eta=" + "%.3f" % dual_efficiency(r, rp, rc) + r"$ and "
        r"the mean effective pressure is "
        + "%.0f" % mean_effective_pressure(
            dual_efficiency(r, rp, rc) * 0.718 * ((T3 - T2) + K_AIR * (T4 - T3)),
            v1, r) + r" kPa.")

    # Fig 2 — the family.  Holding r fixed and sliding the split between the two
    # burns traces a continuum whose endpoints are exactly Otto and Diesel.
    r_fix = 16.0
    rc_grid = np.linspace(1.0, 3.0, 300)

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    for rp_v, c, ls in ((1.0, FLOW, "--"), (1.5, INK, "-"), (2.5, ALT, ":")):
        ax.plot(rc_grid, [dual_efficiency(r_fix, rp_v, x) for x in rc_grid],
                color=c, lw=2.1, ls=ls, label=r"$r_p=%.1f$" % rp_v)
    ax.plot([1.0], [dual_efficiency(r_fix, 1.0, 1.0)], marker="o", ms=8,
            mfc="white", mec="0.2", mew=1.8, ls="none")
    ax.annotate(r"$r_p=r_c=1$: the Otto cycle", xy=(1.0, dual_efficiency(r_fix, 1.0, 1.0)),
                xytext=(1.35, dual_efficiency(r_fix, 1.0, 1.0) + 0.008),
                fontsize=9, color="0.3",
                arrowprops=dict(arrowstyle="->", color="0.5", lw=1.0))
    ax.annotate(r"$r_p=1$: the Diesel cycle", xy=(2.4, dual_efficiency(r_fix, 1.0, 2.4)),
                xytext=(1.9, dual_efficiency(r_fix, 1.0, 2.4) - 0.035),
                fontsize=9, color=FLOW,
                arrowprops=dict(arrowstyle="->", color=FLOW, lw=1.0))
    ax.set_xlim(1.0, 3.0)
    ax.set_xlabel(r"cutoff ratio $r_c$    ($r=16$ throughout)")
    ax.set_ylabel(r"thermal efficiency $\eta$")
    ax.set_title(r"Dual spans the ground between Otto and Diesel")
    ax.legend(loc="lower left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_dual_family.svg")
    caps["fig2_dual_family.svg"] = (
        r"The dual cycle is not a third alternative so much as the family that "
        r"contains the other two. Fixing the compression ratio at 16 and sliding "
        r"the split between the constant-volume and constant-pressure burns, "
        r"dual_efficiency reduces to the Otto value "
        + "%.3f" % dual_efficiency(r_fix, 1.0, 1.0) + r" when $r_p=r_c=1$ and to "
        r"the Diesel value along the $r_p=1$ curve. Every curve falls as $r_c$ "
        r"grows and rises as $r_p$ grows, which is the same statement twice: "
        r"heat added at high pressure and small volume is worth more than heat "
        r"dribbled in while the piston is already retreating.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
