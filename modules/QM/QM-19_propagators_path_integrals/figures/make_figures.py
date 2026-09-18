"""QM-19 figures — the propagator in action (evolving a packet) and built from paths.

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
from propagator import (                           # noqa: E402
    gaussian_packet, propagate, evolve_free_spectral, packet_center_width,
    path_integral_euclidean, harmonic_propagator_euclidean,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # ------------------------------------------------------------------ Fig 1
    # The free propagator evolves a Gaussian packet: Psi(x,t) = int K0 Psi0 dx'.
    # Snapshots come from the module's `propagate` (the propagator integral);
    # the open markers are an INDEPENDENT split-step FFT (`evolve_free_spectral`)
    # — two unrelated algorithms landing on the same state.
    xs = np.linspace(-45, 45, 2000)
    x0, p0, sigma = -8.0, 2.0, 1.0                  # drift right at v = p0/m = 2
    psi0 = gaussian_packet(xs, x0=x0, p0=p0, sigma=sigma)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    maxdiff = 0.0
    for t, col in [(0.0, INK), (4.0, ALT), (8.0, FLOW)]:
        # at t=0 the kernel is a delta (K0 -> delta(x-x')), so the propagator
        # returns the initial state itself; use propagate for t>0.
        prop = psi0 if t == 0.0 else propagate(psi0, xs, t)
        spec = evolve_free_spectral(psi0, xs, t)    # via independent FFT TDSE solve
        maxdiff = max(maxdiff, float(np.max(np.abs(prop - spec))))
        c, w = packet_center_width(prop, xs)        # measured centre & width
        ax.plot(xs, np.abs(prop) ** 2, color=col, lw=2,
                label=fr"$t={t:.0f}$:  $\langle x\rangle={c:+.1f}$, $\sigma_x={w:.2f}$")
        ax.axvline(x0 + p0 * t, color=col, lw=0.8, ls=":")   # group-velocity centre
        sel = slice(None, None, 45)
        ax.plot(xs[sel], (np.abs(spec) ** 2)[sel], ls="none", marker="o",
                ms=3.2, mfc="none", mec="#555555",
                label=("split-step FFT" if t == 0.0 else None))
    ax.set_xlim(-13, 21)
    ax.set_xlabel("position $x$")
    ax.set_ylabel(r"$|\Psi(x,t)|^2$")
    ax.set_title(r"Free propagator evolves a packet: drift at $v=p_0/m$, width spreads")
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    _save(fig, "fig1_packet_propagation.svg")
    caps["fig1_packet_propagation.svg"] = (
        r"A Gaussian packet ($x_0=-8,\,p_0=2,\,\sigma=1$, $\hbar=m=1$) evolved by the "
        r"free propagator $\Psi(x,t)=\int K_0\,\Psi_0\,dx'$ (propagate) at $t=0,4,8$. "
        r"The centre drifts at the group velocity $v=p_0/m=2$ (dotted lines) while the "
        r"width spreads as $\sigma(t)=\sigma\sqrt{1+(\hbar t/2m\sigma^2)^2}$. Open "
        r"markers are an independent split-step FFT solve of the TDSE "
        rf"(evolve_free_spectral) — the two agree to {maxdiff:.0e}.")

    # ------------------------------------------------------------------ Fig 2
    # The path integral BUILDS the propagator: the Wick-rotated Trotter sum over
    # paths (D F D)^N -> the closed-form Euclidean kernel as N grows.  We plot the
    # kernel column K_E(x; x'=-1, tau=1) for the harmonic oscillator (V=x^2/2).
    xg = np.linspace(-6, 6, 601)
    j = 250                                          # source at x' = xg[250] = -1.0
    xp = float(xg[j])
    tau, omega = 1.0, 1.0
    Vho = lambda z: 0.5 * z ** 2
    exact = harmonic_propagator_euclidean(xg, xp, tau, omega=omega)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for N, col in [(1, STEEL), (2, ALT), (8, FLOW)]:
        K = path_integral_euclidean(xg, tau, N, Vho, j)
        err = float(np.max(np.abs(K - exact)))
        ax.plot(xg, K, color=col, lw=1.8,
                label=fr"$N={N}$ slices  (max err ${err:.1e}$)")
    ax.plot(xg, exact, color=INK, lw=2.6, ls="--",
            label=r"exact kernel  $K_E(x;x')$")
    ax.axvline(xp, color="#888888", lw=0.8, ls=":")
    ax.annotate(r"source $x'=-1$", xy=(xp, 0.02), xytext=(-5.6, 0.05),
                color="#555555", fontsize=9)
    ax.set_xlim(-4.5, 3.5)
    ax.set_xlabel("position $x$")
    ax.set_ylabel(r"$K_E(x;\,x'=-1,\,\tau=1)$")
    ax.set_title(r"Path integral builds the propagator: $(D\,F\,D)^N\to$ closed form")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_path_integral_convergence.svg")
    caps["fig2_path_integral_convergence.svg"] = (
        r"The harmonic-oscillator imaginary-time kernel $K_E(x;x'{=}-1,\tau{=}1)$ "
        r"($V=\tfrac12 x^2$, $\omega=1$) built by the Trotter sum-over-paths "
        r"$(D_{V/2}FD_{V/2})^N$ (path_integral_euclidean) for $N=1,2,8$ slices, "
        r"converging to the closed-form Mehler kernel (harmonic_propagator_euclidean, "
        r"dashed). One slice is crude; by $N=8$ the discretised path integral has "
        r"reproduced the exact propagator — Trotter error falls as $O(1/N^2)$.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
