"""RE-10 figures — the equivalence principle: light bends in an accelerated box
exactly as in a uniform field g, and a rocket's redshift equals a field's.

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
from equivalence_principle import (                # noqa: E402
    C, STD_GRAVITY, light_deflection_elevator,
    accelerated_frame_redshift, redshift_uniform_field, pound_rebka,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — a light ray "falls" as it crosses an accelerating box: parabolic bend.
    L = 10.0
    x = np.linspace(0.0, L, 120)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    # exaggerated accelerations chosen so the deflection is visible (real g gives ~nm):
    cases = [(0.10, STEEL), (0.20, INK), (0.30, FLOW)]
    for ang_full, col in cases:
        a = ang_full * C * C / L                    # a giving exit angle gL/c^2 = ang_full
        drop = np.array([light_deflection_elevator(a, float(xi))[0] for xi in x])
        ax.plot(x, -drop, color=col, lw=2,
                label=fr"$a={a:.2e}\,$m/s$^2$  ($\theta={ang_full}$)")
    ax.plot([0, L], [0, 0], color="#bbbbbb", lw=0.8, ls="--")
    ax.annotate("", xy=(0.0, -0.3), xytext=(0.0, 0.6),
                arrowprops=dict(arrowstyle="->", color=ALT))
    ax.text(0.15, 0.55, "box accelerates $g$", color=ALT, fontsize=9)
    ax.set_xlabel("distance across the box  $x$ (m)")
    ax.set_ylabel("transverse drop  $-\\frac{1}{2}g(x/c)^2$ (m)")
    ax.set_title(r"Light bends in an accelerating box $\equiv$ a uniform field $g$")
    ax.legend(loc="lower left", frameon=False, fontsize=9)
    _save(fig, "fig1_light_bending_elevator.svg")
    caps["fig1_light_bending_elevator.svg"] = (
        "A horizontal light ray traced across a box of width 10 m by the module's "
        "light_deflection_elevator: the accelerating floor makes the ray drop along the "
        "parabola (1/2) g (x/c)^2. Accelerations are exaggerated so the bend is visible. By "
        "the equivalence principle the same parabolic deflection must occur in a real uniform field g.")

    # Fig 2 — equivalence made quantitative: rocket(a) redshift == field(g=a) redshift.
    g = STD_GRAVITY
    h = np.linspace(0.0, 120.0, 200)
    rocket = np.array([abs(accelerated_frame_redshift(g, float(hi))) for hi in h]) * 1e15
    field = np.array([abs(redshift_uniform_field(g, float(hi))) for hi in h]) * 1e15
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(h, rocket, color=INK, lw=3.0, label=r"rocket: $|{-}ah/c^2|$")
    ax.plot(h, field, color=FLOW, lw=1.5, ls="--", label=r"field $g=a$: $|{-}gh/c^2|$")
    pr = pound_rebka() * 1e15                        # Pound-Rebka tower, h = 22.5 m
    ax.plot(22.5, pr, "o", color=ALT, ms=7, zorder=5)
    ax.annotate(f"Pound-Rebka\n$h=22.5$ m, $|{{\\Delta}}f/f|={pr*1e-15:.2e}$",
                xy=(22.5, pr), xytext=(40, pr * 0.45),
                arrowprops=dict(arrowstyle="->", color=ALT), color=ALT, fontsize=9)
    ax.set_xlim(0, 120); ax.set_ylim(bottom=0)
    ax.set_xlabel("height  $h$ (m)")
    ax.set_ylabel(r"$|\Delta f/f|\times 10^{15}$")
    ax.set_title(r"Equivalence: a rocket's redshift equals a field's ($g=a$)")
    ax.legend(loc="upper left", frameon=False)
    _save(fig, "fig2_redshift_equivalence.svg")
    caps["fig2_redshift_equivalence.svg"] = (
        "Fractional gravitational redshift |Delta f/f| versus height. The shift inside a "
        "rocket accelerating at a (accelerated_frame_redshift) lies exactly on top of the "
        "shift in a static uniform field g = a (redshift_uniform_field): no sealed-cabin "
        "experiment can tell them apart. The marker is the 22.5 m Pound-Rebka tower, |Delta f/f| ~ 2.5e-15.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
