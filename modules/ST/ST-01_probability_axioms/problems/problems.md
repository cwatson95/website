# ST-01 — Problems

Work each by hand, then check with `code/probability_axioms.py`. Citations in
`../refs.md`; **PSU L1/L2** = STAT 414 Lessons 1–2. Sample spaces are the explicit
dice space `S = product_sample_space(range(1,7), repeat=2)` ($|S|=36$) and the deck
`standard_deck()` ($|S|=52$) unless stated. Throughout, an event is a subset
$A\subseteq S$ and (for finite equally-likely $S$) $P(A)=|A|/|S|$.

### P1.  Set algebra and De Morgan's laws  *(PSU L1)*
On the two-dice space let $A=\{\text{first die even}\}$ and $B=\{\text{sum}\ge 8\}$.
Write $(A\cup B)^c$ in words, and verify the **De Morgan law**
$(A\cup B)^c=A^c\cap B^c$: an outcome avoids *both* "$A$ or $B$" exactly when it is
in neither, i.e. the first die is odd **and** the sum is below $8$. Likewise
$(A\cap B)^c=A^c\cup B^c$. These let you trade a hard event for an easier
complement. *Check:* with `S=set(product_sample_space(range(1,7),2))`,
`A={w for w in S if w[0]%2==0}`, `B={w for w in S if sum(w)>=8}`,
`complement_set(S, A|B) == complement_set(S,A) & complement_set(S,B)` $=$ `True`,
and the same for `A&B` vs `A^c ∪ B^c`.

**Solution.** Membership chases straight through the definitions: an outcome lies in $(A\cup B)^c$ exactly when it belongs to neither set,
$$\omega\in(A\cup B)^c\iff\omega\notin A\ \text{and}\ \omega\notin B\iff\omega\in A^c\cap B^c,$$
which in words is "the first die is **odd** *and* the sum is **below 8**." Applying the same equivalence with $A^c,B^c$ in the roles of $A,B$ (and $(X^c)^c=X$) gives the dual $(A\cap B)^c=A^c\cup B^c$. These are pure set identities, true before any probability is assigned, and they let a stubborn event be traded for an easier complement. On the explicit $36$-outcome space that is exactly why `complement_set(S, A|B) == complement_set(S,A) & complement_set(S,B)` returns `True`, with the companion identity for `A&B` versus $A^c\cup B^c$ equally `True`.

### P2.  Equally-likely outcomes: two dice  *(PSU L1; §7)*
Using $P(A)=|A|/|S|$ on the $36$-outcome space, count the ways to make each total.
There are $6$ ways to roll a $7$ — $(1,6),(2,5),\dots,(6,1)$ — so $P(\text{sum}=7)
=6/36=1/6$; and only $(5,6),(6,5)$ give $11$, so $P(\text{sum}=11)=2/36=1/18$.
*Check:* `event_probability(S, lambda w: sum(w)==7)` $=0.16667$;
`event_probability(S, lambda w: sum(w)==11)` $=0.055556$;
`prob_equally_likely(6, 36)` $=1/6$.

**Solution.** Each of the $36$ ordered outcomes $(a,b)$ is equally likely with weight $1/36$, so $P(A)=|A|/36$. Listing the favorable pairs, a total of $7$ comes from $(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)$ — six ways — while $11$ allows only $(5,6),(6,5)$:
$$P(\text{sum}=7)=\frac{6}{36}=\frac16=0.16667,\qquad P(\text{sum}=11)=\frac{2}{36}=\frac{1}{18}=0.055556.$$
Counting favorable outcomes over $|S|=36$ is the whole computation. This matches `event_probability(S, lambda w: sum(w)==7)`$=0.16667$, `event_probability(S, lambda w: sum(w)==11)`$=0.055556$, and `prob_equally_likely(6, 36)`$=1/6$.

### P3.  The complement rule and "at least one"  *(PSU L2; §4)*
Find $P(\text{at least one die shows a }6)$ for two dice. Direct counting is fussy
(inclusion–exclusion of two events), but the **complement** is easy: "no $6$" means
each die is one of $\{1,\dots,5\}$, so $P(\text{no }6)=(5/6)^2=25/36$, hence
$$P(\text{at least one }6)=1-\tfrac{25}{36}=\tfrac{11}{36}=0.30556.$$
This complement trick (§4) is the standard route to every "at least one" event.
*Check:* with `no6 = event_probability(S, lambda w: w[0]!=6 and w[1]!=6)` $=25/36$,
`complement(no6)` $=0.30556$; equivalently
`event_probability(S, lambda w: w[0]==6 or w[1]==6)` $=0.30556$.

