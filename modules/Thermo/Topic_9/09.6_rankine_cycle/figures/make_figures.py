"""Module 9.6 figures — the ideal Rankine cycle drawn inside the real steam dome,
and the boiler-pressure trade that reheat exists to fix.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
The saturation dome is read straight from ../../../steam_tables/ (Table A-2),
the same CSVs Topic 5 is built on.
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
from rankine_cycle import (                       # noqa: E402
    turbine_work, condenser_heat, pump_work, boiler_heat, rankine_efficiency,
    back_work_ratio, pump_work_approx, quality_from_entropy,
    enthalpy_two_phase, reheat_efficiency,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

A2 = os.path.join(HERE, "..", "..", "..", "steam_tables",
                  "A2_sat_water_temperature.csv")

# Saturated water at the two cycle pressures  [Moran 8e, Table A-3].
P_BOIL, P_COND = 80.0, 0.08                        # bar
SG_BOIL, HG_BOIL, TSAT_BOIL = 5.7432, 2758.0, 295.06
SF_C, SFG_C, HF_C, HFG_C, TSAT_C = 0.5926, 7.6361, 173.88, 2403.1, 41.51
VF_C = 1.0084e-3                                   # m^3/kg


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _dome():
    T, sf, sg = [], [], []
    with open(A2, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            T.append(float(row["T_C"]))
            sf.append(float(row["sf_kJkgK"]))
            sg.append(float(row["sg_kJkgK"]))
    return np.array(T), np.array(sf), np.array(sg)


def main():
    caps = {}

    # Fig 1 — the ideal cycle inside the real dome.  The turbine expansion ends
    # INSIDE the two-phase region, which is the characteristic problem of vapour
    # power plants: wet steam erodes the last blade rows.
    T, sf, sg = _dome()
    x2 = quality_from_entropy(SG_BOIL, SF_C, SF_C + SFG_C)
    h1 = HG_BOIL
    h2 = enthalpy_two_phase(x2, HF_C, HFG_C)
    h3 = HF_C
    wp = pump_work_approx(VF_C, P_COND * 100.0, P_BOIL * 100.0)
    h4 = h3 + wp
    eta = rankine_efficiency(h1, h2, h3, h4)
    bwr = back_work_ratio(h1, h2, h3, h4)

    s1, s2 = SG_BOIL, SG_BOIL
    s3 = SF_C
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    ax.plot(sf, T, color="0.6", lw=1.8)
    ax.plot(sg, T, color="0.6", lw=1.8, label=r"saturation dome (Table A-2)")
    ax.plot([s3, s3], [TSAT_C, TSAT_C + 1.5], color=ALT, lw=2.6,
            label=r"3$\rightarrow$4 pump  ($w_p=%.1f$ kJ/kg)" % wp)
    s_boil = np.linspace(s3, SG_BOIL, 100)
    T_boil = np.where(s_boil < np.interp(TSAT_BOIL, T, sf) + 1e-9,
                      np.interp(s_boil, sf, T), TSAT_BOIL)
    ax.plot(s_boil, np.maximum(T_boil, TSAT_C), color=FLOW, lw=2.4,
            label=r"4$\rightarrow$1 boiler")
    ax.plot([s1, s2], [TSAT_BOIL, TSAT_C], color=INK, lw=2.4,
            label=r"1$\rightarrow$2 turbine (isentropic)")
    ax.plot([s2, s3], [TSAT_C, TSAT_C], color="0.45", lw=2.4, ls="--",
            label=r"2$\rightarrow$3 condenser")
    for s, Tp, lab, dx, dy in ((s3, TSAT_C, "3", -0.30, -22), (s3, TSAT_C, "4", 0.10, 14),
                               (s1, TSAT_BOIL, "1", 0.13, 8),
                               (s2, TSAT_C, "2", 0.13, -6)):
        ax.plot([s], [Tp], marker="o", ms=6, mfc="white", mec="0.2", mew=1.5,
                ls="none", zorder=6)
        ax.text(s + dx, Tp + dy, lab, fontsize=11, color="0.2")
    ax.annotate(r"exit quality $x_2=%.3f$: wet steam" % x2, xy=(s2, TSAT_C),
                xytext=(3.0, 150), fontsize=9, color=INK,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
    ax.set_xlim(-0.3, 9.4)
    ax.set_ylim(0, 400)
    ax.set_xlabel(r"specific entropy $s$ (kJ/kg$\cdot$K)")
    ax.set_ylabel(r"temperature $T$ ($^\circ$C)")
    ax.set_title(r"Ideal Rankine cycle, 80 bar $\rightarrow$ 0.08 bar")
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_rankine_ts.svg")
    caps["fig1_rankine_ts.svg"] = (
        r"The ideal Rankine cycle laid over the real saturation dome read from "
        r"Table A-2. Steam leaves the boiler saturated at 80 bar and expands "
        r"isentropically to the condenser pressure, which lands it at quality "
        r"$x_2=" + "%.3f" % x2 + r"$ (quality_from_entropy) — deep inside the "
        r"dome, where liquid droplets erode the last turbine stages. The cycle's "
        r"efficiency is " + "%.3f" % eta + r" (rankine_efficiency) and its back "
        r"work ratio only " + "%.4f" % bwr + r": pumping a LIQUID from 0.08 to "
        r"80 bar costs just " + "%.1f" % wp + r" kJ/kg (pump_work_approx, "
        r"$v\Delta p$), against roughly " + "%.0f" % turbine_work(h1, h2) +
        r" kJ/kg from the turbine. That asymmetry with the gas turbine of module "
        r"9.5 is the reason steam plants tolerate poor component efficiencies "
        r"far better.")

    # Fig 2 — raising boiler pressure raises efficiency but drives the exit
    # quality DOWN, into the erosion region.  Reheat is the standard escape and
    # is shown for comparison at each pressure.
    p_grid = np.linspace(20.0, 160.0, 60)
    # saturated-vapour entropy and enthalpy along the boiler pressure, from A-2
    T_dome, sf_d, sg_d = _dome()
    p_of_T = {}
    with open(A2, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            p_of_T[float(row["P_bar"])] = (float(row["sg_kJkgK"]),
                                           float(row["hg_kJkg"]))
    ps = np.array(sorted(p_of_T))
    sg_at_p = np.array([p_of_T[p][0] for p in ps])
    hg_at_p = np.array([p_of_T[p][1] for p in ps])

    eta_s, x_s = [], []
    for p in p_grid:
        sg_p = float(np.interp(p, ps, sg_at_p))
        hg_p = float(np.interp(p, ps, hg_at_p))
        x = quality_from_entropy(sg_p, SF_C, SF_C + SFG_C)
        h2p = enthalpy_two_phase(x, HF_C, HFG_C)
        h4p = HF_C + pump_work_approx(VF_C, P_COND * 100.0, p * 100.0)
        eta_s.append(rankine_efficiency(hg_p, h2p, HF_C, h4p))
        x_s.append(x)

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(6.4, 3.4))
    axL.plot(p_grid, eta_s, color=INK, lw=2.3)
    axL.set_xlabel(r"boiler pressure (bar)")
    axL.set_ylabel(r"thermal efficiency $\eta$")
    axL.set_title(r"efficiency improves", fontsize=10.5)
    axL.grid(alpha=0.25, lw=0.6)

    axR.plot(p_grid, x_s, color=FLOW, lw=2.3)
    axR.axhline(0.88, color=ALT, lw=1.6, ls="--")
    axR.text(90, 0.885, "erosion limit $x\\approx0.88$", fontsize=8.5,
             color=ALT)
    axR.set_xlabel(r"boiler pressure (bar)")
    axR.set_ylabel(r"turbine exit quality $x_2$")
    axR.set_title(r"...but the steam gets wetter", fontsize=10.5)
    axR.grid(alpha=0.25, lw=0.6)
    fig.tight_layout()
    _save(fig, "fig2_boiler_pressure_tradeoff.svg")
    caps["fig2_boiler_pressure_tradeoff.svg"] = (
        r"The trade that shapes every real steam plant. Raising boiler pressure "
        r"raises the average temperature of heat addition and so the efficiency "
        r"(left), but it also steepens the isentropic expansion and pushes the "
        r"turbine exit further into the dome (right) — from "
        r"$x_2=" + "%.2f" % x_s[0] + r"$ at 20 bar down to $"
        + "%.2f" % x_s[-1] + r"$ at 160 bar, well past the "
        r"$x\approx0.88$ below which droplet erosion becomes serious. Both "
        r"curves are computed from Table A-2 saturated-vapour states with "
        r"quality_from_entropy. The standard escape is to superheat and then "
        r"REHEAT between turbine stages, which reclaims the efficiency without "
        r"the moisture — reheat_efficiency evaluates that six-state cycle.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
