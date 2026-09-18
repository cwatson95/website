"""ST-01 figures -- sample spaces & the axioms of probability.

Two SVG figures (+ captions.json) built from the module's own code in ../code:
  fig1 -- the addition rule / inclusion-exclusion on a 52-card deck;
  fig2 -- the two-dice sum law, an equally-likely pmf whose masses sum to 1.
Run:  python3 make_figures.py
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"      # text as vector paths (portable)
matplotlib.rcParams["font.size"] = 11
import matplotlib.pyplot as plt                    # noqa: E402
import numpy as np                                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code"))
from probability_axioms import (                   # noqa: E402
    standard_deck, event_probability, union_two, product_sample_space,
)

INK, FLOW, ALT, STEEL = "#3b3b6d", "#b5651d", "#9a5a8a", "#5a7d9a"


def _save(fig, name):
    fig.savefig(os.path.join(HERE, name), format="svg", bbox_inches="tight")
    plt.close(fig)


def main():
    caps = {}

    # Fig 1 -- inclusion-exclusion (addition rule) on the 52-card deck.
    deck = standard_deck()
    is_heart = lambda c: c[1] == "hearts"
    is_face = lambda c: c[0] in ("J", "Q", "K")
    pA = event_probability(deck, is_heart)
    pB = event_probability(deck, is_face)
    pAB = event_probability(deck, lambda c: is_heart(c) and is_face(c))
    pAuB = union_two(pA, pB, pAB)
    brute = event_probability(deck, lambda c: is_heart(c) or is_face(c))

    labels = [r"$P(A)$", r"$P(B)$", r"$-P(A\cap B)$", r"$P(A\cup B)$"]
    vals = [pA, pB, -pAB, pAuB]
    cols = [INK, STEEL, FLOW, ALT]
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.bar(range(4), vals, color=cols, width=0.62)
    ax.axhline(0, color="#aaaaaa", lw=0.6)
    for i, v in enumerate(vals):
        ax.annotate(f"{v:+.3f}" if i == 2 else f"{v:.3f}", (i, v),
                    ha="center", va="bottom" if v >= 0 else "top",
                    xytext=(0, 3 if v >= 0 else -3), textcoords="offset points")
    ax.set_xticks(range(4)); ax.set_xticklabels(labels)
    ax.set_ylabel("probability"); ax.set_ylim(-0.12, 0.5)
    ax.set_title(r"Addition rule:  $P(A\cup B)=P(A)+P(B)-P(A\cap B)$")
    ax.text(0.03, 0.96, f"A = heart, B = face card\nbrute-force union = {brute:.3f}",
            transform=ax.transAxes, va="top", color=INK)
    _save(fig, "fig1_inclusion_exclusion.svg")
    caps["fig1_inclusion_exclusion.svg"] = (
        "Inclusion-exclusion on a 52-card deck with A = heart and B = face card. The "
        "overlap P(A and B) is subtracted once so it is not double counted, giving "
        "P(A or B) = 0.250 + 0.231 - 0.058 = 0.423, matching the brute-force count.")

    # Fig 2 -- two fair dice: the sum pmf, an equally-likely law summing to 1.
    S2 = product_sample_space(range(1, 7), repeat=2)
    sums = list(range(2, 13))
    pmf = [event_probability(S2, lambda w, s=s: w[0] + w[1] == s) for s in sums]
    total = sum(pmf)
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.bar(sums, pmf, color=INK, width=0.74)
    for s, p in zip(sums, pmf):
        ax.annotate(f"{int(round(p * 36))}/36", (s, p), ha="center", va="bottom",
                    xytext=(0, 2), textcoords="offset points", fontsize=8, color=ALT)
    ax.set_xticks(sums)
    ax.set_xlabel(r"sum $X+Y$ of two fair dice"); ax.set_ylabel(r"$P(X+Y=s)$")
    ax.set_ylim(0, 0.20)
    ax.set_title(f"Equally-likely sample space ($|S|=36$): masses sum to {total:.3f}")
    _save(fig, "fig2_dice_sum_pmf.svg")
    caps["fig2_dice_sum_pmf.svg"] = (
        "The probability law of the sum of two fair dice, built from the 36-outcome "
        "equally-likely sample space via P(A) = |A|/|S|. The masses form a triangle "
        "peaking at 7 (6/36) and obey Axiom A2: they sum to exactly 1.")

    with open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8") as fh:
        json.dump(caps, fh, indent=2)
    print("wrote", len(caps), "figures + captions.json to", HERE)


if __name__ == "__main__":
    main()
