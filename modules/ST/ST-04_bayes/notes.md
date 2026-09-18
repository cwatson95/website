# ST-04 — Bayes' Theorem (notes)

Conditional probability (`~ST-03`) asks: *given* $A$, how likely is $B$? Bayes'
theorem asks the **inverse** question — given that $B$ happened, how likely was each
possible *cause* $A_i$? — and answers it by combining what we believed before (the
**prior**) with how well each cause explains the data (the **likelihood**). This is
the engine of all inference: diagnostic testing, spam filtering, particle-physics
hypothesis ranking, and the Bayesian view of quantum measurement all run the one
update rule derived below.

Citation key (full details + granularity in `refs.md`): **PSU L6** = Penn State
STAT 414, Lesson 6 *Bayes' Theorem*; **HTZ** = Hogg, Tanis & Zimmerman, *Probability
and Statistical Inference*, Ch. 1; **WMS** = Wackerly–Mendenhall–Scheaffer, Ch. 2;
**Ross** = Ross, *A First Course in Probability*, Ch. 3. Cited at **lesson/chapter
level** (this trunk has no PDF shelf — see `refs.md`).

## 1. Partitions and the law of total probability

A collection $\{A_1,A_2,\dots,A_k\}$ is a **partition** of the sample space $S$ when
the cells are pairwise disjoint and cover everything [PSU L6; HTZ §1.5]:
$$A_i\cap A_j=\varnothing\ (i\neq j),\qquad \bigcup_{i=1}^k A_i=S.$$
Then *exactly one* $A_i$ occurs on every outcome. Any event $B$ is carved by the
partition into disjoint pieces $B=\bigcup_i (B\cap A_i)$, so by countable additivity
(`~ST-01`) and the **multiplication rule** $P(B\cap A_i)=P(A_i)\,P(B\mid A_i)$ of
`~ST-03`,
$$\boxed{\,P(B)=\sum_{i=1}^k P(B\cap A_i)=\sum_{i=1}^k P(B\mid A_i)\,P(A_i)\,}$$
the **law of total probability**. It is a **weighted average** of the conditional
probabilities $P(B\mid A_i)$ with the **priors** $P(A_i)$ as weights, so $P(B)$
always lies between the smallest and largest likelihood. Code: the per-cell joints
$P(A_i\cap B)$ are `joint_probabilities(priors, likelihoods)`; their sum is
`total_probability(priors, likelihoods)`. The simplest partition is a single event
and its complement, $\{A,A^c\}$:
$$P(B)=P(B\mid A)\,P(A)+P(B\mid A^c)\,P(A^c),$$
the two-row case that powers the disease screen of §3.

## 2. Bayes' theorem: posterior ∝ prior × likelihood

We want the **reverse** conditional $P(A_i\mid B)$. By the definition of
conditional probability twice (`~ST-03`), $P(A_i\mid B)\,P(B)=P(A_i\cap B)
=P(B\mid A_i)\,P(A_i)$. Dividing by $P(B)$ and expanding it with the law of total
probability of §1 gives **Bayes' theorem** [PSU L6; HTZ §1.6; Ross §3.3]:
$$\boxed{\,P(A_i\mid B)=\frac{P(B\mid A_i)\,P(A_i)}{P(B)}
=\frac{P(B\mid A_i)\,P(A_i)}{\sum_{j} P(B\mid A_j)\,P(A_j)}\,}$$
Read the three pieces:
$$\underbrace{P(A_i\mid B)}_{\text{posterior}}
=\frac{\overbrace{P(B\mid A_i)}^{\text{likelihood}}\;\overbrace{P(A_i)}^{\text{prior}}}
{\underbrace{P(B)}_{\text{evidence}}}\;\propto\;\text{prior}\times\text{likelihood}.$$
The evidence $P(B)$ is just the constant that makes the posterior probabilities sum
to $1$ over the partition, so it **cancels** in any ratio of two hypotheses (§4) and
need not be computed to *compare* them — only to *normalize*. Code:
`bayes_posterior(priors, likelihoods)` returns the whole posterior vector
$P(A_i\mid B)$, computing $P(A_i)\,P(B\mid A_i)$ and dividing by its sum; the test
`test_posterior_proportional_to_prior_times_likelihood` checks that posterior ratios
equal joint ratios (the proportionality) and that the posterior is exactly
joint/evidence. With a **flat prior** $P(A_i)=1/k$ the posterior is the *normalized
likelihood* alone (`test_uniform_prior_gives_normalized_likelihood`) — the precise
sense in which Bayes reduces to maximum likelihood when you bring no prior knowledge.

## 3. The disease screen and the base-rate effect

