# ST-17 — The MGF Technique & Normal Sampling Distributions

Seventeenth module of the **PROBABILITY THEORY** trunk (see `modules/ST/list_ST.txt`),
a module-by-module replica of Penn State **STAT 414**. Covers **Lesson 25 — The
Moment-Generating Function Technique** and **Lesson 26 — Random Functions
Associated with Normal Distributions**. This is where the mgf stops being a
bookkeeping device and becomes a *machine for finding distributions*: multiply the
moment-generating functions of independent pieces, recognize the product, and read
off the law of the sum. Pointed at a normal sample, that machine manufactures the
three distributions of classical inference — $\chi^2$, Student's $t$, and
Snedecor's $F$.

- **Prerequisites:** `~ST-06` (moment-generating functions — $M(t)=E[e^{tX}]$, the
  product rule $M_{X+Y}=M_XM_Y$ for independents, and the **uniqueness theorem**
  that lets us recognize a distribution from its mgf), `~ST-12` (the normal — its
  mgf $e^{\mu t+\sigma^2t^2/2}$ and closure under linear maps), `~ST-11` (the gamma
  family — gamma mgf $(1-\theta t)^{-\alpha}$, and the chi-square as gamma
  $(r/2,2)$), `~ST-16` (transformations — $Z^2\sim\chi^2_1$, the change-of-variable
  that turns $T^2$ into $F_{1,r}$).
- **Cross-links:** `~ST-10` (continuous random variables — the pdfs of $t$ and $F$),
  `~MA-12` (the gamma and **Beta** functions normalizing those pdfs), `~ST-18`
  (the central limit theorem — the *limiting* version of "sums of independents
  add their variances"), `~ST-09` (the Poisson process — gammas/Erlang as
  arrival-time sums), `~SM-06` (kinetic theory — a molecule's energy is a
  $\chi^2_3$, a sum of squared velocity components).

## Scope

Two lessons, one engine — the **product rule** $M_{\sum X_i}(t)=\prod_i M_{X_i}(t)$
for independent variables, made decisive by **uniqueness** (`~ST-06`).

**(A) The mgf technique (L25).** To find the law of a sum, multiply mgfs and
recognize the answer. Three closure facts fall straight out:

- **Sum of independent normals is normal.** $X_i\sim N(\mu_i,\sigma_i^2)$ gives
  $\prod e^{\mu_i t+\frac12\sigma_i^2t^2}=e^{(\sum\mu_i)t+\frac12(\sum\sigma_i^2)t^2}$,
  so $\sum X_i\sim N(\sum\mu_i,\sum\sigma_i^2)$; more generally
  $\sum a_iX_i\sim N(\sum a_i\mu_i,\sum a_i^2\sigma_i^2)$ — even a **difference**
  $X_1-X_2\sim N(\mu_1-\mu_2,\sigma_1^2+\sigma_2^2)$ *adds* the variances.
- **Sum of independent gammas (common scale) adds shapes.** $(1-\theta t)^{-\alpha_i}$
  multiply to $(1-\theta t)^{-\sum\alpha_i}$, so $\sum\mathrm{Gamma}(\alpha_i,\theta)
  =\mathrm{Gamma}(\sum\alpha_i,\theta)$.
- **Sum of independent chi-squares adds degrees of freedom.** $(1-2t)^{-r_i/2}$
  multiply to $(1-2t)^{-\sum r_i/2}$. With $Z^2\sim\chi^2_1$ (`~ST-16`), the sum
  $\sum_{i=1}^n Z_i^2\sim\chi^2_n$.

**(B) Random functions of a normal sample (L26).** From $X_1,\dots,X_n$ iid
$N(\mu,\sigma^2)$:

- the **sample mean** $\bar X=\frac1n\sum X_i\sim N(\mu,\sigma^2/n)$ (a linear
  combination with $a_i=1/n$), so the standardized mean
  $Z=(\bar X-\mu)/(\sigma/\sqrt n)$ is *exactly* $N(0,1)$;
