"""QF-03 figures — Yukawa->Coulomb as the photon mass vanishes, and the
gauge-invariance of the covariant derivative vs the bare derivative.

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
from gauge_theory import (                         # noqa: E402
    yukawa_to_coulomb, covariant_derivative, gauge_transform,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — one-boson-exchange potential V(r)=e^{-m r}/(4 pi r) from
    # yukawa_to_coulomb(): a massive mediator is short-range Yukawa; m -> 0 (the
    # massless photon) gives the long-range Coulomb tail 1/(4 pi r).
    r = np.linspace(0.12, 6.0, 500)
    coul = yukawa_to_coulomb(r, 0.0)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    masses = [(2.0, STEEL), (1.0, ALT), (0.3, FLOW)]
    for mm, col in masses:
        ax.plot(r, yukawa_to_coulomb(r, mm), color=col, lw=2,
                label=fr"$m={mm}$  (Yukawa $e^{{-mr}}/4\pi r$)")
    ax.plot(r, coul, color=INK, lw=2.4, ls="--",
            label=r"$m=0$  (Coulomb $1/4\pi r$)")
    ax.set_yscale("log")
    ax.set_xlim(0, 6)
    ax.set_xlabel(r"separation $r$")
    ax.set_ylabel(r"$V(r)$")
    ax.set_title(r"Massless photon $\Rightarrow$ long-range Coulomb: Yukawa $\to$ Coulomb as $m\to0$")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_yukawa_coulomb.svg")
    caps["fig1_yukawa_coulomb.svg"] = (
        r"One-boson-exchange potential $V(r)=e^{-mr}/4\pi r$ from "
        r"yukawa_to_coulomb(): a massive mediator gives the short-range Yukawa "
        r"potential that is exponentially cut off at $r\sim 1/m$, but as the mass "
        r"$m\to0$ the exponential $\to 1$ and $V\to$ the long-range Coulomb tail "
        r"$1/4\pi r$ (dashed). Gauge symmetry forbids a photon mass, so "
        r"electrostatics is exactly Coulombic.")

    # Fig 2 — minimal coupling restores gauge invariance.  On a 2-D lattice apply a
    # local phase psi -> e^{i s alpha} psi with paired shift A -> A - (1/e) d(s alpha),
    # for increasing amplitude s, and measure how much the modulus of the BARE
    # derivative (covariant_derivative with e=0) changes versus the COVARIANT
    # derivative (e=1).  Both come from the SAME real function.
    N, L = 96, 2.0 * np.pi
    dx = L / N
    xg = np.linspace(0.0, L, N, endpoint=False)
    X0, X1 = np.meshgrid(xg, xg, indexing="ij")
    A = np.stack([0.4 * np.sin(X1), 0.3 * np.cos(X0) + 0.2 * np.sin(2.0 * X1)])
    e = 1.0
    psi = (1.0 + 0.3 * np.cos(X0)) * np.exp(0.6j * np.sin(X1))
    alpha0 = 0.8 * np.cos(X0) * np.sin(X1)
    sl = (slice(None), slice(1, -1), slice(1, -1))      # interior (drop wrap edges)

    g0 = covariant_derivative(psi, A, 0.0, dx)          # e=0 -> bare d_mu psi
    D0 = covariant_derivative(psi, A, e, dx)            # e=1 -> covariant D_mu psi
    s_vals = np.linspace(0.1, 2.0, 24)
    chg_bare = np.empty_like(s_vals)
    chg_cov = np.empty_like(s_vals)
    for i, s in enumerate(s_vals):
        alpha = s * alpha0
        psi_g = np.exp(1j * alpha) * psi
        A_g = gauge_transform(A, -alpha / e, dx)        # A_mu - (1/e) d_mu(s alpha)
        g1 = covariant_derivative(psi_g, A_g, 0.0, dx)
        D1 = covariant_derivative(psi_g, A_g, e, dx)
        chg_bare[i] = np.max(np.abs(np.abs(g1) - np.abs(g0))[sl])
        chg_cov[i] = np.max(np.abs(np.abs(D1) - np.abs(D0))[sl])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(s_vals, chg_bare, color=FLOW, lw=2, marker="o", ms=3.5,
            label=r"bare $|\partial_\mu\psi|$  ($e=0$): $O(1)$ change")
    ax.plot(s_vals, chg_cov, color=INK, lw=2, marker="s", ms=3.5,
            label=r"covariant $|D_\mu\psi|$  ($e=1$): $O(dx^2)$ only")
    ax.set_yscale("log")
    ax.set_xlim(0, 2.05)
    ax.set_xlabel(r"gauge amplitude $s$  ($\alpha=s\,\alpha_0(x)$)")
    ax.set_ylabel(r"max change in derivative modulus")
    ax.set_title(r"Minimal coupling restores gauge invariance ($|D_\mu\psi|$ unchanged)")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    _save(fig, "fig2_covariant_derivative.svg")
    caps["fig2_covariant_derivative.svg"] = (
        r"Under a local phase rotation $\psi\to e^{i\alpha(x)}\psi$ with the paired "
        r"shift $A_\mu\to A_\mu-\tfrac1e\partial_\mu\alpha$ (gauge_transform), the "
        r"modulus of the bare derivative $|\partial_\mu\psi|$ changes by an $O(1)$ "
        r"amount that grows with the gauge amplitude, while the covariant derivative "
        r"$|D_\mu\psi|$ — the SAME covariant_derivative() with $e{=}1$ instead of "
        r"$e{=}0$ — is invariant down to the $O(dx^2)$ lattice error. Minimal "
        r"coupling $\partial_\mu\to D_\mu$ is what makes the matter sector gauge "
        r"invariant.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
