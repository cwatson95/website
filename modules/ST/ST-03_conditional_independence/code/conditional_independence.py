"""ST-03  Conditional probability & independence -- the multiplication rule,
the chain rule, independence, pairwise vs mutual, conditioning as a measure.

Probability theory trunk, module ST-03 (Penn State STAT 414, Lessons 4-5).
Source: STAT 414 OER  https://online.stat.psu.edu/stat414  (L4 Conditional
Probability, L5 Independent Events).  Builds on ST-01 (the axioms) and ST-02
(counting); the natural sequel is ST-04 (Bayes' theorem).

Conditioning on an event B that has happened *rescales* the probability of A by
how much of A lives inside B:

    P(A | B) = P(A ∩ B) / P(B),         P(B) > 0.

Rearranged this is the **multiplication rule** P(A ∩ B) = P(B) P(A|B), which
iterates into the **chain rule** for an ordered intersection.  Two events are
**independent** when conditioning changes nothing, P(A|B) = P(A), equivalently
P(A ∩ B) = P(A) P(B).  For three or more events independence comes in two
strengths -- *pairwise* (every pair factors) and *mutual* (every sub-collection
factors); the two are not the same.  Finally, for fixed B the map A |-> P(A|B)
is itself a bona-fide probability measure: it satisfies the ST-01 axioms.

Pure Python standard library only (math, itertools).  No numpy/scipy.
"""

import itertools
import math

__all__ = [
    # finite probability spaces
    "normalize", "prob", "prob_inter", "prob_union", "is_probability_measure",
    # conditional probability
    "conditional", "conditional_event", "conditional_measure",
    # multiplication / chain rule
    "multiplication_rule", "chain_rule", "chain_rule_factors",
    # independence
    "independent_check", "independent_events", "conditional_equals_marginal",
    "pairwise_independent", "mutually_independent",
    "conditionally_independent_check",
    # continuous illustrations
    "exponential_pdf", "exponential_survival", "memoryless_conditional",
    "uniform_square_joint", "prob_rect",
    # demo spaces
    "two_coin_space", "two_card_deck",
]


# --- finite probability spaces (ST-01 foundations) ---------------------------
#
# A *probability measure* is a dict mapping each outcome of a finite sample
# space Omega to its probability; an *event* is any iterable of outcomes
# (a subset of Omega).  P(A) is the sum of the outcome probabilities in A.

def normalize(weights):
    """Turn nonnegative weights {outcome: w} into a probability measure summing
    to 1:  P({o}) = w(o) / sum_o w(o)."""
    total = math.fsum(weights.values())
    if total <= 0.0:
        raise ValueError("weights must have positive total")
    return {o: w / total for o, w in weights.items()}


def prob(measure, event):
    """Probability of an event A under a measure:  P(A) = sum_{o in A} P({o})."""
    return math.fsum(measure[o] for o in event)


def prob_inter(measure, A, B):
    """Probability of the intersection  P(A ∩ B)."""
    return prob(measure, set(A) & set(B))


def prob_union(measure, A, B):
    """Probability of the union  P(A ∪ B) = P(A) + P(B) - P(A ∩ B)  (ST-01)."""
    return prob(measure, set(A) | set(B))


def is_probability_measure(measure, tol=1e-12):
    """Check Kolmogorov's axioms (ST-01): nonnegativity P({o}) >= 0 and
    normalization sum_o P({o}) = 1.  (Additivity is automatic for a finite
    sum-over-outcomes definition of P.)"""
    if any(p < -tol for p in measure.values()):
        return False
    return abs(math.fsum(measure.values()) - 1.0) <= tol


# --- conditional probability (STAT 414 L4) -----------------------------------

def conditional(p_ab, p_b):
    """Conditional probability  P(A | B) = P(A ∩ B) / P(B),  P(B) > 0."""
    if p_b <= 0.0:
        raise ZeroDivisionError("P(B) = 0: conditioning undefined")
    return p_ab / p_b