- the **sample variance** obeys $(n-1)S^2/\sigma^2\sim\chi^2_{n-1}$, with $\bar X$
  and $S^2$ **independent** (one degree of freedom is spent estimating $\mu$);
- **Student's $t$** $T=Z/\sqrt{V/r}$ ($Z\sim N(0,1)$, $V\sim\chi^2_r$ independent)
  has the density below and $\to N(0,1)$ as $r\to\infty$; in particular
  $(\bar X-\mu)/(S/\sqrt n)\sim t_{n-1}$;
- **Snedecor's $F$** $F=(U/r_1)/(V/r_2)$ ($U\sim\chi^2_{r_1}$, $V\sim\chi^2_{r_2}$
  independent) is the ratio of two scaled chi-squares; and $T^2\sim F_{1,r}$.

The closed-form densities, built from the gamma/Beta functions, are
$$f_T(t)=\frac{\Gamma(\frac{r+1}{2})}{\sqrt{r\pi}\,\Gamma(\frac r2)}
\Big(1+\frac{t^2}{r}\Big)^{-\frac{r+1}{2}},\qquad
f_F(x)=\frac{(r_1/r_2)^{r_1/2}}{B(\frac{r_1}2,\frac{r_2}2)}\,
\frac{x^{r_1/2-1}}{\big(1+\frac{r_1}{r_2}x\big)^{(r_1+r_2)/2}}\ (x>0).$$

## Operations — `code/mgf_technique_sampling.py`  (numpy + stdlib only)

| call | meaning | reference |
|------|---------|-----------|
| `normal_mgf(t, mu, sigma)` | $M(t)=e^{\mu t+\sigma^2t^2/2}$ | L25; `~ST-12` |
| `gamma_mgf(t, alpha, theta)` | $M(t)=(1-\theta t)^{-\alpha}$ | L25; `~ST-11` |
| `chi2_mgf(t, r)` | $M(t)=(1-2t)^{-r/2}$ (gamma, $\theta=2$) | L25; `~ST-11` |
| `product_of_normal_mgfs(t, means, vars)` | $\prod_i M_{X_i}(t)$ — mgf of the sum | L25 |
| `sum_of_normals_via_mgf(means, vars)` | $\sum X_i\sim N(\sum\mu_i,\sum\sigma_i^2)$ → `(mu, var)` | L25 |
| `mgf_of_linear_combination_normals(t, a, means, vars)` | $\prod_i M_{X_i}(a_it)$ | L25 |
| `linear_combination_of_normals(a, means, vars)` | $\sum a_iX_i\sim N(\sum a_i\mu_i,\sum a_i^2\sigma_i^2)$ | L25 |
| `product_of_gamma_mgfs(t, alphas, theta)` | $\prod_i(1-\theta t)^{-\alpha_i}$ | L25 |
| `sum_of_gammas_via_mgf(alphas, theta)` | $\mathrm{Gamma}(\sum\alpha_i,\theta)$ → `(alpha, theta)` | L25; `~ST-11` |
| `product_of_chi2_mgfs(t, dfs)` | $\prod_i(1-2t)^{-r_i/2}$ | L25 |
| `sum_of_chisquares(dfs)` | $\chi^2_{\sum r_i}$ — degrees of freedom add | L25 |
| `square_of_standard_normal_pdf(x)` | $\varphi(\sqrt x)/\sqrt x=\chi^2_1$ pdf ($Z^2\sim\chi^2_1$) | L25; `~ST-16` |
| `sampling_dist_of_mean(mu, sigma2, n)` | $\bar X\sim N(\mu,\sigma^2/n)$ → `(mean, var)` | L26 |
| `standardized_mean_mgf(t, mu, sigma2, n)` | mgf of $(\bar X-\mu)/(\sigma/\sqrt n)=e^{t^2/2}$ | L26 |
| `sample_variance_chi2_df(n)` | $r=n-1$: $(n-1)S^2/\sigma^2\sim\chi^2_{n-1}$ | L26 |
| `students_t_pdf(t, r)` | $\frac{\Gamma(\frac{r+1}2)}{\sqrt{r\pi}\,\Gamma(\frac r2)}(1+\frac{t^2}{r})^{-\frac{r+1}2}$ | L26 |
| `students_t_mean(r)` / `students_t_var(r)` | $0\ (r>1)$; $\dfrac{r}{r-2}\ (r>2)$ | L26 |
| `f_pdf(x, r1, r2)` | $\dfrac{(r_1/r_2)^{r_1/2}}{B(\frac{r_1}2,\frac{r_2}2)}\dfrac{x^{r_1/2-1}}{(1+\frac{r_1}{r_2}x)^{(r_1+r_2)/2}}$ | L26 |
| `f_mean(r2)` / `f_var(r1, r2)` | $\dfrac{r_2}{r_2-2}$; $\dfrac{2r_2^2(r_1+r_2-2)}{r_1(r_2-2)^2(r_2-4)}$ | L26 |
| `t_squared_pdf(w, r)` | density of $T^2$, $=f_F(w;1,r)$ ($T^2\sim F_{1,r}$) | L26; `~ST-16` |
| `beta_function(a, b)` | $B(a,b)=\Gamma(a)\Gamma(b)/\Gamma(a+b)$ | `~MA-12` |

