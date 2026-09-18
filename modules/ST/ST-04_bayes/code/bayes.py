"""ST-04  Bayes' theorem -- partitions, total probability, posterior updating.

Probability-theory trunk, module ST-04 (a faithful replica of Penn State STAT 414,
Lesson 6 "Bayes' Theorem").  Builds directly on ~ST-03 (conditional probability and
the multiplication rule P(A and B) = P(A) P(B|A)) and on ~MA-19 (the binomial pmf
and the beta/gamma functions used for the continuous conjugate update below).

Source: STAT 414, https://online.stat.psu.edu/stat414/, Lesson 6 "Bayes' Theorem"
(law of total probability + Bayes' rule + the medical-test example).  Follows Hogg,
Tanis & Zimmerman, *Probability and Statistical Inference*, Ch. 1.

------------------------------------------------------------------------------
The idea, in one screen
------------------------------------------------------------------------------
Let {A_1, ..., A_k} PARTITION the sample space: the A_i are mutually exclusive and
their union is everything, so exactly one occurs.  The LAW OF TOTAL PROBABILITY
slices any event B through the partition,

    P(B) = SUM_i P(B | A_i) P(A_i)                                   (total_probability)

-- a weighted average of the conditional probabilities, weights = the priors P(A_i).
BAYES' THEOREM reverses the conditioning by dividing one term of that sum by the
whole sum:

    P(A_i | B) = P(B | A_i) P(A_i) / SUM_j P(B | A_j) P(A_j)         (bayes_posterior)
               = likelihood x prior / evidence,

i.e. POSTERIOR is proportional to PRIOR x LIKELIHOOD, renormalized by the evidence
P(B).  The classic shock is the disease screen: a 99%-accurate test for a disease of
prevalence 0.1% gives a positive predictive value P(disease | +) of only ~9% -- the
BASE-RATE EFFECT (ppv).  Two independent positives push it past 90% (sequential_update).

In ODDS form Bayes is multiplicative -- posterior odds = prior odds x likelihood
ratio -- so log-odds simply ADD up evidence (posterior_odds, lr_positive).  The same
identity, with the sum replaced by an integral, runs continuous parameter estimation:
a Beta(a,b) prior on a coin's bias theta, updated by k heads in n flips, yields a
Beta(a+k, b+n-k) posterior, with evidence = INT prior(theta) likelihood(theta) dtheta
(posterior_beta_binomial, evidence_beta_binomial) -- the continuous law of total
probability.
"""

import math

import numpy as np

__all__ = [
    "total_probability", "joint_probabilities", "bayes_posterior",
    "ppv", "npv",
    "prob_to_odds", "odds_to_prob",
    "lr_positive", "lr_negative", "posterior_odds",
    "sequential_update",
    "beta_pdf", "binomial_likelihood",
    "posterior_beta_binomial", "evidence_beta_binomial", "beta_mean",
]


# =============================================================================
# 0. numerical integrator (for the continuous-update checks)
# =============================================================================

def _integrate(f, a, b, n=20000):
    """Midpoint-rule integral of f on [a, b] with n panels (continuous checks)."""
    h = (b - a) / n
    return sum(f(a + (i + 0.5) * h) * h for i in range(n))


# =============================================================================
# 1. Law of total probability  (STAT 414 L6; ~ST-03 multiplication rule)
# =============================================================================
# A partition {A_i} carries priors P(A_i); the likelihoods P(B|A_i) say how B looks
# under each cell.  The joint P(A_i and B) = P(A_i) P(B|A_i) is the multiplication
# rule of ~ST-03; summing the joints over the partition marginalizes out which A_i
# occurred and leaves P(B).

def joint_probabilities(priors, likelihoods):
    """Joint P(A_i and B) = P(A_i) P(B | A_i)  (the multiplication rule, ~ST-03)."""
    return np.asarray(priors, dtype=float) * np.asarray(likelihoods, dtype=float)


def total_probability(priors, likelihoods):
    """Law of total probability  P(B) = SUM_i P(B|A_i) P(A_i)  (STAT 414 L6).

    `priors` are the partition weights P(A_i) (should sum to 1); `likelihoods` are
    the conditional probabilities P(B|A_i).  Returns the marginal P(B) = the sum of
    the joint probabilities -- the evidence that normalizes Bayes' theorem."""
    return float(np.sum(joint_probabilities(priors, likelihoods)))


# =============================================================================
# 2. Bayes' theorem: posterior ~ prior x likelihood  (STAT 414 L6)
# =============================================================================

def bayes_posterior(priors, likelihoods, observed=None):
    """Bayes' theorem  P(A_i|B) = P(B|A_i)P(A_i) / SUM_j P(B|A_j)P(A_j)  (STAT 414 L6).

    `priors` = P(A_i).  `likelihoods` is either
      * a 1-D vector P(B|A_i) of the likelihood of the single observed event B, or
      * a 2-D matrix L[i, j] = P(outcome_j | A_i); then `observed` selects column j.
    Returns the full posterior vector P(A_i|B) -- prior x likelihood, renormalized by
    the evidence P(B) (`total_probability`).  Raises if the evidence is 0."""
    p = np.asarray(priors, dtype=float)
    L = np.asarray(likelihoods, dtype=float)
    lik = L[:, observed] if L.ndim == 2 else L
    joint = p * lik
    Z = float(np.sum(joint))
    if Z <= 0.0:
        raise ValueError("evidence P(B) = 0: the data are impossible under the prior")
    return joint / Z


