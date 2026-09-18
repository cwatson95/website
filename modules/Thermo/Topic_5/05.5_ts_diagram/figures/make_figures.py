"""Module 5.5 figures — the T-S plane, where the area under a reversible path is
the heat and the Carnot cycle becomes a rectangle.

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
from ts_diagram import (                          # noqa: E402
    heat_TdS, heat_isothermal, heat_linear_TS, carnot_net_work,
    carnot_efficiency,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the Carnot cycle is a RECTANGLE here: two isotherms (horizontal)
    # and two isentropes (vertical).  Heat in is the area under the top edge,
    # heat out the area under the bottom edge, and the enclosed box is the work.
    T_H, T_C = 800.0, 320.0
    S1, S2 = 1.0, 3.0
    dS = S2 - S1
    Q_in = heat_isothermal(T_H, S1, S2)
    Q_out = heat_isothermal(T_C, S2, S1)
    W = carnot_net_work(T_H, T_C, dS)
    eta = carnot_efficiency(T_H, T_C)

    fig, ax = plt.subplots(figsize=(6.2, 3.9))
    ax.fill_between([S1, S2], T_C, T_H, color=ALT, alpha=0.20, lw=0)
    ax.fill_between([S1, S2], 0, T_C, color=FLOW, alpha=0.14, lw=0)
    ax.plot([S1, S2], [T_H, T_H], color=INK, lw=2.6)
    ax.plot([S1, S2], [T_C, T_C], color=FLOW, lw=2.6)
    ax.plot([S2, S2], [T_C, T_H], color="0.55", lw=2.0)
    ax.plot([S1, S1], [T_C, T_H], color="0.55", lw=2.0)
    ax.annotate("", xy=(2.3, T_H), xytext=(1.7, T_H),
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))
    ax.annotate("", xy=(1.7, T_C), xytext=(2.3, T_C),
                arrowprops=dict(arrowstyle="->", color=FLOW, lw=1.6))
    ax.text(2.0, 0.5 * (T_H + T_C), r"$W_{net}=(T_H-T_C)\,\Delta S$" "\n"
                                    r"$=%.0f$ kJ" % W,
            ha="center", fontsize=10.5, color="0.2")
    ax.text(2.0, T_C / 2, r"$Q_{out}=T_C\,\Delta S=%.0f$ kJ" % abs(Q_out),
            ha="center", fontsize=9.5, color="0.3")
    ax.text(S1 - 0.02, T_H + 48, r"$Q_{in}=T_H\Delta S=%.0f$ kJ" % Q_in,
            fontsize=9.5, color=INK)
    ax.text(S1 - 0.055, 0.5 * (T_H + T_C), "isentropic", rotation=90,
            fontsize=8.5, color="0.45", va="center")
    ax.set_xlim(0.6, 3.4)
    ax.set_ylim(0, 950)
    ax.set_xlabel(r"entropy $S$ (kJ/K)")
    ax.set_ylabel(r"temperature $T$ (K)")
    ax.set_title(r"The Carnot cycle is a rectangle on $T$-$S$   ($\eta=%.3f$)" % eta)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_ts_carnot_rectangle.svg")
    caps["fig1_ts_carnot_rectangle.svg"] = (
        r"On a temperature-entropy diagram an internally reversible heat "
        r"transfer is an AREA, $Q=\int T\,dS$, and the Carnot cycle becomes a "
        r"plain rectangle: two isotherms top and bottom, two isentropes (vertical "
        r"lines, $dS=0$) at the sides. Heat in is the strip under the top edge, "
        + "%.0f" % Q_in + r" kJ (heat_isothermal); heat rejected is the strip "
        r"under the bottom edge, " + "%.0f" % abs(Q_out) + r" kJ; and the "
        r"enclosed box is the net work, " + "%.0f" % W + r" kJ "
        r"(carnot_net_work). The efficiency "
        r"$\eta=W/Q_{in}=1-T_C/T_H=" + "%.3f" % eta + r"$ is then just the ratio "
        r"of two areas that share the same base $\Delta S$ — which is why it "
        r"depends on temperatures alone.")

    # Fig 2 — a general reversible path where T varies with S.  The trapezoid
    # quadrature heat_TdS integrates the sampled path; for a straight ramp it
    # must agree with the closed form heat_linear_TS.
    S = np.linspace(1.0, 3.0, 60)
    T_lin = 320.0 + (800.0 - 320.0) * (S - S[0]) / (S[-1] - S[0])
    Q_num = heat_TdS(list(T_lin), list(S))
    Q_exact = heat_linear_TS(T_lin[0], T_lin[-1], S[0], S[-1])
    T_curve = 320.0 + 480.0 * ((S - S[0]) / (S[-1] - S[0])) ** 2
    Q_curve = heat_TdS(list(T_curve), list(S))

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(S, T_lin, color=INK, lw=2.3,
            label=r"linear ramp:  $Q=%.0f$ kJ" % Q_num)
    ax.fill_between(S, 0, T_lin, color=INK, alpha=0.12, lw=0)
    ax.plot(S, T_curve, color=FLOW, lw=2.3, ls="--",
            label=r"a curved path:  $Q=%.0f$ kJ" % Q_curve)
    ax.set_xlim(1.0, 3.0)
    ax.set_ylim(0, 900)
    ax.set_xlabel(r"entropy $S$ (kJ/K)")
    ax.set_ylabel(r"temperature $T$ (K)")
    ax.set_title(r"Heat is the area under the path:  $Q=\int T\,dS$")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_heat_as_area.svg")
    caps["fig2_heat_as_area.svg"] = (
        r"For any internally reversible process the heat transferred is the area "
        r"under the path on $T$-$S$. Sampling a straight ramp from 320 K to "
        r"800 K and integrating with the module's trapezoid rule heat_TdS gives "
        + "%.1f" % Q_num + r" kJ, matching the closed form heat_linear_TS "
        r"($\tfrac12(T_1+T_2)\Delta S$) to "
        + "%.2g" % abs(Q_num - Q_exact) + r" kJ. A path reaching the same end "
        r"states through lower temperatures encloses less area and so transfers "
        r"less heat — " + "%.0f" % Q_curve + r" kJ here. This is the entropy "
        r"counterpart of the $p$-$V$ work diagram in module 5.4, and the two "
        r"together are how every cycle in Topic 9 is read.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
