"""RE-15 figures -- expansion histories and the dilution of the cosmic fluids.

Two SVG figures (+captions.json) built from RE-15's OWN code in ../code:
  1. the scale factor a(t) for radiation, matter, and a Lambda (de Sitter)
     universe, from the real reference scale factors `power_law_scale_factor`
     and `de_sitter_scale_factor`;
  2. the energy density rho(a) = a^{-3(1+w)} for radiation / matter / Lambda
     from `era_density`, showing which component dominates in each era.
Run:  python3 make_figures.py
Convention (shared by every module): matplotlib -> SVG with svg.fonttype='path'
so text ships as portable vector outlines, saved next to a captions.json.
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"      # text as vector paths (portable)
matplotlib.rcParams["font.size"] = 11
import matplotlib.pyplot as plt                    # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from cosmology import (                            # noqa: E402
    power_law_scale_factor, de_sitter_scale_factor, era_density,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- a(t) for the three single-fluid eras, normalised to a(1) = 1.
    a_rad = power_law_scale_factor(0.5)             # radiation: a ~ t^(1/2)
    a_mat = power_law_scale_factor(2.0 / 3.0)       # matter:    a ~ t^(2/3)
    H = 0.8
    a_lam = de_sitter_scale_factor(H)               # Lambda:    a ~ e^(H t)
    t = np.linspace(0.02, 3.0, 500)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for fn, col, lab in (
        (a_rad, STEEL, r"radiation  $a\propto t^{1/2}$"),
        (a_mat, INK,   r"matter  $a\propto t^{2/3}$"),
        (a_lam, FLOW,  r"$\Lambda$ (de Sitter)  $a\propto e^{Ht}$"),
    ):
        ref = fn(1.0)
        ax.plot(t, [fn(ti) / ref for ti in t], color=col, lw=2, label=lab)
    ax.axhline(1.0, color="#cccccc", lw=0.6)
    ax.axvline(1.0, color="#cccccc", lw=0.6)
    ax.set_xlim(0.0, 3.0)
    ax.set_ylim(0.0, 4.2)
    ax.set_xlabel("cosmic time $t$")
    ax.set_ylabel("scale factor $a$  (a = 1 at t = 1)")
    ax.set_title("Expansion histories: how fast the universe grows by era")
    ax.legend(loc="upper left", frameon=False)
    _save(fig, "fig1_scale_factor.svg")
    caps["fig1_scale_factor.svg"] = (
        "Scale factor a(t) for the three single-fluid eras, each from the module's "
        "reference scale factors and normalised to a = 1 at t = 1. The power-law "
        "matter (a ~ t^(2/3)) and radiation (a ~ t^(1/2)) eras start from a Big Bang "
        "at a = 0 and decelerate, while the Lambda-dominated de Sitter case a ~ e^(Ht) "
        "never reaches zero and accelerates away at late times.")

    # Fig 2 -- era_density: rho(a) = a^{-3(1+w)} for radiation / matter / Lambda.
    a = np.logspace(-2.0, 2.0, 500)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for w, col, lab in (
        (1.0 / 3.0, STEEL, r"radiation $w=1/3$,  $\rho\propto a^{-4}$"),
        (0.0,       INK,   r"matter $w=0$,  $\rho\propto a^{-3}$"),
        (-1.0,      FLOW,  r"$\Lambda$ $w=-1$,  $\rho=$ const"),
    ):
        ax.loglog(a, [era_density(ai, w) for ai in a], color=col, lw=2, label=lab)
    ax.axvline(1.0, color="#cccccc", lw=0.6)
    ax.set_xlim(1e-2, 1e2)
    ax.set_xlabel("scale factor $a$")
    ax.set_ylabel(r"energy density $\rho/\rho_0$")
    ax.set_title(r"Cosmic dilution: $\rho\propto a^{-3(1+w)}$ sets the era sequence")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_era_density.svg")
    caps["fig2_era_density.svg"] = (
        "Energy density vs scale factor from era_density(a, w), normalised to "
        "rho = 1 at a = 1. Radiation (a^-4) falls fastest, matter (a^-3) slower, "
        "and the cosmological constant (w = -1) stays constant -- so the early "
        "universe is radiation dominated, then matter, and finally Lambda takes "
        "over as everything else dilutes away.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
