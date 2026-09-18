"""MA-08 figures — heat decay & wave oscillation vs separation-of-variables, and Laplace.

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
from pde import (                                   # noqa: E402
    heat_1d, wave_1d, laplace_2d, heat_mode, wave_mode,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    L, N = 1.0, 41
    dx = L / (N - 1)
    xs = [i * dx for i in range(N)]
    xa = np.array(xs)
    u0 = [math.sin(math.pi * x) for x in xs]          # fundamental mode sin(pi x)

    # Fig 1 — heat (parabolic, decays) and wave (hyperbolic, oscillates), each vs
    # its separation-of-variables mode.  Top: u_t = u_xx.  Bottom: u_tt = u_xx.
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.2, 5.6), sharex=True)
    fig.subplots_adjust(hspace=0.42)

    h_exact = heat_mode(L, 1.0, 1)                    # sin(pi x) e^{-(pi)^2 t}
    dt_h, cols = 2e-4, [INK, STEEL, ALT, FLOW]
    for t, c in zip([0.0, 0.02, 0.05, 0.1], cols):
        uf = heat_1d(u0, 1.0, dx, dt_h, round(t / dt_h))
        ax1.plot(xa, uf, color=c, lw=2, label=fr"$t={t:g}$")
        ax1.plot(xa, [h_exact(x, t) for x in xs], color=c, lw=0, marker="o", ms=3,
                 markevery=3, alpha=0.8)
    ax1.set_ylabel(r"$u(x,t)$")
    ax1.set_title(r"Heat $u_t=u_{xx}$: amplitude decays as $e^{-(\pi/L)^2 t}$")
    ax1.legend(loc="upper right", frameon=False, fontsize=8.5, ncol=2)

    w_exact = wave_mode(L, 1.0, 1)                    # sin(pi x) cos(pi t)
    v0 = [0.0] * N
    for t, c in zip([0.0, 0.25, 0.5, 0.75, 1.0], [INK, STEEL, ALT, FLOW, "#7a3b3b"]):
        uf = wave_1d(u0, v0, 1.0, dx, dx, round(t / dx))     # Courant C = 1
        ax2.plot(xa, uf, color=c, lw=2, label=fr"$t={t:g}$")
        ax2.plot(xa, [w_exact(x, t) for x in xs], color=c, lw=0, marker="o", ms=3,
                 markevery=3, alpha=0.8)
    ax2.axhline(0, color="#cccccc", lw=0.6)
    ax2.set_xlabel(r"position $x$"); ax2.set_ylabel(r"$u(x,t)$")
    ax2.set_title(r"Wave $u_{tt}=u_{xx}$: standing wave, amplitude $\cos(\pi t)$")
    ax2.legend(loc="upper right", frameon=False, fontsize=8.5, ncol=3)
    _save(fig, "fig1_heat_wave.svg")
    caps["fig1_heat_wave.svg"] = (
        r"Finite-difference solutions (solid) versus the separated mode (dots) for the "
        r"fundamental $u(x,0)=\sin(\pi x)$. Top: heat_1d (FTCS) decays as "
        r"$\sin(\pi x)\,e^{-(\pi/L)^2 t}$, matching heat_mode. Bottom: wave_1d (leapfrog at "
        r"Courant $C=1$) keeps the shape but its amplitude swings as $\cos(\pi t)$, matching "
        r"wave_mode — parabolic decay versus hyperbolic oscillation from the same initial data.")

    # Fig 2 — Laplace's equation on a square by Gauss-Seidel relaxation (hot top edge).
    n = 41
    grid = [[0.0] * n for _ in range(n)]
    for j in range(n):
        grid[0][j] = 1.0                              # top edge held at 1 (Dirichlet)
    sol, iters = laplace_2d(grid, tol=1e-5)
    U = np.array(sol)

    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    im = ax.imshow(U, extent=[0, 1, 0, 1], origin="upper", cmap="viridis",
                   vmin=0.0, vmax=1.0)
    cs = ax.contour(np.linspace(0, 1, n), np.linspace(1, 0, n), U,
                    levels=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.85],
                    colors="w", linewidths=0.8, alpha=0.8)
    ax.clabel(cs, inline=True, fontsize=7, fmt="%.2f")
    ax.set_xlabel(r"$x$"); ax.set_ylabel(r"$y$")
    ax.set_title(fr"Laplace $\nabla^2 u=0$: Gauss-Seidel relaxation ({iters} sweeps)")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label=r"$u(x,y)$")
    _save(fig, "fig2_laplace.svg")
    caps["fig2_laplace.svg"] = (
        r"Steady-state solution of $\nabla^2 u=0$ on the unit square with the top edge held at "
        r"$u=1$ and the other three at $0$, relaxed with laplace_2d (Gauss-Seidel: each "
        r"interior point becomes the average of its four neighbours). White curves are "
        r"isopotentials. With no time derivative the field is harmonic — the same boundary-value "
        r"problem as the electrostatic potential and steady-state temperature.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
