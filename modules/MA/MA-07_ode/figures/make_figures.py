"""MA-07 figures — Euler vs RK4 on the oscillator, and a linear system by eigen-modes.

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
from ode import (                                   # noqa: E402
    integrate, euler_step, rk4_step, second_order_system,
    linear_rhs, linear_evolve_symmetric,
)
from linalg import eig_symmetric                    # noqa: E402  (ode added MA-04 to sys.path)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — SHO y'' = -y in the phase plane: Euler injects energy, RK4 holds the orbit.
    sho = second_order_system(lambda t, y, v: -y)        # d/dt [y, v] = [v, -y]
    t1, n = 6.0 * np.pi, 190                              # same coarse dt ~ 0.10 for both
    _, yE = integrate(sho, [1.0, 0.0], 0.0, t1, n, method=euler_step)
    _, yR = integrate(sho, [1.0, 0.0], 0.0, t1, n, method=rk4_step)
    yE, vE = np.array([s[0] for s in yE]), np.array([s[1] for s in yE])
    yR, vR = np.array([s[0] for s in yR]), np.array([s[1] for s in yR])
    th = np.linspace(0, 2 * np.pi, 300)

    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    ax.plot(np.cos(th), -np.sin(th), color="#999999", lw=1.2, ls="--",
            label=r"exact orbit $y^2+y'^2=1$")
    ax.plot(yE, vE, color=FLOW, lw=1.6, label=fr"Euler ($n={n}$): spirals out")
    ax.plot(yR, vR, color=INK, lw=1.6, label=fr"RK4 ($n={n}$): on the orbit")
    ax.plot(1.0, 0.0, "o", ms=6, color="k"); ax.annotate(r"start $(1,0)$", (1.0, 0.0),
            xytext=(6, 6), textcoords="offset points", fontsize=9)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$y$"); ax.set_ylabel(r"$y' $")
    ax.set_title(r"Phase portrait of $y''=-y$: Euler vs RK4 (same step $\Delta t$)")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_euler_vs_rk4.svg")
    caps["fig1_euler_vs_rk4.svg"] = (
        r"The harmonic oscillator $y''=-y$ in the phase plane $(y,y')$, both schemes taking "
        r"the same coarse step $\Delta t\approx0.1$ via integrate. The exact motion is the "
        r"unit circle (constant energy); explicit Euler (orange) gains energy and spirals "
        r"outward, while RK4 (blue) — fourth order — stays on the orbit. This is why RK4 is "
        r"the workhorse integrator.")

    # Fig 2 — linear flow dx/dt = A x by diagonalization (MA-04 eigen) vs RK4.
    A = [[0.0, 1.0], [1.0, 0.0]]                          # symmetric; eigenvalues +/- 1 (saddle)
    vals, vecs = eig_symmetric(A)
    tt = np.linspace(-1.25, 1.25, 90)
    starts = [(np.cos(a), np.sin(a)) for a in np.radians([20, 65, 115, 160, 200, 245, 295, 340])]

    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    for k, x0 in enumerate(starts):                       # exact streamlines e^{At}x0
        xs = np.array([linear_evolve_symmetric(A, list(x0), float(t)) for t in tt])
        ax.plot(xs[:, 0], xs[:, 1], color=ALT, lw=1.3,
                label=r"exact $e^{At}\mathbf{x}_0$" if k == 0 else None)
    # eigen-directions (the normal modes): lam=+1 unstable, lam=-1 stable
    for lam, v in zip(vals, vecs):
        s = 2.2 / max(abs(v[0]), abs(v[1]))
        col = FLOW if lam > 0 else STEEL
        ax.plot([-s * v[0], s * v[0]], [-s * v[1], s * v[1]], color=col, lw=2.0, ls="--",
                label=fr"eigvec $\lambda={lam:+.0f}$")
    _, xr = integrate(linear_rhs(A), list(starts[0]), 0.0, 1.25, 60, method=rk4_step)
    xr = np.array(xr)
    ax.plot(xr[::3, 0], xr[::3, 1], "o", ms=4.5, color=INK, label="RK4 check")
    ax.set_aspect("equal"); ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.2, 2.2)
    ax.set_xlabel(r"$x_1$"); ax.set_ylabel(r"$x_2$")
    ax.set_title(r"Linear flow $\dot{\mathbf{x}}=A\mathbf{x}$: exact eigen-modes vs RK4")
    ax.legend(loc="upper right", frameon=False, fontsize=8.5)
    _save(fig, "fig2_linear_saddle.svg")
    caps["fig2_linear_saddle.svg"] = (
        r"Flow of $\dot{\mathbf{x}}=A\mathbf{x}$ for $A=[[0,1],[1,0]]$. Diagonalizing with the "
        r"MA-04 eigensolver gives eigenvalues $\lambda=\pm1$; the exact solution "
        r"$\mathbf{x}(t)=\sum_i(\mathbf{v}_i\!\cdot\!\mathbf{x}_0)e^{\lambda_i t}\mathbf{v}_i$ "
        r"(purple streamlines, from linear_evolve_symmetric) is a saddle that grows along the "
        r"$\lambda=+1$ eigenvector and decays along $\lambda=-1$. RK4 of the same system "
        r"(blue dots) lands right on it — these eigen-modes are the normal modes.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
