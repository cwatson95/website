# ST-03 — References

This trunk has **no PDF on the shelf**: the primary source is the Penn State
**STAT 414** Open Educational Resource, cited by **lesson number and title**.
Textbook cross-references are given at **chapter level only** (we do not hold the
PDFs, so no page numbers).

| Source | Where | Notes |
|---|---|---|
| Penn State **STAT 414**, *Introduction to Probability Theory* (OER, CC BY-NC 4.0) | `https://online.stat.psu.edu/stat414/` (lesson pages `.../lesson/<n>`) | **primary**; this module = **Lesson 4** *Conditional Probability* + **Lesson 5** *Independent Events* |
| Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* | (the text STAT 414 follows) | cross-cited at **chapter level** — Ch. 1 *Probability* (§§ conditional probability, independent events, multiplication rule) |
| Wackerly, Mendenhall & Scheaffer, *Mathematical Statistics with Applications* | — | cross-cited at **chapter level** — Ch. 2 *Probability* (conditional probability, independence, multiplicative & event-composition laws) |
| Ross, *A First Course in Probability* | — | cross-cited at **chapter level** — Ch. 3 *Conditional Probability and Independence* |

> **Granularity.** Citations are at **OER-lesson level** (STAT 414) and **textbook
> chapter level** (HTZ / Wackerly / Ross). Penn State numbers its lessons stably;
> the lesson↔textbook section correspondence is the standard STAT 414 mapping but
> printed↔page offsets were **not** verified (we do not hold these PDFs locally —
> cf. `~SM-06/refs.md`, which *does* verify Pathria page-by-page). The material —
> the definition $P(A\mid B)=P(A\cap B)/P(B)$, the multiplication/chain rule, and
> independence — is entirely standard; tighten to section level against any of the
> three texts if needed.

## Topic → location

| Topic (code symbol) | Source | Lesson / chapter |
|---|---|---|
| Conditional probability $P(A\mid B)=P(A\cap B)/P(B)$; renormalizing to $B$ (`conditional`, `conditional_event`) | PSU | **L4** *Conditional Probability* |
| Multiplication rule $P(A\cap B)=P(B)P(A\mid B)$; chain rule; tree diagrams; sampling without replacement (`multiplication_rule`, `chain_rule`, `chain_rule_factors`, `two_card_deck`) | PSU | **L4** *Conditional Probability* |
| Conditional probability is itself a probability measure (the axioms hold for $Q=P(\cdot\mid B)$) (`conditional_measure`, `is_probability_measure`) | PSU | **L4** *Conditional Probability* |
| Independence $P(A\cap B)=P(A)P(B)\iff P(A\mid B)=P(A)$ (`independent_check`, `independent_events`, `conditional_equals_marginal`) | PSU | **L5** *Independent Events* |
| Pairwise vs mutual independence; the two-coin counterexample (`pairwise_independent`, `mutually_independent`, `two_coin_space`) | PSU | **L5** *Independent Events* |
| Conditional independence $P(A\cap B\mid C)=P(A\mid C)P(B\mid C)$ (`conditionally_independent_check`) | PSU | L4/L5 (basis for **L6**, `~ST-04`) |
| Exponential memorylessness $P(T>s+t\mid T>s)=P(T>t)$ (`exponential_survival`, `memoryless_conditional`) | PSU | L4 conditioning + **L15** (exponential, `~ST-11`) |
| Independence as factorization of a joint density (`uniform_square_joint`, `prob_rect`) | PSU | L5 + **L19–L20** (`~ST-13`) |
| Conditional probability, independence, multiplicative law (cross-text) | HTZ | Ch. 1 *Probability* |
| Conditional probability, independence, event-composition / law of total probability | Wackerly | Ch. 2 *Probability* |
| Conditional probability, independence, the multiplication rule | Ross | Ch. 3 *Conditional Probability and Independence* |

## See also
- `~ST-01` (sample spaces & the Kolmogorov axioms — the measure being conditioned;
  inclusion–exclusion for `prob_union`) and `~ST-02` (counting — equally-likely
  outcomes behind the coin/card demos): the two prerequisites.
- `~ST-04` (**Bayes' theorem** & law of total probability, STAT 414 **L6**) — the
  direct sequel, built on the multiplication rule and on $P(\cdot\mid B)$ being a
  measure (§§2, 6 of `notes.md`).
- `~ST-05` (random variables), `~ST-13` (joint distributions) — independence of
  *events* becomes independence/factorization of *variables*; `~ST-07` (binomial —
  independent Bernoulli trials), `~ST-08`/`~ST-11` (geometric/exponential
  memorylessness).
- `~MA-19` / `~SM-01` — the probability foundations this trunk deep-dives.
- STAT 414 L4–L5 (primary, worked examples online); Hogg–Tanis–Zimmerman Ch. 1
  (the text the course follows); Ross Ch. 3 and Wackerly Ch. 2 (parallel
  treatments, more proofs).
