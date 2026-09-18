"""Module 9.5 figures — the Brayton cycle on T-s, and the pressure ratio that
maximises net work rather than efficiency.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
"""
import json
import math
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
from brayton_cycle import (                       # noqa: E402
    K_AIR, brayton_efficiency, pressure_ratio_max_work,
    temp_after_isentropic_compression, temp_after_isentropic_expansion,
    back_work_ratio, regenerator_exit_enthalpy, heat_added_regenerative,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

CP = 1.005                                         # kJ/kg.K


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — Brayton on T-s.  Heat is exchanged along constant-PRESSURE lines
    # (exponential curves here, since s = cp ln T along one), joined by two
    # vertical isentropes.  Both curves have the same shape, just shifted.
    T1, T3, rp = 300.0, 1400.0, 10.0
    T2 = temp_after_isentropic_compression(T1, rp)
    T4 = temp_after_isentropic_expansion(T3, rp)

    s1 = 0.0
    s_23 = lambda T: s1 + CP * math.log(T / T2)     # along the high pressure
    s_41 = lambda T: s1 + CP * math.log(T / T1)     # along the low pressure
    T_hi = np.linspace(T2, T3, 200)
    T_lo = np.linspace(T1, T4, 200)

    fig, ax = plt.subplots(figsize=(6.2, 3.9))
    ax.plot([s1, s1], [T1, T2], color=INK, lw=2.3,
            label=r"1$\rightarrow$2 compressor (isentropic)")
    ax.plot([s_23(t) for t in T_hi], T_hi, color=ALT, lw=2.4,
            label=r"2$\rightarrow$3 combustor (const. $p$)")
    ax.plot([s_23(T3), s_41(T4)], [T3, T4], color=FLOW, lw=2.3,
            label=r"3$\rightarrow$4 turbine (isentropic)")
    ax.plot([s_41(t) for t in T_lo], T_lo, color="0.55", lw=2.2, ls="--",
            label=r"4$\rightarrow$1 exhaust (const. $p$)")
    ax.fill(np.concatenate([[s1], [s_23(t) for t in T_hi], [s_41(t) for t in T_lo[::-1]]]),
            np.concatenate([[T1], T_hi, T_lo[::-1]]), color=ALT, alpha=0.09, lw=0)
    for s, T, lab, dx, dy in ((s1, T1, "1", -0.07, -60), (s1, T2, "2", -0.07, 40),
                              (s_23(T3), T3, "3", 0.03, 45),
                              (s_41(T4), T4, "4", 0.03, 40)):
        ax.plot([s], [T], marker="o", ms=6.5, mfc="white", mec="0.2", mew=1.6,
                ls="none", zorder=5)
        ax.text(s + dx, T + dy, lab, fontsize=11, color="0.2")
    ax.annotate(r"exhaust still at %.0f K:" "\n" r"the regenerator's opportunity" % T4,
                xy=(s_41(T4) * 0.75, T4), xytext=(0.55, 830), fontsize=9,
                color="0.35",
                arrowprops=dict(arrowstyle="->", color="0.5", lw=1.0))
    ax.set_xlim(-0.15, 1.65)
    ax.set_ylim(150, 1550)
    ax.set_xlabel(r"specific entropy $s-s_1$ (kJ/kg$\cdot$K)")
    ax.set_ylabel(r"temperature $T$ (K)")
    ax.set_title(r"Air-standard Brayton cycle, $r_p=10$")
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_brayton_ts.svg")
    caps["fig1_brayton_ts.svg"] = (
        r"The gas-turbine cycle on $T$-$s$: two vertical isentropes for the "
        r"compressor and turbine, joined by two constant-pressure curves for "
        r"combustion and exhaust. With $r_p=10$ from 300 K, air leaves the "
        r"compressor at " + "%.0f" % T2 + r" K and the turbine exhaust is still "
        r"at " + "%.0f" % T4 + r" K — HOTTER than the compressor discharge, "
        r"which is the entire premise of regeneration: that exhaust can preheat "
        r"the combustor feed for free (regenerator_exit_enthalpy, "
        r"heat_added_regenerative). The back work ratio here is "
        + "%.2f" % back_work_ratio(CP * T1, CP * T2, CP * T3, CP * T4) + r", so "
        r"nearly half the turbine's output is consumed driving its own "
        r"compressor — far worse than a steam plant's 1%, and why gas turbines "
        r"are so sensitive to component efficiency.")

    # Fig 2 — efficiency and net work answer different questions, so they get
    # separate panels.  Efficiency climbs forever with rp; net work per kg peaks
    # and then falls, because the compressor eventually eats the gains.
    rp_grid = np.linspace(2.0, 40.0, 400)
    eta = np.array([brayton_efficiency(x) for x in rp_grid])
    w_net = np.array([CP * ((T3 - temp_after_isentropic_expansion(T3, x))
                            - (temp_after_isentropic_compression(T1, x) - T1))
                      for x in rp_grid])
    rp_opt = pressure_ratio_max_work(T1, T3)

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(6.4, 3.4))
    axL.plot(rp_grid, eta, color=INK, lw=2.3)
    axL.axvline(rp_opt, color=FLOW, lw=1.4, ls="--")
    axL.set_xlabel(r"pressure ratio $r_p$")
    axL.set_ylabel(r"thermal efficiency $\eta$")
    axL.set_title(r"$\eta$ rises without limit", fontsize=10.5)
    axL.grid(alpha=0.25, lw=0.6)

    axR.plot(rp_grid, w_net, color=ALT, lw=2.3)
    axR.axvline(rp_opt, color=FLOW, lw=1.4, ls="--")
    axR.plot([rp_opt], [CP * ((T3 - temp_after_isentropic_expansion(T3, rp_opt))
                              - (temp_after_isentropic_compression(T1, rp_opt) - T1))],
             marker="o", ms=8, mfc="white", mec=FLOW, mew=1.8, ls="none")
    axR.annotate(r"$r_p=%.1f$" % rp_opt, xy=(rp_opt, w_net.max()),
                 xytext=(rp_opt + 6, w_net.max() * 0.93), fontsize=9.5,
                 color=FLOW)
    axR.set_xlabel(r"pressure ratio $r_p$")
    axR.set_ylabel(r"net work $w_{net}$ (kJ/kg)")
    axR.set_title(r"$w_{net}$ has a maximum", fontsize=10.5)
    axR.grid(alpha=0.25, lw=0.6)
    fig.tight_layout()
    _save(fig, "fig2_brayton_optimum.svg")
    caps["fig2_brayton_optimum.svg"] = (
        r"Two different design questions, deliberately on separate axes. "
        r"Efficiency $\eta=1-r_p^{(1-k)/k}$ (brayton_efficiency) increases "
        r"monotonically with pressure ratio, so on that criterion alone one "
        r"would compress forever. But the net work per kilogram of air peaks and "
        r"then declines, because past a point the compressor absorbs more than "
        r"the extra expansion returns. For $T_1=300$ K and $T_3=1400$ K the "
        r"maximum sits at $r_p=" + "%.1f" % rp_opt + r"$ "
        r"(pressure_ratio_max_work, the $\sqrt{T_3/T_1}$ result). A machine "
        r"built for peak specific work is therefore SMALLER for a given output; "
        r"one built for peak efficiency burns less fuel. Real engines are placed "
        r"between the two.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
