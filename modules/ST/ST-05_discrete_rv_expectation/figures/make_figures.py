"""ST-05 figures -- discrete random variables & expectation.

Two SVG figures (+ captions.json) built from the module's own code in ../code:
  fig1 -- a skewed pmf with the mean marked as the balance point (E, Var, sigma);
  fig2 -- the cdf F(x)=P(X<=x) of the same law, a right-continuous staircase to 1.
Run:  python3 make_figures.py
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"
matplotlib.rcParams["font.size"] = 11
import matplotlib.pyplot as plt                    # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from discrete_rv_expectation import (              # noqa: E402
    expectation, variance, std, pmf_is_valid, cdf_table,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    values = np.array([0., 1., 2., 3., 4., 5., 6., 7.])
    probs = np.array([0.30, 0.25, 0.18, 0.12, 0.08, 0.04, 0.02, 0.01])
    assert pmf_is_valid(values, probs)
    mu = expectation(values, probs)
    var = variance(values, probs)
    sd = std(values, probs)

    # Fig 1 -- pmf bars + mean as the balance point (fulcrum).
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.bar(values, probs, color=INK, width=0.7, zorder=2)
    ax.axvspan(mu - sd, mu + sd, color=STEEL, alpha=0.16, zorder=0,
               label=r"$\mu\pm\sigma$")
    ax.axvline(mu, color=FLOW, lw=2, zorder=3, label=fr"$\mu=E[X]={mu:.2f}$")
    ax.plot([mu], [0], marker="^", ms=14, color=FLOW, clip_on=False, zorder=4)
    ax.set_xlabel(r"value $x$"); ax.set_ylabel(r"$f(x)=P(X=x)$")
    ax.set_ylim(0, 0.34)
    ax.set_title("Expectation is the balance point of the pmf")
    ax.legend(loc="upper right", frameon=False)
    ax.text(0.60, 0.60, fr"$\sigma^{{2}}=\mathrm{{Var}}(X)={var:.2f}$" + "\n" +
            fr"$\sigma={sd:.2f}$", transform=ax.transAxes, fontsize=10, color=INK)
    _save(fig, "fig1_pmf_balance_point.svg")
    caps["fig1_pmf_balance_point.svg"] = (
        "A right-skewed pmf f(x)=P(X=x). The mean mu = E[X] = sum x f(x) = 1.68 (orange "
        "line and triangular fulcrum) is the balance point or centre of mass of the bars, "
        "pulled right of the mode by the long tail. The shaded band is mu +/- sigma, with "
        "variance Var(X) = 2.72.")

    # Fig 2 -- the cdf staircase F(x)=P(X<=x).
    xs, cum = cdf_table(values, probs)
    xx = np.concatenate(([xs[0] - 1.0], xs))
    yy = np.concatenate(([0.0], cum))
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.step(xx, yy, where="post", color=INK, lw=2)
    ax.plot(xs, cum, "o", color=FLOW, zorder=3)
    ax.axhline(1.0, color="#aaaaaa", lw=0.8, ls="--")
    ax.set_xlabel(r"value $x$"); ax.set_ylabel(r"$F(x)=P(X\leq x)$")
    ax.set_ylim(0, 1.08); ax.set_xlim(xs[0] - 1.0, xs[-1] + 1.0)
    ax.set_title(r"The cdf: a right-continuous staircase rising to $1$")
    _save(fig, "fig2_cdf_staircase.svg")
    caps["fig2_cdf_staircase.svg"] = (
        "The cumulative distribution F(x)=P(X<=x) of the same variable: a right-continuous "
        "staircase that starts at 0, jumps by f(x_i) at each support point (dots mark the "
        "value attained at the jump), and rises to exactly 1.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
