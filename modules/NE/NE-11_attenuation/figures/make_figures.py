"""NE-11 figures -- exponential attenuation in mean free paths, mass
coefficients across materials and energies, geometric vs material attenuation,
and the path-length distribution.

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
from attenuation import (                          # noqa: E402
    MATERIALS, load_photon_coefficients, mass_coefficient, linear_coefficient,
    uncollided_intensity, path_length_pdf, mean_free_path, half_thickness,
    tenth_thickness, point_source_flux, point_source_flux_shielded,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"
COLOURS = {"water": STEEL, "concrete": LEAF, "iron": ALT, "lead": FLOW, "air": "#8a8a5a"}


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- attenuation: the same curve for every material, in mfp.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 3.7))
    x_cm = np.linspace(0, 60, 400)
    for m in ("water", "concrete", "iron", "lead"):
        mu = linear_coefficient(m, 1.0)
        axL.semilogy(x_cm, np.exp(-mu * x_cm), color=COLOURS[m], lw=1.9,
                     label="%s ($\\mu$ = %.3f cm$^{-1}$)" % (m, mu))
    axL.set_xlabel("thickness (cm)")
    axL.set_ylabel("uncollided fraction")
    axL.set_ylim(1e-6, 1.5)
    axL.legend(fontsize=8)
    axL.set_title("In centimetres: four curves")

    n_mfp = np.linspace(0, 14, 300)
    axR.semilogy(n_mfp, np.exp(-n_mfp), color=INK, lw=2.4)
    for m in ("water", "concrete", "iron", "lead"):
        mu = linear_coefficient(m, 1.0)
        axR.plot([mu * 10.0], [math.exp(-mu * 10.0)], "o", color=COLOURS[m], ms=8)
        axR.annotate("10 cm of\n%s" % m, xy=(mu * 10.0, math.exp(-mu * 10.0)),
                     xytext=(mu * 10.0 + 0.5, math.exp(-mu * 10.0) * 2.5),
                     fontsize=8, color=COLOURS[m])
    axR.set_xlabel("optical thickness $\\mu x$ (mean free paths)")
    axR.set_ylim(1e-6, 1.5)
    axR.set_title("In mean free paths: one curve")
    fig.tight_layout()
    _save(fig, "fig1_attenuation.svg")
    caps["fig1_attenuation.svg"] = (
        "Uncollided transmission of 1 MeV photons (uncollided_intensity). Plotted against "
        "thickness in centimetres the four materials look unrelated; plotted against "
        "optical thickness mu*x they collapse onto a single exponential, because that "
        "product is the only variable the physics depends on. This is why shielding is "
        "specified in mean free paths, and why 10 cm of lead (7.7 mfp) and 109 cm of water "
        "do the same job.")

    # Fig 2 -- mass coefficients: the three photon processes.
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    for m in ("water", "iron", "lead"):
        rows = load_photon_coefficients(m)
        e = [r[0] for r in rows]
        ax.loglog(e, [r[1]["total"] for r in rows], color=COLOURS[m], lw=2.0, label=m)
    rows = load_photon_coefficients("lead")
    e = [r[0] for r in rows]
    ax.loglog(e, [r[1]["ph"] for r in rows], color=FLOW, lw=1.0, ls=":")
    ax.loglog(e, [r[1]["c"] for r in rows], color=FLOW, lw=1.0, ls="--")
    ax.axvline(1.022, color="0.6", lw=1.1)
    ax.text(1.1, 1.6e-3, "pair production\nthreshold\n1.022 MeV", fontsize=8, color="0.4")
    ax.annotate("K edge (lead, 88 keV)", xy=(0.088, 2.0), xytext=(0.13, 12),
                fontsize=8, color=FLOW,
                arrowprops=dict(arrowstyle="->", color=FLOW, lw=1.0))
    ax.set_xlabel("photon energy (MeV)")
    ax.set_ylabel("$\\mu/\\rho$  (cm$^2$/g)")
    ax.set_xlim(1e-2, 1e2)
    ax.set_ylim(1e-3, 1e2)
    ax.legend(fontsize=9)
    ax.set_title("Mass attenuation coefficients (Appendix C.3)")
    _save(fig, "fig2_mass_coefficients.svg")
    caps["fig2_mass_coefficients.svg"] = (
        "Total mass attenuation coefficient from the extracted Appendix C.3 "
        "(mass_coefficient), with lead's photoelectric (dotted) and Compton (dashed) "
        "components shown separately. Because mu/rho is per GRAM, the three materials "
        "nearly coincide above ~1 MeV -- lead is a good shield because it is dense, not "
        "because it is special. Below ~0.5 MeV the photoelectric effect's steep Z "
        "dependence takes over and lead pulls away by two orders of magnitude. Details "
        "in NE-12.")

    # Fig 3 -- geometric vs material attenuation.
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    s = 3.7e10
    r = np.linspace(50, 1000, 400)
    ax.loglog(r / 100.0, [point_source_flux(s, x) for x in r], color=STEEL, lw=2.2,
              label="distance only  ($1/r^2$)")
    mu_pb = linear_coefficient("lead", 1.0)
    for t, ls in [(2.0, "--"), (5.0, "-."), (10.0, ":")]:
        ax.loglog(r / 100.0, [point_source_flux_shielded(s, x, mu_pb, t) for x in r],
                  color=FLOW, lw=1.8, ls=ls, label="+ %g cm lead (%.1f mfp)" % (t, mu_pb * t))
    ax.set_xlabel("distance from source (m)")
    ax.set_ylabel("uncollided flux density (cm$^{-2}$ s$^{-1}$)")
    ax.legend(fontsize=8.5)
    ax.set_title("1 Ci of a 1 MeV emitter: shielding beats distance")
    _save(fig, "fig3_point_source.svg")
    caps["fig3_point_source.svg"] = (
        "Uncollided flux from a 1 Ci point source (point_source_flux_shielded). The two "
        "attenuations behave completely differently: distance gives a power law, so ten "
        "times further buys a factor of 100, while material gives an exponential, so 10 cm "
        "of lead buys a factor of 2300 and the next 10 cm buys the same factor again. This "
        "is why shielding, not standoff, is the tool of choice once space is limited.")

    # Fig 4 -- the path-length distribution, and its identity with decay.
    fig, ax = plt.subplots(figsize=(6.4, 3.7))
    mu = linear_coefficient("water", 1.0)
    x = np.linspace(0, 70, 500)
    ax.plot(x, [path_length_pdf(mu, v) for v in x], color=INK, lw=2.1,
            label="$p(x) = \\mu e^{-\\mu x}$")
    mfp, x12 = mean_free_path(mu), half_thickness(mu)
    ax.axvline(mfp, color=FLOW, ls="--", lw=1.4)
    ax.axvline(x12, color=STEEL, ls=":", lw=1.4)
    ax.annotate("mean free path\n%.1f cm  ($1/\\mu$)" % mfp, xy=(mfp, path_length_pdf(mu, mfp)),
                xytext=(mfp + 6, 0.045), fontsize=9, color=FLOW,
                arrowprops=dict(arrowstyle="->", color=FLOW, lw=1.0))
    ax.annotate("half-thickness\n%.1f cm  ($\\ln 2/\\mu$)" % x12, xy=(x12, path_length_pdf(mu, x12)),
                xytext=(x12 + 14, 0.062), fontsize=9, color=STEEL,
                arrowprops=dict(arrowstyle="->", color=STEEL, lw=1.0))
    ax.fill_between(x, 0, [path_length_pdf(mu, v) for v in x],
                    where=(x <= x12), color=STEEL, alpha=0.18)
    ax.text(2.0, 0.012, "half of all\nphotons\ninteract here", fontsize=8.5, color="0.35")
    ax.set_xlabel("distance to first interaction (cm)")
    ax.set_ylabel("probability density (cm$^{-1}$)")
    ax.set_xlim(0, 70)
    ax.set_ylim(0, 0.082)
    ax.legend(fontsize=9)
    ax.set_title("Where a 1 MeV photon first interacts in water")
    _save(fig, "fig4_path_length.svg")
    caps["fig4_path_length.svg"] = (
        "Distribution of the distance a photon travels before its first interaction "
        "(path_length_pdf). It is exponential, with mean 1/mu and median ln2/mu -- exactly "
        "the decay-time distribution of NE-06 with distance in place of time and mu in "
        "place of lambda. The mean exceeds the median because the tail is long, which is "
        "the same reason a nuclide's mean life is 1.44 half-lives.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
