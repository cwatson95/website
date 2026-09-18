# ST-03 — Conditional probability & independence

Third module of the **PROBABILITY THEORY** trunk (see `modules/topic_network.txt`),
a faithful module-by-module replica of Penn State's **STAT 414**. Covers
**Lesson 4 (Conditional Probability)** and **Lesson 5 (Independent Events)**.
The whole module turns on one definition — conditioning *rescales* probability to
the part of the sample space you already know occurred — and its two corollaries,
the **multiplication / chain rule** and **independence**.

- **Prerequisites:** `~ST-01` (sample spaces and the Kolmogorov axioms — the
  measure $P$ being conditioned, inclusion–exclusion for $P(A\cup B)$), `~ST-02`
  (counting — the equally-likely outcomes behind the coin and card spaces).
- **Cross-links:** `~ST-04` (Bayes' theorem and the law of total probability —
  the *next* lesson, built directly on the multiplication rule below), `~ST-05`
  (random variables — independence of *events* becomes independence of *variables*),
  `~ST-07` (the binomial — $n$ **independent** Bernoulli trials), `~ST-11`
  (exponential — its **memorylessness** is the continuous conditional identity
  here), `~ST-13` (joint distributions — independence as factorization of a joint
  pmf/pdf), `~MA-19` / `~SM-01` (the probability foundations this trunk deep-dives).

## Scope
**Conditional probability** is defined by
$P(A\mid B)=P(A\cap B)/P(B)$ for $P(B)>0$: knowing $B$ occurred restricts the
sample space to $B$ and renormalizes. Rearranging gives the **multiplication
rule** $P(A\cap B)=P(B)\,P(A\mid B)$, which iterates into the **chain rule**
$P(A_1\cap\dots\cap A_n)=P(A_1)P(A_2\mid A_1)\cdots P(A_n\mid A_1\cap\dots\cap A_{n-1})$
— the engine behind drawing cards without replacement and behind tree diagrams.
Two events are **independent** when conditioning changes nothing,
$P(A\mid B)=P(A)$, equivalently the symmetric product rule
$P(A\cap B)=P(A)P(B)$. For three or more events independence splits into
**pairwise** (every pair factors) and **mutual** (every sub-collection factors);
the classic two-coin example shows pairwise $\not\Rightarrow$ mutual. Finally,
for fixed $B$ the map $A\mapsto P(A\mid B)$ is **itself a probability measure** —
it satisfies the `~ST-01` axioms — which is what licenses **conditional
independence** $P(A\cap B\mid C)=P(A\mid C)P(B\mid C)$ and the whole of `~ST-04`.

## Operations — `code/conditional_independence.py`  (pure stdlib)

| call | meaning | reference |
|------|---------|-----------|
| `normalize(weights)` | weights $\to$ measure $P(\{o\})=w_o/\sum w$ | L4; `~ST-01` |
| `prob(measure, A)` | $P(A)=\sum_{o\in A}P(\{o\})$ | L2; `~ST-01` |
| `prob_inter(m,A,B)` / `prob_union(m,A,B)` | $P(A\cap B)$; $P(A\cup B)=P(A)+P(B)-P(A\cap B)$ | L2 |
| `conditional(p_ab, p_b)` | $P(A\mid B)=P(A\cap B)/P(B)$ | **L4** |
| `conditional_event(m,A,B)` | $P(A\mid B)$ read off a finite measure | L4 |
| `conditional_measure(m,B)` | the measure $Q(\cdot)=P(\cdot\mid B)$ (valid measure) | L4 |
| `multiplication_rule(p_b, p_a_given_b)` | $P(A\cap B)=P(B)P(A\mid B)$ | L4 |
| `chain_rule(factors)` | $\prod$ of $P(A_1),P(A_2\mid A_1),\dots$ | L4 |
| `chain_rule_factors(m, events)` | builds $[P(A_1),P(A_2\mid A_1),\dots]$ from a measure | L4 |
| `independent_check(pa,pb,pab)` | $P(A\cap B)\overset?=P(A)P(B)$ | **L5** |
| `independent_events(m,A,B)` | independence of two events of a measure | L5 |
| `conditional_equals_marginal(m,A,B)` | the equivalent form $P(A\mid B)\overset?=P(A)$ | L5 |
| `pairwise_independent(m, events)` | every pair factors | L5 |
| `mutually_independent(m, events)` | every sub-collection of size $\ge2$ factors | L5 |
| `conditionally_independent_check(m,A,B,C)` | $P(A\cap B\mid C)\overset?=P(A\mid C)P(B\mid C)$ | L4/L5 |
| `exponential_survival(t, rate)` / `memoryless_conditional(s,t,rate)` | $P(T>t)=e^{-\lambda t}$; $P(T>s+t\mid T>s)=P(T>t)$ | L4; `~ST-11` |
| `uniform_square_joint`, `prob_rect` | independent Uniforms; $P(X<a,Y<b)=ab$ by 2-D integral | L5; `~ST-13` |
| `two_coin_space()` / `two_card_deck()` | the worked demo spaces | L4/L5 |

## Use
```python
from conditional_independence import (two_coin_space, two_card_deck,
    conditional_event, independent_events, conditional_equals_marginal,
    pairwise_independent, mutually_independent, chain_rule, chain_rule_factors,
    conditional_measure, is_probability_measure, memoryless_conditional)

m, A, B, C = two_coin_space()        # A=first H, B=second H, C=tosses agree
conditional_event(m, A, B)           # 0.5   = P(A): A,B independent
independent_events(m, A, B)          # True
conditional_equals_marginal(m, A, B) # True  (the equivalent form of independence)
pairwise_independent(m, [A, B, C])   # True
mutually_independent(m, [A, B, C])   # False  (pairwise != mutual)
is_probability_measure(conditional_measure(m, B))   # True (conditioning is a measure)

deck, fa, sa = two_card_deck()       # two cards, no replacement
chain_rule_factors(deck, [fa, sa])   # [4/52, 3/51]
chain_rule(_)                        # 1/221 = P(both aces)
memoryless_conditional(2.0, 3.0, 0.7)  # = P(T>3) = e^{-2.1}: exponential is memoryless
```

## Run
```bash
cd code
python3 conditional_independence.py        # demo: coins, cards, pairwise≠mutual, memorylessness
python3 test_conditional_independence.py   # tests  ->  "All 11 tests passed."
```

## Files
- `notes.md` — definition → multiplication/chain rule → independence and its two
  forms → pairwise vs mutual → conditioning as a probability measure → continuous
  memorylessness & factorization; each result tied to a code symbol
- `code/conditional_independence.py`, `code/test_conditional_independence.py` (stdlib only, self-contained)
- `problems/problems.md` — worked problems (STAT 414 L4–L5; numerical cross-checks to the code)
- `refs.md` — citation table (STAT 414 OER primary; Hogg–Tanis–Zimmerman, Wackerly, Ross at chapter level)
