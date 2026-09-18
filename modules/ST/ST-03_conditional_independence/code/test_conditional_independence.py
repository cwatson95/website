"""Tests for ST-03 conditional probability & independence.

Asserts the headline analytic identities of STAT 414 L4-L5: the definition of
conditional probability, the multiplication and chain rules, the two equivalent
forms of independence, pairwise != mutual, that conditioning is itself a valid
probability measure, and the continuous memorylessness/factorization identities.

Run:  python3 test_conditional_independence.py     ->  "All N tests passed."
"""
import math

from conditional_independence import (
    normalize, prob, prob_inter, prob_union, is_probability_measure,
    conditional, conditional_event, conditional_measure,
    multiplication_rule, chain_rule, chain_rule_factors,
    independent_check, independent_events, conditional_equals_marginal,
    pairwise_independent, mutually_independent, conditionally_independent_check,
    exponential_pdf, exponential_survival, memoryless_conditional,
    uniform_square_joint, prob_rect, _integrate,
    two_coin_space, two_card_deck,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_conditional_definition():
    # P(A|B) = P(A∩B)/P(B); the two-coin space gives P(A|B) = 1/2.
    measure, A, B, C = two_coin_space()
    assert _approx(conditional(0.25, 0.5), 0.5)
    assert _approx(conditional_event(measure, A, B), 0.5)
    # consistency: conditional_event reproduces conditional() of the raw numbers
    assert _approx(conditional_event(measure, A, B),
                   conditional(prob_inter(measure, A, B), prob(measure, B)))
    # a *dependent* conditional: P(A | A∪C-ish), use C-given-A on the agree event
    # P(C | A) = P(C∩A)/P(A) = P(HH)/P(first H) = 0.25/0.5 = 0.5
    assert _approx(conditional_event(measure, C, A), 0.5)


def test_multiplication_rule_inverts_conditional():
    # P(A∩B) = P(B)·P(A|B): multiplying back recovers the joint.
    measure, A, B, _ = two_coin_space()
    pB = prob(measure, B)
    p_a_given_b = conditional_event(measure, A, B)
    assert _approx(multiplication_rule(pB, p_a_given_b), prob_inter(measure, A, B))
    # symmetric: P(A∩B) = P(A)·P(B|A) too
    pA = prob(measure, A)
    p_b_given_a = conditional_event(measure, B, A)
    assert _approx(multiplication_rule(pA, p_b_given_a), prob_inter(measure, A, B))


def test_chain_rule_two_cards():
    # Two cards without replacement: P(both aces) = (4/52)(3/51) = 1/221.
    deck, first_ace, second_ace = two_card_deck()
    facts = chain_rule_factors(deck, [first_ace, second_ace])
    assert _approx(facts[0], 4 / 52)
    assert _approx(facts[1], 3 / 51)
    assert _approx(chain_rule(facts), 1 / 221)
    # the chain-rule product equals the directly-enumerated intersection
    assert _approx(chain_rule(facts), prob_inter(deck, first_ace, second_ace))
    # draws WITHOUT replacement are dependent: P(A2|A1)=3/51 != P(A2)=4/52
    assert not independent_events(deck, first_ace, second_ace)


def test_chain_rule_matches_intersection():
    # For any ordered events, prod of chain-rule factors = P of the intersection.
    measure, A, B, C = two_coin_space()
    facts = chain_rule_factors(measure, [A, B, C])
    inter = set(A) & set(B) & set(C)
    assert _approx(chain_rule(facts), prob(measure, inter))


def test_independence_two_equivalent_forms():
    # A ⟂ B  <=>  P(A∩B)=P(A)P(B)  <=>  P(A|B)=P(A).  Both forms must agree.
    measure, A, B, C = two_coin_space()
    assert independent_check(0.5, 0.5, 0.25)            # product form
    assert independent_events(measure, A, B)            # from the measure
    assert conditional_equals_marginal(measure, A, B)   # conditional form
    # a dependent pair: in the deck, first/second ace are NOT independent,
    # and the two forms agree on that.
    deck, fa, sa = two_card_deck()
    assert not independent_events(deck, fa, sa)
    assert not conditional_equals_marginal(deck, fa, sa)


def test_pairwise_not_mutual():
    # The classic counterexample: A=first H, B=second H, C=tosses agree are
    # pairwise independent but NOT mutually independent.
    measure, A, B, C = two_coin_space()
    assert pairwise_independent(measure, [A, B, C])
    assert not mutually_independent(measure, [A, B, C])
    # the failure is exactly the triple: P(A∩B∩C)=1/4 != P(A)P(B)P(C)=1/8
    p_abc = prob(measure, set(A) & set(B) & set(C))
    prod = prob(measure, A) * prob(measure, B) * prob(measure, C)
    assert _approx(p_abc, 0.25)
    assert _approx(prod, 0.125)
    assert not _approx(p_abc, prod)
    # an actually-mutually-independent triple: three independent fair bits
    outs = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
    m3 = normalize({o: 1.0 for o in outs})
    Ea = frozenset(o for o in outs if o[0] == 1)
    Eb = frozenset(o for o in outs if o[1] == 1)
    Ec = frozenset(o for o in outs if o[2] == 1)
    assert mutually_independent(m3, [Ea, Eb, Ec])


def test_conditioning_is_a_probability_measure():
    # For fixed B, Q(·)=P(·|B) satisfies the ST-01 axioms.
    measure, A, B, C = two_coin_space()
    Q = conditional_measure(measure, B)
    # nonnegativity + normalization (Kolmogorov)
    assert is_probability_measure(Q)
    assert _approx(math.fsum(Q.values()), 1.0)
    # P(Omega | B) = 1 and P(B | B) = 1
    Omega = list(measure.keys())
    assert _approx(prob(Q, Omega), 1.0)
    assert _approx(prob(Q, B), 1.0)
    # outcomes outside B carry zero conditional mass -> P(B^c | B) = 0
    Bc = [o for o in measure if o not in set(B)]
    assert _approx(prob(Q, Bc), 0.0)
    # finite additivity on disjoint pieces inside B:
    # A∩B and (B minus A) are disjoint and union to B
    AB = set(A) & set(B)
    BmA = set(B) - set(A)
    assert _approx(prob(Q, AB) + prob(Q, BmA), prob(Q, B))
    # Bayes-free sanity: Q(A) = P(A|B) matches conditional_event
    assert _approx(prob(Q, A), conditional_event(measure, A, B))


def test_conditional_independence():
    # Build a space where A,B are conditionally independent given C but the
    # check correctly rejects a dependent construction.
    # Independent given C: inside C, A and B are independent fair bits.
    outs = []
    w = {}
    # outcomes (c, a, b); c in {0,1}; within each c, a and b independent fair
    for c in (0, 1):
        for a in (0, 1):
            for b in (0, 1):
                outs.append((c, a, b))
                w[(c, a, b)] = 1.0
    m = normalize(w)
    C = frozenset(o for o in outs if o[0] == 1)
    A = frozenset(o for o in outs if o[1] == 1)
    B = frozenset(o for o in outs if o[2] == 1)
    assert conditionally_independent_check(m, A, B, C)
    # now make A and B perfectly dependent inside C (a == b there)
    w2 = {o: 1.0 for o in outs if not (o[0] == 1 and o[1] != o[2])}
    m2 = normalize(w2)
    C2 = frozenset(o for o in w2 if o[0] == 1)
    A2 = frozenset(o for o in w2 if o[1] == 1)
    B2 = frozenset(o for o in w2 if o[2] == 1)
    assert not conditionally_independent_check(m2, A2, B2, C2)


def test_union_and_measure_axioms():
    # P(A∪B) = P(A)+P(B)-P(A∩B) (inclusion-exclusion, ST-01), and the base
    # measure itself is valid.
    measure, A, B, C = two_coin_space()
    assert is_probability_measure(measure)
    lhs = prob_union(measure, A, B)
    rhs = prob(measure, A) + prob(measure, B) - prob_inter(measure, A, B)
    assert _approx(lhs, rhs)
    assert _approx(lhs, 0.75)  # P(first H or second H) = 3/4


def test_exponential_memorylessness():
    # P(T>s+t | T>s) = P(T>t) = e^{-rate t}, independent of s.
    rate = 0.7
    for s in (0.0, 1.0, 5.0):
        assert _approx(memoryless_conditional(s, 3.0, rate),
                       exponential_survival(3.0, rate))
    assert _approx(exponential_survival(3.0, rate), math.exp(-rate * 3.0))
    # survival = integral of the density over the tail (continuous check)
    t = 1.5
    tail = _integrate(lambda x: exponential_pdf(x, rate), t, t + 60.0 / rate, n=60000)
    assert _approx(tail, exponential_survival(t, rate), tol=1e-4)
    # the full density integrates to 1
    total = _integrate(lambda x: exponential_pdf(x, rate), 0.0, 80.0 / rate, n=80000)
    assert _approx(total, 1.0, tol=1e-4)


def test_continuous_independence_factorization():
    # Independent Uniform(0,1): P(X<a, Y<b) = a·b = P(X<a)·P(Y<b), and the
    # conditional equals the marginal, P(X<a | Y<b) = a.
    a, b = 0.6, 0.4
    joint = prob_rect(uniform_square_joint, 0.0, a, 0.0, b)
    assert _approx(joint, a * b, tol=1e-4)
    # marginals are the 1-D integrals
    px = _integrate(lambda x: 1.0, 0.0, a)
    py = _integrate(lambda y: 1.0, 0.0, b)
    assert _approx(joint, px * py, tol=1e-4)
    # conditional = marginal (independence): P(X<a|Y<b) = (a·b)/b = a
    assert _approx(conditional(joint, py), a, tol=1e-4)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
