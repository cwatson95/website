"""EM-14 figures -- Poynting flux, energy density, and field equipartition.

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
from conservation_laws import (                    # noqa: E402
    plane_wave_snapshot, poynting_vector, energy_density, C,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # a plane-wave snapshot built by the module: E along x, B along y
    E0, k = 1000.0, 2.0 * np.pi
    E, B = plane_wave_snapshot(E0, k)
    z = np.linspace(0.0, 2.0, 600)                 # two wavelengths

    u = np.array([energy_density(E, B)(0.0, 0.0, zz) for zz in z])
    Sz = np.array([poynting_vector(E, B)(0.0, 0.0, zz)[2] for zz in z])

    # Fig 1 -- energy density u and Poynting flux S, locked by S = c u.
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ln1, = ax.plot(z, u, color=INK, lw=2.2, label=r"$u$  (energy density)")
    ax.set_xlabel(r"position $z$")
    ax.set_ylabel(r"$u$  [J/m$^{3}$]", color=INK)
    ax.tick_params(axis="y", labelcolor=INK)
    ax2 = ax.twinx()
    ln2, = ax2.plot(z, Sz, color=FLOW, lw=2.0, ls="--",
                    label=r"$|\mathbf{S}|=\frac{1}{\mu_0}|\mathbf{E}\times\mathbf{B}|$")
    ax2.set_ylabel(r"$|\mathbf{S}|$  [W/m$^{2}$]", color=FLOW)
    ax2.tick_params(axis="y", labelcolor=FLOW)
    ax.set_title(r"Energy flux tracks energy density: $|\mathbf{S}|=c\,u$")
    ax.set_xlim(0, 2)
    ax.legend([ln1, ln2], [ln1.get_label(), ln2.get_label()],
              loc="upper right", frameon=False)
    _save(fig, "fig1_poynting_energy.svg")
    caps["fig1_poynting_energy.svg"] = (
        "For the plane-wave snapshot, the field energy density u (blue, left axis) "
        "and the Poynting flux |S| (orange dashed, right axis) have the identical "
        "cos^{2}(kz) profile. Their ratio is the speed of light: |S| = c u, so energy "
        "streams along +z at c.")

    # Fig 2 -- equipartition: electric and magnetic energy densities are equal.
    zeroE = lambda x, y, z: (0.0, 0.0, 0.0)         # noqa: E731
    zeroB = lambda x, y, z: (0.0, 0.0, 0.0)         # noqa: E731
    uE = np.array([energy_density(E, zeroB)(0.0, 0.0, zz) for zz in z])
    uB = np.array([energy_density(zeroE, B)(0.0, 0.0, zz) for zz in z])
    uT = np.array([energy_density(E, B)(0.0, 0.0, zz) for zz in z])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(z, uT, color=ALT, lw=2.4, label=r"$u=u_E+u_B$")
    ax.plot(z, uE, color=INK, lw=2.0,
            label=r"$u_E=\frac{\varepsilon_0}{2}|\mathbf{E}|^{2}$")
    ax.plot(z, uB, color=FLOW, lw=2.0, ls="--",
            label=r"$u_B=\frac{1}{2\mu_0}|\mathbf{B}|^{2}$")
    ax.set_xlabel(r"position $z$"); ax.set_ylabel(r"energy density  [J/m$^{3}$]")
    ax.set_title("Equipartition in a wave: electric energy $=$ magnetic energy")
    ax.set_xlim(0, 2)
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig2_equipartition.svg")
    caps["fig2_equipartition.svg"] = (
        "The same energy_density routine, fed the field with B (or E) zeroed, "
        "separates the electric part uE (blue) and magnetic part uB (orange dashed): "
        "they overlap exactly. In a plane wave the energy is shared equally between "
        "E and B, and their sum is the total density u (purple).")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
