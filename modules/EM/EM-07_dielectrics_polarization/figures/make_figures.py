"""EM-07 figures -- dielectric screening and bound charge on a polarized sphere.

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
from dielectrics import (                          # noqa: E402
    displacement_point_free_charge, permittivity, susceptibility_from_eps_r,
    polarized_sphere_surface_charge, polarized_sphere_inner_field,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- a free point charge embedded in a linear dielectric: D is fixed by
    # the free charge (medium-independent), and E = D/eps is screened by 1/eps_r.
    q = 1e-9
    D = displacement_point_free_charge(q)            # |D| = q / (4 pi r^2), medium-free
    s = np.linspace(0.04, 0.40, 240)
    Dmag = np.array([D(r, 0.0, 0.0)[0] for r in s])  # D points radially (+x on the axis)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    colors = {1.0: INK, 2.0: STEEL, 4.0: ALT}
    for eps_r, col in colors.items():
        E = Dmag / permittivity(eps_r)               # E = D / eps = E_vac / eps_r
        lbl = (r"$\varepsilon_r=1$ (vacuum)" if eps_r == 1.0
               else fr"$\varepsilon_r={eps_r:.0f}$  ($\chi_e={susceptibility_from_eps_r(eps_r):.0f}$)")
        ax.plot(s * 100, E, color=col, lw=2, label=lbl)
    ax.set_xlabel("distance from charge  $r$  (cm)")
    ax.set_ylabel(r"field magnitude  $|E|$  (V/m)")
    ax.set_title(r"Dielectric screening: $E=D/\varepsilon=E_{\mathrm{vac}}/\varepsilon_r$")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig1_dielectric_screening.svg")
    caps["fig1_dielectric_screening.svg"] = (
        "A free point charge (1 nC) embedded in a linear dielectric. The displacement D "
        "is set by the free charge alone (medium-independent), so the actual field "
        "E = D/eps = E_vac/eps_r is reduced by 1/eps_r: higher eps_r screens the field more.")

    # Fig 2 -- uniformly polarized sphere (P along z): bound surface charge
    # sigma_b(theta) = P cos(theta), and the uniform depolarizing field E = -P/3eps0.
    P_mag = 1e-6
    sigma_b = polarized_sphere_surface_charge(P_mag)
    theta = np.linspace(0.0, np.pi, 300)
    sig = np.array([sigma_b(t) for t in theta])
    E_in = polarized_sphere_inner_field((0.0, 0.0, P_mag))[2]   # = -P/(3 eps0)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(np.degrees(theta), sig * 1e6, color=FLOW, lw=2,
            label=r"$\sigma_b(\theta)=P\cos\theta$")
    ax.axhline(0, color="#aaaaaa", lw=0.6)
    ax.fill_between(np.degrees(theta), sig * 1e6, 0, where=(sig > 0),
                    color=FLOW, alpha=0.15)
    ax.fill_between(np.degrees(theta), sig * 1e6, 0, where=(sig < 0),
                    color=INK, alpha=0.15)
    ax.set_xlim(0, 180)
    ax.set_xlabel(r"polar angle  $\theta$  (deg)")
    ax.set_ylabel(r"bound charge  $\sigma_b$  ($\mu$C/m$^{2}$)")
    ax.set_title(r"Uniformly polarized sphere: bound charge $\sigma_b=P\cos\theta$")
    ax.annotate(fr"inner field $E=-P/3\varepsilon_0={E_in:.2e}$ V/m",
                xy=(90, 0), xytext=(48, -0.55 * P_mag * 1e6),
                fontsize=9.5, color=INK)
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig2_polarized_sphere_bound_charge.svg")
    caps["fig2_polarized_sphere_bound_charge.svg"] = (
        "Bound surface charge on a uniformly polarized sphere with P along z: "
        "sigma_b(theta) = P cos(theta), positive on the north cap and negative on the "
        "south. This bound charge sources the uniform depolarizing field E = -P/3eps0 inside.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
