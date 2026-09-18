"""Tests for ST-04 Bayes' theorem.  Pure numpy + stdlib; self-contained.

Run:  python3 test_bayes.py     ->  "All N tests passed."
"""
import math

import numpy as np

from bayes import (
    _integrate, total_probability, joint_probabilities, bayes_posterior,
    ppv, npv, prob_to_odds, odds_to_prob, lr_positive, lr_negative,
    posterior_odds, sequential_update,
    beta_pdf, binomial_likelihood, posterior_beta_binomial,
    evidence_beta_binomial, beta_mean,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


# disease-screen parameters reused across tests
PI, SE, SP = 1e-3, 0.99, 0.99


def test_total_probability_is_weighted_average():
    priors = [0.5, 0.3, 0.2]
    lik = [0.01, 0.02, 0.03]
    PB = total_probability(priors, lik)
    # explicit sum of the joints P(A_i) P(B|A_i)
    assert _approx(PB, 0.5 * 0.01 + 0.3 * 0.02 + 0.2 * 0.03)
    # equals the dot product of the two vectors
    assert _approx(PB, float(np.dot(priors, lik)))
    # the joints sum to the marginal
    assert _approx(float(np.sum(joint_probabilities(priors, lik))), PB)
    # a weighted average lies between the min and max likelihood
    assert min(lik) <= PB <= max(lik)


def test_posterior_is_normalized_probability():
    priors = [0.5, 0.3, 0.2]
    lik = [0.01, 0.02, 0.03]
    post = bayes_posterior(priors, lik)
    assert _approx(float(np.sum(post)), 1.0)
    assert np.all(post >= 0.0)


def test_posterior_proportional_to_prior_times_likelihood():
    priors = np.array([0.5, 0.3, 0.2])
    lik = np.array([0.01, 0.02, 0.03])
    post = bayes_posterior(priors, lik)
    joint = priors * lik
    # posterior_i / posterior_j == joint_i / joint_j  (the proportionality, evidence cancels)
    assert _approx(post[0] / post[2], joint[0] / joint[2])
    assert _approx(post[1] / post[0], joint[1] / joint[0])
    # and posterior = joint / evidence exactly
    assert np.allclose(post, joint / total_probability(priors, lik))


def test_uniform_prior_gives_normalized_likelihood():
    # with a flat prior the posterior is just the likelihood, renormalized
    lik = np.array([0.2, 0.5, 0.9, 0.4])
    post = bayes_posterior(np.ones(4) / 4.0, lik)
    assert np.allclose(post, lik / lik.sum())


def test_ppv_matches_bayes_and_total_probability():
    # PPV as a Bayes posterior over {disease, healthy} given a positive test
    p_bayes = bayes_posterior([PI, 1 - PI], [SE, 1 - SP])[0]
    assert _approx(ppv(PI, SE, SP), p_bayes)
    # PPV = (se * prevalence) / P(+)  with P(+) the law of total probability
    P_pos = total_probability([PI, 1 - PI], [SE, 1 - SP])
    assert _approx(ppv(PI, SE, SP), SE * PI / P_pos)
    # the famous base-rate effect: a 99% test, 0.1% disease -> PPV well under 10%
    assert ppv(PI, SE, SP) < 0.10


def test_npv_matches_bayes():
    p_bayes = bayes_posterior([PI, 1 - PI], [1 - SE, SP])[1]
    assert _approx(npv(PI, SE, SP), p_bayes)
    # a negative result on a rare, accurate-test disease is almost surely a true negative
    assert npv(PI, SE, SP) > 0.999


def test_odds_form_equals_ppv():
    # posterior odds = prior odds x LR+  ;  convert back to probability -> PPV
    o_post = posterior_odds(prob_to_odds(PI), lr_positive(SE, SP))
    assert _approx(odds_to_prob(o_post), ppv(PI, SE, SP))
    # prob<->odds are inverse maps
    assert _approx(odds_to_prob(prob_to_odds(0.137)), 0.137)
    # LR+ > 1 > LR- for an informative test
    assert lr_positive(SE, SP) > 1.0 > lr_negative(SE, SP)


def test_sequential_first_step_is_ppv_and_order_independent():
    L = np.array([[1 - SE, SE], [SP, 1 - SP]])     # rows: disease, healthy; cols: -, +
    hist = sequential_update([PI, 1 - PI], L, [1])  # one positive
    assert _approx(hist[1, 0], ppv(PI, SE, SP))
    # Bayes is order-independent for conditionally independent observations:
    # one positive then one negative == one negative then one positive
    h_pn = sequential_update([PI, 1 - PI], L, [1, 0])
    h_np = sequential_update([PI, 1 - PI], L, [0, 1])
    assert np.allclose(h_pn[-1], h_np[-1])


def test_sequential_base_rate_overturned_by_repeated_positives():
    L = np.array([[1 - SE, SE], [SP, 1 - SP]])
    hist = sequential_update([PI, 1 - PI], L, [1, 1, 1])
    pd = hist[:, 0]                      # P(disease) after 0,1,2,3 positives
    # strictly increasing with each positive test
    assert pd[0] < pd[1] < pd[2] < pd[3]
    # two independent positives match the odds-form prediction prior_odds * (LR+)^2
    o2 = prob_to_odds(PI) * lr_positive(SE, SP) ** 2
    assert _approx(pd[2], odds_to_prob(o2))
    # a single positive is unconvincing (<10%) but three are decisive (>99%)
    assert pd[1] < 0.10 and pd[3] > 0.99


def test_beta_pdf_normalized_and_mean():
    # Beta(2,5) integrates to 1 and has mean a/(a+b)
    a, b = 2.0, 5.0
    total = _integrate(lambda t: beta_pdf(t, a, b), 0.0, 1.0)
    assert _approx(total, 1.0, tol=1e-4)
    mean = _integrate(lambda t: t * beta_pdf(t, a, b), 0.0, 1.0)
    assert _approx(mean, beta_mean(a, b), tol=1e-4)
    assert _approx(beta_mean(a, b), a / (a + b))


def test_continuous_evidence_integral_matches_closed_form():
    # evidence = INT prior(theta) likelihood(theta) dtheta  (continuous total probability)
    a, b, k, n = 1.0, 1.0, 8, 10
    ev_int = _integrate(
        lambda t: beta_pdf(t, a, b) * binomial_likelihood(t, k, n), 0.0, 1.0)
    ev_form = evidence_beta_binomial(a, b, k, n)
    assert _approx(ev_int, ev_form, tol=1e-4)
    # uniform prior -> every count 0..n equally likely a priori -> evidence = 1/(n+1)
    assert _approx(ev_form, 1.0 / (n + 1), tol=1e-12)


def test_continuous_posterior_is_prior_times_likelihood_over_evidence():
    # posterior density = prior(theta) likelihood(theta) / evidence, and it is a Beta
    a, b, k, n = 2.0, 2.0, 7, 10
    ap, bp = posterior_beta_binomial(a, b, k, n)
    ev = evidence_beta_binomial(a, b, k, n)
    for t in (0.2, 0.5, 0.8):
        lhs = beta_pdf(t, ap, bp)
        rhs = beta_pdf(t, a, b) * binomial_likelihood(t, k, n) / ev
        assert _approx(lhs, rhs, tol=1e-9)
    # the conjugate posterior integrates to 1
    norm = _integrate(lambda t: beta_pdf(t, ap, bp), 0.0, 1.0)
    assert _approx(norm, 1.0, tol=1e-4)


def test_posterior_mean_shrinks_mle_toward_prior():
    # Beta(1,1) prior (mean 0.5), 8 heads in 10 (MLE 0.8): posterior mean strictly between
    a, b, k, n = 1.0, 1.0, 8, 10
    ap, bp = posterior_beta_binomial(a, b, k, n)
    pm = beta_mean(ap, bp)
    assert beta_mean(a, b) < pm < k / n
    assert _approx(pm, (a + k) / (a + b + n))


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
