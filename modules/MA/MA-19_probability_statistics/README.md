# MA-19 — Probability & Statistics

Math trunk (see `modules/topic_network.txt`). **Prereq:** `~MA-09` (integrals),
basic combinatorics. **Feeds:** `~SM-01` (ensembles & probability foundations),
`~SM-03` (partition functions), and the error analysis of every measurement
(`~PK-04` swarm/rate statistics).

## Scope
The distributions of physics — **binomial**, **Poisson**, **normal/Gaussian**,
**exponential** — with their closed-form moments; the **Central Limit Theorem**
(why the Gaussian is everywhere); **error propagation** σ_f²=Σ(∂f/∂x_i)²σ_i²; and
**least-squares** line fitting with uncertainties. Two limit bridges: binomial →
Poisson (rare events) and binomial → normal (de Moivre–Laplace). Every routine is
checked against its analytic answer.

## Operations — `code/probability.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `binomial_pmf(k, n, p)` | C(n,k)pᵏ(1−p)ⁿ⁻ᵏ | Boas §7 p.756 |
| `poisson_pmf(k, lam)` | λᵏe⁻λ/k! | Boas §9 p.767 |
| `normal_pdf`, `normal_cdf` | Gaussian density & CDF (via erf) | Boas §8 p.761 |
| `exponential_pdf(x, lam)` | λe⁻λˣ | Boas §6 p.750 |
| `mean_var(kind, …)` | closed-form (mean, variance) | Boas §5 p.744 |
| `sample_moments(xs)` | mean, var, skew, kurtosis | Boas §10 p.770 |
| `sample_normal`, `sample_uniform_sum` | sampling; CLT demonstrator | Boas §8 p.761 |
| `error_propagation(f, vals, sigmas)` | σ_f²=Σ(∂f/∂xᵢ)²σᵢ² | Boas §10 p.770 |
| `least_squares_line(xs, ys)` | OLS slope/intercept + σ | Boas §10 p.770 |
| `covariance`, `correlation` | second-moment measures | Boas §10 p.770 |

## Use
```python
import random
from probability import binomial_pmf, poisson_pmf, error_propagation, least_squares_line

binomial_pmf(3, 1000, 0.002)        # ~ poisson_pmf(3, 2.0): rare-event limit
error_propagation(lambda v: v[0]*v[1], [4.0, 5.0], [0.1, 0.2])   # (20.0, 0.943)
least_squares_line([0,1,2,3], [2.1, 5.0, 7.9, 11.1])             # slope ~3, intercept ~2
```

## Run
```bash
cd code
python3 probability.py        # demo (distributions, binomial->Poisson, CLT, fit)
python3 test_probability.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/probability.py` · `code/test_probability.py` · `problems/problems.md`
