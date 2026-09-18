"""Module 4.1 figures — enthalpy across the two-phase region (h and u differ by the
flow work pv), and why Q = dH exactly in a constant-pressure process.

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
from enthalpy import (                            # noqa: E402
    enthalpy, internal_energy_from_quality, enthalpy_from_quality,
    quality_from_enthalpy, const_pressure_heat,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

# Saturated water at p = 10 bar  [Moran 8e, Table A-3].
P_KPA = 1000.0
HF, HG = 762.81, 2778.1                            # kJ/kg
UF, UG = 761.68, 2583.6                            # kJ/kg
VF, VG = 1.1273e-3, 0.19444                        # m^3/kg


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — both h and u run linearly across the dome (the lever rule), but h
    # sits above u everywhere by the flow work pv, and the gap WIDENS with
    # quality because the vapour occupies so much more volume.
    x = np.linspace(0.0, 1.0, 200)
    h = np.array([enthalpy_from_quality(HF, HG, xi) for xi in x])
    u = np.array([internal_energy_from_quality(UF, UG, xi) for xi in x])
    v = VF + x * (VG - VF)
    pv = P_KPA * v                                  # kJ/kg
    # h = u + pv holds pointwise across the dome; check it at the two saturation ends
    assert abs(enthalpy(UF, P_KPA, VF) - HF) < 0.5
    assert abs(enthalpy(UG, P_KPA, VG) - HG) < 0.5

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot(x, h, color=INK, lw=2.3, label=r"enthalpy $h=h_f+x\,h_{fg}$")
    ax.plot(x, u, color=FLOW, lw=2.1, ls="--", label=r"internal energy $u$")
    ax.fill_between(x, u, h, color=ALT, alpha=0.18, lw=0,
                    label=r"flow work $pv$  (the gap)")
    ax.set_xlim(0, 1)
    ax.set_xlabel(r"quality $x$   (mass fraction vapour, at 10 bar)")
    ax.set_ylabel(r"specific energy (kJ/kg)")
    ax.set_title(r"$h=u+pv$ across the two-phase region")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_h_and_u_vs_quality.svg")
    caps["fig1_h_and_u_vs_quality.svg"] = (
        r"Saturated water at 10 bar (Table A-3) as it evaporates. Both enthalpy "
        r"(enthalpy_from_quality) and internal energy "
        r"(internal_energy_from_quality) are linear in the quality $x$ — the "
        r"lever rule — but $h$ lies above $u$ by the flow work $pv$, and that gap "
        r"grows from " + "%.1f" % (P_KPA * VF) + r" kJ/kg in the saturated liquid "
        r"to " + "%.1f" % (P_KPA * VG) + r" kJ/kg in the saturated vapour, "
        r"because the same kilogram now occupies "
        + "%.0f" % (VG / VF) + r" times the volume. Enthalpy is exactly the "
        r"combination that already contains the work needed to push that volume "
        r"across a boundary, which is why it, not $u$, appears in every "
        r"control-volume balance.")

    # Fig 2 — heating 2 kg at constant pressure.  Because W = p dV exactly
    # cancels the pv part, Q = m dh with no correction term: read the heat
    # straight off the enthalpy axis (const_pressure_heat).
    m = 2.0
    Q = np.array([const_pressure_heat(HF, hi, m) for hi in h])
    Q_total = const_pressure_heat(HF, HG, m)
    x_half = quality_from_enthalpy(enthalpy_from_quality(HF, HG, 0.5), HF, HG)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(x, Q, color=INK, lw=2.4)
    ax.fill_between(x, 0, Q, color=INK, alpha=0.10, lw=0)
    ax.plot([0.5], [const_pressure_heat(HF, enthalpy_from_quality(HF, HG, 0.5), m)],
            marker="o", ms=8, mfc="white", mec=FLOW, mew=1.8, ls="none")
    ax.annotate(r"half evaporated: %.0f kJ" % (Q_total / 2),
                xy=(0.5, Q_total / 2), xytext=(0.13, Q_total * 0.72),
                fontsize=9.5, color="0.3",
                arrowprops=dict(arrowstyle="->", color="0.5", lw=1.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, Q_total * 1.08)
    ax.set_xlabel(r"quality $x$   (round trip quality_from_enthalpy $\rightarrow$ %.2f)" % x_half)
    ax.set_ylabel(r"heat supplied $Q$ (kJ)")
    ax.set_title(r"At constant pressure the heat IS the enthalpy change")
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_constant_pressure_heat.svg")
    caps["fig2_constant_pressure_heat.svg"] = (
        r"Boiling 2 kg of water at a fixed 10 bar. In a constant-pressure process "
        r"the boundary work $p\,\Delta V$ exactly absorbs the $pv$ part of the "
        r"enthalpy, so the energy balance reduces to $Q=m\,\Delta h=\Delta H$ "
        r"(const_pressure_heat) with no work term left over — the heat can be "
        r"read directly off an enthalpy table. Taking the charge from saturated "
        r"liquid to saturated vapour costs " + "%.0f" % Q_total + r" kJ, all of "
        r"it latent: the temperature never moves off "
        r"$T_{sat}=179.9\,^\circ$C while this is happening.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
