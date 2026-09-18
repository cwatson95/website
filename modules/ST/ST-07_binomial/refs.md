# ST-07 — References

| Source (edition) | Location | Notes |
|---|---|---|
| Penn State STAT 414, *Probability Theory* (OER, CC BY-NC 4.0) | `online.stat.psu.edu/stat414/lesson/10` — **L10 The Binomial Distribution** | **primary**; this module replicates L10. Also L9 (mgf) for §5 |
| Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* (10th ed.) | Ch. 2 *Discrete Distributions* (§2.4 binomial; §2.3 mgf) | the text STAT 414 follows; cross-cited at **chapter level** |
| Wackerly, Mendenhall & Scheaffer, *Mathematical Statistics with Applications* (7th ed.) | Ch. 3 *Discrete Random Variables and Their Probability Distributions* (§3.4 binomial) | optional cross-reference, **chapter level** |
| Ross, *A First Course in Probability* (9th ed.) | Ch. 4 *Random Variables* (§4.6 the binomial random variable) | optional cross-reference, **chapter level** |

> **Granularity.** This trunk has **no textbook PDF on the shelf**, so the primary
> citation is the **STAT 414 OER by lesson number and title** (stable URLs under
> `online.stat.psu.edu/stat414/lesson/`). Textbook cross-references (HTZ, Wackerly,
> Ross) are given at **chapter/section level only** — chapter and section numbers
> follow the standard editions named above, but **page offsets were not verified**
> (we do not hold the PDFs). Tighten to page level only against a copy in hand.
> The binomial is entirely standard; the OER lesson and any of the three texts
> agree on every formula here.

## Topic → location

| Topic (code symbol) | Source | Lesson / chapter |
|---|---|---|
| Bernoulli trial; indicator pmf $p^kq^{1-k}$, mean $p$, variance $pq$ (`bernoulli_pmf`, `bernoulli_mean`, `bernoulli_var`) | PSU | L10 *The Binomial Distribution* (Bernoulli setup) |
| Binomial pmf $\binom nk p^kq^{n-k}$; counting success patterns with $\binom nk$ (`binom_pmf`, `binom_cdf`) | PSU | L10 (pmf); counting from L3 / `~ST-02` |
| Normalization via the binomial theorem $\sum_k\binom nk p^kq^{n-k}=1$ | PSU | L10 |
| Mean $np$ and variance $np(1-p)$ as sums of $n$ Bernoulli indicators (`binom_mean`, `binom_var`, `binom_std`, `binom_skewness`) | PSU | L10 (and L8 expectation, `~ST-05`) |
| Moment-generating function $M(t)=(q+pe^t)^n$; moments by differentiation; pgf $(q+ps)^n$ (`binom_mgf`, `binom_pgf`) | PSU | L9 *Moment-Generating Functions* + L10 |
| Sum of independent binomials with common $p$ is binomial (Vandermonde / mgf product) (`sum_two_binomials_pmf`) | PSU | L10 (and L9 mgf uniqueness, `~ST-06`) |
| Mode $\lfloor(n+1)p\rfloor$ via the successive-ratio test (`binom_mode`) | PSU / HTZ | L10; HTZ Ch. 2 §2.4 |
| Poisson limit $n\to\infty,\ np=\lambda$ (`_poisson_pmf` benchmark) | PSU | L12 *The Poisson Distribution* (`~ST-09`) |
| Normal / de Moivre–Laplace limit $n\to\infty$, $p$ fixed (`_normal_pdf` benchmark) | PSU | L28 *Approximations for Discrete Distributions* (`~ST-18`) |

## See also
- `~ST-02` (counting techniques) — the binomial coefficient $\binom nk$ that
  weights the pmf (STAT 414 L3); `~ST-05` (discrete RVs & expectation, L7–L8) and
  `~ST-06` (mgf, L9) — the expectation/variance/mgf machinery §4–§5 reuse.
- `~ST-08` (geometric & negative binomial, L11) — the waiting-time duals of the
  same Bernoulli trials.
- Forward limits: `~ST-09` (Poisson, L12 — the rare-event limit of §7) and
  `~ST-18` (CLT & normal approximation, L27–L28 — the large-$n$ limit of §8).
- `~SM-01` (statistical-mechanics foundations) — the fair binomial as two-state
  multiplicity and its $1/\sqrt N$ peak; `~MA-19` (probability & statistics in the
  maths trunk) — the same binomial/normal pair, reused by `~SM-01`.
- Pedagogy: STAT 414 L10 (primary, worked examples); HTZ Ch. 2 (the matching
  text); Wackerly Ch. 3 and Ross Ch. 4 (alternative treatments at chapter level).
