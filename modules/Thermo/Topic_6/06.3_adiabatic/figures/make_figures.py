"""Module 6.3 figures — the isentropic temperature rise a compressor cannot avoid,
and the isentropic efficiency that measures how far a real device misses.

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
from adiabatic import (                           # noqa: E402
    is_adiabatic, cp_from_k, cv_from_k, temp_ratio_from_pressure,
    final_temp_isentropic, pressure_ratio_from_volume,
    isentropic_turbine_eff, isentropic_nozzle_eff,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

R_AIR = 0.287                                      # kJ/kg.K


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    assert is_adiabatic(0.0) and not is_adiabatic(5.0)

    # Fig 1 — compress a gas isentropically and its temperature MUST rise by
    # (p2/p1)^((k-1)/k).  The exponent is set by k alone, so a monatomic gas
    # heats far more than a polyatomic one for the same pressure ratio.
    pr = np.linspace(1.0, 20.0, 300)
    T1 = 300.0

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    for k, name, c, ls in ((1.667, "monatomic (Ar)", INK, "-"),
                           (1.400, "diatomic (air)", FLOW, "--"),
                           (1.300, "polyatomic (CO$_2$)", ALT, ":")):
        T2 = np.array([final_temp_isentropic(T1, p, 1.0, k) for p in pr])
        ax.plot(pr, T2, color=c, lw=2.1, ls=ls,
                label=r"$k=%.3f$  %s" % (k, name))
    ax.set_xlim(1, 20)
    ax.set_xlabel(r"pressure ratio $p_2/p_1$    (from $T_1=300$ K)")
    ax.set_ylabel(r"isentropic exit temperature $T_2$ (K)")
    ax.set_title(r"Isentropic compression: $T_2/T_1=(p_2/p_1)^{(k-1)/k}$")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_isentropic_temperature_rise.svg")
    caps["fig1_isentropic_temperature_rise.svg"] = (
        r"Compressing a gas without heat transfer or friction still heats it: "
        r"$T_2/T_1=(p_2/p_1)^{(k-1)/k}$ (temp_ratio_from_pressure, "
        r"final_temp_isentropic). The exponent depends only on the specific-heat "
        r"ratio, so at a 10:1 pressure ratio air reaches "
        + "%.0f" % final_temp_isentropic(300.0, 10.0, 1.0, 1.4) + r" K while "
        r"argon, with fewer ways to store energy internally, reaches "
        + "%.0f" % final_temp_isentropic(300.0, 10.0, 1.0, 1.667) + r" K. This "
        r"is the floor no compressor can beat, which is why multistage machines "
        r"intercool between stages. cp_from_k and cv_from_k recover the specific "
        r"heats themselves ($c_p=" + "%.3f" % cp_from_k(1.4, R_AIR) +
        r"$ kJ/kg$\cdot$K for air), and pressure_ratio_from_volume gives the "
        r"companion $pv^k=$ const form.")

    # Fig 2 — real devices miss the isentropic ideal.  For a turbine expanding
    # between fixed pressures, the isentropic efficiency scales the enthalpy drop
    # actually delivered; the exit state ends up hotter and higher in entropy.
    h1, h2s = 3230.0, 2480.0                        # kJ/kg, a steam expansion
    eta = np.linspace(0.5, 1.0, 300)
    h2 = h1 - eta * (h1 - h2s)
    w_act = h1 - h2

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(eta, w_act, color=INK, lw=2.4, label=r"actual work $h_1-h_2$")
    ax.axhline(h1 - h2s, color=FLOW, lw=1.6, ls="--",
               label=r"isentropic ideal $h_1-h_{2s}=%.0f$ kJ/kg" % (h1 - h2s))
    for e in (0.70, 0.85):
        ax.plot([e], [e * (h1 - h2s)], marker="o", ms=7.5, mfc="white",
                mec=ALT, mew=1.8, ls="none")
        ax.annotate(r"$\eta_t=%.2f$: %.0f kJ/kg" % (e, e * (h1 - h2s)),
                    xy=(e, e * (h1 - h2s)), xytext=(e - 0.015, e * (h1 - h2s) + 55),
                    fontsize=9, color="0.3", ha="right")
    ax.set_xlim(0.5, 1.0)
    ax.set_ylim(350, 830)
    ax.set_xlabel(r"isentropic turbine efficiency $\eta_t$")
    ax.set_ylabel(r"work delivered (kJ/kg)")
    ax.set_title(r"What irreversibility costs a turbine")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_isentropic_efficiency.svg")
    caps["fig2_isentropic_efficiency.svg"] = (
        r"The isentropic efficiency $\eta_t=(h_1-h_2)/(h_1-h_{2s})$ "
        r"(isentropic_turbine_eff) compares a real expansion against the "
        r"reversible one between the same pressures. The ideal drop here is "
        + "%.0f" % (h1 - h2s) + r" kJ/kg; a good steam turbine at "
        r"$\eta_t=0.85$ delivers " + "%.0f" % (0.85 * (h1 - h2s)) + r" kJ/kg and "
        r"the missing " + "%.0f" % (0.15 * (h1 - h2s)) + r" kJ/kg stays in the "
        r"steam as extra internal energy, leaving the exit hotter and at higher "
        r"entropy than the isentropic state. isentropic_nozzle_eff applies the "
        r"identical idea to exit kinetic energy instead of shaft work.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
