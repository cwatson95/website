"""Module 11.2 figures — the wet-bulb depression as a humidity measurement, and the
adiabatic-saturator energy balance whose root defines it.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
Saturation data come from ../../../steam_tables/ (Table A-2).
"""
import csv
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
from wet_bulb import (                            # noqa: E402
    EPS, CPA, humidity_ratio_at_saturation, humidity_ratio_from_wet_bulb,
    adiabatic_saturator_residual, dry_air_enthalpy, dew_point_pressure,
    exit_humidity_ratio,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

A2 = os.path.join(HERE, "..", "..", "..", "steam_tables",
                  "A2_sat_water_temperature.csv")
P_ATM = 101.325                                    # kPa


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _sat_table():
    T, pg, hf, hg = [], [], [], []
    with open(A2, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            T.append(float(row["T_C"]))
            pg.append(float(row["P_bar"]) * 100.0)
            hf.append(float(row["hf_kJkg"]))
            hg.append(float(row["hg_kJkg"]))
    return (np.array(T), np.array(pg), np.array(hf), np.array(hg))


def main():
    caps = {}
    Tt, pgt, hft, hgt = _sat_table()
    pg_of = lambda t: float(np.interp(t, Tt, pgt))
    hf_of = lambda t: float(np.interp(t, Tt, hft))
    hg_of = lambda t: float(np.interp(t, Tt, hgt))

    def omega_from_wb(T_db, T_wb):
        op = humidity_ratio_at_saturation(pg_of(T_wb), P_ATM)
        return humidity_ratio_from_wet_bulb(
            op, dry_air_enthalpy(T_db), dry_air_enthalpy(T_wb),
            hf_of(T_wb), hg_of(T_wb), hg_of(T_db))

    # Fig 1 — a sling psychrometer reads two temperatures; their DIFFERENCE is
    # the humidity signal.  A large depression means dry air (fast evaporation
    # cools the wick hard); zero depression means saturated.
    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    for T_db, c, ls in ((20.0, INK, "-"), (30.0, FLOW, "--"), (40.0, ALT, ":")):
        dep = np.linspace(0.0, 16.0, 200)
        om = np.array([max(omega_from_wb(T_db, T_db - d), 0.0) for d in dep])
        ax.plot(dep, om * 1000, color=c, lw=2.2, ls=ls,
                label=r"dry-bulb $%g\,^\circ$C" % T_db)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 50)
    ax.set_xlabel(r"wet-bulb depression $T_{db}-T_{wb}$ (K)")
    ax.set_ylabel(r"humidity ratio $\omega$ (g / kg dry air)")
    ax.set_title(r"Two thermometers are enough to measure humidity")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_wet_bulb_depression.svg")
    caps["fig1_wet_bulb_depression.svg"] = (
        r"Why a sling psychrometer works. Water evaporating from the wet wick "
        r"draws its latent heat out of the passing air, so the wet-bulb "
        r"thermometer settles below the dry-bulb one by an amount that depends "
        r"on how much more water the air can absorb. Reading the depression "
        r"backwards through the adiabatic-saturation balance "
        r"(humidity_ratio_from_wet_bulb, with humidity_ratio_at_saturation "
        r"supplying $\omega'$) recovers the humidity ratio: at 30 $^\circ$C, a "
        r"zero depression means saturated air at "
        + "%.1f" % (1000 * omega_from_wb(30.0, 30.0)) + r" g/kg, while a 10 K "
        r"depression means only "
        + "%.1f" % (1000 * omega_from_wb(30.0, 20.0)) + r" g/kg. Warmer air "
        r"gives a steeper curve because it has more capacity to begin with.")

    # Fig 2 — where that number comes from: the adiabatic-saturator energy
    # balance is a residual in omega, and the reading is its root.  Plotting the
    # residual makes the "solve for omega" step visible instead of magic.
    T_db, T_wb = 30.0, 20.0
    op = humidity_ratio_at_saturation(pg_of(T_wb), P_ATM)
    omega_grid = np.linspace(0.0, 0.020, 300)
    resid = np.array([adiabatic_saturator_residual(
        o, op, dry_air_enthalpy(T_db), dry_air_enthalpy(T_wb),
        hg_of(T_db), hg_of(T_wb), hf_of(T_wb)) for o in omega_grid])
    root = omega_from_wb(T_db, T_wb)

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(omega_grid * 1000, resid, color=INK, lw=2.4,
            label=r"energy-balance residual (Eq. 12.50)")
    ax.axhline(0.0, color="0.6", lw=1.1, ls="-.")
    ax.plot([root * 1000], [0.0], marker="o", ms=9, mfc="white", mec=FLOW,
            mew=1.9, ls="none",
            label=r"the reading: $\omega=%.1f$ g/kg" % (root * 1000))
    ax.set_xlim(0, 20)
    ax.set_xlabel(r"trial humidity ratio $\omega$ (g / kg dry air)")
    ax.set_ylabel(r"residual (kJ / kg dry air)")
    ax.set_title(r"$T_{db}=30\,^\circ$C, $T_{wb}=20\,^\circ$C: solving for $\omega$")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_adiabatic_saturator_root.svg")
    caps["fig2_adiabatic_saturator_root.svg"] = (
        r"The wet-bulb reading is defined by an energy balance, and this is that "
        r"balance made visible. An adiabatic saturator takes air in at "
        r"$(T_{db},\omega)$ and returns it saturated at $T_{wb}$, with make-up "
        r"water supplied as liquid at $T_{wb}$; adiabatic_saturator_residual "
        r"measures how badly a trial $\omega$ fails to close it. The function is "
        r"linear in $\omega$ and crosses zero exactly once, at "
        + "%.1f" % (root * 1000) + r" g/kg — which is why the closed-form "
        r"humidity_ratio_from_wet_bulb can simply be solved rather than iterated. "
        r"dew_point_pressure then converts that $\omega$ to the partial pressure "
        r"whose saturation temperature is the dew point, and exit_humidity_ratio "
        r"handles the water mass balance when moisture is deliberately added.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
