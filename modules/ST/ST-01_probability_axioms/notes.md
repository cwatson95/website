# ST-01 — Sample spaces & the axioms of probability (notes)

Probability theory begins by making the vague phrase "the chance of $A$" into a
precise object. A random experiment defines a **sample space** $S$ of possible
outcomes; an **event** is a subset $A\subseteq S$; and a **probability** is a
*set function* $P$ that assigns each event a number, subject to three rules — the
**Kolmogorov axioms**. The entire trunk (`~MA-19` deepened: random variables,
expectation, every named distribution) is downstream of these rules, so we derive
the standard consequences carefully and tie each to a code symbol. The classical
"favorable over total" formula $P(A)=|A|/|S|$ turns out to be just one special
case — the **equally-likely** measure — that powers `~SM-01`'s equal *a priori*
probabilities and, in disguise, `~QM-02`'s Born rule.

Citation key (full details + granularity in `refs.md`): **PSU L$n$** = Penn State
STAT 414 OER, Lesson $n$ (`online.stat.psu.edu/stat414`); **HTZ** = Hogg, Tanis &
Zimmerman, *Probability and Statistical Inference* (the text STAT 414 follows);
**Ross** = Ross, *A First Course in Probability*. Cited at **lesson/chapter
level**.

## 1. Sample space, outcomes, and events

A **random experiment** has an exhaustive, mutually exclusive set of **outcomes**;
their collection is the **sample space** $S$ [PSU L1]. An **event** is any subset
$A\subseteq S$; we say "$A$ occurs" when the realized outcome $\omega\in A$. Two
distinguished events bracket all others,
$$\varnothing\ \subseteq\ A\ \subseteq\ S,\qquad
\text{$\varnothing$ = impossible event},\quad \text{$S$ = certain event}.$$
For two dice the sample space is the Cartesian product
$$S=\{1,\dots,6\}\times\{1,\dots,6\},\qquad |S|=36,$$
built in code by `product_sample_space(range(1,7), repeat=2)`; an event such as
"the dice sum to $7$" is the subset selected by a predicate,
`event_probability(S, lambda w: sum(w)==7)`. A standard deck is the
$52$-outcome space `standard_deck()` of $(\text{rank},\text{suit})$ pairs.

## 2. Set algebra and De Morgan's laws

Because events are sets, they combine by the **algebra of sets** [PSU L1]:
$$A\cup B=\{\omega:\omega\in A\ \text{or}\ \omega\in B\},\quad
A\cap B=\{\omega:\omega\in A\ \text{and}\ \omega\in B\},\quad
A^c=\{\omega\in S:\omega\notin A\}.$$
"Or" is union, "and" is intersection, "not" is complement; $A\setminus B=A\cap B^c$
is "$A$ but not $B$". Events are **mutually exclusive (disjoint)** when
$A\cap B=\varnothing$. Union and intersection are commutative, associative, and
distributive, and complementation satisfies **De Morgan's laws**
$$(A\cup B)^c=A^c\cap B^c,\qquad (A\cap B)^c=A^c\cup B^c,$$
which generalize to any number of events. Code `complement_set(S, A)` returns
$A^c=S\setminus A$, and the test verifies both De Morgan identities on the explicit
$36$-outcome dice space. These laws are the everyday tool for turning an awkward
event into a tractable complement (§4).

## 3. The three Kolmogorov axioms

A **probability** assigns to each event $A$ a real number $P(A)$ subject to three
axioms [PSU L2; HTZ Ch. 1]:
$$\textbf{(A1)}\quad P(A)\ge 0,\qquad
\textbf{(A2)}\quad P(S)=1,\qquad
\textbf{(A3)}\quad P\!\Big(\bigsqcup_{i=1}^{\infty}A_i\Big)=\sum_{i=1}^{\infty}P(A_i)$$
where (A3) — **countable additivity** — holds for any sequence of **pairwise
disjoint** events $A_i\cap A_j=\varnothing\ (i\ne j)$. Axiom A1 is non-negativity;
A2 normalizes the total mass to one; A3 says the probability of a disjoint union
is the *sum* of the pieces. Code `union_disjoint(*probs)` implements A3 for a
finite disjoint family, and `is_valid_probability(p)` checks the range that A1+A2
will force (§4). Everything below is a **theorem**, proved from A1–A3 — not a new
assumption.

