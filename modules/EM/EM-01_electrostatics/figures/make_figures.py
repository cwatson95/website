"""EM-01 figures -- the electric field of point charges (Coulomb + superposition).

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
from electrostatics import coulomb_field, field_magnitude   # noqa: E402

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _field_grid(E, xs, ys):
    """Sample the (non-vectorized) field on the z=0 plane -> Ex, Ey grids."""
    Ex = np.zeros((ys.size, xs.size))
    Ey = np.zeros((ys.size, xs.size))
    for j, y in enumerate(ys):
        for i, x in enumerate(xs):
            ex, ey, _ = E(x, y, 0.0)
            Ex[j, i], Ey[j, i] = ex, ey
    return Ex, Ey


def main():
    caps = {}
    xs = np.linspace(-2.2, 2.2, 46)
    ys = np.linspace(-1.55, 1.55, 34)
    a, q = 1.0, 1e-9

    # Fig 1 -- a dipole (+q, -q): field lines stream out of + into -.
    Edip = coulomb_field([(q, (a, 0.0, 0.0)), (-q, (-a, 0.0, 0.0))])
    Ex, Ey = _field_grid(Edip, xs, ys)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.streamplot(xs, ys, Ex, Ey, color=INK, density=1.1, linewidth=0.8, arrowsize=0.8)
    ax.plot(a, 0, "o", color=FLOW, ms=12, label=r"$+q$")
    ax.plot(-a, 0, "o", color=STEEL, ms=12, label=r"$-q$")
    ax.set_xlim(xs[0], xs[-1]); ax.set_ylim(ys[0], ys[-1]); ax.set_aspect("equal")
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title("Dipole field lines: superposition of two point charges")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig1_dipole_field.svg")
    caps["fig1_dipole_field.svg"] = (
        "Electric field lines of a dipole (+q on the right, -q on the left), built by "
        "superposing the two Coulomb fields from coulomb_field. Lines leave the positive "
        "charge and terminate on the negative one, normal to each charge.")

    # Fig 2 -- two like charges (+q, +q): a null point sits at the midpoint.
    Elike = coulomb_field([(q, (a, 0.0, 0.0)), (q, (-a, 0.0, 0.0))])
    Ex, Ey = _field_grid(Elike, xs, ys)
    mag0 = field_magnitude(Elike)(0.0, 0.0, 0.0)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.streamplot(xs, ys, Ex, Ey, color=FLOW, density=1.1, linewidth=0.8, arrowsize=0.8)
    ax.plot([a, -a], [0, 0], "o", color=INK, ms=12, label=r"$+q$")
    ax.plot(0, 0, "x", color=ALT, ms=11, mew=2.4,
            label=r"null point $|E|=%.0e$" % mag0)
    ax.set_xlim(xs[0], xs[-1]); ax.set_ylim(ys[0], ys[-1]); ax.set_aspect("equal")
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title("Two like charges: field lines repel, with a null between them")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig2_like_charges.svg")
    caps["fig2_like_charges.svg"] = (
        "Field lines of two equal positive charges. By symmetry the superposed field "
        "vanishes at the midpoint (the marked null point), and no field line crosses the "
        "plane between the charges -- like charges repel.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
