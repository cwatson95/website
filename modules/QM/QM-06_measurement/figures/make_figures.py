"""QM-06 figures — the spin-1/2 projection (Malus) law from the generalized
statistical interpretation, and collapse / disturbance in a sequential
Stern-Gerlach cascade.

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
from measurement import (                          # noqa: E402
    spin_state, outcome_probabilities, expectation, measure, index_of, Sx, Sz,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the generalized statistical interpretation, computed: a spin-1/2
    # tilted by theta (spin_state) measured with a z Stern-Gerlach magnet.
    # outcome_probabilities gives P(+/- hbar/2) = cos^2/sin^2(theta/2); expectation
    # gives <S_z> = (hbar/2) cos theta -- the projection ("Malus") law.
    th = np.linspace(0.0, 2.0 * np.pi, 361)
    iup, idn = index_of(Sz, +0.5), index_of(Sz, -0.5)
    Pup, Pdn, Sz_exp = [], [], []
    for t in th:
        psi = spin_state(t)
        _, probs = outcome_probabilities(psi, Sz)
        Pup.append(probs[iup]); Pdn.append(probs[idn])
        Sz_exp.append(expectation(psi, Sz))
    deg = np.degrees(th)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(deg, Pup, color=INK, lw=2, label=r"$P(+\hbar/2)=\cos^2(\theta/2)$")
    ax.plot(deg, Pdn, color=FLOW, lw=2, label=r"$P(-\hbar/2)=\sin^2(\theta/2)$")
    ax.plot(deg, Sz_exp, color=ALT, lw=2, ls="--",
            label=r"$\langle S_z\rangle/\hbar=\frac{1}{2}\cos\theta$")
    ax.axhline(0.0, color="#aaaaaa", lw=0.6)
    ax.set_xlim(0, 360); ax.set_xticks([0, 90, 180, 270, 360])
    ax.set_ylim(-0.62, 1.08)
    ax.set_xlabel(r"tilt angle $\theta$ of the prepared spin (degrees)")
    ax.set_ylabel(r"probability  /  $\langle S_z\rangle/\hbar$")
    ax.set_title(r"Statistical interpretation: $P(a_n)=|\langle a_n|\psi\rangle|^2$")
    ax.legend(loc="lower center", frameon=False, fontsize=8.5, ncol=2)
    _save(fig, "fig1_spin_projection.svg")
    caps["fig1_spin_projection.svg"] = (
        "The generalized statistical interpretation, computed: a spin-1/2 prepared "
        "at tilt theta (spin_state), measured with a z-oriented Stern-Gerlach "
        "magnet. outcome_probabilities returns P(+hbar/2)=cos^2(theta/2) and "
        "P(-hbar/2)=sin^2(theta/2) (the projection / 'Malus' law), and expectation "
        "gives <S_z>=(hbar/2)cos theta -- the same number two ways. theta=0 is "
        "spin-up with certainty, theta=180 spin-down, theta=90 a 50/50 split.")

    # Fig 2 — collapse and incompatibility (a sequential Stern-Gerlach cascade).
    # From |+x>, a first S_x measurement is certain (+hbar/2).  Measuring S_x again
    # (compatible) leaves it certain; slipping an S_z measurement in between (S_z
    # does not commute with S_x) collapses to |0> and randomizes the next S_x.
    plus_x = spin_state(np.pi / 2.0, 0.0)
    ipx, imx = index_of(Sx, +0.5), index_of(Sx, -0.5)
    _, stA = measure(plus_x, Sx, outcome=ipx)                       # S_x -> +
    _, pA = outcome_probabilities(stA, Sx)                          # measure S_x again
    _, stB1 = measure(plus_x, Sx, outcome=ipx)                      # S_x -> +
    _, stB2 = measure(stB1, Sz, outcome=index_of(Sz, +0.5))         # intervening S_z -> +
    _, pB = outcome_probabilities(stB2, Sx)                         # measure S_x again

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    groups = ["$S_x\\!\\to\\!S_x$\n(compatible)", "$S_x\\!\\to\\!S_z\\!\\to\\!S_x$\n(incompatible)"]
    xpos = np.array([0.0, 1.0]); w = 0.34
    Pplus = [pA[ipx], pB[ipx]]
    Pminus = [pA[imx], pB[imx]]
    ax.bar(xpos - w / 2, Pplus, w, color=INK, label=r"final $P(+\hbar/2)$")
    ax.bar(xpos + w / 2, Pminus, w, color=FLOW, label=r"final $P(-\hbar/2)$")
    for xp, pv in zip(xpos - w / 2, Pplus):
        ax.text(xp, pv + 0.02, f"{pv:.2f}", ha="center", fontsize=9)
    for xp, pv in zip(xpos + w / 2, Pminus):
        ax.text(xp, pv + 0.02, f"{pv:.2f}", ha="center", fontsize=9)
    ax.set_xticks(xpos); ax.set_xticklabels(groups, fontsize=9)
    ax.set_xlim(-0.6, 1.6); ax.set_ylim(0, 1.18)
    ax.set_ylabel(r"probability of the re-measured $S_x$")
    ax.set_title("Collapse: an intervening incompatible measurement disturbs")
    ax.legend(loc="upper center", frameon=False, fontsize=9, ncol=2)
    _save(fig, "fig2_sequential_measurement.svg")
    caps["fig2_sequential_measurement.svg"] = (
        "Collapse and incompatibility, the Stern-Gerlach cascade (measure / "
        "collapse / outcome_probabilities). Starting from |+x>, a first S_x reading "
        "is +hbar/2 for certain. LEFT: measuring S_x again (compatible with itself) "
        "leaves it certain, P(+)=1. RIGHT: slipping an S_z measurement in between "
        "(S_z does NOT commute with S_x) collapses the state to |0> and randomizes "
        "the next S_x to 50/50 -- the act of measuring disturbs the system.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
