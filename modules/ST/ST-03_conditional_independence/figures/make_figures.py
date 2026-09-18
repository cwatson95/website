"""ST-03 figures -- conditional probability & independence.

Two SVG figures (+ captions.json) built from the module's own code in ../code:
  fig1 -- P(A|B) vs P(A): equal for independent events, unequal for dependent;
  fig2 -- conditioning as a measure: P(.) reweighted to Q(.)=P(.|B).
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
from conditional_independence import (             # noqa: E402
    two_coin_space, two_card_deck, prob, conditional_event,
    conditional_measure, independent_events,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- independence vs dependence: P(A) compared with P(A|B).
    cm, A, B, C = two_coin_space()
    coin_pA = prob(cm, A)
    coin_pAB = conditional_event(cm, A, B)                 # = P(A): independent
    coin_indep = independent_events(cm, A, B)

    deck, first_ace, second_ace = two_card_deck()
    card_pA = prob(deck, second_ace)
    card_pAB = conditional_event(deck, second_ace, first_ace)   # 3/51 < 4/52
    card_indep = independent_events(deck, second_ace, first_ace)

    groups = ["coins:  A=1st H,  B=2nd H", "cards:  A=2nd ace,  B=1st ace"]
    marg = [coin_pA, card_pA]
    cond = [coin_pAB, card_pAB]
    x = np.arange(2); w = 0.36
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.bar(x - w / 2, marg, w, color=INK, label=r"$P(A)$")
    ax.bar(x + w / 2, cond, w, color=FLOW, label=r"$P(A\mid B)$")
    for xi, (m, c) in enumerate(zip(marg, cond)):
        ax.annotate(f"{m:.3f}", (xi - w / 2, m), ha="center", va="bottom",
                    xytext=(0, 2), textcoords="offset points", fontsize=8)
        ax.annotate(f"{c:.3f}", (xi + w / 2, c), ha="center", va="bottom",
                    xytext=(0, 2), textcoords="offset points", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(groups, fontsize=8.5)
    ax.set_ylabel("probability"); ax.set_ylim(0, 0.62)
    ax.set_title(r"Independence: $P(A\mid B)=P(A)$;  dependence: $P(A\mid B)\neq P(A)$")
    ax.legend(loc="upper right", frameon=False)
    ax.text(0.02, 0.80, f"independent?  coins = {coin_indep},  cards = {card_indep}",
            transform=ax.transAxes, fontsize=8.5, color=ALT)
    _save(fig, "fig1_independence_vs_dependence.svg")
    caps["fig1_independence_vs_dependence.svg"] = (
        "Conditioning on B and comparing with the marginal P(A). For two fair coins, A "
        "(1st heads) and B (2nd heads) are independent, so P(A|B)=0.500=P(A). Drawing "
        "two cards without replacement is dependent: P(2nd ace | 1st ace)=3/51=0.059 "
        "falls below P(2nd ace)=4/52=0.077.")

    # Fig 2 -- conditioning as a measure on the two-coin space.
    cm, A, B, C = two_coin_space()
    Q = conditional_measure(cm, B)          # B = second toss is heads
    outs = list(cm.keys())
    labels = ["".join(o) for o in outs]
    pP = [cm[o] for o in outs]
    pQ = [Q[o] for o in outs]
    x = np.arange(len(outs)); w = 0.38
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.bar(x - w / 2, pP, w, color=STEEL, label=r"prior $P(\cdot)$")
    ax.bar(x + w / 2, pQ, w, color=FLOW, label=r"$Q(\cdot)=P(\cdot\mid B)$")
    for xi in range(len(outs)):
        ax.annotate(f"{pP[xi]:.2f}", (xi - w / 2, pP[xi]), ha="center", va="bottom",
                    xytext=(0, 2), textcoords="offset points", fontsize=8)
        ax.annotate(f"{pQ[xi]:.2f}", (xi + w / 2, pQ[xi]), ha="center", va="bottom",
                    xytext=(0, 2), textcoords="offset points", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_xlabel("outcome (1st toss, 2nd toss)")
    ax.set_ylabel("probability"); ax.set_ylim(0, 0.62)
    ax.set_title(r"Conditioning: $Q(\cdot)=P(\cdot\mid B)$ zeros $B^{c}$ and renormalizes")
    ax.legend(loc="upper center", frameon=False, ncol=2)
    _save(fig, "fig2_conditioning_measure.svg")
    caps["fig2_conditioning_measure.svg"] = (
        "Conditioning on B = '2nd toss is heads' turns the uniform prior P (each "
        "outcome 0.25) into Q(.)=P(.|B): the outcomes outside B (HT, TT) get "
        "probability 0 and the survivors HH, TH are renormalized to 0.50 each. Q is "
        "itself a valid probability measure.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
