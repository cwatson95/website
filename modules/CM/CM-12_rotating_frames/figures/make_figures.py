"""CM-12 figures -- a free particle seen in the inertial vs the rotating frame
(Coriolis deflection), and the outward centrifugal acceleration field.

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
from rotating_frames import centrifugal_acceleration, coriolis_acceleration   # noqa: E402
# Use MA-07's tested integrator to step the rotating-frame equation of motion:
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "MA", "MA-07_ode", "code"))
from ode import integrate                          # noqa: E402

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    W = 1.0
    omega = (0.0, 0.0, W)                           # rotation about +z
    V = 1.0                                         # launch speed (radially outward at t=0)
    tmax = 4.0

    # Fig 1 -- a FREE particle (no real force). Inertial frame: a straight line.
    # Rotating frame: integrate a_rot = (-2 omega x v) + (-omega x (omega x r)),
    # i.e. coriolis_acceleration + centrifugal_acceleration from the module.
    def rhs(t, y):
        x, yy, vx, vy = y
        acf = centrifugal_acceleration(omega, (x, yy, 0.0))
        acor = coriolis_acceleration(omega, (vx, vy, 0.0))
        return [vx, vy, acf[0] + acor[0], acf[1] + acor[1]]

    ts, ys = integrate(rhs, [0.0, 0.0, V, 0.0], 0.0, tmax, 1200)
    ts = np.array(ts)
    xr = np.array([s[0] for s in ys]); yr = np.array([s[1] for s in ys])
    xi = V * ts                                     # inertial straight line: r = (V t, 0)
    yi = np.zeros_like(ts)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(xi, yi, color=INK, lw=2.2, label="inertial frame (straight)")
    ax.plot(xr, yr, color=FLOW, lw=2.2, label="rotating frame (deflected)")
    ax.plot(0, 0, "o", color="#444444", ms=6)
    ax.annotate("start", xy=(0, 0), xytext=(0.25, 0.45), fontsize=9, color="#444444")
    ax.plot(xi[-1], yi[-1], "o", color=INK, ms=5)
    ax.plot(xr[-1], yr[-1], "o", color=FLOW, ms=5)
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title(r"Same free motion, two frames: Coriolis bends the path ($\omega=1\,\hat z$)")
    ax.legend(loc="lower left", frameon=False)
    _save(fig, "fig1_inertial_vs_rotating.svg")
    caps["fig1_inertial_vs_rotating.svg"] = (
        "A free particle launched from the centre. In the inertial frame it travels in a straight "
        "line. In the frame rotating at omega about z, integrating the module's fictitious "
        "accelerations (Coriolis -2 omega x v plus centrifugal) bends the very same motion into a "
        "curved spiral -- the apparent deflection seen by an observer on a turntable.")

    # Fig 2 -- the centrifugal acceleration field -omega x (omega x r): outward,
    # magnitude omega^2 * rho (real centrifugal_acceleration on a grid). Coriolis
    # arrows (for an outward-moving particle) show the perpendicular deflection.
    g = np.linspace(-3.0, 3.0, 7)
    X, Y = np.meshgrid(g, g)
    U = np.zeros_like(X); Vv = np.zeros_like(Y)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            a = centrifugal_acceleration(omega, (X[i, j], Y[i, j], 0.0))
            U[i, j], Vv[i, j] = a[0], a[1]

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.quiver(X, Y, U, Vv, color=STEEL, angles="xy", scale_units="xy", scale=4.0,
              width=0.005, label="_nolegend_")
    # Coriolis arrows for a particle moving outward (+x): a_cor = -2 omega x v.
    acor = coriolis_acceleration(omega, (V, 0.0, 0.0))   # constant for constant v
    for xp in (1.0, 2.0):
        ax.annotate("", xy=(xp + 0.5 * acor[0], 0.5 * acor[1]), xytext=(xp, 0.0),
                    arrowprops=dict(arrowstyle="->", color=FLOW, lw=2))
    ax.plot([], [], color=STEEL, lw=2, label=r"centrifugal $\omega^{2}\rho$ (outward)")
    ax.plot([], [], color=FLOW, lw=2, label=r"Coriolis $-2\,\omega\times v$ ($v\!=\!+x$)")
    ax.plot(0, 0, "+", color="#888888", ms=10)
    ax.set_aspect("equal")
    ax.set_xlim(-3.6, 3.6); ax.set_ylim(-3.6, 3.6)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title(r"Fictitious accelerations: centrifugal field, Coriolis $\perp v$")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_centrifugal_field.svg")
    caps["fig2_centrifugal_field.svg"] = (
        "The centrifugal acceleration field -omega x (omega x r) from the module: it points radially "
        "outward and grows in magnitude as omega^2 times the distance from the axis. Orange arrows "
        "show the Coriolis acceleration -2 omega x v for a particle moving in +x; it acts "
        "perpendicular to the velocity, sideways, which is what curves the path in Fig 1.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
