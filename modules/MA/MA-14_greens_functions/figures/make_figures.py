"""MA-14 figures — the Green's function as a point-source response, its spectral
sum, and the built-up solution u=int G f.

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
from greens_function import (                       # noqa: E402
    green_dirichlet, green_series, solve_bvp_greens, solve_bvp_direct,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    x = np.linspace(0.0, 1.0, 400)

    # Fig 1 — the point-source response G(x,xi) for -u'' on [0,1], and its
    # eigenfunction sum. The closed-form tent green_dirichlet(x,xi)=x_<(1-x_>) has
    # a unit kink at the source xi; green_series adds modes phi_n phi_n / lambda_n
    # and converges to it (G = L^{-1} written in the eigenbasis).
    xi = 0.5
    G_tent = [green_dirichlet(xx, xi) for xx in x]

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    for nmax, col in [(1, STEEL), (3, ALT), (12, FLOW)]:
        Gs = [green_series(xx, xi, nmax) for xx in x]
        ax.plot(x, Gs, color=col, lw=1.6,
                label=fr"spectral sum, $n\leq{nmax}$")
    ax.plot(x, G_tent, color=INK, lw=2.4,
            label=r"closed form $x_<(1-x_>)$")
    ax.axvline(xi, color="#888888", lw=0.8, ls=":")
    ax.plot(xi, green_dirichlet(xi, xi), "o", color=INK, ms=5)
    ax.annotate(r"source $\xi=\frac{1}{2}$",
                xy=(xi, green_dirichlet(xi, xi)), xytext=(0.56, 0.205),
                color="#444444", fontsize=9)
    ax.set_xlim(0, 1)
    ax.set_xlabel("position $x$")
    ax.set_ylabel(r"$G(x,\xi)$")
    ax.set_title(r"Green's function $G(x,\xi)=\sum_n \phi_n(x)\phi_n(\xi)/\lambda_n$")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_point_source.svg")
    caps["fig1_point_source.svg"] = (
        r"Response to a unit point source at $\xi=\tfrac12$ for $-u''$ on $[0,1]$: the "
        r"closed-form tent $G=x_<(1-x_>)$ (green_dirichlet, dark) has a unit slope-jump "
        r"at the source. The eigenfunction series $\sum_n\phi_n(x)\phi_n(\xi)/\lambda_n$ "
        r"with $\phi_n=\sqrt2\sin n\pi x,\ \lambda_n=(n\pi)^2$ (green_series) converges to "
        r"it as more modes are added — $G$ is $L^{-1}$ in the eigenbasis.")

    # Fig 2 — the built-up solution u(x)=int G(x,xi) f(xi) dxi for two forcings,
    # each against its exact answer and an independent finite-difference solve.
    xs_eval = [0.05 * (i + 1) for i in range(19)]           # interior sample points
    f_sin = lambda t: math.sin(math.pi * t)                 # exact u = sin(pi x)/pi^2
    f_one = lambda t: 1.0                                    # exact u = x(1-x)/2
    u_sin = solve_bvp_greens(f_sin, xs_eval)
    u_one = solve_bvp_greens(f_one, xs_eval)
    xd, ud = solve_bvp_direct(f_sin, 19)                    # independent FD cross-check

    u_sin_exact = np.sin(math.pi * x) / math.pi ** 2
    u_one_exact = x * (1.0 - x) / 2.0

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(x, u_sin_exact, color=INK, lw=2,
            label=r"$f=\sin\pi x$: exact $\sin(\pi x)/\pi^2$")
    ax.plot(xs_eval, u_sin, "o", color=INK, ms=5, mfc="white",
            label=r"$\int G f\,d\xi$ (Green)")
    ax.plot(xd, ud, "x", color=STEEL, ms=6, label="finite-difference solve")
    ax.plot(x, u_one_exact, color=FLOW, lw=2,
            label=r"$f=1$: exact $x(1-x)/2$")
    ax.plot(xs_eval, u_one, "s", color=FLOW, ms=4, mfc="white",
            label=r"$\int G f\,d\xi$ (Green)")
    ax.set_xlim(0, 1)
    ax.set_xlabel("position $x$")
    ax.set_ylabel("solution $u(x)$")
    ax.set_title(r"Built-up solution $u(x)=\int_0^1 G(x,\xi)\,f(\xi)\,d\xi$")
    ax.legend(loc="upper center", frameon=False, fontsize=8.5, ncol=1)
    _save(fig, "fig2_built_up_solution.svg")
    caps["fig2_built_up_solution.svg"] = (
        r"Superposing point-source responses solves the BVP: $u(x)=\int_0^1 "
        r"G(x,\xi)f(\xi)\,d\xi$ (solve_bvp_greens, open markers) for $f=\sin\pi x$ and "
        r"$f=1$ lands exactly on the analytic solutions $\sin(\pi x)/\pi^2$ and "
        r"$x(1-x)/2$ (solid), and agrees with an independent finite-difference solve "
        r"(solve_bvp_direct, crosses).")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