def conditional_event(measure, A, B):
    """P(A | B) read straight off a finite measure:
        P(A | B) = P(A ∩ B) / P(B)."""
    return conditional(prob_inter(measure, A, B), prob(measure, B))


def conditional_measure(measure, B):
    """The conditional probability measure  Q(·) = P(· | B).  Restrict to B and
    renormalize by P(B); this Q is itself a valid probability measure on Omega
    (STAT 414 L4):  Q({o}) = P({o})/P(B) for o in B, else 0."""
    pB = prob(measure, B)
    if pB <= 0.0:
        raise ZeroDivisionError("P(B) = 0: conditioning undefined")
    Bset = set(B)
    return {o: (p / pB if o in Bset else 0.0) for o, p in measure.items()}


# --- the multiplication and chain rules (STAT 414 L4) ------------------------

def multiplication_rule(p_b, p_a_given_b):
    """Multiplication rule  P(A ∩ B) = P(B) · P(A | B)  (conditional, rearranged)."""
    return p_b * p_a_given_b


def chain_rule(factors):
    """Chain (general multiplication) rule: the joint probability of an ordered
    intersection is the product of successive conditionals,
        P(A1 ∩ … ∩ An) = P(A1) P(A2|A1) P(A3|A1∩A2) … P(An | A1∩…∩A_{n-1}).
    Here `factors` is that list [P(A1), P(A2|A1), …]; returns their product."""
    p = 1.0
    for f in factors:
        p *= f
    return p


def chain_rule_factors(measure, events):
    """Build the chain-rule factors [P(A1), P(A2|A1), …, P(An|A1∩…∩A_{n-1})]
    from a finite measure and an *ordered* list of events.  Their product equals
    P(A1 ∩ … ∩ An)."""
    factors = []
    prefix = None
    for i, A in enumerate(events):
        if i == 0:
            factors.append(prob(measure, A))
            prefix = set(A)
        else:
            p_prefix = prob(measure, prefix)
            inter = prefix & set(A)
            factors.append(prob(measure, inter) / p_prefix)
            prefix = inter
    return factors


# --- independence (STAT 414 L5) ----------------------------------------------

def independent_check(pa, pb, pab, tol=1e-12):
    """Definition of independence: A ⟂ B  ⇔  P(A ∩ B) = P(A) P(B).
    Returns True iff the product rule holds to tolerance."""
    return abs(pab - pa * pb) <= tol


def independent_events(measure, A, B, tol=1e-12):
    """A ⟂ B for events of a finite measure:  P(A ∩ B) = P(A) P(B)."""
    return independent_check(prob(measure, A), prob(measure, B),
                             prob_inter(measure, A, B), tol)


def conditional_equals_marginal(measure, A, B, tol=1e-12):
    """The equivalent form of independence (STAT 414 L5): when P(B) > 0,
        A ⟂ B  ⇔  P(A | B) = P(A).
    Returns True iff the conditional equals the marginal."""
    return abs(conditional_event(measure, A, B) - prob(measure, A)) <= tol


def pairwise_independent(measure, events, tol=1e-12):
    """Pairwise independence: every *pair* factors,
        P(Ai ∩ Aj) = P(Ai) P(Aj)  for all i < j."""
    for i, j in itertools.combinations(range(len(events)), 2):
        if not independent_check(prob(measure, events[i]), prob(measure, events[j]),
                                 prob_inter(measure, events[i], events[j]), tol):
            return False
    return True


def mutually_independent(measure, events, tol=1e-12):
    """Mutual (complete) independence: *every* sub-collection of size >= 2
    factors,  P(∩_{i in S} Ai) = ∏_{i in S} P(Ai)  for all |S| >= 2.
    Stronger than pairwise."""
    n = len(events)
    for k in range(2, n + 1):
        for S in itertools.combinations(range(n), k):
            inter = set(events[S[0]])
            prod = 1.0
            for idx in S:
                inter &= set(events[idx])
                prod *= prob(measure, events[idx])
            if abs(prob(measure, inter) - prod) > tol:
                return False
    return True


