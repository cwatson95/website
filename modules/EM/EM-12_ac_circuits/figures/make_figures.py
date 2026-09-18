"""EM-12 figures -- the series-RLC resonance curve and an off-resonance phasor diagram.

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
from ac_circuits import (                          # noqa: E402
    series_rlc_impedance, resonant_frequency, quality_factor,
    current_amplitude, current_phase,
    impedance_resistor, impedance_inductor, impedance_capacitor,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    L, C, V0 = 1e-3, 1e-6, 5.0
    w0 = resonant_frequency(L, C)

    # Fig 1 -- resonance curve |I|(w) for two damping resistances. Lower R -> higher
    # Q -> sharper, taller peak at w0 where the reactances cancel (Z = R).
    ratio = np.linspace(0.40, 1.80, 400)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for R, col in [(5.0, INK), (20.0, FLOW)]:
        Q = quality_factor(R, L, C)
        Imag = np.array([current_amplitude(V0, series_rlc_impedance(R, L, C, r * w0))
                         for r in ratio])
        ax.plot(ratio, Imag, color=col, lw=2,
                label=fr"$R={R:.0f}\,\Omega$  ($Q={Q:.1f}$)")
    ax.axvline(1.0, color="#bbbbbb", lw=0.8, ls="--")
    ax.text(1.02, 0.05, r"$\omega_0=1/\sqrt{LC}$", color="#666666", fontsize=9.5,
            transform=ax.get_xaxis_transform())
    ax.set_xlabel(r"drive frequency  $\omega/\omega_0$")
    ax.set_ylabel(r"current amplitude  $|I|$  (A)")
    ax.set_title("Series-RLC resonance: lower $R$ sharpens the peak")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig1_resonance_curve.svg")
    caps["fig1_resonance_curve.svg"] = (
        "Current amplitude |I| = V0/|Z| of a driven series RLC vs frequency, for two "
        "resistances. The peak sits at the resonance w0 = 1/sqrt(LC), where the inductive "
        "and capacitive reactances cancel (Z = R); a smaller R means a higher Q and a "
        "sharper, taller resonance.")

    # Fig 2 -- phasor diagram below resonance (w = 0.7 w0, capacitive). Taking the
    # common current I as the reference (+x), the element voltages V_R, V_L, V_C add
    # to the source V; the current leads V by phi = -arg(Z).
    R = 20.0
    w = 0.70 * w0
    Z = series_rlc_impedance(R, L, C, w)
    I0 = current_amplitude(V0, Z)
    phi = current_phase(Z)                              # current relative to voltage
    VR = I0 * impedance_resistor(R)
    VL = I0 * impedance_inductor(L, w)
    VC = I0 * impedance_capacitor(C, w)
    Vtot = I0 * Z                                       # = VR + VL + VC

    def arrow(ax, vec, color, label, lw=2.2, tail=(0.0, 0.0)):
        ax.annotate("", xy=(tail[0] + vec.real, tail[1] + vec.imag), xytext=tail,
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw))
        ax.plot([], [], color=color, lw=lw, label=label)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.axhline(0, color="#dddddd", lw=0.6); ax.axvline(0, color="#dddddd", lw=0.6)
    # current reference phasor (scaled into volts for display)
    Iref = (VR.real) * 1.25
    ax.annotate("", xy=(Iref, 0.0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#999999", lw=1.6, ls="--"))
    ax.text(Iref, -0.5, r"$I$ (ref)", color="#777777", fontsize=10, ha="center")
    arrow(ax, VR, FLOW, r"$V_R=IR$")
    arrow(ax, VL, STEEL, r"$V_L=i\omega L\,I$")
    arrow(ax, VC, ALT, r"$V_C=I/i\omega C$")
    arrow(ax, Vtot, INK, r"$V=IZ$ (source)", lw=2.8)
    ax.set_aspect("equal")
    ax.set_xlabel("in-phase component  (V)")
    ax.set_ylabel("quadrature component  (V)")
    ax.set_title(fr"RLC phasors below resonance: $I$ leads $V$ by {math.degrees(phi):.0f}$^\circ$")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    pad = 1.3 * max(abs(VC.imag), abs(VL.imag), Iref)
    ax.set_xlim(-0.4 * pad, pad); ax.set_ylim(-pad, 0.7 * pad)
    _save(fig, "fig2_rlc_phasors.svg")
    caps["fig2_rlc_phasors.svg"] = (
        "Phasor diagram of a series RLC driven below resonance (w = 0.7 w0, capacitive), "
        "with the common current I as reference. The resistor voltage is in phase, V_L "
        "leads and V_C lags by 90 degrees, and they sum to the source V = IZ; the current "
        "leads the source voltage by phi = -arg(Z).")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