# =============================================================================
# 3. The medical-test problem: predictive values and the base-rate effect
# =============================================================================
# Partition = {disease D, healthy H}, priors {prevalence, 1-prevalence}.
# A test has SENSITIVITY  P(+|D)  and SPECIFICITY  P(-|H); hence the off-diagonals
# P(+|H) = 1-specificity (false positive) and P(-|D) = 1-sensitivity (false negative).
# Bayes turns test accuracy into the PREDICTIVE VALUE a patient actually cares about.

def ppv(prevalence, sensitivity, specificity):
    """Positive predictive value  P(D|+) = se*pi / (se*pi + (1-sp)*(1-pi))  (STAT 414 L6).

    pi = prevalence, se = sensitivity = P(+|D), sp = specificity = P(-|H).  Equals
    bayes_posterior([pi, 1-pi], [se, 1-sp])[0].  For a rare disease this is small even
    for an accurate test -- the BASE-RATE EFFECT."""
    num = sensitivity * prevalence
    return num / (num + (1.0 - specificity) * (1.0 - prevalence))


def npv(prevalence, sensitivity, specificity):
    """Negative predictive value  P(H|-) = sp*(1-pi) / (sp*(1-pi) + (1-se)*pi).

    Equals bayes_posterior([pi, 1-pi], [1-se, sp])[1]: probability of being healthy
    given a negative test."""
    num = specificity * (1.0 - prevalence)
    return num / (num + (1.0 - sensitivity) * prevalence)


# =============================================================================
# 4. Odds form: posterior odds = prior odds x likelihood ratio
# =============================================================================
# Dividing Bayes for two hypotheses cancels the evidence P(B):
#     P(A1|B)/P(A2|B) = [P(A1)/P(A2)] x [P(B|A1)/P(B|A2)].
# Odds make Bayes MULTIPLICATIVE, so independent evidence multiplies (log-odds add).

def prob_to_odds(p):
    """Probability -> odds  o = p / (1 - p)."""
    return p / (1.0 - p)


def odds_to_prob(o):
    """Odds -> probability  p = o / (1 + o)  (inverse of prob_to_odds)."""
    return o / (1.0 + o)


def lr_positive(sensitivity, specificity):
    """Likelihood ratio of a positive test  LR+ = P(+|D)/P(+|H) = se/(1-sp)."""
    return sensitivity / (1.0 - specificity)


def lr_negative(sensitivity, specificity):
    """Likelihood ratio of a negative test  LR- = P(-|D)/P(-|H) = (1-se)/sp."""
    return (1.0 - sensitivity) / specificity


def posterior_odds(prior_odds, likelihood_ratio):
    """Posterior odds = prior odds x likelihood ratio  (the odds form of Bayes)."""
    return prior_odds * likelihood_ratio


# =============================================================================
# 5. Sequential updating: yesterday's posterior is today's prior
# =============================================================================
# Bayes applied repeatedly: feed the posterior of one observation back in as the
# prior for the next.  For conditionally INDEPENDENT observations the result is
# order-independent and equals one update against the product of likelihoods --
# which is why a few repeated positive tests overwhelm a tiny base rate.

def sequential_update(priors, likelihoods, observations):
    """Repeated Bayes updates over a sequence of observations  (STAT 414 L6).

    `likelihoods` is the 2-D matrix L[i, j] = P(outcome_j | A_i); `observations` is a
    list of observed column indices j_1, j_2, ....  Returns the array of posteriors
    [prior, after obs1, after obs2, ...] (shape (len(observations)+1, k)); each row is
    the prior for the next step.  Demonstrates the base-rate effect being overturned
    by accumulating evidence."""
    p = np.asarray(priors, dtype=float)
    history = [p.copy()]
    for obs in observations:
        p = bayes_posterior(p, likelihoods, obs)
        history.append(p)
    return np.array(history)


# =============================================================================
# 6. Continuous Bayes: the Beta-Binomial conjugate update  (~MA-19)
# =============================================================================
# Replace the discrete partition by a continuous parameter theta in [0,1] (a coin's
# bias).  Prior density pi(theta) = Beta(a,b); likelihood of k heads in n flips is the
# binomial C(n,k) theta^k (1-theta)^(n-k).  The posterior is again Beta -- conjugacy --
# and the EVIDENCE is the continuous law of total probability INT pi(theta) L(theta) d theta.

def _beta_fn(a, b):
    """Beta function  B(a,b) = Gamma(a) Gamma(b) / Gamma(a+b)  (math.gamma)."""
    return math.gamma(a) * math.gamma(b) / math.gamma(a + b)