Take the partition $\{D,H\}$ = diseased / healthy with prior $P(D)=\pi$ (the
**prevalence** or **base rate**). A test has two quoted accuracies [PSU L6]:
$$\text{sensitivity } se=P(+\mid D),\qquad \text{specificity } sp=P(-\mid H),$$
hence the error rates $P(+\mid H)=1-sp$ (false positive) and $P(-\mid D)=1-se$
(false negative). The quantity a patient actually wants is the **positive
predictive value** $P(D\mid +)$, which Bayes delivers:
$$\boxed{\,\mathrm{PPV}=P(D\mid +)=\frac{se\,\pi}{se\,\pi+(1-sp)(1-\pi)}\,}$$
the denominator being $P(+)$ from the law of total probability. Code:
`ppv(prevalence, sensitivity, specificity)`; the test
`test_ppv_matches_bayes_and_total_probability` verifies
$\mathrm{PPV}=\texttt{bayes\_posterior}([\pi,1-\pi],[se,1-sp])[0]
= se\,\pi/\texttt{total\_probability}(\dots)$. The **negative predictive value** is
the mirror image,
$$\mathrm{NPV}=P(H\mid -)=\frac{sp(1-\pi)}{sp(1-\pi)+(1-se)\pi},$$
code `npv(...)`. The lesson is the **base-rate effect**: with $se=sp=0.99$ but a
rare disease $\pi=0.001$,
$$\mathrm{PPV}=\frac{0.99\cdot 0.001}{0.99\cdot 0.001+0.01\cdot 0.999}
=\frac{0.00099}{0.01098}\approx 0.090,$$
so **91% of positives are false alarms** even though the test is 99% accurate —
because the $0.01\times 0.999$ healthy false positives swamp the $0.99\times 0.001$
true positives. Ignoring the prior $P(A_i)$ and reading $P(D\mid +)$ off the
likelihood $P(+\mid D)$ is the **base-rate fallacy**. The demo's prevalence sweep
shows PPV climbing $0.0098\to 0.090\to 0.50\to 0.917$ as $\pi$ goes
$10^{-4}\to10^{-3}\to10^{-2}\to10^{-1}$ (PPV $=\tfrac12$ exactly when $\pi=1-sp$).

## 4. The odds form: Bayes is multiplication

Write Bayes for two hypotheses ($A_1$ vs $A_2$) and divide; the evidence $P(B)$
cancels [PSU L6; HTZ §1.6]:
$$\frac{P(A_1\mid B)}{P(A_2\mid B)}
=\underbrace{\frac{P(A_1)}{P(A_2)}}_{\text{prior odds}}\times
\underbrace{\frac{P(B\mid A_1)}{P(B\mid A_2)}}_{\text{likelihood ratio (Bayes factor)}}.$$
So in **odds** ($o=p/(1-p)$, inverse $p=o/(1+o)$) Bayes is simply
$$\boxed{\,\text{posterior odds}=\text{prior odds}\times \text{likelihood ratio}\,}$$
Code: `prob_to_odds`, `odds_to_prob` (mutually inverse — checked in
`test_odds_form_equals_ppv`), and `posterior_odds(prior_odds, lr)`. For the disease
screen the **diagnostic likelihood ratios** are
$$LR^+=\frac{P(+\mid D)}{P(+\mid H)}=\frac{se}{1-sp},\qquad
LR^-=\frac{P(-\mid D)}{P(-\mid H)}=\frac{1-se}{sp},$$
code `lr_positive`, `lr_negative`; an *informative* test has $LR^+>1>LR^-$. Then
$$P(D\mid +)=\texttt{odds\_to\_prob}\big(\texttt{prob\_to\_odds}(\pi)\cdot LR^+\big)
=\mathrm{PPV},$$
exactly (`test_odds_form_equals_ppv`). For $\pi=10^{-3}$, $se=sp=0.99$: prior odds
$\approx 0.001$, $LR^+=99$, posterior odds $\approx 0.099\Rightarrow P\approx 0.090$.
Because odds **multiply**, $\log$-odds **add** — each independent datum contributes
an additive "weight of evidence" $\log LR$, the bridge to §5.

## 5. Sequential updating: today's posterior is tomorrow's prior

Bayes is **recursive**. After observing $B_1$ the posterior $P(A_i\mid B_1)$ is a
complete description of belief; feed it back in as the *prior* for the next
observation $B_2$. If $B_1,B_2$ are **conditionally independent given each $A_i$**,
$P(B_1\cap B_2\mid A_i)=P(B_1\mid A_i)P(B_2\mid A_i)$, then [PSU L6; HTZ §1.6]
$$P(A_i\mid B_1\cap B_2)\;\propto\;P(A_i)\,P(B_1\mid A_i)\,P(B_2\mid A_i),$$
which is **order-independent** (multiplication commutes) and equals one update
against the product likelihood. In odds: posterior odds $=$ prior odds $\times
LR_1\times LR_2$. Code: `sequential_update(priors, likelihoods, observations)`
returns the trajectory $[\,\text{prior},\,\text{posterior}_1,\,\text{posterior}_2,
\dots]$. For the rare disease, two independent positives give
$$\text{odds}=\frac{\pi}{1-\pi}(LR^+)^2=0.001\cdot 99^2\approx 9.81
\;\Rightarrow\;P\approx 0.908,$$
so $P(D)$ marches $0.001\to 0.090\to 0.908$ — the base rate is **overturned by
accumulating evidence** (`test_sequential_base_rate_overturned_by_repeated_positives`
checks the monotone rise, the $(LR^+)^2$ identity, and order-independence). The
modeling caveat is the conditional-independence assumption: correlated repeat tests
(same lab error, same biological confounder) reuse evidence and overstate the
update.

