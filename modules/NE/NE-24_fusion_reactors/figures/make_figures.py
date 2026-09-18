"""NE-24 figures -- how abruptly a plasma switches on, fusion power against
bremsstrahlung and the ignition temperatures, the Lawson and triple-product
curves, and what ICF must buy with density.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.

Palette note: ALT and STEEL are indistinguishable under deuteranopia, so any
panel using both also varies linestyle or marker (modules/CHANGELOG.md Known-bad).
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
from fusion import (                               # noqa: E402
    K_B_EV, HYDROGEN_IONIZATION_PRINTED, saha_ionization_fraction,
    sigma_v_dt, sigma_v_dd, fusion_power_density, bremsstrahlung_power_density,
    ignition_temperature, lawson_n_tau, triple_product, optimal_temperature,
    icf_confinement_time, areal_density_for_burn, gain_factor,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- the Saha switch.
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    t = np.logspace(2.4, 4.6, 400)
    ax.semilogx(t, [saha_ionization_fraction(x, 2e21) for x in t], color=INK,
                lw=2.4, label="$I$ = 13.598 eV (correct)")
    ax.semilogx(t, [saha_ionization_fraction(x, 2e21, HYDROGEN_IONIZATION_PRINTED)
                    for x in t], color=FLOW, lw=1.8, ls="--",
                label="$I$ = 13.06 eV (as printed)")
    ax.axvline(13150, color=ALT, ls=":", lw=1.6)
    ax.plot([13150], [0.95], "o", color=ALT, ms=9)
    ax.annotate("S&F's example:\n95% at 13 150 K\n(needs 13.06 eV)",
                xy=(13150, 0.95), xytext=(1200, 0.80), fontsize=8.5, color=ALT,
                arrowprops=dict(arrowstyle="->", color=ALT, lw=1.0))
    ax.annotate("at 293 K the fraction\nis $10^{-116}$", xy=(400, 0.05),
                fontsize=9, color=STEEL)
    ax.set_xlabel("temperature (K)")
    ax.set_ylabel("ionised fraction $f$")
    ax.set_ylim(-0.03, 1.05)
    ax.legend(fontsize=9, loc="center left")
    ax.set_title("There is no gentle approach to a plasma")
    _save(fig, "fig1_saha.svg")
    caps["fig1_saha.svg"] = (
        "The Saha equation (S&F Eq. 12.1) at n = 2e21 m^-3. Because I/kT sits in an exponential, "
        "the ionised fraction goes from 1e-4 at 5000 K to essentially 1 at 20 000 K -- there is "
        "no intermediate regime to work in, which is the first of fusion's three compounding "
        "difficulties. The dashed curve uses the 13.06 eV that §12.1.1 prints; the solid one uses "
        "hydrogen's actual 13.598 eV. The book's worked example (95% ionised at 13 150 K) "
        "reproduces to four figures only with 13.06, so the example is internally consistent "
        "with what looks like a transposed 13.60.")

    # Fig 2 -- power balance and ignition.
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    n = 1e15
    tt = np.logspace(math.log10(0.6), math.log10(100), 400)
    ax.loglog(tt, [fusion_power_density(n, x) for x in tt], color=INK, lw=2.4,
              label="D-T fusion")
    tdd = np.logspace(math.log10(0.6), math.log10(99), 300)
    ax.loglog(tdd, [fusion_power_density(n, x, "D-D") for x in tdd], color=LEAF,
              lw=2.2, ls="-.", label="D-D fusion")
    ax.loglog(tt, [bremsstrahlung_power_density(n, x) for x in tt], color=FLOW,
              lw=2.2, ls="--", label="bremsstrahlung ($Z$=1)")
    for r, col in (("D-T", INK), ("D-D", LEAF)):
        ti = ignition_temperature(r)
        ax.plot([ti], [bremsstrahlung_power_density(n, ti)], "o", color=col, ms=9)
        ax.annotate("$T_c$ = %.2e K" % (ti * 1e3 / K_B_EV),
                    xy=(ti, bremsstrahlung_power_density(n, ti)),
                    xytext=(ti * 0.30, bremsstrahlung_power_density(n, ti) * 12),
                    fontsize=8.5, color=col,
                    arrowprops=dict(arrowstyle="->", color=col, lw=1.0))
    ax.set_xlabel("plasma temperature $kT$ (keV)")
    ax.set_ylabel("power density (W cm$^{-3}$), $n=10^{15}$ cm$^{-3}$")
    ax.set_ylim(1e-6, 1e4)
    ax.legend(fontsize=8.5, loc="lower right")
    ax.set_title("S&F Fig. 12.2: where burning overtakes radiating")
    _save(fig, "fig2_ignition.svg")
    caps["fig2_ignition.svg"] = (
        "S&F Fig. 12.2, recomputed. Both fusion power and bremsstrahlung go as n^2, so the "
        "density cancels and the crossing -- the critical ignition temperature -- is a property "
        "of the fuel alone. The module's reactivity fits put it at 3.1e7 K for D-T and 5.3e8 K "
        "for D-D, against the book's 3e7 and 6e8: a 4% and 12% agreement that validates the "
        "fits, the bremsstrahlung coefficient and the identical-particle factors all at once. "
        "The factor of seventeen between them is why every serious experiment burns tritium, "
        "despite tritium being radioactive, scarce and impossible to stockpile.")

    # Fig 3 -- Lawson and the triple product.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.0))
    tt = np.logspace(math.log10(1.5), math.log10(150), 300)
    axL.loglog(tt, [lawson_n_tau(x) for x in tt], color=INK, lw=2.4, label="D-T")
    tdd = np.logspace(math.log10(1.5), math.log10(24), 200)
    axL.loglog(tdd, [lawson_n_tau(x, "D-D") for x in tdd], color=LEAF, lw=2.2,
               ls="-.", label="D-D")
    axL.set_xlabel("$kT$ (keV)")
    axL.set_ylabel("$n\\tau_E$  (s cm$^{-3}$)")
    axL.legend(fontsize=9)
    axL.set_title("Lawson: $n\\tau_E \\geq 12kT/(E_c\\langle\\sigma v\\rangle)$")

    axR.semilogx(tt, [triple_product(x) for x in tt], color=INK, lw=2.4,
                 label="triple product $n\\tau_E T$")
    t_opt, v_opt = optimal_temperature("D-T")
    axR.plot([t_opt], [v_opt], "o", color=ALT, ms=9)
    axR.annotate("minimum at %.0f keV\n%.1e keV s cm$^{-3}$" % (t_opt, v_opt),
                 xy=(t_opt, v_opt), xytext=(2.2, 1.4e16), fontsize=8.5, color=ALT,
                 arrowprops=dict(arrowstyle="->", color=ALT, lw=1.0))
    axR.axhline(2e15, color=FLOW, ls="--", lw=1.6)
    axR.annotate("S&F Eq. (12.14): $> 2\\times10^{15}$", xy=(20, 2.3e15),
                 fontsize=8.5, color=FLOW)
    axR.axvspan(t_opt / 1.7, t_opt * 1.7, color=LEAF, alpha=0.12, lw=0)
    axR.annotate("a factor of 3 in $T$\ncosts under 35%", xy=(t_opt, 6e15),
                 fontsize=8.5, color=LEAF, ha="center")
    axR.set_yscale("log")
    axR.set_xlabel("$kT$ (keV)")
    axR.set_ylabel("$n\\tau_E T$  (keV s cm$^{-3}$)")
    axR.set_ylim(1e15, 3e16)
    axR.set_title("...and why the triple product replaced it")
    fig.tight_layout()
    _save(fig, "fig3_lawson.svg")
    caps["fig3_lawson.svg"] = (
        "Left: the Lawson product (S&F Eq. 12.10). D-T bottoms out near 1e14 s/cm^3 and D-D "
        "needs 40 to 80 times more at every temperature the fits can both be evaluated at. "
        "Right: the triple product (Eq. 12.11), whose minimum is 3e15 keV s cm^-3 -- consistent "
        "with the book's stated bound of 2e15. The shaded band shows why it took over as the "
        "figure of merit: a factor of three in temperature around the optimum costs under 35%, "
        "so the number characterises the CONFINEMENT SCHEME rather than the operating point. "
        "Note also that its minimum sits at a lower temperature than the Lawson product's, "
        "exactly as Fig. 12.3 shows.")

    # Fig 4 -- ICF and the gain factor.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.0))
    radii = np.logspace(-3, -0.7, 200)
    for kt, col, ls in ((5.0, LEAF, "-."), (10.0, INK, "-"), (40.0, FLOW, "--")):
        axL.loglog(radii * 1e4, [icf_confinement_time(r, kt) for r in radii],
                   color=col, lw=2.2, ls=ls, label="$kT$ = %g keV" % kt)
    axL.axhspan(1e-9, 1e-8, color=ALT, alpha=0.12, lw=0)
    axL.annotate("ICF pulse lengths\n1-10 ns", xy=(20, 3e-9), fontsize=8.5,
                 color=ALT)
    axL.plot([500], [icf_confinement_time(0.05, 10.0)], "o", color=INK, ms=8)
    axL.annotate("a 1 mm pellet:\n0.8 ns", xy=(500, icf_confinement_time(0.05, 10.0)),
                 xytext=(60, 2e-10), fontsize=8.5, color=INK,
                 arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
    axL.set_xlabel("compressed radius ($\\mu$m)")
    axL.set_ylabel("$\\tau_E = R\\sqrt{m/kT}$  (s)")
    axL.legend(fontsize=8.5)
    axL.set_title("ICF has nanoseconds, not seconds")

    phis = np.linspace(0.01, 0.6, 200)
    axR.plot(100 * phis, [areal_density_for_burn(p) for p in phis], color=INK, lw=2.4)
    for p, lab in ((0.1, "10%"), (0.3, "a third")):
        axR.plot([100 * p], [areal_density_for_burn(p)], "o", color=FLOW, ms=8)
        axR.annotate("%s burned:\n$\\rho R$ = %.1f g/cm$^2$" % (lab, areal_density_for_burn(p)),
                     xy=(100 * p, areal_density_for_burn(p)),
                     xytext=(100 * p - 8, areal_density_for_burn(p) + 1.4),
                     fontsize=8.5, color=FLOW)
    axR.axhline(0.02, color=LEAF, ls="--", lw=1.6)
    axR.annotate("an uncompressed 1 mm pellet: $\\rho R\\approx 0.02$",
                 xy=(5, 0.35), fontsize=8.5, color=LEAF)
    axR.set_xlabel("burn fraction (%)")
    axR.set_ylabel("required $\\rho R$  (g cm$^{-2}$)")
    axR.set_ylim(0, 9)
    axR.set_title("...so it must buy $n\\tau$ with compression")
    fig.tight_layout()
    _save(fig, "fig4_icf.svg")
    caps["fig4_icf.svg"] = (
        "Left: S&F Eq. (12.15). A millimetre pellet at 10 keV is inertially confined for about "
        "0.8 ns -- eight orders of magnitude less than a tokamak's energy confinement time -- so "
        "the Lawson product n*tau has to be found entirely in n. Right: the consequence, using "
        "the standard burn-fraction relation that S&F gesture at with 'only a small portion of "
        "the pellet fuel actually fuses'. Burning a third of the fuel needs rho*R = 2.6 g/cm^2 "
        "against about 0.02 for an uncompressed pellet -- a factor of 130 in areal density, "
        "which is a thousandfold in volume density. That is the entire engineering problem of "
        "inertial confinement stated in one number.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