def beta_pdf(theta, a, b):
    """Beta(a,b) density  theta^(a-1) (1-theta)^(b-1) / B(a,b)  on [0,1]  (~MA-19)."""
    t = np.asarray(theta, dtype=float)
    out = t ** (a - 1.0) * (1.0 - t) ** (b - 1.0) / _beta_fn(a, b)
    return float(out) if np.ndim(out) == 0 else out


def binomial_likelihood(theta, k, n):
    """Binomial likelihood  P(k heads in n | theta) = C(n,k) theta^k (1-theta)^(n-k)."""
    t = np.asarray(theta, dtype=float)
    out = math.comb(n, k) * t ** k * (1.0 - t) ** (n - k)
    return float(out) if np.ndim(out) == 0 else out


def posterior_beta_binomial(a, b, k, n):
    """Conjugate update: Beta(a,b) prior + (k heads, n-k tails)  ->  Beta(a+k, b+n-k).
    Returns the posterior (a', b')."""
    return (a + k, b + n - k)


def evidence_beta_binomial(a, b, k, n):
    """Marginal likelihood (evidence)  P(k|n) = INT Beta(a,b)(theta) Binom(k,n|theta) d theta
    = C(n,k) B(a+k, b+n-k) / B(a,b)  -- the continuous law of total probability."""
    return math.comb(n, k) * _beta_fn(a + k, b + n - k) / _beta_fn(a, b)


def beta_mean(a, b):
    """Mean of Beta(a,b):  a / (a+b).  The posterior mean shrinks the MLE toward the prior."""
    return a / (a + b)


# =============================================================================
# demo
# =============================================================================

def _demo():
    print("ST-04  Bayes' theorem  (STAT 414 Lesson 6)")
    print("=" * 60)

    # 1) law of total probability through a partition
    priors = [0.5, 0.3, 0.2]            # three factories' share of output
    defect = [0.01, 0.02, 0.03]         # P(defective | factory_i)
    PB = total_probability(priors, defect)
    print("\n1) Law of total probability  P(B) = SUM P(B|A_i) P(A_i)")
    print("   priors      :", priors)
    print("   likelihoods :", defect)
    print("   P(defective) = %.4f" % PB)
    post = bayes_posterior(priors, defect)
    print("   posterior P(factory_i | defective) =", np.round(post, 4),
          " (sums to %.3f)" % post.sum())

    # 2) the disease screen and the base-rate effect
    print("\n2) Disease screen: PPV vs prevalence  (test se = sp = 0.99)")
    se, sp = 0.99, 0.99
    for pi in (1e-4, 1e-3, 1e-2, 1e-1):
        print("   prevalence = %7.4f  ->  P(disease|+) = %.4f" % (pi, ppv(pi, se, sp)))
    print("   -> a near-perfect test is mostly false alarms when the disease is rare.")

    # 3) odds form: posterior odds = prior odds x likelihood ratio
    pi = 1e-3
    o_post = posterior_odds(prob_to_odds(pi), lr_positive(se, sp))
    print("\n3) Odds form (pi = 1e-3):  LR+ = %.1f," % lr_positive(se, sp),
          "prior odds = %.5f" % prob_to_odds(pi))
    print("   posterior odds = %.4f  ->  P = %.4f  ( = PPV %.4f)"
          % (o_post, odds_to_prob(o_post), ppv(pi, se, sp)))

    # 4) sequential updating overturns the base rate
    L = np.array([[1 - se, se],         # row 0 = disease : P(-|D), P(+|D)
                  [sp, 1 - sp]])        # row 1 = healthy : P(-|H), P(+|H)
    hist = sequential_update([pi, 1 - pi], L, [1, 1])   # two positive tests
    print("\n4) Sequential updating, two independent positive tests (pi = 1e-3)")
    print("   P(disease) :  %.4f  ->  %.4f  ->  %.4f"
          % (hist[0, 0], hist[1, 0], hist[2, 0]))
    print("   -> repeated evidence multiplies in odds space: 9% -> 91%.")

    # 5) continuous Bayes: Beta-Binomial conjugate update (~MA-19)
    a, b, k, n = 1.0, 1.0, 8, 10        # uniform prior, observe 8 heads in 10
    ap, bp = posterior_beta_binomial(a, b, k, n)
    ev = evidence_beta_binomial(a, b, k, n)
    ev_num = _integrate(lambda t: beta_pdf(t, a, b) * binomial_likelihood(t, k, n), 0.0, 1.0)
    print("\n5) Continuous Bayes: Beta(%g,%g) prior, %d heads in %d  (~MA-19)" % (a, b, k, n))
    print("   posterior = Beta(%g, %g)" % (ap, bp))
    print("   evidence P(8|10) = %.6f  (closed form)   = %.6f  (numerical integral)"
          % (ev, ev_num))
    print("   posterior mean = %.4f  (MLE k/n = %.3f, pulled toward prior 0.5)"
          % (beta_mean(ap, bp), k / n))


if __name__ == "__main__":
    _demo()
