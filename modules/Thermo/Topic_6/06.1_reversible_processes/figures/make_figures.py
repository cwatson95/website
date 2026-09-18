"""Module 6.1 figures — the internally reversible process as an area on T-s, and
the vertical line an adiabatic reversible process draws there.

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
from reversible import (                          # noqa: E402
    entropy_change_int_rev, heat_int_rev_isothermal, heat_int_rev_area,
    sigma_internally_reversible, is_isentropic, carnot_eff_ts,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — three internally reversible paths between the same entropies.  Q is
    # the area under each; the isothermal one is a rectangle (closed form), the
    # others are evaluated by the same quadrature heat_int_rev_area.
    s1, s2 = 1.2, 3.0
    T_iso = 500.0
    s = np.linspace(s1, s2, 200)
    T_ramp = 350.0 + (650.0 - 350.0) * (s - s1) / (s2 - s1)
    T_curve = 350.0 + 300.0 * ((s - s1) / (s2 - s1)) ** 2

    Q_iso = heat_int_rev_isothermal(T_iso, s2, s1)
    Q_ramp = heat_int_rev_area(list(T_ramp), list(s))
    Q_curve = heat_int_rev_area(list(T_curve), list(s))

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot([s1, s2], [T_iso, T_iso], color=INK, lw=2.3,
            label=r"isothermal:  $q=T\Delta s=%.0f$ kJ/kg" % Q_iso)
    ax.fill_between([s1, s2], 0, T_iso, color=INK, alpha=0.10, lw=0)
    ax.plot(s, T_ramp, color=FLOW, lw=2.2, ls="--",
            label=r"linear ramp:  $q=%.0f$ kJ/kg" % Q_ramp)
    ax.plot(s, T_curve, color=ALT, lw=2.2, ls=":",
            label=r"curved path:  $q=%.0f$ kJ/kg" % Q_curve)
    ax.set_xlim(s1, s2)
    ax.set_ylim(0, 750)
    ax.set_xlabel(r"specific entropy $s$ (kJ/kg$\cdot$K)")
    ax.set_ylabel(r"temperature $T$ (K)")
    ax.set_title(r"Internally reversible: $q=\int T\,ds$ is the area")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_heat_as_area.svg")
    caps["fig1_heat_as_area.svg"] = (
        r"For an internally reversible process — and only then — the heat "
        r"transfer is the area under the path on a $T$-$s$ diagram. Three "
        r"different paths carrying the same entropy change from 1.2 to "
        r"3.0 kJ/kg$\cdot$K enclose different areas and so transfer different "
        r"heat: " + "%.0f" % Q_iso + r", " + "%.0f" % Q_ramp + r" and "
        + "%.0f" % Q_curve + r" kJ/kg (heat_int_rev_isothermal for the "
        r"rectangle, heat_int_rev_area for the sampled paths). "
        r"entropy_change_int_rev runs the same relation backwards, giving "
        r"$\Delta s=q/T$ for the isothermal case. The entropy PRODUCED along any "
        r"of them is zero (sigma_internally_reversible) — that is what makes "
        r"them reversible.")

    # Fig 2 — adiabatic AND internally reversible = isentropic, a vertical line.
    # Two Carnot cycles sharing a cold reservoir show how the enclosed area, and
    # hence the efficiency, grows with the top temperature.
    T_C = 300.0
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    for T_H, c, alpha in ((600.0, ALT, 0.18), (900.0, INK, 0.12)):
        ax.plot([s1, s2, s2, s1, s1], [T_H, T_H, T_C, T_C, T_H], color=c,
                lw=2.2,
                label=r"$T_H=%d$ K:  $\eta=%.3f$" % (T_H, carnot_eff_ts(T_H, T_C)))
        ax.fill_between([s1, s2], T_C, T_H, color=c, alpha=alpha, lw=0)
    ax.annotate("isentropic legs\n(adiabatic + reversible)", xy=(s2, 700),
                xytext=(2.35, 380), fontsize=9, color="0.35", ha="center",
                arrowprops=dict(arrowstyle="->", color="0.5", lw=1.0))
    ax.set_xlim(0.9, 3.3)
    ax.set_ylim(200, 1000)
    ax.set_xlabel(r"specific entropy $s$ (kJ/kg$\cdot$K)")
    ax.set_ylabel(r"temperature $T$ (K)")
    ax.set_title(r"An isentropic process is a vertical line on $T$-$s$")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_isentropic_and_carnot.svg")
    caps["fig2_isentropic_and_carnot.svg"] = (
        r"A process that is adiabatic AND internally reversible has no entropy "
        r"transfer and no entropy production, so its entropy cannot change: "
        r"is_isentropic returns True and the path is a vertical line. Building a "
        r"cycle from two such legs and two isotherms gives the Carnot rectangle, "
        r"and raising the top temperature from 600 K to 900 K over the same cold "
        r"reservoir enlarges the enclosed area — the net work — while the heat "
        r"rejected below $T_C$ is unchanged. Reading the efficiency straight off "
        r"the areas (carnot_eff_ts) gives "
        + "%.3f" % carnot_eff_ts(600.0, T_C) + r" and "
        + "%.3f" % carnot_eff_ts(900.0, T_C) + r".")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
