# ST-01 — References

| Source | Locator | Notes |
|---|---|---|
| Penn State **STAT 414**, *Probability Theory* (OER, CC BY-NC 4.0) | `online.stat.psu.edu/stat414` — **Lesson 1** *The Big Picture*, **Lesson 2** *Properties of Probability* | **primary**; this module is a faithful replica of L1–L2 |
| Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* (10th ed.) | **Ch. 1** *Probability* (§§1.1–1.4) | the textbook STAT 414 follows; cross-cited at **chapter/section level** |
| Ross, *A First Course in Probability* (10th ed.) | **Ch. 2** *Axioms of Probability* | cross-cited at **chapter level** (inclusion–exclusion, Boole) |
| Wackerly, Mendenhall & Scheaffer, *Mathematical Statistics with Applications* (7th ed.) | **Ch. 2** *Probability* | optional cross-reference at **chapter level** |

> **Granularity.** There is **no textbook PDF on this trunk's shelf**, so the
> **primary** citation is the STAT 414 OER itself, given by **lesson number and
> title** (the lesson pages are stable; the definitions are standard). Textbook
> cross-references (HTZ, Ross, Wackerly) are given by **chapter/section only** —
> **page offsets were not verified** (cf. `~QF-01/refs.md`, which cites Peskin at
> section level for the same reason). Chapter numbers follow the editions listed
> above; tighten to page level only against a copy in hand.

## Topic → location

| Topic (code symbol) | Source | Lesson / chapter |
|---|---|---|
| Random experiment, sample space $S$, events as subsets (`product_sample_space`, `standard_deck`, `event_probability`) | PSU | **L1** *The Big Picture* |
| Set algebra: union / intersection / complement, **De Morgan** (`complement_set`) | PSU / HTZ | **L1**; HTZ §1.1 |
| The three **Kolmogorov axioms** A1–A3; countable additivity (`union_disjoint`, `is_valid_probability`) | PSU / HTZ | **L2** *Properties of Probability*; HTZ §1.2 |
| Consequences: $P(\varnothing)=0$, complement rule, monotonicity (`prob_empty`, `prob_sure`, `complement`, `monotone`, `prob_difference`) | PSU / HTZ | **L2**; HTZ §1.2 |
| **Addition rule** $P(A\cup B)=P(A)+P(B)-P(A\cap B)$ (`union_two`, `intersection_from_union`) | PSU / Ross | **L2**; Ross §2.4 |
| **Inclusion–exclusion** (3-set and general) and **Boole's inequality** (`union_three`, `inclusion_exclusion`, `boole_bound`) | Ross / HTZ | Ross §2.4; HTZ §1.2 |
| **Equally-likely** outcomes, classical probability $P(A)=\lvert A\rvert/\lvert S\rvert$ (`prob_equally_likely`) | PSU / HTZ | **L1–L2**; HTZ §1.1 |
| Continuous sample spaces, $P(A)=\int_A f$ (`uniform_pdf`, `prob_continuous`) | PSU | **L1** (preview; full treatment in `~ST-10`) |
| **Born rule** $P_i=\lvert\psi_i\rvert^2/\langle\psi\vert\psi\rangle$ (`born_probabilities`) | — | the axioms applied to $\lvert\psi\rvert^2$; see `~QM-02` |

## See also
- `~MA-19` (probability & statistics — the applied toolkit this trunk re-derives
  from the axioms here) and `~ST-02` (counting — the $\lvert A\rvert,\lvert S\rvert$
  behind the equally-likely measure).
- `~ST-03` (conditional probability & independence) and `~ST-04` (Bayes' theorem)
  — the next refinements of the set function $P$ on this same sample space.
- `~SM-01` (statistical-mechanics ensembles — equal *a priori* probabilities, the
  physical equally-likely measure $P=\Omega/\Omega_{\rm tot}$).
- `~QM-02` (wavefunction & Born rule — the same axioms read off $\lvert\psi\rvert^2$)
  and `~QM-06` (measurement postulates).
- STAT 414 L1–L2 (primary); HTZ Ch. 1 (the followed text); Ross Ch. 2
  (axioms, inclusion–exclusion, Boole); Wackerly Ch. 2 (optional, same material).
