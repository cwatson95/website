# SM-01 — Probability Foundations & Ensembles

First module of the **STATISTICAL MECHANICS & THERMODYNAMICS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~MA-19` (probability & statistics) — used directly (`binomial_pmf`, `normal_pdf`).
- **Feeds into:** `~SM-02` (entropy & the laws of thermodynamics), `~SM-03` (the canonical ensemble).

## Scope
Statistical mechanics is built on **counting microstates**. A macrostate's
**multiplicity** Ω is the number of microstates that realize it; the **fundamental
postulate** (equal a priori probabilities) makes every microstate equally likely,
so a macrostate's probability is Ω/Ω_total. The **Boltzmann entropy** S = k ln Ω
turns the multiplication of multiplicities into the addition of entropies, and for
large N the macrostate distribution is so sharply peaked (fractional width ~ 1/√N)
that thermodynamics looks deterministic.

The two-state paramagnet is literally a **binomial distribution**, so this module
consumes `~MA-19`: `two_state_probability` is MA-19's `binomial_pmf` at p = ½, and
the de Moivre–Laplace Gaussian limit is its `normal_pdf`.

## Operations — `code/probability_ensembles.py`

| call | meaning | reference |
|------|---------|-----------|
| `multiplicity_two_state(N, n)` | Ω(N,n) = C(N,n) for n up-spins of N | Pa §1.2 p.3 |
| `multiplicity_einstein_solid(N, q)` | Ω = C(q+N−1, q), q quanta in N oscillators | Pa §1.4 p.10 |
| `boltzmann_entropy(omega, k)` | S = k ln Ω (additive) | Pa §1.2 p.3 |
| `stirling_ln_factorial(n)` | ln n! ≈ n ln n − n (+½ln 2πn) | Pa §1.4 p.10; Sch Ch.2 |
| `two_state_probability(N, n)` | P = C(N,n)/2ᴺ (reuses MA-19 `binomial_pmf`) | Pa §1.2 p.3 |
| `most_probable_n(N)` / `fractional_width(N)` | peak at N/2; width = 1/√N | Pa §1.2 p.3 |
| `gaussian_approx_two_state(N, n)` | normal(N/2, √N/2) limit (MA-19 `normal_pdf`) | Pa §1.2 p.3 |

Constant: `K_B` (Boltzmann constant, 1.380649×10⁻²³ J/K).

## Use
```python
from probability_ensembles import (
    multiplicity_two_state, boltzmann_entropy, two_state_probability, fractional_width)

multiplicity_two_state(100, 50)        # C(100,50) ~ 1.01e29  (most microstates)
boltzmann_entropy(2**100, k=1.0)       # ln(2^100) ~ 69.3 nats (all states accessible)

sum(two_state_probability(20, n) for n in range(21))   # 1.0 (normalized)
fractional_width(10**6)                # 1e-3: the peak sharpens as 1/sqrt(N)
```

## Run
```bash
cd code
python3 probability_ensembles.py          # demo: multiplicity, entropy additivity, Stirling, sharpening
python3 test_probability_ensembles.py     # tests  ->  "All 6 tests passed."
```
(`probability_ensembles.py` imports MA-19 by relative path; becomes `from physkit… import …` once the shared package exists.)

## Files
- `notes.md` — derivations with inline page citations
- `code/probability_ensembles.py`, `code/test_probability_ensembles.py`
- `problems/problems.md` — worked problems (Pathria Ch.1–2; Schroeder Ch.2)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
