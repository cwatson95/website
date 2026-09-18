"""NE-05 figures -- the 1.022 MeV beta-plus window, alpha line energies against
Q, and the sharp-versus-continuous contrast between alpha and beta spectra.

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
from decay_modes import (                          # noqa: E402
    TWO_ME_MEV, load_atomic_masses, has_nuclide, daughter_of,
    q_alpha, alpha_kinetic_energy, q_beta_minus, q_beta_plus,
    q_electron_capture, measured_emissions,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    t = load_atomic_masses()

    # Fig 1 -- the electron-capture-only window.
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    qec, qbp, labels = [], [], []
    for A, Z, name in [(7, 4, "7Be"), (55, 26, "55Fe"), (51, 24, "51Cr"),
                       (125, 53, "125I"), (145, 62, "145Sm"), (22, 11, "22Na"),
                       (18, 9, "18F"), (11, 6, "11C"), (64, 29, "64Cu"),
                       (27, 14, "27Si"), (40, 19, "40K")]:
        Ad, Zd = daughter_of(A, Z, "ec")
        if not has_nuclide(Ad, Zd, t):
            continue
        qec.append(q_electron_capture(A, Z, t))
        qbp.append(q_beta_plus(A, Z, t))
        labels.append(name)
    y = np.arange(len(labels))
    ax.barh(y - 0.19, qec, height=0.36, color=STEEL, label=r"$Q_{\rm EC}$")
    ax.barh(y + 0.19, qbp, height=0.36, color=FLOW, label=r"$Q_{\beta^+}$")
    ax.axvline(0, color="k", lw=1.1)
    ax.axvspan(0, TWO_ME_MEV, color="0.88", zorder=0)
    ax.text(TWO_ME_MEV / 2, len(labels) - 0.3, "EC-only\nwindow", ha="center",
            fontsize=8.5, color="0.35")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("$Q$ (MeV)")
    ax.set_title(r"$\beta^+$ costs $2m_ec^2=1.022$ MeV more than electron capture")
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    _save(fig, "fig1_ec_window.svg")
    caps["fig1_ec_window.svg"] = (
        "Electron-capture and positron-emission Q-values for the same parent-daughter "
        "pairs (q_electron_capture, q_beta_plus). The two always differ by exactly 2 m_e c^2 "
        "= 1.022 MeV, so nuclides whose Q_EC falls in the shaded window can only capture: "
        "7Be, 55Fe, 51Cr, 125I and 145Sm are all pure EC emitters.")

    # Fig 2 -- alpha kinetic energy vs Q, showing the ~98% share.
    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    Qs, Es, names = [], [], []
    for (Z, A) in sorted(t):
        if A < 200 or Z < 80:
            continue
        Ad, Zd = daughter_of(A, Z, "alpha")
        if not has_nuclide(Ad, Zd, t):
            continue
        q = q_alpha(A, Z, t)
        if q <= 0:
            continue
        Qs.append(q)
        Es.append(alpha_kinetic_energy(A, Z, t))
    ax.plot(Qs, Es, ".", color=STEEL, ms=3)
    lim = [min(Qs) * 0.95, max(Qs) * 1.03]
    ax.plot(lim, lim, "-", color="0.6", lw=1.0, label=r"$E_\alpha=Q$ (no recoil)")
    for A, Z, lab in [(238, 92, r"$^{238}$U"), (226, 88, r"$^{226}$Ra"),
                      (210, 84, r"$^{210}$Po"), (241, 95, r"$^{241}$Am")]:
        q, e = q_alpha(A, Z, t), alpha_kinetic_energy(A, Z, t)
        ax.plot([q], [e], "o", color=FLOW, ms=6)
        ax.annotate(lab, xy=(q, e), xytext=(q + 0.06, e - 0.28), fontsize=9, color=FLOW)
    ax.set_xlabel(r"$Q_\alpha$ (MeV)")
    ax.set_ylabel(r"$E_\alpha$ (MeV)")
    ax.set_title(r"The alpha takes $A_D/(A_D+4)\approx98\%$ of the decay energy")
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    _save(fig, "fig2_alpha_energy_split.svg")
    caps["fig2_alpha_energy_split.svg"] = (
        "Alpha kinetic energy against decay Q-value for every heavy alpha emitter in "
        "Appendix B (alpha_kinetic_energy). Two-body kinematics fixes the split at "
        "M_D/(M_D+M_alpha), so the points sit just below the no-recoil diagonal: the "
        "daughter keeps roughly 2%, which is still ~100 keV and enough to shatter the "
        "host molecule.")

    # Fig 3 -- sharp alpha line vs continuous beta spectrum.
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    E_a = alpha_kinetic_energy(226, 88, t)
    ax.vlines([E_a], 0, 1.0, color=FLOW, lw=2.4, label=r"$^{226}$Ra alpha line")
    Q = q_beta_minus(90, 38, t)
    x = np.linspace(1e-4, Q, 400)
    # Fermi-function-free approximate beta shape: p E (Q-E)^2
    p = np.sqrt(x * (x + 2 * 0.511))
    shape = p * (x + 0.511) * (Q - x) ** 2
    ax.plot(x, shape / shape.max(), color=INK, lw=1.8, label=r"$^{90}$Sr beta spectrum")
    ax.axvline(Q, color=INK, ls=":", lw=1.2)
    ax.annotate("endpoint = $Q$ = %.3f MeV" % Q, xy=(Q, 0.42), xytext=(Q + 0.15, 0.55),
                fontsize=9, color=INK, arrowprops=dict(arrowstyle="->", color=INK))
    ax.set_xlim(0, 5.4)
    ax.set_ylim(0, 1.15)
    ax.set_xlabel("particle kinetic energy (MeV)")
    ax.set_ylabel("relative intensity")
    ax.set_title("Two-body decay gives a line; three-body decay gives a spectrum")
    ax.legend(frameon=False, fontsize=9)
    _save(fig, "fig3_line_vs_spectrum.svg")
    caps["fig3_line_vs_spectrum.svg"] = (
        "The 226Ra alpha at its computed 4.784 MeV (a single sharp energy, because the "
        "decay is two-body) against the 90Sr beta spectrum, which runs continuously from "
        "zero to the endpoint Q = 0.546 MeV because an antineutrino shares the energy. "
        "Only the endpoint carries the mass information.")

    # Fig 4 -- the 60Co decay energy budget closing across two appendices.
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    q = q_beta_minus(60, 27, t) * 1000
    endpoint = max(float(r["E_max_keV"])
                   for r in measured_emissions("60Co", "beta") if r["E_max_keV"])
    gammas = sorted(float(r["E_keV"])
                    for r in measured_emissions("60Co", "gamma_xray") if r["E_keV"])
    parts = [("beta endpoint", endpoint, FLOW)] + \
            [("gamma %.1f keV" % g, g, INK if i == 0 else ALT) for i, g in enumerate(gammas)]
    left = 0.0
    for lab, v, col in parts:
        ax.barh([0], [v], left=[left], color=col, height=0.45)
        ax.text(left + v / 2, 0, "%.1f" % v, ha="center", va="center",
                fontsize=8.5, color="white")
        left += v
    ax.barh([1], [q], color=STEEL, height=0.45)
    ax.text(q / 2, 1, "$Q_{\\beta^-}$ from masses = %.1f keV" % q, ha="center",
            va="center", fontsize=9, color="white")
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Appendix D\n(measured)", "Appendix B\n(masses)"], fontsize=9)
    ax.set_xlabel("energy (keV)")
    ax.set_title(r"$^{60}$Co: the cascade closes on $Q$ to 0.3 keV")
    ax.set_xlim(0, q * 1.08)
    _save(fig, "fig4_cobalt60_budget.svg")
    caps["fig4_cobalt60_budget.svg"] = (
        "Energy budget of 60Co decay. The beta endpoint plus the two gamma-ray energies "
        "from Appendix D sum to 2823.6 keV, against 2823.9 keV for Q computed from the "
        "Appendix B atomic masses -- two independent data sets closing to 0.3 keV. Almost "
        "all the decay energy leaves as the two photons, which is why 60Co is a gamma source.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
