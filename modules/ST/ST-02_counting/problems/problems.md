# ST-02 — Problems

Work each by hand, then check with `code/counting.py`. Citations in `../refs.md`;
**PSU** = STAT 414 Lesson 3. Throughout, "draw $k$ from $n$" is classified by
**ordered/unordered** and **with/without replacement**, and the equally-likely
model of `~ST-01` turns each count into a probability $P=N(A)/N(S)$.

### P1.  The four sampling schemes  *(PSU L3.1–L3.2)*
A jar holds $n=5$ distinct tokens; draw $k=3$. Count the outcomes when the draw is
(a) ordered with replacement, (b) ordered without replacement, (c) unordered
without replacement, (d) unordered with replacement. Show these are $n^k$,
$P(n,k)=n!/(n-k)!$, $\binom{n}{k}$, and $\binom{n+k-1}{k}$, and explain the strict
ordering $\binom{n}{k}\le P(n,k)\le n^k$ (removing order divides by $k!$; removing
replacement removes the repeated draws). Then count the license plates of 2 letters
followed by 3 digits (ordered, with replacement, mixed alphabets):
$26^2\cdot10^3$. *Check:* `ordered_with_replacement(5,3)`$=125$,
`permutations(5,3)`$=60$, `combinations(5,3)`$=10$,
`combinations_with_replacement(5,3)`$=35$; `multiplication_principle([26,26,10,10,10])`$=676000$.

**Solution.** With $n=5,\ k=3$: (a) each of the $3$ slots can be any of the $5$ tokens, $n^k=5^3=125$; (b) drawing without reuse, $5\cdot4\cdot3=60=P(5,3)$; (c) each unordered triple is counted $3!$ times among those ordered draws, so $\binom53=60/3!=10$; (d) unordered *with* replacement is stars-and-bars, $\binom{n+k-1}{k}=\binom73=35$. The chain $\binom nk\le P(n,k)\le n^k$ reads $10\le60\le125$ — removing order divides by $k!$, while allowing replacement adds the repeated-token draws. License plates multiply independent slots, $26^2\cdot10^3=676000$. This matches `ordered_with_replacement(5,3)`$=125$, `permutations(5,3)`$=60$, `combinations(5,3)`$=10$, `combinations_with_replacement(5,3)`$=35$, and `multiplication_principle([26,26,10,10,10])`$=676000$.

### P2.  Permutations: ordered roles  *(PSU L3.2)*
Ten sprinters race; gold, silver, and bronze medals are awarded. How many distinct
podiums are possible? This is an **ordered** selection of $k=3$ from $n=10$ without
replacement, $P(10,3)=10\cdot9\cdot8=10!/7!$. Verify the "choose then order"
identity $P(n,k)=\binom{n}{k}\,k!$ by counting the same podium as: pick the 3
medalists ($\binom{10}{3}$ ways), then order them on the podium ($3!$ ways).
*Check:* `permutations(10,3)`$=720$ and `combinations(10,3)*factorial(3)`
$=120\cdot6=720$.

**Solution.** A podium is an ordered choice of $3$ from $10$ without replacement, so by the multiplication principle the gold, silver, and bronze slots fill in $10\cdot9\cdot8=720=10!/7!$ ways. Counting the same podiums "choose then order" — pick the $3$ medalists in $\binom{10}{3}=120$ ways, then arrange them across the three distinct medals in $3!=6$ ways — gives the identity
$$P(n,k)=\binom{n}{k}\,k!\ \Longrightarrow\ P(10,3)=120\cdot6=720.$$
This matches `permutations(10,3)`$=720$ and `combinations(10,3)*factorial(3)`$=120\cdot6=720$.

### P3.  Combinations and symmetry  *(PSU L3.2)*
(a) How many 5-card hands can be dealt from a 52-card deck? Order is irrelevant, no
replacement: $\binom{52}{5}$. (b) A committee of 3 is chosen from 12 people; show
that choosing the 3 members ($\binom{12}{3}$) equals choosing the 9 non-members
($\binom{12}{9}$) — the symmetry $\binom{n}{k}=\binom{n}{n-k}$. *Check:*
`combinations(52,5)`$=2598960$; `combinations(12,3)`$=$`combinations(12,9)`$=220$.

