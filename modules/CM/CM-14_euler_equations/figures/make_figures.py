"""CM-14 figures — torque-free rigid-body rotation from Euler's equations: the
body-frame angular velocity vs time, and the polhode portrait that makes rotation
stable about the two extreme principal axes but unstable about the middle one.

Imports the module's own code in ../code and renders two SVGs plus a captions.json
(matplotlib -> SVG with text as portable vector outlines, saved next to a
captions.json the browser shows under each figure).  Run:  python3 make_figures.py
"""
import json
import math
import os
import sys

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"
matplotlib.rcParams["font.size"] = 11
import matplotlib.pyplot as plt                    # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from euler_equations import (                       # noqa: E402
    integrate_euler, rotational_energy, L_magnitude_sq,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"
I = (1.0, 2.0, 3.0)                                 # principal moments, I1 < I2 < I3


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — torque-free angular velocity in the body frame; |L|^2 and 2T stay fixed.
    ts, ws = integrate_euler(I, (1.0, 1.0, 1.0), 0.0, 10.0, 4000)
    W = np.array(ws)
    L2 = (L_magnitude_sq(I, ws[0]), L_magnitude_sq(I, ws[-1]))
    TT = (rotational_energy(I, ws[0]), rotational_energy(I, ws[-1]))
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(ts, W[:, 0], color=INK,   lw=2, label=r"$\omega_1$")
    ax.plot(ts, W[:, 1], color=FLOW,  lw=2, label=r"$\omega_2$")
    ax.plot(ts, W[:, 2], color=STEEL, lw=2, label=r"$\omega_3$")
    ax.set_xlabel("time $t$")
    ax.set_ylabel(r"body-frame $\vec{\omega}$ components")
    ax.set_title("Torque-free asymmetric top: periodic exchange among $\\omega_i$")
    ax.text(0.02, 0.04,
            r"conserved:  $|L|^2=%.2f$,  $2T=%.2f$" % (L2[1], 2 * TT[1]),
            transform=ax.transAxes, color="#555555")
    ax.legend(loc="upper right", ncol=3, frameon=False)
    _save(fig, "fig1_omega_vs_time.svg")
    caps["fig1_omega_vs_time.svg"] = (
        "Body-frame angular velocity components omega_1, omega_2, omega_3 for a torque-free "
        "asymmetric top (principal moments 1, 2, 3) from Euler's equations. They trade "
        "amplitude periodically while |L|^2 and the kinetic energy 2T stay constant.")

    # Fig 2 — polhodes: omega-space orbits at fixed |L|^2, swept over energy 2T.
    L2fix = 6.0
    Amat = np.array([[I[0], I[2]], [I[0] ** 2, I[2] ** 2]])    # solve for start in omega2 = 0 plane
    energies = sorted(list(np.linspace(2.2, 5.8, 11)) + [3.0])
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    lab_done = {"axis1": False, "axis3": False, "sep": False}
    for E2 in energies:
        a, b = np.linalg.solve(Amat, [E2, L2fix])             # a = omega1^2, b = omega3^2
        if a < 0 or b < 0:
            continue
        _, wsorb = integrate_euler(I, (math.sqrt(a), 0.0, math.sqrt(b)), 0.0, 9.0, 3000)
        Wo = np.array(wsorb)
        w1, w3 = Wo[:, 0], Wo[:, 2]
        if abs(E2 - 3.0) < 0.02:
            col, lw, key, lab = FLOW, 2.2, "sep", "separatrix (intermediate axis)"
        elif E2 > 3.0:
            col, lw, key, lab = INK, 1.1, "axis1", "polhode about axis 1"
        else:
            col, lw, key, lab = STEEL, 1.1, "axis3", "polhode about axis 3"
        for sx in (1.0, -1.0):
            for sz in (1.0, -1.0):
                ax.plot(sx * w1, sz * w3, color=col, lw=lw,
                        label=(lab if not lab_done[key] else None))
                lab_done[key] = True
    c1, c3 = math.sqrt(L2fix) / I[0], math.sqrt(L2fix) / I[2]
    ax.plot([c1, -c1], [0, 0], "o", color=ALT, ms=6)
    ax.plot([0, 0], [c3, -c3], "o", color=ALT, ms=6)
    ax.plot(0, 0, "x", color="#444444", ms=8, mew=2)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$\omega_1$")
    ax.set_ylabel(r"$\omega_3$")
    ax.set_title(r"Polhodes (fixed $|L|^2$): stable spin about axes 1 and 3")
    ax.legend(loc="upper right", fontsize=8.5, frameon=False)
    _save(fig, "fig2_polhode.svg")
    caps["fig2_polhode.svg"] = (
        "Polhodes: torque-free omega-space orbits at fixed |L|^2, projected on the "
        "omega_1-omega_3 plane. Closed loops circle the extreme principal axes 1 (blue) and "
        "3 (slate) -- stable spin -- while the orange separatrix through the centre marks the "
        "unstable intermediate axis 2 (the tennis-racket theorem).")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
