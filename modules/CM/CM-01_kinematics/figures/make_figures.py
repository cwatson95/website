"""CM-01 figures — projectile paths and the tangential/normal acceleration split.

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
matplotlib.rcParams["svg.fonttype"] = "path"      # text as vector paths (portable)
matplotlib.rcParams["font.size"] = 11
import matplotlib.pyplot as plt                    # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from kinematics import (                           # noqa: E402
    projectile, range_, max_height, time_of_flight,
    speed, tangential_acceleration, normal_acceleration,
)

INK, FLOW, ALT, FOUR = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — real projectile() trajectories at several launch angles; range peaks at 45 deg.
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    v0 = 20.0
    for ang_deg, col in [(30.0, INK), (45.0, FLOW), (60.0, ALT)]:
        ang = math.radians(ang_deg)
        r = projectile(v0, ang)
        T = time_of_flight(v0, ang)
        ts = np.linspace(0.0, T, 200)
        xs = [r(float(t))[0] for t in ts]
        zs = [r(float(t))[2] for t in ts]
        ax.plot(xs, zs, color=col, lw=2,
                label=fr"$\theta={ang_deg:.0f}^\circ$  (R={range_(v0, ang):.1f} m)")
        ax.plot(range_(v0, ang), 0.0, "o", color=col, ms=5)                # landing
        ax.plot(range_(v0, ang) / 2.0, max_height(v0, ang), "^", color=col, ms=6)  # apex
    ax.axhline(0, color="#aaaaaa", lw=0.6)
    ax.set_xlabel("horizontal $x$ (m)"); ax.set_ylabel("height $z$ (m)")
    ax.set_title(r"Projectile range is maximal at $45^\circ$ ($v_0=20$ m/s)")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig1_projectile_range.svg")
    caps["fig1_projectile_range.svg"] = (
        "Trajectories from the module's projectile() launched at 20 m/s for 30, 45 and "
        "60 degrees (circles mark the landing range R, triangles the apex). The range "
        "v0^2 sin(2 theta)/g is largest at 45 degrees; 30 and 60 give the same range.")

    # Fig 2 — uniform circular motion: tangential/normal split via the real functions.
    R, w = 2.0, 3.0
    circ = lambda t: (R * math.cos(w * t), R * math.sin(w * t), 0.0)
    sp = speed(circ)
    aT = tangential_acceleration(circ)
    aN = normal_acceleration(circ)
    ts = np.linspace(0.0, 2.0 * math.pi / w, 220)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(ts, [sp(float(t)) for t in ts], color=INK, lw=2, label=r"speed $|v|=R\omega$")
    ax.plot(ts, [aN(float(t)) for t in ts], color=FLOW, lw=2,
            label=r"$a_N=v^2/R$ (centripetal)")
    ax.plot(ts, [aT(float(t)) for t in ts], color=ALT, lw=2, label=r"$a_T=d|v|/dt$")
    ax.axhline(R * w, color=INK, ls=":", lw=1)
    ax.axhline((R * w) ** 2 / R, color=FLOW, ls=":", lw=1)
    ax.set_xlabel("time $t$ (s)"); ax.set_ylabel("magnitude (SI)")
    ax.set_title(r"Circular motion: constant speed, all acceleration normal")
    ax.legend(loc="center right", frameon=False)
    _save(fig, "fig2_circular_accel_split.svg")
    caps["fig2_circular_accel_split.svg"] = (
        "Uniform circular motion (R=2, omega=3) decomposed by the module's speed, "
        "tangential_acceleration and normal_acceleration. The speed is constant (R omega=6) "
        "so a_T is essentially zero, while the entire acceleration is normal: a_N = v^2/R = 18.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
