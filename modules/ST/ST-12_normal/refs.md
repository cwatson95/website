# ST-12 — References

| Source (edition) | Location | Notes |
|---|---|---|
| Penn State **STAT 414**, *Probability Theory* (OER, CC BY-NC 4.0) | online.stat.psu.edu/stat414 — **Lesson 16, *Normal Distributions*** (`.../lesson/16`) | **primary**; cited by **lesson/subsection** (L16.1 the pdf, L16.2 standardizing & the empirical rule, L16.3 the cdf & percentiles) |
| Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* (10th ed.) | **Ch. 5, *Distributions of Continuous Type*** (§5.4 *The Normal Distribution*) | text STAT 414 follows; cross-cited at **chapter/section level** |
| Wackerly, Mendenhall & Scheaffer, *Mathematical Statistics with Applications* (7th ed.) | **Ch. 4 §4.5, *The Normal Probability Distribution*** | optional cross-reference, **section level** |
| Ross, *A First Course in Probability* (10th ed.) | **Ch. 5 §5.4, *The Normal Random Variable*** | optional cross-reference, **section level** |

> **Granularity.** This trunk has **no textbook PDF on the shelf**: citations are
> to the **STAT 414 OER by lesson number and title** (stable URLs), and to the
> companion texts at **chapter/section level only** — page offsets were **not**
> verified (cf. `~QF-01/refs.md`, where Peskin is likewise cited by section, and
> `~SM-06/refs.md`, where Pathria *is* checked page-by-page because the PDF is on
> the shelf). Lesson 16's three subsections L16.1–L16.3 are quoted below; the
> standard-edition chapter numbers of HTZ/WMS/Ross are stable across printings.

## Topic → location

| Topic (code symbol) | Source | Lesson / section |
|---|---|---|
| Gaussian integral $\int e^{-x^2/2}dx=\sqrt{2\pi}$ (`gaussian_integral_check`, `SQRT_2PI`) | PSU L16 / HTZ | L16.1 / §5.4 |
| The normal pdf $f(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-(x-\mu)^2/2\sigma^2}$; symmetry, mode, inflection (`normal_pdf`, `standard_normal_pdf`) | PSU L16 / HTZ | L16.1 *The Normal Distribution* / §5.4 |
| Standardizing $Z=(X-\mu)/\sigma$, the $Z$-score (`standardize`) | PSU L16 / HTZ | L16.2 / §5.4 |
| Mean $\mu$ and variance $\sigma^2$ by integration (`normal_mean_by_integration`, `normal_variance_by_integration`) | PSU L16 / HTZ | L16.1 / §5.4 |
| Moment-generating function $M(t)=e^{\mu t+\sigma^2 t^2/2}$; moments by differentiation (`normal_mgf`, `mgf_moment`) | PSU L16 / HTZ | L16.1 / §5.4 (mgf: `~ST-06`) |
| Standard-normal cdf $\Phi(z)=\tfrac12[1+\operatorname{erf}(z/\sqrt2)]$; general $F(x)=\Phi((x-\mu)/\sigma)$ (`standard_normal_cdf`, `normal_cdf`, `normal_interval_prob`) | PSU L16 / HTZ | L16.3 *Finding Probabilities* / §5.4 |
| The 68–95–99.7 (empirical) rule $P(|Z|\le k)=2\Phi(k)-1$ (`empirical_rule`) | PSU L16 | L16.2 |
| Percentiles / inverse cdf $z_p=\Phi^{-1}(p)$ by bisection; $x_p=\mu+\sigma z_p$ (`probit`, `normal_quantile`) | PSU L16 | L16.3 *Finding Percentiles* |

## See also
- `~ST-10` (continuous random variables — pdf/cdf/percentiles, the uniform whose
  inverse-cdf transform seeds `probit`) and `~ST-11` (exponential/gamma/$\chi^2$ —
  the $\Gamma(\tfrac12)=\sqrt\pi$ behind §1, and the family the normal joins).
- `~ST-06` (moment-generating functions — the $M(t)=e^{\mu t+\sigma^2t^2/2}$ of §6
  and the uniqueness theorem used in `~ST-18`).
- Forward: `~ST-18` (**central limit theorem** & normal approximation — WMS Ch. 7,
  HTZ Ch. 5/8), `~ST-15` (bivariate normal), `~ST-17` ($\chi^2$, $t$, $F$ from
  normal samples).
- Physics homes: `~SM-01` (Gaussian thermodynamic fluctuations — de Moivre–Laplace
  of the two-state system), `~QM-07` (the minimum-uncertainty Gaussian wavepacket),
  `~MA-19` (the trunk's parent probability survey), `~MA-10` (Laplace/Fourier
  transforms behind the mgf and the wavepacket's self-Fourier property).
- STAT 414 L16 (primary, computational, with $\Phi$-tables); HTZ Ch. 5 (the
  textbook derivations); WMS Ch. 4 / Ross Ch. 5 (alternative treatments).
