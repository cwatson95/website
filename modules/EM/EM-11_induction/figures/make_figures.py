"""EM-11 figures -- Faraday's law (EMF = -dPhi/dt) and the two energy pictures.

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
from induction import (                            # noqa: E402
    flat_loop_surface, magnetic_flux, faraday_emf, lenz_sign,
    solenoid_inductance, energy_in_inductor, magnetic_field_energy_solenoid,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- a flat loop in a uniform field B(t) = B0 sin(wt) zhat. The flux is
    # computed with the module's surface integral; the EMF is -dPhi/dt (Faraday),
    # and the sign opposes the change in flux (Lenz).
    a, b = 0.10, 0.10                                 # 0.01 m^2 loop
    surf = flat_loop_surface(0.0, a, 0.0, b, z=0.0)
    B0, omega = 0.5, 100.0

    def flux_of_t(t):
        Bt = lambda x, y, z: (0.0, 0.0, B0 * math.sin(omega * t))
        return magnetic_flux(Bt, surf, n=10)          # exact for a uniform field

    t = np.linspace(0.0, 2.0 * (2.0 * math.pi / omega), 240)
    phi = np.array([flux_of_t(tt) for tt in t])
    emf = np.array([faraday_emf(flux_of_t, tt) for tt in t])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(t * 1e3, phi * 1e3, color=INK, lw=2, label=r"flux $\Phi(t)$")
    ax.axhline(0, color="#bbbbbb", lw=0.6)
    ax.set_xlabel("time  $t$  (ms)")
    ax.set_ylabel(r"flux $\Phi$  (mWb)", color=INK)
    ax.tick_params(axis="y", labelcolor=INK)
    ax2 = ax.twinx()
    ax2.plot(t * 1e3, emf, color=FLOW, lw=2, label=r"EMF $=-\,d\Phi/dt$")
    ax2.set_ylabel("EMF  (V)", color=FLOW)
    ax2.tick_params(axis="y", labelcolor=FLOW)
    ax.set_title(r"Faraday & Lenz: EMF $=-\,d\Phi/dt$ (90$^\circ$ out of phase)")
    lines = ax.get_lines()[:1] + ax2.get_lines()[:1]
    ax.legend(lines, [ln.get_label() for ln in lines], loc="upper right", frameon=False)
    # Lenz: when flux rises the EMF is negative (opposes), and vice versa.
    s_quarter = lenz_sign((flux_of_t(t[6] + 1e-4) - flux_of_t(t[6])) / 1e-4)
    _save(fig, "fig1_faraday_emf.svg")
    caps["fig1_faraday_emf.svg"] = (
        "A loop in a uniform field B(t) = B0 sin(wt): the flux Phi(t) (blue, via the "
        "module's surface integral) and the induced EMF = -dPhi/dt (orange). The EMF leads "
        "the flux by 90 degrees and always opposes the change in flux (Lenz's law); here "
        "the rising-flux quarter has sign " + str(s_quarter) + ".")

    # Fig 2 -- a solenoid's stored energy two ways: the circuit expression
    # W = (1/2) L I^2 and the field-integral (1/2mu0) int B^2 dV agree exactly.
    N, area, length = 1000, 1e-4, 0.20
    L = solenoid_inductance(N, area, length)
    I = np.linspace(0.0, 5.0, 120)
    W_circuit = np.array([energy_in_inductor(L, ii) for ii in I])
    W_field = np.array([magnetic_field_energy_solenoid(N, area, length, ii) for ii in I])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(I, W_circuit * 1e3, color=INK, lw=2.4,
            label=r"$\frac{1}{2}LI^{2}$  (circuit)")
    ax.plot(I[::4], W_field[::4] * 1e3, "o", color=FLOW, ms=5,
            label=r"$\frac{1}{2\mu_0}\int B^{2}\,dV$  (field)")
    ax.set_xlabel("current  $I$  (A)")
    ax.set_ylabel("stored energy  $W$  (mJ)")
    ax.set_title(fr"Solenoid energy, two pictures ($L={L*1e3:.2f}$ mH)")
    ax.legend(loc="upper left", frameon=False)
    _save(fig, "fig2_inductor_energy.svg")
    caps["fig2_inductor_energy.svg"] = (
        "Energy stored in a 1000-turn solenoid vs current. The circuit formula "
        "W = (1/2) L I^2 (curve) and the magnetic-field integral (1/2mu0) integral B^2 dV "
        "(dots) coincide -- the same energy whether attributed to the inductor or to the field.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
