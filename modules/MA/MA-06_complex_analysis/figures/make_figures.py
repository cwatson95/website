"""MA-06 figures — a contour integral with poles & residues, and Cauchy's theorem.

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
from complex_analysis import (                      # noqa: E402
    circle, contour_integral, residue_at, winding_number,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"
TWO_PI = 2.0 * math.pi


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    f = lambda z: 1.0 / (z * z + 1.0)        # poles at +/- i, residues -/+ i/2

    # Fig 1 — |f| over the plane, a contour round one pole, and the residue theorem.
    C = circle(1j, 0.6)                       # positively-oriented loop enclosing +i
    res_i = residue_at(f, 1j)                 # ~ -0.5j
    oint = contour_integral(f, C, 0.0, TWO_PI)   # ~ 2*pi*i*res = pi
    w_in, w_out = winding_number(C, 1j), winding_number(C, -1j)   # 1 and 0

    gx = np.linspace(-2.2, 2.2, 420)
    X, Y = np.meshgrid(gx, gx)
    with np.errstate(divide="ignore", invalid="ignore"):
        M = np.log10(np.abs(1.0 / ((X + 1j * Y) ** 2 + 1.0)))
    M = np.clip(M, -1.4, 1.4)

    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    im = ax.imshow(M, extent=[-2.2, 2.2, -2.2, 2.2], origin="lower", cmap="magma")
    t = np.linspace(0, TWO_PI, 240)
    pts = np.array([C(tt) for tt in t])
    ax.plot(pts.real, pts.imag, color=STEEL, lw=2.2, label=r"contour $C$")
    ax.plot([0, 0], [1, -1], "x", ms=11, mew=2.4, color="w")
    ax.annotate(r"$+i$", (0, 1), color="w", xytext=(8, 2), textcoords="offset points")
    ax.annotate(r"$-i$", (0, -1), color="w", xytext=(8, -10), textcoords="offset points")
    ax.set_aspect("equal"); ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.2, 2.2)
    ax.set_xlabel(r"$\mathrm{Re}\,z$"); ax.set_ylabel(r"$\mathrm{Im}\,z$")
    ax.set_title(r"$\log_{10}|f|,\ f=\frac{1}{z^2+1}$:  $\oint_C f\,dz=2\pi i\,\mathrm{Res}_{+i}f$")
    txt = (f"Res$_{{+i}}f$ = {res_i.real:+.2f}{res_i.imag:+.2f}$i$\n"
           f"$\\oint_C f\\,dz$ = {oint.real:.3f}\n"
           f"$2\\pi i\\cdot$Res = {(2j*math.pi*res_i).real:.3f}\n"
           f"winding: $+i$={w_in:.0f}, $-i$={w_out:.0f}")
    ax.text(0.03, 0.97, txt, transform=ax.transAxes, va="top", ha="left", fontsize=8.5,
            color="w", bbox=dict(boxstyle="round", fc="#000000", ec="none", alpha=0.45))
    ax.legend(loc="lower right", frameon=False, labelcolor="w", fontsize=9)
    _save(fig, "fig1_residue_contour.svg")
    caps["fig1_residue_contour.svg"] = (
        r"Brightness is $\log_{10}|f|$ for $f=1/(z^2+1)$; the two flares are the poles at "
        r"$\pm i$. The loop $C$ (winding number $1$ about $+i$, $0$ about $-i$) encloses one "
        r"pole, so the residue theorem gives $\oint_C f\,dz=2\pi i\,\mathrm{Res}_{+i}f$. "
        r"Computed with the module: $\mathrm{Res}_{+i}f=-\tfrac{i}{2}$ and $\oint_C f\,dz\approx\pi$.")

    # Fig 2 — Cauchy's theorem / the Laurent fact:  oint z^n dz = 2*pi*i * delta_{n,-1}.
    ns = list(range(-3, 4))
    unit = circle(0.0, 1.0)
    vals = [(contour_integral(lambda z, k=k: z ** k, unit, 0.0, TWO_PI) / (2j * math.pi)).real
            for k in ns]
    vals = [0.0 if abs(v) < 1e-9 else v for v in vals]   # kill ~1e-13 trapezoid noise
    cols = [FLOW if k == -1 else INK for k in ns]

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.bar(ns, vals, color=cols, width=0.6)
    ax.axhline(0, color="#888888", lw=0.7)
    for k, v in zip(ns, vals):
        ax.annotate(f"{v:.2f}", (k, max(v, 0.0)), textcoords="offset points",
                    xytext=(0, 4), ha="center", va="bottom", fontsize=8.5)
    ax.set_xticks(ns); ax.set_ylim(0.0, 1.18)
    ax.set_xlabel(r"exponent $n$")
    ax.set_ylabel(r"$\frac{1}{2\pi i}\oint_{|z|=1} z^{\,n}\,dz$")
    ax.set_title(r"Cauchy's theorem & residues:  $\oint z^{\,n}\,dz = 2\pi i\,\delta_{n,-1}$")
    _save(fig, "fig2_cauchy_zn.svg")
    caps["fig2_cauchy_zn.svg"] = (
        r"The unit-circle integral $\frac{1}{2\pi i}\oint z^{\,n}\,dz$ from contour_integral, "
        r"for $n=-3\ldots3$. Every power is $0$ except $n=-1$, which gives $1$: analytic "
        r"integrands ($n\ge0$) vanish by Cauchy's theorem and higher poles ($n\le-2$) are "
        r"pure derivatives, so only the $1/z$ term carries a residue — the basis of the "
        r"residue calculus.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
