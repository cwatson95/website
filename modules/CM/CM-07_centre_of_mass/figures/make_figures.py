"""CM-07 figures -- centre of mass of a multi-particle system, and reduced mass.

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
from centre_of_mass import centre_of_mass, reduced_mass   # noqa: E402

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- a drifting binary: each particle loops, but the CM (from the real
    # centre_of_mass) drifts in a straight inertial line. Internal forces cancel.
    m1, m2 = 3.0, 1.0                       # heavy + light particle
    M = m1 + m2
    V = np.array([1.0, 0.4])               # uniform CM drift velocity
    R0 = np.array([0.0, 0.0])
    D, Omega = 1.6, 2.4                     # separation and orbital rate of the pair
    t = np.linspace(0.0, 6.0, 700)

    p1 = np.zeros((len(t), 2)); p2 = np.zeros((len(t), 2)); cm = np.zeros((len(t), 2))
    for i, ti in enumerate(t):
        Rcm = R0 + V * ti                                   # where the CM "should" be
        rel = D * np.array([np.cos(Omega * ti), np.sin(Omega * ti)])   # relative vector
        r1 = Rcm + (m2 / M) * rel                           # split by mass weighting
        r2 = Rcm - (m1 / M) * rel
        p1[i], p2[i] = r1, r2
        # CM recovered from the real module function (3-vectors, z=0):
        Rc = centre_of_mass([m1, m2], [[r1[0], r1[1], 0.0], [r2[0], r2[1], 0.0]])
        cm[i] = [Rc[0], Rc[1]]

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(p1[:, 0], p1[:, 1], color=STEEL, lw=1.3, alpha=0.9, label=r"particle 1 ($m_1=3$)")
    ax.plot(p2[:, 0], p2[:, 1], color=ALT, lw=1.3, alpha=0.9, label=r"particle 2 ($m_2=1$)")
    ax.plot(cm[:, 0], cm[:, 1], color=INK, lw=2.4, label="centre of mass")
    ax.plot(p1[0, 0], p1[0, 1], "o", color=STEEL, ms=5)
    ax.plot(p2[0, 0], p2[0, 1], "o", color=ALT, ms=5)
    ax.plot(cm[0, 0], cm[0, 1], "o", color=INK, ms=5)
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title(r"CM of a drifting pair: $R=\frac{m_1 r_1+m_2 r_2}{m_1+m_2}$ stays inertial")
    ax.legend(loc="upper left", frameon=False)
    _save(fig, "fig1_cm_worldline.svg")
    caps["fig1_cm_worldline.svg"] = (
        "Two particles (mass 3 and 1) orbit each other while their system drifts. Each particle "
        "traces a looping path, but the centre of mass R = (m1 r1 + m2 r2)/(m1 + m2), computed by "
        "the module, moves in a straight line at constant velocity: internal forces cancel, so the "
        "CM behaves like a single free particle carrying the total mass.")

    # Fig 2 -- reduced mass mu(m1,m2)/m1 versus the mass ratio m2/m1 (real reduced_mass).
    ratio = np.logspace(-1.5, 2.5, 400)        # m2/m1 from ~0.03 to ~300
    mu = np.array([reduced_mass(1.0, q) for q in ratio])   # m1 = 1, so mu/m1 = mu
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(ratio, mu, color=FLOW, lw=2,
            label=r"$\mu=\frac{m_1 m_2}{m_1+m_2}$")
    ax.axhline(1.0, color="#aaaaaa", lw=0.8, ls="--")
    ax.axhline(0.5, color="#cccccc", lw=0.8, ls=":")
    ax.plot(1.0, 0.5, "o", color=INK, ms=6)
    ax.annotate(r"equal masses: $\mu=\frac{m_1}{2}$", xy=(1.0, 0.5),
                xytext=(1.6, 0.30), color=INK, fontsize=10,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1))
    ax.annotate(r"$\mu\to m_1$ (heavy partner)", xy=(120, 0.99),
                xytext=(4, 0.80), color=ALT, fontsize=10)
    ax.set_xscale("log")
    ax.set_xlabel(r"mass ratio $m_2/m_1$"); ax.set_ylabel(r"$\mu/m_1$")
    ax.set_ylim(0, 1.08)
    ax.set_title("Reduced mass: light for equal partners, saturates at the lighter mass")
    ax.legend(loc="lower right", frameon=False)
    _save(fig, "fig2_reduced_mass.svg")
    caps["fig2_reduced_mass.svg"] = (
        "Reduced mass mu = m1 m2/(m1 + m2) divided by m1, versus the mass ratio m2/m1 (log axis). "
        "For equal masses mu = m1/2; as the partner grows heavy mu saturates at the lighter mass m1. "
        "This is the effective mass of the two-body relative motion, used to reduce it to one body.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
