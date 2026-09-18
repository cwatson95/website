"""ST-16 figures — transformations of random variables: the change-of-variables
(Jacobian) density of Y=g(X) checked against a histogram of transformed samples,
and a sum of independents as a convolution.

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
from transformations import (                      # noqa: E402
    uniform_pdf, exp_pdf, change_of_variables_1d, convolution,
    triangular_pdf, sum_two_uniforms_pdf,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    rng = np.random.default_rng(7)
    caps = {}

    # Fig 1 — change of variables: X ~ U(0,1), Y = -ln(X) ~ Exp(1).  The Jacobian
    # formula f_Y = f_X(g^{-1}(y)) |dx/dy| (module fn) vs a histogram of samples.
    u = rng.uniform(0.0, 1.0, 6000)
    y_samp = -np.log(u)                              # transformed samples
    yy = np.linspace(0.0, 6.0, 240)
    ginv = lambda yv: math.exp(-yv)                  # x = g^{-1}(y) = e^{-y}
    dxdy = lambda yv: -math.exp(-yv)                 # dx/dy (signed)
    f_jac = np.array([change_of_variables_1d(uniform_pdf, ginv, dxdy, float(v))
                      for v in yy])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.hist(y_samp, bins=40, range=(0.0, 6.0), density=True, color=STEEL,
            alpha=0.35, edgecolor="white", lw=0.4, label="samples $-\\ln X$")
    ax.plot(yy, f_jac, color=FLOW, lw=2.4,
            label=r"$f_Y=f_X(g^{-1}(y))\,|dx/dy|$")
    ax.plot(yy, exp_pdf(yy, 1.0), color=INK, lw=1.5, ls="--",
            label=r"target $\mathrm{Exp}(1)$")
    ax.set_xlim(0, 6); ax.set_xlabel("$y$"); ax.set_ylabel("density")
    ax.set_title(r"Change of variables: $Y=-\ln X$ for $X\sim U(0,1)$")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig1_change_of_variables.svg")
    caps["fig1_change_of_variables.svg"] = (
        "Transforming X ~ U(0,1) by Y = -ln(X). The change-of-variables density "
        "f_Y(y) = f_X(g^{-1}(y)) |dx/dy| (orange) lands exactly on the Exp(1) target "
        "(dashed) and on a histogram of transformed samples, confirming the Jacobian "
        "formula.")

    # Fig 2 — sum of two independents as a convolution: U(0,1)+U(0,1) is Triangular.
    z_samp = rng.uniform(0.0, 1.0, 6000) + rng.uniform(0.0, 1.0, 6000)
    zz = np.linspace(0.0, 2.0, 240)
    f_conv = np.array([convolution(uniform_pdf, uniform_pdf, float(z), 0.0, 1.0)
                       for z in zz])

    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.hist(z_samp, bins=40, range=(0.0, 2.0), density=True, color=STEEL,
            alpha=0.35, edgecolor="white", lw=0.4, label="samples $X_1+X_2$")
    ax.plot(zz, f_conv, color=FLOW, lw=2.4,
            label=r"$\int f_X(t)f_Y(z-t)\,dt$ (convolution)")
    ax.plot(zz, triangular_pdf(zz), color=INK, lw=1.5, ls="--",
            label="closed form: triangular")
    ax.set_xlim(0, 2); ax.set_xlabel("$z$"); ax.set_ylabel("density")
    ax.set_title(r"Sum of independents = convolution: $U(0,1)+U(0,1)$")
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    _save(fig, "fig2_convolution_sum.svg")
    caps["fig2_convolution_sum.svg"] = (
        "The density of a sum of independent variables is the convolution of their "
        "densities. For two Uniform(0,1) terms the convolution integral (orange) gives "
        "the triangular law on [0,2] (dashed closed form), matching a histogram of "
        "sampled sums.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
