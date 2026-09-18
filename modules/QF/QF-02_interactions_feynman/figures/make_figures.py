"""QF-02 figures — Mandelstam kinematics & the Feynman propagator.

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
from feynman import (                              # noqa: E402
    mandelstam, mandelstam_sum, propagator, minkowski_square,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the three Mandelstam invariants vs CM scattering angle, and the
    # invariant identity s + t + u = 4 m^2 (flat) computed from mandelstam().
    m, E_cm = 1.0, 5.0
    theta = np.linspace(0.0, np.pi, 400)
    s = np.empty_like(theta); t = np.empty_like(theta); u = np.empty_like(theta)
    for i, th in enumerate(theta):
        s[i], t[i], u[i] = mandelstam(E_cm, float(th), m)
    deg = np.degrees(theta)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(deg, s, color=INK, lw=2, label=r"$s=E_{cm}^2$  (constant)")
    ax.plot(deg, t, color=FLOW, lw=2, label=r"$t=-2|\mathbf{p}|^2(1-\cos\theta)$")
    ax.plot(deg, u, color=STEEL, lw=2, label=r"$u=-2|\mathbf{p}|^2(1+\cos\theta)$")
    ax.plot(deg, s + t + u, color=ALT, lw=2, ls="--",
            label=r"$s+t+u=4m^2$")
    ax.axhline(mandelstam_sum(m), color="#888888", lw=0.8)
    ax.axhline(0, color="#cccccc", lw=0.6)
    ax.set_xlim(0, 180); ax.set_xticks([0, 45, 90, 135, 180])
    ax.set_xlabel(r"CM scattering angle $\theta$ (deg)")
    ax.set_ylabel("invariant value")
    ax.set_title(r"Mandelstam invariants ($m=1,\ \sqrt{s}=5$): $s+t+u=4m^2$ pinned")
    ax.legend(loc="center left", frameon=False, fontsize=9)
    _save(fig, "fig1_mandelstam.svg")
    caps["fig1_mandelstam.svg"] = (
        r"The three Mandelstam invariants of $2\to2$ equal-mass scattering from "
        r"mandelstam$(\sqrt{s}{=}5,\theta,m{=}1)$: $s$ is fixed by the CM energy "
        r"while $t,u$ slide linearly in $\cos\theta$ (both $\le 0$, spacelike "
        r"momentum transfer). Their sum (dashed) stays pinned at $s+t+u=4m^2$ for "
        r"every angle — the kinematic identity that leaves only two independent "
        r"invariants.")

    # Fig 2 — the Feynman propagator D_F = i/(p^2 - m^2 + i eps) built by calling
    # propagator() on 4-vectors with a swept invariant square p^2 = m^2 + x.
    m, eps = 1.0, 0.3
    x = np.linspace(-3.0, 3.0, 600)               # x = p^2 - m^2
    re = np.empty_like(x); im = np.empty_like(x)
    for i, xi in enumerate(x):
        p2 = m * m + xi
        p4 = (np.array([np.sqrt(p2), 0.0, 0.0, 0.0]) if p2 >= 0.0
              else np.array([0.0, np.sqrt(-p2), 0.0, 0.0]))
        z = propagator(p4, m, eps=eps)
        # sanity: the constructed 4-vector really has invariant square p^2 = m^2 + x
        assert abs(minkowski_square(p4) - p2) < 1e-9
        re[i], im[i] = z.real, z.imag

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(x, re, color=INK, lw=2,
            label=r"$\mathrm{Re}\,D_F=\epsilon/(x^2+\epsilon^2)$  (nascent $\pi\delta$)")
    ax.plot(x, im, color=FLOW, lw=2,
            label=r"$\mathrm{Im}\,D_F=x/(x^2+\epsilon^2)$  (principal value $1/x$)")
    ax.axvline(0, color="#888888", lw=0.8, ls=":")
    ax.axhline(0, color="#cccccc", lw=0.6)
    ax.annotate(r"on-shell pole $p^2=m^2$", xy=(0.0, 1.0/eps), xytext=(0.6, 2.7),
                color=ALT, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=ALT, lw=1.0))
    ax.set_xlim(-3, 3)
    ax.set_xlabel(r"$x=p^2-m^2$")
    ax.set_ylabel(r"$D_F(p)$")
    ax.set_title(r"Feynman propagator $D_F=i/(p^2-m^2+i\epsilon)$  ($\epsilon=0.3$)")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    _save(fig, "fig2_propagator.svg")
    caps["fig2_propagator.svg"] = (
        r"The scalar Feynman propagator $D_F=i/(p^2-m^2+i\epsilon)$ from "
        r"propagator(), evaluated on 4-vectors swept through the invariant "
        r"$x=p^2-m^2$ (regulator $\epsilon=0.3$). $\mathrm{Re}\,D_F$ is a Lorentzian "
        r"of width $\epsilon$ peaking at the on-shell pole $x=0$ (a nascent "
        r"$\pi\delta(x)$), while $\mathrm{Im}\,D_F$ is the dispersive principal "
        r"value $\to 1/x$ off shell — the $i\epsilon$ causal prescription that sits "
        r"on every internal line.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
