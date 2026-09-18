# ST-01 — Sample spaces & the axioms of probability

First module of the **PROBABILITY THEORY** trunk (see `modules/list_ST.txt`), a
faithful module-by-module replica of Penn State's **STAT 414**. It covers
**Lesson 1 (The Big Picture)** and **Lesson 2 (Properties of Probability)**: a
random experiment has a **sample space** $S$ of outcomes; **events** are subsets
of $S$; and a **probability** is a set function $P$ obeying three **Kolmogorov
axioms**. Everything downstream in the trunk — random variables, expectation,
every named distribution — is built on the rules pinned down here.

- **Prerequisites:** `~MA-19` (the working probability/statistics toolkit —
  binomial/normal pmf/pdf, sample moments — that this trunk now deep-dives from
  the axioms up), basic set notation and the idea of a function (`~MA-01`).
- **Cross-links:** `~SM-01` (statistical mechanics' *equal a priori
  probabilities* — the equally-likely measure $P(A)=|A|/|S|$ made physical),
  `~QM-02` (the **Born rule** $P_i=|\psi_i|^2$ — the *same* axioms applied to a
  quantum amplitude vector), `~ST-02` (counting, which supplies $|A|$ and $|S|$),
  `~ST-03` (conditional probability & independence — the next refinement of $P$),
  `~ST-10`/`~ST-12` (continuous sample spaces where $P(A)=\int_A f$).

## Scope
A **sample space** $S$ is the set of all outcomes of a random experiment; an
**event** $A\subseteq S$ is a set of outcomes; the impossible event is $\varnothing$
and the certain event is $S$. Events combine by **set algebra** — union
$A\cup B$, intersection $A\cap B$, complement $A^c$ — obeying the distributive and
**De Morgan** laws $(A\cup B)^c=A^c\cap B^c$, $(A\cap B)^c=A^c\cup B^c$. A
**probability** is a function $P$ on events satisfying **Kolmogorov's three
axioms**: (A1) $P(A)\ge 0$; (A2) $P(S)=1$; (A3) countable additivity,
$P\!\big(\bigsqcup_i A_i\big)=\sum_i P(A_i)$ for pairwise-disjoint events. From
these alone follow $P(\varnothing)=0$, the **complement rule** $P(A^c)=1-P(A)$,
**monotonicity** $A\subseteq B\Rightarrow P(A)\le P(B)$, the range $0\le P\le 1$,
the **addition rule** $P(A\cup B)=P(A)+P(B)-P(A\cap B)$, its three-set extension
and the general **inclusion–exclusion** law, and **Boole's inequality**
$P(\bigcup A_i)\le\sum P(A_i)$. When $S$ is finite and outcomes are **equally
likely**, $P$ collapses to counting, $P(A)=|A|/|S|$ — the classical probability
of dice and cards. The code builds explicit dice/deck sample spaces, checks
inclusion–exclusion against brute-force counts, verifies De Morgan on real sets,
and carries the axioms to a **continuous** sample space ($P(A)=\int_A f$) and to
the **Born rule** (`~QM-02`).

## Operations — `code/probability_axioms.py`

| call | meaning | reference |
|------|---------|-----------|
| `is_valid_probability(p)` | axiom range $0\le P(A)\le 1$ (A1+A2) | L2 |
| `prob_empty()` / `prob_sure()` | $P(\varnothing)=0$ ; $P(S)=1$ (A2) | L2 |
| `complement(p)` | complement rule $P(A^c)=1-P(A)$ | L2 |
| `prob_equally_likely(k, n)` | classical probability $P(A)=\lvert A\rvert/\lvert S\rvert$ | L1; `~SM-01` |
| `union_disjoint(*p)` | additivity $P(\bigsqcup A_i)=\sum P(A_i)$ (A3) | L2 |
| `union_two(pa, pb, pab)` | addition rule $P(A)+P(B)-P(A\cap B)$ | L2 |
| `intersection_from_union(pa, pb, paub)` | invert: $P(A\cap B)=P(A)+P(B)-P(A\cup B)$ | L2 |
| `prob_difference(pa, pab)` | $P(A\setminus B)=P(A)-P(A\cap B)$ | L2 |
| `union_three(...)` | 3-set inclusion–exclusion | L2 |
| `inclusion_exclusion(singles, pairs, triples, quad)` | $S_1-S_2+S_3-S_4$ | L2 |
| `boole_bound(probs)` | Boole's inequality $P(\bigcup A_i)\le\sum P(A_i)$ | L2 |
| `monotone(p_sub, p_super)` | monotonicity $A\subseteq B\Rightarrow P(A)\le P(B)$ | L2 |
| `complement_set(S, A)` | set complement $A^c=S\setminus A$ (De Morgan) | L1 |
| `product_sample_space(outcomes, repeat)` | $S=\text{outcomes}^{\text{repeat}}$ (dice) | L1 |
| `event_probability(S, predicate)` | $P(A)=\lvert A\rvert/\lvert S\rvert$ by a predicate | L1 |
| `standard_deck()` | the 52-card $(\text{rank},\text{suit})$ sample space | L1 |
| `uniform_pdf(x, a, b)` / `prob_continuous(pdf, a, b)` | continuous $f=1/(b-a)$ ; $P([a,b])=\int_a^b f$ | L1; `~ST-10` |
| `born_probabilities(amps)` | Born rule $P_i=\lvert\psi_i\rvert^2/\sum_j\lvert\psi_j\rvert^2$ | `~QM-02` |

## Use
```python
from probability_axioms import (product_sample_space, event_probability,
                                union_two, union_three, complement, born_probabilities)

S = product_sample_space(range(1, 7), repeat=2)        # two dice, |S| = 36
event_probability(S, lambda w: sum(w) == 7)            # 0.16667  = 6/36 = 1/6
event_probability(S, lambda w: w[0] == 6 or w[1] == 6) # 0.30556  = 11/36

union_two(13/52, 12/52, 3/52)                          # 0.42308  heart OR face = 22/52
complement(25/36)                                      # 0.30556  P(A^c) = 1 - P(A)
born_probabilities([1, 1, 1, 1])                       # [0.25, 0.25, 0.25, 0.25]  (~QM-02)
```

## Run
```bash
cd code
python3 probability_axioms.py        # demo: dice, cards, inclusion-exclusion, De Morgan, Born rule
python3 test_probability_axioms.py   # tests  ->  "All 10 tests passed."
```

## Files
- `notes.md` — sample space & events → set algebra/De Morgan → the three axioms →
  consequences (complement, monotonicity, addition rule, inclusion–exclusion,
  Boole) → equally-likely outcomes → continuous sample spaces → the Born rule
- `code/probability_axioms.py`, `code/test_probability_axioms.py` (pure stdlib, self-contained)
- `problems/problems.md` — worked problems (STAT 414 L1–L2; numeric checks to the code)
- `refs.md` — citation table (STAT 414 OER primary; Hogg–Tanis–Zimmerman, Ross, Wackerly cross-cited at chapter level)
