# ST-02 — References

| Source (edition) | Location | Notes |
|---|---|---|
| Penn State **STAT 414**, *Introduction to Probability Theory* (OER, CC BY-NC 4.0) | `online.stat.psu.edu/stat414/` → **Lesson 3: Counting Techniques** (`/lesson/3`) | **primary**; cited by lesson/subsection (L3.1 multiplication principle, L3.2 permutations & combinations) |
| Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* (the text STAT 414 follows) | **Ch. 1** (Probability) | cross-cited at **chapter level** (§1.4 methods of enumeration) |
| Wackerly, Mendenhall & Scheaffer, *Mathematical Statistics with Applications* | **Ch. 2** (Probability) | cross-cited at **chapter level** (§2.6 combinatorial analysis) |
| Ross, *A First Course in Probability* | **Ch. 1** (Combinatorial Analysis) | cross-cited at **chapter level** (binomial & multinomial theorems) |

> **Granularity.** This trunk has **no textbook PDF on the shelf**: the **only**
> verifiable primary source is the STAT 414 OER, cited by **lesson number and
> title** (here Lesson 3). The Hogg–Tanis–Zimmerman, Wackerly and Ross references
> are given at **chapter level only** — STAT 414 follows HTZ, but we do not have
> the PDFs, so **page offsets are not verified** and no page numbers are quoted.
> The material (the four sampling schemes, Pascal's rule, the binomial/multinomial
> theorems) is entirely standard and edition-stable; tighten to section level by
> opening the lesson page above. Mirrors the granularity note of `~QF-01/refs.md`.

## Topic → location

| Topic (code symbol) | Source | Lesson / chapter |
|---|---|---|
| Multiplication (fundamental counting) principle; $n^k$ ordered with replacement (`multiplication_principle`, `ordered_with_replacement`) | PSU | L3.1 *The Multiplication Principle* |
| Factorial $n!$, empty product $0!=1$ (`factorial`) | PSU / HTZ | L3.2; HTZ Ch.1 |
| Permutations $P(n,k)=n!/(n-k)!$ (ordered, no replacement) (`permutations`) | PSU | L3.2 *Permutations* |
| Combinations $\binom{n}{k}=n!/[k!(n-k)!]$; $P=\binom{n}{k}k!$; symmetry (`combinations`) | PSU | L3.2 *Combinations* |
| Distinguishable permutations / multinomial $n!/(k_1!\cdots k_m!)$ (`multinomial`, `permutations_with_repetition`) | PSU / Ross | L3.2; Ross Ch.1 (multinomial theorem) |
| Combinations with replacement / stars & bars $\binom{n+k-1}{k}$, $\binom{n+k-1}{k-1}$ (`combinations_with_replacement`, `stars_and_bars`) | WMS / Ross | WMS Ch.2; Ross Ch.1 |
| Pascal's rule $\binom{n}{k}=\binom{n-1}{k-1}+\binom{n-1}{k}$; the triangle (`pascal_rule_holds`, `pascal_row`) | PSU / HTZ | L3.2; HTZ Ch.1 |
| Binomial theorem $(x+y)^n=\sum_k\binom{n}{k}x^ky^{n-k}$; row sums $2^n$ (`binomial_theorem_check`, `binomial_coefficient_sum`) | Ross / HTZ | Ross Ch.1; HTZ Ch.1 |
| Beta/Gamma bridge $\int_0^1 x^k(1-x)^{n-k}dx=1/[(n+1)\binom{n}{k}]$, $\Gamma(n+1)=n!$ (`beta_integral`, `_integrate`) | (standard) | cf. `~ST-11`, `~MA-12` |

## See also
- `~ST-01` (sample spaces & axioms) — the equally-likely model $P(A)=N(A)/N(S)$
  these counts serve; `~MA-19` (probability & statistics) — factorials and the
  binomial/normal distributions that reuse $\binom{n}{k}$.
- `~SM-01` (statistical multiplicity & Boltzmann entropy) — the **multinomial
  coefficient is the multiplicity $W$**; its Einstein-solid $\Omega=\binom{q+N-1}{q}$
  is this module's `stars_and_bars`. Counting joins thermodynamics through $S=k_B\ln W$.
- Forward: `~ST-07` (binomial — pmf normalized by the §7 binomial theorem),
  `~ST-08` (geometric & negative binomial — same coefficients), `~ST-09`
  (Poisson & multinomial), `~ST-11` (gamma/chi-square — the §8 $\Gamma(n+1)=n!$).
- STAT 414 Lesson 3 (primary, the four schemes); HTZ Ch.1 §1.4 (methods of
  enumeration — the text STAT 414 follows); Ross Ch.1 (combinatorial analysis,
  binomial & multinomial theorems); WMS Ch.2 (combinatorial probability).
