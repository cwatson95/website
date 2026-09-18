"""CM-10 figures -- centripetal acceleration vectors on a circular path, and the
tangential/centripetal split of acceleration in non-uniform circular motion.

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
from circular_motion import uniform_circular, centripetal_acceleration   # noqa: E402
# CM-10 is built on CM-01; reuse its kinematics on the trajectory:
from kinematics import velocity, speed, tangential_acceleration, normal_acceleration  # noqa: E402

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- uniform circular motion: the velocity is tangent, the acceleration
    # points inward with constant magnitude a_c = v^2/R (real centripetal_acceleration).
    R, omega = 2.0, 1.3
    circ = uniform_circular(R, omega)              # real module trajectory r(t)
    vfun = velocity(circ)                          # CM-01 velocity of that trajectory
    v_speed = R * omega
    a_c = centripetal_acceleration(v_speed, R)     # real module function: v^2/R

    th = np.linspace(0, 2 * math.pi, 240)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(R * np.cos(th), R * np.sin(th), color="#cccccc", lw=1.5)
    ax.plot(0, 0, "+", color="#888888", ms=9)
    sv, sa = 0.45, 0.45                            # arrow display scales
    for k in range(8):
        tk = k * (2 * math.pi / omega) / 8.0
        x, y, _ = circ(tk)
        vx, vy, _ = vfun(tk)
        n = math.hypot(vx, vy)
        # velocity arrow (tangent, orange)
        ax.annotate("", xy=(x + sv * vx / n * v_speed * 0.5, y + sv * vy / n * v_speed * 0.5),
                    xytext=(x, y), arrowprops=dict(arrowstyle="->", color=FLOW, lw=1.6))
        # centripetal acceleration arrow (inward = -r_hat, blue), magnitude a_c
        rhx, rhy = x / R, y / R
        ax.annotate("", xy=(x - sa * rhx * a_c * 0.5, y - sa * rhy * a_c * 0.5),
                    xytext=(x, y), arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))
    ax.plot([], [], color=FLOW, lw=1.6, label=r"velocity $v$ (tangent)")
    ax.plot([], [], color=INK, lw=1.6, label=r"$a_c=v^{2}/R$ (inward)")
    ax.set_aspect("equal")
    ax.set_xlim(-3.2, 3.2); ax.set_ylim(-3.0, 3.0)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title(r"Uniform circular motion: $a_c=v^{2}/R$ points to the centre, $a\perp v$")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig1_centripetal_vectors.svg")
    caps["fig1_centripetal_vectors.svg"] = (
        "Uniform circular motion from the module's uniform_circular trajectory. The velocity "
        "(orange) is everywhere tangent to the circle; the acceleration (blue) has constant "
        "magnitude a_c = v^2/R and always points inward to the centre, perpendicular to v. It "
        "changes the direction of the velocity, not its speed.")

    # Fig 2 -- non-uniform circular motion (spin-up): speed grows, so acceleration
    # splits into a constant tangential part (changes speed) and a growing
    # centripetal part a_N = v^2/R (real centripetal_acceleration), from CM-01.
    R2, alpha = 1.5, 0.8

    def spinup(t):
        phi = 0.5 * alpha * t * t                  # phi'' = alpha (constant angular accel)
        return (R2 * math.cos(phi), R2 * math.sin(phi), 0.0)

    sp = speed(spinup)
    aT = tangential_acceleration(spinup)
    aN = normal_acceleration(spinup)
    t = np.linspace(0.05, 3.0, 300)
    v = np.array([sp(ti) for ti in t])
    a_tan = np.array([aT(ti) for ti in t])
    a_nrm = np.array([aN(ti) for ti in t])
    a_cp = np.array([centripetal_acceleration(sp(ti), R2) for ti in t])   # real fn, = v^2/R
    a_tot = np.sqrt(a_tan ** 2 + a_nrm ** 2)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(t, v, color=STEEL, lw=2, label=r"speed $v$")
    ax.plot(t, a_tan, color=FLOW, lw=2, label=r"$a_T$ tangential")
    ax.plot(t, a_nrm, color=INK, lw=2, label=r"$a_N=v^{2}/R$ centripetal")
    ax.plot(t, a_cp, color=ALT, lw=1.2, ls="--", label=r"$v^{2}/R$ (module)")
    ax.plot(t, a_tot, color="#777777", lw=1.0, ls=":", label=r"$|a|$")
    ax.set_xlabel("time $t$"); ax.set_ylabel("speed / acceleration")
    ax.set_title("Non-uniform circular motion: constant $a_T$, growing $a_N=v^{2}/R$")
    ax.legend(loc="upper left", frameon=False, ncol=2)
    _save(fig, "fig2_tangential_vs_centripetal.svg")
    caps["fig2_tangential_vs_centripetal.svg"] = (
        "A circle traversed with constant angular acceleration. The tangential acceleration a_T is "
        "constant and raises the speed v; the centripetal (normal) acceleration a_N grows as v^2/R, "
        "shown both from CM-01 and from the module's centripetal_acceleration (dashed, identical). "
        "Total acceleration is the quadrature sum of the two perpendicular parts.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
