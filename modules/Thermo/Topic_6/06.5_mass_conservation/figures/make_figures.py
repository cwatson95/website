"""Module 6.5 figures — continuity as a hyperbola (area against velocity at fixed
mass flow), and the tank whose level is set by the imbalance of its streams.

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
from mass_conservation import (                   # noqa: E402
    mass_flow_rate, mass_flow_rate_rho, mdot_from_volumetric,
    velocity_from_mdot, dmcv_dt, is_steady_mass,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — continuity at fixed mdot: V = mdot v / A is a hyperbola, so
    # narrowing a duct speeds the flow in exact inverse proportion.  Three
    # specific volumes show that a gas (large v) needs far more area than a
    # liquid for the same mass flow.
    A = np.linspace(0.002, 0.06, 300)

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    for v, lab, c, ls in ((0.001, r"liquid water, $v=0.001$", INK, "-"),
                          (0.10, r"steam, $v=0.10$", FLOW, "--"),
                          (0.50, r"steam, $v=0.50$", ALT, ":")):
        V = np.array([velocity_from_mdot(2.0, v, a) for a in A])
        ax.plot(A * 1e3, V, color=c, lw=2.1, ls=ls,
                label=lab + r" m$^3$/kg")
    ax.set_xlim(2, 60)
    ax.set_ylim(0, 320)
    ax.set_xlabel(r"flow area $A$ ($\times10^{-3}$ m$^2$)")
    ax.set_ylabel(r"velocity $V$ (m/s)")
    ax.set_title(r"Continuity at $\dot{m}=2$ kg/s:  $V=\dot{m}v/A$")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_continuity_hyperbola.svg")
    caps["fig1_continuity_hyperbola.svg"] = (
        r"One-dimensional continuity $\dot m=AV/v$ (mass_flow_rate) rearranged "
        r"for velocity (velocity_from_mdot). At a fixed 2 kg/s the velocity is "
        r"inversely proportional to area, so halving a duct doubles the speed — "
        r"and the specific volume sets the whole scale. Carrying 2 kg/s of "
        r"liquid water through 10 cm$^2$ needs only "
        + "%.1f" % velocity_from_mdot(2.0, 0.001, 0.001) + r" m/s, whereas the "
        r"same mass flow of low-pressure steam through the same area demands "
        + "%.0f" % velocity_from_mdot(2.0, 0.5, 0.001) + r" m/s. This is why "
        r"steam lines are enormous compared with the feedwater piping that "
        r"carries the identical mass around a Rankine cycle. mass_flow_rate_rho "
        r"and mdot_from_volumetric express the same relation in density and "
        r"volumetric-flow terms.")

    # Fig 2 — unsteady: a receiver with a fixed inflow and a throttled outflow.
    # dm_cv/dt is the imbalance, and the stored mass is its running integral.
    t = np.linspace(0.0, 120.0, 400)
    mdot_in = 3.0
    mdot_out = np.where(t < 40.0, 1.5, np.where(t < 80.0, 3.0, 4.5))
    rate = np.array([dmcv_dt([mdot_in], [mo]) for mo in mdot_out])
    m_stored = 50.0 + np.concatenate([[0.0], np.cumsum(0.5 * (rate[1:] + rate[:-1])
                                                       * np.diff(t))])

    fig, (axT, axB) = plt.subplots(2, 1, figsize=(6.2, 4.4), sharex=True,
                                   gridspec_kw={"height_ratios": [1, 1.15]})
    axT.plot(t, rate, color=INK, lw=2.2)
    axT.axhline(0.0, color="0.6", lw=1.0, ls="-.")
    axT.fill_between(t, 0, rate, where=(rate > 0), color=INK, alpha=0.14, lw=0)
    axT.fill_between(t, 0, rate, where=(rate < 0), color=FLOW, alpha=0.16, lw=0)
    axT.set_ylabel(r"$dm_{cv}/dt$ (kg/s)")
    axT.set_title(r"Filling, holding, then draining a receiver")
    axT.grid(alpha=0.25, lw=0.6)
    axT.text(18, 1.0, "filling", fontsize=9, color=INK, ha="center")
    axT.text(60, 0.28, r"steady  (is_steady_mass $\rightarrow$ %s)"
             % is_steady_mass([3.0], [3.0]), fontsize=8.5, color="0.35",
             ha="center")
    axT.text(100, -1.0, "draining", fontsize=9, color=FLOW, ha="center")

    axB.plot(t, m_stored, color=ALT, lw=2.4)
    axB.set_xlim(0, 120)
    axB.set_xlabel(r"time (s)")
    axB.set_ylabel(r"mass in the CV (kg)")
    axB.grid(alpha=0.25, lw=0.6)
    fig.tight_layout()
    _save(fig, "fig2_unsteady_inventory.svg")
    caps["fig2_unsteady_inventory.svg"] = (
        r"What the mass rate balance says when the steady assumption is dropped. "
        r"A receiver takes a constant 3 kg/s while its outlet is stepped from "
        r"1.5 to 3.0 to 4.5 kg/s: dmcv_dt returns the instantaneous imbalance "
        r"(top), and the stored mass is its running integral (bottom). Only the "
        r"middle stretch satisfies is_steady_mass, and only there is the "
        r"inventory flat. The slope of the lower curve IS the upper curve — the "
        r"whole content of $dm_{cv}/dt=\sum\dot m_i-\sum\dot m_e$, and the "
        r"template every transient filling or discharging problem follows.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
