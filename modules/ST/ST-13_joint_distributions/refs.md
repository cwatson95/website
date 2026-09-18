# ST-13 — References

This trunk has **no textbook PDF on the shelf**. The **primary** source is the
Penn State STAT 414 Open Educational Resource, cited **by lesson number and
title**; the text STAT 414 follows is cross-referenced at **chapter level** only.

| Source | Locator | Notes |
|---|---|---|
| Penn State STAT 414, *Probability Theory* (OER) | `https://online.stat.psu.edu/stat414/`, lesson pages `.../lesson/17` and `.../lesson/20` | **primary**; CC BY-NC 4.0. **L17** *Distributions of Two Discrete Random Variables*, **L20** *Distributions of Two Continuous Random Variables* |
| Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* (10th ed.) | Ch. 4 *Bivariate Distributions* | the text STAT 414 follows; cross-cited at **chapter level** |
| Wackerly, Mendenhall & Scheaffer, *Mathematical Statistics with Applications* (7th ed.) | Ch. 5 *Multivariate Probability Distributions* | optional cross-reference (joint/marginal/independence/$E[g(X,Y)]$) |
| Ross, *A First Course in Probability* (10th ed.) | Ch. 6 *Jointly Distributed Random Variables* | optional cross-reference (joint cdf, independence, expectation of sums) |

> **Granularity.** Citations are **OER-lesson-level**. Lesson numbers/titles are
> from the live STAT 414 site (Section 4, *Bivariate Distributions*); the
> chapter-level book references are standard locations for joint distributions and
> were **not** verified against specific page numbers (we hold no PDF of these
> texts). Tighten to section/example level by opening the lesson pages above if
> needed. STAT 414 follows Hogg–Tanis–Zimmerman, so HTZ Ch. 4 is the closest book
> chapter throughout.

## Topic → location

| Topic (code symbol) | Source | Lesson / chapter |
|---|---|---|
| Joint pmf $f(x,y)=P(X{=}x,Y{=}y)$, validity $\sum f=1$ (`joint_pmf_is_valid`) | PSU | **L17** *Two Discrete Random Variables* |
| Discrete marginals $f_X(x)=\sum_y f$, $f_Y(y)=\sum_x f$ (`marginal_x`, `marginal_y`) | PSU | **L17** |
| Discrete independence $f(x,y)=f_X f_Y$ (`independent_rv_check`) | PSU | **L17** |
| Bivariate LOTUS $E[g(X,Y)]=\sum g\,f$; means, $E[XY]$, linearity (`expectation_joint`) | PSU | **L17** |
| Joint / marginal cdf $F(x,y)=P(X\le x,Y\le y)$ (`joint_cdf`, `marginal_cdf_x`) | PSU | **L17** |
| Joint pdf $f(x,y)\ge0$, $\iint f=1$, normalizing constant (`joint_pdf_is_valid`, `normalize_joint_pdf`) | PSU | **L20** *Two Continuous Random Variables* |
| Continuous marginals $f_X(x)=\int f\,dy$ (`marginal_pdf_x`, `marginal_pdf_y`) | PSU | **L20** |
| Continuous independence, grid factorization test (`independent_pdf_check`) | PSU | **L20** |
| Continuous LOTUS $E[g]=\iint g\,f$ (`expectation_joint_continuous`) | PSU | **L20** |
| Continuous joint cdf $F=\iint f$, $f=\partial^2 F/\partial x\,\partial y$ (`joint_cdf_continuous`) | PSU | **L20** |
| Double integrals / volume under a surface (`_integrate2d`) | HTZ | Ch. 4 (and `~MA-15`) |
| Bivariate distributions, marginals, independence, $E[g(X,Y)]$ — book treatment | HTZ | Ch. 4 *Bivariate Distributions* |

## See also

- `~ST-05` (a single discrete random variable: pmf, cdf, $E[X]$, variance) and
  `~ST-10`/`~ST-12` (continuous RVs) — the one-variable theory this module lifts;
  each marginal is one of those.
- `~ST-14` (covariance, correlation, conditional distributions — STAT 414 **L18,
  L19**, HTZ Ch. 4) — the immediate sequel: $\mathrm{Cov}=E[XY]-E[X]E[Y]$ is the
  expectation gap of §4, and $f(x\mid y)=f(x,y)/f_Y(y)$ uses this module's joint and
  marginals.
- `~ST-15` (bivariate normal — STAT 414 **L21**) — the headline continuous joint
  density; `~ST-06` (mgf) — the joint mgf factors iff independent; `~ST-16`
  (transformations of two RVs — sums by convolution).
- `~MA-15` (multiple integrals) — the double integral that replaces the double sum;
  `~SM-01` (multiplicity, independence of subsystems) — the same product rule in
  statistical physics.
- STAT 414 Lessons 17 & 20 (primary, with worked examples); HTZ Ch. 4 (book
  development); Wackerly Ch. 5 and Ross Ch. 6 (alternative treatments, optional).
