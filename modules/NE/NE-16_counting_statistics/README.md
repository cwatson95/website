# NE-16 — Counting statistics: Poisson counting, propagated error, dead time

Sixteenth module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`), and the last of Chapter 8. Covers **§§8.6–8.7**
(printed pp. 259–267) of Shultis & Faw, 3rd ed.: measurement uncertainty,
counting statistics, confidence intervals, dead time, and NIM instrumentation.

- **Prerequisites:** `~NE-15` (the detectors), `~NE-06` (memoryless decay, which
  is why counting is Poisson), `~ST-09`/`~ST-11` (the general machinery).
- **Cross-links:** `~NE-17` (dose measurements inherit this propagation),
  `~NE-26` (activation analysis is a detection-limit problem).

## Scope
Radiation measurement is unusual in that **the uncertainty is known from the
single measurement**: decay is Bernoulli, so a count x has variance x and
σ/x = 1/√x. That is a wall — 1% needs 10 000 counts, 0.1% needs a million, and no
improvement in electronics touches it. Errors then compound: a net rate is a
*difference*, so the background contributes its own full uncertainty and never
cancels, which is what makes detection limits a subject. And a detector busy with
one event misses the next, so the observed rate understates the truth — a
correction that diverges, and whose forward map *saturates*, meaning a saturated
detector reads the same for any input above its ceiling.

## Operations — `code/counting_statistics.py`

| call | meaning | reference |
|------|---------|-----------|
| `counting_sigma(x)` | √x; **raises below 20 counts** | Eq. (8.10) |
| `relative_error(x)`, `counts_for_relative_error(f)` | 1/√x and its inverse | Table 8.3 |
| `mean_of_counts`, `sigma_of_sum`, `sigma_of_mean` | x̄, √Σx, √(x̄/N) | Eqs. (8.11)–(8.13) |
| `probability_within(k)`, `confidence_multiplier(p)` | erf(k/√2) and its inverse | Table 8.4 |
| `propagate_sum` / `propagate_difference` | quadrature — *identical* for both | added |
| `propagate_product_or_ratio(v, pairs)` | relative errors in quadrature | added |
| `net_rate`, `net_rate_sigma` | background-subtracted rate and its error | added |
| `optimal_time_split(r_g, r_b)` | √r_g/(√r_g+√r_b) — not 50/50 | added |
| `true_rate(m, τ)` | m/(1−mτ); **raises past mτ = 0.5** | Eq. (8.15) |
| `observed_rate(n, τ)` | the forward map, which saturates at 1/τ | §8.6.3 |
| `max_rate_for_loss(τ, f)` | the mτ < 0.05 rule; 500 /s for a GM tube | §8.6.3 |
| `dead_time_from_two_source_method(...)` | where τ actually comes from | added |
| `fwhm_from_sigma`, `sigma_from_fwhm` | FWHM = 2.355σ | §8.6.2 |

## Use
```python
from counting_statistics import (relative_error, counts_for_relative_error,
                                 sigma_of_mean, net_rate, net_rate_sigma,
                                 optimal_time_split, true_rate, observed_rate,
                                 confidence_multiplier, counting_sigma)

counts_for_relative_error(0.01)                  # 10 000 counts for 1%
sigma_of_mean([1255, 1286, 1234, 1301, 1221])    # 15.87   -- S&F Prob. 7

net_rate(520, 60, 500, 60)                       # 0.333 /s
net_rate_sigma(520, 60, 500, 60)                 # 0.532 /s -- 160%, no detection

optimal_time_split(50.0, 2.0)                    # 0.833, not 0.5
confidence_multiplier(0.90)                      # 1.6449 (the book rounds to 1.65)

true_rate(900.0, 0.25e-3)                        # 1161 /s  -- S&F Prob. 2
observed_rate(1e9, 100e-6)                       # 9999.9   -- saturated, and lying
true_rate(6000.0, 100e-6)                        # raises: correction exceeds the data
counting_sigma(5)                                # raises: Gaussian invalid below ~20
```

## Run
```bash
cd code
python3 counting_statistics.py        # demo: Tables 8.3-8.4, Prob. 7, dead time
python3 test_counting_statistics.py   # tests  ->  "All 15 tests passed."
cd ../figures && python3 make_figures.py
```

## Files
- `notes.md` — the single measurement and the 1/√N wall → propagation, detection
  limits and optimal time allocation → dead time, its two models, and the
  saturation trap, with a "Where this goes" map and a note on how the module
  tests itself.
- `code/counting_statistics.py`, `code/test_counting_statistics.py` (stdlib
  only). Two functions **refuse** rather than answering: `counting_sigma` below
  20 counts, and `true_rate` past mτ = 0.5 where the answer would be set by the
  assumed dead-time model rather than the data. The Poisson claim is checked by
  simulating exponential inter-arrival times, and the time-split formula by
  numerical minimisation.
- `problems/problems.md` — 7 worked problems (S&F Ch. 8 problems 2 and 7 plus
  five added: how long to count, a source barely above background, dividing the
  time, a saturated survey meter, and measuring τ) with numeric `*Check:*` lines.
- `figures/` — the 1/√N wall with Table 8.3 marked, relative error against net
  rate for three backgrounds with the detection limit visible, optimal time
  allocation against the naive even split, and the dead-time saturation ceiling
  beside the size of the correction.
- `refs.md` — page-verified citations; **three additions** (propagation, time
  allocation, the two-source method) the chapter needs but omits; the two places
  the module refuses; and the paralysable/non-paralysable model distinction S&F
  do not mention.
