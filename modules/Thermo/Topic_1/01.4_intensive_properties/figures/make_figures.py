"""Module 1.4 figures — intensive properties are unchanged by scaling the system,
and combining subsystems needs a MASS-weighted average, not a plain one.

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
from intensive import (                           # noqa: E402
    density, specific_volume, mass_average, is_size_independent,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — scale a system by k and normalise every quantity to its k=1 value,
    # so extensive and intensive can share ONE axis.  Mass and volume ride the
    # diagonal; density and specific volume sit flat at 1.  That flat line is
    # what "intensive" means.
    m1, V1 = 2.0, 1.6                              # kg, m^3
    k = np.arange(1, 9)
    m_k, V_k = m1 * k, V1 * k
    rho = np.array([density(float(m), float(V)) for m, V in zip(m_k, V_k)])
    v = np.array([specific_volume(float(V), float(m)) for m, V in zip(m_k, V_k)])
    ok = is_size_independent(density(m1, V1), density(m1 * 8, V1 * 8))

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(k, m_k / m1, color=INK, lw=2.0, marker="o", ms=5.5, mfc="white",
            mew=1.5, label=r"mass $m$  (extensive)")
    ax.plot(k, V_k / V1, color=FLOW, lw=2.0, ls="--", marker="s", ms=5.5,
            mfc="white", mew=1.5, label=r"volume $V$  (extensive)")
    ax.plot(k, rho / rho[0], color=ALT, lw=2.4, ls="-", marker="^", ms=6.5,
            mfc="white", mew=1.7, label=r"density $\rho=m/V$  (intensive)")
    ax.plot(k, v / v[0], color=ALT, lw=1.2, ls=":", marker="v", ms=6.5,
            mfc="white", mew=1.3, label=r"specific volume $v=V/m$  (intensive)")
    ax.set_xlabel(r"scale factor $k$ (system copied $k$ times)")
    ax.set_ylabel(r"quantity relative to $k=1$")
    ax.set_title(r"Intensive properties do not know how big the system is")
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_intensive_invariance.svg")
    caps["fig1_intensive_invariance.svg"] = (
        r"The same rescaling that sends every extensive property up the diagonal "
        r"(module 1.3) leaves the intensive ones untouched. Copying a 2 kg, "
        r"1.6 m$^3$ system $k$ times multiplies mass and volume by $k$, but "
        r"density $\rho=m/V$ and specific volume $v=V/m$ (density, "
        r"specific_volume) stay pinned at their original value — the ratio of two "
        r"extensive quantities cancels the extent. is_size_independent confirms "
        r"it for an eight-fold scale-up. Temperature and pressure behave the same "
        r"way, which is why they can be quoted for a substance without saying how "
        r"much of it you have.")

    # Fig 2 — combining subsystems.  Two masses at different temperatures: the
    # correct mixture temperature is the MASS-weighted average (mass_average),
    # which only equals the plain mean at a 50/50 split.  Sweep the split.
    T_a, T_b = 300.0, 500.0
    m_total = 10.0
    frac = np.linspace(0.0, 1.0, 200)               # fraction of mass at T_a
    T_mass = np.array([mass_average([T_a, T_b], [f * m_total, (1 - f) * m_total])
                       for f in frac])
    T_plain = np.full_like(frac, 0.5 * (T_a + T_b))

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(frac, T_mass, color=INK, lw=2.2, label=r"mass-weighted  $\sum m_iT_i/\sum m_i$")
    ax.plot(frac, T_plain, color=FLOW, lw=2.0, ls="--",
            label=r"plain mean $\frac{1}{2}(T_a+T_b)$  (wrong)")
    ax.plot([0.5], [0.5 * (T_a + T_b)], marker="o", ms=8, mfc="white",
            mec=ALT, mew=1.8, ls="none", label=r"agree only at a 50/50 split")
    ax.set_xlabel(r"fraction of the total mass held at $T_a=300$ K")
    ax.set_ylabel(r"mixture temperature (K)")
    ax.set_title(r"An intensive property combines by MASS, not by count")
    ax.legend(loc="upper right", frameon=False, fontsize=8.5)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_mass_average.svg")
    caps["fig2_mass_average.svg"] = (
        r"Intensive properties add over subsystems only when weighted by mass. "
        r"Two parcels of the same substance at 300 K and 500 K are combined while "
        r"the mass split is swept: the correct mixture temperature (mass_average) "
        r"runs linearly from 500 K to 300 K, while the unweighted mean of the two "
        r"values is stuck at 400 K. They coincide at exactly one point, the 50/50 "
        r"split. Averaging intensive properties without their masses is one of "
        r"the most common bookkeeping errors in mixture problems.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
