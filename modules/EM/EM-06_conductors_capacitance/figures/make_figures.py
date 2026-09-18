"""EM-06 figures -- capacitor energy two ways, and capacitance vs geometry.

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
from conductors_capacitance import (               # noqa: E402
    capacitance_parallel_plate, capacitance_spherical, capacitance_isolated_sphere,
    energy_stored, field_energy,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- parallel plate: (1/2) C V^2 equals the field-energy integral.
    A, Volt = 0.01, 12.0
    side = math.sqrt(A)
    d = np.linspace(0.5e-3, 5.0e-3, 60)
    Wcap = np.array([energy_stored(capacitance_parallel_plate(A, dd), Volt) for dd in d])

    dmark = d[::6]
    Wfield = []
    for dd in dmark:
        Ez = Volt / dd
        Eunif = lambda x, y, z, _Ez=Ez: (0.0, 0.0, _Ez)   # uniform gap field
        Wfield.append(field_energy(Eunif, 0.0, side, 0.0, side, 0.0, dd, n=6))
    Wfield = np.array(Wfield)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(d * 1e3, Wcap * 1e9, color=INK, lw=2.2,
            label=r"$\frac{1}{2}CV^2$  ($C=\varepsilon_0 A/d$)")
    ax.plot(dmark * 1e3, Wfield * 1e9, "o", color=FLOW, ms=7,
            label=r"$\frac{\varepsilon_0}{2}\int|E|^2\,d\tau$")
    ax.set_xlabel(r"plate separation $d$  (mm)")
    ax.set_ylabel(r"stored energy $W$  (nJ)")
    ax.set_title(r"Capacitor energy two ways agree ($V=12$ V, $A=100\,\mathrm{cm}^2$)")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig1_energy_two_ways.svg")
    caps["fig1_energy_two_ways.svg"] = (
        "Energy of a parallel-plate capacitor versus gap d at fixed voltage. The charge "
        "picture (1/2)CV^2 (line, from capacitance_parallel_plate) matches the field-energy "
        "integral eps0/2 of |E|^2 over the gap (markers, from field_energy); both rise as "
        "1/d as the plates close.")

    # Fig 2 -- spherical capacitor approaching the isolated-sphere limit.
    a_in = 0.05
    ratio = np.linspace(1.25, 9.0, 160)            # b/a
    Csph = np.array([capacitance_spherical(a_in, a_in * rr) for rr in ratio])
    Ciso = capacitance_isolated_sphere(a_in)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(ratio, Csph / Ciso, color=INK, lw=2.4,
            label=r"spherical $C=\frac{4\pi\varepsilon_0 a b}{b-a}$")
    ax.axhline(1.0, color=FLOW, lw=1.6, ls="--",
               label=r"isolated sphere $4\pi\varepsilon_0 a$  ($b\to\infty$)")
    ax.set_xlabel(r"radius ratio $b/a$")
    ax.set_ylabel(r"$C/(4\pi\varepsilon_0 a)$")
    ax.set_title(r"Capacitance vs geometry: gap controls $C$")
    ax.set_ylim(0.9, 4.4)
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig2_capacitance_geometry.svg")
    caps["fig2_capacitance_geometry.svg"] = (
        "Capacitance of a spherical capacitor (inner radius a, outer b) normalized to the "
        "isolated-sphere value, from capacitance_spherical and capacitance_isolated_sphere. "
        "A tight gap (b/a near 1) gives large C; as b/a grows the outer shell stops "
        "mattering and C approaches the isolated-sphere limit 4 pi eps0 a.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
