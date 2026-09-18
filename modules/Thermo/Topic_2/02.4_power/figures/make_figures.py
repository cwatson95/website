"""Module 2.4 figures — power as the slope of the energy transfer, on a shaft and
in a resistor, and the energy that accumulates behind a given power level.

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
from power import (                               # noqa: E402
    shaft_power, rpm_to_rad_s, energy_from_power, power_from_work,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — shaft power rises linearly with rotational speed at fixed torque,
    # so a given power can be bought either with torque or with rpm.  This is the
    # whole argument for gearboxes.
    rpm = np.linspace(0.0, 6000.0, 300)
    omega = np.array([rpm_to_rad_s(r) for r in rpm])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for tau, c, ls in ((10.0, INK, "-"), (20.0, FLOW, "--"), (40.0, ALT, ":")):
        P = np.array([shaft_power(tau, w) for w in omega]) / 1000.0    # kW
        ax.plot(rpm, P, color=c, lw=2.1, ls=ls,
                label=r"$\tau=%d$ N$\cdot$m" % tau)
    ax.set_xlim(0, 6000)
    ax.set_xlabel(r"rotational speed (rev/min)")
    ax.set_ylabel(r"shaft power $\dot{W}=\tau\omega$ (kW)")
    ax.set_title(r"Shaft power: torque times angular speed")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_shaft_power_vs_rpm.svg")
    caps["fig1_shaft_power_vs_rpm.svg"] = (
        r"Shaft power $\dot W=\tau\omega$ (shaft_power, with rpm_to_rad_s "
        r"converting rev/min to rad/s) is linear in speed at fixed torque. The "
        r"same "
        + "%.1f" % (shaft_power(40.0, rpm_to_rad_s(3000.0)) / 1000.0) +
        r" kW can be delivered as 40 N$\cdot$m at 3000 rpm or as 20 N$\cdot$m at "
        r"6000 rpm — the trade a gearbox exists to make. Power is a RATE, not an "
        r"amount: it says nothing about how much energy has moved until it is "
        r"multiplied by a duration.")

    # Fig 2 — that multiplication.  Energy grows linearly with time at constant
    # power; the three slopes are three power levels.  A marker shows the
    # round-trip power_from_work(energy_from_power(P, t), t) == P.
    t = np.linspace(0.0, 120.0, 300)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for P, c, ls in ((500.0, INK, "-"), (1500.0, FLOW, "--"), (3000.0, ALT, ":")):
        E = np.array([energy_from_power(P, ti) for ti in t]) / 1000.0   # kJ
        ax.plot(t, E, color=c, lw=2.1, ls=ls, label=r"$\dot{W}=%.1f$ kW" % (P / 1000.0))
    P_back = power_from_work(energy_from_power(1500.0, 60.0), 60.0)
    ax.plot([60.0], [energy_from_power(1500.0, 60.0) / 1000.0], ls="none",
            marker="o", ms=8, mfc="white", mec="0.25", mew=1.8,
            label=r"round trip: %.0f W recovered" % P_back)
    ax.set_xlim(0, 120)
    ax.set_xlabel(r"time (s)")
    ax.set_ylabel(r"energy transferred (kJ)")
    ax.set_title(r"Energy is the area under the power curve")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_energy_from_power.svg")
    caps["fig2_energy_from_power.svg"] = (
        r"Holding power constant, the energy transferred is $\dot W\Delta t$ "
        r"(energy_from_power) — a straight line whose slope IS the power. Two "
        r"minutes at 3 kW moves 360 kJ, the same energy a 500 W trickle would "
        r"take twelve minutes to deliver. The marked point closes the loop: "
        r"feeding that energy back through power_from_work recovers the original "
        r"1500 W, which is the arithmetic identity the two helpers are meant to "
        r"satisfy.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
