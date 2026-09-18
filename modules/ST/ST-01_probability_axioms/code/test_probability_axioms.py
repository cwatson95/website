"""Tests for ST-01 sample spaces & the axioms of probability.

Each test asserts a real theorem of the Kolmogorov axioms -- inclusion-exclusion
against brute-force counts on explicit dice/card sample spaces, De Morgan's laws
on finite sets, the continuous addition rule by integration, and Born-rule
normalization (~QM-02) -- not tautologies.

Run:  python3 test_probability_axioms.py     ->  "All N tests passed."
"""
import math

from probability_axioms import (
    is_valid_probability, prob_empty, prob_sure, complement, prob_equally_likely,
    union_disjoint, union_two, intersection_from_union, prob_difference,
    union_three, inclusion_exclusion, boole_bound, monotone, complement_set,
    product_sample_space, event_probability, standard_deck, uniform_pdf,
    prob_continuous, born_probabilities,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _integrate(f, a, b, n=20000):
    h = (b - a) / n
    return math.fsum(f(a + (i + 0.5) * h) * h for i in range(n))


# explicit sample spaces reused across tests
DICE = product_sample_space(range(1, 7), repeat=2)   # |S| = 36
DECK = standard_deck()                                # |S| = 52


def test_axioms_and_complement():
    # Axiom A1/A2 range, and the boundary cases
    assert is_valid_probability(0.0) and is_valid_probability(1.0)
    assert is_valid_probability(0.37)
    assert not is_valid_probability(-0.01)
    assert not is_valid_probability(1.5)
    # P(empty)=0, P(S)=1
    assert _approx(prob_empty(), 0.0)
    assert _approx(prob_sure(), 1.0)
    # complement rule and its involution P((A^c)^c) = P(A)
    assert _approx(complement(0.3), 0.7)
    assert _approx(complement(complement(0.3)), 0.3)
    # complement is consistent with S = A u A^c being disjoint and summing to 1
    assert _approx(union_disjoint(0.3, complement(0.3)), 1.0)


def test_equally_likely_dice_and_cards():
    # two dice, six ways to make 7  ->  6/36 = 1/6
    assert _approx(event_probability(DICE, lambda w: sum(w) == 7), 1.0 / 6.0)
    assert _approx(event_probability(DICE, lambda w: sum(w) == 11), 2.0 / 36.0)
    # one suit out of four
    assert _approx(prob_equally_likely(13, 52), 0.25)
    # red cards (hearts + diamonds) = 26/52 = 1/2
    assert _approx(event_probability(DECK, lambda c: c[1] in ("hearts", "diamonds")), 0.5)
    # total over a partition of S is 1 (Axiom A2 via equally-likely counts)
    suits = ("clubs", "diamonds", "hearts", "spades")
    assert _approx(union_disjoint(*[event_probability(DECK, lambda c, s=s: c[1] == s)
                                    for s in suits]), 1.0)


def test_addition_rule_two_events():
    pa, pb, pab = 0.5, 0.4, 0.2
    pu = union_two(pa, pb, pab)
    assert _approx(pu, 0.7)
    assert is_valid_probability(pu)
    # disjoint case reduces to plain additivity (Axiom A3)
    assert _approx(union_two(0.3, 0.45, 0.0), union_disjoint(0.3, 0.45))
    # inverting the addition rule recovers the intersection
    assert _approx(intersection_from_union(pa, pb, pu), pab)
    # set difference  P(A\B) = P(A) - P(A n B);  and P(A) = P(A\B) + P(A n B)
    assert _approx(prob_difference(pa, pab), 0.3)
    assert _approx(prob_difference(pa, pab) + pab, pa)


def test_addition_rule_matches_brute_force_on_cards():
    # heart OR face card, computed by the addition rule and by direct counting
    p_heart = event_probability(DECK, lambda c: c[1] == "hearts")
    p_face = event_probability(DECK, lambda c: c[0] in ("J", "Q", "K"))
    p_both = event_probability(DECK, lambda c: c[1] == "hearts" and c[0] in ("J", "Q", "K"))
    p_rule = union_two(p_heart, p_face, p_both)
    p_brute = event_probability(DECK, lambda c: c[1] == "hearts" or c[0] in ("J", "Q", "K"))
    assert _approx(p_rule, p_brute)
    assert _approx(p_rule, 22.0 / 52.0)   # 13 + 12 - 3 = 22


def test_inclusion_exclusion_three_vs_brute():
    A = lambda w: w[0] % 2 == 0
    B = lambda w: sum(w) >= 8
    C = lambda w: w[1] == 3
    pa = event_probability(DICE, A)
    pb = event_probability(DICE, B)
    pc = event_probability(DICE, C)
    pab = event_probability(DICE, lambda w: A(w) and B(w))
    pac = event_probability(DICE, lambda w: A(w) and C(w))
    pbc = event_probability(DICE, lambda w: B(w) and C(w))
    pabc = event_probability(DICE, lambda w: A(w) and B(w) and C(w))
    ie = union_three(pa, pb, pc, pab, pac, pbc, pabc)
    brute = event_probability(DICE, lambda w: A(w) or B(w) or C(w))
    assert _approx(ie, brute)
    # the generic inclusion_exclusion must agree with the hand-rolled 3-set form
    ie_gen = inclusion_exclusion([pa, pb, pc], [pab, pac, pbc], [pabc])
    assert _approx(ie_gen, ie)
    # Boole's inequality: the union never exceeds the sum of the marginals
    assert brute <= boole_bound([pa, pb, pc]) + 1e-12


def test_inclusion_exclusion_four_vs_brute():
    # four events on the dice space; check the full S1 - S2 + S3 - S4 law
    preds = [
        lambda w: w[0] <= 3,          # first die small
        lambda w: w[1] <= 3,          # second die small
        lambda w: sum(w) % 2 == 0,    # even sum
        lambda w: w[0] == w[1],       # doubles
    ]
    P = lambda f: event_probability(DICE, f)
    singles = [P(p) for p in preds]
    pairs, triples = [], []
    n = len(preds)
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append(P(lambda w, i=i, j=j: preds[i](w) and preds[j](w)))
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                triples.append(P(lambda w, i=i, j=j, k=k:
                                 preds[i](w) and preds[j](w) and preds[k](w)))
    quad = P(lambda w: all(p(w) for p in preds))
    ie = inclusion_exclusion(singles, pairs, triples, quad)
    brute = P(lambda w: any(p(w) for p in preds))
    assert _approx(ie, brute)


def test_de_morgan_on_finite_sets():
    S = set(DICE)
    A = {w for w in DICE if w[0] % 2 == 0}
    B = {w for w in DICE if sum(w) >= 8}
    # (A u B)^c = A^c n B^c   and   (A n B)^c = A^c u B^c
    assert complement_set(S, A | B) == complement_set(S, A) & complement_set(S, B)
    assert complement_set(S, A & B) == complement_set(S, A) | complement_set(S, B)
    # the complement of an event has the complementary probability
    assert _approx(event_probability(DICE, lambda w: w in complement_set(S, A)),
                   complement(event_probability(DICE, lambda w: w in A)))


def test_monotonicity():
    # A = {sum = 12} is a subset of B = {sum >= 10}, so P(A) <= P(B)
    pa = event_probability(DICE, lambda w: sum(w) == 12)
    pb = event_probability(DICE, lambda w: sum(w) >= 10)
    assert monotone(pa, pb)
    assert pa <= pb
    # P(B) - P(A) = P(B \ A) >= 0 (the difference of a nested pair)
    assert prob_difference(pb, pa) >= 0.0


def test_continuous_axioms_by_integration():
    f = lambda x: uniform_pdf(x, 0.0, 1.0)
    # total mass = 1 (Axiom A2, continuous version)
    assert _approx(_integrate(f, 0.0, 1.0), 1.0, tol=1e-6)
    # addition rule on two overlapping intervals I1=[0.2,0.6], I2=[0.4,0.8]
    p1 = prob_continuous(f, 0.2, 0.6)         # 0.4
    p2 = prob_continuous(f, 0.4, 0.8)         # 0.4
    p_int = prob_continuous(f, 0.4, 0.6)      # overlap 0.2
    p_union = prob_continuous(f, 0.2, 0.8)    # 0.6
    assert _approx(union_two(p1, p2, p_int), p_union, tol=1e-6)
    # complement: P([0,1] \ [0.3,0.7]) = 1 - 0.4
    assert _approx(1.0 - prob_continuous(f, 0.3, 0.7), 0.6, tol=1e-6)


def test_born_rule_normalization():
    # equal 4-state superposition -> uniform 1/4 each (~QM-02)
    probs = born_probabilities([1.0, 1.0, 1.0, 1.0])
    assert _approx(math.fsum(probs), 1.0)              # Axiom A2 = <psi|psi>
    for p in probs:
        assert is_valid_probability(p)                 # Axiom A1
        assert _approx(p, 0.25)
    # a non-uniform (complex) state still normalizes; |3|^2 : |4i|^2 = 9 : 16
    probs2 = born_probabilities([3.0, 4.0j])
    assert _approx(math.fsum(probs2), 1.0)
    assert _approx(probs2[0], 9.0 / 25.0)
    assert _approx(probs2[1], 16.0 / 25.0)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
