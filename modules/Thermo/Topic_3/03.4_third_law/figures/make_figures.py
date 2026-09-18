"""Module 3.4 figures — the Debye heat capacity that lets the entropy integral
converge to S(0)=0, and the unattainability of absolute zero.

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
from third_law import (                           # noqa: E402
    standard_entropy_at_zero, debye_cp, absolute_entropy,
    absolute_entropy_debye, carnot_cop_refrigerator,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — why the third law is consistent.  S(T) = int_0^T c_p/T' dT' would
    # diverge at the origin unless c_p vanishes there; the Debye T^3 law makes
    # the integrand c_p/T ~ aT^2 vanish too, so S(0) = 0 is reachable.  The
    # numerical quadrature is checked against the closed form.
    a = 1.0e-3                                      # J/(mol K^4)
    T = np.linspace(1.0, 60.0, 200)
    cp = np.array([debye_cp(t, a) for t in T])
    S_closed = np.array([absolute_entropy_debye(t, a) for t in T])
    S_num = np.array([absolute_entropy(t, lambda x: debye_cp(x, a)) for t in T[::12]])

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(T, cp, color=INK, lw=2.2, label=r"$c_p=aT^3$  (Debye limit)")
    ax.plot(T, S_closed, color=FLOW, lw=2.2, ls="--",
            label=r"$S(T)=\int_0^T\!c_p/T'\,dT'=aT^3/3$")
    ax.plot(T[::12], S_num, ls="none", marker="o", ms=6, mfc="white", mec=ALT,
            mew=1.7, label=r"absolute_entropy (numerical)")
    ax.plot([0], [standard_entropy_at_zero()], marker="*", ms=13, mfc=FLOW,
            mec=FLOW, ls="none", label=r"$S(0)=0$: the third law")
    ax.set_xlim(0, 60)
    ax.set_xlabel(r"temperature $T$ (K)")
    ax.set_ylabel(r"$c_p$ (J/mol$\cdot$K)   and   $S$ (J/mol$\cdot$K)")
    ax.set_title(r"Both $c_p$ and $S$ vanish as $T\rightarrow 0$")
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_debye_entropy.svg")
    caps["fig1_debye_entropy.svg"] = (
        r"The third law needs the heat capacity to die at the origin, and it "
        r"does. With the low-temperature Debye form $c_p=aT^3$ (debye_cp) the "
        r"entropy integrand $c_p/T=aT^2$ also vanishes, so "
        r"$S(T)=\int_0^Tc_p/T'\,dT'=aT^3/3$ converges to a finite value and can "
        r"be anchored at $S(0)=0$ for a pure crystalline solid "
        r"(standard_entropy_at_zero). The circles are the module's numerical "
        r"quadrature absolute_entropy, which lands on the closed form "
        r"absolute_entropy_debye. Had $c_p$ stayed finite at $T=0$, the integral "
        r"would diverge logarithmically and absolute entropies would not exist.")

    # Fig 2 — unattainability.  A reversible refrigerator's COP is the heat moved
    # per unit work; as the cold side approaches 0 K the COP collapses, so the
    # work needed to remove each further joule diverges.
    T_H = 300.0
    T_cold = np.linspace(1.0, 290.0, 400)
    cop = np.array([carnot_cop_refrigerator(t, T_H) for t in T_cold])
    work_per_J = 1.0 / cop                          # W per unit Q_C removed

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(T_cold, work_per_J, color=INK, lw=2.4,
            label=r"$W/Q_C=1/\beta_{max}=(T_H-T_C)/T_C$")
    ax.set_yscale("log")
    ax.set_xlim(0, 290)
    ax.set_xlabel(r"cold-side temperature $T_C$ (K)    ($T_H=300$ K)")
    ax.set_ylabel(r"work per joule removed (log scale)")
    ax.set_title(r"Absolute zero costs infinite work to reach")
    ax.set_ylim(2e-2, 3e3)
    for t, dy in ((100.0, 2.2), (10.0, 2.6), (1.0, 0.24)):
        y = 1.0 / carnot_cop_refrigerator(t, T_H)
        ax.plot([t], [y], marker="o", ms=7, mfc="white", mec=FLOW, mew=1.7,
                ls="none")
        ax.text(t + 16, y * dy, r"%g K: $%.0f\times$" % (t, y), fontsize=9,
                color="0.35", va="center")
    ax.legend(loc="lower left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6, which="both")
    _save(fig, "fig2_unattainability.svg")
    caps["fig2_unattainability.svg"] = (
        r"The practical face of the third law. Even a perfectly reversible "
        r"refrigerator has COP $\beta_{max}=T_C/(T_H-T_C)$ "
        r"(carnot_cop_refrigerator), so removing one joule from a body at $T_C$ "
        r"costs $(T_H-T_C)/T_C$ joules of work. Against a 300 K room that is "
        r"2 J at 100 K, "
        + "%.0f" % (1.0 / carnot_cop_refrigerator(10.0, T_H)) + r" J at 10 K and "
        + "%.0f" % (1.0 / carnot_cop_refrigerator(1.0, T_H)) + r" J at 1 K — the "
        r"cost diverges as $T_C\to0$. Absolute zero is not merely hard to reach; "
        r"reaching it in a finite number of steps is impossible, which is the "
        r"unattainability statement of the third law.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
