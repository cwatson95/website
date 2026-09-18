"""RE-16 figures -- the two polarizations on a ring, and the inspiral chirp.

Two SVG figures (+captions.json) built from RE-16's OWN code in ../code:
  1. a ring of free test masses deformed by the plus and cross polarizations,
     using `unit_ring` and `ring_response` (the geodesic-deviation displacement);
  2. the binary-inspiral chirp waveform h(t), built by integrating the real
     quadrupole-order `chirp_rate` (with `chirp_mass`) so the frequency and
     amplitude rise toward merger.
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
from gravitational_waves import (                  # noqa: E402
    unit_ring, ring_response, chirp_mass, chirp_rate,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def _closed(points):
    xs = [p[0] for p in points] + [points[0][0]]
    ys = [p[1] for p in points] + [points[0][1]]
    return np.array(xs), np.array(ys)


def main():
    caps = {}

    # Fig 1 -- a ring of test masses under the + and x polarizations (phase = 0,
    # peak amplitude). Amplitude exaggerated so the deformation is visible.
    amp = 0.45
    ring = unit_ring(240)
    cx, cy = _closed(ring)
    fig, axes = plt.subplots(1, 2, figsize=(6.2, 3.5))
    for ax, (hp, hx, col, title) in zip(axes, (
        (amp, 0.0, INK,  r"plus  $h_+$"),
        (0.0, amp, FLOW, r"cross  $h_{\times}$"),
    )):
        dx, dy = _closed(ring_response(hp, hx, 0.0, ring))
        ax.plot(cx, cy, color="#bbbbbb", lw=1.0, ls="--", label="undeformed")
        ax.plot(dx, dy, color=col, lw=2.2, label="deformed")
        masses = ring_response(hp, hx, 0.0, ring[::20])
        ax.scatter([p[0] for p in masses], [p[1] for p in masses],
                   color=col, s=16, zorder=3)
        ax.set_aspect("equal")
        ax.set_xlim(-1.7, 1.7)
        ax.set_ylim(-1.7, 1.7)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(title)
    axes[0].legend(loc="lower center", frameon=False, fontsize=8,
                   bbox_to_anchor=(0.5, -0.18))
    fig.suptitle("A gravitational wave shears a ring of free test masses",
                 fontsize=11)
    _save(fig, "fig1_ring_polarizations.svg")
    caps["fig1_ring_polarizations.svg"] = (
        "A ring of free test masses (unit_ring) displaced by ring_response at peak "
        "phase. The plus polarization (left) stretches x while squeezing y along the "
        "coordinate axes; the cross polarization (right) is the same pattern rotated "
        "45 degrees onto the diagonals. The amplitude is exaggerated for visibility, "
        "and the deformation is area-preserving because the wave is traceless.")

    # Fig 2 -- inspiral chirp: integrate df/dt = chirp_rate(f, Mc) and accumulate
    # the phase. Geometric stepping in f keeps the waveform smooth and avoids the
    # finite-time (merger) singularity.
    Mc = chirp_mass(36.0, 29.0)                     # GW150914-like, in solar masses
    f0 = 1.2e-4
    fmax = 8.0 * f0
    alpha = 0.0015
    f, t, phase = f0, 0.0, 0.0
    ts, hs, env = [0.0], [1.0], [1.0]
    while f < fmax and len(ts) < 200000:
        fdot = chirp_rate(f, Mc)
        dt = alpha * f / fdot
        phase += 2.0 * math.pi * f * dt
        t += dt
        f += fdot * dt
        a = (f / f0) ** (2.0 / 3.0)                 # amplitude grows as f^(2/3)
        ts.append(t); hs.append(a * math.cos(phase)); env.append(a)
    tau = np.array(ts) / ts[-1]                     # normalise time to merger
    env = np.array(env)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(tau, env, color=FLOW, lw=1.2, ls="--")
    ax.plot(tau, -env, color=FLOW, lw=1.2, ls="--", label=r"envelope $\propto f^{2/3}$")
    ax.plot(tau, hs, color=INK, lw=1.4, label=r"strain $h(t)$")
    ax.set_xlim(0.0, 1.0)
    ax.set_xlabel("time  (0 = early inspiral,  1 = merger)")
    ax.set_ylabel("strain $h$  (arb.)")
    ax.set_title(r"Binary-inspiral chirp:  $36+29\,M_\odot$,  rising $f$ and $h$")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    _save(fig, "fig2_inspiral_chirp.svg")
    caps["fig2_inspiral_chirp.svg"] = (
        "Inspiral strain h(t) obtained by integrating the quadrupole-order chirp_rate "
        "df/dt = (96/5) pi^(8/3) Mc^(5/3) f^(11/3) for a 36 + 29 solar-mass binary "
        "(chirp_mass Mc). As the binary tightens the frequency sweeps up and the "
        "amplitude grows like f^(2/3) (dashed envelope), producing the characteristic "
        "chirp that ends at merger.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE,
          "  (chirp samples:", len(ts), ", cycles:", round(phase / (2 * math.pi), 1), ")")


if __name__ == "__main__":
    main()
