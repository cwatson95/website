"""PK-04 figures — the KrF* excimer pulse & the EEDF rate coefficient (Arrhenius).

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
from molecular_kinetics import (                   # noqa: E402
    simulate_krf, default_krf_params, _pump_pulse, photon_energy_eV,
    rate_coefficient_maxwellian, rate_coefficient_step_closed_form,
    K_B_EV,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the 0-D KrF* excimer pulse from simulate_krf(): the Gaussian pump
    # builds the precursor Kr*, the harpoon Kr*+F2->KrF*+F builds the excimer to
    # a peak, then 25-ns radiative decay drains it while 248 nm photons pile up.
    res = simulate_krf()
    p = default_krf_params()
    t_ns = res["t"] * 1e9
    U = 1e22                                       # density unit for the axis [m^-3]
    pump = _pump_pulse(res["t"], p["t0"], p["tau_p"])   # module's own pump shape g(t)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(t_ns, 2.3 * pump, color="#9a9a9a", lw=1.4, ls="--",
            label=r"pump $g(t)$ (scaled)")
    ax.plot(t_ns, res["Krs"] / U, color=FLOW, lw=2,
            label=r"$\mathrm{Kr}^*$ precursor")
    ax.plot(t_ns, res["photons"] / U, color=STEEL, lw=1.8,
            label=r"248 nm photons (cumulative)")
    ax.plot(t_ns, res["KrFs"] / U, color=INK, lw=2.4,
            label=r"$\mathrm{KrF}^*$ excimer")
    tpk = res["peak_time"] * 1e9
    ax.plot([tpk], [res["peak_KrFs"] / U], marker="o", ms=5, color=INK)
    ax.annotate(r"peak $1.45\times10^{22}\,\mathrm{m^{-3}}$ at 54 ns",
                xy=(tpk, res["peak_KrFs"] / U), xytext=(tpk + 8, 1.62),
                color=INK, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=INK, lw=0.8))
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 2.5)
    ax.set_xlabel("time $t$ [ns]")
    ax.set_ylabel(r"density [$10^{22}\,\mathrm{m^{-3}}$]")
    ax.set_title("KrF* excimer pulse: harpoon builds it, 25-ns decay drains it")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_krf_excimer_pulse.svg")
    caps["fig1_krf_excimer_pulse.svg"] = (
        "0-D KrF* excimer pulse from simulate_krf(): a Gaussian discharge $g(t)$ "
        "(grey, scaled) pumps the precursor Kr* (orange), which feeds the harpoon "
        "Kr*+F2->KrF*+F that builds the KrF* excimer (blue) to a peak "
        "$1.45\\times10^{22}\\,$m$^{-3}$ at ~54 ns; then $\\tau=25\\,$ns radiative "
        "decay drains it while cumulative 248 nm photons (steel) accumulate. The "
        "closed reactions conserve the Kr- and F-atom inventories to ~$10^{-15}$.")

    # Fig 2 — electron-impact rate coefficient k = <sigma v> over a Maxwellian
    # EEDF for a step (threshold) cross-section: dots are the numeric energy
    # integral (the module's own rate_coefficient_maxwellian), curves the closed
    # form sigma0<v>(1+Eth/kT)e^{-Eth/kT}.  The e^{-Eth/kT} tail is Arrhenius:
    # the cross-section threshold acts as the activation energy.
    sigma0 = 1.0e-20
    kT_line = np.linspace(0.65, 5.0, 250)          # electron temperature [eV]
    kT_pts = np.linspace(0.7, 5.0, 13)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for Eth, col, lab in [(9.9, INK, "9.9 eV (Kr excitation)"),
                          (14.0, FLOW, "14 eV (Kr ionization)")]:
        k_cf = rate_coefficient_step_closed_form(kT_line / K_B_EV, sigma0, Eth)
        k_num = [rate_coefficient_maxwellian(kT / K_B_EV, sigma0, Eth)
                 for kT in kT_pts]
        ax.plot(kT_line, k_cf, color=col, lw=2,
                label=fr"$E_{{\rm th}}=${lab}")
        ax.plot(kT_pts, k_num, ls="none", marker="o", ms=4.5,
                mfc="white", mec=col, mew=1.3)
    ax.set_yscale("log")
    ax.set_xlim(0.65, 5.0)
    ax.set_ylim(1e-22, 3e-14)
    ax.set_xlabel(r"electron temperature $kT$ [eV]")
    ax.set_ylabel(r"$k=\langle\sigma v\rangle$ [m$^3$/s]")
    ax.set_title(r"Threshold $\to$ Arrhenius: $k\propto e^{-E_{\rm th}/kT}$")
    ax.annotate("dots: numeric EEDF integral\ncurves: closed form",
                xy=(2.6, 3e-21), color="#555555", fontsize=8.5)
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    _save(fig, "fig2_rate_coefficient_arrhenius.svg")
    caps["fig2_rate_coefficient_arrhenius.svg"] = (
        "Electron-impact rate coefficient $k=\\langle\\sigma v\\rangle$ over a "
        "Maxwellian EEDF for a step cross-section ($\\sigma_0=10^{-20}\\,$m$^2$), "
        "vs electron temperature $kT$: dots are the numeric energy integral "
        "rate_coefficient_maxwellian, curves the closed form "
        "$\\sigma_0\\langle v\\rangle(1+E_{\\rm th}/kT)e^{-E_{\\rm th}/kT}$. The "
        "steep $e^{-E_{\\rm th}/kT}$ tail is the Arrhenius law: the cross-section "
        "threshold $E_{\\rm th}$ (9.9 eV excitation, 14 eV ionization) plays the "
        "role of the activation energy.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)
    print("248 nm photon energy =", round(photon_energy_eV(248.0), 3), "eV")


if __name__ == "__main__":
    main()
