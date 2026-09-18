# ST-02 — Counting Techniques

Second module of the **PROBABILITY THEORY** trunk (a module-by-module replica of
Penn State's STAT 414; see `modules/ST/list_ST.txt`). It covers **Lesson 3,
Counting Techniques**, and supplies the arithmetic engine for the equally-likely
model of `~ST-01`: when every outcome of a sample space $S$ is equally likely,
$P(A)=N(A)/N(S)$, and the whole problem reduces to **counting** $N(A)$ and $N(S)$.

- **Prerequisites:** `~ST-01` (sample spaces & the axioms — the equally-likely
  model $P(A)=N(A)/N(S)$ this module feeds), `~MA-19` (factorials, binomial
  coefficients, the binomial/normal distributions).
- **Cross-links:** `~SM-01` (statistical multiplicity — the **multinomial
  coefficient $W$** that counts microstates *is* `multinomial`; the Einstein-solid
  $\Omega=\binom{q+N-1}{q}$ is `stars_and_bars`), `~ST-07` (the binomial
  distribution — its pmf normalizes by the binomial theorem with $x=p,\,y=1-p$
  computed here), `~ST-09` (the multinomial / Poisson limits), `~ST-11` (the
  Beta/Gamma functions tying $\binom{n}{k}$ to a continuous integral).

## Scope
Counting answers "how many ways?" by four sampling schemes — draw $k$ objects
from $n$, distinguishing **ordered/unordered** and **with/without replacement**.
The **multiplication principle** $N=\prod_i n_i$ underlies all of them. Ordered
selections give the **permutations** $P(n,k)=n!/(n-k)!$ (and $n^k$ with
replacement); dividing out the $k!$ orderings gives the **combinations**
$\binom{n}{k}=n!/[k!(n-k)!]$; allowing repeats in an unordered draw gives
**stars and bars** $\binom{n+k-1}{k}$. Counting arrangements of $n$ objects that
fall into $m$ indistinguishable classes gives the **multinomial coefficient**
$\binom{n}{k_1,\dots,k_m}=n!/(k_1!\cdots k_m!)$ — the same number `~SM-01` calls
the multiplicity $W$. The binomial coefficients tile **Pascal's triangle** via
$\binom{n}{k}=\binom{n-1}{k-1}+\binom{n-1}{k}$ and assemble the **binomial
theorem** $(x+y)^n=\sum_k\binom{n}{k}x^k y^{n-k}$, whose $x=p,\ y=1-p$ case is the
normalization $\sum_k\binom{n}{k}p^k(1-p)^{n-k}=1$ of the binomial pmf (`~ST-07`).

## Operations — `code/counting.py`

| call | meaning | reference |
|------|---------|-----------|
| `factorial(n)` | $n!=\prod_{i=1}^n i$, with $0!=1$ (cross-checks `math.factorial`) | PSU L3.1 |
| `multiplication_principle(sizes)` | $\lvert A_1\times\cdots\times A_m\rvert=\prod_i\lvert A_i\rvert$ | PSU L3.1 |
| `ordered_with_replacement(n, k)` | ordered, with replacement: $n^k$ | PSU L3.1 |
| `permutations(n, k)` | $P(n,k)=n!/(n-k)!$ (ordered, no replacement) | PSU L3.2 |
| `combinations(n, k)` | $\binom{n}{k}=n!/[k!(n-k)!]=P(n,k)/k!$ | PSU L3.2 |
| `permutations_with_repetition(n, ks)` | distinguishable perms $n!/(k_1!\cdots k_m!)$ (= `multinomial`) | PSU L3.2 |
| `multinomial(n, ks)` | $\binom{n}{k_1,\dots,k_m}$ — multiplicity $W$ (`~SM-01`) | PSU L3.2 |
| `stars_and_bars(n, k)` | $x_1+\cdots+x_k=n$: $\binom{n+k-1}{k-1}$ solutions | PSU L3.2 |
| `combinations_with_replacement(n, k)` | unordered, with replacement: $\binom{n+k-1}{k}$ | PSU L3.2 |
| `pascal_row(n)` / `pascal_rule_holds(n,k)` | row $[\binom{n}{0},\dots]$; $\binom{n}{k}=\binom{n-1}{k-1}+\binom{n-1}{k}$ | PSU L3.2 |
| `binomial_theorem_check(x, y, n)` | $\big(\sum_k\binom{n}{k}x^ky^{n-k},\,(x+y)^n\big)$ | PSU L3.2 |
| `binomial_coefficient_sum(n, signed)` | $\sum_k\binom{n}{k}=2^n$; signed $\Rightarrow 0$ | PSU L3.2 |
| `beta_integral(k, n)` | $\int_0^1 x^k(1-x)^{n-k}dx=\tfrac1{(n+1)\binom{n}{k}}$ (`~ST-11`) | PSU L3.2 |

## Use
```python
from counting import (permutations, combinations, multinomial, stars_and_bars,
                      combinations_with_replacement, binomial_theorem_check)

permutations(5, 3)                       # 60     ordered, no replacement
combinations(5, 3)                       # 10     unordered, no replacement
combinations_with_replacement(5, 3)      # 35     unordered, with replacement = C(7,3)
stars_and_bars(10, 4)                    # 286    10 quanta in 4 oscillators = C(13,3)
multinomial(11, [1, 4, 4, 2])            # 34650  arrangements of 'MISSISSIPPI'
binomial_theorem_check(0.3, 0.7, 6)      # (1.0, 1.0)  -> binomial pmf normalizes (~ST-07)
```

## Run
```bash
cd code
python3 counting.py            # demo: four sampling schemes, Pascal triangle, binomial theorem
python3 test_counting.py       # tests  ->  "All 14 tests passed."
```

## Files
- `notes.md` — multiplication principle → permutations → combinations → stars &
  bars → multinomial; Pascal's triangle & the binomial theorem; the Beta/Gamma
  bridge; the `~SM-01` multiplicity and `~ST-07` normalization links
- `code/counting.py`, `code/test_counting.py` (stdlib `math` only, self-contained)
- `problems/problems.md` — worked problems (STAT 414 L3; cross-checks to the code)
- `refs.md` — citation table (STAT 414 OER primarily; Hogg/Tanis/Zimmerman,
  Wackerly, Ross cross-cited at chapter level)
