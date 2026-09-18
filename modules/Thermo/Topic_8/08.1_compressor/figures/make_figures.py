"""Module 8.1 figures — the power a compressor actually draws as its isentropic
efficiency falls, and the hotter exit state that inefficiency leaves behind.

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
from compressor import (                          # noqa: E402
    mass_flow_rate_ideal_gas, power_input, actual_compressor_work,
    isentropic_compressor_work, isentropic_efficiency,
    exit_enthalpy_from_efficiency,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

CP_AIR = 1.005                                     # kJ/kg.K
R_AIR = 287.0                                      # J/kg.K


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — air compressed 1 -> 8 bar.  The isentropic work is fixed by the
    # end pressures; the power actually drawn is that divided by eta_c, so it
    # blows up hyperbolically as the machine degrades.
    T1, pr, k = 293.0, 8.0, 1.4
    T2s = T1 * pr ** ((k - 1) / k)
    h1, h2s = CP_AIR * T1, CP_AIR * T2s
    ws = isentropic_compressor_work(h1, h2s)
    eta = np.linspace(0.55, 1.0, 300)

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    for mdot, c, ls in ((0.5, INK, "-"), (1.5, FLOW, "--"), (3.0, ALT, ":")):
        P = np.array([power_input(mdot, h1, exit_enthalpy_from_efficiency(h1, h2s, e))
                      for e in eta])
        ax.plot(eta, P, color=c, lw=2.1, ls=ls, label=r"$\dot{m}=%g$ kg/s" % mdot)
    ax.set_xlim(0.55, 1.0)
    ax.set_xlabel(r"isentropic efficiency $\eta_c$")
    ax.set_ylabel(r"shaft power required (kW)")
    ax.set_title(r"Air 1$\rightarrow$8 bar: the power an inefficiency costs")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_power_vs_efficiency.svg")
    caps["fig1_power_vs_efficiency.svg"] = (
        r"Compressing air from 1 to 8 bar starting at 20 $^\circ$C. The "
        r"isentropic work is set entirely by the end states — "
        + "%.0f" % ws + r" kJ/kg (isentropic_compressor_work) — but the shaft "
        r"must supply that DIVIDED by the isentropic efficiency "
        r"(exit_enthalpy_from_efficiency then power_input), so the curves rise "
        r"hyperbolically as the machine degrades. At 1.5 kg/s a drop from "
        r"$\eta_c=0.9$ to $0.65$ adds about "
        + "%.0f" % (power_input(1.5, h1, exit_enthalpy_from_efficiency(h1, h2s, 0.65))
                    - power_input(1.5, h1, exit_enthalpy_from_efficiency(h1, h2s, 0.9)))
        + r" kW to the bill for the identical duty. mass_flow_rate_ideal_gas "
        r"converts a duct size and velocity into the $\dot m$ these lines are "
        r"indexed by.")

    # Fig 2 — where the wasted work goes: into the gas.  A less efficient
    # compressor delivers the same pressure but a hotter stream, which the next
    # component then has to live with.
    T2 = np.array([exit_enthalpy_from_efficiency(h1, h2s, e) / CP_AIR for e in eta])

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(eta, T2 - 273.15, color=INK, lw=2.4, label=r"actual exit $T_2$")
    ax.axhline(T2s - 273.15, color=FLOW, lw=1.6, ls="--",
               label=r"isentropic exit $T_{2s}=%.0f\,^\circ$C" % (T2s - 273.15))
    ax.fill_between(eta, T2s - 273.15, T2 - 273.15, color=ALT, alpha=0.13, lw=0)
    ax.set_xlim(0.55, 1.0)
    ax.set_xlabel(r"isentropic efficiency $\eta_c$")
    ax.set_ylabel(r"compressor exit temperature ($^\circ$C)")
    ax.set_title(r"The work you waste ends up in the gas")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_exit_temperature.svg")
    caps["fig2_exit_temperature.svg"] = (
        r"An adiabatic compressor has nowhere to put its losses except into the "
        r"stream it is compressing. The exit enthalpy is "
        r"$h_2=h_1+(h_{2s}-h_1)/\eta_c$ (exit_enthalpy_from_efficiency), so the "
        r"same 8 bar is reached at "
        + "%.0f" % (T2s - 273.15) + r" $^\circ$C isentropically but at "
        + "%.0f" % (exit_enthalpy_from_efficiency(h1, h2s, 0.65) / CP_AIR - 273.15) +
        r" $^\circ$C at $\eta_c=0.65$. The shaded gap is real, measurable "
        r"superheat: it raises the duty on any intercooler downstream and, in a "
        r"gas-turbine cycle, is why the compressor's irreversibility eats "
        r"directly into the net work. actual_compressor_work and "
        r"isentropic_efficiency close the loop between the two states.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
