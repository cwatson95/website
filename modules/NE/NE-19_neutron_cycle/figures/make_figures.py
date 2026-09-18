"""NE-19 figures -- the four factors pulling against each other, why only heavy
water moderates natural uranium, what lumping the fuel buys, and how leakage sets
the critical size.

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
from neutron_cycle import (                        # noqa: E402
    FUEL_THERMAL_AVERAGED, MODERATOR_THERMAL, OPTIMUM_RATIOS, LATTICE_TABLE,
    westcott_averaged_cross_section, thermal_utilization_homogeneous,
    resonance_escape_homogeneous, k_infinity, four_factor_formula_as_printed,
    diffusion_length_squared, thermal_nonleakage, fast_nonleakage,
    geometric_buckling, critical_radius_sphere, eta_of_uranium,
    resonance_integral_rod, resonance_escape_lattice, AVOGADRO,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"
NATURAL_U = {"234U": 0.000055, "235U": 0.007204, "238U": 0.992745}


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    sig_u = sum(a * FUEL_THERMAL_AVERAGED[k]["sigma_a"] for k, a in NATURAL_U.items())
    eta_nat = eta_of_uranium(0.007204)

    # Fig 1 -- the factors pulling against each other (S&F Fig. 10.4).
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.0), sharey=True)
    for ax, mod, sig_mod, label in (
            (axL, "graphite", westcott_averaged_cross_section(0.00386), "graphite"),
            (axR, "heavy water", westcott_averaged_cross_section(0.001194), "heavy water")):
        ratios = np.logspace(1, 4, 300)
        f = [thermal_utilization_homogeneous(sig_u, sig_mod, r) for r in ratios]
        p = [resonance_escape_homogeneous(0.992745 / r, mod) for r in ratios]
        k = [k_infinity(eta_nat, pp, ff) for pp, ff in zip(p, f)]
        ax.semilogx(ratios, f, color=FLOW, lw=2.0, ls="--", label="$f$ (thermal utilization)")
        ax.semilogx(ratios, p, color=LEAF, lw=2.0, ls="-.", label="$p$ (resonance escape)")
        ax.semilogx(ratios, k, color=INK, lw=2.6, label="$k_\\infty=\\eta p f$")
        ax.axhline(1.0, color="0.8", lw=1.0, zorder=0)
        best = int(np.argmax(k))
        ax.plot([ratios[best]], [k[best]], "o", color=ALT, ms=8)
        ax.annotate("max $k_\\infty$ = %.3f\nat $N_M/N_U$ = %.0f" % (k[best], ratios[best]),
                    xy=(ratios[best], k[best]), xytext=(ratios[best] * 0.06, 0.45),
                    fontsize=8.5, color=ALT,
                    arrowprops=dict(arrowstyle="->", color=ALT, lw=1.0))
        ax.set_xlabel("moderator-to-uranium atom ratio $N_M/N_U$")
        ax.set_title("natural uranium in %s" % label)
    axL.set_ylabel("factor")
    axL.set_ylim(0, 1.45)
    axL.legend(fontsize=8.5, loc="upper left")
    fig.tight_layout()
    _save(fig, "fig1_four_factors.svg")
    caps["fig1_four_factors.svg"] = (
        "Why there is an optimum moderator-to-fuel ratio (S&F Fig. 10.4, computed here from "
        "Eqs. (10.9) and (10.11) for natural uranium). Adding moderator raises the resonance "
        "escape probability p -- neutrons cross 238U's resonances in fewer, larger steps -- and "
        "lowers the thermal utilization f, because the moderator itself starts absorbing the "
        "thermal neutrons. The two pull against each other, so k_inf has an interior maximum. "
        "In graphite that maximum is below 1 and no homogeneous natural-uranium reactor is "
        "possible; heavy water absorbs so weakly that it can be piled on until p is high "
        "without killing f, and its maximum clears 1.")

    # Fig 2 -- Table 10.5, and the missing epsilon.
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    mods = ["H2O", "D2O", "Be", "C"]
    x = np.arange(len(mods))
    with_eps = [k_infinity(v[2], v[4], v[3], v[1]) for v in
                (OPTIMUM_RATIOS[m] for m in mods)]
    without = [four_factor_formula_as_printed(v[2], v[4], v[3]) for v in
               (OPTIMUM_RATIOS[m] for m in mods)]
    ax.bar(x - 0.19, with_eps, 0.36, color=INK, edgecolor="white", lw=0.8,
           label="$\\epsilon\\,p\\,f\\,\\eta$  (Tables 10.5, 10.8)")
    ax.bar(x + 0.19, without, 0.36, color=FLOW, hatch="///", edgecolor="white",
           lw=0.8, label="$p\\,f\\,\\eta$  (Eq. 10.17 as printed)")
    ax.axhline(1.0, color=ALT, ls="--", lw=1.6)
    ax.annotate("critical", xy=(3.35, 1.02), fontsize=9, color=ALT)
    for i, (a, b) in enumerate(zip(with_eps, without)):
        ax.text(i - 0.19, a + 0.015, "%.3f" % a, ha="center", fontsize=8.5)
        if abs(a - b) > 1e-3:
            ax.text(i + 0.19, b + 0.015, "%.3f" % b, ha="center", fontsize=8.5,
                    color=FLOW)
    ax.set_xticks(x)
    ax.set_xticklabels(["%s\n$N_M/N_U$=%g" % (m, OPTIMUM_RATIOS[m][0]) for m in mods])
    ax.set_ylabel("$k_\\infty$ at the optimum ratio")
    ax.set_ylim(0, 1.32)
    ax.legend(fontsize=8.5, loc="upper left")
    ax.set_title("Natural uranium, homogeneously moderated")
    _save(fig, "fig2_optimum_moderators.svg")
    caps["fig2_optimum_moderators.svg"] = (
        "S&F Table 10.5: the best k_inf a homogeneous natural-uranium mixture can reach in each "
        "moderator. Only heavy water clears 1 -- which is the reason enrichment plants exist, "
        "and the reason the only natural-uranium power reactor in commercial service is the "
        "CANDU. The hatched bars show what S&F's printed Eq. (10.17) gives: it omits the fast "
        "fission factor eps and calls the remaining three-factor product the 'four-factor "
        "formula'. Water is the only row with eps != 1, and it is exactly the row that "
        "discriminates -- 0.888 with eps against 0.845 without. Tables 10.5 and 10.8 both "
        "include eps, so the tables and the equation disagree.")

    # Fig 3 -- what lumping buys (Table 10.8).
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.0))
    pitches = sorted(LATTICE_TABLE)
    axL.plot(pitches, [LATTICE_TABLE[a][3] for a in pitches], "o-", color=LEAF,
             lw=2.0, label="$p$, lattice")
    axL.plot(pitches, [LATTICE_TABLE[a][2] for a in pitches], "s--", color=FLOW,
             lw=2.0, label="$f$, lattice")
    axL.plot(pitches, [LATTICE_TABLE[a][4] for a in pitches], "^-", color=INK,
             lw=2.6, label="$k_\\infty$, lattice")
    hom_p = []
    for a in pitches:
        vm_vf = (a ** 2 - math.pi * 1.25 ** 2) / (math.pi * 1.25 ** 2)
        hom_p.append(resonance_escape_homogeneous(0.992745 / vm_vf, "graphite"))
    axL.plot(pitches, hom_p, ":", color=STEEL, lw=2.0,
             label="$p$, same ratio homogeneous")
    axL.axhline(1.0, color="0.8", lw=1.0, zorder=0)
    best = max(LATTICE_TABLE, key=lambda a: LATTICE_TABLE[a][4])
    axL.plot([best], [LATTICE_TABLE[best][4]], "*", color=ALT, ms=16, zorder=5)
    axL.annotate("optimum pitch %d cm\n$k_\\infty$ = %.3f" % (best, LATTICE_TABLE[best][4]),
                 xy=(best, LATTICE_TABLE[best][4]), xytext=(21, 0.62),
                 fontsize=8.5, color=ALT,
                 arrowprops=dict(arrowstyle="->", color=ALT, lw=1.0))
    axL.set_xlabel("lattice pitch $a$ (cm)")
    axL.set_ylabel("factor")
    axL.set_ylim(0.3, 1.25)
    axL.legend(fontsize=8, loc="lower left")
    axL.set_title("Lumping doubles the resonance escape")

    radii = np.linspace(0.3, 4.0, 200)
    axR.plot(radii, [resonance_integral_rod(r, 19.1) for r in radii], color=INK,
             lw=2.4, label="$^{238}$U metal")
    axR.plot(radii, [resonance_integral_rod(r, 10.97, "238UO2") for r in radii],
             color=FLOW, lw=2.0, ls="--", label="$^{238}$UO$_2$")
    axR.plot(radii, [resonance_integral_rod(r, 11.7, "232Th metal") for r in radii],
             color=LEAF, lw=2.0, ls="-.", label="$^{232}$Th metal")
    axR.plot([1.25], [resonance_integral_rod(1.25, 19.1)], "o", color=ALT, ms=8)
    axR.annotate("S&F's 1.25 cm rod", xy=(1.25, resonance_integral_rod(1.25, 19.1)),
                 xytext=(1.7, 22), fontsize=8.5, color=ALT,
                 arrowprops=dict(arrowstyle="->", color=ALT, lw=1.0))
    axR.set_xlabel("fuel rod radius $r$ (cm)")
    axR.set_ylabel("resonance integral $I$ (b)")
    axR.legend(fontsize=8.5)
    axR.set_title("$I = A + C/\\sqrt{r\\rho}$: fatter rods\nself-shield better")
    fig.tight_layout()
    _save(fig, "fig3_lumping.svg")
    caps["fig3_lumping.svg"] = (
        "Left: S&F Table 10.8, the graphite lattice with 1.25 cm natural-uranium rods. Lumping "
        "the fuel roughly doubles the resonance escape probability against a homogeneous "
        "mixture at the same fuel-to-moderator ratio (dotted), because neutrons now slow down "
        "in moderator that contains no 238U at all and only those reaching resonance energies "
        "near a rod are in danger. That is enough to push k_inf above 1 where the homogeneous "
        "mixture peaks at 0.78 -- which is how Fermi's CP-1 worked on natural uranium. Right: "
        "the mechanism, Eq. (10.19). Resonance capture in a lump happens in a thin surface "
        "skin, so the integral falls as 1/sqrt(r rho) and a fatter rod hides more of its own "
        "238U from the neutron flux.")

    # Fig 4 -- leakage and the critical size.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.0))
    f_core = thermal_utilization_homogeneous(
        FUEL_THERMAL_AVERAGED["235U"]["sigma_a"], 0.00386, 35000.0)
    l2 = diffusion_length_squared(MODERATOR_THERMAL["C"]["L2"], f_core)
    tau = MODERATOR_THERMAL["C"]["tau"]
    kinf = 1.6939
    rs = np.linspace(40, 400, 300)
    b2 = [geometric_buckling("sphere", R=r) for r in rs]
    axL.plot(rs, [fast_nonleakage(b, tau) for b in b2], color=FLOW, lw=2.0,
             ls="--", label="$P_{NL}^{f}=e^{-B^2\\tau}$")
    axL.plot(rs, [thermal_nonleakage(l2, b) for b in b2], color=LEAF, lw=2.0,
             ls="-.", label="$P_{NL}^{th}=1/(1+L^2B^2)$")
    axL.plot(rs, [kinf * fast_nonleakage(b, tau) * thermal_nonleakage(l2, b)
                  for b in b2], color=INK, lw=2.6, label="$k_{eff}$")
    axL.axhline(1.0, color=ALT, ls="--", lw=1.4)
    rc = critical_radius_sphere(kinf, l2, tau)
    axL.plot([rc], [1.0], "o", color=ALT, ms=8)
    axL.annotate("critical at\n$R$ = %.0f cm" % rc, xy=(rc, 1.0), xytext=(rc + 45, 0.72),
                 fontsize=9, color=ALT,
                 arrowprops=dict(arrowstyle="->", color=ALT, lw=1.0))
    axL.set_xlabel("bare sphere radius $R$ (cm)")
    axL.set_ylabel("probability / $k_{eff}$")
    axL.set_ylim(0, 1.75)
    axL.legend(fontsize=8.5, loc="lower right")
    axL.set_title("$^{235}$U in graphite, 1:35 000")

    kk = np.linspace(1.02, 2.4, 200)
    for l2v, tauv, col, ls, lab in ((l2, tau, INK, "-", "graphite ($\\tau$=368)"),
                                    (8.12 * (1 - f_core), 27.0, FLOW, "--",
                                     "water ($\\tau$=27)"),
                                    (24900 * (1 - f_core), 131.0, LEAF, "-.",
                                     "heavy water ($\\tau$=131)")):
        axR.semilogy(kk, [critical_radius_sphere(k, l2v, tauv) for k in kk],
                     color=col, lw=2.0, ls=ls, label=lab)
    axR.set_xlabel("$k_\\infty$ of the core material")
    axR.set_ylabel("critical radius (cm)")
    axR.legend(fontsize=8.5)
    axR.set_title("Critical size diverges as $k_\\infty\\to1$")
    fig.tight_layout()
    _save(fig, "fig4_criticality.svg")
    caps["fig4_criticality.svg"] = (
        "Left: S&F Examples 10.4-10.5. Both non-leakage probabilities rise toward 1 as the core "
        "grows, so k_eff climbs from far below k_inf to k_inf itself; criticality is wherever it "
        "crosses 1, here at R = 127 cm. Note the fast term is the more punishing one in "
        "graphite, because the Fermi age tau = 368 cm2 is thirteen times water's. Right: the "
        "critical radius against the material's own k_inf, for three moderators. It diverges as "
        "k_inf approaches 1 -- a material only barely above 1 needs an unboundedly large core, "
        "which is why a natural-uranium reactor is necessarily a big one, and why water's tiny "
        "Fermi age lets a light-water core be metres rather than tens of metres across.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
