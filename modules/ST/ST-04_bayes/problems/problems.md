# ST-04 — Problems

Work each by hand, then check with `code/bayes.py`. Citations in `../refs.md`;
**PSU L6** = Penn State STAT 414, Lesson 6 *Bayes' Theorem*. Throughout, a
**partition** $\{A_i\}$ carries **priors** $P(A_i)$ and **likelihoods** $P(B\mid A_i)$
of an observed event $B$; Bayes turns the latter around into the **posterior**
$P(A_i\mid B)$ (`~ST-03` is the conditional-probability prerequisite).

### P1.  Law of total probability and the reverse question  *(PSU L6)*
Three factories supply a parts bin: factory 1 makes $50\%$ of the parts, factory 2
makes $30\%$, factory 3 makes $20\%$, with defect rates $1\%$, $2\%$, $3\%$
respectively. (a) Find $P(\text{defective})$ by the law of total probability
$P(B)=\sum_i P(B\mid A_i)P(A_i)$. (b) A part is found defective — which factory most
likely made it? Use $P(A_i\mid B)=P(B\mid A_i)P(A_i)/P(B)$. Note the posterior is
*not* ordered like the defect rates, because factory 1's large share offsets its low
defect rate. *Check:* `total_probability([0.5,0.3,0.2],[0.01,0.02,0.03])` $=0.017$;
`bayes_posterior([0.5,0.3,0.2],[0.01,0.02,0.03])` $=[0.2941,0.3529,0.3529]$ (factories
2 and 3 tie as most likely).

**Solution.** (a) The law of total probability is the share-weighted average of the defect rates:
$$P(B)=\sum_i P(B\mid A_i)P(A_i)=0.5(0.01)+0.3(0.02)+0.2(0.03)=0.005+0.006+0.006=0.017.$$
(b) Bayes divides each joint $P(B\mid A_i)P(A_i)$ by that evidence:
$$P(A_i\mid B)=\frac{[\,0.005,\ 0.006,\ 0.006\,]}{0.017}=[\,0.2941,\ 0.3529,\ 0.3529\,].$$
Although factory $3$ has the highest defect rate, its small output share offsets it, so factories $2$ and $3$ tie as the likeliest source rather than $3$ leading. This matches `total_probability([0.5,0.3,0.2],[0.01,0.02,0.03])`$=0.017$ and `bayes_posterior([0.5,0.3,0.2],[0.01,0.02,0.03])`$=[0.2941,0.3529,0.3529]$.

### P2.  Reversing a draw: which urn?  *(PSU L6; `~ST-03`)*
Urn 1 holds 2 red and 3 blue balls; urn 2 holds 4 red and 1 blue. You pick an urn at
random (prior $\tfrac12,\tfrac12$) and draw a **red** ball. Show
$P(\text{red}\mid U_1)=\tfrac25$, $P(\text{red}\mid U_2)=\tfrac45$, so by total
probability $P(\text{red})=\tfrac12\cdot\tfrac25+\tfrac12\cdot\tfrac45=\tfrac35$, and
by Bayes $P(U_1\mid\text{red})=\dfrac{\tfrac12\cdot\tfrac25}{\tfrac35}=\tfrac13$.
The red draw shifts belief from $\tfrac12$ toward the red-richer urn 2. *Check:*
`total_probability([0.5,0.5],[0.4,0.8])` $=0.6$; `bayes_posterior([0.5,0.5],[0.4,0.8])`
$=[0.3333,0.6667]$.

**Solution.** The likelihoods come straight from each urn: urn $1$ has $2$ red of $5$ so $P(\text{red}\mid U_1)=\tfrac25$, urn $2$ has $4$ red of $5$ so $P(\text{red}\mid U_2)=\tfrac45$. With equal priors the total probability of drawing red is
$$P(\text{red})=\tfrac12\cdot\tfrac25+\tfrac12\cdot\tfrac45=\tfrac15+\tfrac25=\tfrac35,$$
and Bayes reverses the draw:
$$P(U_1\mid\text{red})=\frac{\tfrac12\cdot\tfrac25}{\tfrac35}=\frac{1/5}{3/5}=\tfrac13.$$
The red ball pulls belief from the prior $\tfrac12$ down to $\tfrac13$, i.e. toward the red-richer urn $2$. This matches `total_probability([0.5,0.5],[0.4,0.8])`$=0.6$ and `bayes_posterior([0.5,0.5],[0.4,0.8])`$=[0.3333,0.6667]$.

