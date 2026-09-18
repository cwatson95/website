"""NE-27 figures -- the anode's fixed energies, the CT number scale S&F omits,
why only 18F travels, and PET's two irreducible resolution limits.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.

Palette note: ALT and STEEL are indistinguishable under deuteranopia, so any
panel using both also varies linestyle or marker (modules/CHANGELOG.md Known-bad).
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
from medical import (                             # noqa: E402
    ANODE_LINES, ATOMIC_NUMBER, PET_NUCLIDES,
    moseley_k_alpha, hounsfield_unit, mu_from_hounsfield,
    positron_range_mm, activity_after_transport, usable_transport_time,
    coincidence_window_length,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # --- fig 1: the anode's energies are fixed by Z ------------------------
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(11.0, 4.2))

    order = ["Mo", "Rh", "W"]
    colours = {"Mo": FLOW, "Rh": LEAF, "W": INK}
    for i, el in enumerate(order):
        for name, (lam, e, kv) in sorted(ANODE_LINES[el].items()):
            heavy = name.startswith("K")
            ax.vlines(e, i - 0.32, i + 0.32, color=colours[el],
                      lw=2.6 if heavy else 1.2,
                      linestyle="-" if heavy else (0, (2, 1.6)))
            if heavy:
                ax.annotate(name.replace("a", "$\\alpha$").replace("b", "$\\beta$"),
                            xy=(e, i + 0.34), fontsize=7.5, color=colours[el],
                            ha="center")
    ax.axvspan(17.0, 23.0, color=ALT, alpha=0.13, zorder=0)
    ax.annotate("mammography window", xy=(20.0, 2.62), fontsize=8.5, color=ALT,
                ha="center")
    ax.set_xscale("log")
    ax.set_xlim(1.8, 110)
    ax.set_ylim(-0.6, 2.9)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(["%s (Z=%d)" % (e, ATOMIC_NUMBER[e]) for e in order])
    ax.set_xlabel("photon energy (keV)")
    ax.set_title("Table 14.2: an anode emits where its shells are")

    zs = np.arange(20, 84)
    bx.plot(zs, [moseley_k_alpha(z) for z in zs], color=STEEL, lw=1.8,
            label="Moseley  10.2 eV $(Z-1)^2$")
    for el in order:
        bx.plot(ATOMIC_NUMBER[el], ANODE_LINES[el]["Ka1"][1], "o", ms=8,
                color=colours[el], zorder=5)
        bx.annotate(el, xy=(ATOMIC_NUMBER[el], ANODE_LINES[el]["Ka1"][1]),
                    xytext=(4, -10), textcoords="offset points",
                    fontsize=9, color=colours[el])
    bx.set_xlabel("atomic number $Z$")
    bx.set_ylabel("K$\\alpha_1$ energy (keV)")
    bx.set_title("...and where its shells are is set by $Z$ alone")
    bx.legend(loc="upper left", fontsize=8.5, frameon=False)
    _save(fig, "fig1_anode_lines.svg")
    caps["fig1_anode_lines.svg"] = (
        "Left: every characteristic line in S&F Table 14.2, on a log energy axis (K lines solid, "
        "L lines dashed). Right: the same K-alpha lines against Moseley's law, which reproduces "
        "them to 2% for Mo and Rh and 8% for W -- the screening approximation degrades at high Z. "
        "Together they make the design point that the chapter states only implicitly: a "
        "characteristic line cannot be tuned, only replaced. Mammography needs 17-20 keV to "
        "exploit the photoelectric contrast of soft tissue against soft tissue, so it uses a "
        "molybdenum anode; general radiography needs penetration, so it uses tungsten at 59 keV. "
        "The choice of metal IS the choice of energy.")

    # --- fig 2: the CT number scale, which S&F never defines ---------------
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(11.0, 4.2))

    tissues = [("air", -1000), ("lung", -700), ("fat", -100), ("water", 0),
               ("muscle", 40), ("liver", 60), ("trabecular bone", 400),
               ("cortical bone", 1200)]
    ys = np.arange(len(tissues))
    vals = [h for _, h in tissues]
    cols = [STEEL if h < 0 else (FLOW if h < 100 else INK) for h in vals]
    ax.barh(ys, vals, color=cols, height=0.62)
    ax.axvline(0.0, color=ALT, lw=1.4)
    ax.annotate("water $\\equiv$ 0", xy=(30, 6.6), fontsize=8.5, color=ALT)
    ax.annotate("air $\\equiv -1000$", xy=(-980, 5.6), fontsize=8.5, color=ALT)
    ax.set_yticks(ys)
    ax.set_yticklabels([t for t, _ in tissues], fontsize=9)
    ax.set_xlabel("CT number (Hounsfield units)")
    ax.set_title("Two fixed points make $\\mu$ portable")

    hus = np.linspace(-1000, 1500, 400)
    bx.plot(hus, [mu_from_hounsfield(h) for h in hus], color=INK, lw=1.9)
    for t, h in tissues:
        bx.plot(h, mu_from_hounsfield(h), "o", ms=5, color=FLOW, zorder=5)
    bx.axhline(0.206, color=ALT, lw=1.1, linestyle=(0, (4, 2)))
    bx.annotate("$\\mu_{\\rm water}=0.206$ cm$^{-1}$", xy=(-950, 0.225),
                fontsize=8.5, color=ALT)
    bx.set_xlabel("CT number (HU)")
    bx.set_ylabel("$\\mu$ at 70 keV (cm$^{-1}$)")
    bx.set_title("HU is $\\mu$, affinely rescaled")
    _save(fig, "fig2_hounsfield_scale.svg")
    caps["fig2_hounsfield_scale.svg"] = (
        "The CT number scale -- which S&F §14.1.5 never defines. The chapter develops the Radon "
        "transform (Eq. 14.8) and filtered backprojection in full, and names Hounsfield, but "
        "never states the unit that carries his name and in which every clinical CT image is "
        "actually displayed. It is HU = 1000(mu - mu_w)/mu_w: an affine rescaling of ~NE-11's "
        "attenuation coefficient pinned at two points, water at 0 and air at -1000. Pinning it "
        "twice is what makes a CT number comparable between machines, and the -1000 floor is "
        "physical -- below it mu would be negative -- which is why the module's "
        "mu_from_hounsfield refuses to go there. The tissue values plotted are representative "
        "clinical numbers, not S&F's; the right panel is exact.")

    # --- fig 3: only 18F survives a journey --------------------------------
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(11.0, 4.2))

    t = np.linspace(0, 7.0, 500)
    styles = {"18F": (INK, "-", 2.2), "11C": (FLOW, "-", 1.8),
              "13N": (LEAF, (0, (5, 2)), 1.7), "15O": (STEEL, (0, (1.5, 1.5)), 1.7)}
    for n in ("18F", "11C", "13N", "15O"):
        c, ls, lw = styles[n]
        ax.plot(t, [activity_after_transport(n, x) for x in t], color=c,
                linestyle=ls, lw=lw,
                label="%s  ($T_{1/2}$ = %.3g min)" % (n, PET_NUCLIDES[n][3]))
    ax.axhline(0.10, color=ALT, lw=1.2, linestyle=(0, (4, 2)))
    ax.annotate("10% of delivered activity", xy=(3.6, 0.135), fontsize=8.5, color=ALT)
    ax.set_yscale("log")
    ax.set_ylim(1e-4, 1.4)
    ax.set_xlabel("time since end of bombardment (h)")
    ax.set_ylabel("surviving fraction")
    ax.set_title("Decay during delivery")
    ax.legend(loc="lower left", fontsize=8.0, frameon=False)

    names = ["15O", "13N", "11C", "18F"]
    hrs = [usable_transport_time(n) for n in names]
    bcols = [STEEL, STEEL, STEEL, INK]
    bx.barh(np.arange(len(names)), hrs, color=bcols, height=0.6)
    for i, h in enumerate(hrs):
        bx.annotate("%.2f h" % h if h > 1 else "%.0f min" % (h * 60),
                    xy=(h, i), xytext=(5, -4), textcoords="offset points",
                    fontsize=8.5, color=INK)
    bx.axvline(1.0, color=ALT, lw=1.2, linestyle=(0, (4, 2)))
    bx.annotate("one hour", xy=(1.08, 0.25), fontsize=8.5, color=ALT, rotation=90)
    bx.set_yticks(range(len(names)))
    bx.set_yticklabels(names)
    bx.set_xlim(0, 7.4)
    bx.set_xlabel("time to fall to 10% (h)")
    bx.set_title("Only $^{18}$F can be shipped")
    _save(fig, "fig3_pet_transport.svg")
    caps["fig3_pet_transport.svg"] = (
        "Why a PET centre is a far larger commitment than a SPECT one. S&F note that of Table "
        "14.3's four positron emitters, 'only 18F [has] a sufficiently long life to permit "
        "transport of radiopharmaceuticals to sites a few hours from the point of preparation'; "
        "the figure puts numbers on it. 18F takes 6.1 hours to fall to a tenth of its activity, "
        "15O takes 6.8 minutes -- a factor of 54. The other three therefore require the cyclotron "
        "to be in the building, and the reason they are all short-lived traces back to ~NE-26: a "
        "positron emitter is proton-rich, so it is made by a (p,x) reaction on a cyclotron, and "
        "nuclides that far from stability do not last.")

    # --- fig 4: PET's two irreducible limits -------------------------------
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(11.0, 4.2))

    e = np.linspace(0.0, 0.85, 300)
    ax.plot(e, [positron_range_mm(x) for x in e], color=INK, lw=2.0)
    for n, c in (("18F", FLOW), ("11C", LEAF), ("13N", ALT), ("15O", STEEL)):
        eav = PET_NUCLIDES[n][1]
        r = positron_range_mm(eav)
        ax.plot(eav, r, "o", ms=7, color=c, zorder=5)
        ax.annotate("%s\n%.2f mm" % (n, r), xy=(eav, r), xytext=(-2, 8),
                    textcoords="offset points", fontsize=8, color=c, ha="center")
    ax.set_xlabel("mean positron energy $\\bar{E}$ (MeV)")
    ax.set_ylabel("range in tissue (mm)")
    ax.set_xlim(0, 0.85)
    ax.set_ylim(0, 3.3)
    ax.set_title("Limit 1: the positron walks before it annihilates")

    taus = np.logspace(-1.4, 1.4, 200)
    bx.plot(taus, [coincidence_window_length(x) for x in taus], color=INK, lw=2.0)
    bx.axhspan(0, 40, color=LEAF, alpha=0.12, zorder=0)
    bx.annotate("patient-sized", xy=(0.05, 20), fontsize=8.5, color=LEAF)
    for tau, lab, c in ((10.0, "conventional\ncoincidence", FLOW),
                        (0.4, "time-of-flight\nPET", ALT)):
        bx.plot(tau, coincidence_window_length(tau), "o", ms=7, color=c, zorder=5)
        bx.annotate("%s\n%.0f cm" % (lab, coincidence_window_length(tau)),
                    xy=(tau, coincidence_window_length(tau)), xytext=(-6, 10),
                    textcoords="offset points", fontsize=8, color=c, ha="right")
    bx.set_xscale("log")
    bx.set_yscale("log")
    bx.set_xlabel("coincidence timing window $\\tau$ (ns)")
    bx.set_ylabel("localisation length $c\\tau$ (cm)")
    bx.set_title("Limit 2: timing does not localise (yet)")
    _save(fig, "fig4_pet_limits.svg")
    caps["fig4_pet_limits.svg"] = (
        "PET's resolution is bounded twice over, and neither bound is a detector problem. Left: "
        "the positron travels before it annihilates, so the line of response points at where it "
        "STOPPED, not where the tracer was -- 0.5 mm for 18F, 2.5 mm for 15O. No detector, at any "
        "price, recovers that. It is a second reason 18F dominates, independent of its half-life. "
        "Right: coincidence detection replaces SPECT's physical collimator with an electronic "
        "one, but a 10 ns window corresponds to 150 cm along the line of response -- far larger "
        "than a patient -- so conventional PET localises by reconstruction, not by timing. "
        "Time-of-flight scanners at 400 ps get to 6 cm, which finally beats the patient and is "
        "why they improve the signal-to-noise ratio rather than the resolution.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
