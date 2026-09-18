"""Module 6.4 figures — steady-state turbine power straight from the enthalpy drop,
and the velocity at which the kinetic term stops being negligible.

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
from steady_state import (                        # noqa: E402
    steady_mass_residual, is_steady, delta_ke, heat_rate_steady,
    power_rate_steady, turbine_power_adiabatic,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    # steady state means BOTH balances close
    assert is_steady(steady_mass_residual([4.0, 1.0], [5.0]), 0.0)

    # Fig 1 — at steady state an adiabatic turbine's power is just mdot times the
    # enthalpy drop: a fan of straight lines, one per mass flow rate.
    dh = np.linspace(0.0, 900.0, 300)
    h1 = 3230.0

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    for mdot, c, ls in ((2.0, INK, "-"), (5.0, FLOW, "--"), (12.0, ALT, ":")):
        W = np.array([turbine_power_adiabatic(mdot, h1, h1 - d) for d in dh]) / 1000.0
        ax.plot(dh, W, color=c, lw=2.1, ls=ls,
                label=r"$\dot{m}=%g$ kg/s" % mdot)
    ax.set_xlim(0, 900)
    ax.set_xlabel(r"enthalpy drop $h_1-h_2$ (kJ/kg)")
    ax.set_ylabel(r"turbine power $\dot{W}_{cv}$ (MW)")
    ax.set_title(r"Steady adiabatic turbine: $\dot{W}=\dot{m}(h_1-h_2)$")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_turbine_power.svg")
    caps["fig1_turbine_power.svg"] = (
        r"Steady state is the assumption that makes control-volume problems "
        r"tractable: nothing accumulates, so $dm_{cv}/dt$ and $dE_{cv}/dt$ both "
        r"vanish (steady_mass_residual, is_steady) and the energy rate balance "
        r"collapses to $\dot W=\dot m(h_1-h_2)$ for an adiabatic turbine with "
        r"negligible KE and PE (turbine_power_adiabatic). The result is linear in "
        r"both factors — 12 kg/s through an 800 kJ/kg drop is "
        + "%.1f" % (turbine_power_adiabatic(12.0, h1, h1 - 800.0) / 1000.0) +
        r" MW. power_rate_steady and heat_rate_steady solve the same balance for "
        r"the other unknowns.")

    # Fig 2 — when may the kinetic term be dropped?  Compare the specific KE
    # change against a representative enthalpy drop.  Below ~100 m/s it is
    # noise; a nozzle at 600 m/s is a different story.
    V2 = np.linspace(0.0, 700.0, 400)
    dke = np.array([delta_ke(0.0, v) for v in V2])

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(V2, dke, color=INK, lw=2.4, label=r"$\Delta ke=(V_2^2-V_1^2)/2$")
    for ref, lab, c in ((10.0, "1% of a 1000 kJ/kg drop", FLOW),
                        (100.0, "10% of it", ALT)):
        ax.axhline(ref, color=c, lw=1.4, ls="--")
        ax.text(12, ref * 1.14, lab, fontsize=9, color=c)
    ax.set_xlim(0, 700)
    ax.set_ylim(0.5, 400)
    ax.set_yscale("log")
    ax.set_xlabel(r"exit velocity $V_2$ (m/s), from rest")
    ax.set_ylabel(r"$\Delta ke$ (kJ/kg, log scale)")
    ax.set_title(r"When the kinetic term stops being negligible")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6, which="both")
    _save(fig, "fig2_when_ke_matters.svg")
    caps["fig2_when_ke_matters.svg"] = (
        r"The standard phrase 'kinetic energy changes are negligible', made into "
        r"a criterion. delta_ke returns $(V_2^2-V_1^2)/2$ in kJ/kg, so against a "
        r"representative 1000 kJ/kg turbine enthalpy drop the kinetic term "
        r"reaches 1% only near " + "%.0f" % (2 * 10.0 * 1000.0) ** 0.5 + r" m/s "
        r"and 10% near " + "%.0f" % (2 * 100.0 * 1000.0) ** 0.5 + r" m/s. "
        r"Turbine and compressor ducts run well below the first mark, so the "
        r"term is dropped without apology; nozzles and diffusers exist precisely "
        r"to push past the second, and there it is the enthalpy change that "
        r"serves the kinetic one.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
