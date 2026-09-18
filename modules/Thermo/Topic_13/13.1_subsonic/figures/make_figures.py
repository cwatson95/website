"""Module 13.1 figures — the stagnation ratios that make compressibility matter,
and the area-velocity relation whose sign flips at M = 1.

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
from subsonic import (                            # noqa: E402
    speed_of_sound_ideal_gas, mach_number, stagnation_temperature_ratio,
    stagnation_pressure_ratio, stagnation_density_ratio, area_change_ratio,
    duct_shape,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

K, R_AIR = 1.4, 287.0


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — how far a flow may be treated as incompressible.  All three
    # stagnation ratios depart from 1 quadratically in M, and the conventional
    # M = 0.3 cutoff is where the density error reaches ~5%.
    M = np.linspace(0.0, 1.0, 400)
    Tr = np.array([stagnation_temperature_ratio(m, K) for m in M])
    pr = np.array([stagnation_pressure_ratio(m, K) for m in M])
    rr = np.array([stagnation_density_ratio(m, K) for m in M])

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot(M, pr, color=INK, lw=2.2, label=r"$p_o/p$")
    ax.plot(M, rr, color=FLOW, lw=2.2, ls="--", label=r"$\rho_o/\rho$")
    ax.plot(M, Tr, color=ALT, lw=2.2, ls=":", label=r"$T_o/T$")
    ax.axvline(0.3, color="0.6", lw=1.3, ls="-.")
    ax.text(0.31, 1.62, r"$M=0.3$: the usual" "\n" r"incompressible cutoff",
            fontsize=9, color="0.4")
    ax.set_xlim(0, 1)
    ax.set_ylim(1.0, 1.95)
    ax.set_xlabel(r"Mach number $M$")
    ax.set_ylabel(r"stagnation / static ratio")
    ax.set_title(r"Bringing a flow to rest raises $T$, $p$ and $\rho$")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig1_stagnation_ratios.svg")
    caps["fig1_stagnation_ratios.svg"] = (
        r"Decelerating a flow isentropically to rest converts its kinetic energy "
        r"into thermodynamic state: $T_o/T=1+\frac{k-1}{2}M^2$ and the pressure "
        r"and density ratios follow as powers of it "
        r"(stagnation_temperature_ratio, stagnation_pressure_ratio, "
        r"stagnation_density_ratio). All three depart from unity quadratically, "
        r"which is why low-speed flow can be treated as incompressible: at "
        r"$M=0.3$ the density has changed by only "
        + "%.1f" % (100 * (stagnation_density_ratio(0.3, K) - 1)) + r"%, the "
        r"conventional threshold. By $M=1$ the stagnation pressure is "
        + "%.2f" % stagnation_pressure_ratio(1.0, K) + r" times the static "
        r"value and the approximation is long gone. At 300 K the speed of sound "
        r"in air is " + "%.0f" % speed_of_sound_ideal_gas(K, R_AIR, 300.0) +
        r" m/s (speed_of_sound_ideal_gas), which mach_number turns a velocity "
        r"into $M$ against.")

    # Fig 2 — the sign flip.  dA/A = -(dV/V)(1 - M^2): to accelerate a subsonic
    # flow you must NARROW the duct, but to accelerate a supersonic one you must
    # WIDEN it.  Hence the converging-diverging nozzle.
    Mg = np.linspace(0.05, 2.5, 400)
    dVV = 0.01                                      # a 1% velocity increase
    dAA = np.array([area_change_ratio(dVV, m) for m in Mg])

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot(Mg, dAA * 100, color=INK, lw=2.4)
    ax.axhline(0.0, color="0.6", lw=1.1)
    ax.axvline(1.0, color=FLOW, lw=1.6, ls="--")
    ax.fill_between(Mg, 0, dAA * 100, where=(Mg < 1.0), color=INK, alpha=0.10,
                    lw=0)
    ax.fill_between(Mg, 0, dAA * 100, where=(Mg > 1.0), color=ALT, alpha=0.12,
                    lw=0)
    ax.text(0.5, -3.2, "subsonic:\nnarrow to speed up\n(%s)" % duct_shape(dVV, 0.5),
            fontsize=9, color="0.3", ha="center")
    ax.text(1.9, 2.6, "supersonic:\nwiden to speed up\n(%s)" % duct_shape(dVV, 1.9),
            fontsize=9, color="0.3", ha="center")
    ax.text(1.02, -5.5, r"$M=1$ at the throat", fontsize=9, color=FLOW,
            rotation=90)
    ax.set_xlim(0, 2.5)
    ax.set_xlabel(r"Mach number $M$")
    ax.set_ylabel(r"area change $dA/A$ (%) for a $+1$% velocity change")
    ax.set_title(r"$dA/A=-(dV/V)(1-M^2)$: the sign flips at $M=1$")
    ax.grid(alpha=0.25, lw=0.6)
    _save(fig, "fig2_area_velocity.svg")
    caps["fig2_area_velocity.svg"] = (
        r"The single most consequential result in gas dynamics. "
        r"$dA/A=-(dV/V)(1-M^2)$ (area_change_ratio) says that speeding up a "
        r"SUBSONIC stream requires a converging duct, exactly as incompressible "
        r"intuition expects — but past $M=1$ the bracket changes sign and "
        r"speeding up a SUPERSONIC stream requires a DIVERGING one "
        r"(duct_shape returns the verdict). Density is falling so fast above "
        r"Mach 1 that area must grow just to pass the same mass. A nozzle that "
        r"is to reach supersonic exit must therefore converge to a throat, pass "
        r"through $M=1$ there where $dA=0$, and then diverge — the "
        r"converging-diverging geometry that module 13.2 takes up.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
