"""QM-10 figures -- spherical-harmonic angular distributions and space quantization.

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
from angular_momentum import (                     # noqa: E402
    spherical_harmonic, casimir_eigenvalue, m_values,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- |Y_l^m|^2 angular distributions (cross-section in the x-z plane).
    # |Y_l^m|^2 is phi-independent, so r(theta)=|Y_l^m(theta,0)|^2 traced as a polar
    # lobe about the z (vertical) axis.  Y from the module's spherical_harmonic.
    theta = np.linspace(0.0, np.pi, 500)
    cases = [(1, 0), (2, 0), (2, 1), (2, 2)]
    cols = [INK, FLOW, ALT, STEEL]
    fig, axes = plt.subplots(2, 2, figsize=(6.4, 6.0))
    for ax, (l, m), col in zip(axes.ravel(), cases, cols):
        r = np.abs(spherical_harmonic(l, m, theta, 0.0)) ** 2
        X = r * np.sin(theta)                            # horizontal (x), z vertical
        Z = r * np.cos(theta)
        xs = np.concatenate([X, -X[::-1]])               # mirror for the full lobe
        zs = np.concatenate([Z, Z[::-1]])
        ax.fill(xs, zs, color=col, alpha=0.80)
        ax.plot(xs, zs, color=INK, lw=0.8)
        R = 1.08 * float(np.max(r))
        ax.axhline(0, color="#bbbbbb", lw=0.5); ax.axvline(0, color="#bbbbbb", lw=0.5)
        ax.set_xlim(-R, R); ax.set_ylim(-R, R); ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlabel(r"$x$", fontsize=9); ax.set_ylabel(r"$z$", fontsize=9)
        ax.set_title(fr"$|Y_{{{l}}}^{{{m}}}|^2$", fontsize=11)
    fig.suptitle(r"Angular distributions $|Y_l^m(\theta,\phi)|^2$  ($x$–$z$ section)",
                 fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _save(fig, "fig1_spherical_harmonics.svg")
    caps["fig1_spherical_harmonics.svg"] = (
        r"Probability lobes $|Y_l^m(\theta,\phi)|^2$ (independent of $\phi$) from "
        r"the module's spherical_harmonic, as cross-sections about the vertical $z$ "
        r"axis. $Y_1^0$ is the dumbbell along $z$; raising $l$ adds polar structure "
        r"($Y_2^0$), while at fixed $l$ raising $|m|$ pushes the density to the "
        r"equator -- $Y_2^2\propto\sin^4\theta$ is a torus. These are the "
        r"position-space eigenstates of $L^2$ and $L_z$.")

    # Fig 2 -- space quantization (vector model) for l=2: L_z = m hbar takes 2l+1
    # values while |L| = hbar sqrt(l(l+1)) > l, so L can never align with z.
    # |L| from casimir_eigenvalue, the rungs from m_values -- both the module's.
    l = 2.0
    Lmag = float(np.sqrt(casimir_eigenvalue(l)))
    ms = m_values(l)
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    phi = np.linspace(0, 2 * np.pi, 400)
    ax.plot(Lmag * np.cos(phi), Lmag * np.sin(phi), color="#cccccc", lw=0.9, ls="--")
    for mm, col in zip(ms, (INK, FLOW, ALT, STEEL, INK)):
        xt = float(np.sqrt(max(Lmag ** 2 - mm ** 2, 0.0)))
        for sx in (+1, -1):                              # both sides hint the cone
            ax.annotate("", xy=(sx * xt, mm), xytext=(0, 0),
                        arrowprops=dict(arrowstyle="->", color=col, lw=1.8))
        ax.plot([-Lmag, Lmag], [mm, mm], color="#dddddd", lw=0.7, ls=":")
        ax.text(Lmag + 0.12, mm, fr"$m={int(mm):+d}$", va="center", color=col, fontsize=9)
    ax.axvline(0, color="#888888", lw=0.8)
    ax.set_xlim(-Lmag - 0.7, Lmag + 0.9); ax.set_ylim(-Lmag - 0.3, Lmag + 0.3)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$L_x$  (in-plane component, $\hbar$)")
    ax.set_ylabel(r"$L_z/\hbar$")
    ax.set_title(r"Space quantization ($l=2$): $|L|=\sqrt{l(l+1)}\,\hbar>l\hbar$")
    ax.text(0.15, Lmag - 0.18, fr"$|L|=\sqrt{{6}}={Lmag:.3f}$", color="#555555", fontsize=9)
    _save(fig, "fig2_space_quantization.svg")
    caps["fig2_space_quantization.svg"] = (
        r"The vector model for $l=2$: $L_z=m\hbar$ takes the $2l+1=5$ values from "
        r"m_values, while the magnitude $|L|=\hbar\sqrt{l(l+1)}=\sqrt6\,\hbar$ (from "
        r"casimir_eigenvalue) is FIXED. Each allowed orientation is a cone (arrows "
        r"to both sides) of fixed length projecting onto its rung; because "
        r"$\sqrt{l(l+1)}>l$, the vector never lies along $z$ -- the geometric face "
        r"of $[L_x,L_y]\neq0$.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
