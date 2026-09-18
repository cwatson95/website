"""CM-11 figures -- Kepler orbit shapes by eccentricity (integrated), and the
effective potential with its circular-orbit minimum and bound-orbit turning points.

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
from central_force import (                        # noqa: E402
    orbit, kepler_force, kepler_potential, effective_potential,
    circular_orbit_radius, kepler_period,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    mu, k = 1.0, 1.0
    r0 = 1.0                                        # start at r0 on +x, velocity tangential (+y)
    vc = math.sqrt(k / (mu * r0))                   # circular speed at r0; escape = sqrt(2) vc
    Fr = kepler_force(k)

    # Fig 1 -- orbit shapes from real `orbit` integration, by initial tangential
    # speed. Starting at perihelion with purely tangential v0, e = |v0^2 r0 mu/k - 1|.
    def trace(v0, tmax, n=4000):
        """Integrate the orbit forward and backward; stitch into one open/closed curve."""
        tf, yf = orbit(Fr, mu, (r0, 0.0), (0.0, v0), 0.0, tmax, n)
        tb, yb = orbit(Fr, mu, (r0, 0.0), (0.0, v0), 0.0, -tmax, n)
        xs = [s[0] for s in reversed(yb)] + [s[0] for s in yf]
        ys = [s[1] for s in reversed(yb)] + [s[1] for s in yf]
        return np.array(xs), np.array(ys)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    cases = [
        (1.00 * vc, 0.0, "circle  $e=0$", INK),
        (1.20 * vc, 0.44, "ellipse  $e\\approx0.44$", STEEL),
        (math.sqrt(2.0) * vc, 1.0, "parabola  $e=1$", FLOW),
        (1.62 * vc, 1.62, "hyperbola  $e\\approx1.6$", ALT),
    ]
    for v0, e, lab, col in cases:
        if e < 1.0 - 1e-9:                          # bound: integrate one full period
            a_semi = 1.0 / (2.0 / r0 - v0 * v0 / (k / mu))
            tmax = kepler_period(a_semi, mu, k)
            tf, yf = orbit(Fr, mu, (r0, 0.0), (0.0, v0), 0.0, tmax, 4000)
            xs = np.array([s[0] for s in yf]); ys = np.array([s[1] for s in yf])
        else:                                       # unbound: open arc, both branches
            xs, ys = trace(v0, 6.0, 4000)
        ax.plot(xs, ys, color=col, lw=2, label=lab)
    ax.plot(0, 0, "*", color="#caa200", ms=14, label="force centre")
    ax.plot(r0, 0, "o", color="#555555", ms=4)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-5.5, 2.5); ax.set_ylim(-3.6, 3.6)
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.set_title(r"Kepler orbits by eccentricity ($U=-k/r$), launched from $r_0$")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig1_orbit_shapes.svg")
    caps["fig1_orbit_shapes.svg"] = (
        "Trajectories integrated by the module's orbit() under the attractive force F = -k/r^2, all "
        "launched tangentially from the same point r0 with increasing speed. Below escape speed the "
        "orbit is a bound ellipse (a circle when v equals the circular speed); at escape speed it is "
        "a parabola (e=1); above it, an unbound hyperbola. The force centre sits at one focus.")

    # Fig 2 -- effective potential U_eff(r) = U(r) + L^2/(2 mu r^2) for two L, with
    # the circular-orbit minimum (circular_orbit_radius) and an energy level whose
    # turning points are the perihelion/aphelion of a bound orbit.
    r = np.linspace(0.25, 8.0, 800)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    U = kepler_potential(k)
    for L, col in [(1.0, INK), (1.4, STEEL)]:
        Ueff = effective_potential(U, L, mu)        # real module function
        ax.plot(r, [Ueff(ri) for ri in r], color=col, lw=2, label=fr"$U_{{\rm eff}},\ L={L}$")
        rmin = circular_orbit_radius(L, mu, k)      # real module function: minimum of U_eff
        ax.plot(rmin, Ueff(rmin), "o", color=col, ms=6)

    # bound-orbit energy line for L = 1.4: pick E between U_eff(min) and 0, mark turning points
    L = 1.4
    Ueff = effective_potential(U, L, mu)
    rmin = circular_orbit_radius(L, mu, k)
    E = 0.5 * Ueff(rmin)                             # negative -> bound; halfway up the well
    g = np.array([Ueff(ri) - E for ri in r])
    cross = r[:-1][(g[:-1] * g[1:] < 0)]            # turning points where U_eff = E
    ax.axhline(E, color=ALT, lw=1.3, ls="--", label=r"energy $E<0$")
    for rt in cross:
        ax.plot(rt, E, "v", color=ALT, ms=8)
    ax.axhline(0, color="#aaaaaa", lw=0.7)
    ax.set_ylim(-1.1, 0.6)
    ax.set_xlabel("radius $r$"); ax.set_ylabel(r"$U_{\rm eff}(r)$")
    ax.set_title(r"Effective potential: $U_{\rm eff}=-\frac{k}{r}+\frac{L^{2}}{2\mu r^{2}}$")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    _save(fig, "fig2_effective_potential.svg")
    caps["fig2_effective_potential.svg"] = (
        "The effective potential U_eff(r) = -k/r + L^2/(2 mu r^2) combines the attractive well with "
        "the centrifugal barrier. Its minimum (dots, from circular_orbit_radius) is the stable "
        "circular orbit. A negative energy level (dashed) cuts U_eff at two turning points -- the "
        "perihelion and aphelion between which a bound orbit oscillates in r.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
