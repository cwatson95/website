"""QO-03 figures — laser threshold turn-on & the g^(2)(0) coherence landscape.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
"""
import json
import os
import sys
from math import lgamma

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"      # text as vector paths (portable, no font dep)
matplotlib.rcParams["font.size"] = 11
import matplotlib.pyplot as plt                    # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from emission_coherence import (                   # noqa: E402
    laser_threshold, laser_steady_state,
    g2_thermal, g2_coherent, g2_fock, g2_from_distribution,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — laser threshold: photon turn-on and gain clamping.
    # Steady (N, n) computed by the module's own laser_steady_state across a pump
    # sweep; R_th from laser_threshold.  Below R_th the pump only builds inversion
    # (n=0, N=R/gamma); above it the inversion clamps at kappa/G and every extra
    # pump quantum becomes a laser photon — the order-parameter turn-on of a
    # second-order phase transition.
    g, kappa, gamma = 1.0, 1.0, 1.0
    Rth = laser_threshold(g, kappa, gamma)
    R = np.linspace(0.0, 4.0, 400)
    N = np.array([laser_steady_state(r, g, kappa, gamma)[0] for r in R])
    n = np.array([laser_steady_state(r, g, kappa, gamma)[1] for r in R])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.axvspan(0.0, Rth, color="#eeeeee", zorder=0)
    ax.plot(R, n, color=INK, lw=2.2, label=r"photon number $n$")
    ax.plot(R, N, color=FLOW, lw=2.2, label=r"inversion $N$")
    ax.axhline(kappa / g, color=FLOW, lw=1.0, ls=":",
               label=r"clamp $N_{th}=\kappa/G$")
    ax.axvline(Rth, color="#888888", lw=1.0, ls="--")
    ax.annotate(r"$R_{th}=\gamma\kappa/G$", xy=(Rth, 0.06), xytext=(Rth + 0.12, 0.18),
                color="#555555", fontsize=9)
    ax.text(0.5, 1.55, "below:\ndark", ha="center", color="#777777", fontsize=9)
    ax.set_xlim(0, 4); ax.set_ylim(0, 3.1)
    ax.set_xlabel(r"pump rate $R$"); ax.set_ylabel("steady-state value")
    ax.set_title(r"Laser threshold: photon turn-on, inversion clamps ($G{=}\kappa{=}\gamma{=}1$)")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig1_laser_threshold.svg")
    caps["fig1_laser_threshold.svg"] = (
        "Single-mode laser steady state vs pump rate R from laser_steady_state "
        "(G=kappa=gamma=1, so R_th=1). Below threshold (shaded) the photon number "
        "n=0 and the pump only builds inversion N=R/gamma; above it the gain clamps "
        "the inversion at N_th=kappa/G=1 and n rises linearly, (R-R_th)/kappa — the "
        "order-parameter turn-on of a second-order phase transition.")

    # Fig 2 — the g^(2)(0) coherence landscape: bunching / coherent / antibunching.
    # Curve = g2_fock(n)=1-1/n (the module's closed form); open markers = the SAME
    # numbers recomputed by g2_from_distribution on Fock delta-distributions, to
    # show the operational <n(n-1)>/<n>^2 definition agrees.  Reference lines:
    # g2_thermal()=2 and g2_coherent()=1, each pinned by g2_from_distribution on a
    # Bose-Einstein and a Poisson distribution.  Shaded g^(2)<1 = nonclassical.
    nn = np.arange(1, 13)
    g2_curve = np.array([g2_fock(int(k)) for k in nn])
    g2_markers = []
    for k in nn:
        p = np.zeros(int(k) + 1)
        p[int(k)] = 1.0                              # Fock |k>
        g2_markers.append(g2_from_distribution(p))
    g2_markers = np.array(g2_markers)

    # validate the two reference lines against photon-number distributions
    m = np.arange(400)
    nbar = 2.0
    p_th = nbar ** m / (1.0 + nbar) ** (m + 1)        # Bose-Einstein (thermal)
    p_co = np.exp(-nbar + m * np.log(nbar)            # Poisson (coherent)
                  - np.array([lgamma(int(k) + 1) for k in m]))
    g2_th = g2_from_distribution(p_th)
    g2_co = g2_from_distribution(p_co)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.axhspan(-0.15, 1.0, color="#f0eaf0", zorder=0)
    ax.text(8.4, 0.12, r"nonclassical: $g^{(2)}(0)<1$", color=ALT, fontsize=9)
    ax.axhline(g2_th, color=FLOW, lw=2, ls="--",
               label=fr"thermal / chaotic $=2$  (bunching; via dist. ${g2_th:.3f}$)")
    ax.axhline(g2_co, color=STEEL, lw=2, ls="--",
               label=fr"coherent / laser $=1$  (Poisson; via dist. ${g2_co:.3f}$)")
    ax.plot(nn, g2_curve, color=INK, lw=2, marker="o", ms=5,
            label=r"Fock $|n\rangle$: $g^{(2)}(0)=1-\frac{1}{n}$")
    ax.plot(nn, g2_markers, ls="none", marker="o", ms=9, mfc="none",
            mec=ALT, mew=1.4, label=r"$\langle n(n{-}1)\rangle/\langle n\rangle^2$ (g2_from_distribution)")
    ax.plot([1], [g2_fock(1)], marker="*", ms=15, color="#c0392b", ls="none")
    ax.annotate(r"single photon $|1\rangle$: $g^{(2)}(0)=0$", xy=(1, 0.0),
                xytext=(1.6, 0.30), color="#c0392b", fontsize=9,
                arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.0))
    ax.set_xlim(0.5, 12.5); ax.set_ylim(-0.15, 2.25)
    ax.set_xlabel(r"Fock-state photon number $n$"); ax.set_ylabel(r"$g^{(2)}(0)$")
    ax.set_title(r"Second-order coherence: bunching, coherent, antibunching")
    ax.legend(loc="center right", frameon=False, fontsize=8.5)
    _save(fig, "fig2_g2_coherence.svg")
    caps["fig2_g2_coherence.svg"] = (
        "The g^(2)(0) landscape that classifies light. Blue curve: g2_fock(n)=1-1/n; "
        "open circles: the same values recomputed by g2_from_distribution as "
        "<n(n-1)>/<n>^2 on Fock |n> distributions (they agree). Dashed lines mark "
        "g2_thermal()=2 (bunching) and g2_coherent()=1 (Poissonian), each reproduced "
        "by g2_from_distribution on Bose-Einstein and Poisson statistics. The shaded "
        "g^(2)(0)<1 band is impossible classically; the single photon |1> sits at 0 — "
        "perfect antibunching.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
