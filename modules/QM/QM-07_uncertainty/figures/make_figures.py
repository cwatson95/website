"""QM-07 figures — the position-momentum trade-off and Ehrenfest's theorem.

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
from uncertainty import (                          # noqa: E402
    grid, normalize, gaussian_packet,
    sigma_x, sigma_p, uncertainty_product,
    split_step_evolve, classical_sho,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _momentum_density(psi, dx):
    """Momentum-space probability density |psi-tilde(p)|^2 on the conjugate grid,
    via the FFT (x and p are conjugate Fourier variables -- the same spectral
    p-hat the module applies).  Returned sorted in p and normalised to unit area."""
    N = psi.size
    k = 2.0 * np.pi * np.fft.fftfreq(N, d=dx)      # matches uncertainty._kgrid
    phi = np.fft.fft(psi) * dx
    order = np.argsort(k)
    k = k[order]
    rho = np.abs(phi[order]) ** 2
    dk = k[1] - k[0]
    rho /= rho.sum() * dk
    return k, rho


def main():
    caps = {}
    x, dx = grid(L=40.0, N=2048)

    # Fig 1 — the position-momentum trade-off: a packet narrow in x is broad in p,
    # and BOTH saturate sigma_x sigma_p = hbar/2.  Densities, widths and products
    # all come from the module (gaussian_packet, sigma_x, sigma_p, ...).
    cases = [("narrow", 0.7, INK), ("wide", 1.8, FLOW)]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.2, 4.8))
    for tag, sig, col in cases:
        psi = gaussian_packet(x, x0=0.0, sigma=sig, p0=0.0)
        rho_x = np.abs(normalize(psi, dx)) ** 2
        p, rho_p = _momentum_density(normalize(psi, dx), dx)
        sx, sp = sigma_x(psi, x, dx), sigma_p(psi, dx)
        prod = uncertainty_product(psi, x, dx)
        ax1.plot(x, rho_x, color=col, lw=2,
                 label=fr"$\sigma_x={sx:.2f}$  ($\sigma_x\sigma_p={prod:.3f}$)")
        ax2.plot(p, rho_p, color=col, lw=2, label=fr"$\sigma_p={sp:.2f}$")
    ax1.set_xlim(-6, 6); ax1.set_xlabel("position $x$"); ax1.set_ylabel(r"$|\Psi(x)|^2$")
    ax1.set_title(r"Conjugate trade-off: narrow in $x$ $\Leftrightarrow$ broad in $p$,"
                  r"  $\sigma_x\sigma_p=\frac{1}{2}$")
    ax1.legend(loc="upper right", frameon=False, fontsize=9)
    ax2.set_xlim(-6, 6); ax2.set_xlabel("momentum $p$"); ax2.set_ylabel(r"$|\tilde\Psi(p)|^2$")
    ax2.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_position_momentum_tradeoff.svg")
    caps["fig1_position_momentum_tradeoff.svg"] = (
        r"Two minimum-uncertainty Gaussians ($\hbar=m=1$): position densities "
        r"$|\Psi(x)|^2$ (top) and their FFT momentum densities $|\tilde\Psi(p)|^2$ "
        r"(bottom), with $\sigma_x,\sigma_p$ from the module's sigma_x/sigma_p. The "
        r"narrow packet ($\sigma_x=0.7$) is broad in $p$ and the wide one "
        r"($\sigma_x=1.8$) is sharp in $p$, yet BOTH saturate "
        r"$\sigma_x\sigma_p=\hbar/2$ — the trade-off is a property of the state.")

    # Fig 2 — Ehrenfest in the harmonic well: the packet CENTRE rides the classical
    # trajectory.  <x>(t), <p>(t) are recorded by split_step_evolve; the dots are
    # the independent classical curve classical_sho(t).
    xo, dxo = grid(L=40.0, N=1024)
    omega, x0, p0 = 1.0, 3.0, 0.0
    pkt = gaussian_packet(xo, x0=x0, sigma=1.0, p0=p0)        # coherent (min-uncertainty) state
    V = 0.5 * omega ** 2 * xo ** 2
    nper, dt = 2, 0.01
    nsteps = int(nper * 2.0 * np.pi / dt)
    t, xs, ps, Fs, _ = split_step_evolve(pkt, xo, V=V, dt=dt, nsteps=nsteps,
                                         dVdx=lambda xx: omega ** 2 * xx)
    xcl = classical_sho(t, x0, p0, omega)
    err = float(np.max(np.abs(xs - xcl)))
    sub = slice(0, len(t), 60)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(t, xs, color=INK, lw=2, label=r"$\langle x\rangle(t)$  (split-step)")
    ax.plot(t, ps, color=STEEL, lw=2, label=r"$\langle p\rangle(t)$  (split-step)")
    ax.plot(t[sub], xcl[sub], ls="none", marker="o", ms=4, color=FLOW,
            label=r"classical $x_0\cos\omega t+\frac{p_0}{m\omega}\sin\omega t$")
    ax.axhline(0, color="#cccccc", lw=0.6)
    for k in range(1, nper + 1):
        ax.axvline(k * 2 * np.pi, color="#dddddd", lw=0.8, ls=":")
    ax.set_xlim(0, nper * 2 * np.pi)
    ax.set_xlabel(r"time $t$"); ax.set_ylabel(r"expectation value")
    ax.set_title(r"Ehrenfest in the harmonic well: $\langle x\rangle$ rides the classical orbit")
    ax.annotate(fr"$\max|\langle x\rangle-x_{{cl}}|={err:.1e}$", xy=(0.4, -2.6),
                color="#555555", fontsize=9)
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_ehrenfest_harmonic.svg")
    caps["fig2_ehrenfest_harmonic.svg"] = (
        r"A coherent Gaussian ($x_0=3,\,\sigma=1$) evolved in $V=\frac12\omega^2x^2$ by "
        r"the module's split_step_evolve. The recorded $\langle x\rangle(t)$ (blue) and "
        r"$\langle p\rangle(t)$ (steel) obey $d\langle x\rangle/dt=\langle p\rangle/m$, "
        r"and $\langle x\rangle$ lands exactly on the independent classical curve "
        r"classical_sho (dots) — Ehrenfest's theorem is EXACT for the harmonic "
        r"well, where $\langle V'(x)\rangle=V'(\langle x\rangle)$.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
