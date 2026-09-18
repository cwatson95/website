# ST-06 — References

| Source (edition) | Location | Notes |
|---|---|---|
| Penn State **STAT 414**, *Introduction to Probability Theory* (OER, CC BY-NC 4.0) | `online.stat.psu.edu/stat414` — **Lesson 9** *Moment Generating Functions* (§9.1 definition; §9.2 finding moments; §9.3 sums) | **primary**; the trunk replicates this course module-by-module |
| Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* | **Ch. 3** (discrete distributions; mgf, §3.x) | the text STAT 414 follows; cited at **chapter level** |
| Wackerly, Mendenhall & Scheaffer, *Mathematical Statistics with Applications* | **Ch. 3** (mgf §3.9; §3.11 the mgf technique) | cross-cited at **chapter level** |
| Ross, *A First Course in Probability* | **Ch. 7** (moment generating functions) | cross-cited at **chapter level** |

> **Granularity.** Citations are at the **OER lesson level** (and chapter level
> for the printed texts). There is **no PDF on this trunk's shelf**, so printed↔PDF
> page offsets are **not** verified — every reference is given by lesson/section
> number and title or by chapter, never by page (cf. `~QF-01/refs.md`, which is
> likewise section-level). The mgf material is standard and stable across editions;
> the STAT 414 lesson page may be opened to confirm a definition if needed.

## Topic → location

| Topic (code symbol) | Source | Lesson / chapter |
|---|---|---|
| Definition $M(t)=E[e^{tX}]$, existence on $(-h,h)$, $M(0)=1$ (`mgf`, `mgf_continuous`, `cgf`) | PSU L9 | §9.1 *Moment Generating Functions* |
| Moments by differentiation $M^{(k)}(0)=E[X^k]$; mean $M'(0)$, variance $M''(0)-[M'(0)]^2$ (`moment_from_mgf`, `mean_from_mgf`, `var_from_mgf`) | PSU L9 | §9.2 *Finding Moments* |
| Direct $E[X]$, $\mathrm{Var}(X)$ (the ground truth, `mean`, `variance`) | PSU L8 | Lesson 8 *Mathematical Expectation* (`~ST-05`) |
| mgf of a sum of independents $=$ product; convolution (`mgf_of_sum`, `convolve_dists`) | PSU L9 | §9.3; HTZ Ch. 3 |
| Uniqueness theorem (mgf determines the distribution); the mgf technique | PSU L9 | §9.3; WMS Ch. 3 §3.11 (`~ST-17`) |
| Closed-form mgfs: Bernoulli/binomial/geometric/Poisson (`bernoulli_mgf`, `binomial_mgf`, `geometric_mgf`, `poisson_mgf`) | PSU L9–L12 | Lessons 10–12 (`~ST-07`/`~ST-08`/`~ST-09`) |
| Closed-form mgfs: exponential/gamma/normal (`exponential_mgf`, `gamma_mgf`, `normal_mgf`) | PSU L15–L16 | Lessons 15–16 (`~ST-11`/`~ST-12`) |
| Cumulants $\kappa_k=K^{(k)}(0)$, $K=\ln M$; additivity over independent sums (`cumulant_from_mgf`) | HTZ Ch. 3 | (cumulant generating function) |
| mgf as the two-sided Laplace transform at $s=-t$; uniqueness $=$ invertibility | — | `~MA-10` (Laplace/integral transforms) |
| $\ln Z(\beta)$ generates the energy cumulants $U=-\partial_\beta\ln Z$, $\mathrm{Var}(E)=\partial_\beta^2\ln Z$ | — | `~SM-03` (partition function; Pathria Ch. 3) |

## See also
- `~ST-05` (discrete random variables & expectation) — the moments and variance
  this module generates; `mean`/`variance` are its `~ST-05` definitions, used as
  the numeric ground truth.
- `~MA-10` (Laplace & integral transforms) — the mgf is the bilateral Laplace
  transform of the density at $s=-t$; §5's product rule is the convolution theorem
  and §6's uniqueness is transform invertibility.
- `~SM-03` (classical statistical mechanics) — the partition function $\ln Z(\beta)$
  is the cumulant generating function of the energy; mean energy and heat capacity
  are its first two cumulants (Pathria Ch. 3; `~SM-01` for the counting picture).
- Forward: `~ST-17` (the mgf technique & the $\chi^2$/$t$/$F$ sampling
  distributions), `~ST-18` (the central limit theorem via the standardized-sum
  mgf), and the named-law lessons `~ST-07`–`~ST-12` whose mgfs appear in §7.
- STAT 414 Lesson 9 (primary); HTZ Ch. 3 and WMS Ch. 3 (the standard textbook
  treatments); Ross Ch. 7 (a concise alternative).
