# ST-17 — References

| Source (edition) | Location | Notes |
|---|---|---|
| Penn State **STAT 414**, *Probability Theory* (OER, CC BY-NC 4.0) | online.stat.psu.edu/stat414 — **Lesson 25, *The Moment-Generating Function Technique*** (`.../lesson/25`) and **Lesson 26, *Random Functions Associated with Normal Distributions*** (`.../lesson/26`) | **primary**; cited by **lesson** (L25 the technique & sums; L26 the sample mean, $\chi^2$, $t$, $F$) |
| Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* (10th ed.) | **Ch. 5, *Distributions of Continuous Type*** (§5.4 the normal & its mgf; §5.5 distributions of $\bar X$ and $S^2$; §5.6 the $t$ and $F$ distributions) | text STAT 414 follows; cross-cited at **chapter/section level** |
| Wackerly, Mendenhall & Scheaffer, *Mathematical Statistics with Applications* (7th ed.) | **Ch. 7, *Sampling Distributions and the Central Limit Theorem*** (§7.2 sampling distributions related to the normal: $\chi^2$, $t$, $F$) | optional cross-reference, **section level** |
| Ross, *A First Course in Probability* (10th ed.) | **Ch. 6 §6.3, *Sums of Independent Random Variables*** and **Ch. 7 §7.7, the mgf method**; **Ch. 6 §6.4** ($\chi^2$, $t$, $F$) | optional cross-reference, **section level** |

> **Granularity.** This trunk has **no textbook PDF on the shelf**: citations are
> to the **STAT 414 OER by lesson number and title** (stable URLs), and to the
> companion texts at **chapter/section level only** — page offsets were **not**
> verified (cf. `~QF-01/refs.md`, where Peskin is likewise cited by section, and
> `~SM-06/refs.md`, where Pathria *is* checked page-by-page because the PDF is on
> the shelf). Lessons 25–26 are cited whole; the standard-edition chapter numbers
> of HTZ/WMS/Ross are stable across printings. The $t$ and $F$ density formulas and
> their moment constraints follow the standard parameterization used by STAT 414.

## Topic → location

| Topic (code symbol) | Source | Lesson / section |
|---|---|---|
| The mgf technique: $M_{\sum X_i}=\prod M_{X_i}$ + uniqueness; recognized closed forms (`normal_mgf`, `gamma_mgf`, `chi2_mgf`, `product_of_*`) | PSU L25 / HTZ | L25 / §5.4 (mgf: `~ST-06`) |
| Sum / linear combination of independent normals is normal (`sum_of_normals_via_mgf`, `linear_combination_of_normals`, `mgf_of_linear_combination_normals`) | PSU L25 / HTZ | L25 *The MGF Technique* / §5.4 (`~ST-12`) |
| Sum of common-scale gammas adds shapes; chi-squares add d.f. (`sum_of_gammas_via_mgf`, `sum_of_chisquares`) | PSU L25 / HTZ | L25 / §5.4 (`~ST-11`) |
| $Z^2\sim\chi^2_1$; $\sum_{i=1}^n Z_i^2\sim\chi^2_n$ (`square_of_standard_normal_pdf`, `chi2_pdf`) | PSU L25 / HTZ | L25 / §5.4 (transform: `~ST-16`) |
| Sampling distribution of the mean $\bar X\sim N(\mu,\sigma^2/n)$; standardized mean is $N(0,1)$ (`sampling_dist_of_mean`, `standardized_mean_mgf`) | PSU L26 / HTZ | L26 / §5.5 |
| $(n-1)S^2/\sigma^2\sim\chi^2_{n-1}$; independence of $\bar X$ and $S^2$ (`sample_variance_chi2_df`) | PSU L26 / HTZ | L26 / §5.5 |
| Student's $t$: $T=Z/\sqrt{V/r}$, pdf, mean $0$, variance $r/(r-2)$, $t_r\to N(0,1)$ (`students_t_pdf`, `students_t_mean`, `students_t_var`) | PSU L26 / HTZ | L26 *Random Functions...* / §5.6 |
| Snedecor's $F$: $F=(U/r_1)/(V/r_2)$, pdf via Beta, mean $r_2/(r_2-2)$; $T^2\sim F_{1,r}$ (`f_pdf`, `f_mean`, `f_var`, `t_squared_pdf`, `beta_function`) | PSU L26 / HTZ | L26 / §5.6 (Beta: `~MA-12`) |

## See also
- `~ST-06` (moment-generating functions — the product rule and **uniqueness
  theorem** that the whole technique stands on) and `~ST-12` (the normal — its mgf
  $e^{\mu t+\sigma^2t^2/2}$, closed under the linear maps of §2 and §5).
- `~ST-11` (exponential/gamma/$\chi^2$ — the gamma mgf $(1-\theta t)^{-\alpha}$ of
  §3 and the chi-square as gamma $(r/2,2)$) and `~ST-16` (transformations —
  $Z^2\sim\chi^2_1$ and the $T^2=F_{1,r}$ change of variable).
- Forward: `~ST-18` (**central limit theorem** — the limiting version of §2's
  closure under addition; WMS Ch. 7, HTZ Ch. 5).
- `~ST-10` (continuous random variables — the $t$/$F$ pdfs) and `~MA-12` (gamma and
  **Beta** functions normalizing them); `~ST-09` (the Poisson process — gamma sums
  as Erlang arrival times).
- Physics home: `~SM-06` (kinetic theory — the scaled molecular energy $2E/kT$ is a
  $\chi^2_3$, a sum of three squared standard normals).
- STAT 414 L25–L26 (primary, computational); HTZ Ch. 5 §5.4–5.6 (the textbook
  derivations of the $t$ and $F$ densities); WMS Ch. 7 / Ross Ch. 6 (alternative
  treatments of sampling distributions).
