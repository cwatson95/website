# NE-16 — References

Page-level citations **verified by reading the page text** (poppler `pdftotext`)
in the PDF under `books/library/`. **Printed** = the number on the page;
**PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, **3rd ed.** (2017) | `NE_Nuclear_Engineering/nuclear_science_shultis_faw.pdf` | PDF = printed **+ 23** |
| Shultis & Faw, *Problem Solution Manual*, 3rd ed. (2016) | `NE_Nuclear_Engineering/nuclear_science_sol_shultis_faw.pdf` | indexed by chapter/problem |

Chapter 8 is by **Douglas S. McGregor** (Kansas State University).

## Topic → location

| Topic (code symbol) | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|
| Measurement theory | §8.6 | 259 | 282 |
| Types of uncertainty; accuracy vs precision | §8.6.1 | 259 | 282 |
| Uncertainty from counting statistics; binomial → Gaussian | §8.6.2 | 259–260 | 282–283 |
| **The Gaussian distribution** | Eq. (8.9) | 259 | 282 |
| **σ = √x**, for x above about 20 (`counting_sigma`) | Eq. (8.10) | 260 | 283 |
| **Table 8.3** — counts vs percent standard deviation (`SIGMA_TABLE`) | Table 8.3 | 261 | 284 |
| **Table 8.4** — kσ vs probability (`CONFIDENCE_TABLE`) | Table 8.4 | 261 | 284 |
| Sample mean (`mean_of_counts`) | Eq. (8.11) | 261 | 284 |
| Variance of a sum (`sigma_of_sum`) | Eq. (8.12) | 261 | 284 |
| **σ of the mean = √(x̄/N)** (`sigma_of_mean`) | Eq. (8.13) | 261 | 284 |
| The reported result x̄ ± √(x̄/N) | Eq. (8.14) | 262 | 285 |
| Confidence intervals; the one-sigma convention | §8.6.2 | 262 | 285 |
| **FWHM = 2.355σ**; resolution = 235.5σ/E (`fwhm_from_sigma`) | §8.6.2 | 262 | 285 |
| Dead time | §8.6.3 | 262 | 285 |
| **n = m/(1 − mτ)** (`true_rate`) | Eq. (8.15) | 262 | 285 |
| The mτ < 0.05 rule; the 500 counts/s GM limit (`max_rate_for_loss`) | §8.6.3 | 262 | 285 |
| Detection equipment; the NIM standard | §8.7 | 263–267 | 286–290 |

## Problems (verified, S&F 3rd ed. Ch. 8)
Chapter 8's problems begin on printed **268** (PDF 291). Problems **2** and **7**
belong to this module; the rest are detector physics and are worked in `~NE-15`.

- **Prob. 2** — a GM tube with τ = 0.25 ms reading 900 counts/s — printed 268, PDF 291.
- **Prob. 7** — five one-minute counts; σ of the average — printed 269, PDF 292.

## Three things this module adds

S&F's §8.6 covers the single measurement and dead time but stops short of three
standard results that any real measurement needs. Each is flagged in the source
rather than folded in silently.

### Error propagation

The book gives σ for a count and for an average, but never for a **difference** —
which is what every background-subtracted measurement is. The quadrature rule
σ² = σ₁² + σ₂², identical for sums and differences, is standard and is what makes
detection limits a subject at all. `propagate_sum`, `net_rate_sigma`.

### Optimal counting-time allocation

Minimising the net-rate variance at fixed total time gives t_g/t_b = √(r_g/r_b),
not the even split. `optimal_time_split`. The derivation is a one-line Lagrange
multiplier; the test verifies it by scanning 20 000 splits numerically rather
than asserting the formula against itself.

### Where τ comes from

Eq. (8.15) is stated with no indication of how the dead time is measured. The
**two-source method** — count each source alone and both together, and use the
non-linearity of the loss — is the standard answer.
`dead_time_from_two_source_method` implements the leading-order form and the test
documents how it degrades (always low: 4% at modest loss, 23% when
(n₁+n₂)τ ≈ 0.84).

## Two places the module refuses rather than answering

**Below 20 counts.** S&F state that the Gaussian approximation holds for x above
about 20. Below that the Poisson distribution is visibly skewed, and a symmetric
x ± √x interval misrepresents it — the lower limit can even go negative.
`counting_sigma` raises rather than returning a number that looks fine.

**Past mτ = 0.5.** Eq. (8.15) diverges at mτ = 1, but it stops being trustworthy
well before: past 0.5 the correction exceeds the measurement itself, so the answer
is determined by the assumed model rather than by the data.

That model choice is real and the book does not mention it. Eq. (8.15) is the
**non-paralysable** model, in which an event arriving during the dead period is
simply lost. In the **paralysable** model each arriving event *extends* the dead
period, so the observed rate rises, peaks at 1/(eτ), and then *falls* — meaning a
single low reading can correspond to two very different true rates, one of them
enormous. The two models agree at small mτ and diverge exactly where the
correction matters, which is why `true_rate` refuses instead of picking one.

## The saturation trap

Worth stating separately because it is a safety matter, not a precision one. The
forward map m = n/(1 + nτ) **saturates at 1/τ**, so a detector at saturation
reports the same reading for any input above it. On a 100 μs detector, true rates
of 10⁵ and 10⁹ s⁻¹ both read as roughly 10⁴ s⁻¹ — a factor of 10 000 in the field
compressed into 10% on the meter.

A reading that seems implausibly low near a strong source must therefore be
treated as suspect rather than reassuring. `test_the_observed_rate_saturates_...`
asserts the compression explicitly.

## A note on the module's own tests

`test_poisson_variance_really_is_the_mean` generates events from **exponential
inter-arrival times** — the physical process of `~NE-06` — rather than from a
binomial. A first draft used a binomial with p = 0.2, whose variance is np(1−p),
20% below the mean; that draft would have failed against correct code. The
binomial case is now retained in the test as an explicit contrast, so the
distinction is recorded rather than merely fixed.

## Cross-module dependencies
- **`~NE-15`** — the detectors whose output this interprets; Table 8.1's decay
  times set the achievable dead time.
- **`~NE-06`** — the memoryless decay law that makes counting Poisson, and the
  exponential waiting time the simulation uses.
- **`~NE-17`** — dose measurements inherit all of the propagation here.
- **`~NE-26`** — activation analysis is a small net peak on a large background,
  i.e. entirely a detection-limit problem.
- **`~ST-09`, `~ST-11`** — the general Poisson and propagation machinery.

## Further reading
- Knoll, G.F., *Radiation Detection and Measurement*, 4th ed., Ch. 3–4 — counting
  statistics and dead time in full, including both dead-time models and the
  two-source derivation.
- Currie, L.A., *Anal. Chem.* **40** (1968) 586 — the standard definitions of
  decision level, detection limit and determination limit, which P4 gestures at.
- Bevington & Robinson, *Data Reduction and Error Analysis*, Ch. 3–4 — general
  propagation, and the χ² test for whether observed scatter matches counting
  statistics (the diagnostic in P2).
- Gilmore, G., *Practical Gamma-ray Spectrometry*, Ch. 5 — peak-area
  uncertainties, where the background under a peak makes §2's problem sharper.
