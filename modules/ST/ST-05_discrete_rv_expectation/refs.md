# ST-05 — References

| Source (edition) | Location | Notes |
|---|---|---|
| Penn State **STAT 414**, *Probability Theory* (OER, CC BY-NC 4.0) | `online.stat.psu.edu/stat414` → **Lesson 7** *Discrete Random Variables*, **Lesson 8** *Mathematical Expectation* | **primary**; this module is a faithful replica of L7–L8. Cited by **lesson number/title**. L9 *Moment-Generating Functions* is the §8 preview (own module `~ST-06`). |
| Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* (10th ed.) | **Ch. 2** *Discrete Distributions* (§2.1 random variables of the discrete type, §2.2 mathematical expectation, §2.3 special expectations: mean/variance/mgf) | the text STAT 414 follows; cross-cited at **chapter/section level** |
| Wackerly, Mendenhall & Scheaffer, *Mathematical Statistics with Applications* (7th ed.) | **Ch. 3** *Discrete Random Variables and Their Probability Distributions* (§3.2 pmf, §3.3 expected value, §3.4 variance) | optional cross-reference, **chapter level** |
| Ross, *A First Course in Probability* (9th/10th ed.) | **Ch. 4** *Random Variables* (expectation §4.3–4.4, variance §4.5) | optional cross-reference, **chapter level** |

> **Granularity.** This trunk has **no textbook PDF on the shelf**: the primary
> citation is the **STAT 414 OER, by lesson number and title** (the URLs above are
> stable). Book cross-references are given at **chapter/section level only** — no
> page numbers, since the printed↔PDF page offsets were **not** verified (cf.
> `~QF-01/refs.md`, which likewise cites at section level, vs. `~SM-06/refs.md`,
> which does verify page-by-page). HTZ chapter/section numbers follow the standard
> editions; tighten to page level only against a copy in hand. Definitions here are
> completely standard and identical across all four sources; the OER lesson page
> may be opened to confirm any single definition.

## Topic → location

| Topic (code symbol) | Source | Lesson / chapter & title |
|---|---|---|
| Discrete RV, pmf $f(x)$, the two pmf axioms (`pmf_is_valid`, `support`) | PSU | **L7** *Discrete Random Variables* |
| Cdf $F(x)=P(X\le x)$ as a right-continuous step function; jumps $=f(x)$ (`cdf_from_pmf`, `cdf_table`) | PSU | **L7** *Discrete Random Variables* |
| Mathematical expectation; **LOTUS** $E[g(X)]=\sum g(x)f(x)$ (`expectation_of`, `lotus`) | PSU | **L8** *Mathematical Expectation* |
| Mean $\mu=E[X]$ (`expectation`, `mean`); tail-sum / survival form (`survival`, `mean_via_survival`) | PSU | **L8** *Mathematical Expectation* |
| Variance $\sigma^2=E[X^2]-\mu^2$, std $\sigma$ (`variance`, `std`) | PSU | **L8** *Mathematical Expectation* |
| Raw & central moments, standardization, skewness (`raw_moment`, `central_moment`, `standardize`, `skewness`, `excess_kurtosis`) | PSU | **L8** *Mathematical Expectation* |
| Linearity $E[aX+b]=aE[X]+b$; $\mathrm{Var}(aX+b)=a^2\mathrm{Var}(X)$ (`linear_transform`) | PSU | **L8** *Mathematical Expectation* |
| Moment-generating function $M(t)=E[e^{tX}]$ preview (`mgf`) | PSU | **L9** *Moment-Generating Functions* (own module `~ST-06`) |
| All of the above, derived from first principles | HTZ | **Ch. 2** §2.1–2.3 *Discrete Distributions* |
| Expected value & variance of a discrete RV | WMS | **Ch. 3** §3.2–3.4 |
| Random variables, expectation, variance | Ross | **Ch. 4** §4.3–4.5 |

## See also
- `~QM-06` (measurement postulates — the quantum expectation value
  $\langle A\rangle=\sum_a a|c_a|^2$ and variance $\sigma_A^2=\langle A^2\rangle-
  \langle A\rangle^2$, *the* §4–§5 formulas with the Born pmf $f(a)=|c_a|^2$) and
  `~SM-01` (ensembles — the average $\langle\cdot\rangle=\sum_i(\cdot)P_i$ over
  Boltzmann weights).
- `~ST-06` (moment-generating functions — the §8 preview developed in full,
  HTZ §2.3) and `~ST-01` (probability axioms — the pmf axioms inherit from these).
- Forward: `~ST-07` (binomial), `~ST-08` (geometric / negative binomial), `~ST-09`
  (Poisson) — the named discrete distributions whose $\mu,\sigma^2$ this machinery
  computes; `~ST-10`–`~ST-12` (continuous RVs — the same definitions with
  $\sum\to\int$).
- `~MA-19` (probability & statistics — the sample $\bar x,s^2$ that estimate the
  population $\mu,\sigma^2$ defined here).
