"""NE-06 figures -- exponential decay on linear and log axes, specific activity
against half-life, the mean-vs-median gap, and competing channels.

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
from decay_kinetics import (                       # noqa: E402
    LN2, SECONDS_PER, load_half_lives, specific_activity, curies,
    fraction_remaining, decay_time_pdf, mean_lifetime, decay_constant,
    branching_fractions, half_life,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"
YEAR = SECONDS_PER["y"]


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}
    hl = load_half_lives()

    # Fig 1 -- the exponential, linear and semilog.
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.3))
    n = np.linspace(0, 6, 300)
    f = 2.0 ** (-n)
    ax1.plot(n, f, color=INK, lw=1.8)
    for k in range(1, 5):
        ax1.plot([k, k], [0, 2.0 ** -k], ":", color="0.6", lw=1.0)
        ax1.plot([0, k], [2.0 ** -k, 2.0 ** -k], ":", color="0.6", lw=1.0)
        ax1.text(k + 0.08, 2.0 ** -k + 0.02, "$2^{-%d}$" % k, fontsize=8.5, color="0.35")
    ax1.set_xlabel("time (half-lives)")
    ax1.set_ylabel("$N/N_0$")
    ax1.set_title("linear", fontsize=10)
    ax2.semilogy(n, f, color=INK, lw=1.8)
    ax2.set_xlabel("time (half-lives)")
    ax2.set_title("semilog: a straight line of slope $-\\lambda$", fontsize=10)
    ax2.set_ylim(1e-2, 1.4)
    fig.suptitle("Exponential decay", y=1.02)
    _save(fig, "fig1_exponential.svg")
    caps["fig1_exponential.svg"] = (
        "Surviving fraction against time in units of the half-life (fraction_remaining). "
        "On a logarithmic axis the exponential is a straight line whose slope is -lambda, "
        "which is how a half-life is read off measured count-rate data without knowing the "
        "sample size or detector efficiency.")

    # Fig 2 -- specific activity spans ten decades.
    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    picks = [("3H", 3), ("60Co", 60), ("90Sr", 90), ("137Cs", 137), ("131I", 131),
             ("14C", 14), ("226Ra", 226), ("239Pu", 239), ("235U", 235), ("238U", 238),
             ("40K", 40), ("32P", 32), ("99Mo", 99)]
    xs, ys, labels = [], [], []
    for nuc, A in picks:
        if nuc not in hl or not math.isfinite(hl[nuc]):
            continue
        xs.append(hl[nuc] / YEAR)
        ys.append(curies(specific_activity(hl[nuc], A)))
        labels.append(nuc)
    ax.loglog(xs, ys, "o", color=STEEL, ms=6)
    for x, y, lab in zip(xs, ys, labels):
        ax.annotate(lab, xy=(x, y), xytext=(x * 1.5, y * 1.4), fontsize=8.5, color=INK)
    grid = np.logspace(-4, 11, 50)
    ax.loglog(grid, curies(LN2 * 6.0221415e23 / 100.0 / (grid * YEAR)), "--",
              color="0.65", lw=1.0, label=r"$\propto 1/T_{1/2}$  (at $A=100$)")
    ax.set_xlabel("half-life (years)")
    ax.set_ylabel("specific activity (Ci/g)")
    ax.set_title("Short-lived means intensely radioactive")
    ax.legend(frameon=False, fontsize=9, loc="lower left")
    _save(fig, "fig2_specific_activity.svg")
    caps["fig2_specific_activity.svg"] = (
        "Specific activity against half-life for thirteen nuclides (specific_activity), "
        "both axes logarithmic. The inverse proportionality spans ten orders of magnitude "
        "from tritium to 238U: activity and longevity are the same parameter read two ways, "
        "which is the central trade-off in waste management.")

    # Fig 3 -- mean vs median.
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    T = 1.0
    lam = decay_constant(T)
    t = np.linspace(0, 5, 400)
    p = np.array([decay_time_pdf(x, lam=lam) for x in t])
    ax.plot(t, p, color=INK, lw=1.8)
    ax.fill_between(t, 0, p, where=(t <= T), color=STEEL, alpha=0.3)
    ax.axvline(T, color=FLOW, lw=1.5)
    ax.axvline(mean_lifetime(t_half=T), color=LEAF, lw=1.5, ls="--")
    ax.annotate("half-life\n(median): 1.00", xy=(T, 0.45), xytext=(T + 0.25, 0.55),
                fontsize=9, color=FLOW, arrowprops=dict(arrowstyle="->", color=FLOW))
    ax.annotate("mean life: 1.44", xy=(mean_lifetime(t_half=T), 0.22),
                xytext=(2.1, 0.32), fontsize=9, color=LEAF,
                arrowprops=dict(arrowstyle="->", color=LEAF))
    ax.text(0.42, 0.12, "half the\nnuclei", fontsize=8.5, color="0.25", ha="center")
    ax.set_xlabel("decay time (half-lives)")
    ax.set_ylabel("$p(t)$")
    ax.set_title(r"The mean life is $1/\ln 2 = 1.44$ half-lives")
    _save(fig, "fig3_mean_vs_median.svg")
    caps["fig3_mean_vs_median.svg"] = (
        "Decay-time probability density lambda exp(-lambda t) (decay_time_pdf). The "
        "half-life is the median -- shaded area one half -- while the mean sits 44% later, "
        "pulled right by the unbounded tail. The two are routinely confused; they differ by "
        "a factor 1/ln2 for every exponential process.")

    # Fig 4 -- competing channels.
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    lam_b, lam_ec = 0.8928, 0.1072
    fr = branching_fractions([lam_b, lam_ec])
    t = np.linspace(0, 4, 300)
    tot = np.exp(-(lam_b + lam_ec) * t)
    ax.plot(t, tot, color=INK, lw=2.0, label=r"total: $\lambda=\lambda_1+\lambda_2$")
    ax.plot(t, np.exp(-lam_b * t), "--", color=FLOW, lw=1.3,
            label=r"$\beta^-$ alone ($f=%.3f$)" % fr[0])
    ax.plot(t, np.exp(-lam_ec * t), "--", color=LEAF, lw=1.3,
            label=r"EC alone ($f=%.3f$)" % fr[1])
    ax.axhline(0.5, color="0.7", lw=1.0, ls=":")
    ax.set_xlabel(r"time ($1/\lambda_{\rm tot}$ units scaled to $^{40}$K branches)")
    ax.set_ylabel("$N/N_0$")
    ax.set_ylim(0, 1.05)
    ax.set_title(r"Competing channels: rates add, so the total decays fastest")
    ax.legend(frameon=False, fontsize=9)
    _save(fig, "fig4_competing_channels.svg")
    caps["fig4_competing_channels.svg"] = (
        "Survival curves for the two 40K channels separately and combined "
        "(total_decay_constant, branching_fractions). Because independent channels add "
        "their rates, the observed decay is faster than either branch alone -- so a partial "
        "half-life is always longer than the measured one and is never directly observable.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
