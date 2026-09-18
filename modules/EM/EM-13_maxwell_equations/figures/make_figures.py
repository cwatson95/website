"""EM-13 figures -- a vacuum plane wave and Maxwell's displacement current.

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
from maxwell_equations import (                    # noqa: E402
    plane_wave_fields, partial_t, curl, C_SI,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # the vacuum plane wave built by the module (natural units c=1)
    E0, k, c = 1.0, 1.0, 1.0
    E, B, w = plane_wave_fields(E0, k, c)
    z = np.linspace(0.0, 4.0 * np.pi, 600)

    # Fig 1 -- E and B are in phase, transverse, and the wave propagates +z.
    Ex0 = np.array([E(0.0, 0.0, zz, 0.0)[0] for zz in z])
    By0 = np.array([B(0.0, 0.0, zz, 0.0)[1] for zz in z])
    t1 = np.pi / 2.0
    Ex1 = np.array([E(0.0, 0.0, zz, t1)[0] for zz in z])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(z, Ex0, color=INK, lw=2.2, label=r"$E_x(z,0)$")
    ax.plot(z, By0, color=FLOW, lw=2.0, ls="--", label=r"$cB_y(z,0)$")
    ax.plot(z, Ex1, color=STEEL, lw=1.4, alpha=0.7,
            label=r"$E_x(z,t_{1})$  (later)")
    ax.axhline(0, color="#aaaaaa", lw=0.6)
    ax.set_xlabel(r"position $z$"); ax.set_ylabel("field amplitude")
    ax.set_title(r"Vacuum plane wave: $E\perp B\perp k$, in phase, moving $+z$")
    ax.set_xlim(0, 4 * np.pi)
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig1_plane_wave.svg")
    caps["fig1_plane_wave.svg"] = (
        "The plane wave from plane_wave_fields (E0=1, k=1, c=1): Ex (blue) and the "
        "magnetic component cBy (orange dashed) coincide -- E and B are in phase, "
        "transverse, and equal in natural units. The faint curve is Ex a quarter "
        "period later, showing the crest has propagated toward +z.")

    # Fig 2 -- displacement current: curl B equals (1/c^2) dE/dt with no real current.
    Bsnap = lambda X, Y, Z: B(X, Y, Z, 0.0)        # noqa: E731  freeze B at t=0
    curlB_x = np.array([curl(Bsnap)(0.0, 0.0, zz)[0] for zz in z])
    disp_x = np.array([partial_t(E, 0.0, 0.0, zz, 0.0)[0] / c ** 2 for zz in z])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(z, curlB_x, color=INK, lw=2.2,
            label=r"$(\nabla\times\mathbf{B})_x$")
    ax.plot(z, disp_x, color=FLOW, lw=2.0, ls="--",
            label=r"$\frac{1}{c^{2}}\,\partial_t E_x=\mu_0 J_{d,x}$")
    ax.axhline(0, color="#aaaaaa", lw=0.6)
    ax.set_xlabel(r"position $z$"); ax.set_ylabel("curl / displacement term")
    ax.set_title(r"Displacement current sources $\nabla\times\mathbf{B}$  (vacuum, $J=0$)")
    ax.set_xlim(0, 4 * np.pi)
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig2_displacement_current.svg")
    caps["fig2_displacement_current.svg"] = (
        "Ampere-Maxwell with no conduction current: the curl of B (blue, from the "
        "module's curl operator) lies exactly on the displacement term "
        "(1/c^{2}) partial_t Ex = mu0 J_d (orange dashed, from partial_t). Maxwell's "
        "added displacement current is what lets a changing E sustain the curl of B, "
        "so the wave can propagate. Speed c = 1/sqrt(mu0 eps0) = %.3e m/s in SI."
        % C_SI)

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
