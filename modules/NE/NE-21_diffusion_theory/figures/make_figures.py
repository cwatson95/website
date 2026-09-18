"""NE-21 figures -- the plane-source solution and where it stops being valid,
the critical flux profiles and their peaking factors, buckling as the meeting of
material and geometry, and what the extrapolation distance costs a small core.

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
from diffusion import (                            # noqa: E402
    J0_FIRST_ZERO, plane_source_flux, point_source_flux, diffusion_valid,
    transport_mfp, diffusion_coefficient, material_buckling,
    geometric_buckling, critical_dimension, critical_flux_profile,
    peak_to_average, extrapolation_distance, extrapolated_dimension,
    k_effective_from_buckling, bessel_j0,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    sigma_tr, sigma_a = 0.4, 2.74e-4
    d = diffusion_coefficient(sigma_tr)
    l = math.sqrt(d / sigma_a)

    # Fig 1 -- the plane source, and where diffusion theory fails.
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    x = np.linspace(0.01, 250, 500)
    phi = [plane_source_flux(1.0, xx, d, l) for xx in x]
    ax.semilogy(x, phi, color=INK, lw=2.4, label="plane source, $e^{-x/L}$")
    unc = [math.exp(-sigma_tr * xx) * plane_source_flux(1.0, 0.0, d, l) for xx in x]
    ax.semilogy(x, unc, color=FLOW, lw=1.8, ls="--",
                label="uncollided, $e^{-\\Sigma_{tr}x}$ (~NE-11)")
    bad = 3 * transport_mfp(sigma_tr)
    ax.axvspan(0, bad, color=ALT, alpha=0.14, lw=0)
    ax.annotate("within 3 $\\lambda_{tr}$:\nFick's law fails\n(and the boundary\ncondition lives here)",
                xy=(bad / 2, 1e-2), fontsize=8.5, color=ALT, ha="center")
    ax.axvline(l, color=LEAF, ls=":", lw=1.6)
    ax.annotate("$L$ = %.0f cm" % l, xy=(l + 4, 2e1), fontsize=9, color=LEAF)
    ax.set_xlabel("distance from the source plane (cm)")
    ax.set_ylabel("$\\phi(x)$  (arbitrary)")
    ax.set_ylim(1e-3, 1e2)
    ax.legend(fontsize=9)
    ax.set_title("$\\phi(x)=(S_0L/2D)\\,e^{-|x|/L}$   (S&F Eq. 10.72)")
    _save(fig, "fig1_plane_source.svg")
    caps["fig1_plane_source.svg"] = (
        "S&F's fixed-source solution (Eq. 10.72) for an infinite plane source in a "
        "non-multiplying medium, with graphite-like constants. The flux decays purely "
        "exponentially with scale L = 55 cm -- which is what the diffusion length MEANS before "
        "it acquires any random-walk interpretation. The dashed line is ~NE-11's uncollided "
        "attenuation over the same distances: by 50 cm it is eight decades below the diffusion "
        "answer, because it counts only neutrons that have never scattered while diffusion "
        "counts the whole scattered population. The shaded strip is where Fick's law is not "
        "valid at all -- "
        "within about three transport mean free paths of the source, the angular flux is nowhere "
        "near isotropic. Note that the boundary condition J(0+) = S0/2 used to fix the "
        "coefficient is imposed exactly there.")

    # Fig 2 -- the critical flux profiles and their peaking.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.0))
    u = np.linspace(-0.999, 0.999, 400)
    axL.plot(u, [critical_flux_profile("slab", uu * 0.5, a=1.0) for uu in u],
             color=INK, lw=2.4, label="slab  ($\\pi/2$ = 1.57)")
    ur = np.linspace(1e-6, 0.999, 400)
    axL.plot(np.concatenate([-ur[::-1], ur]),
             [critical_flux_profile("sphere", abs(uu), R=1.0)
              for uu in np.concatenate([-ur[::-1], ur])],
             color=FLOW, lw=2.2, ls="--", label="sphere  ($\\pi^2/3$ = 3.29)")
    axL.plot(u, [bessel_j0(J0_FIRST_ZERO * abs(uu)) for uu in u],
             color=LEAF, lw=2.2, ls="-.", label="infinite cylinder  (2.32)")
    axL.axhline(0, color="0.85", lw=1.0, zorder=0)
    axL.set_xlabel("fractional position from the centre")
    axL.set_ylabel("$\\phi/\\phi_{\\max}$")
    axL.legend(fontsize=8.5, title="geometry (peak/average)", title_fontsize=8.5)
    axL.set_title("The shape has no material in it")

    geoms = ["slab", "infinite cylinder", "sphere", "cylinder", "parallelepiped"]
    labels = ["slab", "inf. cyl.", "sphere", "cylinder", "cube"]
    vals = [peak_to_average(g) for g in geoms]
    cols = [INK, LEAF, FLOW, STEEL, ALT]
    bars = axR.bar(range(len(geoms)), vals, 0.6, color=cols, edgecolor="white", lw=0.8)
    for i, b in enumerate(bars):
        axR.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.06,
                 "%.2f" % vals[i], ha="center", fontsize=9)
    axR.axhline(1.0, color="0.7", ls="--", lw=1.2)
    axR.annotate("a flat core would be 1.0", xy=(0.1, 1.08), fontsize=8.5, color="0.4")
    axR.set_xticks(range(len(geoms)))
    axR.set_xticklabels(labels, fontsize=9)
    axR.set_ylabel("peak / average flux")
    axR.set_ylim(0, 4.4)
    axR.set_title("Power peaking in a bare core")
    fig.tight_layout()
    _save(fig, "fig2_flux_profiles.svg")
    caps["fig2_flux_profiles.svg"] = (
        "Left: the critical flux profiles of S&F Table 10.10, each normalised to its peak. They "
        "are eigenfunctions of the geometry and contain no material properties whatever -- so "
        "once the shape is chosen, the power distribution is fixed. Right: the consequence. A "
        "bare cylindrical core runs its centre 3.6 times hotter than its average, and since the "
        "hottest fuel pin sets the limit for the whole reactor, that factor is thrown-away "
        "capacity. It is why real cores are never bare and never uniform: a reflector raises the "
        "edges (~NE-19 §10.6), and fuel zoning puts fresh fuel at the periphery and depleted "
        "fuel at the centre.")

    # Fig 3 -- buckling: material meets geometry.
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    k_inf, l2 = 1.6939, 570.1
    sizes = np.linspace(40, 400, 400)
    for geom, key, col, ls in (("sphere", "R", INK, "-"),
                               ("infinite cylinder", "R", LEAF, "-."),
                               ("slab", "a", FLOW, "--")):
        ax.semilogy(sizes, [geometric_buckling(geom, **{key: s}) for s in sizes],
                    color=col, lw=2.2, ls=ls, label="$B_g^2$, %s" % geom)
    b2 = material_buckling(k_inf, l2)
    ax.axhline(b2, color=ALT, lw=2.4)
    ax.annotate("$B_{mat}^2=(k_\\infty-1)/L^2$ = %.2e\n(material only)" % b2,
                xy=(250, b2 * 1.5), fontsize=9, color=ALT)
    for geom, key, col in (("sphere", "R", INK), ("infinite cylinder", "R", LEAF),
                           ("slab", "a", FLOW)):
        s = critical_dimension(geom, k_inf, l2)
        ax.plot([s], [b2], "o", color=col, ms=8, zorder=5)
        ax.annotate("%.0f cm" % s, xy=(s, b2), xytext=(s - 12, b2 * 0.35),
                    fontsize=8.5, color=col)
    ax.set_xlabel("characteristic dimension (cm)")
    ax.set_ylabel("buckling $B^2$  (cm$^{-2}$)")
    ax.set_ylim(1e-4, 1e-2)
    ax.legend(fontsize=8.5, loc="upper right")
    ax.set_title("Criticality is where the two bucklings meet")
    _save(fig, "fig3_buckling.svg")
    caps["fig3_buckling.svg"] = (
        "S&F Eq. (10.80), B_mat^2 = B_g^2, drawn. The horizontal line depends only on the "
        "material -- (k_inf - 1)/L^2 for ~NE-19's 235U/graphite core -- and the falling curves "
        "depend only on the shape and size. Criticality is an intersection, and that clean "
        "factorisation is what lets a designer choose fuel and geometry almost independently. "
        "Two things are visible. A material with k_inf <= 1 puts the horizontal line at or below "
        "zero, where no curve reaches it, which is the algebraic statement that no amount of "
        "geometry saves a subcritical material. And the sphere intersects at the smallest "
        "dimension for a given volume, because leakage is a surface effect.")

    # Fig 4 -- what the extrapolation distance costs, and the missing fast leakage.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.0))
    sizes = np.logspace(math.log10(10), math.log10(600), 300)
    for mat, s_tr, col, ls in (("graphite ($\\lambda_{tr}$=2.5 cm)", 0.4, INK, "-"),
                               ("water ($\\lambda_{tr}$=0.43 cm)", 1.0 / 0.43, FLOW, "--")):
        err = [100 * (1 - (s / extrapolated_dimension(s, sigma_tr=s_tr)) ** 2)
               for s in sizes]
        axL.loglog(sizes, err, color=col, lw=2.2, ls=ls, label=mat)
    axL.axhline(5.0, color=LEAF, ls=":", lw=1.6)
    axL.annotate("5% error", xy=(12, 5.6), fontsize=9, color=LEAF)
    axL.set_xlabel("slab thickness (cm)")
    axL.set_ylabel("error in $B^2$ from ignoring $d$ (%)")
    axL.legend(fontsize=8.5)
    axL.set_title("S&F set the extrapolation\ndistance to zero")

    kk = np.linspace(1.05, 3.0, 300)
    one = [critical_dimension("sphere", k, l2) for k in kk]
    axR.plot(kk, one, color=INK, lw=2.4, label="one-speed (this module)")
    two = []
    for k in kk:
        lo, hi = 1e-9, 1e-2
        for _ in range(120):
            mid = 0.5 * (lo + hi)
            if k * math.exp(-mid * 368.0) / (1 + l2 * mid) > 1.0:
                lo = mid
            else:
                hi = mid
        two.append(math.pi / math.sqrt(0.5 * (lo + hi)))
    axR.plot(kk, two, color=FLOW, lw=2.2, ls="--",
             label="with Fermi age $\\tau$ = 368 cm$^2$ (~NE-19)")
    axR.plot([1.6939], [critical_dimension("sphere", 1.6939, l2)], "o", color=INK, ms=8)
    axR.plot([1.6939], [126.7], "s", color=FLOW, ms=8)
    axR.annotate("90 cm vs 127 cm\nfor the same material", xy=(1.75, 108),
                 fontsize=8.5, color=ALT)
    axR.set_xlabel("$k_\\infty$")
    axR.set_ylabel("critical sphere radius (cm)")
    axR.set_ylim(0, 400)
    axR.legend(fontsize=8.5)
    axR.set_title("One speed is not enough")
    fig.tight_layout()
    _save(fig, "fig4_limits.svg")
    caps["fig4_limits.svg"] = (
        "Two ways the textbook treatment is incomplete, quantified. Left: S&F drop the "
        "extrapolation distance d = 0.7104 lambda_tr as 'generally very small compared to the "
        "size of the reactor'. True for a metre-scale power core; a 20 cm graphite assembly is "
        "effectively 18% larger than it looks, a 28% error in the buckling. In water the "
        "transport mean free path is six times shorter and the approximation is safe almost "
        "everywhere. Right: the one-speed model has no fast-leakage term, because it never lets "
        "a neutron slow down. For ~NE-19's 235U/graphite core it puts the critical sphere at "
        "90 cm where the two-group answer with the Fermi age is 127 cm -- a 30% "
        "underestimate, and in the unsafe direction.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
