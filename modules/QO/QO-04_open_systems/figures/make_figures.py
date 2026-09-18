"""QO-04 figures — decoherence (T1/T2) and optical-Bloch saturation.

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
from open_systems import (                         # noqa: E402
    ket_e, ket_g, density_matrix, evolve_lindblad,
    excited_population, coherence,
    spontaneous_emission_op, dephasing_op,
    two_level_hamiltonian, steady_state_excited_population,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    gamma = 1.0                                    # decay rate sets the time unit 1/gamma

    # Fig 1 — decoherence: population (T1) and coherence (T2) decay, computed by
    # evolve_lindblad on the |+> state; pure dephasing damps ONLY the coherence.
    # Solid lines: the module's simulation.  Dashed: the closed forms it reproduces.
    plus = (ket_e + ket_g) / np.sqrt(2.0)          # equal-coherence superposition
    rho0 = density_matrix(plus)
    t = np.linspace(0.0, 6.0, 400)
    L_spont = spontaneous_emission_op(gamma)

    rhos = evolve_lindblad(rho0, np.zeros((2, 2)), [L_spont], t)
    pe = np.array([excited_population(r) for r in rhos])         # ~ e^{-gamma t}
    coh = np.array([abs(coherence(r)) for r in rhos])           # ~ e^{-gamma t/2}

    gamma_phi = 0.8                                # pure-dephasing rate 1/T_phi
    rhos_d = evolve_lindblad(rho0, np.zeros((2, 2)),
                             [L_spont, dephasing_op(gamma_phi)], t)
    coh_d = np.array([abs(coherence(r)) for r in rhos_d])       # ~ e^{-(gamma/2+gamma_phi)t}

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(t, pe, color=INK, lw=2,
            label=r"population $\rho_{ee}$  ($T_1=1/\gamma$)")
    ax.plot(t, coh, color=FLOW, lw=2,
            label=r"coherence $|\rho_{eg}|$  ($T_2=2T_1$)")
    ax.plot(t, coh_d, color=ALT, lw=2,
            label=r"$|\rho_{eg}|$ + dephasing $\gamma_\phi=0.8$")
    ax.plot(t, 0.5 * np.exp(-gamma * t), color="#888888", lw=1.0, ls="--")
    ax.plot(t, 0.5 * np.exp(-0.5 * gamma * t), color="#888888", lw=1.0, ls="--")
    ax.plot(t, 0.5 * np.exp(-(0.5 * gamma + gamma_phi) * t), color="#888888",
            lw=1.0, ls="--", label=r"closed forms $\frac{1}{2}e^{-t/T}$")
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 0.52)
    ax.set_xlabel(r"time $\gamma t$")
    ax.set_ylabel("population / coherence")
    ax.set_title(r"Decoherence: coherence decays at half the population rate ($T_2=2T_1$)")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_decoherence_T1_T2.svg")
    caps["fig1_decoherence_T1_T2.svg"] = (
        r"Spontaneous-emission decoherence from evolve_lindblad on the $|+\rangle$ "
        r"state ($\hbar=1$). The excited population $\rho_{ee}$ (blue) decays at "
        r"$\gamma$ ($T_1$) while the coherence $|\rho_{eg}|$ (orange) decays at "
        r"$\gamma/2$, so $T_2=2T_1$; adding pure dephasing $\gamma_\phi$ (purple) "
        r"damps only the coherence, $1/T_2=\gamma/2+\gamma_\phi$. Dashed: the closed "
        r"forms the simulation reproduces.")

    # Fig 2 — optical-Bloch saturation: steady-state excited population vs Rabi
    # frequency for several detunings.  Curves: steady_state_excited_population
    # (analytic).  Markers: rho_ee at long time from evolve_lindblad (the sim).
    omega = np.linspace(0.0, 12.0, 400)
    omega_pts = np.array([1.0, 2.0, 4.0, 8.0])
    t_ss = np.linspace(0.0, 60.0, 600)             # long enough to reach steady state

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for Delta, col in [(0.0, INK), (1.0, STEEL), (2.5, FLOW)]:
        ax.plot(omega, [steady_state_excited_population(O, gamma, Delta)
                        for O in omega], color=col, lw=2,
                label=fr"$\Delta={Delta:g}\,\gamma$")
        sim = []
        for O in omega_pts:
            H = two_level_hamiltonian(O, Delta)
            traj = evolve_lindblad(density_matrix(ket_g), H, [L_spont], t_ss)
            sim.append(excited_population(traj[-1]))
        ax.plot(omega_pts, sim, ls="none", marker="o", ms=5, color=col)
    ax.axhline(0.5, color="#888888", lw=1.0, ls="--",
               label=r"saturation $\rho_{ee}^{ss}\to\frac{1}{2}$")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 0.55)
    ax.set_xlabel(r"Rabi frequency $\Omega/\gamma$")
    ax.set_ylabel(r"steady-state population $\rho_{ee}^{ss}$")
    ax.set_title("Optical Bloch: a classical drive saturates but never inverts the atom")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    _save(fig, "fig2_optical_bloch_saturation.svg")
    caps["fig2_optical_bloch_saturation.svg"] = (
        r"Driven-damped steady state $\rho_{ee}^{ss}=(\Omega^2/4)/(\Delta^2+\gamma^2/4"
        r"+\Omega^2/2)$ vs Rabi frequency for detunings $\Delta=0,1,2.5\,\gamma$. "
        r"Curves are steady_state_excited_population; dots are $\rho_{ee}$ at long "
        r"time from evolve_lindblad driven out of $|g\rangle$. The population rises "
        r"toward $\frac{1}{2}$ but never crosses it — a classical field can equalize "
        r"but cannot invert a two-level atom.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
