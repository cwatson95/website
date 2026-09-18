# ST-03 — Problems

Work each by hand, then check with `code/conditional_independence.py`. Citations
in `../refs.md`; **PSU L4** = STAT 414 *Conditional Probability*, **PSU L5** =
*Independent Events*. The two demo spaces are `two_coin_space()` (two fair coins,
$A=$ first $H$, $B=$ second $H$, $C=$ the tosses agree) and `two_card_deck()` (two
distinct cards drawn without replacement).

### P1.  Conditional probability as renormalization  *(PSU L4)*
Two fair coins are tossed. Using $P(A\mid B)=P(A\cap B)/P(B)$, find (a) the
probability the first toss is heads **given** the second is heads, and (b) the
probability the two tosses **agree** ($C$) given the first is heads ($A$). For (a),
$P(A\cap B)=P(HH)=\tfrac14$ and $P(B)=\tfrac12$, so $P(A\mid B)=\tfrac14/\tfrac12
=\tfrac12$. For (b), $C\cap A=\{HH\}$ so $P(C\mid A)=\tfrac{1/4}{1/2}=\tfrac12$. In
both cases the conditional equals the marginal $\tfrac12$ — heralding independence
(P3). *Check:* `m,A,B,C = two_coin_space()`; `conditional_event(m,A,B)` $=0.5$ and
`conditional_event(m,C,A)` $=0.5$.

**Solution.** Conditioning renormalizes by the probability of the conditioning event. With each of $\{HH,HT,TH,TT\}$ at $1/4$: (a) $A\cap B=\{HH\}$ and $B=\{HH,TH\}$, so
$$P(A\mid B)=\frac{P(A\cap B)}{P(B)}=\frac{1/4}{1/2}=\frac12;$$
(b) with $C=\{HH,TT\}$ and $A=\{HH,HT\}$, the overlap is $C\cap A=\{HH\}$, so $P(C\mid A)=\frac{1/4}{1/2}=\frac12$. In both cases the conditional equals the unconditional $\tfrac12$ — the signature of independence taken up in P3. This matches `conditional_event(m,A,B)`$=0.5$ and `conditional_event(m,C,A)`$=0.5$.

### P2.  The chain rule without replacement  *(PSU L4)*
Draw two cards from a $52$-card deck without replacement. By the multiplication
rule $P(\text{ace}_1\cap\text{ace}_2)=P(\text{ace}_1)\,P(\text{ace}_2\mid
\text{ace}_1)$. The first factor is $4/52$; **given** an ace is gone, $3$ aces
remain among $51$ cards, so the second factor is $3/51$. Hence
$$P(\text{two aces})=\frac{4}{52}\cdot\frac{3}{51}=\frac{12}{2652}=\frac{1}{221}
\approx0.004525 .$$
The second factor differs from $4/52$, so the draws are **dependent**. *Check:*
`deck,fa,sa = two_card_deck()`; `chain_rule_factors(deck,[fa,sa])` $=[0.07692\ldots,
0.05882\ldots]$ (i.e. $4/52,\,3/51$); `chain_rule(_)` $=0.0045249=$
`prob_inter(deck,fa,sa)`; and `independent_events(deck,fa,sa)` is `False`.

**Solution.** The multiplication rule splits the joint into a first draw times a conditional second draw. The first card is an ace with probability $4/52$; **given** that ace is gone, $3$ aces remain among the $51$ cards left, so the second factor is $3/51$:
$$P(\text{two aces})=\frac{4}{52}\cdot\frac{3}{51}=\frac{12}{2652}=\frac{1}{221}\approx0.004525.$$
Because the second factor $3/51=0.0588$ differs from $4/52=0.0769$, knowing the first draw changes the second — the draws are **dependent**. This matches `chain_rule_factors(deck,[fa,sa])`$=[0.07692,0.05882]$, `chain_rule(_)`$=0.0045249=$`prob_inter(deck,fa,sa)`, and `independent_events(deck,fa,sa)` is `False`.

### P3.  Independence has two equivalent forms — and is not disjointness  *(PSU L5)*
Show the two fair-coin events $A$ (first $H$) and $B$ (second $H$) are independent
in **both** senses: the product rule $P(A\cap B)=\tfrac14=\tfrac12\cdot\tfrac12
=P(A)P(B)$, and the conditional rule $P(A\mid B)=\tfrac12=P(A)$. Then contrast with
$A$ and its complement $A^{c}$ (first toss tails): these are **disjoint**, so
$P(A\cap A^{c})=0\ne P(A)P(A^{c})=\tfrac14$ — disjoint events of positive
probability are the *opposite* of independent. *Check:* `independent_events(m,A,B)`
and `conditional_equals_marginal(m,A,B)` are both `True`; with `Ac` the complement
of `A`, `independent_events(m,A,Ac)` is `False` (and `prob_inter(m,A,Ac)` $=0$).

