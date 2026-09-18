"""Module 8.3 figures — the flow-rate ratio two streams must hold to trade a given
amount of heat, and the energy balance closing across the whole exchanger.

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
from heat_exchanger import (                      # noqa: E402
    energy_balance_residual, mass_flow_ratio_cold_to_hot, mass_flow_other,
    heat_duty, sensible_enthalpy_change, enthalpy_two_phase,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

CP_WATER, CP_AIR = 4.18, 1.005                     # kJ/kg.K


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — hot water giving up a fixed amount of heat to a cold stream.  The
    # flow ratio needed is inversely proportional to the temperature rise the
    # cold side is allowed: ask for a small rise and you need a torrent.
    dh_hot = sensible_enthalpy_change(CP_WATER, 90.0, 50.0)     # negative
    dT_cold = np.linspace(3.0, 45.0, 300)

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    for cp, lab, c, ls in ((CP_WATER, r"cold stream is water", INK, "-"),
                           (CP_AIR, r"cold stream is air", FLOW, "--")):
        ratio = np.array([mass_flow_ratio_cold_to_hot(
            CP_WATER * 90.0, CP_WATER * 50.0, cp * 15.0, cp * (15.0 + d))
            for d in dT_cold])
        ax.plot(dT_cold, ratio, color=c, lw=2.1, ls=ls, label=lab)
    ax.set_yscale("log")
    ax.set_xlim(3, 45)
    ax.set_xlabel(r"temperature rise allowed on the cold side (K)")
    ax.set_ylabel(r"$\dot{m}_{cold}/\dot{m}_{hot}$ (log scale)")
    ax.set_title(r"Hot water cooled 90 $\rightarrow$ 50 $^\circ$C")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6, which="both")
    _save(fig, "fig1_flow_ratio.svg")
    caps["fig1_flow_ratio.svg"] = (
        r"An adiabatic two-stream exchanger must satisfy "
        r"$\dot m_c/\dot m_h=(h_{h,in}-h_{h,out})/(h_{c,out}-h_{c,in})$ "
        r"(mass_flow_ratio_cold_to_hot). Cooling water from 90 to 50 $^\circ$C, "
        r"the ratio falls hyperbolically with the rise permitted on the cold "
        r"side — matching that 40 K drop with only a 5 K rise takes "
        + "%.1f" % mass_flow_ratio_cold_to_hot(CP_WATER * 90, CP_WATER * 50,
                                               CP_WATER * 15, CP_WATER * 20) +
        r" times the cold flow. Swapping water for air lifts every point by "
        r"roughly the specific-heat ratio $c_{p,w}/c_{p,a}\approx"
        + "%.1f" % (CP_WATER / CP_AIR) + r"$, which is why air-cooled exchangers "
        r"are so much bulkier. mass_flow_other solves the same relation for "
        r"whichever flow rate is unknown.")

    # Fig 2 — the balance itself.  Pick the cold flow from the ratio above and
    # the whole-exchanger residual must vanish; sweeping a deliberately WRONG
    # flow shows how the residual reports the error.
    mdot_h = 2.0
    h_hi, h_ho = CP_WATER * 90.0, CP_WATER * 50.0
    h_ci, h_co = CP_WATER * 15.0, CP_WATER * 35.0
    mdot_c_correct = mdot_h * mass_flow_ratio_cold_to_hot(h_hi, h_ho, h_ci, h_co)
    mdot_c = np.linspace(0.5 * mdot_c_correct, 1.5 * mdot_c_correct, 300)
    resid = np.array([energy_balance_residual(mdot_h, h_hi, h_ho, m, h_ci, h_co)
                      for m in mdot_c])

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(mdot_c, resid, color=INK, lw=2.4,
            label=r"$\dot{Q}$ imbalance across the exchanger")
    ax.axhline(0.0, color="0.6", lw=1.1, ls="-.")
    ax.plot([mdot_c_correct], [0.0], marker="o", ms=9, mfc="white", mec=FLOW,
            mew=1.9, ls="none",
            label=r"balance closes at $\dot{m}_c=%.2f$ kg/s" % mdot_c_correct)
    ax.set_xlim(mdot_c[0], mdot_c[-1])
    ax.set_xlabel(r"cold-stream mass flow $\dot{m}_{cold}$ (kg/s)   ($\dot{m}_{hot}=2$ kg/s)")
    ax.set_ylabel(r"energy balance residual (kW)")
    ax.set_title(r"Only one flow rate closes the books")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_balance_closure.svg")
    caps["fig2_balance_closure.svg"] = (
        r"The whole-exchanger energy balance used as a check rather than a "
        r"formula. With the hot stream fixed at 2 kg/s giving up "
        + "%.0f" % abs(heat_duty(mdot_h, h_hi, h_ho)) + r" kW, "
        r"energy_balance_residual is swept over candidate cold-side flows: it "
        r"crosses zero at exactly one value, "
        + "%.2f" % mdot_c_correct + r" kg/s, and its sign says which way a wrong "
        r"guess is out. This is the routine to reach for when a problem is "
        r"over-specified — six measured states with a residual that ought to "
        r"vanish is a far better test of the data than recomputing one unknown "
        r"from the other five. enthalpy_two_phase supplies the endpoint "
        r"enthalpies when a stream is condensing or evaporating rather than "
        r"changing temperature.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
