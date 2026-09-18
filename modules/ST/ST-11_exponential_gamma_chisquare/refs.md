# ST-11 — References

| Source (edition) | Locator | Notes |
|---|---|---|
| Penn State **STAT 414**, *Probability Theory* (OER, CC BY-NC 4.0) | `online.stat.psu.edu/stat414/lesson/15` | **primary**; **Lesson 15** *Exponential, Gamma and Chi-Square Distributions* — the module is a faithful replica of L15 |
| Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* (10th ed.) | Ch. 3 (*Continuous Distributions*) | the text STAT 414 follows; cross-cited at **chapter level** |
| Wackerly, Mendenhall & Scheaffer, *Mathematical Statistics with Applications* (7th ed.) | Ch. 4 (*Continuous Variables and Their Probability Distributions*) | cross-cited at **chapter level** (gamma, exponential, chi-square §4.6–4.7) |
| Ross, *A First Course in Probability* (9th ed.) | Ch. 5 (*Continuous Random Variables*) | cross-cited at **chapter level** (exponential & gamma, §5.5–5.6) |

> **Granularity.** Citations are **OER-lesson-level**: Penn State STAT 414 is
> organized by *Lesson → subsection* (here Lesson 15.1–15.4), and that is the unit
> we cite — there is **no textbook PDF on this shelf**, so Hogg–Tanis–Zimmerman,
> Wackerly and Ross are given by **chapter only** (page offsets are not verified;
> cf. `~QF-01/refs.md`). The exponential/gamma/chi-square definitions are standard
> and stable across editions; the lesson subsection numbers (L15.1 the gamma
> function, L15.2 exponential, L15.3 gamma, L15.4 chi-square) follow the current
> STAT 414 site and may be re-lettered in future revisions.

## Topic → location

| Topic (code symbol) | Source | Lesson / chapter |
|---|---|---|
| Gamma function $\Gamma(\alpha)=\int_0^\infty t^{\alpha-1}e^{-t}dt$, recursion $\Gamma(\alpha{+}1)=\alpha\Gamma(\alpha)$, $\Gamma(n)=(n{-}1)!$, $\Gamma(\tfrac12)=\sqrt\pi$ (`gamma_function`, `gamma_lanczos`) | STAT 414 | L15.1 *The Gamma Function* |
| Exponential pdf/cdf/survival, mean $1/\lambda$, variance $1/\lambda^2$, mgf $\lambda/(\lambda-t)$ (`exponential_pdf`, `exponential_cdf`, `exponential_survival`, `exponential_mean`, `exponential_var`, `exponential_mgf`) | STAT 414 | L15.2 *The Exponential Distribution* |
| Memorylessness $P(X{>}s{+}t\mid X{>}s)=P(X{>}t)$ (`exp_memoryless_check`) | STAT 414 | L15.2 *The Exponential Distribution* |
| Gamma pdf $x^{\alpha-1}e^{-x/\theta}/(\Gamma(\alpha)\theta^\alpha)$, mean $\alpha\theta$, variance $\alpha\theta^2$, mgf $(1-\theta t)^{-\alpha}$ (`gamma_pdf`, `gamma_mean`, `gamma_var`, `gamma_mgf`) | STAT 414 | L15.3 *The Gamma Distribution* |
| Gamma cdf / regularized lower incomplete gamma $P(\alpha,x/\theta)$ (`gamma_cdf`, `lower_incomplete_gamma_regularized`) | STAT 414 | L15.3 *The Gamma Distribution* |
| Sum of $\alpha$ iid exponentials is gamma (Erlang waiting time); convolution & mgf proof (`convolve_two_exponentials_pdf`, `simulate_sum_of_exponentials`) | STAT 414 | L15.3 (with the mgf technique, `~ST-17` / L25) |
| Chi-square $=$ gamma$(r/2,2)$, mean $r$, variance $2r$, mgf $(1-2t)^{-r/2}$, $\chi^2_2=$Exp$(\tfrac12)$ (`chi2_pdf`, `chi2_cdf`, `chi2_mean`, `chi2_var`, `chi2_mgf`) | STAT 414 | L15.4 *The Chi-Square Distribution* |

## See also
- `~MA-12` (special functions — the gamma function $\Gamma$, its recursion and
  half-integer values) — the analytic backbone of every normalizer here.
- `~ST-06` (moment-generating functions) — the device for all the means/variances
  and for the sum-of-exponentials proof; `~ST-10` (continuous random variables) —
  the pdf/cdf/percentile framework these distributions inhabit.
- `~ST-09` (the Poisson process) — exponential inter-arrivals, gamma arrival times;
  `~ST-08` (geometric/negative binomial) — the discrete memoryless analogue.
- Forward: `~ST-17` (the MGF technique & normal sampling distributions — chi-square
  $=\sum Z_i^2$, Student-$t$, $F$), `~ST-12` (the normal — $\chi^2_1=Z^2$,
  $\Gamma(\tfrac12)=\sqrt\pi$).
- `~SM-06` (kinetic theory — molecular energy $2E/kT\sim\chi^2_3$, the gamma of
  shape $\tfrac32$; the Maxwell speed law as the matching $\chi$ distribution).
- STAT 414 Lesson 15 (primary, worked examples); Hogg–Tanis–Zimmerman Ch. 3,
  Wackerly Ch. 4, Ross Ch. 5 (parallel treatments, chapter level).
