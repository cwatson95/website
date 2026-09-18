"""NE-09 figures -- the fissile/fissionable split, the 200 MeV budget, the
prompt fission-neutron spectrum, and decay heat after shutdown.

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
from fission import (                              # noqa: E402
    FISSION_ENERGY_MEV, SPONTANEOUS_FISSION, NEUTRON_YIELD,
    load_atomic_masses, excitation_energy, is_fissile,
    watt_spectrum, watt_peak_energy, watt_mean_energy,
    decay_heat_total, fission_energy,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    t = load_atomic_masses()

    # Fig 1 -- fissile vs fissionable, and the pairing gap that separates them.
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    targets = [("$^{232}$Th", 232, 90), ("$^{233}$U", 233, 92), ("$^{235}$U", 235, 92),
               ("$^{238}$U", 238, 92), ("$^{239}$Pu", 239, 94),
               ("$^{240}$Pu", 240, 94), ("$^{241}$Pu", 241, 94)]
    labs, vals, cols = [], [], []
    for lab, A, Z in targets:
        e = excitation_energy(A, Z, 0.0, t)
        labs.append(lab + ("\n(odd N)" if (A - Z) % 2 else "\n(even N)"))
        vals.append(e)
        cols.append(FLOW if is_fissile(A, Z, table=t) else STEEL)
    ax.bar(range(len(vals)), vals, color=cols, width=0.62)
    ax.axhline(6.2, color=INK, ls="--", lw=1.5)
    ax.text(0.05, 6.33, "fission barrier $\\simeq$ 6.2 MeV", fontsize=9, color=INK)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.12, "%.2f" % v, ha="center", fontsize=8.5, color="0.25")
    ax.set_xticks(range(len(labs)))
    ax.set_xticklabels(labs, fontsize=8.5)
    ax.set_ylabel("$E^*$ from a zero-energy neutron (MeV)")
    ax.set_ylim(0, 7.8)
    ax.set_title("Fissile (orange) vs fissionable (blue): one pairing term apart")
    _save(fig, "fig1_fissile_split.svg")
    caps["fig1_fissile_split.svg"] = (
        "Excitation energy handed to the compound nucleus by a zero-energy neutron, "
        "E* = S_n (excitation_energy), against the ~6.2 MeV fission barrier. Every target "
        "with an ODD neutron number clears it -- the added neutron completes a pair and "
        "releases about 1.5 MeV more (the pairing term of NE-02). Every even-N target "
        "falls short and needs a fast neutron instead. That single term is the whole "
        "difference between reactor fuel and reactor blanket.")

    # Fig 2 -- the 200 MeV budget, produced vs recoverable.
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    order = ["fragment_kinetic", "prompt_neutrons", "prompt_gammas",
             "capture_gammas", "delayed_beta", "delayed_gamma", "neutrinos"]
    names = ["fission fragment\nkinetic energy", "prompt\nneutrons", "prompt\n$\\gamma$",
             "capture\n$\\gamma$", "delayed\n$\\beta$", "delayed\n$\\gamma$", "neutrinos"]
    prod = [FISSION_ENERGY_MEV[k][0] for k in order]
    rec = [FISSION_ENERGY_MEV[k][1] for k in order]
    x = np.arange(len(order))
    ax.bar(x - 0.2, prod, 0.4, color=STEEL, label="produced (%.0f MeV)" % fission_energy(False))
    ax.bar(x + 0.2, rec, 0.4, color=FLOW, label="recoverable (%.0f MeV)" % fission_energy(True))
    ax.annotate("lost:\nneutrinos leave\nthe planet", xy=(6.2, 0.5), xytext=(4.8, 60),
                fontsize=9, color=ALT, ha="center",
                arrowprops=dict(arrowstyle="->", color=ALT, lw=1.1))
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=8)
    ax.set_ylabel("MeV per fission")
    ax.legend(fontsize=9)
    ax.set_title("Where the 200 MeV goes (S&F Table 6.5, thermal $^{235}$U)")
    _save(fig, "fig2_energy_budget.svg")
    caps["fig2_energy_budget.svg"] = (
        "The per-fission energy budget of S&F Table 6.5 (FISSION_ENERGY_MEV). Fission "
        "fragments carry 168 of the 207 MeV and stop within a fraction of a millimetre, "
        "which is why fuel gets hot rather than the coolant. The 12 MeV in neutrinos "
        "leaves the reactor, the planet and the solar system unimpeded and is the only "
        "component that is entirely unrecoverable; capture gammas are a core-dependent "
        "bonus of 3-9 MeV that partly offsets it.")

    # Fig 3 -- the prompt fission-neutron spectrum.
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    e = np.linspace(0.001, 10.0, 900)
    for nuc, spec, lab, col in [("235U", "thermal", "$^{235}$U thermal", FLOW),
                                ("239Pu", "thermal", "$^{239}$Pu thermal", LEAF),
                                ("252Cf", "spontaneous", "$^{252}$Cf spontaneous", ALT)]:
        ax.plot(e, [watt_spectrum(x, nuc, spec) for x in e], color=col, lw=1.9, label=lab)
    pk, mn = watt_peak_energy(), watt_mean_energy()
    ax.axvline(pk, color=STEEL, ls=":", lw=1.3)
    ax.axvline(mn, color=INK, ls="--", lw=1.3)
    ax.text(pk + 0.1, 0.34, "mode\n%.2f MeV" % pk, fontsize=9, color=STEEL)
    ax.text(mn + 0.15, 0.26, "mean\n%.2f MeV" % mn, fontsize=9, color=INK)
    ax.axvspan(0.0, 0.0253e-6, color="0.9")
    ax.set_xlabel("neutron energy (MeV)")
    ax.set_ylabel("$\\chi(E)$  (MeV$^{-1}$)")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 0.42)
    ax.legend(fontsize=9)
    ax.set_title("Fission neutrons are born fast: $\\chi(E)$ from Eq. (6.42)")
    _save(fig, "fig3_watt_spectrum.svg")
    caps["fig3_watt_spectrum.svg"] = (
        "The Watt prompt fission-neutron spectrum (watt_spectrum, S&F Eq. 6.42) for three "
        "fissioning systems. It is broad and strongly right-skewed, so the most probable "
        "energy (0.70 MeV) and the mean (1.99 MeV) differ by a factor of three -- quoting "
        "one for the other is a standard error. Thermal energy, 0.025 eV, is off the left "
        "edge by five decades: every fission neutron must be slowed by the ~115 graphite "
        "or ~18 hydrogen collisions of NE-08 before it can efficiently cause the next "
        "fission.")

    # Fig 4 -- decay heat after shutdown.
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ts = np.logspace(1, 5, 400)
    ax.loglog(ts, [decay_heat_total(x) for x in ts], color=INK, lw=2.0,
              label="$1.4t^{-1.2} + 1.26t^{-1.2}$  [Eqs. (6.44)-(6.45)]")
    for t_s, lab in [(10.0, "10 s"), (3600.0, "1 h"), (86400.0, "1 d")]:
        v = decay_heat_total(t_s)
        ax.plot([t_s], [v], "o", color=FLOW, ms=7)
        ax.annotate("%s\n%.2e MeV/s" % (lab, v), xy=(t_s, v),
                    xytext=(t_s * 1.4, v * 2.4), fontsize=8.5, color=FLOW)
    ax.set_xlabel("time after fission (s)")
    ax.set_ylabel("delayed $\\beta+\\gamma$ power per fission (MeV s$^{-1}$)")
    ax.legend(fontsize=9, loc="lower left")
    ax.set_title("Decay heat: a power law, so it never really switches off")
    _save(fig, "fig4_decay_heat.svg")
    caps["fig4_decay_heat.svg"] = (
        "Delayed beta and gamma power per fission after shutdown (decay_heat_total, S&F "
        "Eqs. 6.44-6.45). The straight line on log-log axes is the point: decay heat falls "
        "as t^-1.2, not exponentially, because it is the sum of hundreds of fission-product "
        "chains with half-lives spread over ten decades. It therefore has no characteristic "
        "time -- a shut-down core still needs active cooling days later, and every "
        "loss-of-coolant accident is a story about this curve.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
