"""PK-03 figures — electrostatic wave dispersion & the two-stream instability.

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
from plasma_waves import (                         # noqa: E402
    ELEM_CHARGE, ELECTRON_MASS, PROTON_MASS, K_B,
    plasma_frequency, debye_length, thermal_speed,
    bohm_gross, ion_acoustic, two_stream_growth_rate,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

# fiducial plasma (the module demo / tests use these)
N = 1.0e18          # electron density [1/m^3]
T = 1.0e4           # temperature      [K]  (~0.86 eV)
E, ME, MI = ELEM_CHARGE, ELECTRON_MASS, PROTON_MASS


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    wp = plasma_frequency(N, E, ME)          # electron plasma frequency
    lD = debye_length(N, T, E)               # electron Debye length
    cs = np.sqrt(K_B * T / MI)               # ion-acoustic sound speed c_s
    wpi = cs / lD                            # ion plasma frequency w_pi = c_s/lam_D

    # Fig 1 — the two longitudinal branches vs k*lam_D, each normalised to its own
    # characteristic frequency.  Curves are the module's bohm_gross / ion_acoustic.
    kld = np.linspace(1e-3, 1.0, 600)
    k = kld / lD
    wL = bohm_gross(k, N, T, ME) / wp                  # Langmuir, -> 1 (w_p) at k->0
    wIA = ion_acoustic(k, T, N, MI) / wpi              # ion-acoustic, -> k lam_D (sound)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(kld, wL, color=INK, lw=2,
            label=r"Langmuir  $\omega/\omega_p=\sqrt{1+3(k\lambda_D)^2}$")
    ax.plot(kld, wIA, color=FLOW, lw=2,
            label=r"ion-acoustic  $\omega/\omega_{pi}$")
    ax.plot(kld, kld, color=ALT, lw=1.4, ls=":",
            label=r"sound  $\omega=k\,c_s$")
    ax.axhline(1.0, color=STEEL, lw=1.0, ls="--",
               label=r"cutoff $\omega_p$ / saturation $\omega_{pi}$")
    ax.set_xlim(0, 1.0); ax.set_ylim(0, 2.05)
    ax.set_xlabel(r"wavenumber $k\lambda_D$")
    ax.set_ylabel(r"frequency $\omega/\omega_*$  (branch scale)")
    ax.set_title("Electrostatic dispersion: a gapped wave and a sound wave")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig1_dispersion.svg")
    caps["fig1_dispersion.svg"] = (
        r"The two longitudinal branches vs $k\lambda_D$, each normalised to its own "
        r"scale (curves from bohm_gross / ion_acoustic). Langmuir starts at the "
        r"$\omega_p$ cutoff and stiffens via the Bohm$-$Gross pressure term "
        r"$3k^2v_{th}^2$; ion-acoustic is gapless sound $\omega\simeq kc_s$ that bends "
        r"over and saturates at the ion plasma frequency $\omega_{pi}=c_s/\lambda_D$.")

    # Fig 2 — two-stream instability: growth rate Im(w) of two cold beams at +/- v0.
    # Markers: the module's two_stream_growth_rate (numpy.roots of the bi-quadratic).
    # Line: the closed form  (gamma/w_p)^2 = -1/2[(2x^2+1) - sqrt(8x^2+1)],  x=kv0/w_p.
    v0 = 5.0 * thermal_speed(T, ME)
    x = np.linspace(1e-3, 1.3, 400)                    # x = k v0 / w_p
    kk = x * wp / v0
    g_code = np.array([two_stream_growth_rate(float(ki), N, ME, v0) for ki in kk]) / wp
    w2 = 0.5 * ((2 * x**2 + 1.0) - np.sqrt(8 * x**2 + 1.0))   # (w/w_p)^2, <0 -> growth
    g_th = np.sqrt(np.clip(-w2, 0.0, None))
    x_pk, g_pk = np.sqrt(3.0 / 8.0), 1.0 / np.sqrt(8.0)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.axvspan(0, 1.0, color=INK, alpha=0.06)
    ax.plot(x, g_th, color=FLOW, lw=2, label=r"closed form  $\mathrm{Im}\,\omega/\omega_p$")
    ax.plot(x[::12], g_code[::12], ls="none", marker="o", ms=4.5, color=INK,
            label=r"two_stream_growth_rate (numpy.roots)")
    ax.plot([x_pk], [g_pk], marker="*", ms=14, color=ALT, ls="none",
            label=r"peak $\frac{\omega_p}{\sqrt{8}}$ at $kv_0=\sqrt{\frac{3}{8}}\,\omega_p$")
    ax.axvline(1.0, color=STEEL, lw=1.0, ls="--")
    ax.annotate("unstable\n$kv_0<\\omega_p$", xy=(0.30, 0.05), color=INK, fontsize=9)
    ax.annotate("stable", xy=(1.07, 0.30), color=STEEL, fontsize=9)
    ax.set_xlim(0, 1.3); ax.set_ylim(0, 0.40)
    ax.set_xlabel(r"wavenumber $k v_0/\omega_p$")
    ax.set_ylabel(r"growth rate $\gamma/\omega_p$")
    ax.set_title("Two-stream instability: free streaming energy feeds the wave")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_two_stream.svg")
    caps["fig2_two_stream.svg"] = (
        r"Growth rate of the cold two-stream instability (counter-streaming beams at "
        r"$\pm v_0$): dots are two_stream_growth_rate, which solves the bi-quadratic "
        r"$\varepsilon(k,\omega)=0$ with numpy.roots, on the closed-form curve. "
        r"$\mathrm{Im}\,\omega>0$ only in the band $kv_0<\omega_p$, peaking at "
        r"$\gamma_{\max}=\omega_p/\sqrt8$ at $kv_0=\sqrt{3/8}\,\omega_p$ — the "
        r"opposite-sign cousin of Landau damping, fed by the beams' free energy.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
