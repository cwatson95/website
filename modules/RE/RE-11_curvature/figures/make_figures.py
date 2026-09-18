"""RE-11 figures — curvature: the Kretschmann invariant of Schwarzschild (true vs
coordinate singularity) and geodesic deviation (curvature focuses geodesics).

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
from curvature import (                            # noqa: E402
    kretschmann, geodesic_deviation,
    schwarzschild_metric, sphere_metric, minkowski_metric,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _deviation_curve(metric, x_of_lam, u, xi0, dl, n, comp):
    """Integrate D^2 xi/dlam^2 = geodesic_deviation, started parallel (xi'=0).
    Returns (lambda array, xi-component array)."""
    xi = list(xi0)
    xidot = [0.0] * len(xi0)
    lams, vals = [0.0], [xi0[comp]]
    for k in range(n):
        A = geodesic_deviation(metric, x_of_lam(k * dl), u, xi)
        xidot = [xidot[i] + A[i] * dl for i in range(len(xi))]
        xi = [xi[i] + xidot[i] * dl for i in range(len(xi))]
        lams.append((k + 1) * dl); vals.append(xi[comp])
    return np.array(lams), np.array(vals)


def main():
    caps = {}

    # Fig 1 — Kretschmann scalar K = 48 M^2/r^6 for Schwarzschild (M = 1).
    sch = schwarzschild_metric(1.0)
    r = np.linspace(2.05, 16.0, 60)
    K = np.array([kretschmann(sch, [0.0, float(ri), 1.2, 0.7]) for ri in r])
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(r, K, color=FLOW, lw=2, label=r"$K=R_{abcd}R^{abcd}$ (code)")
    ax.plot(r, 48.0 / r**6, color=INK, lw=1.0, ls="--", label=r"$48M^2/r^6$")
    ax.axvline(2.0, color=ALT, lw=1.4, ls=":")
    ax.text(2.15, K.max() * 0.25, "horizon\n$r=2M$\n(K finite)", color=ALT, fontsize=9)
    ax.annotate("singularity as $r\\to0$", xy=(2.05, K.max()), xytext=(5.5, K.max() * 0.7),
                arrowprops=dict(arrowstyle="->", color=INK), color=INK, fontsize=9)
    ax.set_yscale("log")
    ax.set_xlabel("areal radius  $r$  (units of $M$)")
    ax.set_ylabel(r"Kretschmann scalar  $K$")
    ax.set_title(r"Schwarzschild curvature: finite at $r=2M$, diverges at $r\to0$")
    ax.legend(loc="upper right", frameon=False)
    _save(fig, "fig1_kretschmann_schwarzschild.svg")
    caps["fig1_kretschmann_schwarzschild.svg"] = (
        "Kretschmann curvature invariant K = R_{abcd} R^{abcd} of the Schwarzschild metric "
        "(M=1) from the module's `kretschmann`, matching 48 M^2/r^6. K stays finite at the "
        "horizon r = 2M (a mere coordinate singularity, dotted) but diverges as r -> 0 -- the "
        "real, frame-invariant physical singularity.")

    # Fig 2 — geodesic deviation: positive curvature focuses parallel geodesics.
    xi0_mag = 0.30
    sph = sphere_metric(1.0)
    lam_s, xi_s = _deviation_curve(                 # sphere: equator, separated in theta
        sph, lambda lam: [math.pi / 2, lam], [0.0, 1.0], [xi0_mag, 0.0],
        dl=0.02, n=88, comp=0)
    mink = minkowski_metric()
    lam_f, xi_f = _deviation_curve(                 # flat: straight worldline, separated in y
        mink, lambda lam: [0.0, lam, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, xi0_mag, 0.0], dl=0.02, n=88, comp=2)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    # two neighbouring geodesics drawn at +/- xi/2 about a common fiducial line
    ax.plot(lam_s,  xi_s / 2, color=INK, lw=2)
    ax.plot(lam_s, -xi_s / 2, color=FLOW, lw=2)
    ax.fill_between(lam_s, -xi_s / 2, xi_s / 2, color=INK, alpha=0.06)
    ax.plot(lam_f,  xi_f / 2, color="#999999", lw=1.3, ls="--")
    ax.plot(lam_f, -xi_f / 2, color="#999999", lw=1.3, ls="--")
    # focal point where the sphere separation first reaches zero
    zc = np.where(np.diff(np.sign(xi_s)))[0]
    if len(zc):
        lf = lam_s[zc[0]]
        ax.plot(lf, 0, "o", color=ALT, ms=6, zorder=5)
        ax.annotate("focal point", xy=(lf, 0), xytext=(lf - 0.7, 0.10),
                    arrowprops=dict(arrowstyle="->", color=ALT), color=ALT, fontsize=9)
    ax.axhline(0, color="#cccccc", lw=0.6)
    sph_h = plt.Line2D([], [], color=INK, lw=2, label="sphere ($K>0$): converge")
    flat_h = plt.Line2D([], [], color="#999999", lw=1.3, ls="--", label="flat ($K=0$): parallel")
    ax.set_xlabel(r"affine parameter along the fiducial geodesic  $\lambda$")
    ax.set_ylabel(r"transverse separation  $\pm\,\xi/2$")
    ax.set_title("Geodesic deviation: curvature focuses initially-parallel geodesics")
    ax.legend(handles=[sph_h, flat_h], loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_geodesic_deviation_focusing.svg")
    caps["fig2_geodesic_deviation_focusing.svg"] = (
        "Two neighbouring geodesics that start parallel (zero relative velocity), with their "
        "separation evolved by integrating the module's `geodesic_deviation`. On the unit "
        "sphere (K>0) the separation follows cos(lambda) and the geodesics meet at a focal "
        "point a quarter-circle away; in flat Minkowski space (K=0) they stay parallel forever.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
