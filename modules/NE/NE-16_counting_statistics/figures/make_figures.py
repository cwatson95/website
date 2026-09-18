"""NE-16 figures -- the 1/sqrt(N) wall, background subtraction and detection
limits, optimal time allocation, and dead-time saturation.

Generates SVG figures into this `figures/` directory (plus captions.json), by
importing the module's own code in ../code. Run:  python3 make_figures.py
Convention shared by every module: matplotlib -> SVG (svg.fonttype='path' so the
text is portable vector outlines), saved next to a captions.json mapping each
filename to a one-line caption the browser renders under the figure.

Palette note: ALT and STEEL are indistinguishable under deuteranopia, so any
panel using both also varies linestyle or marker (modules/CHANGELOG.md Known-bad).
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
from counting_statistics import (                  # noqa: E402
    SIGMA_TABLE, relative_error, counts_for_relative_error,
    net_rate, net_rate_sigma, optimal_time_split,
    true_rate, observed_rate, max_rate_for_loss,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- the 1/sqrt(N) wall.
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    n = np.logspace(math.log10(20), 7, 400)   # the guard refuses below 20 counts
    ax.loglog(n, [100 * relative_error(x) for x in n], color=INK, lw=2.2)
    for counts, pct in sorted(SIGMA_TABLE.items()):
        ax.plot([counts], [pct], "o", color=FLOW, ms=7)
        ax.annotate("%d → %g%%" % (counts, pct), xy=(counts, pct),
                    xytext=(counts * 1.5, pct * 1.15), fontsize=8.5, color=FLOW)
    for target, lab in ((1.0, "1%"), (0.1, "0.1%")):
        need = counts_for_relative_error(target / 100)
        ax.axhline(target, color="0.85", lw=0.9, zorder=0)
        ax.annotate("%s needs %s counts" % (lab, format(int(need), ",")),
                    xy=(need, target), xytext=(60, target * 1.5),
                    fontsize=9, color=STEEL,
                    arrowprops=dict(arrowstyle="->", color=STEEL, lw=1.0))
    ax.set_xlabel("counts recorded")
    ax.set_ylabel("relative standard error (%)")
    ax.set_xlim(20, 1e7)
    ax.set_ylim(0.02, 30)
    ax.set_title("The $1/\\sqrt{N}$ wall (S&F Table 8.3)")
    _save(fig, "fig1_sqrt_n_wall.svg")
    caps["fig1_sqrt_n_wall.svg"] = (
        "Relative counting error against counts recorded (relative_error), with S&F Table 8.3 "
        "marked. This is the constraint that shapes every radiation measurement: 1% precision "
        "needs 10 000 counts and 0.1% needs a million, so halving an uncertainty costs four "
        "times the counting time. No improvement in electronics changes it -- the uncertainty "
        "is in the source, not the instrument.")

    # Fig 2 -- background subtraction and the detection limit.
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    t = 60.0
    bkg_rate = 8.0
    net = np.logspace(-2, 1.4, 300)
    for rb, col, ls in ((0.5, LEAF, "-"), (8.0, FLOW, "--"), (50.0, ALT, "-.")):
        rel = []
        for r in net:
            cg, cb = (r + rb) * t, rb * t
            rel.append(100 * net_rate_sigma(cg, t, cb, t) / r)
        ax.loglog(net, rel, color=col, lw=2.0, ls=ls,
                  label="background %g /s" % rb)
    ax.axhline(100, color=INK, ls=":", lw=1.4)
    ax.text(0.012, 130, "uncertainty = signal:\nno detection below here",
            fontsize=9, color=INK)
    ax.set_xlabel("net source rate (counts/s)")
    ax.set_ylabel("relative error on the net rate (%)")
    ax.set_xlim(1e-2, 25)
    ax.set_ylim(0.5, 5000)
    ax.legend(fontsize=9)
    ax.set_title("Subtracting a background always costs precision (60 s counts)")
    _save(fig, "fig2_background_limit.svg")
    caps["fig2_background_limit.svg"] = (
        "Relative uncertainty on a net source rate (net_rate_sigma) for three background "
        "levels, at a fixed 60 s counting time. Because a net rate is a difference, the "
        "background contributes its own full uncertainty and never cancels: a source at 0.3 "
        "counts/s on an 8 counts/s background is a 160% measurement even though each raw count "
        "is known to better than 5%. Where a curve crosses 100%, the uncertainty equals the "
        "signal -- that is the detection limit, and it moves right as the background rises.")

    # Fig 3 -- optimal time allocation.
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    ratio = np.logspace(-1, 3, 300)
    ax.semilogx(ratio, [optimal_time_split(r, 1.0) for r in ratio],
                color=INK, lw=2.2, label="optimal: $\\sqrt{r_g}/(\\sqrt{r_g}+\\sqrt{r_b})$")
    ax.axhline(0.5, color=STEEL, ls="--", lw=1.5, label="naive 50/50")
    for r, mk in ((1.0, "o"), (10.0, "s"), (100.0, "^")):
        f = optimal_time_split(r, 1.0)
        ax.plot([r], [f], mk, color=FLOW, ms=8)
        ax.annotate("%g:1 → %.0f%%" % (r, 100 * f), xy=(r, f),
                    xytext=(r * 1.3, f - 0.06), fontsize=9, color=FLOW)
    ax.set_xlabel("source rate / background rate")
    ax.set_ylabel("fraction of the time spent on the sample")
    ax.set_xlim(0.1, 1000)
    ax.set_ylim(0.2, 1.0)
    ax.legend(fontsize=9, loc="lower right")
    ax.set_title("How to split a fixed counting time")
    _save(fig, "fig3_time_split.svg")
    caps["fig3_time_split.svg"] = (
        "The optimal division of a fixed total counting time between sample and background "
        "(optimal_time_split), verified in the tests by direct numerical minimisation. The "
        "even split is only correct when the two rates are equal; for a source ten times "
        "background, 76% of the time belongs on the sample and an even split wastes about 10% "
        "of the attainable precision. Beyond S&F, which does not treat time allocation.")

    # Fig 4 -- dead time, and the saturation trap.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.8, 3.8))
    tau = 100e-6
    n_true = np.logspace(2, 6, 400)
    axL.loglog(n_true, [observed_rate(x, tau) for x in n_true], color=INK, lw=2.2)
    axL.loglog(n_true, n_true, color=STEEL, ls="--", lw=1.4, label="ideal (no dead time)")
    axL.axhline(1 / tau, color=FLOW, ls=":", lw=1.6)
    axL.annotate("ceiling $1/\\tau$ = %.0f /s" % (1 / tau), xy=(3e5, 1 / tau),
                 xytext=(2e3, 2.2e4), fontsize=9, color=FLOW,
                 arrowprops=dict(arrowstyle="->", color=FLOW, lw=1.0))
    axL.set_xlabel("true rate (counts/s)")
    axL.set_ylabel("observed rate (counts/s)")
    axL.legend(fontsize=8.5, loc="upper left")
    axL.set_title("A saturated detector reads the same\nfor any input")

    m = np.linspace(0, 0.62 / tau, 300)
    corr = []
    for mm in m:
        try:
            corr.append(100 * (true_rate(mm, tau) / mm - 1) if mm > 0 else 0.0)
        except (ValueError, ZeroDivisionError):
            corr.append(np.nan)
    axR.plot(m * tau, corr, color=INK, lw=2.2)
    axR.axvline(0.05, color=LEAF, ls="--", lw=1.5)
    axR.text(0.06, 60, "S&F: keep\n$m\\tau<0.05$", fontsize=9, color=LEAF)
    axR.axvline(0.5, color=ALT, ls=":", lw=1.6)
    axR.text(0.36, 20, "module\nrefuses\nbeyond here", fontsize=9, color=ALT)
    axR.set_xlabel("$m\\tau$ (fraction of time dead)")
    axR.set_ylabel("upward correction (%)")
    axR.set_xlim(0, 0.62)
    axR.set_ylim(0, 110)
    axR.set_title("The correction overtakes the measurement")
    fig.tight_layout()
    _save(fig, "fig4_dead_time.svg")
    caps["fig4_dead_time.svg"] = (
        "Left: the forward dead-time map m = n/(1+n tau) saturates at 1/tau, so a detector at "
        "saturation reports the same reading for any input above it -- a catastrophically "
        "intense field can read as a merely moderate one, which makes dead time a safety "
        "matter and not just a precision one. Right: the size of the correction from S&F "
        "Eq. (8.15). Past m*tau = 0.5 it exceeds the measurement itself and the answer is set "
        "by the assumed model rather than the data, so true_rate() raises there.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
