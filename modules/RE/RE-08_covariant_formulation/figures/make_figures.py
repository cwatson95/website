"""RE-08 figures — covariant formulation: components mix under a boost while the
Lorentz invariants stay fixed.

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
from covariant_sr import (                         # noqa: E402
    ETA, mdot, transform_vector, transform_tensor2,
    antisymmetric_part, double_contract,
)
import lorentz                                     # noqa: E402  (RE-03, put on path by covariant_sr)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _field_invariant(F):
    """F_{mu nu} F^{mu nu} via the module's metric ETA and double_contract."""
    Flow = [[sum(ETA[m][a] * ETA[n][b] * F[a][b] for a in range(4) for b in range(4))
             for n in range(4)] for m in range(4)]
    return double_contract(Flow, F)


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    betas = np.linspace(-0.95, 0.95, 200)

    # Fig 1 — a 4-vector: time/space components mix under a boost, V.V invariant.
    V = [2.0, 1.0, 0.0, 0.0]                       # timelike: V.V = -4 + 1 = -3
    V0, V1, inv = [], [], []
    for b in betas:
        L = lorentz.boost(float(b), axis=1)
        Vp = transform_vector(L, V)
        V0.append(Vp[0]); V1.append(Vp[1]); inv.append(mdot(Vp, Vp))
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(betas, V0, color=FLOW, lw=2, label=r"$V'^{0}$ (time)")
    ax.plot(betas, V1, color=INK, lw=2, label=r"$V'^{1}$ (space)")
    ax.plot(betas, inv, color=ALT, lw=2, ls="--",
            label=r"$V'\!\cdot V'=\eta_{\mu\nu}V'^{\mu}V'^{\nu}$")
    ax.axhline(0, color="#bbbbbb", lw=0.6)
    ax.set_xlabel(r"boost rapidity parameter  $\beta$")
    ax.set_ylabel("component value")
    ax.set_title(r"4-vector under a boost: components mix, $V\!\cdot V=-3$ fixed")
    ax.legend(loc="upper center", frameon=False, ncol=1)
    _save(fig, "fig1_vector_boost_invariant.svg")
    caps["fig1_vector_boost_invariant.svg"] = (
        "A timelike 4-vector V = (2, 1, 0, 0) boosted along x by transform_vector for beta in "
        "(-0.95, 0.95). The time and space components V'^{0}, V'^{1} mix freely, yet the "
        "Minkowski square V.V = eta_{mu nu} V'^{mu} V'^{nu} stays pinned at -3: the scalar "
        "invariant the covariant formulation is built to expose.")

    # Fig 2 — the field tensor: a boost rotates E into B; F_{mu nu}F^{mu nu} invariant.
    F = [[0.0] * 4 for _ in range(4)]              # pure "electric" field in y: F^{02}
    F[0][2] = 1.0; F[2][0] = -1.0
    Ey, Bz, finv, asym = [], [], [], []
    for b in betas:
        L = lorentz.boost(float(b), axis=1)
        Fp = transform_tensor2(L, F)
        A = antisymmetric_part(Fp)
        Ey.append(Fp[0][2]); Bz.append(Fp[1][2]); finv.append(_field_invariant(Fp))
        asym.append(max(abs(Fp[i][j] - A[i][j]) for i in range(4) for j in range(4)))
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(betas, Ey, color=INK, lw=2, label=r"$F'^{02}$  ($\sim E_y$)")
    ax.plot(betas, Bz, color=FLOW, lw=2, label=r"$F'^{12}$  ($\sim B_z$)")
    ax.plot(betas, finv, color=ALT, lw=2, ls="--",
            label=r"$F_{\mu\nu}F^{\mu\nu}=-2$")
    ax.axhline(0, color="#bbbbbb", lw=0.6)
    ax.set_xlabel(r"boost $\beta$ along $x$")
    ax.set_ylabel("tensor component")
    ax.set_title(r"Field tensor $F^{\mu\nu}$ under a boost: $E$ and $B$ mix")
    ax.legend(loc="upper center", frameon=False)
    _save(fig, "fig2_field_tensor_boost.svg")
    caps["fig2_field_tensor_boost.svg"] = (
        "An antisymmetric field tensor F^{mu nu} starting as a pure electric field "
        "F^{02} ~ E_y, boosted along x by transform_tensor2. The boost generates a magnetic "
        "component F^{12} ~ B_z out of nothing -- moving electric fields look magnetic -- "
        "while the scalar F_{mu nu} F^{mu nu} = -2 and the antisymmetry are preserved.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
