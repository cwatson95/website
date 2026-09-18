"""NE-03 figures -- the measured binding-energy curve, the odd-even stagger in
neutron separation energy, and shell closures seen in S_n.

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
from binding_energy import (                       # noqa: E402
    MAGIC_NUMBERS, load_atomic_masses, has_nuclide,
    binding_energy_per_nucleon, binding_energy_curve, most_bound_nuclide,
    neutron_separation_energy, two_neutron_separation_energy,
    alpha_separation_energy,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    t = load_atomic_masses()

    # Fig 1 -- the measured B/A curve with the landmarks marked.
    curve = binding_energy_curve(t, z_tolerance=0)
    A = [r[0] for r in curve]
    B = [r[2] for r in curve]
    pk_A, pk_Z, pk_B = most_bound_nuclide(t)

    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    ax.plot(A, B, "-", color=INK, lw=1.4)
    for a, z, lab, dx, dy in [(4, 2, r"$^4$He", 6, -0.9), (12, 6, r"$^{12}$C", 8, -0.6),
                              (56, 26, r"$^{56}$Fe", 6, 0.45),
                              (235, 92, r"$^{235}$U", -30, 0.7)]:
        b = binding_energy_per_nucleon(a, z, t)
        ax.plot([a], [b], "o", color=FLOW, ms=5)
        ax.annotate(lab, xy=(a, b), xytext=(a + dx, b + dy), fontsize=9, color=FLOW)
    ax.plot([pk_A], [pk_B], "*", color=LEAF, ms=13)
    ax.annotate(r"$^{62}$Ni, %.3f MeV" % pk_B, xy=(pk_A, pk_B), xytext=(pk_A + 40, pk_B + 0.35),
                fontsize=9, color=LEAF, arrowprops=dict(arrowstyle="->", color=LEAF))
    ax.annotate("", xy=(50, 8.35), xytext=(14, 7.3),
                arrowprops=dict(arrowstyle="->", color="0.45", lw=1.3))
    ax.text(22, 7.05, "fusion", fontsize=9, color="0.35")
    ax.annotate("", xy=(120, 8.4), xytext=(230, 7.6),
                arrowprops=dict(arrowstyle="->", color="0.45", lw=1.3))
    ax.text(178, 7.35, "fission", fontsize=9, color="0.35")
    ax.set_xlabel("mass number $A$")
    ax.set_ylabel("$B/A$ (MeV per nucleon)")
    ax.set_ylim(0, 9.5)
    ax.set_title("Binding energy per nucleon, from measured masses")
    _save(fig, "fig1_measured_ba_curve.svg")
    caps["fig1_measured_ba_curve.svg"] = (
        "Binding energy per nucleon computed from the Appendix B atomic masses "
        "(binding_energy_per_nucleon) along the most-bound isobar at each A. The maximum "
        "is 62Ni at 8.7945 MeV/nucleon, marginally above 56Fe; both fusion from the left "
        "and fission from the right move nucleons up the curve and release the difference.")

    # Fig 2 -- odd-even stagger in S_n along four isotope chains.
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    chains = [(8, "O", INK, "-"), (20, "Ca", FLOW, "--"),
              (50, "Sn", ALT, "-."), (82, "Pb", STEEL, ":")]
    for Z, sym, col, ls in chains:
        As, Sn = [], []
        for a in range(2 * Z - 4, 3 * Z + 40):
            if has_nuclide(a, Z, t) and has_nuclide(a - 1, Z, t):
                As.append(a - Z)
                Sn.append(neutron_separation_energy(a, Z, t))
        if As:
            ax.plot(As, Sn, marker="o", ls=ls, color=col, ms=3, lw=1.0,
                    label="Z=%d (%s)" % (Z, sym))
    ax.set_xlabel("neutron number $N$")
    ax.set_ylabel("$S_n$ (MeV)")
    ax.set_title("Neutron separation energy staggers with the parity of $N$")
    ax.legend(frameon=False, fontsize=9, ncol=2)
    ax.set_ylim(0, 22)
    _save(fig, "fig2_separation_energy_stagger.svg")
    caps["fig2_separation_energy_stagger.svg"] = (
        "One-neutron separation energy (neutron_separation_energy) along four isotope "
        "chains. The sawtooth is the pairing energy: even-N nuclides hold their last "
        "neutron 3-4 MeV more tightly than their odd-N neighbours, which is the ~NE-02 "
        "pairing term measured directly, with no model in between.")

    # Fig 3 -- shell closures in S_2n (pairing removed).
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    for Z, sym, col in [(50, "Sn", INK), (82, "Pb", FLOW), (58, "Ce", ALT)]:
        Ns, S2 = [], []
        for a in range(2 * Z - 6, 3 * Z + 40):
            if has_nuclide(a, Z, t) and has_nuclide(a - 2, Z, t):
                Ns.append(a - Z)
                S2.append(two_neutron_separation_energy(a, Z, t))
        if Ns:
            ax.plot(Ns, S2, "o-", color=col, ms=3.2, lw=1.1, label="Z=%d (%s)" % (Z, sym))
    for m in (50, 82, 126):
        ax.axvline(m, color="0.7", lw=1.0, ls="--")
        ax.text(m + 1, 30.5, "N=%d" % m, fontsize=8.5, color="0.4")
    ax.set_xlabel("neutron number $N$")
    ax.set_ylabel("$S_{2n}$ (MeV)")
    ax.set_ylim(0, 33)
    ax.set_title("Two-neutron separation energy: the drop at each shell closure")
    ax.legend(frameon=False, fontsize=9)
    _save(fig, "fig3_shell_closures.svg")
    caps["fig3_shell_closures.svg"] = (
        "Two-neutron separation energy (two_neutron_separation_energy), which removes a "
        "pair and so cancels the odd-even sawtooth of Fig. 2. What remains is a smooth "
        "decline interrupted by sharp drops immediately after the magic numbers N=50, 82 "
        "and 126 -- the first neutron outside a closed shell is barely bound.")

    # Fig 4 -- alpha separation energy changing sign.
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    As, Sa = [], []
    for (Z, a) in sorted(t):
        if a < 8 or Z < 4:
            continue
        if not has_nuclide(a - 4, Z - 2, t):
            continue
        try:
            s = alpha_separation_energy(a, Z, t)
        except (KeyError, ValueError):
            continue
        As.append(a)
        Sa.append(s)
    ax.plot(As, Sa, ".", color=STEEL, ms=2.2)
    ax.axhline(0, color="k", lw=1.1)
    ax.text(30, -9, "below this line, alpha emission is exothermic",
            fontsize=9, color="0.3")
    for a, z, lab in [(238, 92, r"$^{238}$U"), (226, 88, r"$^{226}$Ra"),
                      (208, 82, r"$^{208}$Pb")]:
        s = alpha_separation_energy(a, z, t)
        ax.plot([a], [s], "o", color=FLOW, ms=5)
        ax.annotate(lab, xy=(a, s), xytext=(a - 26, s - 4), fontsize=9, color=FLOW)
    ax.set_xlabel("mass number $A$")
    ax.set_ylabel(r"$S_\alpha$ (MeV)")
    ax.set_ylim(-14, 16)
    ax.set_title(r"Alpha separation energy turns negative in the heavy elements")
    _save(fig, "fig4_alpha_separation.svg")
    caps["fig4_alpha_separation.svg"] = (
        "Alpha separation energy (alpha_separation_energy) for every nuclide whose "
        "alpha daughter is tabulated. Above A~150 it goes negative, meaning alpha "
        "emission releases energy and Q_alpha = -S_alpha. 208Pb sits barely below zero, "
        "energetically unstable yet observationally stable because of the Coulomb barrier.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
