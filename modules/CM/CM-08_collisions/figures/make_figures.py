"""CM-08 figures -- elastic vs inelastic 1-D collisions, and Rutherford scattering.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
"""
import json
import math
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
from collisions import (                           # noqa: E402
    elastic_collision_1d, inelastic_collision, rutherford_cross_section,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- projectile m1=1, v1=1 hits a stationary target m2; final velocities
    # versus mass ratio m2/m1, elastic (real elastic_collision_1d) vs perfectly
    # inelastic (real inelastic_collision, which returns the CM velocity).
    q = np.logspace(-2, 2, 400)                    # m2/m1
    v1p = np.array([elastic_collision_1d(1.0, 1.0, m2, 0.0)[0] for m2 in q])
    v2p = np.array([elastic_collision_1d(1.0, 1.0, m2, 0.0)[1] for m2 in q])
    vc = np.array([inelastic_collision(1.0, [1.0, 0.0, 0.0], m2, [0.0, 0.0, 0.0])[0] for m2 in q])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(q, v1p, color=INK, lw=2, label=r"$v_1'$ elastic")
    ax.plot(q, v2p, color=FLOW, lw=2, label=r"$v_2'$ elastic")
    ax.plot(q, vc, color=ALT, lw=2, ls="--", label=r"$v'$ inelastic (stick)")
    ax.axhline(0, color="#aaaaaa", lw=0.7)
    ax.axvline(1.0, color="#cccccc", lw=0.8, ls=":")
    ax.set_xscale("log")
    ax.set_xlabel(r"mass ratio $m_2/m_1$"); ax.set_ylabel(r"final velocity ($v_1=1$)")
    ax.set_title("Head-on collision with a target at rest: elastic vs inelastic")
    ax.legend(loc="center left", frameon=False)
    _save(fig, "fig1_elastic_vs_inelastic.svg")
    caps["fig1_elastic_vs_inelastic.svg"] = (
        "A projectile (v1=1) strikes a target at rest; final velocities vs the mass ratio m2/m1. "
        "Elastic: light target gets v2'->2 while v1' stays near +1; equal masses exchange (v1'=0, "
        "v2'=1); a heavy target reflects the projectile to v1'->-1. The inelastic stick velocity is "
        "just the centre-of-mass velocity v' = m1/(m1+m2), always between the two.")

    # Fig 2 -- Rutherford differential cross-section vs scattering angle (log y),
    # for two energies, from the real rutherford_cross_section. Forward divergence.
    theta_deg = np.linspace(5.0, 175.0, 400)
    theta = np.radians(theta_deg)
    k = 1.0
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for E, col in [(1.0, FLOW), (2.0, STEEL)]:
        dsig = np.array([rutherford_cross_section(th, E, k) for th in theta])
        ax.plot(theta_deg, dsig, color=col, lw=2, label=fr"$E={E:.0f},\ k=1$")
    ax.set_yscale("log")
    ax.set_xlabel(r"scattering angle $\theta$ (degrees)")
    ax.set_ylabel(r"$d\sigma/d\Omega$")
    ax.set_title(r"Rutherford: $\frac{d\sigma}{d\Omega}=\left(\frac{k}{4E}\right)^{2}\!/\sin^{4}\!\frac{\theta}{2}$")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig2_rutherford_cross_section.svg")
    caps["fig2_rutherford_cross_section.svg"] = (
        "Rutherford differential cross-section dsigma/dOmega = (k/4E)^2 / sin^4(theta/2) versus "
        "scattering angle (log scale), for two beam energies. It diverges strongly at small angles "
        "(most particles barely deflect) and falls off toward backscattering; higher energy E "
        "uniformly lowers the cross-section.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
