"""QO-02 figures — semiclassical Rabi flopping & Jaynes-Cummings collapse/revival.

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
from scipy.linalg import expm                      # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from atom_field import (                           # noqa: E402
    rabi_excited_population, generalized_rabi, two_level_hamiltonian, ket_e, ket_g,
    jcm_inversion, resonant_inversion_series, collapse_time, revival_time,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — semiclassical Rabi flopping: a CLASSICAL drive flops the excited
    # population P_e(t) = (Om^2/Om_R^2) sin^2(Om_R t/2).  On resonance the flop is
    # complete (pi-pulse fully inverts at Om t = pi); off resonance it is faster
    # (rate Om_R) but saturates below 1 at Om^2/(Om^2+d^2).  Curves from the
    # module's rabi_excited_population; saturation lines from generalized_rabi;
    # open markers are a genuine exp(-iHt) evolution of |g> under
    # two_level_hamiltonian (closed form == dynamics).
    Omega = 1.0
    t = np.linspace(0.0, 4.0 * np.pi, 800)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for d, col in [(0.0, INK), (1.0, FLOW), (2.0, ALT)]:
        Pe = rabi_excited_population(t, Omega, d)
        ax.plot(t, Pe, color=col, lw=2,
                label=fr"$\delta={d:.0f}\,\Omega$,  $\Omega_R={generalized_rabi(Omega, d):.2f}$")
        if d > 0:                                   # saturated amplitude Om^2/Om_R^2 < 1
            sat = Omega ** 2 / generalized_rabi(Omega, d) ** 2
            ax.axhline(sat, color=col, lw=1.0, ls=":")
    # open markers: real time evolution of |g> under the RWA 2x2 H, on resonance
    tm = np.linspace(0.0, 4.0 * np.pi, 17)
    Hm = two_level_hamiltonian(Omega, 0.0)
    Pe_dyn = [abs(np.vdot(ket_e, expm(-1j * Hm * ti) @ ket_g)) ** 2 for ti in tm]
    ax.plot(tm, Pe_dyn, ls="none", marker="o", ms=5, mfc="none", mec=INK,
            label=r"$e^{-iHt}|g\rangle$ evolution ($\delta=0$)")
    ax.set_xlim(0, 4 * np.pi)
    ax.set_ylim(-0.03, 1.05)
    ax.set_xlabel(r"$\Omega t$")
    ax.set_ylabel(r"excited population $P_e(t)$")
    ax.set_title("Semiclassical Rabi flopping: resonant inversion vs detuned saturation")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_rabi_oscillations.svg")
    caps["fig1_rabi_oscillations.svg"] = (
        r"Semiclassical Rabi flopping $P_e(t)=(\Omega^2/\Omega_R^2)\sin^2(\Omega_R t/2)$ "
        r"from rabi_excited_population for detunings $\delta=0,\Omega,2\Omega$. On "
        r"resonance the atom fully inverts every $\Omega t=\pi$ ($\pi$-pulse) and "
        r"returns at $2\pi$; off resonance the flop is faster ($\Omega_R=\sqrt{\Omega^2+\delta^2}$) "
        r"but saturates at $\Omega^2/(\Omega^2+\delta^2)<1$ (dotted lines). Open "
        r"circles are a genuine $e^{-iHt}|g\rangle$ evolution under "
        r"two_level_hamiltonian, matching the closed form.")

    # Fig 2 — Jaynes-Cummings collapse and revival: the atom starts EXCITED over a
    # coherent field |alpha>; quantizing the field replaces the single Rabi tone by
    # a Poisson sum of tones 2 g sqrt(n+1), which DEPHASE (the inversion collapses
    # on t_c ~ sqrt2/g) and later REPHASE (partial revival at t_r ~ 2 pi sqrt(nbar)/g)
    # -- a signature absent for any classical field.  Solid: jcm_inversion (exact
    # eigenbasis evolution); markers: resonant_inversion_series (Poisson sum), an
    # independent cross-check.
    wc = wa = 5.0
    g = 1.0
    alpha = 4.0
    nbar = abs(alpha) ** 2                          # = 16
    N = 60
    tc, tr = collapse_time(g), revival_time(g, nbar)
    t = np.linspace(0.0, tr + 5.0, 1400)
    W = jcm_inversion(t, wc, wa, g, alpha, N)
    t_chk = np.linspace(0.0, tr + 5.0, 46)
    W_chk = resonant_inversion_series(t_chk, g, alpha, N)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.axhline(0.0, color="#aaaaaa", lw=0.6)
    ax.plot(t, W, color=INK, lw=1.6, label=r"$\langle\sigma_z\rangle(t)$  (jcm_inversion)")
    ax.plot(t_chk, W_chk, ls="none", marker="o", ms=4, mfc="none", mec=FLOW,
            label=r"$\sum_n P_n\cos(2g\sqrt{n+1}\,t)$  (Poisson sum)")
    ax.axvline(tc, color=STEEL, lw=1.0, ls="--")
    ax.axvline(tr, color=ALT, lw=1.0, ls="--")
    ax.annotate(r"collapse  $t_c\!\sim\!\sqrt{2}/g$", xy=(tc, -0.55),
                xytext=(tc + 1.0, -0.7), color=STEEL, fontsize=9)
    ax.annotate(r"revival  $t_r\!\sim\!2\pi\sqrt{\bar n}/g$", xy=(tr, 0.55),
                xytext=(tr - 11.5, 0.72), color=ALT, fontsize=9)
    ax.set_xlim(0, tr + 5.0)
    ax.set_ylim(-0.85, 1.05)
    ax.set_xlabel(r"$g t$")
    ax.set_ylabel(r"atomic inversion $\langle\sigma_z\rangle$")
    ax.set_title(r"Jaynes-Cummings collapse & revival over $|\alpha|^2=\bar n=16$")
    ax.legend(loc="lower left", frameon=False, fontsize=9)
    _save(fig, "fig2_collapse_revival.svg")
    caps["fig2_collapse_revival.svg"] = (
        r"Atomic inversion $\langle\sigma_z\rangle(t)$ for an excited atom over a "
        r"coherent field ($\bar n=|\alpha|^2=16$, resonant) from jcm_inversion (solid). "
        r"Field quantization replaces the single Rabi tone by a Poisson sum of tones "
        r"$2g\sqrt{n+1}$: they dephase, so the inversion COLLAPSES to zero on "
        r"$t_c\sim\sqrt{2}/g$, then rephase into a partial REVIVAL near "
        r"$t_r\sim2\pi\sqrt{\bar n}/g$ -- with no classical-field counterpart. Open "
        r"circles are the independent closed-form Poisson sum "
        r"(resonant_inversion_series).")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
