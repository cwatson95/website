"""NE-08 figures -- the threshold penalty above |Q|, the Coulomb barrier
landscape, the elastic-scattering energy band, and the moderator comparison.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
"""
import json
import math
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
from binary_kinematics import (                    # noqa: E402
    M_N_U, U_MEV, COULOMB_MEV_FM, R0_FM,
    load_atomic_masses, atomic_mass, q_value_masses,
    threshold_energy, threshold_energy_approx, coulomb_barrier,
    cm_kinetic_energy, elastic_scattering_energy_ratio, alpha_collision,
    average_log_energy_decrement, collisions_to_thermalize,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    tab = load_atomic_masses()

    def m(A, Z):
        return M_N_U if (A, Z) == (1, 0) else atomic_mass(A, Z, table=tab)

    # Fig 1 -- the threshold always exceeds |Q|, by the mass ratio.
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ratio = np.linspace(0.0, 1.0, 300)
    ax.plot(ratio, 1.0 + ratio, color=INK, lw=1.9,
            label="$E_{th}/|Q| = 1 + m_x/m_X$   [Eq. (6.15)]")
    ax.axhline(1.0, color="0.55", ls="--", lw=1.2)
    ax.text(0.03, 1.02, "the naive answer $E_{th}=|Q|$ -- always too low",
            fontsize=9, color="0.35")
    marks = [("n on $^{238}$U", M_N_U / 238.0, STEEL, "o"),
             ("p on $^{7}$Li", 1.0078 / 7.016, LEAF, "s"),
             ("$\\alpha$ on $^{9}$Be", 4.0026 / 9.012, FLOW, "^"),
             ("d on d", 1.0, ALT, "D")]
    for lab, r, col, mk in marks:
        ax.plot([r], [1 + r], mk, color=col, ms=7)
        ax.annotate(lab, xy=(r, 1 + r), xytext=(r - 0.02, 1 + r + 0.06),
                    fontsize=9, color=col, ha="right")
    ax.set_xlabel("projectile / target mass ratio  $m_x/m_X$")
    ax.set_ylabel("$E_{th}\\,/\\,|Q|$")
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(0.95, 2.15)
    ax.legend(fontsize=9, loc="upper left")
    ax.set_title("The threshold penalty: energy lost to centre-of-mass motion")
    _save(fig, "fig1_threshold_penalty.svg")
    caps["fig1_threshold_penalty.svg"] = (
        "Kinematic threshold divided by the magnitude of the Q-value (threshold_energy). "
        "Only the centre-of-mass energy E_lab*m_X/(m_x+m_X) can drive a reaction, so the "
        "beam must supply |Q|(1 + m_x/m_X). A neutron on 238U wastes 0.4%; two deuterons "
        "waste half. Quoting |Q| as the threshold, as a naive Q-value calculation does, "
        "is always an underestimate.")

    # Fig 2 -- Coulomb barrier vs target Z, one curve per projectile.
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ZX = np.arange(1, 93)
    AX = np.array([round(2.0 * z + 0.0155 * z ** (5.0 / 3.0)) for z in ZX])  # valley of stability
    for (Zx, Ax, lab, col, ls) in [(0, 1, "neutron", STEEL, "-"),
                                   (1, 1, "proton", LEAF, "--"),
                                   (1, 2, "deuteron", ALT, "-."),
                                   (2, 4, "alpha", FLOW, ":")]:
        vc = [coulomb_barrier(Zx, Ax, int(z), int(a)) for z, a in zip(ZX, AX)]
        ax.plot(ZX, vc, color=col, lw=1.9, ls=ls, label=lab)
    ax.annotate("neutrons: zero at every target,\nat every energy",
                xy=(55, 0.0), xytext=(30, 5.5), fontsize=9, color=STEEL,
                arrowprops=dict(arrowstyle="->", color=STEEL, lw=1.1))
    ax.set_xlabel("target atomic number $Z_X$")
    ax.set_ylabel("Coulomb barrier $E_x^C$ (MeV)")
    ax.set_xlim(0, 93)
    ax.set_ylim(-1, 31)
    ax.legend(fontsize=9, loc="upper left")
    ax.set_title("Why reactors run on neutrons")
    _save(fig, "fig2_coulomb_barrier.svg")
    caps["fig2_coulomb_barrier.svg"] = (
        "Coulomb barrier height against target charge for four projectiles (coulomb_barrier), "
        "S&F Eq. (6.19) with R = 1.2(Ax^1/3 + AX^1/3) fm. An alpha faces 28 MeV at uranium -- "
        "far beyond thermal energies -- while the neutron curve lies flat on zero. This is "
        "why fission chains are sustained by neutrons and why charged-particle reactions "
        "need accelerators however exoergic they are.")

    # Fig 3 -- the elastic scattering energy band.
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    deg = np.linspace(0, 180, 361)
    th = np.radians(deg)
    for A, lab, col, ls in [(1, "$^{1}$H", FLOW, "-"), (2, "$^{2}$H", ALT, "--"),
                            (12, "$^{12}$C", LEAF, "-."), (238, "$^{238}$U", STEEL, ":")]:
        r = [elastic_scattering_energy_ratio(A, t) for t in th]
        ax.plot(deg, r, color=col, lw=1.9, ls=ls,
                label=lab + "  ($\\alpha$ = %.3f)" % alpha_collision(A))
        ax.axhline(alpha_collision(A), color=col, ls=":", lw=1.0)
    ax.set_xlabel("laboratory scattering angle $\\theta_s$ (degrees)")
    ax.set_ylabel("$E'/E$")
    ax.set_xlim(0, 180)
    ax.set_ylim(-0.03, 1.05)
    ax.set_xticks([0, 30, 60, 90, 120, 150, 180])
    ax.legend(fontsize=9, loc="lower left")
    ax.set_title("One elastic collision: $E'/E$ from Eq. (6.25)")
    _save(fig, "fig3_scattering_band.svg")
    caps["fig3_scattering_band.svg"] = (
        "Fraction of its energy a neutron retains after one elastic collision, against "
        "laboratory scattering angle (elastic_scattering_energy_ratio). Every curve starts "
        "at 1 for a glancing hit and bottoms out at alpha = ((A-1)/(A+1))^2 for backscatter "
        "(dotted lines). Hydrogen reaches zero -- a neutron can be stopped dead by a single "
        "proton, and cannot backscatter from one at all; 238U never gives up more than 1.7%.")

    # Fig 4 -- collisions to thermalise, and why light moderators win.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.4, 3.7))
    A = np.arange(1, 60)
    axL.plot(A, [average_log_energy_decrement(int(a)) for a in A], color=INK, lw=1.9)
    for a, lab, col, mk in [(1, "H", FLOW, "o"), (2, "D", ALT, "D"),
                            (9, "Be", LEAF, "^"), (12, "C", STEEL, "s")]:
        xi = average_log_energy_decrement(a)
        axL.plot([a], [xi], mk, color=col, ms=7)
        axL.annotate("%s  %.3f" % (lab, xi), xy=(a, xi), xytext=(a + 2, xi + 0.03),
                     fontsize=9, color=col)
    axL.set_xlabel("scatterer mass number $A$")
    axL.set_ylabel("$\\xi = \\langle \\ln(E/E')\\rangle$")
    axL.set_title("Logarithmic energy decrement")
    axL.set_ylim(0, 1.15)

    mods = [("$^{1}$H", 1), ("$^{2}$H", 2), ("$^{4}$He", 4), ("$^{9}$Be", 9),
            ("$^{12}$C", 12), ("$^{16}$O", 16), ("$^{56}$Fe", 56), ("$^{238}$U", 238)]
    n = [collisions_to_thermalize(a, 2.0, 0.025) for _, a in mods]
    cols = [FLOW, ALT, "#8a8a5a", LEAF, STEEL, "#5a9a9a", "#9a5a5a", INK]
    axR.barh(range(len(mods)), n, color=cols)
    axR.set_yticks(range(len(mods)))
    axR.set_yticklabels([lab for lab, _ in mods])
    axR.invert_yaxis()
    axR.set_xscale("log")
    axR.set_xlabel("elastic collisions, 2 MeV $\\to$ 0.025 eV")
    for i, v in enumerate(n):
        axR.text(v * 1.15, i, "%.0f" % v, va="center", fontsize=9, color="0.25")
    axR.set_xlim(10, 8000)
    axR.set_title("Table 6.1, recomputed")
    fig.tight_layout()
    _save(fig, "fig4_moderators.svg")
    caps["fig4_moderators.svg"] = (
        "Left: the mean logarithmic energy decrement xi (average_log_energy_decrement), "
        "which is independent of energy and so gives a constant collision cost per decade "
        "of slowing-down. Right: the resulting number of elastic scatters to bring a 2 MeV "
        "fission neutron to 0.025 eV (collisions_to_thermalize), reproducing S&F Table 6.1. "
        "Hydrogen needs 18, graphite 115, uranium 2172 -- the reason moderators are light "
        "and the reason a fast reactor needs no moderator at all.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
