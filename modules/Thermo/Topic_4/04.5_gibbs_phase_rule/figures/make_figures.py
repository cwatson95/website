"""Module 4.5 figures — the degrees of freedom F = 2 + N - P over the whole
(components, phases) grid, and what F means on a one-component phase diagram.

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
from gibbs_phase_rule import (                    # noqa: E402
    gibbs_phase_rule, single_component_dof, max_phases,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the rule over its whole domain.  Each cell is F = 2 + N - P; every
    # extra phase costs one degree of freedom, every extra component buys one
    # back.  Cells where F would go negative are impossible states of matter and
    # are struck out rather than coloured.
    Ns = np.arange(1, 5)
    Ps = np.arange(1, 7)
    F = np.array([[gibbs_phase_rule(int(n), int(p)) for n in Ns] for p in Ps])
    Fm = np.ma.masked_less(F, 0)

    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    cmap = plt.get_cmap("Purples").copy()
    cmap.set_bad("0.92")
    im = ax.imshow(Fm, cmap=cmap, vmin=0, vmax=5, origin="upper", aspect="auto")
    for i, p in enumerate(Ps):
        for j, n in enumerate(Ns):
            f = F[i, j]
            if f < 0:
                ax.text(j, i, "—", ha="center", va="center", fontsize=13,
                        color="0.55")
            else:
                ax.text(j, i, "%d" % f, ha="center", va="center", fontsize=12,
                        color="white" if f >= 3 else "0.2")
    ax.set_xticks(range(len(Ns)))
    ax.set_xticklabels(["N=%d" % n for n in Ns])
    ax.set_yticks(range(len(Ps)))
    ax.set_yticklabels(["P=%d" % p for p in Ps])
    ax.set_xlabel(r"number of components $N$")
    ax.set_ylabel(r"number of coexisting phases $P$")
    ax.set_title(r"Degrees of freedom  $F=2+N-P$")
    cb = fig.colorbar(im, ax=ax, pad=0.02)
    cb.set_label(r"$F$ (intensive variables you may still set)", fontsize=9)
    _save(fig, "fig1_phase_rule_grid.svg")
    caps["fig1_phase_rule_grid.svg"] = (
        r"The Gibbs phase rule $F=2+N-P$ (gibbs_phase_rule) tabulated over its "
        r"whole domain. Reading down a column, each additional coexisting phase "
        r"consumes one degree of freedom; reading across a row, each additional "
        r"component restores one. The struck-out cells are combinations with "
        r"$F<0$ — more phases than the system can support, which simply cannot "
        r"occur at equilibrium. The boundary is $P_{max}=N+2$ (max_phases): "
        + "%d" % max_phases(1) + r" phases for a pure substance, "
        + "%d" % max_phases(2) + r" for a binary mixture.")

    # Fig 2 — what F means on the p-T diagram of a pure substance.  Areas are
    # F=2 (choose p and T freely), the coexistence curves are F=1 (choose one,
    # the other follows) and the triple point is F=0 (no choice at all).
    fig, ax = plt.subplots(figsize=(6.2, 3.9))
    Tt, pt = 0.30, 0.22                             # schematic triple point
    T_fus = np.array([Tt, Tt - 0.035])
    p_fus = np.array([pt, 1.0])
    # exponents chosen so both curves stay inside the axes: an artist placed
    # outside the view is not clipped and would blow up the tight bounding box.
    T_vap = np.linspace(Tt, 0.86, 200)
    p_vap = pt * np.exp(2.55 * (T_vap - Tt))        # schematic Clausius-Clapeyron
    T_sub = np.linspace(0.02, Tt, 100)
    p_sub = pt * np.exp(11.0 * (T_sub - Tt))

    ax.plot(T_vap, p_vap, color=INK, lw=2.3)
    ax.plot(T_fus, p_fus, color=INK, lw=2.3)
    ax.plot(T_sub, p_sub, color=INK, lw=2.3)
    ax.plot([T_vap[-1]], [p_vap[-1]], marker="o", ms=8, mfc="white", mec=FLOW,
            mew=1.9, ls="none")
    ax.text(T_vap[-1] - 0.03, p_vap[-1] + 0.06, "critical point", fontsize=9,
            color="0.35", ha="right")
    ax.plot([Tt], [pt], marker="o", ms=9, mfc=FLOW, mec=FLOW, ls="none",
            zorder=5)

    ax.text(0.12, 0.70, "SOLID\n$P=1$, $F=%d$" % single_component_dof(1),
            ha="center", fontsize=9.5, color="0.25")
    ax.text(0.55, 0.72, "LIQUID\n$P=1$, $F=%d$" % single_component_dof(1),
            ha="center", fontsize=9.5, color="0.25")
    ax.text(0.62, 0.13, "VAPOUR\n$P=1$, $F=%d$" % single_component_dof(1),
            ha="center", fontsize=9.5, color="0.25")
    ax.annotate(r"coexistence curves: $P=2$, $F=%d$" % single_component_dof(2),
                xy=(0.52, p_vap[np.argmin(abs(T_vap - 0.52))]), xytext=(0.30, 0.90),
                fontsize=9, color=INK,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
    ax.annotate(r"triple point: $P=3$, $F=%d$" % single_component_dof(3),
                xy=(Tt, pt), xytext=(0.44, 0.30), fontsize=9, color=FLOW,
                arrowprops=dict(arrowstyle="->", color=FLOW, lw=1.1))
    ax.set_xlim(0, 0.95)
    ax.set_ylim(0, 1.05)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel(r"temperature $T$ $\rightarrow$")
    ax.set_ylabel(r"pressure $p$ $\rightarrow$")
    ax.set_title(r"One component ($N=1$): $F=3-P$")
    _save(fig, "fig2_single_component.svg")
    caps["fig2_single_component.svg"] = (
        r"What the phase rule looks like on the $p\!-\!T$ diagram of a pure "
        r"substance, where it reduces to $F=3-P$ (single_component_dof). In the "
        r"single-phase AREAS $F=2$: pressure and temperature may be varied "
        r"independently. On the melting, boiling and sublimation CURVES two "
        r"phases coexist and $F=1$ — fix the temperature and the pressure is no "
        r"longer yours to choose, which is exactly why a saturation table can be "
        r"indexed by either one alone. At the triple POINT three phases coexist, "
        r"$F=0$, and the state is completely pinned; that rigidity is what makes "
        r"the triple point of water a usable temperature standard. (Schematic — "
        r"the curves are illustrative, not to scale.)")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
