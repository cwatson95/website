"""NE-04 figures -- Q-values across reaction families, the electron-bookkeeping
trap, excited-state channels, and Coulomb barriers against Q.

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
from q_values import (                             # noqa: E402
    M_E_U, U_MEV, load_atomic_masses, atomic_mass, has_nuclide,
    q_value, q_value_reaction, q_value_excited, parse_reaction,
    coulomb_barrier_mev, format_nuclide,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    t = load_atomic_masses()

    # Fig 1 -- a bar chart of Q across reaction families.
    rxns = [
        ("3H(d,n)4He", "D-T fusion", LEAF),
        ("2H(d,n)3He", "D-D fusion", LEAF),
        ("6Li(n,a)3H", "tritium breeding", LEAF),
        ("9Be(a,n)12C", "neutron discovery", INK),
        ("10B(n,a)7Li", "neutron detection", INK),
        ("14N(n,p)14C", "cosmogenic 14C", INK),
        ("16O(n,a)13C", "endothermic", FLOW),
        ("16O(n,p)16N", "endothermic", FLOW),
    ]
    labels, vals, cols = [], [], []
    for rx, lab, col in rxns:
        labels.append("%s\n%s" % (rx, lab))
        vals.append(q_value_reaction(rx, t))
        cols.append(col)
    order = np.argsort(vals)[::-1]
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.barh([labels[i] for i in order], [vals[i] for i in order],
            color=[cols[i] for i in order])
    ax.axvline(0, color="k", lw=1.1)
    for y, i in enumerate(order):
        v = vals[i]
        ax.text(v + (0.4 if v > 0 else -0.4), y, "%+.2f" % v, va="center",
                ha="left" if v > 0 else "right", fontsize=8.5)
    ax.set_xlabel("$Q$ (MeV)")
    ax.set_xlim(-13, 21)
    ax.invert_yaxis()
    ax.tick_params(axis="y", labelsize=8)
    ax.set_title("Q-values: positive is exothermic")
    _save(fig, "fig1_q_value_survey.svg")
    caps["fig1_q_value_survey.svg"] = (
        "Q-values for eight reactions (q_value_reaction), sorted by magnitude. D-T fusion "
        "leads at +17.6 MeV because the 4He product is exceptionally tightly bound; the two "
        "(n,alpha) and (n,p) reactions on 16O are endothermic and cannot proceed below "
        "their thresholds.")

    # Fig 2 -- (n,gamma) Q along the actinides, against the fission barrier.
    fig, ax = plt.subplots(figsize=(6.4, 3.7))
    for Z, sym, col in [(92, "U", INK), (94, "Pu", FLOW)]:
        As, Qs = [], []
        for A in range(230, 246):
            if has_nuclide(A, Z, t) and has_nuclide(A + 1, Z, t):
                As.append(A)
                Qs.append(q_value([format_nuclide(A, Z), "n"],
                                  [format_nuclide(A + 1, Z), "g"], t))
        ax.plot(As, Qs, "o-", color=col, ms=5, lw=1.2, label=sym)
        for A, Q in zip(As, Qs):
            if (Z, A) in [(92, 235), (92, 238), (94, 239)]:
                ax.annotate("$^{%d}$%s" % (A, sym), xy=(A, Q), xytext=(A - 1.6, Q + 0.35),
                            fontsize=9, color=col)
    ax.axhspan(6.0, 6.4, color="0.85", zorder=0)
    ax.text(231, 6.15, "fission barrier ~6.2 MeV", fontsize=8.5, color="0.35")
    ax.set_xlabel("target mass number $A$")
    ax.set_ylabel(r"$Q$ of $(n,\gamma)$  (MeV)")
    ax.set_title("Neutron capture energy decides which nuclides are fissile")
    ax.legend(frameon=False, fontsize=9)
    _save(fig, "fig2_capture_q_actinides.svg")
    caps["fig2_capture_q_actinides.svg"] = (
        "Q-value of radiative capture (which equals the product's neutron separation "
        "energy) along the uranium and plutonium isotopes. Odd-A targets such as 235U and "
        "239Pu form even-N compound nuclei and gain the pairing energy, clearing the ~6.2 "
        "MeV fission barrier with a thermal neutron; even-A targets such as 238U fall short.")

    # Fig 3 -- excited-state channels close as E* rises.
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    r, p = parse_reaction("9Be(a,n)12C")
    ex = np.linspace(0, 10, 300)
    Q = [q_value_excited(r, p, float(e), t) for e in ex]
    ax.plot(ex, Q, color=INK, lw=1.8)
    ax.axhline(0, color="k", lw=1.0)
    ax.fill_between(ex, 0, Q, where=(np.array(Q) > 0), color=LEAF, alpha=0.18)
    ax.fill_between(ex, 0, Q, where=(np.array(Q) <= 0), color=FLOW, alpha=0.18)
    for e, lab in [(4.44, "first excited"), (7.65, "Hoyle state")]:
        ax.axvline(e, color="0.55", ls=":", lw=1.1)
        ax.annotate("%s\n%.2f MeV" % (lab, e), xy=(e, q_value_excited(r, p, e, t)),
                    xytext=(e - 0.2, 4.2), fontsize=8.5, color="0.3", ha="right")
    ax.set_xlabel(r"excitation energy $E^*$ of $^{12}$C (MeV)")
    ax.set_ylabel("$Q$ (MeV)")
    ax.set_title(r"$^{9}$Be$(\alpha,n)^{12}$C: each level is its own channel")
    _save(fig, "fig3_excited_channels.svg")
    caps["fig3_excited_channels.svg"] = (
        "Q-value of 9Be(alpha,n)12C as a function of the excitation left in the 12C product "
        "(q_value_excited). Q falls one-for-one with E*, so the ground-state channel is "
        "exothermic, the 4.44 MeV channel weakly so, and the 7.65 MeV Hoyle channel is "
        "closed until the incident alpha supplies another 1.95 MeV.")

    # Fig 4 -- Coulomb barrier vs Q for light-ion reactions.
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    pairs = [("3H(d,n)4He", (2, 1, 3, 1), "d+t"), ("2H(d,n)3He", (2, 1, 2, 1), "d+d"),
             ("9Be(a,n)12C", (4, 2, 9, 4), r"$\alpha$+$^{9}$Be"),
             ("6Li(n,a)3H", (1, 0, 6, 3), r"n+$^{6}$Li"),
             ("10B(n,a)7Li", (1, 0, 10, 5), r"n+$^{10}$B")]
    for rx, (A1, Z1, A2, Z2), lab in pairs:
        Q = q_value_reaction(rx, t)
        V = coulomb_barrier_mev(A1, Z1, A2, Z2)
        col = STEEL if Z1 == 0 else FLOW
        ax.plot([V], [Q], "o", color=col, ms=8)
        ax.annotate(lab, xy=(V, Q), xytext=(V + 0.08, Q + 0.6), fontsize=9, color=col)
    ax.axvline(0, color="0.6", lw=1.0, ls="--")
    ax.text(0.03, 16.5, "neutrons: no barrier", fontsize=9, color=STEEL)
    ax.set_xlabel("Coulomb barrier $V_c$ (MeV)")
    ax.set_ylabel("$Q$ (MeV)")
    ax.set_xlim(-0.2, 3.4)
    ax.set_ylim(0, 20)
    ax.set_title("Energy released against energy needed to get in")
    _save(fig, "fig4_barrier_vs_q.svg")
    caps["fig4_barrier_vs_q.svg"] = (
        "Q-value against Coulomb barrier (coulomb_barrier_mev) for five exothermic "
        "reactions. Neutron-induced reactions sit on the zero-barrier axis and proceed at "
        "thermal energies, which is why reactors are built around neutrons; the "
        "charged-particle reactions release just as much energy but must first be pushed "
        "over an MeV-scale barrier.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
