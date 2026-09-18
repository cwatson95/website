"""EM-16 figures -- waveguide dispersion and phase/group velocities.

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
from waveguides import (                           # noqa: E402
    cutoff_angular_frequency, guide_wavenumber,
    phase_velocity_guide, group_velocity_guide, tem_line_speed, C,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"
TWO_PI = 2.0 * np.pi


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    a, b = 0.0229, 0.0102                          # WR-90 X-band guide (metres)

    # Fig 1 -- dispersion f(k) for several modes, with the light line.
    modes = [(1, 0, INK), (2, 0, FLOW), (0, 1, STEEL), (1, 1, ALT)]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    kmax = 0.0
    for (m, n, col) in modes:
        w_co = cutoff_angular_frequency(m, n, a, b)
        w = np.linspace(w_co * 1.0001, w_co * 3.5, 250)
        k = np.array([guide_wavenumber(wi, w_co) for wi in w])
        kmax = max(kmax, k.max())
        ax.plot(k, w / TWO_PI / 1e9, color=col, lw=2.0,
                label=r"TE$_{%d%d}$  ($f_c{=}%.1f$ GHz)" % (m, n, w_co / TWO_PI / 1e9))
        ax.plot(0.0, w_co / TWO_PI / 1e9, "o", color=col, ms=4)
    kline = np.linspace(0.0, kmax, 50)
    ax.plot(kline, C * kline / TWO_PI / 1e9, color="#999999", lw=1.3, ls=":",
            label=r"light line $\omega=ck$")
    ax.set_xlabel(r"guide wavenumber $k$  [rad/m]")
    ax.set_ylabel(r"frequency $f=\frac{\omega}{2\pi}$  [GHz]")
    ax.set_title("Waveguide dispersion: each mode has a cutoff")
    ax.set_xlim(left=0)
    ax.legend(loc="lower right", frameon=False, fontsize=8.5)
    _save(fig, "fig1_dispersion.svg")
    caps["fig1_dispersion.svg"] = (
        "Dispersion of a WR-90 rectangular guide from cutoff_angular_frequency and "
        "guide_wavenumber. Each TE mode rises from its cutoff frequency fc at k=0 "
        "(dots) and bends toward the light line omega=ck (dotted) at high frequency. "
        "Below its cutoff a mode cannot propagate.")

    # Fig 2 -- phase and group velocity of the dominant TE10 mode vs frequency.
    w_co = cutoff_angular_frequency(1, 0, a, b)
    r = np.linspace(1.001, 5.0, 400)               # omega / omega_co
    w = r * w_co
    vp = np.array([phase_velocity_guide(wi, w_co) for wi in w]) / C
    vg = np.array([group_velocity_guide(wi, w_co) for wi in w]) / C
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.plot(r, vp, color=INK, lw=2.2, label=r"$v_{\mathrm{phase}}/c$  ($>1$)")
    ax.plot(r, vg, color=FLOW, lw=2.2, label=r"$v_{\mathrm{group}}/c$  ($<1$)")
    ax.plot(r, vp * vg, color=ALT, lw=1.6, ls="--",
            label=r"$v_p v_g/c^{2}=1$")
    ax.axhline(tem_line_speed() / C, color="#999999", lw=1.2, ls=":",
               label=r"TEM line $=c$")
    ax.set_xlabel(r"$\omega/\omega_{\mathrm{co}}$")
    ax.set_ylabel(r"velocity / $c$")
    ax.set_title(r"Above cutoff: $v_{\mathrm{phase}}>c>v_{\mathrm{group}}$,  $v_pv_g=c^{2}$")
    ax.set_ylim(0, 4)
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_velocities.svg")
    caps["fig2_velocities.svg"] = (
        "Phase and group velocity of the dominant TE10 mode versus drive frequency, "
        "from phase_velocity_guide and group_velocity_guide. The phase velocity "
        "exceeds c while the group (signal) velocity stays below c; their product is "
        "exactly c^{2} (purple dashed). A TEM line has no cutoff and carries every "
        "frequency at c (dotted).")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
