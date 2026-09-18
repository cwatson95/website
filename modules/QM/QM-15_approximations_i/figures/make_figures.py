"""QM-15 figures — the variational upper bound and the perturbation series.

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
from approximations import (                       # noqa: E402
    ho_energies, ho_matrix_power, perturbed_energy, exact_energy,
    gaussian_trial, variational_energy, gaussian_ho_energy,
    gaussian_variational_min, fd_ground_energy,
)

INK, FLOW, ALT, EXTRA = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — variational principle: every trial energy <H>(b) lies above E_gs;
    # minimizing squeezes the bound down. Exact for the Gaussian-on-oscillator
    # (the family contains the true state), a genuine upper bound for the quartic.
    b = np.linspace(0.2, 2.2, 400)
    Eho = np.array([gaussian_ho_energy(bb) for bb in b])           # closed form b/2 + 1/(8b)
    xg = np.linspace(-12.0, 12.0, 6001)
    Vq = 0.25 * xg ** 4
    Eq = np.array([variational_energy(gaussian_trial(bb, xg), xg, Vq) for bb in b])  # grid Rayleigh quotient
    E0_ho = 0.5                                                    # exact oscillator ground state
    Egs_q = fd_ground_energy(lambda t: 0.25 * t ** 4, np.linspace(-8.0, 8.0, 2000))  # exact FD truth
    Emin_ho, bopt_ho = gaussian_variational_min(lambda t: 0.5 * t ** 2, xg)
    Emin_q, bopt_q = gaussian_variational_min(lambda t: 0.25 * t ** 4, xg)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(b, Eho, color=INK, lw=2, label=r"oscillator $V=\frac{1}{2}x^2$")
    ax.plot(b, Eq, color=FLOW, lw=2, label=r"quartic $V=\frac{1}{4}x^4$")
    ax.axhline(E0_ho, color=INK, lw=1.0, ls="--",
               label=r"$E_0=\frac{1}{2}$ (oscillator, exact)")
    ax.axhline(Egs_q, color=FLOW, lw=1.0, ls="--",
               label=r"$E_{gs}=%.3f$ (quartic, exact FD)" % Egs_q)
    ax.plot([bopt_ho], [Emin_ho], "o", color=INK, ms=6, zorder=5)
    ax.plot([bopt_q], [Emin_q], "o", color=FLOW, ms=6, zorder=5)
    ax.set_xlim(0.2, 2.2); ax.set_ylim(0.35, 1.55)
    ax.set_xlabel(r"trial width $b$"); ax.set_ylabel(r"$\langle H\rangle(b)$")
    ax.set_title(r"Variational principle: $\langle H\rangle(b)\geq E_{gs}$, minimized over $b$")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig1_variational.svg")
    caps["fig1_variational.svg"] = (
        "Variational principle (QM-15). Gaussian trial energy $\\langle H\\rangle(b)$ for "
        "$\\psi_b\\propto e^{-bx^2}$ vs width $b$: oscillator $V=\\tfrac12x^2$ (blue, closed form "
        "gaussian_ho_energy) and quartic $V=\\tfrac14x^4$ (orange, grid Rayleigh quotient "
        "variational_energy). Every point lies above the true ground state (dashed). Minimizing "
        "(dots, gaussian_variational_min) hits $E_0=\\tfrac12$ exactly for the oscillator — the "
        "family contains the true state — but for the quartic the bound settles ~2% above the "
        "exact finite-difference $E_{gs}\\approx0.421$. $\\hbar=m=\\omega=1$.")

    # Fig 2 — nondegenerate perturbation theory: H = H0 + lambda x^2 (anharmonic
    # stiffening of the oscillator). Exact diagonalization vs the series truncated
    # at order 0/1/2 — each added order tracks the truth over a wider lambda range.
    D = 40
    E0 = ho_energies(D)
    Hp = ho_matrix_power(D, 2)                                     # H' = x^2
    lam = np.linspace(0.0, 1.0, 201)
    exact = np.array([exact_energy(E0, Hp, 0, l) for l in lam])
    o0 = np.array([perturbed_energy(E0, Hp, 0, l, order=0) for l in lam])
    o1 = np.array([perturbed_energy(E0, Hp, 0, l, order=1) for l in lam])
    o2 = np.array([perturbed_energy(E0, Hp, 0, l, order=2) for l in lam])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(lam, exact, color=INK, lw=2.6, label="exact (diagonalization)")
    ax.plot(lam, o0, color="#9a9a9a", lw=1.6, ls=":", label=r"order 0: $E_0^0$")
    ax.plot(lam, o1, color=ALT, lw=1.8, ls="--", label=r"order 1: $+\lambda E_0^{(1)}$")
    ax.plot(lam, o2, color=FLOW, lw=1.8, label=r"order 2: $+\lambda^2 E_0^{(2)}$")
    ax.set_xlim(0.0, 1.0)
    ax.set_xlabel(r"perturbation strength $\lambda$")
    ax.set_ylabel(r"ground-state energy $E_0$")
    ax.set_title(r"Perturbation theory: $H=H_0+\lambda x^2$, orders vs exact")
    ax.legend(loc="upper left", frameon=False)
    _save(fig, "fig2_perturbation.svg")
    caps["fig2_perturbation.svg"] = (
        "Time-independent perturbation theory (QM-15) for $H=H_0+\\lambda x^2$ — an anharmonic "
        "stiffening of the oscillator, ground state. Exact diagonalization (blue) vs the "
        "perturbation series truncated at order 0, 1, 2 (perturbed_energy / exact_energy). Each "
        "added order hugs the exact curve over a wider range of $\\lambda$ before peeling away — "
        "the signature of an asymptotic series: $E_0=E_0^0+\\lambda E_0^{(1)}+\\lambda^2E_0^{(2)}$ "
        "with $E_0^{(1)}=\\tfrac12$, $E_0^{(2)}=-\\tfrac14$. $\\hbar=m=\\omega=1$.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
