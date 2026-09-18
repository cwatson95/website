"""CM-06 figures — impulse builds momentum, and Newton's third law conserves total P.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
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
from linear_momentum import momentum, total_momentum, impulse  # noqa: E402

INK, FLOW, ALT, FOUR = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — a force pulse and the momentum it builds: impulse = area under F(t) = Delta p.
    Fmax, tc, sg = 6.0, 1.0, 0.25
    force = lambda t: (Fmax * math.exp(-((t - tc) / sg) ** 2), 0.0, 0.0)   # smooth kick
    ts = np.linspace(0.0, 2.0, 140)
    Fvals = [force(float(t))[0] for t in ts]
    p0 = 0.0
    pvals = [p0 + impulse(force, 0.0, float(t))[0] for t in ts]            # p(t) = p0 + integral F dt
    Jtot = impulse(force, 0.0, 2.0)[0]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.fill_between(ts, Fvals, color=FLOW, alpha=0.15)
    ax.plot(ts, Fvals, color=FLOW, lw=2, label=r"force $F(t)$ (N)")
    ax.plot(ts, pvals, color=INK, lw=2, label=r"momentum $p=p_0+\int F\,dt$")
    ax.axhline(Jtot, color=INK, ls=":", lw=1, label=fr"$\Delta p=J={Jtot:.2f}$ kg m/s")
    ax.set_xlabel("time $t$ (s)"); ax.set_ylabel("force (N) / momentum (kg m/s)")
    ax.set_title(r"Impulse-momentum theorem: $J=\int F\,dt=\Delta p$")
    ax.legend(loc="center right", frameon=False)
    _save(fig, "fig1_impulse_momentum.svg")
    caps["fig1_impulse_momentum.svg"] = (
        "A Gaussian force pulse F(t) (shaded) delivers impulse J = integral F dt, computed "
        "by the module's impulse(). The momentum p(t)=p0+J rises by exactly the shaded area "
        "and levels off once the force ends: the impulse-momentum theorem J = Delta p.")

    # Fig 2 — Newton's third law: equal & opposite internal forces conserve total P.
    m1, m2 = 2.0, 3.0
    f12 = lambda t: (5.0 * t, 0.0, 0.0)             # force on body 1
    f21 = lambda t: (-5.0 * t, 0.0, 0.0)            # reaction on body 2
    p1_0 = momentum(m1, (-1.0, 0.0, 0.0))[0]        # initial momenta (real function)
    p2_0 = momentum(m2, (1.0, 0.0, 0.0))[0]
    ts = np.linspace(0.0, 1.0, 100)
    p1 = [p1_0 + impulse(f12, 0.0, float(t))[0] for t in ts]
    p2 = [p2_0 + impulse(f21, 0.0, float(t))[0] for t in ts]
    Ptot = [a + b for a, b in zip(p1, p2)]
    P0 = total_momentum([m1, m2], [(-1.0, 0.0, 0.0), (1.0, 0.0, 0.0)])[0]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(ts, p1, color=INK, lw=2, label=r"$p_1$ (body 1)")
    ax.plot(ts, p2, color=FLOW, lw=2, label=r"$p_2$ (body 2)")
    ax.plot(ts, Ptot, color=ALT, lw=2, ls="--", label=r"$P=p_1+p_2$ (constant)")
    ax.axhline(P0, color="#aaaaaa", lw=0.6)
    ax.set_xlabel("time $t$ (s)"); ax.set_ylabel(r"momentum $p_x$ (kg m/s)")
    ax.set_title("Newton's third law: internal forces conserve total momentum")
    ax.legend(loc="center left", frameon=False)
    _save(fig, "fig2_momentum_conservation.svg")
    caps["fig2_momentum_conservation.svg"] = (
        "Two bodies exchange equal and opposite internal forces. Each momentum changes by "
        "its own impulse (p1 rises, p2 falls), but the total P = p1 + p2 from "
        "total_momentum() stays flat -- internal forces cannot change the total momentum.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