**Solution.** For $A,B$ both forms of independence hold. The product rule:
$$P(A\cap B)=P(HH)=\tfrac14=\tfrac12\cdot\tfrac12=P(A)P(B),$$
and equivalently $P(A\mid B)=\frac{1/4}{1/2}=\tfrac12=P(A)$, so conditioning on $B$ reveals nothing about $A$. Disjointness is the opposite extreme: $A$ and $A^c$ cannot co-occur, so $P(A\cap A^c)=0$, yet $P(A)P(A^c)=\tfrac12\cdot\tfrac12=\tfrac14\neq0$. Two disjoint events of positive probability are maximally **dependent** — one occurring forbids the other. This matches `independent_events(m,A,B)` and `conditional_equals_marginal(m,A,B)` both `True`, while `independent_events(m,A,Ac)` is `False` (with `prob_inter(m,A,Ac)`$=0$).

### P4.  Pairwise but not mutually independent  *(PSU L5)*
For the two coins let $C=$ "the tosses agree." Show $A,B,C$ are **pairwise**
independent — $P(A\cap B)=P(A\cap C)=P(B\cap C)=\tfrac14=$ (product of the two
marginals each $\tfrac12$) — yet **not mutually** independent, because $A$ and $B$
together force $C$:
$$P(A\cap B\cap C)=P(HH)=\tfrac14\ \ne\ P(A)P(B)P(C)=\tfrac18 .$$
This is why mutual independence ($2^{n}-n-1$ equations) is strictly stronger than
pairwise ($\binom n2$ equations). *Check:* `pairwise_independent(m,[A,B,C])`
$=$ `True` while `mutually_independent(m,[A,B,C])` $=$ `False`;
`prob(m, set(A)&set(B)&set(C))` $=0.25$ but `prob(m,A)*prob(m,B)*prob(m,C)`
$=0.125$.

**Solution.** Every marginal is $\tfrac12$, and each pair meets only in $HH$: $A\cap B=A\cap C=B\cap C=\{HH\}$, so each pairwise probability is $\tfrac14=\tfrac12\cdot\tfrac12$ — **pairwise independent**. But $A$ and $B$ together (both heads) force agreement, so $A\cap B\subseteq C$ and
$$P(A\cap B\cap C)=P(HH)=\tfrac14\neq P(A)P(B)P(C)=\tfrac18,$$
so the triple fails to factor. Mutual independence demands $2^3-3-1=4$ equations against the $\binom32=3$ of pairwise, hence is strictly stronger. This matches `pairwise_independent(m,[A,B,C])` is `True` while `mutually_independent(m,[A,B,C])` is `False`, with $0.25\neq0.125$.

### P5.  Conditioning produces a valid probability measure  *(PSU L4; `~ST-01`)*
Fix $B=$ "second toss $H$" and define $Q(\cdot)=P(\cdot\mid B)$. Verify $Q$ obeys
the Kolmogorov axioms (`~ST-01`): it is nonnegative, $Q(\Omega)=Q(B)=1$, and the
outcomes outside $B$ carry zero mass, $Q(B^{c})=0$. Concretely the two outcomes in
$B$, $HH$ and $TH$, each get reweighted to $P(\{o\})/P(B)=\tfrac{1/4}{1/2}
=\tfrac12$, summing to $1$. *Check:* `Q = conditional_measure(m,B)`;
`is_probability_measure(Q)` $=$ `True`; `prob(Q,B)` $=1.0$; `Q[('H','H')]` $=0.5$;
`prob(Q,[o for o in m if o not in set(B)])` $=0.0$.

**Solution.** Define $Q(\cdot)=P(\cdot\mid B)$, i.e. $Q(\{o\})=P(\{o\})/P(B)$ for $o\in B$ and $0$ otherwise. Nonnegativity is inherited because $P\ge0$ and $P(B)>0$; normalization holds because the retained mass is exactly $P(B)$:
$$Q(\Omega)=\sum_{o\in B}\frac{P(\{o\})}{P(B)}=\frac{P(B)}{P(B)}=1,\qquad Q(B^c)=0.$$
Concretely $B=\{HH,TH\}$, each outcome reweighted to $\frac{1/4}{1/2}=\tfrac12$, summing to $1$. So $Q$ satisfies the ~ST-01 Kolmogorov axioms — conditioning produces a genuine probability measure. This matches `is_probability_measure(Q)` is `True`, `prob(Q,B)`$=1.0$, `Q[('H','H')]`$=0.5$, and the outside-$B$ mass $=0.0$.

