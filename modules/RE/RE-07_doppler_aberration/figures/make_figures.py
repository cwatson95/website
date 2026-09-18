"""RE-07 figures — relativistic Doppler shift and aberration (beaming) of light.

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
from doppler_aberration import (                   # noqa: E402
    doppler_general, doppler_longitudinal, doppler_transverse,
    aberration, headlight_halfangle, gamma,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — relativistic Doppler factor f_obs/f_src vs ray angle, for several beta.
    theta = np.linspace(0.0, np.pi, 400)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for beta, col in [(0.3, STEEL), (0.6, INK), (0.9, FLOW)]:
        d = [doppler_general(beta, t) for t in theta]
        ax.plot(np.degrees(theta), d, color=col, lw=2,
                label=fr"$\beta={beta}$  ($1/\gamma={doppler_transverse(beta):.2f}$)")
    ax.axhline(1.0, color="#aaaaaa", lw=0.8, ls="--")
    ax.axvline(90.0, color="#cccccc", lw=0.8)
    ax.text(8, 1.05, "blueshift", color=INK)
    ax.text(120, 0.55, "redshift", color=FLOW)
    ax.set_yscale("log")
    ax.set_xlim(0, 180)
    ax.set_xticks([0, 45, 90, 135, 180])
    ax.set_xlabel(r"ray angle from boost axis  $\theta$  (deg)")
    ax.set_ylabel(r"$f_{obs}/f_{src}$")
    ax.set_title(r"Relativistic Doppler  $f_{obs}/f_{src}=1/[\gamma(1-\beta\cos\theta)]$")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig1_doppler_factor.svg")
    caps["fig1_doppler_factor.svg"] = (
        "Relativistic Doppler factor f_obs/f_src = 1/[gamma(1 - beta cos theta)] versus the "
        "ray's angle theta from the boost axis, for beta = 0.3, 0.6, 0.9. Forward rays "
        "(theta -> 0) are blueshifted (>1) and backward rays (theta -> 180 deg) redshifted "
        "(<1); the transverse value at 90 deg is the pure time-dilation redshift 1/gamma.")

    # Fig 2 — aberration / headlight beaming: rest-frame isotropic rays bunch forward.
    beta = 0.9
    rest_deg = np.linspace(0.0, 180.0, 19)        # rays evenly spaced in the rest frame
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for a in rest_deg:
        ar = np.radians(a)
        lab = aberration(ar, -beta)               # rest -> lab is the -beta boost
        for sgn in (1.0, -1.0):                    # mirror to fill the full circle
            ax.plot([0, np.cos(ar)], [0, sgn * np.sin(ar)],
                    color="#cfcfdc", lw=1.0, zorder=1)
            ax.plot([0, np.cos(lab)], [0, sgn * np.sin(lab)],
                    color=FLOW, lw=1.4, zorder=2)
    thc = headlight_halfangle(beta)               # forward cone arccos(beta)
    for sgn in (1.0, -1.0):
        ax.plot([0, 1.18 * np.cos(thc)], [0, sgn * 1.18 * np.sin(thc)],
                color=INK, lw=1.6, ls="--", zorder=3)
    ax.annotate("source motion", xy=(1.12, 0), xytext=(0.2, 0),
                arrowprops=dict(arrowstyle="->", color=ALT), color=ALT, va="center")
    ax.plot(0, 0, "o", color=INK, ms=4)
    ax.text(0.62, 0.30, fr"half-cone $\arccos\beta={np.degrees(thc):.0f}^\circ$",
            color=INK, fontsize=9)
    ax.set_aspect("equal")
    ax.set_xlim(-1.25, 1.35); ax.set_ylim(-1.25, 1.25)
    ax.set_xlabel("boost axis  $x$"); ax.set_ylabel("$y$")
    ax.set_title(r"Aberration / beaming ($\beta=0.9$): isotropic rays bunch forward")
    grey = plt.Line2D([], [], color="#cfcfdc", lw=1.0, label="rest-frame rays")
    orng = plt.Line2D([], [], color=FLOW, lw=1.4, label="lab-frame (aberrated)")
    ax.legend(handles=[grey, orng], loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig2_aberration_beaming.svg")
    caps["fig2_aberration_beaming.svg"] = (
        "Stellar aberration / relativistic headlight effect at beta = 0.9. Rays emitted "
        "isotropically in the source rest frame (grey) are swept toward the forward "
        "direction in the lab frame (orange) by cos theta' = (cos theta - beta)/(1 - beta cos theta); "
        "half of all photons fall inside the forward cone of half-angle arccos(beta) (dashed).")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
