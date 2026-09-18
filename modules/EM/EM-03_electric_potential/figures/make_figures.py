"""EM-03 figures -- the electric potential V and the relation E = -grad V.

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
from electric_potential import potential_point_charges, field_from_potential  # noqa: E402

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    q, a = 1e-9, 0.6
    charges = [(q, (a, 0.0, 0.0)), (-q, (-a, 0.0, 0.0))]
    V = potential_point_charges(charges)
    E = field_from_potential(V)                    # E = -grad V (MA-02 gradient)

    # Fig 1 -- V heatmap + equipotentials, with E = -grad V arrows overlaid.
    xs = np.linspace(-2.0, 2.0, 90)
    ys = np.linspace(-1.4, 1.4, 70)
    Vg = np.array([[V(x, y, 0.0) for x in xs] for y in ys])
    vlim = np.nanpercentile(np.abs(Vg), 94)
    Vc = np.clip(Vg, -vlim, vlim)

    xq = np.linspace(-1.85, 1.85, 19)
    yq = np.linspace(-1.25, 1.25, 13)
    Ex = np.zeros((yq.size, xq.size)); Ey = np.zeros((yq.size, xq.size))
    for j, y in enumerate(yq):
        for i, x in enumerate(xq):
            ex, ey, _ = E(x, y, 0.0)
            n = np.hypot(ex, ey) or 1.0
            Ex[j, i], Ey[j, i] = ex / n, ey / n     # unit arrows: show direction

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    im = ax.imshow(Vc, extent=[xs[0], xs[-1], ys[0], ys[-1]], origin="lower",
                   cmap="RdBu_r", vmin=-vlim, vmax=vlim, aspect="equal",
                   interpolation="bilinear")            # raster fill -> compact SVG
    ax.contour(xs, ys, Vc, levels=np.linspace(-vlim, vlim, 13),
               colors=INK, linewidths=0.5, alpha=0.6)
    ax.quiver(xq, yq, Ex, Ey, color="#222222", scale=26, width=0.004, alpha=0.85)
    ax.plot(a, 0, "o", color=FLOW, ms=10, mec="white")
    ax.plot(-a, 0, "o", color=STEEL, ms=10, mec="white")
    ax.set_xlim(xs[0], xs[-1]); ax.set_ylim(ys[0], ys[-1]); ax.set_aspect("equal")
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title(r"Dipole potential $V$ with field $E=-\nabla V$ (arrows)")
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.02)
    cb.set_label("$V$  (volts)")
    _save(fig, "fig1_potential_map.svg")
    caps["fig1_potential_map.svg"] = (
        "Potential V of a dipole (red positive, blue negative) with equipotential contours "
        "and unit arrows of E = -grad V from field_from_potential. The field points downhill "
        "in V, crossing every equipotential at right angles.")

    # Fig 2 -- along a horizontal line: E_x is minus the slope of V.
    y0 = 0.5
    xl = np.linspace(-2.0, 2.0, 320)
    Vl = np.array([V(x, y0, 0.0) for x in xl])
    Exl = np.array([E(x, y0, 0.0)[0] for x in xl])
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(xl, Vl, color=INK, lw=2.2, label=r"$V(x)$")
    ax.set_xlabel("$x$  (along $y=%.1f$)" % y0); ax.set_ylabel("$V$  (volts)", color=INK)
    ax.axhline(0, color="#cccccc", lw=0.7)
    ax2 = ax.twinx()
    ax2.plot(xl, Exl, color=FLOW, lw=2.0, label=r"$E_x=-\partial_x V$")
    ax2.set_ylabel(r"$E_x$  (V/m)", color=FLOW)
    ax.set_title(r"$E=-\nabla V$: the field is minus the slope of $V$")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper right", frameon=False)
    _save(fig, "fig2_slope_relation.svg")
    caps["fig2_slope_relation.svg"] = (
        "Potential V(x) (blue) and the recovered field E_x = -dV/dx (orange) along a line "
        "offset from the charges. E_x is largest where V is steepest and reverses sign "
        "where V turns over -- a direct read of E = -grad V from field_from_potential.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
