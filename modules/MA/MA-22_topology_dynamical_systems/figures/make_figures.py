"""MA-22 figures — the logistic route to chaos and the linear-stability gallery.

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
matplotlib.rcParams["savefig.dpi"] = 200          # resolution for the one rasterized layer
import matplotlib.pyplot as plt                    # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from topo_dynamics import (                        # noqa: E402
    logistic_orbit, lyapunov_logistic, period_of_orbit,
    eigenvalues_2x2, classify_equilibrium,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _fmt_eigs(ev):
    """Render the eigenvalue pair from eigenvalues_2x2 as mathtext."""
    a, b = ev
    if abs(a.imag) < 1e-9:                                   # real pair
        return fr"$\lambda={a.real:+.0f},\,{b.real:+.0f}$"
    im = abs(a.imag)
    im_s = "i" if abs(im - 1.0) < 1e-9 else f"{im:.0f}i"
    re_s = "" if abs(a.real) < 1e-9 else f"{a.real:+.0f}"
    return fr"$\lambda={re_s}\pm {im_s}$"     # space after \pm: avoids '\pmi'


def main():
    caps = {}

    # Fig 1 — the logistic map's route to chaos: bifurcation diagram (top) over the
    # Lyapunov exponent (bottom), both from the module's own iterators. The attractor
    # is logistic_orbit after transients; lyapunov_logistic averages ln|f'| along it
    # (lambda<0 on a cycle, >0 in chaos, = ln 2 at r=4). period_of_orbit tags the
    # period-3 window where order briefly returns inside the chaos.
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.2, 5.2), sharex=True,
                                   gridspec_kw={"height_ratios": [2.0, 1.1]})

    R, X = [], []
    for r in np.linspace(2.8, 4.0, 900):
        pts = logistic_orbit(r, 0.1, 220, skip=600)         # discard transients
        R.extend([r] * len(pts)); X.extend(pts)
    # ~200k attractor points: rasterize this one data layer so the SVG stays light
    # (axes, ticks, labels, title and the Lyapunov curve below remain pure vector).
    ax1.plot(R, X, ",", color=INK, alpha=0.30, rasterized=True)
    r_inf = 3.5699                                          # Feigenbaum accumulation point
    ax1.axvline(r_inf, color="#888888", lw=0.8, ls=":")
    ax1.text(r_inf - 0.02, 0.05, r"$r_\infty$", color="#555555", fontsize=10, ha="right")
    p3 = period_of_orbit(3.83)                              # detect the period-3 window
    ax1.annotate(fr"period-{p3} window", xy=(3.83, 0.16), xytext=(3.50, 0.30),
                 fontsize=9, color=FLOW,
                 arrowprops=dict(arrowstyle="->", color=FLOW, lw=0.8))
    ax1.set_ylim(0, 1)
    ax1.set_ylabel(r"attractor  $x_n$")
    ax1.set_title(r"Logistic map $x_{n+1}=r\,x_n(1-x_n)$: period-doubling into chaos")

    r_lyap = np.linspace(2.8, 4.0, 420)
    lam = np.array([lyapunov_logistic(r, n=20000, skip=2000) for r in r_lyap])
    ax2.axhline(0.0, color="#888888", lw=0.8, ls=":")
    ax2.fill_between(r_lyap, 0.0, lam, where=(lam > 0), color=FLOW, alpha=0.30)
    ax2.plot(r_lyap, lam, color=ALT, lw=1.3)
    ax2.axhline(math.log(2.0), color=STEEL, lw=0.8, ls="--")
    ax2.text(2.84, math.log(2.0) + 0.04, r"$\ln 2$", color=STEEL, fontsize=9)
    ax2.set_ylim(-2.5, 1.0)
    ax2.set_xlim(2.8, 4.0)
    ax2.set_xlabel(r"growth rate  $r$")
    ax2.set_ylabel(r"Lyapunov  $\lambda$")
    _save(fig, "fig1_logistic_bifurcation.svg")
    caps["fig1_logistic_bifurcation.svg"] = (
        r"The logistic map's route to chaos, all from the module's iterators. Top: the "
        r"bifurcation diagram (logistic_orbit after transients) shows a stable fixed "
        r"point period-double 2$\to$4$\to$8$\to\cdots$ at the Feigenbaum point "
        r"$r_\infty\approx3.57$, then chaos pierced by periodic windows (period_of_orbit "
        r"flags the period-3 window near $r\approx3.83$). Bottom: the Lyapunov exponent "
        r"$\lambda=\langle\ln|f'|\rangle$ (lyapunov_logistic) is $<0$ on every stable "
        r"cycle and $>0$ in chaos (orange), touching exactly $\ln 2$ at $r=4$.")

    # Fig 2 — linear-stability gallery: each 2x2 Jacobian's flow x'=Jx, titled with the
    # type from classify_equilibrium and the eigenvalues from eigenvalues_2x2. The sign
    # of the real parts sets stability; a complex pair spirals, a pure-imaginary pair
    # orbits (center). Same matrices the module's demo and tests use.
    cases = [
        ([[1, 0], [0, -1]],   STEEL),     # saddle: real, opposite sign
        ([[-2, 0], [0, -1]],  INK),       # stable node: real, same sign
        ([[-1, -2], [2, -1]], ALT),       # stable spiral: complex, Re<0
        ([[0, -1], [1, 0]],   FLOW),      # center: pure imaginary
    ]
    g = np.linspace(-2.0, 2.0, 24)
    Xg, Yg = np.meshgrid(g, g)
    fig, axes = plt.subplots(2, 2, figsize=(6.4, 5.9))
    for ax, (J, c) in zip(axes.flat, cases):
        (a, b), (cc, d) = J
        U = a * Xg + b * Yg
        V = cc * Xg + d * Yg
        ax.streamplot(Xg, Yg, U, V, color=c, density=0.9, linewidth=0.8, arrowsize=0.8)
        ax.plot(0, 0, "o", color="#222222", ms=4)
        ax.set_title(f"{classify_equilibrium(J)}\n{_fmt_eigs(eigenvalues_2x2(J))}",
                     fontsize=10)
        ax.set_xlim(-2, 2); ax.set_ylim(-2, 2)
        ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle(r"Linear stability: equilibria typed by the Jacobian's eigenvalues",
                 fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    _save(fig, "fig2_equilibria_gallery.svg")
    caps["fig2_equilibria_gallery.svg"] = (
        r"Phase portraits of the planar flow $\dot{x}=Jx$ for four Jacobians, each "
        r"labelled by classify_equilibrium and its eigenvalues_2x2 pair. Real "
        r"opposite-sign eigenvalues give a saddle ($\det J<0$); real same-sign a node; "
        r"a complex pair $\alpha\pm i\beta$ a spiral (stable when $\alpha<0$); and a "
        r"pure-imaginary pair a center of closed orbits. The sign of the eigenvalues' "
        r"real parts decides stability — the linearization theorem in one picture.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
