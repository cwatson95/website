"""QM-16 figures — Rabi oscillations and the sinc^2 resonance line.

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
from tdpt import (                                 # noqa: E402
    rabi_probability, two_level_exact_probability,
    generalized_rabi_frequency, sinusoidal_probability,
)

INK, FLOW, ALT, EXTRA = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — Rabi flopping: full inversion on resonance, capped + faster off it.
    Omega_R = 1.0
    t = np.linspace(0.0, 4.0 * np.pi, 700)         # time in units of 1/Omega_R
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    rows = [(0.0, INK,  r"$\delta=0$"),
            (1.0, ALT,  r"$\delta=\Omega_R$"),
            (2.0, FLOW, r"$\delta=2\Omega_R$")]
    for delta, col, lab in rows:
        P = rabi_probability(t, Omega_R, delta)
        cap = Omega_R ** 2 / (Omega_R ** 2 + delta ** 2)      # off-resonant ceiling
        Omega = generalized_rabi_frequency(Omega_R, delta)    # flopping frequency
        ax.plot(t, P, color=col, lw=2,
                label=lab + fr"  ($P_{{\max}}={cap:.2f}$, $\Omega={Omega:.2f}$)")
        if delta > 0:
            ax.axhline(cap, color=col, lw=0.8, ls=":")        # the cap it never beats
    # overlay the EXACT 2x2 dynamics on the detuned curve: closed form == e^{-iHt}
    td = np.linspace(0.0, 4.0 * np.pi, 17)
    Pd = [two_level_exact_probability(tt, 1.0, Omega_R) for tt in td]
    ax.plot(td, Pd, "o", color=EXTRA, ms=4.5, mew=0,
            label=r"exact $2\times2$ evolution ($\delta=\Omega_R$)")
    ax.set_xlim(0, 4 * np.pi); ax.set_ylim(-0.03, 1.05)
    ax.set_xlabel(r"time $t$  (units $\Omega_R^{-1}$)")
    ax.set_ylabel(r"transition probability $P_{i\to f}$")
    ax.set_title("Rabi flopping: full inversion on resonance, capped when detuned")
    ax.legend(loc="upper right", frameon=False, fontsize=8.5)
    _save(fig, "fig1_rabi_oscillations.svg")
    caps["fig1_rabi_oscillations.svg"] = (
        "Exact two-level Rabi formula $P=\\frac{\\Omega_R^2}{\\Omega_R^2+\\delta^2}"
        "\\sin^2(\\sqrt{\\Omega_R^2+\\delta^2}\\,t/2)$ (hbar=1, Omega_R=1). On "
        "resonance (delta=0, blue) the population fully inverts to P=1 every "
        "pi/Omega_R; detuning caps the amplitude at Omega_R^2/(Omega_R^2+delta^2) "
        "(dotted) and speeds the flopping up to the generalized Rabi frequency "
        "sqrt(Omega_R^2+delta^2). Dots are the exact 2x2 evolution e^{-iHt} — the "
        "closed form and the honest dynamics agree.")

    # Fig 2 — sinusoidal drive: a sinc^2 resonance that grows ~t^2, narrows ~1/t.
    omega_fi, V_fi = 1.0, 0.05
    omega = np.linspace(0.3, 1.7, 2001)            # scan the drive frequency
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for T, col in [(8.0, ALT), (16.0, FLOW), (32.0, INK)]:
        P = sinusoidal_probability(T, omega, omega_fi, V_fi)
        peak = (V_fi * T / 2.0) ** 2               # central height |V_fi|^2 t^2/4
        ax.plot(omega, P, color=col, lw=2,
                label=fr"$t={T:.0f}$  (peak $={peak:.3f}$, width $\sim{2*np.pi/T:.2f}$)")
    ax.axvline(omega_fi, color="#aaaaaa", lw=0.8, ls=":")     # resonance w = w_fi
    ax.set_xlim(0.3, 1.7)
    ax.set_xlabel(r"drive frequency $\omega$  (resonance at $\omega_{fi}=1$)")
    ax.set_ylabel(r"transition probability $P_{i\to f}$")
    ax.set_title(r"Resonance line: $\mathrm{sinc}^2$ peak grows $\sim t^2$, narrows $\sim 1/t$")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_resonance_lineshape.svg")
    caps["fig2_resonance_lineshape.svg"] = (
        "First-order transition probability under a sinusoidal drive "
        "$P=|V_{fi}|^2\\,\\sin^2[(\\omega_{fi}-\\omega)t/2]/(\\omega_{fi}-\\omega)^2$ "
        "vs the drive frequency, for three driving times (V_fi=0.05, omega_fi=1). "
        "The line is a sinc^2 sharply peaked on resonance omega=omega_fi (dotted): "
        "the central peak grows like t^2 while the width shrinks like 1/t (first "
        "zeros at omega_fi ± 2*pi/t). Driving longer makes the resonance taller and "
        "more frequency-selective — the energy-time complementarity behind "
        "spectroscopic linewidths and Fermi's golden rule.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
