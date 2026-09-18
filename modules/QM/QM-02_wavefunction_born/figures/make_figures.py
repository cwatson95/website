"""QM-02 figures — Born's rule as area under |Psi|^2, and the position/momentum
Fourier trade-off of the Gaussian wavepacket.

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
from wavefunction import (                          # noqa: E402
    gaussian_packet, prob_density, prob_between, expectation_x, sigma_x,
    momentum_space, sigma_p,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — Born's rule: |Psi|^2 is a probability *density*, and the probability
    # of finding the particle in an interval is the AREA under it.  Shade the
    # +/-1 sigma and +/-2 sigma bands of a Gaussian packet; prob_between returns
    # those areas as erf(1/sqrt2)=0.6827 and erf(2/sqrt2)=0.9545.
    x = np.linspace(-12.0, 12.0, 3000)
    psi = gaussian_packet(x, x0=0.0, sigma=2.0, k0=0.0)
    rho = prob_density(psi)
    mu, sx = expectation_x(psi, x), sigma_x(psi, x)
    P1 = prob_between(psi, x, mu - sx, mu + sx)
    P2 = prob_between(psi, x, mu - 2 * sx, mu + 2 * sx)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    m2 = (x >= mu - 2 * sx) & (x <= mu + 2 * sx)
    m1 = (x >= mu - sx) & (x <= mu + sx)
    ax.fill_between(x[m2], rho[m2], color=STEEL, alpha=0.30, lw=0,
                    label=fr"$\pm2\sigma_x$:  $P={P2:.4f}$")
    ax.fill_between(x[m1], rho[m1], color=INK, alpha=0.50, lw=0,
                    label=fr"$\pm1\sigma_x$:  $P={P1:.4f}$")
    ax.plot(x, rho, color=INK, lw=2)
    for s in (-2, -1, 1, 2):
        ax.axvline(mu + s * sx, color="#aaaaaa", lw=0.7, ls=":")
    ax.set_xlim(-9, 9)
    ax.set_ylim(0, rho.max() * 1.18)
    ax.set_xlabel("position $x$")
    ax.set_ylabel(r"$\rho=|\Psi|^2$")
    ax.set_title(r"Born's rule: $P(a\leq x\leq b)=\int_a^b|\Psi|^2\,dx$ (area = probability)")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_born_density.svg")
    caps["fig1_born_density.svg"] = (
        "Born's statistical interpretation made visual: the probability of finding "
        "the particle in an interval is the AREA under rho=|Psi|^2 (prob_density). "
        "For the Gaussian wavepacket (sigma=2) prob_between returns P=0.682 inside "
        "+/-1 sigma_x (dark) and P=0.954 inside +/-2 sigma_x (light), matching the "
        "analytic erf(1/sqrt2)=0.6827 and erf(sqrt2)=0.9545. The whole density "
        "integrates to 1: the particle is somewhere.")

    # Fig 2 — the move to momentum space (momentum_space = Fourier transform) and
    # the conjugate-width trade-off: squeezing |Psi|^2 in x necessarily broadens
    # |Phi|^2 in p, with sigma_x*sigma_p = hbar/2 either way (minimum uncertainty).
    xx = np.linspace(-16.0, 16.0, 4096)
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(6.8, 3.3), layout="constrained")
    for s, col in [(0.7, FLOW), (2.0, INK)]:
        ps = gaussian_packet(xx, x0=0.0, sigma=s, k0=0.0)
        sxn = sigma_x(ps, xx)
        spn = sigma_p(ps, xx)
        p, phi = momentum_space(ps, xx)
        axL.plot(xx, prob_density(ps), color=col, lw=2,
                 label=fr"$\sigma_x={sxn:.2f}$")
        axR.plot(p, np.abs(phi) ** 2, color=col, lw=2,
                 label=fr"$\sigma_p={spn:.2f}$,  $\sigma_x\sigma_p={sxn*spn:.3f}$")
    axL.set_xlim(-7, 7); axL.set_xlabel("position $x$"); axL.set_ylabel(r"$|\Psi(x)|^2$")
    axL.set_title("position space", fontsize=10)
    axL.legend(loc="upper right", frameon=False, fontsize=8.5)
    axR.set_xlim(-3, 3); axR.set_xlabel("momentum $p$"); axR.set_ylabel(r"$|\Phi(p)|^2$")
    axR.set_title("momentum space", fontsize=10)
    axR.legend(loc="upper right", frameon=False, fontsize=7.5)
    fig.suptitle(r"Fourier trade-off: $\sigma_x\,\sigma_p=\hbar/2$ (minimum-uncertainty Gaussian)")
    _save(fig, "fig2_position_momentum.svg")
    caps["fig2_position_momentum.svg"] = (
        "The same state in position and momentum space (momentum_space = Fourier "
        "transform of Psi). Squeezing the packet in x (orange, sigma_x=0.70) "
        "necessarily broadens |Phi(p)|^2 in momentum (sigma_p=0.71), while the wide "
        "packet (blue, sigma_x=2.0) is sharp in p (sigma_p=0.25). Either way "
        "sigma_x*sigma_p=0.50=hbar/2: the Gaussian saturates the Heisenberg bound "
        "(the minimum-uncertainty state).")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
