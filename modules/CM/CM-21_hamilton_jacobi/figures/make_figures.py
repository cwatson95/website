"""CM-21 figures — pendulum separatrix in phase space, and the anharmonic period.

Generates SVG figures into this `figures/` directory (plus captions.json) by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path'), saved
next to a captions.json mapping each filename to a short caption.
"""
import json
import math
import os
import sys

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"
matplotlib.rcParams["font.size"] = 11
import matplotlib.pyplot as plt                    # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from hamilton_jacobi import (                      # noqa: E402
    turning_points, action_variable, period,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"
PI = math.pi


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    m = 1.0
    V = lambda q: 1.0 - math.cos(q)                 # pendulum potential, E_sep = 2

    # ---- Fig 1: phase portrait with the separatrix --------------------------
    fig, ax = plt.subplots(figsize=(6.2, 3.5))

    # librations (E < 2): closed orbits between the turning points
    for E, col in [(0.4, STEEL), (1.0, ALT), (1.6, FLOW)]:
        a, b = turning_points(V, E, -PI + 1e-6, PI - 1e-6, 0.0)
        qq = np.linspace(a, b, 240)
        pp = np.sqrt(np.clip(2.0 * m * (E - (1.0 - np.cos(qq))), 0.0, None))
        ax.plot(qq, pp, color=col, lw=1.6)
        ax.plot(qq, -pp, color=col, lw=1.6, label=fr"$E={E}$ (libration)")

    # separatrix (E = 2): runs into the saddles at q = +/- pi
    qs = np.linspace(-PI, PI, 400)
    psep = np.sqrt(np.clip(2.0 * m * (2.0 - (1.0 - np.cos(qs))), 0.0, None))
    ax.plot(qs, psep, color="k", lw=2.0, label=r"$E=2$ (separatrix)")
    ax.plot(qs, -psep, color="k", lw=2.0)

    # rotations (E > 2): open curves, p never vanishes
    for E in (2.6, 3.6):
        pr = np.sqrt(2.0 * m * (E - (1.0 - np.cos(qs))))
        ax.plot(qs, pr, color="#9aa0a6", lw=1.1)
        ax.plot(qs, -pr, color="#9aa0a6", lw=1.1)

    ax.plot([0.0], [0.0], "o", color=INK, ms=6, zorder=5)          # center
    ax.plot([-PI, PI], [0.0, 0.0], "x", color="k", ms=8, mew=2, zorder=5)  # saddles
    ax.set_xlim(-PI, PI); ax.set_ylim(-3.2, 3.2)
    ax.set_xticks([-PI, 0, PI]); ax.set_xticklabels([r"$-\pi$", "0", r"$\pi$"])
    ax.set_xlabel(r"angle $q$"); ax.set_ylabel(r"momentum $p$")
    ax.set_title("Pendulum phase portrait: libration, separatrix, rotation")
    ax.legend(loc="upper right", frameon=False, fontsize=8)
    _save(fig, "fig1_separatrix.svg")
    caps["fig1_separatrix.svg"] = (
        "Pendulum phase portrait for V(q) = 1 - cos q. Closed orbits (libration, "
        "E < 2) lie inside the separatrix (black, E = 2), which runs into the "
        "saddle points at q = +/- pi; for E > 2 the pendulum rotates (open grey "
        "curves). Libration turning points are located with the module's "
        "turning_points; the origin is the stable centre.")

    # ---- Fig 2: anharmonic period vs isochronous SHO ------------------------
    Vsho = lambda q: 0.5 * q * q                    # harmonic, omega = 1
    Es = np.linspace(0.03, 1.985, 70)
    Tpend = [period(V, m, float(E), -PI + 1e-6, PI - 1e-6, 0.0) for E in Es]
    Tsho = [period(Vsho, m, float(E), -12.0, 12.0, 0.0) for E in Es]

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(Es, Tsho, color=INK, lw=2.0, label="harmonic well (isochronous)")
    ax.plot(Es, Tpend, color=FLOW, lw=2.0, label="pendulum (anharmonic)")
    ax.axhline(2.0 * PI, color="#aaaaaa", lw=0.7, ls=":")
    ax.axvline(2.0, color="#9aa0a6", lw=1.0, ls="--")
    ax.text(1.62, 7.0, r"separatrix $E=2$", color="#6b7075", fontsize=8, rotation=90)
    ax.text(0.06, 6.45, r"$2\pi$", color="#888888", fontsize=9)
    # an action value computed by the module, quoted in the caption
    Jsho = action_variable(Vsho, m, 1.0, -12.0, 12.0, 0.0)
    ax.set_ylim(5.8, 17.5)
    ax.set_xlabel(r"energy $E$"); ax.set_ylabel(r"period $T(E)=dJ/dE$")
    ax.set_title("Oscillation period: anharmonic growth toward the separatrix")
    ax.legend(loc="upper left", frameon=False)
    _save(fig, "fig2_anharmonic_period.svg")
    caps["fig2_anharmonic_period.svg"] = (
        "Oscillation period T(E) = dJ/dE from the module's period(). The harmonic "
        "well (blue) is isochronous, T = 2 pi for every amplitude (its action is "
        f"J(E=1) = {Jsho:.3f}), but the anharmonic pendulum (orange) takes ever "
        "longer as its energy nears the separatrix E = 2, where T diverges. The "
        "two agree at small E, where the pendulum is effectively harmonic.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
