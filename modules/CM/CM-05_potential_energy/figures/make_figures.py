"""CM-05 figures — a double-well potential landscape and energy conservation.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
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
from potential_energy import (                     # noqa: E402
    force_from_potential, total_energy, is_equilibrium, is_stable,
)

INK, FLOW, ALT, FOUR = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — double-well U(x), the force F=-dU/dx, and the classified equilibria.
    Uw = lambda x: x ** 4 - 2.0 * x ** 2                 # 1-D double well
    U3 = lambda x, y, z: x ** 4 - 2.0 * x ** 2           # same potential embedded in 3-D
    F = force_from_potential(U3)                         # F = -grad U (real function)
    xs = np.linspace(-1.8, 1.8, 400)
    Ux = [Uw(float(x)) for x in xs]
    Fx = [F(float(x), 0.0, 0.0)[0] for x in xs]

    eqs = [-1.0, 0.0, 1.0]
    stable = [x for x in eqs if is_equilibrium(Uw, x) and is_stable(Uw, x)]
    unstable = [x for x in eqs if is_equilibrium(Uw, x) and not is_stable(Uw, x)]

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(xs, Ux, color=INK, lw=2, label=r"$U(x)=x^4-2x^2$")
    ax.plot(xs, Fx, color=FLOW, lw=2, label=r"$F=-\frac{dU}{dx}$")
    ax.axhline(0, color="#aaaaaa", lw=0.6)
    ax.plot(stable, [Uw(x) for x in stable], "o", color=ALT, ms=9, label="stable minima")
    ax.plot(unstable, [Uw(x) for x in unstable], "s", color=FOUR, ms=9, label="unstable maximum")
    E = -0.5
    ax.axhline(E, color="#888888", ls=":", lw=1.2)
    ax.text(1.25, E + 0.05, fr"$E={E}$ (turning points)", fontsize=9, color="#555555")
    ax.set_xlabel("position $x$"); ax.set_ylabel("energy / force (SI)")
    ax.set_title(r"Double well: force $-dU/dx$ pushes toward the stable minima")
    ax.legend(loc="upper center", frameon=False, ncol=2, fontsize=9)
    _save(fig, "fig1_double_well.svg")
    caps["fig1_double_well.svg"] = (
        "Potential U(x)=x^4-2x^2 with the force F=-dU/dx from force_from_potential(). "
        "is_equilibrium / is_stable flag x=+/-1 as stable minima (circles) and x=0 as an "
        "unstable maximum (square); F is zero there and points downhill elsewhere. A level "
        "E=-0.5 cuts the wells at the classical turning points.")

    # Fig 2 — energy conservation of a 1-D oscillator: T and U trade off, E constant.
    m, k, A = 1.0, 4.0, 1.0
    w = math.sqrt(k / m)
    Usp = lambda x, y, z: 0.5 * k * (x * x + y * y + z * z)
    ts = np.linspace(0.0, 2.0 * math.pi / w, 240)
    KE, PE, Etot = [], [], []
    for t in ts:
        x = A * math.cos(w * float(t))
        v = -A * w * math.sin(w * float(t))
        e = total_energy(m, (v, 0.0, 0.0), Usp, (x, 0.0, 0.0))   # real function
        pe = Usp(x, 0.0, 0.0)
        Etot.append(e); PE.append(pe); KE.append(e - pe)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(ts, KE, color=FLOW, lw=2, label=r"kinetic $T$")
    ax.plot(ts, PE, color=ALT, lw=2, label=r"potential $U$")
    ax.plot(ts, Etot, color=INK, lw=2, ls="--", label=r"total $E=T+U$")
    ax.set_xlabel("time $t$ (s)"); ax.set_ylabel("energy (J)")
    ax.set_title(r"Conservative motion: $T$ and $U$ trade off, $E$ stays constant")
    ax.legend(loc="center right", frameon=False)
    _save(fig, "fig2_energy_conservation.svg")
    caps["fig2_energy_conservation.svg"] = (
        "A spring oscillator (k=4, A=1): kinetic T and potential U each swing between 0 and "
        "the total, but total_energy() (dashed) stays fixed at E = 1/2 k A^2 = 2 J -- the "
        "conserved mechanical energy of a conservative force.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
