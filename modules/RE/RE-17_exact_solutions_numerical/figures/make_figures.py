"""RE-17 figures -- Kerr black-hole structure from the exact-solution code.

The module's design hint mentions geodesic orbits / effective potentials, but
RE-17's actual code provides the Kerr / Reissner-Nordstrom / de Sitter metrics,
field-equation validators, and the Kerr horizon & ergosphere functions -- there
is no geodesic integrator. So the figures illustrate the real API:
  1. the Kerr ergosphere and horizon in the poloidal plane, from the actual
     `kerr_ergosphere` and `kerr_horizons`;
  2. the inner/outer horizons and the equatorial static limit vs spin a, showing
     the horizons merge at the extremal limit a = M.
Run:  python3 make_figures.py
Convention (shared by every module): matplotlib -> SVG with svg.fonttype='path'
so text ships as portable vector outlines, saved next to a captions.json.
"""
import json
import os
import sys
import math

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"      # text as vector paths (portable)
matplotlib.rcParams["font.size"] = 11
import matplotlib.pyplot as plt                    # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from exact_solutions import kerr_horizons, kerr_ergosphere   # noqa: E402

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- Kerr ergosphere & horizon in the poloidal (x, z) plane, a = 0.9 M.
    M, a = 1.0, 0.9
    r_minus, r_plus = kerr_horizons(M, a)
    th = np.linspace(0.0, math.pi, 240)
    rE = np.array([kerr_ergosphere(M, a, t) for t in th])
    # (r, theta) -> (x = r sin theta, z = r cos theta); mirror to -x for the slice.
    xE, zE = rE * np.sin(th), rE * np.cos(th)
    xh, zh = r_plus * np.sin(th), r_plus * np.cos(th)
    xi, zi = r_minus * np.sin(th), r_minus * np.cos(th)

    def ring(x, z):
        return np.concatenate([x, -x[::-1]]), np.concatenate([z, z[::-1]])

    ex, ez = ring(xE, zE)
    hx, hz = ring(xh, zh)
    ix, iz = ring(xi, zi)

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.fill(ex, ez, color=FLOW, alpha=0.18)
    ax.fill(hx, hz, color=INK, alpha=0.30)
    ax.plot(ex, ez, color=FLOW, lw=2.2, label=r"static limit (ergosphere)")
    ax.plot(hx, hz, color=INK, lw=2.0, label=r"outer horizon $r_+$")
    ax.plot(ix, iz, color=STEEL, lw=1.4, ls="--", label=r"inner horizon $r_-$")
    ax.axvline(0.0, color="#cccccc", lw=0.6, ls=":")
    ax.set_aspect("equal")
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.4, 2.4)
    ax.set_xlabel(r"cylindrical radius $x/M$")
    ax.set_ylabel(r"$z/M$  (spin axis)")
    ax.set_title(r"Kerr ($a=0.9\,M$): ergosphere bulges outside the horizon")
    ax.legend(loc="upper right", frameon=False, fontsize=8)
    _save(fig, "fig1_kerr_ergosphere.svg")
    caps["fig1_kerr_ergosphere.svg"] = (
        "Poloidal cross-section of a Kerr black hole at spin a = 0.9 M, drawn from "
        "kerr_ergosphere and kerr_horizons. The static-limit surface (ergosphere, "
        "orange) reaches r = 2M at the equator but touches the outer horizon r_plus "
        "(blue) at the poles; the gap between them is the ergoregion, where frame "
        "dragging forbids any static observer. The dashed inner horizon r_minus sits "
        "inside.")

    # Fig 2 -- horizon radii and the equatorial static limit vs spin a.
    a_arr = np.linspace(0.0, 1.0, 300)
    rp, rm = [], []
    for av in a_arr:
        lo, hi = kerr_horizons(M, av)
        rm.append(lo); rp.append(hi)
    rp, rm = np.array(rp), np.array(rm)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.fill_between(a_arr, rp, 2.0, color=FLOW, alpha=0.15)
    ax.plot(a_arr, rp, color=INK, lw=2.2, label=r"outer horizon $r_+$")
    ax.plot(a_arr, rm, color=STEEL, lw=2.0, label=r"inner horizon $r_-$")
    ax.axhline(2.0, color=FLOW, lw=2.0, ls="--",
               label=r"static limit $r_E=2M$ (equator)")
    ax.axvline(1.0, color="#aaaaaa", lw=1.0, ls=":")
    ax.text(0.55, 0.45, "ergoregion\n(equatorial)", color="#9a6b30", fontsize=9)
    ax.set_xlim(0.0, 1.05)
    ax.set_ylim(0.0, 2.2)
    ax.set_xlabel(r"spin  $a/M$")
    ax.set_ylabel(r"radius  $r/M$")
    ax.set_title(r"Kerr horizons merge at the extremal limit $a=M$")
    ax.legend(loc="center left", frameon=False, fontsize=9)
    _save(fig, "fig2_kerr_horizons.svg")
    caps["fig2_kerr_horizons.svg"] = (
        "Kerr horizon radii vs spin from kerr_horizons: the outer horizon r_plus "
        "shrinks and the inner horizon r_minus grows with spin until they meet at "
        "r = M for the extremal black hole a = M (beyond which kerr_horizons raises -- "
        "a naked singularity). The equatorial static limit stays at r_E = 2M "
        "(kerr_ergosphere), so the shaded equatorial ergoregion opens up as the hole "
        "spins.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
