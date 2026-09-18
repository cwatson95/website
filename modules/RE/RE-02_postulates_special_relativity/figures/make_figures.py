"""RE-02 figures — the two postulates: a light-cone spacetime diagram with the
radar (Bondi) construction of a distant event, and the relativity of simultaneity.

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
from postulates import (                           # noqa: E402
    radar_coordinates, simultaneity_breakdown, gamma,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — postulate 2 (c is universal): a light cone at 45 deg, and the radar
    # method placing a distant event from a single clock + light echoes.
    t_send, t_echo = 1.0, 5.0
    t_ev, x_ev = radar_coordinates(t_send, t_echo)         # -> (3.0, 2.0)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    cone = np.array([-3.5, 3.5])
    ax.plot(cone, cone, color=STEEL, lw=1.2, ls="--")
    ax.plot(cone, -cone, color=STEEL, lw=1.2, ls="--", label="light cone $ct=\\pm x$")
    ax.axvline(0, color=INK, lw=2, label="observer worldline $x=0$")
    # outgoing pulse (emit at t_send) and returning echo (received at t_echo)
    ax.plot([0, x_ev], [t_send, t_ev], color=FLOW, lw=2, label="light out / back")
    ax.plot([x_ev, 0], [t_ev, t_echo], color=FLOW, lw=2)
    ax.scatter([0, 0], [t_send, t_echo], color=INK, zorder=5, s=30)
    ax.scatter([x_ev], [t_ev], color=ALT, zorder=5, s=45)
    ax.annotate(r"event $(ct,x)=(%.0f,%.0f)$" % (t_ev, x_ev), (x_ev, t_ev),
                textcoords="offset points", xytext=(6, -2), color=ALT, fontsize=9)
    ax.annotate("emit @%.0f" % t_send, (0, t_send), textcoords="offset points",
                xytext=(-78, -4), fontsize=9)
    ax.annotate("echo @%.0f" % t_echo, (0, t_echo), textcoords="offset points",
                xytext=(-78, -4), fontsize=9)
    ax.set_xlim(-3.5, 4.5); ax.set_ylim(-1.0, 6.0)
    ax.set_xlabel("space $x$"); ax.set_ylabel("time $ct$")
    ax.set_title("Radar method: light at $45^{\\circ}$ locates an event")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    _save(fig, "fig1_lightcone_radar.svg")
    caps["fig1_lightcone_radar.svg"] = (
        "Spacetime diagram (x horizontal, ct vertical). Because c is the same for "
        "everyone, light always runs at 45 degrees (dashed cone). An observer on x=0 "
        "emits a pulse at ct=1 and receives its echo at ct=5; radar_coordinates places "
        "the reflecting event at the midpoint time ct=3, half the round trip away at x=2.")

    # Fig 2 — relativity of simultaneity: events simultaneous in S (dt=0) acquire a
    # time offset dt' = -gamma*beta*dx in S', growing with separation and speed.
    dx = np.linspace(0.0, 3.0, 200)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for beta, col in [(0.3, STEEL), (0.6, FLOW), (0.9, ALT)]:
        dtp = np.array([simultaneity_breakdown(beta, 0.0, d) for d in dx])
        ax.plot(dx, dtp, color=col, lw=2,
                label=r"$\beta=%.1f$  ($\gamma=%.2f$)" % (beta, gamma(beta)))
    ax.axhline(0, color="#cccccc", lw=0.6)
    ax.set_xlabel(r"spatial separation $\Delta x$ in $S$")
    ax.set_ylabel(r"time gap $\Delta t'$ in $S'$")
    ax.set_xlim(0, 3)
    ax.set_title(r"Simultaneous in $S$ ($\Delta t=0$) is not simultaneous in $S'$")
    ax.legend(loc="lower left", frameon=False)
    _save(fig, "fig2_simultaneity.svg")
    caps["fig2_simultaneity.svg"] = (
        "Two events that are simultaneous in frame S (Delta t = 0) but a distance Delta x "
        "apart are assigned a time gap Delta t' = -gamma*beta*Delta x in a frame S' moving "
        "at beta, computed by simultaneity_breakdown. The offset grows linearly with "
        "separation and with speed, so a shared 'now' cannot survive a boost.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