def conditionally_independent_check(measure, A, B, C, tol=1e-12):
    """Conditional independence of A and B given C (P(C) > 0):
        P(A ∩ B | C) = P(A | C) P(B | C).
    Independence *inside* the conditional world Q(·) = P(·|C)."""
    pC = prob(measure, C)
    if pC <= 0.0:
        raise ZeroDivisionError("P(C) = 0: conditioning undefined")
    p_ab_c = prob(measure, set(A) & set(B) & set(C)) / pC
    p_a_c = prob_inter(measure, A, C) / pC
    p_b_c = prob_inter(measure, B, C) / pC
    return abs(p_ab_c - p_a_c * p_b_c) <= tol


# --- continuous illustrations ------------------------------------------------
#
# Conditional probability and independence are identical for continuous models;
# two clean examples (full theory in ST-10/ST-11/ST-13).

def _integrate(f, a, b, n=20000):
    """Midpoint-rule numerical integral of f on [a, b] (for continuous checks)."""
    dx = (b - a) / n
    return math.fsum(f(a + (i + 0.5) * dx) * dx for i in range(n))


def _integrate2(f, ax, bx, ay, by, nx=400, ny=400):
    """Midpoint-rule double integral of f(x, y) over [ax,bx] × [ay,by]."""
    dx = (bx - ax) / nx
    dy = (by - ay) / ny
    total = 0.0
    for i in range(nx):
        x = ax + (i + 0.5) * dx
        total += math.fsum(f(x, ay + (j + 0.5) * dy) for j in range(ny))
    return total * dx * dy


def exponential_pdf(x, rate):
    """Exponential density  f(x) = rate · e^{-rate x},  x >= 0  (rate = 1/mean)."""
    return rate * math.exp(-rate * x) if x >= 0.0 else 0.0


def exponential_survival(t, rate):
    """Survival (tail) probability  P(T > t) = ∫_t^∞ rate e^{-rate s} ds
    = e^{-rate t}  for t >= 0."""
    return math.exp(-rate * t) if t >= 0.0 else 1.0


def memoryless_conditional(s, t, rate):
    """Memorylessness as a conditional probability (the exponential is the only
    continuous law with it):
        P(T > s + t | T > s) = P(T > s+t) / P(T > s) = e^{-rate t} = P(T > t)."""
    return conditional(exponential_survival(s + t, rate), exponential_survival(s, rate))


def uniform_square_joint(x, y):
    """Joint density of two *independent* Uniform(0,1) variables:
        f(x, y) = f_X(x) f_Y(y) = 1 on the unit square, 0 outside."""
    return 1.0 if (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0) else 0.0


def prob_rect(joint, ax, bx, ay, by):
    """P(ax < X < bx, ay < Y < by) = ∫∫ joint(x, y) dx dy over the rectangle."""
    return _integrate2(joint, ax, bx, ay, by)


# --- demonstration sample spaces ---------------------------------------------

def two_coin_space():
    """Two fair coin tosses.  Returns (measure, A, B, C) with
        A = first toss heads, B = second toss heads, C = the two tosses agree.
    A, B, C are pairwise independent but NOT mutually independent."""
    outs = [("H", "H"), ("H", "T"), ("T", "H"), ("T", "T")]
    measure = normalize({o: 1.0 for o in outs})
    A = frozenset([("H", "H"), ("H", "T")])   # first toss heads
    B = frozenset([("H", "H"), ("T", "H")])   # second toss heads
    C = frozenset([("H", "H"), ("T", "T")])   # the tosses agree
    return measure, A, B, C