**Solution.** Counting "at least one $6$" directly means inclusion–exclusion of the two single-die events; its complement "**no** die is a $6$" is far easier. On the product space the dice are independent and each avoids $6$ with probability $5/6$, so $P(\text{no }6)=(5/6)^2=25/36$. The complement rule $P(A)=1-P(A^c)$ then finishes it:
$$P(\text{at least one }6)=1-\frac{25}{36}=\frac{11}{36}=0.30556.$$
This complement trick is the standard route to any "at least one" event. It matches `complement(no6)`$=0.30556$ (with `no6`$=25/36$) and the direct count `event_probability(S, lambda w: w[0]==6 or w[1]==6)`$=0.30556$.

### P4.  The addition rule on a deck  *(PSU L2; §5)*
Draw one card from a standard deck. Let $H=\{\heartsuit\}$ ($13$ cards) and
$F=\{\text{face card: J, Q, K}\}$ ($12$ cards). They overlap in the $3$ hearts that
are face cards, so the **addition rule** gives
$$P(H\cup F)=P(H)+P(F)-P(H\cap F)=\tfrac{13}{52}+\tfrac{12}{52}-\tfrac{3}{52}
=\tfrac{22}{52}=0.42308.$$
Adding $13+12$ would double-count those $3$ cards; subtracting $P(H\cap F)$ fixes it.
*Check:* `union_two(13/52, 12/52, 3/52)` $=0.42308$, equal to the brute-force
`event_probability(standard_deck(), lambda c: c[1]=="hearts" or c[0] in ("J","Q","K"))`.
Inverting, `intersection_from_union(13/52, 12/52, 22/52)` $=3/52$.

**Solution.** Hearts and face cards share the three cards $\text{J}\heartsuit,\text{Q}\heartsuit,\text{K}\heartsuit$, which a naive $13+12=25$ would count twice. The addition rule removes that overlap exactly once:
$$P(H\cup F)=\frac{13}{52}+\frac{12}{52}-\frac{3}{52}=\frac{22}{52}=0.42308,$$
matching the direct count $|H\cup F|=13+12-3=22$ cards. Rearranging the same identity recovers the overlap, $P(H\cap F)=P(H)+P(F)-P(H\cup F)=\tfrac{13+12-22}{52}=\tfrac{3}{52}$. This matches `union_two(13/52, 12/52, 3/52)`$=0.42308$ (equal to brute force) and `intersection_from_union(13/52, 12/52, 22/52)`$=3/52$.

### P5.  Three-set inclusion–exclusion  *(PSU L2; §6)*
On the dice space let $A=\{\text{first die even}\}$, $B=\{\text{sum}\ge 8\}$,
$C=\{\text{second die}=3\}$. The marginals are $P(A)=18/36$, $P(B)=15/36$,
$P(C)=6/36$; the pairwise overlaps $P(A\cap B)=9/36$, $P(A\cap C)=3/36$,
$P(B\cap C)=2/36$; and the triple $P(A\cap B\cap C)=1/36$. Then
$$P(A\cup B\cup C)=\tfrac{18+15+6}{36}-\tfrac{9+3+2}{36}+\tfrac{1}{36}
=\tfrac{39-14+1}{36}=\tfrac{26}{36}=0.72222.$$
Note **Boole's bound** $P(A)+P(B)+P(C)=39/36=1.0833>1$ is a (loose but valid) upper
bound. *Check:* `union_three(18/36,15/36,6/36, 9/36,3/36,2/36, 1/36)` $=0.72222$,
equal to brute `event_probability(S, lambda w: A or B or C)`; and
`boole_bound([18/36,15/36,6/36])` $=1.0833$.

**Solution.** Inclusion–exclusion alternates the sums $S_k$ of all $k$-fold intersection probabilities. Counting outcomes over $36$, the marginals give $S_1=\tfrac{18+15+6}{36}$, the three pairwise overlaps $S_2=\tfrac{9+3+2}{36}$, and the triple $S_3=\tfrac1{36}$ (only $(6,3)$ has the first die even, the second equal to $3$, and sum $\ge8$). Then
$$P(A\cup B\cup C)=S_1-S_2+S_3=\frac{39-14+1}{36}=\frac{26}{36}=0.72222.$$
Truncating after $S_1=39/36=1.0833$ is **Boole's bound** — a valid upper bound that here exceeds $1$ precisely because the overlaps are still double-counted. This matches `union_three(...)`$=0.72222$ (equal to brute force) and `boole_bound([18/36,15/36,6/36])`$=1.0833$.

### P6.  Four-set inclusion–exclusion  *(PSU L2; §6)*
Take the four dice events $A_1=\{\text{first}\le 3\}$, $A_2=\{\text{second}\le 3\}$,
$A_3=\{\text{even sum}\}$, $A_4=\{\text{doubles}\}$. The general law
$P(\bigcup A_i)=S_1-S_2+S_3-S_4$ with $S_k$ the sum of all $k$-fold intersection
probabilities gives $P(\bigcup A_i)=32/36=0.88889$. *Check:* build `singles`,
`pairs`, `triples` from `event_probability` and the single `quad`
$=P(A_1\cap A_2\cap A_3\cap A_4)$, then `inclusion_exclusion(singles, pairs,
triples, quad)` equals the brute-force union $=0.88889$ (see
`test_inclusion_exclusion_four_vs_brute`).

