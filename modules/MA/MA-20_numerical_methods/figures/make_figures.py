"""MA-20 figures — order-of-accuracy convergence (quadrature & ODE) and root-finder rates.

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
from numerical import (                            # noqa: E402
    trapezoid, simpson, euler, rk4, quad_order, ode_order, newton,
)

INK, RUST, PLUM, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 — the organizing idea of the module: error ~ h^p is a straight line of
    # slope -p on log-log. Quadrature of int_0^1 e^x and the ODE y'=y, both exact-known.
    Ns = [2, 4, 8, 16, 32, 64, 128, 256]
    fexp = math.exp
    Iexact = math.e - 1.0
    et = [abs(trapezoid(fexp, 0.0, 1.0, N) - Iexact) for N in Ns]
    es = [abs(simpson(fexp, 0.0, 1.0, N) - Iexact) for N in Ns]
    ode = lambda t, y: y
    ee = [abs(euler(ode, 1.0, 1.0, N) - math.e) for N in Ns]
    er = [abs(rk4(ode, 1.0, 1.0, N) - math.e) for N in Ns]
    P = np.array(Ns, dtype=float)
    # measured orders (the module's own diagnostics), quoted in the caption
    o_t = quad_order(trapezoid, fexp, 0.0, 1.0, Iexact)
    o_s = quad_order(simpson, fexp, 0.0, 1.0, Iexact)
    o_e = ode_order(euler, ode, 1.0, 1.0, math.e)
    o_r = ode_order(rk4, ode, 1.0, 1.0, math.e)

    fig, (axq, axo) = plt.subplots(1, 2, figsize=(6.9, 3.4))
    axq.loglog(Ns, et, "o-", color=INK, lw=1.8, label="trapezoid (2)")
    axq.loglog(Ns, es, "s-", color=RUST, lw=1.8, label="Simpson (4)")
    axq.loglog(P, et[0] * (P / P[0]) ** -2.0, color=INK, ls=":", lw=1.0)
    axq.loglog(P, es[0] * (P / P[0]) ** -4.0, color=RUST, ls=":", lw=1.0)
    axq.set_title(r"Quadrature $\int_0^1 e^x\,dx$")
    axq.set_xlabel("subintervals $N$"); axq.set_ylabel("absolute error")
    axq.legend(frameon=False, fontsize=9)

    axo.loglog(Ns, ee, "o-", color=PLUM, lw=1.8, label="Euler (1)")
    axo.loglog(Ns, er, "s-", color=STEEL, lw=1.8, label="RK4 (4)")
    axo.loglog(P, ee[0] * (P / P[0]) ** -1.0, color=PLUM, ls=":", lw=1.0)
    axo.loglog(P, er[0] * (P / P[0]) ** -4.0, color=STEEL, ls=":", lw=1.0)
    axo.set_title(r"ODE $y'=y,\ y(1)=e$")
    axo.set_xlabel("steps $n$"); axo.set_ylabel("absolute error")
    axo.legend(frameon=False, fontsize=9)
    fig.suptitle(r"Order of accuracy: error $\propto h^p$ (dotted = slope $-p$)", y=1.02)
    _save(fig, "fig1_order_convergence.svg")
    caps["fig1_order_convergence.svg"] = (
        "Order of accuracy made visible: absolute error vs the number of steps on "
        "log-log, where a method of order $p$ falls as a straight line of slope $-p$ "
        "(dotted guides). Left: trapezoid and Simpson on $\\int_0^1 e^x\\,dx$ (measured "
        f"orders {o_t:.1f} and {o_s:.1f}). Right: Euler and RK4 on $y'=y$ (measured "
        f"orders {o_e:.1f} and {o_r:.1f}). Doubling the work buys $2^p$ in accuracy "
        "— the single most useful check in numerics.")

    # Fig 2 — root finders for x^2 - 2 = 0: how fast the error dies per iteration.
    # Newton returns its iterate history; bisection/secant are stepped here to expose
    # the same per-iteration error (they mirror the module's bisection/secant).
    root = math.sqrt(2.0)
    f = lambda x: x * x - 2.0
    fp = lambda x: 2.0 * x

    _, hist = newton(f, fp, 2.0)
    e_newton = [abs(x - root) for x in hist]

    a, c = 1.0, 2.0; fa = f(a)                       # bisection on [1,2] (linear)
    e_bis = [abs(0.5 * (a + c) - root)]
    for _ in range(60):
        m = 0.5 * (a + c); fm = f(m)
        if fa * fm < 0:
            c = m
        else:
            a, fa = m, fm
        e_bis.append(abs(0.5 * (a + c) - root))
        if (c - a) < 1e-16:
            break

    x0, x1 = 1.0, 2.0; f0, f1 = f(x0), f(x1)         # secant (order ~1.618)
    e_sec = [abs(x1 - root)]
    for _ in range(20):
        if abs(f1) < 1e-15:
            break
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        x0, f0, x1, f1 = x1, f1, x2, f(x2)
        e_sec.append(abs(x1 - root))

    floor = lambda seq: [max(e, 1e-17) for e in seq]
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.semilogy(range(len(e_newton)), floor(e_newton), "o-", color=RUST, lw=1.9,
                label="Newton (quadratic)")
    ax.semilogy(range(len(e_sec)), floor(e_sec), "^-", color=PLUM, lw=1.8,
                label=r"secant ($\approx 1.62$)")
    ax.semilogy(range(len(e_bis)), floor(e_bis), "s-", color=STEEL, lw=1.5,
                label="bisection (linear)")
    ax.set_xlim(0, 24)
    ax.set_ylim(1e-16, 5.0)
    ax.set_xlabel("iteration $k$"); ax.set_ylabel(r"error $|x_k-\sqrt{2}|$")
    ax.set_title(r"Root finding for $x^2-2=0$: convergence rates")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_root_convergence.svg")
    caps["fig2_root_convergence.svg"] = (
        "Convergence of three root finders on $x^2-2=0$ (error vs iteration, log scale). "
        "Newton (from the iterate history returned by newton()) roughly squares the "
        "error each step — the correct digits double — reaching machine precision in "
        "about five steps; the secant method is nearly as fast without a derivative; "
        "bisection is a straight line, gaining one bit (a factor of 2) per step.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
