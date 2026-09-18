"""CM-03 figures — the same two-body event in the lab frame and the centre-of-mass frame.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
"""
import json
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
from reference_frames import (                     # noqa: E402
    cm_velocity, to_cm_frame, total_momentum, galilean_position,
)

INK, FLOW, ALT, FOUR = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    masses = [2.0, 1.0]
    x0 = [-4.0, 5.0]
    vels = [[1.5, 0.0, 0.0], [-2.0, 0.0, 0.0]]
    Vcm = cm_velocity(masses, vels)                # real function
    vcm_frame = to_cm_frame(masses, vels)          # velocities in the C-frame
    M = sum(masses)
    xcm0 = sum(m * x for m, x in zip(masses, x0)) / M
    ts = np.linspace(0.0, 4.0, 120)
    cols = [INK, FLOW]

    # Fig 1 — lab frame: two worldlines and the steadily drifting centre of mass.
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for i in range(2):
        xs = [x0[i] + vels[i][0] * float(t) for t in ts]
        ax.plot(xs, ts, color=cols[i], lw=2, label=fr"body {i + 1} (m={masses[i]:.0f})")
    ax.plot([xcm0 + Vcm[0] * float(t) for t in ts], ts, color=ALT, lw=2, ls="--",
            label=fr"CM ($V_{{cm}}={Vcm[0]:.2f}$ m/s)")
    ax.set_xlabel("position $x$ (m)"); ax.set_ylabel("time $t$ (s)")
    ax.set_title("Lab frame: the centre of mass drifts at constant velocity")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig1_lab_frame.svg")
    caps["fig1_lab_frame.svg"] = (
        "Worldlines x(t) of two bodies (m=2 and m=1) in the lab frame, with the "
        "centre-of-mass line from cm_velocity(). The CM drifts uniformly at V_cm = 0.33 "
        "m/s because no external force acts; the bodies move asymmetrically about it.")

    # Fig 2 — boost to the CM frame with galilean_position: CM at rest, total P = 0.
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for i in range(2):
        xs = [galilean_position([x0[i] + vels[i][0] * float(t), 0.0, 0.0], Vcm, float(t))[0]
              for t in ts]
        ax.plot(xs, ts, color=cols[i], lw=2,
                label=fr"body {i + 1} ($v'={vcm_frame[i][0]:+.2f}$ m/s)")
    xcm_p = [galilean_position([xcm0 + Vcm[0] * float(t), 0.0, 0.0], Vcm, float(t))[0]
             for t in ts]
    ax.plot(xcm_p, ts, color=ALT, lw=2, ls="--", label="CM (at rest)")
    Pcm = total_momentum(masses, vcm_frame)
    ax.set_xlabel(r"position $x'$ (m)"); ax.set_ylabel("time $t$ (s)")
    ax.set_title(r"CM frame: bodies converge on a stationary centre, $P'=0$")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig2_cm_frame.svg")
    caps["fig2_cm_frame.svg"] = (
        "The same event after a Galilean boost to the CM frame via galilean_position(): "
        "the centre of mass is now a vertical (stationary) worldline and the two bodies "
        f"carry equal and opposite momenta, so the total momentum is P' = {Pcm[0]:.0e} ~ 0.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