### P3.  The disease screen and the base-rate effect  *(PSU L6)*
A disease has prevalence $\pi=0.001$. A test has sensitivity $se=P(+\mid D)=0.99$ and
specificity $sp=P(-\mid H)=0.99$. (a) Compute the positive predictive value
$\mathrm{PPV}=P(D\mid +)=\dfrac{se\,\pi}{se\,\pi+(1-sp)(1-\pi)}$ and explain why a
$99\%$-accurate test gives only $\approx 9\%$ — the **base-rate effect**: false
positives from the huge healthy majority swamp the few true positives. (b) Show PPV
$=\tfrac12$ exactly when $\pi=1-sp$ (here $\pi=0.01$). (c) Compute the negative
predictive value and note it is essentially $1$. *Check:* `ppv(0.001,0.99,0.99)`
$=0.0902$; `ppv(0.01,0.99,0.99)` $=0.5$; `npv(0.001,0.99,0.99)` $\approx 0.99999$.

**Solution.** (a) Bayes against the partition $\{D,H\}$ gives the positive predictive value
$$\mathrm{PPV}=\frac{se\,\pi}{se\,\pi+(1-sp)(1-\pi)}=\frac{0.99(0.001)}{0.99(0.001)+0.01(0.999)}=\frac{0.00099}{0.01098}=0.0902.$$
The false-positive mass $(1-sp)(1-\pi)=0.01\cdot0.999\approx0.01$ from the vast healthy majority dwarfs the true-positive mass $se\,\pi\approx0.001$ — the **base-rate effect**. (b) With $se=sp$, $\mathrm{PPV}=\tfrac12$ requires $se\,\pi=(1-sp)(1-\pi)$, i.e. $\pi=1-sp=0.01$. (c) The negative predictive value $\mathrm{NPV}=\frac{sp(1-\pi)}{sp(1-\pi)+(1-se)\pi}\approx0.99999$ — a negative all but clears you. This matches `ppv(0.001,0.99,0.99)`$=0.0902$, `ppv(0.01,0.99,0.99)`$=0.5$, and `npv(0.001,0.99,0.99)`$\approx0.99999$.

### P4.  The odds form: posterior odds = prior odds × LR⁺  *(PSU L6)*
Redo P3 in **odds**. The prior odds of disease are $\pi/(1-\pi)=0.001/0.999\approx
0.001$; the positive likelihood ratio is $LR^+=se/(1-sp)=0.99/0.01=99$. Multiply:
posterior odds $=0.001\times 99\approx 0.099$, hence $P=\dfrac{0.099}{1.099}\approx
0.090$ — the same PPV, with the evidence $P(+)$ never computed because it cancels in
the odds. *Check:* `lr_positive(0.99,0.99)` $=99$;
`odds_to_prob(prob_to_odds(0.001)*lr_positive(0.99,0.99))` $=0.0902$ $=$
`ppv(0.001,0.99,0.99)`.

**Solution.** In odds form Bayes is multiplicative — posterior odds $=$ prior odds $\times LR^+$ — and the evidence $P(+)$ never appears because it cancels between the two hypotheses. The prior odds are $\frac{\pi}{1-\pi}=\frac{0.001}{0.999}\approx0.001001$ and the positive likelihood ratio is $LR^+=\frac{se}{1-sp}=\frac{0.99}{0.01}=99$, so
$$\text{posterior odds}=0.001001\times99\approx0.0991\ \Longrightarrow\ P=\frac{0.0991}{1.0991}\approx0.0902,$$
the very same PPV as P3, reached without ever computing $P(+)$. This matches `lr_positive(0.99,0.99)`$=99$ and `odds_to_prob(prob_to_odds(0.001)*lr_positive(0.99,0.99))`$=0.0902=$`ppv(0.001,0.99,0.99)`.

### P5.  Sequential updating overturns the base rate  *(PSU L6)*
The patient retests. Treating the tests as conditionally independent given disease
status, each positive multiplies the odds by $LR^+=99$. (a) After two positives the
odds are $0.001\times 99^2\approx 9.81$, so $P\approx 0.908$; after three,
$0.001\times 99^3\approx 971$, so $P\approx 0.999$ — accumulating evidence overturns
the tiny prior. (b) Show a positive *then* a negative returns belief to the base
rate, because $LR^+\!\cdot LR^-=\dfrac{se}{1-sp}\cdot\dfrac{1-se}{sp}=1$ here. *Check:*
with `L = np.array([[0.01,0.99],[0.99,0.01]])`,
`sequential_update([0.001,0.999], L, [1,1,1])[:,0]` $=[0.001,0.0902,0.9075,0.999]$;
`sequential_update([0.001,0.999], L, [1,0])[:,0]` $=[0.001,0.0902,0.001]$ (a $+$ and a
$-$ cancel).