## Use
```python
import math
from mgf_technique_sampling import (
    sum_of_normals_via_mgf, product_of_normal_mgfs, normal_mgf,
    linear_combination_of_normals, sum_of_chisquares, square_of_standard_normal_pdf,
    chi2_pdf, sampling_dist_of_mean, standardized_mean_mgf,
    students_t_pdf, students_t_var, f_mean, t_squared_pdf, f_pdf)

# sum of independent normals: the mgf product IS a normal mgf  ->  params add
sum_of_normals_via_mgf([1.0, -0.5, 2.0], [4.0, 2.25, 1.0])     # (2.5, 7.25)
product_of_normal_mgfs(0.3, [1,-0.5,2], [4,2.25,1])            # 2.9336577
normal_mgf(0.3, 2.5, math.sqrt(7.25))                          # 2.9336577  (equal)

# a difference still ADDS the variances:
linear_combination_of_normals([1, -1], [5, 3], [4, 9])         # (2.0, 13.0)

# chi-squares add d.f.; Z^2 is a chi^2_1:
sum_of_chisquares([3, 5, 2])                                    # 10.0
square_of_standard_normal_pdf(2.0), chi2_pdf(2.0, 1)           # (0.103777, 0.103777)

# sampling distribution of the mean, and its exact standard-normal standardization:
sampling_dist_of_mean(100, 225, 25)                            # (100.0, 9.0)  sigma^2/n
standardized_mean_mgf(0.7, 100, 225, 25)                       # 1.2776213 = e^{0.7^2/2}

# Student t and Snedecor F:
students_t_var(5)                                              # 1.6667 = 5/3
students_t_pdf(0.0, 3)                                         # 0.367553
f_mean(10)                                                     # 1.25 = 10/8
t_squared_pdf(4.0, 6) - f_pdf(4.0, 1, 6)                       # ~0   (T^2 ~ F_{1,r})
```

## Run
```bash
cd code
python3 mgf_technique_sampling.py        # demo: mgf products, sampling dist of mean, t and F
python3 test_mgf_technique_sampling.py   # tests  ->  "All 13 tests passed."
```

## Files
- `notes.md` — the product rule + uniqueness → sums of normals/gammas/chi-squares
  → the sample mean → $(n-1)S^2/\sigma^2\sim\chi^2_{n-1}$ → Student's $t$ and its
  normal limit → Snedecor's $F$ and $T^2=F_{1,r}$; each result tied to a code symbol.
- `code/mgf_technique_sampling.py`, `code/test_mgf_technique_sampling.py`
  (numpy + stdlib `math` only; self-contained — no sibling imports).
- `problems/problems.md` — worked problems (STAT 414 L25–L26; numeric cross-checks
  to the code).
- `refs.md` — citation table (STAT 414 L25–L26 primary; Hogg–Tanis–Zimmerman,
  Wackerly, Ross cross-cited at chapter level).