**Solution.** (a) A hand is an unordered choice of $5$ from $52$ without replacement, $\binom{52}{5}=\frac{52!}{5!\,47!}=2{,}598{,}960$. (b) Choosing the $3$ committee members is the very same act as choosing the $9$ people left off it — a bijection between $3$-subsets and their complements — so
$$\binom{12}{3}=\binom{12}{9}=220,$$
the symmetry $\binom nk=\binom{n}{n-k}$, visible because $\frac{n!}{k!(n-k)!}$ is unchanged under $k\leftrightarrow n-k$. This matches `combinations(52,5)`$=2598960$ and `combinations(12,3)`$=$`combinations(12,9)`$=220$.

### P4.  Stars and bars: distributing identical items  *(PSU L3.2; WMS Ch.2)*
Ten **identical** candies are handed out to 4 children. (a) If a child may receive
none, count the distributions: non-negative solutions of $x_1+x_2+x_3+x_4=10$,
which is $\binom{10+4-1}{4-1}=\binom{13}{3}$. (b) If **every** child must get at
least one, give one to each first and distribute the remaining $6$ freely:
$\binom{6+4-1}{4-1}=\binom{9}{3}$. Note this count is exactly the
`~SM-01` Einstein-solid multiplicity $\Omega=\binom{q+N-1}{q}$ with $q=10$ quanta,
$N=4$ oscillators. *Check:* `stars_and_bars(10,4)`$=286$ and `stars_and_bars(6,4)`$=84$.

**Solution.** (a) Lay the $10$ identical candies in a row and insert $4-1=3$ dividers to split them among the four children; choosing the divider positions among the $10+3$ symbols gives
$$\binom{10+4-1}{4-1}=\binom{13}{3}=286$$
non-negative solutions of $x_1+x_2+x_3+x_4=10$. (b) If every child must get one, hand out four candies first, then distribute the remaining $6$ freely, $\binom{6+4-1}{3}=\binom93=84$. This is exactly the Einstein-solid multiplicity $\Omega=\binom{q+N-1}{q}$ with $q=10,\ N=4$ (here $\binom{13}{10}=\binom{13}{3}$). This matches `stars_and_bars(10,4)`$=286$ and `stars_and_bars(6,4)`$=84$.

### P5.  Multinomial: arrangements with repeated letters  *(PSU L3.2; Ross Ch.1)*
Count the distinguishable arrangements of the letters of **MISSISSIPPI** (1 M, 4 I,
4 S, 2 P, total 11): of the $11!$ orderings of distinct tiles, those permuting like
letters coincide, an overcount of $1!\,4!\,4!\,2!$, giving $\binom{11}{1,4,4,2}=
11!/(1!\,4!\,4!\,2!)$. Do the same for **STATISTICS** (3 S, 3 T, 1 A, 2 I, 1 C,
total 10). Recall this multinomial coefficient is the statistical multiplicity $W$
of `~SM-01`. *Check:* `multinomial(11,[1,4,4,2])`$=34650$ and
`multinomial(10,[3,3,1,2,1])`$=50400$.

**Solution.** Treating the $11$ tiles of **MISSISSIPPI** as distinct gives $11!$ orderings, but permuting the identical letters among themselves ($1$ M, $4$ I, $4$ S, $2$ P) never changes the word, an overcount of $1!\,4!\,4!\,2!$:
$$\binom{11}{1,4,4,2}=\frac{11!}{1!\,4!\,4!\,2!}=\frac{39{,}916{,}800}{1\cdot24\cdot24\cdot2}=34{,}650.$$
The same multinomial count for **STATISTICS** ($3$ S, $3$ T, $1$ A, $2$ I, $1$ C) is $\frac{10!}{3!\,3!\,1!\,2!\,1!}=\frac{3{,}628{,}800}{6\cdot6\cdot2}=50{,}400$ — the statistical multiplicity $W$ of ~SM-01. This matches `multinomial(11,[1,4,4,2])`$=34650$ and `multinomial(10,[3,3,1,2,1])`$=50400$.