**Solution.** The general law is $P\!\left(\bigcup_i A_i\right)=S_1-S_2+S_3-S_4$, with $S_k$ the sum of every $k$-fold intersection probability. Counting outcomes over $36$ (so each $S_k$ is in units of $1/36$): $S_1=18+18+18+6=60$, $S_2=9+9+3+9+3+6=39$, $S_3=5+3+3+3=14$, and $S_4=3$, giving
$$P\!\left(\bigcup_i A_i\right)=\frac{60-39+14-3}{36}=\frac{32}{36}=0.88889.$$
As a check, the complement (in *none* of the four events) is the $4$ outcomes with both dice $\ge4$, odd sum, and not a double — $(4,5),(5,4),(5,6),(6,5)$ — so $1-4/36=32/36$ as well. This matches `inclusion_exclusion(singles, pairs, triples, quad)`$=0.88889$, equal to the brute-force union.

### P7.  A continuous sample space  *(PSU L1; §8)*
Spin a pointer to a uniform angle, modeled as $X\sim\text{Uniform}(0,1)$ with density
$f(x)=1$ on $[0,1]$. Probabilities are *areas*: $P([c,d])=d-c$, and the axioms are
unchanged ($\int_0^1 f=1$, disjoint intervals add). Verify the addition rule for
the overlapping intervals $I_1=[0.2,0.6]$, $I_2=[0.4,0.8]$: $P(I_1)=P(I_2)=0.4$,
overlap $P([0.4,0.6])=0.2$, so $P(I_1\cup I_2)=0.4+0.4-0.2=0.6=P([0.2,0.8])$.
*Check:* with `f = lambda x: uniform_pdf(x,0,1)`, `prob_continuous(f,0,1)` $=1.0$;
`union_two(prob_continuous(f,0.2,0.6), prob_continuous(f,0.4,0.8), prob_continuous(f,0.4,0.6))`
$=0.6=$ `prob_continuous(f,0.2,0.8)`.

**Solution.** For a continuous model probabilities are integrals of the density: $P([c,d])=\int_c^d f=\int_c^d 1\,dx=d-c$, and $\int_0^1 f=1$ is Axiom A2. The two intervals have lengths $P(I_1)=0.6-0.2=0.4$ and $P(I_2)=0.8-0.4=0.4$, overlapping on $[0.4,0.6]$ of length $0.2$, so the addition rule gives
$$P(I_1\cup I_2)=P(I_1)+P(I_2)-P(I_1\cap I_2)=0.4+0.4-0.2=0.6,$$
identical to the direct length of $I_1\cup I_2=[0.2,0.8]$, namely $0.8-0.2=0.6$. The axioms carry over unchanged from the finite case — only sums become integrals. This matches `prob_continuous(f,0,1)`$=1.0$ and `union_two(...)`$=0.6=$`prob_continuous(f,0.2,0.8)`.

### P8.  The Born rule is the same axioms  *(§9; `~QM-02`)*
A qubit in the (unnormalized) state $\psi=(3,\,4i)$ is measured. The **Born rule**
$P_i=|\psi_i|^2/\sum_j|\psi_j|^2$ assigns outcome probabilities
$$P_0=\frac{|3|^2}{|3|^2+|4i|^2}=\frac{9}{25}=0.36,\qquad
P_1=\frac{|4i|^2}{25}=\frac{16}{25}=0.64,$$
with $P_0+P_1=1$ (Axiom A2 = normalization $\langle\psi|\psi\rangle$) and each
$P_i\ge 0$ (Axiom A1). An *equal* superposition $(1,1,1,1)$ instead gives the
uniform $P_i=1/4$ — the equally-likely measure of §7. *Check:*
`born_probabilities([3.0, 4.0j])` $=[0.36, 0.64]$ summing to $1.0$;
`born_probabilities([1,1,1,1])` $=[0.25,0.25,0.25,0.25]$.

**Solution.** The Born rule weights each outcome by $|\psi_i|^2$ and normalizes by $Z=\sum_j|\psi_j|^2=\langle\psi|\psi\rangle$. For $\psi=(3,\,4i)$ the moduli are $|3|^2=9$ and $|4i|^2=16$ (the phase $i$ drops out of $|\cdot|$), so $Z=25$ and
$$P_0=\frac{9}{25}=0.36,\qquad P_1=\frac{16}{25}=0.64,\qquad P_0+P_1=1.$$
Each $P_i\ge0$ is Axiom A1 and the sum-to-one is Axiom A2 — Kolmogorov's axioms applied to an amplitude vector. An equal superposition $(1,1,1,1)$ has $Z=4$ and every $P_i=1/4$, the equally-likely measure of §7. This matches `born_probabilities([3.0, 4.0j])`$=[0.36, 0.64]$ and `born_probabilities([1,1,1,1])`$=[0.25,0.25,0.25,0.25]$.
