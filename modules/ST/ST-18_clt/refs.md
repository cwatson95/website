# ST-18 — References

| Source (edition) | Location | Notes |
|---|---|---|
| Penn State **STAT 414**, *Probability Theory* (OER, CC BY-NC 4.0) | online.stat.psu.edu/stat414 — **Lesson 27, *The Central Limit Theorem*** (`.../lesson/27`) and **Lesson 28, *Approximations for Discrete Distributions*** (`.../lesson/28`) | **primary**; cited by **lesson** (L27 the CLT for sums/sample means; L28 the normal approximations & continuity correction) |
| Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* (10th ed.) | **Ch. 5, *Distributions of Continuous Type*** (§5.6 *The Central Limit Theorem*, §5.7 *Approximations for Discrete Distributions*) | text STAT 414 follows; cross-cited at **chapter/section level** |
| Wackerly, Mendenhall & Scheaffer, *Mathematical Statistics with Applications* (7th ed.) | **Ch. 7 §7.3–§7.4, *The Central Limit Theorem* & *normal approximation to the binomial*** | optional cross-reference, **section level** |
| Ross, *A First Course in Probability* (10th ed.) | **Ch. 8 §8.3, *The Central Limit Theorem*** (and §8.2 Chebyshev / weak law) | optional cross-reference, **section level** |

> **Granularity.** This trunk has **no textbook PDF on the shelf**: citations are
> to the **STAT 414 OER by lesson number and title** (stable URLs), and to the
> companion texts at **chapter/section level only** — page offsets were **not**
> verified (cf. `~QF-01/refs.md`, where Peskin is likewise cited by section, and
> `~SM-06/refs.md`, where Pathria *is* checked page-by-page because the PDF is on
> the shelf). Lessons 27–28 are quoted below; the standard-edition chapter numbers
> of HTZ/WMS/Ross are stable across printings. The Berry–Esseen constant
> ($C\le0.7655$ van Beek; $\approx0.469$ Shevtsova) is from the research literature,
> not the OER, and is cited only as the analytic bound behind `berry_esseen_bound`.

## Topic → location

| Topic (code symbol) | Source | Lesson / section |
|---|---|---|
| Mean/variance of a sum & sample mean; standard error $\sigma/\sqrt n$ (`pmf_mean`, `pmf_var`, `nfold_pmf`) | PSU L27 / HTZ | L27 / §5.6 |
| **Central limit theorem** $Z_n=(\bar X-\mu)/(\sigma/\sqrt n)\to N(0,1)$ (sum & sample-mean forms) | PSU L27 / HTZ | L27 / §5.6 |
| The limit law $\Phi(z)=\tfrac12[1+\operatorname{erf}(z/\sqrt2)]$, $\varphi$ (`standard_normal_cdf`, `standard_normal_pdf`) | PSU L27 / HTZ | L27 / §5.6 (the normal: `~ST-12`) |
| mgf proof: $M_{Z_n}(t)=[M_Y(t/\sqrt n)]^n\to e^{t^2/2}$; uniqueness theorem | PSU L27 / HTZ | L27 / §5.6 (mgf: `~ST-06`) |
| Convergence by convolution; standardized cdf gap (`convolve_pmf`, `clt_cdf_max_error`, `clt_demo`) | PSU L27 | L27 (convolution: `~ST-16`) |
| Berry–Esseen rate $\sup|F_n-\Phi|\le C\rho/(\sigma^3\sqrt n)$ (`kolmogorov_cdf_error`, `pmf_third_abs_moment`, `berry_esseen_bound`) | HTZ / lit. | §5.6 (asymptotics: `~MA-21`) |
| Normal approximation to the **binomial** $\mathrm{Bin}(n,p)\approx N(np,npq)$ (`binom_cdf`, `normal_approx_binomial`) | PSU L28 / HTZ | L28 / §5.7 (binomial: `~ST-07`) |
| **Continuity correction** $P(X\le k)\approx\Phi(\tfrac{k+0.5-\mu}{\sigma})$; intervals (`normal_approx_binomial_interval`) | PSU L28 / HTZ | L28 / §5.7 |
| **de Moivre–Laplace local limit** $P(X{=}k)\approx\tfrac1\sigma\varphi(\tfrac{k-\mu}\sigma)$ (`de_moivre_laplace_pmf`) | HTZ | §5.7 |
| Normal approximation to the **Poisson** $\mathrm{Poisson}(\lambda)\approx N(\lambda,\lambda)$ (`poisson_cdf`, `normal_approx_poisson`) | PSU L28 / HTZ | L28 / §5.7 (Poisson: `~ST-09`) |
| Approximation error vs $n$/$\lambda$; rule of thumb $np,n(1-p)\ge5$ (`binomial_approx_error_table`, `poisson_approx_max_error`, `normal_approx_applicable`) | PSU L28 | L28 |

## See also
- `~ST-12` (the **normal distribution** — the limit law derived here; its $\Phi$,
  $\varphi$, mgf $e^{\mu t+\sigma^2t^2/2}$ and the closure under addition that the
  CLT upgrades to a *limit*) and `~ST-06` (mgf & uniqueness — the §3 proof engine).
- `~ST-16` (transformations & **sums by convolution** — the exact law of $S_n$
  exhibited in §4) and `~ST-05` (mean/variance of a distribution).
- `~ST-07` (the **binomial** — de Moivre–Laplace, §6–7) and `~ST-09` (the
  **Poisson** — §8); both are large-parameter limits this module makes Gaussian.
- Physics homes: `~SM-01` (Gaussian thermodynamic fluctuations, fractional width
  $1/\sqrt N$ — the **B11** bridge, the de Moivre–Laplace of the two-state system),
  `~PK-01` (kinetic distribution functions and their moments), `~MA-21` (asymptotic
  analysis — the Berry–Esseen $O(n^{-1/2})$ rate and Laplace's method), `~MA-19`
  (the trunk's parent probability survey).
- Forward: `~ST-17` ($\chi^2$, $t$, $F$ sampling distributions) — with the CLT,
  the basis of confidence intervals and hypothesis tests in statistical inference.
- STAT 414 L27–L28 (primary, computational, with worked normal-approximation
  examples); HTZ Ch. 5 §5.6–5.7 (the textbook derivations); WMS Ch. 7 / Ross Ch. 8
  (alternative treatments, with Chebyshev and the weak law of large numbers).