### P6.  Conditional independence  *(PSU L4/L5; basis for `~ST-04`)*
Toss three independent fair bits and let $A,B,C$ be "bit $2$ is $1$," "bit $3$ is
$1$," "bit $1$ is $1$." Inside the world where $C$ holds, $A$ and $B$ are still
independent fair bits, so $P(A\cap B\mid C)=P(A\mid C)P(B\mid C)$. Compute
$P(A\mid C)=P(B\mid C)=\tfrac12$ and $P(A\cap B\mid C)=\tfrac14=\tfrac12\cdot
\tfrac12$ — conditional independence holds. *Check:* build the space
`outs=[(c,a,b) for c in (0,1) for a in (0,1) for b in (0,1)]`,
`mm=normalize({o:1.0 for o in outs})`, with `C,A,B` the bit-indicators; then
`conditionally_independent_check(mm,A,B,C)` $=$ `True`, `P(A|C)=0.5`,
`P(A∩B|C)=0.25`.

**Solution.** The eight triples $(c,a,b)$ are equally likely. Conditioning on $C$ (bit $1$ equals $1$) keeps four equally likely outcomes; among them bit $2$ is $1$ in exactly half, so $P(A\mid C)=\tfrac12$, and likewise $P(B\mid C)=\tfrac12$. The lone outcome $(1,1,1)$ gives $P(A\cap B\cap C)=\tfrac18$, hence
$$P(A\cap B\mid C)=\frac{P(A\cap B\cap C)}{P(C)}=\frac{1/8}{1/2}=\frac14=\tfrac12\cdot\tfrac12=P(A\mid C)\,P(B\mid C).$$
So $A\perp B\mid C$ — independence survives inside the conditioned world, the structure ~ST-04 leans on. This matches `conditionally_independent_check(mm,A,B,C)` is `True`, `P(A|C)=0.5`, and `P(A∩B|C)=0.25`.

### P7.  Memorylessness of the exponential  *(PSU L4; `~ST-11`)*
Let $T\sim\text{Exp}(\lambda)$ with $\lambda=0.7$, survival $P(T>t)=e^{-\lambda t}$.
Show the conditional "extra wait" forgets the elapsed time: for $s=2,\,t=3$,
$$P(T>s+t\mid T>s)=\frac{P(T>5)}{P(T>2)}=\frac{e^{-0.7\cdot5}}{e^{-0.7\cdot2}}
=e^{-0.7\cdot3}=e^{-2.1}\approx0.122456=P(T>t),$$
independent of $s$. The exponential is the unique continuous law with this
property (continuous cousin of the geometric, `~ST-08`). *Check:*
`memoryless_conditional(2.0,3.0,0.7)` $\approx 0.122456$ $=$
`exponential_survival(3.0,0.7)` $= e^{-2.1}$.

**Solution.** With survival $P(T>t)=e^{-\lambda t}$, and using $\{T>s+t\}\subseteq\{T>s\}$ so the conditional's intersection is just $\{T>s+t\}$, the ratio collapses:
$$P(T>s+t\mid T>s)=\frac{P(T>s+t)}{P(T>s)}=\frac{e^{-\lambda(s+t)}}{e^{-\lambda s}}=e^{-\lambda t}=P(T>t).$$
The elapsed time $s$ cancels completely. For $\lambda=0.7,\ t=3$ this is $e^{-2.1}\approx0.122456$, independent of $s=2$ — and the exponential is the only continuous law with this memoryless property. This matches `memoryless_conditional(2.0,3.0,0.7)`$\approx0.122456=$`exponential_survival(3.0,0.7)`.

### P8.  Independence by factorization (continuous)  *(PSU L5; `~ST-13`)*
Let $X,Y$ be independent $\text{Uniform}(0,1)$, joint density $f(x,y)=1$ on the
unit square. Show the product event factors,
$$P(X<a,\,Y<b)=\int_0^a\!\!\int_0^b 1\,dy\,dx=ab=P(X<a)\,P(Y<b),$$
so for $a=0.6,\,b=0.4$ the joint is $0.24$, and the conditional equals the marginal,
$P(X<a\mid Y<b)=ab/b=a=0.6$. This factorization *is* independence of random
variables (`~ST-13`). *Check:* `prob_rect(uniform_square_joint,0.0,0.6,0.0,0.4)`
$\approx0.24$ and `conditional(0.24, 0.4)` $=0.6$.

**Solution.** Independence of $X,Y$ means the joint density factors, $f(x,y)=1=f_X(x)f_Y(y)$ on the unit square, so the rectangle probability separates into a product of one-dimensional integrals:
$$P(X<a,\,Y<b)=\int_0^a\!\!\int_0^b 1\,dy\,dx=ab=P(X<a)\,P(Y<b).$$
For $a=0.6,\ b=0.4$ this is $0.24$. The conditional then strips off the $Y$-factor, $P(X<a\mid Y<b)=\frac{ab}{b}=a=0.6=P(X<a)$ — conditional equals marginal, which *is* independence of the random variables (~ST-13). This matches `prob_rect(uniform_square_joint,0.0,0.6,0.0,0.4)`$\approx0.24$ and `conditional(0.24, 0.4)`$=0.6$.