## 6. Continuous Bayes: the Beta–Binomial conjugate update

Replace the discrete partition by a **continuous parameter** $\theta\in[0,1]$ — say
a coin's bias. The prior is now a *density* $\pi(\theta)$ and the sums become
integrals; the **continuous law of total probability** is the evidence
$$P(\text{data})=\int_0^1 \pi(\theta)\,\mathcal L(\theta)\,d\theta,
\qquad \pi(\theta\mid\text{data})=\frac{\pi(\theta)\,\mathcal L(\theta)}{P(\text{data})}.$$
Take a **Beta prior** $\pi(\theta)=\mathrm{Beta}(a,b)=\theta^{a-1}(1-\theta)^{b-1}/
B(a,b)$ (`beta_pdf`, with $B(a,b)=\Gamma(a)\Gamma(b)/\Gamma(a+b)$ from `~MA-19`) and
a **binomial likelihood** $\mathcal L(\theta)=\binom{n}{k}\theta^k(1-\theta)^{n-k}$
(`binomial_likelihood`, the $\binom{n}{k}$ from `~ST-02`). Multiplying,
$$\pi(\theta\mid k,n)\;\propto\;\theta^{a-1}(1-\theta)^{b-1}\cdot\theta^k(1-\theta)^{n-k}
=\theta^{(a+k)-1}(1-\theta)^{(b+n-k)-1},$$
which is **again a Beta** — the Beta family is **conjugate** to the binomial:
$$\boxed{\,\mathrm{Beta}(a,b)\xrightarrow{\;k\text{ heads},\,n-k\text{ tails}\;}
\mathrm{Beta}(a+k,\,b+n-k)\,}$$
code `posterior_beta_binomial`. The normalizer falls out of the Beta integral
$\int_0^1\theta^{\alpha-1}(1-\theta)^{\beta-1}d\theta=B(\alpha,\beta)$, giving the
closed-form **evidence**
$$P(k\mid n)=\binom{n}{k}\frac{B(a+k,\,b+n-k)}{B(a,b)}$$
(`evidence_beta_binomial`), the **Beta–Binomial** marginal. The test
`test_continuous_evidence_integral_matches_closed_form` confirms this equals the
midpoint-integrated $\int_0^1\pi(\theta)\mathcal L(\theta)\,d\theta$ (helper
`_integrate`), and that a *uniform* prior $\mathrm{Beta}(1,1)$ makes every count
$k\in\{0,\dots,n\}$ equally likely a priori, $P(k\mid n)=1/(n+1)$. The **posterior
mean** $\tfrac{a+k}{a+b+n}$ (`beta_mean`) sits strictly between the prior mean
$\tfrac{a}{a+b}$ and the MLE $k/n$ — Bayesian **shrinkage** (e.g. uniform prior, $8$
heads in $10$: mean $9/12=0.75$, between $0.5$ and $0.8$;
`test_posterior_mean_shrinks_mle_toward_prior`). STAT 414 keeps this discrete, but
the identity *posterior ∝ prior × likelihood* is exactly the same machine.

## Where this goes

- `~ST-03` (conditional probability, the multiplication rule, independence) — the
  three lines Bayes is assembled from; this module is its capstone.
- `~ST-01`/`~ST-02` (axioms, partitions, counting) — the additivity and the
  $\binom{n}{k}$ behind the law of total probability and the binomial likelihood.
- `~MA-19` (binomial pmf, beta/gamma functions) and forward to `~ST-07` (binomial),
  `~ST-09` (Poisson), `~ST-11` (gamma) — the likelihoods you update on; the
  Beta–Binomial of §6 is the conjugate seed of Bayesian parameter estimation.
- `~SM-01` (statistical ensembles) — a posterior is a probability distribution over
  hypotheses, i.e. an ensemble; updating is conditioning the ensemble on data.
- `~QM-02` (the Born rule / quantum measurement) — $|\langle a\mid\psi\rangle|^2$ is
  physics' likelihood $P(\text{outcome }a\mid\text{state})$, and "collapse" given a
  measurement is a Bayes-style update of the state's description.
