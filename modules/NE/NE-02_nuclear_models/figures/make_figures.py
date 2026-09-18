"""NE-02 figures -- the binding-energy curve, the SEMF term breakdown, the chart
of the nuclides with the line of stability, and the A=110 mass parabolas.

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
from nuclear_models import (                       # noqa: E402
    A_V, A_S, A_C, A_A, MAGIC_NUMBERS,
    semf_terms, semf_binding_energy, semf_binding_energy_per_nucleon,
    most_stable_Z, most_stable_Z_rounded, isobar_masses, parity_class,
    load_atomic_masses, measured_binding_energy, is_doubly_magic,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    table = load_atomic_masses()

    # Fig 1 -- B/A: the SEMF curve over the measured points.
    meas_A, meas_B = [], []
    for (Z, A), _m in sorted(table.items()):
        if A < 2 or Z < 1:
            continue
        if abs(Z - most_stable_Z(A)) > 0.6:      # keep the valley floor only
            continue
        try:
            meas_B.append(measured_binding_energy(A, Z, table) / A)
            meas_A.append(A)
        except KeyError:
            continue
    As = np.arange(4, 250)
    semf = [semf_binding_energy_per_nucleon(int(a), most_stable_Z_rounded(int(a))) for a in As]

    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    ax.plot(meas_A, meas_B, ".", color=STEEL, ms=3.5, label="measured (Appendix B)")
    ax.plot(As, semf, color=INK, lw=1.7, label="liquid drop model")
    peak = int(As[int(np.argmax(semf))])
    ax.axvline(peak, color=FLOW, lw=1.0, ls=":")
    ax.annotate("peak near A=%d\n(8.7 MeV/nucleon)" % peak, xy=(peak, max(semf)),
                xytext=(peak + 45, 7.2), fontsize=9, color=FLOW,
                arrowprops=dict(arrowstyle="->", color=FLOW))
    ax.annotate("fusion\nreleases energy", xy=(20, 6.0), fontsize=9, color="0.35", ha="center")
    ax.annotate("fission\nreleases energy", xy=(215, 6.0), fontsize=9, color="0.35", ha="center")
    ax.set_xlabel("mass number $A$")
    ax.set_ylabel("$B/A$ (MeV per nucleon)")
    ax.set_ylim(0, 9.6)
    ax.set_title("Binding energy per nucleon")
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    _save(fig, "fig1_binding_energy_curve.svg")
    caps["fig1_binding_energy_curve.svg"] = (
        "Binding energy per nucleon from the semi-empirical mass formula "
        "(semf_binding_energy_per_nucleon, evaluated along the line of stability) over "
        "values computed from the measured masses of Appendix B. The peak near A=56 is "
        "why fusing light nuclei and fissioning heavy ones both release energy.")

    # Fig 2 -- how the five terms build that curve (S&F Ch.3 Prob. 9).
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    Zs = np.array([most_stable_Z_rounded(int(a)) for a in As])
    ax.axhline(A_V, color=INK, lw=1.6, label=r"volume  $+a_v$")
    ax.plot(As, A_S * As ** (-1.0 / 3.0), color=FLOW, lw=1.5,
            label=r"$-$surface  $a_sA^{-1/3}$")
    ax.plot(As, A_C * Zs ** 2 / As ** (4.0 / 3.0), color=ALT, lw=1.5,
            label=r"$-$Coulomb  $a_cZ^2A^{-4/3}$")
    ax.plot(As, A_A * (As - 2 * Zs) ** 2 / As ** 2, color=LEAF, lw=1.5,
            label=r"$-$asymmetry  $a_a(A-2Z)^2A^{-2}$")
    ax.plot(As, semf, color="k", lw=2.0, ls="--", label="total $B/A$")
    ax.set_xlabel("mass number $A$")
    ax.set_ylabel("MeV per nucleon")
    ax.set_ylim(0, 17)
    ax.set_title("Where the binding-energy curve comes from")
    ax.legend(frameon=False, fontsize=8.5, ncol=2)
    _save(fig, "fig2_semf_terms.svg")
    caps["fig2_semf_terms.svg"] = (
        "The liquid-drop terms per nucleon (from semf_terms) against A, with corrections "
        "plotted as positive penalties. The constant volume term is the ceiling; the "
        "surface penalty decays as A^(-1/3) and makes B/A rise, while the Coulomb penalty "
        "grows as A^(2/3) and makes it fall. Their crossover sets the iron peak.")

    # Fig 3 -- the chart of the nuclides, coloured by shell surplus.
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    zz, nn, resid = [], [], []
    for (Z, A), _m in table.items():
        N = A - Z
        if Z < 1 or N < 1 or A > 250:
            continue
        try:
            r = measured_binding_energy(A, Z, table) - semf_binding_energy(A, Z)
        except (KeyError, ValueError):
            continue
        zz.append(Z); nn.append(N); resid.append(r)
    sc = ax.scatter(nn, zz, c=resid, s=1.6, cmap="RdBu_r", vmin=-12, vmax=12)
    line_A = np.arange(2, 251)
    line_Z = np.array([most_stable_Z(int(a)) for a in line_A])
    ax.plot(line_A - line_Z, line_Z, color="k", lw=1.4, label="Eq. (3.18) stability line")
    ax.plot([0, 160], [0, 160], color="0.5", lw=1.0, ls=":", label="$N=Z$")
    for m in MAGIC_NUMBERS:
        ax.axhline(m, color="0.75", lw=0.6, zorder=0)
        ax.axvline(m, color="0.75", lw=0.6, zorder=0)
    ax.set_xlim(0, 160); ax.set_ylim(0, 105)
    ax.set_xlabel("neutron number $N$")
    ax.set_ylabel("proton number $Z$")
    ax.set_title("Chart of the nuclides: measured $-$ liquid-drop binding energy")
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    fig.colorbar(sc, ax=ax, label="residual (MeV)", shrink=0.85)
    _save(fig, "fig3_chart_of_nuclides.svg")
    caps["fig3_chart_of_nuclides.svg"] = (
        "Every nuclide of Appendix B in the N-Z plane, coloured by measured binding energy "
        "minus the liquid-drop prediction. The stability line of Eq. (3.18) bends away from "
        "N=Z as Coulomb repulsion grows; red ridges sit on the magic numbers (grey lines), "
        "extra binding the smooth drop model cannot reproduce.")

    # Fig 4 -- mass parabolas for A=110 (S&F Fig. 3.13).
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    rows = isobar_masses(110, 42, 53)
    for cls, col, mk in [("even-even", INK, "o"), ("odd-odd", FLOW, "s")]:
        pts = [(Z, (m - 109.9) * 1000) for Z, m in rows if parity_class(110, Z) == cls]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], mk + "-", color=col,
                ms=5, lw=1.3, label=cls)
    zstar = most_stable_Z(110)
    ax.axvline(zstar, color="0.45", ls=":", lw=1.2)
    ax.annotate("Eq. (3.18): $Z=%.2f$" % zstar, xy=(zstar, 28), xytext=(zstar + 0.3, 30),
                fontsize=9, color="0.3")
    for Z, lab in [(46, "$^{110}$Pd"), (48, "$^{110}$Cd")]:
        m = dict(rows)[Z]
        ax.annotate(lab + "\n(stable)", xy=(Z, (m - 109.9) * 1000), xytext=(Z - 0.4, -4),
                    fontsize=8.5, ha="center", color=LEAF)
    ax.set_xlabel("proton number $Z$")
    ax.set_ylabel("mass $-$ 109.9 u  (mu)")
    ax.set_title("Mass parabolas of the $A=110$ isobar")
    ax.legend(frameon=False, fontsize=9)
    _save(fig, "fig4_mass_parabolas.svg")
    caps["fig4_mass_parabolas.svg"] = (
        "Liquid-drop masses across the A=110 isobar (isobar_masses), split by the pairing "
        "term into an even-even branch and an odd-odd branch 2a_p/sqrt(A) above it. The two "
        "stable nuclides, 110Pd and 110Cd, are both even-even and straddle the Eq. (3.18) "
        "minimum at Z=47.4 -- the structure of S&F Fig. 3.13.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
