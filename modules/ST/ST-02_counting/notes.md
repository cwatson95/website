# ST-02 — Counting Techniques (notes)

The axioms of `~ST-01` reduce probability, in the **equally-likely** model, to
arithmetic: if the sample space $S$ has $N(S)$ outcomes all of probability
$1/N(S)$, then for any event $A$
$$P(A)=\frac{N(A)}{N(S)}.$$
So the entire problem is to **count** $N(A)$ and $N(S)$. This module builds the
counting toolkit — the multiplication principle, permutations, combinations,
stars & bars, and multinomial coefficients — and the two structural facts that
organize them (Pascal's triangle and the binomial theorem). Each result is tied
to a symbol in `code/counting.py`.

Citation key (full table + granularity note in `refs.md`): **PSU** = Penn State
STAT 414 OER, **Lesson 3 "Counting Techniques"** (subsections L3.1 multiplication
principle, L3.2 permutations/combinations); **HTZ** = Hogg, Tanis & Zimmerman,
*Probability and Statistical Inference*, Ch. 1; **WMS** = Wackerly–Mendenhall–
Scheaffer, Ch. 2; **Ross**, *A First Course in Probability*, Ch. 1. Cited at
chapter/lesson level.

## 1. The multiplication principle

If a procedure consists of $m$ stages, the $i$-th performable in $n_i$ ways
*independently* of the earlier choices, then the whole procedure has [PSU L3.1]
$$N=\prod_{i=1}^{m} n_i = n_1 n_2\cdots n_m$$
distinct outcomes — the size of the Cartesian product $A_1\times\cdots\times A_m$.
Code: `multiplication_principle(sizes)`. Every other formula in this module is a
specialization. The most immediate one: filling $k$ slots, each independently
from the **same** set of $n$ symbols (sampling **ordered, with replacement**),
gives
$$n\cdot n\cdots n = n^{k},$$
the number of length-$k$ strings over an $n$-letter alphabet (`ordered_with_replacement(n,k)`).
A license plate of 2 letters then 3 digits has $26^2\cdot10^3=676\,000$ forms.

## 2. Permutations: ordered, without replacement

Now draw $k$ of the $n$ objects **in order** but **without replacement**: the
first slot has $n$ choices, the next $n-1$, …, the $k$-th has $n-k+1$. By the
multiplication principle [PSU L3.2; HTZ Ch.1]
$$P(n,k)=n(n-1)\cdots(n-k+1)=\frac{n!}{(n-k)!},\qquad 0\le k\le n.$$
Code: `permutations(n,k)`. Two boundary cases fix the conventions: $P(n,0)=1$
(there is exactly one way to choose nothing — the empty arrangement, forcing the
**empty product** $0!=1$ used by `factorial`), and $P(n,n)=n!$, the number of full
orderings of $n$ distinct objects. The recurrence $n!=n\,(n-1)!$ that defines the
factorial is checked in code; `factorial(n)` cross-checks `math.factorial`.

## 3. Combinations: unordered, without replacement

If order does **not** matter, every unordered $k$-subset has been counted $k!$
times among the permutations (its $k!$ orderings). Dividing out that overcount
[PSU L3.2]:
$$\binom{n}{k}=\frac{P(n,k)}{k!}=\frac{n!}{k!\,(n-k)!}.$$
Code: `combinations(n,k)` ($=$ `permutations(n,k)//factorial(k)`, cross-checked
against `math.comb`). The bookkeeping identity worth remembering is therefore
$$\boxed{\;P(n,k)=\binom{n}{k}\,k!\;}$$
"choose the subset, then order it." Two structural properties:
$$\binom{n}{k}=\binom{n}{n-k}\quad(\text{symmetry: choosing a committee}=\text{choosing its complement}),$$
$$\binom{n}{0}=\binom{n}{n}=1 .$$
Outside $0\le k\le n$ we set $\binom{n}{k}=0$, so sums over $k$ extend cleanly.

## 4. Combinations with replacement — stars and bars

The fourth scheme: draw $k$ objects **unordered, with replacement** from $n$
types — equivalently, count the **multisets** of size $k$, or the non-negative
integer solutions of $x_1+x_2+\cdots+x_n=k$ where $x_t$ is how many of type $t$
were drawn. Encode a solution as $k$ **stars** (the items) separated into $n$
groups by $n-1$ **bars**; any arrangement of the $k+(n-1)$ symbols is a valid
solution, and choosing which $n-1$ of the $k+n-1$ positions are bars gives [PSU L3.2;
WMS Ch.2]
$$\#\{x_1+\cdots+x_n=k,\ x_t\ge0\}=\binom{n+k-1}{\,n-1\,}=\binom{n+k-1}{k}.$$
Code: `combinations_with_replacement(n,k)`. The complementary parametrization —
**$n$ identical items into $k$ distinct boxes** — is the same formula relabeled,
$$\binom{n+k-1}{k-1},$$
which is `stars_and_bars(n,k)`; the two are duals, `combinations_with_replacement(n,k) = stars_and_bars(k,n)`.
This is exactly the **Einstein-solid multiplicity** of `~SM-01`: $q$ identical
energy quanta shared among $N$ oscillators has $\Omega=\binom{q+N-1}{q}=$
`stars_and_bars(q,N)` microstates.

## 5. Permutations with repetition — the multinomial coefficient

Arrange $n$ objects of which $k_1$ are of type 1, $k_2$ of type 2, …, $k_m$ of
type $m$ (objects of one type indistinguishable, $\sum_i k_i=n$). Of the $n!$
orderings of distinct objects, those differing only by permuting like objects
coincide, an overcount of $k_1!\,k_2!\cdots k_m!$ [PSU L3.2; Ross Ch.1]:
$$\binom{n}{k_1,k_2,\dots,k_m}=\frac{n!}{k_1!\,k_2!\cdots k_m!}.$$
Code: `multinomial(n, ks)` (and its alias `permutations_with_repetition`). It
generalizes the binomial coefficient — for $m=2$, $\binom{n}{k,\,n-k}=\binom{n}{k}$
— and counts, equivalently, the ways to **partition** $n$ labeled objects into
groups of prescribed sizes $k_1,\dots,k_m$. This number is precisely the
**statistical multiplicity $W$** of `~SM-01`: the number of microstates
(distinguishable arrangements of particles) compatible with an occupation
$(k_1,\dots,k_m)$, whose logarithm is the Boltzmann entropy $S=k_B\ln W$.

A check by **double counting**: assigning each of $n$ objects independently to one
of $m$ types gives $m^n$ outcomes; grouping by the occupation vector
$(k_1,\dots,k_m)$ gives the **multinomial theorem**
$$\sum_{k_1+\cdots+k_m=n}\binom{n}{k_1,\dots,k_m}=m^{n},$$
verified in code by enumerating all compositions.

## 6. Pascal's triangle and the recurrence

Fix one distinguished object among $n$. A $k$-subset either **omits** it — a
$k$-subset of the remaining $n-1$, $\binom{n-1}{k}$ ways — or **includes** it —
together with a $(k-1)$-subset of the rest, $\binom{n-1}{k-1}$ ways. These cases
are disjoint and exhaustive, so [PSU L3.2; HTZ Ch.1]
$$\binom{n}{k}=\binom{n-1}{k-1}+\binom{n-1}{k}\qquad(\textbf{Pascal's rule}).$$
Code: `pascal_rule_holds(n,k)`, with `pascal_row(n)` returning
$\big[\binom{n}{0},\binom{n}{1},\dots,\binom{n}{n}\big]$ — each entry the sum of
the two above it. The triangle is left–right symmetric (the $\binom{n}{k}=\binom{n}{n-k}$
of §3).

## 7. The binomial theorem and its row sums

Expanding $(x+y)^n=(x+y)(x+y)\cdots(x+y)$, each term picks $x$ from some $k$ of
the $n$ factors and $y$ from the other $n-k$; there are $\binom{n}{k}$ ways to
choose that $k$-subset, so [PSU L3.2; Ross Ch.1]
$$\boxed{\;(x+y)^n=\sum_{k=0}^{n}\binom{n}{k}\,x^{k}\,y^{\,n-k}.\;}$$
Code: `binomial_theorem_check(x,y,n)` returns the left sum and $(x+y)^n$ — equal.
Two specializations are workhorses:
$$x=y=1:\quad \sum_{k=0}^{n}\binom{n}{k}=2^{n}\quad(\text{the }2^n\text{ subsets of an }n\text{-set}),$$
$$x=-1,\,y=1:\quad \sum_{k=0}^{n}(-1)^k\binom{n}{k}=0\quad(n\ge1)\quad(\text{equal \#even and \#odd subsets}),$$
both in `binomial_coefficient_sum(n, signed)`. The probabilistic specialization —
$x=p,\ y=1-p$ — is the one that **feeds `~ST-07`**:
$$\sum_{k=0}^{n}\binom{n}{k}\,p^{k}(1-p)^{n-k}=(p+(1-p))^{n}=1,$$
i.e. the binomial theorem **is** the statement that the binomial pmf
$f(k)=\binom{n}{k}p^k(1-p)^{n-k}$ sums to $1$ over its support. Here
$\binom{n}{k}$ counts the equally-likely orderings of $k$ successes among $n$
Bernoulli trials.

## 8. The Beta–Gamma bridge (a continuous check)

The discrete $\binom{n}{k}$ has a continuous shadow. The **Gamma function** extends
the factorial,
$$\Gamma(s)=\int_0^\infty t^{\,s-1}e^{-t}\,dt,\qquad \Gamma(n+1)=n!,$$
and the **Beta function** ties two factorials to an integral over $[0,1]$,
$$B(a,b)=\int_0^1 x^{a-1}(1-x)^{b-1}\,dx=\frac{\Gamma(a)\,\Gamma(b)}{\Gamma(a+b)} .$$
Setting $a=k+1,\ b=n-k+1$ gives the clean identity used as the module's
continuous test (numerical midpoint integrator `_integrate`):
$$\int_0^1 x^{k}(1-x)^{\,n-k}\,dx=\frac{k!\,(n-k)!}{(n+1)!}=\frac{1}{(n+1)\binom{n}{k}} .$$
Code: `beta_integral(k,n)` returns the right-hand value; the test integrates the
left side and confirms agreement, and integrates $t^n e^{-t}$ to recover $n!$.
This is the seam where counting (`~ST-02`) joins the continuous distributions —
the Gamma function reappears as the normalizer of the gamma/chi-square family in
`~ST-11`, and the Beta integral is the normalizing constant of the Beta
distribution and the continuous analogue of $\binom{n}{k}$.

## Where this goes

- `~ST-01` (axioms, equally-likely model $P=N(A)/N(S)$) — *what these counts are
  for*; this module is its arithmetic engine.
- `~ST-07` (the binomial distribution) — its pmf normalization is the §7 binomial
  theorem at $x=p,\,y=1-p$, and $\binom{n}{k}$ counts the success-orderings; the
  **negative binomial / geometric** of `~ST-08` reuse the same coefficients.
- `~ST-09` (Poisson, and the multinomial in multi-category counts) — the
  multinomial coefficient of §5 generalizes the binomial; the Poisson arises as
  its rare-event limit.
- `~SM-01` (statistical multiplicity & entropy) — the **multinomial coefficient is
  the multiplicity $W$**, and the §4 stars-and-bars count is the Einstein-solid
  $\Omega=\binom{q+N-1}{q}$; $S=k_B\ln W$ turns these products into sums.
- `~ST-11` (exponential/gamma/chi-square) — the §8 Gamma function $\Gamma(n+1)=n!$
  is the continuous factorial that normalizes the gamma family; `~MA-12` for the
  special-function machinery.
