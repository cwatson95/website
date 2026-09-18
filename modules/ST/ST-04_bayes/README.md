# ST-04 — Bayes' Theorem

Fourth module of the **PROBABILITY THEORY** trunk (a faithful module-by-module
replica of Penn State's STAT 414; see `modules/ST/list_ST.txt`). This is **STAT 414
Lesson 6**: the law of total probability and Bayes' theorem — how to *reverse* a
conditional probability and update beliefs as evidence arrives.

- **Prerequisites:** `~ST-03` (conditional probability and the multiplication rule
  $P(A\cap B)=P(A)\,P(B\mid A)$, independence, tree diagrams — Bayes is built from
  exactly these), `~ST-01` (the probability axioms and partitions of the sample
  space), `~MA-19` (the binomial pmf and the beta/gamma functions used in the
  continuous conjugate update).
- **Cross-links:** `~ST-02` (counting — the $\binom{n}{k}$ in the binomial
  likelihood), `~ST-07` (the binomial distribution, the likelihood made a
  first-class object), `~ST-09` (Poisson — another likelihood you can update on),
  `~SM-01` (a prior/posterior is a probability distribution over hypotheses, exactly
  an ensemble), `~QM-02` (the Born rule — physics' own "likelihood" $|\langle a\mid
  \psi\rangle|^2$ for an outcome given a state).

## Scope
A **partition** $\{A_1,\dots,A_k\}$ chops the sample space into mutually exclusive,
collectively exhaustive cells. The **law of total probability** slices any event $B$
through the partition,
$$P(B)=\sum_i P(B\mid A_i)\,P(A_i),$$
a weighted average of conditional probabilities with the **priors** $P(A_i)$ as
weights. **Bayes' theorem** divides one joint term by that whole sum to reverse the
conditioning,
$$P(A_i\mid B)=\frac{P(B\mid A_i)\,P(A_i)}{\sum_j P(B\mid A_j)\,P(A_j)}
\;\propto\; \underbrace{P(A_i)}_{\text{prior}}\times\underbrace{P(B\mid A_i)}_{\text{likelihood}},$$
renormalized by the **evidence** $P(B)$. The signature application is the **medical
screen**: combining a test's **sensitivity** $P(+\mid D)$ and **specificity**
$P(-\mid H)$ with a disease's **prevalence** (base rate) yields the **positive
predictive value** $P(D\mid +)$ — which is shockingly low for a rare disease even
with a near-perfect test (the **base-rate effect**). Written in **odds**, Bayes is
multiplicative — posterior odds $=$ prior odds $\times$ likelihood ratio — so
independent evidence simply *accumulates*, and **sequential updating** (each
posterior becomes the next prior) overturns the base rate after a few repeated
positives. The same identity with $\sum\to\int$ drives continuous estimation: a
**Beta–Binomial conjugate update** turns a $\mathrm{Beta}(a,b)$ prior on a coin's
bias into a $\mathrm{Beta}(a+k,b+n-k)$ posterior, its evidence the *continuous* law
of total probability $\int \pi(\theta)\,\mathcal L(\theta)\,d\theta$.

## Operations — `code/bayes.py`

| call | meaning | reference |
|------|---------|-----------|
| `total_probability(priors, likelihoods)` | $P(B)=\sum_i P(B\mid A_i)P(A_i)$ | L6; `~ST-03` |
| `joint_probabilities(priors, likelihoods)` | $P(A_i\cap B)=P(A_i)P(B\mid A_i)$ (multiplication rule) | L6; `~ST-03` |
| `bayes_posterior(priors, likelihoods[, observed])` | $P(A_i\mid B)=\dfrac{P(B\mid A_i)P(A_i)}{\sum_j P(B\mid A_j)P(A_j)}$ | L6 |
| `ppv(prevalence, sensitivity, specificity)` | $P(D\mid +)=\dfrac{se\,\pi}{se\,\pi+(1-sp)(1-\pi)}$ | L6 |
| `npv(prevalence, sensitivity, specificity)` | $P(H\mid -)=\dfrac{sp(1-\pi)}{sp(1-\pi)+(1-se)\pi}$ | L6 |
| `prob_to_odds(p)` / `odds_to_prob(o)` | $o=\dfrac{p}{1-p}$, $p=\dfrac{o}{1+o}$ | L6 |
| `lr_positive(se, sp)` / `lr_negative(se, sp)` | $LR^+=\dfrac{se}{1-sp}$, $LR^-=\dfrac{1-se}{sp}$ | L6 |
| `posterior_odds(prior_odds, lr)` | posterior odds $=$ prior odds $\times$ $LR$ | L6 |
| `sequential_update(priors, likelihoods, observations)` | repeated Bayes; posterior$_n\to$ prior$_{n+1}$ | L6 |
| `beta_pdf(theta, a, b)` | $\dfrac{\theta^{a-1}(1-\theta)^{b-1}}{B(a,b)}$ | `~MA-19` |
| `binomial_likelihood(theta, k, n)` | $\binom{n}{k}\theta^k(1-\theta)^{n-k}$ | `~ST-02`, `~MA-19` |
| `posterior_beta_binomial(a, b, k, n)` | $\mathrm{Beta}(a,b)\to\mathrm{Beta}(a+k,\,b+n-k)$ | L6 (conjugacy) |
| `evidence_beta_binomial(a, b, k, n)` | $\int\pi(\theta)\mathcal L(\theta)\,d\theta=\binom{n}{k}\dfrac{B(a+k,b+n-k)}{B(a,b)}$ | L6 |
| `beta_mean(a, b)` | $\dfrac{a}{a+b}$ (posterior mean shrinks the MLE) | `~MA-19` |

## Use
```python
import numpy as np
from bayes import (total_probability, bayes_posterior, ppv, npv,
                   prob_to_odds, odds_to_prob, lr_positive, sequential_update)

total_probability([0.5, 0.3, 0.2], [0.01, 0.02, 0.03])   # 0.017  P(defective)
bayes_posterior([0.5, 0.3, 0.2], [0.01, 0.02, 0.03])     # [0.294 0.353 0.353]

ppv(prevalence=0.001, sensitivity=0.99, specificity=0.99)   # 0.0902  (base-rate effect!)
npv(prevalence=0.001, sensitivity=0.99, specificity=0.99)   # 0.99999

# odds form: posterior odds = prior odds x likelihood ratio
odds_to_prob(prob_to_odds(0.001) * lr_positive(0.99, 0.99))  # 0.0902  (= PPV)

# two independent positive tests overturn the base rate
L = np.array([[0.01, 0.99],     # disease : P(-|D), P(+|D)
              [0.99, 0.01]])     # healthy : P(-|H), P(+|H)
sequential_update([0.001, 0.999], L, [1, 1])[:, 0]   # 0.001 -> 0.090 -> 0.908
```

## Run
```bash
cd code
python3 bayes.py        # demo: total probability, the disease screen, odds, sequential, Beta-Binomial
python3 test_bayes.py   # tests  ->  "All 13 tests passed."
```

## Files
- `notes.md` — partitions → law of total probability → Bayes (posterior ∝ prior×likelihood)
  → the disease screen & base-rate effect → odds form → sequential updating → the
  continuous Beta–Binomial conjugate update
- `code/bayes.py`, `code/test_bayes.py` (numpy + stdlib `math` only, self-contained)
- `problems/problems.md` — worked problems (STAT 414 L6; each with a numerical check to the code)
- `refs.md` — citation table (STAT 414 OER primary; Hogg–Tanis–Zimmerman, Wackerly, Ross at chapter level)
