"""Module 5.4 figures — the p-V plane, where the area under a path is the work and
the area enclosed by a cycle is the net work.

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
from pv_diagram import (                          # noqa: E402
    work_pdV, work_isobaric, p_polytropic, work_polytropic,
    work_isothermal_ideal_gas,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — three ways from the same V1 to the same V2, and the area each one
    # sweeps.  work_pdV integrates the SAMPLED path, so it also serves as an
    # independent check on the three closed forms.
    p1, V1, V2 = 300.0, 0.10, 0.30
    Vg = np.linspace(V1, V2, 400)

    paths = []
    p_iso = np.full_like(Vg, p1)
    paths.append((r"isobaric $n=0$", p_iso, work_isobaric(p1, V1, V2), INK, "-"))
    p_t = p1 * V1 / Vg
    paths.append((r"isothermal $n=1$", p_t, work_isothermal_ideal_gas(p1, V1, V2),
                  FLOW, "--"))
    n = 1.3
    p_n = np.array([p_polytropic(p1, V1, v, n) for v in Vg])
    paths.append((r"polytropic $n=1.3$", p_n,
                  work_polytropic(p1, V1, p_polytropic(p1, V1, V2, n), V2, n),
                  ALT, ":"))

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    for lab, p, W, c, ls in paths:
        W_num = work_pdV(list(p), list(Vg))
        ax.plot(Vg, p, color=c, lw=2.1, ls=ls,
                label=r"%s:  $W=%.1f$ kJ" % (lab, W_num))
        ax.fill_between(Vg, 0, p, color=c, alpha=0.09, lw=0)
        assert abs(W_num - W) < 0.2 * max(1.0, abs(W))     # sampled == closed form
    ax.set_xlim(V1, V2)
    ax.set_ylim(0, 330)
    ax.set_xlabel(r"volume $V$ (m$^3$)")
    ax.set_ylabel(r"pressure $p$ (kPa)")
    ax.set_title(r"On a $p$-$V$ diagram the area under the path is the work")
    ax.legend(loc="lower left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_pv_path_areas.svg")
    caps["fig1_pv_path_areas.svg"] = (
        r"Three quasiequilibrium paths from 0.1 to 0.3 m$^3$ starting at 3 bar, "
        r"with the area under each shaded. The legend values come from work_pdV, "
        r"the trapezoid rule applied to the SAMPLED path, and each one is "
        r"asserted against its closed form (work_isobaric, "
        r"work_isothermal_ideal_gas, work_polytropic) inside this script. The "
        r"ordering is the general rule: the higher the polytropic exponent, the "
        r"faster the pressure decays as the gas expands, and the less work the "
        r"same volume change returns.")

    # Fig 2 — close the path and the enclosed area becomes the NET work.  Going
    # clockwise (expand hot, compress cold) the cycle delivers work; run it
    # anticlockwise and the same area is consumed.
    # two DISTINCT isotherms: pV = 30 on the way out, pV = 18 on the way back.
    # (Equal pV products would put both legs on one curve and enclose nothing.)
    pA, pB = 300.0, 60.0
    VA, VB = 0.10, 0.30
    V_top = np.linspace(VA, VB, 200)
    p_top = pA * VA / V_top                          # expand along pV = const
    V_bot = np.linspace(VB, VA, 200)
    p_bot = pB * VB / V_bot                          # compress along a lower isotherm
    W_out = work_pdV(list(p_top), list(V_top))
    W_in = work_pdV(list(p_bot), list(V_bot))
    W_net = W_out + W_in

    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.plot(V_top, p_top, color=INK, lw=2.2, label=r"expansion: $W=%+.1f$ kJ" % W_out)
    ax.plot(V_bot, p_bot, color=FLOW, lw=2.2, ls="--",
            label=r"compression: $W=%+.1f$ kJ" % W_in)
    ax.plot([VB, VB], [p_top[-1], pB], color="0.6", lw=1.6)
    ax.plot([VA, VA], [pB * VB / VA, pA], color="0.6", lw=1.6)
    ax.fill(np.concatenate([V_top, V_bot]), np.concatenate([p_top, p_bot]),
            color=ALT, alpha=0.18, lw=0)
    ax.text(0.176, 143, r"enclosed area" "\n" r"$=W_{net}=%.1f$ kJ" % W_net,
            ha="center", fontsize=10, color="0.25")
    ax.annotate("", xy=(0.22, p_top[np.argmin(abs(V_top - 0.22))]),
                xytext=(0.16, p_top[np.argmin(abs(V_top - 0.16))]),
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))
    ax.annotate("", xy=(0.16, p_bot[np.argmin(abs(V_bot - 0.16))]),
                xytext=(0.22, p_bot[np.argmin(abs(V_bot - 0.22))]),
                arrowprops=dict(arrowstyle="->", color=FLOW, lw=1.6))
    ax.set_xlim(0.08, 0.32)
    ax.set_ylim(0, 340)
    ax.set_xlabel(r"volume $V$ (m$^3$)")
    ax.set_ylabel(r"pressure $p$ (kPa)")
    ax.set_title(r"A closed cycle: the enclosed area is the net work")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_cycle_enclosed_area.svg")
    caps["fig2_cycle_enclosed_area.svg"] = (
        r"Why engines are drawn as loops. Expanding along the upper path "
        r"delivers " + "%.1f" % W_out + r" kJ and returning along the lower one "
        r"costs " + "%.1f" % abs(W_in) + r" kJ, so the cycle nets "
        + "%.1f" % W_net + r" kJ — exactly the enclosed area, evaluated here by "
        r"applying work_pdV to each leg and adding. The sign follows the "
        r"direction of travel: clockwise produces work, anticlockwise consumes "
        r"it, which is the only difference between an engine and a heat pump on "
        r"this diagram. Since the cycle returns to its start, $\Delta U=0$ and "
        r"the first law makes this net work equal to the net heat.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
