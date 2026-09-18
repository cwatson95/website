"""RE-01 figures — Galilean relativity: worldlines under a boost, and the
linear (Galilean) vs saturating (Einstein) velocity-addition rule.

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
from galilean import (                             # noqa: E402
    galilean_position, galilean_velocity_add, relativistic_velocity_add, C_LIGHT,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — worldlines of three objects in the lab frame and in a frame boosted
    # at V, using the module's Galilean position transform r' = r - V t.
    V = 0.5                                         # boost velocity (units: x per t)
    objects = [                                     # (label, x0, v_lab, colour)
        ("at rest", -2.0, 0.0, INK),
        ("moves at V", 0.0, V, FLOW),
        ("fast", 2.0, 1.0, ALT),
    ]
    t = np.linspace(0.0, 4.0, 60)
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(6.2, 3.5), sharey=True)
    for label, x0, v, col in objects:
        x_lab = x0 + v * t
        # boosted positions via the real CM-03/RE-01 transform (loop: it is 3-vector)
        x_boost = np.array([galilean_position([x0 + v * ti, 0.0, 0.0],
                                              [V, 0.0, 0.0], ti)[0] for ti in t])
        axL.plot(x_lab, t, color=col, lw=2, label=label)
        axR.plot(x_boost, t, color=col, lw=2)
    axL.set_title("lab frame $S$")
    axR.set_title(r"boosted frame $S'$ ($V=0.5$)")
    for ax in (axL, axR):
        ax.axvline(0, color="#cccccc", lw=0.6)
        ax.set_xlabel("position $x$")
        ax.set_xlim(-3, 6)
    axL.set_ylabel("time $t$ (absolute)")
    axL.legend(loc="upper left", frameon=False, fontsize=9)
    fig.suptitle("Galilean boost re-slants worldlines; the $V$-object stands still in $S'$")
    _save(fig, "fig1_galilean_worldlines.svg")
    caps["fig1_galilean_worldlines.svg"] = (
        "Worldlines of three objects (x horizontal, absolute time t vertical) in the lab "
        "frame S and in a frame S' boosted at V=0.5, mapped by the module's Galilean "
        "transform x' = x - V t. Every slope shifts by -V, so the object moving at V "
        "becomes a vertical (at-rest) worldline in S'; time is unchanged.")

    # Fig 2 — velocity addition: Galilean u+v is linear and overshoots c, while
    # Einstein's rule (the module's relativistic_velocity_add) saturates at c.
    u = 0.5 * C_LIGHT
    frac = np.linspace(0.0, 0.999, 300)
    w_gal = np.array([galilean_velocity_add(u, f * C_LIGHT) for f in frac]) / C_LIGHT
    w_rel = np.array([relativistic_velocity_add(u, f * C_LIGHT) for f in frac]) / C_LIGHT
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(frac, w_gal, color=FLOW, lw=2, label=r"Galilean  $w=u+v$ (linear)")
    ax.plot(frac, w_rel, color=INK, lw=2,
            label=r"Einstein  $w=\frac{u+v}{1+uv/c^{2}}$")
    ax.axhline(1.0, color=ALT, lw=1.2, ls="--", label="speed of light $c$")
    ax.set_xlabel(r"added velocity $v/c$  (with $u=0.5\,c$ fixed)")
    ax.set_ylabel(r"combined velocity $w/c$")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.6)
    ax.set_title("Velocities add linearly for Galileo — but never exceed $c$ for Einstein")
    ax.legend(loc="upper left", frameon=False)
    _save(fig, "fig2_velocity_addition.svg")
    caps["fig2_velocity_addition.svg"] = (
        "Combining a fixed u=0.5c with a second velocity v. The Galilean rule w=u+v "
        "(orange) is a straight line that overshoots c, while Einstein's relativistic "
        "addition (blue) saturates at the dashed light line c. The two agree only at "
        "small v/c, where Galilean relativity is the low-speed limit.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
