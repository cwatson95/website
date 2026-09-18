"""SM-06 figures — the Maxwell-Boltzmann speed distribution and its T-dependence.

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
from kinetic_theory import (                       # noqa: E402
    maxwell_speed_pdf, most_probable_speed, mean_speed, rms_speed,
    mean_kinetic_energy, K_B,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

M_N2 = 4.652e-26          # nitrogen molecule [kg]


def _pdf(v_arr, m, T):
    """Vectorise the module's scalar maxwell_speed_pdf over a speed grid."""
    return np.array([maxwell_speed_pdf(float(v), m, T) for v in v_arr])


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the speed distribution with the three characteristic speeds,
    # in their fixed ordering v_p < <v> < v_rms.  All four from the module's code.
    T = 300.0
    v = np.linspace(0.0, 1500.0, 1200)
    f = _pdf(v, M_N2, T)
    vp = most_probable_speed(M_N2, T)
    vbar = mean_speed(M_N2, T)
    vrms = rms_speed(M_N2, T)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(v, f, color=INK, lw=2, label=r"$f(v)=4\pi(\frac{m}{2\pi kT})^{3/2}v^2 e^{-mv^2/2kT}$")
    ax.fill_between(v, f, color=INK, alpha=0.08)
    for x, col, lab in [(vp, FLOW, r"$v_p=\sqrt{2kT/m}$"),
                        (vbar, ALT, r"$\langle v\rangle=\sqrt{8kT/\pi m}$"),
                        (vrms, STEEL, r"$v_\mathrm{rms}=\sqrt{3kT/m}$")]:
        ax.axvline(x, color=col, lw=1.6, ls="--",
                   label=f"{lab}  = {x:.0f} m/s")
    ax.set_xlim(0, 1500)
    ax.set_ylim(bottom=0)
    ax.set_xlabel("molecular speed $v$ (m/s)")
    ax.set_ylabel(r"probability density $f(v)$ (s/m)")
    ax.set_title(r"Maxwell-Boltzmann speeds (N$_2$, 300 K): $v_p<\langle v\rangle<v_\mathrm{rms}$")
    ax.legend(loc="upper right", frameon=False, fontsize=8.5)
    _save(fig, "fig1_speed_distribution.svg")
    caps["fig1_speed_distribution.svg"] = (
        r"Maxwell-Boltzmann speed distribution $f(v)$ for N$_2$ at 300 K, from "
        r"maxwell_speed_pdf. The three characteristic speeds (dashed) sit in the "
        r"temperature-independent order $v_p<\langle v\rangle<v_\mathrm{rms}$ = "
        r"$1:\sqrt{4/\pi}:\sqrt{3/2}$ (422 < 476 < 517 m/s): the peak, the mean, and "
        r"the root-mean-square speed.")

    # Fig 2 — heating: peak shifts as v_p ~ sqrt(T) and the curve broadens, while
    # the area (the normalisation integral f dv) stays 1.  Integral via numpy on
    # the module-computed pdf.
    v = np.linspace(0.0, 2800.0, 1600)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for T, col in [(200.0, STEEL), (500.0, ALT), (1000.0, FLOW)]:
        f = _pdf(v, M_N2, T)
        area = float(np.trapezoid(f, v))
        vp = most_probable_speed(M_N2, T)
        ax.plot(v, f, color=col, lw=2,
                label=fr"$T={T:.0f}$ K:  $v_p={vp:.0f}$ m/s,  $\int f\,dv={area:.3f}$")
        ax.axvline(vp, color=col, lw=1.0, ls=":")
    ax.set_xlim(0, 2800)
    ax.set_ylim(bottom=0)
    ax.set_xlabel("molecular speed $v$ (m/s)")
    ax.set_ylabel(r"probability density $f(v)$ (s/m)")
    ax.set_title(r"Heating shifts the peak ($v_p\propto\sqrt{T}$) and broadens $f(v)$")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_temperature_dependence.svg")
    caps["fig2_temperature_dependence.svg"] = (
        r"The same distribution (N$_2$) at 200, 500 and 1000 K from maxwell_speed_pdf. "
        r"Heating pushes the most-probable speed out as $v_p\propto\sqrt{T}$ (dotted) "
        r"and flattens the curve, yet each integrates to 1 ($\int f\,dv\approx1$): a "
        r"hotter gas spreads the same total probability over a wider, faster band of "
        r"speeds.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
