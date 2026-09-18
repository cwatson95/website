"""RE-14 figures — Schwarzschild effective potential (ISCO) & light deflection.

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
from schwarzschild import (                        # noqa: E402
    effective_potential, circular_orbit_radius, isco, horizon_radius,
    light_deflection, M_SUN, R_SUN, ARCSEC_PER_RAD,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    M = 1.0

    # Fig 1 — the massive effective potential V(r)=(1-2M/r)(1+L^2/r^2) for several L.
    # The purely-GR -2M L^2/r^3 term builds an inner barrier and the ISCO at 6M;
    # circular orbits are its extrema (circular_orbit_radius).  A Newtonian curve
    # (no GR term) is overlaid to show that the barrier/ISCO are relativistic.
    r = np.linspace(2.1, 22.0, 900)
    Lc = 2.0 * math.sqrt(3.0)                       # critical L: roots merge at the ISCO
    Ls = [(Lc, STEEL, r"$L=2\sqrt{3}\,M$ (ISCO)"),
          (3.9, ALT,  r"$L=3.9\,M$"),
          (4.6, INK,  r"$L=4.6\,M$")]

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    for L, c, lbl in Ls:
        ax.plot(r, effective_potential(r, L, M), color=c, lw=2, label=lbl)
        r_min = circular_orbit_radius(L, M, stable=True)    # stable: minimum of V
        r_max = circular_orbit_radius(L, M, stable=False)   # unstable: the barrier top
        if r_min is not None:
            ax.plot(r_min, effective_potential(r_min, L, M), "o", ms=5, color=c)
        if r_max is not None and r_max > horizon_radius(M):
            ax.plot(r_max, effective_potential(r_max, L, M), "x", ms=6, color=c)
    # Newtonian effective potential for L=4.6 (drop the -2M L^2/r^3 GR term):
    Ln = 4.6
    V_newt = 1.0 - 2.0 * M / r + Ln ** 2 / r ** 2
    ax.plot(r, V_newt, color="#999999", lw=1.4, ls="--",
            label=r"Newtonian $L=4.6\,M$ (no GR term)")
    ax.axvline(isco(M), color="#b5651d", lw=1.0, ls=":")
    ax.text(isco(M) + 0.2, 1.205, r"ISCO $6M$", color="#b5651d", fontsize=9)
    ax.axvspan(2.0, horizon_radius(M), color="#000000", alpha=0.06)
    ax.text(2.05, 0.875, r"horizon $2M$", color="#444444", fontsize=8, rotation=90, va="bottom")
    ax.set_xlim(2.0, 22.0)
    ax.set_ylim(0.86, 1.24)
    ax.set_xlabel(r"radius $r$  (units of $M$)")
    ax.set_ylabel(r"effective potential $V(r)$")
    ax.set_title(r"Schwarzschild orbits: the GR term makes a barrier and the ISCO")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    _save(fig, "fig1_effective_potential.svg")
    caps["fig1_effective_potential.svg"] = (
        r"Massive effective potential $V=(1-2M/r)(1+L^2/r^2)$ from effective_potential "
        r"for several $L$: filled dots mark stable circular orbits (minima), crosses "
        r"the unstable maxima (circular_orbit_radius). The purely-GR $-2ML^2/r^3$ term "
        r"raises an inner barrier absent from the Newtonian curve (dashed); at "
        r"$L=2\sqrt3\,M$ the extrema merge at the ISCO $r=6M$.")

    # Fig 2 — deflection of light grazing the Sun: GR 4M/b vs the EP-only half 2M/b.
    # light_deflection gives the full GR 4M/b; the equivalence principle alone (RE-10)
    # would give exactly half -- the figure shows GR is twice the naive value.
    b = np.linspace(1.0, 12.0, 400)                 # impact parameter in solar radii
    defl_gr = np.array([light_deflection(M_SUN, bi * R_SUN) for bi in b]) * ARCSEC_PER_RAD
    defl_ep = 0.5 * defl_gr                          # equivalence-principle-only 2M/b

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(b, defl_gr, color=INK, lw=2, label=r"general relativity $\;4M/b$")
    ax.plot(b, defl_ep, color=FLOW, lw=2, ls="--",
            label=r"equivalence principle only $\;2M/b$")
    graze_gr = light_deflection(M_SUN, R_SUN) * ARCSEC_PER_RAD
    ax.plot(1.0, graze_gr, "o", ms=5, color=INK)
    ax.annotate(fr"grazing Sun: ${graze_gr:.2f}''$" + "\n(Eddington 1919)",
                xy=(1.0, graze_gr), xytext=(2.6, graze_gr * 0.92),
                fontsize=9, color=INK,
                arrowprops=dict(arrowstyle="->", color=INK, lw=0.8))
    ax.plot(1.0, 0.5 * graze_gr, "o", ms=5, color=FLOW)
    ax.set_xlim(1.0, 12.0)
    ax.set_xlabel(r"impact parameter $b$  (units of $R_\odot$)")
    ax.set_ylabel(r"light deflection (arcsec)")
    ax.set_title(r"Light bending: GR predicts exactly twice the EP value")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_light_deflection.svg")
    caps["fig2_light_deflection.svg"] = (
        r"Deflection of starlight vs impact parameter from light_deflection: the GR "
        r"value $4M/b$ (solid) is exactly twice the equivalence-principle-only $2M/b$ "
        r"(dashed) — half from time dilation, half from spatial curvature. Grazing the "
        r"Sun ($b=R_\odot$) gives $1.75''$, the 1919 eclipse result.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
