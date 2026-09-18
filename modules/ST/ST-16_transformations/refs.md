# ST-16 — References

| Source (edition) | Locator | Notes |
|---|---|---|
| Penn State **STAT 414**, *Probability Theory* (OER, CC BY-NC 4.0) | `online.stat.psu.edu/stat414/lesson/22`–`/24` | **primary**; cited by **lesson number & title** (L22–L24, Section 5 *Distributions of Functions of Random Variables*) |
| Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* (10th ed.) | Ch. 5 | the text STAT 414 follows; cross-cited at **chapter/section level** (§5.1 one variable, §5.2 two variables, §5.3 several variables) |
| Wackerly, Mendenhall & Scheaffer, *Mathematical Statistics with Applications* (7th ed.) | Ch. 6 | cross-cited at **chapter level** (*Functions of Random Variables*: distribution-function, transformation, and mgf methods) |
| Ross, *A First Course in Probability* (10th ed.) | Ch. 6 §6.7; Ch. 7 | cross-cited at **chapter level** (distributions of functions; sums of independent variables) |

> **Granularity.** This trunk has **no textbook PDF on the shelf**: the primary
> citations are to the **STAT 414 OER lesson pages** (lesson number + title, stable
> across the live site). The Hogg–Tanis–Zimmerman, Wackerly, and Ross
> cross-references are given at **chapter/section level only** — printed↔PDF page
> offsets were **not** verified (cf. `~QF-01/refs.md`, which cites a shelved PDF by
> section). STAT 414 Section 5 (Lessons 22–28) is the "Distributions of Functions
> of Random Variables" section; this module is L22–L24, with the mgf technique
> (L25–L26) in `~ST-17` and the CLT (L27–L28) in `~ST-18`.

## Topic → location

| Topic (code symbol) | Source | Lesson / section |
|---|---|---|
| The **cdf (distribution-function) method**, $F_Y(y)=P(g(X)\le y)$ (`cdf_of_Y`, `pdf_of_Y_cdf_method`) | PSU | **L22** *Functions of One Random Variable* |
| **Change-of-variables** formula $f_Y=f_X(g^{-1}(y))\lvert dx/dy\rvert$ for monotone $g$; multi-branch sum (`change_of_variables_1d`) | PSU | **L22**; HTZ §5.1 |
| **Probability integral transform** $F_X(X)\sim U(0,1)$ and inverse-transform sampling (`probability_integral_transform_pdf`, `exp_quantile`) | PSU | **L22**; HTZ §5.1 |
| **2-D Jacobian transformation** $f_{UV}=f_{XY}(x,y)\lvert J\rvert$, $J=\det\partial(x,y)/\partial(u,v)$ (`jacobian_det_2d`, `jacobian_transform_2d`) | PSU | **L23** *Transformations of Two Random Variables*; HTZ §5.2; `~MA-03` |
| **Convolution** $f_{X+Y}=\int f_X(t)f_Y(z-t)\,dt$; sum of two $U(0,1)$ $\to$ triangular (`convolution`, `sum_two_uniforms_pdf`, `triangular_pdf`) | PSU | **L23**; HTZ §5.2; `~MA-09` |
| **Several independent variables**: sum of $n$ $\mathrm{Exp}(\lambda)\to$ Gamma$(n,\lambda)$ (Erlang) (`sum_n_exponentials_pdf`, `gamma_pdf`) | PSU | **L24** *Several Independent Random Variables*; HTZ §5.3 |
| Base laws transformed here: uniform, exponential, gamma, normal (`uniform_pdf`, `exp_pdf`, `gamma_pdf`, `normal_pdf`) | PSU | L10 (uniform), L15 (exponential/gamma), L16 (normal) — see `~ST-10`, `~ST-11`, `~ST-12` |
| $Z^2=\chi^2_1$ as a transformation; setup for $\chi^2/t/F$ sampling laws | PSU | L23–L26 (the mgf technique itself is `~ST-17`) |

## See also
- `~ST-17` (the **MGF technique** & normal sampling distributions, STAT 414 L25–L26)
  — convolution here $\leftrightarrow$ products of mgfs there; the $\chi^2_1=Z^2$ of
  §1 generates the chi-square, Student-$t$, and $F$ families; `~ST-06` (mgfs).
- `~MA-03` (coordinate systems & **Jacobians**) — the area-rescaling determinant
  $|J|$ of the 2-D rule; `~MA-09` (Fourier & **convolution**) — the transform-domain
  twin of summing independents, and the analytic backbone of `~ST-18` (CLT).
- `~ST-10` (continuous RVs / uniform), `~ST-11` (exponential, gamma, chi-square,
  the $\Gamma$ function), `~ST-12` (normal), `~ST-13` (joint distributions) — the
  prerequisites whose laws are transformed; `~MA-19` (probability & statistics).
- `~SM-06` (kinetic theory) — the Maxwell speed distribution is a physics
  change-of-variables from a Gaussian velocity vector to its magnitude.
- STAT 414 OER (primary, computational, free); Hogg–Tanis–Zimmerman Ch. 5 (the
  followed text); Wackerly Ch. 6 and Ross Ch. 6–7 (alternative treatments of the
  three methods).
