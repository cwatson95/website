# ST-09 — References

The Probability Theory trunk has **no textbook PDF on the shelf**: the primary
source is the open courseware this trunk replicates, cited by **lesson number and
title**. Textbooks are cross-referenced at **chapter level only** (no page
numbers — we do not have the PDFs).

| Source | Where | Notes |
|---|---|---|
| **Penn State STAT 414**, *Probability Theory* (OER, CC BY-NC 4.0) | `https://online.stat.psu.edu/stat414/` → **Lesson 12, "The Poisson Distribution"** (`.../lesson/12`) | **primary**; cited by sub-lesson **L12.1** (the pmf, law of rare events) and **L12.2** (mean/variance, mgf) |
| Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* (10th ed.) | the textbook STAT 414 follows | cross-cited at **chapter level**, §2.6 *The Poisson Distribution* |
| Wackerly, Mendenhall & Scheaffer, *Mathematical Statistics with Applications* (7th ed.) | optional cross-reference | **Ch. 3** *Discrete Random Variables*, §3.8 the Poisson |
| Ross, *A First Course in Probability* (10th ed.) | optional cross-reference | **Ch. 4** *Random Variables*, §4.7 the Poisson; **Ch. 9** the Poisson process |

> **Granularity.** Citations are **OER-lesson-level**: the STAT 414 lesson and
> sub-lesson numbers (L12.1/L12.2) are stable and were used to organize this
> module, but the textbook **page offsets were not verified** (we hold no PDF),
> so HTZ / Wackerly / Ross are cited by **chapter and section title only**, never
> by page (cf. `~QF-01/refs.md`, which likewise pins chapters, not pages). The
> Poisson material is completely standard; any of the three texts above covers it
> identically. You may open the STAT 414 lesson page to confirm a definition.

## Topic → location

| Topic (code symbol) | Source | Lesson / chapter |
|---|---|---|
| Poisson pmf $e^{-\lambda}\lambda^{k}/k!$, normalization via $\sum\lambda^k/k!=e^\lambda$, recurrence, cdf, mode (`poisson_pmf`, `poisson_cdf`, `poisson_normalization`, `poisson_mode`) | STAT 414 | **L12.1** *The Poisson Distribution* |
| Mean $E[X]=\lambda$, variance $\mathrm{Var}(X)=\lambda$, factorial moments $\lambda^r$, skewness/kurtosis (`poisson_mean`, `poisson_var`, `poisson_std`, `poisson_factorial_moment`, `poisson_skewness`, `poisson_excess_kurtosis`) | STAT 414 | **L12.2** *Poisson... Expected Value & Variance* |
| Moment- and probability-generating functions $M(t)=e^{\lambda(e^t-1)}$, $G(s)=e^{\lambda(s-1)}$ (`poisson_mgf`, `poisson_pgf`) | STAT 414 | **L12.2** (mgf); `~ST-06` (mgf technique) |
| Law of rare events: $\mathrm{Bin}(n,p)\to\mathrm{Poisson}(np)$ (`binomial_pmf`, `poisson_limit_of_binomial`) | STAT 414 | **L12.1** *as an approximation to the binomial*; `~ST-07` |
| Reproductive / additivity property, convolution (`sum_of_poissons`, `poisson_convolution_pmf`) | STAT 414 / HTZ | **L12.2**; HTZ §2.6 / Ross §4.7 |
| The Poisson process, $\lambda=\nu t$, and the gamma-integral / arrival-time link (the `_integrate` check) | Ross | **Ch. 9** *The Poisson Process*; `~ST-11` (exponential & gamma) |
| Normal approximation to the Poisson (large $\lambda$) | STAT 414 | **L28** *Approximations for Discrete Distributions*; `~ST-18` |

## See also
- `~ST-07` (binomial — the Poisson is its rare-events limit, §4) and `~ST-06`
  (mgf, the uniqueness theorem that proves the limit and the additivity property).
- `~ST-05` (discrete random variables — pmf, $E[X]$, $\mathrm{Var}(X)$, the
  prerequisite machinery); `~ST-08` (geometric / negative binomial — partner
  discrete laws).
- `~ST-11` (exponential, gamma, chi-square — interarrival and arrival times of the
  Poisson process); `~ST-18` (CLT) and `~ST-12` (normal) — the large-$\lambda$
  Gaussian limit.
- `~QO-01` (quantized light — Poissonian photon counting and shot noise; STAT 414's
  Poisson is the photon-statistics distribution there) and `~PK-04` (atomic &
  molecular kinetics — collision/reaction counts and the birth-process master
  equation); `~SM-01` (counting and the rare-event limit).
- Primary: STAT 414 Lesson 12 (computational, with worked examples). Cross-texts:
  Hogg–Tanis–Zimmerman §2.6 (the course's own text), Wackerly Ch. 3, Ross Ch. 4 &
  9 (the process picture, gentle).
