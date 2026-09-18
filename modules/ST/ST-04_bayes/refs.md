# ST-04 — References

| Source (edition) | Locator | Notes |
|---|---|---|
| Penn State **STAT 414**, *Introduction to Probability Theory* (OER, CC BY-NC 4.0) | `online.stat.psu.edu/stat414/lesson/6` | **primary**; **Lesson 6 *Bayes' Theorem*** (law of total probability, Bayes' rule, the medical-test example) |
| Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* (the text STAT 414 follows) | Ch. 1 (§§1.4–1.6) | cross-cited at **chapter/section level** (conditional probability, independence, Bayes) |
| Wackerly, Mendenhall & Scheaffer, *Mathematical Statistics with Applications* | Ch. 2 (§§2.9–2.10) | cross-cited at **chapter level** (event composition, the laws of total/Bayes) |
| Ross, *A First Course in Probability* | Ch. 3 | cross-cited at **chapter level** (conditional probability, Bayes' formula, odds) |

> **Granularity.** This trunk has **no textbook PDF on the shelf**, so the primary
> citation is the **OER lesson page** (by lesson number and title), and the textbook
> cross-references are given at **chapter/section level only** — page offsets were
> **not** verified (contrast `~MA-19/refs.md`, which pins Boas page-by-page against
> the PDF). Lesson and chapter numbers follow the standard STAT 414 ordering and the
> current editions of HTZ / WMS / Ross; tighten to page level only against a copy in
> hand. The material (total probability, Bayes, the disease screen) is completely
> standard and appears in every introductory probability text.

## Topic → location

| Topic (code symbol) | Source | Lesson / chapter |
|---|---|---|
| Partition of the sample space; **law of total probability** $P(B)=\sum_i P(B\mid A_i)P(A_i)$ (`total_probability`, `joint_probabilities`) | PSU L6 / HTZ | L6 / §1.5–1.6 |
| **Bayes' theorem** posterior $\propto$ prior $\times$ likelihood (`bayes_posterior`) | PSU L6 / HTZ / Ross | L6 / §1.6 / Ch. 3 |
| Multiplication rule $P(A\cap B)=P(A)P(B\mid A)$ behind the joints (`joint_probabilities`) | `~ST-03` / HTZ | (prereq) / §1.4 |
| Medical-test problem: sensitivity, specificity, prevalence → **PPV/NPV** (`ppv`, `npv`) | PSU L6 / WMS | L6 / §2.10 |
| Odds form: posterior odds $=$ prior odds $\times$ likelihood ratio (`prob_to_odds`, `odds_to_prob`, `lr_positive`, `lr_negative`, `posterior_odds`) | Ross / HTZ | Ch. 3 (odds & Bayes factor) / §1.6 |
| **Sequential updating** (posterior $\to$ prior); conditional independence (`sequential_update`) | PSU L6 / HTZ | L6 / §1.6 |
| Continuous Bayes: binomial likelihood, $\binom{n}{k}$, Beta/Gamma functions (`binomial_likelihood`, `beta_pdf`) | `~ST-02`, `~MA-19` | counting / probability distributions |
| **Beta–Binomial conjugate update** and its evidence $\int\pi\mathcal L\,d\theta$ (`posterior_beta_binomial`, `evidence_beta_binomial`, `beta_mean`) | HTZ / Ross | (conjugacy; standard Bayesian extension of L6) |

## See also
- `~ST-03` (conditional probability, the multiplication rule, independence, tree
  diagrams) — the immediate prerequisite; Bayes is built line-by-line from it
  (STAT 414 L4–L5).
- `~ST-01` (probability axioms, partitions) and `~ST-02` (counting, $\binom{n}{k}$) —
  the additivity and combinatorics underneath §1 and §6 (STAT 414 L1–L3).
- `~MA-19` (binomial pmf; beta/gamma functions) — the math-trunk source for the
  likelihood and the conjugate update of §6; forward to `~ST-07` (binomial),
  `~ST-09` (Poisson), `~ST-11` (gamma/Beta) where these likelihoods become
  first-class distributions.
- `~SM-01` (statistical ensembles) — a prior/posterior is a probability distribution
  over hypotheses; `~QM-02` (the Born rule) — physics' likelihood
  $P(\text{outcome}\mid\text{state})$ and the Bayesian reading of measurement.
- Primary, computational: STAT 414 Lesson 6 (the OER). Textbook cross-refs:
  Hogg–Tanis–Zimmerman Ch. 1 (the course text), Wackerly–Mendenhall–Scheaffer Ch. 2,
  Ross Ch. 3 (Bayes, odds, the Bayes factor).
