"""QO-06 figures — SHG phase-matching sinc^2 and the SBS Lorentzian gain.

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
from nonlinear_optics import (                      # noqa: E402
    shg_efficiency, shg_phase_mismatch, coherence_length,
    brillouin_shift, brillouin_gain,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — chi^(2) SHG phase matching: eta = sinc^2(Delta k L / 2).
    # Curves are shg_efficiency itself; the longer crystal has the NARROWER
    # acceptance, first nulling at Delta k = 2 pi / L (the module's own physics).
    lam = 1.064e-6
    L1, L2 = 1.0e-3, 2.0e-3
    x = np.linspace(-13.0, 13.0, 1600)             # phase mismatch in rad/mm
    dk = x * 1.0e3                                  # -> rad/m for the module call
    eta1 = shg_efficiency(dk, L1)
    eta2 = shg_efficiency(dk, L2)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(x, eta1, color=INK, lw=2, label=r"$L=1$ mm")
    ax.plot(x, eta2, color=FLOW, lw=2, label=r"$L=2$ mm  (narrower)")
    null1 = 2.0 * np.pi / L1 * 1e-3                 # first null, rad/mm
    null2 = 2.0 * np.pi / L2 * 1e-3
    for xn, c in [(null1, INK), (null2, FLOW)]:
        ax.axvline(xn, color=c, lw=0.8, ls=":")
        ax.axvline(-xn, color=c, lw=0.8, ls=":")
    ax.axhline(0, color="#aaaaaa", lw=0.6)
    ax.set_xlim(-13, 13)
    ax.set_ylim(-0.03, 1.06)
    ax.set_xlabel(r"phase mismatch  $\Delta k$  (rad/mm)")
    ax.set_ylabel(r"SHG efficiency  $\eta/\eta_0$")
    ax.set_title(r"SHG phase matching: $\eta=\mathrm{sinc}^2(\Delta k\,L/2)$, null at $\Delta k L=2\pi$")
    ax.legend(loc="upper right", frameon=False)
    # realistic normal-dispersion mismatch -> micron coherence length (real funcs)
    dk_disp = shg_phase_mismatch(1.50, 1.53, lam)
    Lc = coherence_length(dk_disp)
    ax.annotate(r"normal dispersion $\Delta n=0.03$: $L_c=\pi/|\Delta k|\approx%.1f\ \mu$m"
                % (Lc * 1e6), xy=(0.025, 0.07), xycoords="axes fraction",
                fontsize=8.5, color=ALT)
    _save(fig, "fig1_shg_phase_matching.svg")
    caps["fig1_shg_phase_matching.svg"] = (
        "Second-harmonic conversion eta/eta0 = sinc^2(Delta k L/2) vs phase mismatch "
        "Delta k, from shg_efficiency for crystals of L=1 and 2 mm. It peaks at perfect "
        "phase matching Delta k=0 and first nulls at Delta k L = 2 pi (dotted), so the "
        "longer crystal has the narrower acceptance bandwidth. With normal dispersion "
        "(Delta n=0.03 at 1.064 um) the coherence length L_c = pi/|Delta k| from "
        "coherence_length is only ~8.9 um — hence the need for birefringent or "
        "quasi-phase matching to reach Delta k=0.")

    # Fig 2 — chi^(3) stimulated Brillouin gain: a Lorentzian peaked at the
    # acoustic shift nu_B = 2 n v_a / lambda (the kernel of SBS_Project).
    n, v_a, lam_p = 1.33, 1480.0, 532e-9           # water at 532 nm
    nu_B = brillouin_shift(n, v_a, lam_p)          # ~7.4 GHz
    f = np.linspace(nu_B - 0.45e9, nu_B + 0.45e9, 1600)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for gam, c, lab in [(100e6, INK, r"$\Gamma_B=100$ MHz"),
                        (200e6, FLOW, r"$\Gamma_B=200$ MHz")]:
        g = brillouin_gain(f, nu_B, gam)
        ax.plot(f * 1e-9, g, color=c, lw=2, label=lab)
        fhm = np.array([nu_B - 0.5 * gam, nu_B + 0.5 * gam])
        ax.plot(fhm * 1e-9, brillouin_gain(fhm, nu_B, gam),
                ls="none", marker="o", ms=5, color=c)   # half-max points, FWHM = Gamma_B
    ax.axhline(0.5, color="#888888", lw=1.0, ls="--", label=r"half maximum")
    ax.axvline(nu_B * 1e-9, color="#aaaaaa", lw=0.8)
    ax.set_xlim(f[0] * 1e-9, f[-1] * 1e-9)
    ax.set_ylim(0, 1.08)
    ax.set_xlabel(r"frequency  $\nu$  (GHz)")
    ax.set_ylabel(r"Brillouin gain  $g/g_0$")
    ax.set_title(r"Stimulated Brillouin gain: Lorentzian peaked at $\nu_B=2 n v_a/\lambda$")
    ax.annotate(r"$\nu_B=%.2f$ GHz" % (nu_B * 1e-9),
                xy=(nu_B * 1e-9, 1.0), xytext=(nu_B * 1e-9 + 0.12, 0.92),
                fontsize=9, color=ALT,
                arrowprops=dict(arrowstyle="->", color=ALT, lw=0.8))
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig2_brillouin_gain.svg")
    caps["fig2_brillouin_gain.svg"] = (
        "Stimulated-Brillouin gain spectrum g/g0 from brillouin_gain for water at 532 nm: "
        "a Lorentzian peaked at the acoustic shift nu_B = 2 n v_a/lambda ~ 7.40 GHz "
        "(brillouin_shift) with peak g0 and FWHM equal to the phonon damping Gamma_B. Dots "
        "mark the half-maximum points at nu_B +/- Gamma_B/2 for Gamma_B = 100 and 200 MHz. "
        "This lineshape g_B(nu) is exactly the kernel the user's SBS_Project fits; "
        "stimulated Raman is the same Lorentzian at the far larger (THz) vibrational shift.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