**Solution.** (a) Conditionally independent tests each multiply the odds by $LR^+=99$, so $m$ positives give (prior odds)$\times99^m$. Starting from prior odds $\approx0.001$,
$$0.001\times99^2\approx9.81\Rightarrow P=\frac{9.81}{10.81}\approx0.908,\qquad 0.001\times99^3\approx971\Rightarrow P\approx0.999,$$
so accumulating evidence overturns the tiny prior. (b) A positive *then* a negative multiplies the odds by $LR^+\!\cdot LR^-=\frac{se}{1-sp}\cdot\frac{1-se}{sp}=99\cdot\frac{0.01}{0.99}=1$, returning belief exactly to the base rate. This matches `sequential_update([0.001,0.999], L, [1,1,1])[:,0]`$=[0.001,0.0902,0.9075,0.999]$ and `sequential_update([0.001,0.999], L, [1,0])[:,0]`$=[0.001,0.0902,0.001]$.

### P6.  Continuous Bayes: the Beta–Binomial update  *(PSU L6; `~MA-19`)*
A coin of unknown bias $\theta$ gets a **uniform** prior $\mathrm{Beta}(1,1)$. You
flip $8$ heads in $10$. Using conjugacy, the posterior is
$\mathrm{Beta}(1+8,\,1+2)=\mathrm{Beta}(9,3)$, with mean $\tfrac{9}{12}=0.75$ —
between the prior mean $0.5$ and the MLE $\tfrac{8}{10}=0.8$ (Bayesian shrinkage).
The **evidence** $P(8\mid 10)=\int_0^1 1\cdot\binom{10}{8}\theta^8(1-\theta)^2\,d\theta
=\binom{10}{8}B(9,3)=\tfrac{1}{11}$, the uniform-prior result that all $11$ counts
are equally likely a priori. *Check:* `posterior_beta_binomial(1,1,8,10)` $=(9,3)$;
`beta_mean(9,3)` $=0.75$; `evidence_beta_binomial(1,1,8,10)` $=0.090909=\tfrac{1}{11}$
(and equals the midpoint integral of `beta_pdf(t,1,1)*binomial_likelihood(t,8,10)`).

**Solution.** Posterior $\propto$ prior $\times$ likelihood, and since the Beta density and the binomial likelihood are both products of powers of $\theta$ and $1-\theta$, they conjugate:
$$\theta^{a-1}(1-\theta)^{b-1}\cdot\theta^{k}(1-\theta)^{n-k}\ \propto\ \theta^{(a+k)-1}(1-\theta)^{(b+n-k)-1},$$
i.e. $\mathrm{Beta}(1+8,\,1+2)=\mathrm{Beta}(9,3)$, with mean $\frac{9}{9+3}=0.75$ — between the prior mean $0.5$ and the MLE $\tfrac{8}{10}=0.8$ (Bayesian shrinkage). The evidence integrates the likelihood against the flat prior, $P(8\mid10)=\binom{10}{8}B(9,3)=\tfrac{1}{11}$, the uniform-prior statement that all $11$ counts $0,\dots,10$ are a priori equally likely. This matches `posterior_beta_binomial(1,1,8,10)`$=(9,3)$, `beta_mean(9,3)`$=0.75$, and `evidence_beta_binomial(1,1,8,10)`$=0.090909=\tfrac{1}{11}$.

### P7.  How much evidence to cross 50%?  *(PSU L6)*
For the rare disease of P3–P5, find the number $m$ of independent positive tests that
first pushes $P(D)$ above $\tfrac12$, i.e. posterior odds $>1$. Solve $\pi/(1-\pi)
\cdot (LR^+)^m>1$: $m>\dfrac{\ln\!\big((1-\pi)/\pi\big)}{\ln LR^+}=\dfrac{\ln 999}
{\ln 99}\approx 1.50$, so $m=2$ positives are needed (one is not enough). This is the
**weight-of-evidence** view: each positive adds $\log LR^+\approx 4.6$ nats of
log-odds, and you need to overcome $\ln 999\approx 6.9$ of prior skepticism. *Check:*
with `L` as in P5, `sequential_update([0.001,0.999], L, [1,1])[:,0]`
$=[0.001,0.0902,0.9075]$ — below $0.5$ after one positive, above after two.

**Solution.** Each independent positive multiplies the odds by the same $LR^+$, so $m$ positives push $P(D)$ past $\tfrac12$ (posterior odds $>1$) once $\frac{\pi}{1-\pi}(LR^+)^m>1$. Taking logs,
$$m>\frac{\ln\!\frac{1-\pi}{\pi}}{\ln LR^+}=\frac{\ln 999}{\ln 99}=\frac{6.907}{4.595}\approx1.50,$$
so $m=2$ — a single positive is not enough. In log-odds (nats) each positive adds $\ln99\approx4.6$ and must overcome the prior skepticism $\ln999\approx6.9$; two give $9.2>6.9$, one gives only $4.6$. This matches `sequential_update([0.001,0.999], L, [1,1])[:,0]`$=[0.001,0.0902,0.9075]$ — below $0.5$ after one positive, above after two.
