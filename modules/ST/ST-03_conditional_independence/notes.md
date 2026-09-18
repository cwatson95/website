# ST-03 — Conditional probability & independence (notes)

Module `~ST-01` built a probability space $(\Omega,\mathcal F,P)$ obeying
Kolmogorov's axioms. This module asks the next question: **how should $P$ change
once we learn that some event $B$ has occurred?** The answer — *renormalize to
$B$* — is the single most productive idea in elementary probability. It gives the
**multiplication** and **chain** rules (how to build joint probabilities one
factor at a time), the notion of **independence** (when the update does nothing),
and, because the updated assignment is *itself* a probability measure, the entire
machinery of `~ST-04` (Bayes' theorem and the law of total probability).

Citation key (full details + granularity in `refs.md`): **PSU L$n$** = Penn State
STAT 414 OER, Lesson $n$ (L4 *Conditional Probability*, L5 *Independent Events*);
**HTZ** = Hogg, Tanis & Zimmerman, *Probability and Statistical Inference* (Ch. 1);
**Ross** = Ross, *A First Course in Probability* (Ch. 3). Cited at **lesson /
chapter level**.

## 1. Conditional probability: renormalizing to what you know

A fair die is rolled; you are told the result is even. What is the probability it
is a $2$? Not $1/6$ — the outcomes $\{1,3,5\}$ are now impossible, so the sample
space has shrunk to $B=\{2,4,6\}$ and, among those three equally-likely faces, a
$2$ has probability $1/3$. The **conditional probability of $A$ given $B$**
formalizes this restriction-and-renormalization [PSU L4]:
$$\boxed{\,P(A\mid B)=\frac{P(A\cap B)}{P(B)}\,},\qquad P(B)>0 .$$
The numerator keeps only the part of $A$ that lives inside $B$; the denominator
rescales so that $B$ itself becomes the new certain event. Code: `conditional(p_ab,
p_b)` evaluates the ratio, and `conditional_event(measure, A, B)` reads
$P(A\cap B)$ and $P(B)$ straight off a finite measure (`prob`, `prob_inter`). In
the die example $A=\{2\}$, $B=\{2,4,6\}$ give $P(A\cap B)=\tfrac16$, $P(B)=\tfrac12$,
so $P(A\mid B)=\tfrac{1/6}{1/2}=\tfrac13$.

Two immediate sanity facts follow from the definition: if $A\supseteq B$ then
$A\cap B=B$ and $P(A\mid B)=1$ (a superset of the conditioning event is certain);
if $A\cap B=\varnothing$ then $P(A\mid B)=0$. Conditioning can move a probability
either way — $P(A\mid B)$ may exceed or fall below $P(A)$ — depending on whether
$B$ is "evidence for" or "against" $A$.

## 2. The multiplication rule

Clearing the denominator in §1 turns a *quotient* into a *product* — usually the
more useful direction, because joint probabilities are often assembled from
sequential conditional ones [PSU L4]:
$$P(A\cap B)=P(B)\,P(A\mid B)=P(A)\,P(B\mid A).$$
(The two right-hand sides are equal because both equal $P(A\cap B)$; equating
them is the seed of Bayes' theorem in `~ST-04`.) Code: `multiplication_rule(p_b,
p_a_given_b)` returns $P(B)P(A\mid B)$, and the test
`test_multiplication_rule_inverts_conditional` checks it reproduces
$P(A\cap B)$ from *both* orderings.

## 3. The chain rule for $n$ events

Iterate the multiplication rule. Peel one event at a time off the front of an
ordered intersection $A_1\cap A_2\cap\dots\cap A_n$:
$$\boxed{\,P\!\Big(\bigcap_{i=1}^n A_i\Big)=P(A_1)\,P(A_2\mid A_1)\,P(A_3\mid A_1\cap A_2)\cdots
P\big(A_n\mid A_1\cap\dots\cap A_{n-1}\big)\,}.$$
This is the **chain (general multiplication) rule**. Each factor conditions on
everything drawn so far, which is exactly how a **tree diagram** multiplies
probabilities along a branch. The canonical instance is sampling **without
replacement**: draw two cards from a $52$-card deck and ask for two aces,
$$P(\text{ace}_1\cap\text{ace}_2)=P(\text{ace}_1)\,P(\text{ace}_2\mid\text{ace}_1)
=\frac{4}{52}\cdot\frac{3}{51}=\frac{1}{221}\approx0.00452 .$$
The second factor is $3/51$, not $4/52$ — removing the first ace changes the
space, so the draws are *dependent*. Code: `chain_rule_factors(measure, events)`
constructs the list $[P(A_1),P(A_2\mid A_1),\dots]$ from a measure (here the
enumerated `two_card_deck()` of $52\cdot51$ ordered outcomes), and
`chain_rule(factors)` multiplies them; the test
`test_chain_rule_matches_intersection` confirms the product equals the directly
computed $P(\bigcap_i A_i)$ for any ordering.

## 4. Independence and its two equivalent forms

Sometimes learning $B$ tells you **nothing** about $A$: $P(A\mid B)=P(A)$. Feeding
this into the multiplication rule gives the symmetric **product form** [PSU L5]:
$$\boxed{\,A\perp B\iff P(A\cap B)=P(A)\,P(B)\iff P(A\mid B)=P(A)\,}\quad(P(B)>0).$$
The product form $P(A\cap B)=P(A)P(B)$ is the *definition* (it stays meaningful
even when $P(B)=0$ and is manifestly symmetric in $A,B$); the conditional form
$P(A\mid B)=P(A)$ is the intuitive reading. Code splits the two forms exactly:
`independent_check(pa, pb, pab)` tests the product rule, while
`conditional_equals_marginal(measure, A, B)` tests $P(A\mid B)=P(A)$ — and
`test_independence_two_equivalent_forms` asserts they **always agree**, both
returning `True` for the two fair coins ($P(A\cap B)=\tfrac14=\tfrac12\cdot\tfrac12$)
and both `False` for the dependent without-replacement draws.

Two warnings. (i) **Independent $\ne$ disjoint.** Disjoint events with positive
probability are the *opposite* of independent: $A\cap B=\varnothing$ forces
$P(A\cap B)=0\ne P(A)P(B)>0$, and indeed $P(A\mid B)=0$. (ii) Independence is a
statement about $P$, not about physical causation — it is a numerical
coincidence of probabilities that the code checks arithmetically.

A useful corollary: if $A\perp B$ then $A\perp B^{c}$, since
$P(A\cap B^{c})=P(A)-P(A\cap B)=P(A)\big(1-P(B)\big)=P(A)P(B^{c})$. Independence
survives complementation.

## 5. Pairwise vs mutual independence

For three or more events, "independent" must be said carefully. Events
$A_1,\dots,A_n$ are **pairwise independent** if every *pair* factors,
$$P(A_i\cap A_j)=P(A_i)P(A_j)\qquad(i<j),$$
and **mutually (completely) independent** if *every* sub-collection of size $\ge2$
factors,
$$P\!\Big(\bigcap_{i\in S}A_i\Big)=\prod_{i\in S}P(A_i)\qquad\text{for all }S\subseteq\{1,\dots,n\},\ |S|\ge2 .$$
Mutual independence is **strictly stronger** — it imposes $2^n-n-1$ equations, not
just the $\binom n2$ pairwise ones. The standard counterexample (Bernstein's) uses
the two fair coins of `two_coin_space()`:
$$A=\{\text{first toss }H\},\quad B=\{\text{second toss }H\},\quad C=\{\text{the two tosses agree}\}.$$
Each has probability $\tfrac12$, and **every pair** is independent:
$$P(A\cap B)=P(HH)=\tfrac14=P(A)P(B),\quad P(A\cap C)=P(HH)=\tfrac14=P(A)P(C),\quad P(B\cap C)=\tfrac14 .$$
But the triple fails, because knowing $A$ and $B$ *determines* $C$:
$$P(A\cap B\cap C)=P(HH)=\tfrac14\ \ne\ P(A)P(B)P(C)=\tfrac18 .$$
Code: `pairwise_independent(m, [A,B,C])` returns `True`,
`mutually_independent(m, [A,B,C])` returns `False`
(`test_pairwise_not_mutual`); the same test confirms three *independent* fair bits
$(a,b,c)\in\{0,1\}^3$ **are** mutually independent. `mutually_independent` iterates
`itertools.combinations` over all subsets of size $2,\dots,n$, exactly the equation
count above.

## 6. Conditional probability is a probability measure

Fix $B$ with $P(B)>0$ and define $Q(A)=P(A\mid B)$. Then $Q$ obeys **all three
Kolmogorov axioms** of `~ST-01`, so conditioning produces a genuine probability
space $(\Omega,\mathcal F,Q)$ — equivalently, a space on the smaller universe $B$:
$$\text{(i) }Q(A)=\frac{P(A\cap B)}{P(B)}\ge0,\qquad
\text{(ii) }Q(\Omega)=\frac{P(\Omega\cap B)}{P(B)}=\frac{P(B)}{P(B)}=1,$$
$$\text{(iii) for disjoint }A_1,A_2:\ \ Q(A_1\cup A_2)
=\frac{P\big((A_1\cup A_2)\cap B\big)}{P(B)}
=\frac{P(A_1\cap B)+P(A_2\cap B)}{P(B)}=Q(A_1)+Q(A_2),$$
the last step using that $A_1\cap B$ and $A_2\cap B$ are disjoint and that $P$ is
additive. Consequently **every** theorem of `~ST-01` holds verbatim inside the
conditional world: $Q(A^{c})=1-Q(A)$, monotonicity, inclusion–exclusion, and so
on. Code: `conditional_measure(measure, B)` returns $Q$ as a dict on all of
$\Omega$ (mass $P(\{o\})/P(B)$ inside $B$, zero outside); `test_conditioning_is_a
_probability_measure` verifies `is_probability_measure(Q)` is `True`,
$\sum_o Q(\{o\})=1$, $Q(\Omega)=Q(B)=1$, $Q(B^{c})=0$, and additivity on a disjoint
split of $B$.

This is more than bookkeeping. Because $Q=P(\cdot\mid C)$ is a measure, one can
speak of **independence inside it** — *conditional independence*:
$$A\perp B\mid C\iff P(A\cap B\mid C)=P(A\mid C)\,P(B\mid C).$$
Code: `conditionally_independent_check(m, A, B, C)`. Conditional independence is
neither implied by nor implies ordinary independence, and it is the backbone of
the law of total probability and Bayesian updating in `~ST-04` (and, downstream,
of `~ST-13` independence of random variables).

## 7. The continuous mirror: memorylessness and factorization

Conditioning and independence read identically for continuous models (full theory
in `~ST-10`/`~ST-11`/`~ST-13`); two clean identities make the bridge.

**Memorylessness of the exponential.** Let $T\sim\text{Exp}(\lambda)$ with survival
function $P(T>t)=\int_t^\infty\lambda e^{-\lambda s}\,ds=e^{-\lambda t}$. Then for
$s,t\ge0$ the conditional "extra wait" forgets the elapsed time $s$:
$$P(T>s+t\mid T>s)=\frac{P(T>s+t)}{P(T>s)}=\frac{e^{-\lambda(s+t)}}{e^{-\lambda s}}
=e^{-\lambda t}=P(T>t).$$
The exponential is the *only* continuous law with this property — the continuous
analogue of the geometric (`~ST-08`). Code: `exponential_survival(t, rate)` and
`memoryless_conditional(s, t, rate)`; the test integrates the density
($\int_t^\infty\lambda e^{-\lambda s}ds$, via the midpoint helper `_integrate`) to
confirm it matches $e^{-\lambda t}$, and checks the conditional is independent of
$s$.

**Independence as factorization.** For independent $X,Y\sim\text{Uniform}(0,1)$ the
joint density factors, $f(x,y)=f_X(x)f_Y(y)=1$ on the unit square, so any product
event factors too:
$$P(X<a,\,Y<b)=\int_0^a\!\!\int_0^b f(x,y)\,dy\,dx=ab=P(X<a)\,P(Y<b),$$
and therefore $P(X<a\mid Y<b)=ab/b=a=P(X<a)$ — the §4 equivalence in continuous
dress. Code: `uniform_square_joint`, `prob_rect` (a 2-D midpoint integral
`_integrate2`); `test_continuous_independence_factorization` checks the joint
equals $ab$ and that the conditional equals the marginal. This factorization *is*
the definition of independence for random variables in `~ST-13`.

## Where this goes

- `~ST-01` (axioms, sample spaces, inclusion–exclusion) — the measure $P$ that §1
  conditions and that §6 shows the conditional measure inherits; `~ST-02`
  (counting) supplies the equally-likely outcomes of the coin and card spaces.
- `~ST-04` (**Bayes' theorem**, law of total probability) — the immediate sequel,
  built entirely from the §2 multiplication rule and the §6 fact that $P(\cdot\mid
  B)$ is a measure; "reversing the conditioning" $P(B\mid A)$ vs $P(A\mid B)$.
- `~ST-05` (random variables & expectation) and `~ST-13` (joint distributions) —
  where independence of *events* (§4) becomes independence of *variables*
  (factorization of the joint pmf/pdf, §7).
- `~ST-07` (binomial — $n$ **independent** Bernoulli trials, the chain rule of §3
  with constant factors $p$) and `~ST-08`/`~ST-11` (geometric / exponential —
  memorylessness, the §7 conditional identity).
- `~MA-19` / `~SM-01` — the probability foundations this trunk deep-dives;
  independence underlies the multiplicativity of multiplicities and the
  factorization of partition functions there.
