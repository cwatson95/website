"""EM-02 figures -- Gauss's law: the field of a charged sphere and flux = Q_enc.

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
from gauss_law import uniform_sphere_field, enclosed_charge      # noqa: E402
from electrostatics import field_magnitude, EPS0, K_E            # noqa: E402

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    Q, R = 1e-9, 1.0
    E = uniform_sphere_field(Q, R)
    mag = field_magnitude(E)

    # Fig 1 -- E(r) of a uniformly charged solid sphere: linear in, 1/r^2 out.
    r = np.linspace(1e-3, 3.0 * R, 400)
    Er = np.array([mag(rr, 0.0, 0.0) for rr in r])
    inside = K_E * Q * r / R ** 3
    outside = K_E * Q / r ** 2
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(r / R, Er, color=INK, lw=2.4, label=r"$|E(r)|$  (module field)")
    ax.plot(r / R, inside, color=ALT, lw=1.2, ls="--", label=r"inside $\propto r$")
    ax.plot(r / R, outside, color=FLOW, lw=1.2, ls="--", label=r"outside $\propto \frac{1}{r^2}$")
    ax.axvline(1.0, color="#aaaaaa", lw=0.8)
    ax.set_ylim(0, 1.25 * K_E * Q / R ** 2)
    ax.set_xlabel(r"$r/R$"); ax.set_ylabel(r"$|E|$  (V/m)")
    ax.set_title("Uniformly charged sphere: field peaks at the surface $r=R$")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig1_sphere_field.svg")
    caps["fig1_sphere_field.svg"] = (
        "Radial field of a uniformly charged solid sphere from uniform_sphere_field. "
        "Inside it grows linearly (E proportional to r), outside it falls as 1/r^2 like a "
        "point charge, and the two pieces meet continuously at the surface r = R.")

    # Fig 2 -- Gauss's law: flux through a Gaussian sphere measures Q_enc.
    rg = np.linspace(0.18 * R, 2.6 * R, 22)
    Qenc = np.array([enclosed_charge(E, R=rr, n=44) for rr in rg])
    ideal = Q * np.minimum(1.0, (rg / R) ** 3)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(rg / R, ideal / Q, color=INK, lw=2,
            label=r"$Q_{enc}/Q=\min(1,(r/R)^3)$")
    ax.plot(rg / R, Qenc / Q, "o", color=FLOW, ms=6,
            label=r"$\varepsilon_0\oint E\cdot dA\,/\,Q$")
    ax.axvline(1.0, color="#aaaaaa", lw=0.8)
    ax.axhline(1.0, color="#cccccc", lw=0.8)
    ax.set_xlabel(r"Gaussian radius $r/R$"); ax.set_ylabel(r"$Q_{enc}/Q$")
    ax.set_title(r"Gauss's law: flux integral reports the enclosed charge")
    ax.legend(loc="lower right", frameon=False)
    _save(fig, "fig2_flux_enclosed.svg")
    caps["fig2_flux_enclosed.svg"] = (
        "The numerically computed flux (markers, eps0 times the surface integral from "
        "enclosed_charge) versus the analytic enclosed-charge fraction (line). Inside the "
        "sphere it rises as (r/R)^3, then saturates at Q once the Gaussian surface "
        "contains the whole charge -- flux depends only on Q_enc.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
