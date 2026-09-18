"""MA-15 figures — nascent delta sequences peaking up, and the sifting property.

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
from dirac_delta import (                           # noqa: E402
    gaussian_delta, simpson, sift,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    x = np.linspace(-2.0, 2.0, 1600)

    # Fig 1 — the nascent delta peaks up as a -> 0, area pinned at 1.
    # gaussian_delta(x,a) = e^{-(x/a)^2}/(a sqrt(pi)); its integral (the module's
    # own `simpson`) stays 1 while the spike grows taller and narrower.
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    for a, col in [(0.5, STEEL), (0.25, ALT), (0.12, FLOW), (0.06, INK)]:
        y = [gaussian_delta(xx, a) for xx in x]
        area = simpson(lambda t: gaussian_delta(t, a), -4.0, 4.0)
        ax.plot(x, y, color=col, lw=2,
                label=fr"$a={a}$,  $\int\delta_a=\,${area:.3f}")
    ax.set_xlim(-2, 2)
    ax.set_xlabel("$x$")
    ax.set_ylabel(r"$\delta_a(x)$")
    ax.set_title(r"Nascent delta $\delta_a(x)=\frac{1}{a\sqrt{\pi}}e^{-(x/a)^2}$: peaks up, area $=1$")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_nascent_peaking.svg")
    caps["fig1_nascent_peaking.svg"] = (
        r"The Gaussian nascent delta $\delta_a(x)=e^{-(x/a)^2}/(a\sqrt\pi)$ "
        r"(gaussian_delta) as the width $a$ shrinks: the spike grows taller and "
        r"narrower while its area stays pinned at $1$ (each $\int\delta_a\,dx$, computed "
        r"with the module's `simpson`, is shown). In the limit $a\to0$ it becomes the "
        r"Dirac $\delta$ — a distribution, not a function.")

    # Fig 2 — sifting: a narrowing spike at x0 samples phi there.
    # int delta_a(x-x0) phi(x) dx -> phi(x0)  (the module's `sift`).
    phi = lambda t: math.cos(t) + 0.3 * math.sin(2.0 * t)
    x0 = 1.2
    xs = np.linspace(-0.5, 3.6, 1400)

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(xs, [phi(t) for t in xs], color=INK, lw=2.2,
            label=r"$\phi(x)=\cos x+0.3\sin 2x$")
    ax.axhline(0, color="#cccccc", lw=0.6)
    ax.axvline(x0, color="#888888", lw=0.8, ls=":")
    ax.plot(x0, phi(x0), "o", color=INK, ms=6)
    ax.annotate(fr"$\phi(x_0)={phi(x0):.4f}$", xy=(x0, phi(x0)),
                xytext=(x0 + 0.12, phi(x0) + 0.18), color=INK, fontsize=9)

    ax2 = ax.twinx()                                        # spikes on their own scale
    lines2 = []
    for a, col in [(0.30, STEEL), (0.12, ALT), (0.05, FLOW)]:
        sp = [gaussian_delta(t - x0, a) for t in xs]
        val = sift(phi, x0, "gaussian", a)
        (ln,) = ax2.plot(xs, sp, color=col, lw=1.6,
                         label=fr"$a={a}$:  $\int\delta_a\phi={val:.4f}$")
        lines2.append(ln)
    ax2.set_ylim(bottom=0)
    ax2.set_ylabel(r"$\delta_a(x-x_0)$")
    ax.set_xlim(-0.5, 3.6)
    ax.set_xlabel("$x$")
    ax.set_ylabel(r"$\phi(x)$")
    ax.set_title(r"Sifting: the spike localizes at $x_0$ and samples $\phi(x_0)$")
    l1, lab1 = ax.get_legend_handles_labels()
    l2, lab2 = ax2.get_legend_handles_labels()
    ax.legend(l1 + l2, lab1 + lab2, loc="lower left", frameon=False, fontsize=8.5)
    _save(fig, "fig2_sifting.svg")
    caps["fig2_sifting.svg"] = (
        r"The sifting property $\int\delta_a(x-x_0)\,\phi(x)\,dx\to\phi(x_0)$. As the "
        r"nascent spike $\delta_a(x-x_0)$ (right axis) narrows toward $x_0=1.2$, the "
        r"weighted integral `sift` converges to $\phi(x_0)=0.5650$ (dot): the delta is "
        r"the linear functional that evaluates a test function at a point.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
