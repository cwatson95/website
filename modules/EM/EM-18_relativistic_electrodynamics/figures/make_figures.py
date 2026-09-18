"""EM-18 figures -- how E and B transform under a boost, and the invariants.

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
from relativistic_electrodynamics import (         # noqa: E402
    gamma, boost_fields, field_invariants,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    betas = np.linspace(0.0, 0.99, 300)

    # Fig 1 -- boost a pure E field: a magnetic field appears and grows.
    E = (0.0, 1.0, 0.0)                             # pure E, transverse to boost (units c=1)
    B = (0.0, 0.0, 0.0)
    Ey, Bz, gam = [], [], []
    for be in betas:
        Ep, Bp = boost_fields(E, B, be, c=1.0)
        Ey.append(Ep[1]); Bz.append(abs(Bp[2])); gam.append(gamma(be))
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(betas, gam, color=STEEL, lw=1.4, ls=":", label=r"$\gamma$")
    ax.plot(betas, Ey, color=INK, lw=2.2, label=r"$E'_y/E_0=\gamma$")
    ax.plot(betas, Bz, color=FLOW, lw=2.2, label=r"$c\,|B'_z|/E_0=\gamma\beta$")
    ax.set_xlabel(r"boost $\beta=v/c$"); ax.set_ylabel(r"field / $E_0$")
    ax.set_title(r"A boost turns a pure $\mathbf{E}$ field into $\mathbf{E}$ and $\mathbf{B}$")
    ax.set_xlim(0, 0.99); ax.set_ylim(0, 8)
    ax.legend(loc="upper left", frameon=False)
    _save(fig, "fig1_field_transform.svg")
    caps["fig1_field_transform.svg"] = (
        "Boosting a frame with only a transverse E field (boost_fields, c=1): the "
        "electric field is enhanced to E'y = gamma E0 (blue), and a magnetic field "
        "appears with c|B'z| = gamma beta E0 (orange), growing without bound as beta "
        "-> 1. Magnetism is electrostatics seen from a moving frame.")

    # Fig 2 -- the two field invariants stay constant while the fields change.
    E2 = (0.0, 1.0, 0.0)
    B2 = (0.0, 0.5, 0.0)                            # E.B and B^2-E^2/c^2 both nonzero
    I1, I2, Emag2 = [], [], []
    for be in betas:
        Ep, Bp = boost_fields(E2, B2, be, c=1.0)
        i1, i2 = field_invariants(Ep, Bp, c=1.0)
        I1.append(i1); I2.append(i2)
        Emag2.append(Ep[0] ** 2 + Ep[1] ** 2 + Ep[2] ** 2)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(betas, Emag2, color=STEEL, lw=2.0,
            label=r"$|\mathbf{E}'|^{2}$  (frame dependent)")
    ax.plot(betas, I1, color=INK, lw=2.2,
            label=r"$\mathbf{E}\cdot\mathbf{B}$  (invariant)")
    ax.plot(betas, I2, color=FLOW, lw=2.2,
            label=r"$B^{2}-E^{2}/c^{2}$  (invariant)")
    ax.axhline(0, color="#cccccc", lw=0.6)
    ax.set_xlabel(r"boost $\beta=v/c$"); ax.set_ylabel("value")
    ax.set_title("Lorentz invariants survive the boost")
    ax.set_xlim(0, 0.99)
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig2_invariants.svg")
    caps["fig2_invariants.svg"] = (
        "Starting from E and B both along y and boosting along x: the field magnitude "
        "|E'|^{2} climbs with beta (grey), but the two scalars from field_invariants, "
        "E.B (blue) and B^{2}-E^{2}/c^{2} (orange), stay flat. Every observer "
        "disagrees on E and B yet agrees on these Lorentz invariants.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
