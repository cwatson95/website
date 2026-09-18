"""ST-04 figures -- Bayes' theorem: base-rate effect and prior -> posterior.

Two SVG figures (+ captions.json) built from the module's own code in ../code:
  fig1 -- PPV P(disease|+) vs prevalence (the base-rate effect);
  fig2 -- prior P(A_i) updated to posterior P(A_i|B) across a partition.
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
from bayes import ppv, bayes_posterior, total_probability   # noqa: E402

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- positive predictive value vs prevalence, two test accuracies.
    pi = np.logspace(-4, -0.3, 200)
    ppv_99 = np.array([ppv(p, 0.99, 0.99) for p in pi])
    ppv_999 = np.array([ppv(p, 0.999, 0.999) for p in pi])
    p_star = 1e-3
    y_star = ppv(p_star, 0.99, 0.99)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.semilogx(pi, ppv_99, color=FLOW, lw=2, label=r"se = sp = $0.99$")
    ax.semilogx(pi, ppv_999, color=INK, lw=2, label=r"se = sp = $0.999$")
    ax.plot([p_star], [y_star], "o", color=ALT, zorder=4)
    ax.annotate(f"  prevalence {p_star:g}\n  P(D|+) = {y_star:.2f}",
                (p_star, y_star), color=ALT, fontsize=8.5, va="center")
    ax.set_xlabel("prevalence  P(disease)")
    ax.set_ylabel(r"$P(\mathrm{disease}\mid +)$"); ax.set_ylim(0, 1.0)
    ax.set_title("Base-rate effect: a 99% test is mostly false alarms when D is rare")
    ax.legend(loc="upper left", frameon=False)
    _save(fig, "fig1_ppv_vs_prevalence.svg")
    caps["fig1_ppv_vs_prevalence.svg"] = (
        "Bayes' theorem turns test accuracy into the positive predictive value "
        "P(disease|+). Even a 99%-sensitive, 99%-specific test gives only P(D|+)=0.09 at "
        "prevalence 0.001 (purple dot): when the disease is rare most positives are false "
        "alarms. A 99.9% test (blue) lifts the curve.")

    # Fig 2 -- prior -> posterior across a 3-cell partition (factory defects).
    priors = [0.5, 0.3, 0.2]
    likely = [0.01, 0.02, 0.03]           # P(defective | factory_i)
    post = bayes_posterior(priors, likely)
    PB = total_probability(priors, likely)
    labels = ["factory 1\n(p=.01)", "factory 2\n(p=.02)", "factory 3\n(p=.03)"]
    x = np.arange(3); w = 0.36
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.bar(x - w / 2, priors, w, color=STEEL, label=r"prior $P(A_i)$")
    ax.bar(x + w / 2, post, w, color=FLOW, label=r"posterior $P(A_i\mid B)$")
    for xi in range(3):
        ax.annotate(f"{priors[xi]:.2f}", (xi - w / 2, priors[xi]), ha="center",
                    va="bottom", xytext=(0, 2), textcoords="offset points", fontsize=8)
        ax.annotate(f"{post[xi]:.2f}", (xi + w / 2, post[xi]), ha="center",
                    va="bottom", xytext=(0, 2), textcoords="offset points", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("probability"); ax.set_ylim(0, 0.6)
    ax.set_title(r"Bayes update given defect $B$:  posterior $\propto$ prior $\times$ likelihood")
    ax.legend(loc="upper right", frameon=False)
    ax.text(0.02, 0.96, f"evidence  P(B) = {PB:.3f}", transform=ax.transAxes,
            va="top", fontsize=9, color=ALT)
    _save(fig, "fig2_prior_to_posterior.svg")
    caps["fig2_prior_to_posterior.svg"] = (
        "A defective item B is observed; the partition is three factories with prior "
        "output shares P(A_i) and defect likelihoods 0.01/0.02/0.03. The posterior "
        "P(A_i|B) is proportional to prior times likelihood, renormalized by the evidence "
        "P(B)=0.017, so the dirtiest factory 3 climbs from 0.20 to 0.35 while factory 1 "
        "falls from 0.50 to 0.29.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
