"""CM-15 figures — driven resonance (amplitude & phase) and the damping regimes.

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
from oscillations import (                         # noqa: E402
    driven_amplitude, resonance_frequency, quality_factor,
    damped_frequency, integrate_oscillator,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    w0, F0 = 1.0, 1.0

    # Fig 1 — steady-state resonance: amplitude A(w) and phase lag for several Q.
    # A(w) is the module's driven_amplitude; the peak sits at resonance_frequency.
    w = np.linspace(0.02, 2.2, 700)
    Qs = [1.0, 2.0, 4.0, 8.0]
    cols = [STEEL, ALT, FLOW, INK]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.2, 4.7), sharex=True)
    for Q, c in zip(Qs, cols):
        g = w0 / (2.0 * Q)                                  # Q = w0/(2 gamma)
        A = np.array([driven_amplitude(w0, g, F0, wd) for wd in w])
        ax1.plot(w, A, color=c, lw=2, label=fr"$Q={quality_factor(w0, g):.0f}$")
        wr = resonance_frequency(w0, g)                     # peak at sqrt(w0^2-2g^2)
        ax1.plot(wr, driven_amplitude(w0, g, F0, wr), "o", ms=4, color=c)
        # steady-state phase lag delta = atan2(2 g w, w0^2 - w^2)  (x = A cos(wt-delta))
        delta = np.degrees(np.arctan2(2.0 * g * w, w0 ** 2 - w ** 2))
        ax2.plot(w, delta, color=c, lw=2)
    ax1.axvline(w0, color="#888888", lw=0.8, ls=":")
    ax1.set_ylabel(r"amplitude $A(\omega)$")
    ax1.set_title(r"Driven resonance: $A=F_0/\sqrt{(\omega_0^2-\omega^2)^2+(2\gamma\omega)^2}$")
    ax1.legend(loc="upper right", frameon=False, fontsize=9)
    ax2.axvline(w0, color="#888888", lw=0.8, ls=":")
    ax2.axhline(90, color="#888888", lw=0.8, ls=":")
    ax2.set_xlim(0, 2.2)
    ax2.set_yticks([0, 45, 90, 135, 180])
    ax2.set_xlabel(r"drive frequency $\omega$  (units of $\omega_0$)")
    ax2.set_ylabel(r"phase lag $\delta$ (deg)")
    _save(fig, "fig1_resonance.svg")
    caps["fig1_resonance.svg"] = (
        r"Steady-state response of the driven oscillator vs drive frequency for "
        r"$Q=1,2,4,8$ ($\omega_0=1$). Top: amplitude $A(\omega)$ from driven_amplitude, "
        r"sharpening and peaking near $\omega_0$ (dots at resonance_frequency "
        r"$\sqrt{\omega_0^2-2\gamma^2}$) as $Q$ grows. Bottom: the phase lag passes "
        r"through $90^\circ$ at $\omega_0$, ever more steeply for high $Q$.")

    # Fig 2 — free ring-down in the three damping regimes (x0=1, v0=0, no drive),
    # integrated with the module's integrate_oscillator (reuses the MA-07 RK4).
    t1, n = 18.0, 1800
    regimes = [
        ("underdamped",       0.15, INK),
        ("critically damped", 1.0,  FLOW),
        ("overdamped",        2.5,  ALT),
    ]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for name, g, c in regimes:
        ts, ys = integrate_oscillator(w0, g, 1.0, 0.0, 0.0, t1, n)
        t = np.array(ts)
        x = np.array([s[0] for s in ys])
        if name == "underdamped":
            wd = damped_frequency(w0, g)
            lbl = fr"{name} ($\gamma={g}$, $\omega_d={wd:.2f}$)"
            ax.plot(t, np.exp(-g * t), color="#999999", lw=1.0, ls="--",
                    label=r"envelope $\pm e^{-\gamma t}$")
            ax.plot(t, -np.exp(-g * t), color="#999999", lw=1.0, ls="--")
        else:
            lbl = fr"{name} ($\gamma={g}$)"
        ax.plot(t, x, color=c, lw=2, label=lbl)
    ax.axhline(0, color="#cccccc", lw=0.6)
    ax.set_xlim(0, t1)
    ax.set_xlabel(r"time $t$")
    ax.set_ylabel(r"displacement $x(t)$")
    ax.set_title(r"Free ring-down: under- / critically / over-damped ($\omega_0=1$)")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_damping_regimes.svg")
    caps["fig2_damping_regimes.svg"] = (
        r"Free response $x(t)$ from integrate_oscillator ($x_0=1,\,v_0=0$, no drive, "
        r"$\omega_0=1$) in the three regimes. Underdamped ($\gamma<\omega_0$) "
        r"oscillates at $\omega_d=\sqrt{\omega_0^2-\gamma^2}$ inside the decaying "
        r"envelope $e^{-\gamma t}$; critically ($\gamma=\omega_0$) and overdamped "
        r"($\gamma>\omega_0$) return without oscillating.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
