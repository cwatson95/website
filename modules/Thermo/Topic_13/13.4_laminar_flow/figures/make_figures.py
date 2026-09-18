"""Module 13.4 figures — the parabolic Hagen-Poiseuille profile, and the exact
f = 64/Re friction law that only laminar flow enjoys.

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
from laminar_flow import (                        # noqa: E402
    reynolds_number, is_laminar, friction_factor_laminar,
    velocity_profile_parabolic, mean_velocity_from_max, pressure_drop_darcy,
    pressure_drop_hagen_poiseuille, volumetric_flow_hagen_poiseuille,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the profile.  Fully developed laminar pipe flow is exactly
    # parabolic, and the mean velocity is exactly half the centreline value --
    # one of the few results in fluid mechanics with no empirical content.
    R = 1.0
    r = np.linspace(-R, R, 400)
    u_max = 2.0
    u = np.array([velocity_profile_parabolic(u_max, abs(x), R) for x in r])
    V_mean = mean_velocity_from_max(u_max)

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot(u, r, color=INK, lw=2.4, label=r"$u(r)=u_{max}[1-(r/R)^2]$")
    ax.fill_betweenx(r, 0, u, color=INK, alpha=0.10, lw=0)
    ax.axvline(V_mean, color=FLOW, lw=1.8, ls="--",
               label=r"mean $V=u_{max}/2=%.1f$" % V_mean)
    ax.axhline(R, color="0.4", lw=2.5)
    ax.axhline(-R, color="0.4", lw=2.5)
    ax.text(0.06, 0.90, "pipe wall: no slip", fontsize=9, color="0.4")
    ax.set_xlim(0, 2.2)
    ax.set_ylim(-1.25, 1.25)
    ax.set_xlabel(r"axial velocity $u$ (arbitrary units)")
    ax.set_ylabel(r"radial position $r/R$")
    ax.set_title(r"Fully developed laminar flow is exactly parabolic")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_parabolic_profile.svg")
    caps["fig1_parabolic_profile.svg"] = (
        r"Fully developed laminar flow in a round pipe has an exactly parabolic "
        r"velocity profile (velocity_profile_parabolic), pinned to zero at the "
        r"wall by the no-slip condition and peaking on the centreline. "
        r"Integrating it gives the clean result that the mean velocity is "
        r"precisely half the maximum (mean_velocity_from_max) — so a pitot probe "
        r"on the axis of a laminar pipe reads exactly twice the bulk velocity. "
        r"This profile is a solution of the Navier-Stokes equations rather than "
        r"a correlation, which is what makes the laminar results in this module "
        r"exact and the turbulent ones in module 13.5 empirical.")

    # Fig 2 — the friction law, and the two routes to the same pressure drop.
    # f = 64/Re is exact; Darcy-Weisbach with that f must reproduce
    # Hagen-Poiseuille, and does.
    rho, mu, D, L = 998.0, 1.0e-3, 0.02, 10.0
    V = np.linspace(0.005, 0.115, 300)
    Re = np.array([reynolds_number(rho, v, D, mu) for v in V])
    dP_hp = np.array([pressure_drop_hagen_poiseuille(mu, L, v, D) for v in V])
    dP_dw = np.array([pressure_drop_darcy(friction_factor_laminar(re), L, D, rho, v)
                      for re, v in zip(Re, V)])

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot(Re, dP_hp, color=INK, lw=2.6,
            label=r"Hagen-Poiseuille $\Delta p=32\mu LV/D^2$")
    ax.plot(Re[::10], dP_dw[::10], ls="none", marker="o", ms=6.5, mfc="white",
            mec=FLOW, mew=1.7,
            label=r"Darcy-Weisbach with $f=64/Re$")
    ax.axvline(2300.0, color=ALT, lw=1.6, ls="--")
    ax.text(2260, 140, r"$Re=2300$: transition begins" "\n"
                       r"(is_laminar $\rightarrow$ False beyond)",
            fontsize=9, color=ALT, ha="right")
    ax.set_xlim(0, 2600)
    ax.set_xlabel(r"Reynolds number $Re=\rho VD/\mu$")
    ax.set_ylabel(r"pressure drop over 10 m (Pa)")
    ax.set_title(r"Two derivations, one laminar friction law")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_laminar_friction.svg")
    caps["fig2_laminar_friction.svg"] = (
        r"In the laminar regime the friction factor is not fitted to data — it "
        r"is derived: $f=64/Re$ (friction_factor_laminar). The consistency check "
        r"is that feeding it into the general Darcy-Weisbach formula "
        r"(pressure_drop_darcy) must reproduce the Hagen-Poiseuille result "
        r"obtained directly from the parabolic profile "
        r"(pressure_drop_hagen_poiseuille), and the circles land on the line "
        r"everywhere. Pressure drop is therefore strictly LINEAR in velocity "
        r"here, unlike the roughly quadratic turbulent behaviour of module 13.5. "
        r"Water in a 20 mm pipe stays laminar (is_laminar) only up to about "
        + "%.3f" % (2300.0 * 1.0e-3 / (998.0 * 0.02)) + r" m/s; "
        r"volumetric_flow_hagen_poiseuille gives the $R^4$ dependence that makes "
        r"narrow tubes so restrictive.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
