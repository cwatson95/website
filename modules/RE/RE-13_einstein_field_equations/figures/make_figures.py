"""RE-13 figures -- Schwarzschild geometry and the field equation as a check.

Two SVG figures (+captions.json) built from RE-13's OWN code in ../code:
  1. the Schwarzschild metric components g_tt, g_rr vs r (horizon at r = 2M),
     read straight off the real `schwarzschild_metric` callable;
  2. the field-equation residual  G_{mu nu} + Lambda g_{mu nu} - 8 pi T_{mu nu}
     from `field_equation_residual`, certifying Schwarzschild (vacuum) and
     de Sitter (Lambda-vacuum) as solutions while flagging de Sitter with the
     wrong Lambda.
Run:  python3 make_figures.py
Convention (shared by every module): matplotlib -> SVG with svg.fonttype='path'
so text ships as portable vector outlines, saved next to a captions.json.
"""
import json
import os
import sys
import math

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"      # text as vector paths (portable)
matplotlib.rcParams["font.size"] = 11
import matplotlib.pyplot as plt                    # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from einstein_equations import (                   # noqa: E402
    schwarzschild_metric, de_sitter_metric, field_equation_residual,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _maxabs(T):
    n = len(T)
    return max(abs(T[i][j]) for i in range(n) for j in range(n))


def main():
    caps = {}

    # Fig 1 -- Schwarzschild metric components straight from the real metric.
    M = 1.0
    g = schwarzschild_metric(M)
    r = np.linspace(2.02 * M, 12.0 * M, 500)
    g_tt = np.array([g([0.0, ri, math.pi / 2, 0.0])[0][0] for ri in r])
    g_rr = np.array([g([0.0, ri, math.pi / 2, 0.0])[1][1] for ri in r])
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(r, g_tt, color=INK, lw=2, label=r"$g_{tt}=-(1-\frac{2M}{r})$")
    ax.plot(r, g_rr, color=FLOW, lw=2, label=r"$g_{rr}=(1-\frac{2M}{r})^{-1}$")
    ax.axvline(2.0 * M, color="#aaaaaa", lw=1.0, ls="--")
    ax.axhline(0.0, color="#cccccc", lw=0.6)
    ax.text(2.12 * M, 8.7, "horizon\n$r=2M$", color="#777777", fontsize=9)
    ax.set_ylim(-1.6, 11.5)
    ax.set_xlim(0.0, 12.0 * M)
    ax.set_xlabel(r"areal radius $r/M$")
    ax.set_ylabel("metric component")
    ax.set_title(r"Schwarzschild metric: $g_{rr}$ diverges at the horizon $r=2M$")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig1_schwarzschild_metric.svg")
    caps["fig1_schwarzschild_metric.svg"] = (
        "Schwarzschild metric components read from schwarzschild_metric(M): "
        "g_tt = -(1 - 2M/r) (blue) climbs from -1 toward 0 at the horizon, while "
        "g_rr = 1/(1 - 2M/r) (orange) diverges there. The blow-up at r = 2M is a "
        "coordinate artefact of these components, not a real curvature singularity.")

    # Fig 2 -- the field equation as a validator: residual vs radius.
    rr = np.linspace(2.6, 9.0, 22)
    L = 10.0
    sch = schwarzschild_metric(1.0)
    dS = de_sitter_metric(L)
    Lam = 3.0 / (L * L)
    res_sch = [_maxabs(field_equation_residual(sch, 0, [0.0, ri, 1.1, 0.7], Lambda=0.0))
               for ri in rr]
    res_dS0 = [_maxabs(field_equation_residual(dS, 0, [0.0, ri, 1.1, 0.7], Lambda=0.0))
               for ri in rr]
    res_dSL = [_maxabs(field_equation_residual(dS, 0, [0.0, ri, 1.1, 0.7], Lambda=Lam))
               for ri in rr]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.semilogy(rr, res_dS0, color=ALT, lw=2, marker="o", ms=3.5,
                label=r"de Sitter, $\Lambda=0$  (not a vacuum)")
    ax.semilogy(rr, res_sch, color=INK, lw=2, marker="s", ms=3.5,
                label=r"Schwarzschild, $\Lambda=0$  (vacuum)")
    ax.semilogy(rr, res_dSL, color=FLOW, lw=2, marker="^", ms=3.5,
                label=r"de Sitter, $\Lambda=\frac{3}{L^2}$")
    ax.set_xlabel(r"radius $r$  ($M=1$,  $L=10$)")
    ax.set_ylabel(r"residual $\max|G+\Lambda g-8\pi T|$")
    ax.set_title("The field equation as a check: residual ~ 0 on a solution")
    ax.legend(loc="center right", frameon=False, fontsize=9)
    _save(fig, "fig2_field_equation_residual.svg")
    caps["fig2_field_equation_residual.svg"] = (
        "The field-equation residual max|G + Lambda g - 8 pi T| from "
        "field_equation_residual, swept over radius. Schwarzschild (Lambda = 0) "
        "and de Sitter with Lambda = 3/L^2 sit at the finite-difference floor -- "
        "they solve Einstein's equations -- while de Sitter with Lambda = 0 stays "
        "far from zero: it is a solution only once the cosmological constant is "
        "restored.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
