"""Module 13.5 figures — the blunt turbulent velocity profile against the laminar
parabola, and the Moody chart the friction correlations reproduce.

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
from turbulent_flow import (                      # noqa: E402
    reynolds_number, flow_regime, friction_factor_blasius,
    friction_factor_colebrook, friction_factor_haaland,
    power_law_velocity_profile, mean_velocity_power_law, head_loss_darcy,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — turbulent mixing flattens the core and steepens the wall gradient.
    # Both profiles are normalised to the SAME mean velocity so the comparison
    # is fair: same mass flow, very different shape.
    R = 1.0
    r = np.linspace(-R + 1e-9, R - 1e-9, 500)
    n = 7
    u_max_t = 1.0 / mean_velocity_power_law(1.0, n)     # scale to unit mean
    u_turb = np.array([power_law_velocity_profile(u_max_t, abs(x), R, n) for x in r])
    u_lam = 2.0 * (1.0 - (r / R) ** 2)                  # parabola, unit mean

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot(u_lam, r, color=INK, lw=2.3, label=r"laminar parabola (13.4)")
    ax.plot(u_turb, r, color=FLOW, lw=2.4, ls="--",
            label=r"turbulent $1/%d$ power law" % n)
    ax.axvline(1.0, color="0.55", lw=1.4, ls=":", label=r"common mean velocity")
    ax.axhline(R, color="0.4", lw=2.5)
    ax.axhline(-R, color="0.4", lw=2.5)
    ax.set_xlim(0, 2.2)
    ax.set_ylim(-1.25, 1.25)
    ax.set_xlabel(r"axial velocity / mean velocity")
    ax.set_ylabel(r"radial position $r/R$")
    ax.set_title(r"Turbulence flattens the core and sharpens the wall")
    ax.legend(loc="lower right", frameon=False, fontsize=8.5)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_profile_comparison.svg")
    caps["fig1_profile_comparison.svg"] = (
        r"The same mass flow, carried two ways. Turbulent mixing transports "
        r"momentum across the pipe far more effectively than viscosity, so the "
        r"core is nearly uniform and almost all of the velocity change is "
        r"crammed into a thin layer at the wall (power_law_velocity_profile with "
        r"$n=7$). The centreline velocity is only "
        + "%.2f" % (1.0 / mean_velocity_power_law(1.0, 7)) + r" times the mean "
        r"(mean_velocity_power_law), against exactly 2 for the laminar parabola. "
        r"The steeper wall gradient is precisely why turbulent friction is so "
        r"much higher — and why turbulent heat transfer is so much better, which "
        r"is the trade every heat-exchanger designer makes.")

    # Fig 2 — the Moody chart, generated rather than scanned.  Laminar is exact;
    # the turbulent branch is Colebrook, with Blasius valid only on smooth pipe
    # at moderate Re.
    Re_lam = np.logspace(np.log10(600.0), np.log10(2300.0), 60)
    Re_turb = np.logspace(np.log10(4000.0), 8.0, 300)

    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    # the laminar branch is direct-labelled rather than given a legend row: it
    # would otherwise share INK with the smooth-pipe Colebrook curve.
    ax.loglog(Re_lam, 64.0 / Re_lam, color="0.25", lw=2.8)
    ax.text(660, 0.058, r"laminar $64/Re$", fontsize=9, color="0.25",
            rotation=-38)
    for eps, c, ls in ((0.0, INK, "-"), (1e-4, FLOW, "--"), (2e-3, ALT, ":")):
        f = [friction_factor_colebrook(re, eps) for re in Re_turb]
        ax.loglog(Re_turb, f, color=c, lw=2.1, ls=ls,
                  label=r"Colebrook, $\varepsilon/D=%g$" % eps)
    ax.loglog(Re_turb[Re_turb < 1e5], [friction_factor_blasius(re)
                                       for re in Re_turb[Re_turb < 1e5]],
              color="0.5", lw=1.5, ls="-.",
              label=r"Blasius $0.316\,Re^{-1/4}$ (smooth, $Re<10^5$)")
    ax.axvspan(2300.0, 4000.0, color="0.85", alpha=0.6, lw=0)
    ax.text(3000, 0.0135, "transition", rotation=90, fontsize=8.5, color="0.45",
            ha="center", va="center")
    ax.set_xlim(600, 1e8)
    ax.set_ylim(0.007, 0.12)
    ax.set_xlabel(r"Reynolds number $Re$")
    ax.set_ylabel(r"Darcy friction factor $f$")
    ax.set_title(r"The Moody chart, generated from the correlations")
    ax.legend(loc="upper right", frameon=False, fontsize=8)
    ax.grid(alpha=0.25, lw=0.6, which="both")
    _save(fig, "fig2_moody_chart.svg")
    caps["fig2_moody_chart.svg"] = (
        r"The Moody chart, reproduced from the module's own correlations rather "
        r"than read off a scanned figure. The laminar branch is the exact "
        r"$64/Re$; the turbulent branches solve the implicit Colebrook equation "
        r"(friction_factor_colebrook) for three relative roughnesses, and "
        r"flow_regime marks the shaded transition band between them where "
        r"neither applies. The key behaviour is that a rough pipe becomes "
        r"FULLY ROUGH at high $Re$ — its curve flattens and the friction factor "
        r"stops depending on Reynolds number at all, so pressure drop becomes "
        r"purely quadratic in velocity. Blasius tracks the smooth curve only "
        r"below $Re\approx10^5$. friction_factor_haaland gives an explicit "
        r"approximation within about 1.5% of Colebrook — at $Re=10^6$, "
        r"$\varepsilon/D=10^{-4}$ they differ by "
        + "%.2f" % (100 * abs(friction_factor_haaland(1e6, 1e-4)
                              / friction_factor_colebrook(1e6, 1e-4) - 1)) +
        r"% — and head_loss_darcy converts any of them into metres of head.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