## 4. First consequences

**Probability of the empty set.** Take $A_1=S$ and $A_2=A_3=\cdots=\varnothing$ in
A3 (all disjoint): $P(S)=P(S)+\sum_{i\ge 2}P(\varnothing)$, so the infinite sum of
$P(\varnothing)$ must vanish, forcing
$$\boxed{\,P(\varnothing)=0\,}\qquad\text{(code: }\texttt{prob\_empty()}\text{)}.$$

**Complement rule.** $S=A\sqcup A^c$ is a disjoint union, so by A2 and A3
$1=P(S)=P(A)+P(A^c)$, i.e.
$$\boxed{\,P(A^c)=1-P(A)\,}\qquad\text{(code: }\texttt{complement(p)}\text{)}.$$
This is the workhorse for "at least one" events: $P(\text{at least one})
=1-P(\text{none})$.

**Monotonicity and the range.** If $A\subseteq B$ then $B=A\sqcup(B\cap A^c)$, so
$P(B)=P(A)+P(B\cap A^c)\ge P(A)$ by A1. Hence
$$A\subseteq B\ \Longrightarrow\ P(A)\le P(B),\qquad
\text{and since }A\subseteq S,\quad 0\le P(A)\le 1.$$
Code `monotone(p_sub, p_super)` checks the implication; `prob_difference(pa, pab)`
returns $P(A\setminus B)=P(A)-P(A\cap B)\ge 0$, the nonnegative gap above.

## 5. The addition rule for two events

When $A$ and $B$ overlap, A3 does **not** apply directly — adding $P(A)+P(B)$
double-counts $A\cap B$. Decompose into disjoint pieces:
$A\cup B=A\sqcup(B\cap A^c)$ and $B=(A\cap B)\sqcup(B\cap A^c)$, so subtracting,
$$\boxed{\,P(A\cup B)=P(A)+P(B)-P(A\cap B)\,}\qquad\text{(code: }\texttt{union\_two}\text{)}.$$
This **addition rule** [PSU L2] reduces to A3 exactly when $A\cap B=\varnothing$.
Rearranged it recovers the overlap, $P(A\cap B)=P(A)+P(B)-P(A\cup B)$
(`intersection_from_union`). Example (cards): a heart **or** a face card,
$$P(\heartsuit\cup\text{face})=\tfrac{13}{52}+\tfrac{12}{52}-\tfrac{3}{52}
=\tfrac{22}{52}=0.4231,$$
matched by `union_two(13/52, 12/52, 3/52)` and by a brute-force count over the deck.

## 6. Inclusion–exclusion and Boole's inequality

Iterating the addition rule to three events gives [PSU L2; Ross Ch. 2]
$$P(A\cup B\cup C)=P(A)+P(B)+P(C)
-P(A\cap B)-P(A\cap C)-P(B\cap C)+P(A\cap B\cap C),$$
implemented as `union_three(...)`. In general, for $n$ events the
**inclusion–exclusion principle** alternates the sums of $k$-fold intersections,
$$P\!\Big(\bigcup_{i=1}^{n}A_i\Big)=\sum_{k=1}^{n}(-1)^{k+1}S_k,\qquad
S_k=\!\!\sum_{i_1<\cdots<i_k}\!\! P\big(A_{i_1}\cap\cdots\cap A_{i_k}\big),$$
so $P(\bigcup A_i)=S_1-S_2+S_3-S_4+\cdots$. Code
`inclusion_exclusion(singles, pairs, triples, quad)` sums each $S_k$ from the list
of its $k$-fold intersection probabilities; the test pits it against a brute-force
count of $\bigcup A_i$ on the dice space (three- and four-event versions).
Truncating after the first term gives **Boole's inequality** (subadditivity),
$$P\!\Big(\bigcup_{i}A_i\Big)\ \le\ \sum_i P(A_i),$$
returned by `boole_bound(probs)` — a quick upper bound that needs no overlaps.

## 7. Equally-likely outcomes: classical probability

