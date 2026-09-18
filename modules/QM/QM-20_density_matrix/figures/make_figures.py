"""QM-20 figures — purity/entropy along the pure->mixed axis, and the
entanglement signature of the partial trace (Bell vs product).

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
from density_matrix import (                       # noqa: E402
    density_matrix_pure, maximally_mixed, purity, von_neumann_entropy,
    expectation, partial_trace, tensor,
    plus, ket0, ket1, sigma_x,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the pure->mixed axis.  Depolarize |+> toward the maximally mixed
    # state: rho(lam) = lam |+><+| + (1-lam) I/2  (a convex combination, still a
    # valid state).  Everything is computed by the module's OWN routines: purity,
    # von_neumann_entropy, and the Bloch radius via expectation(rho, sigma_x).
    lam = np.linspace(0.0, 1.0, 41)
    pur = np.empty_like(lam)
    S = np.empty_like(lam)
    rblo = np.empty_like(lam)
    rho_mix = maximally_mixed(2)
    rho_plus = density_matrix_pure(plus)
    for i, L in enumerate(lam):
        rho = L * rho_plus + (1.0 - L) * rho_mix       # depolarized |+>
        pur[i] = purity(rho)
        S[i] = von_neumann_entropy(rho)
        # Bloch vector r = (<sx>,<sy>,<sz>); here it points along x with length lam
        rblo[i] = np.sqrt(sum(expectation(rho, s) ** 2
                              for s in (sigma_x,)))      # <sy>=<sz>=0 here
    lam_f = np.linspace(0.0, 1.0, 400)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.2, 4.7), sharex=True)
    # top: purity Tr(rho^2) and the Bloch radius r (both dimensionless, 0..1)
    ax1.plot(lam_f, 0.5 * (1.0 + lam_f ** 2), color=INK, lw=2,
             label=r"$\mathrm{Tr}(\rho^2)=\frac{1}{2}(1+\lambda^2)$")
    ax1.plot(lam, pur, ls="none", marker="o", ms=4, color=INK)
    ax1.plot(lam, rblo, color=STEEL, lw=2, label=r"Bloch radius $r=|\langle\vec\sigma\rangle|=\lambda$")
    ax1.axhline(0.5, color="#888888", lw=0.8, ls=":")
    ax1.axhline(1.0, color="#888888", lw=0.8, ls=":")
    ax1.set_ylim(0.35, 1.08)
    ax1.set_ylabel("purity / Bloch radius")
    ax1.set_title(r"Pure $\to$ mixed: depolarizing $|+\rangle$, $\rho=\lambda|+\rangle\langle+|+(1-\lambda)\frac{I}{2}$")
    ax1.legend(loc="center left", frameon=False, fontsize=9)
    ax1.annotate("pure", xy=(1.0, 1.0), xytext=(0.83, 0.62), color=INK, fontsize=9)
    ax1.annotate(r"$I/2$ (max mixed)", xy=(0.0, 0.5), xytext=(0.06, 0.40),
                 color=ALT, fontsize=9)
    # bottom: von Neumann entropy S(rho) in nats, capped by ln 2
    ax2.plot(lam, S, color=FLOW, lw=2, marker="o", ms=3,
             label=r"$S=-\mathrm{Tr}(\rho\ln\rho)$")
    ax2.axhline(np.log(2.0), color="#888888", lw=0.8, ls=":")
    ax2.annotate(r"$\ln 2$", xy=(0.02, np.log(2.0)), xytext=(0.02, 0.60),
                 color="#666666", fontsize=9)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(-0.03, 0.78)
    ax2.set_xlabel(r"mixing parameter $\lambda$  (1 = pure $|+\rangle$, 0 = maximally mixed)")
    ax2.set_ylabel(r"entropy $S$ (nats)")
    ax2.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_purity_entropy.svg")
    caps["fig1_purity_entropy.svg"] = (
        r"Depolarizing the qubit $|+\rangle$ toward $I/2$: "
        r"$\rho(\lambda)=\lambda|+\rangle\langle+|+(1-\lambda)\tfrac{I}{2}$, with every "
        r"quantity from the module's own routines. Top: purity $\mathrm{Tr}(\rho^2)$ "
        r"(dots) follows the closed form $\tfrac12(1+\lambda^2)$, falling from $1$ "
        r"(pure) to the floor $\tfrac12$ as the Bloch radius $r=|\langle\vec\sigma\rangle|=\lambda$ "
        r"(from expectation) shrinks to $0$. Bottom: the von Neumann entropy rises "
        r"the other way, $0\to\ln 2$ — one number, two faces of mixedness.")

    # Fig 2 — the entanglement signature of the partial trace.  Sweep
    # |psi(t)> = cos(t)|00> + sin(t)|11> from product (t=0) through the Bell state
    # |Phi+> (t=pi/4).  The whole is ALWAYS pure (S_global=0), yet the reduced
    # qubit rho_A = Tr_B rho becomes mixed -- maximally so at the Bell point.
    th = np.linspace(0.0, np.pi / 2, 121)
    SA = np.empty_like(th)
    purA = np.empty_like(th)
    Sglob = np.empty_like(th)
    e00 = tensor(ket0, ket0)
    e11 = tensor(ket1, ket1)
    for i, t in enumerate(th):
        psi = np.cos(t) * e00 + np.sin(t) * e11        # pure two-qubit ket
        rho = density_matrix_pure(psi)                 # global state (pure)
        rhoA = partial_trace(rho, [2, 2], keep=0)      # reduced qubit A
        SA[i] = von_neumann_entropy(rhoA)
        purA[i] = purity(rhoA)
        Sglob[i] = von_neumann_entropy(rho)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(th, SA, color=FLOW, lw=2,
            label=r"$S(\rho_A)$  (entanglement entropy)")
    ax.plot(th, purA, color=INK, lw=2, label=r"$\mathrm{Tr}(\rho_A^2)$  (subsystem purity)")
    ax.plot(th, Sglob, color=STEEL, lw=1.6, ls="--",
            label=r"$S(\rho_{AB})=0$  (whole stays pure)")
    ax.axhline(np.log(2.0), color="#888888", lw=0.8, ls=":")
    ax.axvline(np.pi / 4, color="#888888", lw=0.8, ls=":")
    ax.annotate(r"$\ln 2$", xy=(0.02, np.log(2.0)), xytext=(0.03, 0.60),
                color="#666666", fontsize=9)
    ax.annotate("product\n" + r"$|0\rangle|0\rangle$", xy=(0.0, 0.0),
                xytext=(0.04, 0.10), color=ALT, fontsize=9)
    ax.annotate(r"Bell $|\Phi^+\rangle$", xy=(np.pi / 4, np.log(2.0)),
                xytext=(np.pi / 4 - 0.36, 0.78), color=ALT, fontsize=9)
    ax.set_xlim(0, np.pi / 2)
    ax.set_ylim(-0.04, 0.92)
    ax.set_xticks([0, np.pi / 8, np.pi / 4, 3 * np.pi / 8, np.pi / 2])
    ax.set_xticklabels(["0", r"$\pi/8$", r"$\pi/4$", r"$3\pi/8$", r"$\pi/2$"])
    ax.set_xlabel(r"mixing angle $\theta$ in $|\psi\rangle=\cos\theta\,|00\rangle+\sin\theta\,|11\rangle$")
    ax.set_ylabel("entropy (nats) / purity")
    ax.set_title("Partial trace: an entangled whole has a mixed part")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_entanglement_partial_trace.svg")
    caps["fig2_entanglement_partial_trace.svg"] = (
        r"Tracing out one qubit of $|\psi(\theta)\rangle=\cos\theta|00\rangle+\sin\theta|11\rangle$ "
        r"with partial_trace. The two-qubit whole is pure throughout "
        r"($S(\rho_{AB})=0$, dashed), yet the reduced qubit $\rho_A$ is generally "
        r"mixed: its purity $\mathrm{Tr}(\rho_A^2)$ dips to $\tfrac12$ and its "
        r"entanglement entropy $S(\rho_A)$ peaks at $\ln 2$ exactly at $\theta=\pi/4$, "
        r"the Bell state $|\Phi^+\rangle$ (maximally entangled, $\rho_A=I/2$). At "
        r"$\theta=0$ the state is the product $|00\rangle$ and the part stays pure — "
        r"the operational signature of entanglement (bridge to QM-21).")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
