"""Module 8.2 figures — the heat a condenser must reject as a function of the
quality arriving, and the cooling-water flow that has to carry it away.

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
from condenser import (                           # noqa: E402
    heat_transfer_rate, heat_rejected, condenser_heat_per_mass,
    enthalpy_two_phase, quality_from_h,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

# Saturated water at the usual condenser pressure 0.08 bar  [Moran 8e, A-3].
HF, HG = 173.88, 2577.0                            # kJ/kg
CP_WATER = 4.18                                    # kJ/kg.K


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — turbine exhaust at quality x is condensed to saturated liquid.  The
    # heat to reject is linear in x, and it is LARGE: even at x = 0.9 it is most
    # of the heat the boiler put in.
    x = np.linspace(0.0, 1.0, 200)
    h_in = np.array([enthalpy_two_phase(HF, HG, xi) for xi in x])
    q_out = np.array([condenser_heat_per_mass(h, HF) for h in h_in])

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(x, q_out, color=INK, lw=2.4)
    ax.fill_between(x, 0, q_out, color=INK, alpha=0.10, lw=0)
    for xv in (0.88, 1.0):
        q = condenser_heat_per_mass(enthalpy_two_phase(HF, HG, xv), HF)
        ax.plot([xv], [q], marker="o", ms=7.5, mfc="white", mec=FLOW, mew=1.8,
                ls="none")
        ax.annotate(r"$x=%.2f$: %.0f kJ/kg" % (xv, q), xy=(xv, q),
                    xytext=(xv - 0.06, q + 130), fontsize=9, color="0.3",
                    ha="right")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 2750)
    ax.set_xlabel(r"quality of the turbine exhaust $x$")
    ax.set_ylabel(r"heat rejected per kg (kJ/kg)")
    ax.set_title(r"Condensing to saturated liquid at 0.08 bar")
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_condenser_duty.svg")
    caps["fig1_condenser_duty.svg"] = (
        r"A condenser takes the two-phase turbine exhaust and returns saturated "
        r"liquid for the pump. The heat it must reject per kilogram is "
        r"$h_2-h_3$ (condenser_heat_per_mass), linear in the incoming quality "
        r"through the lever rule (enthalpy_two_phase). The magnitude is the "
        r"striking part: at the typical exhaust quality $x=0.88$ it is "
        + "%.0f" % condenser_heat_per_mass(enthalpy_two_phase(HF, HG, 0.88), HF) +
        r" kJ/kg — comparable to everything the boiler added — because almost "
        r"all of it is latent heat that never became work. quality_from_h "
        r"recovers $x$ from a measured enthalpy.")

    # Fig 2 — that heat has to go somewhere.  Sizing the cooling-water circuit:
    # for a 300 MW rejection duty, the flow needed falls hyperbolically with the
    # temperature rise you are willing to allow the river.
    Qdot = 300e3                                    # kW rejected
    dT = np.linspace(4.0, 20.0, 300)
    mdot_w = Qdot / (CP_WATER * dT)

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(dT, mdot_w / 1000.0, color=INK, lw=2.4,
            label=r"$\dot{m}_w=\dot{Q}/(c_p\,\Delta T)$")
    for d in (8.0, 15.0):
        ax.plot([d], [Qdot / (CP_WATER * d) / 1000.0], marker="o", ms=7.5,
                mfc="white", mec=FLOW, mew=1.8, ls="none")
        ax.annotate(r"$\Delta T=%.0f$ K: %.1f t/s" % (d, Qdot / (CP_WATER * d) / 1000.0),
                    xy=(d, Qdot / (CP_WATER * d) / 1000.0),
                    xytext=(d + 1.0, Qdot / (CP_WATER * d) / 1000.0 + 1.2),
                    fontsize=9, color="0.3")
    ax.set_xlim(4, 20)
    ax.set_xlabel(r"cooling-water temperature rise $\Delta T$ (K)")
    ax.set_ylabel(r"cooling water required (tonne/s)")
    ax.set_title(r"Carrying away 300 MW of rejected heat")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_cooling_water.svg")
    caps["fig2_cooling_water.svg"] = (
        r"The consequence of that duty. Rejecting 300 MW into cooling water "
        r"(heat_transfer_rate / heat_rejected supply the signed and unsigned "
        r"forms) needs a flow of $\dot Q/(c_p\Delta T)$, so the permitted "
        r"temperature rise sets the size of the circuit: "
        + "%.1f" % (Qdot / (CP_WATER * 8.0) / 1000.0) + r" tonnes per second for "
        r"an 8 K rise, falling to "
        + "%.1f" % (Qdot / (CP_WATER * 15.0) / 1000.0) + r" t/s if 15 K is "
        r"allowed. Thermal-discharge limits on rivers therefore translate "
        r"directly into pump and intake sizing, and are a large part of why "
        r"power stations are built beside big water.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
