"""Module 11.1 figures — how much water air can actually hold, and the moist-air
enthalpy that latent heat comes to dominate.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
Saturation data p_g(T) and h_g(T) come from ../../../steam_tables/ (Table A-2).
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
from dry_bulb import (                            # noqa: E402
    EPS, humidity_ratio_from_pressures, relative_humidity,
    vapor_pressure_from_phi, vapor_pressure_from_ratio,
    mixture_enthalpy_per_dry_air, vapor_enthalpy_approx,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

A2 = os.path.join(HERE, "..", "..", "..", "steam_tables",
                  "A2_sat_water_temperature.csv")
P_ATM = 101.325                                    # kPa
CPA = 1.005                                        # kJ/kg(dry air).K


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _sat_table():
    T, pg, hg = [], [], []
    with open(A2, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            T.append(float(row["T_C"]))
            pg.append(float(row["P_bar"]) * 100.0)  # bar -> kPa
            hg.append(float(row["hg_kJkg"]))
    return np.array(T), np.array(pg), np.array(hg)


def main():
    caps = {}
    Tt, pgt, hgt = _sat_table()
    pg_of = lambda t: float(np.interp(t, Tt, pgt))
    hg_of = lambda t: float(np.interp(t, Tt, hgt))

    # Fig 1 — the capacity of air to hold water is set by p_g(T), which climbs
    # steeply.  At fixed relative humidity the absolute moisture therefore rises
    # sharply with temperature: warm air at 50% RH holds far more water than
    # cold air at 100%.
    phi = np.linspace(0.0, 1.0, 200)

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    for T_db, c, ls in ((10.0, INK, "-"), (25.0, FLOW, "--"), (40.0, ALT, ":")):
        pg = pg_of(T_db)
        omega = np.array([humidity_ratio_from_pressures(
            vapor_pressure_from_phi(f, pg), P_ATM) for f in phi])
        ax.plot(phi * 100, omega * 1000, color=c, lw=2.2, ls=ls,
                label=r"dry-bulb $%g\,^\circ$C" % T_db)
    ax.set_xlim(0, 100)
    ax.set_xlabel(r"relative humidity $\phi$ (%)")
    ax.set_ylabel(r"humidity ratio $\omega$ (g water / kg dry air)")
    ax.set_title(r"Warm air holds far more water at the same $\phi$")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_humidity_ratio.svg")
    caps["fig1_humidity_ratio.svg"] = (
        r"Relative humidity and humidity ratio are not interchangeable. "
        r"$\phi=p_v/p_g(T)$ measures how close the air is to saturating "
        r"(relative_humidity), while $\omega=0.622\,p_v/(p-p_v)$ is the actual "
        r"mass of water carried per kilogram of dry air "
        r"(humidity_ratio_from_pressures). Because $p_g$ rises steeply with "
        r"temperature, air at 40 $^\circ$C and 50% RH holds "
        + "%.1f" % (1000 * humidity_ratio_from_pressures(
            vapor_pressure_from_phi(0.5, pg_of(40.0)), P_ATM)) +
        r" g/kg — more than saturated air at 10 $^\circ$C, which manages only "
        + "%.1f" % (1000 * humidity_ratio_from_pressures(pg_of(10.0), P_ATM)) +
        r" g/kg. This is why cooling humid air condenses water out of it, and "
        r"why the constant $\epsilon=" + "%.3f" % EPS + r"$ (the molecular-weight "
        r"ratio of water to air) appears in every psychrometric formula.")

    # Fig 2 — moist-air enthalpy per unit DRY air.  The dry-air part is linear
    # and modest; the vapour part carries latent heat and comes to dominate,
    # which is why air conditioning is mostly a dehumidification problem.
    T_grid = np.linspace(5.0, 45.0, 200)
    h_dry = CPA * T_grid
    h_tot_50 = np.array([mixture_enthalpy_per_dry_air(
        CPA * t,
        humidity_ratio_from_pressures(vapor_pressure_from_phi(0.5, pg_of(t)), P_ATM),
        vapor_enthalpy_approx(hg_of(t))) for t in T_grid])
    h_tot_90 = np.array([mixture_enthalpy_per_dry_air(
        CPA * t,
        humidity_ratio_from_pressures(vapor_pressure_from_phi(0.9, pg_of(t)), P_ATM),
        vapor_enthalpy_approx(hg_of(t))) for t in T_grid])

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot(T_grid, h_dry, color="0.55", lw=2.0, ls="-.",
            label=r"dry air alone, $c_{pa}T$")
    ax.plot(T_grid, h_tot_50, color=INK, lw=2.3, label=r"moist air at $\phi=50$%")
    ax.plot(T_grid, h_tot_90, color=FLOW, lw=2.3, ls="--",
            label=r"moist air at $\phi=90$%")
    ax.fill_between(T_grid, h_dry, h_tot_90, color=ALT, alpha=0.10, lw=0)
    ax.text(33, 62, "latent heat\ncarried by the vapour", fontsize=9,
            color="0.35", ha="center")
    ax.set_xlim(5, 45)
    ax.set_xlabel(r"dry-bulb temperature ($^\circ$C)")
    ax.set_ylabel(r"enthalpy per kg dry air (kJ/kg)")
    ax.set_title(r"Moist-air enthalpy is mostly latent")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_moist_air_enthalpy.svg")
    caps["fig2_moist_air_enthalpy.svg"] = (
        r"Moist-air enthalpy is booked per kilogram of DRY air, "
        r"$h=h_a+\omega h_v$ (mixture_enthalpy_per_dry_air), because the dry air "
        r"is the only component whose mass is conserved through a "
        r"humidifier or a cooling coil. With $h_v\approx h_g(T)$ "
        r"(vapor_enthalpy_approx, the low-pressure approximation) the vapour term "
        r"dwarfs the dry-air term as soon as the air is warm and damp: at "
        r"35 $^\circ$C and 90% RH the total is "
        + "%.0f" % float(np.interp(35.0, T_grid, h_tot_90)) + r" kJ/kg against "
        r"only " + "%.0f" % (CPA * 35.0) + r" kJ/kg for the air itself. Nearly "
        r"all of an air conditioner's duty is therefore spent condensing water, "
        r"not lowering temperature. vapor_pressure_from_ratio inverts $\omega$ "
        r"back to a partial pressure when the dew point is wanted.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
