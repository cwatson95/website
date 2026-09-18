"""QO-05 figures — squeezed-vacuum quadrature variances & even-only photons.

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
from squeezing import (                            # noqa: E402
    squeezed_vacuum, quadrature_variances, photon_distribution,
    mean_photon, mean_photon_number,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — quadrature variances of the squeezed vacuum vs squeeze r.
    # Markers: computed by quadrature_variances(squeezed_vacuum(r)); the module's
    # own code.  Solid lines: the closed forms 1/4 e^{-/+2r}; product pinned at 1/16.
    r_pts = np.linspace(0.0, 1.2, 25)
    v1 = np.empty_like(r_pts)
    v2 = np.empty_like(r_pts)
    prod = np.empty_like(r_pts)
    for i, r in enumerate(r_pts):
        a, b = quadrature_variances(squeezed_vacuum(float(r)))
        v1[i], v2[i], prod[i] = a, b, a * b
    r_fine = np.linspace(0.0, 1.2, 400)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(r_fine, 0.25 * np.exp(-2 * r_fine), color=INK, lw=2,
            label=r"$\frac{1}{4} e^{-2r}$ (squeezed)")
    ax.plot(r_fine, 0.25 * np.exp(+2 * r_fine), color=FLOW, lw=2,
            label=r"$\frac{1}{4} e^{+2r}$ (anti-squeezed)")
    ax.plot(r_pts, v1, ls="none", marker="o", ms=4, color=INK)
    ax.plot(r_pts, v2, ls="none", marker="o", ms=4, color=FLOW)
    ax.plot(r_pts, prod, color=ALT, lw=1.6, label=r"$\mathrm{Var}X_1\,\mathrm{Var}X_2=\frac{1}{16}$")
    ax.axhline(0.25, color="#888888", lw=1.0, ls="--",
               label=r"vacuum / SQL $=\frac{1}{4}$")
    ax.set_yscale("log")
    ax.set_xlim(0, 1.2)
    ax.set_xlabel(r"squeeze parameter $r$")
    ax.set_ylabel(r"quadrature variance")
    ax.set_title(r"Squeezed vacuum: one quadrature below the SQL, product $=\frac{1}{16}$")
    ax.legend(loc="center left", frameon=False, fontsize=9)
    _save(fig, "fig1_quadrature_variances.svg")
    caps["fig1_quadrature_variances.svg"] = (
        r"Quadrature variances of the squeezed vacuum vs squeeze $r$: dots are "
        r"computed by quadrature_variances(squeezed_vacuum(r)), curves the closed "
        r"forms $\mathrm{Var}\,X_1=\tfrac14 e^{-2r}$ (below the vacuum/SQL line "
        r"$\tfrac14$) and $\mathrm{Var}\,X_2=\tfrac14 e^{+2r}$. Their product stays "
        r"pinned at $\tfrac1{16}$ — a minimum-uncertainty state for every $r$.")

    # Fig 2 — photon-number distribution: only EVEN numbers (photons in pairs),
    # broadening with r, with <n>=sinh^2 r.  Bars from photon_distribution itself.
    nmax = 13
    n = np.arange(nmax)
    rA, rB = 0.6, 1.1
    PA = photon_distribution(squeezed_vacuum(rA))[:nmax].real
    PB = photon_distribution(squeezed_vacuum(rB))[:nmax].real

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    w = 0.4
    ax.bar(n - w / 2, PA, width=w, color=INK,
           label=fr"$r={rA}$,  $\langle n\rangle=\sinh^2 r={mean_photon(rA):.3f}$")
    ax.bar(n + w / 2, PB, width=w, color=FLOW,
           label=fr"$r={rB}$,  $\langle n\rangle=\sinh^2 r={mean_photon(rB):.3f}$")
    ax.set_xticks(n)
    ax.set_xlim(-0.7, nmax - 0.3)
    ax.set_xlabel(r"photon number $n$")
    ax.set_ylabel(r"$P(n)=|\langle n|\xi\rangle|^2$")
    ax.set_title("Squeezed vacuum populates only EVEN photon numbers")
    ax.annotate(r"odd-$n$: $P\approx 0$  (photons in pairs)", xy=(4.6, 0.34),
                color=ALT, fontsize=9)
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_photon_distribution.svg")
    caps["fig2_photon_distribution.svg"] = (
        r"Photon-number distribution $P(n)$ of the squeezed vacuum from "
        r"photon_distribution(squeezed_vacuum(r)) for $r=0.6,1.1$. Built from $a^2$, "
        r"$S(\xi)$ makes photons in pairs, so only EVEN $n$ are populated (odd-$n$ "
        r"vanish to machine precision); the mean rises as $\langle n\rangle=\sinh^2 r$.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
