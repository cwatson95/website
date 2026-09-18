"""QM-11 figures -- Larmor precession of a spin and driven Rabi oscillations.

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
from spin import (                                 # noqa: E402
    hamiltonian_field, spin_eigenstate, spin_expectations, larmor_frequency,
    rabi_probability, rabi_frequency,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- Larmor precession.  Spin tilted at alpha to B = B0 z evolves under
    # H = -gamma B.S; spin_expectations returns (<Sx>,<Sy>,<Sz>) at each t.  <Sz>
    # stays frozen while <Sx>,<Sy> rotate at omega = gamma B0 (larmor_frequency).
    gamma, B0, alpha = 2.0, 3.0, np.deg2rad(55.0)
    H = hamiltonian_field(gamma, [0.0, 0.0, B0])
    chi0 = spin_eigenstate(alpha, 0.0)
    omega = larmor_frequency(gamma, B0)
    period = 2.0 * np.pi / omega
    t = np.linspace(0.0, 2.0 * period, 600)
    sx, sy, sz = np.array([spin_expectations(H, chi0, float(ti)) for ti in t]).T

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(t, sx, color=INK, lw=2, label=r"$\langle S_x\rangle$")
    ax.plot(t, sy, color=STEEL, lw=2, label=r"$\langle S_y\rangle$")
    ax.plot(t, sz, color=FLOW, lw=2, label=r"$\langle S_z\rangle$ (frozen)")
    ax.axhline(0.5 * np.cos(alpha), color=FLOW, lw=0.8, ls="--")
    for k in (1, 2):
        ax.axvline(k * period, color="#dddddd", lw=0.8, ls=":")
    ax.set_xlim(0, 2 * period); ax.set_ylim(-0.55, 0.62)
    ax.set_xlabel(r"time $t$"); ax.set_ylabel(r"$\langle S_i\rangle/\hbar$")
    ax.set_title(r"Larmor precession: $\langle S_z\rangle$ frozen, $\langle S_x\rangle,\langle S_y\rangle$ rotate at $\omega=\gamma B_0$")
    ax.annotate(fr"$\omega=\gamma B_0={omega:.0f}$,  period $2\pi/\omega={period:.3f}$",
                xy=(0.05 * period, 0.52), color="#555555", fontsize=9)
    ax.legend(loc="lower right", frameon=False, fontsize=9, ncol=3)
    _save(fig, "fig1_larmor_precession.svg")
    caps["fig1_larmor_precession.svg"] = (
        r"A spin-$\frac12$ tilted $55^\circ$ from $B=B_0\hat z$, evolved under "
        r"$H=-\gamma B\cdot S$ by the module's spin_expectations. $\langle S_z\rangle"
        r"=\frac\hbar2\cos\alpha$ is constant while $\langle S_x\rangle,\langle S_y"
        r"\rangle$ trace a circle -- the spin precesses on a fixed cone at the Larmor "
        r"frequency $\omega=\gamma B_0$ (here $6$), period $2\pi/\omega$. This level "
        r"splitting $\hbar\omega$ is the NMR/ESR resonance.")

    # Fig 2 -- Rabi oscillations.  rabi_probability(t, Omega, Delta) for the upper
    # level: full inversion on resonance, partial flops saturating at
    # Omega^2/Omega_R^2 when detuned, oscillating faster at Omega_R = rabi_frequency.
    Omega = 1.0
    t = np.linspace(0.0, 4.0 * np.pi, 900)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for Delta, col in [(0.0, INK), (1.0, FLOW), (2.0, ALT)]:
        P = rabi_probability(t, Omega, Delta)
        OmR = rabi_frequency(Omega, Delta)
        Pmax = Omega ** 2 / OmR ** 2
        ax.plot(t, P, color=col, lw=2,
                label=fr"$\Delta={Delta:.0f}$:  $P_{{\max}}={Pmax:.2f}$, $\Omega_R={OmR:.2f}$")
        ax.axhline(Pmax, color=col, lw=0.8, ls="--")
    ax.set_xlim(0, 4 * np.pi); ax.set_ylim(0, 1.08)
    ax.set_xlabel(r"time $t$"); ax.set_ylabel(r"$P_\uparrow(t)$")
    ax.set_title(r"Rabi flop ($\Omega=1$): full inversion on resonance, partial when detuned")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_rabi_oscillations.svg")
    caps["fig2_rabi_oscillations.svg"] = (
        r"Upper-level probability $P_\uparrow(t)$ from the module's rabi_probability "
        r"for drive $\Omega=1$ at three detunings $\Delta$. On resonance "
        r"($\Delta=0$) the population fully inverts every $t=\pi/\Omega$ "
        r"($\pi$-pulse); off resonance the flop never completes, saturating at "
        r"$\Omega^2/\Omega_R^2<1$ and oscillating faster at the generalized Rabi "
        r"frequency $\Omega_R=\sqrt{\Omega^2+\Delta^2}$ -- the engine of magnetic "
        r"resonance and single-qubit gates.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
