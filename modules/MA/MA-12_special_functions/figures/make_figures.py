"""MA-12 figures — Legendre polynomials and Bessel functions, two SL families.

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
from special_functions import legendre, bessel_j   # noqa: E402

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"
COLS = [INK, FLOW, ALT, STEEL]


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — Legendre polynomials P_1..P_4 on [-1, 1] from the module's recurrence.
    # SL eigenfunctions of -((1-x^2)y')' = n(n+1) y, weight 1; all satisfy P_n(1)=1.
    x = np.linspace(-1.0, 1.0, 400)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for n, col in zip(range(1, 5), COLS):
        ax.plot(x, [legendre(n, xi) for xi in x], color=col, lw=2, label=fr"$P_{n}$")
    ax.axhline(0, color="#cccccc", lw=0.6)
    ax.plot(1.0, 1.0, "o", ms=4, color="#666666")
    ax.annotate(r"$P_n(1)=1$", xy=(1.0, 1.0), xytext=(0.30, 1.06), fontsize=9.5,
                color="#666666")
    ax.set_xlim(-1.0, 1.0); ax.set_ylim(-1.15, 1.20)
    ax.set_xlabel(r"$x=\cos\theta$"); ax.set_ylabel(r"$P_n(x)$")
    ax.set_title(r"Legendre polynomials $P_n(x)$  (weight $w=1$ on $[-1,1]$)")
    ax.legend(loc="lower right", frameon=False, fontsize=9.5, ncol=2)
    _save(fig, "fig1_legendre.svg")
    caps["fig1_legendre.svg"] = (
        "Legendre polynomials $P_1$–$P_4$ on $[-1,1]$ from legendre (the recurrence "
        "$(n+1)P_{n+1}=(2n+1)xP_n-nP_{n-1}$). Each $P_n$ has $n$ zeros and definite "
        "parity $P_n(-x)=(-1)^n P_n(x)$, with $P_n(1)=1$; they are the orthogonal SL "
        "eigenfunctions of the polar-angle equation $-((1-x^2)y')'=n(n+1)y$ that build "
        "the multipole expansion.")

    # Fig 2 — Bessel functions J_0..J_3 from the integral representation bessel_j.
    # Eigenfunctions of x^2 y'' + x y' + (x^2 - n^2) y = 0 (cylinder modes, weight x).
    xb = np.linspace(0.0, 16.0, 320)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for n, col in zip(range(4), COLS):
        ax.plot(xb, [bessel_j(n, xi) for xi in xb], color=col, lw=2, label=fr"$J_{n}$")
    ax.axhline(0, color="#cccccc", lw=0.6)
    ax.set_xlim(0.0, 16.0); ax.set_ylim(-0.55, 1.05)
    ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$J_n(x)$")
    ax.set_title(r"Bessel functions $J_n(x)$  (cylinder modes, weight $w=x$)")
    ax.legend(loc="upper right", frameon=False, fontsize=9.5, ncol=2)
    _save(fig, "fig2_bessel.svg")
    caps["fig2_bessel.svg"] = (
        "Bessel functions $J_0$–$J_3$ from bessel_j, evaluated by the integral "
        "representation $J_n(x)=\\frac1\\pi\\int_0^\\pi\\cos(n\\tau-x\\sin\\tau)\\,d\\tau$. "
        "They solve $x^2y''+xy'+(x^2-n^2)y=0$ and oscillate with slowly decaying "
        "amplitude ($J_0(0)=1$, $J_{n\\ge1}(0)=0$); their zeros set the radial drum and "
        "waveguide modes, orthogonal under the weight $w=x$.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