def two_card_deck():
    """Ordered draw of two distinct cards from a 52-card deck (no replacement).
    Outcome = (first, second) with first != second, uniform.  Card 0..51,
    rank = card % 13, so the four aces are the cards with rank 0.
    Returns (measure, first_ace, second_ace)."""
    cards = range(52)
    outs = [(i, j) for i in cards for j in cards if i != j]
    measure = normalize({o: 1.0 for o in outs})
    aces = {c for c in cards if c % 13 == 0}
    first_ace = frozenset(o for o in outs if o[0] in aces)
    second_ace = frozenset(o for o in outs if o[1] in aces)
    return measure, first_ace, second_ace


# --- demo --------------------------------------------------------------------

def _demo():
    print("ST-03 conditional probability & independence -- demo")
    print("=" * 56)

    # two-coin space -----------------------------------------------------------
    measure, A, B, C = two_coin_space()
    print("Two fair coins  Omega = {HH, HT, TH, TT}:")
    print(f"  P(A)=P(first H)              = {prob(measure, A):.3f}")
    print(f"  P(B)=P(second H)             = {prob(measure, B):.3f}")
    print(f"  P(A ∩ B)                     = {prob_inter(measure, A, B):.3f}")
    print(f"  P(A | B)                     = {conditional_event(measure, A, B):.3f}"
          f"  (= P(A): independent)")
    print(f"  A ⟂ B  via product rule      = {independent_events(measure, A, B)}")
    print(f"  P(A|B) == P(A)               = {conditional_equals_marginal(measure, A, B)}")

    # pairwise vs mutual -------------------------------------------------------
    print("\nPairwise vs mutual (A=first H, B=second H, C=tosses agree):")
    print(f"  pairwise independent         = {pairwise_independent(measure, [A, B, C])}")
    print(f"  mutually  independent        = {mutually_independent(measure, [A, B, C])}")
    p_abc = prob(measure, set(A) & set(B) & set(C))
    print(f"  P(A∩B∩C)={p_abc:.3f}  vs  P(A)P(B)P(C)="
          f"{prob(measure, A) * prob(measure, B) * prob(measure, C):.3f}  (differ!)")

    # conditioning is a probability measure ------------------------------------
    Q = conditional_measure(measure, B)
    print("\nConditional measure Q(·)=P(·|B) is itself a probability measure:")
    print(f"  sum_o Q({{o}}) = {math.fsum(Q.values()):.3f},  axioms hold = "
          f"{is_probability_measure(Q)}")

    # two-card chain rule ------------------------------------------------------
    deck, first_ace, second_ace = two_card_deck()
    facts = chain_rule_factors(deck, [first_ace, second_ace])
    print("\nTwo cards, no replacement -- chain rule for P(both aces):")
    print(f"  factors P(A1), P(A2|A1)      = {facts[0]:.4f}, {facts[1]:.4f}"
          f"  (= 4/52, 3/51)")
    print(f"  chain rule product           = {chain_rule(facts):.6f}")
    print(f"  direct  P(A1 ∩ A2)           = {prob_inter(deck, first_ace, second_ace):.6f}"
          f"  (= 1/221 = {1/221:.6f})")

    # continuous: exponential memorylessness -----------------------------------
    rate, s, t = 0.7, 2.0, 3.0
    print("\nContinuous -- exponential memorylessness (a conditional identity):")
    print(f"  P(T>s+t | T>s)               = {memoryless_conditional(s, t, rate):.6f}")
    print(f"  P(T>t)                       = {exponential_survival(t, rate):.6f}  (equal)")

    # continuous: independence by factorization --------------------------------
    a, b = 0.6, 0.4
    joint = prob_rect(uniform_square_joint, 0.0, a, 0.0, b)
    print("\nContinuous -- independent Uniform(0,1) X, Y:")
    print(f"  P(X<{a}, Y<{b}) (2-D integral) = {joint:.4f}  vs  P(X<{a})P(Y<{b}) = {a*b:.4f}")


if __name__ == "__main__":
    _demo()
