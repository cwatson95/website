# ST-10 — References

| Source (edition) | Location | Notes |
|---|---|---|
| Penn State STAT 414, *Probability Theory* (OER, CC BY-NC 4.0) | <https://online.stat.psu.edu/stat414/> — **Lesson 13** *Exploring Continuous Data*, **Lesson 14** *Continuous Random Variables* (.../lesson/13, .../lesson/14) | **primary**; cited at **lesson/sub-lesson level** (e.g. L14.3) |
| Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* (10th ed.) | **Ch. 3** *Continuous Distributions* (§3.1–3.2 the uniform; pdf/cdf, expectation) | the text STAT 414 follows; cross-cited at **chapter level** |
| Wackerly, Mendenhall & Scheaffer, *Mathematical Statistics with Applications* (7th ed.) | **Ch. 4** *Continuous Variables and Their Probability Distributions* (§4.1–4.4 pdf/cdf, expected values; §4.4 the uniform) | cross-cited at **chapter level** |
| Sheldon Ross, *A First Course in Probability* (9th/10th ed.) | **Ch. 5** *Continuous Random Variables* (§5.1–5.3 pdf, expectation, the uniform) | cross-cited at **chapter level** |

> **Granularity.** Citations are given at **OER-lesson level** (STAT 414 Lessons
> 13–14) and, for the cross-referenced textbooks, at **chapter level only**: this
> trunk has **no PDF on the shelf**, so printed↔PDF page offsets were **not**
> verified (cf. `~QF-01/refs.md`, which cites Peskin by section, and `~SM-06/refs.md`,
> which *does* verify Pathria page-by-page because that PDF is shelved). Lesson and
> chapter numbers are stable across printings; the material — pdf/cdf, expectation
> as an integral, percentiles, the continuous uniform — is entirely standard.

## Topic → location

| Topic (code symbol) | Source | Lesson / chapter |
|---|---|---|
| pdf axioms $f\ge0$, $\int f=1$ (`pdf_is_normalized`, `_integrate`) | PSU | L14.1 *Continuous Random Variables*; HTZ Ch. 3 |
| cdf $F(x)=\int_{-\infty}^x f$, $f=F'$ (`cdf_from_pdf`) | PSU | L14.2; HTZ Ch. 3; WMS Ch. 4 §4.2 |
| intervals $P(a{<}X{<}b)=F(b)-F(a)$, $P(X{=}x)=0$ (`prob_between`) | PSU | L14.2; Ross Ch. 5 §5.1 |
| expectation $E[X]=\int x f$, LOTUS $E[g(X)]$ (`expectation_continuous`, `expectation_of`, `moment_continuous`) | PSU | L14.3 *Mean and Variance*; HTZ Ch. 3; WMS Ch. 4 §4.3 |
| variance $E[X^2]-(E[X])^2$ (`variance_continuous`) | PSU | L14.3; WMS Ch. 4 §4.3 |
| percentiles/quantiles $F(\pi_p)=p$, median, IQR (`quantile`, `median_continuous`) | PSU | L13 *Exploring Continuous Data*; L14.4 |
| continuous uniform $U(a,b)$: pdf, cdf, mean $\tfrac{a+b}2$, var $\tfrac{(b-a)^2}{12}$ (`uniform_pdf/cdf/mean/var`, `uniform_quantile`) | PSU | L14.6 *Uniform Distributions*; HTZ Ch. 3 §3.2; WMS Ch. 4 §4.4; Ross Ch. 5 §5.3 |
| point mass / Dirac-delta limit of a density (`point_mass_pdf`) | `~MA-15` | (delta as the density of a point mass — Boas Ch. 8 §11) |

## See also
- `~ST-05` (discrete random variables & expectation) — the discrete originals of
  every formula here; the $\sum\to\int$ dictionary, with `~MA-15` (the Dirac
  delta) as the bridge that writes a discrete pmf as a sum of deltas.
- `~ST-06` (moment-generating functions) — the §4 moments repackaged as
  $M(t)=\int e^{tx}f\,dx$; forward to `~ST-11` (exponential/gamma/chi-square, the
  **gamma function**) and `~ST-12` (the normal, the **Gaussian integral**) — the
  named continuous laws this machinery exists to handle.
- `~SM-01`, `~SM-06` — the same continuous-density calculus in statistical
  physics (Maxwell–Boltzmann speed pdf: $\int f=1$, $E[g(v)]=\int g f$).
- STAT 414 OER (primary, computational worked examples); Hogg–Tanis–Zimmerman
  (the matching textbook); Wackerly and Ross (alternative treatments at chapter level).
