"""QO-01 figures — photon statistics & quadrature noise of classical vs quantized light.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
"""
import json
import math
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
from quantized_light import (                       # noqa: E402
    coherent_state, fock_state, photon_distribution,
    mean_n, var_n, mandel_q, quadrature_variance,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    N = 60          # Fock-basis truncation; exact for n << N
    caps = {}

    # Fig 1 — photon-number distribution P(n): the "most classical" coherent state
    # (Poissonian) vs the "most quantum" Fock state, at the SAME mean <n> = 4.
    # Bars are computed by photon_distribution() on the module's own states.
    nmax = 13
    n = np.arange(nmax)
    alpha = 2.0                                   # |alpha|^2 = 4
    coh = coherent_state(alpha, N)
    fock = fock_state(4, N)                       # same mean photon number, sharp
    P_coh = photon_distribution(coh)[:nmax]
    P_fock = photon_distribution(fock)[:nmax]
    # closed-form Poisson check, e^{-<n>} <n>^n / n!, overlaid on the coherent bars
    nbar = abs(alpha) ** 2
    poisson = np.exp(-nbar) * nbar ** n / np.array([math.factorial(int(k)) for k in n])
    # Mandel Q from the module (clean the ~1e-9 float noise for the coherent label)
    q_coh = mandel_q(coh)
    q_coh = 0.0 if abs(q_coh) < 1e-6 else q_coh
    q_fock = mandel_q(fock)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    w = 0.42
    ax.bar(n - w / 2, P_coh, width=w, color=INK,
           label=fr"coherent $|\alpha\rangle$: $\langle n\rangle={mean_n(coh):.2f}$,"
                 fr" $\Delta n={np.sqrt(var_n(coh)):.2f}$, $Q={q_coh:.2f}$")
    ax.bar(n + w / 2, P_fock, width=w, color=FLOW,
           label=fr"Fock $|4\rangle$: $\langle n\rangle=4$, $\Delta n=0$, $Q={q_fock:.2f}$")
    ax.plot(n - w / 2, poisson, ls="none", marker="o", ms=4,
            mfc="none", mec=STEEL, label=r"Poisson $e^{-\langle n\rangle}\langle n\rangle^n/n!$")
    ax.set_xticks(n)
    ax.set_xlim(-0.7, nmax - 0.3)
    ax.set_xlabel(r"photon number $n$")
    ax.set_ylabel(r"$P(n)=|\langle n|\psi\rangle|^2$")
    ax.set_title(r"Photon statistics: coherent (Poissonian, $Q=0$) vs Fock (sharp, $Q=-1$)")
    ax.legend(loc="upper right", frameon=False, fontsize=8.5)
    _save(fig, "fig1_photon_statistics.svg")
    caps["fig1_photon_statistics.svg"] = (
        r"Photon-number distribution $P(n)$ from photon_distribution() for a coherent "
        r"state $|\alpha\rangle$ ($\alpha=2$, blue) and a Fock state $|4\rangle$ "
        r"(orange) of the SAME mean $\langle n\rangle=4$. The coherent bars match the "
        r"closed-form Poisson $e^{-\langle n\rangle}\langle n\rangle^n/n!$ (circles) "
        r"with $\Delta n=\sqrt{\langle n\rangle}$ and Mandel $Q=0$ — the 'most "
        r"classical' light — while the Fock state is a single sharp spike, $\Delta n=0$, "
        r"$Q=-1$ (sub-Poissonian, nonclassical).")

    # Fig 2 — quadrature variance vs mean photon number: number-phase complementarity.
    # Var X = Var P computed by quadrature_variance() on the module's own states.
    # Coherent / vacuum sit on the 1/4 minimum-uncertainty floor; Fock |n> rises as
    # (2n+1)/4 -- a SHARP photon number is paid for with large quadrature (phase) noise.
    n_fock = np.arange(0, 9)
    varx_fock = np.array([quadrature_variance(fock_state(int(k), N))[0] for k in n_fock])
    n_targets = np.arange(1, 9)
    alphas = np.sqrt(n_targets.astype(float))     # |alpha|^2 = target mean
    coh_states = [coherent_state(a, N) for a in alphas]
    coh_mean = np.array([mean_n(s) for s in coh_states])
    coh_varx = np.array([quadrature_variance(s)[0] for s in coh_states])
    nn = np.linspace(0, 8, 200)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(nn, (2 * nn + 1) / 4, color=INK, lw=2,
            label=r"Fock $|n\rangle$:  $\mathrm{Var}\,X=\frac{2n+1}{4}$")
    ax.plot(n_fock, varx_fock, ls="none", marker="o", ms=6, color=INK)
    ax.axhline(0.25, color=ALT, lw=1.6, ls="--",
               label=r"vacuum / coherent floor $=\frac{1}{4}$ (min. uncertainty)")
    ax.plot(coh_mean, coh_varx, ls="none", marker="s", ms=6, color=FLOW,
            label=r"coherent $|\alpha\rangle$ (computed)")
    ax.annotate(r"vacuum $|0\rangle$", xy=(0, 0.25), xytext=(0.5, 0.95),
                fontsize=9, color=ALT,
                arrowprops=dict(arrowstyle="->", color=ALT, lw=1))
    ax.set_xlim(-0.3, 8.3)
    ax.set_ylim(0, 4.6)
    ax.set_xlabel(r"mean photon number $\langle n\rangle$")
    ax.set_ylabel(r"quadrature variance $\mathrm{Var}\,X=\mathrm{Var}\,P$")
    ax.set_title(r"Number-phase complementarity: sharp-$n$ Fock states are noisy in quadrature")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig2_quadrature_noise.svg")
    caps["fig2_quadrature_noise.svg"] = (
        r"Quadrature variance $\mathrm{Var}\,X=\mathrm{Var}\,P$ from "
        r"quadrature_variance() vs mean photon number. Coherent states (orange "
        r"squares) and the vacuum all sit on the minimum-uncertainty floor "
        r"$\tfrac14$, while Fock states $|n\rangle$ (blue) climb as $\frac{2n+1}{4}$: "
        r"a perfectly sharp photon number ($\Delta n=0$) is paid for with large, "
        r"isotropic quadrature (phase) noise — number-phase complementarity. The "
        r"irreducible $\tfrac14$ is the field's zero-point fluctuation.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
