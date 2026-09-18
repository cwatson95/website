"""QM-21 figures — the CHSH violation (Tsirelson bound) and entanglement turn-on.

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
from entanglement import (                         # noqa: E402
    singlet, chsh_from_angles, tsirelson_bound, lhv_deterministic_strategies,
    normalize, density_matrix, partial_trace, purity, concurrence,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — CHSH S swept through the equally-spaced geometry a,a',b,b' = 0,2φ,φ,3φ.
    # S(φ) is computed by the module's chsh_from_angles on the singlet; it pokes
    # above the local/hidden-variable bound (= max|S| over the 16 deterministic
    # strategies) and peaks exactly at the Tsirelson bound 2 sqrt2 at φ=45°.
    phi = np.linspace(0.0, 90.0, 600)
    S = np.array([chsh_from_angles(singlet(), 0.0, 2 * p, p, 3 * p) for p in phi])
    absS = np.abs(S)
    lhv_bound = float(np.max(np.abs(lhv_deterministic_strategies())))  # = 2
    Tb = tsirelson_bound()                                             # = 2 sqrt2
    p_opt = 45.0
    S_opt = abs(chsh_from_angles(singlet(), 0.0, 2 * p_opt, p_opt, 3 * p_opt))

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.fill_between(phi, lhv_bound, absS, where=absS > lhv_bound,
                    color=INK, alpha=0.13, label="quantum violation")
    ax.plot(phi, absS, color=INK, lw=2.2, label=r"singlet $|S(\phi)|$")
    ax.axhline(lhv_bound, color=FLOW, lw=1.8, ls="--",
               label=r"classical / LHV bound $|S|=2$")
    ax.axhline(Tb, color=ALT, lw=1.8, ls="--",
               label=r"Tsirelson bound $2\sqrt{2}$")
    ax.plot(p_opt, S_opt, "o", ms=6, color=INK)
    ax.annotate(r"$|S|=2\sqrt{2}$", xy=(p_opt, S_opt), xytext=(52, 2.55),
                color=INK, fontsize=10)
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 3.0)
    ax.set_xlabel(r"sweep angle $\phi$ (deg),  settings $(a,a',b,b')=(0,2\phi,\phi,3\phi)$")
    ax.set_ylabel(r"$|S|$")
    ax.set_title(r"CHSH: the singlet beats the classical bound, capped at $2\sqrt{2}$")
    ax.legend(loc="lower center", frameon=False, fontsize=9, ncol=2)
    _save(fig, "fig1_chsh_violation.svg")
    caps["fig1_chsh_violation.svg"] = (
        r"CHSH $|S|$ for the singlet vs a single sweep angle $\phi$ (settings "
        r"$a,a',b,b'=0,2\phi,\phi,3\phi$), each point from chsh_from_angles. It "
        r"rises above the local-hidden-variable bound $|S|=2$ (orange, the max over "
        r"lhv_deterministic_strategies) across $0<\phi\lesssim68.5°$ and peaks "
        r"exactly at the Tsirelson bound $2\sqrt2\approx2.828$ at $\phi=45°$ — "
        r"quantum mechanics violates Bell but cannot exceed $2\sqrt2$.")

    # Fig 2 — entanglement turn-on: |psi(θ)> = cosθ|00> + sinθ|11>.  The module's
    # concurrence rises 0->1 while the reduced-state purity Tr(rho_A^2) falls 1->1/2,
    # i.e. "entangled <=> the reduced state goes mixed".  Endpoints are products,
    # the middle (θ=45°) is the maximally-entangled Bell state |Phi+>.
    th = np.linspace(0.0, 90.0, 400)
    C = np.empty_like(th)
    pur = np.empty_like(th)
    for i, t in enumerate(np.radians(th)):
        psi = normalize(np.array([np.cos(t), 0.0, 0.0, np.sin(t)], dtype=complex))
        C[i] = concurrence(psi)
        pur[i] = purity(partial_trace(density_matrix(psi), keep=0))

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(th, C, color=INK, lw=2.2, label=r"concurrence $C=2|ad-bc|$")
    ax.plot(th, pur, color=FLOW, lw=2.2,
            label=r"reduced purity $\mathrm{Tr}(\rho_A^2)$")
    ax.axhline(0.5, color=STEEL, lw=1.0, ls=":")
    ax.axvline(45, color="#999999", lw=0.8, ls=":")
    ax.plot(45, 1.0, "o", ms=5, color=INK)
    ax.plot(45, 0.5, "o", ms=5, color=FLOW)
    ax.annotate("product\n$|00\\rangle$", xy=(2, 0.86), color=ALT, fontsize=9)
    ax.annotate(r"Bell $|\Phi^+\rangle$ (max. entangled)", xy=(46, 0.78),
                color=INK, fontsize=9)
    ax.annotate("product\n$|11\\rangle$", xy=(78, 0.86), color=ALT, fontsize=9)
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 1.08)
    ax.set_xlabel(r"mixing angle $\theta$ (deg)")
    ax.set_ylabel(r"concurrence  /  reduced purity")
    ax.set_title(r"Entangled $\Leftrightarrow$ reduced state mixed:  $|\psi\rangle=\cos\theta\,|00\rangle+\sin\theta\,|11\rangle$")
    ax.legend(loc="center right", frameon=False, fontsize=9)
    _save(fig, "fig2_entanglement_turnon.svg")
    caps["fig2_entanglement_turnon.svg"] = (
        r"Entanglement turn-on for $|\psi(\theta)\rangle=\cos\theta|00\rangle+"
        r"\sin\theta|11\rangle$: concurrence (blue) from concurrence() and the "
        r"reduced-state purity $\mathrm{Tr}(\rho_A^2)$ (orange) from "
        r"purity(partial_trace(...)). As $C$ climbs $0\to1$ the purity falls "
        r"$1\to\tfrac12$ — the product endpoints ($\theta=0,90°$, $\rho_A$ pure) "
        r"give way to the maximally-entangled Bell state $|\Phi^+\rangle$ at "
        r"$\theta=45°$, whose reduced state is the maximally mixed $\mathbb I/2$.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
