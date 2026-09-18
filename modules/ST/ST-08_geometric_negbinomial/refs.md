# ST-08 — References

This trunk has **no textbook PDF on the shelf**. The **primary** reference is the
open Penn State STAT 414 OER, cited **by lesson number and title**; the books
STAT 414 follows are cross-referenced **at chapter level only** (we do not hold the
PDFs, so no page numbers).

| Source | Locator | Notes |
|---|---|---|
| Penn State STAT 414, *Introduction to Probability Theory* (OER) | `online.stat.psu.edu/stat414` → **Lesson 11**, *Geometric and Negative Binomial Distributions* | **primary**; CC BY-NC 4.0. The pmf/mean/variance/mgf forms and the memoryless property are taken from this lesson. (Lesson 9 *Moment Generating Functions* and Lesson 10 *The Binomial Distribution* are background.) |
| Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* (10th ed.) | **Ch. 2**, *Discrete Distributions* (geometric & negative binomial sections) | the text STAT 414 follows; cross-cited at **chapter level** |
| Wackerly, Mendenhall & Scheaffer, *Mathematical Statistics with Applications* (7th ed.) | **Ch. 3**, *Discrete Random Variables and Their Probability Distributions* | optional cross-reference (geometric §3.5, negative binomial §3.6), **chapter level** |
| Ross, *A First Course in Probability* (10th ed.) | **Ch. 4**, *Random Variables* (geometric & negative binomial sections) | optional cross-reference, **chapter level** |

> **Granularity.** Citations are **OER-lesson-level**: the STAT 414 lesson number
> and title are stable, but printed↔PDF page offsets for HTZ / Wackerly / Ross were
> **not** verified (we do not have those PDFs on the shelf), so the book references
> are given **by chapter and title only**, never by page (cf. `~QF-01/refs.md`,
> which cites Peskin at section level for the same reason). The geometric and
> negative binomial are completely standard; the definitions can be confirmed on
> the linked OER lesson page if desired.

## Topic → location

| Topic (code symbol) | Source | Lesson / chapter |
|---|---|---|
| Geometric pmf $(1-p)^{x-1}p$, normalization by the geometric series (`geometric_pmf`) | PSU | L11 *Geometric and Negative Binomial Distributions* |
| Geometric cdf $1-(1-p)^x$, survival $P(X>x)=(1-p)^x$ (`geometric_cdf`, `geometric_sf`) | PSU | L11 |
| Geometric mean $1/p$, variance $(1-p)/p^2$ (`geometric_mean`, `geometric_var`) | PSU; HTZ | L11; Ch. 2 |
| Geometric mgf $pe^t/(1-(1-p)e^t)$, moments by differentiation (`geometric_mgf`) | PSU | L9 *Moment Generating Functions*, L11 |
| **Memoryless** property $P(X>m+n\mid X>m)=P(X>n)$ and its uniqueness (`memoryless_check`) | PSU; HTZ | L11; Ch. 2 |
| Negative binomial pmf $\binom{x-1}{r-1}(1-p)^{x-r}p^r$, normalization by the negative binomial series (`negbinom_pmf`) | PSU; HTZ | L11; Ch. 2 |
| Negative binomial mean $r/p$, variance $r(1-p)/p^2$ (`negbinom_mean`, `negbinom_var`) | PSU | L11 |
| Negative binomial mgf $=$ geometric mgf$^{\,r}$; geometric $=$ negbinom$(r{=}1)$; **sum of $r$ geometrics** (`negbinom_mgf`) | PSU; HTZ | L11; Ch. 2 |
| Binomial background (Bernoulli trials, $\binom{n}{k}$) feeding the negative-binomial count | PSU | L10 *The Binomial Distribution* (`~ST-07`) |

## See also
- `~ST-07` (the binomial — fixed $n$ trials, count successes): the question this
  module inverts; the same independent $p$-coin and the same $\binom{\cdot}{\cdot}$
  counting (`~ST-02`).
- `~ST-05` (discrete random variables, $E[X]$, $\operatorname{Var}$) and `~ST-06`
  (mgf, uniqueness, moments by differentiation): the tools used in §4–§7 of
  `notes.md`.
- `~ST-09` (Poisson — law of rare events; the negative binomial is a
  Gamma-mixture of Poissons) and `~ST-11` (exponential & gamma — the continuous
  memoryless / sum-of-waits analogues; the §8 limit).
- STAT 414 OER (primary, computational and verbal); Hogg, Tanis & Zimmerman Ch. 2
  (the text the course follows); Wackerly Ch. 3 and Ross Ch. 4 (parallel
  treatments, both at chapter level only).
