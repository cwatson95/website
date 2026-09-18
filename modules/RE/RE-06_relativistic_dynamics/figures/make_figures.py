"""RE-06 figures — relativistic dynamics: the energy-momentum mass shell
E^2 = (pc)^2 + (mc^2)^2 with its ultra-relativistic asymptote, and energy /
momentum diverging at c against their bounded Newtonian counterparts.

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
from rel_dynamics import (                         # noqa: E402
    energy, momentum, kinetic_energy,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    m = 1.0
    caps = {}

    # Fig 1 — the mass shell E^2 = p^2 + m^2 (c=1): E vs p from the module, with the
    # rest energy E=m at p=0 and the ultra-relativistic asymptote E=|p|.
    v = np.linspace(0.0, 0.9995, 400)
    p = np.array([momentum(m, [vi, 0, 0])[0] for vi in v])
    E = np.array([energy(m, [vi, 0, 0]) for vi in v])
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(p, E, color=INK, lw=2, label=r"$E=\sqrt{p^{2}+m^{2}}$  (mass shell)")
    ax.plot(p, p, color=STEEL, lw=1.4, ls="--",
            label=r"asymptote  $E=|p|$  (massless / $v\to c$)")
    ax.scatter([0.0], [m], color=FLOW, zorder=5, s=45)
    ax.annotate(r"rest energy $E=m$", (0.0, m), textcoords="offset points",
                xytext=(8, 4), color=FLOW, fontsize=9)
    ax.set_xlim(0, 6); ax.set_ylim(0, 6.2); ax.set_aspect("equal")
    ax.set_xlabel("momentum $p$ (units $mc$)")
    ax.set_ylabel(r"energy $E$ (units $mc^{2}$)")
    ax.set_title(r"Energy-momentum mass shell  $E^{2}=(pc)^{2}+(mc^{2})^{2}$")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    _save(fig, "fig1_mass_shell.svg")
    caps["fig1_mass_shell.svg"] = (
        "Energy versus momentum for a particle of mass m=1 (c=1), from the module's "
        "energy() and momentum(). The curve is the mass-shell hyperbola E = sqrt(p^2 + "
        "m^2): it starts at the rest energy E=m at p=0 and bends onto the asymptote E=|p| "
        "(the massless, ultra-relativistic limit) at large momentum.")

    # Fig 2 — energy, momentum and kinetic energy all diverge as v -> c, whereas the
    # Newtonian p = m v and T = 1/2 m v^2 stay finite.
    v = np.linspace(0.0, 0.99, 400)
    p_rel = np.array([momentum(m, [vi, 0, 0])[0] for vi in v])
    T_rel = np.array([kinetic_energy(m, [vi, 0, 0]) for vi in v])
    p_newt = m * v
    T_newt = 0.5 * m * v * v
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(v, p_rel, color=INK, lw=2, label=r"relativistic $p=\gamma m v$")
    ax.plot(v, p_newt, color=INK, lw=1.4, ls="--", label=r"Newtonian $p=m v$")
    ax.plot(v, T_rel, color=FLOW, lw=2, label=r"relativistic $T=(\gamma-1)m$")
    ax.plot(v, T_newt, color=FLOW, lw=1.4, ls="--",
            label=r"Newtonian $T=\frac{1}{2}m v^{2}$")
    ax.axvline(1.0, color=ALT, lw=1.2, ls=":", label="speed of light")
    ax.set_xlim(0, 1.04); ax.set_ylim(0, 7)
    ax.set_xlabel(r"speed $v/c$")
    ax.set_ylabel(r"momentum / energy (units $mc,\ mc^{2}$)")
    ax.set_title(r"Momentum and energy blow up at $c$; Newton stays finite")
    ax.legend(loc="upper left", frameon=False, fontsize=8)
    _save(fig, "fig2_diverge_at_c.svg")
    caps["fig2_diverge_at_c.svg"] = (
        "Relativistic momentum p = gamma m v and kinetic energy T = (gamma-1)m (solid, "
        "from the module) both diverge as v -> c, while their Newtonian approximations m v "
        "and (1/2) m v^2 (dashed) remain finite and only match at low speed. The vertical "
        "line at v=c is the unreachable speed limit no massive body can cross.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
