"""MA-10 figures — Laplace IVP responses and the s-plane pole picture.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.
"""
import cmath
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
from laplace import solve_ivp_laplace, rk4         # noqa: E402

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"

Q = 4.0                                            # q = w0^2 (natural frequency w0 = 2)
# (p, q, label, colour) for the three damping regimes of  y'' + p y' + q y = 0
REGIMES = [
    (0.6, "underdamped  ($p^2<4q$)", INK),
    (4.0, "critically damped  ($p^2=4q$)", FLOW),
    (6.0, "overdamped  ($p^2>4q$)", ALT),
]


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _poles(p, q):
    """Roots of the characteristic quadratic s^2 + p s + q (the Laplace poles)."""
    r = cmath.sqrt(p * p - 4.0 * q)
    return (-p + r) / 2.0, (-p - r) / 2.0


def main():
    caps = {}

    # Fig 1 — free response y(t) from solve_ivp_laplace in the three regimes,
    # y(0)=1, y'(0)=0. RK4 (rk4) dots cross-check the closed form.
    t = np.linspace(0.0, 8.0, 800)
    tm = np.linspace(0.3, 8.0, 14)                  # sparse RK4 check points
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    for p, lbl, col in REGIMES:
        y = solve_ivp_laplace(p, Q, 1.0, 0.0)
        ax.plot(t, [y(tt) for tt in t], color=col, lw=2, label=lbl)
        ax.plot(tm, [rk4(p, Q, 1.0, 0.0, 0.0, tt) for tt in tm], ls="none",
                marker="o", ms=3.2, mfc="white", mec=col)
    g = 0.6 / 2.0                                   # underdamped decay rate alpha = p/2
    ax.plot(t, np.exp(-g * t), color="#999999", lw=1.0, ls="--",
            label=r"envelope $\pm e^{-pt/2}$")
    ax.plot(t, -np.exp(-g * t), color="#999999", lw=1.0, ls="--")
    ax.axhline(0, color="#cccccc", lw=0.6)
    ax.set_xlim(0, 8); ax.set_xlabel("time $t$"); ax.set_ylabel("displacement $y(t)$")
    ax.set_title(r"Laplace IVP: roots of $s^2+ps+q$ set the regime ($q=4$)")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_damping_regimes.svg")
    caps["fig1_damping_regimes.svg"] = (
        "Free response of $y''+py'+qy=0$ ($y_0=1,\\,y_0'=0,\\,q=4$) from "
        "solve_ivp_laplace, which transforms, does algebra in $s$, and inverts by "
        "partial fractions. Open circles are an independent RK4 (rk4) check. The "
        "discriminant $p^2-4q$ selects the case: underdamped rings inside the "
        "$e^{-pt/2}$ envelope, critically and overdamped decay without oscillating.")

    # Fig 2 — pole migration in the s-plane as the damping p grows at fixed q.
    # Poles = roots of s^2+ps+q (the same roots invert_quadratic switches on).
    ps = np.linspace(0.0, 8.0, 400)
    und = np.array([_poles(p, Q) for p in ps if p * p < 4.0 * Q]).reshape(-1)
    ovr = np.array([_poles(p, Q) for p in ps if p * p > 4.0 * Q]).reshape(-1)
    th = np.linspace(0, 2 * np.pi, 200)

    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot(np.sqrt(Q) * np.cos(th), np.sqrt(Q) * np.sin(th),
            color="#dddddd", lw=1.0, ls="--", zorder=0)        # circle radius sqrt(q)
    ax.scatter(und.real, und.imag, s=8, color=STEEL, label="underdamped (complex pair)")
    ax.scatter(ovr.real, ovr.imag, s=8, color=FLOW, label="overdamped (real roots)")
    ax.scatter([-np.sqrt(Q)], [0.0], s=70, marker="*", color=INK, zorder=5,
               label=r"critical double root $-\sqrt{q}$")
    # the three specific systems of Fig 1, marked with their p value
    for p, _lbl, col in REGIMES:
        for r in _poles(p, Q):
            ax.scatter([r.real], [r.imag], s=46, facecolor="white",
                       edgecolor=col, linewidth=1.6, zorder=6)
        ax.annotate(f"$p={p:g}$", xy=(_poles(p, Q)[0].real, _poles(p, Q)[0].imag),
                    xytext=(_poles(p, Q)[0].real + 0.15, _poles(p, Q)[0].imag + 0.18),
                    fontsize=8.5, color=col)
    ax.axhline(0, color="#cccccc", lw=0.6); ax.axvline(0, color="#cccccc", lw=0.6)
    ax.set_aspect("equal")
    ax.set_xlim(-6.5, 0.8); ax.set_ylim(-2.6, 2.6)
    ax.set_xlabel(r"$\mathrm{Re}\,s$  (decay rate)")
    ax.set_ylabel(r"$\mathrm{Im}\,s$  (frequency)")
    ax.set_title(r"Pole migration as damping $p$ grows ($q=4$ fixed)")
    ax.legend(loc="lower left", frameon=False, fontsize=8.2)
    _save(fig, "fig2_s_plane_poles.svg")
    caps["fig2_s_plane_poles.svg"] = (
        "Poles of $Y(s)$ — the roots of $s^2+ps+q$ — as the damping $p$ increases "
        "with $q=4$ fixed. While $p^2<4q$ a complex-conjugate pair rides the circle "
        "$|s|=\\sqrt{q}$ (oscillation at $\\mathrm{Im}\\,s$, decay at $\\mathrm{Re}\\,s$); "
        "at $p=2\\sqrt{q}$ they merge into a double root $-\\sqrt{q}$, then split along "
        "the real axis (overdamped). White rings mark the three systems of Fig 1; all "
        "poles sit in $\\mathrm{Re}\\,s<0$, so every response decays.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