When $S$ is finite with $|S|=N$ outcomes that are **equally likely**, A2 and A3
force each singleton to weight $1/N$, and an event's probability becomes a *count*
[PSU L1; HTZ Ch. 1]:
$$\boxed{\,P(A)=\frac{\lvert A\rvert}{\lvert S\rvert}\,}\qquad
\text{(code: }\texttt{prob\_equally\_likely(k,n)}\text{, }\texttt{event\_probability}\text{)}.$$
This is the **classical / a priori** definition — dice, cards, fair coins. It is
also the discrete heart of `~SM-01`'s *fundamental postulate* (every accessible
microstate equally probable), where $P(\text{macrostate})=\Omega/\Omega_{\text{tot}}$
is precisely $|A|/|S|$. Counting the $|A|$ and $|S|$ — permutations, combinations,
multinomials — is the subject of `~ST-02`. Example: $P(\text{sum}=7)$ for two dice
is $6/36=1/6$; $P(\text{at least one }6)=1-(5/6)^2=11/36$ via the complement rule.

## 8. Continuous sample spaces: probability as an integral

When outcomes form a continuum (e.g. a point in $[0,1]$), single outcomes have
probability zero and the equally-likely "count" becomes an **integral** of a
**density** $f\ge 0$ [PSU L1; preview of `~ST-10`]:
$$P\big(A\big)=\int_A f(x)\,dx,\qquad \int_S f(x)\,dx=1\ \ (\text{Axiom A2}),$$
with disjoint additivity (A3) now the additivity of integrals over disjoint sets.
The simplest case is the **continuous uniform** density on $[a,b]$,
$f(x)=1/(b-a)$ (`uniform_pdf`), for which $P([c,d])=(d-c)/(b-a)$. Code
`prob_continuous(pdf, a, b)` evaluates $\int_a^b f$ by midpoint quadrature
(`_integrate`); the test confirms the total mass is $1$ and that the addition rule
of §5 holds for two overlapping intervals — the axioms are identical, only the
"measure" changed from counting to integration.

## 9. The Born rule is the same axioms — `~QM-02`

Quantum mechanics assigns a complex **amplitude** $\psi_i=\langle i|\psi\rangle$ to
each outcome of a measurement; the **Born rule** turns amplitudes into a
probability distribution over outcomes,
$$\boxed{\,P_i=\frac{\lvert\psi_i\rvert^2}{\sum_j\lvert\psi_j\rvert^2}\,}\qquad
\text{(code: }\texttt{born\_probabilities}\text{)}.$$
This *is* Kolmogorov's axioms in disguise: $P_i\ge 0$ because it is a squared
modulus (A1), and $\sum_i P_i=1$ once divided by the norm $\langle\psi|\psi\rangle$
(A2) — for a normalized state the denominator is $1$. Disjoint measurement
outcomes add (A3). An equal superposition of $n$ basis states gives the uniform
$P_i=1/n$ — the equally-likely measure of §7 — so `born_probabilities([1,1,1,1])`
returns $[\tfrac14,\tfrac14,\tfrac14,\tfrac14]$. The probability scaffolding of
this module is exactly what `~QM-02` (wavefunction & normalization) stands on.

## Where this goes

- `~MA-19` (the applied probability/statistics toolkit) — this module is its
  axiomatic foundation; from here the trunk re-derives binomial/normal/Poisson
  from first principles.
- `~ST-02` (counting — permutations, combinations, multinomials) supplies the
  $|A|$ and $|S|$ that turn §7's $P(A)=|A|/|S|$ into numbers; `~ST-03`
  (conditional probability & independence) and `~ST-04` (Bayes) refine the set
  function $P$ further.
- `~ST-05` (random variables & expectation) pushes events through to $X(\omega)$
  and $E[X]$; `~ST-10`/`~ST-12` make §8's continuous $P(A)=\int_A f$ the main
  object (uniform, then normal).
- `~SM-01` (statistical mechanics) — the equally-likely measure of §7 as the
  *fundamental postulate* (equal a priori probabilities), $P=\Omega/\Omega_{\rm tot}$.
- `~QM-02` (wavefunction & Born rule) — §9: the very same axioms read off
  $|\psi|^2$; `~QM-06` (measurement postulates) takes that further to expectation
  values of observables.