### P6.  Pascal, the binomial theorem, and the `~ST-07` normalization  *(PSU L3.2; Ross Ch.1)*
(a) Build row 6 of Pascal's triangle by the rule $\binom{6}{k}=\binom{5}{k-1}+
\binom{5}{k}$ and confirm the row sums to $2^6$ (the number of subsets of a 6-set,
from $(1+1)^6$); confirm the alternating sum is $0$. (b) Specialize the binomial
theorem to $x=p,\,y=1-p$ to show $\sum_{k=0}^{n}\binom{n}{k}p^k(1-p)^{n-k}=1$ — this
**is** the normalization of the binomial pmf of `~ST-07`, with $\binom{n}{k}$
counting the orderings of $k$ successes in $n$ trials. *Check:*
`binomial_coefficient_sum(6)`$=64$, `binomial_coefficient_sum(6, signed=True)`$=0$,
`binomial_coefficient_sum(10)`$=1024$; `binomial_theorem_check(0.3,0.7,6)[0]`$=1.0$.

**Solution.** (a) Pascal's rule $\binom6k=\binom5{k-1}+\binom5k$ turns row $5=[1,5,10,10,5,1]$ into row $6=[1,6,15,20,15,6,1]$. Setting $x=y=1$ in $(x+y)^6=\sum_k\binom6k x^ky^{6-k}$ sums the row to $2^6=64$ (the number of subsets of a $6$-set); setting $x=1,\,y=-1$ gives the alternating sum $(1-1)^6=0$. (b) Specializing $x=p,\ y=1-p$,
$$\sum_{k=0}^{n}\binom{n}{k}p^k(1-p)^{n-k}=\big(p+(1-p)\big)^n=1,$$
which *is* the normalization of the binomial pmf of ~ST-07, with $\binom nk$ counting the orderings of $k$ successes among $n$ trials. This matches `binomial_coefficient_sum(6)`$=64$, `binomial_coefficient_sum(6, signed=True)`$=0$, `binomial_coefficient_sum(10)`$=1024$, and `binomial_theorem_check(0.3,0.7,6)[0]`$=1.0$.

### P7.  The continuous shadow: the Beta–Gamma bridge  *(PSU L3.2; cf. `~ST-11`)*
The discrete $\binom{n}{k}$ has a continuous counterpart through the Beta integral
$$\int_0^1 x^{k}(1-x)^{\,n-k}\,dx=\frac{k!\,(n-k)!}{(n+1)!}=\frac{1}{(n+1)\binom{n}{k}}.$$
Take $n=5,\ k=2$: predict $1/[(6)\binom{5}{2}]=1/60$, then integrate numerically.
Separately confirm the factorial is the Gamma integral $\Gamma(6)=\int_0^\infty t^5
e^{-t}dt=5!$. *Check:* `beta_integral(2,5)`$=1/60\approx0.0166667$ and
`_integrate(lambda x: x**2*(1-x)**3, 0, 1)`$\approx0.0166667$;
`_integrate(lambda t: t**5*exp(-t), 0, 60)`$\approx120=$`factorial(5)`.

**Solution.** The Beta integral evaluates through the Gamma function, using $\Gamma(m+1)=m!$:
$$\int_0^1 x^{k}(1-x)^{\,n-k}\,dx=\frac{\Gamma(k+1)\,\Gamma(n-k+1)}{\Gamma(n+2)}=\frac{k!\,(n-k)!}{(n+1)!}=\frac{1}{(n+1)\binom{n}{k}}.$$
For $n=5,\ k=2$, $\binom52=10$ gives $\frac{1}{6\cdot10}=\frac1{60}\approx0.0166667$. Separately the factorial *is* a Gamma integral, $\Gamma(6)=\int_0^\infty t^5e^{-t}\,dt=5!=120$ (repeated integration by parts — the recursion $\Gamma(z+1)=z\,\Gamma(z)$). This matches `beta_integral(2,5)`$=1/60\approx0.0166667$, the numerical `_integrate(lambda x: x**2*(1-x)**3, 0, 1)`$\approx0.0166667$, and `_integrate(lambda t: t**5*exp(-t), 0, 60)`$\approx120=$`factorial(5)`.
