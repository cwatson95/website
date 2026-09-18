"""NE-20 figures -- what delayed neutrons buy, the prompt-critical cliff, the
step-response prompt jump, and the post-shutdown xenon peak.

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
from reactor_kinetics import (                     # noqa: E402
    BETA, SIGMA_A_XE135_B, LAMBDA_X, mean_precursor_lifetime,
    small_insertion_period, asymptotic_period, prompt_jump_factor,
    simple_period, solve_point_kinetics, iodine_xenon_equilibrium,
    xenon_reactivity, poison_reactivity, promethium_samarium_equilibrium,
    beta_total, decay_constants, relative_yields,
)

INK, FLOW, ALT, STEEL, LEAF = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a", "#4f7a4f"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- what 0.65% of the neutrons buy.
    fig, ax = plt.subplots(figsize=(6.9, 4.2))
    t = np.linspace(0, 3, 300)
    tp = simple_period(0.001, 1e-4)
    td = BETA["235U"] * mean_precursor_lifetime() / 0.001
    ax.semilogy(t, np.exp(t / tp), color=FLOW, lw=2.4,
                label="prompt only ($T$ = %.2f s)" % tp)
    ax.semilogy(t, np.exp(t / td), color=INK, lw=2.4,
                label="with delayed neutrons ($T$ = %.0f s)" % td)
    ax.axhline(1.0, color="0.85", lw=1.0, zorder=0)
    ax.annotate("$\\times$22 000 in one second", xy=(1.0, math.exp(1 / tp)),
                xytext=(1.25, 3e3), fontsize=9, color=FLOW,
                arrowprops=dict(arrowstyle="->", color=FLOW, lw=1.0))
    ax.annotate("$\\times$1.012 in one second", xy=(1.0, math.exp(1 / td)),
                xytext=(1.3, 3.0), fontsize=9, color=INK,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
    ax.set_xlabel("time after a $\\delta k = 0.001$ insertion (s)")
    ax.set_ylabel("$n(t)/n_0$")
    ax.set_ylim(0.8, 1e13)
    ax.legend(fontsize=9, loc="upper left")
    ax.set_title("0.65% of the neutrons make reactors possible")
    _save(fig, "fig1_why_delayed_neutrons.svg")
    caps["fig1_why_delayed_neutrons.svg"] = (
        "S&F Eqs. (10.29) and (10.34): the same reactor and the same 0.1% increase in k_eff, "
        "under two models. If every fission neutron appeared promptly, the 1e-4 s cycle would "
        "multiply the population 22 000-fold in one second and no operator or control system "
        "could act in time. Because 0.65% of them are delayed by seconds to minutes, the "
        "effective generation time is beta*tau = 0.084 s instead of 1e-4 s, the period is 84 s, "
        "and the same insertion is a 1.2% rise. Every reactor ever built runs in the narrow "
        "band where that small delayed fraction still controls the answer.")

    # Fig 2 -- the prompt-critical cliff.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.0))
    kd = np.concatenate([np.linspace(0.005, 0.98, 300), np.linspace(1.02, 5, 200)])
    axL.loglog(kd, [asymptotic_period(k, 1e-4) for k in kd], color=INK, lw=2.4,
               label="exact (inhour eq.)")
    ksmall = np.linspace(0.005, 1.0, 200)
    axL.loglog(ksmall, [mean_precursor_lifetime() / k for k in ksmall],
               color=FLOW, lw=1.8, ls="--", label="$T=\\tau/k(\\$)$  Eq. (10.33)")
    axL.axvline(1.0, color=ALT, lw=1.8, ls=":")
    axL.annotate("prompt\ncritical", xy=(1.05, 30), fontsize=9, color=ALT)
    axL.plot([0.1], [asymptotic_period(0.1, 1e-4)], "o", color=LEAF, ms=8)
    axL.annotate("Ex. 10.12 uses 128 s here;\nthe exact value is 98 s",
                 xy=(0.1, asymptotic_period(0.1, 1e-4)), xytext=(0.012, 4.0),
                 fontsize=8.5, color=LEAF,
                 arrowprops=dict(arrowstyle="->", color=LEAF, lw=1.0))
    axL.set_xlabel("reactivity $k(\\$)$")
    axL.set_ylabel("asymptotic period (s)")
    axL.legend(fontsize=8.5, loc="lower left")
    axL.set_title("Three decades of period across\none decade of reactivity")

    kneg = np.logspace(math.log10(0.05), 2, 300)
    axR.semilogx(kneg, [asymptotic_period(-k, 1e-4) for k in kneg], color=INK, lw=2.4)
    floor = -55.7 / math.log(2.0)
    axR.axhline(floor, color=ALT, ls="--", lw=1.6)
    axR.annotate("$-80.4$ s floor: the 55.7 s precursor group",
                 xy=(3.0, floor), xytext=(0.09, -140), fontsize=9, color=ALT,
                 arrowprops=dict(arrowstyle="->", color=ALT, lw=1.0))
    axR.set_xlabel("negative reactivity inserted, $|k(\\$)|$")
    axR.set_ylabel("asymptotic period (s)")
    axR.set_ylim(-200, 0)
    axR.set_title("Shutdown has a speed limit")
    fig.tight_layout()
    _save(fig, "fig2_prompt_critical_cliff.svg")
    caps["fig2_prompt_critical_cliff.svg"] = (
        "Left: the asymptotic period from the exact inhour equation (10.39), against S&F's "
        "small-insertion approximation T = tau/k($). The approximation needs omega << the "
        "smallest decay constant, i.e. T >> 80 s, and it is already 32% high at the 0.1$ of "
        "Example 10.12. Above 1$ -- prompt critical -- the delayed neutrons are no longer "
        "needed and the period collapses onto the prompt lifetime, falling three orders of "
        "magnitude. That cliff is why reactivity is measured in dollars. Right: the same "
        "equation for negative insertions. However hard you scram, the power cannot fall faster "
        "than -80.4 s per e-fold, set by the 55.7 s precursor group -- which is why decay-heat "
        "removal is not optional.")

    # Fig 3 -- point kinetics transients, and the prompt jump.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.0))
    for k, col, ls in ((0.5, INK, "-"), (0.2, FLOW, "--"), (-0.5, LEAF, "-."),
                       (-2.0, STEEL, ":")):
        sol = solve_point_kinetics(lambda t, k=k: k * BETA["235U"], 1e-4, 60.0,
                                   dt=2e-4)
        ts = [p[0] for p in sol]
        ns = [p[1] for p in sol]
        axL.semilogy(ts, ns, color=col, lw=2.0, ls=ls, label="%+.1f\\$" % k)
    axL.axhline(1.0, color="0.85", lw=1.0, zorder=0)
    axL.set_xlabel("time after the step (s)")
    axL.set_ylabel("$n(t)/n_0$")
    axL.legend(fontsize=8.5, title="insertion", title_fontsize=8.5)
    axL.set_title("Point kinetics, six groups (RK4)")

    kk = np.linspace(-3.0, 0.95, 300)
    axR.plot(kk, [prompt_jump_factor(k) for k in kk], color=INK, lw=2.4)
    axR.axhline(1.0, color="0.85", lw=1.0, zorder=0)
    axR.axvline(1.0, color=ALT, ls=":", lw=1.8)
    axR.annotate("diverges at 1\\$", xy=(0.95, 15), xytext=(0.0, 16),
                 fontsize=9, color=ALT,
                 arrowprops=dict(arrowstyle="->", color=ALT, lw=1.0))
    axR.plot([-1.0], [prompt_jump_factor(-1.0)], "o", color=LEAF, ms=8)
    axR.annotate("a $-1\\$$ scram halves the power\nbefore any rod has finished moving",
                 xy=(-1.0, 0.5), xytext=(-2.9, 5.0), fontsize=8.5, color=LEAF,
                 arrowprops=dict(arrowstyle="->", color=LEAF, lw=1.0))
    axR.set_xlabel("reactivity $k(\\$)$")
    axR.set_ylabel("prompt jump $n_+/n_0$")
    axR.set_ylim(0, 20)
    axR.set_xlim(-3, 1.1)
    axR.set_title("$n_+/n_0 = 1/(1-k(\\$))$")
    fig.tight_layout()
    _save(fig, "fig3_transients.svg")
    caps["fig3_transients.svg"] = (
        "Left: the six-group point kinetics equations (10.86) integrated by RK4 for four step "
        "insertions. Each shows the same two-stage shape S&F's Fig. 10.8 sketches -- a fast "
        "prompt jump on the l0/beta ~ 0.06 s scale, then a slow exponential on the precursor "
        "scale. Right: the prompt jump itself, 1/(1 - k($)) from Eq. (10.108). It diverges "
        "exactly at 1$, which is the mathematical signature of prompt criticality; and for "
        "negative insertions it is a prompt DROP, so a -1$ scram halves the power before any "
        "control rod has finished travelling. What it cannot do is keep halving: after the "
        "jump, the decay is limited by the precursors.")

    # Fig 4 -- xenon.
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.0))
    phis = np.logspace(11, 15.5, 200)
    axL.loglog(phis, [iodine_xenon_equilibrium(p)[0] for p in phis], color=FLOW,
               lw=2.2, ls="--", label="$^{135}$I  (linear for ever)")
    axL.loglog(phis, [iodine_xenon_equilibrium(p)[1] for p in phis], color=INK,
               lw=2.4, label="$^{135}$Xe  (saturates)")
    sat = LAMBDA_X / (SIGMA_A_XE135_B * 1e-24)
    axL.axvline(sat, color=ALT, ls=":", lw=1.6)
    axL.annotate("$\\phi=\\lambda_X/\\sigma_a^X$\n$=7.8\\times10^{12}$",
                 xy=(sat, 1e15), xytext=(1.3e11, 4e16), fontsize=8.5, color=ALT,
                 arrowprops=dict(arrowstyle="->", color=ALT, lw=1.0))
    axL.set_xlabel("thermal flux $\\phi_0$ (cm$^{-2}$s$^{-1}$)")
    axL.set_ylabel("$N/\\Sigma_f$ (cm$^2$)")
    axL.legend(fontsize=8.5, loc="upper left")
    axL.set_title("The reservoir that causes the peak")

    hours = np.linspace(0, 60, 400)
    for phi, col, ls in ((1e13, LEAF, "-."), (5e13, FLOW, "--"), (1e14, INK, "-")):
        axR.plot(hours, [-xenon_reactivity(h * 3600.0, 0.0, phi) for h in hours],
                 color=col, lw=2.2, ls=ls, label="$\\phi_0=%g$" % phi)
    r0 = -xenon_reactivity(0.0, 0.0, 1e14)
    axR.axhline(0.10, color=ALT, ls=":", lw=1.8)
    axR.annotate("available override (0.10)", xy=(45, 0.105), fontsize=8.5, color=ALT)
    axR.axvspan(2.5, 33.0, color=ALT, alpha=0.10, lw=0)
    axR.annotate("cannot restart\n(~30 h)", xy=(15, 0.03), fontsize=9, color=ALT,
                 ha="center")
    axR.set_xlabel("hours after shutdown")
    axR.set_ylabel("$|\\rho_{Xe}|$")
    axR.legend(fontsize=8.5, loc="upper right")
    axR.set_title("Xenon keeps growing for 11 hours")
    fig.tight_layout()
    _save(fig, "fig4_xenon.svg")
    caps["fig4_xenon.svg"] = (
        "Left: S&F Eqs. (10.50)-(10.51). 135I grows linearly with flux without limit while "
        "135Xe saturates above 7.8e12 cm-2 s-1, where it is burned out as fast as it is made. "
        "So a high-power reactor sits on an iodine reservoir ten times its xenon inventory. "
        "Right: what that reservoir does after a scram. With no flux to burn it, the iodine "
        "decays into xenon and the poison keeps GROWING for about 11 hours, peaking at 4.5 "
        "times its operating value. A reactor with 0.10 of override reactivity is locked out "
        "from 2.5 hours after shutdown until roughly 33 hours -- S&F's 15-25 hour 'poison "
        "shutdown time'. The operator's window to restart is the first two and a half hours, "
        "which is the pressure that contributed to the Chernobyl-4 sequence.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures +", "captions.json to", HERE)


if __name__ == "__main__":
    main()
