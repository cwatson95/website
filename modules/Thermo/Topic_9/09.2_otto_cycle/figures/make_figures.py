"""Module 9.2 figures — the air-standard Otto cycle drawn on p-v, and the
compression-ratio curve that stops where knock begins.

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
from otto_cycle import (                          # noqa: E402
    K_AIR, otto_efficiency, temp_after_isentropic_compression,
    temp_after_isentropic_expansion, heat_added_cold, net_work_cold,
    mean_effective_pressure,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

R_AIR = 0.287                                      # kJ/kg.K


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the four processes on p-v.  Two isentropes (curved) joined by two
    # constant-volume lines (vertical): heat is added and rejected at fixed
    # volume, which is what "spark ignition" idealizes to.
    r, T1, p1, T3 = 8.0, 300.0, 100.0, 1800.0
    v1 = R_AIR * T1 / p1
    v2 = v1 / r
    T2 = temp_after_isentropic_compression(T1, r)
    T4 = temp_after_isentropic_expansion(T3, r)
    p2 = p1 * r ** K_AIR
    p3 = p2 * T3 / T2
    p4 = p1 * T4 / T1

    v_c = np.linspace(v2, v1, 200)
    p_12 = p1 * (v1 / v_c) ** K_AIR                 # 1->2 compression
    p_34 = p4 * (v1 / v_c) ** K_AIR                 # 3->4 expansion

    fig, ax = plt.subplots(figsize=(6.2, 3.9))
    ax.plot(v_c, p_12, color=INK, lw=2.2, label=r"1$\rightarrow$2 isentropic compression")
    ax.plot(v_c, p_34, color=FLOW, lw=2.2, label=r"3$\rightarrow$4 isentropic expansion")
    ax.plot([v2, v2], [p2, p3], color=ALT, lw=2.4, ls="--",
            label=r"2$\rightarrow$3 heat in at const. $v$")
    ax.plot([v1, v1], [p4, p1], color="0.55", lw=2.4, ls="--",
            label=r"4$\rightarrow$1 heat out at const. $v$")
    ax.fill(np.concatenate([v_c, v_c[::-1]]),
            np.concatenate([p_34, p_12[::-1]]), color=ALT, alpha=0.10, lw=0)
    for v, p, lab, dx, dy in ((v1, p1, "1", 0.03, -260), (v2, p2, "2", -0.035, 90),
                              (v2, p3, "3", -0.035, 120), (v1, p4, "4", 0.03, 120)):
        ax.plot([v], [p], marker="o", ms=6.5, mfc="white", mec="0.2", mew=1.6,
                ls="none", zorder=5)
        ax.text(v + dx, p + dy, lab, fontsize=11, color="0.2")
    ax.set_xlim(0.05, 0.98)
    ax.set_ylim(0, 5400)
    ax.set_xlabel(r"specific volume $v$ (m$^3$/kg)")
    ax.set_ylabel(r"pressure $p$ (kPa)")
    ax.set_title(r"Air-standard Otto cycle, $r=8$")
    ax.legend(loc="upper right", frameon=False, fontsize=8.5)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_otto_pv.svg")
    caps["fig1_otto_pv.svg"] = (
        r"The air-standard Otto cycle at a compression ratio of 8, drawn from the "
        r"module's own state relations (temp_after_isentropic_compression and "
        r"temp_after_isentropic_expansion). Both heat transfers happen on "
        r"VERTICAL lines — combustion is idealized as instantaneous at "
        r"top dead centre, which is what distinguishes Otto from Diesel. The "
        r"enclosed area is the net work, "
        + "%.0f" % net_work_cold(r, T1, T3) + r" kJ/kg here against "
        + "%.0f" % heat_added_cold(T2, T3) + r" kJ/kg of heat in, giving "
        r"$\eta=" + "%.3f" % otto_efficiency(r) + r"$. Spreading that work over "
        r"the displacement gives a mean effective pressure of "
        + "%.0f" % mean_effective_pressure(net_work_cold(r, T1, T3), v1, v2) +
        r" kPa — the constant pressure that would do the same job.")

    # Fig 2 — efficiency depends ONLY on the compression ratio and k, not on how
    # much heat is added.  The curve flattens, and real engines stop where the
    # end-of-compression temperature would pre-ignite the charge.
    rr = np.linspace(2.0, 16.0, 300)

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    for k, lab, c, ls in ((1.4, r"$k=1.4$ (cold air-standard)", INK, "-"),
                          (1.3, r"$k=1.3$ (hot running gas)", FLOW, "--")):
        ax.plot(rr, [otto_efficiency(x, k) for x in rr], color=c, lw=2.2,
                ls=ls, label=lab)
    ax.axvspan(11.0, 16.0, color=ALT, alpha=0.11, lw=0)
    ax.text(13.5, 0.20, "knock-limited\nfor gasoline", fontsize=9, color="0.35",
            ha="center")
    for x in (8.0, 10.0):
        ax.plot([x], [otto_efficiency(x)], marker="o", ms=7, mfc="white",
                mec="0.25", mew=1.7, ls="none")
        ax.annotate(r"$r=%g$: $\eta=%.3f$" % (x, otto_efficiency(x)),
                    xy=(x, otto_efficiency(x)),
                    xytext=(x - 0.4, otto_efficiency(x) - 0.09), fontsize=9,
                    color="0.3", ha="right")
    ax.set_xlim(2, 16)
    ax.set_ylim(0, 0.72)
    ax.set_xlabel(r"compression ratio $r=V_1/V_2$")
    ax.set_ylabel(r"thermal efficiency $\eta=1-r^{1-k}$")
    ax.set_title(r"Otto efficiency is set by the compression ratio alone")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_otto_efficiency.svg")
    caps["fig2_otto_efficiency.svg"] = (
        r"The cold air-standard Otto efficiency $\eta=1-1/r^{k-1}$ "
        r"(otto_efficiency) depends on the compression ratio and the "
        r"specific-heat ratio and on nothing else — not on how much fuel is "
        r"burned. Returns diminish sharply: going from $r=8$ to $r=10$ buys "
        r"about " + "%.1f" % (100 * (otto_efficiency(10.0) - otto_efficiency(8.0))) +
        r" percentage points, and the next two buy less again. Real "
        r"spark-ignition engines stop near $r\approx11$ anyway, because a higher "
        r"ratio leaves the charge hot enough to ignite before the spark — knock. "
        r"The lower curve shows that using a more realistic $k$ for hot "
        r"combustion gas pulls every prediction down, which is why the "
        r"air-standard number always flatters the real engine.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
