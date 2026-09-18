"""Module 1.1 figures — what the flowing matter actually carries across a control
surface (h vs V^2/2 vs gz), and the nozzle that trades enthalpy for velocity.

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
from open_systems import (                        # noqa: E402
    G, flow_energy, nozzle_exit_velocity, turbine_power, Stream,
)
import steam_lookup as st                          # noqa: E402

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the standard modeling assumption "kinetic and potential energy
    # changes are negligible", made quantitative.  psi = h + V^2/2 + gz, so the
    # KE and PE terms are plotted as a PERCENTAGE of a typical steam enthalpy:
    # velocity has to reach ~100 m/s before KE is even 0.1% of h, and a 100 m
    # elevation change is ~0.03%.  One axis (percent of h) for both terms.
    h_ref = st.h_superheated(60.0, 400.0)          # 3177.2 kJ/kg (A-4)
    V = np.linspace(0.0, 300.0, 400)
    ke_pct = 100.0 * (flow_energy(h_ref, V=V) - h_ref) / h_ref
    z = np.linspace(0.0, 300.0, 400)
    pe_pct = 100.0 * (flow_energy(h_ref, z=z) - h_ref) / h_ref

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(V, ke_pct, color=INK, lw=2.0,
            label=r"kinetic $V^2/2$   (x-axis = $V$ in m/s)")
    ax.plot(z, pe_pct, color=FLOW, lw=2.0, ls="--",
            label=r"potential $gz$   (x-axis = $z$ in m)")
    ax.axhline(1.0, color="0.6", lw=0.9, ls=":")
    ax.text(8, 1.06, r"1% of $h$", color="0.35", fontsize=9)
    ax.set_xlim(0, 300)
    ax.set_ylim(0, 1.6)
    ax.set_xlabel(r"velocity $V$ (m/s)   or   elevation $z$ (m)")
    ax.set_ylabel(r"% of $h=3177$ kJ/kg")
    ax.set_title(r"Why $\Delta$KE and $\Delta$PE are usually dropped from $\psi=h+V^2/2+gz$")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_flow_energy_terms.svg")
    caps["fig1_flow_energy_terms.svg"] = (
        r"The flow energy carried across a control surface is "
        r"$\psi=h+V^2/2+gz$ (flow_energy), but the last two terms are almost "
        r"always negligible. Measured against superheated steam at 60 bar, "
        r"400 $^\circ$C ($h=3177$ kJ/kg from steam table A-4), the velocity must "
        r"exceed $\sim$250 m/s before kinetic energy reaches 1% of $h$, and a "
        r"300 m elevation change contributes only 0.09%. This is the arithmetic "
        r"behind the standard phrase 'kinetic and potential energy changes are "
        r"negligible' — and the warning that in a nozzle, where $V$ is the whole "
        r"point, it is not.")

    # Fig 2 — the nozzle: an adiabatic CV with no shaft work converts an enthalpy
    # DROP into velocity, V_out = sqrt(V_in^2 + 2000 dh).  The square-root shape
    # means the inlet velocity stops mattering once the drop is large: the three
    # curves converge.  Distinguished by colour AND linestyle.
    dh = np.linspace(0.0, 200.0, 400)              # enthalpy drop [kJ/kg]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for Vin, c, ls in ((0.0, INK, "-"), (50.0, FLOW, "--"), (100.0, ALT, ":")):
        Vout = [nozzle_exit_velocity(dhi, 0.0, Vin) for dhi in dh]
        ax.plot(dh, Vout, color=c, lw=2.0, ls=ls,
                label=r"$V_{in}=%d$ m/s" % Vin)
    ax.set_xlabel(r"enthalpy drop $h_{in}-h_{out}$ (kJ/kg)")
    ax.set_ylabel(r"exit velocity $V_{out}$ (m/s)")
    ax.set_title(r"Adiabatic nozzle: $V_{out}=\sqrt{V_{in}^2+2\Delta h}$")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_nozzle_exit_velocity.svg")
    caps["fig2_nozzle_exit_velocity.svg"] = (
        r"A nozzle is the control volume where the kinetic term is the point. "
        r"With no shaft work and no heat transfer the steady-flow energy balance "
        r"gives $V_{out}=\sqrt{V_{in}^2+2\,\Delta h}$ (nozzle_exit_velocity, the "
        r"factor $10^3$ converting kJ/kg to J/kg). Because the dependence is a "
        r"square root, the three inlet velocities converge: by a 200 kJ/kg drop "
        r"an inlet at 100 m/s exits only 1.2% faster than one starting from "
        r"rest. A modest enthalpy drop buys a very large velocity — 632 m/s from "
        r"200 kJ/kg.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
