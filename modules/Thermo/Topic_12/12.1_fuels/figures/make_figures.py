"""Module 12.1 figures — the air each fuel demands, and the flue-gas dew point that
excess air pushes down.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
The saturation curve used for the dew point is Table A-2 in ../../../steam_tables/.
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
from fuels import (                               # noqa: E402
    M_AIR, AIR_PER_O2, theoretical_O2, theoretical_air_molar,
    afr_molar_to_mass, equivalence_ratio, percent_excess_air,
    water_vapor_mole_fraction, dew_point_partial_pressure,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

A2 = os.path.join(HERE, "..", "..", "..", "steam_tables",
                  "A2_sat_water_temperature.csv")
P_ATM = 101.325                                    # kPa

# (name, nC, nH, nO, M_fuel)
FUELS = [("methane CH$_4$", 1, 4, 0, 16.04),
         ("octane C$_8$H$_{18}$", 8, 18, 0, 114.23),
         ("ethanol C$_2$H$_5$OH", 2, 6, 1, 46.07)]


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _tsat_of_pv():
    T, p = [], []
    with open(A2, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            T.append(float(row["T_C"]))
            p.append(float(row["P_bar"]) * 100.0)
    return np.array(T), np.array(p)


def main():
    caps = {}

    # Fig 1 — how much air each fuel needs, as a function of how much excess is
    # supplied.  The stoichiometric intercepts differ by nearly a factor of two
    # because oxygen already present in the fuel (ethanol) does not have to be
    # carried in with the air.
    theo = np.linspace(1.0, 2.0, 200)

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    for (name, nC, nH, nO, M), c, ls in zip(FUELS, (INK, FLOW, ALT),
                                            ("-", "--", ":")):
        afr_th = afr_molar_to_mass(theoretical_air_molar(nC, nH, nO), M)
        ax.plot(theo * 100, afr_th * theo, color=c, lw=2.2, ls=ls,
                label=r"%s  ($AF_{stoich}=%.1f$)" % (name, afr_th))
    ax.axvline(100.0, color="0.6", lw=1.2, ls="-.")
    ax.text(101, 6.5, "stoichiometric", fontsize=9, color="0.4", rotation=90)
    ax.set_xlim(100, 200)
    ax.set_xlabel(r"percent theoretical air (%)")
    ax.set_ylabel(r"air-fuel ratio, mass basis (kg air / kg fuel)")
    ax.set_title(r"Every fuel has its own appetite for air")
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_air_fuel_ratio.svg")
    caps["fig1_air_fuel_ratio.svg"] = (
        r"The stoichiometric oxygen requirement follows from the fuel formula "
        r"alone (theoretical_O2: $a=n_C+n_H/4-n_O/2$), and multiplying by "
        + "%.2f" % AIR_PER_O2 + r" mol of air per mol of O$_2$ then by "
        r"$M_{air}/M_{fuel}$ gives the mass-basis air-fuel ratio "
        r"(theoretical_air_molar, afr_molar_to_mass). Methane needs "
        + "%.1f" % afr_molar_to_mass(theoretical_air_molar(1, 4, 0), 16.04) +
        r" kg of air per kg of fuel, octane "
        + "%.1f" % afr_molar_to_mass(theoretical_air_molar(8, 18, 0), 114.23) +
        r", but ethanol only "
        + "%.1f" % afr_molar_to_mass(theoretical_air_molar(2, 6, 1), 46.07) +
        r" — its molecule already carries an oxygen atom, so less has to be "
        r"hauled in with the air. Supplying 150% theoretical air means 50% "
        r"excess (percent_excess_air) and an equivalence ratio "
        r"$\phi=" + "%.2f" % equivalence_ratio(1.5, 1.0) + r"$ "
        r"(equivalence_ratio), i.e. lean.")

    # Fig 2 — the practical consequence of excess air: it dilutes the product
    # water vapour, dropping its partial pressure and so the temperature at
    # which the flue gas will start to condense inside the stack.
    Tt, pt = _tsat_of_pv()
    theo2 = np.linspace(1.0, 3.0, 300)
    dew = []
    for t in theo2:
        # CH4 + 2t(O2 + 3.76 N2) -> CO2 + 2 H2O + 2(t-1) O2 + 7.52t N2
        n_dry = 1.0 + 2.0 * (t - 1.0) + 7.52 * t
        y_v = water_vapor_mole_fraction(2.0, n_dry)
        p_v = dew_point_partial_pressure(y_v, P_ATM)
        dew.append(float(np.interp(p_v, pt, Tt)))
    dew = np.array(dew)

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(theo2 * 100, dew, color=INK, lw=2.4,
            label=r"dew point of the combustion products")
    for t in (1.0, 2.0):
        i = int(np.argmin(abs(theo2 - t)))
        ax.plot([t * 100], [dew[i]], marker="o", ms=7.5, mfc="white", mec=FLOW,
                mew=1.8, ls="none")
        ax.annotate(r"%.0f%% air: %.0f $^\circ$C" % (t * 100, dew[i]),
                    xy=(t * 100, dew[i]), xytext=(t * 100 + 12, dew[i] + 2.5),
                    fontsize=9, color="0.3")
    ax.set_xlim(100, 300)
    ax.set_xlabel(r"percent theoretical air (%)   (methane, 1 atm)")
    ax.set_ylabel(r"product dew point ($^\circ$C)")
    ax.set_title(r"Excess air dilutes the water and lowers the dew point")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_product_dew_point.svg")
    caps["fig2_product_dew_point.svg"] = (
        r"Burning methane makes two moles of water for every mole of fuel, and "
        r"that water condenses if the flue gas cools below its dew point — "
        r"corroding stacks and heat exchangers. The dew point is the saturation "
        r"temperature at the vapour's PARTIAL pressure "
        r"(water_vapor_mole_fraction then dew_point_partial_pressure, inverted "
        r"through Table A-2), so adding excess air dilutes the products and "
        r"pushes it down: from " + "%.0f" % dew[0] + r" $^\circ$C at "
        r"stoichiometric to " + "%.0f" % dew[int(np.argmin(abs(theo2 - 2.0)))] +
        r" $^\circ$C at 200% theoretical air. That is one reason burners run "
        r"lean — though the same excess air also carries sensible heat up the "
        r"stack, which is the competing cost. Condensing boilers deliberately go "
        r"the other way and recover the latent heat.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
